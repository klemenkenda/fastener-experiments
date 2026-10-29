"""H8: does an LLM relevance prior let FASTENER reach its target in fewer fits?

The criterion as registered for H8-E01 (HYPOTHESES.md, H8 and its revision of
2026-10-30; EXPERIMENTS.md, H8-E01), datasets as the unit:

* the measure is H0's (h0_convergence.py): from every trajectory snapshot the
  validation AUF (K = 10) of its front; per pair of arms, dataset and seed the
  target is the lower of the two runs' final values, and each run's result is
  the cumulative fits at its first snapshot at or above it;
* per dataset the effect is the mean over seeds of log2(opponent's fits /
  the arm's fits): positive means the arm got there sooner;
* for each model m: (i) `fastener_llm_m` against `fastener`, (ii) against
  `fastener_llm_m_scrambled`; each needs more positive datasets than negative
  and a two-sided Wilcoxon p < 0.05, Holm-corrected over the three models
  within the part. H8 is supported if (i) and (ii) hold for at least one model.

Beside it: the proposer and ablation arms, H10's mRMR seed, end-of-budget
test AUF, the cost of the model calls, and how the priors relate to mutual
information and to their scrambled twins.

    python experiments/make_report.py --experiment H8-E01      # run_keys.csv
    python experiments/h8_report.py --experiment H8-E01
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

import _bootstrap  # noqa: F401
import h0_convergence as h0
import trajectory as trajectory_io
from make_report import GRID, INK_2, SERIES, _style, holm, wilcoxon_p
import provenance

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
RESULTS = provenance.RESULTS_DIR
PRIORS = HERE / "priors"
MODELS = ("opus", "sonnet", "haiku")
USES = ("mating", "mutation", "initial")
STOCK = "fastener"


def arm(m: str, kind: str = "") -> str:
    return f"fastener_llm_{m}" + (f"_{kind}" if kind else "")


CRITERION = [(m, part, arm(m), STOCK if part == "i" else arm(m, "scrambled"))
             for part in ("i", "ii") for m in MODELS]
BESIDE = ([(arm(m, "proposer"), arm(m)) for m in MODELS]
          + [(arm(m, "proposer"), STOCK) for m in MODELS]
          + [(arm("opus", u), STOCK) for u in USES]
          + [(arm("opus", u), arm("opus")) for u in USES]
          + [("fastener_seed_mrmr", STOCK)]
          + [(arm(m), "fastener_seed_mrmr") for m in MODELS])


def _footer(fig, note: str, split: str) -> None:
    fig.text(0.01, 0.01, f"{split} split  |  {note}", fontsize=7, color=INK_2)


def _method(m: str) -> str:
    return m[:-5] if m.endswith("_lgbm") else m


def run_keys(experiment: str) -> List[Dict]:
    with open(REPORTS / experiment / "tables" / "run_keys.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["method"] = _method(r["method"])
        r["seed"] = int(r["seed"]) if r["seed"] not in ("", None) else None
    return rows


def curves(rows) -> Dict[Tuple[str, str, int], h0.Curve]:
    """(method, dataset, seed) -> the run's validation-AUF step curve."""
    out = {}
    for r in rows:
        trajs = sorted((RESULTS / r["run_id"] / "trajectories").glob("*.jsonl"))
        if not trajs:
            continue
        out[(r["method"], r["dataset"], r["seed"])] = h0.curve(trajectory_io.read(trajs[0]))
    return out


def pair_rows(cur, a: str, b: str) -> List[Dict]:
    """Per dataset and seed: target, fits of a and b, effect log2(b / a)."""
    rows = []
    for (m, d, s), ca in sorted(cur.items()):
        if m != a or (b, d, s) not in cur:
            continue
        cb = cur[(b, d, s)]
        target = min(ca[-1][1], cb[-1][1])
        fa, fb = h0.fits_to_target(ca, target), h0.fits_to_target(cb, target)
        rows.append({"arm": a, "opponent": b, "dataset": d, "seed": s,
                     "target": target, "fits_arm": fa, "fits_opponent": fb,
                     "effect": float(np.log2(fb / fa))})
    return rows


