"""Replicate the FASTENER paper's benchmark tables.

Target: Koprivec, Kenda & Sircelj, Entropy 2020, 22(11), 1198 -- Table 3
(FS-SDS vs FASTENER, AUF over 25 scikit-feature benchmarks) and the FASTENER
column of Table 4.

WHAT THIS IS AND IS NOT
-----------------------
It runs the paper's own protocol (`paper_protocol.py`): 80:20 stratified splits,
the search scored on the F1 of the split's TEST set, AUF with K = 20, then each
selected subset re-scored on 30 further 80:20 splits. Those numbers are
optimistic by construction, and are labelled that way everywhere they appear.

Three deviations from the paper, each forced and each recorded in the manifest:

1. FS-SDS BUDGET. The paper gives FS-SDS 30,000 model evaluations PER k. At
   K = 20 that is 600,000 fits per run, and at 10 splits x 25 data sets it is
   150 million -- measured at this machine's throughput (9-430 fits/second
   depending on the data set) that is weeks. FS-SDS is run at 6,000 per k here,
   a fifth of the paper's. Its AUF is therefore a LOWER BOUND on what the
   paper's budget would give, and the gap must not be read as the method
   failing.

2. POSS IS NOT IN THE PAPER'S TABLES. The paper compares POSS only on EOData
   (its Table 2), not on these 25. POSS is included here at FASTENER's budget as
   an EXTENSION, and is reported in its own column, never as a replication.

3. FS-SDS IS RUN TWICE. The paper drives FS-SDS with an Extreme Learning Machine
   (160 hidden sigmoid units) and FASTENER with a decision tree, which confounds
   the search with the classifier. `fs_sds_elm` matches the paper; `fs_sds`
   drives the same search with the shared decision tree. The pair separates
   "this search is worse" from "this classifier is different". Both are graded
   by the same decision tree in the evaluation phase, so only the search differs.

Usage:
    python experiments/run_paper_replication.py --quick          # 2 sets, 2 splits
    python experiments/run_paper_replication.py --jobs 7
    python experiments/run_paper_replication.py --datasets colon,ALLAML
    python experiments/run_paper_replication.py --methods fastener,poss
"""
import argparse
import csv
import json
import os
import sys
import time
import traceback
import warnings
from pathlib import Path
from typing import Dict, List

# Pin every worker to a single BLAS thread, BEFORE numpy is imported -- these
# are read at load time and ignored afterwards. Without this each of the 7
# worker processes starts its own 8-thread pool on an 8-core machine, and the 56
# threads spend their time descheduling each other: the first launch of this
# script ran at ~14% CPU and about a seventh of single-process speed. The work
# is already parallel across units, so per-worker threading buys nothing.
for _var in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_var, "1")

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paper_protocol as pp  # noqa: E402
import sota_baselines as sota  # noqa: E402
from datasets import PAPER_BENCHMARKS, load_paper_benchmark_raw  # noqa: E402
from provenance import Run  # noqa: E402
from run_fastener import run_fastener  # noqa: E402

# The paper's FASTENER setting is 200 generations in an "exploration setting
# (larger generations)", which it reports costing 11,238-16,670 model fits
# depending on the data set. Rounds are what the paper fixes, so rounds are what
# is fixed here; the fit count is an OUTCOME, reported per run and directly
# comparable with the paper's eval_n column.
#
# The paper does not give the pool size for those benchmark runs (it names 3 for
# the EO experiments, which is a different, cheaper setting). Calibrated here on
# colon: pool 3 gives 8.6 fits/round -> ~1,700 at 200 rounds, sevenfold BELOW
# the paper; pool 10 gives 62 fits/round -> ~12,400, inside the paper's range.
# So pool 10 is what "larger generations" is taken to mean. Running the default
# 3 would have handed FASTENER a seventh of the paper's compute and then
# reported the result as a replication.
FASTENER_ROUNDS = 200
FASTENER_POOL_SIZE = 10
FASTENER_BUCKET_SIZE = 10

# POSS is the extension arm; it gets the middle of FASTENER's measured range so
# that it is neither advantaged nor handicapped on compute.
POSS_EVALUATIONS = 13000

