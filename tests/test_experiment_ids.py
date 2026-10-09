"""Experiment IDs, algorithm IDs, the ledger, and the report generator."""
import json

import numpy as np
import pytest

import experiment_ids as eid
import make_report
import provenance


# ------------------------------------------------------------------ IDs
def test_parse_experiment_id():
    assert eid.parse_experiment_id("H1-E01") == {
        "hypotheses": ["H1"], "group": "H1", "attempt": 1}
    assert eid.parse_experiment_id("H2H3-E12")["hypotheses"] == ["H2", "H3"]
    for bad in ("H1", "H1-E1", "E01", "h1-E01", "H1-E01x"):
        with pytest.raises(ValueError):
            eid.parse_experiment_id(bad)


def test_config_hash_is_order_independent_and_sensitive():
    a = eid.config_hash({"x": 1, "y": [1, 2]})
    assert a == eid.config_hash({"y": [1, 2], "x": 1})
    assert a != eid.config_hash({"x": 2, "y": [1, 2]})
    assert len(a) == 4


def _git(dirty=False, code_dirty=None):
    st = {"available": True, "commit": "a1b2c3d4e5f6", "dirty": dirty}
    if code_dirty is not None:
        st["code_dirty"] = code_dirty
    return {"experiments": st,
            "fastener": {"available": True, "commit": "9f8e7d6c5b4a",
                         "dirty": False, "code_dirty": False}}


def test_algorithm_id_form_and_dirty_suffix():
    cfg = {"init": "sparse"}
    h = eid.config_hash(cfg)
    assert eid.algorithm_id("nsga2_sparse", _git(), cfg) == \
        f"nsga2_sparse@a1b2c3d+9f8e7d6#{h}"
    assert eid.algorithm_id("nsga2", _git(code_dirty=True), cfg).endswith("-dirty")
    # Non-code changes (results, ledger) make the tree dirty but not the code.
    assert not eid.algorithm_id("nsga2", _git(dirty=True, code_dirty=False),
                                cfg).endswith("-dirty")
    missing = {"experiments": {"available": False}, "fastener": {}}
    assert "@nogit+nogit#" in eid.algorithm_id("x", missing, cfg)


# --------------------------------------------------------------- ledger
def test_ledger_issue_add_close(tmp_path):
    led = tmp_path / "EXPERIMENTS.md"
    assert eid.issue("H1", led) == "H1-E01"
    assert eid.issue("H2H3", led) == "H2H3-E01"
    eid.add_run("H1-E01", "20260926T000000Z_a", led)
    eid.add_run("H1-E01", "20260926T010000Z_b", led)
    eid.add_run("H1-E01", "20260926T010000Z_b", led)  # idempotent
    row = eid.find(eid.load_ledger(led), "H1-E01")
    assert row["runs"] == ["20260926T000000Z_a", "20260926T010000Z_b"]
    assert row["status"] == "running"

    eid.set_status("H1-E01", "failed", path=led)
    with pytest.raises(ValueError, match="closed"):
        eid.add_run("H1-E01", "20260926T020000Z_c", led)
    # A closed ID is never reused: the next attempt is E02.
    assert eid.next_experiment_id("H1", led) == "H1-E02"


def test_ledger_keeps_designs_below_the_table(tmp_path):
    led = tmp_path / "EXPERIMENTS.md"
    eid.issue("H1", led)
    designs = ("## Experiment designs\n\n### `H1-E01`\n\n"
               "| `not a ledger row` | a | b | c | d | e |\n|---|---|---|---|---|---|")
    led.write_text(led.read_text(encoding="utf-8") + "\n" + designs + "\n",
                   encoding="utf-8")
    eid.add_run("H1-E01", "r1", led)
    assert [r["experiment"] for r in eid.load_ledger(led)] == ["H1-E01"]
    assert led.read_text(encoding="utf-8").endswith(designs + "\n")


def test_ledger_keeps_notes_above_the_table(tmp_path):
    led = tmp_path / "EXPERIMENTS.md"
    eid.issue("H1", led)
    note = "A note added by hand, with a [link](DATASETS_USED.md)."
    text = led.read_text(encoding="utf-8")
    table = text.index("| experiment |")
    led.write_text(text[:table] + note + "\n\n" + text[table:],
                   encoding="utf-8")
    eid.add_run("H1-E01", "r1", led)
    eid.set_status("H1-E01", "failed", path=led)
    text = led.read_text(encoding="utf-8")
    assert note in text and text.index(note) < text.index("| experiment |")
    assert eid.find(eid.load_ledger(led), "H1-E01")["status"] == "failed"


