"""The FASTENER paper's published Table 3, and the comparison against it.

Transcribed from Koprivec, Kenda & Sircelj, Entropy 2020, 22(11), 1198,
Table 3 ("Mean, max, median value, standard deviation AUF and number of model
evaluations"), which compares FS-SDS against FASTENER on the 25 scikit-feature
benchmarks. Table 4 compares DT-forward against FASTENER; its FASTENER column
is identical to Table 3's and is not duplicated here.

These are the paper's numbers, not ours. `compare` puts a replication run
beside them and reports where it lands -- including, and especially, where it
does not.

The paper's headline claim about this table is that FASTENER beats FS-SDS
everywhere except lung_discrete: 24 of 25. `compare` checks that claim
directly, because reproducing an ORDERING is a stronger and more meaningful
result than landing on the same absolute AUF, which depends on choices the
paper does not fully specify (see paper_protocol.py).
"""
from typing import Dict, List

import numpy as np

# dataset -> {method: (mean, max, median, sd, eval_n)}
PUBLISHED_TABLE_3: Dict[str, Dict[str, tuple]] = {
    "ALLAML":        {"fs_sds": (0.643, 0.717, 0.650, 0.039, 30000),
                      "fastener": (0.776, 0.894, 0.780, 0.062, 11238)},
    "arcene":        {"fs_sds": (0.608, 0.673, 0.607, 0.037, 30000),
                      "fastener": (0.707, 0.785, 0.713, 0.034, 12083)},
    "BASEHOCK":      {"fs_sds": (0.580, 0.618, 0.580, 0.018, 30000),
                      "fastener": (0.742, 0.780, 0.744, 0.019, 13847)},
    "CLL_SUB_111":   {"fs_sds": (0.537, 0.671, 0.534, 0.053, 30000),
                      "fastener": (0.626, 0.790, 0.623, 0.067, 11911)},
    "COIL20":        {"fs_sds": (0.655, 0.673, 0.657, 0.010, 30000),
                      "fastener": (0.687, 0.714, 0.687, 0.012, 14214)},
    "colon":         {"fs_sds": (0.658, 0.770, 0.652, 0.069, 30000),
                      "fastener": (0.763, 0.900, 0.757, 0.076, 11256)},
    "gisette":       {"fs_sds": (0.672, 0.682, 0.671, 0.005, 30000),
                      "fastener": (0.786, 0.802, 0.786, 0.006, 13213)},
    "GLIOMA":        {"fs_sds": (0.549, 0.687, 0.561, 0.067, 30000),
                      "fastener": (0.618, 0.827, 0.617, 0.095, 11674)},
    "GLI_85":        {"fs_sds": (0.659, 0.746, 0.665, 0.063, 30000),
                      "fastener": (0.755, 0.894, 0.770, 0.065, 11238)},
    "Isolet":        {"fs_sds": (0.365, 0.392, 0.364, 0.012, 30000),
                      "fastener": (0.396, 0.432, 0.395, 0.012, 14572)},
    "leukemia":      {"fs_sds": (0.620, 0.770, 0.618, 0.060, 30000),
                      "fastener": (0.824, 0.900, 0.833, 0.057, 11248)},
    "lung":          {"fs_sds": (0.663, 0.750, 0.656, 0.031, 30000),
                      "fastener": (0.727, 0.828, 0.731, 0.038, 11802)},
    "lung_discrete": {"fs_sds": (0.533, 0.666, 0.532, 0.068, 30000),
                      "fastener": (0.511, 0.716, 0.516, 0.086, 11753)},
    "lymphoma":      {"fs_sds": (0.539, 0.619, 0.548, 0.058, 30000),
                      "fastener": (0.590, 0.757, 0.580, 0.070, 11719)},
    "nci9":          {"fs_sds": (0.331, 0.513, 0.311, 0.097, 30000),
                      "fastener": (0.405, 0.610, 0.406, 0.088, 12081)},
    "ORL":           {"fs_sds": (0.347, 0.395, 0.351, 0.029, 30000),
                      "fastener": (0.390, 0.488, 0.389, 0.040, 13540)},
    "orlraws10P":    {"fs_sds": (0.675, 0.770, 0.686, 0.053, 30000),
                      "fastener": (0.694, 0.821, 0.695, 0.062, 13571)},
    "PCMAC":         {"fs_sds": (0.596, 0.624, 0.594, 0.012, 30000),
                      "fastener": (0.710, 0.736, 0.708, 0.013, 15768)},
    "Prostate_GE":   {"fs_sds": (0.676, 0.734, 0.691, 0.041, 30000),
                      "fastener": (0.748, 0.837, 0.749, 0.050, 14002)},
    "RELATHE":       {"fs_sds": (0.520, 0.554, 0.519, 0.017, 30000),
                      "fastener": (0.667, 0.707, 0.667, 0.018, 15541)},
    "TOX_171":       {"fs_sds": (0.421, 0.509, 0.427, 0.046, 30000),
                      "fastener": (0.553, 0.647, 0.550, 0.039, 14759)},
    "USPS":          {"fs_sds": (0.561, 0.569, 0.561, 0.005, 30000),
                      "fastener": (0.583, 0.593, 0.583, 0.005, 16670)},
    "warpAR10P":     {"fs_sds": (0.502, 0.588, 0.525, 0.052, 30000),
                      "fastener": (0.523, 0.672, 0.518, 0.065, 13840)},
    "warpPIE10P":    {"fs_sds": (0.582, 0.646, 0.589, 0.037, 30000),
                      "fastener": (0.633, 0.741, 0.634, 0.041, 13630)},
    "Yale":          {"fs_sds": (0.380, 0.454, 0.376, 0.035, 30000),
                      "fastener": (0.436, 0.594, 0.438, 0.052, 15307)},
}

