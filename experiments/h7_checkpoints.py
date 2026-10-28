"""H7: what the searches of the H5/H6 grids offered part-way through the budget.

For every finished run of the chosen arms in a grid (its report's
tables/run_keys.csv), read the run's trajectory: the front is stored at
every snapshot where it changed, against cumulative fits. At each checkpoint
-- a fraction of the run's fit budget -- take the last stored front at or
below that many fits (a run that stopped earlier, on stagnation, contributes
its final front), refit every entry of at most K features with the grid's
classifier on the training split, score it on validation and once on test
(protocol.evaluate_subset, as every final number is made), and compute AUF
(K = 10) exactly as the reports do (make_report.opt_curve).

One provenance run per grid and dataset, so each is a traceable record:

    python experiments/h7_checkpoints.py --experiment H7-E01 --jobs 12

At checkpoint 1.0 the result must equal the grid's own end-of-budget AUF; a
dry run checks that without an experiment ID (and without reading any
intermediate checkpoint):

    python experiments/h7_checkpoints.py --checkpoints 1.0 --root <scratch>
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import _bootstrap  # noqa: F401  (puts the FASTENER clone on the path)
import experiment_ids
import protocol
import provenance
from datasets import load
from make_report import opt_curve

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
RESULTS = provenance.RESULTS_DIR

# The grids and the classifier each ran with (DEC-40, DEC-41, DEC-44).
SOURCES = {"H5H6-E01": "tree", "H5H6-E02": "rf", "H5H6-E03": "lgbm"}
# H7's three arms, and the two swap arms reported beside them. FS-SDS is
# left out: it runs k = 1..20 one after another, so a share of its total fits
# has seen only the first k's and is not comparable.
METHODS = ("fastener", "nsga2_sparse", "poss",
           "fastener_swap_guided", "fastener_swap_random")
CHECKPOINTS = (0.10, 0.25, 0.50, 1.00)
K = 10


def source_runs(source: str) -> List[Dict]:
    """The grid's finished runs of METHODS, as its report lists them."""
    path = REPORTS / source / "tables" / "run_keys.csv"
    with open(path, encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["method"] in METHODS]


def fronts_at(traj: Path, limits: Dict[float, int]) -> Dict[float, Tuple[int, List[Dict]]]:
    """For each checkpoint, (fits at the snapshot used, its front)."""
    out: Dict[float, Tuple[int, List[Dict]]] = {}
    last: Optional[Tuple[int, List[Dict]]] = None
    pending = sorted(limits.items(), key=lambda kv: kv[1])
    with open(traj, encoding="utf-8") as fh:
        for line in fh:
            snap = json.loads(line)
            while pending and snap["fits"] > pending[0][1]:
                c, _ = pending.pop(0)
                out[c] = last if last else (0, [])
            if "front" in snap:
                last = (int(snap["fits"]), snap["front"])
    for c, _ in pending:            # the run ended before these checkpoints
        out[c] = last if last else (0, [])
    return out


