"""H13 (post hoc): reach against matched-size quality of three NSGA-II arms.

The analysis registered as H13-E01 (HYPOTHESES.md, H13; EXPERIMENTS.md,
H13-E01; DEC-55) on the finished runs of `nsga2` (OBL start),
`nsga2_sparse` (1-30 start) and `nsgaii_miip` (the full NSGAII-MIIP) in
H1-E02 and H5H6-E01 to -E03, read from `experiments/distilled_logs/` only.
No search is run and no model is fitted. The measures are in
`h13_coverage.py`.

Criterion, per grid, `nsga2_sparse` against `nsga2`, datasets as the unit:
(a) reach R: more wins than losses and a two-sided Wilcoxon p < 0.05 after
Holm over the four grids; (b) the 95% bootstrap interval of the mean
matched-size difference within +/-0.02 F1; (c) the reach term at least 75% of
the summed absolute AUF difference. Supported (post hoc) if (a)-(c) hold in
all three H5H6 grids; reversed if (c) is below 50% in at least two of them.
H1-E02 is read the same way, beside the verdict.

Beside it, Q2-Q8: reach against d and budget, NSGAII-MIIP as a third arm,
the large-subset end, missing cells (sensitivity S1-S3), the classifier on
common datasets, time to reach, stagnation stops.

    python experiments/h13_report.py           # -> reports/H13-E01/{tables,figures}
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

import _bootstrap  # noqa: F401
import h13_coverage as cov
from make_report import GRID, INK_2, SERIES, _style, holm, wilcoxon_p
import run_queue

HERE = Path(__file__).resolve().parent
DISTILLED = HERE / "distilled_logs"
REPORTS = HERE / "reports"
EXPERIMENT = "H13-E01"
GRIDS = ("H1-E02", "H5H6-E01", "H5H6-E02", "H5H6-E03")
H5H6 = GRIDS[1:]
LEARNER = {"H1-E02": "decision tree (H1)", "H5H6-E01": "decision tree",
           "H5H6-E02": "random forest", "H5H6-E03": "LightGBM"}
SKIP_FILE = HERE / "h5h6_skip.txt"
SEEDS = tuple(range(2020, 2025))
ARMS = ("nsga2", "nsga2_sparse", "nsgaii_miip")
LABEL = {"nsga2": "OBL start", "nsga2_sparse": "1-30 start",
         "nsgaii_miip": "NSGAII-MIIP"}
COLOR = {"nsga2": SERIES[1], "nsga2_sparse": SERIES[0], "nsgaii_miip": SERIES[2]}
PRIMARY = ("nsga2_sparse", "nsga2")
PAIRS = (("nsga2_sparse", "nsga2"), ("nsga2_sparse", "nsgaii_miip"),
         ("nsgaii_miip", "nsga2"))
MARGIN = 0.02              # (b)
SHARE_SUPPORT, SHARE_REVERSED = 0.75, 0.50   # (c)
ALPHA = 0.05
HORIZONS = (0.10, 0.25, 0.50, 1.00)
N_BOOT_GLM = 2000


# ------------------------------------------------------------------- inputs
def _read(grid: str, table: str) -> pd.DataFrame:
    return pd.read_csv(DISTILLED / grid / f"{table}.csv.xz")


def load_grid(grid: str) -> Tuple[List[Dict], List[Dict]]:
    """(finished runs, missing cells) of the three arms in one grid.

    A finished run is one row of `runs` with its final front (`records`) and
    archive snapshots (`curves`). A missing cell is a planned (dataset, arm,
    seed) without one: timed out in the queue, or skipped (h5h6_skip.txt).
    """
    runs = _read(grid, "runs")
    runs = runs[runs["method"].isin(ARMS)]
    recs = _read(grid, "records")
    recs = recs[recs["method"].isin(ARMS)]
    curves = _read(grid, "curves")
    curves = curves[curves["method"].isin(ARMS)]
    rec_by = {k: g.to_dict("records") for k, g in recs.groupby(["run_id", "method", "seed"])}
    cur_by = {k: g.to_dict("records") for k, g in curves.groupby(["run_id", "method", "seed"])}
    out = []
    for r in runs.to_dict("records"):
        key = (r["run_id"], r["method"], r["seed"])
        params = json.loads(r["params"])
        budget = int(params["evaluation_budget_per_seed"])
        d = int(r["dataset_n_features"])
        records = rec_by.get(key, [])
        m = cov.run_measures(records, d)
        t = cov.time_to_reach(cur_by.get(key, []), budget)
        stopped = r.get("stopped_on")
        stopped = stopped if isinstance(stopped, str) else "budget"
        iters = int(r["iterations"])
        out.append({"grid": grid, "run_id": r["run_id"], "dataset": r["dataset"],
                    "method": r["method"], "seed": int(r["seed"]), "d": d,
                    "budget": budget, "fits": int(r["model_fits"]),
                    "iterations": iters, "stopped_on": stopped,
                    "seconds": float(r["elapsed_seconds"]),
                    "proposals": cov.POPULATION * (iters + 1),
                    "median_front": float(np.median([x["n_features"] for x in records]))
                    if records else float("nan"),
                    **m, "ttr": t})
    jobs = _read(grid, "jobs")
    jobs = jobs[jobs["arm"].isin(ARMS)]
    done = {(r["dataset"], r["method"], r["seed"]) for r in out}
    missing = [{"grid": grid, "dataset": j["dataset"], "method": j["arm"],
                "seed": int(j["seed"]), "why": j["state"]}
               for j in jobs.to_dict("records")
               if (j["dataset"], j["arm"], int(j["seed"])) not in done]
    if grid in H5H6:
        datasets = set(jobs["dataset"]) | {r["dataset"] for r in out}
        for ds, arm in run_queue.parse_skip(f"@{SKIP_FILE}"):
            if arm in ARMS and ds in datasets:
                missing += [{"grid": grid, "dataset": ds, "method": arm, "seed": s,
                             "why": "skipped"} for s in SEEDS]
    return out, missing


def imputed(cell: Dict, d: int) -> Dict:
    """S2: a missing run counted as reaching nothing, AUF 0."""
    return {"grid": cell["grid"], "dataset": cell["dataset"], "method": cell["method"],
            "seed": cell["seed"], "d": d, "reach": np.zeros(cov.K, dtype=bool),
            "c": np.zeros(cov.K), "exact": np.full(cov.K, np.nan),
            "auf_k10": 0.0, "auf_k20": 0.0, "auf_kd": 0.0, "best_f1": None,
            "max_front": None, "imputed": True}


def aggregates(runs: Sequence[Dict]) -> Dict:
    """(grid, arm) -> {dataset: cov.aggregate(...)}."""
    by = defaultdict(list)
    for r in runs:
        by[(r["grid"], r["method"], r["dataset"])].append(r)
    out: Dict = defaultdict(dict)
    for (g, m, ds), rs in by.items():
        out[(g, m)][ds] = cov.aggregate(rs)
        out[(g, m)][ds]["d"] = rs[0]["d"]
    return out


def variant(agg: Dict, name: str, grid: str) -> Dict:
    """Restrict the per-dataset aggregates of one grid to a sensitivity
    variant: S0 all, S1 only datasets with 5 finished seeds, S3 only datasets
    every arm of the grid has. (S2 is built from imputed runs.)"""
    arms = [a for a in ARMS if (grid, a) in agg]
    sub = {a: dict(agg[(grid, a)]) for a in arms}
    if name == "S1":
        sub = {a: {d: v for d, v in s.items() if v["n_seeds"] == len(SEEDS)}
               for a, s in sub.items()}
    if name == "S3":
        common = set.intersection(*[set(s) for s in sub.values()])
        sub = {a: {d: v for d, v in s.items() if d in common} for a, s in sub.items()}
    return sub


# --------------------------------------------------------------- statistics
def compare(A: Dict[str, float], B: Dict[str, float], **meta) -> Dict:
    """a - b per dataset both have: wins/ties/losses, mean and median with
    bootstrap intervals, Wilcoxon (zeros dropped), rank-biserial."""
    ds = sorted(d for d in set(A) & set(B)
                if A[d] is not None and B[d] is not None
                and not (np.isnan(A[d]) or np.isnan(B[d])))
    x = np.array([A[d] - B[d] for d in ds])
    lo, hi = cov.bootstrap_ci(x)
    mlo, mhi = cov.bootstrap_ci(x, stat=np.median)
    return {**meta, "n_datasets": len(ds), "wins": int((x > 0).sum()),
            "ties": int((x == 0).sum()), "losses": int((x < 0).sum()),
            "mean_delta": float(x.mean()) if len(x) else float("nan"),
            "mean_lo": lo, "mean_hi": hi,
            "median_delta": float(np.median(x)) if len(x) else float("nan"),
            "median_lo": mlo, "median_hi": mhi,
            "p": wilcoxon_p(x.tolist()) if len(x) else float("nan"),
            "rank_biserial": cov.rank_biserial(x.tolist()),
            "datasets": ds, "deltas": x.tolist()}


def with_holm(rows: List[Dict]) -> List[Dict]:
    ok = [r for r in rows if not np.isnan(r["p"])]
    for r, ph in zip(ok, holm([r["p"] for r in ok])):
        r["p_holm"] = ph
    for r in rows:
        r.setdefault("p_holm", float("nan"))
    return rows


def scalar(sub: Dict, arm: str, measure: str) -> Dict[str, float]:
    return {d: v[measure] for d, v in sub.get(arm, {}).items()}


def pair_terms(sub: Dict, a: str, b: str) -> Dict[str, Dict]:
    """Per dataset both arms have: decomposition, matched-size difference
    (<= k and exactly k), AUF difference."""
    out = {}
    for ds in sorted(set(sub.get(a, {})) & set(sub.get(b, {}))):
        A, B = sub[a][ds], sub[b][ds]
        reach, quality = cov.decompose(A["r"], A["c_bar"], B["r"], B["c_bar"])
        out[ds] = {"dataset": ds, "d": A["d"], "reach_term": reach,
                   "quality_term": quality, "auf_delta": A["auf_k10"] - B["auf_k10"],
                   "matched": cov.matched_difference(A["r"], A["c_bar"], B["r"], B["c_bar"]),
                   "matched_exact": cov.matched_difference(A["exact_share"], A["exact_bar"],
                                                           B["exact_share"], B["exact_bar"]),
                   "R_a": A["R"], "R_b": B["R"]}
    return out


def matched_summary(terms: Dict[str, Dict], key: str = "matched") -> Dict:
    x = np.array([t[key] for t in terms.values() if t[key] is not None])
    lo, hi = cov.bootstrap_ci(x)
    return {"n_matched": len(x), "n_unmatched": len(terms) - len(x),
            "mean": float(x.mean()) if len(x) else float("nan"), "lo": lo, "hi": hi,
            "within_margin": bool(len(x) and -MARGIN < lo and hi < MARGIN)}


def criterion(agg_by_variant: Dict[str, Dict]) -> Tuple[List[Dict], Dict]:
    """Q1: (a), (b), (c) per grid for the primary pair, under one variant."""
    rows = []
    for g in GRIDS:
        sub = agg_by_variant[g]
        a, b = PRIMARY
        ra = compare(scalar(sub, a, "R"), scalar(sub, b, "R"), grid=g, part="a")
        terms = pair_terms(sub, a, b)
        mb = matched_summary(terms)
        mx = matched_summary(terms, "matched_exact")
        share = cov.reach_share([(t["reach_term"], t["quality_term"]) for t in terms.values()])
        rows.append({**ra, "b": mb, "b_exact": mx, "reach_share": share,
                     "n_terms": len(terms), "terms": terms})
    with_holm(rows)
    for r in rows:
        r["a_holds"] = bool(r["wins"] > r["losses"] and r["p_holm"] < ALPHA)
        r["b_holds"] = r["b"]["within_margin"]
        r["c_holds"] = bool(r["reach_share"] >= SHARE_SUPPORT)
    h = [r for r in rows if r["grid"] in H5H6]
    if all(r["a_holds"] and r["b_holds"] and r["c_holds"] for r in h):
        v = "supported (post hoc)"
    elif sum(r["reach_share"] < SHARE_REVERSED for r in h) >= 2:
        v = "reversed (post hoc)"
    else:
        v = "not supported (post hoc)"
    return rows, {"verdict": v, **{r["grid"]: {p: r[f"{p}_holds"] for p in "abc"}
                                   for r in rows}}


def pairwise(agg: Dict, measures: Sequence[str], grids=H5H6) -> List[Dict]:
    """Q3/Q4: every pair, per grid and measure, Holm over the 3 pairs."""
    out = []
    for g in grids:
        sub = variant(agg, "S0", g)
        for m in measures:
            fam = []
            for a, b in PAIRS:
                if a not in sub or b not in sub:
                    continue
                if m == "matched":
                    t = pair_terms(sub, a, b)
                    A = {d: v["matched"] for d, v in t.items() if v["matched"] is not None}
                    B = {d: 0.0 for d in A}
                    r = compare(A, B, grid=g, measure=m, a=a, b=b)
                    r["reach_share"] = cov.reach_share(
                        [(v["reach_term"], v["quality_term"]) for v in t.values()])
                else:
                    r = compare(scalar(sub, a, m), scalar(sub, b, m),
                                grid=g, measure=m, a=a, b=b)
                fam.append(r)
            out += with_holm(fam)
    return out


# ------------------------------------------------------------ Q2: d, budget
def reach_model(runs: Sequence[Dict]) -> List[Dict]:
    """Per arm and grid: logistic reach(10) ~ log2 d + log2(budget/pop), with
    a dataset-cluster bootstrap; d50 at the grid's median budget. A fit with
    complete separation is flagged; its coefficients are not read."""
    from sklearn.linear_model import LogisticRegression
    out = []
    for g in GRIDS:
        for arm in ARMS:
            rs = [r for r in runs if r["grid"] == g and r["method"] == arm]
            if not rs:
                continue
            X = np.array([[np.log2(r["d"]), np.log2(r["budget"] / cov.POPULATION)]
                          for r in rs])
            y = np.array([bool(r["reach"][-1]) for r in rs])
            ds = np.array([r["dataset"] for r in rs])
            row = {"grid": g, "method": arm, "n_runs": len(rs),
                   "n_datasets": len(set(ds)), "reach_rate": float(y.mean())}
            if y.all() or not y.any():
                out.append({**row, "note": "all runs alike; no fit"})
                continue

            def fit(Xs, ys):
                m = LogisticRegression(C=1e6, max_iter=10_000).fit(Xs, ys)
                return np.r_[m.intercept_, m.coef_[0]]

            beta = fit(X, y)
            sep = _separated(X, y)
            rng = np.random.default_rng(cov.BOOT_SEED)
            uniq = np.unique(ds)
            boots = []
            for _ in range(N_BOOT_GLM):
                pick = rng.choice(uniq, size=len(uniq), replace=True)
                idx = np.concatenate([np.where(ds == u)[0] for u in pick])
                if y[idx].all() or not y[idx].any():
                    continue
                boots.append(fit(X[idx], y[idx]))
            boots = np.array(boots)
            z = float(np.median(X[:, 1]))
            d50 = 2 ** (-(beta[0] + beta[2] * z) / beta[1]) if beta[1] != 0 else float("nan")
            row.update({"b0": beta[0], "b_log2d": beta[1], "b_log2budget": beta[2],
                        "b_log2d_lo": float(np.quantile(boots[:, 1], 0.025)) if len(boots) else float("nan"),
                        "b_log2d_hi": float(np.quantile(boots[:, 1], 0.975)) if len(boots) else float("nan"),
                        "b_log2budget_lo": float(np.quantile(boots[:, 2], 0.025)) if len(boots) else float("nan"),
                        "b_log2budget_hi": float(np.quantile(boots[:, 2], 0.975)) if len(boots) else float("nan"),
                        "n_boot": len(boots), "d50_at_median_budget": float(d50),
                        "separated": sep,
                        "note": "complete separation: read d50 only" if sep else ""})
            out.append(row)
    return out


def _separated(X: np.ndarray, y: np.ndarray) -> bool:
    """Complete separation on log2 d alone: every reaching run has a smaller
    (or every one a larger) d than every non-reaching run."""
    a, b = X[y, 0], X[~y, 0]
    return bool(a.max() < b.min() or a.min() > b.max())


def reach_by_dataset(runs: Sequence[Dict]) -> List[Dict]:
    """Per grid, arm and dataset: d, budget, the analytic OBL start reach,
    the observed reach at the start (archive at generation 0), in the archive
    at the end, and on the final front; lost reach."""
    by = defaultdict(list)
    for r in runs:
        by[(r["grid"], r["method"], r["dataset"])].append(r)
    out = []
    for (g, m, ds), rs in sorted(by.items()):
        d = rs[0]["d"]
        arch = [r["ttr"]["reached"] for r in rs]
        front = [bool(r["reach"][-1]) for r in rs]
        out.append({"grid": g, "method": m, "dataset": ds, "d": d,
                    "budget": rs[0]["budget"], "n_seeds": len(rs),
                    "obl_start_analytic": cov.obl_start_reach(d) if m != "nsga2_sparse" else 1.0,
                    "reach_start": float(np.mean([r["ttr"]["at_start"] for r in rs])),
                    "reach_archive_end": float(np.mean(arch)),
                    "reach_front_end": float(np.mean(front)),
                    "lost_reach": int(sum(a and not f for a, f in zip(arch, front)))})
    return out


# ------------------------------------------------------------ Q5: missing
def missing_table(runs, missing) -> List[Dict]:
    out = []
    for g in GRIDS:
        for arm in ARMS:
            fin = [r for r in runs if r["grid"] == g and r["method"] == arm]
            if not fin and not any(c["grid"] == g and c["method"] == arm for c in missing):
                continue
            mc = [c for c in missing if c["grid"] == g and c["method"] == arm]
            per_ds = defaultdict(int)
            for c in mc:
                per_ds[c["dataset"]] += 1
            out.append({"grid": g, "method": arm, "finished": len(fin),
                        "timeout": sum(c["why"] == "timeout" for c in mc),
                        "skipped": sum(c["why"] == "skipped" for c in mc),
                        "other": sum(c["why"] not in ("timeout", "skipped") for c in mc),
                        "datasets_all_missing": sum(v == len(SEEDS) for v in per_ds.values()),
                        "datasets_some_missing": sum(0 < v < len(SEEDS) for v in per_ds.values())})
    return out


def sensitivity(runs, missing) -> List[Dict]:
    """Q1 (a), (c) and Q3's AUF under S0-S3; whether a decision changes."""
    agg = aggregates(runs)
    d_of = {(r["grid"], r["dataset"]): r["d"] for r in runs}
    agg_s2 = aggregates(list(runs) + [imputed(c, d_of.get((c["grid"], c["dataset"]), 1))
                                      for c in missing])
    out = []
    for name in ("S0", "S1", "S2", "S3"):
        src = agg_s2 if name == "S2" else agg
        by_grid = {g: variant(src, "S0" if name == "S2" else name, g) for g in GRIDS}
        crit, v = criterion(by_grid)
        for r in crit:
            out.append({"variant": name, "grid": r["grid"], "part": "a",
                        "n_datasets": r["n_datasets"], "wins": r["wins"],
                        "losses": r["losses"], "mean_delta": r["mean_delta"],
                        "p_holm": r["p_holm"], "holds": r["a_holds"]})
            out.append({"variant": name, "grid": r["grid"], "part": "c",
                        "n_datasets": r["n_terms"], "share": r["reach_share"],
                        "holds": r["c_holds"]})
        for g in H5H6:
            sub = by_grid[g]
            fam = [compare(scalar(sub, a, "auf_k10"), scalar(sub, b, "auf_k10"),
                           variant=name, grid=g, part="Q3 auf", a=a, b=b)
                   for a, b in PAIRS if a in sub and b in sub]
            for r in with_holm(fam):
                r["holds"] = bool(r["wins"] > r["losses"] and r["p_holm"] < ALPHA)
                out.append({k: v for k, v in r.items() if k not in ("datasets", "deltas")})
        out.append({"variant": name, "part": "verdict", "verdict": v["verdict"]})
    base = {(r.get("grid"), r["part"], r.get("a"), r.get("b")): r.get("holds")
            for r in out if r["variant"] == "S0"}
    for r in out:
        key = (r.get("grid"), r["part"], r.get("a"), r.get("b"))
        if r["variant"] != "S0" and key in base and "holds" in r:
            r["changes_decision"] = r["holds"] != base[key]
    return out


