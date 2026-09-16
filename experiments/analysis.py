"""Turn raw run records into the comparison table, the plot, and a sanity check.

The headline comparison is the accuracy-vs-feature-count curve on the UNTOUCHED
test set: for each method, the best test score reachable at a given number of
features, where "best" was chosen on validation.
"""
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from protocol import make_model  # noqa: E402


def probe_relevant_features(ds, n_repeats: int = 5, seed: int = 20200) -> Dict:
    """Empirically estimate which MADELON features carry signal.

    MADELON has 20 relevant features out of 500, but the organisers never
    published which. We estimate the relevant set with permutation importance on
    a model fit to ALL features, using TRAIN and VAL only -- never the test set.

    This is a sanity check on the selectors, not ground truth, and is reported
    as such.
    """
    rng = np.random.RandomState(seed)
    model = make_model().fit(ds.X_train, ds.y_train)
    base = float((model.predict(ds.X_val) == ds.y_val).mean())

    drops = np.zeros(ds.n_features)
    for j in range(ds.n_features):
        col = ds.X_val[:, j].copy()
        acc = 0.0
        for _ in range(n_repeats):
            rng.shuffle(ds.X_val[:, j])
            acc += float((model.predict(ds.X_val) == ds.y_val).mean())
        ds.X_val[:, j] = col          # restore exactly
        drops[j] = base - acc / n_repeats

    ranked = np.argsort(drops)[::-1]
    return {
        "method": "permutation_importance_on_all_features",
        "base_val_accuracy": base,
        "top20_by_importance": ranked[:20].tolist(),
        "importance_of_top20": drops[ranked[:20]].round(5).tolist(),
        "n_features_with_positive_importance": int((drops > 0).sum()),
        "note": ("Estimated, not official ground truth. MADELON is documented to "
                 "have 20 relevant features (5 informative + 15 redundant); the "
                 "official indices were never released."),
    }


def best_by_k(records: List[Dict]) -> Dict[int, Dict]:
    """Best record per feature count, chosen on VALIDATION score."""
    out: Dict[int, Dict] = {}
    for r in records:
        k = r["n_features"]
        if k not in out or r["val_score"] > out[k]["val_score"]:
            out[k] = r
    return out


def monotone_best_upto_k(records: List[Dict]) -> Dict[int, Dict]:
    """Best record using AT MOST k features, chosen on validation.

    This is the fair way to read a curve: a method allowed k features may always
    use fewer, so its score at k should never look worse than at k-1.
    """
    by_k = best_by_k(records)
    out: Dict[int, Dict] = {}
    best = None
    for k in sorted(by_k):
        cand = by_k[k]
        if best is None or cand["val_score"] > best["val_score"]:
            best = cand
        out[k] = best
    return out


def comparison_table(all_results: List[Dict], ks: List[int]) -> List[Dict]:
    """One row per (method, k) with the test score of the val-selected subset."""
    rows = []
    for res in all_results:
        method = res["method"]
        seed = res.get("seed")
        curve = monotone_best_upto_k(res["records"])
        if not curve:
            continue
        available = sorted(curve)
        for k in ks:
            usable = [a for a in available if a <= k]
            if not usable:
                continue
            rec = curve[max(usable)]
            rows.append({
                "method": method,
                "seed": seed,
                "budget_k": k,
                "n_features_used": rec["n_features"],
                "val_f1": round(rec["val_score"], 4),
                "test_f1": round(rec["test_score"], 4),
                "test_accuracy": round(rec["test"]["accuracy"], 4),
                "test_balanced_accuracy": round(rec["test"]["balanced_accuracy"], 4),
                "features": rec["features"],
            })
    return rows


def overlap_with_probe(features: List[int], probe_top: List[int]) -> Dict:
    s, p = set(features), set(probe_top)
    inter = s & p
    return {
        "n_selected": len(s),
        "n_overlap_with_probe_top20": len(inter),
        "overlap_fraction_of_selected": round(len(inter) / len(s), 3) if s else 0.0,
    }


