"""Tests for the hypervolume scalar and the paired arm comparison.

Hypervolume is checked against areas computed by hand, because a subtly wrong
sweep still produces plausible-looking numbers that order the arms incorrectly.
"""
import math

import pytest

import analysis


def rec(k, test, val=None):
    """Minimal record in the shape `protocol.evaluate_subset` produces."""
    return {
        "n_features": k,
        "test_score": test,
        "val_score": test if val is None else val,
        "features": list(range(k)),
    }


# --------------------------------------------------------------------------
# The area itself
# --------------------------------------------------------------------------

def test_single_point_area_is_the_rectangle():
    # One point at k=2, score 0.8, reference (10, 0.0):
    #   (10 - 2) * (0.8 - 0.0) = 6.4
    assert analysis.hypervolume([rec(2, 0.8)], n_features=10) == pytest.approx(6.4)


def test_staircase_sums_its_slabs():
    # Points (2, 0.6) and (5, 0.9), reference (10, 0):
    #   slab 0.0->0.6 spanning k=2..10  -> 0.6 * 8 = 4.8
    #   slab 0.6->0.9 spanning k=5..10  -> 0.3 * 5 = 1.5
    front = [rec(2, 0.6), rec(5, 0.9)]

    assert analysis.hypervolume(front, n_features=10) == pytest.approx(6.3)


def test_dominated_points_add_nothing():
    """A bigger subset that scores no better must not inflate the number."""
    front = [rec(2, 0.6), rec(5, 0.9)]
    with_dominated = front + [rec(7, 0.5), rec(8, 0.9)]

    assert analysis.hypervolume(with_dominated, n_features=10) == \
           pytest.approx(analysis.hypervolume(front, n_features=10))


def test_duplicate_sizes_keep_only_the_best():
    front = [rec(3, 0.4), rec(3, 0.7)]

    assert analysis.hypervolume(front, n_features=10) == pytest.approx(0.7 * 7)


def test_the_all_features_point_contributes_nothing():
    """"Select everything" is the trivial non-solution; it must score zero."""
    assert analysis.hypervolume([rec(10, 0.95)], n_features=10) == 0.0


def test_a_better_front_has_a_larger_hypervolume():
    worse = [rec(5, 0.70)]
    better_score = [rec(5, 0.80)]
    fewer_features = [rec(3, 0.70)]

    base = analysis.hypervolume(worse, n_features=20)
    assert analysis.hypervolume(better_score, n_features=20) > base
    assert analysis.hypervolume(fewer_features, n_features=20) > base


def test_min_score_reference_shifts_the_baseline():
    # With min_score=0.5 only the part above 0.5 counts: (10-2) * (0.8-0.5).
    assert analysis.hypervolume([rec(2, 0.8)], n_features=10, min_score=0.5) == \
           pytest.approx(2.4)


def test_points_worse_than_the_reference_score_are_ignored():
    assert analysis.hypervolume([rec(2, 0.3)], n_features=10, min_score=0.5) == 0.0


def test_empty_front_is_zero():
    assert analysis.hypervolume([], n_features=10) == 0.0


def test_score_key_selects_which_column_is_measured():
    front = [{"n_features": 2, "test_score": 0.5, "val_score": 0.9}]

    on_test = analysis.hypervolume(front, n_features=10, score_key="test_score")
    on_val = analysis.hypervolume(front, n_features=10, score_key="val_score")

    assert on_test == pytest.approx(4.0)
    assert on_val == pytest.approx(7.2)


def test_normalised_hypervolume_is_between_zero_and_one():
    perfect = [rec(1, 1.0)]
    typical = [rec(5, 0.8)]

    assert analysis.normalised_hypervolume(perfect, n_features=10) == pytest.approx(1.0)
    assert 0.0 < analysis.normalised_hypervolume(typical, n_features=10) < 1.0
    assert analysis.normalised_hypervolume([], n_features=10) == 0.0


# --------------------------------------------------------------------------
# Per-seed rows
# --------------------------------------------------------------------------

def make_result(method, seed, records, fits=100):
    return {"method": method, "seed": seed, "records": records,
            "model_fits": fits, "search_seconds": 1.0}


