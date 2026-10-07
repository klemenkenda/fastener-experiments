"""Watch a running experiment: live progress, per-method rates and ETA.

Reads the `progress.json` heartbeat that run_sota.py writes. It is a separate
process that only ever reads, so attaching or killing the monitor cannot affect
the run it is watching.

Usage:
    python experiments/monitor.py                 # newest run, live
    python experiments/monitor.py --once          # print once and exit
    python experiments/monitor.py --run 20260916T130739Z_madelon_sota
    python experiments/monitor.py --interval 5
    python experiments/monitor.py --experiment H0-E03   # every dataset of a
                                                        # run_h0.py experiment
    python experiments/monitor.py --experiment H1-E01   # every job of a
                                                        # run_queue.py experiment

`--experiment` shows one line per dataset of a run_h0.py experiment: its
state, progress across both arms, each seed of each arm, the unit in flight,
and its ETA; above them, the whole experiment's ETA. It reads the driver's
results/<ID>/driver.json and each dataset's own progress.json.

For an experiment started by run_queue.py it reads results/<ID>/queue.json
instead, and shows one line per dataset and arm: progress over its seeds, each
seed's state, the fits of the seeds in flight, and their time left. The
experiment's ETA plays the remaining jobs over the queue's free processes.
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from progress import format_duration  # noqa: E402
from provenance import RESULTS_DIR  # noqa: E402

BAR_WIDTH = 28
STATE_MARK = {"done": "+", "running": ">", "pending": ".", "failed": "x"}


def find_run(run: Optional[str]) -> Optional[Path]:
    if run:
        d = RESULTS_DIR / run
        if not d.is_dir():
            matches = sorted(RESULTS_DIR.glob(f"*{run}*"))
            if not matches:
                return None
            d = matches[-1]
        return d / "progress.json"

    candidates = sorted(RESULTS_DIR.glob("*/progress.json"),
                        key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None


def read(path: Path) -> Optional[Dict]:
    # The writer replaces this file atomically, but a reader can still catch the
    # moment between unlink and rename on Windows, so treat any failure as
    # "nothing new yet" and retry on the next tick.
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def bar(fraction: float, width: int = BAR_WIDTH) -> str:
    fraction = max(0.0, min(1.0, fraction))
    filled = int(round(fraction * width))
    return "[" + "#" * filled + "-" * (width - filled) + f"] {fraction*100:5.1f}%"


def alive(pid: Optional[int]) -> Optional[bool]:
    """Best-effort liveness check, so a crashed run is not shown as running."""
    if pid is None:
        return None
    try:
        if os.name == "nt":
            import ctypes
            k32 = ctypes.windll.kernel32
            h = k32.OpenProcess(0x1000, False, int(pid))
            if not h:
                return False
            # An exited process can still be opened while anyone holds a
            # handle to it; only STILL_ACTIVE (259) means it is running.
            code = ctypes.c_ulong()
            ok = k32.GetExitCodeProcess(h, ctypes.byref(code))
            k32.CloseHandle(h)
            return bool(ok) and code.value == 259
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, AttributeError):
        return False


def render(snap: Dict, path: Path) -> List[str]:
    out: List[str] = []
    meta = snap.get("meta", {})
    status = snap.get("status", "?")
    running = status == "running"
    live = alive(snap.get("pid")) if running else None

    head = f"  {snap.get('run_id', path.parent.name)}"
    out.append("")
    out.append(head)
    bits = [f"status={status}"]
    if meta.get("dataset"):
        bits.append(f"dataset={meta['dataset']}")
    if running and live is False:
        bits.append("PROCESS GONE (stale heartbeat)")
    out.append("  " + "   ".join(bits))

    # Staleness matters more than the timestamp itself: a heartbeat that stopped
    # updating is the main signal that something wedged.
    try:
        upd = datetime.fromisoformat(snap["updated_utc"])
        age = (datetime.now(timezone.utc) - upd).total_seconds()
        if running and age > 120:
            out.append(f"  last update {format_duration(age)} ago -- possibly stalled")
    except (KeyError, ValueError):
        pass

    out.append("")
    out.append("  overall  " + bar(snap.get("fraction_done", 0.0)) +
               f"  {snap.get('units_done', 0)}/{snap.get('units_total', 0)} units")
    elapsed = snap.get("elapsed_seconds")
    eta = snap.get("eta_seconds")
    line = f"  elapsed  {format_duration(elapsed)}"
    if running:
        line += f"   eta {format_duration(eta)}"
        if eta is not None:
            finish = time.time() + eta
            line += f"   finishes ~{time.strftime('%H:%M', time.localtime(finish))}"
        line += f"   total ~{format_duration((elapsed or 0) + (eta or 0))}"
    out.append(line)

    cur = snap.get("current")
    if cur:
        label = cur["method"] + (f" seed {cur['seed']}" if cur.get("seed") is not None else "")
        out.append("")
        out.append(f"  current  {label}")
        if cur.get("budget_fits"):
            out.append("           " + bar(cur.get("fraction", 0.0)) +
                       f"  {cur.get('fits_done', 0)}/{cur['budget_fits']} fits")
        out.append(f"           running {format_duration(cur.get('elapsed_seconds'))}")

    out.append("")
    out.append(f"  {'unit':<22}{'state':<9}{'fits':>8}{'time':>9}{'s/fit':>9}")
    out.append("  " + "-" * 57)
    rates = snap.get("seconds_per_fit", {})
    for u in snap.get("units", []):
        mark = STATE_MARK.get(u["state"], "?")
        fits = u.get("fits")
        secs = u.get("seconds")
        rate = f"{secs/fits:.3f}" if (fits and secs) else ""
        out.append(f"  {mark} {u['unit_id']:<20}{u['state']:<9}"
                   f"{(fits if fits else ''):>8}"
                   f"{(format_duration(secs) if secs else ''):>9}{rate:>9}")
        if u.get("error"):
            out.append(f"      ! {u['error'][:70]}")

    if rates:
        out.append("")
        out.append("  learned rates: " +
                   "  ".join(f"{m}={v:.3f}s/fit" for m, v in sorted(rates.items())))
    if snap.get("error"):
        out.append(f"\n  ERROR: {snap['error']}")
    out.append("")
    return out


# ------------------------------------------------ one line per dataset
EXPERIMENT_BAR = 16
ARM_SHORT = {"fastener": "fixed", "fastener_2020": "2020"}
SEED_MARK = {"done": "+", "running": ">", "pending": ".", "failed": "x"}
STATE_ORDER = {"running": 0, "failed": 1, "pending": 2, "done": 3, "skipped": 3}
# The driver rewrites driver.json every --interval (60 s by default).
DRIVER_STALE_SECONDS = 300


def age_seconds(stamp: Optional[str]) -> Optional[float]:
    try:
        return (datetime.now(timezone.utc)
                - datetime.fromisoformat(stamp)).total_seconds()
    except (TypeError, ValueError):
        return None


def run_fraction(p: Dict) -> float:
    """Share of the run's fits done: finished units plus the one in flight."""
    total = p.get("units_total") or 0
    if not total:
        return 0.0
    cur = p.get("current") or {}
    return min(1.0, (p.get("units_done", 0) + (cur.get("fraction") or 0.0)) / total)


