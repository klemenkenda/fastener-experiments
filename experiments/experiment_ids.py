"""Experiment IDs, algorithm IDs and the experiment ledger (see METHODOLOGY.md).

* An **experiment ID** (`H1-E01`, `H2H3-E01`) names one attempt at one
  hypothesis. It is issued once, recorded in `EXPERIMENTS.md`, and never reused.
* An **algorithm ID** (`nsga2_sparse@a1b2c3d+9f8e7d6#4c1a`) pins one arm to the
  code of both repositories and to its resolved configuration.

Usage:
    python experiments/experiment_ids.py new H1          # issue H1-E<next>
    python experiments/experiment_ids.py new H2H3
    python experiments/experiment_ids.py status H1-E01 reported
    python experiments/experiment_ids.py list

Nothing here imports FASTENER, so it is safe to use from any script.
"""
import argparse
import contextlib
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "experiments" / "EXPERIMENTS.md"
REPORTS_DIR = REPO_ROOT / "experiments" / "reports"

EXPERIMENT_RE = re.compile(r"^((?:H\d+)+)-E(\d{2,})$")
HYPOTHESIS_RE = re.compile(r"^(?:H\d+)+$")

# `running` accepts further runs; every other status closes the experiment.
STATUSES = ("running", "failed", "invalid", "reported")
OPEN_STATUSES = ("running",)

LEDGER_COLUMNS = ("experiment", "hypothesis", "started", "run IDs", "status",
                  "report")
LEDGER_HEADER = """\
# Experiment ledger

Every experiment ID ever issued, one row each, appended when the experiment
starts -- not when it succeeds. Rows are never deleted. See
[`METHODOLOGY.md`](METHODOLOGY.md) for what the IDs and statuses mean.

Managed by `experiments/experiment_ids.py`; edit the status with
`python experiments/experiment_ids.py status <ID> <status>`.

"""


# ------------------------------------------------------------------ IDs
def parse_experiment_id(experiment_id: str) -> Dict[str, Any]:
    """Split `H2H3-E01` into its hypotheses (['H2', 'H3']) and attempt (1)."""
    m = EXPERIMENT_RE.match(experiment_id)
    if not m:
        raise ValueError(f"not an experiment ID: {experiment_id!r} "
                         f"(expected e.g. H1-E01 or H2H3-E01)")
    return {"hypotheses": re.findall(r"H\d+", m.group(1)),
            "group": m.group(1), "attempt": int(m.group(2))}


def config_hash(config: Dict[str, Any]) -> str:
    """First 4 hex digits of the SHA-256 of the config as sorted JSON."""
    blob = json.dumps(config, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()[:4]


def algorithm_id(arm: str, git: Dict[str, Dict[str, Any]],
                 config: Dict[str, Any]) -> str:
    """`<arm>@<experiments commit>+<fastener commit>#<config>[-dirty]`.

    `git` is the manifest's `git` block: {"experiments": ..., "fastener": ...},
    each as produced by `provenance.git_state`.
    """
    parts, dirty = [], False
    for repo in ("experiments", "fastener"):
        state = git.get(repo, {})
        commit = state.get("commit") if state.get("available") else None
        parts.append(commit[:7] if commit else "nogit")
        dirty = dirty or bool(state.get("code_dirty", state.get("dirty")))
    aid = f"{arm}@{'+'.join(parts)}#{config_hash(config)}"
    return aid + "-dirty" if dirty else aid


# --------------------------------------------------------------- ledger
def _cell(text: str) -> str:
    return text.strip().strip("`").strip()


def load_ledger(path: Path = LEDGER_PATH) -> List[Dict[str, Any]]:
    """Rows of the ledger table, oldest first."""
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c for c in line.strip().strip("|").split("|")]
        if len(cells) != len(LEDGER_COLUMNS):
            raise ValueError(f"malformed ledger row in {path}: {line!r}")
        exp, hyp, started, runs, status, report = cells
        rows.append({
            "experiment": _cell(exp),
            "hypothesis": _cell(hyp),
            "started": _cell(started),
            "runs": [_cell(r) for r in runs.split(",")
                     if _cell(r) not in ("", "--")],
            "status": _cell(status),
            "report": "" if report.strip() == "--" else report.strip(),
        })
    return rows


