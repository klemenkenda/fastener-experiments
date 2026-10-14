"""Run an experiment as a queue of one-seed jobs, at most N at a time.

run_sota.py runs one dataset per process and its arms and seeds one after
another, on one core: the decision tree is single-threaded. An experiment whose
slowest dataset takes days therefore leaves most of the machine idle. This
launcher splits the experiment into one job per (dataset, arm, seed), each its
own run_sota.py process with --seed, and keeps up to --max-procs of them
running, starting the next as soon as one finishes.

Splitting changes nothing in the results: every search seeds its own RNG, so a
seed run alone is the one it would have been inside a five-seed run. Each job
is its own run ID in EXPERIMENTS.md, and make_report.py merges the runs of an
experiment by (dataset, arm, seed).

Jobs start in the order given, so list the slowest datasets and arms first;
otherwise the longest job may start last and set the wall clock on its own.

Writes results/<ID>/queue.json, the live state of every job, and one log per
job in results/<ID>/logs/. Watch the whole experiment with
`python experiments/monitor.py --experiment <ID>`.

Usage:
    python experiments/run_queue.py --experiment H1-E01 \\
        --datasets eodata,crop_mapping,madelon,gina \\
        --methods nsga2,nsga2_sparse --max-procs 10
    python experiments/run_queue.py ... --dry-run     # print the jobs only

An arm written fastener:<arm> runs that FASTENER arm (none, 2020, random,
guided) instead of a run_sota method. Arguments after `--` go to every job.

--budgets gives each job its own dataset's budget, from a JSON file of
{"budgets": {dataset: value}} such as calibrate_budget.py or cpu_budget.py
writes. Its "unit" says what the values are: "fits" (the default; each job
gets --evaluations) or "cpu_seconds" (each job gets --cpu-seconds, H4).
Every dataset must have one, and --evaluations or --cpu-seconds may not also
be passed:

    python experiments/run_queue.py --experiment H2H3-E01 \
        --datasets eodata,Coffee,... \
        --methods fastener:none,fastener:random,fastener:guided \
        --budgets results/h2h3-calibration/budgets.json

--timeout-hours stops a job that has run that long: its process tree is
killed and the job is recorded as `timeout`, not `failed`. It is the per-run
cap of H5/H6 (DEC-40): a method that cannot finish a dataset in the cap has
no result there, and the report says so. A timed-out job leaves its run
folder unfinished; nothing reads it as a result.

--skip names dataset:arm cells not to run at all, as a comma-separated list
or @file with one cell per line (# starts a comment): H5/H6's cells known
before the run to exceed the cap. Every skipped cell must be one the
datasets and methods would otherwise produce, so a typo cannot pass silently.

--resume restarts a queue that was stopped (the machine went down, say) with
the same arguments it was started with: jobs that ended done or timeout in
the queue's queue.json keep that state and are not run again; every other job,
the ones killed while running included, runs from the start. A killed job's
run folder is left unfinished, like a timed-out one's, and nothing reads it as
a result. The job list must match the old one exactly, so a resume cannot
quietly change the experiment.

Deterministic selectors (run_sota.FILTERS: mRMR, ReliefF, HSIC Lasso, the
rankers, RFE, all features) give the same answer for every seed, so they run
once, under the first seed, rather than once per seed.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS_DIR = HERE.parent / "results"
SEEDS = (2020, 2021, 2022, 2023, 2024)
# run_sota.py names a run by the second it starts; two jobs starting in the
# same second with the same name would collide. Names here differ per job, and
# the stagger also keeps the EXPERIMENTS.md ledger lock uncontended.
STAGGER_SECONDS = 1.5
POLL_SECONDS = 5


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    passthrough = []
    if "--" in argv:
        i = argv.index("--")
        argv, passthrough = argv[:i], argv[i + 1:]
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", default=None, metavar="ID",
                    help="experiment ID every job is evidence for")
    ap.add_argument("--name", default=None,
                    help="queue name, for a queue that is not an experiment "
                         "(a calibration, say): its folder under results/ "
                         "and the prefix of its run names. Default: the "
                         "experiment ID, else queue_<UTC time>")
    ap.add_argument("--datasets", required=True, help="comma-separated")
    ap.add_argument("--methods", required=True,
                    help="comma-separated run_sota methods or fastener:<arm>")
    ap.add_argument("--seeds", default=",".join(map(str, SEEDS)),
                    help="comma-separated, default 2020-2024")
    ap.add_argument("--budgets", type=Path, default=None,
                    help="JSON with {\"budgets\": {dataset: fits}}: each job "
                         "runs with --evaluations set to its dataset's budget")
    ap.add_argument("--max-procs", type=int, default=10)
    ap.add_argument("--skip", default=None,
                    help="dataset:arm cells not to run, comma-separated or "
                         "@file")
    ap.add_argument("--timeout-hours", type=float, default=None,
                    help="stop a job after this many hours (state: timeout)")
    ap.add_argument("--resume", action="store_true",
                    help="keep the done and timed-out jobs of this queue's "
                         "queue.json; run the rest")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    args.passthrough = passthrough
    args.budget_of, args.budget_unit = None, None
    if args.budgets is not None:
        if {"--evaluations", "--cpu-seconds"} & set(passthrough):
            ap.error("--budgets sets the budget per dataset; do not pass "
                     "--evaluations or --cpu-seconds as well")
        args.budget_unit, args.budget_of = load_budgets(
            args.budgets, split(args.datasets))
    return args


# A budget file's unit -> the run_sota.py flag that carries it.
BUDGET_FLAGS = {"fits": "--evaluations", "cpu_seconds": "--cpu-seconds"}


def load_budgets(path: Path, datasets):
    """(unit, dataset -> budget) for every dataset, or SystemExit naming gaps."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    budgets = data.get("budgets", data)
    unit = data.get("unit", "fits")
    if unit not in BUDGET_FLAGS:
        raise SystemExit(f"{path}: unknown budget unit {unit!r}; expected one "
                         f"of {sorted(BUDGET_FLAGS)}")
    kind = int if unit == "fits" else (int, float)

    def ok(v):
        return isinstance(v, kind) and not isinstance(v, bool) and v > 0
    missing = [d for d in datasets if not ok(budgets.get(d))]
    if missing:
        raise SystemExit(f"{path}: no budget for {', '.join(missing)}")
    return unit, {d: budgets[d] for d in datasets}


