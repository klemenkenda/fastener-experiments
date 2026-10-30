"""llm_guidance.py: OpenRouter prior and proposer, record and replay, with a
fake transport (no network)."""
import json

import numpy as np
import pytest

import llm_guidance as lg
from fastener import Config, EntropyOptimizer
from guidance import GuidanceContext, PriorGuidedMutationStrategy, ProposalContext
from item import (IntersectionMatingWithWeightedRandomInformationGain,
                  RandomEveryoneWithEveryone)


class FakeTransport:
    """Answers like a chat model: a prior favouring the first `n_good`
    features, or a proposal of features 0..2."""

    def __init__(self, n_good=3, fenced=False, drop=()):
        self.calls = []
        self.n_good, self.fenced, self.drop = n_good, fenced, set(drop)

    def __call__(self, url, headers, body, timeout):
        self.calls.append(body)
        user = body["messages"][-1]["content"]
        if "Current front" in user:
            reply = {"subsets": [[0, 1, 2], [0, 1], ["x"], [1, 2]]}
        else:
            idx = [int(line.split(":")[0]) for line in user.splitlines()
                   if line[:1].isdigit()]
            reply = {"scores": {str(i): (1.0 if i < self.n_good else 0.1)
                                for i in idx if i not in self.drop}}
        text = json.dumps(reply)
        if self.fenced:
            text = f"Here you go:\n```json\n{text}\n```"
        return {"id": "x", "model": body["model"] + "-served",
                "usage": {"total_tokens": 10},
                "choices": [{"message": {"content": text}}]}


def ctx(n=6):
    return GuidanceContext(n, [f"name{i}" for i in range(n)], task="toy",
                           class_names=["a", "b"],
                           metadata={"feature_descriptions": {"name0": "the key one"}})


def test_prior_parses_fills_and_records(tmp_path):
    t = FakeTransport(fenced=True, drop={5})
    log = lg.CallLog(tmp_path / "calls.jsonl", "record", lg.OpenRouterClient("k", transport=t))
    prior = lg.LLMFeaturePrior(log, "vendor/model", chunk=4)
    scores = prior(ctx())
    np.testing.assert_allclose(scores, [1, 1, 1, 0.1, 0.1, 0.1])
    # 6 features in chunks of 4; the second chunk lacked 1 of 2 (> 20%) and was
    # asked once more, for that feature only, which the fake still omits.
    assert len(t.calls) == 3
    assert prior.record["missing"] == [5]
    assert prior.record["calls"][0]["served_model"] == "vendor/model-served"
    assert "the key one" in t.calls[0]["messages"][1]["content"]
    # The file a run reads back.
    path = tmp_path / "p.json"
    lg.save_prior(path, "toy", ctx(), prior, scores)
    np.testing.assert_allclose(lg.load_prior(path, 6), scores)
    with pytest.raises(ValueError):
        lg.load_prior(path, 7)


def test_scrambled_prior_hides_names_and_descriptions(tmp_path):
    t = FakeTransport()
    log = lg.CallLog(tmp_path / "c.jsonl", "record", lg.OpenRouterClient("k", transport=t))
    lg.LLMFeaturePrior(log, "m", scrambled=True)(ctx())
    text = t.calls[0]["messages"][1]["content"]
    assert "name0" not in text and "the key one" not in text
    assert "feature_0" in text and "Task: toy" in text


def test_replay_needs_no_client_and_refuses_unknown_requests(tmp_path):
    path = tmp_path / "calls.jsonl"
    t = FakeTransport()
    first = lg.LLMFeaturePrior(lg.CallLog(path, "record", lg.OpenRouterClient("k", transport=t)), "m")(ctx())
    replay = lg.CallLog(path, "replay")
    again = lg.LLMFeaturePrior(replay, "m")(ctx())
    np.testing.assert_array_equal(first, again)
    assert replay.replayed == 1 and replay.sent == 0
    with pytest.raises(KeyError):
        lg.LLMFeaturePrior(replay, "other/model")(ctx())


def test_client_without_key_refuses_to_send():
    with pytest.raises(RuntimeError):
        lg.OpenRouterClient(api_key="").chat({"model": "m", "messages": []})


def test_proposer_cleans_its_reply(tmp_path):
    t = FakeTransport()
    log = lg.CallLog(tmp_path / "c.jsonl", "record", lg.OpenRouterClient("k", transport=t))
    p = lg.LLMSubsetProposer(log, "m", max_subsets=3)
    pc = ProposalContext(ctx(), 5, [{"size": 1, "features": [3], "score": 0.5}], 40, 100)
    assert p(pc) == [[0, 1, 2], [0, 1]]          # ["x"] dropped, 4th cut
    assert "size 1: [3] (name3) -> 0.5000" in t.calls[0]["messages"][1]["content"]


