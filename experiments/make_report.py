"""Generate the report skeleton for one experiment (see METHODOLOGY.md).

Reads every run of the experiment from `results/<run ID>/`, and writes to
`experiments/reports/<experiment ID>/`:

* `REPORT.md` -- header, the hypothesis and criteria quoted verbatim from
  HYPOTHESES.md at the pre-registration commit, the per-seed tables, the run
  facts, a mechanical reading of the falsification criterion, and every figure,
  with TODO markers where the prose is to be written by hand;
* `figures/F<n>_*.png` -- the candidate figures for the findings;
* `tables/*.csv` -- the numbers behind the tables and figures.

An existing REPORT.md is never overwritten, since it holds hand-written prose;
the new skeleton goes to REPORT.skeleton.md instead (unless --force). Figures
and tables are always regenerated: they are a function of the runs.

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

# H1-H3: the pre-registered paired rule -- the challenger beats the baseline on
# AUF in at least 4 of 5 seeds, on EOData and on at least one other of the
# hypothesis's datasets.
PAIRED = {
    "H1": ("nsga2_sparse", "nsga2"),
    "H2": ("fastener_swap_random", "fastener"),
    "H3": ("fastener_swap_guided", "fastener"),
}
PAIRED_SETS = {"H1": H1_SETS, "H2": DEV_SETS, "H3": DEV_SETS}
PAIRED_MIN_WINS = 4
PAIRED_SEEDS = 5
# H4-H6: per-dataset mean AUF, focal arm against each opponent across datasets.
PAIRWISE = {
    "H4": {"focal": "fs_sds", "opponents": ("fastener",), "n_datasets": 25},
    "H5": {"focal": "fastener", "opponents": None, "n_datasets": 36},
    "H6": {"focal": "fastener_swap_guided", "opponents": None, "n_datasets": 36},
}
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
                "stopped_on": res.get("stopped_on"),
                "iterations": res.get("iterations",
                                      res.get("rounds_completed")),
                "records": res.get("records", []),
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


def evaluate_pairwise(hid: str, cells, K: int) -> Dict[str, Any]:
    spec = PAIRWISE[hid]
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
    cols = min(4, max(1, n))
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(w * cols, h * rows + 0.6),
                             squeeze=False)
    for ax in axes.flat[n:]:
        ax.set_visible(False)
    return fig, list(axes.flat[:n])


def _colors(arms: Sequence[str]) -> Dict[str, str]:
    return {a: SERIES[i % len(SERIES)] for i, a in enumerate(arms)}


def _footer(fig, run_ids: Sequence[str], split: str) -> None:
    import textwrap
    width = int(fig.get_figwidth() * 17)  # characters of 7 pt per inch
    fig.text(0.01, 0.005, textwrap.fill(
        f"{split} split  |  runs: {', '.join(run_ids)}", width),
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
    import matplotlib.pyplot as plt
    _style(plt)
    pairs = ev["pairs"]
    fig, ax = plt.subplots(figsize=(7, 0.45 * max(3, len(pairs)) + 1.2))
    for i, p in enumerate(pairs):
        d = list(p["diffs"].values())
        ax.scatter(d, [i] * len(d), s=24, color=SERIES[0], alpha=0.8,
                   edgecolor="#fcfcfb", linewidth=1, zorder=3)
        if d:
            ax.plot([np.mean(d)] * 2, [i - 0.3, i + 0.3], color=INK, lw=2)
        ax.annotate(f"{p['wins']}-{p['ties']}-{p['losses']}  "
                    f"p_holm={p['p_holm']:.3g}", (1.01, i),
                    xycoords=("axes fraction", "data"), fontsize=7,
                    color=INK_2, va="center")
    ax.axvline(0, color=INK_2, lw=1)
    ax.set_yticks(range(len(pairs)), [p["opponent"] for p in pairs])
    ax.invert_yaxis()
    ax.set_xlabel(f"per-dataset mean AUF (K = {ev['K']}): {ev['focal']} "
                  f"minus opponent  (> 0 favours {ev['focal']})")
    ax.set_title(f"{ev['focal']} against each opponent; one point per dataset, "
                 f"bar = mean; wins-ties-losses")
    _footer(fig, run_ids, "test")
    fig.tight_layout(rect=(0, 0.03, 0.8, 1))
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


def fig_h0_ext_criterion(ev, run_ids, path: Path) -> None:
    """Per dataset: log2(fits 2020 / fits fixed) per seed, bar = the mean."""
    import matplotlib.pyplot as plt
    _style(plt)
    dss = ev["datasets"]
    fig, ax = plt.subplots(figsize=(7.5, 0.28 * max(8, len(dss)) + 1.6))
    for i, ds in enumerate(dss):
        e = [r["effect_log2"] for r in ev["rows"] if r["dataset"] == ds]
        ax.scatter(e, [i] * len(e), s=18, color=SERIES[0], alpha=0.75,
                   edgecolor="#fcfcfb", linewidth=0.8, zorder=3)
        ax.plot([ev["per_dataset"][ds]["effect_log2"]] * 2, [i - 0.35, i + 0.35],
                color=INK, lw=2, zorder=4)
    ax.axvline(0, color=INK_2, lw=1)
    ax.set_yticks(range(len(dss)),
                  [f"{d} ({ev['per_dataset'][d].get('group') or ''})"
                   for d in dss], fontsize=7)
    ax.invert_yaxis()
    p = ev["primary"]
    pv = "--" if p["p_value"] is None else f"{p['p_value']:.3g}"
    ax.set_xlabel("log2(fits to target, 2020 / fixed)  "
                  "(> 0: the fixed code was faster)")
    ax.set_title(f"Per dataset: one point per seed, bar = mean\n"
                 f"{p['positive']} datasets > 0, {p['negative']} < 0, "
                 f"Wilcoxon p = {pv}")
    _footer(fig, run_ids, "validation")
    # The footer lists every run; leave it room below the axis label.
    lines = 1 + len(", ".join(run_ids)) // int(fig.get_figwidth() * 17)
    fig.tight_layout(rect=(0, min(0.35, 0.02 + lines * 0.13
                                  / fig.get_figheight()), 1, 1))
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


def fig_min_size(units, arms, run_ids, path: Path) -> None:
    import matplotlib.pyplot as plt
    _style(plt)
    dss = sorted({u["dataset"] for u in units if u["method"] in arms})
    fig, axes = _grid(plt, max(1, len(dss)))
    col = _colors(arms)
    for ax, ds in zip(axes, dss):
        for i, arm in enumerate(arms):
            v = [min_size(u["records"]) for u in units
                 if u["dataset"] == ds and u["method"] == arm and u["records"]]
            ax.scatter([i] * len(v), v, s=30, color=col[arm],
                       edgecolor="#fcfcfb", linewidth=1.5, zorder=3)
        ax.set_yscale("log")
        ax.set_xticks(range(len(arms)), arms, rotation=20, ha="right")
        ax.set_title(ds)
        ax.set_ylabel("smallest subset on front")
    fig.suptitle("Smallest subset size on the final front, one point per seed",
                 fontsize=10)
    _footer(fig, run_ids, "validation-selected front")
    fig.tight_layout(rect=(0, 0.03, 1, 0.97))
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
        elif hid in PAIRWISE:
            ev = evaluate_pairwise(hid, cells, K)
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
    h0 = [h["ev"] for h in per_h if h["ev"] and h["ev"]["kind"] == "h0"]
    h0_figs = ((("progress_val_auf10", fig_h0_progress, (h0[0],)),
                ("secondary_deltas", fig_h0_secondary, (h0[0],)))
               if h0 else ())
    for slug, fn, args in h0_figs + (
            ("opt_curves", fig_opt_curves, (units, arms_all, K0)),
            ("min_subset_size", fig_min_size, (units, arms_all)),
            ("cost", fig_cost, (units, arms_all))):
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
    L: List[str] = [f"# {experiment_id} -- report", ""]

    L += ["## 1. Header", ""]
    run_cells = []
    for r in runs:
        m = r["manifest"] or {}
        run_cells.append(f"`{r['run_id']}` ({m.get('status', 'no manifest')}"
                         f"{'' if m.get('evidence') else ', NOT evidence'})")
    starts = [m["started_utc"] for m in manifests]
    ends = [m.get("ended_utc") for m in manifests if m.get("ended_utc")]
    verdicts = "; ".join(f"{h['hid']}: " + TODO.format(
        f"verdict (mechanical reading: {h['ev']['reading']})"
        if h["ev"] else "verdict") for h in per_h)
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
              "experiments repo; say in section 5 why that does not matter, or "
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

    L += ["## 4. Summary", "", TODO.format(
        "one paragraph: what was tested, on what, the verdict against the "
        "criterion, with the deciding number and its seed spread"), ""]

    L += ["## 5. Description of the experiment", "", "### Setup", ""]
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

    L += ["## 6. Findings", ""]
    n = 0
    for h in per_h:
        n += 1
        ev = h["ev"]
        L += [f"### Finding {n} -- {h['hid']}: " + TODO.format(
            "claim as a title"), "",
            "**Claim.** " + TODO.format(
                f"the verdict on the pre-registered criterion "
                f"(mechanical reading: {ev['reading'] if ev else 'n/a'})"), "",
            "**Evidence.**", ""]
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
        rel = h["crit_fig"].relative_to(out_dir).as_posix()
        L += [f"![Finding {n}]({rel})", "",
              f"*Figure {h['fig_no']}.* " + TODO.format(
                  "what is plotted, axes, split, what the points/band show"),
              f" Runs: {', '.join(f'`{r}`' for r in run_ids)}.", "",
              "**Bearing on the hypothesis.** " + TODO.format(
                  "supports / contradicts / neutral, and why"), ""]
    L += ["Candidate figures for further (exploratory) findings. Delete the "
          "ones no finding uses; a finding without a figure is not a "
          "finding.", ""]
    for no, p, slug in extra:
        L += [f"### Finding {n + 1} (exploratory) -- " + TODO.format(
                  f"claim, or delete (figure: {slug})"), "",
              "**Claim.** " + TODO.format("") + "", "",
              "**Evidence.** " + TODO.format("") + "", ""]
        if slug == "secondary_deltas" and h0:
            L += [f"{H0_ARMS[1]} minus {H0_ARMS[0]} per seed, summarised per "
                  f"dataset (percent for relative measures):", "",
                  md_table(("dataset", "measure", "seeds",
                            f"{H0_ARMS[1]} higher", "mean", "min", "max"),
                           [(r["dataset"], r["measure"], r["seeds"],
                             r["fixed_higher"], r["mean_delta"],
                             r["min_delta"], r["max_delta"])
                            for r in h0_secondary_summary(h0[0])]), ""]
        L += [f"![{slug}]({p.relative_to(out_dir).as_posix()})", "",
              f"*Figure {no}.* " + TODO.format("caption") +
              f" Runs: {', '.join(f'`{r}`' for r in run_ids)}.", "",
              "**Bearing on the hypothesis.** " + TODO.format("") + "", ""]
        n += 1

    L += ["## 7. Limitations and open questions", "",
          TODO.format("what the seeds, datasets and budget cannot answer; what "
                      "a later experiment should take up"), ""]

    L += ["## 8. Reproduction", "",
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

    target = out_dir / "REPORT.md"
    if target.exists() and not force:
        target = out_dir / "REPORT.skeleton.md"
    target.write_text("\n".join(L), encoding="utf-8")
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
    print(f"wrote {path}")
    print(f"figures: {out / 'figures'}")
    if path.name == "REPORT.skeleton.md":
        print("REPORT.md exists and was left alone; merge from the skeleton.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