# FS-SDS: a fifth of the paper's 30,000 per k. See deviation 1 above.
FS_SDS_EVALUATIONS_PER_K = 6000

METHODS = ("fastener", "poss", "fs_sds", "fs_sds_elm")

# Smallest first, so partial results cover the most data sets per hour spent and
# the two that dominate the bill (gisette, USPS) cannot block everything else.
ORDER_BY_COST = sorted(
    PAPER_BENCHMARKS,
    key=lambda n: {"USPS": 3, "gisette": 2}.get(n, 0))


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default=None,
                    help="comma-separated subset; default all 25, cheapest first")
    ap.add_argument("--methods", default=",".join(METHODS),
                    help=f"comma-separated subset of {','.join(METHODS)}")
    ap.add_argument("--splits", type=int, default=len(pp.FS_SPLIT_SEEDS),
                    help="number of feature-selection splits (paper: 10)")
    ap.add_argument("--fastener-rounds", type=int, default=FASTENER_ROUNDS)
    ap.add_argument("--fastener-pool", type=int, default=FASTENER_POOL_SIZE,
                    help="mating pool and bucket size; 10 reproduces the "
                         "paper's reported evaluation counts at 200 rounds")
    ap.add_argument("--poss-evaluations", type=int, default=POSS_EVALUATIONS)
    ap.add_argument("--fs-sds-per-k", type=int, default=FS_SDS_EVALUATIONS_PER_K)
    ap.add_argument("--resume-from", default=None,
                    help="a previous run id/dir whose finished units should be "
                         "copied in before starting. Units are keyed by "
                         "(data set, method, split), so an interrupted run "
                         "continues instead of repeating work. Pass "
                         "--resume-skip to leave stale methods behind.")
    ap.add_argument("--resume-skip", default="",
                    help="comma-separated methods NOT to carry over from "
                         "--resume-from, for when their code has changed")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--name", default=None)
    return ap.parse_args()


def subsets_from(result: Dict, K: int = pp.PAPER_K) -> List[List[int]]:
    """The subsets a method offers, capped at the sizes AUF can use."""
    out = []
    for rec in result.get("records", []):
        feats = rec.get("features")
        if feats and 1 <= len(feats) <= K:
            out.append(list(feats))
    return out


def run_one(method: str, name: str, fs_seed: int, args, run_dir: Path) -> Dict:
    """One (data set, method, feature-selection split) unit.

    Returns the AUF statistics over the 30 evaluation splits, plus the cost of
    the search in model fits -- the paper's eval_n column.
    """
    X, y, dropped = load_paper_benchmark_raw(name)
    ds = pp.paper_dataset(name, X, y, fs_seed)
    ks = list(range(1, pp.PAPER_K + 1))

    t0 = time.time()
    if method == "fastener":
        # FASTENER names its log directory "log/fastener_seed<seed>" relative to
        # the working directory and refuses to reuse one, so every unit needs a
        # directory of its own -- the same seed recurs on all 25 data sets.
        work = run_dir / "fastener_work" / name
        work.mkdir(parents=True, exist_ok=True)
        # rounds, not a fit cap: the paper fixes generations and reports the
        # resulting fit count, so a cap here would overwrite the very number
        # being compared.
        res = run_fastener(ds, work, seed=fs_seed,
                           rounds=args.fastener_rounds,
                           pool_size=args.fastener_pool,
                           max_bucket_size=args.fastener_pool,
                           # ~95 MB of generation pickles per unit that
                           # nothing reads; over 250 units that is ~24 GB of
                           # disk. (Measured: it costs no wall time -- the
                           # search dominates -- so this is a disk decision,
                           # not a speed one.)
                           dump_logs=False)
        fits = res.get("model_fits")
    elif method == "poss":
        res = sota.run_poss_method(ds, seed=fs_seed,
                                   stop_evaluations=args.poss_evaluations,
                                   k=pp.PAPER_K)
        fits = res.get("model_fits")
    elif method in ("fs_sds", "fs_sds_elm"):
        factory = pp.ELMClassifier if method == "fs_sds_elm" else None
        res = sota.run_fs_sds_method(ds, ks, seed=fs_seed,
                                     stop_evaluations=args.fs_sds_per_k,
                                     model_factory=factory, label=method)
        fits = res.get("model_fits")
    else:
        raise ValueError(method)
    search_seconds = time.time() - t0

    subsets = subsets_from(res)
    stats = pp.evaluate_front(X, y, subsets)
    # Sizes offered, so a front that never reached small k is visible in the
    # unit file rather than only as a depressed AUF.
    stats["subset_sizes"] = sorted(len(s) for s in subsets)

    return {
        "dataset": name,
        "method": method,
        "fs_split_seed": fs_seed,
        "search_model_fits": fits,
        "search_seconds": round(search_seconds, 2),
        "n_subsets_offered": len(subsets),
        "dropped_small_classes": dropped,
        **stats,
    }


