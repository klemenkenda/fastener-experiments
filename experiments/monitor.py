"""Watch a running experiment: live progress, per-method rates and ETA.

Reads the `progress.json` heartbeat that run_sota.py writes. It is a separate
process that only ever reads, so attaching or killing the monitor cannot affect
the run it is watching.

Usage:
    python experiments/monitor.py                 # newest run, live
    python experiments/monitor.py --once          # print once and exit
    python experiments/monitor.py --run 20260916T130739Z_madelon_sota
    python experiments/monitor.py --interval 5
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

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
            h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
            if not h:
                return False
            ctypes.windll.kernel32.CloseHandle(h)
            return True
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None,
                    help="run id or substring; default is the newest")
    ap.add_argument("--interval", type=float, default=3.0)
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()

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
