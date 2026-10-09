"""Set H2 and H3's fit budget per dataset from the calibration runs.

The rule is HYPOTHESES.md, H2, *Fit budget*, fixed before any calibration run
(DEC-33). On every dataset, with seed 1999 and validation scores only:

1. Boruta, one run: its validation AUF (K = 10) is the accuracy reference.
2. Stock FASTENER, one run capped at 12,000 fits, its validation AUF (K = 10)
   read from the trajectory after every generation.
3. The budget is the smallest b in BUDGET_GRID below 12,000 at which the
   FASTENER run's validation AUF is (i) within TOLERANCE of its value at the
   end of the run and (ii) no lower than Boruta's minus TOLERANCE -- then one
   step up the grid. Where no b below 12,000 meets both, the budget is 12,000
   and the dataset is flagged as possibly unconverged.

Validation AUF is h0_convergence.val_auf: opt(k) is the best validation F1
among subsets of size <= k, and 0 where there is none. Test scores are not
read.

Run the calibration with run_queue.py, one job per dataset and method:

    python experiments/run_queue.py --name h2h3-calibration \\
        --datasets <the H2/H3 datasets> --methods fastener:none,boruta \\
        --seeds 1999 --max-procs 10 -- --evaluations 12000

then read it:

    python experiments/calibrate_budget.py --queue results/h2h3-calibration

which prints the table and writes budgets.csv and budgets.json into the queue
folder. The budgets go into H2H3-E01's design in EXPERIMENTS.md before any of
its runs starts.
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import h0_convergence  # noqa: E402
import trajectory as trajectory_io  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402

BUDGET_GRID = (1_000, 2_000, 4_000, 6_000, 12_000)
TOLERANCE = 0.005
K = 10
CALIBRATION_SEED = 1999
FASTENER = "fastener"
BORUTA = "boruta"

Curve = List[Tuple[int, float]]


def value_at(curve: Curve, fits: int) -> float:
    """Validation AUF at the last snapshot taken at or before `fits` fits."""
    value = 0.0
    for f, v in curve:
        if f > fits:
            break
        value = v
    return value


def records_val_auf(records: Sequence[Dict], K: int = K) -> float:
    """Validation AUF (K) of a method's final records -- for Boruta."""
    front = [{"size": int(r["n_features"]), "val_f1": float(r["val_score"])}
             for r in records]
    return h0_convergence.val_auf(front, K)


def choose_budget(curve: Curve, reference: float,
                  grid: Sequence[int] = BUDGET_GRID,
                  tolerance: float = TOLERANCE) -> Dict:
    """Apply the rule to one dataset's calibration curve.

    `reference` is Boruta's validation AUF. Returns the budget, the first grid
    value that met both conditions (None if none below the top did), and the
    curve read at every grid value.
    """
    final = curve[-1][1] if curve else 0.0
    at = {b: value_at(curve, b) for b in grid}
    settled = None
    for b in grid[:-1]:
        if final - at[b] <= tolerance and at[b] >= reference - tolerance:
            settled = b
            break
    if settled is None:
        budget = grid[-1]
    else:
        budget = grid[min(grid.index(settled) + 1, len(grid) - 1)]
    return {"budget": budget, "settled_at": settled,
            "flag": "possibly unconverged" if settled is None else "",
            "final": final, "at": at}


def read_run(run_dir: Path) -> Tuple[Optional[str], Dict]:
    """(dataset, what this run contributes): a FASTENER curve, Boruta's AUF."""
    mpath = run_dir / "manifest.json"
    if not mpath.is_file():
        return None, {}
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    dataset = manifest["params"]["dataset"]
    out: Dict = {}
    traj = run_dir / "trajectories" / f"{FASTENER}_seed{CALIBRATION_SEED}.jsonl"
    if traj.is_file():
        snaps = trajectory_io.read(traj)
        if snaps:
            out["curve"] = h0_convergence.curve(snaps, K)
            out["fits_used"] = int(snaps[-1]["fits"])
    raw = run_dir / "raw_results.json"
    if raw.is_file():
        for res in json.loads(raw.read_text(encoding="utf-8")):
            if res.get("seed") != CALIBRATION_SEED:
                continue
            if res["method"] == BORUTA and res.get("records"):
                out["boruta"] = records_val_auf(res["records"])
            elif res["method"] == FASTENER:
                out["stopped_on"] = res.get("stopped_on")
    return dataset, out