def test_hypervolume_by_seed_gives_one_row_per_run():
    results = [
        make_result("fastener", 2020, [rec(2, 0.6), rec(5, 0.9)]),
        make_result("fastener", 2021, [rec(3, 0.7)]),
    ]

    rows = analysis.hypervolume_by_seed(results, n_features=10)

    assert [r["seed"] for r in rows] == [2020, 2021]
    assert rows[0]["hypervolume"] == pytest.approx(6.3)
    assert rows[0]["smallest_subset"] == 2
    assert rows[0]["model_fits"] == 100


def test_hypervolume_by_seed_uses_the_val_selected_front():
    """Selection on validation, measurement on test -- never test on both."""
    records = [
        rec(2, test=0.60, val=0.70),
        # Better on test but worse on validation: the protocol must not pick it,
        # or the reported number is chosen using the held-out set.
        rec(2, test=0.95, val=0.50),
    ]

    rows = analysis.hypervolume_by_seed([make_result("m", 1, records)],
                                        n_features=10)

    assert rows[0]["hypervolume"] == pytest.approx(0.60 * 8)


def test_runs_without_records_are_skipped():
    rows = analysis.hypervolume_by_seed([make_result("m", 1, [])], n_features=10)

    assert rows == []


# --------------------------------------------------------------------------
# Paired comparison
# --------------------------------------------------------------------------

def hv_row(method, seed, value):
    return {"method": method, "seed": seed, "hypervolume": value}


def test_paired_comparison_matches_on_seed():
    rows = [
        hv_row("a", 2020, 6.0), hv_row("a", 2021, 7.0), hv_row("a", 2022, 8.0),
        hv_row("b", 2020, 5.0), hv_row("b", 2021, 6.5), hv_row("b", 2022, 7.0),
    ]

    out = analysis.paired_hypervolume(rows, "a", "b")

    assert out["n_pairs"] == 3
    assert out["seeds"] == [2020, 2021, 2022]
    # `delta` is rounded to 4 decimal places by the implementation.
    assert out["delta"] == pytest.approx((1.0 + 0.5 + 1.0) / 3, abs=1e-4)
    assert out["a_wins"] == 3


def test_unpaired_seeds_are_excluded():
    rows = [
        hv_row("a", 2020, 6.0), hv_row("a", 2021, 7.0), hv_row("a", 2099, 9.0),
        hv_row("b", 2020, 5.0), hv_row("b", 2021, 6.3),
    ]

    out = analysis.paired_hypervolume(rows, "a", "b")

    assert out["n_pairs"] == 2
    assert 2099 not in out["seeds"]


def test_too_few_shared_seeds_reports_instead_of_testing():
    rows = [hv_row("a", 2020, 6.0), hv_row("b", 2020, 5.0)]

    out = analysis.paired_hypervolume(rows, "a", "b")

    assert out["n_pairs"] == 1
    assert "note" in out
    assert "p_value_ttest" not in out


def test_identical_methods_are_not_significant():
    rows = [hv_row("a", s, 6.0) for s in (1, 2, 3)] + \
           [hv_row("b", s, 6.0) for s in (1, 2, 3)]

    out = analysis.paired_hypervolume(rows, "a", "b")

    assert out["delta"] == 0.0
    assert out["p_value_ttest"] == 1.0
    assert out["significant_at_0.05"] is False


def test_a_consistent_gap_is_detected():
    # Differences vary a little from seed to seed, as real ones do; a constant
    # difference makes the paired t-test degenerate (zero variance).
    gaps = [0.9, 1.1, 0.8, 1.2, 1.0, 0.95, 1.05, 1.15]
    rows = [hv_row("a", s, 5.0 + gaps[s - 1]) for s in range(1, 9)] + \
           [hv_row("b", s, 5.0) for s in range(1, 9)]

    out = analysis.paired_hypervolume(rows, "a", "b")

    assert out["a_wins"] == 8
    assert out["p_value_ttest"] < 0.05
    assert out["significant_at_0.05"] is True


def test_wilcoxon_is_reported_alongside_the_t_test():
    rows = [hv_row("a", s, 6.0 + s * 0.1) for s in range(1, 9)] + \
           [hv_row("b", s, 5.5) for s in range(1, 9)]

    out = analysis.paired_hypervolume(rows, "a", "b")

    assert out["p_value_wilcoxon"] is not None
    assert not math.isnan(out["p_value_wilcoxon"])
