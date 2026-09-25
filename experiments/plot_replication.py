"""Draw a replication run against the FASTENER paper's published Table 3.

The replication pipeline was text-only: `run_paper_replication.py` writes
`partial/*.json` and `paper_tables.csv`, and `report_replication.py` prints
tables. Neither draws anything, so the comparison against the paper had no
figure -- the PNGs in `results/` all come from the MADELON/gina SotA family and
are a different experiment entirely.

Two panels, read together:

* LEVELS -- mean AUF per data set, published (hollow) against ours (filled).
  Both our arms sit above the paper everywhere, so the panel is mostly about
  HOW FAR above, and the two arms are not equally far.
* ORDERING -- FASTENER minus FS-SDS, published against ours, around zero. This
  is the paper's headline claim (FASTENER above FS-SDS on 24 of 25) and the
  panel exists to show whether it reproduces. Rows are sorted by our gap, so
  the sign flip is read off the zero line directly.

Reads a run still in flight, exactly like report_replication.py: every unit is
on disk the moment it finishes.

Usage:
    python experiments/plot_replication.py                     # newest run
    python experiments/plot_replication.py --run <run_id>
    python experiments/plot_replication.py --fs-arm fs_sds_elm
    python experiments/plot_replication.py --out results/fig.png
"""
import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paper_tables as pt  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402
from report_replication import build_rows, load_units  # noqa: E402
# One source of palette truth: these are the slots plot_combined.py already
# validated (node scripts/validate_palette.js -> all checks pass). Slots 1 and 2
# alone re-validate at worst adjacent CVD dE 24.7, normal-vision dE 33.6.
from plot_combined import GRID, INK, INK_MUTED, REFERENCE, SLOTS, SURFACE  # noqa: E402

FASTENER_HUE, FS_SDS_HUE = SLOTS[0], SLOTS[1]

LABELS = {"fastener": "FASTENER", "fs_sds": "FS-SDS (decision tree)",
          "fs_sds_elm": "FS-SDS (ELM, as published)"}


def collect(rows: List[Dict], fs_arm: str) -> List[Dict]:
    """One record per data set that has both arms finished AND a paper row.

    A data set the paper does not carry (or one still running) is dropped
    rather than drawn half-height: a missing marker reads as a low value.
    """
    by = {(r["dataset"], r["method"]): r for r in rows
          if r.get("mean") is not None}
    out = []
    for dataset in sorted({d for d, _ in by}):
        ours_f, ours_s = by.get((dataset, "fastener")), by.get((dataset, fs_arm))
        pub_f, pub_s = pt.published(dataset, "fastener"), pt.published(dataset, fs_arm)
        if not (ours_f and ours_s and pub_f and pub_s):
            continue
        out.append({
            "dataset": dataset,
            "ours_fastener": ours_f["mean"], "paper_fastener": pub_f["mean"],
            "ours_fs_sds": ours_s["mean"], "paper_fs_sds": pub_s["mean"],
            "delta_fastener": ours_f["mean"] - pub_f["mean"],
            "delta_fs_sds": ours_s["mean"] - pub_s["mean"],
            "ours_gap": ours_f["mean"] - ours_s["mean"],
            "paper_gap": pub_f["mean"] - pub_s["mean"],
            "ours_fastener_fits": ours_f.get("eval_n"),
            "paper_fastener_fits": pub_f["eval_n"],
            "ours_fs_sds_fits": ours_s.get("eval_n"),
            "paper_fs_sds_fits": pub_s["eval_n"] * 20,  # per k, over K = 20
            "n_splits": min(ours_f["n_splits"], ours_s["n_splits"]),
        })
    # Sorted by our own gap so the ordering panel reads as one monotone run and
    # the sign flip is a single crossing, not a scatter.
    return sorted(out, key=lambda r: r["ours_gap"])


def dumbbell(ax, y, paper, ours, color, zorder=4):
    """Published -> replicated, as one mark: hollow start, filled end.

    The connector is the quantity of interest (the shift), so it carries the
    hue; the hollow/filled contrast is the secondary encoding that says which
    end is which without relying on position alone.
    """
    ax.plot([paper, ours], [y, y], color=color, lw=2, zorder=zorder,
            solid_capstyle="round", alpha=0.55)
    ax.plot([paper], [y], marker="o", markersize=8, color=SURFACE,
            markeredgecolor=color, markeredgewidth=2, zorder=zorder + 1)
    ax.plot([ours], [y], marker="o", markersize=8.5, color=color,
            markeredgecolor=SURFACE, markeredgewidth=1.2, zorder=zorder + 2)


