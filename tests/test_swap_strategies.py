"""Tests for the swap operators added to FASTENER's pruning step.

Two things are under test:

1. The new behaviour -- that a swap proposes a same-sized replacement, that the
   guided variant actually uses the permutation scores and the mutual
   information, and that it costs one model fit per candidate.
2. That the default path is untouched. Every existing call site constructs
   `EntropyOptimizer` without a swap strategy, and must keep running exactly
   the published algorithm.
"""
import collections
import pickle

import numpy as np
import pytest
from sklearn.tree import DecisionTreeClassifier

from conftest import N_FEATURES, RecordingEvaluator, item_from, selected

import random_utils
from fastener import Config, EntropyOptimizer
from item import (
    InformationGainSwapStrategy,
    IntersectionMatingWithWeightedRandomInformationGain,
    Item,
    RandomEveryoneWithEveryone,
    RandomFlipMutationStrategy,
    RandomSwapStrategy,
    SwapStrategy,
)


class CountingModelFactory:
    def __init__(self):
        self.fits = 0

    def __call__(self):
        self.fits += 1
        return DecisionTreeClassifier(random_state=0)


def make_optimizer(tiny_data, run_dir, swap_strategy=None, name="opt", rounds=3,
                   seed=2020, **kwargs):
    ds = tiny_data
    mating = RandomEveryoneWithEveryone(
        pool_size=3,
        mating_strategy=IntersectionMatingWithWeightedRandomInformationGain())
    factory = CountingModelFactory()
    optimizer = EntropyOptimizer(
        factory, ds.X, ds.y, RecordingEvaluator(ds.X_val, ds.y_val), N_FEATURES,
        mating, RandomFlipMutationStrategy(1.0 / N_FEATURES),
        initial_genes=[[0], [1], [5]],
        config=Config(output_folder=name, random_seed=seed,
                      number_of_rounds=rounds, reset_to_pareto_rounds=2),
        **kwargs,
        swap_strategy=swap_strategy,
    )
    optimizer.factory = factory
    return optimizer


def prepared(tiny_data, run_dir, swap_strategy=None, name="opt", **kwargs):
    optimizer = make_optimizer(tiny_data, run_dir, swap_strategy, name, **kwargs)
    optimizer.prepare_loop()
    return optimizer


# --------------------------------------------------------------------------
# Backwards compatibility
# --------------------------------------------------------------------------

def test_optimizer_builds_with_the_original_positional_signature(tiny_data, run_dir):
    """The pre-existing call shape must still work, and must mean "no swap"."""
    ds = tiny_data
    mating = RandomEveryoneWithEveryone(
        pool_size=3,
        mating_strategy=IntersectionMatingWithWeightedRandomInformationGain())
    optimizer = EntropyOptimizer(
        CountingModelFactory(), ds.X, ds.y,
        RecordingEvaluator(ds.X_val, ds.y_val), N_FEATURES,
        mating, RandomFlipMutationStrategy(1.0 / N_FEATURES), None, None,
        [[0], [1]], Config(output_folder="legacy", random_seed=2020,
                           number_of_rounds=2),
    )
    assert optimizer.swap_strategy is None


def test_legacy_purge_item_still_returns_one_smaller_item(tiny_data, run_dir):
    """`purge_item_with_information_gain` kept its name, arity and return type."""
    optimizer = prepared(tiny_data, run_dir)
    item = item_from([0, 1, 2, 7]).evaluate(optimizer.fitness_function)

    purged = optimizer.purge_item_with_information_gain(item)

    assert purged.size == item.size - 1
    assert selected(purged.genes) < selected(item.genes)


def test_without_swap_strategy_only_the_deletion_candidate_is_produced(tiny_data, run_dir):
    optimizer = prepared(tiny_data, run_dir)
    item = item_from([0, 1, 2, 7]).evaluate(optimizer.fitness_function)

    candidates = optimizer.purge_item_candidates(item)

    assert len(candidates) == 1
    assert candidates[0].size == item.size - 1


def test_default_run_is_unchanged_by_the_new_parameter(tiny_data, run_dir):
    """Passing swap_strategy=None explicitly == not passing it at all."""
    implicit = prepared(tiny_data, run_dir, name="implicit")
    implicit.mainloop()

    explicit = prepared(tiny_data, run_dir, swap_strategy=None, name="explicit")
    explicit.mainloop()

    assert {k: v.number for k, v in implicit.pareto_front.items()} == \
           {k: v.number for k, v in explicit.pareto_front.items()}


