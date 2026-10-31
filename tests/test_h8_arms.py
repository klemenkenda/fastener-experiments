"""H8's arms in run_sota.py: prior files, the guidance passed to FASTENER,
and the proposer arm, with a fake model (no network)."""
import json

import numpy as np
import pytest

import llm_guidance as lg
import run_sota
from datasets import Dataset
from run_fastener import run_fastener

from test_llm_guidance import FakeTransport


@pytest.fixture
def tiny_ds():
    rng = np.random.RandomState(0)
    X = rng.normal(size=(300, 8))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    return Dataset("toy", X[:180], y[:180], X[180:240], y[180:240], X[240:], y[240:],
                   feature_names=np.array([f"x{i}" for i in range(8)]))


@pytest.fixture
def priors(tmp_path, monkeypatch):
    monkeypatch.setattr(lg, "PRIORS_DIR", tmp_path / "priors")
    (tmp_path / "priors" / "dictionaries").mkdir(parents=True)
    (tmp_path / "priors" / "dictionaries" / "toy.json").write_text(
        json.dumps({"task": "toy", "class_names": ["a", "b"]}), encoding="utf-8")
    model = run_sota.H8_MODELS["opus"]
    lg.prior_path("toy", model, False).write_text(
        json.dumps({"scores": [1.0, 1.0] + [0.1] * 6}), encoding="utf-8")
    return tmp_path


def test_every_h8_arm_is_defined_with_its_settings():
    arms = {a: c for a, c in run_sota.FASTENER_ARMS.items() if "llm" in c}
    assert len(arms) == 4 * 3 + 3 + 4 * 9 + 3 + 1 + 2 * 12
    for m in run_sota.H8_MODELS:
        assert arms[f"llm_{m}_blind"]["llm"]["blind"]
        assert arms[f"llm_{m}"]["llm"]["uses"] == ("mating", "mutation", "initial")
        assert arms[f"llm_{m}_scrambled"]["llm"]["scrambled"]
        assert arms[f"llm_{m}_proposer"]["llm"]["proposer"]
    assert arms["llm_opus_mutation"]["llm"]["uses"] == ("mutation",)
    assert all(a in run_sota.FASTENER_ARM_ORDER for a in arms)


def test_a_missing_prior_stops_the_run(tiny_ds, priors, tmp_path):
    llm = run_sota.FASTENER_ARMS["llm_haiku"]["llm"]
    with pytest.raises(FileNotFoundError, match="llm_guidance.py prior"):
        run_sota.h8_guidance(llm, "toy", tiny_ds, tmp_path, "x", 2020)


def test_prior_arm_runs_on_its_budget(tiny_ds, priors, tmp_path):
    llm = run_sota.FASTENER_ARMS["llm_opus"]["llm"]
    guidance, info = run_sota.h8_guidance(llm, "toy", tiny_ds, tmp_path, "fastener_llm_opus", 2020)
    res = run_fastener(tiny_ds, tmp_path, seed=2020, rounds=1000, max_fits=30,
                       guidance=guidance, dump_logs=False)
    res.update(info.pop("finish")(info))
    assert res["model_fits"] == 30 and res["stopped_on"] == "fit_budget"
    assert res["params"]["initial_genes"] == []
    assert len(res["prior_singles"]) == 5
    assert res["prior_file"].startswith("toy__anthropic-claude-opus-5.5")


def test_proposer_arm_calls_the_model_and_logs_it(tiny_ds, priors, tmp_path, monkeypatch):
    real = lg.OpenRouterClient.__init__

    def init(self, api_key=None, **kw):
        real(self, "k", transport=FakeTransport())
    monkeypatch.setattr(lg.OpenRouterClient, "__init__", init)
    llm = run_sota.FASTENER_ARMS["llm_opus_proposer"]["llm"]
    guidance, info = run_sota.h8_guidance(llm, "toy", tiny_ds, tmp_path,
                                          "fastener_llm_opus_proposer", 2020)
    res = run_fastener(tiny_ds, tmp_path, seed=2020, rounds=1000, max_fits=40,
                       guidance=guidance, dump_logs=False)
    res.update(info.pop("finish")(info))
    assert res["model_fits"] == 40
    assert res["proposal_log"] and res["llm_calls_sent"] == len(res["proposal_log"])
    log = tmp_path / "llm_calls_fastener_llm_opus_proposer_s2020.jsonl"
    assert len(log.read_text(encoding="utf-8").splitlines()) == res["llm_calls_sent"]


def test_revised_h8e03_arms_are_defined():
    """DEC-53: per model a lambda-1 prior and its permuted twin; one MI-only arm."""
    arms = run_sota.FASTENER_ARMS
    for m in {**run_sota.H8_MODELS, **run_sota.H8_E03_MODELS}:
        assert arms[f"llm_{m}_l1"]["llm"]["lambda"] == 1.0
        assert arms[f"llm_{m}_permuted_l1"]["llm"]["permuted"]
        assert arms[f"llm_{m}_permuted_l1"]["llm"]["lambda"] == 1.0
    assert arms["mi_only"]["llm"]["flat"] and "lambda" not in arms["mi_only"]["llm"]
    # H8-E01's arms keep their settings (and so their config hashes).
    assert "lambda" not in arms["llm_opus"]["llm"]


def test_permuted_prior_is_the_named_one_shuffled(tiny_ds, priors, tmp_path):
    named, _ = run_sota.h8_guidance(run_sota.FASTENER_ARMS["llm_opus_l1"]["llm"],
                                    "toy", tiny_ds, tmp_path, "a", 2020)
    perm, info = run_sota.h8_guidance(run_sota.FASTENER_ARMS["llm_opus_permuted_l1"]["llm"],
                                      "toy", tiny_ds, tmp_path, "b", 2020)
    order = np.random.RandomState(run_sota.H8_PERMUTE_SEED).permutation(8)
    assert np.array_equal(perm["feature_prior"], named["feature_prior"][order])
    assert not np.array_equal(perm["feature_prior"], named["feature_prior"])
    assert named["prior_weight"] == perm["prior_weight"] == 1.0
    assert info["prior_permutation_seed"] == run_sota.H8_PERMUTE_SEED
    assert info["prior_file"].startswith("toy__anthropic-claude-opus-5.5")


def test_mi_only_arm_needs_no_prior_file_and_runs(tiny_ds, tmp_path, monkeypatch):
    import llm_guidance as lg
    monkeypatch.setattr(lg, "PRIORS_DIR", tmp_path / "none")
    guidance, info = run_sota.h8_guidance(run_sota.FASTENER_ARMS["mi_only"]["llm"],
                                          "toy", tiny_ds, tmp_path, "c", 2020)
    assert np.all(guidance["feature_prior"] == 1.0) and guidance["prior_weight"] == 0.5
    assert info["prior_flat"] and info["prior_file"] is None
    res = run_fastener(tiny_ds, tmp_path, seed=2020, rounds=1000, max_fits=30,
                       guidance=guidance, dump_logs=False)
    assert res["model_fits"] == 30 and len(res["prior_singles"]) == 5