def compare(cur, a: str, b: str, **meta) -> Dict:
    seeds = pair_rows(cur, a, b)
    by_ds: Dict[str, List[float]] = {}
    for r in seeds:
        by_ds.setdefault(r["dataset"], []).append(r["effect"])
    ds = sorted(by_ds)
    e = np.array([np.mean(by_ds[d]) for d in ds])
    return {**meta, "arm": a, "opponent": b, "n_datasets": len(ds),
            "wins": int((e > 0).sum()), "ties": int((e == 0).sum()),
            "losses": int((e < 0).sum()),
            "mean_effect": float(e.mean()) if len(e) else float("nan"),
            "median_effect": float(np.median(e)) if len(e) else float("nan"),
            "p": wilcoxon_p(e.tolist()), "datasets": ds, "effects": e.tolist(),
            "seed_rows": seeds}


def criterion(cur) -> List[Dict]:
    out = [compare(cur, a, b, model=m, part=part) for m, part, a, b in CRITERION]
    for part in ("i", "ii"):
        grp = [r for r in out if r["part"] == part]
        for r, ph in zip(grp, holm([r["p"] for r in grp])):
            r["p_holm"] = ph
            r["holds"] = bool(r["wins"] > r["losses"] and ph < 0.05)
    return out


def verdict(crit) -> Dict:
    per_model = {m: {p: next(r["holds"] for r in crit if r["model"] == m and r["part"] == p)
                     for p in ("i", "ii")} for m in MODELS}
    for m in per_model:
        per_model[m]["both"] = per_model[m]["i"] and per_model[m]["ii"]
    return {"verdict": "supported" if any(v["both"] for v in per_model.values())
            else "not supported", "models": per_model}


def end_auf(rows) -> List[Dict]:
    """Mean end-of-budget test AUF (K = 10) per arm over datasets."""
    acc: Dict[str, Dict[str, List[float]]] = {}
    for r in rows:
        if r["auf_k10"] not in ("", None):
            acc.setdefault(r["method"], {}).setdefault(r["dataset"], []).append(float(r["auf_k10"]))
    return [{"arm": m, "n_datasets": len(by),
             "mean_auf_k10": float(np.mean([np.mean(v) for v in by.values()]))}
            for m, by in sorted(acc.items())]


def spend(rows) -> List[Dict]:
    """Calls, tokens, dollars and seconds of the model calls, per source."""
    out = []

    def add(source, model, path):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            u = e["response"].get("usage") or {}
            out.append({"source": source, "model": model or e["request"]["model"],
                        "prompt_tokens": u.get("prompt_tokens", 0),
                        "completion_tokens": u.get("completion_tokens", 0),
                        "cost": float(u.get("cost") or 0.0),
                        "seconds": float(e.get("seconds") or 0.0)})
    if (PRIORS / "calls.jsonl").is_file():
        add("priors", None, PRIORS / "calls.jsonl")
    for r in rows:
        for f in (RESULTS / r["run_id"]).glob("llm_calls_*.jsonl"):
            add("proposer", None, f)
    summary = {}
    for e in out:
        k = (e["source"], e["model"])
        s = summary.setdefault(k, {"source": k[0], "model": k[1], "calls": 0,
                                   "prompt_tokens": 0, "completion_tokens": 0,
                                   "cost": 0.0, "seconds": 0.0})
        s["calls"] += 1
        for f in ("prompt_tokens", "completion_tokens", "cost", "seconds"):
            s[f] += e[f]
    return sorted(summary.values(), key=lambda s: (s["source"], s["model"]))


def prior_agreement(datasets: List[str]) -> List[Dict]:
    """Spearman of each prior with mutual information on the training split,
    and with its scrambled twin."""
    from scipy.stats import spearmanr
    import fast_mi
    import llm_guidance as lg
    import protocol
    from datasets import load
    out = []
    for d in datasets:
        ds = load(d, max_rows=protocol.ROW_CAP)
        mi = fast_mi.mutual_info_classif(ds.X_train, ds.y_train, random_state=0)
        for m, model_id in zip(MODELS, ("anthropic/claude-opus-5.5",
                                         "anthropic/claude-sonnet-5.5",
                                         "anthropic/claude-haiku-5.5")):
            p, ps = lg.prior_path(d, model_id, False), lg.prior_path(d, model_id, True)
            if not p.is_file():
                continue
            a = lg.load_prior(p)
            row = {"dataset": d, "model": m, "n_features": len(a),
                   "spearman_mi": float(spearmanr(a, mi)[0]),
                   "distinct_scores": int(len(np.unique(a)))}
            if ps.is_file():
                row["spearman_scrambled"] = float(spearmanr(a, lg.load_prior(ps))[0])
            out.append(row)
    return out


