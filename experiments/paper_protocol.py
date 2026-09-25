"""The FASTENER paper's own evaluation protocol, for replicating its tables.

Source: Koprivec, Kenda & Sircelj, "FASTENER: Feature Selection for Inference
from Earth Observation Data", Entropy 2020, 22(11), 1198, Sections 5.1 and 5.4.

This module deliberately reproduces a protocol that `protocol.py` was written to
avoid. Both exist on purpose:

  protocol.py       train / val / test. The search is driven by VALIDATION, the
                    test split is touched once. Honest, and the numbers come in
                    lower.
  paper_protocol.py 80:20 train/test. The search is driven by the F1 score ON
                    THE TEST SPLIT, exactly as Section 5.1 describes. This is
                    what produces the paper's numbers, and it is optimistic by
                    construction -- feature selection has seen the data the
                    score is read from.

Use this one only to replicate the paper. Do not mix its numbers into the
clean-protocol comparison, and never report an AUF from here as if it were an
out-of-sample result.

WHAT THE PAPER SPECIFIES, quoted or closely paraphrased
-------------------------------------------------------
* "The data for feature selection were first split into training and test subset
  (80:20) with stratified random split (sklearn.model_selection.train_test_split
  with a random state 2020 was used). The selected algorithm was run on a
  training subset, where the accuracy score was calculated as the F1 score of
  the resulting model on a test set."
* "For each of the algorithms, 10 different data splits were used for feature
  selection and each feature subset was tested on 30 different test/train data
  splits."
* "a set of 80:20 training/test balanced splits were done using random seeds
  from 20 to 50" -- i.e. the 30 EVALUATION splits are seeds 20..49.
* AUF := (1/K) * sum_{k=1..K} opt(k), where opt(k) = max{item.result : |item| <=
  k}, with K = 20. "the AUF measures the average of the best scoring items with
  a size of less than K."
* FASTENER: decision tree (Gini, min 2 samples per split), mating pool size 3,
  information-gain crossover, 200 generations in the "exploration setting".
* FS-SDS: "uses Extreme Learning Machine (ELM) for classification... configured
  with 160 hidden neurons and the sigmoid activation function", 30,000 model
  evaluations per k.

WHAT IT DOES NOT SPECIFY, and what is assumed here
---------------------------------------------------
* The seeds of the 10 FEATURE-SELECTION splits. The paper names random_state
  2020 for "the" split and then says 10 were used. FS_SPLIT_SEEDS below is
  2020..2029, which contains the stated one; this is an inference, not the
  paper's text.
* Which classifier scores a subset in the 30-split EVALUATION phase. Here it is
  the decision tree for EVERY method, so that the phase compares SUBSETS rather
  than subsets-plus-their-search-classifier. This matters for FS-SDS, whose
  search uses an ELM: under this choice the ELM affects what FS-SDS looks for,
  not how its answer is graded.
* Whether F1 is binary, macro or weighted. The paper says only "F1 score", and
  on a two-class set the choice moves the AUF substantially. All three are
  computed and stored per evaluation split; `PRIMARY_AVERAGE` (weighted,
  matching `protocol.py`) is what the headline tables use, and the others are
  there so the question can be answered from a finished run instead of a
  re-run.
* ELM input scaling. Standardised on the training split; an ELM on raw
  gene-expression columns is numerically hopeless, and the paper does not say
  otherwise.
"""
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datasets import Dataset  # noqa: E402
from protocol import make_model  # noqa: E402

# AUF is normalised over k = 1..K. The paper fixes K = 20 "because the selected
# feature subsets rarely have more than 20 features".
PAPER_K = 20

TEST_FRACTION = 0.20

# The 10 feature-selection splits (inferred -- see the module docstring).
FS_SPLIT_SEEDS = tuple(range(2020, 2030))
# The 30 evaluation splits: "random seeds from 20 to 50".
EVAL_SPLIT_SEEDS = tuple(range(20, 50))

ELM_HIDDEN = 160


# --------------------------------------------------------------------- splits
def split_80_20(X: np.ndarray, y: np.ndarray, seed: int):
    """The paper's split, made with the function the paper names."""
    idx = np.arange(y.shape[0])
    tr, te = train_test_split(idx, test_size=TEST_FRACTION, random_state=seed,
                              stratify=y)
    return tr, te


