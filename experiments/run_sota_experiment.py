"""FASTENER vs. stronger and more recent feature-selection methods.

Extends run_experiment.py with mRMR, ReliefF, Boruta, HSIC-Lasso, plain NSGA-II
and a port of NSGAII-MIIP, over two datasets.

Work is parallelised across (method, seed) tasks with joblib, since the
population-based searches dominate the runtime and are independent of each other.

Usage:
    python experiments/run_sota_experiment.py --dataset madelon
    python experiments/run_sota_experiment.py --dataset gina --jobs 12
    python experiments/run_sota_experiment.py --dataset madelon --quick
"""
import argparse
import csv
import sys
import time
import warnings
from pathlib import Path
from typing import Dict, List

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis  # noqa: E402
import baselines  # noqa: E402
import sota_baselines as sota  # noqa: E402
from datasets import LOADERS, load  # noqa: E402
from protocol import MODEL_SEED, FitCounter  # noqa: E402
from provenance import Run  # noqa: E402
from run_fastener import run_fastener  # noqa: E402

K_GRID = [1, 2, 3, 5, 8, 10, 12, 15, 20, 25, 30, 50, 100, 200, 500]

# Matched to FASTENER's measured model-fit count (~6000 on MADELON at 600
# rounds), so the two searches get equal compute. The paper's own default is
# 10000; that was tried first and is ~40% more expensive for a conclusion the
# 400- and 2000-fit probes already showed to be flat, so equal-compute is the
# reported setting and the difference is stated rather than hidden.
GA_EVALUATIONS = 6000


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="madelon", choices=sorted(LOADERS))
    ap.add_argument("--rounds", type=int, default=600)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--ga-evaluations", type=int, default=GA_EVALUATIONS)
    ap.add_argument("--jobs", type=int, default=6,
                    help="parallel workers for the (method, seed) tasks")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--name", default=None)
    return ap.parse_args()