def test_search_with_llm_guidance_replays_exactly(tiny_data, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    n = tiny_data.X.shape[1]
    g = GuidanceContext(n, [f"f{i}" for i in range(n)], task="toy")

    def run(name, log):
        from conftest import RecordingEvaluator
        from test_swap_strategies import CountingModelFactory
        opt = EntropyOptimizer(
            CountingModelFactory(), tiny_data.X, tiny_data.y,
            RecordingEvaluator(tiny_data.X_val, tiny_data.y_val), n,
            RandomEveryoneWithEveryone(
                pool_size=3,
                mating_strategy=IntersectionMatingWithWeightedRandomInformationGain()),
            PriorGuidedMutationStrategy(1 / n), initial_genes=[[n - 1]],
            config=Config(name, 2020, number_of_rounds=6, reset_to_pareto_rounds=2),
            feature_prior=lg.LLMFeaturePrior(log, "m"),
            guidance_context=g,
            subset_proposer=lg.LLMSubsetProposer(log, "m"), proposer_every=3)
        opt.mainloop()
        return opt

    path = tmp_path / "calls.jsonl"
    rec = run("rec", lg.CallLog(path, "record", lg.OpenRouterClient("k", transport=FakeTransport())))
    rep_log = lg.CallLog(path, "replay")
    rep = run("rep", rep_log)
    assert rep_log.sent == 0 and rep_log.replayed == 3   # prior + 2 proposals
    assert rec.proposal_log == rep.proposal_log
    assert {k: v.genes for k, v in rec.pareto_front.items()} == \
        {k: v.genes for k, v in rep.pareto_front.items()}


def test_blind_prior_hides_names_order_and_description(tmp_path):
    t = FakeTransport(n_good=2)
    log = lg.CallLog(tmp_path / "c.jsonl", "record", lg.OpenRouterClient("k", transport=t))
    c = GuidanceContext(6, [f"name{i}" for i in range(6)], task="toy", class_names=["a", "b"],
                        metadata={"dataset_description": "SECRET",
                                  "feature_descriptions": {"name0": "the key one"}})
    p = lg.LLMFeaturePrior(log, "m", blind=True)
    scores = p(c)
    text = t.calls[0]["messages"][1]["content"]
    assert "SECRET" not in text and "name" not in text and "the key one" not in text
    assert "Task: toy" in text and "Classes: a, b" in text
    perm = p.record["permutation"]
    # The fake rates positions 0 and 1 highest: those are columns perm[0], perm[1].
    assert sorted(np.flatnonzero(scores == 1.0)) == sorted(perm[:2])
    assert lg.prior_path("d", "vendor/m", True, True).name == "d__vendor-m__blind.json"


def test_spending_cap_stops_before_sending(tmp_path):
    t = FakeTransport()
    log = lg.CallLog(tmp_path / "c.jsonl", "record", lg.OpenRouterClient("k", transport=t),
                     max_cost=1.0, spent_before=1.0)
    with pytest.raises(RuntimeError, match="spending cap"):
        lg.LLMFeaturePrior(log, "m")(ctx())
    assert t.calls == []


def test_parse_scores_reads_what_small_models_write():
    names = ["a", "b", "c"]
    assert lg.parse_scores('{"scores": {"0": 0.3, "1": 0.5}}', names) == ({0: 0.3, 1: 0.5}, "json")
    commented = '```json\n{"scores": {\n "0": 0.3, // low\n "1": 0.9,\n}}\n```'
    assert lg.parse_scores(commented, names)[0] == {0: 0.3, 1: 0.9}
    assert lg.parse_scores('```json\n{"0": 0.6, "2": 0.1}\n```', names) == ({0: 0.6, 2: 0.1}, "json-flat")
    assert lg.parse_scores('[{"feature": "b", "score": 0.7}]', names)[0] == {1: 0.7}
    # Cut off by max_tokens: the complete pairs, not the truncated last value.
    assert lg.parse_scores('{"scores": {"0": 0.2, "1": 0.8, "2": 0.', names)[0] == {0: 0.2, 1: 0.8}


class HalfTransport(FakeTransport):
    """Leaves out half the features on the first ask, answers the rest after."""

    def __call__(self, url, headers, body, timeout):
        user = body["messages"][-1]["content"]
        idx = [int(l.split(":")[0]) for l in user.splitlines() if l[:1].isdigit()]
        self.calls.append(body)
        keep = idx if len(self.calls) > 1 else idx[: len(idx) // 2]
        return {"model": body["model"], "choices": [{"message": {"content": json.dumps(
            {"scores": {str(i): 0.5 for i in keep}})}}]}


def test_prior_retries_once_for_missing_features(tmp_path):
    t = HalfTransport()
    log = lg.CallLog(tmp_path / "c.jsonl", "record", lg.OpenRouterClient("k", transport=t))
    p = lg.LLMFeaturePrior(log, "m")
    s = p(ctx())
    assert len(t.calls) == 2 and p.record["missing"] == [] and np.allclose(s, 0.5)
    assert "0: name0" not in t.calls[1]["messages"][1]["content"]   # only the missing ones


def test_proposer_survives_errors_and_its_cap(tmp_path):
    def broken(url, headers, body, timeout):
        raise RuntimeError("network down")
    log = lg.CallLog(tmp_path / "c.jsonl", "record", lg.OpenRouterClient("k", transport=broken))
    p = lg.LLMSubsetProposer(log, "m")
    pc = ProposalContext(ctx(), 5, [{"size": 1, "features": [3], "score": 0.5}], 40, 100)
    assert p(pc) == [] and "network down" in p.calls[0]["error"]
    capped = lg.CallLog(tmp_path / "d.jsonl", "record",
                        lg.OpenRouterClient("k", transport=FakeTransport()), max_cost=0.0)
    assert lg.LLMSubsetProposer(capped, "m")(pc) == []
    assert lg.max_tokens_for("microsoft/phi-4", 16000) == 8000
    assert lg.max_tokens_for("other/model", 16000) == 16000