def seed_marks(p: Dict) -> str:
    arms: Dict[str, str] = {}
    for u in p.get("units", []):
        arms.setdefault(u.get("method"), "")
        arms[u.get("method")] += SEED_MARK.get(u.get("state"), "?")
    return "  ".join(f"{ARM_SHORT.get(m, m)} {s}" for m, s in arms.items())


def dataset_line(row: Dict, p: Optional[Dict]) -> str:
    # "skipped" is the driver's word for a dataset that finished before it
    # was (re)started: to the reader it is done.
    state = "done" if row.get("state") == "skipped" else row.get("state", "?")
    name = row["dataset"]
    mark = STATE_MARK.get(state, "?")
    if state == "pending":
        return f"  {mark} {name:<14}waiting"
    if p is None:
        what = "starting" if state == "running" else state
        return (f"  {mark} {name:<14}{what:<9}"
                f"{format_duration(row.get('elapsed_seconds')):>8}")
    frac = 1.0 if state == "done" else run_fraction(p)
    filled = int(round(frac * EXPERIMENT_BAR))
    line = (f"  {mark} {name:<14}[{'#' * filled}{'-' * (EXPERIMENT_BAR - filled)}]"
            f"{frac * 100:4.0f}%  {seed_marks(p):<25}")
    if state == "running":
        cur = p.get("current") or {}
        if cur:
            what = (f"{ARM_SHORT.get(cur.get('method'), cur.get('method'))}"
                    f" s{cur.get('seed')} {cur.get('fits_done', 0):>5}/"
                    f"{cur.get('budget_fits')}")
            line += what.ljust(24)
        else:
            line += " " * 24
        line += f"{format_duration(p.get('elapsed_seconds')):>8}"
        eta = (p.get("eta_seconds") if p.get("units_done", 0) > 0
               else row.get("eta_seconds"))
        line += f"  ~{format_duration(eta)} left" if eta is not None else ""
        if alive(p.get("pid")) is False:
            line += "  PROCESS GONE"
        elif (age_seconds(p.get("updated_utc")) or 0) > 300:
            line += "  no update for " + format_duration(
                age_seconds(p.get("updated_utc")))
    else:
        # The run's own clock: a driver that did not start it cannot time it.
        secs = p.get("elapsed_seconds") or row.get("elapsed_seconds")
        line += f"{'':<24}{format_duration(secs):>8}"
    if state == "failed":
        line += f"  see {row.get('log')}"
    return line


