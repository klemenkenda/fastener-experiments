"""Shared fixtures for the FASTENER swap-operator tests.

FASTENER uses flat top-level imports, so `experiments/_bootstrap.py` has to run
before anything from the clone can be imported. Importing it here puts both
`experiments/` and `fastener/` on `sys.path` for every test module.
"""
import collections
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "experiments"))

import _bootstrap  # noqa: F401,E402  puts ../fastener on sys.path

from item import Item, Result  # noqa: E402


N_FEATURES = 12
N_INFORMATIVE = 3


TinyData = collections.namedtuple("TinyData", "X y X_val y_val")


@pytest.fixture(scope="session")
def tiny_data():
    """A small, fast, clearly structured classification problem.

    Deliberately tiny: these tests exercise the *operators*, and FASTENER's
    bundled dummy data (100k rows) makes `mutual_info_classif` alone take
    minutes.

    The validation half matters: a decision tree reaches ~100% accuracy on its
    own training data using nothing but noise columns, so an evaluator scoring
    on train could never tell a good subset from a bad one.
    """
    rng = np.random.RandomState(0)
    X = rng.normal(size=(300, N_FEATURES))
    # Only the first N_INFORMATIVE columns carry signal.
    y = (X[:, :N_INFORMATIVE].sum(axis=1) > 0).astype(int)
    return TinyData(X[:200], y[:200], X[200:], y[200:])


@pytest.fixture
def run_dir(tmp_path, monkeypatch):
    """FASTENER's Config writes to "log/<name>" relative to the cwd."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


class RecordingEvaluator:
    """Evaluator with FASTENER's fixed (model, genes, shuffle_indices) signature.

    Module-level (not a closure) because `prepare_loop` pickles the optimizer.
    Scores on held-out data, so subsets of noise features score near chance and
    the permutation-importance step has something to measure.
    """

    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __call__(self, model, genes, shuffle_indices=None):
        data = self.X[:, genes]
        if shuffle_indices:
            data = data.copy()
            for j in shuffle_indices:
                np.random.shuffle(data[:, j])
        return Result(float((model.predict(data) == self.y).mean()))


def genes_from(indices, n_features=N_FEATURES):
    genes = [False] * n_features
    for i in indices:
        genes[i] = True
    return genes


def item_from(indices, n_features=N_FEATURES, generation=0):
    return Item(genes_from(indices, n_features), generation, None, None)


def selected(genes):
    return {i for i, g in enumerate(genes) if g}
