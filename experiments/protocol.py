"""The evaluation protocol shared by FASTENER and every baseline.

One classifier, one metric, one set of splits, used identically everywhere --
so that any difference in the results is attributable to feature selection and
not to an incidental difference in how a method was scored.
"""
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Fixed classifier for every method. FASTENER's reference implementation uses a
# decision tree, so we keep that; the point of the experiment is the feature
# subset, not the learner.
MODEL_SEED = 20200

# The protocol classifier is one per process: every search, every filter that
# fits a model (Boruta, RFE, the tree-importance ranker) and every final score
# use `make_model()`, so switching it here switches it everywhere at once.
# "tree" is the default and every experiment up to H5H6-E01; "rf" is the
# random forest of H5H6-E02 (DEC-41), at scikit-learn's defaults with 100
# trees. Its thread count only splits the trees over cores: a forest with a
# fixed random_state is the same at any n_jobs, so it is not part of an arm's
# configuration. "lgbm" is LightGBM, of H5H6-E03 (DEC-44): LightGBM's
# defaults (100 trees, 31 leaves, learning rate 0.1) except the smallest
# leaf, which follows the training split -- see lgbm_min_child_samples --
# and deterministic=True, so its results too are the same at any thread
# count.
MODELS = ("tree", "rf", "lgbm")
RF_TREES = 100
LGBM_TREES = 100
_MODEL = {"name": "tree", "n_jobs": 1, "n_train": None}


def set_model(name: str, n_jobs: int = 1) -> None:
    """Select the protocol classifier for this process ("tree", "rf" or
    "lgbm"). LightGBM also needs the training split's size: set_train_rows."""
    if name not in MODELS:
        raise ValueError(f"unknown protocol model {name!r}; have {MODELS}")
    _MODEL.update(name=name, n_jobs=max(1, int(n_jobs)), n_train=None)


def set_train_rows(n_train: int) -> None:
    """The training split's size, which LightGBM's smallest leaf follows."""
    _MODEL["n_train"] = int(n_train)


def lgbm_min_child_samples(n_train: int) -> int:
    """LightGBM's smallest leaf for a training split of `n_train` rows.

    LightGBM's default, 20 rows, leaves the smallest datasets nearly
    unlearnable: on Coffee (34 training rows) and BeetleFly (24) one
    10-feature subset scored validation F1 0.39 and 0.33 at the default, 0.62
    and 0.73 with leaves of one row, while on the large sets the default
    scored a little higher (EOData 0.54 against 0.52). So the leaf scales
    with the split: a twentieth of its rows, at least 1, at most LightGBM's
    20 (DEC-44).
    """
    return min(20, max(1, n_train // 20))


def model_name() -> str:
    return _MODEL["name"]


def model_description() -> str:
    """The classifier as recorded in manifests and hashed into algorithm IDs.

    For LightGBM it names the leaf rule, not one dataset's value, so an arm
    keeps one configuration across datasets.
    """
    if _MODEL["name"] == "rf":
        return f"RandomForestClassifier({RF_TREES} trees)"
    if _MODEL["name"] == "lgbm":
        return (f"LGBMClassifier({LGBM_TREES} trees, min_child_samples="
                f"min(20, max(1, n_train // 20)), deterministic)")
    return "DecisionTreeClassifier"


def make_model():
    if _MODEL["name"] == "rf":
        return RandomForestClassifier(n_estimators=RF_TREES,
                                      random_state=MODEL_SEED,
                                      n_jobs=_MODEL["n_jobs"])
    if _MODEL["name"] == "lgbm":
        if _MODEL["n_train"] is None:
            raise RuntimeError("LightGBM's leaf follows the training split: "
                               "call protocol.set_train_rows first")
        from lightgbm import LGBMClassifier
        return LGBMClassifier(
            n_estimators=LGBM_TREES, random_state=MODEL_SEED,
            n_jobs=_MODEL["n_jobs"], deterministic=True, force_col_wise=True,
            min_child_samples=lgbm_min_child_samples(_MODEL["n_train"]),
            verbose=-1)
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
    return weighted_f1(y_true, y_pred)


def weighted_f1(y_true, y_pred) -> float:
    """`f1_score(y_true, y_pred, average="weighted")`, without its overhead.

    The searches call this thousands of times per run on small arrays, where
    scikit-learn's parameter validation and multilabel confusion matrix cost
    about 3.5 ms a call -- more than a tree fit on wide data. The arithmetic is
    scikit-learn's, in its order: per label in the union of both arrays,
    F = 2 tp / (true + predicted), 0 where both are 0, then averaged with
    `np.average` weighted by the true counts. `tests/test_protocol_f1.py`
    checks equality, bit for bit.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    labels, inv = np.unique(np.concatenate([y_true, y_pred]),
                            return_inverse=True)
    n_labels = labels.shape[0]
    t, p = inv[:y_true.shape[0]], inv[y_true.shape[0]:]
    true_sum = np.bincount(t, minlength=n_labels)
    pred_sum = np.bincount(p, minlength=n_labels)
    tp_sum = np.bincount(t[t == p], minlength=n_labels)
    denom = 1.0 * true_sum.astype(np.float64) + pred_sum.astype(np.float64)
    zero = denom == 0
    denom[zero] = 1
    f = 2.0 * tp_sum.astype(np.float64) / denom
    f[zero] = 0.0
    return float(np.average(f, weights=true_sum))


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


def evaluate_subset(ds, features: Sequence[int], counter: FitCounter = None,
                    model_factory=None) -> Dict:
    """Fit on train with `features`, then score on val and test.

    This is the single place a final number is produced, for every method.
    `model_factory` is the classifier that scores the subset; it defaults to
    the protocol classifier (`make_model`), and is the ELM for an arm whose
    search the ELM drove (H4-E02), so an arm is always judged by its own
    classifier.
    """
    features = np.asarray(sorted(set(int(f) for f in features)), dtype=int)
    if features.size == 0:
        raise ValueError("empty feature subset")

    model = (model_factory or make_model)().fit(ds.X_train[:, features],
                                                ds.y_train)
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