def test_ledger_refuses_unissued_skip(tmp_path):
    led = tmp_path / "EXPERIMENTS.md"
    with pytest.raises(ValueError, match="never issued"):
        eid.check_open("H1-E03", led)
    eid.check_open("H1-E01", led)  # the next one is fine
    eid.add_run("H1-E01", "r1", led)
    assert eid.find(eid.load_ledger(led), "H1-E01")["runs"] == ["r1"]


def test_set_status_rejects_unknown(tmp_path):
    led = tmp_path / "EXPERIMENTS.md"
    eid.issue("H1", led)
    with pytest.raises(ValueError):
        eid.set_status("H1-E01", "done", path=led)


# -------------------------------------------------------------- Run
def test_run_refuses_dirty_code(tmp_path, monkeypatch):
    dirty = {"available": True, "commit": "a" * 40, "dirty": True,
             "code_dirty": True, "code_dirty_files": [" M x.py"]}
    monkeypatch.setattr(provenance, "git_state", lambda repo, nc=(): dirty)
    led = tmp_path / "EXPERIMENTS.md"
    with pytest.raises(provenance.DirtyTreeError):
        provenance.Run("t", root=tmp_path, experiment_id="H1-E01", ledger=led)
    assert not led.exists()  # nothing recorded for a refused run

    run = provenance.Run("t", root=tmp_path, experiment_id="H1-E01",
                         allow_dirty=True, ledger=led)
    assert run.manifest["experiment_id"] == "H1-E01"
    assert run.manifest["evidence"] is False
    assert run.algorithm_id("nsga2", {"a": 1}).endswith("-dirty")
    assert eid.find(eid.load_ledger(led), "H1-E01")["runs"] == [run.run_id]


def test_run_algorithm_id_conflict(tmp_path, monkeypatch):
    clean = {"available": True, "commit": "b" * 40, "dirty": False,
             "code_dirty": False, "code_dirty_files": []}
    monkeypatch.setattr(provenance, "git_state", lambda repo, nc=(): clean)
    run = provenance.Run("t", root=tmp_path)
    assert run.manifest["evidence"] is False  # no experiment ID
    aid = run.algorithm_id("poss", {"k": 5})
    assert run.algorithm_id("poss", {"k": 5}) == aid
    with pytest.raises(ValueError, match="two configs"):
        run.algorithm_id("poss", {"k": 6})


# --------------------------------------------------------- metrics
def _rec(k, val, test):
    return {"n_features": k, "val_score": val, "test_score": test}


def test_opt_curve_selects_on_validation():
    recs = [_rec(2, 0.5, 0.6), _rec(3, 0.7, 0.4), _rec(5, 0.6, 0.9)]
    # k=1: nothing -> 0. k=2: 0.6. k=3,4: val-best is size 3 -> test 0.4.
    # k=5: size 5 has lower val than size 3, so 0.4 stays.
    assert make_report.opt_curve(recs, 5).tolist() == [0, 0.6, 0.4, 0.4, 0.4]
    assert make_report.auf(recs, 5) == pytest.approx(1.8 / 5)
    # Sizes above K are ignored.
    assert make_report.opt_curve([_rec(20, 1.0, 1.0)], 10).sum() == 0


def test_holm():
    assert make_report.holm([0.01, 0.04, 0.03]) == pytest.approx(
        [0.03, 0.06, 0.06])


def test_section_and_labels():
    text = ("# T\n\n## H1 -- A claim\n\n**Claim.** It holds.\n\n"
            "**Analysis: pairwise.** Test:\n\n* one\n* two\n\n"
            "**Falsification criterion.** 4 of 5.\n\n## H2 -- Next\n\nx\n")
    sec = make_report.section(text, "H1")
    assert sec.startswith("## H1 --") and "H2" not in sec
    lab = make_report.labelled(sec)
    assert lab["Claim"] == "**Claim.** It holds."
    assert "* two" in lab["Analysis: pairwise"]
    assert lab["Falsification criterion"].endswith("4 of 5.")


