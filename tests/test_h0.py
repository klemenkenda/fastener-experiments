"""Tests for H0: the fits-to-target measure, its verdicts, the 2020 arm and
the EO split.

The measure is checked on curves worked out by hand, because an off-by-one in
where the target is met would still produce plausible fit counts and could hand
a seed to the wrong arm.
"""
import numpy as np
import pytest

import h0_convergence as h0
from datasets import DATA_DIR, EO_SPLIT_ROWS, load
from item import (IntersectionMatingWithWeightedRandomInformationGain,
                  RandomEveryoneWithEveryone)
from run_fastener import MATING_VERSIONS, make_mating


def front(*pairs):
    return [{"size": s, "val_f1": v, "features": list(range(s))}
            for s, v in pairs]


# ------------------------------------------------------------------ val_auf
def test_val_auf_takes_the_best_score_up_to_each_k():
    # opt(k): k=1 -> 0.5, k=2 -> 0.5, k=3..10 -> 0.8
    f = front((1, 0.5), (3, 0.8))
    assert h0.val_auf(f, K=10) == pytest.approx((0.5 + 0.5 + 0.8 * 8) / 10)


def test_val_auf_is_zero_below_the_smallest_subset():
    f = front((3, 0.9))
    assert h0.val_auf(f, K=4) == pytest.approx((0 + 0 + 0.9 + 0.9) / 4)


def test_val_auf_ignores_subsets_above_K():
    assert h0.val_auf(front((1, 0.5), (12, 0.99)), K=10) == pytest.approx(0.5)


def test_val_auf_of_an_empty_front_is_zero():
    assert h0.val_auf([], K=10) == 0.0


# ----------------------------------------------------------- fits and areas
def test_fits_to_target_is_the_first_snapshot_at_or_above_it():
    c = [(10, 0.3), (50, 0.6), (90, 0.6), (140, 0.7)]
    assert h0.fits_to_target(c, 0.6) == 50
    assert h0.fits_to_target(c, 0.65) == 140
    assert h0.fits_to_target(c, 0.8) is None


def test_area_under_curve_is_the_mean_of_the_step_curve():
    # 0 on [0, 10), 0.5 on [10, 60), 1.0 on [60, 100]
    c = [(10, 0.5), (60, 1.0)]
    assert h0.area_under_curve(c, 100) == pytest.approx(
        (0 * 10 + 0.5 * 50 + 1.0 * 40) / 100)


def test_area_under_curve_stops_at_the_budget():
    assert h0.area_under_curve([(0, 1.0), (150, 0.0)], 100) == pytest.approx(1.0)


# --------------------------------------------------------------- comparison
def test_target_is_the_lower_final_value_and_the_faster_arm_wins():
    fixed = [(10, 0.4), (100, 0.7), (200, 0.75)]
    original = [(10, 0.4), (150, 0.7), (200, 0.7)]
    r = h0.compare_seed(fixed, original)
    assert r["target"] == pytest.approx(0.7)
    assert r["fits_to_target_fixed"] == 100
    assert r["fits_to_target_2020"] == 150
    assert r["faster"] == h0.FIXED


def test_equal_fit_counts_are_a_tie():
    c = [(10, 0.4), (100, 0.7)]
    assert h0.compare_seed(c, list(c))["faster"] == "tie"


def test_the_2020_arm_can_win():
    fixed = [(300, 0.7)]
    original = [(100, 0.7)]
    assert h0.compare_seed(fixed, original)["faster"] == h0.ORIGINAL


# ----------------------------------------------------------------- verdicts
def seeds(*outcomes):
    return [{"faster": o} for o in outcomes]


F, O, T = h0.FIXED, h0.ORIGINAL, "tie"


def test_four_of_five_counts_and_a_tie_does_not():
    assert h0.dataset_verdict(seeds(F, F, F, F, O))["counts_for"] == F
    assert h0.dataset_verdict(seeds(F, F, F, T, T))["counts_for"] == "neither"
    assert h0.dataset_verdict(seeds(O, O, O, O, F))["counts_for"] == O


def test_fewer_than_five_seeds_is_incomplete():
    assert h0.dataset_verdict(seeds(F, F, F, F))["counts_for"] == "incomplete"


def verdicts(**counts_for):
    return {d: {"counts_for": c} for d, c in counts_for.items()}


def test_h0_needs_crop_mapping_and_one_other():
    assert h0.h0_verdict(verdicts(crop_mapping=F, USPS=F)) == "supported"
    assert h0.h0_verdict(verdicts(crop_mapping=F, USPS="neither",
                                  har="neither")) == "not supported"
    assert h0.h0_verdict(verdicts(crop_mapping="neither", USPS=F,
                                  har=F)) == "not supported"


def test_the_reverse_outcome_is_reported():
    assert h0.h0_verdict(verdicts(crop_mapping=O, har=O)).startswith("reversed")


def test_h0_without_crop_mapping_is_incomplete():
    assert h0.h0_verdict(verdicts(USPS=F, har=F)).startswith("incomplete")


# ------------------------------------------------------------- the 2020 arm
def test_2020_mating_sets_both_original_flags():
    m = make_mating("2020", pool_size=3)
    assert isinstance(m, RandomEveryoneWithEveryone)
    assert m.allow_self_mating is True
    assert isinstance(m.mating_strategy,
                      IntersectionMatingWithWeightedRandomInformationGain)
    assert m.mating_strategy.include_top_genes is True


