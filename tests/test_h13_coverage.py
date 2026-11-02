"""h13_coverage.py: the measures H13-E01 registers (no data)."""
import numpy as np
import pytest

import h13_coverage as cov
from make_report import auf
from nsgaii_miip import obl_initialization


def rec(n, val, test):
    return {"n_features": n, "val_score": val, "test_score": test}


FRONT = [rec(3, 0.70, 0.68), rec(6, 0.80, 0.77), rec(25, 0.90, 0.88)]


def test_reach_starts_at_the_smallest_subset_on_the_front():
    assert cov.reach_curve(FRONT).tolist() == [False, False] + [True] * 8
    assert not cov.reach_curve([]).any()
    assert not cov.reach_curve([rec(40, 0.9, 0.9)]).any()


def test_exact_curve_only_where_the_front_has_that_size():
    e = cov.exact_curve(FRONT)
    assert e[2] == 0.68 and e[5] == 0.77
    assert np.isnan(e[[0, 1, 3, 4, 6, 7, 8, 9]]).all()


def test_run_measures_auf_and_large_end():
    m = cov.run_measures(FRONT, n_features=30)
    assert m["auf_k10"] == pytest.approx(auf(FRONT, 10))
    assert m["best_f1"] == 0.88 and m["min_front"] == 3 and m["max_front"] == 25
    # AUF at K = d covers the whole front: the 25-feature subset counts.
    assert m["auf_kd"] > m["auf_k10"] * 10 / 30


def _agg(fronts):
    return cov.aggregate([cov.run_measures(f, 50) for f in fronts])


def test_seed_mean_auf_equals_reach_times_conditional_quality():
    fronts = [FRONT, [rec(12, 0.9, 0.9)], [rec(1, 0.5, 0.55), rec(8, 0.7, 0.71)]]
    a = _agg(fronts)
    assert a["R"] == pytest.approx(2 / 3)
    assert np.nanmean(np.nan_to_num(a["r"] * a["c_bar"])) == pytest.approx(a["auf_k10"])


def test_decomposition_is_exact():
    rng = np.random.default_rng(0)
    ra, rb = rng.uniform(0.1, 1, 10), rng.uniform(0.1, 1, 10)
    ca, cb = rng.uniform(0.5, 1, 10), rng.uniform(0.5, 1, 10)
    reach, quality = cov.decompose(ra, ca, rb, cb)
    assert reach + quality == pytest.approx(np.mean(ra * ca - rb * cb))


def test_an_arm_that_never_reaches_k_is_all_reach():
    ra, ca = np.ones(10), np.full(10, 0.8)
    rb, cb = np.zeros(10), np.full(10, np.nan)
    reach, quality = cov.decompose(ra, ca, rb, cb)
    assert reach == pytest.approx(0.8) and quality == 0.0
    assert cov.decompose(rb, cb, rb, cb) == (0.0, 0.0)


def test_equal_reach_is_all_quality():
    r = np.full(10, 0.6)
    reach, quality = cov.decompose(r, np.full(10, 0.8), r, np.full(10, 0.7))
    assert reach == 0.0 and quality == pytest.approx(0.06)


def test_matched_difference_needs_three_of_five_seeds_in_both_arms():
    ra = np.array([0.2, 0.6, 1.0] + [1.0] * 7)
    rb = np.array([0.0, 0.4, 0.6] + [0.8] * 7)
    ca, cb = np.full(10, 0.8), np.full(10, 0.7)
    assert cov.matched_difference(ra, ca, rb, cb) == pytest.approx(0.1)
    assert cov.matched_difference(np.zeros(10), ca, rb, cb) is None


def test_reach_share():
    assert cov.reach_share([(0.3, 0.1), (-0.3, 0.1)]) == pytest.approx(0.75)
    assert np.isnan(cov.reach_share([(0.0, 0.0)]))


