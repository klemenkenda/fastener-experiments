"""Tests for reading the UCR/UEA `.ts` files and loading the TSC datasets."""
import numpy as np
import pytest

import datasets
from download_tsc_datasets import parse_ts

UNIVARIATE = """#A comment line
@problemName Toy
@timeStamps false
@missing false
@univariate true
@equalLength true
@seriesLength 4
@classLabel true a b
@data
1,2,3,4:a
5,6,7,8:b
"""

MULTIVARIATE = """@problemName Toy2
@timeStamps false
@univariate false
@dimensions 2
@equalLength true
@seriesLength 3
@classLabel true x y
@data
1,2,3:10,20,30:x
4,5,6:40,50,60:y
"""


def test_univariate_rows_and_labels():
    X, labels, length, channels = parse_ts(UNIVARIATE)
    assert (length, channels) == (4, 1)
    assert labels == ["a", "b"]
    np.testing.assert_array_equal(X, [[1, 2, 3, 4], [5, 6, 7, 8]])


def test_multivariate_is_flattened_channel_by_channel():
    X, labels, length, channels = parse_ts(MULTIVARIATE)
    assert (length, channels) == (3, 2)
    # Feature c*length + t is channel c at time t.
    np.testing.assert_array_equal(X[0], [1, 2, 3, 10, 20, 30])
    np.testing.assert_array_equal(X[1], [4, 5, 6, 40, 50, 60])
    assert labels == ["x", "y"]


def test_missing_values_become_nan():
    X, _, _, _ = parse_ts(UNIVARIATE.replace("5,6,7,8", "5,?,7,8"))
    assert np.isnan(X[1, 1])
    assert not np.isnan(X[0]).any()


@pytest.mark.parametrize("change, message", [
    (("@equalLength true", "@equalLength false"), "unequal-length"),
    (("@timeStamps false", "@timeStamps true"), "timestamped"),
    (("@classLabel true a b", "@classLabel false"), "no class label"),
    (("@data\n", ""), "no @data"),
])
def test_unsupported_files_are_refused(change, message):
    with pytest.raises(ValueError, match=message):
        parse_ts(UNIVARIATE.replace(*change))


def test_rows_of_different_shape_are_refused():
    with pytest.raises(ValueError, match="shape"):
        parse_ts(UNIVARIATE.replace("5,6,7,8:b", "5,6,7:b"))


def test_channels_of_different_length_are_refused():
    with pytest.raises(ValueError, match="unequal length"):
        parse_ts(MULTIVARIATE.replace("4,5,6:40,50,60", "4,5,6:40,50"))


@pytest.mark.parametrize("change, message", [
    (("@seriesLength 3", "@seriesLength 4"), "header says 4"),
    (("@dimensions 2", "@dimensions 3"), "header says 3"),
])
def test_rows_must_agree_with_the_header(change, message):
    with pytest.raises(ValueError, match=message):
        parse_ts(MULTIVARIATE.replace(*change))


def _write_npz(tmp_path, monkeypatch, name, X, y):
    monkeypatch.setattr(datasets, "TSC_DIR", tmp_path)
    (tmp_path / name).mkdir()
    np.savez_compressed(tmp_path / name / f"{name}.npz", X=X, y=y,
                        feature_names=np.array([f"t{i}" for i in range(X.shape[1])]),
                        class_names=np.array(["a", "b", "c"])[:y.max() + 1],
                        origin=np.zeros(len(y), int), dropped_missing=0)


def test_loader_splits_60_20_20_and_drops_classes_under_five(tmp_path, monkeypatch):
    rng = np.random.RandomState(0)
    y = np.r_[np.zeros(50, int), np.ones(50, int), np.full(3, 2)]
    X = rng.rand(len(y), 6).astype(np.float32)
    _write_npz(tmp_path, monkeypatch, "Coffee", X, y)

    ds = datasets.load("Coffee")

    assert ds.dropped_small_classes == {2: 3}
    assert (ds.X_train.shape[0], ds.X_val.shape[0], ds.X_test.shape[0]) == (60, 20, 20)
    assert set(np.unique(ds.y_test)) == {0, 1}
    assert ds.n_features == 6


def test_every_selected_dataset_is_loadable_by_name():
    for name in datasets.TSC_DATASETS:
        assert name in datasets.LOADERS
    assert len(datasets.TSC_DATASETS) == 39
