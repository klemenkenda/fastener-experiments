"""Stronger, modern feature-selection baselines.

These sit between the simple filters in baselines.py and the ported NSGAII-MIIP.
All of them are either maintained library implementations or textbook algorithms
implemented directly -- none is a guess at an unpublished method.

  mrmr        minimum redundancy maximum relevance (Peng et al. 2005), the
              standard information-theoretic filter that accounts for
              redundancy between features, unlike plain top-k mutual info.
  relieff     ReliefF (Kononenko 1994) via skrebate. The FASTENER paper compares
              against this, so it is the paper's own comparator.
  boruta      Boruta (Kursa & Rudnicki 2010) via BorutaPy: all-relevant
              selection against randomised shadow features.
  hsic_lasso  HSIC Lasso (Yamada et al. 2014) via pyHSICLasso: kernel-based,
              detects non-linear dependence, which matters on MADELON.
  nsga2       Plain NSGA-II wrapper search -- the multi-objective evolutionary
              baseline that both NSGAII-MIIP and BGR-FS benchmark against. This
              is the direct architectural comparator for FASTENER.

Every selector is fit on TRAIN ONLY and its subsets are scored through
protocol.evaluate_subset, identically to every other method.
"""
import sys
import time
import warnings
from pathlib import Path
from typing import Dict, List

import numpy as np
from sklearn.feature_selection import mutual_info_classif

sys.path.insert(0, str(Path(__file__).resolve().parent))

from protocol import FitCounter, evaluate_subset, make_model  # noqa: E402

SEED = 20200


# ---------------------------------------------------------------------- mRMR
def rank_mrmr(ds, n_select: int, n_bins: int = 10) -> np.ndarray:
    """MID variant: maximise I(f;y) - mean redundancy to already-selected.

    Implemented directly (the pip packages for mRMR are thin wrappers with
    heavy deps). Discretisation matches the standard formulation.
    """
    from nsgaii_miip import discretize, mi_matrix

    X = ds.X_train
    codes = discretize(X, n_bins)
    y_codes = np.unique(ds.y_train, return_inverse=True)[1].astype(np.int32)

    relevance = mutual_info_classif(X, ds.y_train, random_state=SEED)

    selected = [int(np.argmax(relevance))]
    remaining = set(range(X.shape[1])) - set(selected)

    # Pairwise MI is computed lazily, only between candidates and the selected
    # set, so this stays O(n_select * F) rather than O(F^2).
    def pair_mi(a: int, b: int) -> float:
        k = n_bins
        joint = np.bincount(codes[:, a] * k + codes[:, b], minlength=k * k)
        p = joint / joint.sum()
        nz = p > 0
        h_ab = -(p[nz] * np.log2(p[nz])).sum()
        pa = np.bincount(codes[:, a], minlength=k) / codes.shape[0]
        pb = np.bincount(codes[:, b], minlength=k) / codes.shape[0]
        h_a = -(pa[pa > 0] * np.log2(pa[pa > 0])).sum()
        h_b = -(pb[pb > 0] * np.log2(pb[pb > 0])).sum()
        return float(h_a + h_b - h_ab)

    redundancy = np.zeros(X.shape[1])
    while len(selected) < min(n_select, X.shape[1]):
        last = selected[-1]
        cand = np.fromiter(remaining, dtype=int)
        for c in cand:
            redundancy[c] += pair_mi(int(c), last)
        score = relevance[cand] - redundancy[cand] / len(selected)
        nxt = int(cand[int(np.argmax(score))])
        selected.append(nxt)
        remaining.discard(nxt)

    return np.array(selected, dtype=int)


def run_mrmr(ds, ks: List[int], counter: FitCounter) -> Dict:
    t0 = time.time()
    order = rank_mrmr(ds, max(ks))
    records = []
    for k in ks:
        if k > order.size:
            continue
        rec = evaluate_subset(ds, order[:k], counter)
        rec["method"] = "mrmr"
        records.append(rec)
    return {"method": "mrmr", "family": "filter",
            "elapsed_seconds": round(time.time() - t0, 2),
            "ranking": order.tolist(), "records": records}


