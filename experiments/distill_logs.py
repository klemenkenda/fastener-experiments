"""Distill an experiment's job logs into a short digest.

Thousands of logs (one per job, results/<ID>/logs/*.log) say the same few
things many times. This groups their lines by signature -- the line with
paths, run IDs, numbers and hex shortened to placeholders -- and reports each
signature once, with how many logs carry it and an example, under:

* errors: tracebacks (by their final exception line), "FAILED", out of
  memory, killed, time limit;
* warnings: Python warnings (category and message) and other "warning" lines;
* incomplete: logs that never reached their closing line (`manifest:`),
  with the job's state from results/<ID>/status/ when there is one;
* stopped_on and wall time per log: a filter's "total wall time", or the sum
  of a search's per-seed times.

    python experiments/distill_logs.py --experiment H10-E01
    python experiments/distill_logs.py results/H5H6-E03/logs/*.log --json out.json

Read-only. The digest goes to stdout (Markdown) and, with --json, to a file.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional

RESULTS = Path(__file__).resolve().parent.parent / "results"

_SUBS = [
    (re.compile(r"\d{8}T\d{6}Z_[\w.-]+"), "<run>"),          # run IDs
    (re.compile(r"(?:[A-Za-z]:)?[/\\][^\s:'\"]*[/\\]([^\s/\\:'\"]+)"), r"<path>/\1"),
    (re.compile(r"0x[0-9a-fA-F]+"), "<hex>"),
    (re.compile(r"(?<![A-Za-z_])[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?"), "<n>"),
]
ERROR = re.compile(r"FAILED|Error\b|Exception\b|out of memory|oom-kill|Killed|"
                   r"MemoryError|DUE TO TIME LIMIT|CANCELLED|Segmentation fault",
                   re.I)
WARNING = re.compile(r"\b(\w*Warning)\b:?\s*(.*)|\bwarning\b", re.I)
WALL = re.compile(r"total wall time:\s*([\d.]+)s")
SEED_SECONDS = re.compile(r"^\s*seed \d+: .*\(([\d.]+)s\)\s*$")
STOPPED = re.compile(r"stopped_on=(\S+)")
CLOSING = "manifest:"


def signature(line: str) -> str:
    s = line.strip()
    for rx, rep in _SUBS:
        s = rx.sub(rep, s)
    return s[:200]


def read(path: Path) -> List[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return [f"<unreadable: {exc}>"]


_QUEUES: Dict[Path, Dict[str, str]] = {}


def job_state(log: Path) -> Optional[str]:
    """The job's state: from its status file (Vega, hpc_jobs.py) or from the
    queue's queue.json (the workstation, run_queue.py), beside the logs."""
    base = log.parent.parent
    try:
        st = json.loads((base / "status" / (log.stem + ".json")).read_text(encoding="utf-8"))
        return st.get("state")
    except (OSError, ValueError):
        pass
    if base not in _QUEUES:
        try:
            q = json.loads((base / "queue.json").read_text(encoding="utf-8"))
            _QUEUES[base] = {j["name"]: j.get("state") for j in q.get("jobs", [])}
        except (OSError, ValueError, AttributeError, KeyError):
            _QUEUES[base] = {}
    return _QUEUES[base].get(log.stem)


