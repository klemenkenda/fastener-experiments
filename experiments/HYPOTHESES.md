# Hypotheses and protocol, fixed before the runs

Written 2026-09-25, before any experiment in this round was started. Nothing
below may be revised after results exist; a revision gets a dated entry at the
bottom saying what changed and why, so that the difference between "what we set
out to test" and "what we found" stays legible.

Hypotheses are numbered in the order they are to be run. Deferred items are
lettered, so they hold no slot in the run order.

## Why this order

1. **H1 first because it is cheap and diagnostic.** Sparse initialisation puts
   NSGA-II in small subsets, where a model fit costs ~0.01s instead of the ~5s
   it costs at 400 features -- so this is the least expensive arm in the round,
   despite NSGA-II being the most expensive method in the previous one. It also
   has a known, undiagnosed failure (see H1), and it exercises the new
   one-classifier protocol end to end. Finding a harness bug here costs minutes;
   finding it in H4 costs days.
2. **H2 before H3** because H2 is H3's control. If a random swap already changes
   the front, the contribution is "FASTENER needed a size-preserving operator",
   not "the guidance is clever" -- and that reading has to be available before
   the guided result is interpreted. The two share arms and execute as a single
   run (see below); the ordering is about the order they are *read*.
3. **H4 last because it is the round's largest run** -- 25 datasets x 2 arms x 5
   seeds -- and because it is the one whose result matters most, so it should
   run on a harness that has already produced correct output three times.

**H2 and H3 are one experiment.** Stock FASTENER, random swap and guided swap
are three arms over the same seeds and the same budget. They are run together in
a single invocation -- running them separately would waste the shared stock arm
and, worse, would let the arms differ by run conditions rather than by operator.

## Protocol, fixed for every hypothesis below

| decision | value | note |
|---|---|---|
| Seeds | **5** | Set by the PI. See "What 5 seeds can and cannot answer" below. |
| Classifier | **one model, driving search AND evaluation, identical across every method** | The previous round let Boruta search with a random forest and FS-SDS with an ELM, then graded everything with a decision tree. No method may optimise against a model it is not then judged by. |
| Budget unit | **unique model fits**, equal across arms, enforced by `Config.max_model_fits` | Wall clock recorded alongside and reported, never substituted. The two diverged 10x in the pilot. |
| Splits | three-way stratified train/val/test; selection on val; test untouched until the final score | |
| Primary metric | **F1 for classification, MAE for regression** | Set by the PI. Every dataset in this round is classification, so F1 throughout; the MAE branch exists for a future regression task and is not exercised here. |
| F1 average | **weighted**, matching `protocol.primary_score` | Binary and macro are computed and stored too -- the paper says only "F1 score", and on a two-class set the choice moves the AUF substantially (see `WHY_RESULTS_DIFFER.md`). |
| Metrics | **compute all of them, every run** | Secondary metrics are for interpretation and are labelled as secondary in any write-up. |
| Pre-registration | this file is committed before the first run | |

### How a single-subset metric becomes a front metric

F1 scores one subset. Every hypothesis here compares *fronts* -- sets of
(size, score) points -- so each needs an aggregate built on F1, named per
hypothesis below and fixed now:

* **AUF** = (1/K) * sum over k=1..K of opt(k), where opt(k) is the best F1 among
  subsets of size <= k, K = 20. The paper's own measure; used wherever a
  published number is being compared against (H4).
* **Hypervolume** = the area dominated by the front in (few features, high F1)
  against a fixed reference point of all-features-at-F1-zero
  (`analysis.hypervolume`). Used where arms are compared against each other and
  no published value exists (H1, H2, H3).

Both are functions of F1 alone. Neither is a new primary metric; they are how
the primary metric is read off a Pareto front.

### Why "one classifier" is not negotiable

A wrapper method optimises a subset *for a particular model*. If method A
searches with the model that later grades it and method B does not, A has
home-field advantage and the comparison measures the mismatch, not the search.
In the pilot this bias ran in FASTENER's favour on every arm except Boruta and
`fs_sds_elm`.

Consequence to accept up front: Boruta cannot take an arbitrary model, because
it is defined over an estimator that exposes feature importances. Under a model
that provides none, Boruta is either dropped or run with the nearest estimator
that does, and labelled as a departure.

### What 5 seeds can and cannot answer

5 seeds is what we have. It is enough for:

* a difference that is large relative to the seed spread;
* a directional check (does arm X ever beat arm Y at any k?);
* an effect visible in every seed rather than on average.

It is **not** enough to resolve the differences the pilot actually showed. Pilot
seed spreads at k=500 on gina: stock FASTENER 0.824-0.863, guided swap
0.772-0.853, random swap 0.839-0.850. Arm-to-arm gaps of 0.02-0.03 sit inside
those ranges. A paired test at n=5 will not separate them, and a null result at
this seed count means "not detected at n=5", never "no effect".

