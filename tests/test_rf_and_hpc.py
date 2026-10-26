"""H5H6-E02's code: the protocol random forest, the NSGA-II stagnation stop
and the SLURM array driver (hpc_jobs.py)."""
import json
import sys
from types import SimpleNamespace

import numpy as np
import pytest

import hpc_jobs
import nsgaii_miip
import protocol
import run_queue
import sota_baselines


@pytest.fixture
def forest():
    protocol.set_model("rf", n_jobs=2)
    yield
    protocol.set_model("tree")


def test_the_tree_is_the_default():
    assert protocol.model_name() == "tree"
    assert type(protocol.make_model()).__name__ == "DecisionTreeClassifier"
    assert protocol.model_description() == "DecisionTreeClassifier"


def test_the_forest_reaches_every_caller_of_make_model(forest):
    m = protocol.make_model()
    assert type(m).__name__ == "RandomForestClassifier"
    assert m.n_estimators == protocol.RF_TREES == 100
    assert m.random_state == protocol.MODEL_SEED and m.n_jobs == 2
    assert protocol.model_description() == "RandomForestClassifier(100 trees)"
    # Boruta's estimator and the tree-importance ranker build theirs through
    # make_model, so they follow the switch.
    rng = np.random.RandomState(0)
    X, y = rng.normal(size=(60, 5)), rng.randint(0, 2, 60)
    est = sota_baselines.TreeForBoruta(random_state=3).fit(X, y)
    assert type(est.tree_).__name__ == "RandomForestClassifier"


def test_the_forest_does_not_depend_on_its_thread_count():
    rng = np.random.RandomState(0)
    X, y = rng.normal(size=(80, 6)), rng.randint(0, 3, 80)
    preds = []
    for jobs in (1, 3):
        protocol.set_model("rf", n_jobs=jobs)
        preds.append(protocol.make_model().fit(X, y).predict(X))
    protocol.set_model("tree")
    assert np.array_equal(*preds)


def test_an_unknown_model_is_refused():
    with pytest.raises(ValueError):
        protocol.set_model("svm")


def test_barren_counter_counts_consecutive_generations_without_a_fit():
    step = nsgaii_miip.barren_counter(3)
    assert [step(e) for e in (100, 150, 150, 150, 160, 160, 160, 160)] == \
        [False, False, False, False, False, False, False, True]
    off = nsgaii_miip.barren_counter(None)
    assert not any(off(5) for _ in range(100))


def _small_ds(n_features=3):
    """Three features: seven non-empty subsets, so the search must stall."""
    rng = np.random.RandomState(1)
    X = rng.normal(size=(90, n_features))
    y = (X[:, 0] > 0).astype(int)
    return SimpleNamespace(n_features=n_features, X_train=X[:50], y_train=y[:50],
                           X_val=X[50:70], y_val=y[50:70],
                           X_test=X[70:], y_test=y[70:])


@pytest.mark.parametrize("init", ["obl", "sparse"])
def test_nsga2_stops_on_stagnation_instead_of_spinning(init):
    res = sota_baselines.run_nsga2(_small_ds(), seed=0, stop_evaluations=10_000,
                                   init=init, pop_size=10,
                                   max_barren_generations=5)
    assert res["stopped_on"] == "stagnation"
    assert res["model_fits"] <= 7
    assert res["records"]


def test_nsga2_without_the_stop_still_ends_on_its_budget():
    res = sota_baselines.run_nsga2(_small_ds(6), seed=0, stop_evaluations=30,
                                   pop_size=10)
    assert res["stopped_on"] == "budget" and res["model_fits"] == 30


def test_nsgaii_miip_stops_on_stagnation():
    res = sota_baselines.run_nsgaii_miip_method(
        _small_ds(), seed=0, stop_evaluations=10_000, pop_size=10,
        max_barren_generations=5)
    assert res["stopped_on"] == "stagnation" and res["model_fits"] <= 7