def paper_dataset(name: str, X: np.ndarray, y: np.ndarray, seed: int) -> Dataset:
    """A Dataset whose VALIDATION split IS its test split.

    That is the whole of the paper's protocol, expressed in the object the
    searches already take: every search in this repo drives itself on
    `X_val`/`y_val`, so pointing those at the test split reproduces Section
    5.1's "accuracy score was calculated as the F1 score of the resulting model
    on a test set" without touching any search code.

    The duplication is deliberate and is why this lives in its own module rather
    than being an option on `datasets.load`.
    """
    tr, te = split_80_20(X, y, seed)
    ds = Dataset(name, X[tr], y[tr], X[te], y[te], X[te], y[te])
    ds.paper_protocol = True
    ds.fs_split_seed = seed
    return ds


# ------------------------------------------------------------------------ ELM
class ELMClassifier:
    """Extreme Learning Machine (Huang, Zhu & Siew 2006), the paper's FS-SDS
    classifier: 160 hidden neurons, sigmoid activation.

    A single hidden layer whose input weights are RANDOM AND NEVER TRAINED; only
    the output layer is solved, in closed form by least squares. That is the
    whole method -- it is fast because there is no iterative training.

    The random weights are drawn from a FIXED seed rather than a global RNG, so
    that scoring the same subset twice gives the same answer. The searches cache
    on subset identity; a classifier that quietly re-randomised would make that
    cache wrong and the fit budget meaningless.
    """

    def __init__(self, n_hidden: int = ELM_HIDDEN, seed: int = 20200):
        self.n_hidden = n_hidden
        self.seed = seed

    def fit(self, X: np.ndarray, y: np.ndarray) -> "ELMClassifier":
        X = np.asarray(X, dtype=np.float64)
        self.classes_ = np.unique(y)

        # Standardise on train; an ELM on raw gene-expression scales saturates
        # the sigmoid and returns a constant.
        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        self.scale_[self.scale_ == 0] = 1.0
        Xs = (X - self.mean_) / self.scale_

        rng = np.random.RandomState(self.seed)
        self.W_ = rng.uniform(-1.0, 1.0, size=(X.shape[1], self.n_hidden))
        self.b_ = rng.uniform(-1.0, 1.0, size=self.n_hidden)

        H = self._hidden(Xs)
        # One-hot targets, then the least-squares output layer.
        T = np.zeros((y.shape[0], self.classes_.size))
        T[np.arange(y.shape[0]),
          np.searchsorted(self.classes_, y)] = 1.0
        self.beta_, *_ = np.linalg.lstsq(H, T, rcond=None)
        return self

    def _hidden(self, Xs: np.ndarray) -> np.ndarray:
        # Clipped to keep exp() from overflowing on outlying rows; the sigmoid
        # is flat out there anyway.
        return 1.0 / (1.0 + np.exp(-np.clip(Xs @ self.W_ + self.b_, -30, 30)))

    def predict(self, X: np.ndarray) -> np.ndarray:
        Xs = (np.asarray(X, dtype=np.float64) - self.mean_) / self.scale_
        return self.classes_[np.argmax(self._hidden(Xs) @ self.beta_, axis=1)]


def make_search_model(kind: str):
    """Factory for the classifier that DRIVES a search."""
    if kind == "tree":
        return make_model()
    if kind == "elm":
        return ELMClassifier()
    raise ValueError(f"unknown search model {kind!r}; have 'tree', 'elm'")


# ------------------------------------------------------------------------ AUF
def opt_curve(items: Sequence[Dict], K: int = PAPER_K) -> np.ndarray:
    """opt(k) for k = 1..K: the best score among items of size at most k.

    `items` are dicts with "n_features" and "score". Sizes above K are ignored,
    as they cannot enter any opt(k) for k <= K.

    A k below the smallest subset the method produced has no item at all. The
    paper does not say what happens there; it is scored 0, because the method
    genuinely offers nothing at that budget and carrying the next-larger
    subset backwards would credit it with a subset it never found.
    """
    best = np.zeros(K, dtype=float)
    running = 0.0
    by_size: Dict[int, float] = {}
    for it in items:
        size = int(it["n_features"])
        if 1 <= size <= K:
            by_size[size] = max(by_size.get(size, -np.inf), float(it["score"]))
    for k in range(1, K + 1):
        if k in by_size:
            running = max(running, by_size[k])
        best[k - 1] = running
    return best


def auf(items: Sequence[Dict], K: int = PAPER_K) -> float:
    """AUF := (1/K) * sum_{k=1..K} opt(k)."""
    return float(opt_curve(items, K).mean())


