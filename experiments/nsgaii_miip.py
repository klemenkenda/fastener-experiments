"""Python port of NSGAII-MIIP (Li et al.), from the authors' MATLAB source.

Source: https://github.com/andali89/NSGAII-MIIP (MIT licence, (c) 2024 An-Da Li)
Paper:  "A multi-objective evolutionary algorithm with mutual-information-guided
         improvement phase for feature selection in complex manufacturing
         processes", EJOR 2025.

THIS IS A REIMPLEMENTATION, NOT THE AUTHORS' RESULTS.
The original runs on MATLAB + Weka and reads .arff files, neither of which is
available here. Every operator below is ported from the published source and the
mapping is noted per function, but a port can differ from the original in ways
that are invisible until they change a number. Any gap between this and FASTENER
may be a property of the method or an artefact of this port; it is not evidence
about the authors' published results.

Two deliberate, documented departures, both to make the comparison controlled
rather than to improve the method:

1. OBJECTIVE. The paper maximises the geometric mean over internal CV folds.
   Here the objective is the same one every other method in this experiment is
   scored by -- weighted F1 of a decision tree fit on train, scored on the
   validation split -- so that differences reflect the SEARCH, not the metric.
   The second objective (minimise subset size) is unchanged.

2. BUDGET. stop_evaluations is set to match FASTENER's measured model-fit count
   rather than the paper's default of 10000, so the two searches get the same
   compute.

Faithful to the source: opposition-based initialisation, binary tournament on
(front, crowding), single-point crossover at a differing locus, balanced
mutation, the MI/entropy-weighted forward/backward/interchange improvement phase
over feature clusters, and NSGA-II survival.
"""
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Weka's unsupervised Discretize filter defaults to 10 equal-width bins, and
# clusterFeature.m leaves that default in place (its setBins call is commented
# out in the published source).
N_BINS = 10


# ----------------------------------------------------------------- information
def discretize(X: np.ndarray, n_bins: int = N_BINS) -> np.ndarray:
    """Equal-width binning, matching Weka's unsupervised Discretize default."""
    out = np.empty(X.shape, dtype=np.int32)
    for j in range(X.shape[1]):
        col = X[:, j]
        lo, hi = col.min(), col.max()
        if hi <= lo:
            out[:, j] = 0
            continue
        edges = np.linspace(lo, hi, n_bins + 1)[1:-1]
        out[:, j] = np.searchsorted(edges, col, side="right")
    return out


def _entropy_from_counts(counts: np.ndarray) -> float:
    n = counts.sum()
    if n == 0:
        return 0.0
    p = counts[counts > 0] / n
    return float(-(p * np.log2(p)).sum())


def entropy_vector(codes: np.ndarray) -> np.ndarray:
    return np.array([
        _entropy_from_counts(np.bincount(codes[:, j]))
        for j in range(codes.shape[1])
    ])


def mi_matrix(codes: np.ndarray, n_jobs: int = 1) -> np.ndarray:
    """Pairwise mutual information (bits) over discretised columns.

    getEntropyMatrix in clusterFeature.m. Cost is O(F^2) in the number of
    columns, which is what bounds the feature count this method can be run on.
    """
    n, m = codes.shape
    k = int(codes.max()) + 1
    H = entropy_vector(codes)

    def mi_row(i: int) -> np.ndarray:
        row = np.zeros(m)
        ci = codes[:, i] * k
        for j in range(i + 1):
            joint = np.bincount(ci + codes[:, j], minlength=k * k)
            pj = joint / n
            nz = pj > 0
            h_joint = float(-(pj[nz] * np.log2(pj[nz])).sum())
            row[j] = H[i] + H[j] - h_joint
        return row

    if n_jobs != 1:
        from joblib import Parallel, delayed
        rows = Parallel(n_jobs=n_jobs, prefer="threads")(
            delayed(mi_row)(i) for i in range(m))
    else:
        rows = [mi_row(i) for i in range(m)]

    M = np.zeros((m, m))
    for i, row in enumerate(rows):
        M[i, : i + 1] = row[: i + 1]
        M[: i + 1, i] = row[: i + 1]
    return M


