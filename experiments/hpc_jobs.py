"""Run an experiment's queue as a SLURM job array, one job per array task.

run_queue.py keeps a queue of one-seed jobs running on one machine. On a
cluster (HPC Vega, H5H6-E02) the scheduler does that instead: this module
writes the same jobs to a file, runs one of them per array task, and gathers
the tasks' states back into the queue.json that monitor.py and make_report.py
read. The jobs are run_queue.build_jobs's, from the same arguments, so a grid
run here is the grid run_queue.py would have run.

    python experiments/hpc_jobs.py emit --experiment H5H6-E02 \\
        --datasets ... --methods ... --budgets experiments/h2h3_budgets.json \\
        --skip @experiments/h5h6_skip.txt --timeout-hours 6 -- --model rf
    python experiments/hpc_jobs.py count --experiment H5H6-E02
    python experiments/hpc_jobs.py indices --experiment H5H6-E02 --unfinished \
        --cells @hpc/vega/h5h6e02_highmem.txt [--invert]
    python experiments/hpc_jobs.py run --experiment H5H6-E02 --index 17
    python experiments/hpc_jobs.py collect --experiment H5H6-E02

`emit` takes run_queue.py's arguments (everything after `--` goes to every
run_sota.py job) and writes results/<ID>/jobs.json. `run` runs job <index>:
it adds `--model-jobs N --n-jobs N` for the task's cores (SLURM_CPUS_PER_TASK,
or --cpus), stops the job at the queue's --timeout-hours as run_queue.py does
(state "timeout"), and writes results/<ID>/status/<name>.json and
results/<ID>/logs/<name>.log. A job already done or timed out is not run
again, so a whole array can be resubmitted after an interruption. `collect`
writes results/<ID>/queue.json from the status files; jobs with none are
pending.

`merge-ledger --from FILE` adds the experiment's runs from another copy of
EXPERIMENTS.md -- the cluster's, fetched by hpc/vega/fetch.sh -- to this
ledger's row, so the runs need no commit on the cluster.
"""
import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import experiment_ids  # noqa: E402
import run_queue  # noqa: E402

RESULTS_DIR = run_queue.RESULTS_DIR
# States a job keeps: run again, it would do the same work for nothing.
FINISHED = run_queue.FINISHED
POLL_SECONDS = 5


def queue_dir(experiment: str) -> Path:
    return RESULTS_DIR / experiment


