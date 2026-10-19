"""Generate the report skeleton for one experiment (see METHODOLOGY.md).

Reads every run of the experiment from `results/<run ID>/`, and writes to
`experiments/reports/<experiment ID>/`:

* `REPORT.md` -- the reading, in three sections: in brief (the hypothesis, its
  criterion and the answer, in plain words, with the criterion figure); the
  findings F1..FN, one at a time, each with its figure; and an assessment of
  the hypothesis written as for a paper. A skeleton, with TODO markers where
  the prose is to be written by hand;
* `SUPPORT.md` -- the record: header, the hypothesis and criteria quoted
  verbatim from HYPOTHESES.md at the pre-registration commit, the run facts,
  the per-seed tables, a mechanical reading of the falsification criterion and
  the reproduction commands;
* `figures/F<n>_*.png` -- the candidate figures for the findings;
* `tables/*.csv` -- the numbers behind the tables and figures.

An existing REPORT.md or SUPPORT.md is never overwritten, since it holds
hand-written prose; the new skeleton goes to REPORT.skeleton.md or
SUPPORT.skeleton.md instead (unless --force). Figures and tables are always
regenerated: they are a function of the runs.

Usage:
    python experiments/make_report.py --experiment H1-E01
    python experiments/make_report.py --experiment H1-E01 --runs <run ID> ...
"""
import argparse
import csv
import json
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis  # noqa: E402
import datasets  # noqa: E402
import experiment_ids  # noqa: E402
import h0_convergence  # noqa: E402
import run_h0  # noqa: E402
import trajectory as trajectory_io  # noqa: E402
from provenance import REPO_ROOT, RESULTS_DIR  # noqa: E402

HYPOTHESES_PATH = "experiments/HYPOTHESES.md"
DEV_SETS = ("eodata", "crop_mapping", "madelon", "gina")
PRIMARY_DEV_SET = "eodata"
# H1's own datasets, by feature count (HYPOTHESES.md, Revisions, 2026-10-07).
H1_SETS = ("satimage", "eodata", "USPS", "har", "COIL20", "gisette",
           "Prostate_GE", "arcene")

# H1: the pre-registered paired rule -- the challenger beats the baseline on
# AUF in at least 4 of 5 seeds, on EOData and on at least one other of the
# hypothesis's datasets.
PAIRED = {
    "H1": ("nsga2_sparse", "nsga2"),
}
PAIRED_SETS = {"H1": H1_SETS}
PAIRED_MIN_WINS = 4
PAIRED_SEEDS = 5
# H2, H3: datasets as the unit (HYPOTHESES.md, Revisions, 2026-10-09; DEC-33).
# Per dataset, the mean over the 5 seeds of challenger minus baseline AUF;
# supported if positive on more datasets than negative and a two-sided
# Wilcoxon over them is significant.
DATASET_UNIT = {
    "H2": ("fastener_swap_random", "fastener"),
    "H3": ("fastener_swap_guided", "fastener"),
}
# EOData and the UCR/UEA sets by cluster, less DuckDuckGeese (DEC-34).
SWAP_EXCLUDED = ("DuckDuckGeese",)
SWAP_CLUSTERS = {"eodata": "EO",
                 **{d: c for d, c in datasets.TSC_DATASETS.items()
                    if d not in SWAP_EXCLUDED}}
SWAP_SETS = tuple(SWAP_CLUSTERS)
SWAP_SEEDS = (2020, 2021, 2022, 2023, 2024)
SWAP_MAX_MISSING = 6
# H3 is read against the random swap too: the guidance is credited only where
# the guided arm also beats it.
GUIDANCE = ("fastener_swap_guided", "fastener_swap_random")
SWAP_STATS = ("swap_proposed", "swap_fits", "swap_kept")
# H4-H6: per-dataset mean AUF, focal arm against each opponent across datasets.
PAIRWISE = {
    "H4": {"focal": "fs_sds", "opponents": ("fastener",), "n_datasets": 25},
    # 39 since the revision of 2026-10-12, before any run (DEC-40).
    "H5": {"focal": "fastener", "opponents": None, "n_datasets": 39},
    "H6": {"focal": "fastener_swap_guided", "opponents": None, "n_datasets": 39},
}
# H4's arms differ by experiment: H4-E01 drives both searches with the tree,
# H4-E02 with the ELM (DEC-38). Read from the runs, so the reading follows
# what was run. (focal, opponent, classifier)
H4_ARMS = (("fs_sds", "fastener", "tree"),
           ("fs_sds_elm", "fastener_elm", "elm"))
# The 2 x 2 is read only between experiments run at the same budget: H4-E01
# (tree) and H4-E02 (ELM), both at equal CPU time. H4-E03 runs at equal fits
# and is not paired with either.
H4_PAIRED = {"H4-E01": "H4-E02", "H4-E02": "H4-E01"}
# The same arms under another budget unit: H4-E03 (equal fits) is read beside
# H4-E01 (equal CPU time), descriptively.
H4_BUDGET_PAIR = {"H4-E03": "H4-E01"}
# The 2 x 2 of H4-E01 and H4-E02: method -> classifier -> arm label.
H4_CELLS = {"FASTENER": {"tree": "fastener", "elm": "fastener_elm"},
            "FS-SDS": {"tree": "fs_sds", "elm": "fs_sds_elm"}}
ALPHA = 0.05
# H0: fits to a common validation target, per seed (h0_convergence applies the
# rule). Baseline first, as in PAIRED's figures.
H0_ARMS = (h0_convergence.ORIGINAL, h0_convergence.FIXED)
# Secondary measures, fixed minus 2020 per seed: (column, label, relative).
# Relative where the scale differs between datasets.
H0_SECONDARY = (("area", "area under val. curve", False),
                ("test_auf10", "test AUF (K = 10)", False),
                ("test_auf20", "test AUF (K = 20)", False),
                ("hypervolume", "hypervolume, % change", True),
                ("generations", "generations, % change", True),
                ("seconds", "wall clock, % change", True))
# No subset of size <= 10, so no AUF(K=10); a reference line only (H5).
REFERENCE_ONLY = ("all_features",)
# H5, H6: the arms the opt(k), front-size and cost figures show -- the two
# focal FASTENER arms, the closest search rival, and the two OBL-started
# searches whose fronts mostly stay above k = 10.
FIELD_ARMS = ("fastener", "fastener_swap_guided", "nsga2_sparse", "nsga2",
              "nsgaii_miip")
# Cells an experiment left out on purpose (run_queue.py --skip @file).
SKIP_FILES = {"H5H6-E01": "experiments/h5h6_skip.txt"}
# run_queue.py's labels for the FASTENER arms, as the runs name the method.
QUEUE_ARMS = {"fastener_none": "fastener",
              "fastener_guided": "fastener_swap_guided",
              "fastener_random": "fastener_swap_random"}

# Reference categorical palette, fixed order (dataviz skill, light mode).
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300",
          "#4a3aa7", "#e34948")
INK, INK_2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

TODO = "<!-- TODO: {} -->"


# ------------------------------------------------------------ inputs
def git(*args: str) -> Optional[str]:
    # UTF-8 explicitly: the Windows default code page mangles non-ASCII text
    # from `git show`, which then never matches the working tree.
    out = subprocess.run(["git", *args], cwd=str(REPO_ROOT),
                         capture_output=True, encoding="utf-8")
    return out.stdout if out.returncode == 0 else None


def load_run(run_id: str) -> Dict[str, Any]:
    d = RESULTS_DIR / run_id
    manifest = json.loads((d / "manifest.json").read_text(encoding="utf-8")) \
        if (d / "manifest.json").is_file() else None
    results, source = [], None
    for name in ("raw_results.json", "raw_results_partial.json"):
        if (d / name).is_file():
            results = json.loads((d / name).read_text(encoding="utf-8"))
            source = name
            break
    return {"run_id": run_id, "dir": d, "manifest": manifest,
            "results": results, "results_source": source}


def units_of(runs: Sequence[Dict]) -> Tuple[List[Dict], List[str]]:
    """One unit per run key (run, arm, dataset, seed). Duplicates are reported."""
    units, seen, notes = [], {}, []
    for run in runs:
        m = run["manifest"] or {}
        ds = (m.get("params") or {}).get("dataset", "?")
        n_features = (m.get("dataset") or {}).get("n_features")
        for res in run["results"]:
            u = {
                "run_id": run["run_id"], "dataset": ds, "n_features": n_features,
                "method": res["method"], "seed": res.get("seed"),
                "algorithm_id": res.get("algorithm_id")
                or (m.get("algorithms", {}).get(res["method"], {}).get("id")),
                "model_fits": res.get("model_fits"),
                "seconds": res.get("elapsed_seconds", res.get("search_seconds")),
                # Process CPU time of the search, where the run recorded it:
                # the unit of an equal-compute budget (H4).
                "cpu_seconds": res.get("search_cpu_seconds"),
                "stopped_on": res.get("stopped_on"),
                "iterations": res.get("iterations",
                                      res.get("rounds_completed")),
                "records": res.get("records", []),
                # FASTENER only: what the pruning step did (H2, H3).
                "prune_stats": res.get("prune_stats"),
                "front_from_swap": res.get("front_from_swap"),
                "n_rows": sum((m.get("dataset") or {}).get(k) or 0
                              for k in ("n_train", "n_val", "n_test")) or None,
            }
            key = (ds, u["method"], u["seed"])
            if key in seen:
                notes.append(f"duplicate run key {ds}/{u['method']}/s{u['seed']}"
                             f" in `{seen[key]}` and `{run['run_id']}`; "
                             f"the first is used")
                continue
            seen[key] = run["run_id"]
            units.append(u)
    return units, notes


# ---------------------------------------------------------- metrics
def opt_curve(records: Sequence[Dict], K: int) -> np.ndarray:
    """opt(k), k = 1..K: test F1 of the val-best subset of size <= k.

    As HYPOTHESES.md defines it: the subset is chosen on validation, the score
    read on test. A k below the smallest subset on the front scores 0 -- the
    method offers nothing at that budget (same rule as paper_protocol).
    """
    best_val, best_test, out = -np.inf, 0.0, np.zeros(K)
    by_size: Dict[int, Dict] = {}
    for r in records:
        s = int(r["n_features"])
        if s <= K and (s not in by_size
                       or r["val_score"] > by_size[s]["val_score"]):
            by_size[s] = r
    for k in range(1, K + 1):
        r = by_size.get(k)
        if r is not None and r["val_score"] > best_val:
            best_val, best_test = r["val_score"], r["test_score"]
        out[k - 1] = best_test
    return out


def auf(records: Sequence[Dict], K: int) -> float:
    return float(opt_curve(records, K).mean())


def min_size(records: Sequence[Dict]) -> Optional[int]:
    return min((int(r["n_features"]) for r in records), default=None)


def holm(pvalues: Sequence[float]) -> List[float]:
    """Holm step-down adjusted p-values, in the input order."""
    p = np.asarray(pvalues, dtype=float)
    order = np.argsort(p)
    adj, running = np.empty_like(p), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        adj[i] = running
    return adj.tolist()


def wilcoxon_p(diffs: Sequence[float]) -> float:
    from scipy.stats import wilcoxon
    d = [x for x in diffs if x != 0]
    if len(d) < 1:
        return 1.0
    return float(wilcoxon(d).pvalue)


# ------------------------------------------------------ hypotheses
def hypotheses_text(commit: Optional[str]) -> Tuple[str, str]:
    """HYPOTHESES.md at `commit` (else the working tree), and what was read."""
    if commit:
        text = git("show", f"{commit}:{HYPOTHESES_PATH}")
        if text is not None:
            return text, f"`{commit[:7]}`"
    return (REPO_ROOT / HYPOTHESES_PATH).read_text(encoding="utf-8"), \
        "the working tree (no run commit available)"


def section(text: str, hid: str) -> Optional[str]:
    m = re.search(rf"^## {hid} -- .*?(?=^## |^---\s*$|\Z)", text,
                  flags=re.M | re.S)
    return m.group(0).strip() if m else None


def labelled(sec: str) -> Dict[str, str]:
    """`**Label.** text` paragraphs, with following unlabelled ones attached."""
    out: Dict[str, str] = {}
    current = None
    for para in re.split(r"\n\s*\n", sec):
        m = re.match(r"\*\*(.+?)\.\*\*", para.strip())
        if m:
            current = m.group(1)
            out[current] = para.strip()
        elif current is not None:
            out[current] += "\n\n" + para.strip()
    return out


def revisions(text: str) -> Optional[str]:
    m = re.search(r"^## [^\n]*[Rr]evision.*?(?=^## |\Z)", text,
                  flags=re.M | re.S)
    return m.group(0).strip() if m else None


def quote(text: str) -> str:
    return "\n".join("> " + line if line else ">" for line in text.splitlines())


def primary_k(sec: str) -> int:
    m = re.search(r"AUF, K = (\d+)", sec)
    return int(m.group(1)) if m else 10


# -------------------------------------------------------- criteria
def by_cell(units: Sequence[Dict], K: int) -> Dict[str, Dict[str, Dict]]:
    """dataset -> method -> seed -> AUF(K)."""
    out: Dict[str, Dict[str, Dict]] = defaultdict(lambda: defaultdict(dict))
    for u in units:
        if u["records"]:
            out[u["dataset"]][u["method"]][u["seed"]] = auf(u["records"], K)
    return out


def evaluate_paired(hid: str, cells, K: int) -> Dict[str, Any]:
    a, b = PAIRED[hid]
    sets = PAIRED_SETS[hid]
    rows, passed, complete = [], {}, {}
    for ds in sets:
        sa, sb = cells.get(ds, {}).get(a, {}), cells.get(ds, {}).get(b, {})
        seeds = sorted(set(sa) & set(sb))
        wins = sum(sa[s] > sb[s] for s in seeds)
        passed[ds] = wins >= PAIRED_MIN_WINS
        complete[ds] = len(seeds) >= PAIRED_SEEDS
        for s in seeds:
            rows.append({"dataset": ds, "seed": s, a: sa[s], b: sb[s],
                         "delta": sa[s] - sb[s], "win": sa[s] > sb[s]})
    others = [d for d in sets if d != PRIMARY_DEV_SET]
    # A dataset with missing seeds could still pass once they are in.
    could = {d: passed[d] or not complete[d] for d in sets}
    if passed[PRIMARY_DEV_SET] and any(passed[d] for d in others):
        reading = "supported"
    elif could[PRIMARY_DEV_SET] and any(could[d] for d in others):
        reading = "incomplete"
    else:
        reading = "not supported"
    per_ds = [{"dataset": ds,
               "seeds": len([r for r in rows if r["dataset"] == ds]),
               "wins": sum(r["win"] for r in rows if r["dataset"] == ds),
               "passes": passed[ds]} for ds in sets]
    return {"kind": "paired", "challenger": a, "baseline": b, "K": K,
            "datasets": list(sets),
            "rows": rows, "per_dataset": per_ds, "reading": reading}