# ---------------------------------------------------------- Q6: classifier
def classifier_effect(agg) -> List[Dict]:
    """Per arm, datasets with a result under all three classifiers: Friedman
    on R and AUF, then Wilcoxon on the three classifier pairs, Holm over
    three. The same for the sparse-OBL AUF difference."""
    from scipy.stats import friedmanchisquare
    out = []

    def block(name, vals: Dict[str, Dict[str, float]]):
        common = sorted(set.intersection(*[set(v) for v in vals.values()]))
        if len(common) < 3:
            return
        M = np.array([[vals[g][d] for g in H5H6] for d in common])
        try:
            p = float(friedmanchisquare(*M.T).pvalue)
        except ValueError:
            p = float("nan")
        row = {"what": name, "n_datasets": len(common), "friedman_p": p,
               **{f"mean_{LEARNER[g].replace(' ', '_')}": float(M[:, i].mean())
                  for i, g in enumerate(H5H6)}}
        fam = [compare({d: vals[g1][d] for d in common}, {d: vals[g2][d] for d in common},
                       what=name, g1=g1, g2=g2)
               for i, g1 in enumerate(H5H6) for g2 in H5H6[i + 1:]]
        with_holm(fam)
        for f in fam:
            row[f"{f['g1']}-{f['g2']}"] = f"{f['mean_delta']:+.4f} (p_holm {f['p_holm']:.3g})"
        out.append(row)

    for arm in ARMS:
        for m in ("R", "auf_k10"):
            block(f"{arm} {m}", {g: scalar(variant(agg, 'S0', g), arm, m) for g in H5H6})
    a, b = PRIMARY
    delta = {}
    for g in H5H6:
        sub = variant(agg, "S0", g)
        delta[g] = {d: sub[a][d]["auf_k10"] - sub[b][d]["auf_k10"]
                    for d in set(sub[a]) & set(sub[b])}
    block("sparse - OBL auf_k10", delta)
    common = set.intersection(*[set(v) for v in delta.values()])
    for g in H5H6:
        sub = variant(agg, "S0", g)
        t = pair_terms({k: {d: v for d, v in s.items() if d in common} for k, s in sub.items()},
                       a, b)
        out.append({"what": f"reach share on common datasets, {LEARNER[g]}",
                    "n_datasets": len(t),
                    "share": cov.reach_share([(x["reach_term"], x["quality_term"])
                                              for x in t.values()])})
    return out


