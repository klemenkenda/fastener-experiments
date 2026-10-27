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


def test_ranges_compress_indices_for_sbatch():
    assert hpc_jobs.ranges([0, 1, 2, 5, 7, 8]) == "0-2,5,7-8"
    assert hpc_jobs.ranges([4]) == "4" and hpc_jobs.ranges([]) == ""


def test_select_splits_by_cells_and_leaves_out_finished_jobs(tmp_path,
                                                             monkeypatch):
    monkeypatch.setattr(hpc_jobs, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(run_queue, "RESULTS_DIR", tmp_path)
    hpc_jobs.emit(["--name", "t", "--datasets", "Coffee,Ham",
                   "--methods", "boruta,mrmr", "--seeds", "2020,2021"])
    spec = hpc_jobs.load_jobs("t")
    cells = [(j["dataset"], j["arm"]) for j in spec["jobs"]]
    high = hpc_jobs.select("t", "Ham:boruta,Coffee:mrmr")
    assert [cells[i] for i in high] == [("Coffee", "mrmr"), ("Ham", "boruta"),
                                        ("Ham", "boruta")]
    low = hpc_jobs.select("t", "Ham:boruta,Coffee:mrmr", invert=True)
    assert sorted(high + low) == list(range(len(cells)))
    assert len(hpc_jobs.select("t", "Ham:*")) == 3
    hpc_jobs.write_json(hpc_jobs.status_path("t", spec["jobs"][0]["name"]),
                        {"state": "done"})
    hpc_jobs.write_json(hpc_jobs.status_path("t", spec["jobs"][1]["name"]),
                        {"state": "failed"})
    assert 0 not in hpc_jobs.select("t", unfinished=True)
    assert 1 in hpc_jobs.select("t", unfinished=True)


def test_collect_gives_the_eta_the_slots_actually_in_use(tmp_path, monkeypatch):
    _emit(tmp_path, monkeypatch)
    spec = hpc_jobs.load_jobs("t")
    monkeypatch.setenv("HPC_MAX_PARALLEL", "200")
    hpc_jobs.collect("t")
    q = json.loads((tmp_path / "t" / "queue.json").read_text())
    assert q["max_procs"] == 200            # nothing running yet: the cap
    for j in spec["jobs"][:2]:
        hpc_jobs.write_json(hpc_jobs.status_path("t", j["name"]),
                            {"state": "running", "started_utc": run_queue.utc()})
    hpc_jobs.collect("t")
    q = json.loads((tmp_path / "t" / "queue.json").read_text())
    assert q["max_procs"] == 2              # what the cluster grants now


def test_run_uses_its_own_interpreter_not_the_emitted_one(tmp_path,
                                                          monkeypatch):
    path, spec = _emit(tmp_path, monkeypatch)
    marker = tmp_path / "ran"
    # As emitted on a login node: a Python that does not exist here.
    _set_cmds(path, spec, [["/tmp/elsewhere/bin/python", "-c",
                            f"open(r'{marker}', 'w').write('x')"]] * 3)
    assert hpc_jobs.run("t", 0, cpus=1) == 0
    assert marker.read_text() == "x"


def test_a_deferred_run_leaves_the_ledger_alone(tmp_path, monkeypatch):
    import experiment_ids
    import provenance
    ledger = tmp_path / "EXPERIMENTS.md"
    experiment_ids.save_ledger([{"experiment": "H9-E01", "hypothesis": "H9",
                                 "started": "2026-10-26", "runs": [],
                                 "status": "running", "report": ""}], ledger)
    monkeypatch.setenv(provenance.DEFER_LEDGER_ENV, "1")
    run = provenance.Run("x", root=tmp_path / "results", experiment_id="H9-E01",
                         allow_dirty=True, ledger=ledger)
    assert run.manifest["ledger"] == "deferred"
    assert experiment_ids.find(experiment_ids.load_ledger(ledger),
                               "H9-E01")["runs"] == []


def test_ledger_records_each_jobs_latest_run_once(tmp_path, monkeypatch):
    import experiment_ids
    monkeypatch.setattr(hpc_jobs, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(run_queue, "RESULTS_DIR", tmp_path)
    ledger = tmp_path / "EXPERIMENTS.md"
    experiment_ids.save_ledger([{"experiment": "H9-E01", "hypothesis": "H9",
                                 "started": "2026-10-26", "runs": ["early"],
                                 "status": "running", "report": ""}], ledger)
    hpc_jobs.emit(["--experiment", "H9-E01", "--datasets", "Coffee",
                   "--methods", "boruta", "--seeds", "2020,2021,2022"])
    spec = hpc_jobs.load_jobs("H9-E01")
    runs = {0: ("2026-10-26T17:10:00+00:00", "b_run"),
            1: ("2026-10-26T17:05:00+00:00", "a_run")}
    for i, (start, rid) in runs.items():
        hpc_jobs.write_json(hpc_jobs.status_path("H9-E01", spec["jobs"][i]["name"]),
                            {"name": spec["jobs"][i]["name"], "state": "done",
                             "started_utc": start,
                             "run_dir": str(tmp_path / rid)})
    hpc_jobs.record_ledger("H9-E01", path=ledger)
    hpc_jobs.record_ledger("H9-E01", path=ledger)
    row = experiment_ids.find(experiment_ids.load_ledger(ledger), "H9-E01")
    assert row["runs"] == ["early", "a_run", "b_run"]


def test_skip_running_leaves_out_jobs_still_running(tmp_path, monkeypatch):
    _emit(tmp_path, monkeypatch)
    spec = hpc_jobs.load_jobs("t")
    for i, state in ((0, "running"), (1, "failed")):
        hpc_jobs.write_json(hpc_jobs.status_path("t", spec["jobs"][i]["name"]),
                            {"state": state})
    assert hpc_jobs.select("t", unfinished=True) == [0, 1, 2]
    assert hpc_jobs.select("t", unfinished=True, skip_running=True) == [1, 2]


def test_within_keeps_an_arm_on_every_dataset(tmp_path, monkeypatch):
    monkeypatch.setattr(hpc_jobs, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(run_queue, "RESULTS_DIR", tmp_path)
    hpc_jobs.emit(["--name", "t", "--datasets", "Coffee,Ham",
                   "--methods", "boruta,fastener:none,fastener:guided",
                   "--seeds", "2020"])
    spec = hpc_jobs.load_jobs("t")
    got = hpc_jobs.select("t", within="*:fastener_none,*:fastener_guided")
    assert {spec["jobs"][i]["arm"] for i in got} == {"fastener_none",
                                                     "fastener_guided"}
    assert len(got) == 4
    # with the high-memory split on top: Ham's jobs in one array, the rest
    high = hpc_jobs.select("t", cells="Ham:*", within="*:fastener_none")
    assert [spec["jobs"][i]["dataset"] for i in high] == ["Ham"]


def test_rerun_runs_a_finished_job_again(tmp_path, monkeypatch):
    path, spec = _emit(tmp_path, monkeypatch)
    marker = tmp_path / "ran"
    _set_cmds(path, spec, [[sys.executable, "-c",
                            f"open(r'{marker}', 'a').write('x')"]] * 3)
    hpc_jobs.run("t", 0, cpus=1)
    hpc_jobs.run("t", 0, cpus=1)
    assert marker.read_text() == "x"
    monkeypatch.setenv("HPC_RERUN", "1")
    hpc_jobs.run("t", 0, cpus=1)
    assert marker.read_text() == "xx"


def test_a_job_that_cannot_start_is_marked_failed(tmp_path, monkeypatch):
    path, spec = _emit(tmp_path, monkeypatch)
    monkeypatch.setattr(hpc_jobs.sys, "executable", str(tmp_path / "no-python"))
    with pytest.raises(OSError):
        hpc_jobs.run("t", 0, cpus=1)
    assert hpc_jobs.read_status("t", spec["jobs"][0]["name"])["state"] == "failed"


def test_bounded_model_store_gives_the_same_front(tmp_path):
    import _bootstrap  # noqa: F401
    from run_fastener import run_fastener
    rng = np.random.RandomState(3)
    X = rng.normal(size=(120, 15))
    y = (X[:, 0] + X[:, 3] > 0).astype(int)
    ds = SimpleNamespace(n_features=15, X_train=X[:70], y_train=y[:70],
                         X_val=X[70:95], y_val=y[70:95], X_test=X[95:],
                         y_test=y[95:])
    runs = {}
    for cache in (None, 0.0):
        run_dir = tmp_path / f"cache_{cache}"
        run_dir.mkdir()
        runs[cache] = run_fastener(ds, run_dir, seed=1, rounds=1000,
                                   swap="guided", max_fits=150,
                                   dump_logs=False, model_cache_mb=cache)
    a, b = runs[None], runs[0.0]
    assert b["model_refits"] > 0 and a["model_fits"] == b["model_fits"]
    assert [(r["features"], r["val_score"], r["test_score"])
            for r in a["records"]] == [(r["features"], r["val_score"],
                                        r["test_score"]) for r in b["records"]]


def test_a_repo_git_cannot_read_is_unverified_not_clean(tmp_path, monkeypatch):
    import provenance
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr(provenance, "_git", lambda repo, *args: None)
    st = provenance.git_state(tmp_path, ("results",))
    assert st["commit"] is None and st["code_dirty"] and st["dirty"]
    with pytest.raises(provenance.DirtyTreeError):
        provenance.Run("x", root=tmp_path / "results", experiment_id="H9-E01",
                       ledger=_one_row_ledger(tmp_path))


def _one_row_ledger(tmp_path):
    import experiment_ids
    ledger = tmp_path / "EXPERIMENTS.md"
    experiment_ids.save_ledger([{"experiment": "H9-E01", "hypothesis": "H9",
                                 "started": "2026-10-28", "runs": [],
                                 "status": "running", "report": ""}], ledger)
    return ledger


# ---------------------------------------------------------------- LightGBM
def test_lgbm_leaf_follows_the_training_split():
    assert [protocol.lgbm_min_child_samples(n) for n in (10, 34, 100, 399, 400, 30000)] \
        == [1, 1, 5, 19, 20, 20]


def test_lgbm_needs_the_split_size_and_is_thread_invariant():
    pytest.importorskip("lightgbm")
    protocol.set_model("lgbm", n_jobs=2)
    with pytest.raises(RuntimeError):
        protocol.make_model()
    rng = np.random.RandomState(0)
    X, y = rng.normal(size=(200, 6)), rng.randint(0, 3, 200)
    preds = []
    for jobs in (1, 3):
        protocol.set_model("lgbm", n_jobs=jobs)
        protocol.set_train_rows(200)
        m = protocol.make_model()
        assert m.min_child_samples == 10
        preds.append(m.fit(X, y).predict_proba(X))
    assert np.array_equal(*preds)
    assert "min(20, max(1, n_train // 20))" in protocol.model_description()
    protocol.set_model("tree")


def test_the_model_store_sizes_lgbm_models():
    pytest.importorskip("lightgbm")
    import _bootstrap  # noqa: F401
    from run_fastener import model_nbytes
    protocol.set_model("lgbm", n_jobs=1)
    protocol.set_train_rows(300)
    rng = np.random.RandomState(1)
    m = protocol.make_model().fit(rng.normal(size=(300, 5)), rng.randint(0, 2, 300))
    protocol.set_model("tree")
    assert model_nbytes(m) > 10_000


# ------------------------------------------------- commits without git (DEC-43)
def _fake_repo(tmp_path, head, refs=None, packed=None):
    g = tmp_path / ".git"
    (g / "refs" / "heads").mkdir(parents=True)
    (g / "HEAD").write_text(head)
    for name, sha in (refs or {}).items():
        (g / "refs" / "heads" / name).write_text(sha + "\n")
    if packed:
        (g / "packed-refs").write_text(packed)
    return tmp_path


def test_read_head_detached_loose_and_packed(tmp_path):
    import provenance
    a = _fake_repo(tmp_path / "a", "3be56971101dd77da08450dc7b5712352d0f4d9f\n")
    assert provenance.read_head(a).startswith("3be5697")
    b = _fake_repo(tmp_path / "b", "ref: refs/heads/master\n", refs={"master": "f" * 40})
    assert provenance.read_head(b) == "f" * 40
    c = _fake_repo(tmp_path / "c", "ref: refs/heads/master\n",
                   packed="# pack-refs\n" + "e" * 40 + " refs/heads/master\n")
    assert provenance.read_head(c) == "e" * 40


def test_without_git_only_the_verified_commit_counts_as_clean(tmp_path, monkeypatch):
    import provenance
    repo = _fake_repo(tmp_path, "ref: refs/heads/master\n", refs={"master": "a" * 40})
    monkeypatch.setattr(provenance, "_git", lambda repo, *args: None)
    monkeypatch.setenv("FASTENER_VERIFIED_EXPERIMENTS", "a" * 40)
    st = provenance.git_state(repo, (), "FASTENER_VERIFIED_EXPERIMENTS")
    assert st["commit"] == "a" * 40 and not st["code_dirty"] and "verified" in st
    monkeypatch.setenv("FASTENER_VERIFIED_EXPERIMENTS", "b" * 40)   # pulled since
    st = provenance.git_state(repo, (), "FASTENER_VERIFIED_EXPERIMENTS")
    assert st["commit"] == "a" * 40 and st["code_dirty"]
    monkeypatch.delenv("FASTENER_VERIFIED_EXPERIMENTS")
    assert provenance.git_state(repo, (), "FASTENER_VERIFIED_EXPERIMENTS")["code_dirty"]
