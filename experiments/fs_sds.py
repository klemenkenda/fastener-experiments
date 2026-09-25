"""FS-SDS: Feature Selection using Stochastic Diffusion Search.

Paper:  H. Alhakbani and M. M. al-Rifaie, "Feature selection using stochastic
        diffusion search", GECCO 2017, pp. 385-392.
        https://doi.org/10.1145/3071178.3079193
Source: https://github.com/mohmaj/SDS-FS -- `SDSFS.py`, written by the paper's
        first author and updated by the second in November 2020.

This is **the FASTENER paper's own comparator**: reference [12] of Koprivec,
Kenda & Sircelj (2020), where it appears under the name FS-SDS, alongside POSS
(reference [11], see `poss.py`) and DT-forward. The FASTENER paper reports
beating it on 24 of 25 benchmark data sets, so the interesting question here is
not whether it wins but whether this experiment's protocol reproduces that.

NOT A LINE-BY-LINE PORT, AND NOT THE AUTHORS' RESULTS. The reference repository
carries no licence, so the algorithm below is written fresh from reading it
rather than adapted from its text. The mechanics are theirs; the code is not.

Stochastic Diffusion Search (Bishop 1989) is a swarm method in which a
population of agents each hold a *hypothesis* and alternate two phases: a TEST
that marks each agent active or inactive, and a DIFFUSION in which inactive
agents copy hypotheses from active ones (and lost agents restart at random).
Information moves through the population by direct agent-to-agent contact
rather than through a shared fitness ranking.

As the authors instantiate it for feature selection:

  HYPOTHESIS   a feature subset of EXACTLY k features, as a binary vector.
               k is fixed for the whole run -- the size objective FASTENER,
               POSS and NSGA-II all optimise does not exist here. One run
               answers for one k.
  TEST         each agent draws another agent uniformly at random and becomes
               active iff its own score is >= that agent's. This is a relative
               test against a random peer, not a threshold on the score.
  DIFFUSION    an inactive agent draws a random agent; if that agent is active
               it copies its hypothesis and applies ONE random swap (one
               selected feature dropped, one unselected feature added); if not,
               it restarts from a random subset. An active agent draws a random
               agent and, if that agent is active and holds an IDENTICAL
               hypothesis, it goes inactive and restarts -- the "context
               sensitive" rule that stops the swarm collapsing onto one point.

Note what the diffusion move is: a uniform-random, SIZE-PRESERVING SWAP. That
is the same neighbourhood as the random-swap arm proposed for FASTENER in
TODO.md, published in 2017 and cited by the FASTENER paper itself. It is prior
art for the swap operator, though not for guiding it -- FS-SDS chooses both
ends uniformly and has no information-gain term anywhere.

TWO DEPARTURES, both to make the comparison controlled:

1. CLASSIFIER AND SCORE. The authors score a subset with an SVM (RBF) on an
   internal random 80:20 split, re-split on every evaluation; the FASTENER paper
   ran it with an Extreme Learning Machine of 160 hidden sigmoid units, and gave
   it the full data set because of that internal splitting. Here the objective is
   the one every method in this experiment is scored by -- weighted F1 of a
   decision tree fit on train, scored on the fixed validation split. The
   re-splitting matters beyond the choice of learner: with a fresh split per
   evaluation the same subset scores differently each time, so a comparison
   between two agents partly measures split noise. The fixed split removes that
   and lets the result cache be correct.

2. BUDGET, WHICH IS PER-K BY CONSTRUCTION. Because a run answers for one k, a
   curve over the k-grid costs one run per k. The FASTENER paper reports FS-SDS
   using 30,000 model evaluations *per k* against ~11,000-16,000 for the whole
   of FASTENER's Pareto front, and 120,000 against 1,000 on the EO data. The
   caller therefore sets a budget PER RUN, matched to what every other search
   gets, and the total is reported separately. Splitting one shared budget
   across the grid instead would leave a few hundred fits per k and build a
   strawman; the cost asymmetry belongs in the reported total, not in a
   handicap.

Faithful to the source: fixed-size hypotheses, the random-peer test, the
copy-with-one-swap diffusion, the random restart when the drawn agent is
inactive, context-sensitive deactivation on duplicate hypotheses, in-place
population update within a diffusion sweep, and evaluation only of agents whose
hypothesis changed.

WHAT IT ACTUALLY DOES HERE, so the numbers are not a surprise. On MADELON,
seed 2020, 6000 fits per k: k=5 reaches test F1 0.819, k=10 reaches 0.754,
k=20 reaches 0.798, each in ~118 sweeps. That k=5 result is ABOVE what FASTENER
(~0.81) and POSS (~0.80) reach on the same split -- FS-SDS is a live competitor
under this protocol, not a walkover, and the cost is where it loses: three k
values cost 18,000 fits against 6,000 for one complete run of either of them.
Roughly half of all diffusion moves are random restarts, because the drawn
partner is inactive about half the time; that is the algorithm, not a bug, and
it is why FS-SDS keeps finding fresh regions at the price of re-sampling.
"""
from typing import Callable, Dict, List, Optional

