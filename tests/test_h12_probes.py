"""h12_probes.py: the grading rules H12 registers (no network, no data)."""
import numpy as np

import h12_probes as h


def test_schema_match_exact_first_then_fuzzy_one_to_one():
    true = ["tBodyAcc-mean()-X", "tBodyAcc-mean()-Y", "word_freq_make"]
    listed = ["tBodyAcc-mean()-Y", "tBodyAcc-mean()-X", "word_freq_mke"]
    m = h.schema_match(true, listed)
    assert m == {0: 1, 1: 0, 2: 2}
    assert h.schema_match(true, listed, fuzzy=1.0) == {0: 1, 1: 0}
    # A listed name matches one true name only.
    assert len(h.schema_match(["a_x", "a_y"], ["a_x"])) == 1


def test_identified_reads_name_and_source():
    assert h.identified("spambase", '{"name": "Spambase", "source": "UCI"}')
    assert h.identified("har", '{"name": "UCI HAR", "source": "Anguita"}')
    assert not h.identified("har", '{"name": "unknown", "source": "chart share"}')
    assert h.identified("pc4", 'not json, but PC4 from NASA MDP')


def test_flat_scores_count_as_zero():
    assert h.spearman0([1, 1, 1], [1, 2, 3]) == 0.0
    assert h.partial_spearman0([1, 1, 1], [1, 2, 3], [3, 2, 1]) == 0.0


def test_partial_spearman_removes_what_the_control_knows():
    rng = np.random.RandomState(0)
    truth = rng.rand(50)
    control = truth + 0.1 * rng.rand(50)
    copy = control.copy()             # knows nothing beyond the control
    assert abs(h.partial_spearman0(copy, truth, control)) < 1e-9
    extra = truth.copy()              # knows truth beyond the control
    assert h.partial_spearman0(extra, truth, control) > 0.5
    # A flat control leaves the plain correlation.
    assert np.isclose(h.partial_spearman0(extra, truth, np.ones(50)),
                      h.spearman0(extra, truth))