# -------------------------------------------------------------------- ReliefF
def run_relieff(ds, ks: List[int], counter: FitCounter,
                n_neighbors: int = 10) -> Dict:
    from skrebate import ReliefF

    t0 = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sel = ReliefF(n_features_to_select=max(ks), n_neighbors=n_neighbors,
                      n_jobs=1)
        sel.fit(ds.X_train, ds.y_train)
    order = np.argsort(sel.feature_importances_)[::-1]

    records = []
    for k in ks:
        if k > ds.n_features:
            continue
        rec = evaluate_subset(ds, order[:k], counter)
        rec["method"] = "relieff"
        records.append(rec)
    return {"method": "relieff", "family": "filter",
            "elapsed_seconds": round(time.time() - t0, 2),
            "n_neighbors": n_neighbors,
            "ranking": order.tolist(), "records": records}


# --------------------------------------------------------------------- Boruta
def run_boruta(ds, ks: List[int], counter: FitCounter,
               max_iter: int = 100) -> Dict:
    """Boruta selects a SET, not a ranking, so it yields one subset.

    Its feature ranking is used to fill the k-grid, but the method's own answer
    is the confirmed set, reported separately as `native_subset`.
    """
    from boruta import BorutaPy
    from sklearn.ensemble import RandomForestClassifier

    t0 = time.time()
    rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=SEED,
                                class_weight="balanced", max_depth=5)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sel = BorutaPy(rf, n_estimators="auto", random_state=SEED,
                       max_iter=max_iter, verbose=0)
        sel.fit(ds.X_train, ds.y_train)

    order = np.argsort(sel.ranking_)  # rank 1 = confirmed
    confirmed = np.where(sel.support_)[0]

    records = []
    for k in ks:
        if k > ds.n_features:
            continue
        rec = evaluate_subset(ds, order[:k], counter)
        rec["method"] = "boruta"
        records.append(rec)

    native = None
    if confirmed.size:
        native = evaluate_subset(ds, confirmed, counter)
        native["method"] = "boruta"

    return {"method": "boruta", "family": "all-relevant",
            "elapsed_seconds": round(time.time() - t0, 2),
            "n_confirmed": int(confirmed.size),
            "native_subset": native,
            "ranking": order.tolist(), "records": records}


# ----------------------------------------------------------------- HSIC Lasso
def run_hsic_lasso(ds, ks: List[int], counter: FitCounter) -> Dict:
    from pyHSICLasso import HSICLasso

    t0 = time.time()
    k_max = min(max(ks), ds.n_features)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        h = HSICLasso()
        h.input(ds.X_train, ds.y_train)
        h.classification(k_max)
    order = np.array(h.get_index(), dtype=int)

    records = []
    for k in ks:
        if k > order.size:
            continue
        rec = evaluate_subset(ds, order[:k], counter)
        rec["method"] = "hsic_lasso"
        records.append(rec)
    return {"method": "hsic_lasso", "family": "kernel filter",
            "elapsed_seconds": round(time.time() - t0, 2),
            "ranking": order.tolist(), "records": records}


