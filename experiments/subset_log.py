"""Every subset a search scores, and what each generation proposed (H14, B14).

One `SubsetLog` per run, written once to a compressed .npz beside the run's
other outputs. Two tables:

* per newly scored subset (one model fit each): the generation it was scored
  in, its size, its validation score, the fit's wall time and the subset as a
  packed bitset (`np.packbits`, d/8 bytes);
* per generation: children proposed, children that were empty, cache hits
  (already scored, no fit), children identical to a member of the current
  population, children mutation left unchanged, forced flips (the `min1`
  control), and the flip counts per child as a histogram of 0, 1, 2, 3+.

Generation 0 is the initial population: it has no mutation, so its mutation
columns are 0. Read a log with `read(path)`.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

FLIP_BINS = 4   # 0, 1, 2, 3+
GEN_FIELDS = ("generation", "proposals", "empty", "cache_hits", "new_fits",
              "same_as_population", "unchanged_by_mutation", "forced_flips",
              "flips_0", "flips_1", "flips_2", "flips_3plus")


class SubsetLog:
    def __init__(self, path: Path, n_features: int) -> None:
        self.path = Path(path)
        self.n_features = int(n_features)
        self._gen = 0
        self._bits: List[bytes] = []
        self._sub: Dict[str, List] = {"generation": [], "size": [],
                                      "val_score": [], "fit_seconds": []}
        self._rows: List[Dict[str, int]] = []
        self._row: Optional[Dict[str, int]] = None
        self.begin(0)

    def begin(self, generation: int) -> None:
        """Start the counters of a generation (0 = the initial population)."""
        if self._row is not None:
            self._rows.append(self._row)
        self._gen = int(generation)
        self._row = {f: 0 for f in GEN_FIELDS}
        self._row["generation"] = self._gen

    def mutation(self, before: np.ndarray, after: np.ndarray,
                 forced: Optional[np.ndarray] = None) -> None:
        """Flip counts of one generation's children, `before` and `after`
        mutation (forced flips included in `after`)."""
        flips = (before != after).sum(axis=1)
        if forced is not None:
            # A forced flip comes after the mutation proper: count it apart.
            flips = flips - forced.astype(int)
            self._row["forced_flips"] += int(forced.sum())
        self._row["unchanged_by_mutation"] += int((flips == 0).sum())
        h = np.bincount(np.minimum(flips, FLIP_BINS - 1), minlength=FLIP_BINS)
        for name, c in zip(("flips_0", "flips_1", "flips_2", "flips_3plus"), h):
            self._row[name] += int(c)

    def proposals(self, children: np.ndarray, population_keys=()) -> None:
        """Children about to be scored: how many, empty, and identical to a
        member of the current population."""
        keys = set(population_keys)
        self._row["proposals"] += int(children.shape[0])
        self._row["empty"] += int((children.sum(axis=1) == 0).sum())
        if keys:
            self._row["same_as_population"] += sum(
                np.packbits(c).tobytes() in keys for c in children)

    def cache_hit(self) -> None:
        self._row["cache_hits"] += 1

    def scored(self, genes: np.ndarray, val_score: float, seconds: float) -> None:
        """One newly scored subset (one model fit)."""
        self._row["new_fits"] += 1
        self._bits.append(np.packbits(genes).tobytes())
        self._sub["generation"].append(self._gen)
        self._sub["size"].append(int(genes.sum()))
        self._sub["val_score"].append(float(val_score))
        self._sub["fit_seconds"].append(float(seconds))

    def write(self) -> Path:
        if self._row is not None:
            self._rows.append(self._row)
            self._row = None
        self.path.parent.mkdir(parents=True, exist_ok=True)
        nbytes = (self.n_features + 7) // 8
        bits = (np.frombuffer(b"".join(self._bits), dtype=np.uint8)
                .reshape(-1, nbytes) if self._bits
                else np.zeros((0, nbytes), dtype=np.uint8))
        gens = {f"gen_{f}": np.array([r[f] for r in self._rows], dtype=np.int64)
                for f in GEN_FIELDS}
        np.savez_compressed(
            self.path, n_features=np.int64(self.n_features), bits=bits,
            sub_generation=np.array(self._sub["generation"], dtype=np.int32),
            sub_size=np.array(self._sub["size"], dtype=np.int32),
            sub_val_score=np.array(self._sub["val_score"], dtype=np.float64),
            sub_fit_seconds=np.array(self._sub["fit_seconds"], dtype=np.float32),
            **gens)
        return self.path


def read(path: Path) -> Dict[str, np.ndarray]:
    """A log as arrays; `subsets` is the boolean matrix (one row per fit)."""
    with np.load(path) as z:
        out = {k: z[k] for k in z.files}
    d = int(out["n_features"])
    out["subsets"] = np.unpackbits(out["bits"], axis=1, count=d).astype(bool)
    return out