def work(source: str, dataset: str, runs: Sequence[Dict],
         checkpoints: Sequence[float], experiment_id: Optional[str],
         root: Optional[str], allow_dirty: bool) -> Dict:
    """One grid and dataset: every run's AUF at every checkpoint."""
    if experiment_id:
        os.environ[provenance.DEFER_LEDGER_ENV] = "1"
    model = SOURCES[source]
    protocol.set_model(model, 1)
    # The protocol's row cap, as run_sota.py loads every dataset: without it
    # EOData (480,000 rows) would be split differently from the grids.
    ds = load(dataset, max_rows=protocol.ROW_CAP)
    protocol.set_train_rows(ds.X_train.shape[0])
    # The split must be the one the runs searched on.
    for r in runs:
        m = json.loads((RESULTS / r["run_id"] / "manifest.json").read_text(encoding="utf-8"))
        if {k: m["dataset"][k] for k in ("n_train", "n_val", "n_test")} !=                 {"n_train": ds.X_train.shape[0], "n_val": ds.X_val.shape[0],
                 "n_test": ds.X_test.shape[0]}:
            raise RuntimeError(f"{dataset}: split differs from {r['run_id']}")
    tag = source.lower().replace("-", "")
    params = {"source": source, "model": model, "dataset": dataset,
              "methods": list(METHODS), "checkpoints": list(checkpoints),
              "K": K, "runs": len(runs)}
    run = provenance.Run(f"h7e01_{tag}_{dataset}", params,
                         root=Path(root) if root else None,
                         experiment_id=experiment_id, allow_dirty=allow_dirty)
    rows, cache = [], {}
    with run:
        run.record("dataset", ds.summary())
        for r in runs:
            src = RESULTS / r["run_id"]
            manifest = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
            budget = int(manifest["params"]["evaluation_budget_per_seed"])
            traj, = sorted((src / "trajectories").glob("*.jsonl"))
            limits = {c: int(c * budget) for c in checkpoints}
            for c, (fits, front) in sorted(fronts_at(traj, limits).items()):
                records = []
                for e in front:
                    feats = tuple(sorted(int(f) for f in e["features"]))
                    if not feats or len(feats) > K:
                        continue
                    if feats not in cache:
                        cache[feats] = protocol.evaluate_subset(ds, feats)
                    records.append(cache[feats])
                curve = opt_curve(records, K)
                rows.append({"source": source, "model": model,
                             "dataset": dataset, "method": r["method"],
                             "seed": int(r["seed"]), "source_run": r["run_id"],
                             "budget": budget, "checkpoint": c,
                             "fit_limit": limits[c], "snapshot_fits": fits,
                             "front_entries_le_k": len(records),
                             "auf_k10": float(curve.mean()),
                             "auf_k10_grid": float(r["auf_k10"])})
        run.record("refits", len(cache))
        run.write_json("checkpoints.json", rows)
    return {"run_id": run.run_id, "rows": rows}


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--experiment", help="experiment ID (evidence); omit for a dry run")
    ap.add_argument("--sources", default=",".join(SOURCES))
    ap.add_argument("--checkpoints", default=",".join(str(c) for c in CHECKPOINTS))
    ap.add_argument("--datasets", default="", help="comma list; default all")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--root", help="where run folders go (default results/)")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args(argv)
    checkpoints = [float(c) for c in args.checkpoints.split(",")]
    only = set(filter(None, args.datasets.split(",")))

    tasks = []
    for source in args.sources.split(","):
        by_ds: Dict[str, List[Dict]] = {}
        for r in source_runs(source):
            if not only or r["dataset"] in only:
                by_ds.setdefault(r["dataset"], []).append(r)
        tasks += [(source, d, rs) for d, rs in sorted(by_ds.items())]
    # The costliest first: tasks with most rows run in parallel early.
    print(f"{len(tasks)} grid-dataset tasks, checkpoints {checkpoints}")

    rows, run_ids = [], []
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futs = {pool.submit(work, s, d, rs, checkpoints, args.experiment,
                            args.root, args.allow_dirty): (s, d)
                for s, d, rs in tasks}
        for i, f in enumerate(as_completed(futs), 1):
            res = f.result()
            rows += res["rows"]
            run_ids.append(res["run_id"])
            print(f"[{i}/{len(tasks)}] {futs[f][0]} {futs[f][1]}: "
                  f"{len(res['rows'])} rows", flush=True)

    if args.experiment:
        for rid in sorted(run_ids):
            experiment_ids.add_run(args.experiment, rid)
    out_dir = Path(args.root) if args.root else RESULTS / (args.experiment or "H7-dry")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "checkpoints.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["source"], r["dataset"],
                                                r["method"], r["seed"],
                                                r["checkpoint"])))
    full = [r for r in rows if r["checkpoint"] == 1.0]
    if full:
        bad = [r for r in full if abs(r["auf_k10"] - r["auf_k10_grid"]) > 1e-9]
        print(f"check at 1.0: {len(full) - len(bad)} of {len(full)} runs match "
              f"the grid's end-of-budget AUF")
        for r in bad[:20]:
            print(f"  {r['source']} {r['dataset']} {r['method']} s{r['seed']}: "
                  f"{r['auf_k10']:.6f} vs {r['auf_k10_grid']:.6f}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