def main() -> int:
    warnings.filterwarnings("ignore")
    args = parse_args()

    names = ([n.strip() for n in args.datasets.split(",") if n.strip()]
             if args.datasets else list(ORDER_BY_COST))
    unknown = [n for n in names if n not in PAPER_BENCHMARKS]
    if unknown:
        raise SystemExit(f"unknown dataset(s): {unknown}")
    methods = [m.strip() for m in args.methods.split(",") if m.strip()]
    unknown = [m for m in methods if m not in METHODS]
    if unknown:
        raise SystemExit(f"unknown method(s): {unknown}; have {list(METHODS)}")

    if args.quick:
        names = names[:2]
        args.splits = 2
        args.fastener_rounds = 20
        args.fastener_pool = 3
        args.poss_evaluations = 300
        args.fs_sds_per_k = 150

    fs_seeds = list(pp.FS_SPLIT_SEEDS[:args.splits])
    name = args.name or ("paper_replication" + ("_quick" if args.quick else ""))

    params = {
        "target": "Koprivec, Kenda & Sircelj, Entropy 2020 -- Tables 3 and 4",
        "protocol": "paper (80:20, search scored on the test split)",
        "auf_K": pp.PAPER_K,
        "datasets": names,
        "methods": methods,
        "fs_split_seeds": fs_seeds,
        "eval_split_seeds": list(pp.EVAL_SPLIT_SEEDS),
        "fastener_rounds": args.fastener_rounds,
        "fastener_pool_size": args.fastener_pool,
        "fastener_paper_eval_n_range": [11238, 16670],
        "poss_evaluations": args.poss_evaluations,
        "fs_sds_evaluations_per_k": args.fs_sds_per_k,
        "fs_sds_paper_evaluations_per_k": 30000,
        "elm_hidden": pp.ELM_HIDDEN,
        "eval_classifier": "DecisionTreeClassifier (all methods)",
        "quick": args.quick,
        "caveats": [
            "Paper protocol: the search is driven by the same test split the "
            "score is read from. These AUFs are optimistic by construction.",
            f"FS-SDS runs at {args.fs_sds_per_k} evaluations per k against the "
            "paper's 30000; its AUF is a lower bound.",
            "POSS is not in the paper's benchmark tables -- it is compared "
            "there only on EOData. It is an extension here, not a replication.",
        ],
    }

    with Run(name, params) as run:
        print(f"run dir: {run.dir}")
        partial_dir = run.dir / "partial"
        partial_dir.mkdir(exist_ok=True)

        if args.resume_from:
            src = Path(args.resume_from)
            if not src.is_dir():
                matches = sorted(Path("results").glob(f"*{args.resume_from}*"))
                if not matches:
                    raise SystemExit(f"no run matching {args.resume_from!r}")
                src = matches[-1]
            skip = {m.strip() for m in args.resume_skip.split(",") if m.strip()}
            copied = 0
            for f in sorted((src / "partial").glob("*.json")):
                # Filename is "<dataset>__<method>__<seed>.json".
                method_of = f.stem.split("__")[1] if "__" in f.stem else ""
                if method_of in skip:
                    continue
                target = partial_dir / f.name
                if not target.exists():
                    target.write_bytes(f.read_bytes())
                    copied += 1
            print(f"resumed {copied} finished unit(s) from {src.name}"
                  + (f", skipping {sorted(skip)}" if skip else ""))
            run.record("resumed_from", {"run": src.name, "units": copied,
                                        "skipped_methods": sorted(skip)})

        tasks = [(m, n, s) for n in names for m in methods for s in fs_seeds]
        print(f"{len(tasks)} units: {len(names)} data sets x {len(methods)} "
              f"methods x {len(fs_seeds)} splits, on {args.jobs} workers")

        def task(method: str, name_: str, fs_seed: int) -> Dict:
            # One file per unit, written the moment it finishes: a run this long
            # must survive being killed, and must be resumable.
            out_path = partial_dir / f"{name_}__{method}__{fs_seed}.json"
            if out_path.exists():
                with open(out_path, encoding="utf-8") as fh:
                    return json.load(fh)
            try:
                res = run_one(method, name_, fs_seed, args, run.dir)
            except Exception as exc:
                return {"dataset": name_, "method": method,
                        "fs_split_seed": fs_seed, "aufs": [],
                        "failed": f"{type(exc).__name__}: {exc}",
                        "traceback": traceback.format_exc()}
            with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(res, fh, default=str)
            return res

        from joblib import Parallel, delayed
        t0 = time.time()
        results = Parallel(n_jobs=args.jobs, prefer="processes", verbose=10)(
            delayed(task)(m, n, s) for m, n, s in tasks)
        elapsed = time.time() - t0

        failures = {f"{r['dataset']}/{r['method']}/{r['fs_split_seed']}":
                    r["failed"] for r in results if r.get("failed")}
        ok = [r for r in results if not r.get("failed")]
        run.write_json("units.json", results)
        if failures:
            run.record("failures", failures)
            print(f"\n{len(failures)} unit(s) failed")

        # ---- the tables -------------------------------------------------
        rows = []
        for name_ in names:
            for method in methods:
                units = [r for r in ok if r["dataset"] == name_
                         and r["method"] == method]
                if not units:
                    continue
                agg = pp.aggregate(units)
                fits = [u["search_model_fits"] for u in units
                        if u.get("search_model_fits") is not None]
                rows.append({
                    "dataset": name_,
                    "method": method,
                    "mean": agg["mean"], "max": agg["max"],
                    "median": agg["median"], "sd": agg["sd"],
                    "n_auf_values": agg["n"],
                    "eval_n": int(round(float(np.mean(fits)))) if fits else None,
                    "n_splits": len(units),
                    "search_seconds_total": round(
                        sum(u["search_seconds"] for u in units), 1),
                })

        run.write_json("table_rows.json", rows)
        csv_path = run.dir / "paper_tables.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else
                               ["dataset", "method"])
            w.writeheader()
            w.writerows(rows)

        run.record("cost", {"wall_seconds": round(elapsed, 1),
                            "jobs": args.jobs, "units": len(tasks)})
        print(f"\nwrote {csv_path.name} ({len(rows)} rows) in {elapsed/60:.1f} min")
        print_tables(rows, methods)

    print(f"\nmanifest: {run.dir / 'manifest.json'}")
    return 1 if failures else 0