def split(s: str):
    return [x.strip() for x in s.split(",") if x.strip()]


def utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


# run_sota.FILTERS, the selectors with no randomness: one job each, not one
# per seed. Kept here rather than imported, since importing run_sota pins the
# queue's own numeric threads; tests/test_run_queue.py checks they agree.
DETERMINISTIC = ("mrmr", "relieff", "hsic_lasso", "kbest_mutual_info",
                 "kbest_anova_f", "tree_importance", "rfe_tree", "all_features")


def parse_skip(spec):
    """{(dataset, arm)} from 'a:b,c:d' or '@file' (one cell per line)."""
    if not spec:
        return set()
    if spec.startswith("@"):
        lines = Path(spec[1:]).read_text(encoding="utf-8").splitlines()
        items = [ln.split("#", 1)[0].strip() for ln in lines]
    else:
        items = split(spec)
    cells = set()
    for it in filter(None, items):
        ds, sep, arm = it.partition(":")
        if not sep or not ds or not arm:
            raise SystemExit(f"--skip: expected dataset:arm, got {it!r}")
        cells.add((ds.strip(), arm.strip()))
    return cells


def arm_label(m: str) -> str:
    return f"fastener_{m.split(':', 1)[1]}" if m.startswith("fastener:") else m


def build_jobs(args):
    jobs = []
    skip = parse_skip(getattr(args, "skip", None))
    known = {(ds, arm_label(m)) for ds in split(args.datasets)
             for m in split(args.methods)}
    unknown = sorted(skip - known)
    if unknown:
        raise SystemExit("--skip names cells this queue does not have: "
                         + ", ".join(f"{d}:{a}" for d, a in unknown))
    prefix = (args.name or args.experiment or "queue").lower().replace("-", "")
    seeds = [int(s) for s in split(args.seeds)]
    for ds in split(args.datasets):
        for m in split(args.methods):
            if (ds, arm_label(m)) in skip:
                continue
            for seed in (seeds[:1] if m in DETERMINISTIC else seeds):
                if m.startswith("fastener:"):
                    arm = m.split(":", 1)[1]
                    arm_args = ["--methods", "", "--fastener-arm", arm]
                    label = f"fastener_{arm}"
                else:
                    arm_args = ["--methods", m, "--no-fastener"]
                    label = m
                name = f"{prefix}_{ds}_{label}_s{seed}"
                cmd = [args.python, str(HERE / "run_sota.py"),
                       "--dataset", ds, *arm_args, "--seed", str(seed),
                       "--name", name]
                if args.experiment:
                    cmd += ["--experiment", args.experiment]
                budget = args.budget_of[ds] if args.budget_of else None
                if budget is not None:
                    cmd += [BUDGET_FLAGS[args.budget_unit], str(budget)]
                jobs.append({"name": name, "dataset": ds, "arm": label,
                             "seed": seed, "budget": budget,
                             "budget_unit": args.budget_unit,
                             "cmd": cmd + args.passthrough,
                             "state": "pending", "run_dir": None, "log": None,
                             "started_utc": None, "ended_utc": None,
                             "exit_code": None})
    return jobs


