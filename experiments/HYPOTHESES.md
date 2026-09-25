# Hypotheses and protocol, fixed before the runs

Written 2026-09-25, before any experiment in this round was started. Nothing
below may be revised after results exist; a revision gets a dated entry at the
bottom saying what changed and why, so that the difference between "what we set
out to test" and "what we found" stays legible.

**Hypotheses are numbered in the order they are to be run.** Renumbered
2026-09-25 from the first draft of this file; no content changed, only labels:

| now | was | |
|---|---|---|
| H1 | H6 | NSGA-II's small-k weakness as an initialisation artifact |
| H2 | H2 | a size-preserving move changes the front at all |
| H3 | H1 | the guided swap specifically improves small-k |
| H4 | H3 | the published FASTENER > FS-SDS ordering under a clean protocol |
| D1 | H4 | *(deferred)* the replication gap is a grading artifact |
| D2 | H5 | *(deferred)* conclusions are model-dependent |

Deferred items are lettered, not numbered, so they never occupy a slot in the
run order.

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

Nothing blocks the order: the metric question that held H2 and H3 was settled
before the first run (see "Metrics", below).

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
seeds** at k <= 10, on **both** datasets. A null here with a positive H3 would be
the interesting outcome (guidance is doing the work); a null in both is the
likely one given the pilot.

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
at k <= 10, on **both** datasets. Fewer than that at the pilot's effect size is
indistinguishable from noise, and H3 is recorded as not supported.

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

**Note on scope.** Confirmed in scope 2026-09-25 (see Decisions recorded). This
is a correction to a paper the PI co-authored, and is framed as such: a confound
identified and measured, not a defect claimed.

---

## Deferred, deliberately

Lettered rather than numbered: they hold no slot in the run order.

**D1 -- the replication gap is a grading artifact.** *(was H4)* Deferred by the
PI. `WHY_RESULTS_DIFFER.md` already reconciles FASTENER to +0.026 via
`min_samples_leaf=2` plus binary F1, and leaves FS-SDS unexplained. Note the
dependency: H4 compares against the published table, so an unexplained offset
against that table weakens H4's interpretation. If H4's result is to be stated
in absolute terms rather than as an ordering, D1 comes back.

**D2 -- conclusions are model-dependent.** *(was H5)* Declined by the PI.
Recorded because the pilot measured the size of what is being set aside: on
gina, HistGradientBoosting scored +0.06 at k=10 and +0.12 at k=400 over the
decision tree, and at k=400 it beat the all-features decision-tree baseline by
0.099. Every result in this round is therefore a statement about decision trees,
and says so.

---

## Decisions recorded

Both questions that were open when this file was first written have been
settled before any run. Nothing below is outstanding.

**1. RESOLVED before the first run (2026-09-25).** The metric rule is: **F1 for
classification, MAE for regression.** Every dataset in this round is
classification, so F1 is primary throughout and the MAE branch is not exercised;
it is recorded so a future regression task inherits a rule rather than a fresh
decision. How F1 becomes a front metric is fixed under "Metrics" above: AUF
where a published value is being matched (H4), hypervolume where arms are
compared only against each other (H1, H2, H3). No hypothesis is blocked.

**2. RESOLVED before the first run (2026-09-25).** H4 is **in scope**. Its
status had been stated twice in one instruction -- declined, then reinstated
("let's give H3 a try again", referring to its old number) -- and the later
statement stands. The run order is H1, H2, H3, H4, with H4 last.

Recorded because it matters for how H4 is reported: it is in scope by an
explicit decision, not by drift. If it is dropped later, that is a change to a
pre-registered plan and gets a dated entry at the bottom of this file, not a
silent deletion.

---

## Datasets

Unchanged from the previous round and already downloaded: madelon (500
features, synthetic), gina (970, real-world), and the 25 scikit-feature
benchmarks for H4. EOData is available but out of scope for this round -- at
480k rows x 182 features it is a different cost regime.

## Analysis plan

Decided now, so that no metric is chosen after seeing the data:

1. Per hypothesis, the falsification criterion above, evaluated first.
2. Per-seed paired comparison against the relevant baseline arm, reported as
   the per-seed table, not only as a mean.
3. Seed spread shown on every figure -- min-max band or per-seed points. A mean
   is never plotted alone.
4. Wall clock reported next to fit counts for every arm.
5. Any arm that stops on something other than the budget says so (`stopped_on`).