# ---------------------------------------------------- end to end
def _fake_run(root, run_id, dataset, arms_scores, seeds=range(2020, 2025)):
    d = root / run_id
    d.mkdir(parents=True)
    results = []
    for arm, base in arms_scores.items():
        for i, s in enumerate(seeds):
            recs = [_rec(k, base + 0.01 * k, base + 0.01 * k + 0.001 * i)
                    for k in (2, 5, 9, 30)]
            results.append({"method": arm, "seed": s, "records": recs,
                            "model_fits": 6000, "elapsed_seconds": 12.0,
                            "algorithm_id": f"{arm}@aaaaaaa+bbbbbbb#0000"})
    manifest = {"run_id": run_id, "experiment_id": "H1-E01",
                "started_utc": "2026-09-26T00:00:00+00:00",
                "ended_utc": "2026-09-26T01:00:00+00:00",
                "status": "ok", "evidence": True,
                "command": f"run_sota.py --dataset {dataset}",
                "params": {"dataset": dataset},
                "dataset": {"name": dataset, "n_features": 100, "n_train": 60,
                            "n_val": 20, "n_test": 20},
                "git": {"experiments": {"available": True, "commit": None}},
                "algorithms": {}}
    (d / "manifest.json").write_text(json.dumps(manifest))
    (d / "raw_results.json").write_text(json.dumps(results))


def test_report_end_to_end_h1(tmp_path, monkeypatch):
    monkeypatch.setattr(make_report, "RESULTS_DIR", tmp_path / "results")
    # Sparse ahead everywhere, so the paired rule reads "supported".
    for ds in ("eodata", "satimage"):
        _fake_run(tmp_path / "results", f"R_{ds}", ds,
                  {"nsga2": 0.5, "nsga2_sparse": 0.6})
    out = tmp_path / "report"
    path = make_report.build("H1-E01", ["R_eodata", "R_satimage"], out)
    # REPORT.md: the reading, in three sections.
    assert path.name == "REPORT.md"
    text = path.read_text(encoding="utf-8")
    for heading in ("## 1. In brief", "### The hypothesis", "### The answer",
                    "## 2. Findings", "### F1 -- ", "## 3. Assessment"):
        assert heading in text
    assert "mechanical reading -- H1: supported" in text
    assert "](SUPPORT.md)" in text
    # SUPPORT.md: the record.
    support = (out / "SUPPORT.md").read_text(encoding="utf-8")
    for heading in ("## 1. Header", "## 2. Hypothesis",
                    "## 3. Evaluation criteria",
                    "## 4. Description of the experiment", "## 5. Evidence",
                    "## 6. Reproduction"):
        assert heading in support
    assert "mechanical reading: supported" in support
    assert "**Falsification criterion.**" in support  # quoted verbatim
    assert "## 6. Findings" not in support and "Summary" not in support
    figs = sorted(p.name for p in (out / "figures").iterdir())
    assert figs[0].startswith("F1_H1_criterion_auf10")
    assert len(figs) == 4
    assert any(f.endswith("_front_size_range.png") for f in figs)
    # A second build must not overwrite hand-written prose.
    assert make_report.build("H1-E01", ["R_eodata", "R_satimage"],
                             out).name == "REPORT.skeleton.md"


def test_paired_reading_incomplete_and_negative():
    cells = {"eodata": {"nsga2": {s: 0.5 for s in range(5)},
                        "nsga2_sparse": {s: 0.6 for s in range(5)}}}
    # EOData passes; the other dev sets are missing, so it could still pass.
    assert make_report.evaluate_paired("H1", cells, 10)["reading"] == "incomplete"
    cells["eodata"]["nsga2_sparse"] = {s: 0.4 for s in range(5)}
    assert make_report.evaluate_paired("H1", cells, 10)["reading"] == \
        "not supported"


def _swap_cells(effects, seeds=range(2020, 2025), arm="fastener_swap_random"):
    """dataset -> {fastener, arm} -> seed -> AUF, with the given mean effects."""
    return {ds: {"fastener": {s: 0.5 for s in seeds},
                 arm: {s: 0.5 + e for s in seeds}}
            for ds, e in effects.items()}


def test_dataset_unit_reading_supported_reversed_and_not():
    sets = make_report.SWAP_SETS
    assert len(sets) == 40 and sets[0] == "eodata"
    # Ahead on 30, behind on 10, by unequal amounts: supported.
    eff = {d: (0.01 + 0.001 * i if i < 30 else -0.005 - 0.0001 * i)
           for i, d in enumerate(sets)}
    ev = make_report.evaluate_dataset_unit("H2", _swap_cells(eff), 10)
    assert ev["primary"]["positive"] == 30 and ev["primary"]["negative"] == 10
    assert ev["reading"] == "supported"
    assert ev["per_dataset"]["eodata"]["passes_4_of_5"]
    # The same with signs swapped: reversed.
    ev = make_report.evaluate_dataset_unit(
        "H2", _swap_cells({d: -e for d, e in eff.items()}), 10)
    assert ev["reading"] == "reversed"
    # Evenly split, equal sizes: not supported.
    eff = {d: (0.01 if i % 2 else -0.01) for i, d in enumerate(sets)}
    ev = make_report.evaluate_dataset_unit("H2", _swap_cells(eff), 10)
    assert ev["reading"] == "not supported"