FIELDS = ("mean", "max", "median", "sd", "eval_n")


def published(dataset: str, method: str) -> Dict[str, float]:
    """The paper's row, as a dict, or {} if the paper has no such entry.

    Only FS-SDS and FASTENER appear in Table 3. POSS is absent by design -- the
    paper compares it on EOData only -- so a POSS row has nothing to be compared
    against and must never be presented as replicating anything.
    """
    # fs_sds_elm is the same method as the paper's FS-SDS, driven by the
    # classifier the paper actually used, so it is compared against the same
    # published row. The tree-driven fs_sds arm is the deliberate variant.
    method = "fs_sds" if method == "fs_sds_elm" else method
    entry = PUBLISHED_TABLE_3.get(dataset, {}).get(method)
    if entry is None:
        return {}
    return dict(zip(FIELDS, entry))


def compare(rows: List[Dict]) -> Dict:
    """Put replication rows beside the published table.

    `rows` are the records written by run_paper_replication (dataset, method,
    mean, max, median, sd, eval_n).

    Reports, per method, the signed difference in mean AUF, and separately the
    paper's own ordering claim: FASTENER above FS-SDS on 24 of 25 data sets.
    """
    by = {(r["dataset"], r["method"]): r for r in rows if r.get("mean") is not None}

    per_method: Dict[str, List[Dict]] = {}
    for (dataset, method), row in sorted(by.items()):
        pub = published(dataset, method)
        if not pub:
            continue
        per_method.setdefault(method, []).append({
            "dataset": dataset,
            "ours_mean": round(row["mean"], 3),
            "paper_mean": pub["mean"],
            "delta": round(row["mean"] - pub["mean"], 3),
            "ours_eval_n": row.get("eval_n"),
            "paper_eval_n": pub["eval_n"],
        })

    summary = {}
    for method, entries in per_method.items():
        deltas = np.array([e["delta"] for e in entries], dtype=float)
        ours = np.array([e["ours_mean"] for e in entries], dtype=float)
        paper = np.array([e["paper_mean"] for e in entries], dtype=float)
        summary[method] = {
            "n_datasets": len(entries),
            "mean_delta": round(float(deltas.mean()), 4),
            "mean_abs_delta": round(float(np.abs(deltas).mean()), 4),
            "ours_above_paper": int((deltas > 0).sum()),
            # Whether the replication ranks the data sets the way the paper
            # does, which survives protocol differences that shift every value.
            "rank_correlation": (
                round(float(np.corrcoef(
                    np.argsort(np.argsort(ours)),
                    np.argsort(np.argsort(paper)))[0, 1]), 3)
                if len(entries) > 2 else None),
        }

    # The paper's headline ordering claim, checked directly.
    ordering = []
    for dataset in sorted({d for d, _ in by}):
        ours_f = by.get((dataset, "fastener"))
        ours_s = by.get((dataset, "fs_sds_elm")) or by.get((dataset, "fs_sds"))
        pub_f, pub_s = published(dataset, "fastener"), published(dataset, "fs_sds")
        if not (ours_f and ours_s and pub_f and pub_s):
            continue
        ordering.append({
            "dataset": dataset,
            "paper_fastener_wins": pub_f["mean"] > pub_s["mean"],
            "ours_fastener_wins": ours_f["mean"] > ours_s["mean"],
            "agrees": (pub_f["mean"] > pub_s["mean"]) ==
                      (ours_f["mean"] > ours_s["mean"]),
        })

    return {
        "per_method": per_method,
        "summary": summary,
        "ordering": ordering,
        "ordering_agreement": (
            f"{sum(o['agrees'] for o in ordering)}/{len(ordering)}"
            if ordering else "n/a"),
        "paper_claim": "FASTENER beats FS-SDS on 24 of 25 (all but lung_discrete)",
    }


def print_comparison(cmp: Dict) -> None:
    for method, entries in sorted(cmp["per_method"].items()):
        s = cmp["summary"][method]
        print(f"\n{method} vs the paper's Table 3 "
              f"({s['n_datasets']} data sets)")
        print(f"  {'Data Set':<16}{'ours':>8}{'paper':>8}{'delta':>8}"
              f"{'ours_n':>10}{'paper_n':>10}")
        print("  " + "-" * 60)
        for e in entries:
            print(f"  {e['dataset']:<16}{e['ours_mean']:>8.3f}"
                  f"{e['paper_mean']:>8.3f}{e['delta']:>+8.3f}"
                  f"{(e['ours_eval_n'] or 0):>10,}{e['paper_eval_n']:>10,}")
        print(f"  mean delta {s['mean_delta']:+.4f}   "
              f"mean |delta| {s['mean_abs_delta']:.4f}   "
              f"above paper on {s['ours_above_paper']}/{s['n_datasets']}   "
              f"rank corr {s['rank_correlation']}")

    if cmp["ordering"]:
        print(f"\nThe paper's ordering claim: {cmp['paper_claim']}")
        print(f"  reproduced on {cmp['ordering_agreement']} data sets")
        disagree = [o["dataset"] for o in cmp["ordering"] if not o["agrees"]]
        if disagree:
            print(f"  disagrees on: {', '.join(disagree)}")
