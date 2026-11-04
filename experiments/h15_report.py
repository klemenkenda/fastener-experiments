"""H15: the fits the OBL start needs to reach k <= 10 grow with d as H14 predicts.

The criterion as registered for H15-E01 (HYPOTHESES.md, H15; EXPERIMENTS.md,
H15-E01; DEC-59) and rerun unchanged as H15-E02 (DEC-60), on its 35 runs of `p2_obl_reach`, read from
`experiments/distilled_logs/H15-E02/`. Fits-to-reach is H13-E01's measure
(`h13_coverage.time_to_reach`): the fits at the end of the generation in
which the archive first held a subset of at most 10 features. A run that
did not reach (cap, stagnation, timeout, missing) is censored and counts as
not reached; in a median it counts as larger than every reached value.

The prediction, fitted on H14-E02's 20 `p2_obl_b10` runs before any H15
run (OLS of ln fits-to-reach on ln d):  F(d) = exp(A + B ln d).

(i)   reach: on every dataset at least 4 of 5 seeds reach before the cap
      (4 F(d)).
(ii)  magnitude: the median fits-to-reach T is within a factor 2 of F(d),
      |ln(T / F(d))| <= ln 2, on at least 5 of the 7 datasets.
(iii) shape: the OLS slope of ln T on ln d over the datasets with a finite
      T (at least 5 needed) has a bootstrap 95% interval (datasets
      resampled, 10,000 times, seed 20200) whose lower end is above 1.
Supported if (i), (ii) and (iii) hold.

    python experiments/distill_results.py
    python experiments/h15_report.py          # -> reports/H15-E02/{tables,figures}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

import _bootstrap  # noqa: F401
import h13_coverage as cov
import h14_report as h14
from make_report import GRID, INK_2, SERIES, _style

HERE = Path(__file__).resolve().parent
EXPERIMENT = "H15-E02"   # H15-E01 was refused before any run (DEC-60)
REPORTS = HERE / "reports"
METHOD = "p2_obl_reach"
DATASETS = ("gas_drift", "crop_mapping", "volkert", "madelon", "Isolet",
            "gina", "ORL")
SEEDS = tuple(range(2030, 2035))
A, B = -0.9607461167011995, 1.8765480534645083   # H14-E02, 20 runs
CAP_FACTOR = 4
SEED_RULE = 4            # (i): seeds of 5 that reach before the cap
TOL = np.log(2)          # (ii): factor 2
DATASET_RULE = 5         # (ii): datasets of 7 within the factor
MIN_SLOPE_DATASETS = 5   # (iii)
N_BOOT, BOOT_SEED = 10_000, 20200


def predicted(d: float) -> float:
    return float(np.exp(A + B * np.log(d)))


def check_budgets(path: Path = HERE / "h15_budgets.json") -> Dict[str, int]:
    """The committed caps are 4 F(d) rounded up to 1,000."""
    b = json.loads(path.read_text(encoding="utf-8"))
    return b["budgets"]


# ------------------------------------------------------------------ inputs
def load(experiment: str = EXPERIMENT) -> List[Dict]:
    """One row per (dataset, seed) of the design; a cell with no finished run
    is censored."""
    runs = [r for r in h14.load_runs(experiment) if r["method"] == METHOD]
    meta = pd.read_csv(HERE / "distilled_logs" / experiment / "runs.csv.xz")
    meta = meta.drop_duplicates("dataset").set_index("dataset")
    have = {(r["dataset"], r["seed"]): r for r in runs}
    out = []
    for ds in DATASETS:
        for s in SEEDS:
            r = have.get((ds, s))
            if r is None:
                out.append({"dataset": ds, "seed": s, "finished": False, "reached": False,
                            "ttr_fits": None, "ttr_seconds": None})
                continue
            out.append({"dataset": ds, "seed": s, "finished": True, "d": r["d"],
                        "cap": r["budget"], "fits": r["fits"], "stopped_on": r["stopped_on"],
                        "seconds": r["seconds"], "reached": bool(r["ttr"]["reached"]),
                        "ttr_fits": r["ttr"]["fits"] if r["ttr"]["reached"] else None,
                        "ttr_seconds": r["ttr"]["seconds"] if r["ttr"]["reached"] else None,
                        "front_reach": bool(r["reach"][-1]), "run_id": r["run_id"],
                        "algorithm_id": r["algorithm_id"],
                        "n_train": int(meta.loc[ds, "n_train"]) if ds in meta.index else None})
    d_of = {r["dataset"]: r["d"] for r in out if r.get("d")}
    for r in out:
        r.setdefault("d", d_of.get(r["dataset"]))
    return out


def censored_median(values: List[Optional[float]]) -> float:
    """Median with censored values (None) larger than every observed one."""
    v = sorted(np.inf if x is None else float(x) for x in values)
    return float(np.median(v)) if v else float("nan")


# --------------------------------------------------------------- criterion
def per_dataset(rows: List[Dict]) -> List[Dict]:
    out = []
    for ds in DATASETS:
        rs = [r for r in rows if r["dataset"] == ds]
        d = rs[0]["d"]
        F = predicted(d) if d else float("nan")
        T = censored_median([r["ttr_fits"] for r in rs])
        ratio = T / F if np.isfinite(T) else float("inf")
        reached = sum(r["reached"] for r in rs)
        secs = [r["ttr_seconds"] / r["ttr_fits"] for r in rs if r["reached"]]
        out.append({"dataset": ds, "d": d, "n_train": rs[0].get("n_train"),
                    "predicted": F, "cap": CAP_FACTOR * F, "n_seeds": len(rs),
                    "finished": sum(r["finished"] for r in rs), "reached": reached,
                    "median_fits_to_reach": T, "ratio": ratio,
                    "log_ratio": float(np.log(ratio)) if np.isfinite(ratio) else float("inf"),
                    "min_fits": min((r["ttr_fits"] for r in rs if r["reached"]), default=None),
                    "max_fits": max((r["ttr_fits"] for r in rs if r["reached"]), default=None),
                    "seconds_per_fit_median": float(np.median(secs)) if secs else float("nan"),
                    "stopped_on": ",".join(sorted({str(r.get("stopped_on")) for r in rs})),
                    "i_holds": reached >= SEED_RULE,
                    "ii_holds": bool(np.isfinite(ratio) and abs(np.log(ratio)) <= TOL)})
    return out


def slope(per: List[Dict]) -> Dict:
    ok = [p for p in per if np.isfinite(p["median_fits_to_reach"])]
    res = {"n_datasets": len(ok), "slope": float("nan"), "intercept": float("nan"),
           "lo": float("nan"), "hi": float("nan"), "n_boot": 0}
    if len(ok) < 2:
        return res
    x = np.log([p["d"] for p in ok])
    y = np.log([p["median_fits_to_reach"] for p in ok])
    res["slope"], res["intercept"] = (float(v) for v in np.polyfit(x, y, 1))
    rng = np.random.default_rng(BOOT_SEED)
    bs = []
    for _ in range(N_BOOT):
        i = rng.integers(0, len(ok), len(ok))
        if len(set(x[i])) < 2:
            continue
        bs.append(np.polyfit(x[i], y[i], 1)[0])
    res["lo"], res["hi"] = (float(v) for v in np.percentile(bs, [2.5, 97.5]))
    res["n_boot"] = len(bs)
    return res


def criterion(per: List[Dict], sl: Dict) -> Dict:
    i = all(p["i_holds"] for p in per)
    n_ii = sum(p["ii_holds"] for p in per)
    ii = n_ii >= DATASET_RULE
    iii = sl["n_datasets"] >= MIN_SLOPE_DATASETS and sl["lo"] > 1
    return {"i": i, "datasets_i": sum(p["i_holds"] for p in per),
            "ii": ii, "datasets_ii": n_ii, "iii": bool(iii),
            "slope": sl["slope"], "slope_lo": sl["lo"], "slope_hi": sl["hi"],
            "slope_datasets": sl["n_datasets"], "prediction_slope": B,
            "supported": bool(i and ii and iii)}


# ------------------------------------------------------------------ figures
def _h14_points() -> pd.DataFrame:
    t = REPORTS / "H14-E02" / "tables" / "run_measures.csv"
    r = pd.read_csv(t)
    return r[r.method == "p2_obl_b10"][["dataset", "d", "ttr_fits"]]


def fig_scaling(rows, per, sl, note, path):
    """Per-seed fits-to-reach against d (log-log): H15's runs, H14-E02's
    (grey, the fit's data), the registered line and its factor-2 band."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(14, 5))
    h = _h14_points()
    ax.scatter(h.d, h.ttr_fits, s=14, color=INK_2, alpha=0.6, label="H14-E02 (the fit's data)")
    xs = np.geomspace(100, 1200, 50)
    ax.plot(xs, [predicted(x) for x in xs], color=SERIES[1], label=f"registered: exp({A:.2f}) d^{B:.2f}")
    ax.fill_between(xs, [predicted(x) / 2 for x in xs], [predicted(x) * 2 for x in xs],
                    color=SERIES[1], alpha=0.12, label="factor 2 ((ii))")
    ax.plot(xs, [CAP_FACTOR * predicted(x) for x in xs], color=SERIES[1], ls=":", lw=1,
            label="cap, 4x the prediction")
    rr = [r for r in rows if r["reached"]]
    ax.scatter([r["d"] for r in rr], [r["ttr_fits"] for r in rr], s=22, color=SERIES[0],
               label=f"{note.split()[3]}, per seed")
    cc = [r for r in rows if not r["reached"] and r["d"]]
    if cc:
        ax.scatter([r["d"] for r in cc], [r.get("fits") or CAP_FACTOR * predicted(r["d"]) for r in cc],
                   marker="^", s=30, color=SERIES[3], label="not reached (censored at its fits)")
    for p in per:
        if np.isfinite(p["median_fits_to_reach"]):
            ax.annotate(p["dataset"], (p["d"], p["median_fits_to_reach"]), xytext=(5, -10),
                        textcoords="offset points", fontsize=7.5, color=INK_2)
    if np.isfinite(sl["slope"]):
        ax.plot(xs, np.exp(sl["intercept"] + sl["slope"] * np.log(xs)), color=SERIES[0], ls="--",
                lw=1, label=f"H15 fit: slope {sl['slope']:.2f} [{sl['lo']:.2f}, {sl['hi']:.2f}]")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("features d (log)")
    ax.set_ylabel("fits until the archive holds\na subset of <= 10 features (log)")
    ax.grid(color=GRID, which="both", lw=0.5)
    ax.legend(fontsize=7.5, loc="upper left", ncol=2)
    fig.suptitle("H15: the OBL start's fits-to-reach against d, on datasets no NSGA-II arm had run on",
                 fontsize=10)
    h14._footer(fig, note, "validation (archive)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_ratio(rows, per, note, path):
    """(ii): per dataset (by d), each seed's fits-to-reach over the
    prediction; the factor-2 band."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(14, 4.6))
    for i, p in enumerate(per):
        rs = [r for r in rows if r["dataset"] == p["dataset"]]
        v = [r["ttr_fits"] / p["predicted"] for r in rs if r["reached"]]
        ax.scatter(np.full(len(v), i), v, s=20, color=SERIES[0])
        n_c = sum(not r["reached"] for r in rs)
        if n_c:
            ax.scatter([i], [CAP_FACTOR], marker="^", s=30, color=SERIES[3])
            ax.annotate(f"{n_c} not reached", (i, CAP_FACTOR), xytext=(6, 0),
                        textcoords="offset points", fontsize=7.5, color=SERIES[3])
        if np.isfinite(p["ratio"]):
            ax.hlines(p["ratio"], i - 0.25, i + 0.25, color=SERIES[0], lw=2)
    ax.axhspan(0.5, 2, color=SERIES[1], alpha=0.12)
    ax.set_ylim(0.4, 2.6)
    ax.axhline(1, color=SERIES[1], lw=1)
    ax.set_yscale("log")
    ax.set_xticks(range(len(per)), [f"{p['dataset']}\nd = {p['d']}" for p in per])
    ax.set_ylabel("fits-to-reach / prediction (log)")
    ax.grid(axis="y", color=GRID, which="both", lw=0.5)
    fig.suptitle("H15 (ii): fits-to-reach over the registered prediction, per seed (bar: median); "
                 "band: factor 2", fontsize=10)
    h14._footer(fig, note, "validation (archive)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_km(rows, per, note, path):
    """Per dataset, KM share of runs whose archive reached k <= 10 against
    fits in multiples of the prediction."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(14, 4.6))
    for j, p in enumerate(per):
        rs = [r for r in rows if r["dataset"] == p["dataset"]]
        t = [(r["ttr_fits"] if r["reached"] else (r.get("fits") or 0)) / p["predicted"] for r in rs]
        ts, s = cov.km(t, [r["reached"] for r in rs])
        reached = 1 - s if len(s) else np.zeros(0)
        last = reached[-1] if len(reached) else 0.0
        ax.step(np.r_[0.05, ts, CAP_FACTOR], np.r_[0.0, reached, last], where="post",
                color=SERIES[j % len(SERIES)], label=f"{p['dataset']} (d = {p['d']})")
    ax.axvspan(0.5, 2, color=INK_2, alpha=0.08)
    ax.set_xscale("log")
    ax.set_xlim(0.3, CAP_FACTOR)
    ax.set_xlabel("fits, in multiples of the prediction (log)")
    ax.set_ylabel("share of runs reached (KM)")
    ax.grid(color=GRID)
    ax.legend(fontsize=7.5, loc="upper left", ncol=2)
    fig.suptitle("H15: when the OBL start's archive first holds a subset of <= 10 features, "
                 "5 seeds per dataset", fontsize=10)
    h14._footer(fig, note, "validation (archive)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--experiment", default=EXPERIMENT)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    out = Path(args.out or REPORTS / args.experiment)
    tabs, figs = out / "tables", out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    caps = check_budgets()
    rows = load(args.experiment)
    for r in rows:
        if r["finished"] and r["cap"] != caps[r["dataset"]]:
            raise SystemExit(f"{r['run_id']}: cap {r['cap']} != h15_budgets.json")
    per = per_dataset(rows)
    sl = slope(per)
    verdict = criterion(per, sl) | {"n_runs": sum(r["finished"] for r in rows)}
    h14.write_csv(tabs / "runs.csv", rows)
    h14.write_csv(tabs / "per_dataset.csv", per)
    h14.write_csv(tabs / "slope.csv", [sl])
    (tabs / "verdict.json").write_text(json.dumps(verdict, indent=1), encoding="utf-8")
    note = f"{verdict['n_runs']} runs of {args.experiment} (decision tree, Sentinel); h15_report.py"
    fig_scaling(rows, per, sl, note, figs / "F1_fits_to_reach_vs_d.png")
    fig_ratio(rows, per, note, figs / "F2_ratio_to_prediction.png")
    fig_km(rows, per, note, figs / "F3_reach_km.png")
    print(json.dumps(verdict, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
