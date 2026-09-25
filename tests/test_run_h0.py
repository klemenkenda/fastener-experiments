"""Tests for the H0 driver's overall ETA and its restart logic."""
import json

import pytest

import run_h0


def test_makespan_runs_queued_work_on_the_first_free_slot():
    # One slot: everything in series.
    assert run_h0.makespan([100.0], [50.0, 30.0], jobs=1) == pytest.approx(180)
    # Two slots: the 50 goes after the 20, the 30 after the 70 -> max(100, 70).
    assert run_h0.makespan([100.0, 20.0], [50.0, 30.0], jobs=2) == pytest.approx(100)
    # Idle slots take queued work straight away.
    assert run_h0.makespan([], [40.0, 30.0, 20.0], jobs=3) == pytest.approx(40)


def test_makespan_of_nothing_is_zero():
    assert run_h0.makespan([], [], jobs=2) == 0.0


def test_plan_matches_the_hypothesis():
    plan = {p["dataset"]: p for p in run_h0.H0_PLAN}
    assert set(plan) == {"crop_mapping", "USPS", "har", "BASEHOCK", "TOX_171"}
    assert plan["crop_mapping"]["split"] == "eo"
    assert plan["crop_mapping"]["evaluations"] == 1000
    for name in ("USPS", "har", "BASEHOCK", "TOX_171"):
        assert plan[name]["split"] == "protocol"
        assert plan[name]["evaluations"] == 6000


def write_manifest(root, name, experiment, dataset, status="ok",
                   arms=("none", "2020")):
    d = root / name
    d.mkdir()
    (d / "manifest.json").write_text(json.dumps({
        "experiment_id": experiment, "status": status,
        "params": {"dataset": dataset, "fastener_arms": list(arms)}}),
        encoding="utf-8")
    return d


def test_finished_runs_only_counts_complete_runs_of_this_experiment(
        tmp_path, monkeypatch):
    monkeypatch.setattr(run_h0, "RESULTS_DIR", tmp_path)
    ok = write_manifest(tmp_path, "a_h0_USPS", "H0-E01", "USPS")
    write_manifest(tmp_path, "b_h0_har", "H0-E01", "har", status="failed")
    write_manifest(tmp_path, "c_h0_TOX", "H0-E02", "TOX_171")
    write_manifest(tmp_path, "d_h0_BASEHOCK", "H0-E01", "BASEHOCK",
                   arms=("none",))
    assert run_h0.finished_runs("H0-E01") == {"USPS": ok}


def test_job_command_carries_the_budget_split_and_both_arms(tmp_path):
    plan = next(p for p in run_h0.H0_PLAN if p["dataset"] == "crop_mapping")
    cmd = run_h0.Job(plan, tmp_path, "H0-E01", smoke=False,
                     allow_dirty=False).cmd
    joined = " ".join(cmd)
    assert "--dataset crop_mapping" in joined
    assert "--split eo" in joined
    assert "--evaluations 1000" in joined
    assert "--experiment H0-E01" in joined
    assert cmd.count("--fastener-arm") == 2
    assert "none" in cmd and "2020" in cmd
    assert "--quick" not in cmd


def test_smoke_job_is_quick_and_has_no_experiment(tmp_path):
    cmd = run_h0.Job(run_h0.H0_PLAN[0], tmp_path, None, smoke=True,
                     allow_dirty=False).cmd
    assert "--quick" in cmd
    assert "--experiment" not in cmd
