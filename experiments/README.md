# Baseline experiment: FASTENER vs. standard feature selectors

## Question

On a high-dimensional dataset with known structure, does FASTENER's
entropy-guided genetic search find better small feature subsets than standard
filter and wrapper selectors — and at what cost?

## Dataset

**MADELON** (NIPS 2003 feature-selection challenge), from the UCI archive.

Chosen because its structure is documented: of 500 features, exactly **20 are
relevant** (5 informative + 15 redundant linear combinations) and **480 are
noise**. It is also non-linear (an XOR-like cluster problem), so univariate
filters are expected to struggle — which makes it a fair test of a method that
searches subsets rather than ranking features one at a time.

The official test labels were never released, so the experiment pools the
released train (2000) and validation (600) rows into 2600 labelled samples and
cuts its own stratified splits (seed `20200`, fixed in `datasets.py`):

| split | rows | role |
|---|---|---|
| train | 1560 | fits every candidate model |
| val   | 520  | drives FASTENER's search; selects *k* for baselines |
| test  | 520  | touched once, for the reported numbers |

## Why three splits

FASTENER's search is *driven* by a score: every candidate subset is evaluated and
the Pareto front keeps the winners. If that score comes from the test set, the
reported number is optimistically biased — the search has fitted the test set
through feature selection.

The reference `eval_fun` shipped in [`fastener.py`](../fastener/fastener.py)
scores against the test globals. That is fine for its purpose as a smoke test,
but not for a comparison, so this experiment supplies its own evaluator closed
over the **validation** split (`ValidationEvaluator` in `run_fastener.py`).

Baselines get the same deal: selectors are fit on **train only**, *k* is chosen on
**val**, and the number reported is on **test**. Every method's final number is
produced by the same function, `protocol.evaluate_subset`.

## Methods compared

| method | family | how it picks features |
|---|---|---|
| `fastener` | genetic | entropy-guided crossover + mutation + permutation-importance pruning |
| `kbest_mutual_info` | filter | top-*k* by mutual information with the label |
| `kbest_anova_f` | filter | top-*k* by ANOVA F |
| `tree_importance` | embedded | top-*k* by impurity importance of one tree on all features |
| `rfe_tree` | wrapper | recursive feature elimination, 10% per step |
| `random` | floor | best of 10 random subsets per *k* (picked on val) |
| `all_features` | reference | all 500 |

The classifier is a `DecisionTreeClassifier(random_state=20200)` for every method
— the same learner FASTENER's reference uses. The comparison is about the feature
subset, not the model.

ReliefF (compared against in the paper) is not included: it needs `skrebate`,
which is unmaintained and not installed. The filter family is represented by
mutual information and ANOVA F instead.

## Fairness caveat — read this before quoting any number

The methods **do not** use comparable compute. FASTENER fits thousands of models
during its search; a filter ranks once and fits |k-grid| models. Every run records
`cost.baseline_model_fits` and `cost.fastener_model_fits_per_seed` in its manifest
so the asymmetry is visible rather than assumed. This is a like-for-like
comparison of *outcomes at a given feature count*, not of outcomes per unit of
compute.

FASTENER also consults the validation split far more intensively than the
baselines do, which is a real and reportable source of validation overfitting.

## Running it

```bash
conda activate fastener-exp                  # python 3.11, sklearn 1.9
python experiments/download_data.py          # verifies pinned SHA256
python experiments/run_experiment.py --rounds 600 --seeds 5
python experiments/run_experiment.py --quick # ~1 min smoke check
```

## Traceability

Each run creates `results/<UTC timestamp>_<name>/` containing:

| file | contents |
|---|---|
| `manifest.json` | git commit + dirty flag of **both** repos, python/package versions, dataset SHA256s, every seed and parameter, elapsed time, and the SHA256 of every output file |
| `comparison.csv` | one row per (method, seed, budget *k*) with val and test scores |
| `raw_results.json` | every evaluated subset, with the exact feature indices |
| `comparison.png` | test score vs. feature budget |
| `log/fastener_seed*/` | FASTENER's own per-generation pickles (population, Pareto front, RNG state) |

The manifest records a `dirty` flag per repo. **A run made from a dirty tree is
not reproducible from its commit alone** — the flag is there so that such a run
can be spotted rather than trusted by accident.

Determinism: dataset split (`20200`), classifier (`20200`), mutual-information
estimator (`20200`), random baseline (`20200`) and each FASTENER seed
(`2020 + i`) are all fixed. FASTENER seeds its RNG inside `Config.__post_init__`.

## Files

| file | role |
|---|---|
| `provenance.py` | run directories, manifests, git/env capture, checksums |
| `download_data.py` | fetches MADELON, verifies pinned checksums |
| `datasets.py` | loading and the stratified three-way split |
| `protocol.py` | the shared model, metric and `evaluate_subset` |
| `baselines.py` | the baseline selectors |
| `run_fastener.py` | FASTENER wired to the protocol |
| `analysis.py` | comparison table, plot, signal probe |
| `run_experiment.py` | the driver |
| `_bootstrap.py` | puts `../fastener` on `sys.path` |

## First result (run `20260916T123417Z_madelon_baseline`)

600 generations × 5 seeds, against the untouched test split.

| feature budget | FASTENER (mean ± sd) | best baseline | seeds beating it | p |
|---|---|---|---|---|
| k=2  | **0.581 ± 0.006** | 0.550 (`tree_importance`) | 5/5 | <0.001 |
| k=3  | **0.669 ± 0.027** | 0.648 (`rfe_tree`) | 4/5 | 0.167 |
| k=5  | 0.798 ± 0.050 | 0.798 (`tree_importance`) | 2/5 | 0.995 |
| k=10 | 0.817 ± 0.031 | 0.806 (`tree_importance`) | 3/5 | 0.487 |

Reference points: all 500 features = 0.731; best random subset = 0.731 (at k=500).

**Reading it honestly.** At the top of the curve FASTENER is at *parity*, not ahead:
+0.011 over a single tree's impurity importance is well inside its own seed
spread (sd 0.031, 3 of 5 seeds ahead, p=0.49), and it costs ~30× the model fits
(≈6,000 vs 209). Quoting "0.817 vs 0.806" as a win would not survive scrutiny.

**Where it does separate.** In the small-*k* region: at k=2 every seed beats every
baseline. That is the result consistent with the method's premise — MADELON is
XOR-like, so features matter jointly, and mutual-information ranking (which scores
features one at a time) never gets past 0.665 no matter how many it is given.
A subset search can see interactions a univariate filter cannot.

**A caveat worth following up.** Validation score keeps improving from round 300
to 1000 (0.856 → 0.862) while test score stays flat (~0.78). The search is
overfitting the split that guides it, which is expected when one split drives
thousands of subset evaluations. Cross-validated or resampled fitness inside the
search would be the obvious next thing to test.

**Cost.** FASTENER's per-generation pickles are ~1.5 GB per 5-seed run. They are
gitignored, but `results/` will grow quickly; delete old `log/` directories
freely, since the manifest records the seeds needed to regenerate them.

Determinism was verified by running the whole experiment twice: identical
per-seed test scores both times.