def render_plot(rows: List[Dict], out_path: Path, title: str) -> Path:
    """Accuracy-vs-feature-count on the untouched test set."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Average over seeds for methods that have them (FASTENER).
    series: Dict[str, Dict[int, List[float]]] = {}
    for r in rows:
        series.setdefault(r["method"], {}).setdefault(r["budget_k"], []).append(r["test_f1"])

    style = {
        "fastener": dict(color="#C1440E", lw=2.4, marker="o", zorder=5),
        "kbest_mutual_info": dict(color="#1F6FB2", lw=1.8, marker="s"),
        "kbest_anova_f": dict(color="#4C9F70", lw=1.8, marker="^"),
        "tree_importance": dict(color="#8A6BBE", lw=1.8, marker="v"),
        "rfe_tree": dict(color="#D98F00", lw=1.8, marker="D"),
        "random": dict(color="#999999", lw=1.4, marker="x", ls="--"),
        "all_features": dict(color="#444444", lw=1.2, ls=":"),
    }

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for method, by_k in sorted(series.items()):
        ks = sorted(by_k)
        means = [float(np.mean(by_k[k])) for k in ks]
        kw = style.get(method, dict(lw=1.5, marker="."))
        if method == "all_features":
            ax.axhline(means[-1], label=f"all 500 features ({means[-1]:.3f})",
                       **{k: v for k, v in kw.items() if k in ("color", "lw", "ls")})
            continue
        ax.plot(ks, means, label=method, markersize=5, **kw)
        spread = [by_k[k] for k in ks]
        if any(len(v) > 1 for v in spread):
            lo = [min(v) for v in spread]
            hi = [max(v) for v in spread]
            ax.fill_between(ks, lo, hi, color=kw.get("color", "grey"), alpha=0.15, lw=0)

    ax.set_xscale("log")
    ax.set_xlabel("feature budget k (log scale)")
    ax.set_ylabel("weighted F1 on untouched test set")
    ax.set_title(title)
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="lower right", fontsize=9, framealpha=0.95)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    return out_path


def seed_significance(rows: List[Dict], ks: List[int],
                      stochastic: str = "fastener",
                      deterministic=("tree_importance", "rfe_tree", "kbest_anova_f")) -> List[Dict]:
    """Does the stochastic method's advantage survive its own seed variance?

    The baselines here are deterministic (one value, no seeds), so this is a
    one-sample t-test of the seed scores against that fixed value. With only a
    handful of seeds this has little power -- which is the point: it stops a
    mean difference from being read as a win when the seeds straddle the
    baseline.
    """
    from scipy import stats

    out = []
    for k in ks:
        seed_scores = [r["test_f1"] for r in rows
                       if r["method"] == stochastic and r["budget_k"] == k]
        if len(seed_scores) < 2:
            continue
        base = {r["method"]: r["test_f1"] for r in rows
                if r["budget_k"] == k and r["method"] in deterministic}
        if not base:
            continue
        name = max(base, key=base.get)
        value = base[name]

        t, p = stats.ttest_1samp(seed_scores, value)
        out.append({
            "budget_k": k,
            "n_seeds": len(seed_scores),
            "mean_test_f1": round(float(np.mean(seed_scores)), 4),
            "sd_test_f1": round(float(np.std(seed_scores, ddof=1)), 4),
            "min_test_f1": round(float(np.min(seed_scores)), 4),
            "max_test_f1": round(float(np.max(seed_scores)), 4),
            "best_baseline": name,
            "best_baseline_test_f1": round(value, 4),
            "delta_vs_baseline": round(float(np.mean(seed_scores)) - value, 4),
            "seeds_beating_baseline": int(sum(1 for v in seed_scores if v > value)),
            "t_statistic": round(float(t), 3),
            "p_value": round(float(p), 4),
            "significant_at_0.05": bool(p < 0.05),
        })
    return out