# ------------------------------------------------------------ hpc_jobs.py
def _emit(tmp_path, monkeypatch, timeout_hours=None):
    monkeypatch.setattr(hpc_jobs, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(run_queue, "RESULTS_DIR", tmp_path)
    argv = ["--name", "t", "--datasets", "Coffee", "--methods", "boruta",
            "--seeds", "2020,2021,2022"]
    if timeout_hours:
        argv += ["--timeout-hours", str(timeout_hours)]
    hpc_jobs.emit(argv + ["--", "--model", "rf"])
    path = tmp_path / "t" / "jobs.json"
    return path, json.loads(path.read_text())


def _set_cmds(path, spec, cmds):
    for j, c in zip(spec["jobs"], cmds):
        j["cmd"] = c
    path.write_text(json.dumps(spec))


def test_emit_writes_run_queues_jobs_with_the_passthrough(tmp_path, monkeypatch):
    _, spec = _emit(tmp_path, monkeypatch)
    assert [j["seed"] for j in spec["jobs"]] == [2020, 2021, 2022]
    assert all(j["cmd"][-2:] == ["--model", "rf"] for j in spec["jobs"])


def test_emit_refuses_a_different_job_list(tmp_path, monkeypatch):
    _emit(tmp_path, monkeypatch)
    with pytest.raises(SystemExit):
        hpc_jobs.emit(["--name", "t", "--datasets", "Coffee",
                       "--methods", "boruta", "--seeds", "2020"])


def test_run_and_collect(tmp_path, monkeypatch):
    path, spec = _emit(tmp_path, monkeypatch, timeout_hours=1.0 / 3600)
    monkeypatch.setattr(hpc_jobs, "POLL_SECONDS", 0.1)
    _set_cmds(path, spec, [
        [sys.executable, "-c", "pass"],
        [sys.executable, "-c", "import time; time.sleep(60)"],
        [sys.executable, "-c", "import sys; sys.exit(3)"]])
    assert hpc_jobs.run("t", 0, cpus=2) == 0
    assert hpc_jobs.run("t", 1, cpus=2) == 0
    assert hpc_jobs.run("t", 2, cpus=2) == 1
    hpc_jobs.collect("t")
    q = json.loads((tmp_path / "t" / "queue.json").read_text())
    assert [j["state"] for j in q["jobs"]] == ["done", "timeout", "failed"]
    assert q["jobs"][2]["exit_code"] == 3 and q["pid"] is None
    st = hpc_jobs.read_status("t", spec["jobs"][0]["name"])
    assert st["cpus"] == 2


def test_a_finished_job_is_not_run_again(tmp_path, monkeypatch):
    path, spec = _emit(tmp_path, monkeypatch)
    marker = tmp_path / "ran"
    _set_cmds(path, spec, [[sys.executable, "-c",
                            f"open(r'{marker}', 'a').write('x')"]] * 3)
    hpc_jobs.run("t", 0, cpus=1)
    hpc_jobs.run("t", 0, cpus=1)
    assert marker.read_text() == "x"


def test_jobs_without_a_status_are_pending(tmp_path, monkeypatch):
    _emit(tmp_path, monkeypatch)
    hpc_jobs.collect("t")
    q = json.loads((tmp_path / "t" / "queue.json").read_text())
    assert {j["state"] for j in q["jobs"]} == {"pending"}


def test_merge_ledger_adds_only_the_clusters_new_runs(tmp_path):
    import experiment_ids
    here, there = tmp_path / "here.md", tmp_path / "there.md"
    base = [{"experiment": "H9-E01", "hypothesis": "H9", "started": "2026-10-26",
             "runs": ["a"], "status": "running", "report": ""},
            {"experiment": "H8-E01", "hypothesis": "H8", "started": "2026-10-01",
             "runs": ["x"], "status": "reported", "report": ""}]
    experiment_ids.save_ledger(base, here)
    other = [dict(base[0], runs=["a", "b", "c"]), dict(base[1], runs=["y"])]
    experiment_ids.save_ledger(other, there)
    hpc_jobs.merge_ledger("H9-E01", there, path=here)
    rows = {r["experiment"]: r for r in experiment_ids.load_ledger(here)}
    assert rows["H9-E01"]["runs"] == ["a", "b", "c"]
    assert rows["H8-E01"]["runs"] == ["x"]