def render_experiment(driver: Dict, experiment: str) -> List[str]:
    rows = driver.get("datasets", [])
    counts: Dict[str, int] = {}
    for r in rows:
        s = "done" if r["state"] == "skipped" else r["state"]
        counts[s] = counts.get(s, 0) + 1
    out = ["", f"  {experiment}   {len(rows)} datasets   " + "   ".join(
        f"{s} {counts[s]}" for s in ("running", "done", "failed", "pending")
        if counts.get(s))]
    active = bool(counts.get("running") or counts.get("pending"))
    # Between driver updates, count the clock on while anything is left.
    since = (age_seconds(driver.get("updated_utc")) or 0.0) if active else 0.0
    elapsed = (driver.get("elapsed_seconds") or 0.0) + since
    eta = max(0.0, (driver.get("eta_seconds") or 0.0) - since)
    line = f"  elapsed {format_duration(elapsed)}"
    if active:
        finish = time.localtime(time.time() + eta)
        line += (f"   ~{format_duration(eta)} left, done around "
                 f"{time.strftime('%a %H:%M', finish)}")
    out.append(line)
    if active and since > DRIVER_STALE_SECONDS:
        out.append(f"  driver.json not updated for {format_duration(since)}"
                   " -- is run_h0.py still running?")
    out.append("")
    out.append(f"    {'dataset':<14}{'progress':<25}{'seeds: + done > running':<25}"
               f"{'in flight':<24}{'elapsed':>8}")
    ordered = sorted(rows, key=lambda r: STATE_ORDER.get(r["state"], 9))
    for r in ordered:
        p = read(Path(r["run_dir"]) / "progress.json") if r.get("run_dir") else None
        out.append(dataset_line(r, p))
    out.append("")
    return out


# ------------------------------------------- one line per dataset and arm
def job_remaining(j: Dict, p: Optional[Dict]) -> Optional[float]:
    """Seconds a running job still needs, from its own heartbeat."""
    if p is None:
        return None
    if p.get("units_done", 0) > 0 and p.get("eta_seconds") is not None:
        return float(p["eta_seconds"])
    frac = run_fraction(p)
    elapsed = age_seconds(j.get("started_utc"))
    # Below 2% the extrapolation is mostly start-up cost.
    if frac < 0.02 or not elapsed:
        return None
    return elapsed * (1 - frac) / frac


