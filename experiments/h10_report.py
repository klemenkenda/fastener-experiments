"""H10: the filter-seeded FASTENER arms against stock FASTENER and the filter.

The criterion as registered for H10-E01 (HYPOTHESES.md, H10; EXPERIMENTS.md,
H10-E01's design), for `fastener_seed_mrmr`, datasets as the unit (mean over
seeds):

(a) against mRMR alone (H5H6-E03's `mrmr`), AUF (K = 10): more wins than
    losses and a two-sided Wilcoxon p < 0.05;
(b) against stock FASTENER (H5H6-E03's `fastener`) at the full budget: the
    one-sided 95% lower bound of the mean per-dataset difference above
    -0.005 (paired bootstrap over datasets, 10,000 resamples, seed 20200);
(c) against stock FASTENER at 10% and 25% of the budget (h7_checkpoints.py's
    procedure; the stock arm's values from H7-E01), each with more wins than
    losses and a two-sided Wilcoxon p < 0.05 after Holm over the two.

Supported if (a), (b) and (c) hold. `fastener_seed_boruta` is reported
against the same three, as secondary.

Inputs, all made before this script reads them:

    python experiments/make_report.py --experiment H10-E01        # run_keys.csv
    python experiments/h7_checkpoints.py --experiment H10-E01 --sources H10-E01 --jobs 12
    python experiments/h10_report.py --experiment H10-E01
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
REPORTS = HERE / "reports"
RESULTS = provenance.RESULTS_DIR
BASE = "H5H6-E03"            # the grid H10-E01 is compared with
STOCK_CHECKPOINTS = "H7-E01"  # stock FASTENER's checkpoints under LightGBM
ARMS = ("fastener_seed_mrmr", "fastener_seed_boruta")
PRIMARY_ARM = "fastener_seed_mrmr"
FILTER = {"fastener_seed_mrmr": "mrmr", "fastener_seed_boruta": "boruta"}
LABEL = {"fastener_seed_mrmr": "FASTENER, mRMR seed",
         "fastener_seed_boruta": "FASTENER, Boruta seed",
         "fastener": "FASTENER", "mrmr": "mRMR", "boruta": "Boruta"}
EARLY = (0.10, 0.25)
MARGIN = -0.005
N_BOOT, BOOT_SEED = 10_000, 20200
CLUSTERS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "EO"]


def _footer(fig, note: str, split: str) -> None:
    fig.text(0.01, 0.01, f"{split} split  |  {note}", fontsize=7, color=INK_2)


def _method(m: str) -> str:
    return m[:-5] if m.endswith("_lgbm") else m


def run_keys(experiment: str) -> List[Dict]:
    with open(REPORTS / experiment / "tables" / "run_keys.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["method"] = _method(r["method"])
    return rows


def final_means(rows, methods) -> Dict[str, Dict[str, float]]:
    """method -> {dataset: mean end-of-budget AUF over seeds}."""
    acc: Dict = {}
    for r in rows:
        if r["method"] in methods and r["auf_k10"] not in ("", None):
            acc.setdefault(r["method"], {}).setdefault(r["dataset"], []) \
               .append(float(r["auf_k10"]))
    return {m: {d: float(np.mean(v)) for d, v in by.items()} for m, by in acc.items()}


def checkpoint_means(experiment: str) -> Dict:
    """(checkpoint, method) -> {dataset: mean AUF over seeds}, for the seeded
    arms (this experiment) and stock FASTENER under LightGBM (H7-E01)."""
    acc: Dict = {}
    for exp, keep in ((experiment, set(ARMS)), (STOCK_CHECKPOINTS, {"fastener"})):
        with open(RESULTS / exp / "checkpoints.csv", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r["source"] not in (experiment, BASE) or r["method"] not in keep:
                    continue
                acc.setdefault((float(r["checkpoint"]), r["method"]), {}) \
                   .setdefault(r["dataset"], []).append(float(r["auf_k10"]))
    return {k: {d: float(np.mean(v)) for d, v in by.items()} for k, by in acc.items()}


def compare(A: Dict[str, float], B: Dict[str, float], **meta) -> Dict:
    ds = sorted(set(A) & set(B))
    d = np.array([A[x] - B[x] for x in ds])
    return {**meta, "n_datasets": len(ds),
            "wins": int((d > 0).sum()), "ties": int((d == 0).sum()),
            "losses": int((d < 0).sum()),
            "mean_delta": float(d.mean()) if len(d) else float("nan"),
            "median_delta": float(np.median(d)) if len(d) else float("nan"),
            "p": wilcoxon_p(d.tolist()), "datasets": ds, "deltas": d.tolist()}


def bootstrap_lower(deltas, n=N_BOOT, seed=BOOT_SEED) -> float:
    """One-sided 95% lower bound of the mean, paired bootstrap over datasets."""
    d = np.asarray(deltas, dtype=float)
    rng = np.random.default_rng(seed)
    means = d[rng.integers(0, len(d), size=(n, len(d)))].mean(axis=1)
    return float(np.quantile(means, 0.05))


def criterion(final, ckpt) -> List[Dict]:
    out = []
    for arm in ARMS:
        role = "primary" if arm == PRIMARY_ARM else "secondary"
        a = compare(final.get(arm, {}), final.get(FILTER[arm], {}), arm=arm,
                    part="a", opponent=FILTER[arm], checkpoint=1.0, role=role)
        a["holds"] = bool(a["wins"] > a["losses"] and a["p"] < 0.05)
        b = compare(final.get(arm, {}), final.get("fastener", {}), arm=arm,
                    part="b", opponent="fastener", checkpoint=1.0, role=role)
        b["lower_95"] = bootstrap_lower(b["deltas"]) if b["n_datasets"] else float("nan")
        b["holds"] = bool(b["lower_95"] > MARGIN)
        cs = [compare(ckpt.get((c, arm), {}), ckpt.get((c, "fastener"), {}),
                      arm=arm, part="c", opponent="fastener", checkpoint=c, role=role)
              for c in EARLY]
        for r, ph in zip(cs, holm([r["p"] for r in cs])):
            r["p_holm"] = ph
            r["holds"] = bool(r["wins"] > r["losses"] and ph < 0.05)
        out += [a, b] + cs
    return out


def verdict(crit) -> Dict:
    out = {}
    for arm in ARMS:
        parts = {p: all(r["holds"] for r in crit if r["arm"] == arm and r["part"] == p)
                 for p in "abc"}
        out[arm] = {**parts, "all": all(parts.values())}
    out["verdict"] = "supported" if out[PRIMARY_ARM]["all"] else "not supported"
    return out


def secondary(final, ckpt) -> List[Dict]:
    """Beside the criterion: against the better of filter and stock FASTENER
    per dataset (H10's title), and at 50%."""
    out = []
    for arm in ARMS:
        F, S = final.get(FILTER[arm], {}), final.get("fastener", {})
        best = {d: max(F[d], S[d]) for d in set(F) & set(S)}
        out.append(compare(final.get(arm, {}), best, arm=arm, part="beside",
                           opponent=f"max({FILTER[arm]}, fastener)", checkpoint=1.0))
        out.append(compare(ckpt.get((0.5, arm), {}), ckpt.get((0.5, "fastener"), {}),
                           arm=arm, part="beside", opponent="fastener", checkpoint=0.5))
        out.append(compare(final.get(arm, {}), final.get("mrmr" if arm != "fastener_seed_mrmr"
                                                          else "boruta", {}),
                           arm=arm, part="beside",
                           opponent="boruta" if arm == "fastener_seed_mrmr" else "mrmr",
                           checkpoint=1.0))
    return out


def seed_costs(rows) -> List[Dict]:
    """Per run: the seed's fits and time against the search's, from raw results."""
    out = []
    for r in rows:
        if r["method"] not in ARMS:
            continue
        d = RESULTS / r["run_id"]
        raw = sorted(d.glob("raw_results*.json"))
        if not raw:
            continue
        res = json.loads(raw[0].read_text(encoding="utf-8"))[0]
        out.append({"dataset": r["dataset"], "method": r["method"], "seed": r["seed"],
                    "seed_fits": res.get("seed_fits"),
                    "seed_seconds": res.get("seed_seconds"),
                    "seed_cpu_seconds": res.get("seed_cpu_seconds"),
                    "model_fits": res.get("model_fits"),
                    "search_seconds": res.get("search_seconds"),
                    "stopped_on": res.get("stopped_on")})
    return out


# ------------------------------------------------------------------ figures
def fig_criterion(crit, note, path):
    """One panel per part; one point per dataset, bar = mean."""
    import matplotlib.pyplot as plt
    _style(plt)
    parts = [("a", "(a) minus the seed filter, 100%"),
             ("b", "(b) minus stock FASTENER, 100%"),
             ("c", "(c) minus stock FASTENER, 10% and 25%")]
    fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharey=True,
                             gridspec_kw={"width_ratios": [1, 1, 2]})
    for ax, (p, title) in zip(axes, parts):
        grp = [r for r in crit if r["part"] == p]
        grp.sort(key=lambda r: (r["checkpoint"], ARMS.index(r["arm"])))
        for i, r in enumerate(grp):
            d = np.array(r["deltas"])
            x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(d))
            col = SERIES[ARMS.index(r["arm"])]
            ax.scatter(x, d, s=14, color=col, alpha=0.9 if r["holds"] else 0.5,
                       facecolors=None if r["holds"] else "none")
            ax.plot([i - 0.3, i + 0.3], [r["mean_delta"]] * 2, color="k", lw=2)
            stat = (f"lower {r['lower_95']:+.4f}" if p == "b"
                    else f"p={r.get('p_holm', r['p']):.2g}")
            ax.annotate(f"{r['wins']}-{r['ties']}-{r['losses']}\n{stat}"
                        + ("\nholds" if r["holds"] else ""),
                        (i, 0), xycoords=("data", "axes fraction"),
                        xytext=(0, -34), textcoords="offset points",
                        ha="center", va="top", fontsize=7,
                        annotation_clip=False)
        if p == "b":
            ax.axhline(MARGIN, color=SERIES[7], lw=0.8, ls="--")
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(range(len(grp)),
                      [f"{LABEL[r['arm']].split(', ')[1]}"
                       + (f"\n{int(r['checkpoint'] * 100)}%" if p == "c" else "")
                       for r in grp], fontsize=7.5)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel("seeded arm's AUF (K = 10) minus the opponent's\n"
                       "(per dataset, mean over seeds)")
    fig.suptitle("H10: the seeded arms against the filter and stock FASTENER; one point "
                 "per dataset, bar = mean; filled = holds (dashed: margin -0.005)",
                 fontsize=10)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.13, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_curves(final, ckpt, note, path):
    """Mean AUF at each checkpoint, with the filters' end values as lines."""
    import matplotlib.pyplot as plt
    _style(plt)
    cps = sorted({c for c, _ in ckpt})
    arms = ("fastener",) + ARMS
    common = set.intersection(*[set(ckpt.get((c, a), {})) for c in cps for a in arms])
    fig, ax = plt.subplots(figsize=(12, 4.6))
    for j, a in enumerate(arms):
        y = [np.mean([ckpt[(c, a)][d] for d in common]) for c in cps]
        ax.plot([c * 100 for c in cps], y, marker="o", color=SERIES[(j + 2) % len(SERIES)],
                lw=2.2 if a == PRIMARY_ARM else 1.3, label=LABEL[a])
    for j, f in enumerate(("mrmr", "boruta")):
        vals = [final.get(f, {}).get(d) for d in common]
        vals = [v for v in vals if v is not None]
        if vals:
            ax.axhline(np.mean(vals), color=SERIES[(j + 5) % len(SERIES)], ls=":",
                       label=f"{LABEL[f]} alone ({len(vals)} datasets)")
    ax.set_xscale("log")
    ax.set_xticks([c * 100 for c in cps], [f"{int(c * 100)}%" for c in cps])
    ax.set_xlabel("share of the fit budget (the Boruta seed's own fits included)")
    ax.set_ylabel("mean AUF (K = 10), test")
    ax.set_title(f"Mean AUF at each checkpoint, LightGBM, over the {len(common)} datasets "
                 "every arm has", fontsize=10)
    ax.grid(color=GRID)
    ax.legend(fontsize=8, loc="center right")
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_clusters(final, ckpt, note, path):
    """Per cluster: each seeded arm minus stock FASTENER (10%, 100%) and minus
    its filter (100%)."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(17, 4.6), sharey=True)
    x = np.arange(len(CLUSTERS))
    for ax, arm in zip(axes, ARMS):
        series = [("vs FASTENER, 10%", ckpt.get((0.10, arm), {}), ckpt.get((0.10, "fastener"), {})),
                  ("vs FASTENER, 100%", final.get(arm, {}), final.get("fastener", {})),
                  (f"vs {LABEL[FILTER[arm]]}, 100%", final.get(arm, {}), final.get(FILTER[arm], {}))]
        for j, (lab, A, B) in enumerate(series):
            vals = []
            for cl in CLUSTERS:
                ds = [d for d in A if d in B and SWAP_CLUSTERS.get(d, "EO") == cl]
                vals.append(np.mean([A[d] - B[d] for d in ds]) if ds else np.nan)
            ax.bar(x + (j - 1) * 0.27, vals, 0.27, label=lab, color=SERIES[j])
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(x, CLUSTERS)
        ax.set_title(LABEL[arm], fontsize=10)
        ax.grid(axis="y", color=GRID)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("seeded arm minus opponent,\nmean AUF (K = 10)")
    fig.suptitle("By cluster (descriptive; 1-7 datasets per cluster)", fontsize=10)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: List[str] = []
    for r in rows:
        keys += [k for k in r if k not in keys and k not in ("datasets", "deltas")]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--experiment", required=True)
    args = ap.parse_args(argv)
    own = run_keys(args.experiment)
    final = final_means(own, set(ARMS))
    final.update(final_means(run_keys(BASE), {"fastener", "mrmr", "boruta"}))
    ckpt = checkpoint_means(args.experiment)
    crit = criterion(final, ckpt)
    v = verdict(crit)
    beside = secondary(final, ckpt)
    costs = seed_costs(own)

    out = REPORTS / args.experiment
    tabs, figs = out / "tables", out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    write_csv(tabs / "criterion.csv", crit)
    write_csv(tabs / "beside.csv", beside)
    write_csv(tabs / "seed_costs.csv", costs)
    write_csv(tabs / "per_dataset.csv",
              [{"method": m, "checkpoint": 1.0, "dataset": d, "auf_k10": a}
               for m, by in sorted(final.items()) for d, a in sorted(by.items())]
              + [{"method": m, "checkpoint": c, "dataset": d, "auf_k10": a}
                 for (c, m), by in sorted(ckpt.items()) for d, a in sorted(by.items())])
    (tabs / "verdict.json").write_text(json.dumps(v, indent=1), encoding="utf-8")
    note = (f"{len(own)} runs of {args.experiment}; {BASE}'s fastener, mrmr, boruta; "
            f"checkpoints: results/{args.experiment}, results/{STOCK_CHECKPOINTS}")
    fig_criterion(crit, note, figs / "F1_H10_criterion.png")
    fig_curves(final, ckpt, note, figs / "F2_auf_by_checkpoint.png")
    fig_clusters(final, ckpt, note, figs / "F3_by_cluster.png")
    print(json.dumps(v))
    for r in crit + beside:
        extra = (f" lower95 {r['lower_95']:+.4f}" if "lower_95" in r else
                 f" holm {r['p_holm']:.3g}" if "p_holm" in r else "")
        print(f"{r['arm']:<22} ({r['part']}) {int(r['checkpoint'] * 100):>3}% vs "
              f"{r['opponent']:<22} {r['wins']}-{r['ties']}-{r['losses']} "
              f"mean {r['mean_delta']:+.4f} p {r['p']:.3g}{extra}"
              + (f" holds={r['holds']}" if "holds" in r else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
