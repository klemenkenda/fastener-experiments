"""H15: the OBL start stopped at reach (`stop_at_size`)."""
import numpy as np

import run_sota
import sota_baselines
import subset_log
from test_h14_pilot import _ds


def _run(ds, tmp_path, tag, **kw):
    log = subset_log.SubsetLog(tmp_path / f"{tag}.npz", ds.n_features)
    # The stagnation stop, as every real run has (DEC-41): without it a
    # converged toy population can re-propose cached subsets forever.
    r = sota_baselines.run_nsga2(ds, 11, 1500, pop_size=20, init="obl",
                                 rng_streams=True, name=tag, subset_log=log,
                                 max_barren_generations=50, **kw)
    return r, subset_log.read(r["subset_log"])


def test_stop_at_reach_is_the_prefix_of_an_unstopped_run(tmp_path):
    ds = _ds(d=40)
    full, zf = _run(ds, tmp_path, "full")
    stop, zs = _run(ds, tmp_path, "stop", stop_at_size=10)
    first = int(np.argmax(zf["sub_size"] <= 10)) + 1   # fits to reach
    assert (zf["sub_size"] <= 10).any() and first < full["model_fits"]
    assert stop["stopped_on"] == "reach" and stop["stop_at_size"] == 10
    # It stops at the end of the generation that reached: at most one
    # population of fits after the first subset of at most 10 features.
    assert first <= stop["model_fits"] < first + 20
    n = stop["model_fits"]
    assert (zs["bits"] == zf["bits"][:n]).all()
    assert (zs["sub_size"] <= 10).any()
    assert min(r["n_features"] for r in stop["records"]) <= 10


def test_stop_at_size_off_changes_nothing():
    ds = _ds(d=40)
    kw = dict(pop_size=20, rng_streams=True, max_barren_generations=50)
    a = sota_baselines.run_nsga2(ds, 5, 600, **kw)
    b = sota_baselines.run_nsga2(ds, 5, 600, stop_at_size=None, **kw)
    key = lambda r: [(x["n_features"], x["val_score"]) for x in r["records"]]
    assert key(a) == key(b) and a["model_fits"] == b["model_fits"]
    assert "stop_at_size" not in b and b["stopped_on"] != "reach"


def test_the_reach_arm():
    spec = run_sota.P2_SEARCHES["p2_obl_reach"]
    assert spec == {"init": "obl", "mutation": "balanced",
                    "budget_multiple": 1, "stop_at_size": 10}
    # The other arms' specs, and so their config hashes, are unchanged.
    assert all("stop_at_size" not in s for m, s in run_sota.P2_SEARCHES.items()
               if m != "p2_obl_reach")


def test_committed_caps_are_four_times_the_prediction():
    import json, math
    import h15_report as h
    b = json.loads((h.HERE / "h15_budgets.json").read_text(encoding="utf-8"))
    assert set(b["budgets"]) == set(h.DATASETS)
    d = {"gas_drift": 128, "crop_mapping": 174, "volkert": 180, "madelon": 500,
         "Isolet": 617, "gina": 970, "ORL": 1024}
    for ds, cap in b["budgets"].items():
        F = h.predicted(d[ds])
        assert b["predicted_fits_to_reach"][ds] == round(F)
        assert cap == math.ceil(h.CAP_FACTOR * F / 1000) * 1000


def test_censored_median_and_the_criterion():
    import h15_report as h
    assert h.censored_median([1, 2, None, None, None]) == float("inf")
    assert h.censored_median([1, 2, 3, None, None]) == 3
    rows = []
    for ds, d in zip(h.DATASETS, (128, 174, 180, 500, 617, 970, 1024)):
        F = h.predicted(d)
        for j, s in enumerate(h.SEEDS):
            ok = not (ds == "ORL" and j < 2)       # ORL: 3 of 5 reach
            rows.append({"dataset": ds, "seed": s, "d": d, "finished": True,
                         "reached": ok, "ttr_fits": F * (1.5 if ds == "gina" else 1) if ok else None,
                         "ttr_seconds": 1.0 if ok else None, "n_train": 100})
    per = h.per_dataset(rows)
    sl = h.slope(per)
    v = h.criterion(per, sl)
    assert not v["i"] and v["datasets_i"] == 6           # ORL fails (i)
    assert v["datasets_ii"] == 7 and v["ii"]             # all within factor 2
    assert abs(sl["slope"] - h.B) < 0.1 and v["iii"]
    assert not v["supported"]
