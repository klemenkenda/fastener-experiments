# Hypotheses and protocol, fixed before the runs

Written 2026-09-25, before any experiment in this round was started. Nothing
below may be revised after results exist; a revision gets a dated entry at the
bottom saying what changed and why, so that the difference between "what we set
out to test" and "what we found" stays legible.

Hypotheses are numbered in the order they are to be run. Deferred items are
lettered, so they hold no slot in the run order.

## Terms

| term | meaning here |
|---|---|
| **fit** | one training of the classifier on one feature subset. The unit of budget. |
| **arm** | one algorithm configuration compared under identical conditions to the others. One method can be several arms: NSGA-II with OBL and with sparse initialisation are two arms. |
| **run** | one arm on one dataset with one seed. |
| **seed** | the random seed of the *search*. The data split never changes with it. |
| **iteration** | one step of an algorithm's own loop; its meaning differs per algorithm (see *Progress tracking*). |
| **front** | the set of (subset size, score) points an algorithm returns, one best subset per size. |
| **low k** | subset sizes k = 1..10. |

## Why this order

0. **H0 first because every later FASTENER result stands on it.** H2-H6 all run
   FASTENER with three bug fixes the published results did not have (see H0).
   H0 measures what the fixes change before any comparison is built on the
   fixed code. It runs only FASTENER, on five datasets of its own, so it is also
   the first end-to-end check of progress tracking, which its metric depends on
   entirely.
1. **H1 next because it is cheap and diagnostic.** Sparse initialisation keeps
   NSGA-II in small subsets, where fits are cheapest, and the sparse arm has a
   known, undiagnosed failure from the previous round (see H1). H1 also
   exercises the whole protocol end to end. Finding a harness bug here costs
   minutes; finding it in H4 costs days.
2. **H2 before H3** because H2 is H3's control. If a random swap already changes
   the front, the contribution is "FASTENER needed a size-preserving operator",
   not "the guidance is clever" -- and that reading has to be available before
   the guided result is interpreted. The two share arms and run as a single
   invocation; the ordering is about the order they are *read*.
3. **H4 after the swap hypotheses because it is the largest targeted run** --
   25 datasets x 2 arms x 5 seeds -- so it should run on a harness that has
   already produced correct output four times.
4. **H5 and H6 last because they are the full grid** -- every algorithm on every
   dataset. The runs behind H1-H4 are part of that grid and are reused, not
   repeated; H5 and H6 add the remaining algorithm-dataset cells. H5 is read
   before H6, since H6's comparison includes stock FASTENER.

**H2 and H3 are one experiment.** Stock FASTENER, random swap and guided swap
are three arms over the same seeds and the same budget, run together in one
invocation. Running them separately would waste the shared stock arm and, worse,
would let the arms differ by run conditions rather than by operator.

**H0 is an experiment of its own.** Its budgets, and on the Earth-observation
sets its split, differ from the protocol table (see H0). Its `fastener` runs are
therefore not the stock arm of H2 and H3, and are not reused by any later
hypothesis.

## Protocol, fixed for every hypothesis below

| decision | value | note |
|---|---|---|
| Classifier | **`protocol.make_model()`: `DecisionTreeClassifier(random_state=20200)`, scikit-learn defaults** (Gini, `min_samples_split=2`) | The setting the paper states in Section 5.1. Drives every search **and** scores every result, for every method. |
| FASTENER version | **the current code: FASTENER clone `08e6acd`, mating `include_top_genes=True, allow_self_mating=False`** (`run_fastener.MATING_VERSIONS["fixed"]`) | Decided by the PI after H0-E03 (Revisions, 2026-10-07). Every FASTENER arm in H1-H6 -- stock, random swap, guided swap -- runs it. The 2020 mating is run only where an experiment's design names the `fastener_2020` arm. From H2 on the clone is at `b7e724d`, which adds only the pruning counters H2 and H3 report; the search is unchanged (Revisions, 2026-10-09). |
| Seeds | **5: 2020, 2021, 2022, 2023, 2024** | Set by the PI. See *What 5 seeds can and cannot answer*. |
| Budget | **6,000 unique fits per run; 12,000 on the 11 datasets in `protocol.LONG_BUDGET_DATASETS`**, enforced by each method's fit cap | Equal across arms: the budget follows the dataset, not the arm. The 11 had not converged at 6,000 in H0 (Revisions, 2026-09-30). Cached re-evaluations of a subset already fitted are not charged. Wall clock is recorded alongside and reported, never substituted: the two diverged 10x in the pilot. **H2 and H3 set the budget per dataset from a calibration step instead** (see H2; Revisions, 2026-10-09). |
| FS-SDS budget | **k = 1..20, 300 fits per k -- 6,000 in total** (600 per k, 12,000 in total, on the long-budget datasets) | FS-SDS searches one fixed k per run, so its 6,000 are split evenly across the k it runs at. Giving it 6,000 *per k* would hand it 20x the budget of every other arm -- the same kind of mismatch H4 is about. |
| k grid | **1, 2, ..., 20, then 25, 30, 50, 100, 200, 500**, capped at the dataset's feature count | Every integer up to 20 because AUF needs opt(k) at each k. |
| Splits | **stratified 60/20/20 train/validation/test, `SPLIT_SEED = 20200`** | Fixed across seeds. Search and selection use validation; test is read once, for the final score. |
| Row cap | **datasets over 50,000 rows use a fixed stratified 50,000-row subsample** | Drawn once with `SPLIT_SEED`, identical for every arm and seed. Applies to eodata, crop_mapping, covertype, miniboone, higgs and volkert. See *Datasets: cost*. |
| Primary metric | **F1 for classification, MAE for regression** | Set by the PI. Every dataset here is classification, so F1 throughout; the MAE branch is for a future regression task. |
| F1 average | **weighted**, matching `protocol.primary_score` | Binary and macro are computed and stored too -- the paper says only "F1 score", and on a two-class set the choice moves the AUF substantially (see `WHY_RESULTS_DIFFER.md`). |
| Metrics | **compute all of them, every run** | Secondary metrics are for interpretation and are labelled as secondary in any write-up. |
| Pre-registration | this file is committed before the first run | |

### How a single-subset metric becomes a front metric

F1 scores one subset. Every hypothesis compares *fronts*, so each needs an
aggregate built on F1, fixed now:

* **AUF** = (1/K) * sum over k = 1..K of opt(k), where opt(k) is the best test
  F1 among subsets of size <= k (subsets chosen on validation), and **0 where a
  run has no subset of size <= k** -- at that budget it offers nothing. The
  paper's own measure. This is what makes AUF penalise a search that never
  reaches small subsets (H1).
  * **K = 10 -- the primary metric for H1, H2, H3, H5 and H6.** All of them are
    claims about low k, and every falsification criterion below is stated at
    k <= 10, so the metric is read over exactly that range.
  * **K = 20 -- the primary metric for H4**, the aggregate the paper's Table 3
    uses.
  * **H0 reads AUF (K = 10) on validation, at every progress snapshot**, to
    get a curve of the score against fits. See H0 for how the curve becomes a
    convergence measure. Test AUF is still read once, at the end.
* **Hypervolume** = the area dominated by the front in (few features, high F1)
  against a fixed reference point of all-features-at-F1-zero
  (`analysis.hypervolume`). **Secondary** for every hypothesis: it summarises
  the whole front, including the large-k region no hypothesis here is about.

All are functions of F1 alone. None is a new primary metric; they are how the
primary metric is read off a front.

### Why "one classifier" is not negotiable

A wrapper method optimises a subset *for a particular model*. If method A
searches with the model that later grades it and method B does not, A has
home-field advantage and the comparison measures the mismatch, not the search.
In the pilot this bias ran in FASTENER's favour on every arm except Boruta and
`fs_sds_elm`.

Two consequences:

* **Boruta runs on the decision tree**, not the random forest it is normally
  paired with. Boruta is defined over any estimator that exposes feature
  importances, and the tree does. The change is labelled as a departure from
  Boruta's usual configuration.
* **FS-SDS runs on the decision tree**, not the ELM the paper paired it with.
  That is the point of H4.

### What 5 seeds can and cannot answer

5 seeds is enough for:

* a difference that is large relative to the seed spread;
* a directional check (does arm X ever beat arm Y at any k?);
* an effect visible in every seed rather than on average.

It is **not** enough to resolve the differences the pilot actually showed. Pilot
seed spreads at k=500 on gina: stock FASTENER 0.824-0.863, guided swap
0.772-0.853, random swap 0.839-0.850. Arm-to-arm gaps of 0.02-0.03 sit inside
those ranges. A paired test at n=5 will not separate them, and a null result at
this seed count means "not detected at n=5", never "no effect".

Therefore: **no hypothesis is declared confirmed or refuted on a mean difference
alone.** H0 and H1 use a per-seed sign test that 5 seeds can carry. H2-H6
take datasets as the unit instead of seeds, which gives them 39, 25 or 36
observations.
If a result lands in the ambiguous middle, the honest output is "needs more
seeds", and the seed count becomes the finding.

### Pilot data

The previous round was discarded. Its runs are recoverable at commit `3bfce8c`
but are **not evidence**: the comparison they rest on was confounded (a
decision-tree-scored FASTENER against an ELM-scored FS-SDS, at mismatched
budgets) and the arms were separated by less than their own seed spread. They
are used here only as pilot data -- to size this round and to say which
hypotheses already look unpromising.

---

## H0 -- The bug-fixed FASTENER converges faster than the 2020 code

*(first: H2-H6 run the fixed code, and this measures what the fixes change)*

**Claim.** The fixed FASTENER reaches a given low-k score in fewer fits than the
2020 code that produced the published results.

**The three fixes.** All are in the fastener clone's mating step, described in
its README under *Changes to the original mating behaviour*:

1. **Weighted information-gain mating no longer always adds the top genes.**
   `IntersectionMatingWithWeightedRandomInformationGain` started from its parent
   class's child, the intersection plus the top-k genes by mutual information,
   and then sampled k more. The top-k were therefore in every child, a child got
   up to 2k genes back (1.3k on average), and the weighted sample rarely added
   anything new. It now starts from the plain intersection.
2. **An item is no longer mated with itself.** `RandomEveryoneWithEveryone` drew
   its mating pool with replacement. About 13% of pairs at `pool_size=3` were an
   item and itself, and their child was a copy of the parent. The pool is now
   drawn without replacement.
3. **`pool_size=None` no longer crashes.** It is meant to use the whole
   population as the pool.

The harness runs `pool_size=3`, so fix 3 never fires in this round. **H0 tests
fixes 1 and 2**, and any write-up says so. Fix 3 is covered by the clone's unit
tests, not by an experiment.

**Why it might hold.** Under the old fix 1, every mating of the same two parents
returned the same top-k genes, so repeated matings explored little beyond one
greedy child. Children were also larger than the rule intends, which pulls the
search away from low k. Under the old fix 2, a self-mated child is a copy of an
item already scored: it costs no fit, since the cache absorbs it, but it takes a
crossover slot that would otherwise have produced a new subset. Both effects
spend the search's effort on less new ground per fit.

**Why it might not.** Always adding the top genes by mutual information is a
greedy bias toward informative features. That bias can speed the early part of a
search, which is exactly where convergence speed is measured. Removing it could
slow the start and help only later, or not at all. Fix 2 frees generations, not
fits, so under a fit budget its effect may be small.

**Pilot evidence.** None usable. Every pilot FASTENER run used the 2020 mating,
but none was paired with a run of the fixed code, so the pilot holds no
comparison.

**Arms.**

* `fastener` -- the fixed code, with the clone's defaults. This is **stock
  FASTENER in H2-H6**.
* `fastener_2020` -- the same code with `include_top_genes=True` and
  `allow_self_mating=True`. The clone's README states that with both flags set a
  run is identical to the original: the same fits and the same Pareto front for
  the same seed. This arm is the published algorithm, not a variant of it.

Both arms start from the same initial population for a given seed. Their random
streams part at the first mating step.

**Datasets, budgets and splits.** Five datasets, chosen to differ in domain and
shape. Crop mapping is the one Earth-observation set. EOData, madelon and gina
are left out. EOData is replaced by USPS, a much shorter set of handwritten
digit images, which adds a third domain next to the sensor data of har and the
text of BASEHOCK. TOX_171 adds gene expression, the very wide and very short
shape of half the paper's benchmarks. It is the largest class-balanced gene set
on disk; lung has more rows, but one of its classes gets a single validation
row. Madelon and gina are both feature-selection challenge sets and add little
variety next to these.

| dataset | kind | rows | features | rows used: train / validation / test | budget per run |
|---|---|---:|---:|---|---:|
| **crop_mapping** | Earth observation, optical and radar | 325,834 | 174 | 40,000 / 10,000 / 50,000 (EO split, below) | **1,000 fits** |
| **USPS** | handwritten digit images, 16x16 pixels; a paper benchmark | 9,298 | 256 | 5,578 / 1,860 / 1,860 (60/20/20) | **6,000 fits** |
| **har** | smartphone sensor signals, several statistics each | 10,299 | 561 | 6,181 / 2,059 / 2,059 (60/20/20) | **6,000 fits** |
| **BASEHOCK** | text, word features; a paper benchmark | 1,993 | 4,862 | 1,195 / 399 / 399 (60/20/20) | **6,000 fits** |
| **TOX_171** | gene expression, toxicology microarray; a paper benchmark | 171 | 5,748 | 103 / 34 / 34 (60/20/20) | **6,000 fits** |

*Budget.* Crop mapping gets 1,000 fits, the budget of the paper's own EO
setting: Table 2 reports FASTENER at 1,000 model evaluations on EOData, and its
AUF progress curve (Figure 9) has mostly levelled off within the first 800. Fits
on crop mapping are also the most expensive in H0. The other three get the
protocol's 6,000 fits. They are cheap to fit, and FASTENER on the
paper's non-EO benchmarks ran for 11,000-17,000 evaluations, so they are not
expected to settle as early. Each dataset is judged on its own, so budgets can
differ between datasets. Within a dataset both arms always get the same budget.

*EO split.* From crop mapping, a stratified subsample of 100,000
rows is drawn once with `SPLIT_SEED`. It is halved, stratified, into 50,000
**search** rows and 50,000 **test** rows. The search rows are split 80/20,
stratified, into training and validation, the paper's 80:20 ratio. The search
reads only training and validation. The 50,000 test rows are read once, at the
end. The subsample keeps each class's share; the smallest class has about 175
rows in each half.

*Departures from the protocol table,* stated wherever H0 is reported: the
1,000-fit budget on crop mapping, and the EO split in place of the 50,000-row
cap and the 60/20/20 split. USPS, har, BASEHOCK and TOX_171 run under the protocol as
written.

*Cost.* One decision-tree fit, measured on this machine, and one run at the
budget above. The range runs from all fits at 20 features to all at 100. Crop
mapping's fit times are scaled up from the 30,000-row training split measured to
the 40,000 rows of the EO split.

| dataset | one fit, 20 / 100 features | one run | H0 on it: 10 runs in series |
|---|---|---|---|
| crop_mapping | 1.0 / 6.1 s | 17 min to 1.7 h | 3 to 17 h |
| USPS | 0.14 / 0.67 s | 14 min to 1.1 h | 2.3 to 11 h |
| har | 0.11 / 0.59 s | 11 min to 1 h | 2 to 10 h |
| BASEHOCK | 0.002 / 0.016 s | about 3 min | about 30 min |
| TOX_171 | 0.002 / 0.004 s | about 3 min | about 30 min |

