"""Watch OpenRouter spending and an LLM experiment's progress, refreshed.

Shows what experiment processes run on this machine and which H12-E01
(dataset, model) pairs are in flight, the key's usage as OpenRouter reports it (today, this week, this
month, all time, and the limit), what the project's call logs have spent
(the $50 limit on model calls is counted over these), and H12-E01's progress.
Reads only: it sends no model call.

    python experiments/usage_watch.py            # refresh every 30 s, Ctrl+C stops
    python experiments/usage_watch.py --once
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import llm_guidance as lg

HERE = Path(__file__).resolve().parent
LOGS = {"H8 priors": HERE / "priors" / "calls.jsonl",
        "H12-E01": HERE / "h12" / "calls.jsonl"}
LIMIT = 50.0


def key_usage() -> dict:
    key = os.environ.get(lg.KEY_ENV) or lg.api_key_from_env_file()
    req = urllib.request.Request("https://openrouter.ai/api/v1/key",
                                 headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8")).get("data", {})


def log_stats(path: Path):
    calls, cost, last = 0, 0.0, None
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                e = json.loads(line)
                calls += 1
                cost += float((e["response"].get("usage") or {}).get("cost") or 0)
                last = e.get("utc")
    return calls, cost, last


def processes():
    """Python processes running an experiments/ script: pid, start, script
    and arguments, CPU %, memory."""
    import psutil
    out = []
    for p in psutil.process_iter(["pid", "name", "cmdline", "create_time", "memory_info"]):
        try:
            cmd = p.info["cmdline"] or []
            if "python" not in (p.info["name"] or "").lower():
                continue
            script = next((c for c in cmd if c.endswith(".py")), None)
            if (not script or Path(script).name == Path(__file__).name
                    or not (HERE / Path(script).name).is_file()):   # experiments/ only
                continue
            args = " ".join(cmd[cmd.index(script) + 1:])
            out.append((p.info["pid"], datetime.fromtimestamp(p.info["create_time"]),
                        Path(script).name, args, p.cpu_percent(interval=0.05),
                        p.info["memory_info"].rss / 2 ** 20))
        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
            continue
    return sorted(out, key=lambda r: r[1])


def h12_in_flight(path: Path):
    """H12-E01 pairs with calls in the log but no probe file yet: model,
    dataset, calls so far, first call (the pair's P1a names the dataset by
    its row count)."""
    import h12_probes as h
    by_rows = {f"{v['rows']:,} rows": d for d, v in h.IDENTITY.items()}
    names = {v["name"]: d for d, v in h.IDENTITY.items()}
    started, counts = {}, {}
    if not path.is_file():
        return []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        m = e["request"]["model"]
        user = e["request"]["messages"][-1]["content"]
        d = next((d for k, d in by_rows.items() if k in user), None)             or next((d for k, d in names.items() if k in user), None)
        if d is None:   # P1b, P5: names only -- counted to the model's open pair
            continue
        counts[(m, d)] = counts.get((m, d), 0) + 1
        started.setdefault((m, d), e["utc"])
    return [(m, d, counts[(m, d)], started[(m, d)]) for (m, d) in started
            if not h.probe_path(d, m).is_file()]


def money(x) -> str:
    return f"{'--':>10s}" if x is None else f"{'$' + format(float(x), ',.2f'):>10s}"


def render() -> str:
    lines = [f"Running on this machine  {datetime.now():%Y-%m-%d %H:%M:%S}", ""]
    procs = processes()
    for pid, t0, script, args, cpu, mem in procs:
        mins = (datetime.now() - t0).total_seconds() / 60
        lines.append(f"  pid {pid:6d}  {mins:6.1f} min  {cpu:5.0f}% CPU  {mem:6.0f} MB  "
                     f"{script} {args}"[:150])
    if not procs:
        lines.append("  (no experiment script running)")
    flight = h12_in_flight(LOGS["H12-E01"])
    if flight:
        lines += ["", f"  H12-E01 pairs in flight ({len(flight)}):"]
        for m, d, n, t in sorted(flight, key=lambda r: r[3]):
            lines.append(f"    {d:14s} {m.split('/', 1)[1]:28s} {n:3d} calls  since {t[11:19]} UTC")
    lines += ["", "OpenRouter usage", ""]
    try:
        u = key_usage()
        lines += [f"  today      {money(u.get('usage_daily'))}",
                  f"  this week  {money(u.get('usage_weekly'))}",
                  f"  this month {money(u.get('usage_monthly'))}",
                  f"  all time   {money(u.get('usage'))}",
                  f"  key limit  {money(u.get('limit'))}   remaining "
                  f"{money(u.get('limit_remaining'))}"]
    except Exception as exc:  # noqa: BLE001  keep watching
        lines.append(f"  (OpenRouter not reachable: {type(exc).__name__}: {exc})")
    lines += ["", "Project call logs"]
    total = 0.0
    for name, path in LOGS.items():
        calls, cost, last = log_stats(path)
        total += cost
        lines.append(f"  {name:10s} {calls:6d} calls {money(cost)}   last {last or '--'}")
    lines.append(f"  in logs    {money(total)}   (H8-E01's proposer calls are in its run folders)")
    probes = HERE / "h12" / "probes"
    truth = HERE / "h12" / "truth"
    n_p = len(list(probes.glob("*.json"))) if probes.is_dir() else 0
    n_t = len(list(truth.glob("*.json"))) if truth.is_dir() else 0
    lines += ["", f"H12-E01  probe pairs {n_p}/192   truth {n_t}/16   cap $10"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--every", type=float, default=30.0, help="seconds between refreshes")
    ap.add_argument("--once", action="store_true")
    args = ap.parse_args()
    while True:
        text = render()
        if args.once:
            print(text)
            return 0
        os.system("cls" if os.name == "nt" else "clear")
        print(text, flush=True)
        try:
            time.sleep(args.every)
        except KeyboardInterrupt:
            return 0


if __name__ == "__main__":
    sys.exit(main())