def test_default_run_does_not_consult_a_swap_strategy(tiny_data, run_dir, monkeypatch):
    """Nothing in the default path may reach into the swap machinery."""
    def explode(*_args, **_kwargs):
        raise AssertionError("swap strategy used on the default path")

    monkeypatch.setattr(SwapStrategy, "propose", explode)
    optimizer = prepared(tiny_data, run_dir)
    optimizer.mainloop()  # must not raise

    assert optimizer.pareto_front


# --------------------------------------------------------------------------
# What a swap proposes
# --------------------------------------------------------------------------

@pytest.mark.parametrize("strategy", [RandomSwapStrategy, InformationGainSwapStrategy])
def test_swap_candidate_keeps_the_size_and_changes_the_subset(strategy, tiny_data, run_dir):
    optimizer = prepared(tiny_data, run_dir, swap_strategy=strategy())
    item = item_from([0, 1, 2, 7]).evaluate(optimizer.fitness_function)

    candidates = optimizer.purge_item_candidates(item)

    assert len(candidates) == 2
    deletion, swapped = candidates
    assert deletion.size == item.size - 1
    assert swapped.size == item.size
    assert swapped.number != item.number

    before, after = selected(item.genes), selected(swapped.genes)
    assert len(before - after) == 1, "exactly one feature dropped"
    assert len(after - before) == 1, "exactly one feature inserted"
    assert (after - before).isdisjoint(before), "inserted feature was not selected"


@pytest.mark.parametrize("strategy", [RandomSwapStrategy, InformationGainSwapStrategy])
def test_number_of_swaps_gives_that_many_distinct_candidates(strategy, tiny_data, run_dir):
    optimizer = prepared(tiny_data, run_dir,
                         swap_strategy=strategy(number_of_swaps=3))
    item = item_from([0, 1, 2, 7]).evaluate(optimizer.fitness_function)

    candidates = optimizer.purge_item_candidates(item)

    assert len(candidates) == 4  # one deletion + three swaps
    swaps = candidates[1:]
    assert len({c.number for c in swaps}) == 3
    assert all(c.size == item.size for c in swaps)


@pytest.mark.parametrize("strategy", [RandomSwapStrategy, InformationGainSwapStrategy])
def test_a_full_subset_has_nothing_to_insert(strategy, tiny_data, run_dir):
    optimizer = prepared(tiny_data, run_dir, swap_strategy=strategy())
    item = item_from(range(N_FEATURES)).evaluate(optimizer.fitness_function)

    candidates = optimizer.purge_item_candidates(item)

    assert len(candidates) == 1, "no room for a swap, so deletion only"


@pytest.mark.parametrize("strategy", [RandomSwapStrategy, InformationGainSwapStrategy])
def test_more_swaps_requested_than_available(strategy, tiny_data, run_dir):
    """Asking for more insertions than there are unselected features is capped."""
    optimizer = prepared(tiny_data, run_dir,
                         swap_strategy=strategy(number_of_swaps=5))
    item = item_from(range(N_FEATURES - 2)).evaluate(optimizer.fitness_function)

    candidates = optimizer.purge_item_candidates(item)

    assert len(candidates) == 1 + 2


def test_propose_without_permutation_scores_returns_nothing(tiny_data):
    """Defensive: an empty `changes` list means there is nothing to remove."""
    strategy = RandomSwapStrategy()
    assert strategy.propose(item_from([0, 1]), []) == []


# --------------------------------------------------------------------------
# Guidance: which feature leaves, which feature enters
# --------------------------------------------------------------------------

def test_guided_swap_removes_the_permutation_weakest_feature():
    """The same feature the original pruning step would have deleted."""
    strategy = InformationGainSwapStrategy()
    # (score drop, gene index), as purge_item_candidates builds them, sorted.
    changes = sorted([(0.30, 0), (0.01, 5), (0.20, 9)])

    assert strategy.select_removal(None, changes) == 5


def test_random_swap_removal_is_not_tied_to_the_permutation_scores():
    strategy = RandomSwapStrategy()
    genes = [i in (0, 5, 9) for i in range(N_FEATURES)]
    changes = sorted([(0.30, 0), (0.01, 5), (0.20, 9)])

    random_utils.seed(1234)
    removals = {strategy.select_removal(genes, changes) for _ in range(60)}

    assert removals == {0, 5, 9}, "random removal should reach every selected feature"