# ------------------------------------------------------ Q7: time to reach
def time_to_reach(runs) -> Tuple[List[Dict], List[Dict]]:
    """Pooled KM summaries per arm and grid; per-dataset RMST (share of the
    budget, KM within the dataset's seeds) compared per pair, Holm over 3."""
    summ = []
    for g in GRIDS:
        for arm in ARMS:
            rs = [r for r in runs if r["grid"] == g and r["method"] == arm]
            if not rs:
                continue
            t = [r["ttr"]["share"] for r in rs]
            e = [r["ttr"]["reached"] for r in rs]
            ts, s = cov.km(t, e)
            reached_secs = [r["ttr"]["seconds"] for r in rs if r["ttr"]["reached"]]
            row = {"grid": g, "method": arm, "n_runs": len(rs),
                   "reached": int(sum(e)),
                   **{f"reached_by_{int(h * 100)}pct": cov.km_reached_by(t, e, h)
                      for h in HORIZONS},
                   "median_share": float(ts[np.argmax(1 - s >= 0.5)])
                   if len(s) and (1 - s >= 0.5).any() else float("nan"),
                   "median_seconds_reached": float(np.median(reached_secs))
                   if reached_secs else float("nan"),
                   "lost_reach": int(sum(r["ttr"]["reached"] and not r["reach"][-1] for r in rs))}
            summ.append(row)
    rm: Dict = defaultdict(dict)
    by = defaultdict(list)
    for r in runs:
        by[(r["grid"], r["method"], r["dataset"])].append(r)
    for (g, m, ds), rs in by.items():
        rm[(g, m)][ds] = cov.rmst([r["ttr"]["share"] for r in rs],
                                  [r["ttr"]["reached"] for r in rs])
    tests = []
    for g in GRIDS:
        fam = [compare(rm[(g, a)], rm[(g, b)], grid=g, measure="rmst_share", a=a, b=b)
               for a, b in PAIRS if (g, a) in rm and (g, b) in rm]
        tests += with_holm(fam)
    return summ, tests


