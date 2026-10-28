"""Distil results/ into a few small tables under experiments/distilled_logs/.

results/ is not tracked: the pickled FASTENER states, the selected-feature
lists and the job logs make it tens of gigabytes. The numbers the analysis
reads are a few megabytes, so this script keeps those, as xz-compressed csv
tables, one folder per experiment (the run's `experiment_id`, or the tag in
its name, e.g. `h56pilot`, for runs outside the ledger):

* `runs.csv.xz` -- one row per method and seed of a run: the run ID, dataset
  and its shape, the scalar fields of raw_results.json (method, seed,
  elapsed_seconds, model_fits, iterations, stopped_on, ...), the manifest's
  status, times, commit, command and params (as JSON);
* `records.csv.xz` -- one row per solution of a final front: n_features,
  val_score, test_score and every validation and test metric. The feature
  lists themselves are left out;
* `curves.csv.xz` -- the trajectories, one row per snapshot where the front
  or the best validation F1 changed (and the first and last): fits, seconds,
  best_val_f1, and val_auf, the validation AUF (K = h0_convergence.K) of the
  front in force, the quantity H0's convergence rule reads;
* `jobs.csv.xz` -- the queue's jobs (state, times, exit code), with the tail
  of the log, repeated lines dropped, for every job that did not finish;
* `files/<dir>/` -- the small .json/.csv/.md files of the experiment's own
  directory in results/ (e.g. H0-E01/h0_summary.json).

`index.json` holds a signature (sizes and modification times) of the source
files of every run and experiment directory distilled. A source whose
signature is unchanged is not read again; an experiment's tables are
rewritten only when one of its sources changed. A source deleted from
results/ keeps its rows.

Read a table with e.g. `pandas.read_csv(".../records.csv.xz")`.

Usage:
    python experiments/distill_results.py
    python experiments/distill_results.py --force
"""
import argparse
import csv
import hashlib
import io
import json
import lzma
import os
import shutil
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import h0_convergence  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "results"
OUT_DIR = REPO_ROOT / "experiments" / "distilled_logs"
INDEX = OUT_DIR / "index.json"

TABLES = ("runs", "records", "curves", "jobs")
RUN_FILES = ("manifest.json", "raw_results.json", "raw_results_partial.json",
             "progress.json")
SMALL_FILE_MAX = 256 * 1024
SMALL_SUFFIXES = {".json", ".csv", ".md", ".txt"}
QUEUE_FILES = {"queue.json", "jobs.json"}
LOG_TAIL_LINES = 30
MAX_REPEATS = 3
XZ_PRESET = 9 | lzma.PRESET_EXTREME
csv.field_size_limit(2 ** 31 - 1)


# -- signatures --------------------------------------------------------------

def signature(paths) -> str:
    h = hashlib.sha1()
    for p in sorted(paths):
        if p.is_file():
            st = p.stat()
            h.update(f"{p.name}|{st.st_size}|{st.st_mtime_ns}\n".encode())
    return h.hexdigest()[:16]


def run_sources(d: Path):
    srcs = [d / f for f in RUN_FILES]
    td = d / "trajectories"
    if td.is_dir():
        srcs += sorted(td.glob("*.jsonl"))
    return srcs


def dir_sources(d: Path):
    return [p for p in d.iterdir() if p.is_file()
            and (p.name in QUEUE_FILES or small_file(p))]


def small_file(p: Path) -> bool:
    return p.suffix in SMALL_SUFFIXES and p.name not in QUEUE_FILES \
        and ".tmp" not in p.name and p.stat().st_size <= SMALL_FILE_MAX


def is_run_dir(d: Path) -> bool:
    return any((d / f).is_file() for f in RUN_FILES)


# -- reading one run ---------------------------------------------------------

def read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def group_of(run_id: str, manifest) -> str:
    exp = (manifest or {}).get("experiment_id")
    if exp:
        return exp
    parts = run_id.split("_")
    return parts[1] if len(parts) > 1 else run_id


