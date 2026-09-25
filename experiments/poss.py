"""POSS: Pareto Optimization for Subset Selection (Qian, Yu & Zhou, NIPS 2015).

Paper: "Subset Selection by Pareto Optimization", NeurIPS 28 (2015).
       https://papers.nips.cc/paper/2015/hash/b4d168b48157c623fbd095b4a565b5bb

Implemented here from Algorithm 1 of the paper, which is short and fully
specified -- unlike the NSGAII-MIIP port in `nsgaii_miip.py`, there is no large
MATLAB source being transliterated, so the room for a porting artefact is much
smaller. What the paper does not fix (the objective, and what to do with the
archive at the end) is documented as a departure below.

POSS is the closest published relative of FASTENER in the comparison set, and
that is why it is here: it maintains a Pareto ARCHIVE over (subset quality,
subset size) and advances it with single-parent bit-flip mutation, exactly
FASTENER's shape, but with no crossover, no information guidance and no pruning
step. It is therefore the control that says how much of FASTENER's result comes
from those extra operators rather than from Pareto archiving itself.

The algorithm, as published:

    P <- {0^n}
    repeat T times:
        s  <- uniformly at random from P
        s' <- flip each bit of s independently with probability 1/n
        if no z in P strictly dominates s':
            P <- (P minus {z in P : s' weakly dominates z}) union {s'}
    return argmax over {s in P : |s| <= k} of f(s)

with the bi-objective, as in the paper's constraint handling:

    f1(s) = -inf  if |s| >= 2k   (infeasible)   else  f(s)      [maximise]
    f2(s) = |s|                                                 [minimise]

THREE DEPARTURES, all to make the comparison controlled rather than to change
the method:

1. OBJECTIVE. The paper's f is R^2 for sparse regression, and a monotone set
   function for the theory. Here f is the objective every other method in this
   experiment is scored by -- weighted F1 of a decision tree fit on train and
   scored on validation -- so that differences reflect the SEARCH. This does
   cost POSS its approximation guarantee, which is stated for submodular f; a
   wrapper score is not submodular. The guarantee is not what is being compared.

2. BUDGET. The paper's T is 2*e*k^2*n iterations. At n=500, k=50 that is 6.8M
   objective evaluations, against the ~6000 model fits every arm in this
   experiment is given. POSS is run at the shared budget, because a comparison
   in which one arm gets a thousand times the compute measures nothing -- but
   the theoretical T is recorded in the result as `theoretical_evaluations`
   next to the granted one. **POSS at this budget is POSS truncated far below
   the regime its guarantee describes, and a weak showing here is evidence
   about its anytime behaviour, not about the published algorithm.**

3. OUTPUT. The paper returns the single best feasible subset with |s| <= k.
   Here the whole archive is returned, since the comparison is a curve over
   feature counts and the archive already is that curve; the paper's own answer
   is recovered by `poss_best` and reported separately.

Everything else -- the empty-set start, uniform parent selection, the 1/n
bit-flip, the dominance test on acceptance, the weak-dominance sweep on
insertion, and the 2k feasibility cut -- follows the pseudocode as written.

WHAT THE BUDGET ACTUALLY BUYS. Measured on MADELON (n=500, k=50, seed 2020):
6000 model fits produce an archive spanning sizes 1..7 and no infeasible draw
at all. POSS starts empty and grows one accepted bit-flip at a time, so it
climbs the size axis slowly and the 2k cut never binds at this budget -- k is
close to inert here, and the run stops at ~7 features rather than at 2k-1.
That is the mirror image of the NSGAII-MIIP init problem in `nsgaii_miip.py`:
that search never comes DOWN below ~200 features, this one never gets UP past
single digits. Both are absent from part of the curve for structural reasons,
and `subset_size_reach` in the run manifest is where that is recorded rather
than left to look like missing data.
"""
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np

# f(empty set). The paper assumes f(0^n) = 0 for its monotone objectives; any
# value below the worst attainable F1 works identically here, since it only has
# to keep the empty set from dominating a real subset.
EMPTY_OBJECTIVE = 0.0

Objective = Tuple[float, int]  # (quality, to maximise; size, to minimise)