# States a resumed queue keeps; every other job runs again from the start.
FINISHED = ("done", "timeout")


def resume_jobs(jobs, status_path: Path):
    """jobs with the finished ones' state taken from an earlier queue.json.

    SystemExit if the earlier queue's job names differ from these, which
    would mean the queue is not being resumed with its own arguments.
    """
    old = {j["name"]: j for j in
           json.loads(Path(status_path).read_text(encoding="utf-8"))["jobs"]}
    names = [j["name"] for j in jobs]
    if set(old) != set(names):
        extra, missing = sorted(set(old) - set(names)), sorted(set(names) - set(old))
        raise SystemExit(f"--resume: {status_path} has a different job list "
                         f"({len(extra)} jobs only there, {len(missing)} only "
                         f"here, e.g. {(extra + missing)[:3]}); resume with "
                         f"the arguments the queue was started with")
    for j in jobs:
        if old[j["name"]]["state"] in FINISHED:
            j.update({k: v for k, v in old[j["name"]].items() if k != "cmd"})
    return jobs


def job_run_dir(j, results_dir: Path = None):
    """This job's run folder, or None while run_sota.py has not made it yet.

    run_sota.py names its folder <UTC stamp>_<name>, stamped when it starts,
    so the job's folder is the newest one stamped no earlier than the job was
    started. Without that bound, a folder left by an earlier queue under the
    same job name was taken for this job's (the first H4 calibration's
    COIL20, gisette, lymphoma, TOX_171 and warpPIE10P, DEC-37).
    """
    if not j.get("started_utc"):
        return None
    since = datetime.fromisoformat(j["started_utc"]).strftime("%Y%m%dT%H%M%SZ")
    found = sorted(d for d in (results_dir or RESULTS_DIR).glob(f"*_{j['name']}")
                   if d.name.split("_", 1)[0] >= since)
    return str(found[-1]) if found else None


