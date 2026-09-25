"""SotA experiment: FASTENER vs. modern feature selectors.

run_experiment.py compares FASTENER against the simple filters (mutual info,
ANOVA-F, tree importance, RFE, random). This script runs the stronger set --
mRMR, ReliefF, Boruta, HSIC Lasso, plain NSGA-II, POSS, FS-SDS and the
NSGAII-MIIP port -- under the identical protocol, so the two runs stack into one
picture. POSS and FS-SDS are the FASTENER paper's own wrapper comparators.

The evolutionary arms are budgeted by MODEL FITS, not generations, because
generations are not comparable across algorithms with different population
sizes. The default matches what FASTENER measured on MADELON in the baseline
run (~6000 fits/seed).

Usage:
    python experiments/run_sota.py --quick              # smoke check
    python experiments/run_sota.py                      # full run, MADELON
    python experiments/run_sota.py --dataset gina
    python experiments/run_sota.py --methods mrmr,boruta --no-fastener
"""
import argparse
import csv
import sys
import traceback
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis  # noqa: E402
import sota_baselines as sota  # noqa: E402
from datasets import DATA_DIR, load  # noqa: E402
from progress import Progress, format_duration  # noqa: E402
from protocol import FitCounter, MODEL_SEED  # noqa: E402
from provenance import Run  # noqa: E402
from run_experiment import K_GRID  # noqa: E402
from run_fastener import SWAP_ARMS, run_fastener  # noqa: E402

# The three FASTENER arms, keyed by swap-strategy name. The method labels match
# what run_fastener stamps on its records, so the plot styles in analysis.py and
# the significance tables pick them up without further mapping.
FASTENER_ARM_NAMES = {
    "none": "fastener",
    "random": "fastener_swap_random",
    "guided": "fastener_swap_guided",
}

# Deterministic selectors: one pass each, no seed.
FILTERS = ("mrmr", "relieff", "hsic_lasso")
# Boruta is a filter in spirit but randomised in fact -- it permutes every
# column to build shadow features and refits a forest each iteration -- so it
# gets the same seed treatment as the searches and reports a spread, not a
# single point that the significance tests would read as a fixed baseline.
SEEDED_FILTERS = ("boruta",)
# Population searches: one run per seed.
SEARCHES = ("nsga2", "poss", "nsgaii_miip")
# FS-SDS fixes the subset size for a whole run, so it needs one run per k and
# its total cost is (budget x len(k_grid)). It is budgeted per run like the
# others -- see run_fs_sds_method -- but it cannot share their accounting, so
# it is planned and reported separately.
PER_K_SEARCHES = ("fs_sds",)
ALL_METHODS = FILTERS + SEEDED_FILTERS + SEARCHES + PER_K_SEARCHES

