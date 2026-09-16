"""Live progress and ETA for long runs.

A run declares its planned units up front, then reports as each starts, ticks
and finishes. State is written to `progress.json` in the run directory after
every update, so `monitor.py` (or anything else) can read it from another
process without touching the run.

The ETA is deliberately per-method. A model fit is not a constant unit of work
here: an NSGA-II fit on a 269-feature subset costs roughly eight times a
FASTENER fit on a 4-feature one, so a single global rate would be badly wrong
for whichever method it was not calibrated on. Rates are learned from the units
that have actually finished in this run, and fall back to the priors below only
until there is real data.
"""
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Seconds per model fit, measured on the MADELON smoke run. Used only as a cold
# start; a method's own measured rate replaces it as soon as one unit finishes.
PRIOR_SECONDS_PER_FIT = {
    "nsga2": 0.24,
    "nsgaii_miip": 0.26,
    "fastener": 0.031,
}
DEFAULT_SECONDS_PER_FIT = 0.1

# Whole-unit priors for the deterministic filters, which have no fit budget.
PRIOR_FILTER_SECONDS = {
    "mrmr": 8.0,
    "relieff": 60.0,
    "boruta": 160.0,
    "hsic_lasso": 25.0,
}
DEFAULT_FILTER_SECONDS = 30.0


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