def dataset_effects(cells, a: str, b: str, sets: Sequence[str],
                    seeds: Sequence[int] = SWAP_SEEDS) -> Dict[str, Dict]:
    """Per dataset: mean over common seeds of AUF(a) - AUF(b), and counts.

    Only the experiment's seeds count, so a calibration run at another seed
    can never enter. A dataset is complete with every seed for both arms.
    """
    out = {}
    for ds in sets:
        sa, sb = cells.get(ds, {}).get(a, {}), cells.get(ds, {}).get(b, {})
        common = [s for s in seeds if s in sa and s in sb]
        deltas = [sa[s] - sb[s] for s in common]
        out[ds] = {"seeds": len(common), "complete": len(common) == len(seeds),
                   "effect": float(np.mean(deltas)) if deltas else None,
                   "wins": sum(d > 0 for d in deltas),
                   f"auf_{a}": float(np.mean([sa[s] for s in common]))
                   if common else None,
                   f"auf_{b}": float(np.mean([sb[s] for s in common]))
                   if common else None,
                   "deltas": dict(zip(common, deltas))}
    return out


def unit_test(per_ds: Dict[str, Dict], max_missing: int) -> Dict[str, Any]:
    """The datasets-as-unit rule over complete datasets."""
    used = {d: v["effect"] for d, v in per_ds.items() if v["complete"]}
    missing = sorted(d for d, v in per_ds.items() if not v["complete"])
    effects = list(used.values())
    pos = sum(e > 0 for e in effects)
    neg = sum(e < 0 for e in effects)
    p = wilcoxon_p(effects) if effects else None
    if len(missing) > max_missing:
        reading = (f"incomplete ({len(missing)} of {len(per_ds)} datasets "
                   f"missing; at most {max_missing} allowed)")
    elif p is not None and p < ALPHA and pos > neg:
        reading = "supported"
    elif p is not None and p < ALPHA and neg > pos:
        reading = "reversed"
    else:
        reading = "not supported"
    return {"n_datasets": len(effects), "positive": pos, "negative": neg,
            "zero": len(effects) - pos - neg, "p_value": p,
            "median_effect": float(np.median(effects)) if effects else None,
            "mean_effect": float(np.mean(effects)) if effects else None,
            "missing": missing, "reading": reading}


def swap_activity(units: Sequence[Dict], methods: Sequence[str],
                  seeds: Sequence[int] = SWAP_SEEDS) -> List[Dict]:
    """Per dataset and arm, the pruning counters averaged over seeds."""
    acc: Dict[Tuple[str, str], List[Dict]] = defaultdict(list)
    for u in units:
        if u["method"] in methods and u["seed"] in seeds and u["prune_stats"]:
            acc[(u["dataset"], u["method"])].append(u)
    rows = []
    for (ds, m), us in sorted(acc.items()):
        row = {"dataset": ds, "method": m, "seeds": len(us)}
        for k in SWAP_STATS + ("pruned_items",):
            row[k] = float(np.mean([u["prune_stats"].get(k, 0) for u in us]))
        row["front_from_swap"] = float(np.mean(
            [u["front_from_swap"] or 0 for u in us]))
        row["share_of_fits_on_swaps"] = float(np.mean(
            [u["prune_stats"].get("swap_fits", 0) / u["model_fits"]
             for u in us if u["model_fits"]])) if us else None
        rows.append(row)
    return rows


def evaluate_dataset_unit(hid: str, cells, K: int,
                          units: Sequence[Dict] = ()) -> Dict[str, Any]:
    a, b = DATASET_UNIT[hid]
    per_ds = dataset_effects(cells, a, b, SWAP_SETS)
    primary = unit_test(per_ds, SWAP_MAX_MISSING)
    shape = {}
    for u in units:
        shape.setdefault(u["dataset"], {"p": u["n_features"], "n": u["n_rows"]})
    for ds, v in per_ds.items():
        v["cluster"] = SWAP_CLUSTERS[ds]
        v["p"] = shape.get(ds, {}).get("p")
        v["n"] = shape.get(ds, {}).get("n")
        v["passes_4_of_5"] = v["wins"] >= PAIRED_MIN_WINS
    by_cluster = {}
    for c in dict.fromkeys(SWAP_CLUSTERS.values()):
        es = [v["effect"] for v in per_ds.values()
              if v["cluster"] == c and v["complete"]]
        by_cluster[c] = {"n": len(es),
                         "mean_effect": float(np.mean(es)) if es else None,
                         "positive": sum(e > 0 for e in es),
                         "negative": sum(e < 0 for e in es)}
    secondary = {"eodata": per_ds["eodata"], "by_cluster": by_cluster,
                 "swap_activity": swap_activity(units, (a, b))}
    if hid == "H3":
        g = dataset_effects(cells, *GUIDANCE, SWAP_SETS)
        secondary["guided_vs_random"] = {
            **unit_test(g, SWAP_MAX_MISSING),
            "per_dataset": {d: v["effect"] for d, v in g.items()}}
    rows = [{"dataset": ds, "cluster": v["cluster"], "seed": s, "delta": dlt}
            for ds, v in per_ds.items() for s, dlt in v["deltas"].items()]
    order = sorted((d for d in per_ds if per_ds[d]["effect"] is not None),
                   key=lambda d: (SWAP_CLUSTERS[d], -per_ds[d]["effect"]))
    return {"kind": "dataset_unit", "challenger": a, "baseline": b, "K": K,
            "datasets": order, "per_dataset": per_ds, "rows": rows,
            "primary": primary, "secondary": secondary,
            "reading": primary["reading"]}


def table3_comparison(cells, units: Sequence[Dict],
                      arms: Tuple[str, str] = ("fs_sds", "fastener")
                      ) -> Dict[str, Any]:
    """Our per-dataset AUF (K = 20) beside the paper's Table 3 (H4 secondary).

    `cells` must be read at K = 20, the paper's aggregate. eval_n is our mean
    number of fits per run, where the paper's is its evaluation count.
    """
    import paper_tables
    fits = defaultdict(list)
    for u in units:
        if u["model_fits"] is not None:
            fits[(u["dataset"], u["method"])].append(u["model_fits"])
    rows = []
    for ds, meths in cells.items():
        for m in arms:
            v = list(meths.get(m, {}).values())
            # FASTENER on any classifier is set beside the paper's FASTENER
            # row; fs_sds_elm is the paper's own FS-SDS setting and
            # paper_tables compares it with the FS-SDS row by that name.
            name = "fastener" if m.startswith("fastener") else m
            if v:
                rows.append({"dataset": ds, "method": name,
                             "mean": float(np.mean(v)),
                             "max": float(np.max(v)),
                             "median": float(np.median(v)),
                             "sd": float(np.std(v)),
                             "eval_n": float(np.mean(fits[(ds, m)]))
                             if fits[(ds, m)] else None})
    return paper_tables.compare(rows)


def compute_per_arm(units: Sequence[Dict], methods: Sequence[str]
                    ) -> List[Dict]:
    """Per dataset and arm: mean fits, CPU seconds and wall clock per run."""
    acc = defaultdict(list)
    for u in units:
        if u["method"] in methods:
            acc[(u["dataset"], u["method"])].append(u)
    out = []
    for (ds, m), us in sorted(acc.items()):
        def mean(key):
            v = [u[key] for u in us if u.get(key) is not None]
            return float(np.mean(v)) if v else None
        out.append({"dataset": ds, "method": m, "runs": len(us),
                    "fits": mean("model_fits"), "cpu_seconds": mean("cpu_seconds"),
                    "wall_seconds": mean("seconds"),
                    "stopped_on": sorted({str(u["stopped_on"]) for u in us})})
    return out


def h4_arms(units: Sequence[Dict]):
    """The (focal, opponent, classifier) of the H4 arms these runs hold."""
    methods = {u["method"] for u in units}
    for arms in H4_ARMS:
        if arms[0] in methods or arms[1] in methods:
            return arms
    return H4_ARMS[0]


def h4_two_by_two(experiment_id: str, cells, K: int) -> Optional[Dict]:
    """Per dataset, mean AUF of every H4 cell (method x classifier) that the
    reported H4 experiments hold, this one's runs included.

    The other H4 experiments' runs are read from the ledger, so the table is
    complete only once both H4-E01 (tree) and H4-E02 (ELM) have run. None if
    only one classifier is available.
    """
    all_cells = {ds: dict(m) for ds, m in cells.items()}
    partner = H4_PAIRED.get(experiment_id)
    for row in experiment_ids.load_ledger():
        if row["experiment"] != partner \
                or row["status"] not in ("reported", "running"):
            continue
        runs = [load_run(r) for r in row["runs"]
                if (RESULTS_DIR / r).is_dir()]
        other = by_cell(units_of(runs)[0], K)
        for ds, meths in other.items():
            for m, seeds in meths.items():
                all_cells.setdefault(ds, {}).setdefault(m, seeds)
    labels = [lab for cl in H4_CELLS.values() for lab in cl.values()]
    have = {m for meths in all_cells.values() for m in meths}
    if not all(lab in have for lab in labels):
        return None
    per_ds = {}
    for ds, meths in sorted(all_cells.items()):
        if all(meths.get(lab) for lab in labels):
            per_ds[ds] = {lab: float(np.mean(list(meths[lab].values())))
                          for lab in labels}
    effects = {}
    for meth, cl in H4_CELLS.items():
        d = [per_ds[ds][cl["elm"]] - per_ds[ds][cl["tree"]] for ds in per_ds]
        effects[f"{meth}: ELM minus tree"] = d
    for clf in ("tree", "elm"):
        d = [per_ds[ds][H4_CELLS["FS-SDS"][clf]]
             - per_ds[ds][H4_CELLS["FASTENER"][clf]] for ds in per_ds]
        effects[f"{clf}: FS-SDS minus FASTENER"] = d
    summary = {k: {"n": len(v), "positive": sum(x > 0 for x in v),
                   "negative": sum(x < 0 for x in v),
                   "mean": float(np.mean(v)), "median": float(np.median(v)),
                   "p": wilcoxon_p(v)} for k, v in effects.items()}
    return {"per_dataset": per_ds, "summary": summary,
            "means": {lab: float(np.mean([v[lab] for v in per_ds.values()]))
                      for lab in labels}}


def h4_budget_compare(experiment_id: str, cells, units: Sequence[Dict],
                      K: int) -> Optional[Dict]:
    """Per dataset and arm: mean AUF and fits here and in the paired
    experiment run under another budget unit (H4_BUDGET_PAIR)."""
    partner = H4_BUDGET_PAIR.get(experiment_id)
    row = experiment_ids.find(experiment_ids.load_ledger(), partner) \
        if partner else None
    if row is None:
        return None
    runs = [load_run(r) for r in row["runs"] if (RESULTS_DIR / r).is_dir()]
    other_units = units_of(runs)[0]
    other = by_cell(other_units, K)

    def fits_of(us):
        acc = defaultdict(list)
        for u in us:
            acc[(u["dataset"], u["method"])].append(u["model_fits"])
        return {k: float(np.mean(v)) for k, v in acc.items()}
    f_here, f_other = fits_of(units), fits_of(other_units)
    per_ds = {}
    for ds, meths in cells.items():
        for m, seeds in meths.items():
            o = other.get(ds, {}).get(m)
            if seeds and o:
                per_ds.setdefault(ds, {})[m] = {
                    "here": float(np.mean(list(seeds.values()))),
                    "other": float(np.mean(list(o.values()))),
                    "fits_here": f_here.get((ds, m)),
                    "fits_other": f_other.get((ds, m))}
    return {"partner": partner, "per_dataset": per_ds}


def evaluate_pairwise(hid: str, cells, K: int,
                      arms: Optional[Tuple[str, str]] = None) -> Dict[str, Any]:
    spec = dict(PAIRWISE[hid])
    if arms is not None:
        spec["focal"], spec["opponents"] = arms[0], (arms[1],)
    focal = spec["focal"]
    means = {ds: {m: float(np.mean(list(s.values())))
                  for m, s in meths.items() if s}
             for ds, meths in cells.items()}
    opponents = spec["opponents"] or sorted(
        {m for d in means.values() for m in d} - {focal} - set(REFERENCE_ONLY))
    pairs = []
    for opp in opponents:
        ds_both = sorted(d for d in means if focal in means[d]
                         and opp in means[d])
        diffs = [means[d][focal] - means[d][opp] for d in ds_both]
        pairs.append({
            "opponent": opp, "n_datasets": len(ds_both),
            "wins": sum(x > 0 for x in diffs), "ties": sum(x == 0 for x in diffs),
            "losses": sum(x < 0 for x in diffs),
            "mean_delta": float(np.mean(diffs)) if diffs else float("nan"),
            "p": wilcoxon_p(diffs) if diffs else float("nan"),
            "diffs": dict(zip(ds_both, diffs)),
        })
    ps = [p["p"] for p in pairs if not np.isnan(p["p"])]
    adj = iter(holm(ps)) if ps else iter(())
    for p in pairs:
        p["p_holm"] = next(adj) if not np.isnan(p["p"]) else float("nan")
        p["significant"] = p["p_holm"] < ALPHA

    n_seen = len(means)
    complete = n_seen >= spec["n_datasets"]
    if hid == "H4":
        p = pairs[0] if pairs else None
        if p is None or not p["n_datasets"]:
            reading = "incomplete"
        elif p["wins"] > p["losses"] and p["significant"] and p["mean_delta"] > 0:
            reading = "supported"
        elif p["significant"] and p["mean_delta"] < 0:
            reading = "refuted (published ordering reproduces)"
        else:
            reading = "not significant either way (methods comparable)"
    else:
        ok = pairs and all(p["wins"] > p["losses"] and p["significant"]
                           and p["mean_delta"] > 0 for p in pairs)
        reading = "supported" if ok else "not supported"
    if not complete and not reading.startswith("incomplete"):
        reading += f" (on {n_seen} of {spec['n_datasets']} datasets -- incomplete)"
    return {"kind": "pairwise", "focal": focal, "K": K, "pairs": pairs,
            "means": means, "reading": reading}