def test_guided_insertion_follows_the_mutual_information():
    strategy = InformationGainSwapStrategy()
    information_gain = np.full(N_FEATURES, 0.001)
    information_gain[8] = 5.0  # one clearly dominant unselected feature
    strategy.use_data_information(None, None, information_gain)
    genes = [i in (0, 1, 2) for i in range(N_FEATURES)]

    random_utils.seed(7)
    counts = collections.Counter(
        strategy.select_insertions(genes, removed=0, count=1)[0]
        for _ in range(200)
    )

    uniform_share = 200 / (N_FEATURES - 3)
    assert counts[8] > 4 * uniform_share, counts


def test_random_insertion_ignores_the_mutual_information():
    strategy = RandomSwapStrategy()
    genes = [i in (0, 1, 2) for i in range(N_FEATURES)]

    random_utils.seed(7)
    counts = collections.Counter(
        strategy.select_insertions(genes, removed=0, count=1)[0]
        for _ in range(300)
    )

    assert set(counts) == set(range(3, N_FEATURES))
    # Uniform enough that no candidate takes a dominant share.
    assert max(counts.values()) < 3 * (300 / (N_FEATURES - 3)), counts


def test_guided_insertion_falls_back_to_uniform_when_no_feature_is_informative():
    strategy = InformationGainSwapStrategy()
    strategy.use_data_information(None, None, np.zeros(N_FEATURES))
    genes = [i in (0, 1) for i in range(N_FEATURES)]

    random_utils.seed(3)
    picks = {strategy.select_insertions(genes, removed=0, count=1)[0]
             for _ in range(200)}

    assert picks == set(range(2, N_FEATURES))


def test_guided_insertion_can_reach_a_zero_information_feature():
    """Sampling without replacement must not fail when most weights are zero."""
    strategy = InformationGainSwapStrategy(number_of_swaps=3)
    information_gain = np.zeros(N_FEATURES)
    information_gain[11] = 1.0
    strategy.use_data_information(None, None, information_gain)
    genes = [i in (0, 1) for i in range(N_FEATURES)]

    picks = strategy.select_insertions(genes, removed=0, count=3)

    assert len(set(picks)) == 3


# --------------------------------------------------------------------------
# Plumbing of the mutual-information vector
# --------------------------------------------------------------------------

def test_guided_swap_reuses_the_mating_strategys_vector(tiny_data, run_dir, monkeypatch):
    """The point of the plumbing: no second `mutual_info_classif` pass."""
    import sklearn.feature_selection

    calls = []
    real = sklearn.feature_selection.mutual_info_classif

    def counting(*args, **kwargs):
        calls.append(1)
        return real(*args, **kwargs)

    monkeypatch.setattr(sklearn.feature_selection, "mutual_info_classif", counting)

    strategy = InformationGainSwapStrategy()
    optimizer = prepared(tiny_data, run_dir, swap_strategy=strategy)

    assert len(calls) == 1, "mutual information computed more than once"
    np.testing.assert_array_equal(
        np.asarray(strategy.scikit_information_gain),
        np.asarray(optimizer.mating_information_gain()))


def test_guided_swap_computes_its_own_vector_when_mating_has_none(tiny_data):
    ds = tiny_data
    strategy = InformationGainSwapStrategy()

    strategy.use_data_information(ds.X, ds.y, None)

    assert len(strategy.scikit_information_gain) == N_FEATURES


def test_mating_information_gain_is_none_for_a_mating_strategy_without_one(tiny_data, run_dir):
    from item import UnionMating

    ds = tiny_data
    optimizer = EntropyOptimizer(
        CountingModelFactory(), ds.X, ds.y,
        RecordingEvaluator(ds.X_val, ds.y_val), N_FEATURES,
        RandomEveryoneWithEveryone(pool_size=3, mating_strategy=UnionMating()),
        RandomFlipMutationStrategy(1.0 / N_FEATURES),
        initial_genes=[[0], [1]],
        config=Config(output_folder="no_ig", random_seed=2020, number_of_rounds=1),
    )
    optimizer.prepare_loop()

    assert optimizer.mating_information_gain() is None


# --------------------------------------------------------------------------
# Cost, and the front update
# --------------------------------------------------------------------------

def test_each_swap_candidate_costs_exactly_one_extra_fit(tiny_data, run_dir):
    """The honest unit: one extra fit per pruned subset, no extra scoring pass."""
    baseline = prepared(tiny_data, run_dir, name="cost_base")
    item = item_from([0, 1, 2, 7]).evaluate(baseline.fitness_function)
    before = baseline.factory.fits
    baseline.purge_item_candidates(item)
    deletion_only = baseline.factory.fits - before

    swapping = prepared(tiny_data, run_dir, name="cost_swap",
                        swap_strategy=InformationGainSwapStrategy())
    item = item_from([0, 1, 2, 7]).evaluate(swapping.fitness_function)
    before = swapping.factory.fits
    swapping.purge_item_candidates(item)
    with_swap = swapping.factory.fits - before

    assert with_swap == deletion_only + 1


