"""The evaluation protocol shared by FASTENER and every baseline.

One classifier, one metric, one set of splits, used identically everywhere --
so that any difference in the results is attributable to feature selection and
not to an incidental difference in how a method was scored.
"""
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Fixed classifier for every method. FASTENER's reference implementation uses a
# decision tree, so we keep that; the point of the experiment is the feature
# subset, not the learner.
MODEL_SEED = 20200


def make_model():
    return DecisionTreeClassifier(random_state=MODEL_SEED)


# Feature budgets at which every curve is read. Every integer up to 20, because
# AUF (see analysis.auf) averages opt(k) over EACH k = 1..K, and K is 10 or 20 in
# HYPOTHESES.md; then a sparse tail for the large-k region. Callers drop the
# entries above a dataset's feature count.
K_GRID = list(range(1, 21)) + [25, 30, 50, 100, 200, 500]

# FS-SDS holds a whole run at one fixed k, so it is run once per k over this
# range and its fit budget is split evenly across it (HYPOTHESES.md: 6,000 in
# total, 300 per k). It covers exactly what AUF at K = 20 needs.
FS_SDS_K_RANGE = list(range(1, 21))

# Fit budget per run, equal across arms.
FIT_BUDGET = 6000

# Datasets whose search had not converged at FIT_BUDGET get twice as much. In
# H0 (H0-E01, H0-E02) the mean validation AUF at K = 10 of at least one arm was
# still rising by 0.005 or more over the last quarter of the 6,000 fits on
# these; on every other dataset it rose by less (HYPOTHESES.md, Revisions,
# 2026-09-30). Still equal across arms: the budget follows the dataset.
LONG_FIT_BUDGET = 12_000
LONG_BUDGET_DATASETS = frozenset({
    "nci9", "BASEHOCK", "lung_discrete", "warpAR10P", "arcene", "PCMAC",
    "TOX_171", "ORL", "RELATHE", "warpPIE10P", "CLL_SUB_111",
})


def fit_budget(dataset: str) -> int:
    """The fit budget per run on a dataset, for every arm."""
    return LONG_FIT_BUDGET if dataset in LONG_BUDGET_DATASETS else FIT_BUDGET

# Datasets with more rows than this are cut to a fixed stratified subsample of
# this many rows, identical for every arm and seed (HYPOTHESES.md, "Cost, and
# the row cap"). Measured: EOData drops from ~24 h to ~2 h per run.
ROW_CAP = 50_000


# The score that drives FASTENER's search and selects k for the baselines.
# Weighted F1 matches the reference eval_fun in fastener.py.
def primary_score(y_true, y_pred) -> float:
    return float(f1_score(y_true, y_pred, average="weighted"))


def all_scores(y_true, y_pred) -> Dict[str, float]:
    """Every metric, for later interpretation. `f1_weighted` is the primary.

    Macro F1 is always computed. Binary F1 only exists for a two-class problem,
    where it is taken on the higher-coded class; it is None otherwise. The
    paper says only "F1 score", and on a two-class set the averages differ
    substantially, so all three are kept.
    """
    labels = np.unique(np.concatenate([np.asarray(y_true), np.asarray(y_pred)]))
    binary = None
    if np.unique(y_true).size == 2:
        binary = float(f1_score(y_true, y_pred, average="binary",
                                pos_label=np.max(y_true), zero_division=0))
    return {
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted",
                                      zero_division=0)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro",
                                   labels=labels, zero_division=0)),
        "f1_binary": binary,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
    }


class FitCounter:
    """Counts model fits so each method's search cost is reported, not assumed."""

    def __init__(self) -> None:
        self.fits = 0

    def reset(self) -> None:
        self.fits = 0


def evaluate_subset(ds, features: Sequence[int], counter: FitCounter = None) -> Dict:
    """Fit on train with `features`, then score on val and test.

    This is the single place a final number is produced, for every method.
    """
    features = np.asarray(sorted(set(int(f) for f in features)), dtype=int)
    if features.size == 0:
        raise ValueError("empty feature subset")

    model = make_model().fit(ds.X_train[:, features], ds.y_train)
    if counter is not None:
        counter.fits += 1

    val = all_scores(ds.y_val, model.predict(ds.X_val[:, features]))
    test = all_scores(ds.y_test, model.predict(ds.X_test[:, features]))

    return {
        "n_features": int(features.size),
        "features": features.tolist(),
        "val": val,
        "test": test,
        "val_score": val["f1_weighted"],
        "test_score": test["f1_weighted"],
    }


def pareto_front(records: List[Dict], size_key="n_features", score_key="val_score") -> List[Dict]:
    """Keep records not dominated on (fewer features, higher score).

    Selection uses the validation score -- never the test score, which would
    leak the held-out set back into the choice of what to report.
    """
    best_by_size: Dict[int, Dict] = {}
    for r in records:
        k = r[size_key]
        if k not in best_by_size or r[score_key] > best_by_size[k][score_key]:
            best_by_size[k] = r

    front: List[Dict] = []
    best_so_far = -np.inf
    for k in sorted(best_by_size):
        r = best_by_size[k]
        if r[score_key] > best_so_far:
            front.append(r)
            best_so_far = r[score_key]
    return front
