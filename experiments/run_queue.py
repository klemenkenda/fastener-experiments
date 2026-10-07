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

Usage:
    python experiments/run_queue.py --experiment H1-E01 \\
        --datasets eodata,crop_mapping,madelon,gina \\
        --methods nsga2,nsga2_sparse --max-procs 10
    python experiments/run_queue.py ... --dry-run     # print the jobs only

An arm written fastener:<arm> runs that FASTENER arm (none, 2020, random,
guided) instead of a run_sota method. Arguments after `--` go to every job.
"""
import argparse
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
    ap.add_argument("--datasets", required=True, help="comma-separated")
    ap.add_argument("--methods", required=True,
                    help="comma-separated run_sota methods or fastener:<arm>")
    ap.add_argument("--seeds", default=",".join(map(str, SEEDS)),
                    help="comma-separated, default 2020-2024")
    ap.add_argument("--max-procs", type=int, default=10)
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    args.passthrough = passthrough
    return args


def split(s: str):
    return [x.strip() for x in s.split(",") if x.strip()]


def build_jobs(args):
    jobs = []
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
                prefix = (args.experiment or "queue").lower().replace("-", "")
                name = f"{prefix}_{ds}_{label}_s{seed}"
                cmd = [args.python, str(HERE / "run_sota.py"),
                       "--dataset", ds, *arm_args, "--seed", str(seed),
                       "--name", name]
                if args.experiment:
                    cmd += ["--experiment", args.experiment]
                jobs.append({"name": name, "cmd": cmd + args.passthrough})
    return jobs


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def main(argv=None) -> int:
    args = parse_args(argv)
    jobs = build_jobs(args)
    if args.dry_run:
        for j in jobs:
            print(subprocess.list2cmdline(j["cmd"]))
        print(f"{len(jobs)} jobs, at most {args.max_procs} at a time")
        return 0

    RESULTS_DIR.mkdir(exist_ok=True)
    pending, running, failed = list(jobs), [], []
    print(f"{stamp()}  {len(jobs)} jobs, at most {args.max_procs} at a time")
    while pending or running:
        for j in list(running):
            code = j["proc"].poll()
            if code is None:
                continue
            j["log_file"].close()
            running.remove(j)
            if code:
                failed.append(j)
            print(f"{stamp()}  {'FAILED' if code else 'done  '} {j['name']}"
                  f" (exit {code}); {len(pending)} pending,"
                  f" {len(running)} running", flush=True)
        while pending and len(running) < args.max_procs:
            j = pending.pop(0)
            # results/*.log is ignored by git: scratch, not results.
            log = RESULTS_DIR / f"{j['name']}.log"
            j["log_file"] = open(log, "w", encoding="utf-8")
            j["proc"] = subprocess.Popen(j["cmd"], stdout=j["log_file"],
                                         stderr=subprocess.STDOUT,
                                         cwd=str(HERE.parent))
            running.append(j)
            print(f"{stamp()}  start  {j['name']}  -> {log}", flush=True)
            time.sleep(STAGGER_SECONDS)
        time.sleep(5)

    print(f"{stamp()}  finished: {len(jobs) - len(failed)} ok, "
          f"{len(failed)} failed")
    for j in failed:
        print(f"  FAILED {j['name']}: see results/{j['name']}.log")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