# ------------------------------------------------------- Q8: stagnation
def stagnation(runs) -> Tuple[List[Dict], List[Dict]]:
    summ = []
    for g in GRIDS:
        for arm in ARMS:
            rs = [r for r in runs if r["grid"] == g and r["method"] == arm]
            if not rs:
                continue
            st = [r for r in rs if r["stopped_on"] == "stagnation"]
            bu = [r for r in rs if r["stopped_on"] != "stagnation"]
            summ.append({"grid": g, "method": arm, "n_runs": len(rs),
                         "stagnation": len(st),
                         "median_fits_share_at_stop": float(np.median(
                             [r["fits"] / r["budget"] for r in st])) if st else float("nan"),
                         "R_stopped": float(np.mean([r["reach"][-1] for r in st])) if st else float("nan"),
                         "R_budget": float(np.mean([r["reach"][-1] for r in bu])) if bu else float("nan"),
                         "median_repeat_share": float(np.median(
                             [1 - r["fits"] / r["proposals"] for r in rs]))})
    per_ds = []
    by = defaultdict(list)
    for r in runs:
        by[(r["grid"], r["method"], r["dataset"])].append(r)
    for (g, m, ds), rs in sorted(by.items()):
        k = float(np.nanmedian([r["median_front"] for r in rs]))
        per_ds.append({"grid": g, "method": m, "dataset": ds, "d": rs[0]["d"],
                       "median_front": k,
                       "expected_flips": cov.expected_flips(k, rs[0]["d"])
                       if 0 < k < rs[0]["d"] else float("nan"),
                       "median_repeat_share": float(np.median(
                           [1 - r["fits"] / r["proposals"] for r in rs])),
                       "stagnation": sum(r["stopped_on"] == "stagnation" for r in rs),
                       "n_seeds": len(rs)})
    return summ, per_ds