def save_ledger(rows: List[Dict[str, Any]], path: Path = LEDGER_PATH) -> None:
    lines = [LEDGER_HEADER.rstrip("\n"), "",
             "| " + " | ".join(LEDGER_COLUMNS) + " |",
             "|" + "---|" * len(LEDGER_COLUMNS)]
    for r in rows:
        runs = ", ".join(f"`{x}`" for x in r["runs"]) or "--"
        lines.append(f"| `{r['experiment']}` | {r['hypothesis']} | "
                     f"{r['started']} | {runs} | {r['status']} | "
                     f"{r['report'] or '--'} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@contextlib.contextmanager
def ledger_lock(path: Path = LEDGER_PATH, timeout: float = 60.0,
                stale: float = 120.0):
    """Hold the ledger for one read-modify-write.

    Runs started side by side each add themselves to the ledger at the same
    moment; without a lock, one read-modify-write can overwrite another's and a
    run silently drops out of the ledger. A lock file created with O_EXCL is
    the lock; one older than `stale` seconds is left over from a killed
    process and is removed.
    """
    lock = Path(str(path) + ".lock")
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > stale:
                    lock.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.time() > deadline:
                raise TimeoutError(f"could not lock {path} within {timeout} s; "
                                   f"remove {lock} if no run is starting")
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass


def find(rows: List[Dict[str, Any]], experiment_id: str) -> Optional[Dict]:
    return next((r for r in rows if r["experiment"] == experiment_id), None)


def next_experiment_id(hypothesis: str, path: Path = LEDGER_PATH) -> str:
    """The next unissued attempt number for `hypothesis` (e.g. 'H1', 'H2H3')."""
    if not HYPOTHESIS_RE.match(hypothesis):
        raise ValueError(f"not a hypothesis: {hypothesis!r}")
    used = [parse_experiment_id(r["experiment"])["attempt"]
            for r in load_ledger(path)
            if parse_experiment_id(r["experiment"])["group"] == hypothesis]
    return f"{hypothesis}-E{max(used, default=0) + 1:02d}"


def issue(hypothesis: str, path: Path = LEDGER_PATH) -> str:
    """Issue and record the next experiment ID for `hypothesis`."""
    with ledger_lock(path):
        eid = next_experiment_id(hypothesis, path)
        rows = load_ledger(path)
        rows.append(_new_row(eid))
        save_ledger(rows, path)
    return eid


def _new_row(experiment_id: str) -> Dict[str, Any]:
    info = parse_experiment_id(experiment_id)
    return {"experiment": experiment_id,
            "hypothesis": ", ".join(info["hypotheses"]),
            "started": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "runs": [], "status": "running", "report": ""}


def check_open(experiment_id: str, path: Path = LEDGER_PATH) -> None:
    """Raise unless `experiment_id` may take another run.

    An ID that is not in the ledger yet is accepted only if it is the next
    unissued one for its hypothesis -- skipping numbers, or reviving an old
    one, would break "never reused".
    """
    info = parse_experiment_id(experiment_id)
    row = find(load_ledger(path), experiment_id)
    if row is None:
        expected = next_experiment_id(info["group"], path)
        if experiment_id != expected:
            raise ValueError(f"{experiment_id} was never issued; the next ID "
                             f"for {info['group']} is {expected}")
        return
    if row["status"] not in OPEN_STATUSES:
        raise ValueError(f"{experiment_id} is closed (status "
                         f"{row['status']!r}); IDs are never reused -- issue a "
                         f"new one with: python experiments/experiment_ids.py "
                         f"new {info['group']}")


def add_run(experiment_id: str, run_id: str, path: Path = LEDGER_PATH) -> None:
    """Record `run_id` under `experiment_id`, creating the row if needed."""
    with ledger_lock(path):
        check_open(experiment_id, path)
        rows = load_ledger(path)
        row = find(rows, experiment_id)
        if row is None:
            row = _new_row(experiment_id)
            rows.append(row)
        if run_id not in row["runs"]:
            row["runs"].append(run_id)
        save_ledger(rows, path)


def set_status(experiment_id: str, status: str, report: Optional[str] = None,
               path: Path = LEDGER_PATH) -> None:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, not {status!r}")
    with ledger_lock(path):
        rows = load_ledger(path)
        row = find(rows, experiment_id)
        if row is None:
            raise ValueError(f"{experiment_id} is not in the ledger")
        row["status"] = status
        if report is not None:
            row["report"] = report
        save_ledger(rows, path)


def report_link(experiment_id: str) -> str:
    return f"[report](reports/{experiment_id}/REPORT.md)"


# ------------------------------------------------------------------ CLI
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_new = sub.add_parser("new", help="issue the next experiment ID")
    p_new.add_argument("hypothesis", help="e.g. H1, or H2H3 for a joint run")
    p_st = sub.add_parser("status", help="set an experiment's status")
    p_st.add_argument("experiment")
    p_st.add_argument("status", choices=STATUSES)
    sub.add_parser("list", help="print the ledger")
    args = ap.parse_args(argv)

    if args.cmd == "new":
        print(issue(args.hypothesis))
    elif args.cmd == "status":
        report = report_link(args.experiment) if args.status != "running" \
            and (REPORTS_DIR / args.experiment / "REPORT.md").is_file() else None
        set_status(args.experiment, args.status, report=report)
        print(f"{args.experiment}: {args.status}")
    else:
        for r in load_ledger():
            print(f"{r['experiment']:10s} {r['status']:9s} {r['started']}  "
                  f"{', '.join(r['runs']) or '--'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
