"""H7's evidence: tables and figures from h7_checkpoints.py's output.

    python experiments/h7_report.py --experiment H7-E01

Reads results/<ID>/checkpoints.csv (and, for wall clock at each checkpoint,
the source runs' trajectories) and writes reports/<ID>/tables/*.csv and
reports/<ID>/figures/F*.png. The criterion is HYPOTHESES.md's, H7: per
classifier, FASTENER against sparse NSGA-II and against POSS at 10% and 25%
of the budget, datasets as the unit (mean over seeds), more datasets ahead
than behind and a two-sided Wilcoxon test significant after Holm correction
over the four; supported if all four hold under at least two classifiers,
reversed if a rival meets that against FASTENER.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

import _bootstrap  # noqa: F401
from make_report import (GRID, INK_2, SERIES, SWAP_CLUSTERS, _style, holm,
                         wilcoxon_p)
import provenance

HERE = Path(__file__).resolve().parent
LEARNERS = {"H5H6-E01": "decision tree", "H5H6-E02": "random forest",
            "H5H6-E03": "LightGBM"}
RIVALS = ("nsga2_sparse", "poss")
PRIMARY = (0.10, 0.25)
ARMS = ("fastener", "fastener_swap_guided", "fastener_swap_random",
        "nsga2_sparse", "poss")
LABEL = {"fastener": "FASTENER", "fastener_swap_guided": "FASTENER, guided swap",
         "fastener_swap_random": "FASTENER, random swap",
         "nsga2_sparse": "sparse NSGA-II", "poss": "POSS"}
CLUSTERS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "EO"]


def _footer(fig, note: str, split: str) -> None:
    fig.text(0.01, 0.01, f"{split} split  |  {note}", fontsize=7, color=INK_2)


def load(experiment: str) -> List[Dict]:
    path = provenance.RESULTS_DIR / experiment / "checkpoints.csv"
    with open(path, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in ("checkpoint", "auf_k10", "auf_k10_grid"):
            r[k] = float(r[k])
        for k in ("seed", "budget", "fit_limit", "snapshot_fits"):
            r[k] = int(r[k])
    return rows


def per_dataset(rows) -> Dict:
    """(source, checkpoint, method) -> {dataset: mean AUF over seeds}."""
    acc: Dict = {}
    for r in rows:
        acc.setdefault((r["source"], r["checkpoint"], r["method"]), {}) \
           .setdefault(r["dataset"], []).append(r["auf_k10"])
    return {key: {d: float(np.mean(v)) for d, v in by.items()}
            for key, by in acc.items()}


def pairwise(means, source, c, a, b) -> Dict:
    """a against b over the datasets both have."""
    A, B = means.get((source, c, a), {}), means.get((source, c, b), {})
    ds = sorted(set(A) & set(B))
    d = np.array([A[x] - B[x] for x in ds])
    return {"source": source, "classifier": LEARNERS[source], "checkpoint": c,
            "arm": a, "opponent": b, "n_datasets": len(ds),
            "wins": int((d > 0).sum()), "ties": int((d == 0).sum()),
            "losses": int((d < 0).sum()),
            "mean_delta": float(d.mean()) if len(d) else float("nan"),
            "median_delta": float(np.median(d)) if len(d) else float("nan"),
            "p": wilcoxon_p(d.tolist()), "datasets": ds, "deltas": d.tolist()}


def criterion(means, checkpoints) -> List[Dict]:
    out = []
    for source in LEARNERS:
        for a, b, role in [("fastener", r, "focal") for r in RIVALS] + \
                          [(r, "fastener", "reverse") for r in RIVALS]:
            for c in checkpoints:
                row = pairwise(means, source, c, a, b)
                row["role"] = role
                out.append(row)
        # Holm over the four comparisons of each direction, per classifier.
        for role in ("focal", "reverse"):
            grp = [r for r in out if r["source"] == source and r["role"] == role
                   and r["checkpoint"] in PRIMARY]
            for r, ph in zip(grp, holm([r["p"] for r in grp])):
                r["p_holm"] = ph
                r["holds"] = bool(r["wins"] > r["losses"] and ph < 0.05)
    return out


def verdict(crit) -> Dict:
    def classifiers_meeting(role):
        n = 0
        for source in LEARNERS:
            grp = [r for r in crit if r["source"] == source and r["role"] == role
                   and r["checkpoint"] in PRIMARY]
            n += len(grp) == 4 and all(r["holds"] for r in grp)
        return n
    focal, rev = classifiers_meeting("focal"), classifiers_meeting("reverse")
    word = ("supported" if focal >= 2 else "reversed" if rev >= 2
            else "not supported")
    return {"verdict": word, "classifiers_all_four": focal,
            "classifiers_reversed": rev}


def seconds_at(rows) -> List[Dict]:
    """Wall clock of each run's search at the snapshot each checkpoint used."""
    out, cache = [], {}
    for r in rows:
        key = r["source_run"]
        if key not in cache:
            traj, = sorted((provenance.RESULTS_DIR / key / "trajectories").glob("*.jsonl"))
            fits_secs = []
            with open(traj, encoding="utf-8") as fh:
                for line in fh:
                    s = json.loads(line)
                    fits_secs.append((int(s["fits"]), float(s["seconds"])))
            cache[key] = fits_secs
        secs = [s for f, s in cache[key] if f <= r["fit_limit"]]
        out.append({**{k: r[k] for k in ("source", "dataset", "method", "seed",
                                          "checkpoint")},
                    "seconds": secs[-1] if secs else 0.0})
    return out


