"""The CPU-time budget (H4): FS-SDS and FASTENER stop on process CPU time."""
import time

import numpy as np
import pytest

import cpu_budget
from fs_sds import run_fs_sds


def _slow_objective(genes):
    # Burn about 2 ms of CPU per evaluation, so a small CPU budget is reached.
    # Timed with perf_counter: process_time advances in ~15.6 ms steps on
    # Windows, too coarse to time 2 ms (but fine for budgets of seconds).
    t = time.perf_counter()
    while time.perf_counter() - t < 0.002:
        pass
    return float(np.sum(np.where(genes)[0] % 7))


def test_fs_sds_stops_on_its_cpu_budget_without_a_fit_cap():
    out = run_fs_sds(200, 5, _slow_objective, seed=1, stop_evaluations=None,
                     stop_cpu_seconds=0.3, population_size=20)
    assert out["stopped_on"] == "cpu_budget"
    # Stops before the first evaluation past the budget: at most one over,
    # plus process_time's coarse steps.
    assert out["cpu_seconds"] < 0.3 + 0.05
    assert out["evaluations"] > 20


def test_fs_sds_without_a_cpu_budget_still_stops_on_fits():
    out = run_fs_sds(200, 5, _slow_objective, seed=1, stop_evaluations=40,
                     population_size=20)
    assert out["stopped_on"] == "budget" and out["evaluations"] == 40


def test_fastener_stops_on_its_cpu_budget(tmp_path):
    from datasets import Dataset
    from run_fastener import run_fastener
    rng = np.random.RandomState(0)
    X = rng.rand(300, 40)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    ds = Dataset("toy", X[:180], y[:180], X[180:240], y[180:240],
                 X[240:], y[240:])
    res = run_fastener(ds, tmp_path, seed=1, rounds=100_000, max_fits=None,
                       max_cpu_seconds=1.0, dump_logs=False)
    assert res["stopped_on"] == "cpu_budget"
    assert 1.0 <= res["search_cpu_seconds"] < 2.0
    assert res["params"]["max_cpu_seconds"] == 1.0


@pytest.mark.parametrize("cpu, want", [(0.1, 10), (10.0, 10), (10.01, 20),
                                       (123.4, 130)])
def test_budget_rounds_up_to_ten_seconds(cpu, want):
    assert cpu_budget.budget_from(cpu) == want
