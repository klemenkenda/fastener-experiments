"""Report a replication run against the FASTENER paper's published tables.

Reads a run directory produced by run_paper_replication.py -- including one that
is still going, since every unit is written the moment it finishes -- and prints
the AUF tables plus the comparison against `paper_tables.PUBLISHED_TABLE_3`.

Usage:
    python experiments/report_replication.py                    # newest run
    python experiments/report_replication.py --run <run_id>
    python experiments/report_replication.py --run <run_id> --csv out.csv
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paper_protocol as pp  # noqa: E402
import paper_tables as pt  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402


def load_units(run_dir: Path) -> List[Dict]:
    """Every finished unit, from the per-unit files.

    Read from `partial/` rather than units.json so that a run still in flight
    reports exactly as much as it has actually finished.
    """
    partial = run_dir / "partial"
    units = []
    for path in sorted(partial.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                units.append(json.load(fh))
        except json.JSONDecodeError:
            # A file caught mid-write by a concurrent worker; it will be
            # complete on the next read.
            continue
    return [u for u in units if not u.get("failed")]


def build_rows(units: List[Dict]) -> List[Dict]:
    rows = []
    keys = sorted({(u["dataset"], u["method"]) for u in units})
    for dataset, method in keys:
        mine = [u for u in units
                if u["dataset"] == dataset and u["method"] == method]
        agg = pp.aggregate(mine)
        fits = [u["search_model_fits"] for u in mine
                if u.get("search_model_fits") is not None]
        rows.append({
            "dataset": dataset,
            "method": method,
            "mean": agg["mean"], "max": agg["max"],
            "median": agg["median"], "sd": agg["sd"],
            "n_auf_values": agg["n"],
            "eval_n": int(round(float(np.mean(fits)))) if fits else None,
            "n_splits": len(mine),
            "search_seconds_total": round(
                sum(u.get("search_seconds", 0) for u in mine), 1),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None,
                    help="run id or directory; default is the newest "
                         "paper_replication run")
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()

    if args.run:
        run_dir = Path(args.run)
        if not run_dir.is_dir():
            matches = sorted(RESULTS_DIR.glob(f"*{args.run}*"))
            if not matches:
                raise SystemExit(f"no run matching {args.run!r}")
            run_dir = matches[-1]
    else:
        matches = sorted(RESULTS_DIR.glob("*paper_replication"))
        if not matches:
            raise SystemExit("no paper_replication run found")
        run_dir = matches[-1]

    units = load_units(run_dir)
    if not units:
        raise SystemExit(f"{run_dir.name} has no finished units yet")
    rows = build_rows(units)

    done = {(u["dataset"], u["method"]) for u in units}
    print(f"run: {run_dir.name}")
    print(f"  {len(units)} finished units, "
          f"{len({d for d, _ in done})} data sets, "
          f"{len({m for _, m in done})} methods")
    splits = sorted({r["n_splits"] for r in rows})
    print(f"  splits per (data set, method): {splits[0]}-{splits[-1]}")

    methods = sorted({r["method"] for r in rows})
    from run_paper_replication import print_tables
    print_tables(rows, methods)

    cmp = pt.compare(rows)
    pt.print_comparison(cmp)

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
