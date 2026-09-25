"""Tests for the fit-capped stopping condition.

The cap exists so that two variants of the algorithm can be compared at equal
compute. That makes two properties load-bearing, and both are tested here:
the cap is *exact* (not "roughly, at the end of a generation"), and it counts
the same unit -- a model fit -- no matter which arm is running.
"""
import pytest

from conftest import N_FEATURES, RecordingEvaluator, item_from

from fastener import Config, EntropyOptimizer, FitBudgetExhausted
from item import (
    InformationGainSwapStrategy,
    IntersectionMatingWithWeightedRandomInformationGain,
    RandomEveryoneWithEveryone,
    RandomFlipMutationStrategy,
    RandomSwapStrategy,
)
from test_swap_strategies import CountingModelFactory, make_optimizer


def run_capped(tiny_data, run_dir, cap, name, swap_strategy=None, rounds=200):
    optimizer = make_optimizer(tiny_data, run_dir, swap_strategy, name,
                               rounds=rounds)
    optimizer.config.max_model_fits = cap
    optimizer.mainloop()
    return optimizer


# --------------------------------------------------------------------------
# Backwards compatibility
# --------------------------------------------------------------------------

def test_no_cap_by_default(tiny_data, run_dir):
    optimizer = make_optimizer(tiny_data, run_dir, rounds=4)

    assert optimizer.config.max_model_fits is None

    optimizer.mainloop()

    assert optimizer.stop_reason == "rounds"
    assert optimizer.rounds_completed == 4


def test_config_keeps_its_original_positional_order():
    """The new field is appended, so existing positional Config calls still work."""
    config = Config("out", 2020, 50, 3, 5)

    assert config.number_of_rounds == 50
    assert config.max_bucket_size == 3
    assert config.reset_to_pareto_rounds == 5
    assert config.max_model_fits is None


# --------------------------------------------------------------------------
# The cap itself
# --------------------------------------------------------------------------

def test_run_stops_exactly_at_the_cap(tiny_data, run_dir):
    """Exactly, not approximately -- an overshoot is unequal budget."""
    optimizer = run_capped(tiny_data, run_dir, cap=40, name="cap40")

    assert optimizer.model_fits == 40
    assert optimizer.stop_reason == "fit_budget"


@pytest.mark.parametrize("cap", [25, 40, 75])
def test_the_cap_is_exact_at_several_budgets(cap, tiny_data, run_dir):
    optimizer = run_capped(tiny_data, run_dir, cap=cap, name=f"cap{cap}")

    assert optimizer.model_fits == cap


@pytest.mark.parametrize("strategy", [None, RandomSwapStrategy, InformationGainSwapStrategy])
def test_every_arm_stops_at_the_same_budget(strategy, tiny_data, run_dir):
    """The whole point: arms are comparable because they spend the same."""
    swap = None if strategy is None else strategy()
    optimizer = run_capped(tiny_data, run_dir, cap=60,
                           name=f"arm_{strategy and strategy.__name__}",
                           swap_strategy=swap)

    assert optimizer.model_fits == 60
    assert optimizer.stop_reason == "fit_budget"


def test_swap_evaluations_are_charged_to_the_budget(tiny_data, run_dir):
    """A swap candidate is a fit, so it must consume budget like any other."""
    plain = run_capped(tiny_data, run_dir, cap=60, name="charge_plain")
    swapping = run_capped(tiny_data, run_dir, cap=60, name="charge_swap",
                          swap_strategy=InformationGainSwapStrategy())

    assert plain.model_fits == swapping.model_fits == 60
    # Same spend, but the swap arm spent part of it on replacement candidates,
    # so it cannot have completed as many generations.
    assert swapping.rounds_completed <= plain.rounds_completed


def test_the_counter_agrees_with_the_model_factory(tiny_data, run_dir):
    """`model_fits` must count real fits, not calls that might be cached."""
    optimizer = run_capped(tiny_data, run_dir, cap=50, name="agree")

    assert optimizer.factory.fits == optimizer.model_fits == 50


