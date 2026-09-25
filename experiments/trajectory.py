"""Best score per iteration, recorded for every search (HYPOTHESES.md,
"Progress tracking").

A search feeds this two things:

* `observe(features, val_score)` -- every subset it has scored, from the one
  place it fits a model;
* `step(iteration, fits)` -- at the end of each of its own iterations.

From those it keeps an archive of the best validation score seen at each subset
size, and after every step appends one JSON line holding the best score so far
(overall and per k), the smallest and largest size on the front, and the front
itself -- so any front metric can be recomputed later without re-running.

The front is written only on a line where it changed (`front_changed: true`);
on the other lines it is the same as on the last line that carried one. That
loses nothing -- `read(..., fill_fronts=True)` restores it on every line -- and
keeps a long FASTENER or POSS run, where most iterations change nothing, from
repeating the same front thousands of times.

Validation only: nothing here ever sees the test split. Lines are appended and
flushed as they happen, so a run that is killed still leaves its trajectory.

The object holds no open file handle and only plain attributes, because
FASTENER pickles its whole optimizer -- this included -- at the start of a run.
"""
import json
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence


class Trajectory:
    def __init__(self, path: Path, method: str, seed: int,
                 k_grid: Sequence[int]) -> None:
        self.path = str(path)
        self.method = method
        self.seed = seed
        self.k_grid = sorted(int(k) for k in k_grid)
        self.t0 = time.time()
        # size -> (best validation score, sorted feature list)
        self.best_at_size: Dict[int, tuple] = {}
        self._last_front = None
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        # Start clean: a rerun into the same directory must not append to an
        # old trajectory and silently double it.
        Path(self.path).write_text("", encoding="utf-8")

    def observe(self, features: Iterable[int], val_score: float) -> None:
        feats = sorted(int(f) for f in features)
        size = len(feats)
        if size == 0:
            return
        score = float(val_score)
        prev = self.best_at_size.get(size)
        if prev is None or score > prev[0]:
            self.best_at_size[size] = (score, feats)

    def front(self) -> List[Dict]:
        """The Pareto front of the archive: each size kept only if it scores
        strictly better than every smaller size."""
        out, best = [], float("-inf")
        for size in sorted(self.best_at_size):
            score, feats = self.best_at_size[size]
            if score > best:
                out.append({"size": size, "val_f1": round(score, 6),
                            "features": feats})
                best = score
        return out

    def best_up_to(self, k: int) -> Optional[float]:
        scores = [s for size, (s, _) in self.best_at_size.items() if size <= k]
        return round(max(scores), 6) if scores else None

    def step(self, iteration: int, fits: int, **extra) -> Dict:
        front = self.front()
        snap = {
            "method": self.method,
            "seed": self.seed,
            "iteration": int(iteration),
            "fits": int(fits),
            "seconds": round(time.time() - self.t0, 3),
            "best_val_f1": front[-1]["val_f1"] if front else None,
            "best_val_f1_by_k": {str(k): self.best_up_to(k) for k in self.k_grid},
            "min_size": front[0]["size"] if front else None,
            "max_size": front[-1]["size"] if front else None,
        }
        key = [(f["size"], f["val_f1"]) for f in front]
        snap["front_changed"] = key != self._last_front
        if snap["front_changed"]:
            snap["front"] = front
            self._last_front = key
        snap.update(extra)
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(snap) + "\n")
        return snap


def read(path: Path, fill_fronts: bool = True) -> List[Dict]:
    """All snapshots in a trajectory file, in order.

    With `fill_fronts`, every snapshot gets the front in force at that point,
    carried forward from the last line that wrote one.
    """
    with open(path, encoding="utf-8") as fh:
        snaps = [json.loads(line) for line in fh if line.strip()]
    if fill_fronts:
        current = []
        for snap in snaps:
            if snap.get("front_changed"):
                current = snap["front"]
            else:
                snap["front"] = current
    return snaps