import numpy as np

# The reference implementation's settings (`SDSFS.py`, non-test run).
DEFAULT_POPULATION = 100
REFERENCE_ITERATIONS = 50

# ...but 50 sweeps at a population of 100 exhaust themselves after ~2600 model
# fits on MADELON, i.e. well UNDER the budget every other search in this
# experiment is given. Those defaults come from a demo on data sets of 6 and 34
# features; stopping there would hand FS-SDS less compute than its competitors
# and then report it as weaker. So the iteration cap is off by default and the
# fit budget is what stops a run. Pass max_iterations=REFERENCE_ITERATIONS to
# get the reference behaviour back.
MAX_ITERATIONS_GUARD = 1_000_000

# THE SWARM CAN STALL, AND THEN THE BUDGET NEVER ARRIVES.
#
# The test phase marks an agent active when its score is >= a random peer's, so
# on a data set where many subsets score IDENTICALLY -- which is the norm at 44
# training rows, as on ALLAML -- nearly every agent is active. Diffusion only
# creates novelty through agents that are inactive (they restart at random) or
# through the duplicate-hypothesis reset, so once the swarm is all-active it
# stops generating unseen subsets almost entirely: measured on ALLAML at k=10,
# 2000 sweeps produced 424 restarts and 1103 new subsets, then nothing.
#
# With no iteration cap that state spins until MAX_ITERATIONS_GUARD, doing
# cache lookups and no work. In the first full run it cost 5.5 HOURS per unit
# at 1.5 new fits/second on hardware good for 430.
#
# So: stop after this many consecutive sweeps that produce no new evaluation.
# This is not a departure from the method -- the method has simply converged,
# and the reference implementation's own 50-sweep cap would have stopped it far
# sooner. It is reported as stopped_on="stagnation", because "FS-SDS could not
# use the budget it was given" is a result about the method and must be visible
# rather than hidden inside a wall-clock number.
MAX_BARREN_SWEEPS = 50

# What the FASTENER paper gave FS-SDS per k, for reporting how truncated a run
# at this experiment's budget is (Table 3 of Koprivec, Kenda & Sircelj 2020).
PAPER_EVALUATIONS_PER_K = 30000


def random_hypothesis(n_features: int, k: int, rng) -> np.ndarray:
    """A uniformly random subset of exactly k features."""
    genes = np.zeros(n_features, dtype=bool)
    genes[rng.choice(n_features, size=k, replace=False)] = True
    return genes


def swap_once(genes: np.ndarray, rng) -> np.ndarray:
    """Drop one selected feature, add one unselected: the diffusion offset.

    Size-preserving by construction, which is the whole point -- every agent in
    the swarm holds exactly k features for the entire run.
    """
    out = genes.copy()
    selected = np.flatnonzero(out)
    unselected = np.flatnonzero(~out)
    if selected.size and unselected.size:
        out[selected[rng.randint(selected.size)]] = False
        out[unselected[rng.randint(unselected.size)]] = True
    return out


