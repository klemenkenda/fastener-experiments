"""P2's pilot (H14-E01): the new starts, the min1 mutation, the random
streams and the subset log."""
from types import SimpleNamespace

import numpy as np
import pytest

import nsgaii_miip as nm
import run_sota
import sota_baselines
import subset_log


def _ds(d=40, seed=1):
    rng = np.random.RandomState(seed)
    X = rng.normal(size=(150, d))
    y = (X[:, 0] + X[:, 3] > 0).astype(int)
    return SimpleNamespace(n_features=d, X_train=X[:80], y_train=y[:80],
                           X_val=X[80:115], y_val=y[80:115],
                           X_test=X[115:], y_test=y[115:])


def test_uniform_start_covers_every_size_equally():
    d = 60
    pop = nm.uniform_initialization(6000, d, np.random.RandomState(0))
    k = pop.sum(axis=1)
    assert k.min() >= 1 and k.max() <= d
    assert k.mean() == pytest.approx((d + 1) / 2, rel=0.03)
    assert (k <= 10).mean() == pytest.approx(10 / d, abs=0.015)


def test_loguniform_start_puts_harmonic_mass_on_small_sizes():
    d = 200
    pop = nm.loguniform_initialization(6000, d, np.random.RandomState(0))
    k = pop.sum(axis=1)
    H = lambda n: (1.0 / np.arange(1, n + 1)).sum()
    assert k.min() >= 1 and k.max() <= d
    assert (k <= 10).mean() == pytest.approx(H(10) / H(d), abs=0.02)
    assert (k == 1).mean() == pytest.approx(1 / H(d), abs=0.015)


def test_min1_leaves_no_child_unchanged_and_keeps_zero_drift():
    rng = np.random.RandomState(0)
    d, k = 200, 8
    pop = np.zeros((4000, d), dtype=bool)
    for i in range(len(pop)):
        pop[i, rng.choice(d, k, replace=False)] = True
    out, forced = nm.balanced_mutation_min1(pop, 1.0 / d, rng)
    assert not (out == pop).all(axis=1).any()
    # At k = 8, d = 200 balanced mutation flips 2k/d = 0.08 bits per child,
    # so it leaves about e^-0.08 = 92% of children as they were: those are
    # the forced ones.
    assert forced.mean() > 0.9
    assert (out.sum(axis=1) - k).mean() == pytest.approx(0, abs=0.06)


def test_min1_edges_add_from_one_and_remove_from_full():
    rng = np.random.RandomState(1)
    one = np.zeros((50, 30), dtype=bool)
    one[:, 0] = True
    out, forced = nm.balanced_mutation_min1(one, 1e-9, rng)
    assert forced.all() and (out.sum(axis=1) == 2).all()
    full = np.ones((50, 30), dtype=bool)
    out, forced = nm.balanced_mutation_min1(full, 1e-9, rng)
    assert forced.all() and (out.sum(axis=1) == 29).all()


def test_streams_give_mutation_arms_the_same_start():
    ds = _ds()
    a = sota_baselines.run_nsga2(ds, 7, 120, pop_size=20, init="uniform",
                                 rng_streams=True, name="a")
    b = sota_baselines.run_nsga2(ds, 7, 120, pop_size=20, init="uniform",
                                 rng_streams=True, mutation="min1", name="b")
    c = sota_baselines.run_nsga2(ds, 8, 120, pop_size=20, init="uniform",
                                 rng_streams=True, name="c")
    assert a["start_population_sha256"] == b["start_population_sha256"]
    assert a["start_population_sha256"] != c["start_population_sha256"]
    assert a["method"] == "a" and a["mutation"] == "balanced"
    assert b["mutation"] == "min1"


def test_the_subset_log_is_passive_and_complete(tmp_path):
    ds = _ds()
    log = subset_log.SubsetLog(tmp_path / "s.npz", ds.n_features)
    a = sota_baselines.run_nsga2(ds, 3, 150, pop_size=20, init="sparse",
                                 rng_streams=True, mutation="min1", name="x")
    b = sota_baselines.run_nsga2(ds, 3, 150, pop_size=20, init="sparse",
                                 rng_streams=True, mutation="min1", name="x",
                                 subset_log=log)
    key = lambda r: [(x["n_features"], x["val_score"]) for x in r["records"]]
    assert key(a) == key(b) and a["iterations"] == b["iterations"]
    z = subset_log.read(b["subset_log"])
    assert len(z["sub_size"]) == b["model_fits"] == z["gen_new_fits"].sum()
    assert (z["subsets"].sum(axis=1) == z["sub_size"]).all()
    # Every scored subset is distinct, and generations are logged in order.
    assert len({r.tobytes() for r in z["bits"]}) == len(z["bits"])
    assert z["gen_generation"].tolist() == list(range(b["iterations"] + 1))
    assert z["gen_proposals"][0] == 20
    # min1: from generation 1 on, no child leaves mutation with 0 flips
    # unless it was forced; the histogram counts the mutation proper.
    g = z["gen_generation"] > 0
    assert (z["gen_flips_0"][g] == z["gen_forced_flips"][g]).all()
    assert (z["gen_flips_0"] + z["gen_flips_1"] + z["gen_flips_2"]
            + z["gen_flips_3plus"])[g].tolist() == z["gen_proposals"][g].tolist()


def test_p2_arms_and_their_configs():
    assert set(run_sota.P2_SEARCHES) == {
        "p2_obl", "p2_sparse", "p2_uniform", "p2_loguniform",
        "p2_obl_min1", "p2_sparse_min1", "p2_uniform_min1",
        "p2_loguniform_min1", "p2_obl_b3", "p2_obl_b10", "p2_obl_reach"}
    assert run_sota.P2_SEARCHES["p2_obl_b10"]["budget_multiple"] == 10
    assert all(m in run_sota.ALL_METHODS for m in run_sota.P2_SEARCHES)


def test_unknown_init_or_mutation_is_refused():
    with pytest.raises(ValueError):
        sota_baselines.run_nsga2(_ds(), 0, 10, init="dense")
    with pytest.raises(ValueError):
        sota_baselines.run_nsga2(_ds(), 0, 10, mutation="flip")
