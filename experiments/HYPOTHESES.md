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

1. **H1 first because it is cheap and diagnostic.** Sparse initialisation keeps
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
   already produced correct output three times.
4. **H5 and H6 last because they are the full grid** -- every algorithm on every
   dataset. The runs behind H1-H4 are part of that grid and are reused, not
   repeated; H5 and H6 add the remaining algorithm-dataset cells. H5 is read
   before H6, since H6's comparison includes stock FASTENER.

**H2 and H3 are one experiment.** Stock FASTENER, random swap and guided swap
are three arms over the same seeds and the same budget, run together in one
invocation. Running them separately would waste the shared stock arm and, worse,
would let the arms differ by run conditions rather than by operator.

## Protocol, fixed for every hypothesis below

| decision | value | note |
|---|---|---|
| Classifier | **`protocol.make_model()`: `DecisionTreeClassifier(random_state=20200)`, scikit-learn defaults** (Gini, `min_samples_split=2`) | The setting the paper states in Section 5.1. Drives every search **and** scores every result, for every method. |
| Seeds | **5: 2020, 2021, 2022, 2023, 2024** | Set by the PI. See *What 5 seeds can and cannot answer*. |
| Budget | **6,000 unique fits per run**, enforced by each method's fit cap | Equal across arms. Cached re-evaluations of a subset already fitted are not charged. Wall clock is recorded alongside and reported, never substituted: the two diverged 10x in the pilot. |
| FS-SDS budget | **k = 1..20, 300 fits per k -- 6,000 in total** | FS-SDS searches one fixed k per run, so its 6,000 are split evenly across the k it runs at. Giving it 6,000 *per k* would hand it 20x the budget of every other arm -- the same kind of mismatch H4 is about. |
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
  F1 among subsets of size <= k (subsets chosen on validation). The paper's own
  measure.
  * **K = 10 -- the primary metric for H1, H2, H3, H5 and H6.** All of them are
    claims about low k, and every falsification criterion below is stated at
    k <= 10, so the metric is read over exactly that range.
  * **K = 20 -- the primary metric for H4**, the aggregate the paper's Table 3
    uses.
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
alone.** H1-H3 use a per-seed sign test that 5 seeds can carry. H4-H6 take
datasets as the unit instead of seeds, which gives them 25 or 36 observations.
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

## H1 -- NSGA-II's weakness at small k is an initialisation artifact

*(first: cheapest, and it shakes out the harness)*

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

**Datasets.** The four development sets.

**Primary metric.** AUF, K = 10. Reported beside it, as the diagnostic quantity
this hypothesis is about: the smallest subset size on the front, per seed.

**Falsification criterion.** H1 is supported if `nsga2_sparse` has a higher
AUF (K = 10) than `nsga2` in **at least 4 of 5 seeds**, on **EOData and on at
least one other development set**. Otherwise it is not supported. If the sparse
arm reaches small subsets and still fails that test, the weakness is the search
after all -- the more interesting outcome for H5 and H6.

**Blocker to clear first.** The sparse arm was launched once in the previous
round and produced nothing; both of its log files were zero bytes. Whatever
failed there must be diagnosed before the arm counts for anything. This is the
main reason H1 runs first.

## H2 -- A size-preserving move changes the front at all, guided or not

*(second: the control for H3; shares a run with it)*

**Claim.** Adding *any* size-preserving swap to FASTENER's pruning step improves
its front at low k, relative to stock FASTENER.

**Why it comes before H3.** H2 is the weaker, more defensible claim, and it is
the ablation that isolates guidance: if random swap also helps, the contribution
is "FASTENER needed a size-preserving operator", not "the guidance is clever".
If neither helps, H3 cannot be true for the reason H3 gives.

**Pilot evidence.** Null. Random swap averaged 0.7956 over the gina k-grid
against stock's 0.7960 -- a difference of 0.0004, far inside seed spread.

**Arms.** `fastener` (stock) and `fastener_swap_random`.

**Datasets.** The four development sets.

**Primary metric.** AUF, K = 10.

**Falsification criterion.** `fastener_swap_random` must have a higher AUF
(K = 10) than `fastener` in **at least 4 of 5 seeds**, on **EOData and on at
least one other development set**. A null here with a positive H3 would be the
interesting outcome (the guidance is doing the work); a null in both is the
likely one given the pilot.

## H3 -- The guided swap improves FASTENER at small k

*(third: read after its control, though it runs in the same invocation)*

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

**Datasets.** The four development sets.

**Primary metric.** AUF, K = 10.

**Falsification criterion.** `fastener_swap_guided` must have a higher AUF
(K = 10) than `fastener` in **at least 4 of 5 seeds**, on **EOData and on at
least one other development set**. Fewer than that at the pilot's effect size
is indistinguishable from noise, and H3 is recorded as not supported.

**Prior art, which narrows the claim.** FS-SDS's diffusion move is already a
size-preserving swap: copy a good agent's subset, drop one selected feature at
random, add one unselected at random (Alhakbani & al-Rifaie 2017, the FASTENER
paper's own reference [12]). The operator is not novel. What has no precedent
found so far is guiding *both* ends from quantities FASTENER already computes.
Any write-up states this.

## H4 -- The published FASTENER > FS-SDS ordering does not survive a clean protocol

*(fourth: the largest targeted run, on a harness already proven three times)*

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

*(fifth: the full grid)*

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

*(sixth: read after H5, on the same grid)*

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

Thirty-six datasets are on disk under `data/`, each checksum-pinned by its
download script, all classification, and all used in this round. Every one loads
through `datasets.load(name)` and is split as the protocol table states. Shapes
below are measured from the files, not transcribed, and are the full datasets
before the row cap. "Smallest class" is counted after cleaning (see *Dropped
rows*).

### Development sets -- used by H1, H2, H3, H5 and H6

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
| The runner passes the 50,000-row cap to the loader | **to build** -- `run_sota.py` calls `load(name)` with no cap | H1 |
| One classifier: every method uses `protocol.make_model()` | done except Boruta | -- |
| Boruta runs on the decision tree | **to build** -- currently a 100-tree random forest | H5 |
| 6,000-fit cap on FASTENER, NSGA-II, NSGAII-MIIP and POSS | done -- `Config.max_model_fits`, `stop_evaluations` | -- |
| FS-SDS gets 6,000 in total, 300 per k over k = 1..20 | **to build** -- the budget is currently applied *per k* | H4 |
| k grid includes every k from 1 to 20 | **to build** -- the current `K_GRID` skips 4, 6, 7, 9, 11, 13, 14 and 16-19 | H1 |
| AUF computed from the front at every k <= K | **to build** -- `paper_protocol.auf` exists for the replication protocol, not for this one | H1 |
| Best score per iteration recorded for every algorithm | **to build** -- runs record only a fit-count heartbeat; FASTENER's per-generation pickles hold enough to derive it | H1 |
| `nsga2_sparse` produces output | **to diagnose** -- it produced zero-byte logs in the previous round | H1 |
| Seeds 2020-2024 | done -- `run_sota.py` uses `2020 + i` | -- |

The first run of H1 is the acceptance test for everything marked blocking H1.

## Analysis plan

Decided now, so that no metric is chosen after seeing the data:

1. Per hypothesis, the falsification criterion above, evaluated first.
2. For H1-H3, a per-seed paired comparison against the relevant baseline arm,
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
which case the budget, not the method, set the result; and, for H1, how fast
each initialisation moves the smallest subset size down.