def queue_eta(jobs: List[Dict], snaps: Dict[str, Optional[Dict]],
              slots: int) -> Tuple[Optional[float], bool]:
    """Seconds until the queue is empty, and whether that is only a floor.

    The running jobs hold their slots for their own remaining time; each
    pending job, in queue order, takes the first slot to free up, for as long
    as the finished or running jobs of its dataset and arm took or will take.
    A pending job with nothing to go on yet counts as zero, so the result is
    then a lower bound.
    """
    durations: Dict[Tuple[str, str], List[float]] = {}
    for j in jobs:
        key = (j["dataset"], j["arm"])
        if j["state"] == "done":
            start, end = j.get("started_utc"), j.get("ended_utc")
            try:
                d = (datetime.fromisoformat(end)
                     - datetime.fromisoformat(start)).total_seconds()
                durations.setdefault(key, []).append(d)
            except (TypeError, ValueError):
                pass
        elif j["state"] == "running":
            rem = job_remaining(j, snaps.get(j["name"]))
            elapsed = age_seconds(j.get("started_utc"))
            if rem is not None and elapsed is not None:
                durations.setdefault(key, []).append(elapsed + rem)

    free, floor = [], False
    for j in jobs:
        if j["state"] == "running":
            rem = job_remaining(j, snaps.get(j["name"]))
            if rem is None:
                floor = True
            free.append(rem or 0.0)
    free += [0.0] * max(0, slots - len(free))
    free.sort()
    for j in jobs:
        if j["state"] != "pending":
            continue
        known = durations.get((j["dataset"], j["arm"]))
        if not known:
            floor = True
        t = free.pop(0) + (sum(known) / len(known) if known else 0.0)
        free.append(t)
        free.sort()
    return (max(free) if free else 0.0), floor


def group_line(jobs: List[Dict], snaps: Dict[str, Optional[Dict]]) -> str:
    states = [j["state"] for j in jobs]
    if "running" in states:
        state = "running"
    elif "failed" in states:
        state = "failed"
    elif all(s == "done" for s in states):
        state = "done"
    else:
        state = "pending"
    fracs = []
    for j in jobs:
        if j["state"] == "done":
            fracs.append(1.0)
        elif j["state"] == "running" and snaps.get(j["name"]):
            fracs.append(run_fraction(snaps[j["name"]]))
        else:
            fracs.append(0.0)
    frac = sum(fracs) / len(fracs)
    filled = int(round(frac * EXPERIMENT_BAR))
    seeds = "".join(SEED_MARK.get(s, "?") for s in states)
    line = (f"  {STATE_MARK.get(state, '?')} {jobs[0]['dataset']:<13}"
            f"{jobs[0]['arm']:<14}[{'#' * filled}{'-' * (EXPERIMENT_BAR - filled)}]"
            f"{frac * 100:4.0f}%  {seeds:<7}")
    running = [j for j in jobs if j["state"] == "running"]
    if running:
        fits = [(snaps.get(j["name"]) or {}).get("current") or {}
                for j in running]
        done = [c.get("fits_done", 0) for c in fits]
        budget = next((c.get("budget_fits") for c in fits
                       if c.get("budget_fits")), None)
        span = f"{min(done)}" if min(done) == max(done) \
            else f"{min(done)}-{max(done)}"
        line += f"{span:>11}/{budget or '?':<6}"
        rems = [job_remaining(j, snaps.get(j["name"])) for j in running]
        rems = [r for r in rems if r is not None]
        if rems:
            line += f"  ~{format_duration(max(rems))} left"
        gone = [j for j in running if snaps.get(j["name"])
                and alive(snaps[j["name"]].get("pid")) is False]
        if gone:
            line += f"  PROCESS GONE: s{', s'.join(str(j['seed']) for j in gone)}"
    failed = [j for j in jobs if j["state"] == "failed"]
    if failed:
        line += "  failed: " + ", ".join(
            f"s{j['seed']} ({Path(j['log']).name})" for j in failed)
    return line