# FASTENER's measured cost on MADELON (manifest of 20260916T123417Z: 5615-6468
# fits per seed). The evolutionary arms get the same budget so the comparison is
# of search quality, not of who was allowed more compute.
DEFAULT_EVALUATIONS = 6000


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="madelon")
    ap.add_argument("--methods", default=",".join(ALL_METHODS),
                    help=f"comma-separated subset of {','.join(ALL_METHODS)}")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--evaluations", type=int, default=DEFAULT_EVALUATIONS,
                    help="model-fit budget per seed for the evolutionary arms")
    ap.add_argument("--boruta-max-iter", type=int, default=100)
    ap.add_argument("--sds-population", type=int, default=None,
                    help="FS-SDS swarm size (default 100, the authors' "
                         "reference setting)")
    ap.add_argument("--sds-iterations", type=int, default=None,
                    help="cap on FS-SDS diffusion sweeps per k. Default: no "
                         "cap, so the fit budget stops the run and FS-SDS gets "
                         "the same per-run compute as every other search. Pass "
                         "50 for the authors' reference setting, which on "
                         "MADELON stops at ~2600 fits per k.")
    ap.add_argument("--poss-k", type=int, default=None,
                    help="POSS's constraint parameter: subsets of 2k or more "
                         "features are infeasible by definition, so this is "
                         "both the size it optimises for and the widest subset "
                         "its archive can hold. Default min(50, n_features), "
                         "which covers the region the comparison reports.")
    ap.add_argument("--init", default="obl", choices=("obl", "sparse"),
                    help="initialisation for the evolutionary arms. 'obl' is "
                         "the ported algorithm (~50%% density, i.e. ~250 "
                         "features on MADELON). 'sparse' seeds 1-30 features "
                         "and is a DEPARTURE from the source, used to separate "
                         "the search from where it was told to start; such "
                         "runs are labelled *_sparse.")
    ap.add_argument("--no-fastener", action="store_true",
                    help="skip the FASTENER arm (it is included by default so "
                         "the plot has its reference curve)")
    ap.add_argument("--fastener-rounds", type=int, default=600)
    ap.add_argument("--fastener-swap", action="append",
                    choices=sorted(SWAP_ARMS),
                    help="FASTENER pruning arm, repeatable; default runs all "
                         "three (none = the published algorithm)")
    ap.add_argument("--n-jobs", type=int, default=-1,
                    help="parallelism for NSGAII-MIIP's pairwise MI matrix")
    ap.add_argument("--quick", action="store_true",
                    help="tiny budget for a smoke check")
    ap.add_argument("--name", default=None)
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    quick = args.quick

    methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    unknown = [m for m in methods if m not in ALL_METHODS]
    if unknown:
        raise SystemExit(f"unknown method(s): {unknown}; have {list(ALL_METHODS)}")

    n_seeds = 2 if quick else args.seeds
    seeds = [2020 + i for i in range(n_seeds)]
    evaluations = 300 if quick else args.evaluations
    boruta_max_iter = 10 if quick else args.boruta_max_iter
    fastener_rounds = 40 if quick else args.fastener_rounds
    # Ordered so the published algorithm is always the first arm reported.
    fastener_arms = args.fastener_swap or ["none", "random", "guided"]
    fastener_arms = [a for a in ("none", "random", "guided")
                     if a in fastener_arms]
    ks = [k for k in K_GRID if k <= 30] if quick else K_GRID
    name = args.name or f"{args.dataset}_sota" + ("_quick" if quick else "")

    ds = load(args.dataset)
    print(ds)
    ks = [k for k in ks if k <= ds.n_features]

    params = {
        "dataset": args.dataset,
        "methods": methods,
        "with_fastener": not args.no_fastener,
        "fastener_rounds": fastener_rounds,
        "fastener_arms": fastener_arms,
        "fastener_max_fits": evaluations,
        "seeds": seeds,
        "evaluation_budget_per_seed": evaluations,
        "boruta_max_iter": boruta_max_iter,
        "fs_sds_evaluations_per_k": evaluations,
        "fs_sds_population": args.sds_population,
        "fs_sds_iterations": args.sds_iterations,
        "poss_k": args.poss_k if args.poss_k is not None
                  else min(50, ds.n_features),
        "init": args.init,
        "k_grid": ks,
        "model": "DecisionTreeClassifier",
        "model_seed": MODEL_SEED,
        "primary_metric": "f1_weighted",
        "quick": quick,
    }

    with Run(name, params) as run:
        print(f"run dir: {run.dir}")
        run.record("dataset", ds.summary())
        data_dir = DATA_DIR / args.dataset
        if data_dir.is_dir():
            run.record_inputs(**{p.name: p for p in sorted(data_dir.iterdir())
                                 if p.is_file()})

        all_results = []
        failures = {}
        counter = FitCounter()

        def checkpoint() -> None:
            """Persist what is finished after every unit.

            A multi-hour run that only writes at the end has nothing to show for
            itself if it is interrupted, and nothing a partial analysis can read
            while it is still going.
            """
            run.write_json("raw_results_partial.json", all_results)

        # Declare the whole plan before starting, so the ETA covers the run
        # rather than only the step in flight.
        prog = Progress(run.dir / "progress.json", run.run_id,
                        meta={"dataset": args.dataset, "quick": quick,
                              "seeds": seeds,
                              "evaluation_budget_per_seed": evaluations})
        for m in methods:
            if m in FILTERS:
                prog.plan(m)
        for m in methods:
            if m in SEEDED_FILTERS:
                for s in seeds:
                    prog.plan(m, seed=s)
        for m in methods:
            if m in SEARCHES:
                for s in seeds:
                    prog.plan(m, seed=s, budget_fits=evaluations)
        for m in methods:
            if m in PER_K_SEARCHES:
                for s in seeds:
                    prog.plan(m, seed=s, budget_fits=evaluations * len(ks))
        if not args.no_fastener:
            for arm in fastener_arms:
                for s in seeds:
                    prog.plan(FASTENER_ARM_NAMES[arm], seed=s,
                              budget_fits=evaluations)
        prog.write(force=True)
        print(f"progress: {run.dir / 'progress.json'}")
        print(f"  monitor with: python experiments/monitor.py "
              f"--run {run.run_id}")

        # ---- deterministic selectors ------------------------------------
        filter_fns = {
            "mrmr": lambda: sota.run_mrmr(ds, ks, counter),
            "relieff": lambda: sota.run_relieff(ds, ks, counter),
            "hsic_lasso": lambda: sota.run_hsic_lasso(ds, ks, counter),
        }
        selected_filters = [m for m in methods if m in FILTERS]
        if selected_filters:
            print("\nfilters:")
        for m in selected_filters:
            prog.start(m)
            try:
                res = filter_fns[m]()
            except Exception as exc:
                # One unavailable library must not discard the rest of the run.
                failures[m] = f"{type(exc).__name__}: {exc}"
                prog.fail(m, failures[m])
                print(f"  {m:14s} FAILED  {failures[m]}")
                traceback.print_exc()
                continue
            prog.finish(m, seconds=res["elapsed_seconds"])
            best = max(res["records"], key=lambda r: r["val_score"])
            print(f"  {m:14s} best test_f1={best['test_score']:.4f} "
                  f"@k={best['n_features']} ({res['elapsed_seconds']}s)")
            all_results.append(res)
            checkpoint()

        # ---- seeded filters ---------------------------------------------
        seeded_filter_fns = {
            "boruta": lambda s: sota.run_boruta(ds, ks, counter,
                                                max_iter=boruta_max_iter,
                                                seed=s),
        }
        for m in [m for m in methods if m in SEEDED_FILTERS]:
            print(f"\n{m} (x{len(seeds)} seeds):")
            for seed in seeds:
                unit = f"{m}:{seed}"
                prog.start(unit)
                try:
                    res = seeded_filter_fns[m](seed)
                except Exception as exc:
                    failures[unit] = f"{type(exc).__name__}: {exc}"
                    prog.fail(unit, failures[unit])
                    print(f"  seed {seed}: FAILED {failures[unit]}")
                    traceback.print_exc()
                    continue
                prog.finish(unit, seconds=res["elapsed_seconds"])
                best = max(res["records"], key=lambda r: r["val_score"])
                print(f"  seed {seed}: best test_f1={best['test_score']:.4f} "
                      f"@k={best['n_features']} "
                      f"confirmed={res['n_confirmed']} "
                      f"({res['elapsed_seconds']}s)")
                all_results.append(res)
                checkpoint()

        # ---- population searches ----------------------------------------
        # The MI matrix and clustering depend only on the training data, so they
        # are computed once and shared across seeds.
        cluster_cache = {}
        search_fns = {
            "nsga2": lambda s, cb: sota.run_nsga2(ds, s, evaluations,
                                                  init=args.init,
                                                  progress_cb=cb),
            # POSS takes no init: the paper starts it at the empty set, which is
            # already the sparse end, so the obl/sparse question does not arise.
            "poss": lambda s, cb: sota.run_poss_method(ds, s, evaluations,
                                                       k=args.poss_k,
                                                       progress_cb=cb),
            "nsgaii_miip": lambda s, cb: sota.run_nsgaii_miip_method(
                ds, s, evaluations, cluster_cache=cluster_cache,
                n_jobs=args.n_jobs, init=args.init, progress_cb=cb),
        }
        for m in [m for m in methods if m in SEARCHES]:
            print(f"\n{m} ({evaluations} fits x {len(seeds)} seeds):")
            for seed in seeds:
                unit = f"{m}:{seed}"
                prog.start(unit)
                try:
                    res = search_fns[m](seed, prog.tick)
                except Exception as exc:
                    failures[unit] = f"{type(exc).__name__}: {exc}"
                    prog.fail(unit, failures[unit])
                    print(f"  seed {seed}: FAILED {failures[unit]}")
                    traceback.print_exc()
                    continue
                prog.finish(unit, fits=res["model_fits"],
                            seconds=res["elapsed_seconds"])
                best = max(res["records"], key=lambda r: r["val_score"])
                print(f"  seed {seed}: front={len(res['records']):2d} "
                      f"best test_f1={best['test_score']:.4f} "
                      f"@k={best['n_features']} fits={res['model_fits']} "
                      f"({res['elapsed_seconds']}s)")
                all_results.append(res)
                checkpoint()

        # ---- per-k searches ----------------------------------------------
        # One SDS run per feature count, each at the same budget a whole run of
        # any other search gets. The total is therefore much larger, which is
        # the method's structure and is reported as such.
        for m in [m for m in methods if m in PER_K_SEARCHES]:
            print(f"\n{m} ({evaluations} fits x {len(ks)} k-values "
                  f"x {len(seeds)} seeds):")
            for seed in seeds:
                unit = f"{m}:{seed}"
                prog.start(unit)
                try:
                    res = sota.run_fs_sds_method(
                        ds, ks, seed=seed, stop_evaluations=evaluations,
                        population_size=args.sds_population,
                        max_iterations=args.sds_iterations,
                        progress_cb=prog.tick)
                except Exception as exc:
                    failures[unit] = f"{type(exc).__name__}: {exc}"
                    prog.fail(unit, failures[unit])
                    print(f"  seed {seed}: FAILED {failures[unit]}")
                    traceback.print_exc()
                    continue
                prog.finish(unit, fits=res["model_fits"],
                            seconds=res["elapsed_seconds"])
                best = max(res["records"], key=lambda r: r["val_score"])
                print(f"  seed {seed}: points={len(res['records']):2d} "
                      f"best test_f1={best['test_score']:.4f} "
                      f"@k={best['n_features']} "
                      f"total_fits={res['model_fits']} "
                      f"({res['elapsed_seconds']}s)")
                all_results.append(res)
                checkpoint()

        # ---- FASTENER arms ----------------------------------------------
        # Every arm is capped at the same number of model fits as the searches.
        # The swap arms buy extra fits per generation, so at equal ROUNDS they
        # would simply have been handed more compute; `rounds` is left high
        # enough that the cap is what stops the run.
        if not args.no_fastener:
            for arm in fastener_arms:
                label = FASTENER_ARM_NAMES[arm]
                print(f"\n{label} ({evaluations} fits x {len(seeds)} seeds):")
                for seed in seeds:
                    unit = f"{label}:{seed}"
                    prog.start(unit)
                    try:
                        res = run_fastener(ds, run.dir, seed=seed,
                                           rounds=fastener_rounds,
                                           swap=arm,
                                           max_fits=evaluations)
                    except Exception as exc:
                        failures[unit] = f"{type(exc).__name__}: {exc}"
                        prog.fail(unit, failures[unit])
                        print(f"  seed {seed}: FAILED {failures[unit]}")
                        traceback.print_exc()
                        continue
                    prog.finish(unit, fits=res["model_fits"],
                                seconds=res["search_seconds"])
                    best = max(res["records"], key=lambda r: r["val_score"])
                    print(f"  seed {seed}: front={len(res['records']):2d} "
                          f"best test_f1={best['test_score']:.4f} "
                          f"@k={best['n_features']} fits={res['model_fits']} "
                          f"stopped_on={res.get('stopped_on')} "
                          f"({res['search_seconds']}s)")
                    all_results.append(res)
                    checkpoint()

        prog.done("failed" if not all_results else "done")

        if not all_results:
            run.record("failures", failures)
            raise SystemExit("every method failed; nothing to compare")
        if failures:
            run.record("failures", failures)

        # ---- comparison ---------------------------------------------------
        rows = analysis.comparison_table(all_results, ks)

        csv_path = run.dir / "comparison.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=[
                "method", "seed", "budget_k", "n_features_used", "val_f1",
                "test_f1", "test_accuracy", "test_balanced_accuracy",
            ], extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

        # Each stochastic arm is tested against the best deterministic filter,
        # so seed variance is not read as an advantage.
        present = {r["method"] for r in rows}
        deterministic = tuple(m for m in FILTERS if m in present)
        sig = {}
        stochastic_arms = (tuple(FASTENER_ARM_NAMES[a] for a in fastener_arms)
                           + SEEDED_FILTERS + SEARCHES + PER_K_SEARCHES)
        if deterministic:
            for m in stochastic_arms:
                if m not in present:
                    continue
                s = analysis.seed_significance(rows, ks, stochastic=m,
                                               deterministic=deterministic)
                if s:
                    sig[m] = s
        run.record("seed_significance", sig)
        run.write_json("seed_significance.json", sig)
        run.write_json("raw_results.json", all_results)
        run.write_json("comparison_rows.json", rows)

        plot_path = analysis.render_plot(
            rows, run.dir / "comparison.png",
            f"FASTENER vs SotA selectors on {ds.name.upper()} "
            f"({ds.X_train.shape[0]} train / {ds.X_test.shape[0]} test, "
            f"{ds.n_features} features)")

        run.record("cost", {
            "filter_model_fits": counter.fits,
            "search_fits_per_seed": {
                m: [r["model_fits"] for r in all_results if r["method"] == m]
                for m in present
                if m in SEARCHES or m in PER_K_SEARCHES
                or m in FASTENER_ARM_NAMES.values()
            },
            "elapsed_by_method": {
                r["method"]: r.get("elapsed_seconds", r.get("search_seconds"))
                for r in all_results
            },
        })

        print(f"\nwrote {csv_path.name}, raw_results.json, {plot_path.name}")
        print(f"total wall time: {format_duration(run.elapsed())}")
        summarise(rows, ks)
        summarise_significance(sig)
        if failures:
            print(f"\nFAILED: {failures}")

    print(f"\nmanifest: {run.dir / 'manifest.json'}")
    return 0


