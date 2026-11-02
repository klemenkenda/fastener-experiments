"""H13's measures: reach, matched-size quality and their share of AUF.

Pure functions over one run's final front (the distilled `records`) and
archive trajectory (the distilled `curves`), and over the per-dataset
aggregates built from them. `h13_report.py` loads the runs, applies the tests
and draws the figures; everything that defines a number H13-E01 reports is
here, so the tests in `tests/test_h13_coverage.py` pin it.

Definitions, as registered (EXPERIMENTS.md, H13-E01):

* reach(k): the final front holds a subset of at most k features;
* c(k): the run's `make_report.opt_curve` value at k, defined only where
  reach(k) holds;
* per dataset and arm: r(k), the share of finished seeds with reach(k), and
  c_bar(k), the mean of c(k) over those seeds; R = r(K). The seed-mean AUF is
  (1/K) sum_k r(k) c_bar(k);
* matched-size difference: the mean of c_bar_a(k) - c_bar_b(k) over the k
  both arms reach in at least MATCH_SHARE of their seeds;
* decomposition: r_a c_a - r_b c_b = (r_a - r_b)(c_a + c_b)/2
  + (r_a + r_b)(c_a - c_b)/2, the first term reach, the second quality; an
  arm with r(k) = 0 takes the other arm's c_bar(k), so that k is all reach.

The front a run returns (`records`, the last population's first rank) is not
its archive (`curves`: the best subset at each size among all subsets scored).
The archive's smallest size never grows; the final front can lose a small
subset the archive still holds ("lost reach").
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from scipy.stats import binom

from make_report import auf, opt_curve

K = 10
MATCH_SHARE = 0.6          # 3 of 5 seeds
POPULATION = 100           # every NSGA-II arm in H1-E02 and H5H6-E01 to -E03
OBL_PAIRS = POPULATION // 2
N_BOOT, BOOT_SEED = 10_000, 20200


# ------------------------------------------------------------------ one run
def min_front_size(records: Sequence[Dict]) -> Optional[int]:
    return min((int(r["n_features"]) for r in records), default=None)


def reach_curve(records: Sequence[Dict], K: int = K) -> np.ndarray:
    """reach(k), k = 1..K, for one run's final front."""
    m = min_front_size(records)
    ks = np.arange(1, K + 1)
    return np.zeros(K, dtype=bool) if m is None else ks >= m


def exact_curve(records: Sequence[Dict], K: int = K) -> np.ndarray:
    """Test F1 of the validation-best subset of exactly k features, k = 1..K;
    NaN where the front has none of that size (the check of matched size)."""
    out = np.full(K, np.nan)
    best = np.full(K, -np.inf)
    for r in records:
        s = int(r["n_features"])
        if 1 <= s <= K and r["val_score"] > best[s - 1]:
            best[s - 1], out[s - 1] = r["val_score"], r["test_score"]
    return out


def best_unrestricted(records: Sequence[Dict]) -> Optional[float]:
    """Test F1 of the front's validation-best subset, at any size."""
    if not records:
        return None
    return float(max(records, key=lambda r: r["val_score"])["test_score"])


def run_measures(records: Sequence[Dict], n_features: int) -> Dict:
    """Everything H13 reads from one run's final front."""
    sizes = [int(r["n_features"]) for r in records]
    return {"reach": reach_curve(records), "c": opt_curve(records, K),
            "exact": exact_curve(records),
            "auf_k10": auf(records, K), "auf_k20": auf(records, 20),
            "auf_kd": auf(records, n_features),
            "best_f1": best_unrestricted(records),
            "min_front": min(sizes, default=None),
            "max_front": max(sizes, default=None)}


def time_to_reach(curve: Sequence[Dict], budget: int, K: int = K) -> Dict:
    """When the archive first held a subset of at most K features.

    `curve` is one run's snapshots in order (fits, seconds, min_size). A run
    whose archive never reaches is censored at its last snapshot: it is never
    assigned the budget. Times are also given as a share of the budget.
    """
    snaps = sorted(curve, key=lambda s: s["fits"])
    if not snaps:
        return {"reached": False, "fits": None, "seconds": None, "share": None,
                "at_start": False, "archive_min": None}
    hit = next((s for s in snaps if s["min_size"] is not None
                and not np.isnan(s["min_size"]) and s["min_size"] <= K), None)
    last = snaps[-1]
    s = hit or last
    return {"reached": hit is not None, "fits": int(s["fits"]),
            "seconds": float(s["seconds"]), "share": s["fits"] / budget,
            "at_start": hit is not None and hit is snaps[0],
            "archive_min": last["min_size"]}


# ---------------------------------------------------------- one dataset-arm
def aggregate(runs: Sequence[Dict], K: int = K) -> Dict:
    """Per dataset and arm, over its finished seeds: r(k), c_bar(k), R, the
    exact-size curve and its share, and the means of the scalar measures."""
    reach = np.array([r["reach"] for r in runs], dtype=float)
    c = np.array([r["c"] for r in runs], dtype=float)
    exact = np.array([r["exact"] for r in runs], dtype=float)
    r_k = reach.mean(axis=0)
    with np.errstate(invalid="ignore"):
        c_bar = np.where(r_k > 0, (c * reach).sum(axis=0)
                         / np.maximum(reach.sum(axis=0), 1), np.nan)
    have = ~np.isnan(exact)
    exact_share = have.mean(axis=0)
    exact_bar = np.array([exact[have[:, k], k].mean() if have[:, k].any() else np.nan
                          for k in range(K)])
    scal = {m: float(np.mean([r[m] for r in runs if r[m] is not None]))
            if any(r[m] is not None for r in runs) else float("nan")
            for m in ("auf_k10", "auf_k20", "auf_kd", "best_f1", "max_front")}
    return {"n_seeds": len(runs), "r": r_k, "c_bar": c_bar, "R": float(r_k[K - 1]),
            "exact_share": exact_share, "exact_bar": exact_bar, **scal}


