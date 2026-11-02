"""H14: P2's pilot -- starts over all sizes, an OBL budget sweep, forced mutation.

The criterion as registered for H14-E01 (HYPOTHESES.md, H14; EXPERIMENTS.md,
H14-E01; DEC-56), on its 200 runs, read from `experiments/distilled_logs/
H14-E01/` (runs, final fronts, archive trajectories) and the runs' subset logs
(`results/<run>/subsets/*.npz`, `subset_log.py`), which this script reduces to
`tables/subset_summary.csv` so that the report reads from committed tables.

Per seed, as H1: a comparison holds on a dataset if it holds in at least
4 of 5 seeds (paired by seed number), and a part holds if it holds on at
least 3 of the 4 datasets.

(i)   `p2_uniform` and `p2_loguniform` against `p2_sparse`: (i-a) the final
      front reaches k <= 10; (i-b) best test F1 at any size at least
      `p2_sparse`'s; (i-c) AUF (K = 10) no more than 0.01 below. A start is
      supported if (i-a), (i-b) and (i-c) hold.
(ii)  `p2_obl`, `_b3`, `_b10`: (ii-a) the share of seeds reaching k <= 10
      does not fall with budget on any dataset; (ii-b) at 10x it is below 1
      on Earthquakes or Computers. Supported if both hold.
(iii) `p2_sparse` and `p2_loguniform`, `_min1` against balanced: (iii-a)
      repeat share (cache hits / proposals) at most half; (iii-b) AUF
      (K = 10) higher. Supported if both hold for both starts.

    python experiments/distill_results.py
    python experiments/h14_report.py          # -> reports/H14-E01/{tables,figures}
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

import _bootstrap  # noqa: F401
import h13_coverage as cov
from make_report import GRID, INK_2, SERIES, _style
import provenance
import subset_log

HERE = Path(__file__).resolve().parent
EXPERIMENT = "H14-E01"
DISTILLED = HERE / "distilled_logs" / EXPERIMENT
REPORTS = HERE / "reports"
DATASETS = ("Adiac", "Strawberry", "Earthquakes", "Computers")
LARGE = ("Earthquakes", "Computers")
SEEDS = tuple(range(2025, 2030))
STARTS = ("obl", "sparse", "uniform", "loguniform")
SWEEP = {"p2_obl": 1, "p2_obl_b3": 3, "p2_obl_b10": 10}
SEED_RULE, DATASET_RULE = 4, 3
MARGIN_I = 0.01
LABEL = {"p2_obl": "OBL", "p2_sparse": "1-30", "p2_uniform": "uniform 1..d",
         "p2_loguniform": "log-uniform 1..d", "p2_obl_b3": "OBL 3x",
         "p2_obl_b10": "OBL 10x"}
for _s in STARTS:
    LABEL[f"p2_{_s}_min1"] = LABEL[f"p2_{_s}"] + ", min1"
COLOR = {"p2_obl": SERIES[1], "p2_sparse": SERIES[0], "p2_uniform": SERIES[3],
         "p2_loguniform": SERIES[2], "p2_obl_b3": SERIES[4], "p2_obl_b10": SERIES[6]}


# ------------------------------------------------------------------ inputs
def load_runs() -> List[Dict]:
    runs = pd.read_csv(DISTILLED / "runs.csv.xz")
    recs = pd.read_csv(DISTILLED / "records.csv.xz")
    curves = pd.read_csv(DISTILLED / "curves.csv.xz")
    rec_by = {k: g.to_dict("records") for k, g in recs.groupby(["run_id", "method", "seed"])}
    cur_by = {k: g.to_dict("records") for k, g in curves.groupby(["run_id", "method", "seed"])}
    out = []
    for r in runs.to_dict("records"):
        if not str(r["method"]).startswith("p2_"):
            continue
        key = (r["run_id"], r["method"], r["seed"])
        base = int(json.loads(r["params"])["evaluation_budget_per_seed"])
        budget = base * (SWEEP.get(r["method"], 1))
        d = int(r["dataset_n_features"])
        records = rec_by.get(key, [])
        out.append({"run_id": r["run_id"], "dataset": r["dataset"], "method": r["method"],
                    "seed": int(r["seed"]), "d": d, "base_budget": base, "budget": budget,
                    "fits": int(r["model_fits"]), "iterations": int(r["iterations"]),
                    "stopped_on": r.get("stopped_on") if isinstance(r.get("stopped_on"), str)
                    else "budget",
                    "seconds": float(r["elapsed_seconds"]),
                    "start_hash": r.get("start_population_sha256"),
                    "algorithm_id": r["algorithm_id"],
                    **cov.run_measures(records, d),
                    "ttr": cov.time_to_reach(cur_by.get(key, []), budget)})
    return out


def subset_summary(runs: List[Dict], cached: Optional[Path]) -> Dict:
    """(method, dataset, seed) -> totals from the run's subset log; read from
    `cached` (the committed table) when the logs are not on disk."""
    out = {}
    if cached is not None and cached.is_file():
        for r in csv.DictReader(open(cached, encoding="utf-8")):
            out[(r["method"], r["dataset"], int(r["seed"]))] = {
                k: float(v) for k, v in r.items() if k not in ("method", "dataset", "seed", "run_id")}
        if len(out) >= len(runs):
            return out
    for r in runs:
        p = provenance.RESULTS_DIR / r["run_id"] / "subsets" / f"{r['method']}_seed{r['seed']}.npz"
        if not p.is_file():
            continue
        z = subset_log.read(p)
        g = {f: int(z[f"gen_{f}"].sum()) for f in subset_log.GEN_FIELDS if f != "generation"}
        after0 = z["gen_generation"] > 0
        children = int(z["gen_proposals"][after0].sum())
        k_med = float(np.median(z["sub_size"])) if len(z["sub_size"]) else float("nan")
        out[(r["method"], r["dataset"], r["seed"])] = {
            **{k: float(v) for k, v in g.items()},
            "repeat_share": g["cache_hits"] / g["proposals"] if g["proposals"] else float("nan"),
            "unchanged_share": (z["gen_unchanged_by_mutation"][after0].sum() / children
                                if children else float("nan")),
            "median_scored_size": k_med,
            "expected_flips_2k_over_d": (cov.expected_flips(k_med, r["d"])
                                         if 0 < k_med < r["d"] else float("nan")),
            "scored_subsets": float(len(z["sub_size"]))}
    return out


def by_seed(runs, method, dataset) -> Dict[int, Dict]:
    return {r["seed"]: r for r in runs if r["method"] == method and r["dataset"] == dataset}


# --------------------------------------------------------------- criterion
def seedwise(runs, a: str, b: str, pred, part: str, **meta) -> List[Dict]:
    """Per dataset: in how many seeds (paired by number) pred(run_a, run_b)."""
    out = []
    for ds in DATASETS:
        A, B = by_seed(runs, a, ds), by_seed(runs, b, ds) if b else {}
        seeds = sorted(set(A) & set(B)) if b else sorted(A)
        hits = [s for s in seeds if pred(A[s], B.get(s))]
        out.append({"part": part, "a": a, "b": b or "", "dataset": ds,
                    "n_seeds": len(seeds), "seeds_holding": len(hits),
                    "holds": len(hits) >= SEED_RULE, **meta})
    return out


def part_holds(rows) -> bool:
    return sum(r["holds"] for r in rows) >= DATASET_RULE


def criterion(runs, subs) -> (List[Dict], Dict):
    rows, verdict = [], {}
    # (i)
    for start in ("p2_uniform", "p2_loguniform"):
        ra = seedwise(runs, start, None, lambda x, _: bool(x["reach"][-1]), "i-a")
        rb = seedwise(runs, start, "p2_sparse",
                      lambda x, y: x["best_f1"] >= y["best_f1"], "i-b")
        rc = seedwise(runs, start, "p2_sparse",
                      lambda x, y: x["auf_k10"] >= y["auf_k10"] - MARGIN_I, "i-c")
        rows += ra + rb + rc
        parts = {"i-a": part_holds(ra), "i-b": part_holds(rb), "i-c": part_holds(rc)}
        verdict[f"(i) {start}"] = {**parts, "supported": all(parts.values())}
    # (ii)
    R = {(m, ds): float(np.mean([bool(r["reach"][-1]) for r in by_seed(runs, m, ds).values()]))
         if by_seed(runs, m, ds) else float("nan") for m in SWEEP for ds in DATASETS}
    for ds in DATASETS:
        vals = [R[(m, ds)] for m in SWEEP]
        rows.append({"part": "ii-a", "dataset": ds, "a": "p2_obl..b10",
                     **{f"R_{m}": R[(m, ds)] for m in SWEEP},
                     "holds": bool(vals[0] <= vals[1] <= vals[2])})
    ii_a = all(r["holds"] for r in rows if r["part"] == "ii-a")
    ii_b = any(R[("p2_obl_b10", ds)] < 1 for ds in LARGE)
    rows.append({"part": "ii-b", "dataset": ",".join(LARGE), "a": "p2_obl_b10",
                 **{f"R_10x_{ds}": R[("p2_obl_b10", ds)] for ds in LARGE}, "holds": ii_b})
    verdict["(ii)"] = {"ii-a": ii_a, "ii-b": ii_b, "supported": ii_a and ii_b}
    # (iii)
    ok3 = []
    for start in ("p2_sparse", "p2_loguniform"):
        m1 = f"{start}_min1"

        def rep(x):
            return subs.get((x["method"], x["dataset"], x["seed"]), {}).get("repeat_share", np.nan)

        ra = seedwise(runs, m1, start, lambda x, y: rep(x) <= 0.5 * rep(y), "iii-a")
        rb = seedwise(runs, m1, start, lambda x, y: x["auf_k10"] > y["auf_k10"], "iii-b")
        rows += ra + rb
        parts = {"iii-a": part_holds(ra), "iii-b": part_holds(rb)}
        verdict[f"(iii) {start}"] = parts
        ok3.append(all(parts.values()))
    verdict["(iii)"] = {"supported": all(ok3)}
    for start in ("p2_obl", "p2_uniform"):     # beside: the dense starts
        rows += seedwise(runs, f"{start}_min1", start,
                         lambda x, y: x["auf_k10"] > y["auf_k10"], "beside iii-b")
    return rows, verdict


# ------------------------------------------------------------------ beside
def per_arm(runs, subs) -> List[Dict]:
    """Per arm and dataset: reach, AUF, best F1, front sizes, fits, stops,
    time to reach (KM) and repeat share, over seeds."""
    out = []
    by = defaultdict(list)
    for r in runs:
        by[(r["method"], r["dataset"])].append(r)
    for (m, ds), rs in sorted(by.items()):
        t = [x["ttr"]["share"] * SWEEP.get(m, 1) for x in rs]   # in base budgets
        e = [x["ttr"]["reached"] for x in rs]
        sub = [subs.get((m, ds, x["seed"]), {}) for x in rs]
        out.append({
            "method": m, "dataset": ds, "d": rs[0]["d"], "n_seeds": len(rs),
            "R": float(np.mean([bool(x["reach"][-1]) for x in rs])),
            "auf_k10": float(np.mean([x["auf_k10"] for x in rs])),
            "auf_k10_min": float(np.min([x["auf_k10"] for x in rs])),
            "auf_k10_max": float(np.max([x["auf_k10"] for x in rs])),
            "auf_k20": float(np.mean([x["auf_k20"] for x in rs])),
            "auf_kd": float(np.mean([x["auf_kd"] for x in rs])),
            "best_f1": float(np.mean([x["best_f1"] for x in rs])),
            "max_front": float(np.median([x["max_front"] for x in rs])),
            "min_front": float(np.median([x["min_front"] for x in rs])),
            "fits": float(np.median([x["fits"] for x in rs])),
            "stagnation": sum(x["stopped_on"] == "stagnation" for x in rs),
            "seconds_median": float(np.median([x["seconds"] for x in rs])),
            "reached_at_start": sum(x["ttr"]["at_start"] for x in rs),
            "reached_by_1x_budget": cov.km_reached_by(t, e, 1.0),
            "median_base_budgets_to_reach": float(np.median([x for x, y in zip(t, e) if y]))
            if any(e) else float("nan"),
            "lost_reach": sum(x["ttr"]["reached"] and not x["reach"][-1] for x in rs),
            "repeat_share": float(np.nanmedian([s.get("repeat_share", np.nan) for s in sub]))
            if sub else float("nan"),
            "unchanged_share": float(np.nanmedian([s.get("unchanged_share", np.nan) for s in sub]))
            if sub else float("nan"),
            "expected_flips_2k_over_d": float(np.nanmedian(
                [s.get("expected_flips_2k_over_d", np.nan) for s in sub])) if sub else float("nan"),
            "forced_flips": float(np.sum([s.get("forced_flips", 0) for s in sub]))})
    return out


def matched(runs) -> List[Dict]:
    """H13's matched-size difference of each new start against `p2_sparse`."""
    out = []
    for start in ("p2_uniform", "p2_loguniform", "p2_obl"):
        for ds in DATASETS:
            A = [r for r in runs if r["method"] == start and r["dataset"] == ds]
            B = [r for r in runs if r["method"] == "p2_sparse" and r["dataset"] == ds]
            if not A or not B:
                continue
            a, b = cov.aggregate(A), cov.aggregate(B)
            reach, quality = cov.decompose(a["r"], a["c_bar"], b["r"], b["c_bar"])
            out.append({"a": start, "b": "p2_sparse", "dataset": ds,
                        "matched": cov.matched_difference(a["r"], a["c_bar"], b["r"], b["c_bar"]),
                        "reach_term": reach, "quality_term": quality,
                        "auf_delta": a["auf_k10"] - b["auf_k10"]})
    return out