def evaluate_h0(runs: Sequence[Dict]) -> Dict[str, Any]:
    """H0's rule, applied by h0_convergence to every run with trajectories.

    Also returns each run key's validation curve and each dataset's budget, for
    the progress figure. A run without a manifest (killed before it wrote one)
    cannot be read and is left out; the header lists it.
    """
    dirs = [r["dir"] for r in runs
            if r["manifest"] and (r["dir"] / "trajectories").is_dir()]
    summary = h0_convergence.summarise(dirs)
    curves: Dict[Tuple[str, str, int], list] = {}
    budgets: Dict[str, int] = {}
    for r in runs:
        if r["dir"] not in dirs:
            continue
        params = r["manifest"]["params"]
        ds = params["dataset"]
        budgets[ds] = int(params["evaluation_budget_per_seed"])
        for seed in params["seeds"]:
            for arm in H0_ARMS:
                p = r["dir"] / "trajectories" / f"{arm}_seed{seed}.jsonl"
                if p.is_file():
                    curves[(ds, arm, seed)] = h0_convergence.curve(
                        trajectory_io.read(p), h0_convergence.K)
    # The required dataset first: the criterion hinges on it.
    order = sorted(summary["per_dataset"],
                   key=lambda d: (d != h0_convergence.REQUIRED_DATASET, d))
    return {"kind": "h0", "K": h0_convergence.K, "rows": summary["per_seed"],
            "per_dataset": summary["per_dataset"], "datasets": order,
            "curves": curves, "budgets": budgets,
            "reading": summary["verdict"]}


# --------------------------------------------------------- figures
# The designs of H0-E02 and H0-E03, each with its own rule, both with datasets
# as the unit. They are quoted from HYPOTHESES.md at the experiment's
# pre-registration commit, where they were subsections with these titles; from
# 2026-10-07 they live in EXPERIMENTS.md, *Experiment designs*.
H0_EXT_TITLE = "H0 on every other dataset"
H0_REPEAT_TITLE = "H0 repeated with the top genes kept"


def subsection(text: str, title: str) -> Optional[str]:
    m = re.search(rf"^### {re.escape(title)}.*?(?=^## |^### |^---\s*$|\Z)",
                  text, flags=re.M | re.S)
    return m.group(0).strip() if m else None


def is_h0_extension(runs: Sequence[Dict]) -> bool:
    """True when every run is on a dataset of H0's second experiment."""
    ext = {p["dataset"] for p in run_h0.H0_EXTENSION_PLAN}
    ds = {(r["manifest"] or {}).get("params", {}).get("dataset")
          for r in runs if r["manifest"]}
    return bool(ds) and ds <= ext


def is_h0_repeat(runs: Sequence[Dict]) -> bool:
    """True when the runs span H0-E01's and H0-E02's datasets: H0-E03."""
    core = {p["dataset"] for p in run_h0.H0_PLAN}
    ext = {p["dataset"] for p in run_h0.H0_EXTENSION_PLAN}
    ds = {(r["manifest"] or {}).get("params", {}).get("dataset")
          for r in runs if r["manifest"]}
    return bool(ds & core) and bool(ds & ext)


def finished_dirs(experiment_id: str) -> List[Path]:
    """Run directories of an experiment, from the ledger, that finished."""
    row = experiment_ids.find(experiment_ids.load_ledger(), experiment_id)
    out = []
    for rid in (row or {}).get("runs", []):
        d = RESULTS_DIR / rid
        m = d / "manifest.json"
        if m.is_file() and json.loads(m.read_text(encoding="utf-8")).get(
                "status") == "ok":
            out.append(d)
    return out


def best_final_f1(run_dir: Path) -> Dict[str, float]:
    """Per arm, the mean over seeds of the test weighted F1 of the subset with
    the best validation score on the final front (the smaller on a tie)."""
    path = run_dir / "raw_results.json"
    if not path.is_file():
        return {}
    out: Dict[str, List[float]] = defaultdict(list)
    for res in json.loads(path.read_text(encoding="utf-8")):
        recs = res.get("records") or []
        if res.get("method") in H0_ARMS and recs:
            r = max(recs, key=lambda r: (r["val_score"], -r["n_features"]))
            out[res["method"]].append(r["test"]["f1_weighted"])
    return {m: float(np.mean(v)) for m, v in out.items()}


def evaluate_h0_extension(runs: Sequence[Dict],
                          repeat: bool = False) -> Dict[str, Any]:
    """The rule of H0-E02, or with `repeat` of H0-E03, by h0_convergence.

    H0-E02: H0-E01's finished runs feed only the secondary test over all
    datasets. H0-E03: every dataset's effect in H0-E01 or H0-E02 is set beside
    its effect here, as a comparison across experiments, not a test.
    """
    dirs = [r["dir"] for r in runs
            if r["manifest"] and (r["dir"] / "trajectories").is_dir()]
    if repeat:
        plan, earlier = run_h0.H0_REPEAT_PLAN, []
        max_missing = run_h0.REPEAT_MAX_MISSING
    else:
        plan, earlier = run_h0.H0_EXTENSION_PLAN, finished_dirs("H0-E01")
        max_missing = h0_convergence.EXTENSION_MAX_MISSING
    s = h0_convergence.extension_summary(
        dirs, expected=[p["dataset"] for p in plan],
        groups={p["dataset"]: p["group"] for p in plan},
        earlier_run_dirs=earlier, max_missing=max_missing)
    for d in dirs:
        ds = json.loads((d / "manifest.json").read_text(
            encoding="utf-8"))["params"]["dataset"]
        f1 = best_final_f1(d)
        if ds in s["per_dataset"]:
            s["per_dataset"][ds]["best_f1_fixed"] = f1.get(h0_convergence.FIXED)
            s["per_dataset"][ds]["best_f1_2020"] = f1.get(
                h0_convergence.ORIGINAL)
    if repeat:
        prior = h0_convergence.extension_summary(
            finished_dirs("H0-E01") + finished_dirs("H0-E02"))["per_dataset"]
        for ds, v in s["per_dataset"].items():
            v["earlier_effect_log2"] = (prior[ds]["effect_log2"]
                                        if ds in prior else None)
    budgets = {r["manifest"]["params"]["dataset"]:
               int(r["manifest"]["params"]["evaluation_budget_per_seed"])
               for r in runs if r["manifest"]}
    order = sorted(s["per_dataset"],
                   key=lambda d: -s["per_dataset"][d]["effect_log2"])
    return {"kind": "h0_ext", "repeat": repeat,
            "K": h0_convergence.K, "rows": s["per_seed"],
            "per_dataset": s["per_dataset"], "datasets": order,
            "primary": s["primary"], "secondary": s["secondary"],
            "missing": s["missing"], "budgets": budgets,
            "earlier_runs": [d.name for d in earlier],
            "reading": s["verdict"]}


def _style(plt) -> None:
    plt.rcParams.update({
        "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
        "axes.edgecolor": GRID, "axes.labelcolor": INK_2,
        "xtick.color": INK_2, "ytick.color": INK_2, "text.color": INK,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False,
        "font.size": 9, "axes.titlesize": 10, "legend.frameon": False,
    })


def _grid(plt, n: int, w: float = 3.2, h: float = 2.6):
    # Enough columns that the grid is wider than tall (about 16:9): figures
    # are read on a screen, beside text, not scrolled down a page.
    cols = max(min(4, n), int(np.ceil(np.sqrt(1.8 * n * h / w))))
    cols = min(cols, max(1, n))
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(w * cols, h * rows + 0.6),
                             squeeze=False)
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    return fig, list(axes.flat[:n])


def _colors(arms: Sequence[str]) -> Dict[str, str]:
    return {a: SERIES[i % len(SERIES)] for i, a in enumerate(arms)}


FOOTER_MAX_RUNS = 6


def _footer(fig, run_ids: Sequence[str], split: str) -> None:
    import textwrap
    width = int(fig.get_figwidth() * 17)  # characters of 7 pt per inch
    # Past a few runs -- one per dataset, arm and seed under run_queue.py --
    # the IDs would cover the panels; the report's run-key table lists them.
    runs = (f"runs: {', '.join(run_ids)}" if len(run_ids) <= FOOTER_MAX_RUNS
            else f"{len(run_ids)} runs, listed in tables/run_keys.csv")
    fig.text(0.01, 0.005, textwrap.fill(f"{split} split  |  {runs}", width),
             fontsize=7, color=INK_2, ha="left", va="bottom")