def main() -> int:
    warnings.filterwarnings("ignore")
    args = parse_args()

    rounds = 60 if args.quick else args.rounds
    n_seeds = 2 if args.quick else args.seeds
    ga_evals = 400 if args.quick else args.ga_evaluations
    ks = [k for k in K_GRID if k <= 30] if args.quick else K_GRID
    seeds = [2020 + i for i in range(n_seeds)]
    name = args.name or f"{args.dataset}_sota"

    ds = load(args.dataset)
    ks = [k for k in ks if k <= ds.n_features]
    print(ds)

    params = {
        "dataset": args.dataset,
        "fastener_rounds": rounds,
        "seeds": seeds,
        "ga_evaluations": ga_evals,
        "k_grid": ks,
        "model": "DecisionTreeClassifier",
        "model_seed": MODEL_SEED,
        "primary_metric": "f1_weighted",
        "parallel_jobs": args.jobs,
        "quick": args.quick,
    }

    with Run(name, params) as run:
        print(f"run dir: {run.dir}")
        run.record("dataset", ds.summary())

        all_results: List[Dict] = []
        counter = FitCounter()

        # ---- deterministic selectors, run serially (they are cheap) --------
        print("\nfilters and wrappers:")
        t0 = time.time()
        all_results.append(baselines.run_all_features(ds, counter))
        for nm in baselines.RANKERS:
            all_results.append(baselines.run_ranker(ds, nm, ks, counter))
        all_results.append(baselines.run_rfe(ds, [k for k in ks if k <= 100], counter))
        all_results.append(baselines.run_random(ds, ks, counter))

        for label, fn in (
            ("mrmr", lambda: sota.run_mrmr(ds, ks, counter)),
            ("relieff", lambda: sota.run_relieff(ds, ks, counter)),
            ("boruta", lambda: sota.run_boruta(ds, ks, counter)),
            ("hsic_lasso", lambda: sota.run_hsic_lasso(ds, ks, counter)),
        ):
            try:
                all_results.append(fn())
            except Exception as exc:
                # A baseline that cannot run is recorded as such, not silently
                # dropped -- an absent method must not look like a weak one.
                print(f"  {label:18s} FAILED: {type(exc).__name__}: {exc}")
                run.manifest.setdefault("failed_methods", {})[label] = (
                    f"{type(exc).__name__}: {exc}")
                continue

        for res in all_results:
            if res["records"]:
                best = max(res["records"], key=lambda r: r["val_score"])
                print(f"  {res['method']:18s} best test={best['test_score']:.4f} "
                      f"@k={best['n_features']:<4d} ({res['elapsed_seconds']}s)")
        serial_seconds = time.time() - t0
        baseline_fits = counter.fits

        # ---- population searches, run in parallel -------------------------
        # The MI matrix and clustering for NSGAII-MIIP depend only on the
        # training data, so compute once up front and share across all seeds.
        print("\nprecomputing MI matrix and feature clusters for NSGAII-MIIP ...")
        t0 = time.time()
        from nsgaii_miip import cluster_features
        clusters, mi, ent = cluster_features(
            ds.X_train, ds.y_train, np.random.RandomState(MODEL_SEED),
            n_jobs=min(args.jobs, 8))
        cluster_cache = {"clusters": clusters, "mi": mi, "ent": ent}
        print(f"  {mi.shape[0]}x{mi.shape[0]} MI matrix, {len(clusters)} clusters "
              f"({time.time() - t0:.1f}s)")

        tasks = []
        for seed in seeds:
            tasks.append(("fastener", seed))
            tasks.append(("nsga2", seed))
            tasks.append(("nsgaii_miip", seed))
            tasks.append(("nsgaii_miip_sparse", seed))

        print(f"\npopulation searches: {len(tasks)} tasks on {args.jobs} workers")
        print(f"  fastener={rounds} rounds; GA methods={ga_evals} model fits")

        # Each task writes its own result file the moment it finishes, so a
        # crash or a kill loses only the tasks still in flight. An earlier run
        # of this script died with everything still in memory and produced
        # nothing despite hours of completed work.
        partial_dir = run.dir / "partial"
        partial_dir.mkdir(exist_ok=True)

        def run_task(method: str, seed: int) -> Dict:
            import json as _json
            out_path = partial_dir / f"{method}_seed{seed}.json"
            if out_path.exists():
                # Resume: a completed task is not redone.
                with open(out_path, encoding="utf-8") as fh:
                    return _json.load(fh)
            try:
                if method == "fastener":
                    res = run_fastener(ds, run.dir, seed=seed, rounds=rounds)
                elif method == "nsga2":
                    res = sota.run_nsga2(ds, seed=seed, stop_evaluations=ga_evals)
                elif method == "nsgaii_miip":
                    res = sota.run_nsgaii_miip_method(
                        ds, seed=seed, stop_evaluations=ga_evals,
                        cluster_cache=cluster_cache)
                elif method == "nsgaii_miip_sparse":
                    res = sota.run_nsgaii_miip_method(
                        ds, seed=seed, stop_evaluations=ga_evals,
                        cluster_cache=cluster_cache, init="sparse")
                else:
                    raise ValueError(method)
            except Exception as exc:
                # One failed search must not destroy the whole run.
                return {"method": method, "seed": seed, "records": [],
                        "failed": f"{type(exc).__name__}: {exc}"}

            with open(out_path, "w", encoding="utf-8") as fh:
                _json.dump(res, fh, default=str)
            return res

        t0 = time.time()
        from joblib import Parallel, delayed
        ga_results = Parallel(n_jobs=args.jobs, prefer="processes", verbose=10)(
            delayed(run_task)(m, s) for m, s in tasks)
        parallel_seconds = time.time() - t0

        for res in ga_results:
            if res.get("failed"):
                print(f"  {res['method']} seed {res['seed']} FAILED: {res['failed']}")
                run.manifest.setdefault("failed_methods", {})[
                    f"{res['method']}_seed{res['seed']}"] = res["failed"]
        ga_results = [r for r in ga_results if r.get("records")]

        for res in ga_results:
            if res["records"]:
                best = max(res["records"], key=lambda r: r["val_score"])
                secs = res.get("elapsed_seconds", res.get("search_seconds", "?"))
                print(f"  {res['method']:20s} seed {res['seed']}: "
                      f"front={len(res['records']):3d} "
                      f"best test={best['test_score']:.4f} @k={best['n_features']:<4d} "
                      f"fits={res.get('model_fits','?')} ({secs}s)")
        all_results.extend(ga_results)

        # ---- signal probe -------------------------------------------------
        probe = analysis.probe_relevant_features(ds)
        run.record("relevant_feature_probe", probe)

        # ---- comparison ---------------------------------------------------
        rows = analysis.comparison_table(all_results, ks)
        for r in rows:
            r["overlap"] = analysis.overlap_with_probe(
                r["features"], probe["top20_by_importance"])["n_overlap_with_probe_top20"]

        with open(run.dir / "comparison.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=[
                "method", "seed", "budget_k", "n_features_used", "val_f1",
                "test_f1", "test_accuracy", "test_balanced_accuracy", "overlap",
            ], extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

        run.write_json("raw_results.json", all_results)
        run.write_json("comparison_rows.json", rows)

        for stochastic in ("fastener", "nsgaii_miip", "nsga2"):
            sig = analysis.seed_significance(rows, ks, stochastic=stochastic)
            run.manifest.setdefault("seed_significance", {})[stochastic] = sig
        run.write_json("seed_significance.json", run.manifest["seed_significance"])

        # Head-to-head between the two evolutionary methods.
        h2h = analysis.head_to_head(rows, "fastener", "nsgaii_miip", ks)
        run.record("fastener_vs_nsgaii_miip", h2h)
        run.write_json("head_to_head.json", h2h)

        analysis.render_plot(
            rows, run.dir / "comparison.png",
            f"FASTENER vs baselines and NSGAII-MIIP on {args.dataset.upper()} "
            f"({ds.X_train.shape[0]} train / {ds.X_test.shape[0]} test, "
            f"{ds.n_features} features)")

        run.record("cost", {
            "baseline_model_fits": baseline_fits,
            "serial_baseline_seconds": round(serial_seconds, 1),
            "parallel_search_seconds": round(parallel_seconds, 1),
            "parallel_jobs": args.jobs,
            "per_method_fits": {
                f"{r['method']}_seed{r.get('seed')}": r.get("model_fits")
                for r in ga_results
            },
        })

        reach = summarise_reach(all_results)
        run.record("subset_size_reach", reach)
        summarise(rows, ks)
        summarise_h2h(h2h)

    print(f"\nmanifest: {run.dir / 'manifest.json'}")
    return 0


