"""Tests for the FS-SDS implementation.

The properties checked here are the ones that make it FS-SDS rather than a
generic swarm: every hypothesis holds exactly k features for the whole run, the
diffusion move is a size-preserving swap off an ACTIVE agent's hypothesis, and
the budget counts distinct subsets. A version that quietly let k drift, or that
copied without the swap, would still run and still return a plausible subset.
"""
import numpy as np
import pytest

import fs_sds


def constant_objective(value=0.5):
    def fn(genes):
        return value
    return fn


# --------------------------------------------------------------------------
# The two moves
# --------------------------------------------------------------------------

def test_random_hypothesis_has_exactly_k_features():
    rng = np.random.RandomState(0)
    for k in (1, 3, 9):
        genes = fs_sds.random_hypothesis(20, k, rng)
        assert genes.dtype == bool
        assert int(genes.sum()) == k


def test_swap_preserves_size_and_changes_exactly_two_bits():
    rng = np.random.RandomState(0)
    genes = fs_sds.random_hypothesis(30, 6, rng)

    for _ in range(50):
        out = fs_sds.swap_once(genes, rng)
        assert int(out.sum()) == 6, "the swap changed the subset size"
        changed = np.flatnonzero(out != genes)
        assert changed.size == 2, "a swap drops exactly one and adds exactly one"
        # One bit went 1->0 and the other 0->1.
        assert sorted(genes[changed].tolist()) == [False, True]


def test_swap_is_a_noop_when_every_feature_is_selected():
    # k == n_features leaves nothing to swap in; the move must not corrupt the
    # hypothesis or raise.
    rng = np.random.RandomState(0)
    genes = np.ones(5, dtype=bool)

    out = fs_sds.swap_once(genes, rng)

    assert out.tolist() == genes.tolist()


# --------------------------------------------------------------------------
# Run invariants
# --------------------------------------------------------------------------

def test_every_evaluated_subset_has_exactly_k_features():
    seen = []

    def objective(genes):
        seen.append(int(genes.sum()))
        return float(np.where(genes)[0].sum())

    fs_sds.run_fs_sds(40, 7, objective, seed=1, stop_evaluations=300,
                      population_size=20, max_iterations=20)

    assert seen, "nothing was evaluated"
    assert set(seen) == {7}, f"subset size drifted off k: {sorted(set(seen))}"


def test_best_genes_is_the_best_subset_actually_scored():
    scores = {}

    def objective(genes):
        key = tuple(np.flatnonzero(genes).tolist())
        scores[key] = float(np.cos(sum(key)))
        return scores[key]

    out = fs_sds.run_fs_sds(25, 4, objective, seed=3, stop_evaluations=200,
                            population_size=15, max_iterations=15)

    assert out["best_score"] == pytest.approx(max(scores.values()))
    assert tuple(np.flatnonzero(out["best_genes"]).tolist()) in scores
    assert int(out["best_genes"].sum()) == 4


def test_budget_is_never_exceeded_and_is_reported():
    budget = 90
    calls = []

    def objective(genes):
        calls.append(np.flatnonzero(genes).tolist())
        return float(len(calls))

    out = fs_sds.run_fs_sds(60, 5, objective, seed=2, stop_evaluations=budget,
                            population_size=30, max_iterations=100)

    assert len(calls) <= budget
    assert out["evaluations"] == len(calls)
    assert out["stopped_on"] == "budget"
    distinct = {tuple(c) for c in calls}
    assert len(calls) == len(distinct), "a cached subset was refit"


def test_iterations_can_stop_the_run_before_the_budget():
    out = fs_sds.run_fs_sds(30, 3, constant_objective(), seed=0,
                            stop_evaluations=10_000, population_size=10,
                            max_iterations=4)

    assert out["iterations"] == 4
    assert out["stopped_on"] == "iterations"