# ------------------------------------------------------------------ figures
def fig_criterion(crit, note, path):
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(17, 5), sharey=True)
    for ax, part, title in zip(axes, ("i", "ii"),
                               ("(i) LLM prior against stock FASTENER",
                                "(ii) LLM prior against the scrambled prior")):
        grp = [r for r in crit if r["part"] == part]
        for i, r in enumerate(grp):
            e = np.array(r["effects"])
            x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(e))
            ax.scatter(x, e, s=16, color=SERIES[i], alpha=0.9 if r["holds"] else 0.5,
                       facecolors=None if r["holds"] else "none")
            ax.plot([i - 0.3, i + 0.3], [r["mean_effect"]] * 2, color="k", lw=2)
            ax.annotate(f"{r['wins']}-{r['ties']}-{r['losses']}\np={r['p_holm']:.2g}"
                        + ("\nholds" if r["holds"] else ""),
                        (i, 0), xycoords=("data", "axes fraction"), xytext=(0, -34),
                        textcoords="offset points", ha="center", va="top", fontsize=7.5,
                        annotation_clip=False)
        ax.axhline(0, color=INK_2, lw=0.8)
        ax.set_xticks(range(len(grp)), [r["model"] for r in grp])
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", color=GRID)
    axes[0].set_ylabel("log2(opponent's fits / LLM arm's fits) to the common target\n"
                       "(per dataset, mean over seeds; > 0 = LLM arm sooner)")
    fig.suptitle("H8: fits to a common validation target; one point per dataset, bar = mean; "
                 "filled = holds after Holm over the three models", fontsize=10)
    _footer(fig, note, "validation")
    fig.tight_layout(rect=(0, 0.12, 1, 0.94))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_beside(beside, note, path):
    import matplotlib.pyplot as plt
    _style(plt)
    fig, ax = plt.subplots(figsize=(17, 5.2))
    for i, r in enumerate(beside):
        e = np.array(r["effects"])
        x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(e))
        ax.scatter(x, e, s=12, color=SERIES[i % len(SERIES)], alpha=0.7)
        ax.plot([i - 0.3, i + 0.3], [r["mean_effect"]] * 2, color="k", lw=2)
        ax.annotate(f"{r['wins']}-{r['ties']}-{r['losses']}\np={r['p']:.2g}", (i, 0),
                    xycoords=("data", "axes fraction"), xytext=(0, -62),
                    textcoords="offset points", ha="center", va="top", fontsize=7,
                    annotation_clip=False)
    short = lambda a: a.replace("fastener_", "").replace("llm_", "")
    ax.set_xticks(range(len(beside)), [f"{short(r['arm'])}\nvs {short(r['opponent'])}"
                                       for r in beside], fontsize=7, rotation=0)
    ax.axhline(0, color=INK_2, lw=0.8)
    ax.grid(axis="y", color=GRID)
    ax.set_ylabel("log2(opponent's fits / arm's fits)\n(per dataset; > 0 = arm sooner)")
    ax.set_title("Beside the criterion: proposer, single-operator ablations (Opus), "
                 "mRMR seed; unadjusted p, descriptive", fontsize=10)
    _footer(fig, note, "validation")
    fig.tight_layout(rect=(0, 0.16, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_end_auf(rows, note, path):
    import matplotlib.pyplot as plt
    _style(plt)
    acc: Dict[str, Dict[str, List[float]]] = {}
    for r in rows:
        if r["auf_k10"] not in ("", None):
            acc.setdefault(r["method"], {}).setdefault(r["dataset"], []).append(float(r["auf_k10"]))
    arms = sorted(acc, key=lambda a: (a != STOCK, a))
    base = {d: np.mean(v) for d, v in acc.get(STOCK, {}).items()}
    fig, ax = plt.subplots(figsize=(17, 4.8))
    for i, a in enumerate(arms):
        diffs = [np.mean(v) - base[d] for d, v in acc[a].items() if d in base]
        x = i + np.random.default_rng(i).uniform(-0.18, 0.18, len(diffs))
        ax.scatter(x, diffs, s=12, color=SERIES[i % len(SERIES)], alpha=0.7)
        if diffs:
            ax.plot([i - 0.3, i + 0.3], [np.mean(diffs)] * 2, color="k", lw=2)
    ax.axhline(0, color=INK_2, lw=0.8)
    ax.set_xticks(range(len(arms)), [a.replace("fastener_", "") for a in arms],
                  rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("test AUF (K = 10) minus stock FASTENER's\n(per dataset, mean over seeds)")
    ax.set_title("End of the 1,000-fit budget: every arm against stock FASTENER (descriptive)",
                 fontsize=10)
    ax.grid(axis="y", color=GRID)
    _footer(fig, note, "test")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def fig_priors(agree, costs, note, path):
    import matplotlib.pyplot as plt
    _style(plt)
    fig, axes = plt.subplots(1, 2, figsize=(17, 4.8), gridspec_kw={"width_ratios": [3, 1]})
    ds = sorted({r["dataset"] for r in agree})
    x = np.arange(len(ds))
    for j, m in enumerate(MODELS):
        v = {r["dataset"]: r for r in agree if r["model"] == m}
        axes[0].bar(x + (j - 1) * 0.27, [v[d]["spearman_mi"] if d in v else np.nan for d in ds],
                    0.27, color=SERIES[j], label=f"{m}: prior vs MI")
        axes[0].scatter(x + (j - 1) * 0.27,
                        [v[d].get("spearman_scrambled", np.nan) if d in v else np.nan for d in ds],
                        color="k", marker="_", s=60, zorder=3,
                        label="prior vs its scrambled twin" if j == 0 else None)
    axes[0].axhline(0, color=INK_2, lw=0.8)
    axes[0].set_xticks(x, ds, rotation=40, ha="right", fontsize=8)
    axes[0].set_ylabel("Spearman correlation")
    axes[0].legend(fontsize=8, ncol=4, loc="lower left")
    axes[0].grid(axis="y", color=GRID)
    axes[0].set_title("What the priors say: agreement with mutual information on the "
                      "training split, and with the scrambled prior", fontsize=10)
    labels = [f"{c['source']}\n{c['model'].split('/')[-1]}" for c in costs]
    axes[1].bar(range(len(costs)), [c["cost"] for c in costs], color=SERIES[3])
    axes[1].set_xticks(range(len(costs)), labels, fontsize=7, rotation=30, ha="right")
    axes[1].set_ylabel("US$ (OpenRouter)")
    axes[1].set_title(f"Model calls: ${sum(c['cost'] for c in costs):.2f} in all", fontsize=10)
    axes[1].grid(axis="y", color=GRID)
    _footer(fig, note, "train")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_csv(path: Path, rows: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: List[str] = []
    for r in rows:
        keys += [k for k in r if k not in keys and k not in ("datasets", "effects", "seed_rows")]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--experiment", required=True)
    ap.add_argument("--no-priors", action="store_true",
                    help="skip the prior-agreement table (loads every dataset)")
    args = ap.parse_args(argv)
    rows = run_keys(args.experiment)
    cur = curves(rows)
    crit = criterion(cur)
    v = verdict(crit)
    beside = [compare(cur, a, b) for a, b in BESIDE]
    beside = [r for r in beside if r["n_datasets"]]
    costs = spend(rows)
    datasets = sorted({r["dataset"] for r in rows})
    agree = [] if args.no_priors else prior_agreement(datasets)

    out = REPORTS / args.experiment
    tabs, figs = out / "tables", out / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    write_csv(tabs / "criterion.csv", crit)
    write_csv(tabs / "beside.csv", beside)
    write_csv(tabs / "per_seed.csv", [s for r in crit + beside for s in r["seed_rows"]])
    write_csv(tabs / "end_auf.csv", end_auf(rows))
    if costs:
        write_csv(tabs / "spend.csv", costs)
    if agree:
        write_csv(tabs / "prior_agreement.csv", agree)
    (tabs / "verdict.json").write_text(json.dumps(v, indent=1), encoding="utf-8")
    note = f"{len(rows)} runs of {args.experiment}; LightGBM, 1,000 fits"
    fig_criterion(crit, note, figs / "F1_H8_criterion.png")
    if beside:
        fig_beside(beside, note, figs / "F2_beside.png")
    fig_end_auf(rows, note, figs / "F3_end_auf.png")
    if agree or costs:
        fig_priors(agree, costs, note, figs / "F4_priors_and_cost.png")
    print(json.dumps(v))
    for r in crit + beside:
        extra = f" holm {r['p_holm']:.3g} holds={r['holds']}" if "p_holm" in r else ""
        print(f"{r['arm']:<30} vs {r['opponent']:<30} {r['wins']}-{r['ties']}-{r['losses']} "
              f"mean {r['mean_effect']:+.3f} p {r['p']:.3g}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
