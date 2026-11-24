"""H8, post hoc (DEC-61): the Anthropic models' lambda-0.5 arms against MI alone.

H8-E01 ran `fastener_llm_{opus,sonnet,haiku}` (prior and mutual information
combined, lambda 0.5) and H8-E03 ran `fastener_mi_only` (a flat prior at
lambda 0.5, w = MI^0.5), so the two were never compared. This script pairs
them by dataset and seed and reads them with H8's measure, unchanged
(`h8_report.compare`): per dataset, the mean over seeds of
log2(MI-only fits / the lambda-0.5 arm's fits) to the common validation
target. Beside them are H8-E03's own nine lambda-0.5 arms against MI alone,
so that all twelve models are on one table, with Holm over the twelve.

The reading, fixed in DEC-61 before the comparison was computed: a model's
lambda-0.5 arm beats MI alone if it wins more datasets than it loses and
its Holm-adjusted p is below 0.05; the reverse case is read the same way.
It is post hoc and gives no verdict. H8-E03's verdict is unchanged.

It reads the committed distilled curves (distilled_logs/<ID>/curves.csv.xz),
not results/. Before computing anything new it checks two things and stops
if either fails:
* the curves reproduce H8-E01's part (i) rows and every row of H8-E03's
  criterion and beside tables exactly;
* the two experiments can be paired: the same FASTENER commit for every
  arm read, the same stock method ID, identical stock curves for every
  dataset and seed, and no run from a dirty tree.

    python experiments/h8_mixed_vs_mi.py

Writes into reports/H8-E03/: tables/mixed_vs_mi_only.csv,
tables/mixed_vs_mi_only_by_dataset.csv, tables/mixed_vs_mi_only_per_seed.csv
and figures/F8_mixed_vs_mi_only.png.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

import h8_report as h8
from make_report import GRID, INK_2, SERIES, _style, holm

HERE = Path(__file__).resolve().parent
DISTILLED = HERE / "distilled_logs"
OUT = h8.REPORTS / "H8-E03"
STOCK, MI_ONLY = h8.STOCK, h8.MI_ONLY
ANTHROPIC = ("opus", "sonnet", "haiku")
OTHERS = ("llama70b", "gemma4b", "gemma27b", "ministral8b", "qwen14b", "phi4",
          "deepseekflash", "gptluna", "geminilite")
# The arms whose curves are read from each experiment.
READ = {"H8-E01": [STOCK] + [h8.arm(m) for m in ANTHROPIC],
        "H8-E03": [STOCK, MI_ONLY] + [h8.arm(m) for m in OTHERS]
                  + [h8.arm(m, k) for m in ANTHROPIC + OTHERS for k in ("l1", "permuted_l1")]}

Curves = Dict[Tuple[str, str, int], h8.h0.Curve]


def load(experiment: str, base: Path = DISTILLED) -> Tuple[Curves, List[Dict]]:
    """(method, dataset, seed) -> validation-AUF step curve, and the runs."""
    import pandas as pd
    runs = pd.read_csv(base / experiment / "runs.csv.xz")
    c = pd.read_csv(base / experiment / "curves.csv.xz").merge(
        runs[["run_id", "dataset"]], on="run_id", validate="many_to_one")
    cur: Curves = {}
    for (m, d, s), g in c.groupby(["method", "dataset", "seed"], sort=True):
        g = g.sort_values("fits", kind="stable")
        cur[(m, d, int(s))] = list(zip(g["fits"].astype(int).tolist(),
                                       g["val_auf"].astype(float).tolist()))
    return cur, runs.to_dict("records")


def _table(path: Path) -> List[Dict]:
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check_reproduction(e01: Curves, e03: Curves) -> List[str]:
    """The committed rows this script recomputes and does not reproduce.

    Counts, mean, median and p must match exactly. The bootstrap interval's
    bounds may differ in the last bit: np.percentile's rounding differs
    between numpy versions (5.6e-17 on one H8-E03 row under numpy 2.5)."""
    checks = [(e01, h8.REPORTS / "H8-E01" / "tables" / "criterion.csv",
               lambda r: r["part"] == "i"),
              (e03, h8.REPORTS / "H8-E03" / "tables" / "criterion.csv", lambda r: True),
              (e03, h8.REPORTS / "H8-E03" / "tables" / "beside.csv", lambda r: True)]
    bad = []
    for cur, path, keep in checks:
        for want in filter(keep, _table(path)):
            got = h8.compare(cur, want["arm"], want["opponent"])
            same = all(int(want[k]) == got[k]
                       for k in ("n_datasets", "wins", "ties", "losses")) and \
                all(float(want[k]) == got[k]
                    for k in ("mean_effect", "median_effect", "p") if k in want) and \
                all(abs(float(want[k]) - got[k]) <= 1e-12
                    for k in ("ci_low", "ci_high") if k in want)
            if not same:
                bad.append(f"{path.parent.parent.name}: {want['arm']} vs {want['opponent']}")
    return bad


def check_pairing(e01: Curves, e03: Curves, runs01: List[Dict], runs03: List[Dict]) -> List[str]:
    """Why E01's and E03's arms may be paired; each failed condition."""
    problems = []
    read = [(r, e) for e, runs in (("H8-E01", runs01), ("H8-E03", runs03))
            for r in runs if r["method"] in READ[e]]
    fast = {r["algorithm_id"].split("@")[1].split("#")[0].split("+")[1] for r, _ in read}
    if len(fast) != 1:
        problems.append(f"FASTENER commits differ: {sorted(fast)}")
    stock = {r["algorithm_id"].split("@")[0] + "#" + r["algorithm_id"].split("#")[1]
             for r, _ in read if r["method"] == STOCK}
    if len(stock) != 1:
        problems.append(f"stock method IDs differ beyond the commit: {sorted(stock)}")
    if any(bool(r["dirty"]) for r, _ in read):
        problems.append("a run was made from a dirty tree")
    keys = sorted(k for k in e01 if k[0] == STOCK)
    differ = [k for k in keys if e03.get(k) != e01[k]]
    if not keys or differ or len(keys) != sum(k[0] == STOCK for k in e03):
        problems.append(f"stock curves differ for {len(differ)} of {len(keys)} dataset-seeds")
    return problems


def mixed_vs_mi(e01: Curves, e03: Curves) -> List[Dict]:
    """The twelve lambda-0.5 arms against MI alone, Holm over the twelve."""
    joined = {**{k: v for k, v in e01.items() if k[0] != STOCK},
              **{k: v for k, v in e03.items() if k[0] == MI_ONLY}}
    rows = [h8.compare(joined, h8.arm(m), MI_ONLY, model=m, source="H8-E01 vs H8-E03")
            for m in ANTHROPIC]
    rows += [h8.compare(e03, h8.arm(m), MI_ONLY, model=m, source="H8-E03")
             for m in OTHERS]
    for r, ph in zip(rows, holm([r["p"] for r in rows])):
        r["p_holm"] = ph
        r["beats_mi"] = bool(r["wins"] > r["losses"] and ph < 0.05)
        r["mi_beats"] = bool(r["losses"] > r["wins"] and ph < 0.05)
    return rows


def by_dataset(rows: List[Dict], e01: Curves, e03: Curves) -> List[Dict]:
    """Per dataset and Anthropic model: against MI alone, and, for context,
    the lambda-0.5 arm and MI alone each against stock."""
    stock_mi = h8.compare(e03, MI_ONLY, STOCK)
    mi_vs_stock = dict(zip(stock_mi["datasets"], stock_mi["effects"]))
    out = []
    for r in rows:
        if r["model"] not in ANTHROPIC:
            continue
        vs = h8.compare(e01, h8.arm(r["model"]), STOCK)
        vs_stock = dict(zip(vs["datasets"], vs["effects"]))
        for d, e in zip(r["datasets"], r["effects"]):
            out.append({"model": r["model"], "dataset": d, "vs_mi_only": e,
                        "mixed_vs_stock": vs_stock[d], "mi_only_vs_stock": mi_vs_stock[d]})
    return out


def figure(rows: List[Dict], per_ds: List[Dict], path: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(17, 5.6), gridspec_kw={"width_ratios": [3, 2]})
    ax = axes[0]
    for i, r in enumerate(rows):
        e = np.array(r["effects"])
        x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(e))
        col = SERIES[ANTHROPIC.index(r["model"])] if r["model"] in ANTHROPIC else INK_2
        ax.scatter(x, e, s=16, color=col, alpha=0.85)
        ax.plot([i - 0.3, i + 0.3], [r["mean_effect"]] * 2, color="k", lw=2)
        ax.annotate(f"{r['wins']}-{r['ties']}-{r['losses']}\np={r['p']:.2g}\nHolm {r['p_holm']:.2g}",
                    (i, 0), xycoords=("data", "axes fraction"), xytext=(0, -40),
                    textcoords="offset points", ha="center", va="top", fontsize=7,
                    annotation_clip=False)
    ax.axvline(len(ANTHROPIC) - 0.5, color=INK_2, lw=0.8, ls=":")
    ax.axhline(0, color=INK_2, lw=0.8)
    ax.set_xticks(range(len(rows)), [r["model"] for r in rows], fontsize=8, rotation=30)
    ax.set_ylabel("log2(MI-only fits / lambda-0.5 arm's fits) to the common target\n"
                  "(per dataset, mean over seeds; > 0 = prior + MI sooner)")
    ax.set_title("The lambda-0.5 arm (prior x MI) against MI alone: left of the dotted line "
                 "H8-E01's arms paired with H8-E03's MI-only (DEC-61, post hoc)", fontsize=9)
    ax.grid(axis="y", color=GRID)

    ax = axes[1]
    ds = sorted({r["dataset"] for r in per_ds},
                key=lambda d: -np.mean([r["vs_mi_only"] for r in per_ds if r["dataset"] == d]))
    y = np.arange(len(ds))
    for j, m in enumerate(ANTHROPIC):
        v = {r["dataset"]: r["vs_mi_only"] for r in per_ds if r["model"] == m}
        seeds = next(r["seed_rows"] for r in rows if r["model"] == m)
        yy = y + (j - 1) * 0.22
        for yi, d in zip(yy, ds):
            e = [s["effect"] for s in seeds if s["dataset"] == d]
            ax.plot([min(e), max(e)], [yi, yi], color=SERIES[j], lw=1, alpha=0.35)
        ax.scatter([v[d] for d in ds], yy, s=18, color=SERIES[j], label=m, zorder=3)
    ax.axvline(0, color=INK_2, lw=0.8)
    ax.set_yticks(y, ds, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("log2(MI-only fits / lambda-0.5 arm's fits)\n"
                  "dot = mean over seeds; line = range over the five seeds")
    ax.set_title("Per dataset, the three Anthropic models (sorted by their mean)", fontsize=9)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(axis="x", color=GRID)
    fig.text(0.01, 0.01, "validation split  |  80 runs per arm (16 datasets x 5 seeds); "
             "LightGBM, 1,000 fits; H8-E01 and H8-E03 distilled curves", fontsize=7, color=INK_2)
    fig.tight_layout(rect=(0, 0.13, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=OUT,
                    help="report folder to write into (default: H8-E03's)")
    args = ap.parse_args(argv)
    e01, runs01 = load("H8-E01")
    e03, runs03 = load("H8-E03")
    bad = check_reproduction(e01, e03)
    if bad:
        print("the distilled curves do not reproduce the committed rows:\n  "
              + "\n  ".join(bad), file=sys.stderr)
        return 1
    problems = check_pairing(e01, e03, runs01, runs03)
    if problems:
        print("H8-E01 and H8-E03 cannot be paired:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print("checks passed: committed rows reproduced; stock curves identical in H8-E01 and H8-E03")
    rows = mixed_vs_mi(e01, e03)
    per_ds = by_dataset(rows, e01, e03)
    tabs, figs = args.out / "tables", args.out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    h8.write_csv(tabs / "mixed_vs_mi_only.csv", rows)
    h8.write_csv(tabs / "mixed_vs_mi_only_by_dataset.csv", per_ds)
    h8.write_csv(tabs / "mixed_vs_mi_only_per_seed.csv",
                 [s for r in rows for s in r["seed_rows"]])
    figure(rows, per_ds, figs / "F8_mixed_vs_mi_only.png")
    for r in rows:
        print(f"{r['arm']:<28} vs MI alone {r['wins']:>2}-{r['ties']}-{r['losses']:<2} "
              f"mean {r['mean_effect']:+.3f} [{r['ci_low']:+.2f}, {r['ci_high']:+.2f}] "
              f"median {r['median_effect']:+.3f} p {r['p']:.3g} Holm {r['p_holm']:.3g}"
              + ("  beats MI" if r["beats_mi"] else "  MI beats it" if r["mi_beats"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