def test_population_is_evaluated_once_on_initialisation():
    # A constant objective makes every agent active in the test phase (the rule
    # is `>=`), and distinct random hypotheses mean no context-sensitive resets,
    # so one sweep costs nothing and the whole bill is the initial population.
    pop = 12
    calls = []

    out = fs_sds.run_fs_sds(50, 4,
                            lambda g: calls.append(1) or 0.5,
                            seed=0, stop_evaluations=10_000,
                            population_size=pop, max_iterations=1)

    assert len(calls) == pop
    assert out["evaluations"] == pop
    assert out["context_resets"] == 0
    assert out["population_size"] == pop


def test_runs_are_reproducible_for_a_seed():
    def objective(genes):
        return float(np.sin(np.flatnonzero(genes).sum()))

    kw = dict(seed=17, stop_evaluations=150, population_size=20,
              max_iterations=10)
    a = fs_sds.run_fs_sds(40, 5, objective, **kw)
    b = fs_sds.run_fs_sds(40, 5, objective, **kw)

    assert a["best_score"] == b["best_score"]
    assert a["best_genes"].tolist() == b["best_genes"].tolist()
    assert a["evaluations"] == b["evaluations"]


def test_it_finds_a_planted_signal_at_the_right_k():
    """Five of sixty features carry the signal, and k is set to five.

    A correctness check, not a performance claim: a swarm that never
    concentrates on the planted features is broken.
    """
    signal = {2, 11, 23, 38, 49}

    def objective(genes):
        return float(len(set(np.flatnonzero(genes).tolist()) & signal))

    out = fs_sds.run_fs_sds(60, 5, objective, seed=5, stop_evaluations=4000,
                            population_size=50, max_iterations=200)

    assert set(np.flatnonzero(out["best_genes"]).tolist()) == signal


# --------------------------------------------------------------------------
# Guards
# --------------------------------------------------------------------------

@pytest.mark.parametrize("k", [0, -1, 31])
def test_k_must_fit_the_feature_count(k):
    with pytest.raises(ValueError):
        fs_sds.run_fs_sds(30, k, constant_objective(), stop_evaluations=10)


def test_population_must_allow_drawing_a_partner():
    # Both phases draw an agent OTHER than self; a population of one would spin
    # forever looking for it.
    with pytest.raises(ValueError):
        fs_sds.run_fs_sds(30, 3, constant_objective(), population_size=1,
                          stop_evaluations=10)


def test_stagnating_swarm_stops_instead_of_spinning():
    """A converged swarm must end the run, not burn the iteration guard.

    With a constant objective every agent is active at every test (the rule is
    `>=`), so no agent ever restarts and no new subset is ever produced. Before
    the barren-sweep guard this spun to `max_iterations`; on the real experiment
    that cost 5.5 hours per unit at 1.5 new fits/second.
    """
    calls = []

    out = fs_sds.run_fs_sds(200, 5, lambda g: calls.append(1) or 0.5,
                            seed=0, stop_evaluations=100_000,
                            population_size=20, max_barren_sweeps=10)

    assert out["stopped_on"] == "stagnation"
    assert out["iterations"] <= 12, "kept sweeping after the swarm had converged"
    assert out["evaluations"] < 100_000, "the budget should not have been reached"


def test_a_productive_search_is_not_cut_short_by_the_guard():
    """The guard must fire on convergence only, never on a working search.

    The objective gives every distinct subset its own score, so the test phase
    keeps producing inactive agents, inactive agents keep restarting, and new
    subsets keep arriving. Under those conditions the budget must be what stops
    the run.
    """
    def objective(genes):
        # Deterministic per subset, and spread out enough that ties are rare --
        # ties are what stall the swarm.
        key = np.flatnonzero(genes).tobytes()
        return float(abs(hash(key)) % 10_000) / 10_000.0

    out = fs_sds.run_fs_sds(300, 4, objective, seed=1, stop_evaluations=400,
                            population_size=30, max_barren_sweeps=10)

    assert out["stopped_on"] == "budget"
    assert out["evaluations"] == 400
