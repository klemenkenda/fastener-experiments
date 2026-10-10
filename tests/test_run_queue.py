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