def decompose(ra, ca, rb, cb) -> Tuple[float, float]:
    """(reach term, quality term) of the seed-mean AUF difference a - b.

    Exact: the two terms sum to mean_k(r_a c_a - r_b c_b). Where an arm has
    r(k) = 0 its c_bar(k) is undefined and takes the other arm's, so that k
    contributes only to the reach term. A k neither arm reaches contributes
    nothing.
    """
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    ca, cb = np.array(ca, float), np.array(cb, float)
    ca = np.where(ra > 0, ca, cb)
    cb = np.where(rb > 0, cb, ca)
    ca, cb = np.nan_to_num(ca), np.nan_to_num(cb)
    reach = (ra - rb) * (ca + cb) / 2
    quality = (ra + rb) * (ca - cb) / 2
    return float(reach.mean()), float(quality.mean())


def matched_difference(ra, ca, rb, cb, share: float = MATCH_SHARE) -> Optional[float]:
    """Mean c_bar_a(k) - c_bar_b(k) over the k both arms reach in at least
    `share` of their seeds; None if there is no such k."""
    ra, rb = np.asarray(ra, float), np.asarray(rb, float)
    M = (ra >= share - 1e-12) & (rb >= share - 1e-12)
    if not M.any():
        return None
    return float(np.mean(np.asarray(ca, float)[M] - np.asarray(cb, float)[M]))


def reach_share(terms: Sequence[Tuple[float, float]]) -> float:
    """Sum |reach| / (sum |reach| + sum |quality|) over datasets."""
    a = sum(abs(r) for r, _ in terms)
    b = sum(abs(q) for _, q in terms)
    return a / (a + b) if a + b > 0 else float("nan")


# ------------------------------------------------------------------ analytic
def obl_start_reach(d: int, K: int = K, pairs: int = OBL_PAIRS) -> float:
    """P(an OBL start of `pairs` complementary pairs holds a non-empty subset
    of at most K features).

    `obl_initialization` draws each bit with probability 1/2 and adds the
    complement, so a pair has sizes k and d - k with k ~ Binomial(d, 1/2).
    """
    k = np.arange(d + 1)
    hit = ((k >= 1) & (k <= K)) | ((d - k >= 1) & (d - k <= K))
    p_pair = float(binom.pmf(k, d, 0.5)[hit].sum())
    return 1.0 - (1.0 - p_pair) ** pairs


# --------------------------------------------------------------- statistics
def rank_biserial(deltas: Sequence[float]) -> float:
    """Matched-pairs rank-biserial correlation (W+ - W-)/(W+ + W-), zeros
    dropped as in `make_report.wilcoxon_p`."""
    from scipy.stats import rankdata
    d = np.array([x for x in deltas if x != 0], dtype=float)
    if not len(d):
        return 0.0
    ranks = rankdata(np.abs(d))
    return float((ranks[d > 0].sum() - ranks[d < 0].sum()) / ranks.sum())


def bootstrap_ci(deltas: Sequence[float], stat=np.mean, n: int = N_BOOT,
                 seed: int = BOOT_SEED) -> Tuple[float, float]:
    """95% percentile interval, paired bootstrap over datasets."""
    d = np.asarray(deltas, dtype=float)
    if not len(d):
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    s = stat(d[rng.integers(0, len(d), size=(n, len(d)))], axis=1)
    return float(np.quantile(s, 0.025)), float(np.quantile(s, 0.975))


def km(times: Sequence[float], events: Sequence[bool]) -> Tuple[np.ndarray, np.ndarray]:
    """Kaplan-Meier: (event times, P(not yet reached) just after each)."""
    t = np.asarray(times, float)
    e = np.asarray(events, bool)
    ts = np.unique(t[e])
    surv, s = [], 1.0
    for x in ts:
        at_risk = (t >= x).sum()
        s *= 1 - ((t == x) & e).sum() / at_risk
        surv.append(s)
    return ts, np.array(surv)


def km_reached_by(times, events, horizon: float) -> float:
    """KM estimate of the share reached by `horizon`."""
    ts, s = km(times, events)
    before = s[ts <= horizon]
    return float(1 - before[-1]) if len(before) else 0.0


def rmst(times, events, horizon: float = 1.0) -> float:
    """Restricted mean time to reach, the area under the KM curve on
    [0, horizon]: censored runs are handled by KM, never set to the horizon."""
    ts, s = km(times, events)
    grid = np.concatenate([[0.0], ts[ts < horizon], [horizon]])
    vals = np.concatenate([[1.0], s[ts < horizon]])
    return float(np.sum(np.diff(grid) * vals))


def expected_flips(k: float, d: int) -> float:
    """Expected bits flipped per child by `balanced_mutation` at rate 1/d,
    0 < k < d (P2's EVIDENCE.md): 2k/d."""
    return 2.0 * k / d
