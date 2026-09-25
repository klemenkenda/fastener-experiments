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

## SOTA comparison

`run_sota_experiment.py` extends the baseline experiment with stronger and more
recent competitors, across two datasets.

### Methods added

| method | family | provenance |
|---|---|---|
| `mrmr` | information filter | Peng et al. 2005, implemented directly (MID criterion) |
| `relieff` | filter | `skrebate` -- the FASTENER paper's own comparator |
| `boruta` | all-relevant | `BorutaPy`, RF shadow features |
| `hsic_lasso` | kernel filter | `pyHSICLasso`, detects non-linear dependence |
| `nsga2` | multi-objective EA | implemented here; the baseline both recent papers benchmark against |
| `poss` | Pareto archive | Qian, Yu & Zhou 2015, implemented from the published Algorithm 1 |
| `fs_sds` | swarm (SDS) | Alhakbani & al-Rifaie 2017, from the authors' reference implementation |
| `nsgaii_miip` | multi-objective EA | **ported** from the authors' MATLAB (2025) |
| `nsgaii_miip_sparse` | multi-objective EA | the port with a **non-faithful** sparse init, as a control |

### FASTENER's own comparators

Two of the methods here are the ones the FASTENER paper itself benchmarks
against: **POSS** (its reference [11]) and **FS-SDS** (its reference [12]).
Running them under this experiment's protocol is the closest thing available to
a replication of the paper's own comparison -- with the difference that here
every method is scored identically, whereas the paper let each method keep its
own classifier (FS-SDS on an Extreme Learning Machine, FASTENER on a decision
tree). That difference is the point: it separates the search from the learner.

### About FS-SDS

[`fs_sds.py`](fs_sds.py) implements **Feature Selection using Stochastic
Diffusion Search** (Alhakbani & al-Rifaie, GECCO 2017). SDS is a swarm method:
agents hold hypotheses, a TEST phase marks each agent active or inactive against
a randomly drawn peer, and a DIFFUSION phase spreads good hypotheses by direct
agent-to-agent contact, with random restarts for agents whose contact was
inactive.