def render_queue(queue: Dict, experiment: str) -> List[str]:
    jobs = queue.get("jobs", [])
    snaps = {j["name"]: read(Path(j["run_dir"]) / "progress.json")
             if j.get("run_dir") else None for j in jobs}
    counts: Dict[str, int] = {}
    for j in jobs:
        counts[j["state"]] = counts.get(j["state"], 0) + 1
    slots = queue.get("max_procs") or 1
    out = ["", f"  {experiment}   {len(jobs)} jobs on {slots} processes   "
           + "   ".join(f"{s} {counts[s]}"
                        for s in ("running", "done", "failed", "pending")
                        if counts.get(s))]
    active = bool(counts.get("running") or counts.get("pending"))
    line = f"  elapsed {format_duration(age_seconds(queue.get('started_utc')))}"
    if active:
        eta, floor = queue_eta(jobs, snaps, slots)
        finish = time.localtime(time.time() + eta)
        line += (f"   {'at least ' if floor else '~'}{format_duration(eta)}"
                 f" left, done around {time.strftime('%a %H:%M', finish)}")
    out.append(line)
    if active and alive(queue.get("pid")) is False:
        out.append("  run_queue.py is no longer running -- pending jobs will"
                   " not start")
    out.append("")
    out.append(f"    {'dataset':<13}{'arm':<14}{'progress':<25}{'seeds':<7}"
               f"{'fits in flight':>18}")
    groups: Dict[Tuple[str, str], List[Dict]] = {}
    for j in jobs:
        groups.setdefault((j["dataset"], j["arm"]), []).append(j)
    for g in groups.values():
        out.append(group_line(g, snaps))
    out.append("")
    out.append("  seeds: + done  > running  . pending  x failed")
    out.append("")
    return out


def watch_experiment(experiment: str, interval: float, once: bool) -> int:
    # run_queue.py writes queue.json, run_h0.py driver.json.
    queue_path = RESULTS_DIR / experiment / "queue.json"
    path = RESULTS_DIR / experiment / "driver.json"
    last = ""
    while True:
        queue = read(queue_path)
        driver = None if queue is not None else read(path)
        if queue is not None:
            text = "\n".join(render_queue(queue, experiment))
        elif driver is None:
            if once:
                print(f"neither {queue_path.name} nor {path.name} found in "
                      f"{path.parent}: has {experiment} started?")
                return 1
            text = f"waiting for {queue_path} ..."
        else:
            text = "\n".join(render_experiment(driver, experiment))
        if once:
            print(text)
            return 0
        if text != last:
            os.system("cls" if os.name == "nt" else "clear")
            print(text)
            last = text
        if queue is not None and all(
                j["state"] in ("done", "failed")
                for j in queue.get("jobs", [])):
            return 0
        if driver is not None and all(
                r["state"] in ("done", "failed", "skipped")
                for r in driver.get("datasets", [])):
            return 0
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None,
                    help="run id or substring; default is the newest")
    ap.add_argument("--interval", type=float, default=3.0)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--experiment", default=None, metavar="ID",
                    help="show every dataset of a run_h0.py experiment "
                         "(e.g. H0-E03) or every job of a run_queue.py one "
                         "(e.g. H1-E01)")
    args = ap.parse_args()
    if args.experiment:
        return watch_experiment(args.experiment, max(args.interval, 5.0),
                                args.once)

    path = find_run(args.run)
    if path is None:
        print("no run with a progress.json found under results/")
        return 1
    print(f"watching {path}")

    last = ""
    while True:
        snap = read(path)
        if snap is not None:
            text = "\n".join(render(snap, path))
            if args.once:
                print(text)
                return 0
            if text != last:
                # Clear and repaint only on change, so the display does not
                # flicker while a long unit is in flight.
                os.system("cls" if os.name == "nt" else "clear")
                print(f"watching {path}")
                print(text)
                last = text
            if snap.get("status") != "running":
                return 0
        elif args.once:
            print("progress.json not readable yet")
            return 1
        try:
            time.sleep(args.interval)
        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
