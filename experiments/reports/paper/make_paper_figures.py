"""Figures and tables for the summary paper (experiments/reports/paper).

Reads only the committed report tables of H5H6-E01 and H5H6-E02 and writes
figures/P*.png and paper_data.json, which build_paper.js turns into the
Word document.

    python experiments/reports/paper/make_paper_figures.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPORTS = HERE.parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)

EXPS = {"H5H6-E01": "decision tree", "H5H6-E02": "random forest",
        "H5H6-E03": "LightGBM"}
CLUSTERS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "EO"]
SEARCHES = ["fastener", "fastener_swap_guided", "fastener_swap_random",
            "nsga2_sparse", "nsga2", "nsgaii_miip", "poss", "fs_sds"]
FILTERS = ["boruta", "rfe_tree", "tree_importance", "mrmr", "hsic_lasso",
           "relieff", "kbest_mutual_info", "kbest_anova_f"]
LABEL = {
    "fastener": "FASTENER", "fastener_swap_guided": "FASTENER guided",
    "fastener_swap_random": "FASTENER random swap", "nsga2_sparse": "NSGA-II sparse",
    "nsga2": "NSGA-II (OBL)", "nsgaii_miip": "NSGAII-MIIP", "poss": "POSS",
    "fs_sds": "FS-SDS", "boruta": "Boruta", "rfe_tree": "RFE",
    "tree_importance": "tree importance", "mrmr": "mRMR", "hsic_lasso": "HSIC Lasso",
    "relieff": "ReliefF", "kbest_mutual_info": "MI ranker",
    "kbest_anova_f": "ANOVA-F ranker", "random": "random subsets",
    "all_features": "all features",
}


def load(exp):
    t = REPORTS / exp / "tables"
    rk = pd.read_csv(t / "run_keys.csv")
    pdx = pd.read_csv(t / "per_dataset.csv")
    clus = pdx[["dataset", "cluster"]].drop_duplicates().set_index("dataset")["cluster"]
    rk["cluster"] = rk["dataset"].map(clus)
    return rk, pdx


data = {}
for exp in EXPS:
    rk, pdx = load(exp)
    g = rk.groupby("method")["seconds"]
    time = pd.DataFrame({"runs": g.size(), "median_s": g.median(),
                         "p90_s": g.quantile(0.9), "max_s": g.max(),
                         "total_h": g.sum() / 3600})
    auf = pdx.pivot_table(index="method", columns="cluster", values="auf_k10", aggfunc="mean")
    auf["all"] = pdx.groupby("method")["auf_k10"].mean()
    # Datasets each mean rests on; a method missing some of a cluster's
    # datasets (timed out or skipped) is marked in the paper's tables.
    n = pdx.pivot_table(index="method", columns="cluster", values="auf_k10", aggfunc="count")
    n["all"] = pdx.groupby("method")["auf_k10"].count()
    size = pdx.groupby("cluster")["dataset"].nunique()
    size["all"] = pdx["dataset"].nunique()
    rank = pd.read_csv(REPORTS / exp / "tables" / "cluster_ranks.csv").set_index("method")
    # Best search against best filter/ranker, per cluster, among the methods
    # with a result on every dataset of the cluster.
    gap = []
    for c in CLUSTERS:
        full = [m for m in auf.index if n.loc[m, c] == size[c]]
        s = auf.loc[[m for m in SEARCHES if m in full], c].dropna()
        f = auf.loc[[m for m in FILTERS if m in full], c].dropna()
        gap.append({"cluster": c, "best_search": s.idxmax(), "search_auf": s.max(),
                    "best_filter": f.idxmax(), "filter_auf": f.max(),
                    "gap": s.max() - f.max()})
    data[exp] = {
        "time": time.reset_index().to_dict("records"),
        "auf": auf.reset_index().to_dict("records"),
        "auf_n": n.reset_index().to_dict("records"),
        "cluster_size": {k: int(v) for k, v in size.items()},
        "rank_all": rank["rank_all"].to_dict(),
        "gap": gap,
    }

# P1: cost against score, per method, both learners. The OBL-started NSGA-II
# searches score far below the rest; they are drawn at the bottom edge.
MARKERS = "osD^vP*Xh"
STYLE = {}
for group, colour in ((["fastener", "fastener_swap_guided", "fastener_swap_random"], "tab:blue"),
                      (["nsga2_sparse", "poss", "fs_sds", "nsga2", "nsgaii_miip"], "tab:orange"),
                      (FILTERS, "tab:green"), (["random"], "tab:gray")):
    for i, m in enumerate(group):
        STYLE[m] = (colour, MARKERS[i])
FLOOR = 0.575
fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=True)
for ax, (exp, learner) in zip(axes, EXPS.items()):
    time = pd.DataFrame(data[exp]["time"]).set_index("method")
    auf = pd.DataFrame(data[exp]["auf"]).set_index("method")["all"]
    for m, (col, mk) in STYLE.items():
        y = auf[m]
        low = y < FLOOR
        ax.scatter(time.loc[m, "median_s"], FLOOR + 0.003 if low else y, s=60,
                   color=col, marker=mk, zorder=3, edgecolor="k", linewidth=0.4,
                   label=LABEL[m] + (" *" if m in ("nsga2", "nsgaii_miip") else ""))
    ax.set_xscale("log")
    ax.set_ylim(FLOOR, 0.705)
    ax.set_xlabel("median wall clock per run (s, log)")
    ax.set_title(f"{exp}: {learner}" + (" (1 core, workstation)" if exp == "H5H6-E01"
                                        else " (8 cores, Vega)"), fontsize=10)
    ax.grid(alpha=0.3)
axes[0].set_ylabel("mean AUF (K = 10) over datasets")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="center right", fontsize=8, frameon=False)
fig.text(0.845, 0.06, "* mean AUF 0.17-0.39, below the axis;\n  drawn at its edge", fontsize=7.5)
fig.tight_layout(rect=(0, 0, 0.845, 1))
fig.savefig(FIG / "P1_cost_vs_score.png", dpi=150)
plt.close(fig)

# P2: best search minus best filter, per cluster, both learners.
fig, ax = plt.subplots(figsize=(13, 4.4))
x = np.arange(len(CLUSTERS))
for i, (exp, learner) in enumerate(EXPS.items()):
    gaps = [r["gap"] for r in data[exp]["gap"]]
    bars = ax.bar(x + (i - 1) * 0.27, gaps, 0.27, label=learner,
                  color=["tab:olive", "tab:purple", "tab:cyan"][i])
    for b, r in zip(bars, data[exp]["gap"]):
        win = LABEL[r["best_search"]] if r["gap"] >= 0 else LABEL[r["best_filter"]]
        ax.annotate(win, (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom" if r["gap"] >= 0 else "top",
                    fontsize=6.5, rotation=90,
                    xytext=(0, 2 if r["gap"] >= 0 else -2), textcoords="offset points")
ax.axhline(0, color="k", lw=0.8)
ax.set_xticks(x, ["C1 small lab", "C2 p >> n", "C3 long signals", "C4 short, mid",
                  "C5 larger sensor", "C6 large audio/ind.", "C7 many short", "EOData"],
              fontsize=8.5)
ax.set_ylabel("best search minus best filter\n(mean AUF, K = 10)")
ax.set_ylim(-0.05, 0.09)
ax.legend(fontsize=9, frameon=False, loc="upper left")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(FIG / "P2_search_vs_filter_by_cluster.png", dpi=150)
plt.close(fig)

def _nulls(o):
    if isinstance(o, float) and o != o:
        return None
    if isinstance(o, dict):
        return {k: _nulls(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_nulls(v) for v in o]
    return o


# Missing cells (NaN) become null, which JSON has and NaN is not.
(HERE / "paper_data.json").write_text(json.dumps(_nulls(data), indent=1, default=float))
print("ok")
