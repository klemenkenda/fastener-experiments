"""The harness does what HYPOTHESES.md says a run does.

One test per protocol decision a run depends on: the k grid, AUF, the row cap,
equal and exact fit budgets (FS-SDS included), Boruta on the shared tree, the
stored metrics, and best-score-per-iteration tracking for every search.
"""
import json
import random

import numpy as np
import pytest

import analysis
import datasets
import protocol
import sota_baselines as sota
from trajectory import Trajectory, read


# ------------------------------------------------------------------ fixtures
@pytest.fixture(scope="module")
def ds():
    """A small Dataset with a clear signal in the first 3 of 25 features."""
    rng = np.random.RandomState(0)
    X = rng.normal(size=(600, 25))
    y = (X[:, :3].sum(axis=1) > 0).astype(int)
    return datasets.Dataset("toy", X[:360], y[:360], X[360:480], y[360:480],
                            X[480:], y[480:])


def record(size, val, test):
    return {"n_features": size, "val_score": val, "test_score": test,
            "test": {"f1_weighted": test}}


# ------------------------------------------------------------ the constants
def test_k_grid_has_every_k_up_to_20():
    assert set(range(1, 21)) <= set(protocol.K_GRID)
    assert protocol.K_GRID == sorted(protocol.K_GRID)


def test_protocol_constants_match_hypotheses():
    assert protocol.FS_SDS_K_RANGE == list(range(1, 21))
    assert protocol.FIT_BUDGET == 6000
    assert protocol.ROW_CAP == 50_000
    # 6,000 split evenly over k = 1..20 is 300 per k, with nothing left over.
    assert protocol.FIT_BUDGET % len(protocol.FS_SDS_K_RANGE) == 0
    assert protocol.LONG_FIT_BUDGET % len(protocol.FS_SDS_K_RANGE) == 0


def test_fit_budget_doubles_only_on_the_unconverged_datasets():
    assert protocol.fit_budget("nci9") == 12_000
    assert protocol.fit_budget("TOX_171") == 12_000
    assert protocol.fit_budget("madelon") == protocol.FIT_BUDGET
    assert len(protocol.LONG_BUDGET_DATASETS) == 11
    # A misspelt name would silently keep the short budget.
    assert protocol.LONG_BUDGET_DATASETS <= set(datasets.LOADERS)


def test_every_runner_uses_the_one_grid():
    import run_experiment
    import run_sota
    import run_sota_experiment
    assert run_experiment.K_GRID is protocol.K_GRID
    assert run_sota.K_GRID is protocol.K_GRID
    assert run_sota_experiment.K_GRID is protocol.K_GRID


# ---------------------------------------------------------------------- AUF
def test_auf_reads_test_score_of_the_validation_choice():
    # Size 2 wins on validation but loses on test: opt(k) must follow the
    # validation choice, not the better test score of the size-1 subset.
    recs = [record(1, 0.60, 0.90), record(2, 0.70, 0.50)]
    out = analysis.auf(recs, K=2)
    assert out["auf"] == pytest.approx((0.90 + 0.50) / 2)
    assert out["k_covered"] == 2


def test_auf_scores_zero_below_the_smallest_subset():
    recs = [record(3, 0.8, 0.8)]
    out = analysis.auf(recs, K=4)
    assert out["auf"] == pytest.approx((0 + 0 + 0.8 + 0.8) / 4)
    assert out["k_covered"] == 2


def test_auf_agrees_with_make_report():
    """Two implementations of the primary metric must never drift apart."""
    import make_report
    rng = random.Random(0)
    for _ in range(200):
        recs = [record(rng.randint(1, 30), rng.random(), rng.random())
                for _ in range(rng.randint(1, 12))]
        for K in (10, 20):
            assert analysis.auf(recs, K)["auf"] == pytest.approx(
                make_report.auf(recs, K))


# ------------------------------------------------------------------- metrics
def test_all_scores_stores_every_f1_average():
    y = np.array([0, 1, 1, 0, 1])
    p = np.array([0, 1, 0, 0, 1])
    s = protocol.all_scores(y, p)
    assert {"f1_weighted", "f1_macro", "f1_binary", "accuracy",
            "balanced_accuracy"} <= set(s)
    assert s["f1_weighted"] == pytest.approx(protocol.primary_score(y, p))


def test_binary_f1_only_for_two_classes():
    y = np.array([0, 1, 2, 0, 1, 2])
    assert protocol.all_scores(y, y)["f1_binary"] is None


