"""SotA experiment: FASTENER against every other feature selector in the repo.

One runner covers every algorithm HYPOTHESES.md compares: the simple rankers,
RFE, random subsets and the all-features reference (from baselines.py); mRMR,
ReliefF, Boruta and HSIC Lasso; plain NSGA-II from OBL and from sparse
initialisation; POSS, FS-SDS and the NSGAII-MIIP port; and the three FASTENER
arms. POSS and FS-SDS are the FASTENER paper's own wrapper comparators.

The run follows HYPOTHESES.md:

* one classifier, protocol.make_model(), drives every search and scores every
  result -- Boruta included. It is the decision tree, or with --model rf the
  protocol's 100-tree random forest (H5H6-E02, DEC-41), for every method;
* every search gets the same fit budget, protocol.FIT_BUDGET (6,000). FS-SDS
  holds a run at one k, so it spreads that budget evenly over k = 1..20;
* curves are read on protocol.K_GRID, every k up to 20 then a sparse tail;
* datasets over protocol.ROW_CAP rows use a fixed stratified subsample;
* every search records its best score after each of its own iterations, in
  trajectories/<method>_seed<seed>.jsonl;
* AUF at K = 10 and K = 20, under every metric, is written per method and seed
  to auf.csv. The primary values are auf10_f1_weighted (H1-H3, H5, H6) and
  auf20_f1_weighted (H4).

Usage:
    python experiments/run_sota.py --quick              # smoke check
    python experiments/run_sota.py                      # full run, MADELON
    python experiments/run_sota.py --dataset gina
    python experiments/run_sota.py --methods mrmr,boruta --no-fastener
    python experiments/run_sota.py --dataset eodata --experiment H1-E01 \\
        --methods nsga2,nsga2_sparse --no-fastener
    python experiments/run_sota.py --dataset crop_mapping --split eo \\
        --evaluations 1000 --methods "" --fastener-arm none \\
        --fastener-arm 2020 --experiment H0-E01          # H0

Runs that test a hypothesis pass --experiment (see METHODOLOGY.md): the run is
then refused from uncommitted code, recorded in EXPERIMENTS.md, and every arm
gets an algorithm ID in the manifest and in every result row.
"""
import os

# One thread per numeric library, set before numpy is first imported (DEC-37).
# The environment's MKL (8 threads) and OpenMP (16) pools only spin and fight
# over cores here: on lymphoma, 1,500 FASTENER fits took 384.6 CPU s and 91.9 s
# of wall clock with them, 40.3 and 40.5 s without, with the same front. Runs
# go in parallel one process per job, so a single thread each is also the
# fastest setting, and it makes CPU time a measure of work (H4's budget).
NUMERIC_THREADS = "1"
for _var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_var] = NUMERIC_THREADS

import argparse
import csv
import sys
import time
import traceback
import warnings
from pathlib import Path

# Raised from the random forest's worker threads, tens of thousands of times a
# run on some datasets (ItalyPowerDemand under FASTENER's guided swap): the
# threads cannot be handed scikit-learn's configuration, which this code never
# changes. It alters no result, and on a cluster it filled every job's log on
# the shared file system.
warnings.filterwarnings(
    "ignore", message=r"`sklearn\.utils\.parallel\.delayed` should be used")

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis  # noqa: E402
import baselines  # noqa: E402
import sota_baselines as sota  # noqa: E402
from datasets import DATA_DIR, SPLITS, load  # noqa: E402
from progress import Progress, format_duration  # noqa: E402
from nsgaii_miip import MAX_BARREN_GENERATIONS  # noqa: E402
from protocol import (FIT_BUDGET, fit_budget, FS_SDS_K_RANGE, K_GRID, MODEL_SEED,  # noqa: E402
                      MODELS, RF_TREES, ROW_CAP, FitCounter,
                      lgbm_min_child_samples, model_description, set_model,
                      set_train_rows)
from provenance import DirtyTreeError, Run  # noqa: E402
from run_fastener import (MATING_VERSIONS, run_fastener,  # noqa: E402
                          search_model_factory)
from trajectory import Trajectory  # noqa: E402