Therefore: **no hypothesis below is declared confirmed or refuted on a mean
difference alone.** Each states a falsification criterion that 5 seeds can
actually carry -- a per-seed sign test, or an effect so large it does not need
one. If a result lands in the ambiguous middle, the honest output is "needs more
seeds", and the seed count becomes the finding.

### Pilot data

The previous round was discarded. Its runs are recoverable at commit `3bfce8c`
but are **not evidence**: the comparison they rest on was confounded (a
decision-tree-scored FASTENER against an ELM-scored FS-SDS, at mismatched
budgets) and the arms were separated by less than their own seed spread. They
are used here only as PILOT data -- to size this round and to say which
hypotheses already look unpromising.

---

## H1 -- NSGA-II's weakness at small k is an initialisation artifact

*(first: cheapest, independent, and it shakes out the harness)*

**Claim.** NSGA-II and NSGAII-MIIP trail at small feature counts because of
where they start, not because the search is worse.

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

**Arms.** `nsga2` (OBL init, as ported), `nsga2_sparse` (subsets of 1-30 at
init). The sparse arm is a **departure from the source** and is labelled as one
everywhere; it is a controlled variant, not the published algorithm.

**Primary metric.** F1 (weighted), read off the front as hypervolume. The
diagnostic quantity reported beside it is the smallest subset size any seed
reaches, which is what this hypothesis is actually about.

**Falsification criterion.** H1 is supported if the sparse arm produces fronts
reaching k <= 30 and competes with FASTENER there. If the sparse arm reaches
small subsets and still loses badly, the weakness is the search after all, and
H1 is refuted -- which is the more interesting outcome for the comparison.

**Blocker to clear first.** The sparse arm was launched once in the previous
round and produced nothing; `results/nsga2_sparse.log` and `.err.log` were both
zero bytes. Whatever failed there is unknown and must be diagnosed before the
arm counts for anything. This is the main reason H1 runs first.

## H2 -- A size-preserving move changes the front at all, guided or not

*(second: the control for H3; shares a run with it)*

**Claim.** Adding *any* size-preserving swap to FASTENER's pruning step changes
its Pareto front, relative to stock.

**Why it comes before H3.** H2 is the weaker, more defensible claim, and it is
the ablation that isolates guidance: if random swap also helps, the contribution
is "FASTENER needed a size-preserving operator", not "the guidance is clever".
If neither helps, H3 cannot be true for the reason H3 gives.

**Pilot evidence.** Null. Random swap averaged 0.7956 over the gina k-grid
against stock's 0.7960 -- a difference of 0.0004, far inside seed spread.

**Arms.** `fastener` (stock), `fastener_swap_random`.

**Primary metric.** F1 (weighted), read off the front as hypervolume.

**Falsification criterion.** Random swap must beat stock in **at least 4 of 5
seeds** at k <= 10, on **EOData and on at least one of madelon and gina**. A
null here with a positive H3 would be the interesting outcome (guidance is
doing the work); a null in both is the likely one given the pilot.

## H3 -- The guided swap improves FASTENER at small k

*(third: read after its ablation, though it runs in the same invocation)*

**Claim.** Replacing a subset's weakest feature (by the permutation scores
FASTENER already computes) with a feature sampled by mutual information (the
vector `IntersectionMatingWithInformationGain` already computes) produces a
better Pareto front at small feature counts, under an equal fit budget, than
stock FASTENER.

**Why it might hold.** No FASTENER operator preserves subset size. Mating pulls
a child toward the middle of its parents' sizes; pruning strictly decreases.
Only mutation can hold size constant, and only by flipping two bits at once --
probability ~k(d-k)/d^2, about 0.047 for k=10 of d=200. Same-size exploration is
a second-order event with no operator behind it.

**Pilot evidence, and it points the wrong way.** On gina the guided arm was
*behind* stock FASTENER from k=20 outward (0.817 vs 0.844 at k=500) and ahead
only at k=2 (0.766 vs 0.748). Its seed spread was also the widest of the three
arms. This hypothesis enters the round with evidence against it.

**Arms.** `fastener` (stock), `fastener_swap_guided`. Shares the stock arm with
H2.

**Primary metric.** F1 (weighted), read off the front as hypervolume -- the
same aggregate as H2, so the two arms are read on one scale.

**Falsification criterion.** Guided must beat stock in **at least 4 of 5 seeds**
at k <= 10, on **EOData and on at least one of madelon and gina**. Fewer than
that at the pilot's effect size is indistinguishable from noise, and H3 is
recorded as not supported.