def queue_run_dirs(queue_dir: Path) -> List[Path]:
    """The run folders of a run_queue.py queue, finished jobs only."""
    q = json.loads((queue_dir / "queue.json").read_text(encoding="utf-8"))
    return [Path(j["run_dir"]) for j in q["jobs"]
            if j.get("run_dir") and j.get("exit_code") == 0]


def calibrate(run_dirs: Sequence[Path]) -> List[Dict]:
    found: Dict[str, Dict] = {}
    for d in run_dirs:
        ds, part = read_run(d)
        if ds is not None:
            found.setdefault(ds, {}).update(part)
    rows = []
    for ds in sorted(found, key=str.lower):
        got = found[ds]
        row = {"dataset": ds, "boruta_val_auf": got.get("boruta"),
               "fits_used": got.get("fits_used"),
               "stopped_on": got.get("stopped_on")}
        missing = [w for w, k in (("FASTENER run", "curve"),
                                  ("Boruta run", "boruta")) if k not in got]
        if missing:
            row.update({"budget": None,
                        "flag": "missing " + " and ".join(missing)})
        else:
            c = choose_budget(got["curve"], got["boruta"])
            row.update({"budget": c["budget"], "settled_at": c["settled_at"],
                        "flag": c["flag"], "final_val_auf": c["final"],
                        **{f"val_auf_at_{b}": v for b, v in c["at"].items()}})
            if got.get("fits_used", 0) < BUDGET_GRID[-1]:
                row["flag"] = (row["flag"] + "; " if row["flag"] else "") + \
                    f"run ended at {got.get('fits_used')} fits " \
                    f"({got.get('stopped_on')})"
        rows.append(row)
    return rows


def _fmt(x, nd=4) -> str:
    return "--" if x is None else (f"{x:.{nd}f}" if isinstance(x, float)
                                   else str(x))


def print_table(rows: Sequence[Dict]) -> None:
    cols = ["dataset", "boruta_val_auf"] + \
        [f"val_auf_at_{b}" for b in BUDGET_GRID] + \
        ["settled_at", "budget", "flag"]
    head = ["dataset", "Boruta"] + [f"{b // 1000}k" for b in BUDGET_GRID] + \
        ["settled", "budget", "flag"]
    print("| " + " | ".join(head) + " |")
    print("|" + "|".join("---" for _ in head) + "|")
    for r in rows:
        print("| " + " | ".join(_fmt(r.get(c)) for c in cols) + " |")


def main() -> int:
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--queue", type=Path,
                     help="a run_queue.py folder, e.g. results/h2h3-calibration")
    src.add_argument("--runs", nargs="+", type=Path, help="run folders")
    ap.add_argument("--out", type=Path, default=None,
                    help="where to write budgets.csv/json; default: the "
                         "queue folder")
    args = ap.parse_args()

    if args.queue:
        queue = args.queue if args.queue.is_absolute() else \
            (RESULTS_DIR.parent / args.queue)
        run_dirs = queue_run_dirs(queue)
        out = args.out or queue
    else:
        run_dirs = args.runs
        if args.out is None:
            raise SystemExit("--out is required with --runs")
        out = args.out
    rows = calibrate(run_dirs)
    print_table(rows)

    out.mkdir(parents=True, exist_ok=True)
    fields = sorted({k for r in rows for k in r},
                    key=lambda k: (k != "dataset", k))
    with open(out / "budgets.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (out / "budgets.json").write_text(json.dumps(
        {"rule": "HYPOTHESES.md, H2, Fit budget (DEC-33)",
         "grid": list(BUDGET_GRID), "tolerance": TOLERANCE, "K": K,
         "seed": CALIBRATION_SEED,
         "runs": [Path(d).name for d in run_dirs],
         "budgets": {r["dataset"]: r["budget"] for r in rows}},
        indent=2), encoding="utf-8")
    print(f"\nwrote {out / 'budgets.csv'} and budgets.json")
    missing = [r["dataset"] for r in rows if r["budget"] is None]
    if missing:
        print(f"no budget for: {', '.join(missing)}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
