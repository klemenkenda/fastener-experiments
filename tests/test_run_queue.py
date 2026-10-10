"""Tests for run_queue.py's job list, and --budgets in particular."""
import json

import pytest

import run_queue


def _budgets(tmp_path, budgets):
    path = tmp_path / "budgets.json"
    path.write_text(json.dumps({"budgets": budgets}))
    return str(path)


def _evaluations(cmd):
    return [cmd[i + 1] for i, a in enumerate(cmd) if a == "--evaluations"]


def test_each_job_gets_its_own_datasets_budget(tmp_path):
    args = run_queue.parse_args([
        "--experiment", "H9-E01", "--datasets", "Coffee,eodata",
        "--methods", "fastener:none,fastener:guided", "--seeds", "2020,2021",
        "--budgets", _budgets(tmp_path, {"Coffee": 12000, "eodata": 2000,
                                         "Wafer": 2000})])
    jobs = run_queue.build_jobs(args)
    assert len(jobs) == 8
    for j in jobs:
        want = {"Coffee": 12000, "eodata": 2000}[j["dataset"]]
        assert j["budget"] == want
        assert _evaluations(j["cmd"]) == [str(want)]


def test_a_dataset_without_a_budget_is_refused(tmp_path):
    with pytest.raises(SystemExit, match="no budget for Ham"):
        run_queue.parse_args([
            "--datasets", "Coffee,Ham", "--methods", "boruta",
            "--budgets", _budgets(tmp_path, {"Coffee": 2000, "Ham": None})])


def test_budgets_and_evaluations_together_are_refused(tmp_path):
    with pytest.raises(SystemExit):
        run_queue.parse_args([
            "--datasets", "Coffee", "--methods", "boruta",
            "--budgets", _budgets(tmp_path, {"Coffee": 2000}),
            "--", "--evaluations", "6000"])


def test_without_budgets_the_passthrough_is_unchanged():
    args = run_queue.parse_args([
        "--datasets", "Coffee", "--methods", "fastener:none", "--seeds", "1999",
        "--", "--evaluations", "12000"])
    (job,) = run_queue.build_jobs(args)
    assert job["budget"] is None
    assert _evaluations(job["cmd"]) == ["12000"]


def test_cpu_second_budgets_become_cpu_seconds_flags(tmp_path):
    path = tmp_path / "budgets.json"
    path.write_text(json.dumps({"unit": "cpu_seconds",
                                "budgets": {"colon": 120, "USPS": 900.5}}))
    args = run_queue.parse_args([
        "--datasets", "colon,USPS", "--methods", "fs_sds,fastener:none",
        "--seeds", "2020", "--budgets", str(path)])
    jobs = run_queue.build_jobs(args)
    for j in jobs:
        i = j["cmd"].index("--cpu-seconds")
        assert j["cmd"][i + 1] == str({"colon": 120, "USPS": 900.5}[j["dataset"]])
        assert "--evaluations" not in j["cmd"]
        assert j["budget_unit"] == "cpu_seconds"


def test_an_unknown_budget_unit_is_refused(tmp_path):
    path = tmp_path / "budgets.json"
    path.write_text(json.dumps({"unit": "hours", "budgets": {"colon": 1}}))
    with pytest.raises(SystemExit, match="unknown budget unit"):
        run_queue.parse_args(["--datasets", "colon", "--methods", "fs_sds",
                              "--budgets", str(path)])


def test_a_job_is_not_matched_to_an_older_runs_folder(tmp_path):
    """A folder left under the same job name by an earlier queue is not this
    job's, even while this job's own folder does not exist yet."""
    name = "h9calibration_colon_fastener_none_s1999"
    (tmp_path / f"20261010T121124Z_{name}").mkdir()
    job = {"name": name, "started_utc": "2026-10-10T12:26:03.5+00:00"}
    assert run_queue.job_run_dir(job, tmp_path) is None
    (tmp_path / f"20261010T122603Z_{name}").mkdir()
    assert run_queue.job_run_dir(job, tmp_path).endswith(
        f"20261010T122603Z_{name}")
    assert run_queue.job_run_dir({"name": name, "started_utc": None},
                                 tmp_path) is None
