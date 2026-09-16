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


# The score that drives FASTENER's search and selects k for the baselines.
# Weighted F1 matches the reference eval_fun in fastener.py.
def primary_score(y_true, y_pred) -> float:
    return float(f1_score(y_true, y_pred, average="weighted"))


def all_scores(y_true, y_pred) -> Dict[str, float]:
    return {
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
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