# The FASTENER arms. "none", "random" and "guided" are the three pruning arms
# of H2/H3 on the fixed code; "2020" is the original mating behaviour, the arm
# H0 compares the fixed code against. The method labels match what
# run_fastener stamps on its records, so the plot styles in analysis.py and the
# significance tables pick them up without further mapping.
FASTENER_ARMS = {
    "none": {"label": "fastener", "swap": "none", "mating": "fixed"},
    "2020": {"label": "fastener_2020", "swap": "none", "mating": "2020"},
    "random": {"label": "fastener_swap_random", "swap": "random",
               "mating": "fixed"},
    "guided": {"label": "fastener_swap_guided", "swap": "guided",
               "mating": "fixed"},
}
FASTENER_ARM_NAMES = {k: v["label"] for k, v in FASTENER_ARMS.items()}
# Report order: the fixed stock arm first, then the published code, then swaps.
FASTENER_ARM_ORDER = ("none", "2020", "random", "guided")
# What runs when no arm is named: H2/H3's three arms, as before.
DEFAULT_FASTENER_ARMS = ("none", "random", "guided")

# Deterministic selectors: one pass each, no seed. The three rankers, RFE and
# the all-features reference come from baselines.py, so that one runner covers
# every algorithm H5 and H6 compare.
RANKERS = ("kbest_mutual_info", "kbest_anova_f", "tree_importance")
FILTERS = ("mrmr", "relieff", "hsic_lasso") + RANKERS + ("rfe_tree",
                                                          "all_features")
# Boruta is a filter in spirit but randomised in fact -- it permutes every
# column to build shadow features and refits its estimator each iteration -- so
# it gets the same seed treatment as the searches and reports a spread, not a
# single point that the significance tests would read as a fixed baseline.
# Random subsets are seeded for the same reason.
SEEDED_FILTERS = ("boruta", "random")
# Population searches: one run per seed. nsga2 always starts from OBL, as
# ported; nsga2_sparse always starts from 1-30 features. They are separate
# methods rather than one method under a flag, so H1 runs both arms in one
# invocation.
SEARCHES = ("nsga2", "nsga2_sparse", "poss", "nsgaii_miip")
# FS-SDS fixes the subset size for a whole run, so it runs once per k over
# protocol.FS_SDS_K_RANGE, with the run's fit budget divided evenly across
# them -- 300 per k at the default 6,000 -- so it spends what every other arm
# spends (HYPOTHESES.md).
PER_K_SEARCHES = ("fs_sds",)
ALL_METHODS = FILTERS + SEEDED_FILTERS + SEARCHES + PER_K_SEARCHES

# Equal across arms, so the comparison is of search quality, not of who was
# allowed more compute.
DEFAULT_EVALUATIONS = FIT_BUDGET