def test_cached_subsets_are_not_charged(tiny_data, run_dir):
    """Re-evaluating a known subset is free, so the budget counts UNIQUE fits."""
    optimizer = make_optimizer(tiny_data, run_dir, name="cache", rounds=1)
    optimizer.prepare_loop()
    before = optimizer.model_fits

    genes = item_from([0, 1, 2]).genes
    optimizer.fitness_function(genes)
    after_first = optimizer.model_fits
    for _ in range(5):
        optimizer.fitness_function(genes)

    assert after_first == before + 1
    assert optimizer.model_fits == after_first, "cache hits charged to the budget"


def test_budget_beats_rounds_and_rounds_beat_budget(tiny_data, run_dir):
    """Whichever limit binds first is the one that stops the run."""
    tight = run_capped(tiny_data, run_dir, cap=30, name="tight", rounds=200)
    loose = run_capped(tiny_data, run_dir, cap=100_000, name="loose", rounds=3)

    assert tight.stop_reason == "fit_budget"
    assert loose.stop_reason == "rounds"
    assert loose.rounds_completed == 3


def test_front_is_still_valid_after_an_interrupted_generation(tiny_data, run_dir):
    """Stopping mid-generation must not leave a dominated entry on the front."""
    optimizer = run_capped(tiny_data, run_dir, cap=47, name="interrupted",
                           swap_strategy=InformationGainSwapStrategy())

    front = optimizer.pareto_front
    assert front
    sizes = sorted(front)
    scores = [front[s].result.score for s in sizes]
    assert all(front[s].size == s for s in sizes)
    # Non-dominated: a bigger subset must score strictly better than any
    # smaller one, or it would have been pruned.
    assert scores == sorted(scores)
    assert len(set(scores)) == len(scores)


def test_a_cap_too_small_for_the_initial_population_is_reported(tiny_data, run_dir):
    """Better a clear error than a silent run with no search in it."""
    optimizer = make_optimizer(tiny_data, run_dir, name="impossible", rounds=5)
    optimizer.config.max_model_fits = 1

    with pytest.raises(FitBudgetExhausted, match="budget of 1 model fits"):
        optimizer.mainloop()


def test_capped_runs_are_reproducible(tiny_data, run_dir):
    a = run_capped(tiny_data, run_dir, cap=55, name="repro_a")
    b = run_capped(tiny_data, run_dir, cap=55, name="repro_b")

    assert {k: v.number for k, v in a.pareto_front.items()} == \
           {k: v.number for k, v in b.pareto_front.items()}
    assert a.model_fits == b.model_fits


# --------------------------------------------------------------------------
# Runner interface
# --------------------------------------------------------------------------

def test_run_fastener_passes_the_cap_through(tiny_data, run_dir, monkeypatch):
    """`run_fastener(max_fits=...)` must reach Config.max_model_fits."""
    import run_fastener

    seen = {}
    real_config = run_fastener.Config

    def spy(**kwargs):
        seen.update(kwargs)
        return real_config(**kwargs)

    monkeypatch.setattr(run_fastener, "Config", spy)

    ds = tiny_data

    class DS:
        n_features = N_FEATURES
        X_train, y_train = ds.X, ds.y
        X_val, y_val = ds.X_val, ds.y_val
        X_test, y_test = ds.X_val, ds.y_val

    res = run_fastener.run_fastener(DS(), run_dir, seed=2020, rounds=200,
                                    max_fits=45, initial_genes=[[0], [1]])

    assert seen["max_model_fits"] == 45
    assert res["model_fits"] == 45
    assert res["stopped_on"] == "fit_budget"
    assert res["params"]["max_fits"] == 45


def test_run_fastener_is_uncapped_by_default(tiny_data, run_dir, monkeypatch):
    import run_fastener

    seen = {}
    real_config = run_fastener.Config

    def spy(**kwargs):
        seen.update(kwargs)
        return real_config(**kwargs)

    monkeypatch.setattr(run_fastener, "Config", spy)

    ds = tiny_data

    class DS:
        n_features = N_FEATURES
        X_train, y_train = ds.X, ds.y
        X_val, y_val = ds.X_val, ds.y_val
        X_test, y_test = ds.X_val, ds.y_val

    res = run_fastener.run_fastener(DS(), run_dir, seed=2020, rounds=3,
                                    initial_genes=[[0], [1]])

    assert seen["max_model_fits"] is None
    assert res["stopped_on"] == "rounds"