def scalars(d: dict, prefix: str = "") -> dict:
    return {prefix + k: v for k, v in d.items()
            if v is None or isinstance(v, (str, int, float, bool))}


def distil_run(d: Path):
    run_id = d.name
    m = read_json(d / "manifest.json") or {}
    results = None
    for name in ("raw_results.json", "raw_results_partial.json"):
        results = read_json(d / name)
        if results is not None:
            source = name
            break
    progress = read_json(d / "progress.json") or {}
    ds = m.get("dataset") or {}
    git = ((m.get("git") or {}).get("experiments") or {})
    base = {
        "run_id": run_id, "experiment": m.get("experiment_id"),
        "name": m.get("name"), "dataset": ds.get("name")
        or (m.get("params") or {}).get("dataset"),
        "dataset_n_features": ds.get("n_features"),
        "n_train": ds.get("n_train"), "n_val": ds.get("n_val"),
        "n_test": ds.get("n_test"), "run_status": m.get("status"),
        "progress_status": progress.get("status"),
        "progress_error": progress.get("error"),
        "started_utc": m.get("started_utc"), "ended_utc": m.get("ended_utc"),
        "run_elapsed_seconds": m.get("elapsed_seconds"),
        "commit": git.get("commit"), "dirty": git.get("dirty"),
        "command": m.get("command"),
        "params": json.dumps(m.get("params"), sort_keys=True)
        if m.get("params") is not None else None,
        "results_file": source if results is not None else None,
    }
    runs, records = [], []
    for res in results or [{}]:
        row = dict(base)
        row.update(scalars({k: v for k, v in res.items() if k != "records"}))
        row["n_records"] = len(res.get("records") or ())
        runs.append(row)
        for i, r in enumerate(res.get("records") or ()):
            rec = {"run_id": run_id, "method": res.get("method"),
                   "seed": res.get("seed"), "rank": i}
            rec.update(scalars({k: v for k, v in r.items()
                                if k not in ("features", "val", "test")}))
            rec.update(scalars(r.get("val") or {}, "val_"))
            rec.update(scalars(r.get("test") or {}, "test_"))
            records.append(rec)
    curves = []
    for p in sorted((d / "trajectories").glob("*.jsonl")) \
            if (d / "trajectories").is_dir() else ():
        curves += distil_trajectory(run_id, p)
    return group_of(run_id, m), {"runs": runs, "records": records,
                                 "curves": curves}