def numeric_thread_pools():
    """Each loaded numeric thread pool and its thread count."""
    try:
        from threadpoolctl import threadpool_info
    except ImportError:
        return None
    return {f"{d.get('internal_api')}:{d.get('prefix')}": d.get("num_threads")
            for d in threadpool_info()}


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="madelon")
    ap.add_argument("--methods", default=",".join(ALL_METHODS),
                    help=f"comma-separated subset of {','.join(ALL_METHODS)}")
    ap.add_argument("--seeds", type=int, default=5,
                    help="run seeds 2020 .. 2020 + n - 1")
    ap.add_argument("--seed", type=int, action="append", default=None,
                    help="run only this seed, repeatable; overrides --seeds. "
                         "Each search seeds its own RNG, so a seed run alone "
                         "gives the same result as inside a five-seed run, and "
                         "per-seed runs of one experiment can go in parallel "
                         "(run_queue.py); make_report merges them.")
    ap.add_argument("--evaluations", type=int, default=None,
                    help="model-fit budget per run, for every search. FS-SDS "
                         "divides it evenly over k = 1..20. Default: "
                         "protocol.fit_budget(dataset), "
                         f"{DEFAULT_EVALUATIONS} on most datasets.")
    ap.add_argument("--cpu-seconds", type=float, default=None,
                    help="process-CPU-time budget per run, in place of the fit "
                         "budget (H4: equal compute between methods). FASTENER "
                         "stops when its search has used this much CPU time; "
                         "FS-SDS gets an even share per k over k = 1..20. "
                         "Only FASTENER arms and fs_sds take it.")
    ap.add_argument("--search-model", default="tree", choices=("tree", "elm"),
                    help="classifier that drives the search and scores its "
                         "result: the protocol's decision tree (default) or "
                         "the FASTENER paper's ELM (H4-E02). With elm, arms "
                         "are labelled fastener_elm and fs_sds_elm. Only "
                         "FASTENER arms and fs_sds take it.")
    ap.add_argument("--model", default="tree", choices=MODELS,
                    help="the protocol classifier, for EVERY method: the "
                         "decision tree (default), a random forest of "
                         f"{RF_TREES} trees (rf, H5H6-E02) or LightGBM "
                         "(lgbm, H5H6-E03). Arm labels do not "
                         "change; the model is in the manifest and in every "
                         "algorithm ID.")
    ap.add_argument("--model-jobs", type=int, default=1,
                    help="threads a random forest fits its trees on. Does "
                         "not change any result (fixed random_state), so it "
                         "is recorded but not part of an arm's configuration.")
    ap.add_argument("--nsga-max-barren", type=int,
                    default=MAX_BARREN_GENERATIONS,
                    help="stop nsga2, nsga2_sparse and nsgaii_miip after this "
                         "many generations in a row score no new subset "
                         f"(default {MAX_BARREN_GENERATIONS}, DEC-41); 0 runs "
                         "until the fit budget is spent, the code of "
                         "H5H6-E01 and earlier.")
    ap.add_argument("--boruta-max-iter", type=int, default=100)
    ap.add_argument("--sds-population", type=int, default=None,
                    help="FS-SDS swarm size (default 100, the authors' "
                         "reference setting)")
    ap.add_argument("--sds-iterations", type=int, default=None,
                    help="cap on FS-SDS diffusion sweeps per k. Default: no "
                         "cap, so the fit budget stops the run.")
    ap.add_argument("--poss-k", type=int, default=None,
                    help="POSS's constraint parameter: subsets of 2k or more "
                         "features are infeasible by definition, so this is "
                         "both the size it optimises for and the widest subset "
                         "its archive can hold. Default min(50, n_features), "
                         "which covers the region the comparison reports.")
    ap.add_argument("--init", default="obl", choices=("obl", "sparse"),
                    help="initialisation for NSGAII-MIIP only. 'obl' is the "
                         "ported algorithm; 'sparse' seeds 1-30 features, is a "
                         "DEPARTURE from the source, and labels the run "
                         "nsgaii_miip_sparse. Plain NSGA-II does not read this "
                         "flag: run nsga2 and nsga2_sparse as methods.")
    ap.add_argument("--split", default="protocol", choices=SPLITS,
                    help="'protocol' (default): the row cap, then 60/20/20. "
                         "'eo': H0's split for Earth-observation sets -- a "
                         "stratified 100,000-row subsample split 40/10/50 "
                         "into train/validation/test; --max-rows is ignored.")
    ap.add_argument("--max-rows", type=int, default=ROW_CAP,
                    help=f"row cap: a dataset with more rows uses a fixed "
                         f"stratified subsample of this many, identical for "
                         f"every arm and seed. Default {ROW_CAP}, per "
                         f"HYPOTHESES.md; 0 uses every row.")
    ap.add_argument("--no-fastener", action="store_true",
                    help="skip the FASTENER arms")
    ap.add_argument("--fastener-rounds", type=int, default=100_000,
                    help="generation cap, set far above what the fit budget "
                         "allows so that the budget is what stops FASTENER, as "
                         "for every other search; `stopped_on` confirms it.")
    ap.add_argument("--fastener-arm", "--fastener-swap", dest="fastener_arm",
                    action="append", choices=sorted(FASTENER_ARMS),
                    help="FASTENER arm, repeatable: none (stock, fixed code), "
                         "2020 (the original mating, H0), random, guided. "
                         "Default: none, random and guided.")
    ap.add_argument("--n-jobs", type=int, default=-1,
                    help="parallelism for NSGAII-MIIP's pairwise MI matrix")
    ap.add_argument("--quick", action="store_true",
                    help="tiny budget for a smoke check")
    ap.add_argument("--name", default=None)
    ap.add_argument("--experiment", default=None, metavar="ID",
                    help="experiment ID this run is evidence for, e.g. "
                         "H1-E01 (issue one with experiment_ids.py new H1)")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="with --experiment: run from uncommitted code anyway. "
                         "Algorithm IDs get -dirty and the run cannot be cited "
                         "as evidence.")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    quick = args.quick

    # Before anything builds a classifier: every method reads it from here.
    set_model(args.model, args.model_jobs)
    barren = args.nsga_max_barren or None

    methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    unknown = [m for m in methods if m not in ALL_METHODS]
    if unknown:
        raise SystemExit(f"unknown method(s): {unknown}; have {list(ALL_METHODS)}")

    if args.seed:
        seeds = sorted(set(args.seed))
    else:
        n_seeds = 2 if quick else args.seeds
        seeds = [2020 + i for i in range(n_seeds)]
    evaluations = 300 if quick else (
        args.evaluations if args.evaluations is not None
        else fit_budget(args.dataset))
    boruta_max_iter = 10 if quick else args.boruta_max_iter
    fastener_rounds = 40 if quick else args.fastener_rounds
    # Ordered so the stock arm is always the first arm reported.
    fastener_arms = args.fastener_arm or list(DEFAULT_FASTENER_ARMS)
    fastener_arms = [a for a in FASTENER_ARM_ORDER if a in fastener_arms]
    ks = [k for k in K_GRID if k <= 30] if quick else K_GRID
    # The k grid before the per-dataset cap: part of an arm's configuration,
    # while the cap is a property of the dataset.
    grid = list(ks)
    # FS-SDS's share of the run budget per k. Fixed by the full range, not by
    # the dataset, so the arm's configuration -- and its algorithm ID -- is the
    # same on every dataset. The remainder of an uneven division goes unspent
    # rather than to some k and not others.
    fs_per_k = max(1, evaluations // len(FS_SDS_K_RANGE))
    # A CPU-time budget replaces the fit budget for the two searches that take
    # one; every other search would silently run on fits, so they are refused.
    cpu_seconds = args.cpu_seconds
    fs_cpu_per_k = None
    # The classifier the searches use. Every other method is defined on the
    # protocol tree, so a different model is refused for them rather than
    # silently ignored.
    search_model = args.search_model
    model_suffix = "" if search_model == "tree" else f"_{search_model}"
    model_desc = {"tree": model_description(),
                  "elm": "ELMClassifier(160 sigmoid hidden, seed 20200)"
                  }[search_model]
    if search_model != "tree" and args.model != "tree":
        raise SystemExit("--search-model elm replaces the decision tree for "
                         "its arms; it cannot be combined with --model "
                         f"{args.model}")
    if search_model != "tree":
        other = [m for m in methods if m not in PER_K_SEARCHES]
        if other:
            raise SystemExit(f"--search-model {search_model} is supported only "
                             f"for FASTENER and fs_sds, not {other}")
    if cpu_seconds is not None:
        if cpu_seconds <= 0:
            raise SystemExit("--cpu-seconds must be positive")
        other = [m for m in methods if m not in PER_K_SEARCHES]
        if other:
            raise SystemExit(f"--cpu-seconds is supported only for FASTENER "
                             f"and fs_sds, not {other}")
        if args.evaluations is not None:
            raise SystemExit("--cpu-seconds replaces the fit budget; do not "
                             "pass --evaluations as well")
        fs_cpu_per_k = cpu_seconds / len(FS_SDS_K_RANGE)
        evaluations = None
        fs_per_k = None
    name = args.name or (f"{args.dataset}_sota" + ("_quick" if quick else "")
                         + ("".join(f"_s{s}" for s in seeds) if args.seed
                            else ""))

    ds = load(args.dataset, max_rows=args.max_rows or None, split=args.split)
    # LightGBM's smallest leaf follows the training split (DEC-44).
    set_train_rows(ds.X_train.shape[0])
    print(ds)
    if ds.max_rows and ds.n_rows_used <= ds.max_rows:
        print(f"  row cap {ds.max_rows}: using {ds.n_rows_used} rows")
    ks = [k for k in ks if k <= ds.n_features]
    fs_ks = [k for k in FS_SDS_K_RANGE if k <= ds.n_features]

    params = {
        "dataset": args.dataset,
        "methods": methods,
        "with_fastener": not args.no_fastener,
        "fastener_rounds": fastener_rounds,
        "fastener_arms": fastener_arms,
        "fastener_max_fits": evaluations,
        "seeds": seeds,
        "evaluation_budget_per_seed": evaluations,
        "cpu_seconds_per_run": cpu_seconds,
        "fs_sds_cpu_seconds_per_k": fs_cpu_per_k,
        "boruta_max_iter": boruta_max_iter,
        "boruta_estimator": f"protocol {model_description()}",
        "fs_sds_k_range": fs_ks,
        "fs_sds_evaluations_per_k": fs_per_k,
        "fs_sds_evaluations_total": (fs_per_k * len(fs_ks)
                                     if fs_per_k is not None else None),
        "fs_sds_population": args.sds_population,
        "fs_sds_iterations": args.sds_iterations,
        "poss_k": args.poss_k if args.poss_k is not None
                  else min(50, ds.n_features),
        "nsgaii_miip_init": args.init,
        "nsga_max_barren_generations": barren,
        "k_grid": ks,
        "split": args.split,
        "max_rows": ds.max_rows,
        "n_rows_used": ds.n_rows_used,
        "model": model_desc,
        "search_model": search_model,
        "protocol_model": args.model,
        "model_n_jobs": args.model_jobs,
        "lgbm_min_child_samples": (lgbm_min_child_samples(ds.X_train.shape[0])
                                   if args.model == "lgbm" else None),
        "model_seed": MODEL_SEED,
        "primary_metric": "f1_weighted",
        "quick": quick,
        # What the numeric libraries actually run with (DEC-37), read back
        # rather than assumed from the environment variables set above.
        "numeric_threads": numeric_thread_pools(),
    }

    # Base method -> everything that changes what that arm does, other than the
    # dataset and the seed. Hashed into the algorithm ID, so a flag that alters
    # an arm without a commit still gives it a different ID.
    common = {"model": model_desc, "model_seed": MODEL_SEED,
              "primary_metric": "f1_weighted", "quick": quick}
    # Left out when off, so a run with --nsga-max-barren 0 has the algorithm
    # ID it had before the stop existed.
    nsga_stop = {"max_barren_generations": barren} if barren else {}
    arm_configs = {
        "mrmr": {"k_grid": grid},
        "relieff": {"k_grid": grid},
        "hsic_lasso": {"k_grid": grid},
        "rfe_tree": {"k_grid": grid},
        "all_features": {},
        "boruta": {"k_grid": grid, "max_iter": boruta_max_iter,
                   "estimator": "protocol_tree"},
        "random": {"k_grid": grid, "n_repeats": 10},
        "nsga2": {"evaluations": evaluations, "init": "obl", **nsga_stop},
        "nsga2_sparse": {"evaluations": evaluations, "init": "sparse",
                         **nsga_stop},
        # None = the default rule, min(50, n_features).
        "poss": {"evaluations": evaluations, "poss_k": args.poss_k},
        "nsgaii_miip": {"evaluations": evaluations, "init": args.init,
                        **nsga_stop},
        "fs_sds": {"evaluations_per_k": fs_per_k,
                   **({"cpu_seconds_per_k": fs_cpu_per_k}
                      if fs_cpu_per_k is not None else {}),
                   "k_range": list(FS_SDS_K_RANGE),
                   "population": args.sds_population,
                   "iterations": args.sds_iterations},
    }
    for r in RANKERS:
        arm_configs[r] = {"k_grid": grid}
    for arm in fastener_arms:
        # The mating flags themselves, not only the version's name, so a
        # change to what "fixed" means changes the algorithm ID's config hash.
        arm_configs[FASTENER_ARM_NAMES[arm]] = {
            "max_fits": evaluations, "rounds": fastener_rounds,
            **({"cpu_seconds": cpu_seconds} if cpu_seconds is not None
               else {}),
            "swap": FASTENER_ARMS[arm]["swap"],
            "mating": FASTENER_ARMS[arm]["mating"],
            **MATING_VERSIONS[FASTENER_ARMS[arm]["mating"]]}

    try:
        run = Run(name, params, experiment_id=args.experiment,
                  allow_dirty=args.allow_dirty)
    except (DirtyTreeError, ValueError) as exc:
        raise SystemExit(str(exc))

    with run:
        print(f"run dir: {run.dir}")
        if args.experiment:
            print(f"experiment: {args.experiment}"
                  + ("" if run.manifest["evidence"]
                     else "  (DIRTY TREE -- not citable as evidence)"))
        run.record("dataset", ds.summary())
        data_dir = DATA_DIR / args.dataset
        if data_dir.is_dir():
            run.record_inputs(**{p.name: p for p in sorted(data_dir.iterdir())
                                 if p.is_file()})

        all_results = []
        failures = {}
        counter = FitCounter()

        def tag(res, base: str) -> None:
            """Stamp the arm's algorithm ID on a result and its records."""
            aid = run.algorithm_id(res["method"], {**common,
                                                   **arm_configs[base]})
            res["algorithm_id"] = aid
            for rec in res["records"]:
                rec["algorithm_id"] = aid

        def trajectory(method: str, seed: int) -> Trajectory:
            """Best score per iteration, one file per (method, seed)."""
            return Trajectory(
                run.dir / "trajectories" / f"{method}_seed{seed}.jsonl",
                method, seed, ks)

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
                    prog.plan(m, seed=s, budget_fits=(
                        fs_per_k * len(fs_ks) if fs_per_k is not None
                        else None))
        if not args.no_fastener:
            for arm in fastener_arms:
                for s in seeds:
                    prog.plan(FASTENER_ARM_NAMES[arm], seed=s,
                              budget_fits=evaluations)
        prog.write(force=True)
        print(f"progress: {run.dir / 'progress.json'}")
        print(f"  monitor with: python experiments/monitor.py "
              f"--run {run.run_id}")

        def cpu_progress():
            """A progress callback that reports CPU time used, as a fraction
            of the run's CPU budget, instead of fits against a fit budget."""
            t0 = time.process_time()
            return lambda fits: prog.tick(
                fits, fraction=(time.process_time() - t0) / cpu_seconds)

        # ---- deterministic selectors ------------------------------------
        filter_fns = {
            "mrmr": lambda: sota.run_mrmr(ds, ks, counter),
            "relieff": lambda: sota.run_relieff(ds, ks, counter),
            "hsic_lasso": lambda: sota.run_hsic_lasso(ds, ks, counter),
            "rfe_tree": lambda: baselines.run_rfe(ds, ks, counter),
            "all_features": lambda: baselines.run_all_features(ds, counter),
        }
        for r in RANKERS:
            filter_fns[r] = (lambda name: lambda: baselines.run_ranker(
                ds, name, ks, counter))(r)
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
                print(f"  {m:18s} FAILED  {failures[m]}")
                traceback.print_exc()
                continue
            res.setdefault("method", m)
            prog.finish(m, seconds=res.get("elapsed_seconds"))
            best = max(res["records"], key=lambda r: r["val_score"])
            print(f"  {m:18s} best test_f1={best['test_score']:.4f} "
                  f"@k={best['n_features']} ({res.get('elapsed_seconds')}s)")
            tag(res, m)
            all_results.append(res)
            checkpoint()

        # ---- seeded filters ---------------------------------------------
        seeded_filter_fns = {
            "boruta": lambda s: sota.run_boruta(ds, ks, counter,
                                                max_iter=boruta_max_iter,
                                                seed=s),
            "random": lambda s: baselines.run_random(ds, ks, counter, seed=s),
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
                res.setdefault("seed", seed)
                prog.finish(unit, seconds=res.get("elapsed_seconds"))
                best = max(res["records"], key=lambda r: r["val_score"])
                extra = (f"confirmed={res['n_confirmed']} "
                         if "n_confirmed" in res else "")
                print(f"  seed {seed}: best test_f1={best['test_score']:.4f} "
                      f"@k={best['n_features']} {extra}"
                      f"({res.get('elapsed_seconds')}s)")
                tag(res, m)
                all_results.append(res)
                checkpoint()

        # ---- population searches ----------------------------------------
        # The MI matrix and clustering depend only on the training data, so they
        # are computed once and shared across seeds.
        cluster_cache = {}
        miip_label = "nsgaii_miip" if args.init == "obl" else "nsgaii_miip_sparse"
        search_fns = {
            "nsga2": lambda s, cb, t: sota.run_nsga2(
                ds, s, evaluations, init="obl", progress_cb=cb, trajectory=t,
                max_barren_generations=barren),
            "nsga2_sparse": lambda s, cb, t: sota.run_nsga2(
                ds, s, evaluations, init="sparse", progress_cb=cb,
                trajectory=t, max_barren_generations=barren),
            # POSS takes no init: the paper starts it at the empty set, which is
            # already the sparse end, so the obl/sparse question does not arise.
            "poss": lambda s, cb, t: sota.run_poss_method(
                ds, s, evaluations, k=args.poss_k, progress_cb=cb,
                trajectory=t),
            "nsgaii_miip": lambda s, cb, t: sota.run_nsgaii_miip_method(
                ds, s, evaluations, cluster_cache=cluster_cache,
                n_jobs=args.n_jobs, init=args.init, progress_cb=cb,
                trajectory=t, max_barren_generations=barren),
        }
        for m in [m for m in methods if m in SEARCHES]:
            print(f"\n{m} ({evaluations} fits x {len(seeds)} seeds):")
            label = miip_label if m == "nsgaii_miip" else m
            for seed in seeds:
                unit = f"{m}:{seed}"
                prog.start(unit)
                try:
                    res = search_fns[m](seed, prog.tick,
                                        trajectory(label, seed))
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
                tag(res, m)
                all_results.append(res)
                checkpoint()

        # ---- per-k searches ----------------------------------------------
        # One SDS run per k over FS_SDS_K_RANGE, the run budget divided evenly
        # across them, so FS-SDS spends what every other arm spends.
        for m in [m for m in methods if m in PER_K_SEARCHES]:
            if fs_cpu_per_k is not None:
                print(f"\n{m} ({fs_cpu_per_k:.1f} CPU s x {len(fs_ks)} "
                      f"k-values = {cpu_seconds:.0f} CPU s per seed x "
                      f"{len(seeds)} seeds):")
            else:
                print(f"\n{m} ({fs_per_k} fits x {len(fs_ks)} k-values "
                      f"= {fs_per_k * len(fs_ks)} per seed x "
                      f"{len(seeds)} seeds):")
            for seed in seeds:
                unit = f"{m}:{seed}"
                prog.start(unit)
                try:
                    res = sota.run_fs_sds_method(
                        ds, fs_ks, seed=seed, stop_evaluations=fs_per_k,
                        population_size=args.sds_population,
                        max_iterations=args.sds_iterations,
                        progress_cb=(prog.tick if cpu_seconds is None
                                     else cpu_progress()),
                        trajectory=trajectory(m + model_suffix, seed),
                        cpu_seconds_per_k=fs_cpu_per_k,
                        model_factory=(None if search_model == "tree" else
                                       search_model_factory(search_model)),
                        label=m + model_suffix)
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
                tag(res, m)
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
                print(f"\n{label} ("
                      + (f"{cpu_seconds:.0f} CPU s" if cpu_seconds is not None
                         else f"{evaluations} fits")
                      + f" x {len(seeds)} seeds):")
                for seed in seeds:
                    unit = f"{label}:{seed}"
                    prog.start(unit)
                    try:
                        res = run_fastener(ds, run.dir, seed=seed,
                                           rounds=fastener_rounds,
                                           swap=FASTENER_ARMS[arm]["swap"],
                                           mating=FASTENER_ARMS[arm]["mating"],
                                           method_name=label + model_suffix,
                                           model=search_model,
                                           progress_cb=(
                                               (lambda f: prog.tick(
                                                   f, evaluations))
                                               if cpu_seconds is None
                                               else cpu_progress()),
                                           max_fits=evaluations,
                                           max_cpu_seconds=cpu_seconds,
                                           dump_logs=False,
                                           trajectory=trajectory(
                                               label + model_suffix, seed))
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
                    tag(res, label)
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
                "method", "algorithm_id", "seed", "budget_k", "n_features_used", "val_f1",
                "test_f1", "test_accuracy", "test_balanced_accuracy",
            ], extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

        # AUF per method and seed, under every metric (HYPOTHESES.md). The
        # primary values are auf10_f1_weighted and auf20_f1_weighted; every
        # other column is secondary.
        auf_rows = analysis.auf_by_seed(all_results, Ks=(10, 20),
                                        n_features=ds.n_features)
        for r in auf_rows:
            match = next((res for res in all_results
                          if res["method"] == r["method"]
                          and res.get("seed") == r["seed"]), {})
            r["algorithm_id"] = match.get("algorithm_id")
        if auf_rows:
            cols = ["method", "algorithm_id", "seed"]
            for r in auf_rows:
                cols += [c for c in r if c not in cols]
            with open(run.dir / "auf.csv", "w", newline="",
                      encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=cols)
                w.writeheader()
                w.writerows(auf_rows)
        run.write_json("auf.json", auf_rows)

        # Each stochastic arm is tested against the best deterministic filter,
        # so seed variance is not read as an advantage.
        present = {r["method"] for r in rows}
        deterministic = tuple(m for m in FILTERS
                              if m in present and m != "all_features")
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
                or m == miip_label or m in FASTENER_ARM_NAMES.values()
            },
            "elapsed_by_method": {
                r["method"]: r.get("elapsed_seconds", r.get("search_seconds"))
                for r in all_results
            },
        })

        print(f"\nwrote {csv_path.name}, auf.csv, raw_results.json, "
              f"trajectories/, {plot_path.name}")
        print(f"total wall time: {format_duration(run.elapsed())}")
        summarise(rows, ks)
        summarise_auf(auf_rows)
        summarise_significance(sig)
        if failures:
            print(f"\nFAILED: {failures}")

    print(f"\nmanifest: {run.dir / 'manifest.json'}")
    return 0


