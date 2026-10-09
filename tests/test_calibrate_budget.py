"""Tests for the H2/H3 budget rule (HYPOTHESES.md, H2, Fit budget)."""
import json

import pytest

import calibrate_budget as cb


def test_value_at_reads_the_last_snapshot_at_or_before():
    curve = [(0, 0.1), (900, 0.3), (2500, 0.5), (12000, 0.6)]
    assert cb.value_at(curve, 1000) == 0.3
    assert cb.value_at(curve, 2000) == 0.3
    assert cb.value_at(curve, 2500) == 0.5
    assert cb.value_at([(10, 0.4)], 5) == 0.0


def test_settled_early_gets_one_step_of_margin():
    curve = [(500, 0.70), (1000, 0.80), (12000, 0.803)]
    c = cb.choose_budget(curve, reference=0.75)
    assert c["settled_at"] == 1000
    assert c["budget"] == 2000
    assert c["flag"] == ""


def test_still_rising_waits_until_within_tolerance():
    curve = [(1000, 0.60), (2000, 0.70), (4000, 0.78), (6000, 0.797),
             (12000, 0.80)]
    c = cb.choose_budget(curve, reference=0.5)
    assert c["settled_at"] == 6000
    assert c["budget"] == 12000


def test_below_boruta_is_not_settled_even_when_flat():
    # Flat from 1,000 on, but below Boruta's reference throughout.
    curve = [(1000, 0.60), (12000, 0.60)]
    c = cb.choose_budget(curve, reference=0.70)
    assert c["settled_at"] is None
    assert c["budget"] == 12000
    assert c["flag"] == "possibly unconverged"


def test_within_tolerance_of_boruta_counts():
    curve = [(1000, 0.696), (12000, 0.696)]
    assert cb.choose_budget(curve, reference=0.70)["budget"] == 2000


def test_records_val_auf_uses_validation_and_zero_below_the_smallest():
    recs = [{"n_features": 3, "val_score": 0.6, "test_score": 0.0},
            {"n_features": 8, "val_score": 0.8, "test_score": 0.0}]
    # opt(k): 0 for k = 1, 2; 0.6 for 3..7; 0.8 for 8..10.
    assert cb.records_val_auf(recs) == pytest.approx((5 * 0.6 + 3 * 0.8) / 10)


def _run(root, name, dataset, fastener_curve=None, boruta=None):
    d = root / name
    (d / "trajectories").mkdir(parents=True)
    (d / "manifest.json").write_text(json.dumps({"params": {"dataset": dataset}}))
    results = []
    if fastener_curve is not None:
        with open(d / "trajectories" / "fastener_seed1999.jsonl", "w") as fh:
            for i, (fits, size, f1) in enumerate(fastener_curve):
                fh.write(json.dumps({
                    "iteration": i, "fits": fits, "front_changed": True,
                    "front": [{"size": size, "val_f1": f1,
                               "features": list(range(size))}]}) + "\n")
        results.append({"method": "fastener", "seed": 1999,
                        "stopped_on": "fit_budget", "records": []})
    if boruta is not None:
        results.append({"method": "boruta", "seed": 1999, "records": [
            {"n_features": 1, "val_score": boruta, "test_score": 0.0}]})
    (d / "raw_results.json").write_text(json.dumps(results))
    return d


def test_calibrate_combines_the_two_runs_of_a_dataset(tmp_path):
    f = _run(tmp_path, "f", "Coffee",
             fastener_curve=[(500, 1, 0.70), (1500, 1, 0.80), (12000, 1, 0.80)])
    b = _run(tmp_path, "b", "Coffee", boruta=0.75)
    rows = cb.calibrate([f, b])
    assert len(rows) == 1
    r = rows[0]
    assert r["boruta_val_auf"] == pytest.approx(0.75)
    assert r["settled_at"] == 2000 and r["budget"] == 4000


def test_a_dataset_without_boruta_gets_no_budget(tmp_path):
    f = _run(tmp_path, "f", "Coffee",
             fastener_curve=[(500, 1, 0.70), (12000, 1, 0.80)])
    rows = cb.calibrate([f])
    assert rows[0]["budget"] is None
    assert "missing Boruta run" in rows[0]["flag"]