The [authors' reference implementation](https://github.com/mohmaj/SDS-FS) is
public but carries **no licence**, so the code here is written fresh from
reading it; the mechanics are theirs, the code is not, and these are not their
results.

**It fixes k for a whole run.** Every agent holds exactly k features from start
to finish -- there is no size objective, so one run produces one point rather
than a front, and a curve costs one run per k. That is the structural difference
from FASTENER, POSS and NSGA-II, and the FASTENER paper makes the same point
(Section 5.4: "Both FS-SDS and DT-forward are rigid when selecting the feature
subset size"). It is also why FS-SDS is planned and budgeted separately in the
runner: `stop_evaluations` is PER K, so the total is (budget x |k-grid|).

**On budget, two decisions worth knowing about:**

- Each run gets the same fit budget a whole run of any other search gets, and
  the much larger total is reported rather than charged against it. Splitting
  one shared budget across the grid would leave a few hundred fits per k and
  manufacture a weak result out of a cost structure the method cannot help.
- The reference implementation stops after 50 sweeps, which on MADELON is
  ~2600 fits per k -- *less* than the shared budget. Stopping there would hand
  FS-SDS less compute than its competitors and then report it as weaker, so the
  iteration cap is off by default and the budget is what stops a run.
  `--sds-iterations 50` restores the reference behaviour.

**It is competitive, and that is worth saying plainly.** On MADELON at 6000
fits per k (seed 2020) it reaches test F1 0.819 at k=5, above FASTENER's ~0.81
and POSS's ~0.80 on the same split. Where it loses is cost: three k values cost
18,000 fits against 6,000 for one complete run of either. The FASTENER paper
reports beating it on 24 of 25 benchmark data sets; MADELON is not among those
25, and the protocol here differs, so the two statements do not conflict -- but
nothing in this run reproduces a walkover, and the results should not be written
up as if it did.

**A note for the swap-operator work in `TODO.md`.** FS-SDS's diffusion move is a
uniform-random, size-preserving swap: copy an active agent's subset, drop one
selected feature, add one unselected. That is the same neighbourhood as the
proposed `fastener_swap_random` arm, published in 2017 and cited by the FASTENER
paper. It is prior art for the swap itself -- not for guiding it, since FS-SDS
picks both ends uniformly and has no information-gain term. The novelty claim
should be scoped to the guidance accordingly.

### About POSS

[`poss.py`](poss.py) implements **Pareto Optimization for Subset Selection**
(Qian, Yu & Zhou, NIPS 2015) from the published Algorithm 1. Unlike the
NSGAII-MIIP port there is no large external source being transliterated -- the
pseudocode is a dozen lines and is reproduced in the module docstring next to
the code -- so the room for a porting artefact is much smaller.

It is in the comparison because it is the closest published relative of
FASTENER: a Pareto **archive** over (quality, subset size), advanced by
single-parent bit-flip mutation, with no crossover, no information guidance and
no pruning. It is the control for how much of FASTENER's result comes from those
operators rather than from Pareto archiving itself.

Three documented departures: the objective is this experiment's shared metric
(not the paper's R^2 / submodular f), the budget is the shared model-fit budget,
and the whole archive is reported as a curve while the paper's own single answer
(best subset with |s| <= k) is reported separately as `native_subset`.

**The budget departure is the one that matters.** The paper's T is 2*e*k^2*n --
6.8M evaluations at n=500, k=50, against the 6000 fits every arm here gets. Each
run records `theoretical_evaluations` beside what it was granted. A weak showing
by POSS in these results is evidence about its anytime behaviour at 6000 fits,
**not** about the published algorithm, whose approximation guarantee needs the
full T and a submodular objective that a wrapper score is not.

Measured consequence on MADELON (6000 fits, seed 2020): the archive spans sizes
1-7, reaching test F1 0.80 at 7 features, and not one draw is rejected as
infeasible -- POSS grows from the empty set one accepted bit-flip at a time, so
k never binds and the curve simply stops in single digits. This is the exact
mirror of the NSGAII-MIIP initialisation problem below: that search never comes
down below ~200 features, this one never gets up past ~8. `subset_size_reach`
records both, so neither reads as missing data.

### About the NSGAII-MIIP port

[`nsgaii_miip.py`](nsgaii_miip.py) is a Python port of
[andali89/NSGAII-MIIP](https://github.com/andali89/NSGAII-MIIP) (MIT), whose
original needs MATLAB and Weka. **It is a reimplementation, not the authors'
results.** A gap between it and FASTENER may be a property of the method or an
artefact of the port, and should not be cited as evidence about the published
algorithm.

Ported faithfully: opposition-based initialisation, binary tournament on
(front, crowding), single-point crossover at a differing locus, balanced
mutation, the MI/entropy-weighted forward/backward/interchange improvement phase
over feature clusters, and NSGA-II survival. Two documented departures: the
objective is this experiment's shared metric rather than the paper's g-mean
(so differences reflect the *search*, not the metric), and the budget is the
paper's 10000 fits, which is *more* than FASTENER's ~6000 -- when the porter is
also the reporter, the port should not lose on compute.

### The initialisation problem, and why there is a `_sparse` variant

The source initialises every individual at ~50% density. On the authors' own
manufacturing data (tens of features) that starts near the useful region. At
500-970 features it starts at 250-485 selected features, and the size objective
has to walk all the way down.

In practice the faithful port never produces a subset below ~200 features within
budget, so it is simply **absent** from the small-*k* comparison -- which in a
score table looks like missing data rather than a result. Two things address
that: `subset_size_reach` in the manifest records the smallest subset each
method actually produced, and `nsgaii_miip_sparse` re-runs the identical search
from small random subsets. The pair separates "this search is worse at small
*k*" from "this search started somewhere else".

### Not included

**BGR-FS** (2026) is paywalled with no public code. Implementing it from its
abstract would produce a strawman, so it is omitted rather than guessed at.

### Datasets

| dataset | rows | features | source | why |
|---|---|---|---|---|
| MADELON | 2600 | 500 | UCI | synthetic, XOR-like, 20 relevant / 480 noise, known structure |
| GINA | 3468 | 970 | OpenML 1038 | real-world digit pixels, binary; different origin and noise structure |

GINA is capped near 1000 features on purpose: NSGAII-MIIP builds a full pairwise
mutual-information matrix, which is O(F^2). A 5000-feature set like GISETTE
would need ~12.5M MI computations before the search starts.

### Parallelism

Population searches are independent, so `(method, seed)` tasks are distributed
with joblib (`--jobs`). The MI matrix and feature clustering depend only on the
training data, so they are computed once and shared across all seeds.

```bash
python experiments/run_sota_experiment.py --dataset madelon --jobs 7
python experiments/run_sota_experiment.py --dataset gina --jobs 7
```

Both datasets can run concurrently; at `--jobs 7` each they use 14 cores.

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

## Pruning-swap arms (TODO.md proposal)

FASTENER's pruning step tests deleting its weakest feature but never replacing
it. The swap operator adds that test; see the "Optional: swap operator" section
of `fastener/README.md` for the algorithm. Three arms are available:

| `--swap` | removal of feature *i* | insertion of feature *j* |
|---|---|---|
| `none` (default) | — deletion only, the published algorithm | — |
| `random` | uniformly random selected feature | uniformly random unselected feature |
| `guided` | permutation-weakest, from scores pruning already computed | sampled with probability weighted by mutual information |

`random` is the ablation: it isolates how much of any effect comes from the
guidance rather than from swapping as such.

```bash
# unchanged default -- the published algorithm
python experiments/run_experiment.py

# all three arms, same rounds and seeds
python experiments/run_experiment.py --swap none --swap random --swap guided
```

The arms appear as separate methods (`fastener`, `fastener_swap_random`,
`fastener_swap_guided`) in `comparison.csv`, in the plot and in the significance
table, each with its own `log/` directory and its own fit count.

### Equal budget: `--max-fits`

Equal `--rounds` is **not** equal compute. The swap arms buy one extra model fit
per pruned subset, so at fixed rounds they are simply given more search. Pass
`--max-fits` and every arm stops at the same number of unique model fits:

```bash
python experiments/run_experiment.py     --swap none --swap random --swap guided     --max-fits 6000 --rounds 100000 --seeds 10
```

Set `--rounds` high enough that the budget, not the round count, is what stops
the run; `stopped_on` is printed per seed and stored per run, and reads
`fit_budget` when the cap bound and `rounds` when it did not. Running several
arms without `--max-fits` prints a warning, because the comparison is confounded.

The cap is exact, not per-generation: `Config.max_model_fits` is checked inside
the one function that fits a model, so a generation cannot overshoot it by
however many subsets it happened to contain. What counts as a fit:

| costs budget | does not |
|---|---|
| a subset evaluated for the first time | a subset already in the cache |
| the pruning step's deletion candidate | permutation scoring (it predicts, never fits) |
| every swap candidate | |

### The scalar: hypervolume

A Pareto front is not one number, so arms are also compared by the hypervolume
of the region they dominate — few features (minimised) against test score
(maximised). The reference point is **all features at score 0**, which makes the
all-features solution, i.e. no selection at all, contribute exactly zero.

The absolute value means nothing; only differences against the same reference
point do. `hypervolume.json` holds one row per (arm, seed), and
`arm_comparison.json` the paired comparison of each swap arm against the
published algorithm, matched by seed, reporting both a paired t-test and
Wilcoxon signed-rank. Selection and measurement stay apart: the front is the one
`protocol.pareto_front` picked on validation, scored on the untouched test set.

### What this is not, yet

Fixing the seed count is still open. The runner defaults to 5 seeds, which is
thin for a paired test — with `n=5` the t-test has little power, so an arm can
be genuinely better and still not show it. `--seeds 10` or more is the honest
setting for an arm comparison, and the default is left alone only because it is
shared with the baseline experiment.

A difference between arms is not a result unless every arm stopped on
`fit_budget` and the seed count is stated.

## Tests

```bash
python -m pytest tests -q
```

`tests/test_swap_strategies.py` covers the swap operators and, just as
importantly, that the default path is untouched: the original positional
constructor call, the legacy `purge_item_with_information_gain` contract, and
runs that must not consult the swap machinery at all. The pre/post equivalence
was additionally checked out-of-band against the committed FASTENER clone --
same Pareto front, same model-fit count, same cache-hit pattern.