def _weakly_dominates(a: Objective, b: Objective) -> bool:
    """`a` is no worse than `b` on either objective."""
    return a[0] >= b[0] and a[1] <= b[1]


def _strictly_dominates(a: Objective, b: Objective) -> bool:
    """`a` weakly dominates `b` and is strictly better somewhere."""
    return _weakly_dominates(a, b) and (a[0] > b[0] or a[1] < b[1])


def theoretical_iterations(n_features: int, k: int) -> int:
    """The paper's T = 2*e*k^2*n, for reporting how truncated a run is."""
    return int(np.ceil(2 * np.e * k * k * n_features))


def run_poss(n_features: int,
             objective: Callable[[np.ndarray], float],
             k: int,
             seed: int = 0,
             stop_evaluations: int = 6000,
             max_iterations: Optional[int] = None,
             progress_cb: Optional[Callable[[int], None]] = None) -> Dict:
    """Run POSS until `stop_evaluations` distinct subsets have been scored.

    `objective` takes a boolean gene vector and returns a score to MAXIMISE. It
    is called once per distinct feasible subset; repeats are served from a cache
    and are not charged to the budget, matching how `run_nsga2` counts fits.

    Iterations that produce an infeasible subset (|s| >= 2k) or the empty set
    cost no model fit, because the paper's f1 is -inf there by definition and
    needs no evaluation. They still consume an iteration, so `max_iterations`
    (default: 500x the fit budget) bounds a run whose archive has saturated and
    is only re-drawing subsets it has already scored.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    rng = np.random.RandomState(seed)
    mutation_rate = 1.0 / n_features
    size_limit = 2 * k  # |s| >= 2k is infeasible
    if max_iterations is None:
        max_iterations = 500 * stop_evaluations

    archive_genes: List[np.ndarray] = [np.zeros(n_features, dtype=bool)]
    archive_objs: List[Objective] = [(EMPTY_OBJECTIVE, 0)]

    cache: Dict[bytes, float] = {}
    evaluations = 0
    iterations = 0
    infeasible = 0

    while evaluations < stop_evaluations and iterations < max_iterations:
        iterations += 1

        parent = archive_genes[rng.randint(len(archive_genes))]
        child = parent ^ (rng.random_sample(n_features) < mutation_rate)
        size = int(child.sum())

        if size == 0:
            obj: Objective = (EMPTY_OBJECTIVE, 0)
        elif size >= size_limit:
            # Infeasible by the paper's f1: strictly dominated by the empty set,
            # so it would always be rejected below. Never worth a model fit.
            infeasible += 1
            continue
        else:
            key = np.packbits(child).tobytes()
            if key not in cache:
                cache[key] = objective(child)
                evaluations += 1
                if progress_cb is not None and evaluations % 25 == 0:
                    progress_cb(evaluations)
            obj = (cache[key], size)

        if any(_strictly_dominates(z, obj) for z in archive_objs):
            continue

        keep = [i for i, z in enumerate(archive_objs)
                if not _weakly_dominates(obj, z)]
        archive_genes = [archive_genes[i] for i in keep] + [child]
        archive_objs = [archive_objs[i] for i in keep] + [obj]

    order = np.argsort([o[1] for o in archive_objs])
    return {
        "archive_genes": [archive_genes[i] for i in order],
        "archive_objs": [archive_objs[i] for i in order],
        "evaluations": evaluations,
        "iterations": iterations,
        "infeasible_draws": infeasible,
        "k": k,
        "size_limit": size_limit,
        "theoretical_evaluations": theoretical_iterations(n_features, k),
        "budget_exhausted": evaluations >= stop_evaluations,
    }


def poss_best(out: Dict) -> Optional[np.ndarray]:
    """The paper's own answer: the best archive member with |s| <= k.

    Returns the gene vector, or None if the archive holds nothing but the empty
    set -- only possible if the budget stopped the run before a single subset
    was accepted.
    """
    best, best_score = None, -np.inf
    for genes, (score, size) in zip(out["archive_genes"], out["archive_objs"]):
        if size == 0 or size > out["k"]:
            continue
        if score > best_score:
            best, best_score = genes, score
    return best