def distill(paths: Iterable[Path]) -> Dict:
    groups = {"errors": defaultdict(lambda: {"logs": set(), "lines": 0, "example": None}),
              "warnings": defaultdict(lambda: {"logs": set(), "lines": 0, "example": None})}
    incomplete, stopped, walls, n = [], Counter(), [], 0

    def add(kind, sig, log, raw):
        g = groups[kind][sig]
        g["logs"].add(log)
        g["lines"] += 1
        if g["example"] is None:
            g["example"] = (log, raw.strip()[:300])

    for p in paths:
        n += 1
        lines, name = read(p), p.name
        in_tb, total, seeds = False, None, []
        for line in lines:
            if line.startswith("Traceback (most recent call last)"):
                in_tb = True
                continue
            if in_tb:
                # The traceback ends at its first unindented line: the exception.
                if line and not line[0].isspace():
                    add("errors", "Traceback -> " + signature(line), name, line)
                    in_tb = False
                continue
            m = STOPPED.search(line)
            if m:
                stopped[m.group(1)] += 1
            m = WALL.search(line)
            if m:
                total = float(m.group(1))
            m = SEED_SECONDS.match(line)
            if m:
                seeds.append(float(m.group(1)))
            if ERROR.search(line):
                add("errors", signature(line), name, line)
            elif WARNING.search(line):
                add("warnings", signature(line), name, line)
        if total is not None or seeds:
            walls.append(total if total is not None else sum(seeds))
        if not any(l.startswith(CLOSING) for l in lines):
            tail = next((l for l in reversed(lines) if l.strip()), "<empty>")
            incomplete.append({"log": name, "state": job_state(p),
                               "last_line": tail.strip()[:300]})

    def table(kind):
        rows = [{"signature": s, "logs": len(g["logs"]), "lines": g["lines"],
                 "example_log": g["example"][0], "example": g["example"][1]}
                for s, g in groups[kind].items()]
        return sorted(rows, key=lambda r: (-r["logs"], -r["lines"]))

    walls.sort()
    q = (lambda f: walls[min(len(walls) - 1, int(f * len(walls)))]) if walls else None
    return {"logs": n, "errors": table("errors"), "warnings": table("warnings"),
            "incomplete": incomplete, "stopped_on": dict(stopped.most_common()),
            "wall_seconds": ({"runs": len(walls), "median": q(0.5), "p90": q(0.9),
                              "max": walls[-1], "total_hours": sum(walls) / 3600}
                             if walls else None)}


def markdown(d: Dict, title: str, top: int) -> str:
    out = [f"# Log digest: {title}", "", f"{d['logs']} logs read.", ""]
    for kind in ("errors", "warnings"):
        rows = d[kind]
        out += [f"## {kind.capitalize()} ({len(rows)} signatures)", ""]
        if not rows:
            out += ["None.", ""]
            continue
        out += ["| logs | lines | signature | example log |", "|---|---|---|---|"]
        for r in rows[:top]:
            sig = r["signature"].replace("|", "\\|")
            out.append(f"| {r['logs']} | {r['lines']} | `{sig}` | {r['example_log']} |")
        if len(rows) > top:
            out.append(f"| ... | | {len(rows) - top} more (--top, --json) | |")
        out.append("")
    inc = d["incomplete"]
    out += [f"## Incomplete logs ({len(inc)})", ""]
    if inc:
        by_tail = Counter((r["state"] or "no status", signature(r["last_line"]))
                          for r in inc)
        out += ["| logs | job state | last line (signature) |", "|---|---|---|"]
        out += ["| %d | %s | `%s` |" % (c, st, s.replace("|", "\\|"))
                for (st, s), c in by_tail.most_common(top)]
        out += ["", "First few: " + ", ".join(r["log"] for r in inc[:10])]
    else:
        out.append("None: every log reached its closing line.")
    out += ["", "## Runs", ""]
    if d["stopped_on"]:
        out.append("stopped_on: " + ", ".join(f"{k} {v}" for k, v in d["stopped_on"].items()))
    w = d["wall_seconds"]
    if w:
        out.append(f"wall time per log: {w['runs']} logs, median {w['median']:.0f} s, "
                   f"p90 {w['p90']:.0f} s, max {w['max']:.0f} s, "
                   f"total {w['total_hours']:.1f} h")
    return "\n".join(out) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", help="log files or globs")
    ap.add_argument("--experiment", help="read results/<ID>/logs/*.log")
    ap.add_argument("--top", type=int, default=25, help="rows per table")
    ap.add_argument("--json", help="also write the full digest here")
    args = ap.parse_args(argv)
    pats = list(args.paths)
    if args.experiment:
        pats.append(str(RESULTS / args.experiment / "logs" / "*.log"))
    paths = sorted({Path(p) for pat in pats for p in glob.glob(pat)})
    if not paths:
        raise SystemExit("no logs found")
    d = distill(paths)
    sys.stdout.write(markdown(d, args.experiment or f"{len(paths)} files", args.top))
    if args.json:
        Path(args.json).write_text(json.dumps(d, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
