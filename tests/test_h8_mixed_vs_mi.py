"""DEC-61's post hoc reading: H8-E01's lambda-0.5 arms against H8-E03's MI
alone, from the committed distilled curves."""
import pytest

import h8_mixed_vs_mi as x


@pytest.fixture(scope="module")
def data():
    e01, runs01 = x.load("H8-E01")
    e03, runs03 = x.load("H8-E03")
    return e01, e03, runs01, runs03


def test_distilled_curves_reproduce_the_committed_h8_tables(data):
    e01, e03, _, _ = data
    assert x.check_reproduction(e01, e03) == []


def test_h8_e01_and_h8_e03_can_be_paired(data):
    assert x.check_pairing(*data) == []


def test_a_changed_stock_curve_blocks_the_pairing(data):
    e01, e03, runs01, runs03 = data
    key = next(k for k in e03 if k[0] == x.STOCK)
    changed = {**e03, key: e03[key][:-1] + [(e03[key][-1][0], e03[key][-1][1] + 0.01)]}
    assert any("stock curves differ" in p for p in x.check_pairing(e01, changed, runs01, runs03))


def test_twelve_models_each_on_sixteen_datasets_with_holm_over_twelve(data):
    e01, e03, _, _ = data
    rows = x.mixed_vs_mi(e01, e03)
    assert [r["model"] for r in rows] == list(x.ANTHROPIC + x.OTHERS)
    assert all(r["n_datasets"] == 16 and r["opponent"] == x.MI_ONLY for r in rows)
    assert all(len(r["seed_rows"]) == 80 for r in rows)
    assert all(r["p_holm"] >= r["p"] for r in rows)
    # The nine non-Anthropic rows are H8-E03's own beside rows, unchanged.
    beside = {(r["arm"], r["opponent"]): r for r in x._table(
        x.h8.REPORTS / "H8-E03" / "tables" / "beside.csv")}
    for r in rows[3:]:
        assert float(beside[(r["arm"], x.MI_ONLY)]["mean_effect"]) == r["mean_effect"]