def draw(records: List[Dict], out_path: Path, fs_arm: str,
         title: str, subtitle: str) -> Path:
    """Panel titles are DERIVED, never asserted.

    The first version hard-coded "the paper's claim does not reproduce", which
    happened to be true of the decision-tree arm and false of the ELM arm drawn
    by the same function. A title that states a count the reader can check
    against the marks cannot go stale that way.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    n = len(records)
    # Header (title, two-line subtitle, the legend strip above the panels) is a
    # fixed 2.6in; only the plotting band grows with the number of data sets,
    # so the header does not stretch on a longer run.
    head, band = 2.15, 0.42 * n + 0.9
    fig, axes = plt.subplots(
        1, 2, figsize=(13.5, head + band), facecolor=SURFACE,
        gridspec_kw={"width_ratios": [1.55, 1], "wspace": 0.06})
    fig.subplots_adjust(top=1 - head / (head + band), bottom=0.9 / (head + band),
                        left=0.105, right=0.985)
    ys = list(range(n))
    names = [r["dataset"] for r in records]

    for ax in axes:
        ax.set_facecolor(SURFACE)
        ax.set_ylim(-0.8, n - 0.2)
        ax.set_yticks(ys)
        ax.grid(axis="x", color=GRID, lw=0.8, alpha=0.7, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=INK_MUTED, labelsize=9, length=0)

    # ------------------------------------------------------------- levels
    ax = axes[0]
    ax.set_yticklabels(names, fontsize=9.5, color=INK)
    for y, r in zip(ys, records):
        # A hairline per row: 14 rows of four markers otherwise drift apart.
        ax.plot([0, 1], [y, y], color=GRID, lw=0.6, alpha=0.6, zorder=0,
                transform=ax.get_yaxis_transform())
        dumbbell(ax, y + 0.16, r["paper_fastener"], r["ours_fastener"],
                 FASTENER_HUE, zorder=5)
        dumbbell(ax, y - 0.16, r["paper_fs_sds"], r["ours_fs_sds"],
                 FS_SDS_HUE, zorder=4)
    lo = min(min(r["paper_fastener"], r["paper_fs_sds"]) for r in records)
    hi = max(max(r["ours_fastener"], r["ours_fs_sds"]) for r in records)
    ax.set_xlim(lo - 0.06, hi + 0.06)
    ax.set_xlabel("mean AUF  (published → replicated)", fontsize=10,
                  color=INK_MUTED)
    above = sum(r["delta_fastener"] > 0 and r["delta_fs_sds"] > 0
                for r in records)
    # pad clears the legend strip that sits above this panel.
    ax.set_title(
        ("Levels: both arms above the paper on every data set" if above == n
         else f"Levels: both arms above the paper on {above} of {n}"),
        fontsize=11, color=INK, pad=34, loc="left")

    handles = [
        Line2D([], [], color=FASTENER_HUE, lw=2, marker="o", markersize=8.5,
               markeredgecolor=SURFACE, label=LABELS["fastener"]),
        Line2D([], [], color=FS_SDS_HUE, lw=2, marker="o", markersize=8.5,
               markeredgecolor=SURFACE, label=LABELS[fs_arm]),
        Line2D([], [], color=INK_MUTED, lw=0, marker="o", markersize=8,
               markerfacecolor=SURFACE, markeredgecolor=INK_MUTED,
               markeredgewidth=2, label="published (Table 3)"),
        Line2D([], [], color=INK_MUTED, lw=0, marker="o", markersize=8.5,
               label="ours"),
    ]
    # Above the panel, not inside it: every row of the left panel is occupied
    # somewhere along the axis, so a boxed legend lands on data wherever it
    # goes.
    leg = ax.legend(handles=handles, loc="lower left", ncol=4, fontsize=9,
                    frameon=False, bbox_to_anchor=(0, 1.012),
                    handletextpad=0.5, columnspacing=1.6)
    for t in leg.get_texts():
        t.set_color(INK_MUTED)

    # ----------------------------------------------------------- ordering
    ax = axes[1]
    ax.set_yticklabels([])
    ax.axvline(0, color=REFERENCE, lw=1.4, ls=(0, (5, 4)), zorder=1)
    for y, r in zip(ys, records):
        ax.plot([0, 1], [y, y], color=GRID, lw=0.6, alpha=0.6, zorder=0,
                transform=ax.get_yaxis_transform())
        # One quantity, so one hue: FASTENER's, since the gap is stated from
        # FASTENER's side. Sign is carried by the zero line, not by colour.
        dumbbell(ax, y, r["paper_gap"], r["ours_gap"], FASTENER_HUE)
    span = max(abs(r["ours_gap"]) for r in records) + 0.04
    span = max(span, max(abs(r["paper_gap"]) for r in records) + 0.04)
    ax.set_xlim(-span, span)
    ax.set_xlabel("FASTENER − FS-SDS  (published → replicated)",
                  fontsize=10, color=INK_MUTED)
    agree = sum((r["ours_gap"] > 0) == (r["paper_gap"] > 0) for r in records)
    ax.set_title(f"Ordering: the paper's sign holds on {agree} of {n}",
                 fontsize=11, color=INK, pad=34, loc="left")
    # Which side of the zero line means what, inside the frame: above it is
    # where the legend strip runs.
    ax.annotate("← FS-SDS ahead", xy=(0.03, 0.992), xycoords="axes fraction",
                fontsize=8.5, color=INK_MUTED, ha="left", va="top")
    ax.annotate("FASTENER ahead →", xy=(0.97, 0.992), xycoords="axes fraction",
                fontsize=8.5, color=INK_MUTED, ha="right", va="top")

    # Selective direct labels: only where ours still agrees with the paper.
    for y, r in zip(ys, records):
        if r["ours_gap"] > 0:
            # Anchored past the rightmost of the pair, so the text never sits
            # on the connector between them.
            ax.annotate(f"+{r['ours_gap']:.3f}",
                        xy=(max(r["ours_gap"], r["paper_gap"]), y),
                        xytext=(9, 0), textcoords="offset points",
                        va="center", ha="left", fontsize=8.5, color=INK_MUTED,
                        zorder=8)

    h = fig.get_size_inches()[1]
    fig.suptitle(title, fontsize=14, color=INK, x=0.008, ha="left",
                 y=1 - 0.35 / h)
    fig.text(0.008, 1 - 0.72 / h, subtitle, fontsize=9.5, color=INK_MUTED,
             ha="left", va="top")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, facecolor=SURFACE)
    plt.close(fig)
    return out_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None,
                    help="run id or directory; default is the newest "
                         "paper_replication run")
    ap.add_argument("--fs-arm", default="fs_sds",
                    choices=["fs_sds", "fs_sds_elm"],
                    help="which FS-SDS arm to draw against the paper's row")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.run:
        run_dir = Path(args.run)
        if not run_dir.is_dir():
            matches = sorted(RESULTS_DIR.glob(f"*{args.run}*"))
            if not matches:
                raise SystemExit(f"no run matching {args.run!r}")
            run_dir = matches[-1]
    else:
        matches = sorted(RESULTS_DIR.glob("*paper_replication"))
        if not matches:
            raise SystemExit("no paper_replication run found")
        run_dir = matches[-1]

    units = load_units(run_dir)
    if not units:
        raise SystemExit(f"{run_dir.name} has no finished units yet")
    records = collect(build_rows(units), args.fs_arm)
    if not records:
        raise SystemExit(f"{run_dir.name} has no data set with both arms done")

    splits = sorted({r["n_splits"] for r in records})
    agree = sum((r["ours_gap"] > 0) == (r["paper_gap"] > 0) for r in records)
    mean_df = sum(r["delta_fastener"] for r in records) / len(records)
    mean_ds = sum(r["delta_fs_sds"] for r in records) / len(records)

    title = "Replicating FASTENER's Table 3"
    # Three short lines rather than two long ones: the run id plus the two mean
    # shifts overran the figure's right edge on the longer arm label.
    subtitle = (
        f"{run_dir.name} · {len(records)} of 25 data sets finished, "
        f"{splits[0]}–{splits[-1]} split seeds each\n"
        f"Mean shift vs. published: FASTENER {mean_df:+.3f}, "
        f"{LABELS[args.fs_arm]} {mean_ds:+.3f} · the paper's ordering "
        f"(FASTENER ahead) holds on {agree} of {len(records)}\n"
        "Paper protocol — the search reads the split it is scored on, so "
        "both sides are optimistic by construction. FS-SDS ran at 6,000 model "
        "fits per k against the paper's 30,000, a fifth of its budget.")

    out = Path(args.out) if args.out else run_dir / f"replication_{args.fs_arm}.png"
    path = draw(records, out, args.fs_arm, title, subtitle)
    print(f"wrote {path}")

    # The figure never ships alone: same numbers, exactly, as a table.
    csv_path = path.with_suffix(".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(records[0]))
        w.writeheader()
        w.writerows(records)
    print(f"wrote {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