def kmedoids_on_distance(D: np.ndarray, k: int, rng: np.random.RandomState,
                         max_iter: int = 100) -> np.ndarray:
    """Voronoi-iteration k-medoids on a precomputed distance matrix.

    Stands in for the repository's kmedoids.m. Clustering only decides which
    features are considered together in the improvement phase.
    """
    n = D.shape[0]
    k = max(1, min(k, n))

    medoids = [rng.randint(n)]
    for _ in range(1, k):
        d = D[medoids].min(axis=0)
        total = d.sum()
        if total <= 0:
            medoids.append(rng.randint(n))
        else:
            medoids.append(int(rng.choice(n, p=d / total)))
    medoids = np.array(medoids)

    labels = np.zeros(n, dtype=int)
    for _ in range(max_iter):
        labels = np.argmin(D[medoids], axis=0)
        new = medoids.copy()
        for c in range(k):
            members = np.where(labels == c)[0]
            if members.size:
                new[c] = members[np.argmin(D[np.ix_(members, members)].sum(axis=1))]
        if np.array_equal(new, medoids):
            break
        medoids = new
    return labels


def cluster_features(X: np.ndarray, y: np.ndarray, rng: np.random.RandomState,
                     n_jobs: int = 1) -> Tuple[List[np.ndarray], np.ndarray, np.ndarray]:
    """clusterFeature.m: discretise, build the MI matrix, cluster the features.

    Returns (clusters, mi, entropy) where mi has the class label appended as its
    last row/column, so mi[i, -1] is feature i's relevance. Note the source names
    this nMImatrix but assigns the raw MI matrix to it, so the weights below use
    raw MI, as the original does.
    """
    codes = discretize(X)
    y_codes = np.unique(y, return_inverse=True)[1].astype(np.int32).reshape(-1, 1)
    allcodes = np.hstack([codes, y_codes])

    mi = mi_matrix(allcodes, n_jobs=n_jobs)
    ent = entropy_vector(allcodes)

    denom = np.minimum.outer(ent, ent)
    with np.errstate(divide="ignore", invalid="ignore"):
        dist = 1.0 - np.where(denom > 0, mi / denom, 0.0)
    dist = np.nan_to_num(dist, nan=1.0, posinf=1.0, neginf=0.0)
    np.fill_diagonal(dist, 0.0)

    # Cluster the FEATURES only; the class column is excluded, as in the source.
    n_features = mi.shape[0] - 1
    k = int(round(np.sqrt(n_features)))
    labels = kmedoids_on_distance(dist[:n_features, :n_features], k, rng)

    clusters = [np.where(labels == c)[0] for c in range(labels.max() + 1)]
    clusters = [c for c in clusters if c.size]
    return clusters, mi, ent


# -------------------------------------------------------------- MIIP operators
def _weight(mi: np.ndarray, ent: np.ndarray, bench: np.ndarray, ind: int) -> float:
    """calWeight: relevance squared over redundancy.

    Redundancy is 1 when bench is empty, else the sum over bench of
    MI(i, class) * MI(i, ind) / H(i).
    """
    rele = mi[ind, -1]
    if bench.size == 0:
        redun = 1.0
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            terms = mi[bench, -1] * mi[bench, ind] / ent[bench]
        redun = float(np.nan_to_num(terms).sum())
        if redun <= 0:
            # Not in the source; without it an all-zero-MI bench divides by zero.
            redun = 1e-12
    return float(rele ** 2 / redun)


def _forward(genes, mi, ent, ones_i, zeros_i):
    if zeros_i.size == 0:
        return genes, False
    w = [_weight(mi, ent, ones_i, int(z)) for z in zeros_i]
    new = genes.copy()
    new[zeros_i[int(np.argmax(w))]] = True
    return new, True


def _backward(genes, mi, ent, ones_i, zeros_i):
    if ones_i.size == 0:
        return genes, False
    new = genes.copy()
    if ones_i.size == 1:
        new[ones_i[0]] = False
        return new, True
    w = []
    for i in range(ones_i.size):
        bench = np.delete(ones_i, i)
        w.append(_weight(mi, ent, bench, int(ones_i[i])))
    new[ones_i[int(np.argmin(w))]] = False
    return new, True