def test_obl_start_reach_matches_the_initialiser():
    assert cov.obl_start_reach(12) == 1.0       # every pair has a small side
    assert cov.obl_start_reach(500) < 1e-60
    d, n, hits = 30, 2000, 0
    rng = np.random.RandomState(1)
    for _ in range(n):
        sizes = obl_initialization(100, d, rng).sum(axis=1)
        hits += bool(((sizes >= 1) & (sizes <= 10)).any())
    assert hits / n == pytest.approx(cov.obl_start_reach(d), abs=0.03)


def test_time_to_reach_from_the_archive_and_censoring():
    curve = [{"fits": 100, "seconds": 1.0, "min_size": 40},
             {"fits": 900, "seconds": 9.0, "min_size": 9},
             {"fits": 2000, "seconds": 20.0, "min_size": 2}]
    t = cov.time_to_reach(curve, budget=2000)
    assert t["reached"] and t["fits"] == 900 and t["share"] == pytest.approx(0.45)
    assert not t["at_start"]
    never = cov.time_to_reach(curve[:1], budget=2000)
    assert not never["reached"] and never["share"] == pytest.approx(0.05)


def test_kaplan_meier_and_rmst():
    t, e = [0.1, 0.2, 0.5, 0.5], [True, True, False, False]
    ts, s = cov.km(t, e)
    assert ts.tolist() == [0.1, 0.2] and s.tolist() == pytest.approx([0.75, 0.5])
    assert cov.km_reached_by(t, e, 0.15) == pytest.approx(0.25)
    # Area under S: 0.1 x 1 + 0.1 x 0.75 + 0.8 x 0.5.
    assert cov.rmst(t, e) == pytest.approx(0.575)
    assert cov.rmst([0.3], [False]) == pytest.approx(1.0)


def test_rank_biserial():
    assert cov.rank_biserial([1, 2, 3]) == 1.0
    assert cov.rank_biserial([-1, -2]) == -1.0
    assert cov.rank_biserial([0, 0]) == 0.0
    assert cov.rank_biserial([1, -2]) == pytest.approx(-1 / 3)


def test_bootstrap_interval_is_reproducible_and_brackets_the_mean():
    x = np.linspace(-0.01, 0.03, 20)
    lo, hi = cov.bootstrap_ci(x)
    assert lo < x.mean() < hi
    assert (lo, hi) == cov.bootstrap_ci(x)


def test_expected_flips():
    assert cov.expected_flips(10, 10_000) == pytest.approx(0.002)


def test_min_test_rows_drops_small_test_sets_from_b_only():
    """DEC-57 (post hoc): with min_test_rows, a dataset with at most that many
    test rows leaves (b); (a) and (c) still read it. Off, nothing changes."""
    import h13_report as h

    def agg(test_f1):
        fronts = [[rec(2, 0.8, test_f1), rec(9, 0.9, test_f1)]] * 5
        a = cov.aggregate([cov.run_measures(f, 40) for f in fronts])
        a["d"] = 40
        return a

    # Both arms reach every k >= 2 on both datasets; on "tiny" (8 test rows)
    # the 1-30 start is 0.2 F1 behind, on "big" (300) level.
    sub = {"nsga2_sparse": {"tiny": agg(0.6), "big": agg(0.8)},
           "nsga2": {"tiny": agg(0.8), "big": agg(0.8)}}
    by_grid = {g: sub for g in h.GRIDS}
    n_test = {(g, d): n for g in h.GRIDS for d, n in (("tiny", 8), ("big", 300))}
    off, _ = h.criterion(by_grid)
    on, _ = h.criterion(by_grid, n_test=n_test, min_test_rows=50)
    assert off[0]["b"]["n_matched"] == 2 and off[0]["b"]["mean"] == pytest.approx(-0.1)
    assert on[0]["b"]["n_matched"] == 1 and on[0]["b"]["mean"] == pytest.approx(0.0)
    assert on[0]["b_left_out"] == "tiny"
    for x, y in zip(off, on):
        assert (x["n_datasets"], x["reach_share"], x["p"]) == \
               (y["n_datasets"], y["reach_share"], y["p"])
    assert h.b_terms({"a": {}, "b": {}}, {"a": 50, "b": 51}, 50) == {"b": {}}
    assert h.b_terms({"a": {}}, {}, None) == {"a": {}}
