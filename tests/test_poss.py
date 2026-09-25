"""Tests for the POSS implementation.

POSS is small enough that a wrong version still runs and still returns a
plausible archive, so the invariants that distinguish it from "some mutation
loop with a front" are checked directly: the archive must stay a genuine Pareto
set, the 2k feasibility cut must hold, the fit budget must be exact, and the
search must actually find the signal on a problem where the answer is known.
"""
import numpy as np
import pytest

import poss


def counting_objective(scores):
    """Objective over a lookup, counting the calls the budget should charge."""
    calls = []

    def fn(genes):
        calls.append(np.where(genes)[0].tolist())
        return scores(genes)

    fn.calls = calls
    return fn


# --------------------------------------------------------------------------
# Dominance, the relation the whole algorithm rests on
# --------------------------------------------------------------------------

def test_weak_and_strict_dominance_agree_with_the_paper():
    better = (0.9, 3)   # higher score, fewer features
    worse = (0.8, 5)

    assert poss._weakly_dominates(better, worse)
    assert poss._strictly_dominates(better, worse)
    assert not poss._weakly_dominates(worse, better)

    # Equal vectors weakly but not strictly dominate, which is what lets an
    # incumbent be replaced without letting it block its own replacement.
    assert poss._weakly_dominates(better, better)
    assert not poss._strictly_dominates(better, better)

    # Incomparable: better score but more features.
    a, b = (0.9, 5), (0.8, 3)
    assert not poss._weakly_dominates(a, b)
    assert not poss._weakly_dominates(b, a)


# --------------------------------------------------------------------------
# Archive invariants
# --------------------------------------------------------------------------

def test_archive_is_a_pareto_set_with_unique_sizes():
    rng = np.random.RandomState(0)
    n = 40
    weights = rng.random_sample(n)

    def objective(genes):
        return float(weights[genes].sum()) / (1 + genes.sum())

    out = poss.run_poss(n, objective, k=8, seed=1, stop_evaluations=200)
    objs = out["archive_objs"]

    sizes = [size for _, size in objs]
    assert sizes == sorted(sizes), "archive is returned ordered by size"
    assert len(set(sizes)) == len(sizes), "one member per size"

    for a in objs:
        for b in objs:
            if a is not b:
                assert not poss._strictly_dominates(a, b), (
                    f"{b} survived in the archive despite {a} dominating it")


def test_no_infeasible_subset_is_ever_evaluated_or_kept():
    n, k = 30, 4
    objective = counting_objective(lambda g: float(g.sum()))  # pushes upward

    out = poss.run_poss(n, objective, k=k, seed=3, stop_evaluations=150)

    assert all(len(f) < 2 * k for f in objective.calls), (
        "a subset of 2k or more features was scored, which the paper defines "
        "as infeasible with f1 = -inf")
    assert all(size < 2 * k for _, size in out["archive_objs"])
    assert out["size_limit"] == 2 * k


def test_empty_set_starts_the_archive_stays_in_it_and_costs_no_fit():
    objective = counting_objective(lambda g: 1.0)

    out = poss.run_poss(20, objective, k=5, seed=0, stop_evaluations=50)

    assert all(f for f in objective.calls), "the empty set was sent to the model"
    # Nothing can dominate size 0, so the paper's starting point never leaves.
    assert out["archive_objs"][0] == (poss.EMPTY_OBJECTIVE, 0)


# --------------------------------------------------------------------------
# Budget accounting -- the basis of the whole comparison
# --------------------------------------------------------------------------

def test_budget_counts_distinct_subsets_exactly():
    budget = 120
    objective = counting_objective(lambda g: float(np.sin(g.sum())))

    out = poss.run_poss(50, objective, k=6, seed=2, stop_evaluations=budget)

    assert out["evaluations"] == budget
    assert len(objective.calls) == budget, "the objective was called off-budget"
    assert out["budget_exhausted"]


def test_repeated_subsets_are_served_from_cache_not_recharged():
    # Four features give 15 non-empty subsets in total, so the search must run
    # out of new ones long before a 500-fit budget and stop on the iteration
    # cap instead -- every draw after that is a cache hit.
    objective = counting_objective(lambda g: float(g.sum()))

    out = poss.run_poss(4, objective, k=3, seed=0, stop_evaluations=500,
                        max_iterations=2000)

    distinct = {tuple(c) for c in objective.calls}
    assert len(objective.calls) == len(distinct), "a cached subset was refit"
    assert out["evaluations"] < 500
    assert out["iterations"] == 2000, "the iteration cap is what stopped it"


def test_theoretical_budget_matches_the_paper():
    # T = 2*e*k^2*n; the number the run reports itself against.
    assert poss.theoretical_iterations(500, 50) == pytest.approx(
        np.ceil(2 * np.e * 2500 * 500), rel=0)


# --------------------------------------------------------------------------
# It has to actually work
# --------------------------------------------------------------------------

def test_poss_finds_a_planted_signal():
    """Three of fifty features carry all the signal; POSS should find them.

    Not a performance claim -- a correctness check. A search that never
    concentrates on the planted features is broken, not merely weak.
    """
    n = 50
    signal = {3, 17, 42}

    def objective(genes):
        picked = set(np.where(genes)[0].tolist())
        # Reward hits, charge for misses, so the optimum at size 3 is exactly
        # the planted set.
        return len(picked & signal) - 0.01 * len(picked - signal)

    out = poss.run_poss(n, objective, k=5, seed=7, stop_evaluations=3000)
    best = poss.poss_best(out)

    assert best is not None
    assert set(np.where(best)[0].tolist()) == signal


def test_poss_best_respects_k_even_when_the_archive_runs_wider():
    n, k = 30, 3

    def objective(genes):
        return float(genes.sum())  # bigger is always better, up to 2k-1

    out = poss.run_poss(n, objective, k=k, seed=5, stop_evaluations=400)

    assert max(size for _, size in out["archive_objs"]) > k, (
        "archive should hold subsets above k -- that is what fills the k-grid")
    assert int(poss.poss_best(out).sum()) == k


def test_runs_are_reproducible_for_a_seed():
    def objective(genes):
        return float(np.cos(genes.sum()) + 0.001 * np.where(genes)[0].sum())

    a = poss.run_poss(30, objective, k=4, seed=11, stop_evaluations=200)
    b = poss.run_poss(30, objective, k=4, seed=11, stop_evaluations=200)

    assert a["archive_objs"] == b["archive_objs"]
    assert a["evaluations"] == b["evaluations"]


def test_k_must_be_positive():
    with pytest.raises(ValueError):
        poss.run_poss(10, lambda g: 0.0, k=0)