def start_check(runs) -> List[Dict]:
    """Arms that differ only in mutation must start from the same population."""
    out = []
    for s in STARTS:
        for ds in DATASETS:
            A, B = by_seed(runs, f"p2_{s}", ds), by_seed(runs, f"p2_{s}_min1", ds)
            for seed in sorted(set(A) & set(B)):
                out.append({"start": s, "dataset": ds, "seed": seed,
                            "same_start": A[seed]["start_hash"] == B[seed]["start_hash"]})
    return out


# ------------------------------------------------------------------ figures
def _footer(fig, note, split):
    fig.text(0.01, 0.01, f"{split} split  |  {note}", fontsize=7, color=INK_2)


def fig_starts(runs, note, path):
    """(i): per dataset and seed, each wide start minus the 1-30 start in
    best F1 at any size and in AUF (K = 10)."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.6))
    x = np.arange(len(DATASETS))
    for ax, (m, lab, thr) in zip(axes, (("best_f1", "best test F1 at any size", 0.0),
                                        ("auf_k10", "AUF (K = 10)", -MARGIN_I))):
        for j, start in enumerate(("p2_uniform", "p2_loguniform")):
            for i, ds in enumerate(DATASETS):
                A, B = by_seed(runs, start, ds), by_seed(runs, "p2_sparse", ds)
                dv = [A[s][m] - B[s][m] for s in sorted(set(A) & set(B))]
                ax.scatter(np.full(len(dv), i + (j - 0.5) * 0.3), dv, s=18,
                           color=COLOR[start], label=LABEL[start] if i == 0 else None)
        ax.axhline(0, color=INK_2, lw=0.8)
        if thr:
            ax.axhline(thr, color=INK_2, lw=0.8, ls="--")
        ax.set_xticks(x, [f"{d}" for d in DATASETS])
        ax.set_title(f"{lab}: start minus the 1-30 start, per seed", fontsize=9.5)
        ax.grid(axis="y", color=GRID)
    axes[0].legend(fontsize=8)
    axes[0].set_ylabel("difference (paired by seed)")
    fig.suptitle("H14 (i): starts over all sizes against the 1-30 start "
                 "(dashed: the -0.01 margin of (i-c))", fontsize=10)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_sweep(runs, note, path):
    """(ii): per dataset, KM share of OBL runs whose archive reaches k <= 10,
    against fits in multiples of the base budget, for 1x, 3x, 10x."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.6), sharey=True)
    for ax, ds in zip(axes, DATASETS):
        for m, mult in SWEEP.items():
            rs = list(by_seed(runs, m, ds).values())
            if not rs:
                continue
            ts, s = cov.km([r["ttr"]["share"] * mult for r in rs], [r["ttr"]["reached"] for r in rs])
            reached = 1 - s if len(s) else np.zeros(0)
            last = reached[-1] if len(reached) else 0.0
            ax.step(np.r_[1e-3, ts, mult], np.r_[0.0, reached, last], where="post",
                    color=COLOR[m], label=f"{LABEL[m]} (R = {np.mean([bool(r['reach'][-1]) for r in rs]):.1f})")
        ax.set_xscale("log")
        ax.set_xlim(0.005, 10)
        ax.set_title(f"{ds} (d = {rs[0]['d'] if rs else '?'})", fontsize=9.5)
        ax.set_xlabel("fits, in multiples of the 1x budget (log)")
        ax.grid(color=GRID)
        ax.legend(fontsize=7.5, loc="upper left")
    axes[0].set_ylabel("share of OBL runs whose archive\nholds a subset of <= 10 features (KM)")
    fig.suptitle("H14 (ii): the OBL start at 1x, 3x and 10x the fit budget; 5 seeds per curve",
                 fontsize=10)
    _footer(fig, note, "validation (archive)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_min1(runs, subs, note, path):
    """(iii): per dataset and seed, repeat share under balanced and min1, and
    min1's AUF (K = 10) minus balanced's, for every start."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(16, 4.8))
    x = np.arange(len(DATASETS))
    for j, s in enumerate(STARTS):
        b, m = f"p2_{s}", f"p2_{s}_min1"
        off = (j - 1.5) * 0.18
        for i, ds in enumerate(DATASETS):
            B, M = by_seed(runs, b, ds), by_seed(runs, m, ds)
            seeds = sorted(set(B) & set(M))
            rb = [subs.get((b, ds, q), {}).get("repeat_share", np.nan) for q in seeds]
            rm = [subs.get((m, ds, q), {}).get("repeat_share", np.nan) for q in seeds]
            axes[0].scatter(np.full(len(rb), i + off), rb, s=16, color=COLOR[b],
                            label=f"{LABEL[b]}, balanced" if i == 0 else None)
            axes[0].scatter(np.full(len(rm), i + off), rm, s=16, color=COLOR[b], marker="x",
                            label=f"{LABEL[b]}, min1" if i == 0 else None)
            axes[1].scatter(np.full(len(seeds), i + off),
                            [M[q]["auf_k10"] - B[q]["auf_k10"] for q in seeds], s=16,
                            color=COLOR[b], label=LABEL[b] if i == 0 else None)
    axes[0].set_ylabel("repeat share: cache hits / proposals")
    axes[1].set_ylabel("AUF (K = 10), min1 minus balanced")
    axes[1].axhline(0, color=INK_2, lw=0.8)
    for ax, t in zip(axes, ("repeat share per run (dot balanced, cross min1)",
                            "min1's AUF gain per seed (same start population)")):
        ax.set_xticks(x, DATASETS)
        ax.set_title(t, fontsize=9.5)
        ax.grid(axis="y", color=GRID)
    axes[0].legend(fontsize=7, ncol=2)
    axes[1].legend(fontsize=7.5)
    fig.suptitle("H14 (iii): a forced flip in children mutation left unchanged", fontsize=10)
    _footer(fig, note, "test (AUF); n/a (repeats)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_flips(runs, subs, note, path):
    """The 2k/d account: share of children balanced mutation left unchanged
    against the expected flips 2k/d at the run's median scored size, with
    e^(-2k/d), the Poisson share of zero flips."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    for s in STARTS:
        b = f"p2_{s}"
        xs = [subs.get((b, r["dataset"], r["seed"]), {}).get("expected_flips_2k_over_d", np.nan)
              for r in runs if r["method"] == b]
        ys = [subs.get((b, r["dataset"], r["seed"]), {}).get("unchanged_share", np.nan)
              for r in runs if r["method"] == b]
        ax.scatter(xs, ys, s=16, color=COLOR[b], label=LABEL[b])
    g = np.logspace(-3, 0.6, 100)
    ax.plot(g, np.exp(-g), color=INK_2, ls="--", lw=1, label="exp(-2k/d)")
    ax.set_xscale("log")
    ax.set_xlabel("expected flips per child, 2k/d (k = the run's median scored size)")
    ax.set_ylabel("share of children mutation\nleft unchanged")
    ax.set_title("Balanced mutation, one point per run (all four datasets)", fontsize=9.5)
    ax.grid(color=GRID)
    ax.legend(fontsize=8)
    _footer(fig, note, "n/a (counts)")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: List[str] = []
    for r in rows:
        keys += [k for k, v in r.items() if k not in keys and not isinstance(v, (dict, list))]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(REPORTS / EXPERIMENT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    tabs, figs = out / "tables", out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    runs = load_runs()
    subs = subset_summary(runs, tabs / "subset_summary.csv")
    write_csv(tabs / "subset_summary.csv",
              [{"method": m, "dataset": d, "seed": s, **v} for (m, d, s), v in sorted(subs.items())])
    crit, verdict = criterion(runs, subs)
    verdict["n_runs"] = len(runs)
    write_csv(tabs / "criterion.csv", crit)
    write_csv(tabs / "per_arm.csv", per_arm(runs, subs))
    write_csv(tabs / "matched.csv", matched(runs))
    write_csv(tabs / "start_check.csv", start_check(runs))
    write_csv(tabs / "run_measures.csv",
              [{k: v for k, v in r.items() if k not in ("reach", "c", "exact", "ttr")}
               | {"reach_k10": bool(r["reach"][-1]), **{f"ttr_{k}": v for k, v in r["ttr"].items()}}
               for r in runs])
    (tabs / "verdict.json").write_text(json.dumps(verdict, indent=1), encoding="utf-8")
    note = f"{len(runs)} runs of H14-E01 (decision tree, Sentinel); h14_report.py"
    fig_starts(runs, note, figs / "F1_starts.png")
    fig_sweep(runs, note, figs / "F2_obl_budget_sweep.png")
    fig_min1(runs, subs, note, figs / "F3_min1.png")
    fig_flips(runs, subs, note, figs / "F4_flips_2k_over_d.png")
    print(json.dumps(verdict, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