On the two very wide sets the fit is not the cost. A smoke run on TOX_171 spent
17 s once, computing mutual information over all 5,748 features, then about
0.02 s per fit of FASTENER's own work. The rows above for BASEHOCK and TOX_171
use that measured rate.

*TOX_171 is noisy by construction.* Its validation split has 34 rows, 8 or 9
per class, so one row moves F1 by about 0.03 and many subsets tie. The curve
moves in coarse steps, and both arms can reach the target at the same snapshot.
Such a seed is a tie under the criterion below. See *What the small sets can
support*.

**Primary metric: fits to a common target.** A fixed-target measure, read on
fits as *Progress tracking* requires, and on validation only:

1. From every progress snapshot, compute AUF (K = 10) on validation F1 from the
   front the snapshot stores. Over a run this gives a step curve of score
   against cumulative unique fits.
2. Per dataset and seed, the **target** is the lower of the two arms' final
   values at that dataset's budget. Both arms reach it by construction.
3. Each arm's result is the cumulative unique fits at the first snapshot whose
   value is at or above the target. Fewer fits is faster.

A common target keeps the comparison about speed. An arm's own final value
would not work: a search that stalls early would look like it converged fast.

**Falsification criterion.** H0 is supported if `fastener` reaches the target in
**fewer fits** than `fastener_2020` in **at least 4 of 5 seeds**, on **crop
mapping and on at least one of the other four datasets**. H0 does not run on
EOData, so its result is not a statement about FASTENER's own dataset. An equal fit count is a tie and
does not count toward the 4. Otherwise H0 is not supported. If `fastener_2020`
meets the same criterion instead, the fixes slowed convergence, and that is
recorded as the finding.

**Reported beside it, as secondary:**

* the area under the validation curve over the whole budget, which combines
  speed and level in one number;
* final test AUF (K = 10), AUF (K = 20) and hypervolume, to show whether faster
  convergence cost the end result;
* generations reached and wall clock, because fix 2 changes how many new
  subsets a generation produces.

A faster arm that ends lower on test AUF (K = 10) is reported as a trade-off,
not as a better algorithm.

**What H0 does not decide.** H2-H6 use the fixed code whatever H0 finds. That
choice is fixed here, before any result, so the baseline cannot follow the
outcome. The fixes correct behaviour the code did not intend. H0 measures what
that correction costs or gains, and does not decide whether to make it.

**Consequence for H4.** The paper's Table 3 was produced by the 2020 code. H4's
FASTENER arm therefore differs from the published one in these fixes as well as
in the protocol. H0 measures the fixes on five datasets, three of which, USPS,
BASEHOCK and TOX_171, are among the 25 benchmarks. If H0 finds a large effect, the H4
write-up states it next to the ordering result.

**Experiments.** Designs, runs and reports in [`EXPERIMENTS.md`](EXPERIMENTS.md).

* `H0-E01` -- the five datasets and the criterion above. Not supported.
* `H0-E02` -- the 31 other datasets, datasets as the unit (Wilcoxon over
  per-dataset effects). Supported, narrowly.
* `H0-E03` -- all 36 datasets, with the fixed arm keeping the top genes, so it
  differs from the 2020 code only in no self-mating; 12,000 fits on the 11
  long-budget datasets. Not supported.

## H1 -- NSGA-II's weakness at small k is an initialisation artifact

*(second: cheap, and it shakes out the rest of the harness)*

**Claim.** NSGA-II trails at small feature counts because of where it starts,
not because the search is worse.

**Why.** `obl_initialization` builds complementary pairs, so every individual
starts at ~50% density -- ~485 of gina's 970 features. `balanced_mutation`
equalises expected additions and deletions by construction, so subset size is a
zero-drift random walk and only selection pulls it down.

**Pilot evidence, and it is unusually strong.** An operator-only simulation --
the real operators, no model fits, the score objective replaced by a fixed
random value, which *removes* the pressure that fights size reduction -- reached
a minimum subset size of 332 after 63 generations on gina. The real run reached
333. Ten times the budget reached only 108. The size floor is therefore operator
dynamics, with essentially no contribution from the data or the objective.

**Arms.** `nsga2` (OBL initialisation, as ported) and `nsga2_sparse` (random
subsets of 1-30 features at initialisation). The sparse arm is a **departure
from the source** and is labelled as one everywhere; it is a controlled variant,
not the published algorithm.

**Datasets.** Eight, chosen to spread the feature count p over three orders
of magnitude, because the claim turns on it: OBL starts at about p/2 features,
so the handicap it predicts grows with p.

| dataset | features | rows | domain | role |
|---|---:|---:|---|---|
| satimage | 36 | 6,430 | Landsat land cover | both arms start at about 15-18 features, so the claim predicts no difference |
| eodata | 182 | 50,000 of 480,000 | Sentinel-2 land cover | the primary dataset |
| USPS | 256 | 9,298 | handwritten digits | |
| har | 561 | 10,299 | smartphone sensor statistics | built like EOData: signals x statistics |
| COIL20 | 1,024 | 1,440 | object images | |
| gisette | 5,000 | 7,000 | handwritten digits | large p with many rows |
| Prostate_GE | 5,966 | 102 | gene expression | wide and short |
| arcene | 10,000 | 200 | mass spectrometry | 12,000 fits (`protocol.LONG_BUDGET_DATASETS`) |

Crop mapping, madelon and gina, the other development sets, are not used:
their feature counts (174-970) fall inside the range EOData, har and COIL20
already cover.

**Primary metric.** AUF, K = 10. Reported beside it, as the diagnostic quantity
this hypothesis is about: the smallest subset size on the front, per seed.

**Falsification criterion.** H1 is supported if `nsga2_sparse` has a higher
AUF (K = 10) than `nsga2` in **at least 4 of 5 seeds**, on **EOData and on at
least one other of the eight datasets**. Otherwise it is not supported. If the
sparse arm reaches small subsets and still fails that test, the weakness is the
search after all -- the more interesting outcome for H5 and H6. The result on
each dataset is reported against its feature count; satimage, where the claim
predicts no difference, is reported as such and is not excluded from the count.

**Blocker to clear first.** The sparse arm was launched once in the previous
round and produced nothing; both of its log files were zero bytes. Whatever
failed there must be diagnosed before the arm counts for anything. This is the
main reason H1 runs first.

**Experiments.** Designs, runs and reports in [`EXPERIMENTS.md`](EXPERIMENTS.md).

* `H1-E01` -- the eight datasets and the criterion above. Stopped after 13
  minutes, on EOData only, so the experiment could be restarted with
  per-job monitoring; no result was read. Failed.
* `H1-E02` -- the same design, restarted. Supported: the sparse start won 5 of
  5 seeds on EOData and on every dataset with 182 features or more, because
  the OBL start never reached k <= 10 there; on satimage the OBL start was
  slightly ahead. Neither start's front left the size range it began in.

## H2 -- A size-preserving move changes the front at all, guided or not

*(third: the control for H3; shares a run with it)*

**Claim.** Adding *any* size-preserving swap to FASTENER's pruning step improves
its front at low k, relative to stock FASTENER.

**Why it comes before H3.** H2 is the weaker, more defensible claim, and it is
the ablation that isolates guidance: if random swap also helps, the contribution
is "FASTENER needed a size-preserving operator", not "the guidance is clever".
If neither helps, H3 cannot be true for the reason H3 gives.

**Pilot evidence.** Null. Random swap averaged 0.7956 over the gina k-grid
against stock's 0.7960 -- a difference of 0.0004, far inside seed spread.

**Arms.** `fastener` (stock) and `fastener_swap_random`.