def test_dataset_unit_incomplete_and_ignores_other_seeds():
    sets = make_report.SWAP_SETS
    eff = {d: 0.01 + 0.001 * i for i, d in enumerate(sets)}
    cells = _swap_cells(eff)
    # A calibration run at seed 1999 is not one of the experiment's seeds.
    cells["eodata"]["fastener"][1999] = 0.0
    ev = make_report.evaluate_dataset_unit("H2", cells, 10)
    assert ev["per_dataset"]["eodata"]["seeds"] == 5
    assert ev["reading"] == "supported"
    # Seven datasets short of a seed: more than 6 missing, so incomplete.
    for d in sets[:7]:
        del cells[d]["fastener_swap_random"][2024]
    ev = make_report.evaluate_dataset_unit("H2", cells, 10)
    assert ev["reading"].startswith("incomplete")
    assert len(ev["primary"]["missing"]) == 7


def test_h3_is_also_read_against_the_random_swap():
    sets = make_report.SWAP_SETS
    cells = _swap_cells({d: 0.02 for d in sets}, arm="fastener_swap_guided")
    for d in sets:
        cells[d]["fastener_swap_random"] = {s: 0.52 for s in range(2020, 2025)}
    ev = make_report.evaluate_dataset_unit("H3", cells, 10)
    assert ev["challenger"] == "fastener_swap_guided"
    gv = ev["secondary"]["guided_vs_random"]
    assert gv["n_datasets"] == 40 and gv["zero"] == 40
    assert gv["reading"] == "not supported"


def test_report_end_to_end_h2h3(tmp_path, monkeypatch):
    monkeypatch.setattr(make_report, "RESULTS_DIR", tmp_path / "results")
    for ds in ("eodata", "Coffee", "Wafer"):
        _fake_run(tmp_path / "results", f"R_{ds}", ds,
                  {"fastener": 0.5, "fastener_swap_random": 0.55,
                   "fastener_swap_guided": 0.6})
    out = tmp_path / "report"
    make_report.build("H2H3-E01", ["R_eodata", "R_Coffee", "R_Wafer"], out)
    support = (out / "SUPPORT.md").read_text(encoding="utf-8")
    # 37 of 40 datasets missing: incomplete, for both hypotheses (each reading
    # appears under the criteria and again under the evidence).
    assert support.count("mechanical reading: incomplete") == 4
    assert "mechanical reading: supported" not in support
    assert "Secondary, EOData on its own" in support
    assert "fastener_swap_guided minus fastener_swap_random" in support
    figs = sorted(p.name for p in (out / "figures").iterdir())
    assert figs[0] == "F1_H2_effect_per_dataset.png"
    assert "F2_H3_effect_per_dataset.png" in figs
    assert (out / "tables" / "H2_by_cluster.csv").is_file()


def test_pairwise_reading():
    rng = np.random.default_rng(0)
    cells = {f"d{i}": {"fs_sds": {0: 0.6 + rng.uniform(0, .05)},
                       "fastener": {0: 0.5}} for i in range(25)}
    ev = make_report.evaluate_pairwise("H4", cells, 20)
    assert ev["reading"] == "supported"
    assert ev["pairs"][0]["wins"] == 25


def test_concurrent_add_run_loses_no_run(tmp_path):
    """Runs started side by side all land in the ledger (H0-E02 lost one)."""
    import multiprocessing as mp
    led = tmp_path / "EXPERIMENTS.md"
    xid = eid.issue("H9", led)
    run_ids = [f"20260926T0000{i:02d}Z_r{i}" for i in range(12)]
    with mp.Pool(6) as pool:
        pool.starmap(eid.add_run, [(xid, r, led) for r in run_ids])
    row = eid.find(eid.load_ledger(led), xid)
    assert sorted(row["runs"]) == sorted(run_ids)
    assert not (tmp_path / "EXPERIMENTS.md.lock").exists()


def test_stale_ledger_lock_is_removed(tmp_path):
    import os
    import time
    led = tmp_path / "EXPERIMENTS.md"
    lock = tmp_path / "EXPERIMENTS.md.lock"
    lock.write_text("12345")
    old = time.time() - 600
    os.utime(lock, (old, old))
    assert eid.issue("H9", led) == "H9-E01"
    assert not lock.exists()