# ------------------------------------------------------- 30-split evaluation
# The paper says "F1 score" and never which average. On a two-class set like
# ALLAML the choice moves the AUF by a lot, so all three are recorded per
# evaluation split and the primary one is chosen afterwards. Recomputing this
# is a full re-run of the experiment; recording it costs three f1_score calls
# on predictions that have already been made.
F1_AVERAGES = ("weighted", "macro", "binary")
PRIMARY_AVERAGE = "weighted"  # matches protocol.py


def _f1(y_true, y_pred, average: str, n_classes: int) -> float:
    if average == "binary" and n_classes != 2:
        return float("nan")
    return float(f1_score(y_true, y_pred, average=average,
                          zero_division=0))


def evaluate_front(X: np.ndarray, y: np.ndarray, subsets: Sequence[Sequence[int]],
                   eval_seeds: Sequence[int] = EVAL_SPLIT_SEEDS,
                   K: int = PAPER_K) -> Dict:
    """Score a method's selected subsets on 30 fresh 80:20 splits.

    Returns one AUF per evaluation split UNDER EACH F1 AVERAGE, plus the
    aggregate statistics the paper's Tables 3 and 4 report. The classifier here
    is the decision tree for every method -- see the module docstring.

    Subsets larger than K never enter an opt(k) for k <= K, so they are dropped
    before any model is fitted rather than fitted and discarded.
    """
    usable = [np.asarray(sorted(set(int(f) for f in s)), dtype=int)
              for s in subsets]
    usable = [s for s in usable if 1 <= s.size <= K]
    empty = {"aufs": [], "aufs_by_average": {}, "mean": None, "max": None,
             "median": None, "sd": None, "n_eval_splits": 0, "n_subsets": 0,
             "eval_model_fits": 0, "subsets": []}
    if not usable:
        return empty

    n_classes = int(np.unique(y).size)
    by_average = {a: [] for a in F1_AVERAGES}
    fits = 0
    for seed in eval_seeds:
        tr, te = split_80_20(X, y, seed)
        scored = {a: [] for a in F1_AVERAGES}
        for feats in usable:
            model = make_model().fit(X[np.ix_(tr, feats)], y[tr])
            pred = model.predict(X[np.ix_(te, feats)])
            fits += 1
            for a in F1_AVERAGES:
                scored[a].append({"n_features": int(feats.size),
                                  "score": _f1(y[te], pred, a, n_classes)})
        for a in F1_AVERAGES:
            items = [it for it in scored[a] if not np.isnan(it["score"])]
            by_average[a].append(auf(items, K) if items else float("nan"))

    arr = np.asarray(by_average[PRIMARY_AVERAGE], dtype=float)
    return {
        "aufs": [round(a, 6) for a in by_average[PRIMARY_AVERAGE]],
        "aufs_by_average": {a: [round(v, 6) for v in vals]
                            for a, vals in by_average.items()},
        "primary_average": PRIMARY_AVERAGE,
        "mean": float(arr.mean()),
        "max": float(arr.max()),
        "median": float(np.median(arr)),
        "sd": float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
        "n_eval_splits": int(arr.size),
        "n_subsets": len(usable),
        "eval_model_fits": fits,
        # The subsets themselves, so that K, the metric, or the aggregation can
        # be reconsidered later without re-running the search.
        "subsets": [s.tolist() for s in usable],
    }


def aggregate(per_split: List[Dict], average: str = PRIMARY_AVERAGE) -> Dict:
    """Pool the AUFs of every (fs split, eval split) pair, as the tables do.

    Table 3 reports one mean/max/median/sd per data set and method, over 10
    feature-selection splits x 30 evaluation splits = 300 values.

    `average` picks the F1 average to pool, so the same finished run can be
    re-read under weighted, macro or binary F1 without recomputation.
    """
    if average == PRIMARY_AVERAGE:
        pooled = [a for p in per_split for a in p.get("aufs", [])]
    else:
        pooled = [a for p in per_split
                  for a in p.get("aufs_by_average", {}).get(average, [])]
    pooled = [a for a in pooled if a == a]  # drop NaN (binary on multiclass)
    if not pooled:
        return {"mean": None, "max": None, "median": None, "sd": None, "n": 0}
    arr = np.asarray(pooled, dtype=float)
    return {
        "mean": round(float(arr.mean()), 4),
        "max": round(float(arr.max()), 4),
        "median": round(float(np.median(arr)), 4),
        "sd": round(float(arr.std(ddof=1)), 4),
        "n": int(arr.size),
    }