# ------------------------------------------------------ reproduction check
def reproduction(runs) -> List[Dict]:
    """Per grid: this script's AUF (K = 10, 20) per run against the grid
    report's own run_keys.csv. A difference is reported, never adjusted."""
    out = []
    for g in GRIDS:
        path = REPORTS / g / "tables" / "run_keys.csv"
        if not path.is_file():
            out.append({"grid": g, "note": "no run_keys.csv"})
            continue
        with open(path, encoding="utf-8") as fh:
            ref = {(r["run_id"], r["method"].removesuffix("_lgbm").removesuffix("_rf"),
                    int(r["seed"])): r for r in csv.DictReader(fh)}
        diffs = {"auf_k10": [], "auf_k20": []}
        unmatched = 0
        for r in runs:
            if r["grid"] != g:
                continue
            x = ref.get((r["run_id"], r["method"], r["seed"]))
            if x is None:
                unmatched += 1
                continue
            for m in diffs:
                if x.get(m) not in (None, ""):
                    diffs[m].append(abs(r[m] - float(x[m])))
        out.append({"grid": g, "runs": sum(r["grid"] == g for r in runs),
                    "not_in_report": unmatched,
                    **{f"max_abs_diff_{m}": max(v) if v else float("nan")
                       for m, v in diffs.items()},
                    **{f"n_diff_{m}": sum(x > 1e-9 for x in v) for m, v in diffs.items()}})
    return out