def summarise(rows, ks) -> None:
    methods = sorted({r["method"] for r in rows})
    shown = [k for k in ks if k <= 50]
    print("\ntest weighted-F1 by feature budget (mean over seeds):")
    header = "  " + "method".ljust(16) + "".join(f"{k:>8}" for k in shown)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for m in methods:
        cells = []
        for k in shown:
            vals = [r["test_f1"] for r in rows
                    if r["method"] == m and r["budget_k"] == k]
            cells.append(f"{np.mean(vals):8.3f}" if vals else " " * 8)
        print("  " + m.ljust(16) + "".join(cells))


def summarise_significance(sig) -> None:
    for method, entries in sig.items():
        print(f"\n{method} vs best deterministic filter (test F1, across seeds):")
        print(f"  {'k':>4} {'mean':>7} {'sd':>7} {'baseline':>9} "
              f"{'delta':>8} {'wins':>6} {'p':>7}")
        print("  " + "-" * 54)
        for r in entries:
            if r["budget_k"] > 50:
                continue
            print(f"  {r['budget_k']:>4} {r['mean_test_f1']:>7.3f} "
                  f"{r['sd_test_f1']:>7.3f} {r['best_baseline_test_f1']:>9.3f} "
                  f"{r['delta_vs_baseline']:>+8.3f} "
                  f"{r['seeds_beating_baseline']:>4}/{r['n_seeds']} "
                  f"{r['p_value']:>7.3f}")


if __name__ == "__main__":
    raise SystemExit(main())
