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
  poss        Pareto Optimization for Subset Selection (Qian et al. 2015): a
              Pareto ARCHIVE advanced by single-parent bit-flip mutation. The
              same shape as FASTENER, without crossover, information guidance
              or pruning, so it isolates what those operators are worth.
  fs_sds      Feature Selection using Stochastic Diffusion Search (Alhakbani &
              al-Rifaie 2017): a swarm of agents holding fixed-size subsets,
              spreading good ones by direct contact. Fixed k per run, so one
              run per feature count.

`poss` and `fs_sds` are the FASTENER paper's own wrapper comparators, its
references [11] and [12]. Running them here is the closest this experiment gets
to reproducing the paper's comparison under a protocol that scores every method
identically.

Every selector is fit on TRAIN ONLY and its subsets are scored through
protocol.evaluate_subset, identically to every other method.
"""
import sys
import time
import warnings
from pathlib import Path
from typing import Dict, List, Optional

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
class TreeForBoruta:
    """The protocol's decision tree, shaped the way BorutaPy needs.

    BorutaPy calls `set_params(n_estimators=...)` on its estimator every
    iteration, sizing a forest. A single tree has no such parameter and rejects
    the call. This accepts it and ignores it -- there is one tree -- and is
    otherwise exactly `protocol.make_model()`, so Boruta ranks features by the
    same model every other method is judged by (HYPOTHESES.md: one classifier).

    Boruta also sets `random_state` each iteration; that is kept, since varying
    the estimator between iterations is part of how Boruta works.
    """

    def __init__(self, n_estimators=1, random_state=None):
        self.n_estimators = n_estimators
        self.random_state = random_state

    def get_params(self, deep=True):
        return {"n_estimators": self.n_estimators,
                "random_state": self.random_state}

    def set_params(self, **params):
        for key, value in params.items():
            if key not in ("n_estimators", "random_state"):
                raise ValueError(f"TreeForBoruta has no parameter {key!r}")
            setattr(self, key, value)
        return self

    def fit(self, X, y):
        tree = make_model()
        if self.random_state is not None:
            tree.set_params(random_state=self.random_state)
        self.tree_ = tree.fit(X, y)
        self.feature_importances_ = self.tree_.feature_importances_
        self.classes_ = self.tree_.classes_
        return self

    def predict(self, X):
        return self.tree_.predict(X)


def run_boruta(ds, ks: List[int], counter: FitCounter,
               max_iter: int = 100, seed: int = SEED) -> Dict:
    """Boruta selects a SET, not a ranking, so it yields one subset.

    Its feature ranking is used to fill the k-grid, but the method's own answer
    is the confirmed set, reported separately as `native_subset`.

    Boruta is stochastic: it permutes every column to build shadow features and
    refits its estimator on each iteration. It therefore takes a seed and is
    run once per seed like the population searches, not as a single fixed pass.

    The estimator is the protocol's decision tree (`TreeForBoruta`), not the
    random forest Boruta is usually paired with: HYPOTHESES.md requires every
    method to use the one classifier it is judged by. This is a departure from
    Boruta's usual configuration and is recorded on the result.
    """
    from boruta import BorutaPy

    t0 = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sel = BorutaPy(TreeForBoruta(), n_estimators="auto", random_state=seed,
                       max_iter=max_iter, verbose=0)
        sel.fit(ds.X_train, ds.y_train)

    # ranking_ is 1 for EVERY confirmed feature and 2 for every tentative one;
    # only rejected features get a graded rank. Sorting on it alone leaves the
    # confirmed block in whatever order the sort happens to produce, so every
    # k < n_confirmed budget would be scored on an arbitrary subset of it.
    # Break those ties on mean shadow-relative importance, Boruta's own measure
    # of strength. Row 0 of the history is the zero-filled seed row.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        imp = np.nanmean(sel.importance_history_[1:], axis=0)
    imp = np.nan_to_num(imp, nan=0.0)
    order = np.lexsort((-imp, sel.ranking_))  # rank asc, then importance desc
    confirmed = np.where(sel.support_)[0]

    records = []
    for k in ks:
        if k > ds.n_features:
            continue
        rec = evaluate_subset(ds, order[:k], counter)
        rec["method"] = "boruta"
        rec["seed"] = seed
        records.append(rec)

    native = None
    if confirmed.size:
        native = evaluate_subset(ds, confirmed, counter)
        native["method"] = "boruta"
        native["seed"] = seed

    return {"method": "boruta", "family": "all-relevant", "seed": seed,
            "estimator": "protocol decision tree (departure: Boruta is "
                         "usually run on a random forest)",
            "elapsed_seconds": round(time.time() - t0, 2),
            "n_confirmed": int(confirmed.size),
            "native_subset": native,
            "ranking": order.tolist(), "records": records}


# ----------------------------------------------------------------- HSIC Lasso
def run_hsic_lasso(ds, ks: List[int], counter: FitCounter) -> Dict:
    from pyHSICLasso import HSICLasso

    # pyHSICLasso's nlars catches `np.linalg.linalg.LinAlgError`, a path
    # numpy 2 removed, so a singular step raised AttributeError instead of
    # being handled (eodata). Restoring the alias lets its handler run as
    # written.
    if not hasattr(np.linalg, "linalg"):
        np.linalg.linalg = np.linalg

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
              init: str = "obl", progress_cb=None, trajectory=None,
              max_barren_generations: Optional[int] = None) -> Dict:
    """Plain NSGA-II wrapper search: same operators as the MIIP port, minus the
    mutual-information improvement phase.

    Running both isolates what MIIP's improvement phase actually contributes,
    since everything else is held identical.

    `trajectory` (a `trajectory.Trajectory`) records the best score after every
    generation; generation 0 is the initial population.

    `max_barren_generations` stops a converged run, as in the MIIP port
    (nsgaii_miip.MAX_BARREN_GENERATIONS); run_sota.py passes it. None (the
    default here) runs until the budget is spent, as before DEC-41.
    """
    from nsgaii_miip import (balanced_mutation, barren_counter,
                             binary_tournament_crossover,
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
        """Score a population. Returns the objectives and a mask of the rows
        that have one.

        The fit budget is exact: once it is spent, a subset that would need a
        NEW fit is left unscored and the caller drops it, rather than letting
        the last generation overshoot the cap by up to a population's worth of
        fits. Cached subsets still score, since they cost nothing. This is how
        FASTENER, POSS and FS-SDS already stop (HYPOTHESES.md: 6,000 fits per
        run, equal across arms).
        """
        nonlocal evaluations
        objs = np.empty((P.shape[0], 2))
        ok = np.ones(P.shape[0], dtype=bool)
        for i, genes in enumerate(P):
            size = int(genes.sum())
            if size == 0:
                objs[i] = (1.0, 0.0)
                continue
            key = np.packbits(genes).tobytes()
            if key not in cache:
                if evaluations >= stop_evaluations:
                    ok[i] = False
                    continue
                cache[key] = objective(genes)
                evaluations += 1
                if trajectory is not None:
                    trajectory.observe(np.where(genes)[0], cache[key])
            objs[i] = (-cache[key], size)
        return objs, ok

    pop = (obl_initialization(pop_size, n_features, rng) if init == "obl"
           else sparse_initialization(pop_size, n_features, rng))
    objs, ok = evaluate(pop)
    pop, objs = pop[ok], objs[ok]
    iteration = 0
    if trajectory is not None:
        trajectory.step(0, evaluations)
    barren = barren_counter(max_barren_generations)
    barren(evaluations)
    stagnated = False

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
        off_objs, ok = evaluate(off)
        off, off_objs = off[ok], off_objs[ok]

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
        if trajectory is not None:
            trajectory.step(iteration, evaluations)
        if barren(evaluations):
            stagnated = True
            break

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
            "stopped_on": "stagnation" if stagnated else "budget",
            "max_barren_generations": max_barren_generations,
            "records": records}


# ---------------------------------------------------------------------- POSS
def run_poss_method(ds, seed: int, stop_evaluations: int, k: int = None,
                    progress_cb=None, trajectory=None) -> Dict:
    """POSS behind the shared protocol.

    `k` is POSS's own constraint parameter, not a grid budget: the algorithm
    treats any subset of 2k or more features as infeasible, so k sets both the
    size it optimises for and the widest subset the archive can hold. It is the
    one parameter POSS has, and the paper requires it -- there is no
    unconstrained variant to fall back on. The caller sets it to the region the
    comparison cares about.

    In practice k barely binds at this experiment's budget: on MADELON at 6000
    fits the archive only reaches ~7 features, far short of 2k-1, and no draw is
    ever rejected as infeasible. See the note in `poss.py`.
    """
    from poss import poss_best, run_poss
    from protocol import primary_score

    if k is None:
        k = min(50, ds.n_features)
    k = min(k, ds.n_features)

    t0 = time.time()

    def objective(genes) -> float:
        feats = np.where(genes)[0]
        model = make_model().fit(ds.X_train[:, feats], ds.y_train)
        score = primary_score(ds.y_val, model.predict(ds.X_val[:, feats]))
        if trajectory is not None:
            trajectory.observe(feats, score)
        return score

    out = run_poss(ds.n_features, objective, k=k, seed=seed,
                   stop_evaluations=stop_evaluations, progress_cb=progress_cb,
                   iteration_cb=(None if trajectory is None
                                 else lambda it, ev: trajectory.step(it, ev)))

    records = []
    for genes in out["archive_genes"]:
        feats = np.where(genes)[0]
        if feats.size == 0:
            continue
        rec = evaluate_subset(ds, feats, counter=None)
        rec["method"] = "poss"
        rec["seed"] = seed
        records.append(rec)

    # The paper returns ONE subset, the best with |s| <= k. The curve above is
    # the whole archive, which is more than POSS claims to deliver, so its own
    # answer is reported separately instead of being read off the curve.
    best_genes = poss_best(out)
    native = None
    if best_genes is not None:
        native = evaluate_subset(ds, np.where(best_genes)[0], counter=None)
        native["method"] = "poss"
        native["seed"] = seed

    return {"method": "poss", "family": "pareto archive", "seed": seed,
            "k": k,
            "elapsed_seconds": round(time.time() - t0, 2),
            "model_fits": out["evaluations"], "iterations": out["iterations"],
            "infeasible_draws": out["infeasible_draws"],
            "theoretical_evaluations": out["theoretical_evaluations"],
            "budget_note": (
                "Run at the shared fit budget. The paper's T = 2*e*k^2*n would "
                f"be {out['theoretical_evaluations']} evaluations, so this is "
                "POSS truncated far below the regime its approximation "
                "guarantee describes."),
            "native_subset": native,
            "records": records}


# -------------------------------------------------------------------- FS-SDS
def run_fs_sds_method(ds, ks: List[int], seed: int,
                      stop_evaluations: Optional[int],
                      population_size: int = None, max_iterations: int = None,
                      model_factory=None, label: str = "fs_sds",
                      progress_cb=None, trajectory=None,
                      cpu_seconds_per_k: Optional[float] = None) -> Dict:
    """FS-SDS behind the shared protocol, one SDS run per feature count.

    FS-SDS holds every agent at EXACTLY k features for a whole run, so unlike
    FASTENER, POSS and NSGA-II it produces one point rather than a front. The
    curve is assembled by running it once per k, which is what the FASTENER
    paper did too (its Table 3 reports FS-SDS's budget "per each k").

    `stop_evaluations` is PER K. What the whole method may spend is the
    CALLER's decision: under HYPOTHESES.md the runner divides the run's total
    budget evenly over k = 1..20 (6,000 in total, 300 per k), so FS-SDS spends
    what every other arm spends. The paper-replication runner instead
    passes a per-k budget, as the paper did.

    `trajectory` records the best score after every sweep. Iterations are
    numbered continuously across the per-k runs, and each snapshot carries the
    k of the run it came from.

    `cpu_seconds_per_k` gives each k-run a process-CPU-time budget (H4: equal
    compute between methods); with `stop_evaluations=None` time alone stops
    it. Time a k-run leaves unused is not passed on to the next k, as unused
    fits were not.

    `model_factory` overrides the classifier that DRIVES the search. It defaults
    to the shared decision tree; the FASTENER paper ran FS-SDS on an Extreme
    Learning Machine instead, so a replication passes
    `paper_protocol.ELMClassifier`. `label` names the arm in the records, so
    both can sit in one comparison without colliding.
    """
    from fs_sds import (DEFAULT_POPULATION, PAPER_EVALUATIONS_PER_K,
                        run_fs_sds)
    from protocol import primary_score

    population_size = population_size or DEFAULT_POPULATION
    # max_iterations stays None unless the caller asks for the reference cap:
    # the fit budget is what stops a run. See fs_sds.MAX_ITERATIONS_GUARD.
    build_model = model_factory or make_model

    t0 = time.time()
    cpu0 = time.process_time()

    def objective(genes) -> float:
        feats = np.where(genes)[0]
        model = build_model().fit(ds.X_train[:, feats], ds.y_train)
        score = primary_score(ds.y_val, model.predict(ds.X_val[:, feats]))
        if trajectory is not None:
            trajectory.observe(feats, score)
        return score

    records = []
    per_k = []
    total_fits = 0
    iteration_offset = [0]  # iterations of the k-runs already finished
    for k in ks:
        if k > ds.n_features:
            continue
        # Progress is reported against the whole method, not the run in flight,
        # so the fraction does not reset to zero at every k.
        done_before = total_fits
        cb = (None if progress_cb is None
              else lambda done, base=done_before: progress_cb(base + done))
        it_cb = None
        if trajectory is not None:
            def it_cb(it, ev, k=k, base_fits=done_before,
                      base_it=iteration_offset[0]):
                trajectory.step(base_it + it, base_fits + ev, k=k)
        out = run_fs_sds(ds.n_features, k, objective, seed=seed,
                         stop_evaluations=stop_evaluations,
                         population_size=population_size,
                         max_iterations=max_iterations,
                         progress_cb=cb, iteration_cb=it_cb,
                         stop_cpu_seconds=cpu_seconds_per_k)
        # +1: each k-run starts with its own iteration 0 (initialisation).
        iteration_offset[0] += out["iterations"] + 1
        total_fits += out["evaluations"]
        per_k.append({"k": k, "model_fits": out["evaluations"],
                      "iterations": out["iterations"],
                      "stopped_on": out["stopped_on"],
                      "restarts": out["restarts"],
                      "context_resets": out["context_resets"],
                      "cpu_seconds": out["cpu_seconds"]})
        if out["best_genes"] is None:
            continue
        rec = evaluate_subset(ds, np.where(out["best_genes"])[0], counter=None,
                              model_factory=model_factory)
        rec["method"] = label
        rec["seed"] = seed
        records.append(rec)

    return {"method": label, "family": "swarm (SDS)", "seed": seed,
            "search_model": "tree" if model_factory is None else "custom",
            "elapsed_seconds": round(time.time() - t0, 2),
            # Process CPU time of the whole method: the unit of H4's budget.
            "search_cpu_seconds": round(time.process_time() - cpu0, 2),
            "cpu_seconds_per_k": cpu_seconds_per_k,
            "model_fits": total_fits,
            "evaluations_per_k": stop_evaluations,
            "population_size": population_size,
            "max_iterations": max_iterations,
            "stopped_on": sorted({p["stopped_on"] for p in per_k}),
            "k_grid": [p["k"] for p in per_k],
            "per_k": per_k,
            "budget_note": (
                (f"{cpu_seconds_per_k} CPU seconds per k"
                 if cpu_seconds_per_k is not None
                 else f"{stop_evaluations} fits per k")
                + f" over {len(per_k)} values of k; {total_fits} fits in "
                f"total. The FASTENER paper gave it "
                f"{PAPER_EVALUATIONS_PER_K} fits per k."),
            "records": records}


def run_nsgaii_miip_method(ds, seed: int, stop_evaluations: int,
                           cluster_cache: Dict = None,
                           pop_size: int = 100, n_jobs: int = 1,
                           init: str = "obl", progress_cb=None,
                           trajectory=None,
                           max_barren_generations: Optional[int] = None
                           ) -> Dict:
    """Wrapper putting the NSGAII-MIIP port behind the shared protocol.

    The MI matrix and clustering depend only on the training data, not the seed,
    so they are computed once and reused across seeds via `cluster_cache`.
    `max_barren_generations`: see nsgaii_miip.MAX_BARREN_GENERATIONS.
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
        score = primary_score(ds.y_val, model.predict(ds.X_val[:, feats]))
        if trajectory is not None:
            trajectory.observe(feats, score)
        return score

    out = run_nsgaii_miip(ds.n_features, objective, clusters, mi, ent,
                          seed=seed, stop_evaluations=stop_evaluations,
                          pop_size=pop_size, init=init,
                          progress_cb=progress_cb,
                          iteration_cb=(None if trajectory is None
                                        else lambda it, ev: trajectory.step(it, ev)),
                          max_barren_generations=max_barren_generations)

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
            "stopped_on": out["stopped_on"],
            "max_barren_generations": max_barren_generations,
            "n_clusters": len(clusters),
            "port_note": "Reimplementation from the authors' MATLAB, not their results.",
            "records": records}