# ------------------------------------------------------------------ figures
def _footer(fig, note: str, split: str) -> None:
    fig.text(0.01, 0.01, f"{split} split  |  {note}", fontsize=7, color=INK_2)


def _datasets_by_d(terms: Dict[str, Dict]) -> List[str]:
    return sorted(terms, key=lambda d: (terms[d]["d"], d))


def fig_criterion(crit, note, path):
    """Per grid: the AUF difference split into reach and quality terms, one
    bar pair per dataset, datasets by d along x."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(2, 2, figsize=(18, 8), sharey=True)
    for ax, r in zip(axes.flat, crit):
        t = r["terms"]
        ds = _datasets_by_d(t)
        x = np.arange(len(ds))
        ax.bar(x - 0.2, [t[d]["reach_term"] for d in ds], 0.4, color=SERIES[0], label="reach term")
        ax.bar(x + 0.2, [t[d]["quality_term"] for d in ds], 0.4, color=SERIES[1], label="quality term")
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(x, [f"{d} ({t[d]['d']})" for d in ds], rotation=70, ha="right", fontsize=6.5)
        b = r["b"]
        ax.set_title(f"{r['grid']}, {LEARNER[r['grid']]}: reach share {r['reach_share']:.2f}; "
                     f"(a) {r['wins']}-{r['ties']}-{r['losses']} p_holm {r['p_holm']:.2g}; "
                     f"(b) {b['mean']:+.4f} [{b['lo']:+.4f}, {b['hi']:+.4f}], n={b['n_matched']}",
                     fontsize=8.5)
        ax.grid(axis="y", color=GRID)
    axes[0, 0].legend(fontsize=8)
    for ax in axes[:, 0]:
        ax.set_ylabel("AUF (K = 10) difference,\n1-30 start minus OBL start")
    fig.suptitle("H13 (post hoc): the 1-30 start's AUF lead split into reach and quality at "
                 "matched size; datasets by feature count d", fontsize=10)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_reach_vs_d(by_ds, note, path):
    """Q2: final-front reach per dataset against d, per arm; the analytic OBL
    start reach as a line; one panel per grid."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.8), sharey=True)
    dd = np.unique(np.round(np.logspace(np.log10(8), np.log10(4e5), 200)).astype(int))
    for ax, g in zip(axes, GRIDS):
        for arm in ARMS:
            rows = [r for r in by_ds if r["grid"] == g and r["method"] == arm]
            if not rows:
                continue
            jit = {"nsga2": -0.02, "nsga2_sparse": 0.0, "nsgaii_miip": 0.02}[arm]
            ax.scatter([r["d"] for r in rows], [r["reach_front_end"] + jit for r in rows],
                       s=16, color=COLOR[arm], label=LABEL[arm], alpha=0.85)
        ax.plot(dd, [cov.obl_start_reach(int(x)) for x in dd], color=INK_2, lw=1,
                ls="--", label="OBL start, analytic")
        ax.set_xscale("log")
        ax.set_xlabel("features d (log)")
        ax.set_title(f"{g}, {LEARNER[g]}", fontsize=9.5)
        ax.grid(color=GRID)
    axes[0].set_ylabel("share of seeds whose final front\nholds a subset of <= 10 features")
    axes[0].legend(fontsize=7.5, loc="center left")
    fig.suptitle("Reach against feature count; points jittered vertically by arm", fontsize=10)
    _footer(fig, note, "n/a (sizes only)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_pairs(rows, measures, title, ylabel, note, path):
    """Q3/Q4: per grid and measure, one point per dataset for each pair."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, len(measures), figsize=(18, 4.8))
    axes = np.atleast_1d(axes)
    for ax, m in zip(axes, measures):
        sel = [r for r in rows if r["measure"] == m]
        for i, r in enumerate(sel):
            d = np.array(r["deltas"])
            x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(d))
            ax.scatter(x, d, s=10, color=SERIES[PAIRS.index((r["a"], r["b"]))], alpha=0.8)
            ax.plot([i - 0.3, i + 0.3], [r["mean_delta"]] * 2, color="k", lw=2)
            ax.annotate(f"{r['wins']}-{r['ties']}-{r['losses']}\np {r['p_holm']:.2g}",
                        (i, 0), xycoords=("data", "axes fraction"), xytext=(0, -30),
                        textcoords="offset points", ha="center", va="top", fontsize=6.5,
                        annotation_clip=False)
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(range(len(sel)),
                      [f"{r['grid'][-3:]}\n{LABEL[r['a']].split()[0]}-{LABEL[r['b']].split()[0]}"
                       for r in sel], fontsize=6.5)
        ax.set_title(m, fontsize=9.5)
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel(ylabel)
    fig.suptitle(title, fontsize=10)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.12, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_time_to_reach(runs, note, path):
    """Q7: KM curves of reaching k <= 10 in the archive, per grid and arm."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.6), sharey=True)
    for ax, g in zip(axes, GRIDS):
        for arm in ARMS:
            rs = [r for r in runs if r["grid"] == g and r["method"] == arm]
            if not rs:
                continue
            ts, s = cov.km([r["ttr"]["share"] for r in rs], [r["ttr"]["reached"] for r in rs])
            reached = 1 - s if len(s) else np.zeros(0)
            last = reached[-1] if len(reached) else 0.0
            ax.step(np.r_[1e-3, ts, 1.0], np.r_[0.0, reached, last], where="post",
                    color=COLOR[arm], label=f"{LABEL[arm]} ({len(rs)} runs)")
        ax.set_xscale("log")
        ax.set_xlim(0.005, 1.0)
        ax.set_xlabel("share of the fit budget (log)")
        ax.set_title(f"{g}, {LEARNER[g]}", fontsize=9.5)
        ax.grid(color=GRID)
        ax.legend(fontsize=7.5, loc="upper left")
    axes[0].set_ylabel("share of runs whose archive holds\na subset of <= 10 features (KM)")
    fig.suptitle("Time to reach k <= 10, runs pooled within a grid (descriptive; tests per "
                 "dataset in tables/q7_rmst.csv)", fontsize=10)
    _footer(fig, note, "validation (archive)")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_stagnation(per_ds, note, path):
    """Q8: per dataset, the share of proposals that were repeats against d,
    with the expected flips per child 2k/d on a second axis."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.6), sharey=True)
    for ax, g in zip(axes, GRIDS):
        for arm in ARMS:
            rows = [r for r in per_ds if r["grid"] == g and r["method"] == arm]
            if rows:
                ax.scatter([r["d"] for r in rows], [r["median_repeat_share"] for r in rows],
                           s=14, color=COLOR[arm], label=LABEL[arm], alpha=0.85)
        ax.set_xscale("log")
        ax.set_xlabel("features d (log)")
        ax.set_title(f"{g}, {LEARNER[g]}" + ("" if g in ("H5H6-E02", "H5H6-E03")
                                             else " (no stagnation stop)"), fontsize=9.5)
        ax.grid(color=GRID)
    axes[0].set_ylabel("repeat share of proposals,\n1 - fits / (100 x generations)\n(median over seeds)")
    axes[0].legend(fontsize=7.5)
    fig.suptitle("Proposals that cost no fit (already scored), per dataset; E01 against "
                 "E02/E03 is not an ablation of the stop", fontsize=10)
    _footer(fig, note, "n/a")
    fig.tight_layout(rect=(0, 0.04, 1, 0.93))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_sensitivity(sens, note, path):
    """Q5: (a)'s mean reach difference and (c)'s reach share under S0-S3."""
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(14, 4.4))
    x = np.arange(len(GRIDS))
    for j, v in enumerate(("S0", "S1", "S2", "S3")):
        a = [next((r["mean_delta"] for r in sens if r["variant"] == v and r.get("grid") == g
                   and r["part"] == "a"), np.nan) for g in GRIDS]
        c = [next((r["share"] for r in sens if r["variant"] == v and r.get("grid") == g
                   and r["part"] == "c"), np.nan) for g in GRIDS]
        axes[0].bar(x + (j - 1.5) * 0.2, a, 0.2, color=SERIES[j], label=v)
        axes[1].bar(x + (j - 1.5) * 0.2, c, 0.2, color=SERIES[j], label=v)
    axes[1].axhline(SHARE_SUPPORT, color=INK_2, ls="--", lw=0.8)
    for ax, t in zip(axes, ("(a) mean reach difference, 1-30 minus OBL",
                            "(c) reach share of the AUF difference")):
        ax.set_xticks(x, [f"{g}\n{LEARNER[g]}" for g in GRIDS], fontsize=7.5)
        ax.set_title(t, fontsize=9.5)
        ax.grid(axis="y", color=GRID)
    axes[0].legend(fontsize=7.5, ncol=4)
    fig.suptitle("Missing runs: S0 as registered; S1 5 seeds only; S2 missing = reaches "
                 "nothing, AUF 0; S3 datasets every arm has", fontsize=10)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.05, 1, 0.92))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    skip = ("datasets", "deltas", "terms", "b", "b_exact")
    keys: List[str] = []
    for r in rows:
        keys += [k for k in r if k not in keys and k not in skip]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(REPORTS / EXPERIMENT))
    args = ap.parse_args(argv)
    runs, missing = [], []
    for g in GRIDS:
        r, m = load_grid(g)
        runs += r
        missing += m
    agg = aggregates(runs)
    crit, v = criterion({g: variant(agg, "S0", g) for g in GRIDS})
    q2 = reach_model(runs)
    by_ds = reach_by_dataset(runs)
    q3 = pairwise(agg, ("R", "auf_k10", "matched"))
    q4 = pairwise(agg, ("auf_k20", "auf_kd", "best_f1", "max_front"))
    q5 = missing_table(runs, missing)
    sens = sensitivity(runs, missing)
    q6 = classifier_effect(agg)
    q7, q7_tests = time_to_reach(runs)
    q8, q8_ds = stagnation(runs)
    rep = reproduction(runs)

    out = Path(args.out)
    tabs, figs = out / "tables", out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    write_csv(tabs / "q1_criterion.csv",
              [{**r, **{f"b_{k}": x for k, x in r["b"].items()},
                **{f"b_exact_{k}": x for k, x in r["b_exact"].items()}} for r in crit])
    write_csv(tabs / "q1_terms.csv", [{"grid": r["grid"], **t} for r in crit
                                     for t in r["terms"].values()])
    write_csv(tabs / "q2_reach_model.csv", q2)
    write_csv(tabs / "q2_reach_by_dataset.csv", by_ds)
    write_csv(tabs / "q3_pairs.csv", q3)
    write_csv(tabs / "q4_large_end.csv", q4)
    write_csv(tabs / "q5_missing.csv", q5)
    write_csv(tabs / "q5_missing_cells.csv", missing)
    write_csv(tabs / "q5_sensitivity.csv", sens)
    write_csv(tabs / "q6_classifier.csv", q6)
    write_csv(tabs / "q7_time_to_reach.csv", q7)
    write_csv(tabs / "q7_rmst.csv", q7_tests)
    write_csv(tabs / "q8_stagnation.csv", q8)
    write_csv(tabs / "q8_by_dataset.csv", q8_ds)
    write_csv(tabs / "reproduction.csv", rep)
    write_csv(tabs / "run_measures.csv",
              [{k: x for k, x in r.items() if k not in ("reach", "c", "exact", "ttr")}
               | {"reach_k10": bool(r["reach"][-1]), **{f"ttr_{k}": x for k, x in r["ttr"].items()}}
               for r in runs])
    (tabs / "verdict.json").write_text(json.dumps(v, indent=1), encoding="utf-8")

    note = (f"{len(runs)} finished runs of nsga2, nsga2_sparse, nsgaii_miip in "
            f"{', '.join(GRIDS)}; experiments/distilled_logs; h13_report.py")
    fig_criterion(crit, note, figs / "F1_H13_criterion.png")
    fig_reach_vs_d(by_ds, note, figs / "F2_reach_vs_d.png")
    fig_pairs(q3, ("R", "auf_k10", "matched"),
              "Three NSGA-II arms, pair by pair: reach, AUF (K = 10), matched-size "
              "difference; one point per dataset, bar = mean, Holm over the 3 pairs",
              "per-dataset difference a - b", note, figs / "F3_three_arms.png")
    fig_pairs(q4, ("auf_k20", "auf_kd", "best_f1", "max_front"),
              "The large-subset end: AUF at K = 20 and K = d, best unrestricted F1, largest "
              "front subset", "per-dataset difference a - b", note, figs / "F4_large_end.png")
    fig_sensitivity(sens, note, figs / "F5_missing_sensitivity.png")
    fig_time_to_reach(runs, note, figs / "F6_time_to_reach.png")
    fig_stagnation(q8_ds, note, figs / "F7_repeats_and_stagnation.png")
    print(json.dumps(v))
    for r in crit:
        print(f"{r['grid']:<9} (a) {r['wins']}-{r['ties']}-{r['losses']} p_holm {r['p_holm']:.3g} "
              f"(b) {r['b']['mean']:+.4f} [{r['b']['lo']:+.4f}, {r['b']['hi']:+.4f}] "
              f"n={r['b']['n_matched']} (c) {r['reach_share']:.3f}")
    for r in rep:
        print("reproduction", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