def test_swap_candidate_can_win_its_size_slot_on_the_front(tiny_data, run_dir, monkeypatch):
    """A same-sized swap competes against the incumbent front entry at that size."""
    optimizer = prepared(tiny_data, run_dir,
                         swap_strategy=InformationGainSwapStrategy())
    # A deliberately poor 3-feature subset made only of noise columns, so a
    # swap towards an informative feature has somewhere to go.
    weak = item_from([9, 10, 11]).evaluate(optimizer.fitness_function)
    optimizer.pareto_front = {3: weak}

    # Watch the size-3 slot in isolation. Normal Pareto pruning drops that slot
    # as soon as the size-2 deletion candidate scores as well as it does, which
    # would hide the replacement rather than contradict it.
    monkeypatch.setattr(EntropyOptimizer, "remove_pareto_non_optimal",
                        lambda self: None)

    random_utils.seed(11)
    for _ in range(10):
        optimizer.purge_front_with_information_gain()
        entry = optimizer.pareto_front[3]
        if entry.number != weak.number:
            break

    assert entry.number != weak.number, "no same-sized replacement entered the front"
    assert entry.size == 3
    assert entry.result.score > weak.result.score


@pytest.mark.parametrize("strategy", [None, RandomSwapStrategy, InformationGainSwapStrategy])
def test_mainloop_runs_end_to_end(strategy, tiny_data, run_dir):
    swap = None if strategy is None else strategy()
    optimizer = prepared(tiny_data, run_dir, swap_strategy=swap, rounds=6)

    optimizer.mainloop()

    assert optimizer.pareto_front
    for size, entry in optimizer.pareto_front.items():
        assert entry.size == size
        assert 0.0 <= entry.result.score <= 1.0


@pytest.mark.parametrize("strategy", [None, RandomSwapStrategy, InformationGainSwapStrategy])
def test_same_seed_gives_the_same_front(strategy, tiny_data, run_dir):
    fronts = []
    for run in range(2):
        swap = None if strategy is None else strategy()
        optimizer = prepared(tiny_data, run_dir, swap_strategy=swap,
                             name=f"repeat{run}", rounds=5)
        optimizer.mainloop()
        fronts.append({k: v.number for k, v in optimizer.pareto_front.items()})

    assert fronts[0] == fronts[1]


@pytest.mark.parametrize("strategy", [RandomSwapStrategy, InformationGainSwapStrategy])
def test_optimizer_with_a_swap_strategy_is_still_picklable(strategy, tiny_data, run_dir):
    """`prepare_loop` pickles the whole optimizer; strategies must survive it."""
    optimizer = prepared(tiny_data, run_dir, swap_strategy=strategy())

    restored = pickle.loads(pickle.dumps(optimizer))

    assert isinstance(restored.swap_strategy, strategy)


def test_swap_does_not_disturb_the_pareto_front_invariants(tiny_data, run_dir):
    """Front entries stay keyed by their own size and stay non-dominated."""
    optimizer = prepared(tiny_data, run_dir,
                         swap_strategy=InformationGainSwapStrategy(), rounds=8)
    optimizer.mainloop()

    sizes = sorted(optimizer.pareto_front)
    scores = [optimizer.pareto_front[s].result.score for s in sizes]
    assert all(optimizer.pareto_front[s].size == s for s in sizes)
    assert scores == sorted(scores), "a larger subset scored no better than a smaller one"


# --------------------------------------------------------------------------
# The experiment-runner interface
# --------------------------------------------------------------------------

def test_make_swap_strategy_defaults_to_the_original_algorithm():
    from run_fastener import make_swap_strategy

    assert make_swap_strategy(None) is None
    assert make_swap_strategy("none") is None


def test_make_swap_strategy_builds_each_arm():
    from run_fastener import make_swap_strategy

    assert isinstance(make_swap_strategy("random"), RandomSwapStrategy)
    assert isinstance(make_swap_strategy("guided"), InformationGainSwapStrategy)
    assert make_swap_strategy("guided", number_of_swaps=4).number_of_swaps == 4


def test_make_swap_strategy_rejects_an_unknown_arm():
    from run_fastener import make_swap_strategy

    with pytest.raises(ValueError, match="unknown swap arm"):
        make_swap_strategy("sideways")
