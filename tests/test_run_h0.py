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


def test_extension_plan_is_every_other_dataset():
    from datasets import H8_DATASETS, LOADERS, TSC_DATASETS
    ext = {p["dataset"] for p in run_h0.H0_EXTENSION_PLAN}
    core = {p["dataset"] for p in run_h0.H0_PLAN}
    assert not ext & core
    # Every dataset on disk when H0 ran; the TSC and H8 sets came later.
    assert ext | core == set(LOADERS) - set(TSC_DATASETS) - set(H8_DATASETS)
    budgets = {p["dataset"]: (p["evaluations"], p["split"])
               for p in run_h0.H0_EXTENSION_PLAN}
    assert budgets["eodata"] == (1000, "eo")
    assert budgets["satimage"] == (1000, "protocol")
    assert all(b == (6000, "protocol") for d, b in budgets.items()
               if d not in ("eodata", "satimage"))


def test_repeat_plan_is_all_36_with_the_protocol_budgets():
    import protocol
    plan = {p["dataset"]: p for p in run_h0.H0_REPEAT_PLAN}
    earlier = run_h0.H0_PLAN + run_h0.H0_EXTENSION_PLAN
    assert set(plan) == {p["dataset"] for p in earlier}
    assert len(plan) == 36
    for p in earlier:
        r = plan[p["dataset"]]
        assert r["split"] == p["split"]
        assert r["group"]
        if p["evaluations"] == 1000:
            assert r["evaluations"] == 1000
        else:
            assert r["evaluations"] == protocol.fit_budget(p["dataset"])
    assert plan["nci9"]["evaluations"] == 12_000
    assert plan["madelon"]["evaluations"] == 6000
    assert run_h0.PLANS["repeat"] is run_h0.H0_REPEAT_PLAN


def test_status_write_survives_a_reader_holding_the_file(tmp_path, monkeypatch):
    real = run_h0.os.replace
    calls = {"n": 0}

    def flaky(src, dst):
        calls["n"] += 1
        if calls["n"] < 3:
            raise PermissionError("in use")
        real(src, dst)

    monkeypatch.setattr(run_h0.os, "replace", flaky)
    monkeypatch.setattr(run_h0.time, "sleep", lambda s: None)
    d = run_h0.Driver([], tmp_path, 1, 60, "x")
    d.write_status({"a": 1})
    assert json.loads((tmp_path / "driver.json").read_text()) == {"a": 1}

    monkeypatch.setattr(run_h0.os, "replace",
                        lambda s, t: (_ for _ in ()).throw(PermissionError()))
    d.write_status({"a": 2})  # gives up quietly, never raises


def test_adopted_run_is_watched_to_its_end(tmp_path):
    import subprocess
    import sys
    plan = {"dataset": "TOX_171", "split": "protocol", "evaluations": 6000,
            "hours": 0.5}
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        j = run_h0.Job(plan, tmp_path, "H0-E99", False, False)
        j.adopt(run_dir, proc.pid, elapsed=100.0)
        j.poll()
        assert j.state == "running" and j.elapsed() >= 100.0
    finally:
        proc.kill()
        proc.wait()
    (run_dir / "manifest.json").write_text(json.dumps({"status": "ok"}))
    j.poll()
    assert j.state == "done"

    k = run_h0.Job(plan, tmp_path, "H0-E99", False, False)
    k.adopt(tmp_path / "gone", proc.pid, elapsed=0.0)
    k.poll()
    assert k.state == "failed"  # died without a manifest