**Datasets: 39 -- 38 of the 39 UCR/UEA sets of
[`DATASETS_USED.md`](DATASETS_USED.md), and EOData.** *(Revised twice on
2026-10-09, both times before any H2 or H3 run; see Revisions.)* A claim that FASTENER lacks an
operator is a claim about FASTENER on any data, so it is tested over as wide a
range of dataset shapes as is to hand. The 39 were chosen by clustering the
whole UCR/UEA archive on examples x features and taking datasets from each of
the seven clusters: n from 40 to 24,000, p from 16 to 192,000. EOData is
added because it is the setting FASTENER was built for. DuckDuckGeese, the
39th, is left out: at 363,150 features a FASTENER run costs hours more than
any other set, for reasons that have nothing to do with the swap. See *Datasets: time
series classification*.

**Fit budget: per dataset, from a calibration step.** *(Revised 2026-10-09.)*
The budget follows the dataset, as in the protocol, and is the same for every
arm; what changes is how it is set. A dataset whose search has stopped
improving gains nothing from more fits, and one that has not needs them.
Before the experiment, on every dataset, with seed 1999 (not one of the five
experiment seeds) and validation only:

1. **Boruta** (on the protocol decision tree), one run. Its validation AUF
   (K = 10) is the accuracy reference: a budget at which FASTENER has not
   reached what a filter reaches is too small.
2. **Stock FASTENER**, one run capped at 12,000 fits, recording its
   validation AUF (K = 10) after every generation.
3. The budget is the smallest **b** in {1,000, 2,000, 4,000, 6,000, 12,000}
   at which the calibration run's validation AUF (K = 10) is (i) within 0.005
   of its value at 12,000 and (ii) no lower than Boruta's minus 0.005, **then
   one step up the grid** (capped at 12,000), because a swap arm may still be
   improving where stock FASTENER has stopped. A dataset where no b below
   12,000 meets both conditions runs at 12,000 and is flagged as possibly
   unconverged. 0.005 is H0's convergence threshold.

The budgets are written into the experiment's design before any of its runs
starts. Calibration runs are not evidence for H2 or H3 and are not pooled with
their runs. Test scores play no part.

**Primary metric.** AUF, K = 10, on test.

**Falsification criterion: datasets as the unit.** *(Revised 2026-10-09; it
replaces the per-seed rule on EOData and one other development set.)* Per
dataset, the effect is the mean over the 5 seeds of AUF(`fastener_swap_random`)
minus AUF(`fastener`). H2 is **supported** if the effect is positive on more
datasets than negative **and** a two-sided Wilcoxon signed-rank test over the
per-dataset effects is significant at alpha = 0.05. **Reversed** -- the swap
makes FASTENER worse -- if the same holds with the signs swapped. Otherwise
**not supported**: no consistent difference over these datasets. Datasets
with a zero effect drop out of the test, as the Wilcoxon test requires, and
their count is reported.

A null here with a positive H3 would be the interesting outcome (the guidance
is doing the work); a null in both is the likely one given the pilot.

**Incomplete datasets.** A dataset whose runs fail, or that has fewer than 5
seeds for either arm when the experiment is stopped, is left out of the test
and listed. If more than 6 of the 39 are left out, the result is reported as
incomplete rather than as a verdict.

**Reported beside it, as secondary:**

* the per-dataset 4-of-5-seeds count, for every dataset;
* **EOData on its own**, with its 4-of-5 count. It no longer decides the
  verdict, but a result that does not hold there is said to not hold in
  FASTENER's own setting;
* the effect per cluster, C1-C7 -- descriptive only, since 3-7 datasets per
  cluster cannot carry a test;
* the effect against p and against n, since the swap's share of all fits
  depends on both;
* **what the swap did**, from the pruning counters (FASTENER `b7e724d`): swaps
  proposed, swaps that cost a fit, swaps that won their size slot, and
  final-front entries a swap made, per arm and dataset. A null in which swaps
  rarely won says something different from one in which they won often and
  changed nothing;
* hypervolume, and final test AUF per arm.

## H3 -- The guided swap improves FASTENER at small k

*(fourth: read after its control, though it runs in the same invocation)*

**Claim.** Replacing a subset's weakest feature (by the permutation scores
FASTENER already computes) with a feature sampled by mutual information (the
vector `IntersectionMatingWithInformationGain` already computes) produces a
better front at low k, under an equal fit budget, than stock FASTENER.

**Why it might hold.** No FASTENER operator preserves subset size. Mating pulls
a child toward the middle of its parents' sizes; pruning strictly decreases.
Only mutation can hold size constant, and only by flipping two bits at once --
probability ~k(d-k)/d^2, about 0.047 for k=10 of d=200. Same-size exploration is
a second-order event with no operator behind it.

**Pilot evidence, and it points the wrong way.** On gina the guided arm was
*behind* stock FASTENER from k=20 outward (0.817 vs 0.844 at k=500) and ahead
only at k=2 (0.766 vs 0.748). Its seed spread was also the widest of the three
arms. This hypothesis enters the round with evidence against it.

**Arms.** `fastener` (stock) and `fastener_swap_guided`. Shares the stock arm
with H2.

**Datasets, budget, metric, incomplete datasets and secondary reporting.**
H2's, unchanged: the same 39 datasets, the same calibrated budgets, AUF
(K = 10) on test. *(Revised 2026-10-09, with H2.)*

**Falsification criterion.** H2's, with `fastener_swap_guided` in place of
`fastener_swap_random`: the per-dataset effect is the mean over 5 seeds of
AUF(`fastener_swap_guided`) minus AUF(`fastener`), and H3 is supported if it is
positive on more datasets than negative and a two-sided Wilcoxon signed-rank
test over them is significant at alpha = 0.05. *(Revised 2026-10-09.)*

**Reading H3 against H2.** The guidance is credited only where H3 holds and
the guided arm also beats the random-swap arm: the per-dataset effect
AUF(`fastener_swap_guided`) minus AUF(`fastener_swap_random`), tested the same
way, is reported as secondary. If H2 and H3 both hold and that difference does
not, the result is "FASTENER needed a size-preserving move", not "the guidance
helps".

