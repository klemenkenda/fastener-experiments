"""Baseline feature selectors.

Every selector is fit on TRAIN ONLY and produces a ranking (or an explicit subset
per k). The resulting subsets go through protocol.evaluate_subset, exactly like
FASTENER's, so the comparison is like-for-like.

The paper compares FASTENER against similarity-based filters (KBest, ReliefF) and
wrapper methods. ReliefF needs the `skrebate` package, which is unmaintained and
not installed here, so we cover the filter family with mutual information and
ANOVA F, and the wrapper family with RFE.
"""
import sys
import time
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.feature_selection import RFE, f_classif, mutual_info_classif

sys.path.insert(0, str(Path(__file__).resolve().parent))

from protocol import FitCounter, evaluate_subset, make_model  # noqa: E402

MI_SEED = 20200


def rank_mutual_info(ds) -> np.ndarray:
    """Feature indices, best first, by mutual information with the label."""
    scores = mutual_info_classif(ds.X_train, ds.y_train, random_state=MI_SEED)
    return np.argsort(scores)[::-1]


def rank_anova_f(ds) -> np.ndarray:
    scores, _ = f_classif(ds.X_train, ds.y_train)
    scores = np.nan_to_num(scores, nan=-np.inf)
    return np.argsort(scores)[::-1]


def rank_tree_importance(ds) -> np.ndarray:
    """Impurity importance from a single tree fit on all features."""
    model = make_model().fit(ds.X_train, ds.y_train)
    return np.argsort(model.feature_importances_)[::-1]


RANKERS = {
    "kbest_mutual_info": rank_mutual_info,
    "kbest_anova_f": rank_anova_f,
    "tree_importance": rank_tree_importance,
}


def run_ranker(ds, name: str, ks: List[int], counter: FitCounter) -> Dict:
    t0 = time.time()
    ranking = RANKERS[name](ds)
    rank_seconds = time.time() - t0

    records = []
    for k in ks:
        if k > ds.n_features:
            continue
        rec = evaluate_subset(ds, ranking[:k], counter)
        rec["method"] = name
        records.append(rec)

    return {
        "method": name,
        "family": "filter",
        "ranking": ranking.tolist(),
        "rank_seconds": round(rank_seconds, 3),
        "elapsed_seconds": round(time.time() - t0, 3),
        "records": records,
    }


def run_rfe(ds, ks: List[int], counter: FitCounter) -> Dict:
    """Recursive feature elimination -- a wrapper baseline.

    RFE is re-run per k (sklearn's RFE gives one subset per target size). Its
    internal fits are counted separately because they dominate its cost.
    """
    t0 = time.time()
    records = []
    internal_fits = 0
    for k in ks:
        if k > ds.n_features:
            continue
        sel = RFE(make_model(), n_features_to_select=k, step=0.1)
        sel.fit(ds.X_train, ds.y_train)
        # RFE fits once per elimination round.
        internal_fits += int(np.ceil(np.log(ds.n_features / k) / np.log(1 / 0.9))) + 1
        rec = evaluate_subset(ds, np.where(sel.support_)[0], counter)
        rec["method"] = "rfe_tree"
        records.append(rec)

    return {
        "method": "rfe_tree",
        "family": "wrapper",
        "internal_fits_estimated": internal_fits,
        "elapsed_seconds": round(time.time() - t0, 3),
        "records": records,
    }


def run_random(ds, ks: List[int], counter: FitCounter, n_repeats: int = 10,
               seed: int = 20200) -> Dict:
    """Random subsets: the floor any real method must clear.

    For each k we draw `n_repeats` subsets and keep the mean and the best-on-val,
    so the floor is not flattered by a single lucky draw.
    """
    t0 = time.time()
    rng = np.random.RandomState(seed)
    records, summary = [], []

    for k in ks:
        if k > ds.n_features:
            continue
        draws = []
        for _ in range(n_repeats):
            feats = rng.choice(ds.n_features, size=k, replace=False)
            rec = evaluate_subset(ds, feats, counter)
            rec["method"] = "random"
            draws.append(rec)
        best = max(draws, key=lambda r: r["val_score"])
        records.append(best)
        summary.append({
            "n_features": k,
            "mean_test_score": float(np.mean([d["test_score"] for d in draws])),
            "std_test_score": float(np.std([d["test_score"] for d in draws])),
            "mean_val_score": float(np.mean([d["val_score"] for d in draws])),
            "n_repeats": n_repeats,
        })

    return {
        "method": "random",
        "family": "floor",
        "n_repeats": n_repeats,
        "seed": seed,
        "elapsed_seconds": round(time.time() - t0, 3),
        "summary_per_k": summary,
        "records": records,
    }


def run_all_features(ds, counter: FitCounter) -> Dict:
    t0 = time.time()
    rec = evaluate_subset(ds, np.arange(ds.n_features), counter)
    rec["method"] = "all_features"
    return {
        "method": "all_features",
        "family": "reference",
        "elapsed_seconds": round(time.time() - t0, 3),
        "records": [rec],
    }