**Prior art, which narrows the claim.** FS-SDS's diffusion move is already a
size-preserving swap: copy a good agent's subset, drop one selected feature at
random, add one unselected at random (Alhakbani & al-Rifaie 2017, the FASTENER
paper's own reference [12]). The operator is not novel. What has no precedent
found so far is guiding *both* ends from quantities FASTENER already computes.
Any write-up states this.

## H4 -- The published FASTENER > FS-SDS ordering does not survive a clean protocol

*(last: the round's largest run, on a harness already proven three times)*

**Claim.** Run FASTENER and FS-SDS with the same classifier driving both
searches and the same fit budget, and the paper's headline ordering -- FASTENER
ahead on 24 of 25 benchmarks -- does not reproduce.

**Why.** Table 3 compares a decision-tree-scored FASTENER against an ELM-scored
FS-SDS (Koprivec, Kenda & Sircelj 2020, Section 5.1, stated verbatim there), at
30,000 evaluations per k for FS-SDS against FASTENER's ~11,000-16,000 total. Two
confounds, stacked. The published claim is therefore partly a statement about
decision trees versus ELMs on these data, not purely about the two searches.

**Pilot evidence.** The ordering flipped: tree-driven FS-SDS beat FASTENER on 11
of 14 finished datasets, at a fifth of the paper's FS-SDS budget.

**Arms.** `fastener`, `fs_sds` -- both driven by the round's single classifier,
both at the same fit budget.

**Primary metric.** F1 (weighted), read off the front as AUF with K = 20 -- the
paper's own aggregate, so the replication lands on the paper's scale. This is the
one hypothesis with a published reference value, so the mean absolute difference
against Table 3 (`paper_tables.compare`, `mean_abs_delta`) is reported beside it
as a secondary measure of replication fidelity.

**Falsification criterion.** H4 is supported only if FS-SDS is ahead on a clear
majority of datasets **and** the per-dataset direction is consistent across
seeds. A mixed result means the clean protocol makes the two methods comparable
-- which is itself a finding, and is reported as such rather than as a flip.

**Note on scope.** This is a correction to a paper the PI co-authored, and is
framed as such: a confound identified and measured, not a defect claimed.

---

## Deferred, deliberately

**D1 -- the replication gap is a grading artifact.** `WHY_RESULTS_DIFFER.md`
already reconciles FASTENER to +0.026 via `min_samples_leaf=2` plus binary F1,
and leaves FS-SDS unexplained. Note the dependency: H4 compares against the
published table, so an unexplained offset against that table weakens H4's
interpretation. If H4's result is to be stated in absolute terms rather than as
an ordering, D1 comes back.

**D2 -- conclusions are model-dependent.** Out of scope. The pilot measured the
size of what is being set aside: on gina, HistGradientBoosting scored +0.06 at
k=10 and +0.12 at k=400 over the decision tree, and at k=400 it beat the
all-features decision-tree baseline by 0.099. Every result in this round is
therefore a statement about decision trees, and says so.

---

## Datasets

Twenty-eight datasets are on disk under `data/`, each checksum-pinned by its
download script, all classification, and all used in this round. Every one loads through
`datasets.load(name)`, and every one is cut the same way: a stratified 60/20/20
train/validation/test split with `SPLIT_SEED = 20200`, fixed across seeds, so
that seeds vary the search and never the rows.

Shapes below are measured from the files, not transcribed. "Smallest class" is
counted after cleaning (see *Dropped rows*).

### Development sets -- used by H1, H2 and H3

| dataset | rows | features | classes | smallest / largest class | domain | source |
|---|---:|---:|---:|---|---|---|
| **eodata** | 480,000 | 182 | 24 | 20,000 / 20,000 | Sentinel-2 land patches, Slovenia 2017: 10 spectral signals (raw bands and vegetation indices), each summarised by 18 temporal statistics over the season, plus DEM height and inclination | Šircelj, Kenda & Koprivec, PANGAEA 2020, [doi:10.1594/PANGAEA.914271](https://doi.org/10.1594/PANGAEA.914271) |
| madelon | 2,600 | 500 | 2 | 1,300 / 1,300 | synthetic: 5 informative features, 15 linear combinations of them, 480 noise | NIPS 2003 feature selection challenge, UCI |
| gina | 3,468 | 970 | 2 | 1,705 / 1,763 | handwritten digit pixels, even vs odd two-digit number | agnostic learning challenge, OpenML 1038 |

**EOData is the primary dataset.** It is the benchmark FASTENER was designed
for and evaluated on in the paper, so a result about FASTENER's operators that
does not hold there is not a result about FASTENER in its own setting. Madelon
and gina are the controls around it: madelon's structure is known, so a
selector can be checked against the planted informative features, but it is
synthetic; gina is real-world but its relevant features are unknown. A result
that holds on some of the three and not the others is reported as such.

Two properties of EOData shape how it is run:

* **It is the opposite shape to the other two** -- very many rows, few features.
  A single decision-tree fit on 20 features over the full training split
  (288,000 rows) measured 14.2 s on this machine, against milliseconds on
  madelon. At the round's 6,000-fit budget that is roughly 24 hours per seed per
  arm, so the number of rows used is a cost decision that has to be fixed before
  the run (see *Open questions*). `load_eodata(max_rows=...)` takes a stratified
  subsample; any subsampled run is labelled with its row count, since it is not
  the paper's setting.
* **The split is random stratified, not spatial.** A spatial split, blocked by
  parcel or location, would be the right protocol for pixel samples, since
  neighbouring pixels of one field are near-duplicates and leak across a random
  split. The published table carries no parcel identifier or coordinate -- all
  182 columns are features -- so there is nothing to block on. The random split
  is the paper's own choice and the only one available; results on EOData are
  therefore optimistic in the same way the paper's are, and are reported with
  that caveat.

### Paper benchmarks -- used by H4

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

**Dropped rows.** A class with fewer than 5 rows cannot survive a 60/20/20
split -- it rounds to no validation and no test rows, so it would sit in
training and never be scored, which distorts weighted F1. Such classes are
dropped at load time and the drop is recorded on the `Dataset`. Two sets are
affected: **lymphoma** loses 8 rows (96 → 88) and **nci9** loses 2 (60 → 58).
Their results are on the cleaned sets and are labelled as such.

**What the small sets can support.** Twelve of the 25 have fewer than 110 rows.
At 60/20/20, GLIOMA's test split is 10 rows and colon's is 13; one row changing
class moves the score by 0.08-0.10. The split is fixed, so the seed spread on
these sets is the *search's* variance, not the split's -- a narrow spread on 10
test rows is not evidence of a stable result, and is not reported as one.

## Open questions

**EOData row count.** Full size costs ~24 h per seed per arm at the 6,000-fit
budget; H1-H3 need 5 arms x 5 seeds on it. The options are the full 480,000
rows, a fixed stratified subsample for every arm (the paper's setting is then
not reproduced, and the run says so), or a smaller fit budget on EOData only
(the budget stops being equal across datasets, which is allowed -- it is
equal across *arms* that matters). To be fixed before H1 starts on EOData.

## Analysis plan

Decided now, so that no metric is chosen after seeing the data:

1. Per hypothesis, the falsification criterion above, evaluated first.
2. Per-seed paired comparison against the relevant baseline arm, reported as
   the per-seed table, not only as a mean.
3. Seed spread shown on every figure -- min-max band or per-seed points. A mean
   is never plotted alone.
4. Wall clock reported next to fit counts for every arm.
5. Any arm that stops on something other than the budget says so (`stopped_on`).
6. **Best score per iteration is recorded for every algorithm**, not only the
   final result. See *Progress tracking* below.

### Progress tracking

Every search records a snapshot after each of its own iterations, written to
disk as it goes so a killed run still leaves its trajectory behind.

**What an iteration is, per algorithm.** The unit differs, so it is named
rather than assumed:

| algorithm | one iteration |
|---|---|
| FASTENER (stock, random swap, guided swap) | one generation |
| NSGA-II, NSGAII-MIIP (OBL and sparse init) | one generation |
| FS-SDS | one test-and-diffusion cycle |
| POSS | one mutation-and-archive-update step |

**The tracked quantity is the best score per iteration:** the best validation
F1 found so far, after each iteration. Recorded two ways, because a feature
selector's best overall score usually sits on its largest subsets:

* **overall** -- the best validation F1 of any subset seen so far;
* **per k** -- the best validation F1 among subsets of size <= k, at each k on
  the grid, so the small-k trajectory that H2 and H3 are about is visible on
  its own.

Each snapshot also carries what is needed to read that curve correctly:

* iteration number, cumulative unique model fits, and wall-clock seconds since
  the start;
* the smallest subset size on the front (the quantity H1 is about);
* the current Pareto front itself -- every (feature subset, validation F1)
  pair -- so hypervolume, AUF or any other front metric can be recomputed later
  without re-running.

**Read on fits, not iterations.** Iterations are not comparable across
algorithms -- a FASTENER generation and a POSS step cost very different numbers
of fits -- so progress curves are plotted against cumulative fits, with wall
clock as a second view. Iteration number is kept for diagnosing one algorithm
on its own.

**Validation only during the search.** Snapshots record validation scores. The
test split is still touched once, at the end. Because the fronts are stored,
test-set progress curves can be computed afterwards for interpretation; they
are secondary, labelled as such, and never used to choose a stopping point, an
arm, or a k.

**What it answers.** Whether an arm's final advantage was there from the start
or appeared late; whether an arm was still improving when the budget ran out,
in which case the budget, not the method, set the result; and, for H1, how
fast each initialisation moves the smallest subset size down.