def distil_trajectory(run_id: str, p: Path):
    """The first and last snapshot, and each where the front or the best
    validation F1 by k changed: the step curves are unchanged."""
    rows, front, prev_by_k, pending = [], [], None, None

    def row(s):
        return {"run_id": run_id, "trajectory": p.stem,
                "method": s.get("method"), "seed": s.get("seed"),
                "iteration": s.get("iteration"), "fits": s.get("fits"),
                "seconds": s.get("seconds"),
                "best_val_f1": s.get("best_val_f1"),
                "val_auf": h0_convergence.val_auf(front),
                "front_len": len(front), "min_size": s.get("min_size"),
                "max_size": s.get("max_size")}
    with open(p, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                s = json.loads(line)
            except ValueError:
                continue  # a line cut short by a killed run
            changed = bool(s.get("front_changed"))
            if changed:
                front = s.get("front") or []
            by_k = s.get("best_val_f1_by_k")
            if not rows or changed or by_k != prev_by_k:
                rows.append(row(s))
                pending = None
            else:
                pending = row(s)
            prev_by_k = by_k
    if pending is not None:
        rows.append(pending)
    return rows


# -- reading one experiment directory ----------------------------------------

def log_tail(path: Path) -> str:
    """The last LOG_TAIL_LINES lines of a log, without the lines repeated
    more than MAX_REPEATS times (warnings that make gigabytes of a log)."""
    counts, tail = {}, deque(maxlen=LOG_TAIL_LINES)
    try:
        with open(path, "rb") as fh:
            for line in fh:
                key = hash(line)
                counts[key] = counts.get(key, 0) + 1
                if counts[key] <= MAX_REPEATS and line.strip():
                    tail.append(line.decode("utf-8", "replace").rstrip())
    except OSError:
        return None
    return "\n".join(tail)


def distil_dir(d: Path):
    q = read_json(d / "queue.json") or read_json(d / "jobs.json") or {}
    group = q.get("experiment") or d.name
    jobs = []
    for j in q.get("jobs") or ():
        row = {"queue_dir": d.name}
        row.update(scalars({k: v for k, v in j.items() if k != "cmd"}))
        if row.get("run_dir"):
            row["run_dir"] = Path(str(row["run_dir"]).replace("\\", "/")).name
        if j.get("log"):
            row["log"] = Path(str(j["log"]).replace("\\", "/")).name
            if j.get("state") not in ("done", None):
                row["log_tail"] = log_tail(d / "logs" / row["log"])
        jobs.append(row)
    files = [p for p in d.iterdir() if p.is_file() and small_file(p)]
    return group, {"jobs": jobs}, files


# -- tables ------------------------------------------------------------------

def table_path(group: str, table: str) -> Path:
    return OUT_DIR / group / f"{table}.csv.xz"


def load_table(group: str, table: str):
    p = table_path(group, table)
    if not p.is_file():
        return []
    with lzma.open(p, "rt", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_table(group: str, table: str, rows) -> None:
    p = table_path(group, table)
    if not rows:
        if p.is_file():
            p.unlink()
        return
    cols = []
    for r in rows:
        cols += [c for c in r if c not in cols]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".part")
    tmp.write_bytes(lzma.compress(buf.getvalue().encode("utf-8"),
                                  preset=XZ_PRESET))
    os.replace(tmp, p)


def key_of(table: str, row) -> str:
    return row["queue_dir"] if table == "jobs" else row["run_id"]


# -- main --------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--force", action="store_true",
                    help="read every source again")
    args = ap.parse_args()
    if not RESULTS_DIR.is_dir():
        sys.exit(f"no results directory: {RESULTS_DIR}")

    index = {} if args.force else (read_json(INDEX) or {})
    entries = sorted(p for p in RESULTS_DIR.iterdir() if p.is_dir())
    fresh = defaultdict(lambda: defaultdict(list))  # group -> table -> rows
    replaced = defaultdict(set)                     # group -> keys re-read
    copies = defaultdict(list)                      # group -> small files
    skipped = 0
    for i, d in enumerate(entries, 1):
        run = is_run_dir(d)
        sig = signature(run_sources(d) if run else dir_sources(d))
        old = index.get(d.name)
        if old and old[1] == sig:
            skipped += 1
        else:
            if run:
                group, tables = distil_run(d)
            else:
                group, tables, files = distil_dir(d)
                copies[group] += [(d.name, f) for f in files]
            for t, rows in tables.items():
                fresh[group][t] += rows
            replaced[group].add(d.name)
            if old and old[0] != group:
                replaced[old[0]].add(d.name)
            index[d.name] = [group, sig]
        if i % 500 == 0 or i == len(entries):
            print(f"[{i}/{len(entries)}] {i - skipped} read, "
                  f"{skipped} unchanged", flush=True)

    for group in sorted(replaced):
        for t in TABLES:
            keep = [r for r in load_table(group, t)
                    if key_of(t, r) not in replaced[group]]
            rows = keep + fresh[group][t]
            rows.sort(key=lambda r: key_of(t, r))  # stable: keeps row order
            write_table(group, t, rows)
        for dirname, f in copies[group]:
            dst = OUT_DIR / group / "files" / dirname / f.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, dst)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    INDEX.write_text("{\n" + ",\n".join(
        f"{json.dumps(k)}: {json.dumps(v)}" for k, v in sorted(index.items()))
        + "\n}\n", encoding="utf-8")
    total = sum(p.stat().st_size for p in OUT_DIR.rglob("*") if p.is_file())
    print(f"{len(entries) - skipped} sources read, {skipped} unchanged; "
          f"{len(replaced)} experiments rewritten; "
          f"{OUT_DIR.relative_to(REPO_ROOT)} is {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
