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


def build_jobs(args):
    jobs = []
    prefix = (args.name or args.experiment or "queue").lower().replace("-", "")
    for ds in split(args.datasets):
        for m in split(args.methods):
            for seed in (int(s) for s in split(args.seeds)):
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
        # run_sota.py names its directory <UTC stamp>_<name>; the newest one
        # is this job's.
        if j["run_dir"] is None:
            found = sorted(RESULTS_DIR.glob(f"*_{j['name']}"))
            if found:
                j["run_dir"] = str(found[-1])

    def start(self, j) -> None:
        log = self.out / "logs" / f"{j['name']}.log"
        self.files[j["name"]] = open(log, "w", encoding="utf-8")
        self.procs[j["name"]] = subprocess.Popen(
            j["cmd"], stdout=self.files[j["name"]], stderr=subprocess.STDOUT,
            cwd=str(HERE.parent))
        j.update(state="running", log=str(log), started_utc=utc())
        print(f"{stamp()}  start  {j['name']}", flush=True)

    def reap(self, j) -> None:
        code = self.procs[j["name"]].poll()
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
        print(f"{stamp()}  finished: {len(self.jobs) - len(failed)} ok, "
              f"{len(failed)} failed")
        for j in failed:
            print(f"  FAILED {j['name']}: see {j['log']}")
        return 1 if failed else 0


def main(argv=None) -> int:
    args = parse_args(argv)
    jobs = build_jobs(args)
    if args.dry_run:
        for j in jobs:
            print(subprocess.list2cmdline(j["cmd"]))
        print(f"{len(jobs)} jobs, at most {args.max_procs} at a time")
        return 0
    return Queue(args, jobs).run()


if __name__ == "__main__":
    sys.exit(main())
