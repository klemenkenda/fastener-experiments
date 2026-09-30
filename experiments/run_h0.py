"""Run H0 end to end: every dataset, both arms, then the H0 report.

One command instead of six. For each dataset in H0_PLAN it runs `run_sota.py`
with the `fastener` and `fastener_2020` arms and that dataset's budget and
split (HYPOTHESES.md, H0), then reads the finished runs with
`h0_convergence.py` and writes the verdict.

While it runs it prints a status line every --interval seconds: each dataset's
units done and ETA, read from the progress.json its run writes, and an ETA for
the whole of H0. Datasets not started yet are estimated from the plan's cost
table, rescaled by how the finished datasets compared with their own
estimates, so the overall ETA sharpens as it goes. For per-seed detail on the
dataset in flight, run `python experiments/monitor.py` in another terminal.

Everything goes to results/<experiment ID>/: one log per dataset under logs/,
driver.json (the live status), and at the end h0_seeds.csv and
h0_summary.json. Each dataset's own run directory sits beside it in results/,
as usual.

Restartable: a dataset that already has a finished run under the same
experiment ID is skipped, so after an interruption the same command picks up
where it stopped. A dataset whose run is still going -- its process outlived a
driver that stopped -- is adopted: watched to the end and counted, not started
a second time.

`--plan extension` runs H0's second experiment instead: every other dataset
on disk (HYPOTHESES.md, "H0 on every other dataset"), longest first so parallel
slots finish together, analysed with datasets as the unit.

`--plan repeat` runs H0-E03 (HYPOTHESES.md, "H0 repeated"): all 36 datasets
of H0-E01 and H0-E02 again, with the fixed arm keeping the top genes and the
protocol's per-dataset budgets, analysed like H0-E02.

Usage:
    python experiments/run_h0.py --new                 # issue the next H0 ID, run all
    python experiments/run_h0.py --new --plan extension --jobs 12   # H0-E02
    python experiments/run_h0.py --new --plan repeat --jobs 12      # H0-E03
    python experiments/run_h0.py --experiment H0-E01   # run, or resume, H0-E01
    python experiments/run_h0.py --experiment H0-E01 --jobs 3
    python experiments/run_h0.py --smoke               # tiny budget, not evidence
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import experiment_ids  # noqa: E402
import h0_convergence  # noqa: E402
from protocol import FIT_BUDGET, fit_budget  # noqa: E402
from monitor import alive  # noqa: E402
from progress import format_duration  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402

HERE = Path(__file__).resolve().parent

# HYPOTHESES.md, H0: dataset, split, fit budget per run. Cheapest first, so a
# harness fault shows up in minutes rather than after the long sets.
# `hours` is the whole dataset (2 arms x 5 seeds) run alone, from the plan's
# cost table and the smoke runs. It is only a cold start for the overall ETA.
H0_PLAN = [
    {"dataset": "TOX_171", "split": "protocol", "evaluations": 6000, "hours": 0.5},
    {"dataset": "BASEHOCK", "split": "protocol", "evaluations": 6000, "hours": 0.5},
    {"dataset": "crop_mapping", "split": "eo", "evaluations": 1000, "hours": 3.0},
    {"dataset": "har", "split": "protocol", "evaluations": 6000, "hours": 4.0},
    {"dataset": "USPS", "split": "protocol", "evaluations": 6000, "hours": 4.5},
]

# HYPOTHESES.md, "H0 on every other dataset" (H0-E02): every dataset on disk
# except H0-E01's five. Earth-observation sets get the paper's EO budget of
# 1,000 fits; eodata also the EO split, satimage (6,430 rows) the protocol
# split. `hours` is a rough whole-dataset estimate (10 runs, alone) from the
# measured fit costs; ordered longest first so parallel slots finish together.
def _ext(dataset, group, hours, split="protocol", evaluations=6000):
    return {"dataset": dataset, "group": group, "hours": hours,
            "split": split, "evaluations": evaluations}


H0_EXTENSION_PLAN = sorted([
    _ext("eodata", "Earth observation", 3.0, split="eo", evaluations=1000),
    _ext("satimage", "Earth observation", 0.3, evaluations=1000),
    _ext("miniboone", "tall", 12.0),
    _ext("higgs", "tall", 10.0),
    _ext("volkert", "tall", 8.0),
    _ext("covertype", "tall", 3.5),
    _ext("gas_drift", "tall", 1.8),
    _ext("madelon", "challenge", 0.5),
    _ext("gina", "challenge", 0.5),
    _ext("gisette", "handwriting and speech", 1.0),
    _ext("Isolet", "handwriting and speech", 0.5),
    _ext("arcene", "mass spectrometry", 0.6),
    _ext("RELATHE", "text", 0.5),
    _ext("PCMAC", "text", 0.5),
    _ext("orlraws10P", "face and object images", 0.6),
    _ext("warpAR10P", "face and object images", 0.4),
    _ext("Yale", "face and object images", 0.4),
    _ext("warpPIE10P", "face and object images", 0.4),
    _ext("ORL", "face and object images", 0.5),
    _ext("COIL20", "face and object images", 0.5),
    _ext("GLIOMA", "gene expression", 0.4),
    _ext("nci9", "gene expression", 0.6),
    _ext("colon", "gene expression", 0.4),
    _ext("ALLAML", "gene expression", 0.5),
    _ext("leukemia", "gene expression", 0.5),
    _ext("lung_discrete", "gene expression", 0.3),
    _ext("GLI_85", "gene expression", 0.8),
    _ext("lymphoma", "gene expression", 0.4),
    _ext("Prostate_GE", "gene expression", 0.5),
    _ext("CLL_SUB_111", "gene expression", 0.6),
    _ext("lung", "gene expression", 0.4),
], key=lambda p: -p["hours"])

# HYPOTHESES.md, "H0 repeated" (H0-E03): every dataset of H0-E01 and H0-E02.
# The EO budgets stay at 1,000; every dataset that had 6,000 gets
# protocol.fit_budget, which doubles it where the search had not converged.
H0_CORE_GROUPS = {"TOX_171": "gene expression", "BASEHOCK": "text",
                  "crop_mapping": "Earth observation", "har": "sensor signals",
                  "USPS": "handwriting and speech"}


def _repeat(p):
    ev = p["evaluations"]
    if ev == FIT_BUDGET:
        ev = fit_budget(p["dataset"])
    return {**p, "group": p.get("group", H0_CORE_GROUPS.get(p["dataset"])),
            "evaluations": ev, "hours": p["hours"] * ev / p["evaluations"]}


H0_REPEAT_PLAN = sorted([_repeat(p) for p in H0_PLAN + H0_EXTENSION_PLAN],
                        key=lambda p: -p["hours"])
# At most this many of the 36 may lack a complete result: the same one in five
# that H0-E02 allowed (6 of 31).
REPEAT_MAX_MISSING = 7
PLANS = {"core": H0_PLAN, "extension": H0_EXTENSION_PLAN,
         "repeat": H0_REPEAT_PLAN}
ARMS = ("none", "2020")
SMOKE_EVALUATIONS = 300  # run_sota.py --quick
SMOKE_SEEDS = 2


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--experiment", metavar="ID",
                     help="an issued H0 experiment ID, e.g. H0-E01")
    who.add_argument("--new", action="store_true",
                     help="issue the next H0 experiment ID and run under it")
    who.add_argument("--smoke", action="store_true",
                     help=f"{SMOKE_EVALUATIONS} fits, {SMOKE_SEEDS} seeds, no "
                          f"experiment ID: checks the pipeline, is not evidence")
    ap.add_argument("--plan", default="core", choices=sorted(PLANS),
                    help="core: H0's five datasets (H0-E01). extension: every "
                         "other dataset (H0-E02). repeat: all 36 again with "
                         "the current fixed arm (H0-E03).")
    ap.add_argument("--datasets", default=None,
                    help="comma-separated subset of the plan's datasets")
    ap.add_argument("--jobs", type=int, default=1,
                    help="datasets run at the same time (default 1). More "
                         "finishes sooner, but the runs then compete for the "
                         "CPU, so wall clock -- a secondary H0 measure -- is "
                         "no longer comparable between arms. Fits are "
                         "unaffected.")
    ap.add_argument("--interval", type=float, default=60.0,
                    help="seconds between status lines (default 60)")
    ap.add_argument("--allow-dirty", action="store_true",
                    help="pass --allow-dirty to run_sota.py: runs from "
                         "uncommitted code, which cannot be cited as evidence")
    return ap.parse_args()


# ------------------------------------------------------------------- helpers
def finished_runs(experiment_id: str) -> Dict[str, Path]:
    """Dataset -> run directory, for runs of this experiment that finished."""
    done = {}
    for manifest in sorted(RESULTS_DIR.glob("*/manifest.json")):
        try:
            m = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (m.get("experiment_id") == experiment_id
                and m.get("status") == "ok"
                and set(m.get("params", {}).get("fastener_arms", [])) >= set(ARMS)):
            done[m["params"]["dataset"]] = manifest.parent
    return done


def read_json(path: Path) -> Optional[Dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def run_dir_from_log(log: Path) -> Optional[Path]:
    """run_sota.py prints 'run dir: <path>' once its run directory exists."""
    try:
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("run dir: "):
                return Path(line[len("run dir: "):].strip())
    except OSError:
        pass
    return None


def makespan(remaining: List[float], queued: List[float], jobs: int) -> float:
    """Seconds until everything is done: running jobs keep their slots, queued
    work goes to whichever slot frees first."""
    slots = sorted(remaining + [0.0] * max(0, jobs - len(remaining)))[:max(jobs, 1)]
    for q in queued:
        slots.sort()
        slots[0] += q
    return max(slots) if slots else 0.0


def clock(seconds: float) -> str:
    t = datetime.now() + timedelta(seconds=seconds)
    return t.strftime("%a %H:%M")


# -------------------------------------------------------------------- driver
class Job:
    def __init__(self, plan: Dict, out: Path, experiment: Optional[str],
                 smoke: bool, allow_dirty: bool) -> None:
        self.plan = plan
        self.name = plan["dataset"]
        self.log = out / "logs" / f"{self.name}.log"
        self.proc: Optional[subprocess.Popen] = None
        self.run_dir: Optional[Path] = None
        self.state = "pending"  # pending, running, done, failed, skipped
        self.t0 = self.t1 = None
        # Set for a run adopted from an earlier driver: watched by its pid,
        # since this driver did not start it.
        self.pid: Optional[int] = None
        cmd = [sys.executable, "-u", str(HERE / "run_sota.py"),
               "--dataset", self.name, "--split", plan["split"],
               "--methods", "", "--name", f"h0_{self.name}"]
        for arm in ARMS:
            cmd += ["--fastener-arm", arm]
        if smoke:
            cmd += ["--quick"]
        else:
            cmd += ["--evaluations", str(plan["evaluations"]),
                    "--experiment", experiment]
        if allow_dirty:
            cmd += ["--allow-dirty"]
        self.cmd = cmd

    def start(self) -> None:
        self.log.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.log, "w", encoding="utf-8")
        # One thread per run: several runs share the machine, and a numerical
        # library spreading one run over every core only makes them fight.
        env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONIOENCODING": "utf-8",
               "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
               "OPENBLAS_NUM_THREADS": "1"}
        self.proc = subprocess.Popen(self.cmd, stdout=self._fh,
                                     stderr=subprocess.STDOUT, env=env,
                                     cwd=str(HERE.parent))
        self.state, self.t0 = "running", time.time()

    def adopt(self, run_dir: Path, pid: int, elapsed: float) -> None:
        """Take over watching a run an earlier driver started."""
        self.run_dir, self.pid = run_dir, pid
        self.state, self.t0 = "running", time.time() - elapsed

    def poll(self) -> None:
        if self.run_dir is None:
            self.run_dir = run_dir_from_log(self.log)
        if self.state == "running" and self.proc is None:
            if not alive(self.pid):
                # run_sota.py writes its manifest last, so "ok" there means
                # the run finished rather than died.
                m = read_json(self.run_dir / "manifest.json")
                self.t1 = time.time()
                self.state = "done" if m and m.get("status") == "ok" else "failed"
            return
        if self.state == "running" and self.proc.poll() is not None:
            self._fh.close()
            self.t1 = time.time()
            self.state = "done" if self.proc.returncode == 0 else "failed"

    def elapsed(self) -> float:
        if self.t0 is None:
            return 0.0
        return (self.t1 or time.time()) - self.t0

    def progress(self) -> Optional[Dict]:
        return read_json(self.run_dir / "progress.json") if self.run_dir else None


class Driver:
    def __init__(self, jobs: List[Job], out: Path, n_jobs: int,
                 interval: float, label: str, smoke: bool = False) -> None:
        self.jobs, self.out, self.n_jobs = jobs, out, max(1, n_jobs)
        self.interval, self.label, self.smoke = interval, label, smoke
        self.t0 = time.time()

    def calibration(self) -> float:
        """Actual over estimated time, from the datasets finished here."""
        fin = [j for j in self.jobs if j.state == "done" and j.t1]
        est = sum(j.plan["hours"] * 3600 for j in fin)
        return sum(j.elapsed() for j in fin) / est if est else 1.0

    def remaining(self, j: Job, scale: float) -> float:
        p = j.progress()
        if p and p.get("eta_seconds") is not None and p.get("units_done", 0) > 0:
            return float(p["eta_seconds"])
        # Nothing finished inside the run yet: its own ETA is still a prior.
        return max(j.plan["hours"] * 3600 * scale - j.elapsed(), 60.0)

    def status(self) -> Dict:
        scale = self.calibration()
        running = [j for j in self.jobs if j.state == "running"]
        pending = [j for j in self.jobs if j.state == "pending"]
        eta = makespan([self.remaining(j, scale) for j in running],
                       [j.plan["hours"] * 3600 * scale for j in pending],
                       self.n_jobs)
        rows = []
        for j in self.jobs:
            row = {"dataset": j.name, "state": j.state,
                   "elapsed_seconds": round(j.elapsed(), 1),
                   "run_dir": str(j.run_dir) if j.run_dir else None,
                   "log": str(j.log)}
            p = j.progress() if j.state == "running" else None
            if p:
                cur = p.get("current") or {}
                row.update(units_done=p.get("units_done"),
                           units_total=p.get("units_total"),
                           current=f"{cur.get('method')} seed {cur.get('seed')} "
                                   f"{cur.get('fits_done', 0)}/{cur.get('budget_fits')} fits"
                           if cur else None,
                           eta_seconds=round(self.remaining(j, scale), 1))
            rows.append(row)
        return {"label": self.label, "elapsed_seconds": round(time.time() - self.t0, 1),
                "eta_seconds": round(eta, 1), "calibration": round(scale, 3),
                "datasets": rows,
                "updated_utc": datetime.now(timezone.utc).isoformat()}

    def print_status(self, st: Dict) -> None:
        parts = []
        for r in st["datasets"]:
            if r["state"] == "running":
                units = (f"{r.get('units_done', 0)}/{r.get('units_total', '?')} units"
                         if r.get("units_total") else "starting")
                cur = f", {r['current']}" if r.get("current") else ""
                eta = format_duration(r.get("eta_seconds"))
                parts.append(f"{r['dataset']}: {units}{cur}, ~{eta} left")
            elif r["state"] in ("done", "failed", "skipped"):
                parts.append(f"{r['dataset']}: {r['state']}"
                             + (f" in {format_duration(r['elapsed_seconds'])}"
                                if r["state"] != "skipped" else ""))
        pend = [r["dataset"] for r in st["datasets"] if r["state"] == "pending"]
        if pend:
            parts.append("waiting: " + ", ".join(pend))
        eta = st["eta_seconds"]
        print(f"[{format_duration(st['elapsed_seconds'])}] "
              + " | ".join(parts)
              + f"\n    H0: ~{format_duration(eta)} left, done around "
                f"{clock(eta)}", flush=True)

    def write_status(self, st: Dict) -> None:
        tmp = self.out / "driver.json.tmp"
        tmp.write_text(json.dumps(st, indent=2), encoding="utf-8")
        # On Windows the replace is refused while a reader (monitor.py) has
        # driver.json open. Retry briefly, then skip this update: the status
        # file is for watching, and must never stop the experiment.
        for _ in range(20):
            try:
                os.replace(tmp, self.out / "driver.json")
                return
            except PermissionError:
                time.sleep(0.1)

    def run(self) -> None:
        last_print = 0.0
        try:
            while True:
                for j in self.jobs:
                    if j.state != "running":
                        continue
                    j.poll()
                    if j.state != "running":
                        print(f"{j.name}: {j.state} after "
                              f"{format_duration(j.elapsed())}"
                              + ("" if j.state == "done"
                                 else f" -- see {j.log}"), flush=True)
                        last_print = 0.0
                running = sum(j.state == "running" for j in self.jobs)
                for j in self.jobs:
                    if running >= self.n_jobs:
                        break
                    if j.state == "pending":
                        j.start()
                        running += 1
                        fits = (SMOKE_EVALUATIONS if self.smoke
                                else j.plan["evaluations"])
                        print(f"{j.name}: started ({fits} fits per run, "
                              f"split {j.plan['split']}), log {j.log}",
                              flush=True)
                        last_print = 0.0
                for j in self.jobs:
                    if j.state == "running":
                        j.poll()
                st = self.status()
                self.write_status(st)
                if not any(j.state in ("running", "pending") for j in self.jobs):
                    break
                if time.time() - last_print >= self.interval:
                    self.print_status(st)
                    last_print = time.time()
                time.sleep(2.0)
        except KeyboardInterrupt:
            for j in self.jobs:
                if (j.state == "running" and j.proc is not None
                        and j.proc.poll() is None):
                    j.proc.terminate()
            print("\ninterrupted: running datasets stopped. Run the same "
                  "command again to resume; finished datasets are skipped.")
            raise SystemExit(130)


def main() -> int:
    args = parse_args()

    full_plan = PLANS[args.plan]
    plan = full_plan
    if args.datasets:
        wanted = [d.strip() for d in args.datasets.split(",") if d.strip()]
        unknown = set(wanted) - {p["dataset"] for p in full_plan}
        if unknown:
            raise SystemExit(f"not an H0 dataset: {sorted(unknown)}")
        plan = [p for p in full_plan if p["dataset"] in wanted]

    if args.smoke:
        experiment = None
        label = "h0_smoke_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        plan = [{**p, "hours": p["hours"] * SMOKE_EVALUATIONS * SMOKE_SEEDS
                 / (p["evaluations"] * 5)} for p in plan]
    else:
        if args.new:
            experiment = experiment_ids.issue("H0")
            print(f"issued {experiment}")
        else:
            experiment = args.experiment
            if experiment_ids.parse_experiment_id(experiment)["group"] != "H0":
                raise SystemExit(f"{experiment} is not an H0 experiment ID")
        label = experiment
    out = RESULTS_DIR / label

    jobs = [Job(p, out, experiment, args.smoke, args.allow_dirty) for p in plan]
    previous = finished_runs(experiment) if experiment else {}
    for j in jobs:
        if j.name in previous:
            j.state, j.run_dir = "skipped", previous[j.name]
            print(f"{j.name}: already finished in {j.run_dir.name}, skipped")
        elif experiment and j.log.is_file():
            run_dir = run_dir_from_log(j.log)
            p = read_json(run_dir / "progress.json") if run_dir else None
            if p and p.get("status") == "running" and alive(p.get("pid")):
                j.adopt(run_dir, int(p["pid"]), p.get("elapsed_seconds") or 0.0)
                print(f"{j.name}: still running in {run_dir.name} "
                      f"(pid {j.pid}), adopted")

    out.mkdir(parents=True, exist_ok=True)
    todo = [j for j in jobs if j.state in ("pending", "running")]
    print(f"H0 {label}: {len(todo)} dataset(s) to run, {args.jobs} at a time; "
          f"status every {format_duration(args.interval)}; output in {out}")
    driver = Driver(jobs, out, args.jobs, args.interval, label, args.smoke)
    driver.run()

    failed = [j.name for j in jobs if j.state == "failed"]
    run_dirs = [j.run_dir for j in jobs
                if j.state in ("done", "skipped") and j.run_dir]
    print(f"\nall datasets finished in {format_duration(time.time() - driver.t0)}"
          + (f"; FAILED: {', '.join(failed)}" if failed else ""))

    if run_dirs and args.plan in ("extension", "repeat"):
        # H0-E01's runs feed only H0-E02's secondary test over all datasets;
        # H0-E03 covers all of them itself.
        extension = args.plan == "extension"
        e01 = list(finished_runs("H0-E01").values()) if extension else []
        summary = h0_convergence.extension_summary(
            run_dirs, expected=[p["dataset"] for p in plan],
            groups={p["dataset"]: p["group"] for p in plan},
            earlier_run_dirs=e01,
            max_missing=(h0_convergence.EXTENSION_MAX_MISSING if extension
                         else REPEAT_MAX_MISSING))
        print()
        h0_convergence.print_extension(summary)
        h0_convergence.write_extension_outputs(summary, out, run_dirs)
        print(f"\nwrote {out / 'h0_seeds.csv'} and h0_extension_summary.json")
    elif run_dirs:
        summary = h0_convergence.summarise(run_dirs)
        if summary["per_seed"]:
            print()
            h0_convergence.print_summary(summary)
            h0_convergence.write_outputs(summary, out, run_dirs)
            print(f"\nwrote {out / 'h0_seeds.csv'} and h0_summary.json")
    if args.smoke:
        print("\nsmoke run: tiny budget and no experiment ID, so none of this "
              "is evidence.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