# ------------------------------------------------------------------- NSGA-II
def run_nsga2(ds, seed: int, stop_evaluations: int, pop_size: int = 100,
              init: str = "obl", progress_cb=None) -> Dict:
    """Plain NSGA-II wrapper search: same operators as the MIIP port, minus the
    mutual-information improvement phase.

    Running both isolates what MIIP's improvement phase actually contributes,
    since everything else is held identical.
    """
    from nsgaii_miip import (balanced_mutation, binary_tournament_crossover,
                             crowding_distance, fast_nondominated_sort,
                             obl_initialization, sparse_initialization)

    rng = np.random.RandomState(seed)
    n_features = ds.n_features
    m_rate = 1.0 / n_features
    evaluations = 0
    cache: Dict[bytes, float] = {}
    t0 = time.time()

    def objective(genes) -> float:
        feats = np.where(genes)[0]
        model = make_model().fit(ds.X_train[:, feats], ds.y_train)
        from protocol import primary_score
        return primary_score(ds.y_val, model.predict(ds.X_val[:, feats]))

    def evaluate(P):
        nonlocal evaluations
        objs = np.empty((P.shape[0], 2))
        for i, genes in enumerate(P):
            size = int(genes.sum())
            if size == 0:
                objs[i] = (1.0, 0.0)
                continue
            key = np.packbits(genes).tobytes()
            if key not in cache:
                cache[key] = objective(genes)
                evaluations += 1
            objs[i] = (-cache[key], size)
        return objs

    pop = (obl_initialization(pop_size, n_features, rng) if init == "obl"
           else sparse_initialization(pop_size, n_features, rng))
    objs = evaluate(pop)
    iteration = 0

    while evaluations < stop_evaluations:
        iteration += 1
        if progress_cb is not None:
            progress_cb(evaluations)
        fronts = fast_nondominated_sort(objs)
        rank = np.empty(pop.shape[0], dtype=int)
        crowd = np.zeros(pop.shape[0])
        for r, f in enumerate(fronts):
            rank[f] = r
            crowd[f] = crowding_distance(objs[f])

        off = binary_tournament_crossover(pop, rank, crowd, 0.9, rng)
        off = balanced_mutation(off, m_rate, rng)
        off_objs = evaluate(off)

        merged = np.vstack([pop, off])
        merged_objs = np.vstack([objs, off_objs])

        keep: List[int] = []
        for f in fast_nondominated_sort(merged_objs):
            if len(keep) + f.size <= pop_size:
                keep.extend(f.tolist())
            else:
                d = crowding_distance(merged_objs[f])
                keep.extend(f[np.argsort(-d)][: pop_size - len(keep)].tolist())
                break
        idx = np.array(keep, dtype=int)
        pop, objs = merged[idx], merged_objs[idx]

    final = fast_nondominated_sort(objs)[0]
    records = []
    for genes in pop[final]:
        feats = np.where(genes)[0]
        if feats.size == 0:
            continue
        rec = evaluate_subset(ds, feats, counter=None)
        rec["method"] = "nsga2"
        rec["seed"] = seed
        records.append(rec)

    name = "nsga2" if init == "obl" else "nsga2_sparse"
    for r in records:
        r["method"] = name
    return {"method": name, "family": "genetic", "seed": seed, "init": init,
            "elapsed_seconds": round(time.time() - t0, 2),
            "model_fits": evaluations, "iterations": iteration,
            "records": records}


def run_nsgaii_miip_method(ds, seed: int, stop_evaluations: int,
                           cluster_cache: Dict = None,
                           pop_size: int = 100, n_jobs: int = 1,
                           init: str = "obl", progress_cb=None) -> Dict:
    """Wrapper putting the NSGAII-MIIP port behind the shared protocol.

    The MI matrix and clustering depend only on the training data, not the seed,
    so they are computed once and reused across seeds via `cluster_cache`.
    """
    from nsgaii_miip import cluster_features, run_nsgaii_miip
    from protocol import primary_score

    t0 = time.time()
    if cluster_cache is not None and "clusters" in cluster_cache:
        clusters, mi, ent = (cluster_cache["clusters"], cluster_cache["mi"],
                             cluster_cache["ent"])
        prep_seconds = 0.0
    else:
        p0 = time.time()
        clusters, mi, ent = cluster_features(
            ds.X_train, ds.y_train, np.random.RandomState(SEED), n_jobs=n_jobs)
        prep_seconds = time.time() - p0
        if cluster_cache is not None:
            cluster_cache.update(clusters=clusters, mi=mi, ent=ent)

    def objective(genes) -> float:
        feats = np.where(genes)[0]
        model = make_model().fit(ds.X_train[:, feats], ds.y_train)
        return primary_score(ds.y_val, model.predict(ds.X_val[:, feats]))

    out = run_nsgaii_miip(ds.n_features, objective, clusters, mi, ent,
                          seed=seed, stop_evaluations=stop_evaluations,
                          pop_size=pop_size, init=init,
                          progress_cb=progress_cb)

    name = "nsgaii_miip" if init == "obl" else "nsgaii_miip_sparse"
    records = []
    for genes in out["pareto_genes"]:
        feats = np.where(genes)[0]
        if feats.size == 0:
            continue
        rec = evaluate_subset(ds, feats, counter=None)
        rec["method"] = name
        rec["seed"] = seed
        records.append(rec)

    return {"method": name, "family": "genetic (ported)", "seed": seed, "init": init,
            "elapsed_seconds": round(time.time() - t0, 2),
            "mi_prep_seconds": round(prep_seconds, 2),
            "model_fits": out["evaluations"], "iterations": out["iterations"],
            "n_clusters": len(clusters),
            "port_note": "Reimplementation from the authors' MATLAB, not their results.",
            "records": records}