class Queue:
    def __init__(self, args, jobs):
        self.args, self.jobs = args, jobs
        name = args.name or args.experiment or datetime.now(timezone.utc).strftime(
            "queue_%Y%m%dT%H%M%SZ")
        self.out = RESULTS_DIR / name
        (self.out / "logs").mkdir(parents=True, exist_ok=True)
        self.started = utc()
        self.procs, self.files = {}, {}

    def write_status(self) -> None:
        st = {"experiment": self.args.experiment, "started_utc": self.started,
              "updated_utc": utc(), "max_procs": self.args.max_procs,
              "pid": os.getpid(),
              "jobs": [{k: v for k, v in j.items() if k != "cmd"}
                       for j in self.jobs]}
        tmp = self.out / "queue.json.tmp"
        tmp.write_text(json.dumps(st, indent=2), encoding="utf-8")
        # On Windows the replace is refused while a reader (monitor.py) has
        # queue.json open. Retry briefly, then skip this update: the status
        # file is for watching, and must never stop the experiment.
        for _ in range(20):
            try:
                os.replace(tmp, self.out / "queue.json")
                return
            except PermissionError:
                time.sleep(0.1)

    def find_run_dir(self, j) -> None:
        j["run_dir"] = j["run_dir"] or job_run_dir(j)

    def start(self, j) -> None:
        log = self.out / "logs" / f"{j['name']}.log"
        self.files[j["name"]] = open(log, "w", encoding="utf-8")
        self.procs[j["name"]] = subprocess.Popen(
            j["cmd"], stdout=self.files[j["name"]], stderr=subprocess.STDOUT,
            cwd=str(HERE.parent))
        j.update(state="running", log=str(log), started_utc=utc())
        print(f"{stamp()}  start  {j['name']}", flush=True)

    def kill_tree(self, j) -> None:
        proc = self.procs[j["name"]]
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            proc.kill()
        proc.wait()

    def timed_out(self, j) -> bool:
        limit = self.args.timeout_hours
        if limit is None:
            return False
        started = datetime.fromisoformat(j["started_utc"])
        return (datetime.now(timezone.utc) - started).total_seconds()             >= limit * 3600

    def reap(self, j) -> None:
        code = self.procs[j["name"]].poll()
        if code is None and self.timed_out(j):
            self.kill_tree(j)
            self.files.pop(j["name"]).close()
            self.find_run_dir(j)
            j.update(state="timeout", exit_code=None, ended_utc=utc())
            print(f"{stamp()}  TIMEOUT {j['name']} (after "
                  f"{self.args.timeout_hours:g} h)", flush=True)
            return
        if code is None:
            return
        self.files.pop(j["name"]).close()
        self.find_run_dir(j)
        j.update(state="failed" if code else "done", exit_code=code,
                 ended_utc=utc())
        print(f"{stamp()}  {'FAILED' if code else 'done  '} {j['name']}"
              f" (exit {code})", flush=True)

    def run(self) -> int:
        print(f"{stamp()}  {len(self.jobs)} jobs, at most "
              f"{self.args.max_procs} at a time; status in "
              f"{self.out / 'queue.json'}", flush=True)
        while True:
            for j in [j for j in self.jobs if j["state"] == "running"]:
                self.find_run_dir(j)
                self.reap(j)
            running = [j for j in self.jobs if j["state"] == "running"]
            pending = [j for j in self.jobs if j["state"] == "pending"]
            while pending and len(running) < self.args.max_procs:
                j = pending.pop(0)
                self.start(j)
                running.append(j)
                self.write_status()
                time.sleep(STAGGER_SECONDS)
            self.write_status()
            if not running and not pending:
                break
            time.sleep(POLL_SECONDS)
        failed = [j for j in self.jobs if j["state"] == "failed"]
        timeout = [j for j in self.jobs if j["state"] == "timeout"]
        print(f"{stamp()}  finished: "
              f"{len(self.jobs) - len(failed) - len(timeout)} ok, "
              f"{len(failed)} failed, {len(timeout)} timed out")
        for j in failed:
            print(f"  FAILED {j['name']}: see {j['log']}")
        for j in timeout:
            print(f"  TIMEOUT {j['name']}")
        return 1 if failed else 0


def main(argv=None) -> int:
    args = parse_args(argv)
    jobs = build_jobs(args)
    if args.resume:
        name = args.name or args.experiment
        if not name:
            raise SystemExit("--resume needs --experiment or --name")
        jobs = resume_jobs(jobs, RESULTS_DIR / name / "queue.json")
        print(f"{stamp()}  resuming: "
              f"{sum(j['state'] in FINISHED for j in jobs)} jobs kept, "
              f"{sum(j['state'] == 'pending' for j in jobs)} to run",
              flush=True)
    if args.dry_run:
        for j in jobs:
            print(subprocess.list2cmdline(j["cmd"]))
        print(f"{len(jobs)} jobs, at most {args.max_procs} at a time")
        return 0
    return Queue(args, jobs).run()


if __name__ == "__main__":
    sys.exit(main())