# ------------------------------------------------------------------ row cap
def test_row_cap_subsamples_a_tall_dataset():
    if not (datasets.DATA_DIR / "satimage" / "satimage.npz").is_file():
        pytest.skip("satimage not downloaded")
    full = datasets.load("satimage")
    capped = datasets.load("satimage", max_rows=1000)
    assert capped.n_rows_used == pytest.approx(1000, abs=10)
    assert capped.max_rows == 1000
    assert full.n_rows_used == 6430
    # Proportional, so the class shares survive the cut.
    share = lambda d: np.bincount(np.concatenate([d.y_train, d.y_val,  # noqa: E731
                                                  d.y_test])) / d.n_rows_used
    assert np.allclose(share(capped), share(full), atol=0.02)


def test_row_cap_is_identical_across_loads():
    if not (datasets.DATA_DIR / "har" / "har.npz").is_file():
        pytest.skip("har not downloaded")
    a = datasets.load("har", max_rows=2000)
    b = datasets.load("har", max_rows=2000)
    assert np.array_equal(a.X_train, b.X_train)


def test_row_cap_is_a_no_op_for_small_datasets():
    if not (datasets.DATA_DIR / "madelon").is_dir():
        pytest.skip("madelon not downloaded")
    d = datasets.load("madelon", max_rows=100)
    assert d.n_rows_used == 2600
    assert d.max_rows is None


# ----------------------------------------------------------------- budgets
def test_nsga2_stops_exactly_at_the_budget(ds):
    for init in ("obl", "sparse"):
        res = sota.run_nsga2(ds, 2020, 150, pop_size=40, init=init)
        assert res["model_fits"] == 150, init


def test_fs_sds_budget_is_split_across_k(ds):
    ks = [1, 2, 3, 4]
    per_k = 20
    res = sota.run_fs_sds_method(ds, ks, seed=2020, stop_evaluations=per_k,
                                 population_size=10)
    assert all(p["model_fits"] <= per_k for p in res["per_k"])
    assert res["model_fits"] <= per_k * len(ks)


def test_runner_gives_fs_sds_the_same_total_as_everyone_else():
    per_k = protocol.FIT_BUDGET // len(protocol.FS_SDS_K_RANGE)
    assert per_k * len(protocol.FS_SDS_K_RANGE) == protocol.FIT_BUDGET


# ------------------------------------------------------------------- Boruta
def test_boruta_runs_on_the_protocol_tree(ds):
    tree = sota.TreeForBoruta()
    tree.set_params(n_estimators=250, random_state=3)  # what BorutaPy does
    tree.fit(ds.X_train, ds.y_train)
    assert type(tree.tree_) is type(protocol.make_model())
    assert tree.feature_importances_.shape == (ds.n_features,)

    res = sota.run_boruta(ds, [1, 3, 5], protocol.FitCounter(), max_iter=10,
                          seed=2020)
    assert "tree" in res["estimator"]
    assert [r["n_features"] for r in res["records"]] == [1, 3, 5]


def test_tree_for_boruta_rejects_unknown_parameters():
    with pytest.raises(ValueError):
        sota.TreeForBoruta().set_params(max_depth=3)


# --------------------------------------------------------------- trajectory
def test_trajectory_records_best_so_far(tmp_path):
    t = Trajectory(tmp_path / "t.jsonl", "m", 1, k_grid=[1, 2, 3])
    t.observe([4], 0.5)
    t.step(0, 1)
    t.observe([1, 2], 0.7)
    t.observe([7], 0.4)            # worse at size 1: ignored
    t.step(1, 3)
    t.step(2, 3)                   # nothing new
    snaps = read(tmp_path / "t.jsonl")
    assert [s["best_val_f1"] for s in snaps] == [0.5, 0.7, 0.7]
    assert snaps[1]["best_val_f1_by_k"] == {"1": 0.5, "2": 0.7, "3": 0.7}
    assert [s["front_changed"] for s in snaps] == [True, True, False]
    # The unchanged line gets its front back on read.
    assert snaps[2]["front"] == snaps[1]["front"]
    assert snaps[1]["min_size"] == 1 and snaps[1]["max_size"] == 2


def test_trajectory_survives_pickling(tmp_path):
    import pickle
    t = Trajectory(tmp_path / "t.jsonl", "m", 1, k_grid=[1])
    t.observe([0], 0.3)
    assert pickle.loads(pickle.dumps(t)).best_up_to(1) == 0.3