# ------------------------------------------------------------------ figures
def fig_criterion(crit, run_note, path):
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=True)
    for ax, source in zip(axes, LEARNERS):
        grp = [r for r in crit if r["source"] == source and r["role"] == "focal"]
        grp.sort(key=lambda r: (r["opponent"], r["checkpoint"]))
        for i, r in enumerate(grp):
            d = np.array(r["deltas"])
            x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(d))
            sig = r.get("holds")
            ax.scatter(x, d, s=14, color=SERIES[0] if r["opponent"] == "poss" else SERIES[1],
                       alpha=0.9 if sig else 0.5,
                       facecolors="none" if not sig else None)
            ax.plot([i - 0.3, i + 0.3], [r["mean_delta"]] * 2, color="k", lw=2)
            ph = r.get("p_holm")
            ax.annotate(f"{r['wins']}-{r['ties']}-{r['losses']}\n"
                        + (f"p={ph:.2g}" if ph is not None else "secondary"),
                        (i, 0), xytext=(0, -40), textcoords="offset points",
                        ha="center", fontsize=7, annotation_clip=False)
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(range(len(grp)),
                      [f"vs {LABEL[r['opponent']]}\n{int(r['checkpoint'] * 100)}%"
                       for r in grp], fontsize=7.5)
        ax.set_title(LEARNERS[source], fontsize=10)
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel("FASTENER's AUF (K = 10) minus the rival's\n(per dataset, mean over seeds)")
    fig.suptitle("FASTENER against its co-leaders part-way through the budget: one "
                 "point per dataset, bar = mean; filled = holds after Holm "
                 "(10% and 25% only)", fontsize=10)
    _footer(fig, run_note, "test")
    fig.tight_layout(rect=(0, 0.06, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_curves(means, checkpoints, run_note, path):
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.8), sharey=True)
    for ax, source in zip(axes, LEARNERS):
        # Datasets every arm has at every checkpoint, so the curves compare.
        common = None
        for a in ARMS:
            for c in checkpoints:
                s = set(means.get((source, c, a), {}))
                common = s if common is None else common & s
        for j, a in enumerate(ARMS):
            y = [np.mean([means[(source, c, a)][d] for d in common])
                 for c in checkpoints]
            ax.plot([c * 100 for c in checkpoints], y, marker="o",
                    color=SERIES[j % len(SERIES)], label=LABEL[a],
                    lw=2.2 if a == "fastener" else 1.3)
        ax.set_xscale("log")
        ax.set_xticks([c * 100 for c in checkpoints],
                      [f"{int(c * 100)}%" for c in checkpoints])
        ax.set_xlabel("share of the fit budget")
        ax.set_title(f"{LEARNERS[source]} ({len(common)} datasets)", fontsize=10)
        ax.grid(color=GRID)
    axes[0].set_ylabel("mean AUF (K = 10), test")
    axes[-1].legend(fontsize=8, loc="lower right")
    fig.suptitle("Mean AUF at each checkpoint, over the datasets every arm has",
                 fontsize=10)
    _footer(fig, run_note, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_clusters(means, run_note, path, c=0.10):
    """FASTENER minus each rival per cluster at one checkpoint."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.4), sharey=True)
    x = np.arange(len(CLUSTERS))
    for ax, source in zip(axes, LEARNERS):
        F = means[(source, c, "fastener")]
        for j, rv in enumerate(RIVALS):
            R = means.get((source, c, rv), {})
            vals = []
            for cl in CLUSTERS:
                ds = [d for d in F if d in R and SWAP_CLUSTERS.get(d, "EO") == cl]
                vals.append(np.mean([F[d] - R[d] for d in ds]) if ds else np.nan)
            ax.bar(x + (j - 0.5) * 0.38, vals, 0.38, label=f"vs {LABEL[rv]}",
                   color=SERIES[j])
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(x, CLUSTERS)
        ax.set_title(LEARNERS[source], fontsize=10)
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel(f"FASTENER minus rival, mean AUF\nat {int(c * 100)}% of the budget")
    axes[-1].legend(fontsize=8)
    fig.suptitle(f"By cluster at {int(c * 100)}% of the budget (descriptive; "
                 "1-7 datasets per cluster)", fontsize=10)
    _footer(fig, run_note, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_seconds(secs, run_note, path, c=0.10):
    """Wall clock to reach a checkpoint, per arm and classifier."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 3, figsize=(17, 4.4), sharey=False)
    for ax, source in zip(axes, LEARNERS):
        data = [[s["seconds"] for s in secs if s["source"] == source
                 and s["method"] == a and s["checkpoint"] == c and s["seconds"] > 0]
                for a in ARMS]
        ax.boxplot(data, showfliers=False)
        ax.set_yscale("log")
        ax.set_xticks(range(1, len(ARMS) + 1), [LABEL[a] for a in ARMS],
                      rotation=25, ha="right", fontsize=8)
        ax.set_title(LEARNERS[source], fontsize=10)
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel(f"search wall clock to {int(c * 100)}% of the budget (s, log)")
    fig.suptitle(f"Time to reach {int(c * 100)}% of the fit budget, one value per run "
                 "(boxes: quartiles; whiskers 1.5 IQR)", fontsize=10)
    _footer(fig, run_note, "n/a")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = [k for k in rows[0] if k not in ("datasets", "deltas")]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--experiment", required=True)
    args = ap.parse_args(argv)
    rows = load(args.experiment)
    checkpoints = sorted({r["checkpoint"] for r in rows})
    means = per_dataset(rows)
    crit = criterion(means, checkpoints)
    v = verdict(crit)
    out = HERE / "reports" / args.experiment
    tabs, figs = out / "tables", out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    write_csv(tabs / "criterion.csv", crit)
    write_csv(tabs / "per_dataset.csv",
              [{"source": s, "checkpoint": c, "method": m, "dataset": d, "auf_k10": a}
               for (s, c, m), by in sorted(means.items()) for d, a in sorted(by.items())])
    secs = seconds_at(rows)
    write_csv(tabs / "seconds.csv", secs)
    (tabs / "verdict.json").write_text(json.dumps(v, indent=1), encoding="utf-8")
    note = f"{len({r['source_run'] for r in rows})} runs; results/{args.experiment}/checkpoints.csv"
    fig_criterion(crit, note, figs / "F1_H7_criterion.png")
    fig_curves(means, checkpoints, note, figs / "F2_auf_by_checkpoint.png")
    c0 = min(checkpoints)   # 10% in H7-E01
    fig_clusters(means, note, figs / f"F3_by_cluster_{int(c0 * 100)}pct.png", c0)
    fig_seconds(secs, note, figs / f"F4_time_to_{int(c0 * 100)}pct.png", c0)
    print(json.dumps(v))
    for r in crit:
        if r["role"] == "focal":
            print(f"{r['classifier']:>14} {int(r['checkpoint']*100):>3}% vs {r['opponent']:<13}"
                  f" {r['wins']}-{r['ties']}-{r['losses']} mean {r['mean_delta']:+.4f}"
                  f" p {r['p']:.3g} holm {r.get('p_holm', float('nan')):.3g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
