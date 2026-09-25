"""Why do our AUFs sit above the FASTENER paper's, and what closes the gap?

A replication that lands consistently high is not automatically wrong -- but the
reason has to be found rather than asserted. This script works through the
candidate explanations in order of cheapness, using the subsets every unit
stored, so none of it needs the searches to be run again.

The candidates, and what each would look like:

1. THE F1 AVERAGE. The paper says "F1 score" and never which average. On a
   two-class set weighted F1 is the most generous and binary the least. If this
   is the cause, our numbers under `binary` should land on the paper's.

2. THE EVALUATION CLASSIFIER. The paper drives FS-SDS with an ELM and FASTENER
   with a decision tree, and never says which one grades the selected subsets in
   the 30-split evaluation phase. `run_paper_replication` grades everything with
   the tree, so that the phase compares subsets rather than subsets-plus-their-
   classifier. If the paper instead graded each method with its own classifier,
   FS-SDS's published AUF would be an ELM score, and re-grading ours with an ELM
   should move it toward the paper's.

3. NEITHER, i.e. a genuine difference in what the searches find. The most likely
   source is the FS-SDS objective: the authors' reference implementation
   re-splits the data on EVERY evaluation, so the same subset scores differently
   each time and the search partly chases split noise. The objective here is
   deterministic, which makes the same algorithm strictly better informed. That
   would raise our FS-SDS above the paper's without anything being wrong in
   either.

Usage:
    python experiments/diagnose_gap.py                    # newest run
    python experiments/diagnose_gap.py --run <run_id> --datasets ALLAML,arcene
"""
import argparse
import collections
import glob
import json
import sys
import warnings
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.metrics import f1_score

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paper_protocol as pp  # noqa: E402
import paper_tables as pt  # noqa: E402
from datasets import load_paper_benchmark_raw  # noqa: E402
from protocol import make_model  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402


def auf_regraded(X, y, subsets, model_factory, average: str = "weighted",
                 K: int = pp.PAPER_K) -> float:
    """AUF for stored subsets under a chosen classifier and F1 average."""
    subsets = [np.asarray(s, dtype=int) for s in subsets if 1 <= len(s) <= K]
    if not subsets:
        return float("nan")
    n_classes = int(np.unique(y).size)
    if average == "binary" and n_classes != 2:
        return float("nan")
    aufs = []
    for seed in pp.EVAL_SPLIT_SEEDS:
        tr, te = pp.split_80_20(X, y, seed)
        items = []
        for feats in subsets:
            model = model_factory().fit(X[np.ix_(tr, feats)], y[tr])
            pred = model.predict(X[np.ix_(te, feats)])
            items.append({
                "n_features": int(feats.size),
                "score": float(f1_score(y[te], pred, average=average,
                                        zero_division=0))})
        aufs.append(pp.auf(items, K))
    return float(np.mean(aufs))


def load_units(run_dir: Path) -> Dict:
    by = collections.defaultdict(list)
    for f in sorted(glob.glob(str(run_dir / "partial" / "*.json"))):
        with open(f, encoding="utf-8") as fh:
            u = json.load(fh)
        if not u.get("failed") and u.get("subsets"):
            by[(u["dataset"], u["method"])].append(u)
    return by


def main() -> int:
    warnings.filterwarnings("ignore")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None)
    ap.add_argument("--datasets", default=None,
                    help="comma-separated subset; default every data set with "
                         "a published row")
    ap.add_argument("--splits", type=int, default=3,
                    help="feature-selection splits to re-grade per cell "
                         "(re-grading is a fresh 30-split evaluation each, so "
                         "this is the cost knob)")
    args = ap.parse_args()

    if args.run:
        matches = sorted(RESULTS_DIR.glob(f"*{args.run}*"))
        run_dir = Path(args.run) if Path(args.run).is_dir() else (
            matches[-1] if matches else None)
    else:
        matches = sorted(RESULTS_DIR.glob("*paper_replication"))
        run_dir = matches[-1] if matches else None
    if run_dir is None:
        raise SystemExit("no replication run found")

    by = load_units(run_dir)
    print(f"run: {run_dir.name}")

    names = ([n.strip() for n in args.datasets.split(",")]
             if args.datasets
             else sorted({d for d, _ in by if d in pt.PUBLISHED_TABLE_3}))

    # ---- candidate 1: the F1 average, free from what is already stored ----
    print("\n[1] AUF under each F1 average (no recomputation)")
    print(f"  {'data set':<14}{'method':<11}{'weighted':>9}{'macro':>8}"
          f"{'binary':>8}{'paper':>8}  closest")
    for name in names:
        for method in ("fastener", "fs_sds"):
            units = by.get((name, method))
            pub = pt.published(name, method)
            if not units or not pub:
                continue
            vals = {a: pp.aggregate(units, average=a)["mean"]
                    for a in pp.F1_AVERAGES}
            live = {a: v for a, v in vals.items() if v is not None}
            closest = (min(live, key=lambda a: abs(live[a] - pub["mean"]))
                       if live else "-")
            cell = lambda v: f"{v:>8.3f}" if v is not None else f"{'--':>8}"
            print(f"  {name:<14}{method:<11}{cell(vals['weighted'])}"
                  f"{cell(vals['macro'])}{cell(vals['binary'])}"
                  f"{pub['mean']:>8.3f}  {closest}")

    # ---- candidate 2: the evaluation classifier --------------------------
    print(f"\n[2] Re-grading the stored subsets with an ELM "
          f"(first {args.splits} split(s) per cell)")
    print(f"  {'data set':<14}{'method':<11}{'tree':>8}{'ELM':>8}{'paper':>8}"
          f"{'residual':>10}")
    residuals = collections.defaultdict(list)
    for name in names:
        X, y, _ = load_paper_benchmark_raw(name)
        for method in ("fastener", "fs_sds"):
            units = by.get((name, method))
            pub = pt.published(name, method)
            if not units or not pub:
                continue
            tree_v, elm_v = [], []
            for u in units[:args.splits]:
                tree_v.append(auf_regraded(X, y, u["subsets"], make_model))
                elm_v.append(auf_regraded(X, y, u["subsets"], pp.ELMClassifier))
            t, e = float(np.mean(tree_v)), float(np.mean(elm_v))
            resid = e - pub["mean"]
            residuals[method].append(resid)
            print(f"  {name:<14}{method:<11}{t:>8.3f}{e:>8.3f}"
                  f"{pub['mean']:>8.3f}{resid:>+10.3f}")

    print("\n[3] What is left after the ELM explanation")
    for method, vals in sorted(residuals.items()):
        arr = np.asarray(vals, dtype=float)
        print(f"  {method:<11} mean residual {arr.mean():+.3f} "
              f"over {arr.size} data set(s)")
    print("  A residual near zero means the evaluation classifier explained the")
    print("  gap. A residual that stays positive means the searches here found")
    print("  genuinely better subsets than the paper's runs did -- report that")
    print("  as a difference in the experiment, not as a defect in either.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