def summarise(rows, ks) -> None:
    methods = sorted({r["method"] for r in rows})
    shown = [k for k in ks if k <= 50]
    print("\ntest weighted-F1 by feature budget (mean over seeds):")
    header = "  " + "method".ljust(22) + "".join(f"{k:>8}" for k in shown)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for m in methods:
        cells = []
        for k in shown:
            vals = [r["test_f1"] for r in rows if r["method"] == m and r["budget_k"] == k]
            cells.append(f"{np.mean(vals):8.3f}" if vals else " " * 8)
        print("  " + m.ljust(22) + "".join(cells))


def summarise_reach(all_results) -> List[Dict]:
    """Smallest and largest subset each method actually produced.

    A search that never produces a small subset shows up as a BLANK row in the
    score table at small k, which looks like missing data but is really the
    result: the method did not get there within its budget. This makes that
    explicit.
    """
    by_method: Dict[str, List[int]] = {}
    for res in all_results:
        for r in res["records"]:
            by_method.setdefault(r["method"], []).append(r["n_features"])

    reach = []
    for m, sizes in sorted(by_method.items()):
        reach.append({"method": m, "min_subset_size": int(min(sizes)),
                      "max_subset_size": int(max(sizes)),
                      "n_subsets_reported": len(sizes)})

    print("\nsmallest subset each method actually produced:")
    print(f"  {'method':22s} {'min k':>7} {'max k':>7}")
    print("  " + "-" * 38)
    for r in reach:
        print(f"  {r['method']:22s} {r['min_subset_size']:>7} {r['max_subset_size']:>7}")
    return reach


def summarise_h2h(h2h) -> None:
    if not h2h:
        return
    print("\nfastener vs nsgaii_miip (port), paired by seed:")
    print(f"  {'k':>4} {'fastener':>10} {'miip':>10} {'delta':>9} {'wins':>7} {'p':>7}")
    print("  " + "-" * 52)
    for r in h2h:
        if r["budget_k"] > 50:
            continue
        print(f"  {r['budget_k']:>4} {r['mean_a']:>10.3f} {r['mean_b']:>10.3f} "
              f"{r['delta']:>+9.3f} {r['a_wins']:>3}/{r['n_pairs']:<3} {r['p_value']:>7.3f}")


if __name__ == "__main__":
    raise SystemExit(main())