def fig_paired(ev, run_ids, path: Path) -> None:
    import matplotlib.pyplot as plt
    _style(plt)
    a, b, K = ev["challenger"], ev["baseline"], ev["K"]
    dss = [d for d in ev["datasets"]
           if any(r["dataset"] == d for r in ev["rows"])]
    fig, axes = _grid(plt, max(1, len(dss)))
    col = _colors([b, a])
    for ax, ds in zip(axes, dss):
        rows = [r for r in ev["rows"] if r["dataset"] == ds]
        for r in rows:
            ax.plot([0, 1], [r[b], r[a]], color=INK_2, lw=1, alpha=0.5)
        ax.scatter([0] * len(rows), [r[b] for r in rows], s=36, color=col[b],
                   edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
        ax.scatter([1] * len(rows), [r[a] for r in rows], s=36, color=col[a],
                   edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
        wins = sum(r["win"] for r in rows)
        ax.set_title(f"{ds}\n{a} ahead on {wins}/{len(rows)} seeds")
        ax.set_xticks([0, 1], [b, a])
        ax.set_xlim(-0.3, 1.3)
        ax.set_ylabel(f"AUF (K = {K}), test F1")
    fig.suptitle(f"AUF (K = {K}) per seed, {a} vs {b}; lines join the same "
                 f"seed", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_pairwise(ev, run_ids, path: Path) -> None:
    """The focal arm against each opponent, opponents along x.

    One point per dataset (focal minus opponent, mean AUF over seeds), a bar
    at the mean; under each opponent its wins-ties-losses and Holm p. A
    filled point marks a pair significant after Holm.
    """
    import matplotlib.pyplot as plt
    _style(plt)
    pairs = sorted(ev["pairs"], key=lambda p: p["mean_delta"])
    fig, ax = plt.subplots(figsize=(13, 5.2))
    rng = np.random.RandomState(0)
    for i, p in enumerate(pairs):
        d = list(p["diffs"].values())
        sig = p["significant"]
        ax.scatter(i + rng.uniform(-0.18, 0.18, len(d)), d, s=18,
                   color=SERIES[0] if sig else "#fcfcfb",
                   edgecolor=SERIES[0], linewidth=1, alpha=0.85, zorder=3)
        if d:
            ax.plot([i - 0.32, i + 0.32], [np.mean(d)] * 2, color=INK, lw=2,
                    zorder=4)
    ax.axhline(0, color=INK_2, lw=1)
    ax.set_xticks(range(len(pairs)),
                  [f"{p['opponent']}\n{p['wins']}-{p['ties']}-{p['losses']}"
                   f"\np = {p['p_holm']:.2g}" for p in pairs],
                  rotation=40, ha="right", rotation_mode="anchor", fontsize=8)
    ax.set_xlim(-0.6, len(pairs) - 0.4)
    ax.set_ylabel(f"mean AUF (K = {ev['K']}): {ev['focal']}\nminus opponent "
                  f"(> 0 favours {ev['focal']})")
    ax.set_title(f"{ev['focal']} against each opponent: one point per dataset, "
                 f"bar = mean; under each name wins-ties-losses and Holm p; "
                 f"filled = significant", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def missing_cells(experiment_id: str) -> Dict[Tuple[str, str], str]:
    """(dataset, method) -> "timeout" or "skipped" for cells with no result.

    Timeouts come from the queue's queue.json, skipped cells from the skip
    file the queue was run with. A cell counts as timed out only when every
    seed did: one seed's timeout leaves the other seeds' mean.
    """
    out: Dict[Tuple[str, str], str] = {}
    spec = SKIP_FILES.get(experiment_id)
    if spec:
        import run_queue
        for ds, arm in run_queue.parse_skip(f"@{REPO_ROOT / spec}"):
            out[(ds, QUEUE_ARMS.get(arm, arm))] = "skipped"
    q = RESULTS_DIR / experiment_id / "queue.json"
    if q.is_file():
        states = defaultdict(set)
        for j in json.loads(q.read_text(encoding="utf-8"))["jobs"]:
            states[(j["dataset"], QUEUE_ARMS.get(j["arm"], j["arm"]))].add(
                j["state"])
        for cell, s in states.items():
            if s == {"timeout"}:
                out[cell] = "timeout"
    return out


def _last_line(path: Path) -> Optional[bytes]:
    """The last line of a file, read from its end (trajectories are large)."""
    with open(path, "rb") as fh:
        fh.seek(0, 2)
        pos, buf = fh.tell(), b""
        while pos > 0 and buf.count(b"\n") < 2:
            step = min(4096, pos)
            pos -= step
            fh.seek(pos)
            buf = fh.read(step) + buf
    lines = [ln for ln in buf.splitlines() if ln.strip()]
    return lines[-1] if lines else None


# Offspring per generation of the NSGA-II searches (sota_baselines.run_nsga2,
# run_nsgaii_miip_method): with every offspring new, a run needs about
# budget / NSGA_POP generations.
NSGA_POP = 100


def timeout_rows(experiment_id: str) -> List[Dict]:
    """One row per timed-out job: fits reached and generations run.

    Read from the last line of the run's trajectory, the state at the
    moment the queue killed it. A run that was still finding new subsets
    needs about budget / NSGA_POP generations; one far past that was mostly
    re-proposing subsets already scored, which cost no fit.
    """
    q = RESULTS_DIR / experiment_id / "queue.json"
    if not q.is_file():
        return []
    rows = []
    for j in json.loads(q.read_text(encoding="utf-8"))["jobs"]:
        if j["state"] != "timeout" or not j.get("run_dir"):
            continue
        tr = sorted((Path(j["run_dir"]) / "trajectories").glob("*.jsonl"))
        last = _last_line(tr[0]) if tr else None
        if last is None:
            continue
        t = json.loads(last)
        rows.append({"dataset": j["dataset"],
                     "method": QUEUE_ARMS.get(j["arm"], j["arm"]),
                     "seed": j["seed"], "budget": j["budget"],
                     "fits": t["fits"], "generations": t["iteration"],
                     "generations_needed": j["budget"] // NSGA_POP,
                     "hours": round(t["seconds"] / 3600, 2)})
    return rows


def fig_timeouts(rows, run_ids, path: Path) -> None:
    """Timed-out runs: generations run against those a fresh run needs.

    Left: generations, log scale, one point per seed, with the budget /
    population line a run needs when all its offspring are new. Right: the
    share of the fit budget spent when the cap stopped it.
    """
    import matplotlib.pyplot as plt
    _style(plt)
    cells = list(dict.fromkeys((r["dataset"], r["method"]) for r in rows))
    arms = list(dict.fromkeys(r["method"] for r in rows))
    col = _colors(arms)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 4.8))
    for i, (d, m) in enumerate(cells):
        rs = [r for r in rows if (r["dataset"], r["method"]) == (d, m)]
        xs = i + np.linspace(-0.2, 0.2, len(rs)) if len(rs) > 1 else [i]
        a1.scatter(xs, [r["generations"] for r in rs], s=24, color=col[m],
                   edgecolor="#fcfcfb", zorder=3)
        a1.plot([i - 0.35, i + 0.35], [rs[0]["generations_needed"]] * 2,
                color=INK, lw=1.6, zorder=4)
        a2.scatter(xs, [r["fits"] / r["budget"] for r in rs], s=24,
                   color=col[m], edgecolor="#fcfcfb", zorder=3)
    labels = [f"{d}\n{m}" for d, m in cells]
    for ax in (a1, a2):
        ax.set_xticks(range(len(cells)), labels, rotation=40, ha="right",
                      rotation_mode="anchor", fontsize=7)
        ax.set_xlim(-0.6, len(cells) - 0.4)
    a1.set_yscale("log")
    a1.set_ylabel("generations run in 6 h")
    a1.set_title("Generations run; bar = budget / population, what a run "
                 "with all-new offspring needs", fontsize=9)
    a2.set_ylim(0, 1.05)
    a2.set_ylabel("share of the fit budget spent")
    a2.set_title("Fits spent when the 6 h cap stopped the run", fontsize=9)
    fig.suptitle(f"The {len(rows)} timed-out runs, one point per seed",
                 fontsize=10)
    _footer(fig, run_ids, "n/a")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def field_ranks(means: Dict[str, Dict[str, float]]):
    """Per dataset, each method's rank by mean AUF (1 = best, ties averaged).

    Ranked among the methods with a result on that dataset; reference-only
    arms are left out.
    """
    from scipy.stats import rankdata
    ranks = {}
    for ds, m in means.items():
        ms = [k for k in m if k not in REFERENCE_ONLY]
        r = rankdata([-m[k] for k in ms], method="average")
        ranks[ds] = dict(zip(ms, map(float, r)))
    return ranks


def cluster_order() -> List[str]:
    return sorted(set(SWAP_CLUSTERS.values()), key=lambda c: (c == "EO", c))


def cluster_rank_table(means) -> Tuple[List[str], List[str], Dict]:
    """Methods (best overall first), columns (clusters, then "all"), and
    {(method, column): (mean rank, datasets with a result)}."""
    ranks = field_ranks(means)
    methods = sorted({m for r in ranks.values() for m in r})
    cols = cluster_order() + ["all"]
    tab = {}
    for c in cols:
        dss = [d for d in ranks if c == "all" or SWAP_CLUSTERS.get(d) == c]
        for m in methods:
            rs = [ranks[d][m] for d in dss if m in ranks[d]]
            tab[(m, c)] = (float(np.mean(rs)) if rs else None, len(rs))
    methods.sort(key=lambda m: tab[(m, "all")][0])
    return methods, cols, tab


def fig_cluster_ranks(means, run_ids, path: Path) -> None:
    """Mean rank of every method in every cluster: who leads where.

    Descriptive: 1-7 datasets per cluster. A blank cell is a method with no
    result on any dataset of the cluster (timed out or skipped).
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    _style(plt)
    methods, cols, tab = cluster_rank_table(means)
    n_ds = {c: sum(1 for d in means if c == "all" or SWAP_CLUSTERS.get(d) == c)
            for c in cols}
    grid = np.array([[tab[(m, c)][0] if tab[(m, c)][0] is not None else np.nan
                      for c in cols] for m in methods])
    cmap = LinearSegmentedColormap.from_list("rank", [SERIES[0], "#f3f2ee",
                                                      "#c9c7c0"])
    cmap.set_bad("#fcfcfb")
    fig, ax = plt.subplots(figsize=(13, 6.4))
    ax.imshow(grid.T, cmap=cmap, vmin=1, vmax=len(methods), aspect="auto")
    ax.grid(False)
    best = np.nanmin(grid, axis=0)
    for j, c in enumerate(cols):
        for i, m in enumerate(methods):
            v, n = tab[(m, c)]
            if v is None:
                ax.text(i, j, "--", ha="center", va="center", fontsize=8,
                        color=INK_2)
                continue
            # Ties for the lead are all boxed.
            lead = bool(np.isclose(v, best[j]))
            ax.text(i, j, f"{v:.1f}", ha="center", va="center", fontsize=8,
                    color="#ffffff" if v < len(methods) * 0.3 else INK,
                    fontweight="bold" if lead else "normal")
            if lead:
                ax.add_patch(plt.Rectangle((i - 0.5, j - 0.5), 1, 1, fill=False,
                                           edgecolor=INK, lw=1.6))
    ax.axhline(len(cols) - 1.5, color=INK, lw=1.2)
    ax.set_xticks(range(len(methods)), methods, rotation=40, ha="right",
                  rotation_mode="anchor")
    ax.set_yticks(range(len(cols)),
                  [f"{c}  ({n_ds[c]} ds)" for c in cols])
    ax.set_title("Mean rank by AUF (K = 10) per cluster, 17 selectors (1 = best "
                 "on every dataset); boxed = row best, ties all boxed; -- = no "
                 "result; descriptive", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_ranks_per_dataset(means, missing, n_features, run_ids,
                          path: Path) -> None:
    """Every method's rank on every dataset, datasets along x by cluster.

    Marks: T = timed out on every seed, S = skipped (predicted over the cap),
    0 = no subset of size <= 10 on any seed, so AUF 0.
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    _style(plt)
    methods, _, _ = cluster_rank_table(means)
    ranks = field_ranks(means)
    dss = sorted(means, key=lambda d: (cluster_order().index(SWAP_CLUSTERS[d]),
                                       n_features.get(d) or 0))
    grid = np.array([[ranks[d].get(m, np.nan) for d in dss] for m in methods])
    cmap = LinearSegmentedColormap.from_list("rank", [SERIES[0], "#f3f2ee",
                                                      "#c9c7c0"])
    cmap.set_bad("#fcfcfb")
    fig, ax = plt.subplots(figsize=(16, 6.6))
    ax.imshow(grid, cmap=cmap, vmin=1, vmax=len(methods), aspect="auto")
    ax.grid(False)
    for i, m in enumerate(methods):
        for j, d in enumerate(dss):
            mark = {"timeout": "T", "skipped": "S"}.get(missing.get((d, m)))
            if mark is None and m in means[d] and means[d][m] == 0:
                mark = "0"
            if mark:
                ax.text(j, i, mark, ha="center", va="center", fontsize=7,
                        color=SERIES[1] if mark != "0" else INK)
    edges = [j for j in range(1, len(dss))
             if SWAP_CLUSTERS[dss[j]] != SWAP_CLUSTERS[dss[j - 1]]]
    for j in edges:
        ax.axvline(j - 0.5, color=INK, lw=1.2)
    starts = [0] + edges + [len(dss)]
    for a, b in zip(starts, starts[1:]):
        ax.text((a + b - 1) / 2, -0.9, SWAP_CLUSTERS[dss[a]], ha="center",
                va="bottom", fontsize=9, fontweight="bold")
    ax.set_xticks(range(len(dss)), dss, rotation=55, ha="right",
                  rotation_mode="anchor", fontsize=7)
    ax.set_yticks(range(len(methods)), methods, fontsize=8)
    ax.set_ylim(len(methods) - 0.5, -1.2)
    ax.set_title("Rank by mean AUF (K = 10) on each dataset (blue = best); "
                 "clusters left to right, datasets by feature count within; "
                 "T = timed out, S = skipped, 0 = nothing of size <= 10",
                 fontsize=10, pad=14)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_h0_criterion(ev, run_ids, path: Path) -> None:
    """Fits to the common target per seed, 2020 against fixed, per dataset."""
    import matplotlib.pyplot as plt
    _style(plt)
    b, a = H0_ARMS
    fig, axes = _grid(plt, max(1, len(ev["datasets"])))
    col = _colors([b, a])
    for ax, ds in zip(axes, ev["datasets"]):
        rows = [r for r in ev["rows"] if r["dataset"] == ds]
        yb = [r["fits_to_target_2020"] for r in rows]
        ya = [r["fits_to_target_fixed"] for r in rows]
        for u, v in zip(yb, ya):
            ax.plot([0, 1], [u, v], color=INK_2, lw=1, alpha=0.5)
        ax.scatter([0] * len(rows), yb, s=36, color=col[b],
                   edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
        ax.scatter([1] * len(rows), ya, s=36, color=col[a],
                   edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
        ax.axhline(ev["budgets"][ds], color=INK_2, lw=1, ls=":")
        v = ev["per_dataset"][ds]
        ax.set_title(f"{ds} (budget {ev['budgets'][ds]:,})\n{a} faster on "
                     f"{v['faster_fixed']}/{v['seeds']} seeds")
        ax.set_xticks([0, 1], [b, a])
        ax.set_xlim(-0.3, 1.3)
        ax.set_ylim(bottom=0)
        ax.set_ylabel("fits to target (fewer is faster)")
    fig.suptitle(f"Cumulative fits to reach the common target, validation AUF "
                 f"(K = {ev['K']}); lines join the same seed, dotted = budget",
                 fontsize=10)
    _footer(fig, run_ids, "validation")
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _dataset_strip(dss, points, means, groups, ylabel, title, run_ids,
                   split, path: Path) -> None:
    """Per dataset along x: one point per seed, a bar at the mean. Wide.

    `points` and `means` are keyed by dataset; `groups` labels each dataset
    (cluster, group), and a rule separates runs of the same label.
    """
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(max(10.0, 0.34 * len(dss) + 2.5), 5.2))
    prev = None
    for i, ds in enumerate(dss):
        if prev is not None and groups.get(ds) != prev:
            ax.axvline(i - 0.5, color=GRID, lw=1)
        prev = groups.get(ds)
        e = points[ds]
        ax.scatter([i] * len(e), e, s=16, color=SERIES[0], alpha=0.75,
                   edgecolor="#fcfcfb", linewidth=0.8, zorder=3)
        if means.get(ds) is not None:
            ax.plot([i - 0.35, i + 0.35], [means[ds]] * 2, color=INK, lw=2,
                    zorder=4)
    ax.axhline(0, color=INK_2, lw=1)
    ax.set_xticks(range(len(dss)),
                  [f"{d} ({groups[d]})" if groups.get(d) else d for d in dss],
                  fontsize=7, rotation=60, ha="right", rotation_mode="anchor")
    ax.set_xlim(-0.6, len(dss) - 0.4)
    ax.set_ylabel(ylabel)
    # Wrapped to the figure's width: a long title is otherwise cut off.
    import textwrap
    ax.set_title(textwrap.fill(title, int(fig.get_figwidth() * 13)))
    _footer(fig, run_ids, split)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_h0_ext_criterion(ev, run_ids, path: Path) -> None:
    """Per dataset: log2(fits 2020 / fits fixed) per seed, bar = the mean."""
    dss = ev["datasets"]
    p = ev["primary"]
    pv = "--" if p["p_value"] is None else f"{p['p_value']:.3g}"
    _dataset_strip(
        dss,
        {d: [r["effect_log2"] for r in ev["rows"] if r["dataset"] == d]
         for d in dss},
        {d: ev["per_dataset"][d]["effect_log2"] for d in dss},
        {d: ev["per_dataset"][d].get("group") for d in dss},
        "log2(fits to target, 2020 / fixed)\n(> 0: the fixed code was faster)",
        f"Per dataset: one point per seed, bar = mean.  {p['positive']} "
        f"datasets > 0, {p['negative']} < 0, Wilcoxon p = {pv}",
        run_ids, "validation", path)


def fig_dataset_unit(ev, run_ids, path: Path) -> None:
    """Per dataset, by cluster: AUF delta per seed, bar = the mean (H2, H3)."""
    a, b, K = ev["challenger"], ev["baseline"], ev["K"]
    dss = ev["datasets"]
    pd_ = ev["per_dataset"]
    p = ev["primary"]
    pv = "--" if p["p_value"] is None else f"{p['p_value']:.3g}"
    _dataset_strip(
        dss, {d: list(pd_[d]["deltas"].values()) for d in dss},
        {d: pd_[d]["effect"] for d in dss}, {d: pd_[d]["cluster"] for d in dss},
        f"AUF (K = {K}), test:\n{a} minus {b}",
        f"{a} minus {b}, per dataset: one point per seed, bar = mean.  "
        f"{p['positive']} datasets > 0, {p['negative']} < 0, Wilcoxon p = {pv}",
        run_ids, "test", path)


# The paper benchmarks' domains, as HYPOTHESES.md groups them (Datasets).
PAPER_DOMAINS = {
    **{d: "genes" for d in ("GLIOMA", "nci9", "colon", "ALLAML", "leukemia",
                            "lung_discrete", "GLI_85", "lymphoma",
                            "Prostate_GE", "CLL_SUB_111", "TOX_171", "lung")},
    "arcene": "mass spec.",
    **{d: "images" for d in ("orlraws10P", "warpAR10P", "Yale", "warpPIE10P",
                             "ORL", "COIL20")},
    **{d: "handwriting, speech" for d in ("Isolet", "gisette", "USPS")},
    **{d: "text" for d in ("RELATHE", "PCMAC", "BASEHOCK")},
}
DOMAIN_ORDER = ("genes", "mass spec.", "images", "handwriting, speech", "text")


def fig_pairwise_strip(ev, cells, run_ids, path: Path) -> None:
    """H4: per dataset, focal minus opponent AUF; points pair seed numbers."""
    p0 = ev["pairs"][0]
    focal, opp, K = ev["focal"], p0["opponent"], ev["K"]
    order = {g: i for i, g in enumerate(DOMAIN_ORDER)}
    dss = sorted(p0["diffs"], key=lambda d: (
        order.get(PAPER_DOMAINS.get(d), len(order)), -p0["diffs"][d]))
    points = {}
    for d in dss:
        a, b = cells[d].get(focal, {}), cells[d].get(opp, {})
        points[d] = [a[s] - b[s] for s in sorted(set(a) & set(b))]
    pv = "--" if p0["p"] is None or np.isnan(p0["p"]) else f"{p0['p']:.3g}"
    _dataset_strip(
        dss, points, {d: p0["diffs"][d] for d in dss},
        {d: PAPER_DOMAINS.get(d) for d in dss},
        f"AUF (K = {K}), test:\n{focal} minus {opp}",
        f"{focal} minus {opp}, per dataset: one point per seed number, bar = "
        f"difference of the means.  {p0['wins']} datasets > 0, "
        f"{p0['losses']} < 0, Wilcoxon p = {pv}",
        run_ids, "test", path)


def fig_compute(rows: Sequence[Dict], methods: Sequence[str], run_ids,
                path: Path) -> None:
    """Equal compute, checked: CPU seconds and fits per run, per dataset."""
    import matplotlib.pyplot as plt
    _style(plt)
    a, b = methods
    by = {(r["dataset"], r["method"]): r for r in rows}
    ds = sorted(d for d, m in by if m == a and (d, b) in by)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    for ax, key, label, log in ((axes[0], "cpu_seconds", "CPU seconds per run",
                                 False),
                                (axes[1], "fits", "model fits per run", True)):
        x = [by[(d, b)][key] for d in ds]
        y = [by[(d, a)][key] for d in ds]
        pairs = [(u, v) for u, v in zip(x, y) if u and v]
        if pairs:
            lo = min(min(pq) for pq in pairs) * 0.8
            hi = max(max(pq) for pq in pairs) * 1.2
            ax.plot([lo, hi], [lo, hi], color=INK_2, lw=1, ls="--")
            ax.scatter(*zip(*pairs), s=24, color=SERIES[0], alpha=0.85,
                       edgecolor="#fcfcfb", linewidth=0.8, zorder=3)
            if log:
                ax.set_xscale("log")
                ax.set_yscale("log")
            ratio = np.median([v / u for u, v in pairs])
            ax.set_title(f"{label}\nmedian {a} / {b} = {ratio:.2f}")
        ax.set_xlabel(b)
        ax.set_ylabel(a)
    fig.suptitle("Compute per run, one point per dataset (mean over seeds); "
                 "dashed line: equal", fontsize=10)
    _footer(fig, run_ids, "search")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_table3(t3, run_ids, path: Path) -> None:
    """H4: ours against the paper's Table 3, values and ordering."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    ax = axes[0]
    allv = []
    for i, (m, es) in enumerate(sorted(t3["per_method"].items())):
        x = [e["paper_mean"] for e in es]
        y = [e["ours_mean"] for e in es]
        allv += x + y
        ax.scatter(x, y, s=24, color=SERIES[i], alpha=0.85,
                   edgecolor="#fcfcfb", linewidth=0.8, zorder=3,
                   label=f"{m} (mean |ours - paper| = "
                         f"{t3['summary'][m]['mean_abs_delta']:.3f})")
    lo, hi = min(allv) - 0.03, max(allv) + 0.03
    ax.plot([lo, hi], [lo, hi], color=INK_2, lw=1, ls="--")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("paper's Table 3: mean AUF")
    ax.set_ylabel("ours: mean test AUF (K = 20)")
    ax.legend(fontsize=7, loc="upper left")
    ax.set_title("Values, one point per dataset and method")
    ax = axes[1]
    by = {(e["dataset"], m): e for m, es in t3["per_method"].items()
          for e in es}
    ds = sorted({d for d, _ in by})
    x = [by[(d, "fastener")]["paper_mean"] - by[(d, "fs_sds")]["paper_mean"]
         for d in ds if (d, "fs_sds") in by and (d, "fastener") in by]
    y = [by[(d, "fastener")]["ours_mean"] - by[(d, "fs_sds")]["ours_mean"]
         for d in ds if (d, "fs_sds") in by and (d, "fastener") in by]
    ax.axhline(0, color=INK_2, lw=1)
    ax.axvline(0, color=INK_2, lw=1)
    ax.scatter(x, y, s=24, color=SERIES[0], alpha=0.85, edgecolor="#fcfcfb",
               linewidth=0.8, zorder=3)
    ax.set_xlabel("paper: FASTENER minus FS-SDS")
    ax.set_ylabel("ours: fastener minus fs_sds")
    ax.set_title(f"Ordering: same sign on {t3['ordering_agreement']} "
                 f"datasets\n(paper: FASTENER ahead on 24 of 25)")
    fig.suptitle("Against the FASTENER paper's Table 3 (values not directly "
                 "comparable: our split and selection differ)", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_two_by_two(tbt, run_ids, path: Path) -> None:
    """H4's 2 x 2: classifier effect per method, search effect per classifier."""
    import matplotlib.pyplot as plt
    _style(plt)
    per = tbt["per_dataset"]
    ds = sorted(per)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    for ax, pairs, title in (
            (axes[0], [(meth, cl["tree"], cl["elm"])
                       for meth, cl in H4_CELLS.items()],
             "Classifier: AUF with the ELM against with the tree"),
            (axes[1], [("FS-SDS minus FASTENER",
                        (H4_CELLS["FS-SDS"]["tree"],
                         H4_CELLS["FASTENER"]["tree"]),
                        (H4_CELLS["FS-SDS"]["elm"],
                         H4_CELLS["FASTENER"]["elm"]))],
             "Search: FS-SDS minus FASTENER, tree (x) against ELM (y)")):
        vals = []
        for i, (label, x_lab, y_lab) in enumerate(pairs):
            if isinstance(x_lab, tuple):
                x = [per[d][x_lab[0]] - per[d][x_lab[1]] for d in ds]
                y = [per[d][y_lab[0]] - per[d][y_lab[1]] for d in ds]
            else:
                x = [per[d][x_lab] for d in ds]
                y = [per[d][y_lab] for d in ds]
            vals += x + y
            ax.scatter(x, y, s=24, color=SERIES[i], alpha=0.85,
                       edgecolor="#fcfcfb", linewidth=0.8, zorder=3,
                       label=label)
        lo, hi = min(vals) - 0.03, max(vals) + 0.03
        ax.plot([lo, hi], [lo, hi], color=INK_2, lw=1, ls="--")
        if lo < 0 < hi:
            ax.axhline(0, color=GRID, lw=1)
            ax.axvline(0, color=GRID, lw=1)
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_title(title, fontsize=9)
        ax.legend(fontsize=7, loc="upper left")
    axes[0].set_xlabel("mean test AUF (K = 20), decision tree")
    axes[0].set_ylabel("mean test AUF (K = 20), ELM")
    axes[1].set_xlabel("decision tree (H4-E01)")
    axes[1].set_ylabel("ELM (H4-E02)")
    fig.suptitle("H4 across classifiers, one point per dataset (mean over "
                 "seeds); dashed line: equal", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_budget_compare(bc, focal, opp, experiment_id, run_ids,
                       path: Path) -> None:
    """Each arm's mean AUF here against in the paired experiment, and the
    per-dataset effect (focal minus opponent) under both budgets."""
    import matplotlib.pyplot as plt
    _style(plt)
    per = bc["per_dataset"]
    ds = sorted(d for d in per if focal in per[d] and opp in per[d])
    other = bc["partner"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    ax = axes[0]
    vals = []
    for i, m in enumerate((opp, focal)):
        x = [per[d][m]["other"] for d in ds]
        y = [per[d][m]["here"] for d in ds]
        vals += x + y
        ax.scatter(x, y, s=24, color=SERIES[i], alpha=0.85,
                   edgecolor="#fcfcfb", linewidth=0.8, zorder=3,
                   label=f"{m} (mean {np.mean(y) - np.mean(x):+.3f})")
    lo, hi = min(vals) - 0.03, max(vals) + 0.03
    ax.plot([lo, hi], [lo, hi], color=INK_2, lw=1, ls="--")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel(f"mean test AUF, {other}")
    ax.set_ylabel(f"mean test AUF, {experiment_id}")
    ax.set_title("Each method's score under the two budgets", fontsize=9)
    ax.legend(fontsize=7, loc="upper left")
    ax = axes[1]
    x = [per[d][focal]["other"] - per[d][opp]["other"] for d in ds]
    y = [per[d][focal]["here"] - per[d][opp]["here"] for d in ds]
    lo, hi = min(x + y) - 0.03, max(x + y) + 0.03
    ax.plot([lo, hi], [lo, hi], color=INK_2, lw=1, ls="--")
    ax.axhline(0, color=GRID, lw=1)
    ax.axvline(0, color=GRID, lw=1)
    ax.scatter(x, y, s=24, color=SERIES[2], alpha=0.85, edgecolor="#fcfcfb",
               linewidth=0.8, zorder=3)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel(f"{focal} minus {opp}, {other}")
    ax.set_ylabel(f"{focal} minus {opp}, {experiment_id}")
    ax.set_title(f"Per dataset: > 0 on {sum(v > 0 for v in x)} in {other}, "
                 f"on {sum(v > 0 for v in y)} here", fontsize=9)
    fig.suptitle(f"{experiment_id} against {other}, one point per dataset "
                 f"(mean over seeds); dashed line: equal", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_effect_vs_size(evs, run_ids, path: Path) -> None:
    """Per-dataset effect against rows (n) and features (p), H2 and H3."""
    import matplotlib.pyplot as plt
    from scipy.stats import spearmanr
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
    for ax, key, label in ((axes[0], "n", "rows in the dataset (n)"),
                           (axes[1], "p", "features in the dataset (p)")):
        for i, ev in enumerate(evs):
            pd_ = ev["per_dataset"]
            ds = [d for d in ev["datasets"] if pd_[d].get(key)]
            x = [pd_[d][key] for d in ds]
            y = [pd_[d]["effect"] for d in ds]
            rho = spearmanr(x, y)[0] if len(ds) > 2 else float("nan")
            ax.scatter(x, y, s=22, color=SERIES[i], alpha=0.8,
                       edgecolor="#fcfcfb", linewidth=0.8, zorder=3,
                       label=f"{ev['challenger']} minus {ev['baseline']} "
                             f"(Spearman rho = {rho:.2f})")
        ax.axhline(0, color=INK_2, lw=1)
        ax.set_xscale("log")
        ax.set_xlabel(label)
        ax.legend(fontsize=7, loc="upper right")
    axes[0].set_ylabel(f"effect: mean AUF (K = {evs[0]['K']}) "
                       f"difference, test")
    fig.suptitle("Per-dataset effect against dataset size; one point per "
                 "dataset", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_by_cluster(evs, run_ids, path: Path) -> None:
    """Per cluster: each swap arm against stock, and guided against random.

    One point per dataset (its mean effect over seeds), a bar at the
    cluster's median. Descriptive only: 1-7 datasets per cluster.
    """
    import matplotlib.pyplot as plt
    _style(plt)
    by = {ev["challenger"]: ev for ev in evs}
    comps = []
    for ev in evs:
        comps.append((f"{ev['challenger']} minus {ev['baseline']}",
                      {d: v["effect"] for d, v in ev["per_dataset"].items()
                       if v["effect"] is not None}))
    gv = by.get(GUIDANCE[0], {}).get("secondary", {}).get("guided_vs_random")
    if gv:
        comps.append((f"{GUIDANCE[0]} minus {GUIDANCE[1]}",
                      {d: e for d, e in gv["per_dataset"].items()
                       if e is not None}))
    clusters = sorted(set(SWAP_CLUSTERS.values()),
                      key=lambda c: (c == "EO", c))
    width = 0.8 / len(comps)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    for j, (label, eff) in enumerate(comps):
        for i, c in enumerate(clusters):
            x0 = i - 0.4 + width * (j + 0.5)
            ys = [e for d, e in eff.items() if SWAP_CLUSTERS.get(d) == c]
            if not ys:
                continue
            ax.scatter([x0] * len(ys), ys, s=16, color=SERIES[j], alpha=0.75,
                       edgecolor="#fcfcfb", linewidth=0.8, zorder=3,
                       label=label if i == 0 else None)
            ax.plot([x0 - width * 0.4, x0 + width * 0.4], [np.median(ys)] * 2,
                    color=INK, lw=2, zorder=4)
    for i in range(1, len(clusters)):
        ax.axvline(i - 0.5, color=GRID, lw=1)
    ax.axhline(0, color=INK_2, lw=1)
    n_of = {c: sum(1 for d in SWAP_SETS if SWAP_CLUSTERS[d] == c)
            for c in clusters}
    ax.set_xticks(range(len(clusters)),
                  [f"{c}\n({n_of[c]} dataset{'s' if n_of[c] != 1 else ''})"
                   for c in clusters])
    ax.set_xlim(-0.5, len(clusters) - 0.5)
    ax.set_ylabel(f"effect: mean AUF (K = {evs[0]['K']}) difference, test")
    ax.legend(fontsize=7, loc="upper right")
    ax.set_title("Per cluster: one point per dataset (mean over seeds), bar = "
                 "cluster median; descriptive only", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_swap_success(evs, run_ids, path: Path) -> None:
    """Guided against random swap, per dataset: how often a swap won its size
    slot, and how many final-front entries a swap made. Means over seeds."""
    import matplotlib.pyplot as plt
    _style(plt)
    act = {}
    for ev in evs:
        for r in ev["secondary"]["swap_activity"]:
            act[(r["dataset"], r["method"])] = r
    g, rnd = GUIDANCE
    ds = sorted(d for d, m in act if m == g and (d, rnd) in act)

    def kept(r):
        return r["swap_kept"] / r["swap_proposed"] if r["swap_proposed"] \
            else 0.0

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    for ax, f, label in (
            (axes[0], kept, "share of swaps that won their size slot"),
            (axes[1], lambda r: r["front_from_swap"],
             "final-front entries a swap made")):
        x = [f(act[(d, rnd)]) for d in ds]
        y = [f(act[(d, g)]) for d in ds]
        top = max(x + y + [1e-9]) * 1.08
        ax.plot([0, top], [0, top], color=INK_2, lw=1, ls="--")
        ax.scatter(x, y, s=24, color=SERIES[2], alpha=0.85,
                   edgecolor="#fcfcfb", linewidth=0.8, zorder=3)
        above = sum(b > a for a, b in zip(x, y))
        below = sum(b < a for a, b in zip(x, y))
        ax.set_xlim(0, top)
        ax.set_ylim(0, top)
        ax.set_xlabel(rnd)
        ax.set_ylabel(g)
        ax.set_title(f"{label}\nabove the diagonal on {above} datasets, "
                     f"below on {below}")
    fig.suptitle("Guided against random swap, one point per dataset, mean "
                 "over seeds", fontsize=10)
    _footer(fig, run_ids, "search")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_h0_progress(ev, run_ids, path: Path) -> None:
    """Validation AUF (K) against cumulative fits: mean, band = min-max."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = _grid(plt, max(1, len(ev["datasets"])), w=3.6, h=2.8)
    col = _colors(list(H0_ARMS))
    for ax, ds in zip(axes, ev["datasets"]):
        budget = ev["budgets"][ds]
        grid = np.linspace(0, budget, 400)
        lows = []
        for arm in H0_ARMS:
            cs = [c for (d, m, _), c in sorted(ev["curves"].items())
                  if d == ds and m == arm]
            if not cs:
                continue
            # A step curve read at each grid point; NaN before its first
            # snapshot, which holds only the initial population.
            vals = np.array([[next((v for f, v in reversed(c) if f <= x),
                                   np.nan) for x in grid] for c in cs])
            start = np.nanmax([c[0][0] for c in cs])
            keep = grid >= start
            x, v = grid[keep], vals[:, keep]
            ax.fill_between(x, v.min(0), v.max(0), color=col[arm],
                            alpha=0.15, lw=0, step="post")
            ax.step(x, v.mean(0), where="post", color=col[arm], lw=2,
                    label=arm)
            lows.append(np.nanmin(vals[:, grid >= 0.05 * budget]))
        if lows:
            ax.set_ylim(bottom=min(lows) - 0.01)
        ax.set_xlim(0, budget)
        ax.set_title(ds)
        ax.set_xlabel("cumulative unique fits")
        ax.set_ylabel(f"AUF (K = {ev['K']}), validation F1")
    axes[0].legend(fontsize=7, loc="lower right")
    fig.suptitle(f"Validation AUF (K = {ev['K']}) against fits: mean over "
                 f"seeds, band = min-max; y axis starts at 5% of the budget",
                 fontsize=10)
    _footer(fig, run_ids, "validation")
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def h0_deltas(ev) -> List[Dict]:
    """Per seed, fixed minus 2020 on each secondary measure (H0_SECONDARY)."""
    out = []
    for r in ev["rows"]:
        row = {"dataset": r["dataset"], "seed": r["seed"]}
        for col, _, rel in H0_SECONDARY:
            f, o = r.get(f"{col}_fixed"), r.get(f"{col}_2020")
            if f is None or o is None:
                row[col] = None
            else:
                row[col] = 100.0 * (f - o) / o if rel else f - o
        out.append(row)
    return out


def h0_secondary_summary(ev) -> List[Dict]:
    """Per dataset and secondary measure: seeds higher for fixed, mean, range."""
    deltas = h0_deltas(ev)
    out = []
    for ds in ev["datasets"]:
        for col, label, rel in H0_SECONDARY:
            d = [r[col] for r in deltas if r["dataset"] == ds
                 and r[col] is not None]
            if not d:
                continue
            out.append({"dataset": ds, "measure": label,
                        "unit": "%" if rel else "absolute",
                        "seeds": len(d), "fixed_higher": sum(x > 0 for x in d),
                        "mean_delta": float(np.mean(d)),
                        "min_delta": float(min(d)),
                        "max_delta": float(max(d))})
    return out


def fig_h0_secondary(ev, run_ids, path: Path) -> None:
    import matplotlib.pyplot as plt
    _style(plt)
    deltas = h0_deltas(ev)
    dss = ev["datasets"]
    fig, axes = plt.subplots(2, 3, figsize=(11, 5.6))
    for ax, (col, label, _) in zip(axes.flat, H0_SECONDARY):
        for i, ds in enumerate(dss):
            d = [r[col] for r in deltas if r["dataset"] == ds
                 and r[col] is not None]
            ax.scatter(d, [i] * len(d), s=24, color=SERIES[0], alpha=0.8,
                       edgecolor="#fcfcfb", linewidth=1, zorder=3)
            if d:
                ax.plot([np.mean(d)] * 2, [i - 0.3, i + 0.3], color=INK, lw=2)
        ax.axvline(0, color=INK_2, lw=1)
        ax.set_yticks(range(len(dss)), dss)
        ax.invert_yaxis()
        ax.set_title(label)
    fig.suptitle(f"Secondary measures, {H0_ARMS[1]} minus {H0_ARMS[0]}; one "
                 f"point per seed, bar = mean; > 0 means higher for {H0_ARMS[1]}",
                 fontsize=10)
    _footer(fig, run_ids, "validation (area) and test (AUF, hypervolume)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.95))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_opt_curves(units, arms, K, run_ids, path: Path) -> None:
    import matplotlib.pyplot as plt
    _style(plt)
    Kc = max(K, 20)
    dss = sorted({u["dataset"] for u in units if u["method"] in arms})
    fig, axes = _grid(plt, max(1, len(dss)))
    col = _colors(arms)
    ks = np.arange(1, Kc + 1)
    for ax, ds in zip(axes, dss):
        for arm in arms:
            curves = [opt_curve(u["records"], Kc) for u in units
                      if u["dataset"] == ds and u["method"] == arm
                      and u["records"]]
            if not curves:
                continue
            c = np.array(curves)
            ax.fill_between(ks, c.min(0), c.max(0), color=col[arm], alpha=0.15,
                            lw=0, step="post")
            ax.step(ks, c.mean(0), where="post", color=col[arm], lw=2,
                    label=arm)
        ax.axvline(K, color=INK_2, lw=1, ls=":")
        ax.set_title(ds)
        ax.set_xlabel("k (subset size at most)")
        ax.set_ylabel("opt(k), test F1")
    axes[0].legend(fontsize=7, loc="lower right")
    fig.suptitle("Best test F1 at size <= k (val-selected): mean over seeds, "
                 "band = min-max; dotted line = K", fontsize=10)
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_size_range(units, arms, run_ids, path: Path) -> None:
    """Where each front lies on the size axis, against the feature count.

    One vertical bar per seed, from the smallest to the largest subset on the
    final front, at the dataset's feature count p; the arms sit side by side.
    The guides mark p, p/2 (where OBL starts) and k = 10.
    """
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(8, 4.6))
    col = _colors(arms)
    ps = sorted({u["n_features"] for u in units if u["n_features"]})
    for i, arm in enumerate(arms):
        first = True
        for u in units:
            if u["method"] != arm or not u["records"] or not u["n_features"]:
                continue
            sizes = [r["n_features"] for r in u["records"]]
            # Seeds fan out a little around p, arms to either side of it.
            shift = 1 + 0.06 * (i - (len(arms) - 1) / 2) \
                + 0.012 * ((u["seed"] or 0) % 5 - 2)
            x = u["n_features"] * shift
            ax.plot([x, x], [min(sizes), max(sizes)], color=col[arm], lw=2.2,
                    solid_capstyle="round", label=arm if first else None)
            first = False
    if ps:
        xs = np.array([ps[0] * 0.7, ps[-1] * 1.4])
        ax.plot(xs, xs, color=INK_2, lw=0.9, ls="-", label="all features (p)")
        ax.plot(xs, xs / 2, color=INK_2, lw=0.9, ls="--",
                label="p/2, where OBL starts")
        ax.axhline(10, color=INK_2, lw=0.9, ls=":", label="k = 10")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("features in the dataset (p)")
    ax.set_ylabel("subset sizes on the final front")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    fig.suptitle("Size range of each final front, smallest to largest subset, "
                 "one bar per seed", fontsize=10)
    _footer(fig, run_ids, "validation-selected front")
    fig.tight_layout(rect=(0, 0.04, 1, 0.97))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_cost(units, arms, run_ids, path: Path) -> None:
    """Fits and wall clock, as two panels: two scales never share an axis."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.4))
    col = _colors(arms)
    for i, arm in enumerate(arms):
        us = [u for u in units if u["method"] == arm]
        f = [u["model_fits"] for u in us if u["model_fits"] is not None]
        s = [u["seconds"] for u in us if u["seconds"] is not None]
        a1.scatter([i] * len(f), f, s=26, color=col[arm], edgecolor="#fcfcfb")
        a2.scatter([i] * len(s), s, s=26, color=col[arm], edgecolor="#fcfcfb")
    for ax, lab in ((a1, "unique model fits"), (a2, "wall clock (s)")):
        ax.set_xticks(range(len(arms)), arms, rotation=20, ha="right")
        ax.set_ylabel(lab)
    a2.set_yscale("log")
    fig.suptitle("Cost per run key (one point per dataset x seed)",
                 fontsize=10)
    _footer(fig, run_ids, "n/a")
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    fig.savefig(path, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------- report
def fmt(x, nd=4) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "--"
    return f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def md_table(header: Sequence[str], rows: Sequence[Sequence]) -> str:
    out = ["| " + " | ".join(header) + " |",
           "|" + "---|" * len(header)]
    out += ["| " + " | ".join(fmt(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def write_csv(path: Path, rows: List[Dict]) -> None:
    if not rows:
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def build(experiment_id: str, run_ids: Sequence[str], out_dir: Path,
          force: bool = False) -> Path:
    info = experiment_ids.parse_experiment_id(experiment_id)
    hids = info["hypotheses"]
    runs = [load_run(r) for r in run_ids]
    units, notes = units_of(runs)
    fig_dir, tab_dir = out_dir / "figures", out_dir / "tables"
    fig_dir.mkdir(parents=True, exist_ok=True)
    tab_dir.mkdir(parents=True, exist_ok=True)

    manifests = [r["manifest"] for r in runs if r["manifest"]]
    commits = sorted({m["git"]["experiments"].get("commit") for m in manifests
                      if m["git"]["experiments"].get("commit")})
    first = min(manifests, key=lambda m: m["started_utc"]) if manifests else None
    prereg = first["git"]["experiments"].get("commit") if first else None
    htext, hsource = hypotheses_text(prereg)
    head_text = (REPO_ROOT / HYPOTHESES_PATH).read_text(encoding="utf-8")
    # git show gives LF; a Windows checkout may have CRLF. Not a change.
    htext, head_text = (t.replace("\r\n", "\n") for t in (htext, head_text))

    algo = {}
    for m in manifests:
        for arm, a in m.get("algorithms", {}).items():
            algo.setdefault(arm, set()).add(a["id"])
    for u in units:
        if u["algorithm_id"]:
            algo.setdefault(u["method"], set()).add(u["algorithm_id"])

    # ---- per hypothesis: sections, criteria, figures --------------------
    fig_no, figures, per_h = 0, [], []
    for hid in hids:
        sec = section(htext, hid)
        K = primary_k(sec or "")
        cells = by_cell(units, K)
        sec_ext = None
        if hid == "H0" and (is_h0_extension(runs) or is_h0_repeat(runs)):
            repeat = is_h0_repeat(runs)
            ev = evaluate_h0_extension(runs, repeat=repeat)
            sec_ext = subsection(htext, H0_REPEAT_TITLE if repeat
                                 else H0_EXT_TITLE)
            K = ev["K"]
            arms = list(H0_ARMS)
        elif hid == "H0":
            ev = evaluate_h0(runs)
            K = ev["K"]
            arms = list(H0_ARMS)
        elif hid in PAIRED:
            ev = evaluate_paired(hid, cells, K)
            arms = [ev["baseline"], ev["challenger"]]
        elif hid in DATASET_UNIT:
            ev = evaluate_dataset_unit(hid, cells, K, units)
            arms = [ev["baseline"], ev["challenger"]]
        elif hid in PAIRWISE:
            ev = evaluate_pairwise(
                hid, cells, K,
                h4_arms(units)[:2] if hid == "H4" else None)
            top = sorted((p for p in ev["pairs"] if p["n_datasets"]),
                         key=lambda p: p["mean_delta"])[:3]
            arms = [ev["focal"]] + [p["opponent"] for p in top]
        else:
            ev, arms = None, sorted({u["method"] for u in units})
        fig_no += 1
        crit_fig = fig_dir / f"F{fig_no}_{hid}_criterion_auf{K}.png"
        if ev and ev["kind"] == "h0_ext":
            crit_fig = fig_dir / f"F{fig_no}_{hid}_effect_per_dataset.png"
            fig_h0_ext_criterion(ev, run_ids, crit_fig)
            write_csv(tab_dir / f"{hid}_per_seed.csv", ev["rows"])
            write_csv(tab_dir / f"{hid}_per_dataset.csv",
                      [{"dataset": d, **ev["per_dataset"][d]}
                       for d in ev["datasets"]])
            write_csv(tab_dir / f"{hid}_by_group.csv",
                      [{"group": g, **v} for g, v in
                       ev["secondary"].get("by_group", {}).items()])
        elif ev and ev["kind"] == "h0":
            crit_fig = fig_dir / f"F{fig_no}_{hid}_fits_to_target.png"
            fig_h0_criterion(ev, run_ids, crit_fig)
            write_csv(tab_dir / f"{hid}_per_seed.csv", ev["rows"])
            write_csv(tab_dir / f"{hid}_per_dataset.csv",
                      [{"dataset": d, **ev["per_dataset"][d]}
                       for d in ev["datasets"]])
            write_csv(tab_dir / f"{hid}_secondary_deltas.csv", h0_deltas(ev))
            write_csv(tab_dir / f"{hid}_secondary_summary.csv",
                      h0_secondary_summary(ev))
        elif ev and ev["kind"] == "paired":
            fig_paired(ev, run_ids, crit_fig)
            write_csv(tab_dir / f"{hid}_auf{K}_per_seed.csv", ev["rows"])
        elif ev and ev["kind"] == "dataset_unit":
            crit_fig = fig_dir / f"F{fig_no}_{hid}_effect_per_dataset.png"
            fig_dataset_unit(ev, run_ids, crit_fig)
            write_csv(tab_dir / f"{hid}_auf{K}_per_seed.csv", ev["rows"])
            write_csv(tab_dir / f"{hid}_per_dataset.csv",
                      [{"dataset": d, **{k: x for k, x in v.items()
                                         if k != "deltas"}}
                       for d, v in ev["per_dataset"].items()])
            write_csv(tab_dir / f"{hid}_by_cluster.csv",
                      [{"cluster": c, **v} for c, v in
                       ev["secondary"]["by_cluster"].items()])
            write_csv(tab_dir / f"{hid}_swap_activity.csv",
                      ev["secondary"]["swap_activity"])
        elif ev and hid == "H4":
            crit_fig = fig_dir / f"F{fig_no}_{hid}_effect_per_dataset.png"
            fig_pairwise_strip(ev, cells, run_ids, crit_fig)
            write_csv(tab_dir / f"{hid}_pairwise.csv",
                      [{k: v for k, v in p.items() if k != "diffs"}
                       for p in ev["pairs"]])
            write_csv(tab_dir / f"{hid}_per_dataset.csv",
                      [{"dataset": d, **{f"auf_{m}": x for m, x in
                                         ev["means"][d].items()}}
                       for d in sorted(ev["means"])])
            arms4 = (ev["focal"], ev["pairs"][0]["opponent"])
            ev["table3"] = table3_comparison(cells, units, arms4)
            ev["compute"] = compute_per_arm(units, arms4)
            ev["two_by_two"] = h4_two_by_two(experiment_id, cells, K)
            ev["budget_compare"] = h4_budget_compare(experiment_id, cells,
                                                     units, K)
            # The per-dataset effect in the shape fig_effect_vs_size reads.
            shape = {}
            for u in units:
                shape.setdefault(u["dataset"], (u["n_rows"], u["n_features"]))
            p0 = ev["pairs"][0]
            ev["size_ev"] = {
                "challenger": ev["focal"], "baseline": p0["opponent"],
                "K": K, "datasets": sorted(p0["diffs"]),
                "per_dataset": {d: {"effect": x, "n": shape.get(d, (0, 0))[0],
                                    "p": shape.get(d, (0, 0))[1]}
                                for d, x in p0["diffs"].items()}}
            write_csv(tab_dir / f"{hid}_table3.csv",
                      [{"method": m, **e} for m, es in
                       ev["table3"]["per_method"].items() for e in es])
            write_csv(tab_dir / f"{hid}_compute.csv", ev["compute"])
        elif ev:
            fig_pairwise(ev, run_ids, crit_fig)
            write_csv(tab_dir / f"{hid}_pairwise.csv",
                      [{k: v for k, v in p.items() if k != "diffs"}
                       for p in ev["pairs"]])
        figures.append((fig_no, crit_fig, hid, "criterion"))
        per_h.append({"hid": hid, "sec": sec, "K": K, "ev": ev, "arms": arms,
                      "crit_fig": crit_fig, "fig_no": fig_no,
                      "sec_ext": sec_ext})

    arms_all = list(dict.fromkeys(a for h in per_h for a in h["arms"]))
    K0 = per_h[0]["K"]
    extra = []
    field = [h["ev"] for h in per_h if h["hid"] in ("H5", "H6") and h["ev"]]
    field_figs = ()
    if field:
        # The whole field at once: who leads in which cluster (H5, H6).
        arms_all = [a for a in FIELD_ARMS if any(u["method"] == a
                                                 for u in units)]
        means = field[0]["means"]
        missing = missing_cells(experiment_id)
        n_feat = {u["dataset"]: u["n_features"] for u in units}
        methods, cols, tab = cluster_rank_table(means)
        write_csv(tab_dir / "cluster_ranks.csv",
                  [{"method": m, **{f"rank_{c}": tab[(m, c)][0] for c in cols},
                    **{f"n_{c}": tab[(m, c)][1] for c in cols}}
                   for m in methods])
        ranks = field_ranks(means)
        write_csv(tab_dir / "per_dataset.csv",
                  [{"dataset": d, "cluster": SWAP_CLUSTERS.get(d),
                    "n_features": n_feat.get(d), "method": m,
                    f"auf_k{K0}": means[d].get(m), "rank": ranks[d].get(m),
                    "missing": missing.get((d, m))}
                   for d in sorted(means) for m in methods])
        field_figs = (("cluster_ranks", fig_cluster_ranks, (means,)),
                      ("ranks_per_dataset", fig_ranks_per_dataset,
                       (means, missing, n_feat)))
        touts = timeout_rows(experiment_id)
        if touts:
            write_csv(tab_dir / "timeouts.csv", touts)
            field_figs += (("timeouts", fig_timeouts, (touts,)),)
    h0 = [h["ev"] for h in per_h if h["ev"] and h["ev"]["kind"] == "h0"]
    h0_figs = ((("progress_val_auf10", fig_h0_progress, (h0[0],)),
                ("secondary_deltas", fig_h0_secondary, (h0[0],)))
               if h0 else ())
    units_ev = [h["ev"] for h in per_h
                if h["ev"] and h["ev"]["kind"] == "dataset_unit"]
    unit_figs = ((("effect_vs_size", fig_effect_vs_size, (units_ev,)),)
                 if units_ev else ())
    h4 = [h["ev"] for h in per_h if h["hid"] == "H4" and h["ev"]
          and h["ev"].get("compute")]
    if h4:
        unit_figs += (("compute", fig_compute,
                       (h4[0]["compute"], (h4[0]["focal"],
                                           h4[0]["pairs"][0]["opponent"]))),
                      ("effect_vs_size", fig_effect_vs_size,
                       ([h4[0]["size_ev"]],)),
                      ("table3", fig_table3, (h4[0]["table3"],)))
        if h4[0].get("budget_compare"):
            unit_figs += (("budget_compare", fig_budget_compare,
                           (h4[0]["budget_compare"], h4[0]["focal"],
                            h4[0]["pairs"][0]["opponent"], experiment_id)),)
        if h4[0].get("two_by_two"):
            unit_figs += (("two_by_two", fig_two_by_two,
                           (h4[0]["two_by_two"],)),)
    if len(units_ev) == 2:
        unit_figs += (("swap_success", fig_swap_success, (units_ev,)),
                      ("by_cluster", fig_by_cluster, (units_ev,)))
    # Over 39 datasets and 17 arms the opt(k) grid shows little the rank
    # figures do not; H5/H6 keep the front sizes and the cost.
    generic = ((("opt_curves", fig_opt_curves, (units, arms_all, K0)),)
               if not field else ()) + (
        ("front_size_range", fig_size_range, (units, arms_all)),
        ("cost", fig_cost, (units, arms_all)))
    for slug, fn, args in h0_figs + unit_figs + field_figs + generic:
        fig_no += 1
        p = fig_dir / f"F{fig_no}_{slug}.png"
        if units:
            fn(*args, run_ids, p)
            extra.append((fig_no, p, slug))

    # AUF table over every unit, for the record.
    auf_rows = [{"run_id": u["run_id"], "dataset": u["dataset"],
                 "method": u["method"], "algorithm_id": u["algorithm_id"],
                 "seed": u["seed"], f"auf_k{K0}": auf(u["records"], K0),
                 "auf_k20": auf(u["records"], 20),
                 "min_subset": min_size(u["records"]),
                 # Secondary; comparable only within one dataset.
                 "hypervolume": analysis.hypervolume(u["records"],
                                                     u["n_features"])
                 if u["n_features"] else None,
                 "model_fits": u["model_fits"], "seconds": u["seconds"],
                 "stopped_on": u["stopped_on"]} for u in units if u["records"]]
    write_csv(tab_dir / "run_keys.csv", auf_rows)

    # ---- markdown ------------------------------------------------------
    now = datetime.now(timezone.utc)
    # SUPPORT.md: the record -- what ran, under which rules, with which
    # numbers. The reading of it is REPORT.md, built further down.
    L: List[str] = [f"# {experiment_id} -- supporting record", "",
                    "The record behind [REPORT.md](REPORT.md): the runs, the "
                    "criteria as registered, the parameters, the per-seed "
                    "numbers and how to reproduce them.", ""]

    L += ["## 1. Header", ""]
    run_cells = []
    for r in runs:
        m = r["manifest"] or {}
        run_cells.append(f"`{r['run_id']}` ({m.get('status', 'no manifest')}"
                         f"{'' if m.get('evidence') else ', NOT evidence'})")
    starts = [m["started_utc"] for m in manifests]
    ends = [m.get("ended_utc") for m in manifests if m.get("ended_utc")]
    verdicts = "; ".join(
        f"{h['hid']}: see [REPORT.md](REPORT.md)"
        + (f" (mechanical reading: {h['ev']['reading']})" if h["ev"] else "")
        for h in per_h)
    L += [md_table(("field", "content"), [
        ("Experiment ID", f"`{experiment_id}`"),
        ("Hypothesis ID", ", ".join(hids)),
        ("Run IDs", "<br>".join(run_cells) or "--"),
        ("Algorithm IDs", "<br>".join(f"`{i}`" for a in sorted(algo)
                                      for i in sorted(algo[a])) or "--"),
        ("Pre-registration", f"`{HYPOTHESES_PATH}` at {hsource}"),
        ("Code commits", ", ".join(f"`{c[:7]}`" for c in commits) or "--"),
        ("Dates", f"runs {min(starts) if starts else '--'} to "
                  f"{max(ends) if ends else '--'}; report "
                  f"{now.strftime('%Y-%m-%d')}"),
        ("Verdict", verdicts),
    ]), ""]
    if len(commits) > 1:
        L += ["**Warning:** the runs were made at different commits of the "
              "experiments repo; say in section 4 why that does not matter, or "
              "that it does.", ""]
    if prereg and htext != head_text:
        L += [f"**Note:** `{HYPOTHESES_PATH}` has changed since {hsource}. The "
              f"quotes below are from {hsource}, the version in force when the "
              f"experiment ran.", ""]

    L += ["## 2. Hypothesis", ""]
    for h in per_h:
        if not h["sec"]:
            L += [f"**{h['hid']}: not found in {HYPOTHESES_PATH} at "
                  f"{hsource}.**", ""]
            continue
        lab = labelled(h["sec"])
        L += [quote(h["sec"].splitlines()[0]), ">",
              quote(lab.get("Claim", TODO.format("no Claim paragraph found"))),
              ""]

    L += ["## 3. Evaluation criteria", ""]
    crit_labels = ("Arms", "Algorithms", "Datasets", "Primary metric",
                   "Datasets, budgets and splits",
                   "Primary metric: fits to a common target",
                   "Algorithms, datasets, primary metric", "Analysis",
                   "Analysis: pairwise", "Falsification criterion")
    for h in per_h:
        if not h["sec"]:
            continue
        lab = labelled(h["sec"])
        L += [f"### {h['hid']}", ""]
        if h.get("sec_ext"):
            # The second experiment: its own subsection, plus the arms and the
            # measure it takes from H0 unchanged. The H0 section's first
            # labels come from H0-E01's text, before the subsection.
            base = labelled(h["sec"].split("### " + H0_EXT_TITLE)[0])
            repeat = h["ev"].get("repeat")
            title = H0_REPEAT_TITLE if repeat else H0_EXT_TITLE
            # H0-E03 defines its own arms; it takes only the measure from H0.
            keys = (("Primary metric: fits to a common target",) if repeat
                    else ("Arms", "Primary metric: fits to a common target"))
            L += [f"This experiment is *{title}*; it takes H0's "
                  + ("measure" if repeat else "arms and measure")
                  + " unchanged:", ""]
            for key in keys:
                if key in base:
                    L += [quote(base[key]), ""]
            L += [quote(h["sec_ext"].splitlines()[0]), ""]
            for key, para in labelled(h["sec_ext"]).items():
                if key not in ("Why", "Relation to H0-E01",
                               "Relation to H0-E01 and H0-E02"):
                    L += [quote(para), ""]
            continue
        for key in crit_labels:
            if key in lab:
                L += [quote(lab[key]), ""]
    rev = revisions(htext)
    L += [quote(rev) if rev else f"No revisions section in `{HYPOTHESES_PATH}` "
          f"at {hsource}: the criteria are as pre-registered.", "",
          "Secondary, shown for interpretation only: AUF at the other K, "
          "hypervolume, the smallest subset size on the front, fits and wall "
          "clock.", ""]

    L += ["## 4. Description of the experiment", "", "### Setup", ""]
    for r in runs:
        m = r["manifest"] or {}
        if not m:
            L += [f"**`{r['run_id']}`** -- no manifest: the run ended before "
                  f"writing one, and contributes no data.", ""]
            continue
        ds = m.get("dataset", {})
        L += [f"**`{r['run_id']}`** -- dataset `{ds.get('name', '?')}`: "
              f"{ds.get('n_features', '?')} features, "
              f"{ds.get('n_train', '?')}/{ds.get('n_val', '?')}/"
              f"{ds.get('n_test', '?')} train/val/test rows.",
              "", f"```\n{m.get('command', '?')}\n```", ""]
    params = [m.get("params", {}) for m in manifests]
    if params:
        keys = sorted({k for p in params for k in p})
        L += ["Parameters per run:", "",
              md_table(["parameter"] + [r["run_id"] for r in runs
                                        if r["manifest"]],
                       [[k] + [json.dumps(p.get(k)) for p in params]
                        for k in keys]), ""]
    L += ["Arms:", "", md_table(("arm", "algorithm ID", "what distinguishes it"),
                                [(a, "<br>".join(f"`{i}`" for i in sorted(ids)),
                                  TODO.format("plain-language description"))
                                 for a, ids in sorted(algo.items())]), "",
          "**Deviations from the protocol:** " + TODO.format(
              "each with its reason, or 'none'"), ""]

    L += ["### What happened", ""]
    L += [md_table(("run", "status", "started (UTC)", "ended (UTC)",
                    "elapsed (s)", "results file"),
                   [(f"`{r['run_id']}`", (r["manifest"] or {}).get("status"),
                     (r["manifest"] or {}).get("started_utc"),
                     (r["manifest"] or {}).get("ended_utc"),
                     (r["manifest"] or {}).get("elapsed_seconds"),
                     r["results_source"] or "none")
                    for r in runs]), ""]
    fails = {r["run_id"]: (r["manifest"] or {}).get("failures")
             for r in runs if (r["manifest"] or {}).get("failures")}
    for rid, f in fails.items():
        L += [f"Failures in `{rid}`:", ""] + \
             [f"* `{k}`: {v}" for k, v in f.items()] + [""]
    L += [f"Run keys ({len(units)}; full list in "
          f"[tables/run_keys.csv](tables/run_keys.csv)):", "",
          md_table(("dataset", "arm", "seed", f"AUF K={K0}", "AUF K=20",
                    "hypervolume", "min subset", "fits", "seconds",
                    "stopped on"),
                   [(r["dataset"], r["method"], r["seed"], r[f"auf_k{K0}"],
                     r["auf_k20"], r["hypervolume"], r["min_subset"],
                     r["model_fits"], r["seconds"],
                     json.dumps(r["stopped_on"]) if r["stopped_on"] else "--")
                    for r in auf_rows]), ""]
    empty = [u for u in units if not u["records"]]
    for u in empty:
        notes.append(f"{u['dataset']}/{u['method']}/s{u['seed']} returned an "
                     f"empty front")
    if notes:
        L += ["Flagged by the generator:", ""] + [f"* {n}" for n in notes] + [""]
    if any((r["dir"] / "trajectories").is_dir() for r in runs):
        L += ["Progress curves: every run key's trajectory is in its run's "
              "`trajectories/` directory.", ""]
    else:
        L += ["Progress curves (best score per iteration) are not in these "
              "runs: progress tracking is still to build (HYPOTHESES.md, "
              "*Before the first run*).", ""]
    L += [
          TODO.format("timeline, restarts, anomalies seen during the run, "
                      "and for a failed attempt what was changed and in which "
                      "commit"), ""]

    L += ["## 5. Evidence", "",
          "The numbers the criterion is evaluated on. What they mean is in "
          "[REPORT.md](REPORT.md).", ""]
    for h in per_h:
        ev = h["ev"]
        L += [f"### {h['hid']}: the criterion"
              + (f" (mechanical reading: {ev['reading']})" if ev else ""), ""]
        if ev and ev["kind"] == "paired":
            L += [md_table(("dataset", "seeds", f"{ev['challenger']} ahead",
                            "passes (>= 4/5)"),
                           [(r["dataset"], r["seeds"], r["wins"],
                             "yes" if r["passes"] else "no")
                            for r in ev["per_dataset"]]), "",
                  md_table(("dataset", "seed", ev["baseline"], ev["challenger"],
                            "delta"),
                           [(r["dataset"], r["seed"], r[ev["baseline"]],
                             r[ev["challenger"]], r["delta"])
                            for r in ev["rows"]]), ""]
        elif ev and ev["kind"] == "dataset_unit":
            a, b, p = ev["challenger"], ev["baseline"], ev["primary"]
            L += [f"Primary: the effect (mean over seeds of {a} minus {b}, "
                  f"test AUF, K = {ev['K']}) is positive on {p['positive']} "
                  f"datasets, negative on {p['negative']}, zero on "
                  f"{p['zero']}; median {fmt(p['median_effect'])}; two-sided "
                  f"Wilcoxon p = {fmt(p['p_value'])} over n = "
                  f"{p['n_datasets']} complete datasets.", ""]
            if p["missing"]:
                L += ["Left out, not complete: " + ", ".join(p["missing"])
                      + ".", ""]
            L += [md_table(("dataset", "cluster", "p", "n", "seeds",
                            f"AUF {b}", f"AUF {a}", "effect",
                            f"{a} ahead", "4 of 5"),
                           [(d, v["cluster"], v["p"], v["n"], v["seeds"],
                             fmt(v[f"auf_{b}"]), fmt(v[f"auf_{a}"]),
                             fmt(v["effect"]), v["wins"],
                             "yes" if v["passes_4_of_5"] else "no")
                            for d in ev["datasets"]
                            for v in (ev["per_dataset"][d],)]), ""]
            eo = ev["secondary"]["eodata"]
            L += [f"Secondary, EOData on its own: {a} ahead on {eo['wins']} "
                  f"of {eo['seeds']} seeds (4 of 5 needed to hold there).", "",
                  "Secondary, by cluster (descriptive; too few datasets per "
                  "cluster for a test):", "",
                  md_table(("cluster", "datasets", "mean effect", "> 0", "< 0"),
                           [(c, v["n"], fmt(v["mean_effect"]), v["positive"],
                             v["negative"]) for c, v in
                            ev["secondary"]["by_cluster"].items()]), ""]
            gv = ev["secondary"].get("guided_vs_random")
            if gv:
                L += [f"Secondary, {GUIDANCE[0]} minus {GUIDANCE[1]}, the same "
                      f"test: {gv['positive']} > 0, {gv['negative']} < 0, "
                      f"Wilcoxon p = {fmt(gv['p_value'])} over n = "
                      f"{gv['n_datasets']} -- {gv['reading']}.", ""]
            act = ev["secondary"]["swap_activity"]
            if act:
                L += ["Secondary, what the pruning step did, mean per run:", "",
                      md_table(("dataset", "arm", "pruned", "swaps proposed",
                                "swap fits", "share of fits", "swaps kept",
                                "final front from a swap"),
                               [(r["dataset"], r["method"],
                                 fmt(r["pruned_items"], 1),
                                 fmt(r["swap_proposed"], 1),
                                 fmt(r["swap_fits"], 1),
                                 fmt(r["share_of_fits_on_swaps"], 3),
                                 fmt(r["swap_kept"], 1),
                                 fmt(r["front_from_swap"], 1))
                                for r in act if r["method"] == a]), ""]
        elif ev and ev["kind"] == "h0_ext":
            p = ev["primary"]
            L += [f"Primary: {p['positive']} datasets favour the fixed code, "
                  f"{p['negative']} the 2020 code, {p['zero']} tie; median "
                  f"effect {fmt(p['median_effect_log2'], 3)}; two-sided "
                  f"Wilcoxon p = {fmt(p['p_value'])} over n = "
                  f"{p['n_datasets']} datasets.", ""]
            if ev["missing"]:
                L += ["Left out: " + ", ".join(ev["missing"]) + ".", ""]
            rep = ev.get("repeat")
            L += [md_table(("dataset", "group", "budget", "effect (mean log2)")
                           + (("effect in H0-E01/E02",) if rep else ())
                           + ("seeds", f"{H0_ARMS[1]} faster",
                              f"{H0_ARMS[0]} faster", "ties",
                              f"test AUF {H0_ARMS[1]}", f"test AUF {H0_ARMS[0]}",
                              f"best F1 {H0_ARMS[1]}", f"best F1 {H0_ARMS[0]}"),
                           [(d, v.get("group"), ev["budgets"].get(d),
                             fmt(v["effect_log2"], 3))
                            + ((fmt(v.get("earlier_effect_log2"), 3),)
                               if rep else ())
                            + (v["seeds"], v["faster_fixed"], v["faster_2020"],
                               v["ties"], fmt(v["test_auf10_fixed"]),
                               fmt(v["test_auf10_2020"]),
                               fmt(v.get("best_f1_fixed")),
                               fmt(v.get("best_f1_2020")))
                            for d in ev["datasets"]
                            for v in (ev["per_dataset"][d],)]), "",
                  "Best F1: test weighted F1 of the subset with the best "
                  "validation score on the final front, mean over seeds. "
                  "Shown for interpretation, not part of the criterion.", ""]
            groups = ev["secondary"].get("by_group", {})
            if groups:
                L += ["Secondary, by dataset group:", "",
                      md_table(("group", "datasets", "mean effect",
                                "> 0", "< 0"),
                               [(g, v["n"], fmt(v["mean_effect_log2"], 3),
                                 v["positive"], v["negative"])
                                for g, v in groups.items()]), ""]
            a36 = ev["secondary"].get("all_datasets_including_H0_E01")
            if a36:
                L += [f"Secondary, all datasets including H0-E01's five "
                      f"(seen before this experiment was registered): "
                      f"{a36['positive']} > 0, {a36['negative']} < 0, "
                      f"Wilcoxon p = {fmt(a36['p_value'])} over n = "
                      f"{a36['n_datasets']}.", ""]
        elif ev and ev["kind"] == "h0":
            L += [md_table(("dataset", "seeds", f"{H0_ARMS[1]} faster",
                            f"{H0_ARMS[0]} faster", "ties", "counts for"),
                           [(d, v["seeds"], v["faster_fixed"],
                             v["faster_2020"], v["ties"], v["counts_for"])
                            for d in ev["datasets"]
                            for v in (ev["per_dataset"][d],)]), "",
                  md_table(("dataset", "seed", "target (val. AUF)",
                            f"fits, {H0_ARMS[0]}", f"fits, {H0_ARMS[1]}",
                            "faster"),
                           [(r["dataset"], r["seed"], r["target"],
                             r["fits_to_target_2020"],
                             r["fits_to_target_fixed"], r["faster"])
                            for d in ev["datasets"] for r in ev["rows"]
                            if r["dataset"] == d]), ""]
        elif ev:
            L += [md_table(("opponent", "datasets", "W", "T", "L",
                            "mean delta", "p", "p (Holm)"),
                           [(p["opponent"], p["n_datasets"], p["wins"],
                             p["ties"], p["losses"], p["mean_delta"], p["p"],
                             p["p_holm"]) for p in ev["pairs"]]), ""]
            if ev.get("means"):
                L += [md_table(("dataset",) + tuple(
                          f"AUF {m}" for m in (ev["focal"],) + tuple(
                              p["opponent"] for p in ev["pairs"])),
                          [(d,) + tuple(fmt(ev["means"][d].get(m))
                                        for m in (ev["focal"],) + tuple(
                                            p["opponent"]
                                            for p in ev["pairs"]))
                           for d in sorted(ev["means"])]), ""]
            t3 = ev.get("table3")
            if t3:
                L += [f"Secondary, against the paper's Table 3 (values not "
                      f"directly comparable: our split and selection differ). "
                      f"The paper's ordering claim -- "
                      f"{t3['paper_claim']} -- agrees with ours on "
                      f"{t3['ordering_agreement']} datasets.", "",
                      md_table(("method", "datasets", "mean delta",
                                "mean |delta|", "ours above paper",
                                "rank correlation"),
                               [(m, sm["n_datasets"], sm["mean_delta"],
                                 sm["mean_abs_delta"], sm["ours_above_paper"],
                                 sm["rank_correlation"])
                                for m, sm in sorted(t3["summary"].items())]),
                      ""]
            tbt = ev.get("two_by_two")
            if tbt:
                L += ["Secondary, H4 across classifiers (H4-E01 tree, H4-E02 "
                      "ELM): per-dataset differences of mean AUF (K = 20).",
                      "",
                      md_table(("comparison", "datasets", "> 0", "< 0",
                                "mean", "median", "Wilcoxon p"),
                               [(k, v["n"], v["positive"], v["negative"],
                                 fmt(v["mean"]), fmt(v["median"]),
                                 fmt(v["p"]))
                                for k, v in tbt["summary"].items()]), "",
                      md_table(("dataset",) + tuple(
                          f"{m} / {c}" for m, cl in H4_CELLS.items()
                          for c in cl),
                          [(d,) + tuple(fmt(v[lab]) for cl in
                                        H4_CELLS.values()
                                        for lab in cl.values())
                           for d, v in tbt["per_dataset"].items()]), ""]
            comp = ev.get("compute")
            if comp:
                L += ["Compute per run, mean over seeds:", "",
                      md_table(("dataset", "arm", "runs", "fits",
                                "CPU s", "wall s", "stopped on"),
                               [(r["dataset"], r["method"], r["runs"],
                                 fmt(r["fits"], 0), fmt(r["cpu_seconds"], 1),
                                 fmt(r["wall_seconds"], 1),
                                 ", ".join(r["stopped_on"]))
                                for r in comp]), ""]
    if h0:
        L += [f"### Secondary measures, {H0_ARMS[1]} minus {H0_ARMS[0]}", "",
              "Per seed, summarised per dataset (percent for relative "
              "measures):", "",
              md_table(("dataset", "measure", "seeds",
                        f"{H0_ARMS[1]} higher", "mean", "min", "max"),
                       [(r["dataset"], r["measure"], r["seeds"],
                         r["fixed_higher"], r["mean_delta"],
                         r["min_delta"], r["max_delta"])
                        for r in h0_secondary_summary(h0[0])]), ""]
    L += ["Figures, all in [figures/](figures/): "
          + ", ".join(f"`{p.name}`" for p in
                      [h["crit_fig"] for h in per_h] + [e[1] for e in extra])
          + f". Every figure is drawn from all {len(run_ids)} runs above.", ""]

    L += ["## 6. Reproduction", "",
          "From a clean checkout of both repositories at the commits in the "
          "header:", "", "```"]
    L += [f"python experiments/{r['manifest']['command']}"
          for r in runs if r["manifest"]]
    if any(h["ev"] and h["ev"]["kind"] == "h0_ext" for h in per_h):
        plan = ("repeat" if any(h["ev"].get("repeat") for h in per_h
                                if h["ev"]) else "extension")
        L += [f"# or all at once: python experiments/run_h0.py --experiment "
              f"{experiment_id} --plan {plan} --jobs 12"]
    if h0:
        L += ["python experiments/h0_convergence.py " + " ".join(
            f"results/{r['run_id']}" for r in runs if r["manifest"])
            + f" --out results/{experiment_id}"]
    L += [f"python experiments/make_report.py --experiment {experiment_id} "
          f"--runs {' '.join(run_ids)}", "```", ""]

    write_md(out_dir, "SUPPORT", L, force)

    # REPORT.md: the reading, for someone who has not followed the
    # experiment. Three sections: in brief, the findings one at a time, and an
    # assessment in the register of a paper. The record stays in SUPPORT.md.
    readings = ", ".join(f"{h['hid']}: {h['ev']['reading']}"
                         for h in per_h if h["ev"])
    R: List[str] = [
        f"# {experiment_id} -- report", "",
        f"*Hypothesis {', '.join(hids)}. The runs, the criteria as registered, "
        f"the per-seed numbers and how to reproduce them are in "
        f"[SUPPORT.md](SUPPORT.md).*", "",
        "## 1. In brief", "",
        "### The hypothesis", "",
        TODO.format("what it says, in two or three plain sentences; no "
                    "jargon a reader outside the project would not know"), "",
        "**How it is judged.** " + TODO.format(
            "the falsification criterion, in plain words"), "",
        "### The answer: " + TODO.format(
            f"confirmed / not confirmed (mechanical reading -- {readings})"),
        "",
        TODO.format("why, in two to four plain sentences, with the one number "
                    "that decides it"), ""]
    for h in per_h:
        rel = h["crit_fig"].relative_to(out_dir).as_posix()
        R += [f"![{h['hid']}: the criterion]({rel})", "",
              f"*{TODO.format('one-line caption: what each point is')}*", ""]

    R += ["## 2. Findings", "",
          "One finding at a time: the statement, what it rests on, and the "
          "figure that shows it.", ""]
    figs = [(h["crit_fig"], f"{h['hid']} criterion") for h in per_h] + \
        [(p, slug) for _, p, slug in extra]
    for i, (p, slug) in enumerate(figs, 1):
        R += [f"### F{i} -- " + TODO.format(
                  f"the finding as one sentence, or delete (figure: {slug})"),
              "", TODO.format("explanation: what was measured, the numbers, "
                              "what they mean; a short table if it helps"), "",
              f"![F{i}]({p.relative_to(out_dir).as_posix()})", "",
              f"*{TODO.format('caption: what is plotted, axes, split')}*", ""]

    R += ["## 3. Assessment", "",
          TODO.format("the hypothesis judged on the findings, written as for a "
                      "paper's results and discussion: what is supported and "
                      "how strongly, effect sizes with their spread, what the "
                      "result does not show, the limits of the seeds, datasets "
                      "and budget, and what follows for later hypotheses"), ""]
    return write_md(out_dir, "REPORT", R, force)


def write_md(out_dir: Path, stem: str, lines: Sequence[str],
             force: bool) -> Path:
    """Write <stem>.md, or <stem>.skeleton.md beside a hand-written one."""
    target = out_dir / f"{stem}.md"
    if target.exists() and not force:
        target = out_dir / f"{stem}.skeleton.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", required=True)
    ap.add_argument("--runs", nargs="*", default=None,
                    help="run IDs; default: the experiment's runs in the ledger")
    ap.add_argument("--out", default=None, help="default: "
                    "experiments/reports/<experiment ID>")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing REPORT.md")
    args = ap.parse_args()

    run_ids = args.runs
    if run_ids is None:
        row = experiment_ids.find(experiment_ids.load_ledger(), args.experiment)
        if row is None:
            raise SystemExit(f"{args.experiment} is not in the ledger; pass "
                             f"--runs")
        run_ids = row["runs"]
    missing = [r for r in run_ids if not (RESULTS_DIR / r).is_dir()]
    if missing:
        raise SystemExit(f"no results directory for: {missing}")
    out = Path(args.out) if args.out else \
        experiment_ids.REPORTS_DIR / args.experiment
    path = build(args.experiment, run_ids, out, force=args.force)
    print(f"wrote {path}, and SUPPORT.md beside it")
    print(f"figures: {out / 'figures'}")
    if path.name == "REPORT.skeleton.md":
        print("REPORT.md exists and was left alone; merge from the skeleton. "
              "SUPPORT.md is treated the same way.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
