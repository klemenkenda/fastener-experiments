"""Set H4's per-dataset CPU-time budget from a calibration run of FASTENER.

H4 compares FASTENER and FS-SDS at equal compute: both searches stop when
they have used the same process CPU time on a dataset (HYPOTHESES.md, H4,
revised 2026-10-10; DEC-36). The time is what stock FASTENER needs to spend
the protocol's fit budget there -- 6,000 fits, or 12,000 on the datasets of
`protocol.LONG_BUDGET_DATASETS` -- measured once per dataset at seed 1999 (not
one of the five experiment seeds):

    python experiments/run_queue.py --name h4-calibration \\
        --datasets <the 25 paper benchmarks> --methods fastener:none \\
        --seeds 1999 --max-procs 10

    python experiments/cpu_budget.py --queue results/h4-calibration

The budget is the calibration run's search CPU seconds, rounded up to the
next ROUND_TO seconds. It writes budgets.csv and budgets.json, with
"unit": "cpu_seconds", into the queue folder; `run_queue.py --budgets` reads
the JSON. Only CPU time and fits are read; no score is.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import RESULTS_DIR  # noqa: E402

CALIBRATION_SEED = 1999
ROUND_TO = 10
METHOD = "fastener"


def budget_from(cpu_seconds: float, round_to: int = ROUND_TO) -> int:
    """CPU seconds rounded up to the next multiple of `round_to`."""
    return int(math.ceil(cpu_seconds / round_to) * round_to)


def read_runs(run_dirs: Sequence[Path]) -> List[Dict]:
    rows = []
    for d in run_dirs:
        mpath, raw = d / "manifest.json", d / "raw_results.json"
        if not (mpath.is_file() and raw.is_file()):
            continue
        ds = json.loads(mpath.read_text(encoding="utf-8"))["params"]["dataset"]
        for res in json.loads(raw.read_text(encoding="utf-8")):
            if res["method"] != METHOD or res.get("seed") != CALIBRATION_SEED:
                continue
            cpu = res.get("search_cpu_seconds")
            rows.append({
                "dataset": ds, "fits": res["model_fits"],
                "stopped_on": res.get("stopped_on"),
                "cpu_seconds": cpu,
                "wall_seconds": res.get("search_seconds"),
                "cpu_budget": budget_from(cpu) if cpu is not None else None,
                "run": d.name})
    return sorted(rows, key=lambda r: r["dataset"].lower())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", type=Path, required=True,
                    help="a run_queue.py folder, e.g. results/h4-calibration")
    args = ap.parse_args()
    queue = args.queue if args.queue.is_absolute() else \
        RESULTS_DIR.parent / args.queue
    q = json.loads((queue / "queue.json").read_text(encoding="utf-8"))
    run_dirs = [Path(j["run_dir"]) for j in q["jobs"] if j.get("run_dir")]
    rows = read_runs(run_dirs)

    print(f"{'dataset':<14}{'fits':>7}{'stopped on':>12}{'CPU s':>9}"
          f"{'wall s':>9}{'budget':>8}")
    for r in rows:
        print(f"{r['dataset']:<14}{r['fits']:>7}{str(r['stopped_on']):>12}"
              f"{r['cpu_seconds'] or 0:>9.1f}{r['wall_seconds'] or 0:>9.1f}"
              f"{r['cpu_budget'] or 0:>8}")
    bad = [r["dataset"] for r in rows
           if r["cpu_budget"] is None or r["stopped_on"] != "fit_budget"]
    with open(queue / "budgets.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["dataset"])
        w.writeheader()
        w.writerows(rows)
    (queue / "budgets.json").write_text(json.dumps({
        "unit": "cpu_seconds",
        "rule": "HYPOTHESES.md, H4, budget (DEC-36): stock FASTENER's search "
                "CPU time for the protocol fit budget, seed 1999, rounded up "
                f"to {ROUND_TO} s",
        "runs": [r["run"] for r in rows],
        "budgets": {r["dataset"]: r["cpu_budget"] for r in rows
                    if r["dataset"] not in bad}}, indent=2), encoding="utf-8")
    print(f"\nwrote {queue / 'budgets.csv'} and budgets.json")
    if bad:
        print(f"no budget (run missing, unfinished or not stopped on its fit "
              f"budget): {', '.join(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
