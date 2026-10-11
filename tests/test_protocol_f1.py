"""The fast weighted F1 equals scikit-learn's, bit for bit."""
import numpy as np
import pytest
from sklearn.metrics import f1_score

import protocol


@pytest.mark.parametrize("n_classes", [2, 3, 7, 26])
def test_weighted_f1_equals_sklearn(n_classes):
    rng = np.random.RandomState(n_classes)
    for _ in range(300):
        n = int(rng.randint(5, 400))
        y = rng.randint(0, n_classes, n)
        # Mostly right, sometimes predicting labels absent from y_true.
        pred = np.where(rng.rand(n) < 0.6, y, rng.randint(0, n_classes + 2, n))
        assert protocol.weighted_f1(y, pred) == \
            float(f1_score(y, pred, average="weighted"))


def test_weighted_f1_edge_cases():
    for y, pred in [([1, 1, 1], [1, 1, 1]), ([0, 1], [1, 0]), ([0], [3]),
                    (["a", "b", "b"], ["b", "b", "c"]),
                    ([2, 5, 5, 9], [5, 5, 5, 5])]:
        assert protocol.weighted_f1(y, pred) == \
            float(f1_score(y, pred, average="weighted", zero_division=0.0))