**Prior art, which narrows the claim.** FS-SDS's diffusion move is already a
size-preserving swap: copy a good agent's subset, drop one selected feature at
random, add one unselected at random (Alhakbani & al-Rifaie 2017, the FASTENER
paper's own reference [12]). The operator is not novel. What has no precedent
found so far is guiding *both* ends from quantities FASTENER already computes.
Any write-up states this.

## H4 -- The published FASTENER > FS-SDS ordering does not survive a clean protocol

*(fifth: the largest targeted run, on a harness already proven four times)*

**Claim.** Run FASTENER and FS-SDS with the same classifier driving both
searches and the same total fit budget, and the paper's headline ordering --
FASTENER ahead on 24 of 25 benchmarks -- does not reproduce.

**Why.** Table 3 compares a decision-tree-scored FASTENER against an ELM-scored
FS-SDS (Koprivec, Kenda & Sircelj 2020, Section 5.1, stated verbatim there), at
30,000 evaluations per k for FS-SDS against FASTENER's ~11,000-16,000 total. Two
confounds, stacked. The published claim is therefore partly a statement about
decision trees versus ELMs on these data, not purely about the two searches.

**Pilot evidence.** The ordering flipped: tree-driven FS-SDS beat FASTENER on 11
of 14 finished datasets, at a fifth of the paper's FS-SDS budget.

**Arms.** `fastener` and `fs_sds`, both on the decision tree, both at 6,000
fits in total (FS-SDS as 300 per k over k = 1..20).

**Datasets.** The 25 paper benchmarks.

**Primary metric.** AUF, K = 20 -- the aggregate of the paper's Table 3. Values
are not directly comparable with the published ones, because this round splits
60/20/20 and selects on validation where the paper selected on its test split.
H4 is therefore a claim about the **ordering**, not the absolute values. The
mean absolute difference against Table 3 (`paper_tables.compare`,
`mean_abs_delta`) is reported as a secondary measure of how far the protocol
moves the numbers.

**Falsification criterion.** Per dataset, each arm's score is its mean AUF over
the 5 seeds. H4 is **supported** if FS-SDS scores higher on more of the 25
datasets than FASTENER does, **and** a Wilcoxon signed-rank test over the 25
per-dataset differences favours FS-SDS at alpha = 0.05. If the test is
significant in FASTENER's favour, the published ordering reproduces and H4 is
refuted. If it is not significant either way, the clean protocol makes the two
methods comparable -- itself a finding, reported as such rather than as a flip.

**Note on scope.** This is a correction to a paper the PI co-authored, and is
framed as such: a confound identified and measured, not a defect claimed.

## H5 -- Stock FASTENER is the best selector at low k, across all datasets

*(sixth: the full grid)*

**Claim.** With every algorithm run on every dataset under the one protocol,
stock FASTENER achieves a better low-k score than each of the other algorithms.

**Why it is worth testing.** The paper compared FASTENER against a handful of
methods, on some datasets each, under per-method classifiers. This is the
general claim those comparisons point towards, tested once, on one protocol,
against the full set of selectors in this repo.

**Algorithms.** FASTENER (stock, random swap, guided swap), NSGA-II (OBL and
sparse initialisation), NSGAII-MIIP, POSS, FS-SDS, mRMR, ReliefF, HSIC Lasso,
Boruta, RFE, the mutual-information, ANOVA-F and tree-importance rankers, and
random subsets. **All features** is run as a reference line only: it has no
subset of size <= 10, so it has no AUF (K = 10) and takes no part in the
pairwise tests.

**Datasets.** All 36: the four development sets, the seven other tall datasets
and the 25 paper benchmarks.

**Primary metric.** AUF, K = 10. Per dataset, an algorithm's score is its mean
over the 5 seeds.

**Analysis: pairwise.** Stock FASTENER is compared against each other algorithm
in turn, over the datasets on which both were run:

* wins, ties and losses across those datasets;
* a Wilcoxon signed-rank test on the per-dataset score differences, with Holm
  correction across the pairs, at alpha = 0.05.

Datasets, not seeds, are the unit of this test, so 36 datasets give it power
that 5 seeds alone could not.

**Falsification criterion.** H5 is supported if stock FASTENER has more wins
than losses against **every** other algorithm, and the difference is significant
after Holm correction against each. Losing any single pairwise comparison, or
failing significance in any, refutes the claim as stated. The pairwise results
then show where FASTENER stands relative to each method on its own.

## H6 -- The guided-swap FASTENER is the best selector at low k, across all datasets

*(seventh: read after H5, on the same grid)*

**Claim.** Under the same grid and protocol as H5, the guided-swap variant of
FASTENER achieves a better low-k score than each of the other algorithms --
including stock FASTENER.

**Why it is separate from H5 and H3.** H3 asks whether the guided swap improves
on stock FASTENER on the four development sets. H6 asks whether it is the best
option available, against every method, on every dataset. H5 and H6 can split:
stock FASTENER can lead the field while the guided variant does not, which is
what the gina pilot suggested, or the reverse.

**Algorithms, datasets, primary metric.** As H5.

**Analysis.** As H5, with guided-swap FASTENER in place of stock FASTENER as the
algorithm every other one is compared against.

**Falsification criterion.** As H5: more wins than losses, significant after
Holm correction, against **every** other algorithm including stock FASTENER.

---

## Deferred, deliberately

**D1 -- the replication gap is a grading artifact.** `WHY_RESULTS_DIFFER.md`
already reconciles FASTENER to +0.026 via `min_samples_leaf=2` plus binary F1,
and leaves FS-SDS unexplained. H4 is framed as an ordering claim so that it does
not depend on D1; if H4's result is to be stated in absolute terms, D1 comes
back.

**D2 -- conclusions are model-dependent.** Out of scope. The pilot measured the
size of what is being set aside: on gina, HistGradientBoosting scored +0.06 at
k=10 and +0.12 at k=400 over the decision tree, and at k=400 it beat the
all-features decision-tree baseline by 0.099. Every result in this round is
therefore a statement about decision trees, and says so.

---

## Datasets

Seventy-five datasets are on disk under `data/`, each checksum-pinned by its
download script, all classification, and all used in this round: the 36 below,
and the 39 UCR/UEA time series sets, 38 of which H2 and H3 run on (see *Time
series classification*). Every one loads
through `datasets.load(name)` and is split as the protocol table states. Shapes
below are measured from the files, not transcribed, and are the full datasets
before the row cap. "Smallest class" is counted after cleaning (see *Dropped
rows*).

### Development sets -- used by H5 and H6

H1 uses EOData and seven other datasets, chosen by feature count (see H1). H2
and H3 use EOData and 38 of the 39 time series sets (Revisions, 2026-10-09).

| dataset | rows | features | classes | smallest / largest class | domain | source |
|---|---:|---:|---:|---|---|---|
| **eodata** | 480,000 | 182 | 24 | 20,000 / 20,000 | Sentinel-2 land patches, Slovenia 2017: 10 spectral signals (raw bands and vegetation indices), each summarised by 18 temporal statistics over the season, plus DEM height and inclination | Šircelj, Kenda & Koprivec, PANGAEA 2020, [doi:10.1594/PANGAEA.914271](https://doi.org/10.1594/PANGAEA.914271) |
| **crop_mapping** | 325,834 | 174 | 7 | 1,143 / 85,074 | Cropland, Manitoba 2012: RapidEye optical and UAVSAR polarimetric radar on two dates in July, with spectral, textural and polarimetric features | UCI 525, [doi:10.24432/C5G89D](https://doi.org/10.24432/C5G89D), CC BY 4.0 |
| madelon | 2,600 | 500 | 2 | 1,300 / 1,300 | synthetic: 5 informative features, 15 linear combinations of them, 480 noise | NIPS 2003 feature selection challenge, UCI |
| gina | 3,468 | 970 | 2 | 1,705 / 1,763 | handwritten digit pixels, even vs odd two-digit number | agnostic learning challenge, OpenML 1038 |

**EOData is the primary dataset.** It is the benchmark FASTENER was designed
for and evaluated on in the paper, so a result about FASTENER's operators that
does not hold there is not a result about FASTENER in its own setting.
**Crop mapping is the second Earth-observation set**: same task family (crop
and land-cover classes from satellite features), same tall shape, a different
sensor pair, region and year, and no connection to the paper. A result that
holds on EOData but not on crop mapping is a result about EOData, not about
Earth observation. Madelon and gina are the controls around them: madelon's
structure is known, so a selector can be checked against the planted
informative features, but it is synthetic; gina is real-world but its relevant
features are unknown. A result that holds on some of the four and not the
others is reported as such.

**EOData's split is random stratified, not spatial.** A spatial split, blocked
by parcel or location, would be the right protocol for pixel samples, since
neighbouring pixels of one field are near-duplicates and leak across a random
split. The published table carries no parcel identifier or coordinate -- all 182
columns are features -- so there is nothing to block on. The random split is
the paper's own choice and the only one available; results on EOData are
therefore optimistic in the same way the paper's are, and are reported with that
caveat. The same holds for crop mapping.

### Other tall datasets -- used by H5 and H6

The 25 paper benchmarks are almost all wide and short. On its own that would
make H5 and H6 a comparison on the shape FASTENER was *not* built for. These
seven fill the gap: many rows relative to features, like EOData, from a spread
of domains. Downloaded and checked against each repository's stated shape by
`download_tall_datasets.py`; loaded by `datasets.load_tall`.

| dataset | rows | features | classes | smallest / largest class | domain | source |
|---|---:|---:|---:|---|---|---|
| covertype | 581,012 | 54 | 7 | 2,747 / 283,301 | Forest cover type, Roosevelt National Forest, Colorado: elevation, slope, distances to water and roads, wilderness area and soil type | OpenML 1596 |
| miniboone | 130,064 | 50 | 2 | 36,499 / 93,565 | Particle identification, MiniBooNE neutrino experiment: electron vs muon neutrino events | OpenML 41150 |
| higgs | 98,049 | 28 | 2 | 46,223 / 51,826 | Higgs boson signal vs background: 21 low-level kinematic and 7 derived high-level features | OpenML 23512 |
| volkert | 58,310 | 180 | 10 | 1,361 / 12,806 | ChaLearn AutoML challenge set, anonymised features; the same feature count as EOData, as a domain-neutral control | OpenML 41166 |
| gas_drift | 13,910 | 128 | 6 | 1,641 / 3,009 | Chemical gas identification: 16 metal-oxide sensors x 8 features each, over 36 months | OpenML 1476 |
| har | 10,299 | 561 | 6 | 1,406 / 1,944 | Human activity recognition: time- and frequency-domain statistics of smartphone accelerometer and gyroscope signals | OpenML 1478 |
| satimage | 6,430 | 36 | 6 | 625 / 1,531 | Landsat multispectral land cover: 4 bands over a 3x3 pixel neighbourhood | OpenML 182 |

Two of these -- har and gas_drift -- are built the way EOData is: a set of
signals, each summarised by several statistics. That is where FASTENER's
redundancy-aware pruning should matter most, and where a result on EOData
should carry over if it is about the method rather than the dataset.

Satimage is a third Earth-observation set, but a small one; it is here for
H5 and H6, not as a development set.

### Paper benchmarks -- used by H4, H5 and H6

The 25 sets of the FASTENER paper's Table 1, from scikit-feature
(`data/paper_benchmarks/*.mat`). Grouped by domain; within a group, by rows.

**Gene expression and other biological assays** -- wide and very short:

| dataset | rows | features | classes | smallest / largest class |
|---|---:|---:|---:|---|
| GLIOMA | 50 | 4,434 | 4 | 7 / 15 |
| nci9 | 58 | 9,712 | 8 | 5 / 9 |
| colon | 62 | 2,000 | 2 | 22 / 40 |
| ALLAML | 72 | 7,129 | 2 | 25 / 47 |
| leukemia | 72 | 7,070 | 2 | 25 / 47 |
| lung_discrete | 73 | 325 | 7 | 5 / 21 |
| GLI_85 | 85 | 22,283 | 2 | 26 / 59 |
| lymphoma | 88 | 4,026 | 6 | 6 / 46 |
| Prostate_GE | 102 | 5,966 | 2 | 50 / 52 |
| CLL_SUB_111 | 111 | 11,340 | 3 | 11 / 51 |
| TOX_171 | 171 | 5,748 | 4 | 39 / 45 |
| lung | 203 | 3,312 | 5 | 6 / 139 |

**Mass spectrometry:**

| dataset | rows | features | classes | smallest / largest class |
|---|---:|---:|---:|---|
| arcene | 200 | 10,000 | 2 | 88 / 112 |

**Face and object images:**

| dataset | rows | features | classes | smallest / largest class |
|---|---:|---:|---:|---|
| orlraws10P | 100 | 10,304 | 10 | 10 / 10 |
| warpAR10P | 130 | 2,400 | 10 | 13 / 13 |
| Yale | 165 | 1,024 | 15 | 11 / 11 |
| warpPIE10P | 210 | 2,420 | 10 | 21 / 21 |
| ORL | 400 | 1,024 | 40 | 10 / 10 |
| COIL20 | 1,440 | 1,024 | 20 | 72 / 72 |

**Handwriting and speech:**

| dataset | rows | features | classes | smallest / largest class |
|---|---:|---:|---:|---|
| Isolet | 1,560 | 617 | 26 | 60 / 60 |
| gisette | 7,000 | 5,000 | 2 | 3,500 / 3,500 |
| USPS | 9,298 | 256 | 10 | 708 / 1,553 |

**Text:**

| dataset | rows | features | classes | smallest / largest class |
|---|---:|---:|---:|---|
| RELATHE | 1,427 | 4,322 | 2 | 648 / 779 |
| PCMAC | 1,943 | 3,289 | 2 | 961 / 982 |
| BASEHOCK | 1,993 | 4,862 | 2 | 994 / 999 |

### Time series classification -- used by H2 and H3

Thirty-nine datasets from the UCR/UEA archive, chosen 2026-10-07 by clustering
all 190 of its datasets on log examples and log features (k-means, k = 7) and
taking seven from each of C1, C3, C4 and C5, five from C2 and three from each
of C6 and C7. The clusters, the selection and the reasons for each pick are in
[`DATASETS_USED.md`](DATASETS_USED.md); downloaded, pinned and checked against
the archive's table by `download_tsc_datasets.py`, loaded by
`datasets.load_tsc`.

| cluster | shape | datasets | n | p |
|---|---|---:|---|---|
| C1 | small lab sets, p >= n | 7 | 40-461 | 286-618 |
| C2 | high-dimensional recordings, p >> n | 5 | 100-440 | 24,705-363,150 |
| C3 | long physiological and device signals | 7 | 360-1,420 | 720-5,376 |
| C4 | short series, mid-sized, n >> p | 7 | 360-1,162 | 24-235 |
| C5 | larger sensor, motion and shape sets | 7 | 4,307-9,236 | 140-1,024 |
| C6 | large audio and industrial sensor sets | 3 | 6,668-13,640 | 2,387-8,928 |
| C7 | very many, very short series | 3 | 10,992-24,000 | 16-96 |

* **One row is one series.** Its time points are the features, channel by
  channel for a multivariate set; a feature subset is a set of (channel, time)
  points. Neighbouring time points are strongly correlated, which is the
  redundancy a feature selector is meant to cut.
* **The archive's train/test split is not used.** The two halves are merged
  and split 60/20/20 like every other dataset, so the protocol is the same
  everywhere. Published accuracies on these sets are on the archive's split
  and are not comparable with ours.
* **None needs the row cap**; Crop, the largest, has 24,000 rows. No class
  falls under the 5-row minimum.
* **The smallest are very small.** BeetleFly's test split is 8 rows, Coffee's
  11, OliveOil's smallest class has 2 rows in validation and test. *What the
  small sets can support* applies to them as to the paper benchmarks.
* **Two corrections to the selection were made at download** (2026-10-09,
  before any run): Epilepsy has 206 time steps, not the 207 the archive's
  table states; UWaveGestureLibrary is served with 440 rows, not 4,479, and
  was replaced by UWaveGestureLibraryAll (4,478 x 945), which has the C5
  shape the pick was made for. See `DATASETS_USED.md`.
* **DuckDuckGeese is not used by H2 and H3** (2026-10-09, see Revisions). It
  stays downloaded and loadable; C2 is represented in H2 and H3 by its other
  four, 24,705 to 192,000 features.

### Dropped rows

A class with fewer than 5 rows cannot survive a 60/20/20 split -- it rounds to no
validation and no test rows, so it would sit in training and never be scored,
which distorts weighted F1. Such classes are dropped at load time and the drop
is recorded on the `Dataset`. Two sets are affected: **lymphoma** loses 8 rows
(96 -> 88) and **nci9** loses 2 (60 -> 58).

Rows with a missing value are removed at download. Only **higgs** has any: it
loses 1 row (98,050 -> 98,049), which held all 9 of its missing values.

Results on these sets are on the cleaned data and are labelled as such.

### What the small sets can support

Twelve of the 25 paper benchmarks have fewer than 110 rows. At 60/20/20,
GLIOMA's test split is 10 rows and colon's is 13; one row changing class moves
the score by 0.08-0.10. The split is fixed, so the seed spread on these sets is
the *search's* variance, not the split's -- a narrow spread on 10 test rows is
not evidence of a stable result, and is not reported as one.

### Cost, and the row cap

One decision-tree fit on 20 features over the training split, measured on this
machine, and what the 6,000-fit budget costs per run at that rate:

| dataset | full size: one fit | full size: per run | at the 50,000-row cap: one fit | at the cap: per run |
|---|---:|---:|---:|---:|
| eodata | 14.2 s | ~24 h | 1.2 s | ~2.0 h |
| crop_mapping | 8.5 s | ~14 h | 0.7 s | ~1.2 h |
| covertype | 4.2 s | ~7 h | 0.2 s | ~0.3 h |
| miniboone | 2.8 s | ~4.6 h | 0.9 s | ~1.4 h |
| higgs | 1.5 s | ~2.5 h | 0.7 s | ~1.2 h |
| har, gas_drift, volkert, satimage | 0.06-0.17 s | under 20 min | -- | -- |

At full size, H1-H3 alone would take roughly 24 h x 5 arms x 5 seeds on EOData.
The cap brings every run under about two hours while keeping enough data for
the scores to mean something: EOData at 50,000 rows keeps ~2,080 rows per class,
~420 of them in each class's test split. A cap of 20,000 rows was measured too,
and is three times cheaper again, but would leave EOData with ~830 rows per
class.

Consequences, stated once here and carried in every result:

* On EOData the capped run is **not the paper's setting**, which used all
  480,000 rows. Results are labelled with their row count.
* The subsample is drawn once and is the same for every arm and seed, so it is
  part of the dataset, not a source of variance between arms. For EOData, which
  is class-balanced, it takes an equal number per class; for the others,
  which are not, it keeps each class's share (`datasets.load_tall(max_rows=)`).

---

## Before the first run

What the harness must do for this protocol to hold, checked against the code as
it stands. Items marked **to build** block the hypothesis named.

| requirement | status | blocks |
|---|---|---|
| Every dataset loads through `datasets.load(name)` | done -- all 36 | -- |
| `load_eodata` and `load_tall` take `max_rows` | done | -- |
| The runner passes the 50,000-row cap to the loader | done -- `run_sota.py --max-rows`, default `protocol.ROW_CAP` | -- |
| One classifier: every method uses `protocol.make_model()` | done | -- |
| Boruta runs on the decision tree | done -- `sota_baselines.TreeForBoruta` | -- |
| 6,000-fit cap on every search, **exact** | done -- NSGA-II and NSGAII-MIIP used to overshoot by up to a generation (386 fits against a cap of 300 in a smoke run); they now drop offspring past the cap unevaluated | -- |
| FS-SDS gets 6,000 in total, 300 per k over k = 1..20 | done -- the runner divides the budget over `protocol.FS_SDS_K_RANGE` | -- |
| k grid includes every k from 1 to 20 | done -- `protocol.K_GRID`, used by every runner | -- |
| AUF computed from the front at every k <= K | done -- `analysis.auf`, written per method and seed to `auf.csv` under every metric; a test keeps it identical to `make_report.auf` | -- |
| Best score per iteration recorded for every algorithm | done -- `trajectory.py`, one `trajectories/<method>_seed<seed>.jsonl` per run, each snapshot storing its front | -- |
| `nsga2_sparse` produces output | done -- the algorithm was never broken; the empty logs came from how it was launched. It is now its own method, so H1 runs both arms in one invocation. Its initialisation also crashed on datasets under 30 features (higgs has 28); fixed | -- |
| Seeds 2020-2024 | done -- `run_sota.py` uses `2020 + i` | -- |
| One runner covers every algorithm H5 and H6 compare | done -- `run_sota.py` now also runs the three rankers, RFE, random subsets and all features | -- |
| Binary and macro F1 stored beside weighted | done -- `protocol.all_scores` | -- |
| The mating fixes committed in the fastener clone | done -- clone commit `564eb8a`, working tree clean | -- |
| A `fastener_2020` arm: `include_top_genes=True`, `allow_self_mating=True`, with its own algorithm ID | done -- `run_sota.py --fastener-arm 2020`, built by `run_fastener.make_mating("2020")` | -- |
| Validation AUF (K = 10) per snapshot, and fits to the common target | done -- `h0_convergence.py` reads the runs' trajectories and applies H0's criterion | -- |
| H0's EO split for crop mapping: a 100,000-row stratified subsample, halved into 50,000 search and 50,000 test rows, the search half split 80/20 | done -- `datasets.load(name, split="eo")`, `run_sota.py --split eo` | -- |
| A budget per dataset | done -- `run_sota.py` runs one dataset per invocation, with `--evaluations` | -- |
| One process per dataset, arm and seed, at most N at a time, watched as one experiment | done -- `run_sota.py --seed`, `run_queue.py`, `monitor.py --experiment`; a seed run alone reproduces the same seed inside a five-seed run | -- |

The first run of H0 is the acceptance test for everything marked blocking H0,
and for the progress tracking it reads. The first run of H1 is the acceptance
test for everything else marked blocking H1.

## Analysis plan

Decided now, so that no metric is chosen after seeing the data:

1. Per hypothesis, the falsification criterion above, evaluated first.
2. For H0-H3, a per-seed paired comparison against the relevant baseline arm,
   reported as the per-seed table, not only as a mean.
3. Seed spread shown on every figure -- min-max band or per-seed points. A mean
   is never plotted alone.
4. Wall clock reported next to fit counts for every arm.
5. Any arm that stops on something other than the budget says so (`stopped_on`).
6. **Pairwise comparison between algorithms across datasets** for H4-H6: wins,
   ties and losses per pair, Wilcoxon signed-rank on per-dataset score
   differences, Holm-corrected where there is more than one pair, reported for
   H5 and H6 as a full algorithm-by-algorithm matrix so every pair is visible,
   not only the ones involving FASTENER.
7. **Best score per iteration is recorded for every algorithm**, not only the
   final result. See *Progress tracking* below.

### Progress tracking

Every search records a snapshot after each of its own iterations, written to
disk as it goes so a killed run still leaves its trajectory behind.

**What an iteration is, per algorithm.**

| algorithm | one iteration |
|---|---|
| FASTENER (stock, random swap, guided swap) | one generation |
| NSGA-II, NSGAII-MIIP (OBL and sparse initialisation) | one generation |
| FS-SDS | one test-and-diffusion cycle, within the run for one k |
| POSS | one mutation-and-archive-update step |
| filters and rankers (mRMR, ReliefF, HSIC Lasso, Boruta, RFE, rankers, random) | none -- they are not iterative searches; their final front is recorded once |

**The tracked quantity is the best score per iteration:** the best validation
F1 found so far, after each iteration. Recorded two ways, because a feature
selector's best overall score usually sits on its largest subsets:

* **overall** -- the best validation F1 of any subset seen so far;
* **per k** -- the best validation F1 among subsets of size <= k, at each k on
  the grid, so the low-k trajectory the hypotheses are about is visible on its
  own.

Each snapshot also carries what is needed to read that curve correctly:

* iteration number, cumulative unique fits, and wall-clock seconds since the
  start;
* the smallest subset size on the front (the quantity H1 is about);
* the current front itself -- every (feature subset, validation F1) pair -- so
  AUF, hypervolume or any other front metric can be recomputed later without
  re-running.

**Read on fits, not iterations.** Iterations are not comparable across
algorithms -- a FASTENER generation and a POSS step cost very different numbers
of fits -- so progress curves are plotted against cumulative fits, with wall
clock as a second view. Iteration number is kept for diagnosing one algorithm on
its own.

**Validation only during the search.** Snapshots record validation scores. The
test split is still read once, at the end. Because the fronts are stored,
test-set progress curves can be computed afterwards for interpretation; they are
secondary, labelled as such, and never used to choose a stopping point, an arm,
or a k.

**What it answers.** Whether an arm's final advantage was there from the start
or appeared late; whether an arm was still improving when the budget ran out, in
which case the budget, not the method, set the result; for H0, how many fits
each version of FASTENER needs to reach the same low-k score; and, for H1, how
fast each initialisation moves the smallest subset size down.

## Revisions

**2026-09-25 -- H0 on every other dataset (H0-E02) added.** Added after
H0-E01 had finished and been reported as not supported, with its datasets split
(fixed code faster on TOX_171 and USPS, 2020 code on BASEHOCK, neither on crop
mapping and har). H0's own criterion, datasets and verdict are unchanged. The
new experiment takes every remaining dataset rather than a chosen subset, and
its criterion is written here before any of its runs started.

**2026-09-30 -- The fixed arm keeps the top genes.** After H0-E01 and H0-E02
were reported, `include_top_genes` became `True` in the clone's defaults and in
the `fastener` arm, so the fixed code now differs from the 2020 code only in
`allow_self_mating`. H0-E01 and H0-E02 tested the fixed code with both flags
off; their verdicts are about that code, not this one. Stock FASTENER in H2-H6
is the new default. Runs of the two arms carry different algorithm IDs through
both repositories' commits (FASTENER `144621c` before, `08e6acd` after), so
they are never pooled. Up to H0-E03 the config part of the ID recorded only the
mating version's name, so the old and new fixed arms share a config hash; from
2026-10-07 the config also records both flags.

**2026-09-30 -- Twice the budget where the search had not converged.** Decided
after H0-E01 and H0-E02 were reported, from their validation curves only (test
scores played no part). A dataset counts as not converged when the mean
validation AUF at K = 10 of at least one H0 arm rose by 0.005 or more over the
last quarter of its budget (4,500 to 6,000 fits). Eleven datasets meet it:

| dataset | rise over the last quarter, fixed / 2020 |
|---|---|
| BASEHOCK | 0.025 / 0.014 |
| nci9 | 0.024 / 0.001 |
| lung_discrete | 0.013 / 0.015 |
| PCMAC | 0.006 / 0.013 |
| warpAR10P | 0.013 / 0.001 |
| TOX_171 | 0.009 / 0.005 |
| arcene | 0.006 / 0.008 |
| ORL | 0.004 / 0.007 |
| RELATHE | 0.001 / 0.007 |
| warpPIE10P | 0.003 / 0.005 |
| CLL_SUB_111 | 0.003 / 0.005 |

These get 12,000 fits per run in H1-H6, for every arm (`protocol.fit_budget`);
every other dataset keeps 6,000, and the EO sets in H0 keep 1,000. On the
smallest of the eleven (nci9, lung_discrete, TOX_171) the validation split has
12-34 rows, so part of the late rise can be the search fitting validation noise
rather than finding better subsets; the extra budget gives it room either way,
and test scores will show which. H0's verdicts are unchanged: its budgets were
fixed before its runs.

**2026-10-07 -- Experiment designs moved to `EXPERIMENTS.md`.** The H0-E02 and
H0-E03 subsections of H0 moved, with their text unchanged, to *Experiment
designs* in [`EXPERIMENTS.md`](EXPERIMENTS.md). H0 now lists its experiments as
bullets. This file keeps the hypotheses, the protocol and what experiments of
one hypothesis share; designs of later experiments go to `EXPERIMENTS.md`. No
claim, criterion or verdict changed.

**2026-10-07 -- The new FASTENER for every later experiment.** Decided by the
PI after H0-E03 was reported (not supported: without self-mating, the current
code converges neither faster nor slower than the 2020 code, and ends level).
Every FASTENER arm in H1-H6 runs the current code, as the *FASTENER version*
row of the protocol states. This confirms what the 2026-09-30 revision already
set for stock FASTENER; no criterion changes.

**2026-10-07 -- H1's datasets: eight, spread by feature count.** Decided by
the PI before any H1 result was read. H1 had been registered on the four
development sets, whose feature counts span only 174-970. The claim is about
OBL starting at half the features, so it predicts an effect that grows with p
and vanishes at small p; the four could not show either end. H1 now runs on
satimage, EOData, USPS, har, COIL20, gisette, Prostate_GE and arcene (36 to
10,000 features), and the criterion's "at least one other development set"
reads "at least one other of the eight datasets". The 4-of-5-seeds rule, the
arms, the metric and EOData's place in the criterion are unchanged.
`make_report.py` reads H1 on these eight (`H1_SETS`).

The change was committed (`3e1ce0c`) without this entry, and `H1-E01` was
started from that commit. It was stopped after 13 minutes, with only EOData's
ten runs started and none finished, and is recorded as failed; no score was
looked at. `H1-E02` restarts it from the commit that adds this entry, one
process per dataset, arm and seed (`run_queue.py`).

**2026-10-09 -- H2 and H3: forty datasets, datasets as the unit, a
calibrated budget.** Decided by the PI before any H2 or H3 run; no swap-arm
result of this round exists. Three changes, to both hypotheses alike:

* **Datasets.** The four development sets span 174-970 features and two
  domains, too narrow for a claim about an operator FASTENER lacks on any
  data. H2 and H3 now run on the 39 UCR/UEA time series sets of
  `DATASETS_USED.md`, chosen by shape cluster, and on EOData: 40 datasets,
  16 to 363,150 features. Crop mapping, madelon and gina leave H2 and H3; they
  remain development sets for H5 and H6.
* **Criterion.** With 40 datasets the per-seed rule on EOData and one other
  set is no longer the useful test. Each hypothesis is now read with datasets
  as the unit, as H0-E02 was: the per-dataset effect is the mean over seeds of
  the swap arm's AUF (K = 10) minus stock's, and the hypothesis is supported if
  the effects lean positive and a two-sided Wilcoxon signed-rank test over them
  is significant at alpha = 0.05. EOData's own 4-of-5 count is reported beside
  it, no longer part of the verdict. The seed count stays at 5.
* **Budget.** Per dataset, set from one Boruta run and one 12,000-fit
  calibration run of stock FASTENER (seed 1999, validation only), by the rule
  in H2, the same for every arm. The PI's reason: some datasets settle within
  1,000 fits and others do not, and fits past the point where the search has
  settled buy nothing.

Unchanged: the arms, the metric, the seeds, the classifier, the split. The
FASTENER clone moves to `b7e724d`, which only counts what the pruning step
does -- swaps proposed, fitted and kept -- for H2 and H3's secondary
reporting. The counters read what pruning did and draw no random numbers, so
the search is the one at `08e6acd`.
Recorded as [DEC-33](DECISIONS.md#dec-33).

**2026-10-09 -- DuckDuckGeese leaves H2 and H3.** Decided by the PI during
the budget calibration, before any H2 or H3 run. At 363,150 features
FASTENER's own bookkeeping, which handles every subset as a vector over all
features, made its calibration run the slowest by far: 1,480 of 12,000 fits
after an hour, about nine hours in all, against two to three for the next
slowest. At a 12,000-fit budget its 15 experiment runs would each take as
long. The cost comes from the feature count, not from anything H2 or H3 is
about. Its calibration run was stopped; no calibration result of it was read,
and no H2 or H3 result of any dataset exists. H2 and H3 now run on 39
datasets: EOData and 38 of the UCR/UEA sets. The rule is unchanged, including
the limit of 6 datasets left out. Recorded as
[DEC-34](DECISIONS.md#dec-34).

**2026-10-09 -- The budget calibration ended early.** Decided by the PI after
reading the calibration's validation curves, before any H2 or H3 run. 35 of
the 39 stock FASTENER runs had reached 12,000 fits; eodata, EigenWorms,
MotorImagery and PEMS-SF were stopped at 5,770-9,009. For those four the
budget rule's "its value at 12,000" reads "its value where it stopped", and
only grid values the run reached can count as settled; nothing else in the
rule changes. The budgets: 10 datasets at 2,000 fits, 2 at 4,000, 10 at
6,000, 17 at 12,000 (table in `EXPERIMENTS.md`, H2H3-E01). Recorded as
[DEC-35](DECISIONS.md#dec-35).