def run_fs_sds(n_features: int,
               k: int,
               objective: Callable[[np.ndarray], float],
               seed: int = 0,
               stop_evaluations: int = 6000,
               population_size: int = DEFAULT_POPULATION,
               max_iterations: Optional[int] = None,
               max_barren_sweeps: int = MAX_BARREN_SWEEPS,
               use_cache: bool = True,
               progress_cb: Optional[Callable[[int], None]] = None) -> Dict:
    """Run FS-SDS for a single subset size k.

    `objective` takes a boolean gene vector and returns a score to MAXIMISE. It
    is called once per distinct subset; repeats come from a cache and are not
    charged to the budget, as in `run_poss` and `run_nsga2`.

    The run stops at whichever comes first: `stop_evaluations` distinct subsets
    scored, or `max_iterations` diffusion sweeps. `max_iterations` defaults to
    no cap, so the budget is what stops it -- see MAX_ITERATIONS_GUARD above for
    why the reference implementation's 50 is not the default. Which rule
    stopped the run is reported in `stopped_on` rather than left to be inferred.
    """
    if not 1 <= k <= n_features:
        raise ValueError(f"k must be in 1..{n_features}, got {k}")
    if population_size < 2:
        # The test and diffusion phases both draw a partner OTHER than self.
        raise ValueError("population_size must be at least 2")
    if max_iterations is None:
        max_iterations = MAX_ITERATIONS_GUARD

    rng = np.random.RandomState(seed)
    cache: Dict[bytes, float] = {}
    evaluations = 0
    budget_reached = False

    best_genes: Optional[np.ndarray] = None
    best_score = -np.inf

    def score_of(genes: np.ndarray) -> float:
        """Evaluate, charging the budget only for a subset not seen before.

        With `use_cache=False` every call is charged and re-evaluated, which is
        what the authors' reference implementation does: its objective re-splits
        the data on each call, so the same subset genuinely has no single score
        and a cache would be wrong.
        """
        nonlocal evaluations, best_genes, best_score, budget_reached
        if not use_cache:
            if evaluations >= stop_evaluations:
                budget_reached = True
                return -np.inf
            value = objective(genes)
            evaluations += 1
            if progress_cb is not None and evaluations % 25 == 0:
                progress_cb(evaluations)
            if value > best_score:
                best_score, best_genes = value, genes.copy()
            return value
        key = np.packbits(genes).tobytes()
        if key not in cache:
            if evaluations >= stop_evaluations:
                budget_reached = True
                # Out of budget: fall back to the worst possible score rather
                # than sneaking in an uncharged fit. The caller sees the run
                # stopped on the budget.
                return -np.inf
            cache[key] = objective(genes)
            evaluations += 1
            if progress_cb is not None and evaluations % 25 == 0:
                progress_cb(evaluations)
        value = cache[key]
        if value > best_score:
            best_score, best_genes = value, genes.copy()
        return value

    # ---- initialisation: a random hypothesis per agent, all evaluated -------
    hypotheses: List[np.ndarray] = [random_hypothesis(n_features, k, rng)
                                    for _ in range(population_size)]
    scores = [score_of(h) for h in hypotheses]
    active = [False] * population_size

    def other_than(i: int) -> int:
        j = rng.randint(population_size)
        while j == i:
            j = rng.randint(population_size)
        return j

    iterations = 0
    restarts = 0
    context_resets = 0
    barren = 0          # consecutive sweeps that produced no new evaluation
    stagnated = False

    while iterations < max_iterations and not budget_reached:
        iterations += 1
        before = evaluations

        # ---- TEST: active iff at least as good as a random peer ------------
        for i in range(population_size):
            active[i] = scores[i] >= scores[other_than(i)]

        # ---- DIFFUSION -----------------------------------------------------
        # Agents are updated in place as the sweep proceeds, so a later agent
        # can copy from an earlier agent's new hypothesis. That is what the
        # reference implementation does; making the sweep simultaneous would be
        # a different algorithm.
        for i in range(population_size):
            j = other_than(i)
            if not active[i]:
                if active[j]:
                    hypotheses[i] = swap_once(hypotheses[j], rng)
                else:
                    hypotheses[i] = random_hypothesis(n_features, k, rng)
                    restarts += 1
                scores[i] = score_of(hypotheses[i])
            elif active[j] and np.array_equal(hypotheses[i], hypotheses[j]):
                # Context-sensitive diffusion: two active agents on the same
                # hypothesis is wasted search, so one of them restarts.
                active[i] = False
                hypotheses[i] = random_hypothesis(n_features, k, rng)
                context_resets += 1
                scores[i] = score_of(hypotheses[i])
            if budget_reached:
                break

        # A sweep that added nothing new means the swarm has converged; see
        # MAX_BARREN_SWEEPS.
        barren = 0 if evaluations > before else barren + 1
        if barren >= max_barren_sweeps:
            stagnated = True
            break

    return {
        "best_genes": best_genes,
        "best_score": best_score,
        "k": k,
        "evaluations": evaluations,
        "iterations": iterations,
        "restarts": restarts,
        "context_resets": context_resets,
        "population_size": population_size,
        "stopped_on": ("budget" if budget_reached
                       else "stagnation" if stagnated else "iterations"),
        "barren_sweeps_at_end": barren,
        "paper_evaluations_per_k": PAPER_EVALUATIONS_PER_K,
    }