def _check(path, res):
    snaps = read(path)
    assert snaps, "no snapshots written"
    fits = [s["fits"] for s in snaps]
    best = [s["best_val_f1"] or 0 for s in snaps]
    assert fits == sorted(fits)
    assert best == sorted(best)
    assert fits[-1] == res["model_fits"]
    return snaps


def test_nsga2_tracks_every_generation(ds, tmp_path):
    t = Trajectory(tmp_path / "n.jsonl", "nsga2_sparse", 1, protocol.K_GRID[:10])
    res = sota.run_nsga2(ds, 1, 120, pop_size=30, init="sparse", trajectory=t)
    snaps = _check(tmp_path / "n.jsonl", res)
    assert [s["iteration"] for s in snaps] == list(range(res["iterations"] + 1))


def test_poss_tracks_every_fit(ds, tmp_path):
    t = Trajectory(tmp_path / "p.jsonl", "poss", 1, protocol.K_GRID[:10])
    res = sota.run_poss_method(ds, 1, 60, k=10, trajectory=t)
    snaps = _check(tmp_path / "p.jsonl", res)
    assert len(snaps) == res["model_fits"]


def test_fs_sds_tracks_across_its_k_runs(ds, tmp_path):
    t = Trajectory(tmp_path / "f.jsonl", "fs_sds", 1, protocol.K_GRID[:10])
    res = sota.run_fs_sds_method(ds, [1, 2, 3], seed=1, stop_evaluations=25,
                                 population_size=10, trajectory=t)
    snaps = _check(tmp_path / "f.jsonl", res)
    assert {s["k"] for s in snaps} == {1, 2, 3}
    its = [s["iteration"] for s in snaps]
    assert its == sorted(its) and len(set(its)) == len(its)


def test_nsgaii_miip_tracks_every_generation(ds, tmp_path):
    t = Trajectory(tmp_path / "m.jsonl", "nsgaii_miip", 1, protocol.K_GRID[:10])
    res = sota.run_nsgaii_miip_method(ds, 1, 100, pop_size=20, init="sparse",
                                      trajectory=t)
    _check(tmp_path / "m.jsonl", res)
    assert res["model_fits"] == 100


def test_fastener_tracks_every_generation(ds, tmp_path, monkeypatch):
    from run_fastener import run_fastener
    monkeypatch.chdir(tmp_path)
    t = Trajectory(tmp_path / "x.jsonl", "fastener", 1, protocol.K_GRID[:10])
    res = run_fastener(ds, tmp_path, seed=1, rounds=10_000, max_fits=80,
                       dump_logs=False, trajectory=t)
    snaps = _check(tmp_path / "x.jsonl", res)
    assert res["stopped_on"] == "fit_budget"
    assert snaps[0]["iteration"] == 0
    assert snaps[-1]["iteration"] == res["rounds_completed"] + 1


def test_auf_by_seed_carries_every_metric(ds):
    res = sota.run_nsga2(ds, 1, 60, pop_size=20, init="sparse")
    row = analysis.auf_by_seed([res], n_features=ds.n_features)[0]
    for K in (10, 20):
        for m in ("f1_weighted", "f1_macro", "f1_binary", "accuracy",
                  "balanced_accuracy"):
            assert f"auf{K}_{m}" in row
    assert json.dumps(row)  # serialisable for auf.json


def test_sparse_init_works_below_30_features():
    """Regression: sparse init drew up to 30 features without replacement and
    crashed on narrower data. Higgs, used in H5 and H6, has 28."""
    from nsgaii_miip import sparse_initialization
    pop = sparse_initialization(100, 28, np.random.RandomState(0))
    assert pop.sum(axis=1).min() >= 1 and pop.sum(axis=1).max() <= 28


def test_sparse_init_unchanged_at_30_or_more_features():
    """The fix must not change the random stream where there was no bug."""
    from nsgaii_miip import sparse_initialization

    def old(pop_size, n_features, rng, max_size=30):
        pop = np.zeros((pop_size, n_features), dtype=bool)
        for i in range(pop_size):
            k = rng.randint(1, max_size + 1)
            pop[i, rng.choice(n_features, size=k, replace=False)] = True
        return pop

    for n in (30, 36, 500):
        assert np.array_equal(sparse_initialization(50, n, np.random.RandomState(7)),
                              old(50, n, np.random.RandomState(7)))