def summarise(rows, ks) -> None:
    methods = sorted({r["method"] for r in rows})
    shown = [k for k in ks if k <= 50]
    print("\ntest weighted-F1 by feature budget (mean over seeds):")
    header = "  " + "method".ljust(22) + "".join(f"{k:>7}" for k in shown)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for m in methods:
        cells = []
        for k in shown:
            vals = [r["test_f1"] for r in rows
                    if r["method"] == m and r["budget_k"] == k]
            cells.append(f"{np.mean(vals):7.3f}" if vals else " " * 7)
        print("  " + m.ljust(22) + "".join(cells))


def summarise_auf(auf_rows) -> None:
    """Mean AUF (K = 10, weighted F1) per method, with its seed range."""
    if not auf_rows:
        return
    print("\nAUF, K = 10, weighted F1 -- the primary metric for H1-H3, H5, H6:")
    print(f"  {'method':<22}{'mean':>8}{'min':>8}{'max':>8}{'seeds':>7}"
          f"{'k covered':>11}")
    for m in sorted({r["method"] for r in auf_rows}):
        vals = [r["auf10_f1_weighted"] for r in auf_rows if r["method"] == m]
        cov = [r["k_covered_10"] for r in auf_rows if r["method"] == m]
        print(f"  {m:<22}{np.mean(vals):8.4f}{min(vals):8.4f}{max(vals):8.4f}"
              f"{len(vals):7d}{min(cov):>8d}-{max(cov):<2d}")


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