def _interchange(genes, mi, ent, ones_i, zeros_i):
    if ones_i.size == 0 or zeros_i.size == 0:
        return genes, False
    benches, w_one = [], []
    for i in range(ones_i.size):
        bench = np.delete(ones_i, i)
        benches.append(bench)
        w_one.append(_weight(mi, ent, bench, int(ones_i[i])))
    order = np.argsort(w_one)  # ascending: weakest selected feature first

    for sel in order:
        w_zero = [_weight(mi, ent, benches[sel], int(z)) for z in zeros_i]
        best = int(np.argmax(w_zero))
        if w_zero[best] >= w_one[sel]:
            new = genes.copy()
            new[ones_i[sel]] = genes[zeros_i[best]]
            new[zeros_i[best]] = genes[ones_i[sel]]
            return new, True
    return genes, False


def improvement(pop: np.ndarray, mi, ent, clusters, rng) -> np.ndarray:
    """improvement.m: three variants per solution (add / remove / swap).

    For each variant the clusters are visited in random order and the first
    cluster where the operator succeeds is the one applied.
    """
    out = []
    for op in (_forward, _backward, _interchange):
        for s in range(pop.shape[0]):
            genes = pop[s].copy()
            for c in rng.permutation(len(clusters)):
                idx = clusters[c]
                sel = genes[idx]
                ones_i = idx[sel]
                zeros_i = idx[~sel]
                new, ok = op(genes, mi, ent, ones_i, zeros_i)
                if ok:
                    genes = new
                    break
            out.append(genes)
    return np.array(out, dtype=bool)


# ------------------------------------------------------------------- NSGA-II
def fast_nondominated_sort(objs: np.ndarray) -> List[np.ndarray]:
    """Standard NSGA-II sort. objs is minimised in every column."""
    n = objs.shape[0]
    dominated: List[List[int]] = [[] for _ in range(n)]
    counts = np.zeros(n, dtype=int)
    fronts: List[List[int]] = [[]]

    for p in range(n):
        dp = np.all(objs[p] <= objs, axis=1) & np.any(objs[p] < objs, axis=1)
        dq = np.all(objs <= objs[p], axis=1) & np.any(objs < objs[p], axis=1)
        dominated[p] = np.where(dp)[0].tolist()
        counts[p] = int(dq.sum())
        if counts[p] == 0:
            fronts[0].append(p)

    i = 0
    while fronts[i]:
        nxt = []
        for p in fronts[i]:
            for q in dominated[p]:
                counts[q] -= 1
                if counts[q] == 0:
                    nxt.append(q)
        i += 1
        fronts.append(nxt)
    return [np.array(f, dtype=int) for f in fronts[:-1]]


def crowding_distance(objs: np.ndarray) -> np.ndarray:
    n, m = objs.shape
    if n == 0:
        return np.zeros(0)
    d = np.zeros(n)
    for j in range(m):
        order = np.argsort(objs[:, j])
        d[order[0]] = d[order[-1]] = np.inf
        span = objs[order[-1], j] - objs[order[0], j]
        if span <= 0:
            continue
        d[order[1:-1]] += (objs[order[2:], j] - objs[order[:-2], j]) / span
    return d