class Progress:
    """Tracks planned/completed units and writes a JSON heartbeat."""

    def __init__(self, path: Path, run_id: str, meta: Optional[Dict] = None,
                 min_write_interval: float = 1.0) -> None:
        self.path = Path(path)
        self.run_id = run_id
        self.meta = meta or {}
        self.units: List[Dict[str, Any]] = []
        self.current: Optional[Dict[str, Any]] = None
        self.status = "running"
        self.error: Optional[str] = None
        self._t0 = time.time()
        # Throttle: an intra-search tick can fire many times a second, and the
        # monitor only ever reads the newest state.
        self._min_write_interval = min_write_interval
        self._last_write = 0.0

    # -- planning ---------------------------------------------------------
    def plan(self, method: str, seed: Optional[int] = None,
             budget_fits: Optional[int] = None) -> str:
        unit_id = method if seed is None else f"{method}:{seed}"
        self.units.append({
            "unit_id": unit_id, "method": method, "seed": seed,
            "budget_fits": budget_fits, "state": "pending",
            "seconds": None, "fits": None,
        })
        return unit_id

    def _unit(self, unit_id: str) -> Dict[str, Any]:
        for u in self.units:
            if u["unit_id"] == unit_id:
                return u
        raise KeyError(unit_id)

    # -- execution --------------------------------------------------------
    def start(self, unit_id: str) -> None:
        u = self._unit(unit_id)
        u["state"] = "running"
        u["started_utc"] = _utc()
        self.current = {"unit_id": unit_id, "t0": time.time(),
                        "fits_done": 0, "fraction": 0.0}
        self.write(force=True)

    def tick(self, fits_done: int, budget: Optional[int] = None) -> None:
        """Report intra-unit progress. Safe to call very often."""
        if self.current is None:
            return
        self.current["fits_done"] = int(fits_done)
        budget = budget or self._unit(self.current["unit_id"])["budget_fits"]
        if budget:
            self.current["fraction"] = min(1.0, fits_done / float(budget))
        self.write()

    def finish(self, unit_id: str, fits: Optional[int] = None,
               seconds: Optional[float] = None, **extra) -> None:
        u = self._unit(unit_id)
        u["state"] = "done"
        u["seconds"] = round(
            seconds if seconds is not None
            else time.time() - (self.current or {}).get("t0", time.time()), 2)
        u["fits"] = fits
        u.update(extra)
        self.current = None
        self.write(force=True)

    def fail(self, unit_id: str, message: str) -> None:
        u = self._unit(unit_id)
        u["state"] = "failed"
        u["error"] = message[:500]
        self.current = None
        self.write(force=True)

    def done(self, status: str = "done", error: Optional[str] = None) -> None:
        self.status = status
        self.error = error
        self.write(force=True)

    # -- estimation -------------------------------------------------------
    def seconds_per_fit(self, method: str) -> float:
        """Rate learned from this run's finished units, else the prior."""
        samples = [u["seconds"] / u["fits"] for u in self.units
                   if u["method"] == method and u["state"] == "done"
                   and u.get("fits") and u.get("seconds")]
        if samples:
            return sum(samples) / len(samples)
        return PRIOR_SECONDS_PER_FIT.get(method, DEFAULT_SECONDS_PER_FIT)

    def _estimate_unit_seconds(self, u: Dict[str, Any]) -> float:
        if u.get("budget_fits"):
            return u["budget_fits"] * self.seconds_per_fit(u["method"])
        done = [x["seconds"] for x in self.units
                if x["method"] == u["method"] and x["state"] == "done"
                and x.get("seconds")]
        if done:
            return sum(done) / len(done)
        return PRIOR_FILTER_SECONDS.get(u["method"], DEFAULT_FILTER_SECONDS)

    def eta_seconds(self) -> Optional[float]:
        remaining = 0.0
        for u in self.units:
            if u["state"] in ("done", "failed"):
                continue
            est = self._estimate_unit_seconds(u)
            if self.current and u["unit_id"] == self.current["unit_id"]:
                # Prefer the in-flight unit's own observed rate: it is the most
                # current evidence, and for the first unit of a method it is the
                # only evidence there is.
                elapsed = time.time() - self.current["t0"]
                frac = self.current.get("fraction", 0.0)
                if frac > 0.02:
                    est = max(elapsed / frac - elapsed, 0.0)
                else:
                    est = max(est - elapsed, 0.0)
            remaining += est
        return remaining

    # -- io ---------------------------------------------------------------
    def snapshot(self) -> Dict[str, Any]:
        total = len(self.units)
        done = sum(1 for u in self.units if u["state"] == "done")
        failed = sum(1 for u in self.units if u["state"] == "failed")
        eta = self.eta_seconds() if self.status == "running" else 0.0
        cur = None
        if self.current:
            cur = {k: v for k, v in self.current.items() if k != "t0"}
            cur["elapsed_seconds"] = round(time.time() - self.current["t0"], 1)
            u = self._unit(self.current["unit_id"])
            cur["method"], cur["seed"] = u["method"], u["seed"]
            cur["budget_fits"] = u["budget_fits"]
        return {
            "run_id": self.run_id,
            "pid": os.getpid(),
            "meta": self.meta,
            "status": self.status,
            "error": self.error,
            "updated_utc": _utc(),
            "elapsed_seconds": round(time.time() - self._t0, 1),
            "eta_seconds": None if eta is None else round(eta, 1),
            "units_total": total,
            "units_done": done,
            "units_failed": failed,
            "fraction_done": round(done / total, 4) if total else 0.0,
            "current": cur,
            "units": self.units,
            # Only the fit-budgeted methods. A filter has no fit count, so a
            # rate for it would be the fallback prior dressed up as a
            # measurement.
            "seconds_per_fit": {
                m: round(self.seconds_per_fit(m), 4)
                for m in sorted({u["method"] for u in self.units
                                 if u.get("budget_fits")})
            },
        }

    def write(self, force: bool = False) -> None:
        now = time.time()
        if not force and now - self._last_write < self._min_write_interval:
            return
        self._last_write = now
        tmp = self.path.with_suffix(".json.tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(self.snapshot(), fh, indent=2, default=str)
            # Atomic replace, so a reader never sees a half-written file.
            os.replace(tmp, self.path)
        except OSError:
            # Progress reporting must never take the run down with it.
            pass


def format_duration(seconds: Optional[float]) -> str:
    if seconds is None:
        return "?"
    seconds = int(max(0, seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}m"
    if m:
        return f"{m}m{s:02d}s"
    return f"{s}s"