def print_tables(rows, methods) -> None:
    """Print one block per method, in the paper's own column order.

    One block per method rather than the paper's side-by-side pairs: at four
    methods a single row would be 160 characters wide and unreadable in a
    terminal. paper_tables.csv carries the same numbers for side-by-side use.
    """
    by = {(r["dataset"], r["method"]): r for r in rows}
    datasets = sorted({r["dataset"] for r in rows})
    print("\nAUF, paper protocol (K=20, 80:20 splits, search scored on the "
          "test split -- OPTIMISTIC by construction)")
    for m in methods:
        print(f"\n  {m}")
        print(f"    {'Data Set':<16}{'Mean':>8}{'Max':>8}{'Medi':>8}"
              f"{'sd':>8}{'eval_n':>10}{'splits':>8}")
        print("    " + "-" * 66)
        for d in datasets:
            r = by.get((d, m))
            if r is None or r["mean"] is None:
                print(f"    {d:<16}{'--':>8}")
                continue
            print(f"    {d:<16}{r['mean']:>8.3f}{r['max']:>8.3f}"
                  f"{r['median']:>8.3f}{r['sd']:>8.3f}"
                  f"{(r['eval_n'] or 0):>10,}{r['n_splits']:>8}")


if __name__ == "__main__":
    raise SystemExit(main())