def obl_initialization(pop_size: int, n_features: int, rng) -> np.ndarray:
    """oblInitialization.m: complementary (opposition) pairs."""
    half = max(1, pop_size // 2)
    r = rng.rand(half, n_features)
    return np.vstack([r > 0.5, r <= 0.5]).astype(bool)


def binary_tournament_crossover(pop, rank, crowd, c_rate, rng) -> np.ndarray:
    """binTour.m: tournament on (front asc, crowding desc), then single-point
    crossover at a randomly chosen DIFFERING locus."""
    n, m = pop.shape
    order = np.concatenate([rng.permutation(n), rng.permutation(n)])
    parents = []
    for i in range(0, 2 * n, 2):
        a, b = order[i], order[i + 1]
        if (rank[a], -crowd[a]) <= (rank[b], -crowd[b]):
            parents.append(a)
        else:
            parents.append(b)
    parents = np.array(parents)

    off = pop[parents].copy()
    for i in range(0, n - 1, 2):
        j = i + 1
        if rng.rand() < c_rate:
            diff = np.where(off[i] != off[j])[0]
            if diff.size > 1:
                point = diff[rng.randint(1, diff.size)]
                tail_i = pop[parents[j], point:].copy()
                tail_j = pop[parents[i], point:].copy()
                off[i, point:] = tail_i
                off[j, point:] = tail_j
    return off


def balanced_mutation(pop: np.ndarray, m_rate: float, rng) -> np.ndarray:
    """mutation.m: 1-bits flip at m_rate; 0-bits at m_rate*n_ones/n_zeros.

    This equalises the expected number of additions and deletions -- the
    imbalance that FASTENER's plain 1/d flip does not correct.
    """
    out = pop.copy()
    n, m = pop.shape
    for i in range(n):
        n_ones = int(pop[i].sum())
        n_zeros = m - n_ones
        rates = np.empty(m)
        rates[pop[i]] = m_rate
        rates[~pop[i]] = m_rate * n_ones / n_zeros if n_zeros > 0 else 0.0
        flip = rng.rand(m) < rates
        out[i, flip] = ~pop[i, flip]
    return out


# ---------------------------------------------------------------------- driver
def run_nsgaii_miip(n_features: int,
                    objective: Callable[[np.ndarray], float],
                    clusters, mi, ent,
                    seed: int,
                    stop_evaluations: int,
                    pop_size: int = 100,
                    c_rate: float = 0.9,
                    m_rate: Optional[float] = None,
                    verbose: bool = False) -> Dict:
    """NSGAIIMIIP.m main loop.

    objective returns the score to MAXIMISE for one boolean gene vector; it is
    negated internally, since NSGA-II minimises. The second objective is the
    number of selected features.
    """
    rng = np.random.RandomState(seed)
    m_rate = m_rate if m_rate is not None else 1.0 / n_features

    evaluations = 0
    cache: Dict[bytes, float] = {}

    def evaluate(P: np.ndarray) -> np.ndarray:
        nonlocal evaluations
        objs = np.empty((P.shape[0], 2))
        for i, genes in enumerate(P):
            size = int(genes.sum())
            if size == 0:
                # Degenerate subset: cannot be fit, so give it the worst score.
                objs[i] = (1.0, 0.0)
                continue
            key = np.packbits(genes).tobytes()
            if key not in cache:
                cache[key] = objective(genes)
                evaluations += 1
            objs[i] = (-cache[key], size)
        return objs

    pop = obl_initialization(pop_size, n_features, rng)
    objs = evaluate(pop)

    iteration = 0
    while evaluations < stop_evaluations:
        iteration += 1
        fronts = fast_nondominated_sort(objs)
        rank = np.empty(pop.shape[0], dtype=int)
        crowd = np.zeros(pop.shape[0])
        for r, f in enumerate(fronts):
            rank[f] = r
            crowd[f] = crowding_distance(objs[f])

        off = binary_tournament_crossover(pop, rank, crowd, c_rate, rng)
        off = balanced_mutation(off, m_rate, rng)
        off_objs = evaluate(off)

        merged = np.vstack([pop, off])
        merged_objs = np.vstack([objs, off_objs])

        # Improvement phase runs on the current non-dominated set.
        first = fast_nondominated_sort(merged_objs)[0]
        improved = improvement(merged[first], mi, ent, clusters, rng)
        improved_objs = evaluate(improved)

        merged = np.vstack([merged, improved])
        merged_objs = np.vstack([merged_objs, improved_objs])

        # Survival: fill by front, break the last front by crowding distance.
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

        if verbose:
            print(f"  iter {iteration}: evals={evaluations}")

    final = fast_nondominated_sort(objs)[0]
    return {
        "pareto_genes": pop[final],
        "pareto_objs": objs[final],
        "evaluations": evaluations,
        "iterations": iteration,
        "unique_subsets_cached": len(cache),
    }