def test_fixed_mating_is_the_clone_default():
    m = make_mating("fixed", pool_size=3)
    default = IntersectionMatingWithWeightedRandomInformationGain()
    assert m.allow_self_mating is RandomEveryoneWithEveryone().allow_self_mating
    assert m.mating_strategy.include_top_genes is default.include_top_genes
    assert MATING_VERSIONS["fixed"] == {"include_top_genes": False,
                                        "allow_self_mating": False}


def test_unknown_mating_version_is_refused():
    with pytest.raises(ValueError):
        make_mating("2019", pool_size=3)


# ----------------------------------------------------------------- EO split
CROP = DATA_DIR / "crop_mapping" / "crop_mapping.npz"


@pytest.mark.skipif(not CROP.is_file(), reason="crop_mapping not downloaded")
def test_eo_split_is_40_10_50_of_a_stratified_subsample():
    ds = load("crop_mapping", split="eo")
    n_tr, n_va, n_te = (ds.X_train.shape[0], ds.X_val.shape[0],
                        ds.X_test.shape[0])
    assert n_tr + n_va + n_te == pytest.approx(EO_SPLIT_ROWS, abs=10)
    assert n_tr == pytest.approx(0.4 * EO_SPLIT_ROWS, abs=10)
    assert n_va == pytest.approx(0.1 * EO_SPLIT_ROWS, abs=10)
    assert n_te == pytest.approx(0.5 * EO_SPLIT_ROWS, abs=10)
    assert ds.summary()["split"] == "eo"
    # Stratified: every class keeps its share in every part.
    share = lambda y: np.bincount(y) / y.size  # noqa: E731
    assert np.allclose(share(ds.y_train), share(ds.y_test), atol=0.002)
    assert np.allclose(share(ds.y_val), share(ds.y_test), atol=0.002)


@pytest.mark.skipif(not CROP.is_file(), reason="crop_mapping not downloaded")
def test_eo_split_parts_do_not_overlap_and_are_fixed():
    a, b = load("crop_mapping", split="eo"), load("crop_mapping", split="eo")
    assert np.array_equal(a.X_test, b.X_test)
    rows = lambda X: {r.tobytes() for r in X}  # noqa: E731
    # Duplicated rows in the source could collide, so allow a handful.
    assert len(rows(a.X_train) & rows(a.X_test)) < 50


def test_eo_split_is_refused_for_a_set_without_a_row_cap():
    with pytest.raises(ValueError):
        load("USPS", split="eo")


# ------------------------------------------------- H0-E02: every other dataset
def test_seed_effect_is_positive_when_the_fixed_arm_is_faster():
    assert h0.seed_effect({"fits_to_target_fixed": 100,
                           "fits_to_target_2020": 400}) == pytest.approx(2.0)
    assert h0.seed_effect({"fits_to_target_fixed": 400,
                           "fits_to_target_2020": 100}) == pytest.approx(-2.0)
    assert h0.seed_effect({"fits_to_target_fixed": 50,
                           "fits_to_target_2020": 50}) == 0.0


def fake_runs(monkeypatch, fits_by_dataset):
    """Stand in for read_run: {dataset: [(fixed, 2020) per seed]}."""
    def read_run(path, K=h0.K):
        ds = str(path)
        rows = []
        for i, (f, o) in enumerate(fits_by_dataset[ds]):
            rows.append({"dataset": ds, "seed": 2020 + i,
                         "fits_to_target_fixed": f, "fits_to_target_2020": o,
                         "faster": (h0.FIXED if f < o else
                                    h0.ORIGINAL if o < f else "tie"),
                         "test_auf10_fixed": 0.5, "test_auf10_2020": 0.5})
        return ds, rows
    monkeypatch.setattr(h0, "read_run", read_run)
    return list(fits_by_dataset)


def test_extension_is_supported_when_datasets_lean_to_the_fixed_code(monkeypatch):
    data = {f"d{i}": [(100, 400)] * 5 for i in range(12)}
    runs = fake_runs(monkeypatch, data)
    s = h0.extension_summary(runs, expected=runs)
    assert s["primary"]["positive"] == 12
    assert s["primary"]["p_value"] < 0.05
    assert s["verdict"] == "supported"


def test_extension_is_reversed_when_datasets_lean_to_the_2020_code(monkeypatch):
    data = {f"d{i}": [(400, 100)] * 5 for i in range(12)}
    runs = fake_runs(monkeypatch, data)
    assert h0.extension_summary(runs, expected=runs)["verdict"].startswith(
        "reversed")


def test_extension_split_is_not_supported(monkeypatch):
    data = {f"d{i}": [(100, 400)] * 5 if i % 2 else [(400, 100)] * 5
            for i in range(12)}
    runs = fake_runs(monkeypatch, data)
    assert h0.extension_summary(runs, expected=runs)["verdict"].startswith(
        "not supported")


def test_extension_with_too_many_missing_datasets_is_incomplete(monkeypatch):
    data = {f"d{i}": [(100, 400)] * 5 for i in range(12)}
    runs = fake_runs(monkeypatch, data)
    expected = runs + [f"gone{i}" for i in range(h0.EXTENSION_MAX_MISSING + 1)]
    s = h0.extension_summary(runs, expected=expected)
    assert s["verdict"].startswith("incomplete")
    assert len(s["missing"]) == h0.EXTENSION_MAX_MISSING + 1


def test_extension_leaves_out_datasets_with_too_few_seeds(monkeypatch):
    data = {f"d{i}": [(100, 400)] * 5 for i in range(12)}
    data["short"] = [(400, 100)] * 3
    runs = fake_runs(monkeypatch, data)
    s = h0.extension_summary(runs, expected=runs)
    assert "short" in s["missing"]
    assert s["primary"]["n_datasets"] == 12