def write_json(path: Path, data) -> None:
    """Write via a temporary file, so a reader never sees half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def load_jobs(experiment: str) -> Dict:
    path = queue_dir(experiment) / "jobs.json"
    if not path.is_file():
        raise SystemExit(f"{path} not found; run `hpc_jobs.py emit` first")
    return json.loads(path.read_text(encoding="utf-8"))


def emit(argv: List[str]) -> int:
    args = run_queue.parse_args(argv)
    if not args.experiment and not args.name:
        raise SystemExit("emit needs --experiment (or --name)")
    jobs = run_queue.build_jobs(args)
    name = args.name or args.experiment
    out = queue_dir(name) / "jobs.json"
    if out.is_file():
        old = [j["name"] for j in json.loads(
            out.read_text(encoding="utf-8"))["jobs"]]
        if old != [j["name"] for j in jobs]:
            raise SystemExit(f"{out} exists with a different job list; an "
                             f"experiment's jobs are emitted once")
    write_json(out, {"experiment": args.experiment, "name": name,
                     "timeout_hours": args.timeout_hours,
                     "created_utc": run_queue.utc(),
                     "jobs": [{k: j[k] for k in ("name", "dataset", "arm",
                                                 "seed", "budget",
                                                 "budget_unit", "cmd")}
                              for j in jobs]})
    print(f"{len(jobs)} jobs -> {out}")
    return 0


def status_path(name: str, job: str) -> Path:
    return queue_dir(name) / "status" / f"{job}.json"


def read_status(name: str, job: str) -> Optional[Dict]:
    p = status_path(name, job)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def kill_group(proc: subprocess.Popen) -> None:
    """The job and every process it started (its own session)."""
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError, AttributeError):
        proc.kill()
    proc.wait()


def run(experiment: str, index: int, cpus: Optional[int]) -> int:
    spec = load_jobs(experiment)
    name, jobs = spec["name"], spec["jobs"]
    if not 0 <= index < len(jobs):
        raise SystemExit(f"index {index} out of range: {len(jobs)} jobs")
    j = jobs[index]
    old = read_status(name, j["name"])
    if old and old.get("state") in FINISHED:
        print(f"{j['name']}: already {old['state']}, not run again")
        return 0
    cpus = cpus or int(os.environ.get("SLURM_CPUS_PER_TASK", "1"))
    cmd = j["cmd"] + ["--model-jobs", str(cpus), "--n-jobs", str(cpus)]
    log = queue_dir(name) / "logs" / f"{j['name']}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    st = {"name": j["name"], "dataset": j["dataset"], "arm": j["arm"],
          "seed": j["seed"], "budget": j["budget"],
          "budget_unit": j["budget_unit"], "index": index,
          "state": "running", "run_dir": None, "log": str(log),
          "started_utc": run_queue.utc(), "ended_utc": None,
          "exit_code": None, "host": socket.gethostname(), "cpus": cpus,
          "slurm_job": os.environ.get("SLURM_JOB_ID"),
          "slurm_array_task": os.environ.get("SLURM_ARRAY_TASK_ID")}
    write_json(status_path(name, j["name"]), st)

    with open(log, "w", encoding="utf-8") as fh:
        proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT,
                                cwd=str(run_queue.HERE.parent),
                                start_new_session=True)

        def stop(signum, frame):
            # SLURM's own time limit or a scancel: stop the job, and say so,
            # rather than leave the status "running" for ever.
            kill_group(proc)
            st.update(state="failed", exit_code=-signum,
                      ended_utc=run_queue.utc(),
                      run_dir=run_queue.job_run_dir(st),
                      note=f"stopped by signal {signum} (SLURM time limit "
                           f"or scancel)")
            write_json(status_path(name, j["name"]), st)
            sys.exit(1)
        signal.signal(signal.SIGTERM, stop)

        limit = (spec.get("timeout_hours") or 0) * 3600 or None
        t0 = time.monotonic()
        code = None
        while code is None:
            try:
                code = proc.wait(timeout=POLL_SECONDS)
            except subprocess.TimeoutExpired:
                if limit and time.monotonic() - t0 >= limit:
                    kill_group(proc)
                    break
    st.update(ended_utc=run_queue.utc(), run_dir=run_queue.job_run_dir(st))
    if code is None:
        st.update(state="timeout", exit_code=None)
    else:
        st.update(state="failed" if code else "done", exit_code=code)
    write_json(status_path(name, j["name"]), st)
    print(f"{j['name']}: {st['state']} (exit {st['exit_code']})")
    return 0 if st["state"] in FINISHED else 1


def collect(experiment: str) -> int:
    spec = load_jobs(experiment)
    name = spec["name"]
    jobs, starts = [], []
    for j in spec["jobs"]:
        st = read_status(name, j["name"]) or {}
        row = {"name": j["name"], "dataset": j["dataset"], "arm": j["arm"],
               "seed": j["seed"], "budget": j["budget"],
               "budget_unit": j["budget_unit"],
               "state": st.get("state", "pending"),
               "run_dir": st.get("run_dir"), "log": st.get("log"),
               "started_utc": st.get("started_utc"),
               "ended_utc": st.get("ended_utc"),
               "exit_code": st.get("exit_code")}
        if row["state"] == "running" and not row["run_dir"]:
            row["run_dir"] = run_queue.job_run_dir(row)
        if row["started_utc"]:
            starts.append(row["started_utc"])
        jobs.append(row)
    # pid None: no single driver process to check (monitor.alive -> None).
    write_json(queue_dir(name) / "queue.json",
               {"experiment": spec["experiment"],
                "started_utc": min(starts) if starts else None,
                "updated_utc": run_queue.utc(),
                "max_procs": int(os.environ.get("HPC_MAX_PARALLEL", "0"))
                or len(jobs), "pid": None, "jobs": jobs})
    counts: Dict[str, int] = {}
    for r in jobs:
        counts[r["state"]] = counts.get(r["state"], 0) + 1
    print(f"{name}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    return 0


def ranges(indices: List[int]) -> str:
    """0,1,2,5,7,8 -> "0-2,5,7-8": an sbatch --array specification."""
    out, start = [], None
    for i, x in enumerate(indices):
        if start is None:
            start = x
        if i + 1 == len(indices) or indices[i + 1] != x + 1:
            out.append(str(start) if start == x else f"{start}-{x}")
            start = None
    return ",".join(out)


def select(experiment: str, cells: Optional[str] = None, invert: bool = False,
           unfinished: bool = False) -> List[int]:
    """Indices of the jobs to submit.

    `cells` ("dataset:arm,..." or "@file", run_queue's skip syntax; arm `*`
    matches any) keeps the jobs in those cells -- or, with `invert`, the
    rest. `unfinished` drops jobs already done or timed out, so a
    resubmission schedules only the work left.
    """
    spec = load_jobs(experiment)
    want = run_queue.parse_skip(cells) if cells else set()
    out = []
    for i, j in enumerate(spec["jobs"]):
        hit = (j["dataset"], j["arm"]) in want or (j["dataset"], "*") in want
        if cells and hit == invert:
            continue
        if unfinished:
            st = read_status(spec["name"], j["name"])
            if st and st.get("state") in FINISHED:
                continue
        out.append(i)
    return out


def merge_ledger(experiment: str, other: Path,
                 path: Path = experiment_ids.LEDGER_PATH) -> int:
    """Add the runs `other`'s ledger lists for `experiment` to this ledger.

    Only that row's run list changes, and only by addition: runs already
    here keep their place, new ones follow in the other ledger's order.
    """
    theirs = experiment_ids.find(experiment_ids.load_ledger(Path(other)),
                                 experiment)
    if theirs is None:
        raise SystemExit(f"{other} has no row for {experiment}")
    with experiment_ids.ledger_lock(path):
        rows = experiment_ids.load_ledger(path)
        mine = experiment_ids.find(rows, experiment)
        if mine is None:
            raise SystemExit(f"{path} has no row for {experiment}; register "
                             f"it before merging its runs")
        new = [r for r in theirs["runs"] if r not in mine["runs"]]
        mine["runs"] += new
        experiment_ids.save_ledger(rows, path)
    print(f"{experiment}: {len(new)} runs added, {len(mine['runs'])} in all")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    commands = ("emit", "count", "indices", "run", "collect", "merge-ledger")
    if not argv or argv[0] not in commands:
        raise SystemExit(f"usage: hpc_jobs.py {{{','.join(commands)}}} ...")
    cmd, rest = argv[0], argv[1:]
    if cmd == "emit":
        return emit(rest)
    ap = argparse.ArgumentParser(prog=f"hpc_jobs.py {cmd}")
    ap.add_argument("--experiment", required=True)
    if cmd == "run":
        ap.add_argument("--index", type=int, default=None,
                        help="job index; default SLURM_ARRAY_TASK_ID plus "
                             "HPC_INDEX_OFFSET")
        ap.add_argument("--cpus", type=int, default=None)
    if cmd == "merge-ledger":
        ap.add_argument("--from", dest="other", required=True, type=Path,
                        help="the other copy of EXPERIMENTS.md")
    if cmd == "indices":
        ap.add_argument("--cells", default=None,
                        help="dataset:arm cells (comma list or @file; arm * "
                             "for every arm) to keep")
        ap.add_argument("--invert", action="store_true",
                        help="keep the jobs NOT in --cells")
        ap.add_argument("--unfinished", action="store_true",
                        help="leave out jobs already done or timed out")
    args = ap.parse_args(rest)
    if cmd == "indices":
        print(ranges(select(args.experiment, args.cells, args.invert,
                            args.unfinished)))
        return 0
    if cmd == "merge-ledger":
        return merge_ledger(args.experiment, args.other)
    if cmd == "count":
        print(len(load_jobs(args.experiment)["jobs"]))
        return 0
    if cmd == "collect":
        return collect(args.experiment)
    index = args.index
    if index is None:
        if "SLURM_ARRAY_TASK_ID" not in os.environ:
            raise SystemExit("--index, or run inside a SLURM array task")
        index = (int(os.environ["SLURM_ARRAY_TASK_ID"])
                 + int(os.environ.get("HPC_INDEX_OFFSET", "0")))
    return run(args.experiment, index, args.cpus)


if __name__ == "__main__":
    sys.exit(main())
