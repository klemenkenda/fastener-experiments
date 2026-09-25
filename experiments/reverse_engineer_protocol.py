"""Reverse-engineer the FASTENER paper's evaluation protocol from its results.

The replication in `run_paper_replication.py` lands consistently ABOVE the
paper: about +0.10 AUF for FASTENER and +0.24 for FS-SDS, on every data set. A
uniform offset with a high rank correlation is the signature of a protocol
difference, not of a different search -- so this script searches the space of
protocol choices the paper leaves open and asks which combination reproduces its
numbers.

Nothing here re-runs a search. Every unit stored the subsets it selected, so
each candidate protocol is just a re-grading of those subsets.

THE OPEN CHOICES, and why each is open
--------------------------------------
1. THE TREE. "the decision tree classifier provided by the scikit-learn library
   ... using Gini index for measuring quality of a split and a requirement of
   keeping, at a minimum, two examples in a split" (Section 5.1). "Two examples
   in a split" is ambiguous: `min_samples_split=2` is scikit-learn's DEFAULT and
   says nothing, while `min_samples_leaf=2` is not the default and regularises
   every tree. The second reading makes the sentence informative, which is a
   reason to suspect it.

2. THE F1 AVERAGE. The paper says "F1 score" and never which average. On a
   two-class problem weighted is the most generous and binary the least.

3. WHO GRADES WHOM. Section 5.1 gives FASTENER a decision tree and says
   "FS-SDS uses Extreme Learning Machine (ELM) for classification ... 160 hidden
   neurons and the sigmoid activation function", in the same breath. That reads
   as each method being REPORTED under its own classifier, which would mean
   Table 3 compares a tree-scored FASTENER against an ELM-scored FS-SDS -- a
   comparison of search AND learner together. The replication deliberately
   grades everything with the tree; this script tests the other reading.

The output is the configuration minimising mean |ours - paper| per method. A
configuration that drives the residual to near zero for BOTH methods is an
explanation. One that does not leaves a genuine difference in what the searches
found, which is then the honest finding.

Usage:
    python experiments/reverse_engineer_protocol.py
    python experiments/reverse_engineer_protocol.py --splits 3 --jobs 1
"""
import argparse
import collections
import glob
import itertools
import json
import sys
import warnings
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paper_protocol as pp  # noqa: E402
import paper_tables as pt  # noqa: E402
from datasets import load_paper_benchmark_raw  # noqa: E402
from protocol import MODEL_SEED  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402

# The candidate classifiers, named as they are discussed above.
CLASSIFIERS = {
    "tree_default": lambda: DecisionTreeClassifier(random_state=MODEL_SEED),
    "tree_leaf2": lambda: DecisionTreeClassifier(random_state=MODEL_SEED,
                                                 min_samples_leaf=2),
    "elm": pp.ELMClassifier,
}
AVERAGES = ("weighted", "macro", "binary")


def auf_under(X, y, subsets, classifier: str, average: str,
              eval_seeds, K: int = pp.PAPER_K) -> float:
    subsets = [np.asarray(s, dtype=int) for s in subsets if 1 <= len(s) <= K]
    if not subsets:
        return float("nan")
    if average == "binary" and int(np.unique(y).size) != 2:
        return float("nan")
    build = CLASSIFIERS[classifier]
    aufs = []
    for seed in eval_seeds:
        tr, te = pp.split_80_20(X, y, seed)
        items = []
        for feats in subsets:
            model = build().fit(X[np.ix_(tr, feats)], y[tr])
            pred = model.predict(X[np.ix_(te, feats)])
            items.append({"n_features": int(feats.size),
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
    ap.add_argument("--splits", type=int, default=2,
                    help="feature-selection splits to re-grade per cell")
    ap.add_argument("--eval-splits", type=int, default=10,
                    help="evaluation splits per re-grading (paper: 30; fewer "
                         "is enough to locate a 0.1-sized offset)")
    ap.add_argument("--methods", default="fastener,fs_sds")
    args = ap.parse_args()

    runs = sorted(RESULTS_DIR.glob(f"*{args.run}*" if args.run
                                   else "*paper_replication"))
    if not runs:
        raise SystemExit("no replication run found")
    run_dir = runs[-1]
    by = load_units(run_dir)
    eval_seeds = pp.EVAL_SPLIT_SEEDS[:args.eval_splits]
    methods = [m.strip() for m in args.methods.split(",")]

    names = sorted({d for d, _ in by if d in pt.PUBLISHED_TABLE_3})
    print(f"run: {run_dir.name}")
    print(f"{len(names)} data set(s), {args.splits} fs-split(s) x "
          f"{len(eval_seeds)} eval split(s) per cell\n")

    # ours[(method, classifier, average)][dataset] = AUF
    ours: Dict = collections.defaultdict(dict)
    for name in names:
        X, y, _ = load_paper_benchmark_raw(name)
        for method in methods:
            units = by.get((name, method))
            if not units or not pt.published(name, method):
                continue
            for classifier, average in itertools.product(CLASSIFIERS, AVERAGES):
                vals = [auf_under(X, y, u["subsets"], classifier, average,
                                  eval_seeds)
                        for u in units[:args.splits]]
                vals = [v for v in vals if v == v]
                if vals:
                    ours[(method, classifier, average)][name] = float(
                        np.mean(vals))
        print(f"  re-graded {name}")

    # ---- which configuration reproduces the paper? ----------------------
    print("\nmean signed difference from the paper (ours - paper), by protocol")
    for method in methods:
        print(f"\n  {method}")
        print(f"    {'classifier':<14}{'average':<10}{'n':>4}{'mean delta':>12}"
              f"{'mean |delta|':>14}")
        scored = []
        for classifier, average in itertools.product(CLASSIFIERS, AVERAGES):
            cell = ours.get((method, classifier, average), {})
            deltas = [v - pt.published(d, method)["mean"]
                      for d, v in cell.items()]
            if not deltas:
                continue
            arr = np.asarray(deltas, dtype=float)
            scored.append((float(np.abs(arr).mean()), classifier, average,
                           float(arr.mean()), arr.size))
        for absd, classifier, average, signed, n in sorted(scored):
            print(f"    {classifier:<14}{average:<10}{n:>4}{signed:>+12.3f}"
                  f"{absd:>14.3f}")
        if scored:
            best = min(scored)
            print(f"    -> closest: {best[1]} + {best[2]} F1  "
                  f"(mean |delta| {best[0]:.3f})")

    print("\nRead this as follows. A configuration whose mean |delta| is small")
    print("for BOTH methods is a plausible reconstruction of the paper's")
    print("protocol. If the best configuration still leaves a large residual on")
    print("one method only, the difference is in what that method's search")
    print("found here, not in how it was graded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
