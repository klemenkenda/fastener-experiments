"""Load MADELON and cut deterministic train/val/test splits.

Why three splits and not two
----------------------------
FASTENER's search is *driven* by a score: every candidate subset is evaluated and
the Pareto front keeps the winners. If that score is computed on the test set,
the reported number is optimistically biased -- the search has effectively fitted
the test set through feature selection. (The reference `eval_fun` shipped in
fastener.py scores on the test globals, which is fine for its smoke-test purpose
but not for a comparison.)

So:
  train -- fits each candidate model
  val   -- drives FASTENER's search AND selects k for the baselines (same budget,
           same information, so the comparison is fair)
  test  -- touched exactly once, at the very end, for the reported numbers

MADELON ground truth
--------------------
Exactly 20 of the 500 features are relevant; the remaining 480 are noise. The
identity of those 20 was never published by the organisers, but the relevant
features are recoverable from the data: the noise columns are i.i.d. draws with
no dependence on the label, so a feature's usable signal shows up in the
label-conditional statistics. We therefore do NOT hardcode a ground-truth list;
we report an empirical redundancy-aware check instead (see analysis.py).
"""
import sys
from pathlib import Path
from typing import Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import DATA_DIR  # noqa: E402

MADELON_DIR = DATA_DIR / "madelon"

# Split proportions of the 2600 labelled rows.
VAL_FRACTION = 0.20
TEST_FRACTION = 0.20

# Fixed forever: changing this changes which rows are "untouched test".
SPLIT_SEED = 20200


class Dataset:
    def __init__(self, name, X_train, y_train, X_val, y_val, X_test, y_test,
                 feature_names=None):
        self.name = name
        self.X_train, self.y_train = X_train, y_train
        self.X_val, self.y_val = X_val, y_val
        self.X_test, self.y_test = X_test, y_test
        self.n_features = X_train.shape[1]
        self.feature_names = (
            feature_names if feature_names is not None
            else np.array([f"f{i}" for i in range(self.n_features)])
        )

    def summary(self) -> dict:
        def dist(y):
            vals, counts = np.unique(y, return_counts=True)
            return {int(v): int(c) for v, c in zip(vals, counts)}
        return {
            "name": self.name,
            "n_features": int(self.n_features),
            "n_train": int(self.X_train.shape[0]),
            "n_val": int(self.X_val.shape[0]),
            "n_test": int(self.X_test.shape[0]),
            "class_balance_train": dist(self.y_train),
            "class_balance_val": dist(self.y_val),
            "class_balance_test": dist(self.y_test),
            "split_seed": SPLIT_SEED,
        }

    def __repr__(self) -> str:
        return (f"Dataset({self.name}: {self.n_features} features, "
                f"{self.X_train.shape[0]}/{self.X_val.shape[0]}/"
                f"{self.X_test.shape[0]} train/val/test)")


def _stratified_three_way(y, val_frac, test_frac, seed) -> Tuple[np.ndarray, ...]:
    """Stratified index split, implemented directly so it does not depend on a
    particular scikit-learn version's shuffling behaviour."""
    rng = np.random.RandomState(seed)
    train_idx, val_idx, test_idx = [], [], []
    for cls in np.unique(y):
        idx = np.where(y == cls)[0]
        rng.shuffle(idx)
        n = len(idx)
        n_test = int(round(n * test_frac))
        n_val = int(round(n * val_frac))
        test_idx.append(idx[:n_test])
        val_idx.append(idx[n_test:n_test + n_val])
        train_idx.append(idx[n_test + n_val:])
    out = []
    for parts in (train_idx, val_idx, test_idx):
        merged = np.concatenate(parts)
        rng.shuffle(merged)
        out.append(merged)
    return tuple(out)


def load_madelon() -> Dataset:
    if not MADELON_DIR.is_dir():
        raise FileNotFoundError(
            f"{MADELON_DIR} missing. Run: python experiments/download_data.py"
        )

    X_a = np.loadtxt(MADELON_DIR / "madelon_train.data")
    y_a = np.loadtxt(MADELON_DIR / "madelon_train.labels")
    X_b = np.loadtxt(MADELON_DIR / "madelon_valid.data")
    y_b = np.loadtxt(MADELON_DIR / "madelon_valid.labels")

    # The official split is irrelevant to us: we pool and re-cut so that the test
    # set is genuinely untouched by anything the search or tuning sees.
    X = np.vstack([X_a, X_b])
    y = np.concatenate([y_a, y_b]).astype(int)

    tr, va, te = _stratified_three_way(y, VAL_FRACTION, TEST_FRACTION, SPLIT_SEED)

    return Dataset(
        "madelon",
        X[tr], y[tr],
        X[va], y[va],
        X[te], y[te],
        feature_names=np.array([f"V{i}" for i in range(X.shape[1])]),
    )


if __name__ == "__main__":
    ds = load_madelon()
    print(ds)
    import json
    print(json.dumps(ds.summary(), indent=2))
