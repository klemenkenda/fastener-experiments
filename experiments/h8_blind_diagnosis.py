"""H8-E02: why the blind prior is about as fast as the named one.

Two diagnostics behind REPORT.md section 4 of H8-E02, from the committed
priors and the training split only (no run is read):

* the guidance weights each arm actually used, w = MI^0.5 x prior^0.5
  (`fastener.guidance.combine`, lambda 0.5), for the named prior, the blind
  prior and a flat prior (mutual information alone): their Spearman
  correlations and the overlap of their top tenth (at least 3 features);
* the blind prior's top positions, read as the dataset's original columns:
  what a model scores highly when it recalls the column order.

    python experiments/h8_blind_diagnosis.py        # -> reports/H8-E02/tables/
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

import _bootstrap  # noqa: F401
import fast_mi
import llm_guidance as lg
import protocol
import run_sota
from datasets import load
from fastener import guidance

OUT = Path(__file__).resolve().parent / "reports" / "H8-E02" / "tables"
MODELS = ("opus", "sonnet", "haiku")
DATASETS = ("adult", "covertype", "crop_mapping", "diabetes130", "eodata", "eye_movements",
            "gas_drift", "har", "heloc", "higgs", "mice_protein", "ozone_8hr", "pc4",
            "phishing", "qsar_biodeg", "spambase")


def _top(v: np.ndarray, k: int) -> set:
    return set(np.argsort(-v, kind="stable")[:k].tolist())


def _sqrt_range(v: np.ndarray) -> float:
    """max / median of a factor as it enters w (scaled, floored, ^0.5)."""
    s = np.sqrt(guidance._unit(v))
    return float(s.max() / np.median(s))


def main() -> int:
    ids = run_sota.H8_MODELS
    weights, tops = [], []
    for d in DATASETS:
        ds = load(d, max_rows=protocol.ROW_CAP)
        mi = fast_mi.mutual_info_classif(ds.X_train, ds.y_train, random_state=0)
        n, k = len(mi), max(3, len(mi) // 10)
        w_mi = guidance.combine(mi, np.ones(n), 0.5)
        for m in MODELS:
            named = lg.load_prior(lg.prior_path(d, ids[m], False))
            pb = lg.prior_path(d, ids[m], True, True)
            blind = lg.load_prior(pb)
            wn, wb = guidance.combine(mi, named, 0.5), guidance.combine(mi, blind, 0.5)
            weights.append({
                "dataset": d, "model": m, "n_features": n, "top_k": k,
                "mi_sqrt_range": _sqrt_range(mi), "named_sqrt_range": _sqrt_range(named),
                "rho_w_named_blind": float(spearmanr(wn, wb)[0]),
                "rho_w_named_mi": float(spearmanr(wn, w_mi)[0]),
                "rho_w_blind_mi": float(spearmanr(wb, w_mi)[0]),
                "top_named_blind": len(_top(wn, k) & _top(wb, k)) / k,
                "top_named_mi": len(_top(wn, k) & _top(w_mi, k)) / k,
                "top_blind_mi": len(_top(wb, k) & _top(w_mi, k)) / k})
            doc = json.loads(pb.read_text(encoding="utf-8"))
            names = json.loads(lg.prior_path(d, ids[m], False).read_text(
                encoding="utf-8"))["feature_names"]
            by_pos = np.asarray(doc["scores"])[np.asarray(doc["permutation"])]
            for rank, p in enumerate(np.argsort(-by_pos, kind="stable")[:6], 1):
                tops.append({"dataset": d, "model": m, "rank": rank, "position": int(p),
                             "score": float(by_pos[p]), "original_column_name": names[p],
                             "named_prior_score_of_that_column": float(named[p])})
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in (("weight_agreement.csv", weights), ("blind_top_positions.csv", tops)):
        with open(OUT / name, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    for key in ("mi_sqrt_range", "named_sqrt_range", "rho_w_named_blind", "rho_w_named_mi",
                "rho_w_blind_mi", "top_named_blind", "top_named_mi", "top_blind_mi"):
        v = np.array([r[key] for r in weights], dtype=float)
        print(f"{key:18s} median {np.nanmedian(v):5.2f}  p10 {np.nanpercentile(v, 10):5.2f}"
              f"  p90 {np.nanpercentile(v, 90):5.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
