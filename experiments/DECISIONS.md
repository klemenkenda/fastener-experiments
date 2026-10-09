# Decision log

Every decision that shapes what an experiment tests or how it is read, with its
date, its reason, where it is recorded, and the experiments it applies to.
[`HYPOTHESES.md`](HYPOTHESES.md) holds the plan as it now stands, and its
*Revisions* section holds the formal record of changes made to the plan after
a result was seen. [`EXPERIMENTS.md`](EXPERIMENTS.md) lists each experiment's
runs. This file connects the two: why each rule is what it is, and which
experiments ran under it.

**Adding a decision.** Append an entry with the next number, and add it to the
index and to *By experiment*. Never renumber or delete an entry. A decision that
is reversed gets a new entry that names the one it replaces, and the old entry
gains a `Replaced by` line. Where a decision was taken after a result was seen,
say so, and name the result.

**Fields.**

- **Why:** the reason.
- **By:** who decided. `PI` is the principal investigator. It is left out where
  the record does not say.
- **Source:** the commits, and the section of `HYPOTHESES.md`, where it is
  recorded. Commits in the FASTENER clone are marked `fastener`; the rest are
  in this repository.
- **Applies to:** experiment IDs, or hypotheses not yet run.

## Index

| # | date | decision | applies to |
|---|---|---|---|
| [DEC-01](#dec-01) | 2026-09-16 | Keep the FASTENER clone untouched in `fastener/`; experiments live in their own repository | all |
| [DEC-02](#dec-02) | 2026-09-16 | Train / validation / test split: search on validation, test read once | all |
| [DEC-03](#dec-03) | 2026-09-16 | One classifier and one metric for every method | all |
| [DEC-04](#dec-04) | 2026-09-16 | Budget searches by unique model fits, not by generations or rounds | all |
| [DEC-05](#dec-05) | 2026-09-16 | Every run writes a provenance manifest | all |
| [DEC-06](#dec-06) | 2026-09-16 | Run on the current package stack, not the 2020 pins | all; the `fastener_2020` arm of H0-E01, H0-E02 and H0-E03 |
| [DEC-07](#dec-07) | 2026-09-16 | Port NSGAII-MIIP and label it a reimplementation; add a labelled sparse-start control; leave out BGR-FS | H1, H5, H6 |
| [DEC-08](#dec-08) | 2026-09-23 | Use the paper's 25 benchmarks and EOData, each checked against the paper's Table 1 | all |
| [DEC-09](#dec-09) | 2026-09-25 | Discard every earlier result as evidence | all |
| [DEC-10](#dec-10) | 2026-09-25 | Pre-register hypotheses and falsification criteria before any run | all |
| [DEC-11](#dec-11) | 2026-09-25 | Primary metric: F1 for classification, MAE for regression | all |
| [DEC-12](#dec-12) | 2026-09-25 | Fix the protocol: seeds, classifier, budget, k grid, AUF, row cap | all |
| [DEC-13](#dec-13) | 2026-09-25 | Add eight tall datasets; crop_mapping joins the development sets | H0-E01, H0-E02, H0-E03; H1-H3, H5, H6 |
| [DEC-14](#dec-14) | 2026-09-25 | Record progress per iteration, read against cumulative fits | all |
| [DEC-15](#dec-15) | 2026-09-25 | Experiment, run and algorithm IDs, a ledger, and no evidence from uncommitted code | all |
| [DEC-16](#dec-16) | 2026-09-25 | Add H0, the bug-fixed FASTENER against the 2020 code, and run it first | H0-E01, H0-E02, H0-E03 |
| [DEC-17](#dec-17) | 2026-09-25 | H0 measure: fits to a common validation target | H0-E01, H0-E02, H0-E03 |
| [DEC-18](#dec-18) | 2026-09-25 | H0 datasets: crop_mapping, USPS, har, BASEHOCK, TOX_171 | H0-E01 |
| [DEC-19](#dec-19) | 2026-09-25 | EO datasets in H0: 1,000 fits on a 100,000-row stratified subsample split 40/10/50 | H0-E01, H0-E02, H0-E03 |
| [DEC-20](#dec-20) | 2026-09-25 | Run datasets in parallel, one thread each | H0-E01, H0-E02, H0-E03 |
| [DEC-21](#dec-21) | 2026-09-25 | After H0-E01, test H0 on all 31 other datasets as H0-E02, with datasets as the unit | H0-E02 |
| [DEC-22](#dec-22) | 2026-09-26 | Keep each run's records in git, but not its trajectories | H0-E01, H0-E02, H0-E03 |
| [DEC-23](#dec-23) | 2026-09-30 | Keep the top genes in the fixed FASTENER | H0-E03; H1-H6 |
| [DEC-24](#dec-24) | 2026-09-30 | Double the fit budget on 11 datasets whose search had not converged | H0-E03; H1-H6 |
| [DEC-25](#dec-25) | 2026-09-30 | Repeat H0 on all 36 datasets as H0-E03 | H0-E03 |
| [DEC-26](#dec-26) | 2026-09-30 | After the H0-E03 driver crashed, adopt its running runs instead of restarting them | H0-E03 |
| [DEC-27](#dec-27) | 2026-10-07 | Record the mating flags in FASTENER arms' algorithm-ID config | H1-H6, later H0 experiments |
| [DEC-28](#dec-28) | 2026-10-07 | Use the new FASTENER for every later experiment | H1-H6 |
| [DEC-29](#dec-29) | 2026-10-07 | H1 on eight datasets spread by feature count, not the four development sets | H1-E01, H1-E02 |
| [DEC-30](#dec-30) | 2026-10-07 | Run one process per dataset, arm and seed, at most ten at a time | H1-E01, H1-E02 |
| [DEC-31](#dec-31) | 2026-10-07 | Stop H1-E01 and restart H1 as H1-E02 | H1-E01, H1-E02 |
| [DEC-32](#dec-32) | 2026-10-09 | Split each report into a short reading (REPORT.md) and its record (SUPPORT.md) | H1-E02 and later |
| [DEC-33](#dec-33) | 2026-10-09 | H2 and H3 on 39 UCR/UEA sets and EOData, datasets as the unit, budget calibrated per dataset | H2, H3 |
| [DEC-34](#dec-34) | 2026-10-09 | DuckDuckGeese leaves H2 and H3 | H2H3-E01 |

## Decisions

### DEC-01

**2026-09-16 -- Keep the FASTENER clone untouched in `fastener/`; experiments
live in their own repository.**

- **Why:** the algorithm's history stays clean, and every change to FASTENER
  itself is a deliberate commit in its own repository. The two repositories are
  pinned separately in every manifest and algorithm ID.
- **Source:** `f8196a2`.
- **Applies to:** all.

### DEC-02

**2026-09-16 -- Train / validation / test split: search on validation, test
read once.**

- **Why:** the reference `eval_fun` in `fastener.py` scores on the test data,
  which would let the search fit the set that is reported.
- **Detail:** the split is stratified 60/20/20 with `SPLIT_SEED = 20200`, fixed
  across seeds. H0's EO sets use their own split ([DEC-19](#dec-19)).
- **Source:** `d9fdd50`; `HYPOTHESES.md`, *Protocol*.
- **Applies to:** all.

### DEC-03

**2026-09-16 -- One classifier and one metric for every method.**

- **Why:** any difference in results should come from feature selection, not
  from scoring. The earlier FS-SDS comparison mixed an ELM with a decision tree,
  which is one of the reasons for [DEC-09](#dec-09).
- **Detail:** `DecisionTreeClassifier(random_state=20200)`, the classifier the
  paper states. It drives every search and scores every result. Boruta runs on
  it too.
- **Source:** `d9fdd50`, `cada3df`, `825737e`; `HYPOTHESES.md`, *Why "one
  classifier" is not negotiable*.
- **Applies to:** all.

### DEC-04

**2026-09-16 -- Budget searches by unique model fits, not by generations or
rounds.**

- **Why:** generations cost different numbers of fits in different algorithms.
  Equal fits is equal compute. Wall clock is recorded beside fits, never in
  place of them.
- **Detail:** the budget was first 6,000 fits for the GAs, FASTENER's measured
  cost on MADELON. It is now exact for every method: NSGA-II used to overshoot
  by up to a generation, and FS-SDS used to get 6,000 fits *per k*.
- **Source:** `a62beff`, `dfde63e`, `190a9f1`, `825737e`.
- **Applies to:** all.

### DEC-05

**2026-09-16 -- Every run writes a provenance manifest.**

- **Why:** any number can then be traced to its code, data and seeds.
- **Detail:** the manifest records the commit and dirty flag of both
  repositories, package versions, dataset SHA256s, the seeds, and a digest of
  every output.
- **Source:** `d9fdd50`.
- **Applies to:** all.

### DEC-06

**2026-09-16 -- Run on the current package stack, not the 2020 pins.**

- **Why:** the 2020 pins (numpy 1.18, scikit-learn 0.22) do not install on the
  Python 3.11 used here. The requirements are lower bounds taken from the
  environment that produced the results.
- **Consequence:** the `fastener_2020` arm is the current code with the 2020
  mating flags switched back on ([DEC-16](#dec-16)). It is not the 2020 code on
  the 2020 stack.
- **Source:** `bdb5775`, `002f1a8`; `fastener` `ff313d1`.
- **Applies to:** all. Named because it matters most for the `fastener_2020`
  arm of H0-E01, H0-E02 and H0-E03.

### DEC-07

**2026-09-16 -- Port NSGAII-MIIP and label it a reimplementation; add a
labelled sparse-start control; leave out BGR-FS.**

- **Why:**
  - The original needs MATLAB and Weka.
  - The faithful port starts every subset at about 50% density and never gets
    below ~200 features at the budget given, so a sparse-start variant
    separates "the search is worse" from "it started elsewhere".
  - BGR-FS has no public code, and building it from an abstract would be a
    strawman.
- **Source:** `a62beff`, `2fba678`; `HYPOTHESES.md`, H1.
- **Applies to:** H1, H5, H6 (not yet run).

### DEC-08

**2026-09-23 -- Use the paper's 25 benchmarks and EOData, each checked against
the paper's Table 1.**

- **Why:** the earlier runs used MADELON and GINA, neither of which the paper
  uses.
- **Detail:** each download is checked against Table 1 on rows, features and
  classes, and pinned by SHA256. EOData needs a custom reader for its malformed
  ARFF header.
- **Source:** `dd2eff7`, `13e508e`; `HYPOTHESES.md`, *Datasets*.
- **Applies to:** all.

### DEC-09

**2026-09-25 -- Discard every earlier result as evidence.**

- **Why:** the comparison those results rest on is confounded. FASTENER was
  scored with a decision tree and FS-SDS with an ELM, at mismatched budgets.
- **Detail:** the results are kept only as pilot data in `HYPOTHESES.md`. The
  summaries are recoverable from git.
- **Source:** `827bac9`; `HYPOTHESES.md`, *Pilot data*.
- **Applies to:** all.

### DEC-10

**2026-09-25 -- Pre-register hypotheses and falsification criteria before any
run.**

- **Why:** a criterion written after the results are seen can be bent to fit
  them.
- **Detail:**
  - Hypotheses are numbered in run order.
  - H4 is in scope and runs last.
  - A change to the plan after a result is seen goes in *Revisions*, dated, and
    names the result.
- **Source:** `3a6f2cb`, `ea8910e`, `f15f7ad`, `b1a51d3`; `HYPOTHESES.md`,
  *Revisions*.
- **Applies to:** all.

### DEC-11

**2026-09-25 -- Primary metric: F1 for classification, MAE for regression.**

- **Why:** set by the PI. Every dataset here is classification, so it is
  weighted F1 throughout, as in the reference `eval_fun`.
- **By:** PI.
- **Source:** `ea8910e`; `HYPOTHESES.md`, *Protocol*.
- **Applies to:** all.

### DEC-12

**2026-09-25 -- Fix the protocol: seeds, classifier, budget, k grid, AUF, row
cap.**

- **Detail:**
  - Seeds: 5, namely 2020 to 2024 (set by the PI).
  - Budget: 6,000 fits per run, equal across arms. FS-SDS gets 300 per k over
    k = 1..20.
  - k grid: 1..20, then 25, 30, 50, 100, 200, 500.
  - Primary front metric: AUF at K = 10.
  - Row cap: 50,000 rows, a fixed stratified subsample, on the six largest
    datasets.
- **Why:** the row cap was chosen from measured fit costs, so that no run
  exceeds about two hours. EOData at full size costs about 24 hours per run.
- **By:** PI (seeds).
- **Source:** `cada3df`, `825737e`; `HYPOTHESES.md`, *Protocol*, *Cost, and the
  row cap*.
- **Applies to:** all. The budget is amended by [DEC-24](#dec-24).

### DEC-13

**2026-09-25 -- Add eight tall datasets; crop_mapping joins the development
sets.**

- **Why:** the paper's benchmarks are nearly all wide and short, the opposite
  of the shape FASTENER was built for.
- **Detail:** the eight are crop_mapping, covertype, satimage, har, gas_drift,
  volkert, miniboone and higgs. H5 and H6 now run on 36 datasets.
- **Source:** `11911a3`, `e9fe545`.
- **Applies to:** H0-E01, H0-E02 and H0-E03 (through their datasets); H1-H3,
  H5, H6.

### DEC-14

**2026-09-25 -- Record progress per iteration, read against cumulative fits.**

- **Why:** an iteration costs a different number of fits in each algorithm.
  The best validation score found so far, overall and per k, is the progress
  quantity. H0's convergence measure is built on it.
- **Source:** `cbe1ee1`, `f18a287`; `HYPOTHESES.md`, *Progress tracking*.
- **Applies to:** all.

### DEC-15

**2026-09-25 -- Experiment, run and algorithm IDs, a ledger, and no evidence
from uncommitted code.**

- **Why:** every number traces to one attempt at one hypothesis and to the
  exact code of each arm.
- **Detail:** a run with `--experiment` refuses a dirty working tree. The
  ledger was given a lock after concurrent runs overwrote an entry (`ae016ae`).
- **Source:** `7942dd4`, `ae016ae`; [`METHODOLOGY.md`](METHODOLOGY.md).
- **Applies to:** all.

### DEC-16

**2026-09-25 -- Add H0, the bug-fixed FASTENER against the 2020 code, and run
it first.**

- **Why:** H2-H6 use the fixed code, so whether the fixes change FASTENER comes
  first.
- **Detail:**
  - The arms are `fastener`, the clone's defaults, and `fastener_2020`, with
    `include_top_genes=True, allow_self_mating=True`.
  - The fixes are `fastener` `564eb8a`: no forced top genes in weighted
    information-gain mating, and no self-mating.
  - The third fix, a crash with `pool_size=None`, is never reached at
    `pool_size=3`.
- **By:** PI.
- **Source:** `2ead614`, `cb490b1`; `fastener` `564eb8a`; `HYPOTHESES.md`, H0.
- **Applies to:** H0-E01, H0-E02, H0-E03. The fixed arm is changed by
  [DEC-23](#dec-23).

### DEC-17

**2026-09-25 -- H0 measure: fits to a common validation target.**

- **Why:** "converges faster" needs a finish line both arms reach.
- **Detail:**
  - Per seed, the target is the lower of the two arms' final validation AUF
    (K = 10).
  - The measure is the unique fits each arm needed to reach that target.
  - H0-E01's criterion: the fixed arm is faster in at least 4 of 5 seeds on
    crop_mapping and on one other dataset.
- **Source:** `2ead614`, `cb490b1`; `HYPOTHESES.md`, H0.
- **Applies to:** H0-E01. H0-E02 and H0-E03 use the same measure with a
  different criterion ([DEC-21](#dec-21)).

### DEC-18

**2026-09-25 -- H0 datasets: crop_mapping, USPS, har, BASEHOCK, TOX_171.**

- **Why:** five datasets that differ in domain and shape:

  | dataset | domain |
  |---|---|
  | crop_mapping | Earth observation |
  | USPS | digit images |
  | har | sensor signals |
  | BASEHOCK | text |
  | TOX_171 | gene expression |

- **Detail:** EOData, madelon and gina are left out. The PI chose crop_mapping
  over EOData, a shorter dataset over a longer one, and asked for one genetic
  dataset. H0 makes no claim about EOData.
- **By:** PI.
- **Source:** `cb490b1`; `HYPOTHESES.md`, H0.
- **Applies to:** H0-E01.

### DEC-19

**2026-09-25 -- EO datasets in H0: 1,000 fits on a 100,000-row stratified
subsample split 40/10/50.**

- **Why:** 1,000 fits is the paper's EO setting (Table 2, Figure 9). The
  stratified subsample keeps each run affordable.
- **Detail:**
  - crop_mapping and eodata use the EO split.
  - satimage has too few rows for the EO split, so it uses the protocol split,
    also at 1,000 fits.
- **By:** PI.
- **Source:** `cb490b1`, `b1a51d3`; `HYPOTHESES.md`, H0.
- **Applies to:** H0-E01 (crop_mapping), H0-E02 (eodata, satimage), H0-E03
  (all three).

### DEC-20

**2026-09-25 -- Run datasets in parallel, one thread each.**

- **Why:** a whole experiment then fits in a day or a weekend. The runs compete
  for the CPU, so wall clock, a secondary H0 measure, is not comparable
  between arms. Fits, which decide H0, are not affected.
- **Detail:** `run_h0.py --jobs`, with one numerical-library thread per run.
- **By:** PI.
- **Source:** `1ce0622`, `b1a51d3`.
- **Applies to:** H0-E01, H0-E02, H0-E03.

### DEC-21

**2026-09-25 -- After H0-E01, test H0 on all 31 other datasets as H0-E02, with
datasets as the unit.**

- **Taken after a result:** H0-E01 was not supported, and its datasets split.
  The fixed code was faster on TOX_171 and USPS, the 2020 code on BASEHOCK, and
  neither on crop_mapping or har.
- **Why:** five datasets cannot tell which pattern is general. Taking every
  remaining dataset, rather than choosing some, keeps the choice from following
  the results.
- **Detail:**
  - Per dataset, the effect is the mean over seeds of log2(fits 2020 / fits
    fixed).
  - Criterion: a two-sided Wilcoxon test over datasets at alpha 0.05, with
    more positive effects than negative.
  - The result is incomplete if more than 6 datasets are missing.
- **By:** PI (to run further datasets). The criterion was registered before
  any H0-E02 run.
- **Source:** `b1a51d3`; `EXPERIMENTS.md`, *Experiment designs*, `H0-E02`
  (in `HYPOTHESES.md` until 2026-10-07); `HYPOTHESES.md`,
  *Revisions*, 2026-09-25.
- **Applies to:** H0-E02.

### DEC-22

**2026-09-26 -- Keep each run's records in git, but not its trajectories.**

- **Why:** trajectory files reach 2 GB per run, and can be regenerated from the
  manifest's seeds and commit. Manifests, results and progress files are kept.
- **Source:** `6bdf1f2`; `.gitignore`.
- **Applies to:** H0-E01, H0-E02, H0-E03, and every later experiment.

### DEC-23

**2026-09-30 -- Keep the top genes in the fixed FASTENER.**

- **Taken after a result:** H0-E01 and H0-E02 had been reported, and an
  exploratory look had suggested that the 2020 code ended slightly more
  accurate where the search was still improving late in its budget.
- **Why:** set by the PI. Only one change from the 2020 mating behaviour was
  intended: no self-mating.
- **Detail:**
  - `include_top_genes` now defaults to `True` in the clone.
  - The `fastener` arm is `include_top_genes=True, allow_self_mating=False`, so
    it differs from `fastener_2020` in `allow_self_mating` alone.
- **Consequence:** H0-E01 and H0-E02 tested the old fixed code, with both flags
  off. Their verdicts are about that code. Stock FASTENER in H1-H6 is the new
  default. Runs of the old and new fixed arms carry different algorithm IDs
  through both repositories' commits (FASTENER `144621c` before, `08e6acd`
  after), so they are never pooled. Up to H0-E03 the ID's config hash recorded
  only the mating version's name, so the two share a config hash (`#2ef0` at
  6,000 fits). From 2026-10-07 the config records both flags
  ([DEC-27](#dec-27)).
- **By:** PI.
- **Source:** `fastener` `08e6acd`; `f381469`; `HYPOTHESES.md`, *Revisions*,
  2026-09-30.
- **Applies to:** H0-E03; H1-H6.
- **Replaces:** the fixed arm's definition in [DEC-16](#dec-16).

### DEC-24

**2026-09-30 -- Double the fit budget on 11 datasets whose search had not
converged.**

- **Taken after a result:** decided from H0-E01's and H0-E02's validation
  curves, not from test scores.
- **Why:** the PI asked for more budget where the search was still improving.
- **Rule:** a dataset had not converged if the mean validation AUF (K = 10) of
  either arm rose by 0.005 or more over the last quarter of its budget.
  Claude proposed the threshold.
- **Detail:**
  - These 11 datasets get 12,000 fits per run, for every arm: nci9, BASEHOCK,
    lung_discrete, warpAR10P, arcene, PCMAC, TOX_171, ORL, RELATHE, warpPIE10P
    and CLL_SUB_111.
  - Every other dataset keeps 6,000 fits. The EO sets in H0 keep 1,000.
  - The budget comes from `protocol.fit_budget`.
- **Caveat:** on nci9, lung_discrete and TOX_171 the validation split has
  12-34 rows. Part of the late rise may be the search fitting validation noise.
- **By:** PI. The threshold was proposed by Claude.
- **Source:** `f381469`; `HYPOTHESES.md`, *Protocol* and *Revisions*,
  2026-09-30.
- **Applies to:** H0-E03; H1-H6.
- **Amends:** the budget in [DEC-12](#dec-12).

### DEC-25

**2026-09-30 -- Repeat H0 on all 36 datasets as H0-E03.**

- **Why:** after [DEC-23](#dec-23) and [DEC-24](#dec-24), the fixed arm that
  H0-E01 and H0-E02 tested no longer exists. H0-E03 asks H0's question of the
  current code. The claim is now narrower: that removing self-mating alone
  makes FASTENER converge faster.
- **Detail:**
  - Criterion as in H0-E02: a two-sided Wilcoxon test over all 36 datasets at
    alpha 0.05.
  - The result is incomplete if more than 7 datasets are missing.
  - The criterion was registered before any H0-E03 run.
- **By:** PI.
- **Source:** `f381469`; `EXPERIMENTS.md`, *Experiment designs*, `H0-E03`
  (in `HYPOTHESES.md` until 2026-10-07).
- **Applies to:** H0-E03.

### DEC-26

**2026-09-30 -- After the H0-E03 driver crashed, adopt its running runs instead
of restarting them.**

- **What happened:** on Windows, the driver's status write failed while
  `monitor.py` had `driver.json` open, and the driver stopped. Its 11 runs
  carried on, and one dataset had already finished.
- **Why:** those runs were intact. Restarting them would have wasted hours and
  produced a second run of the same datasets.
- **Detail:**
  - The status write now retries, then skips an update rather than failing.
  - A resumed driver adopts runs whose process is still alive.
- **Consequence:** the 12 datasets started before the crash carry experiments
  commit `f381469` in their algorithm IDs. Those started after it carry
  `6ef80c0` or later. Only the driver and monitor changed between these
  commits; the algorithm code did not.
- **Source:** `6ef80c0`, `827702d`.
- **Applies to:** H0-E03.

### DEC-27

**2026-10-07 -- Record the mating flags in FASTENER arms' algorithm-ID config.**

- **What happened:** writing the H0-E03 report showed that the fixed arm's
  config hash was `#2ef0` in both H0-E02 and H0-E03, although
  `include_top_genes` had changed between them ([DEC-23](#dec-23)). The config
  recorded only the mating version's name, "fixed".
- **Why:** an algorithm ID must change whenever what the arm does changes. The
  commit hashes already told the two arms apart, but a change made only in the
  experiments' own definition of "fixed" would not have.
- **Detail:** `run_sota.py` adds `include_top_genes` and `allow_self_mating` to
  each FASTENER arm's config. Config hashes of FASTENER arms change from this
  commit on; runs before it keep theirs.
- **Source:** the commit that adds this entry.
- **Applies to:** H1-H6, and any later H0 experiment.

### DEC-28

**2026-10-07 -- Use the new FASTENER for every later experiment.**

- **Taken after a result:** H0-E03 was reported as not supported. Without
  self-mating, the current code converged neither faster nor slower than the
  2020 code (14 datasets to 22, Wilcoxon p = 0.519), and its best final F1 was
  level (18 to 18).
- **Why:** set by the PI. The new code is the fixed one, and H0-E03 found it no
  worse than the 2020 code in speed or in end result.
- **Detail:**
  - The new FASTENER is the clone at `08e6acd` with
    `include_top_genes=True, allow_self_mating=False`, the "fixed" mating in
    `run_fastener.MATING_VERSIONS` and the clone's defaults.
  - Every FASTENER arm in H1-H6 runs it: stock FASTENER and both swap arms.
    The `fastener_2020` arm runs only where an experiment's design names it.
  - No code change was needed: every FASTENER run is built by
    `run_fastener.make_mating`, whose stock and swap arms already use "fixed".
- **By:** PI.
- **Source:** `HYPOTHESES.md`, *Protocol* (row *FASTENER version*) and
  *Revisions*, 2026-10-07.
- **Applies to:** H1-H6.
- **Confirms:** [DEC-23](#dec-23), which set this for stock FASTENER before
  H0-E03 ran.

### DEC-29

**2026-10-07 -- H1 on eight datasets spread by feature count, not the four
development sets.**

- **Why:** H1's mechanism is that OBL starts every individual at about half the
  features, so the handicap it predicts grows with the feature count p and
  vanishes at small p. The four development sets span only 174-970 features
  and could show neither end.
- **Detail:**
  - The eight: satimage (36 features), eodata (182), USPS (256), har (561),
    COIL20 (1,024), gisette (5,000), Prostate_GE (5,966), arcene (10,000).
    satimage is where the claim predicts no difference.
  - Crop mapping, madelon and gina leave H1; they remain development sets for
    H2, H3, H5 and H6.
  - The criterion keeps its form: 4 of 5 seeds on EOData and on at least one
    other of the eight. `make_report.py` reads H1 on the eight (`H1_SETS`).
- **By:** PI, choosing from candidates Claude proposed by feature count.
- **Taken before any H1 result.** It was committed in `3e1ce0c` without the
  matching text in `HYPOTHESES.md`; H1-E01 started from that commit
  ([DEC-31](#dec-31)).
- **Source:** `3e1ce0c`; `HYPOTHESES.md`, H1 and *Revisions*, 2026-10-07.
- **Applies to:** H1-E01, H1-E02.

### DEC-30

**2026-10-07 -- Run one process per dataset, arm and seed, at most ten at a
time.**

- **Why:** `run_sota.py` runs a dataset's arms and seeds one after another on
  one core, so the slowest dataset (EOData, about 47 hours for both arms) would
  have set the wall clock alone. Split into 80 jobs on ten processes, H1 takes
  about half a day.
- **Detail:**
  - `run_sota.py --seed` runs a single seed. Every search seeds its own random
    stream, so a seed run alone gives the same front as the same seed inside a
    five-seed run; checked on madelon for both arms before H1-E01.
  - `run_queue.py` starts the jobs in the order given, slowest first, and keeps
    up to `--max-procs` running. It writes `results/<ID>/queue.json`, which
    `monitor.py --experiment <ID>` reads.
  - Each job is its own run ID; `make_report.py` merges an experiment's runs
    by dataset, arm and seed.
  - As under [DEC-20](#dec-20), the jobs compete for the CPU, so wall clock is
    not comparable between arms. Fits are not affected.
- **By:** PI.
- **Source:** `3e1ce0c` (`--seed`, `run_queue.py`); the commit that adds this
  entry (`queue.json`, `monitor.py --experiment`).
- **Applies to:** H1-E01, H1-E02.

### DEC-31

**2026-10-07 -- Stop H1-E01 and restart H1 as H1-E02.**

- **Why:** the PI stopped H1-E01 after 13 minutes to restart it with a monitor
  that shows every job at once. Its registration also did not yet describe its
  datasets ([DEC-29](#dec-29)), and `make_report.py` would have read only one
  of its eight. No run had finished and no score was read.
- **Detail:** H1-E01 keeps its ID and is recorded as failed, with a short
  report. H1-E02 runs the same design from the commit that registers it.
- **By:** PI.
- **Source:** `EXPERIMENTS.md`, H1-E01 and H1-E02; `reports/H1-E01/REPORT.md`.
- **Applies to:** H1-E01, H1-E02.

### DEC-32

**2026-10-09 -- Split each report into a short reading (REPORT.md) and its
record (SUPPORT.md).**

- **Why:** a report holding every run ID, parameter and per-seed number was
  complete but unreadable. The PI asked for a report a reader can follow, with
  the tracking detail kept beside it.
- **Detail:**
  - `REPORT.md` has three sections. *In brief* gives the hypothesis, how it
    is judged and the answer, in plain words with one figure. *Findings* gives
    F1 to FN one at a time, each with an explanation and a figure. The
    *Assessment* judges the hypothesis on the findings, written as for a
    paper.
  - `SUPPORT.md` holds the header, the hypothesis and criteria quoted
    verbatim, the description of the experiment, the evidence tables and the
    reproduction commands.
  - `make_report.py` generates both. The `experiment-report` skill
    (`.claude/skills/experiment-report/SKILL.md`) is the procedure for writing
    them. `METHODOLOGY.md`, *The report*, states the rules.
  - Reports before H1-E02 keep the earlier single-file form.
- **By:** PI.
- **Taken after a result:** H1-E02's report had been drafted in the old form.
  No verdict or criterion changed: it only changes how a report is laid out.
- **Source:** the commit that adds this entry; `METHODOLOGY.md`, *The report*.
- **Applies to:** H1-E02 and every later experiment.

### DEC-33

**2026-10-09 -- H2 and H3 on the 39 UCR/UEA sets and EOData, read with
datasets as the unit, at a budget calibrated per dataset.**

- **Why:** the four development sets cover 174-970 features and two domains,
  too narrow for a claim about an operator FASTENER lacks on any data. With
  40 datasets the per-seed rule on EOData and one other set is no longer the
  useful test. Fits past the point where a search has settled buy nothing, and
  that point differs between datasets by more than the protocol's two budgets
  allow for.
- **Detail:**
  - Datasets: the 39 of `DATASETS_USED.md` (with UWaveGestureLibraryAll in
    place of UWaveGestureLibrary, which the archive serves with 440 rows), and
    EOData at the 50,000-row cap.
  - Criterion: per-dataset effect = mean over 5 seeds of the swap arm's test
    AUF (K = 10) minus stock's; supported if positive on more datasets than
    negative and a two-sided Wilcoxon signed-rank test is significant at
    alpha = 0.05, reversed if the same with signs swapped. More than 6 of 40
    datasets missing makes the result incomplete. EOData's 4-of-5 count,
    per-cluster effects and the pruning counters are secondary.
  - Budget: per dataset, from one Boruta run and one 12,000-fit stock FASTENER
    run, seed 1999, validation only. The smallest of 1,000, 2,000, 4,000,
    6,000 or 12,000 fits at which validation AUF (K = 10) is within 0.005 of
    its value at 12,000 and no more than 0.005 below Boruta's, then one step
    up. The same budget for every arm.
  - FASTENER clone `b7e724d` (fastener): adds the pruning counters only; the
    search is unchanged.
- **By:** PI. The datasets and the criterion were chosen from options Claude
  proposed; the calibration with Boruta as the reference is the PI's.
- **Taken before any H2 or H3 run.**
- **Source:** `b7e724d` (fastener); `a6f91c9`, `ba193c3`; `HYPOTHESES.md`, H2,
  H3 and *Revisions*, 2026-10-09.
- **Applies to:** H2, H3.

### DEC-34

**2026-10-09 -- DuckDuckGeese leaves H2 and H3.**

- **Why:** at 363,150 features its FASTENER calibration run reached 1,480 of
  12,000 fits in an hour, about nine hours in all, against two to three hours
  for the next slowest dataset; its 15 experiment runs would cost as much each.
  The cost is FASTENER's per-subset bookkeeping over every feature, not
  anything the swap hypotheses are about.
- **Detail:** H2 and H3 run on 39 datasets, EOData and 38 UCR/UEA sets; C2
  keeps MotorImagery, PEMS-SF, Heartbeat and EigenWorms. The criterion and
  the limit of 6 datasets left out are unchanged. DuckDuckGeese's calibration
  run was stopped; its Boruta run had finished and is kept, unread.
  `make_report.SWAP_EXCLUDED` leaves it out of the reading.
- **By:** PI.
- **Taken during the budget calibration, before any H2 or H3 run.** No
  calibration result of DuckDuckGeese was read.
- **Source:** the commit that adds this entry; `HYPOTHESES.md`, H2 and
  *Revisions*, 2026-10-09; `EXPERIMENTS.md`, H2H3-E01.
- **Applies to:** H2H3-E01.

## By experiment

Which decisions each experiment ran under, and which it led to. The protocol
decisions [DEC-01](#dec-01) to [DEC-15](#dec-15) apply to every experiment and
are not repeated.

| experiment | status | ran under | led to | report |
|---|---|---|---|---|
| `H0-E01` | reported: not supported | [DEC-16](#dec-16), [DEC-17](#dec-17), [DEC-18](#dec-18), [DEC-19](#dec-19), [DEC-20](#dec-20) | [DEC-21](#dec-21) | [H0-E01](reports/H0-E01/REPORT.md) |
| `H0-E02` | reported: supported, narrowly | [DEC-16](#dec-16), [DEC-17](#dec-17), [DEC-19](#dec-19), [DEC-20](#dec-20), [DEC-21](#dec-21), [DEC-22](#dec-22) | [DEC-23](#dec-23), [DEC-24](#dec-24), [DEC-25](#dec-25) | [H0-E02](reports/H0-E02/REPORT.md) |
| `H0-E03` | reported: not supported | [DEC-17](#dec-17), [DEC-19](#dec-19), [DEC-20](#dec-20), [DEC-22](#dec-22), [DEC-23](#dec-23), [DEC-24](#dec-24), [DEC-25](#dec-25), [DEC-26](#dec-26) | [DEC-27](#dec-27), [DEC-28](#dec-28) | [H0-E03](reports/H0-E03/REPORT.md) |
| `H1-E01` | failed: stopped before any run finished | [DEC-07](#dec-07), [DEC-23](#dec-23), [DEC-24](#dec-24), [DEC-27](#dec-27), [DEC-28](#dec-28), [DEC-29](#dec-29), [DEC-30](#dec-30) | [DEC-31](#dec-31) | [H1-E01](reports/H1-E01/REPORT.md) |
| `H1-E02` | reported: supported | [DEC-07](#dec-07), [DEC-23](#dec-23), [DEC-24](#dec-24), [DEC-27](#dec-27), [DEC-28](#dec-28), [DEC-29](#dec-29), [DEC-30](#dec-30), [DEC-31](#dec-31) | [DEC-32](#dec-32) | [H1-E02](reports/H1-E02/REPORT.md) |
| H2-H6 | not started | [DEC-07](#dec-07) (H5, H6), [DEC-13](#dec-13), [DEC-23](#dec-23), [DEC-24](#dec-24), [DEC-27](#dec-27), [DEC-28](#dec-28), [DEC-33](#dec-33), [DEC-34](#dec-34) (H2, H3) | -- | -- |
