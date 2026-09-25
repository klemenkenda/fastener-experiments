"""Combine several concluded runs into one comparison figure.

Runs done at different times are comparable as long as they share the split seed
and the model seed, which the protocol fixes globally -- so FASTENER from the
baseline run and the selectors from a later run can be read on one axis.

A dozen selectors is well past the point where one set of hues stays
distinguishable, so the figure is faceted: standard selectors, stronger filters,
and wrapper/multi-objective searches, with FASTENER drawn in all three as the
common reference. Each panel carries its own legend and is read on its own.

Usage:
    python experiments/plot_combined.py --runs 20260916T123417Z_madelon_baseline \
                                               20260916T133104Z_madelon_filters
    python experiments/plot_combined.py --runs <id> <id> --out results/fig.png
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402
from run_experiment import K_GRID  # noqa: E402

# Validated categorical palette, light mode, adjacent pairlist:
# node scripts/validate_palette.js \
#   "#2a78d6,#eb6834,#1baf7a,#eda100,#e87ba4,#008300,#4a3aa7,#e34948" --mode light
# -> all checks pass (worst adjacent CVD dE 9.1, normal-vision dE 19.6); contrast
# WARN on aqua/yellow/magenta obliges "relief", which is why every series also
# carries a distinct marker shape, the panels carry direct labels, and
# comparison.csv ships beside the figure.
#
# Eight slots. Hues are assigned in fixed order and never cycled: at six slots
# a seventh series silently reused FASTENER's blue circle. No panel needs all
# eight today -- the widest holds five -- but the guard in `draw` refuses to
# cycle, so a panel that outgrows the palette gets split instead.
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300",
         "#4a3aa7", "#e34948"]
MARKERS = ["o", "s", "^", "D", "v", "X", "P", "*"]

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_MUTED = "#52514e"
GRID = "#d9d8d4"
REFERENCE = "#8a8984"

# FASTENER is the subject of the comparison, so it is pinned to slot 1 and drawn
# in every panel. The others take the remaining slots in fixed order within
# their own panel.
SUBJECT = "fastener"

# Three panels, not two: with FS-SDS added, the old "stronger / SotA" panel
# would have carried FASTENER plus seven others, past the palette and past what
# one set of hues can keep apart. Splitting filters from wrapper searches is
# also the more honest cut -- a ranker and a population search are not the same
# kind of claim -- and it puts FASTENER beside its own paper's comparators
# (POSS and FS-SDS) in the last panel.
PANELS = [
    ("Standard selectors",
     ["kbest_mutual_info", "kbest_anova_f", "tree_importance", "rfe_tree",
      "random"]),
    ("Stronger filters",
     ["mrmr", "relieff", "boruta", "hsic_lasso"]),
    ("Wrapper / multi-objective searches",
     ["nsga2", "poss", "fs_sds", "nsgaii_miip"]),
    # The pruning-swap arms are the local contribution, so they get their own
    # panel rather than being folded in beside the published comparators: the
    # comparison that matters for them is against FASTENER itself, which is
    # drawn in every panel anyway.
    ("FASTENER pruning-swap arms",
     ["fastener_swap_random", "fastener_swap_guided"]),
]

LABELS = {
    "fastener": "FASTENER",
    "kbest_mutual_info": "mutual info",
    "kbest_anova_f": "ANOVA-F",
    "tree_importance": "tree importance",
    "rfe_tree": "RFE",
    "random": "random",
    "mrmr": "mRMR",
    "relieff": "ReliefF",
    "boruta": "Boruta",
    "hsic_lasso": "HSIC Lasso",
    "nsga2": "NSGA-II",
    "poss": "POSS",
    "fs_sds": "FS-SDS",
    "nsgaii_miip": "NSGAII-MIIP",
    "all_features": "all features",
    "fastener_swap_random": "swap (random)",
    "fastener_swap_guided": "swap (guided)",
}


def load_runs(run_ids: List[str]) -> List[Dict]:
    results = []
    for rid in run_ids:
        d = Path(rid)
        if not d.is_dir():
            d = RESULTS_DIR / rid
        if not d.is_dir():
            matches = sorted(RESULTS_DIR.glob(f"*{rid}*"))
            if not matches:
                raise SystemExit(f"no run directory matching {rid!r}")
            d = matches[-1]
        raw = d / "raw_results.json"
        if not raw.is_file():
            raise SystemExit(f"{d.name} has no raw_results.json (still running?)")
        loaded = json.load(open(raw, encoding="utf-8"))
        for r in loaded:
            r["_run"] = d.name
        results.extend(loaded)
        print(f"  loaded {len(loaded):2d} result blocks from {d.name}")
    return results


def series_from_rows(rows: List[Dict], method: str):
    by_k: Dict[int, List[float]] = {}
    for r in rows:
        if r["method"] == method:
            by_k.setdefault(r["budget_k"], []).append(r["test_f1"])
    if not by_k:
        return None
    ks = sorted(by_k)
    return (ks,
            [float(np.mean(by_k[k])) for k in ks],
            [float(np.min(by_k[k])) for k in ks],
            [float(np.max(by_k[k])) for k in ks],
            max(len(by_k[k]) for k in ks))


def draw(rows: List[Dict], out_path: Path, title: str, subtitle: str) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    present = {r["method"] for r in rows}
    baseline = series_from_rows(rows, "all_features")

    # Only the panels this run actually has members for. A dataset run through
    # the SotA script alone has no standard-selector rows, and an empty panel
    # holding nothing but the FASTENER reference line reads as a result ("the
    # selectors all scored zero") rather than as an absence.
    panels = [p for p in PANELS if any(m in present for m in p[1])]
    if not panels:
        raise SystemExit(f"none of the panelled methods are in these runs; "
                         f"present: {', '.join(sorted(present))}")

    fig, axes = plt.subplots(1, len(panels), figsize=(6.6 * len(panels), 6.2),
                             sharey=True, facecolor=SURFACE, squeeze=False)
    axes = list(axes[0])
    # Headroom for a subtitle that may run to two lines.
    fig.subplots_adjust(top=0.79, bottom=0.12, wspace=0.06)

    for ax, (panel_title, members) in zip(axes, panels):
        ax.set_facecolor(SURFACE)
        # Recessive grid and spines: the data should be the only assertive thing.
        ax.grid(True, which="both", color=GRID, lw=0.7, alpha=0.7, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)

        if baseline is not None:
            ax.axhline(baseline[1][-1], color=REFERENCE, lw=1.4, ls=(0, (5, 4)),
                       zorder=1)
            # Anchored left: the right edge is where the series end labels live.
            ax.annotate(f"{LABELS['all_features']} ({baseline[1][-1]:.3f})",
                        xy=(0.015, baseline[1][-1]),
                        xycoords=("axes fraction", "data"),
                        xytext=(0, 4), textcoords="offset points",
                        ha="left", va="bottom", fontsize=8.5, color=INK_MUTED)

        drawn = [SUBJECT] + [m for m in members if m in present]
        if len(drawn) > len(SLOTS):
            raise SystemExit(
                f"panel {panel_title!r} has {len(drawn)} series but the "
                f"palette has {len(SLOTS)} slots. Cycling would repaint one "
                f"series in another's colour; split the panel instead.")
        ends = []
        for i, method in enumerate(drawn):
            s = series_from_rows(rows, method)
            if s is None:
                continue
            ks, mean, lo, hi, n_seeds = s
            color = SLOTS[i % len(SLOTS)]
            marker = MARKERS[i % len(MARKERS)]
            subject = method == SUBJECT
            ax.plot(ks, mean, color=color, lw=2.4 if subject else 2.0,
                    marker=marker, markersize=8 if subject else 7,
                    markeredgecolor=SURFACE, markeredgewidth=1.2,
                    label=LABELS.get(method, method),
                    zorder=6 if subject else 4)
            if n_seeds > 1 and len(ks) > 1:
                # Seed spread, so a mean is never read as a single outcome.
                ax.fill_between(ks, lo, hi, color=color, alpha=0.14, lw=0,
                                zorder=2)
            elif n_seeds > 1:
                # A method whose sparsest subset lands past the second-largest
                # k has exactly one point on this grid -- NSGA-II on gina, whose
                # fronts never got below ~360 features. fill_between draws
                # nothing across a single x, which would silently hide the seed
                # spread, so the band becomes a bar.
                ax.vlines(ks[0], lo[0], hi[0], color=color, lw=6, alpha=0.2,
                          zorder=2)
            ends.append((mean[-1], ks[-1], LABELS.get(method, method), color))

        ax.set_xscale("log")
        # Room to the right of the last point for the end labels.
        # 4.4x rather than 3.4x: the longest label ("tree importance") ran off
        # the panel edge at the old margin, and narrower panels made it worse.
        ax.set_xlim(right=max(e[1] for e in ends) * 4.4)

        # Selective direct labels: the top three endpoints only, in text ink with
        # the series colour carried by a small marker beside the words. Curves
        # that converge -- as they do here past k=10 -- would otherwise stack
        # their labels on top of each other, so nudge them apart vertically.
        top = sorted(ends, reverse=True)[:3]
        span = np.ptp(ax.get_ylim())
        min_gap = span * 0.038
        placed: List[float] = []
        for value, k, label, color in top:
            y = value
            for prev in placed:
                if abs(y - prev) < min_gap:
                    y = prev - min_gap
            placed.append(y)
            ax.annotate(label, xy=(k, y), xytext=(11, 0),
                        textcoords="offset points", va="center", ha="left",
                        fontsize=9, color=INK_MUTED, zorder=7,
                        annotation_clip=False)
            ax.plot([k], [value], marker="o", markersize=4, color=color,
                    zorder=7)
        ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500])
        ax.get_xaxis().set_major_formatter(
            matplotlib.ticker.ScalarFormatter())
        ax.set_xlabel("feature budget k  (log scale)", fontsize=10,
                      color=INK_MUTED)
        ax.set_title(panel_title, fontsize=11, color=INK, pad=8, loc="left")
        ax.tick_params(colors=INK_MUTED, labelsize=9)
        leg = ax.legend(loc="lower right", fontsize=9, framealpha=0.96,
                        facecolor=SURFACE, edgecolor=GRID)
        for t in leg.get_texts():
            t.set_color(INK_MUTED)

    axes[0].set_ylabel("weighted F1 on untouched test set", fontsize=10,
                       color=INK_MUTED)
    fig.suptitle(title, fontsize=14, color=INK, x=0.012, ha="left", y=0.965)
    fig.text(0.012, 0.935, subtitle, fontsize=9.5, color=INK_MUTED,
             ha="left", va="top")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, facecolor=SURFACE)
    plt.close(fig)
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--title", default="FASTENER vs. feature selectors on MADELON")
    args = ap.parse_args()

    print("combining:")
    results = load_runs(args.runs)
    ks = K_GRID
    rows = analysis.comparison_table(results, ks)

    methods = sorted({r["method"] for r in rows})
    print(f"  methods: {', '.join(methods)}")

    seeds = {r["method"]: len({x["seed"] for x in rows if x["method"] == r["method"]
                               and x["seed"] is not None})
             for r in rows}
    stochastic = [m for m, n in seeds.items() if n > 1]
    subtitle = ("Mean over seeds; shaded band is the seed min-max range. "
                "Selection on validation, scored on the untouched test split. "
                f"Seeded arms: {', '.join(LABELS.get(m, m) for m in sorted(stochastic))}.")

    # A method only gets a row at k once it has produced a subset that small, so
    # one that never went sparse shows up as a short curve or a lone point high
    # on the axis -- which reads as a win unless the figure says otherwise.
    # On gina that is both NSGA-II arms: their fronts bottom out near 400 of 970
    # features, so they are only ever compared at k = 500.
    floors = []
    for method in sorted({r["method"] for r in rows}):
        mine = [r for r in rows if r["method"] == method]
        if min(r["budget_k"] for r in mine) > min(ks):
            smallest = min(r["n_features_used"] for r in mine)
            floors.append(f"{LABELS.get(method, method)} ≥ {smallest}")
    if floors:
        subtitle += ("\nSparsest subset any seed reached, for arms that never "
                     f"got small: {'; '.join(floors)} features — they are "
                     "drawn only at the k they reach, not across the grid.")

    out = Path(args.out) if args.out else RESULTS_DIR / "combined_comparison.png"
    path = draw(rows, out, args.title, subtitle)
    print(f"\nwrote {path}")

    # The contrast relief rule: a table view ships with the figure.
    csv_path = path.with_suffix(".csv")
    import csv as _csv
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = _csv.DictWriter(fh, fieldnames=[
            "method", "seed", "budget_k", "n_features_used", "val_f1", "test_f1"],
            extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
