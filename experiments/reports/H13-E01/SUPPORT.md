# H13-E01 -- supporting record

The record behind [REPORT.md](REPORT.md).

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H13-E01` |
| Hypothesis ID | H13 (post hoc, [DEC-55](../../DECISIONS.md#dec-55)) |
| Runs | none of its own. 1,544 finished runs of `nsga2`, `nsga2_sparse` and `nsgaii_miip` over 46 datasets: H1-E02 80, H5H6-E01 478, H5H6-E02 525, H5H6-E03 461 (their ledger rows; `tables/run_measures.csv` lists every run ID) |
| Algorithm IDs | as in the source reports: H1-E02 `c142251+08e6acd`; H5H6-E01 `2e7a100`, `33fa95e`, `d2102c5` (+ `3be5697`); H5H6-E02 `5efd5a3`, `f3eb230` (+ `3be5697`, per its SUPPORT; the distilled table has no commit for cluster runs); H5H6-E03 `fbbecfe+3be5697` |
| Pre-registration | `be8bcca` (HYPOTHESES.md H13, EXPERIMENTS.md H13-E01, DECISIONS.md DEC-55), committed and pushed before any H13 number was computed |
| Code commits | `h13_coverage.py`, `h13_report.py`, `tests/test_h13_coverage.py` registered at `be8bcca`; the presentation and the two defects fixed after the first run (section 4) are in the commit that adds this report |
| Dates | registration and report 2026-11-02; source runs 2026-10-07 to 2026-10-28 |
| Verdict | **not supported (post hoc)**: (a) and (c) hold in all four grids, (b) fails under the random forest (`tables/verdict.json`) |

## 2. Hypothesis

Quoted verbatim from `experiments/HYPOTHESES.md` at `be8bcca`:

> ## H13 -- At a fixed fit budget, the start decides NSGA-II's AUF at small k by whether the front reaches k <= 10, not by its quality there (post hoc)
>
> *(2026-11-02; proposed by the PI for paper P2, after the end-of-budget
> results of these runs had been read in H1-E02 and H5H6-E01 to -E03 and in an
> unregistered exploratory analysis of `experiments/distilled_logs/`. **Post
> hoc**: formed from the results it is judged on, so it cannot confirm
> anything; see [DEC-55](DECISIONS.md#dec-55).)*
>
> **Claim.** Among the three NSGA-II arms, the OBL start (`nsga2`), the 1-30
> start (`nsga2_sparse`) and the full NSGAII-MIIP (`nsgaii_miip`), the
> difference in AUF (K = 10) comes mostly from **reach**: whether the
> final front holds any subset of at most k features. It does not come from
> the quality of the subsets the arms return at the sizes both of them reach.
>
> **Why it might hold.** OBL starts every individual near d/2 features, and the
> balanced mutation has zero expected drift in size, flipping about 2k/d bits
> per child (P2's EVIDENCE.md). Only selection pulls size down, and at
> 2,000-12,000 fits it does not get to k <= 10 once d is in the hundreds. A
> front that never reaches k <= 10 scores 0 there by AUF's convention, so
> for most of the range AUF measures reach.
>
> **Why it might not.**
> 1. Where both arms do reach, one may still be better at matched size. The
>    sparse start spends its fits inside the measured range.
> 2. Reach is not one event. The sparse start begins inside the range and can
>    drift out of it, and the OBL start can arrive late. Either would make the
>    final front a poor summary of the run.
> 3. The comparison is confounded with how much budget each arm actually spends.
>    Under E02 and E03 the stagnation stop ends some runs early, and under E01 and
>    E03 timeouts remove runs, mostly OBL runs on large d. Missing runs may carry
>    the effect.
> 4. NSGAII-MIIP's MI improvement phase may restore reach from an OBL start,
>    which would mean the start matters less than the claim says.
>
> **Claim type.** Descriptive and associational, within one implementation
> (the NSGAII-MIIP port's operators). No causal claim about NSGA-II in general.
>
> **Criterion** (post hoc; per grid G in {H5H6-E01, -E02, -E03}, `nsga2_sparse`
> against `nsga2`, datasets as the unit):
>
> * (a) **Reach.** R = share of a dataset's finished seeds whose final front
>   holds a subset of at most 10 features. The sparse arm has the higher R on
>   more datasets than the OBL arm does, and a two-sided Wilcoxon over the
>   per-dataset differences gives p < 0.05 after Holm across the four grids
>   (H1-E02 included).
> * (b) **Matched size.** Over the datasets where both arms reach some k <= 10
>   in at least 3 of their finished seeds, the 95% paired-bootstrap interval of
>   the mean per-dataset matched-size difference (defined in H13-E01) lies
>   within +/-0.02 F1.
> * (c) **Decomposition.** The reach term carries at least 75% of the summed
>   absolute AUF difference over the grid's datasets.
>
> H13 is **supported (post hoc)** if (a), (b) and (c) hold in all three
> H5H6 grids. It is **reversed** if (c) gives a reach share below 50% in at
> least two of them, which would mean quality at matched size, not reach,
> carries the difference. Otherwise it is **not supported**. H1-E02 is read
> the same way and reported beside the grids. It enters (a)'s Holm family but
> not the verdict, because it is the experiment the claim grew out of.
>
> **Reported beside it** (descriptive, Holm within each family): NSGAII-MIIP
> as a third arm; reach against d and budget; the cost at the large-subset
> end; time to reach; stagnation stops; missing cells; the classifier.
> These are H13-E01's Q2-Q8.
>
> **Data.** No new runs. The H1-E02 and H5H6-E01 to -E03 runs of the three
> arms, read from `experiments/distilled_logs/`.
>
> **Experiments.**
>
> * `H13-E01` -- the criterion above and Q2-Q8 on 1,544 runs over 46 datasets.
>
> A confirmatory test needs runs not yet seen. P2's extended pilot (new starts,
> an OBL budget sweep, the mutation control, every evaluated subset logged) is
> registered separately, before it runs.

## 3. Evaluation criteria and design

Quoted verbatim from `experiments/EXPERIMENTS.md` at `be8bcca`. The placeholder for the exploratory
table was still open at that commit and is still open now (section 4):

> ### `H13-E01` -- H13 (post hoc): reach and matched-size quality of three NSGA-II arms, on the H1 and H5/H6 runs
>
> Registered 2026-11-02, **after** the end-of-budget results of every run it
> reads had been seen ([DEC-55](DECISIONS.md#dec-55)). What had been seen is
> listed under *Already seen* below.
>
> **Design.** An analysis of existing runs. No new searches and no model fits.
>
> | | |
> |---|---|
> | runs read | every finished run of `nsga2`, `nsga2_sparse` and `nsgaii_miip` in H5H6-E01 (decision tree, no stagnation stop, workstation), H5H6-E02 (random forest, stagnation stop at 50 barren generations, Vega) and H5H6-E03 (LightGBM, the same stop, Vega), and of `nsga2` and `nsga2_sparse` in H1-E02 (decision tree, no stop) |
> | counts | 1,544 finished runs over 46 datasets: H1-E02 80 (8 datasets); H5H6-E01 478 (36 datasets with at least one finished run of these arms), H5H6-E02 525 (39), H5H6-E03 461 (39). Not finished: 47 timeouts under E01 (nsga2 6, nsga2_sparse 30, nsgaii_miip 11), none under E02, 64 under E03 (36, 1, 27); the skipped cells of [`h5h6_skip.txt`](h5h6_skip.txt) in all three grids |
> | source | `experiments/distilled_logs/<ID>/{runs,records,curves,jobs}.csv.xz`; budgets from [`h2h3_budgets.json`](h2h3_budgets.json) and, for H1-E02, `protocol.fit_budget` (6,000; 12,000 on arcene). Feature lists are not in the distilled tables and are not needed |
> | unit | the dataset within a grid. A dataset's value for an arm is the mean over its finished seeds, as in the H5H6 reports (`make_report.py`). Seeds stay within datasets and are never pooled across them. A dataset enters a pair if both arms have at least one finished seed there. H1-E02 is its own grid and is never pooled with H5H6-E01, although both use the tree and share EOData |
> | AUF | `make_report.opt_curve` and `auf`, unchanged: at each k, the subset of size <= k chosen on validation and scored on test, 0 below the smallest subset on the front. AUF is an existing measure (Koprivec et al., 2020), not a contribution |
> | tests | two-sided Wilcoxon signed-rank over per-dataset differences, zero differences dropped (`make_report.wilcoxon_p`); Holm step-down (`make_report.holm`); alpha = 0.05 |
> | effect sizes | for every comparison: wins/ties/losses; the mean and median per-dataset difference with a 95% percentile paired bootstrap over datasets (10,000 resamples, seed 20200, as `h10_report.py`); the matched-pairs rank-biserial correlation (W+ - W-)/(W+ + W-) |
> | where, cost | this workstation; the distilled tables only, so no access to `results/` is needed and the cost is minutes |
> | code | `experiments/h13_coverage.py` (the measures), `experiments/h13_report.py` (tables, figures, REPORT.md and SUPPORT.md skeletons), `tests/test_h13_coverage.py`, all committed before the report is generated |
>
> **Definitions.** For a run and k = 1..10, *reach(k)* is true if the final
> front holds a subset of at most k features, and *c(k)* is that run's
> `opt_curve` value at k, defined only when reach(k) holds. Per dataset and
> arm: r(k) is the share of finished seeds with reach(k), and c̄(k) is the mean
> of c(k) over those seeds. Then R = r(10). The seed-mean AUF is
> (1/10) Σ_k r(k)·c̄(k), which equals the mean of the seeds' AUFs.
>
> * **Matched-size difference** of arms a and b on a dataset: the mean over
>   M = {k <= 10 : r_a(k) >= 0.6 and r_b(k) >= 0.6} of c̄_a(k) - c̄_b(k). The
>   dataset counts only if M is not empty. It is conditional on reaching, so the
>   number of datasets dropped is always shown beside it.
> * **Decomposition** of the AUF difference on a dataset, exactly:
>   r_a c̄_a - r_b c̄_b = (r_a - r_b)(c̄_a + c̄_b)/2 + (r_a + r_b)(c̄_a - c̄_b)/2,
>   summed over k and divided by 10. The first term is the **reach term** and
>   the second the **quality term**. Where an arm has r(k) = 0, its c̄(k) is set
>   to the other arm's, so that k contributes only to reach. *Reach share* =
>   Σ_datasets |reach| / (Σ |reach| + Σ |quality|).
>
> **Questions.** Q1 is H13's criterion. Q2-Q8 are descriptive. Each states its
> Holm family.
>
> | | question | measure | test, family |
> |---|---|---|---|
> | Q1 | reach against matched-size quality | (a) R; (b) matched-size difference; (c) decomposition, for sparse against OBL. Also exact-size matching (subsets of exactly k on both fronts) as a check of (b) | (a) Wilcoxon, Holm over the 4 grids; (b) bootstrap interval; (c) a share, no test |
> | Q2 | reach as a function of d and budget | per run, logistic regression of reach(10) on log2 d and log2 (budget / population), per arm and grid, with a dataset-cluster bootstrap for the coefficients. Beside it, the analytic probability that an OBL start of 50 complementary pairs holds a subset of <= 10 features, 1 - (1 - 2 F(10; d, 1/2))^50, against the observed reach at the first and the last snapshot. Budget was calibrated per dataset and is correlated with d, so the two coefficients are read together, not separately. A fit with complete separation on d is flagged and only the d at which predicted reach is 1/2 (at the grid's median budget) is read | descriptive; no test |
> | Q3 | NSGAII-MIIP as a third arm | Q1's (a)-(c) and AUF for the three pairs sparse-OBL, sparse-MIIP and MIIP-OBL | Wilcoxon, Holm over the 3 pairs within each grid and measure |
> | Q4 | the cost at the large-subset end | AUF at K = 20 (the protocol's second K); AUF at K = d (the whole front, the same function); the best test F1 on the front without a size limit (chosen on validation); the largest subset on the front | Wilcoxon, Holm over the 3 pairs within each grid and measure |
> | Q5 | missing cells | a table per grid and arm: finished, timed out (all seeds or some), skipped. Sensitivity of Q1 (a), (c) and Q3's AUF to: S1, only datasets where both arms finished all 5 seeds; S2, every missing run counted as not reaching, with AUF 0 (pessimistic for the arm that is missing); S3, only datasets where all three arms have a result. Reported: whether any Holm decision or criterion part changes | as Q1/Q3, rerun under each of S1-S3 |
> | Q6 | the classifier, on common datasets | datasets where the arm has at least one finished seed under all three classifiers. Per arm: R and AUF; per pair: the sparse-OBL AUF difference and reach share. E01 against E02 or E03 also changes the stagnation stop, the hardware and the code commit, so it is not a clean classifier contrast. E02 against E03 is the clean one | Friedman over the 3 classifiers, then Wilcoxon on the 3 pairs of classifiers, Holm over those 3 |
> | Q7 | time to reach | from `curves`, the first snapshot whose archive (the best subset at each size among every subset scored so far, `trajectory.Trajectory`, written after every generation) has min_size <= 10, in fits (as a share of budget) and seconds. A run whose archive never reaches is censored at its last snapshot and never assigned the budget. Per arm and grid: Kaplan-Meier curves, the share reached by 10/25/50/100% of the budget, the median. Also *lost reach*: the archive reached k <= 10 but the final front (the last population's first rank, `records`) does not. Seconds are compared only within a grid | per dataset, the restricted mean time to reach (area under its seeds' KM curve up to the budget, censoring handled by KM); Wilcoxon over datasets per pair, Holm over the 3 pairs within each grid. Not a log-rank test over runs, which would pool seeds across datasets |
> | Q8 | stagnation stops | per arm, E02 and E03: runs stopped on stagnation, fits used at the stop as a share of budget, and R among stopped against budget-stopped runs. Proposals ≈ iterations x population; repeat share = 1 - fits / proposals, against d and the median final-front size, beside the 2k/d flips per child expected from the mutation. E01 has no stop (its 47 timeouts were mostly the same spinning, its report's F5), and its classifier, hardware and commit differ too, so E01 against E02/E03 is **not an ablation of the stop** | descriptive; no test |
>
> **Scope (the P3 boundary).** Only the three NSGA-II arms. No FASTENER arm,
> POSS, FS-SDS, filter or ranking of selectors is computed or shown. Those
> belong to P3 (H5H6) and P6 (H10/H11).
>
> **Already seen when this was registered** (so none of it is prospective):
>
> 1. The reports of H1-E02, H5H6-E01, H5H6-E02, H5H6-E03 and H7-E01 in full,
>    including these arms' per-dataset AUF (K = 10), pairwise results,
>    timeouts (H5H6-E01, F5) and fit and time totals.
> 2. The unregistered exploratory analysis of `experiments/distilled_logs/`
>    by `p2_scan.py`, `p2_deep.py` and `p2_matched.py`. Its whole output counts
>    as seen. Its summary is the table in P2's RESEARCH-PLAN.md, *Obstoječi
>    teki H5H6-E01–E03*, quoted here verbatim:
>
>    > **[TO INSERT: the table as committed in P2's RESEARCH-PLAN.md]**
>
> 3. The cell accounting above (job states and `stopped_on` counts), read on
>    2026-11-02 while drafting this design. No score was read for it.
>
> Where H13-E01's code gives a number that differs from (2), the report says so
> and explains the difference. Neither number is adjusted to match the other.

## 4. Description of the experiment

**Setup.** As registered: the three arms, the four grids, datasets as the unit, means over finished
seeds, `make_report.opt_curve` and `auf` unchanged, Wilcoxon with zeros dropped, Holm, 10,000-resample
bootstrap with seed 20200, read from `experiments/distilled_logs/` only. The arms, in plain words:

* `nsga2` -- NSGA-II with the NSGAII-MIIP port's tournament, crossover and balanced mutation (rate 1/d),
  population 100, started by OBL: 50 random bit strings with p = 1/2 and their complements.
* `nsga2_sparse` -- the same, started from 100 random subsets of 1 to min(30, d) features (a departure
  from the source, H1).
* `nsgaii_miip` -- the full NSGAII-MIIP port: OBL start plus its mutual-information improvement phase.

Under H5H6-E02 and -E03 all three stop after 50 generations with no new subset (DEC-41); under H1-E02 and
H5H6-E01 they ran until the budget or the 6-hour cap.

**Deviations from the registration.**

* None in the criterion, the margins or the thresholds.
* The exploratory table that the design says to quote is not quoted: it is in an uncommitted version of
  P2's RESEARCH-PLAN.md on another machine. H13's numbers could therefore not be compared with it; the
  comparison is made against the four source reports instead (below).
* Two defects of `h13_report.py` found on its first run on the data, fixed before any number was read
  into the report: `write_csv` dropped the pair's second arm (a column named `b`), and the Q8 repeat share
  `1 - fits / (100 x (generations + 1))` is negative for NSGAII-MIIP (-0.18 under the tree), whose
  improvement phase fits subsets outside the generations; it is now left undefined for that arm. The
  rows of `run_keys.csv` with an empty seed (the deterministic selectors) were skipped in the
  reproduction check. Figures were relabelled, and F8 (the classifier, Q6) was added so that Q6 has a
  figure. No measure, test or rule changed.

**What happened.**

* One analysis run on the workstation, about 75 s, repeated after each fix; the numbers of the criterion
  were identical in every repetition.
* **Reproduction.** This script's AUF at K = 10 and K = 20 matches every run's value in the four source
  reports' `run_keys.csv` to within 8e-16 (1,544 of 1,544 runs found):

| grid | runs | not_in_report | max_abs_diff_auf_k10 | max_abs_diff_auf_k20 | n_diff_auf_k10 | n_diff_auf_k20 |
|---|---|---|---|---|---|---|
| H1-E02 | 80 | 0 | 2.22e-16 | 4.44e-16 | 0 | 0 |
| H5H6-E01 | 478 | 0 | 2.22e-16 | 3.33e-16 | 0 | 0 |
| H5H6-E02 | 525 | 0 | 3.33e-16 | 5.55e-16 | 0 | 0 |
| H5H6-E03 | 461 | 0 | 4.44e-16 | 7.77e-16 | 0 | 0 |

* **Cells without a run** (Q5):

| grid | method | finished | timeout | skipped | other | datasets_all_missing | datasets_some_missing |
|---|---|---|---|---|---|---|---|
| H1-E02 | nsga2 | 40 | 0 | 0 | 0 | 0 | 0 |
| H1-E02 | nsga2_sparse | 40 | 0 | 0 | 0 | 0 | 0 |
| H5H6-E01 | nsga2 | 164 | 6 | 25 | 0 | 6 | 1 |
| H5H6-E01 | nsga2_sparse | 165 | 30 | 0 | 0 | 6 | 0 |
| H5H6-E01 | nsgaii_miip | 149 | 11 | 35 | 0 | 9 | 1 |
| H5H6-E02 | nsga2 | 170 | 0 | 25 | 0 | 5 | 0 |
| H5H6-E02 | nsga2_sparse | 195 | 0 | 0 | 0 | 0 | 0 |
| H5H6-E02 | nsgaii_miip | 160 | 0 | 35 | 0 | 7 | 0 |
| H5H6-E03 | nsga2 | 134 | 36 | 25 | 0 | 11 | 2 |
| H5H6-E03 | nsga2_sparse | 194 | 1 | 0 | 0 | 0 | 1 |
| H5H6-E03 | nsgaii_miip | 133 | 27 | 35 | 0 | 11 | 2 |

* **Lost reach.** In all 1,544 runs the final front holds a subset of at most 10 features exactly when
  the archive does; no run lost reach.
* The distilled `runs` table flags H1-E02's and H5H6-E01's runs `dirty`: that flag counts every
  uncommitted change, data included. Their own reports found `code_dirty: false` on every finished run.
* Friedman's test raised a warning for the 1-30 start's reach (identical, 1.0, under all classifiers);
  its p-value is reported as empty.

## 5. Evidence

**Criterion (Q1), `nsga2_sparse` minus `nsga2`** (`tables/q1_criterion.csv`):

| grid | n_datasets | wins | ties | losses | mean_delta | mean_lo | mean_hi | p | p_holm | rank_biserial | a_holds | b_n_matched | b_mean | b_lo | b_hi | b_holds | b_exact_mean | b_exact_lo | b_exact_hi | reach_share | c_holds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1-E02 | 8 | 7 | 1 | 0 | 0.8500 | 0.6000 | 1.0000 | 0.0156 | 0.0156 | 1.0000 | True | 1 | -0.0065 | -0.0065 | -0.0065 | True | -0.0070 | -0.0070 | -0.0070 | 0.9984 | True |
| H5H6-E01 | 30 | 22 | 8 | 0 | 0.6800 | 0.5067 | 0.8400 | 6.11e-06 | 1.83e-05 | 1.0000 | True | 10 | -0.000807 | -0.0044 | 0.0025 | True | 0.000661 | -0.0015 | 0.0027 | 0.9973 | True |
| H5H6-E02 | 34 | 24 | 10 | 0 | 0.6353 | 0.4706 | 0.7824 | 3.02e-06 | 1.21e-05 | 1.0000 | True | 13 | -0.0136 | -0.0436 | 0.0083 | False | -0.0111 | -0.0421 | 0.0115 | 0.9812 | True |
| H5H6-E03 | 28 | 17 | 11 | 0 | 0.5429 | 0.3643 | 0.7214 | 0.000106 | 0.000211 | 1.0000 | True | 13 | 0.000674 | -0.0062 | 0.0082 | True | 0.0052 | 5.34e-05 | 0.0121 | 0.9922 | True |

Mechanical reading: {"verdict": "not supported (post hoc)", "H1-E02": {"a": true, "b": true, "c": true}, "H5H6-E01": {"a": true, "b": true, "c": true}, "H5H6-E02": {"a": true, "b": false, "c": true}, "H5H6-E03": {"a": true, "b": true, "c": true}}.

**Per dataset** (`tables/q1_terms.csv`; matched values only where both arms reach in 3 of 5 seeds):

| grid | dataset | d | R_a | R_b | reach_term | quality_term | auf_delta | matched | matched_exact |
|---|---|---|---|---|---|---|---|---|---|
| H1-E02 | satimage | 36 | 1.0000 | 1.0000 | 0.0000 | -0.0065 | -0.0065 | -0.0065 | -0.0070 |
| H1-E02 | eodata | 182 | 1.0000 | 0.2000 | 0.4901 | 0.0013 | 0.4914 |  |  |
| H1-E02 | USPS | 256 | 1.0000 | 0.0000 | 0.6748 | 0.0000 | 0.6748 |  |  |
| H1-E02 | har | 561 | 1.0000 | 0.0000 | 0.8904 | 0.0000 | 0.8904 |  |  |
| H1-E02 | COIL20 | 1024 | 1.0000 | 0.0000 | 0.7788 | 0.0000 | 0.7788 |  |  |
| H1-E02 | gisette | 5000 | 1.0000 | 0.0000 | 0.8628 | 0.0000 | 0.8628 |  |  |
| H1-E02 | Prostate_GE | 5966 | 1.0000 | 0.0000 | 0.6563 | 0.0000 | 0.6563 |  |  |
| H1-E02 | arcene | 10000 | 1.0000 | 0.0000 | 0.6358 | 0.0000 | 0.6358 |  |  |
| H5H6-E01 | PenDigits | 16 | 1.0000 | 1.0000 | 0.0000 | -7.14e-05 | -7.14e-05 | -7.14e-05 | -7.14e-05 |
| H5H6-E01 | ItalyPowerDemand | 24 | 1.0000 | 1.0000 | 0.0000 | 0.0044 | 0.0044 | 0.0044 | 0.000304 |
| H5H6-E01 | Crop | 46 | 1.0000 | 1.0000 | 0.0000 | 0.0037 | 0.0037 | 0.0037 | 0.0033 |
| H5H6-E01 | ProximalPhalanxOutlineCorrect | 80 | 1.0000 | 1.0000 | 0.0000 | -0.0089 | -0.0089 | -0.0089 | -0.0055 |
| H5H6-E01 | TwoLeadECG | 82 | 1.0000 | 1.0000 | 0.6229 | -0.000321 | 0.6226 | -0.0091 |  |
| H5H6-E01 | Libras | 90 | 1.0000 | 1.0000 | 0.0000 | -0.0011 | -0.0011 | -0.0011 | -0.0014 |
| H5H6-E01 | ElectricDevices | 96 | 1.0000 | 1.0000 | 0.1342 | 0.0044 | 0.1386 | 0.0050 | 0.0048 |
| H5H6-E01 | MedicalImages | 99 | 1.0000 | 1.0000 | 0.0000 | -0.0086 | -0.0086 | -0.0086 | -0.0022 |
| H5H6-E01 | ECG5000 | 140 | 1.0000 | 0.8000 | 0.4739 | 0.0065 | 0.4803 | 0.0022 | 0.0044 |
| H5H6-E01 | Wafer | 152 | 1.0000 | 0.0000 | 0.9887 | 0.0000 | 0.9887 |  |  |
| H5H6-E01 | ChlorineConcentration | 166 | 1.0000 | 0.0000 | 0.8095 | 0.0000 | 0.8095 |  |  |
| H5H6-E01 | Adiac | 176 | 1.0000 | 0.8000 | 0.1468 | 0.0017 | 0.1485 | 0.0044 | 0.0024 |
| H5H6-E01 | eodata | 182 | 1.0000 | 0.0000 | 0.4996 | 0.0000 | 0.4996 |  |  |
| H5H6-E01 | LSST | 216 | 1.0000 | 0.0000 | 0.3054 | 0.0000 | 0.3054 |  |  |
| H5H6-E01 | Strawberry | 235 | 1.0000 | 0.0000 | 0.8942 | 0.0000 | 0.8942 |  |  |
| H5H6-E01 | Ham | 431 | 1.0000 | 0.0000 | 0.6687 | 0.0000 | 0.6687 |  |  |
| H5H6-E01 | FordA | 500 | 1.0000 | 0.0000 | 0.5252 | 0.0000 | 0.5252 |  |  |
| H5H6-E01 | Earthquakes | 512 | 1.0000 | 0.0000 | 0.6758 | 0.0000 | 0.6758 |  |  |
| H5H6-E01 | OliveOil | 570 | 1.0000 | 0.0000 | 0.6649 | 0.0000 | 0.6649 |  |  |
| H5H6-E01 | BasicMotions | 600 | 1.0000 | 0.0000 | 0.6510 | 0.0000 | 0.6510 |  |  |
| H5H6-E01 | Epilepsy | 618 | 1.0000 | 0.0000 | 0.5771 | 0.0000 | 0.5771 |  |  |
| H5H6-E01 | Computers | 720 | 1.0000 | 0.0000 | 0.5425 | 0.0000 | 0.5425 |  |  |
| H5H6-E01 | UWaveGestureLibraryAll | 945 | 1.0000 | 0.0000 | 0.6641 | 0.0000 | 0.6641 |  |  |
| H5H6-E01 | StarLightCurves | 1024 | 1.0000 | 0.0000 | 0.8919 | 0.0000 | 0.8919 |  |  |
| H5H6-E01 | NATOPS | 1224 | 1.0000 | 0.0000 | 0.6604 | 0.0000 | 0.6604 |  |  |
| H5H6-E01 | FingerMovements | 1400 | 1.0000 | 0.0000 | 0.4998 | 0.0000 | 0.4998 |  |  |
| H5H6-E01 | CinCECGTorso | 1639 | 1.0000 | 0.0000 | 0.8630 | 0.0000 | 0.8630 |  |  |
| H5H6-E01 | HandOutlines | 2709 | 1.0000 | 0.0000 | 0.7990 | 0.0000 | 0.7990 |  |  |
| H5H6-E01 | EthanolConcentration | 5253 | 1.0000 | 0.0000 | 0.3701 | 0.0000 | 0.3701 |  |  |
| H5H6-E01 | SelfRegulationSCP1 | 5376 | 1.0000 | 0.0000 | 0.7932 | 0.0000 | 0.7932 |  |  |
| H5H6-E02 | PenDigits | 16 | 1.0000 | 1.0000 | 0.0000 | -0.000633 | -0.000633 | -0.000633 | -0.000633 |
| H5H6-E02 | ItalyPowerDemand | 24 | 1.0000 | 1.0000 | 0.0000 | -0.0014 | -0.0014 | -0.0014 | -0.000304 |
| H5H6-E02 | Crop | 46 | 1.0000 | 1.0000 | 0.0000 | 0.000411 | 0.000411 | 0.000411 | 0.000411 |
| H5H6-E02 | ProximalPhalanxOutlineCorrect | 80 | 1.0000 | 1.0000 | 0.0000 | 0.000838 | 0.000838 | 0.000838 | -0.000687 |
| H5H6-E02 | TwoLeadECG | 82 | 1.0000 | 1.0000 | 0.4327 | 0.0157 | 0.4484 | 0.0218 | 0.0388 |
| H5H6-E02 | Libras | 90 | 1.0000 | 1.0000 | 0.0000 | 0.0111 | 0.0111 | 0.0111 | 0.0048 |
| H5H6-E02 | ElectricDevices | 96 | 1.0000 | 1.0000 | 0.3691 | 0.0023 | 0.3715 | 0.0076 | 0.0076 |
| H5H6-E02 | MedicalImages | 99 | 1.0000 | 1.0000 | 0.0000 | 0.0073 | 0.0073 | 0.0073 | 0.0068 |
| H5H6-E02 | ECG5000 | 140 | 1.0000 | 0.8000 | 0.4901 | -3.46e-05 | 0.4901 | 0.0014 | 0.0027 |
| H5H6-E02 | Wafer | 152 | 1.0000 | 0.0000 | 0.9892 | 0.0000 | 0.9892 |  |  |
| H5H6-E02 | ChlorineConcentration | 166 | 1.0000 | 0.0000 | 0.8631 | 0.0000 | 0.8631 |  |  |
| H5H6-E02 | Adiac | 176 | 1.0000 | 0.8000 | 0.1548 | 0.0251 | 0.1798 | 0.0281 | 0.0359 |
| H5H6-E02 | eodata | 182 | 1.0000 | 0.0000 | 0.5848 | 0.0000 | 0.5848 |  |  |
| H5H6-E02 | LSST | 216 | 1.0000 | 0.0000 | 0.3649 | 0.0000 | 0.3649 |  |  |
| H5H6-E02 | Strawberry | 235 | 1.0000 | 0.8000 | 0.2111 | -0.0059 | 0.2053 | -0.0092 | -0.0042 |
| H5H6-E02 | Coffee | 286 | 1.0000 | 1.0000 | 0.0000 | -0.1380 | -0.1380 | -0.1380 | -0.1543 |
| H5H6-E02 | Ham | 431 | 1.0000 | 0.0000 | 0.7147 | 0.0000 | 0.7147 |  |  |
| H5H6-E02 | FordA | 500 | 1.0000 | 0.0000 | 0.5815 | 0.0000 | 0.5815 |  |  |
| H5H6-E02 | BeetleFly | 512 | 1.0000 | 1.0000 | 0.0000 | -0.1057 | -0.1057 | -0.1057 | -0.0806 |
| H5H6-E02 | Earthquakes | 512 | 1.0000 | 0.0000 | 0.6837 | 0.0000 | 0.6837 |  |  |
| H5H6-E02 | OliveOil | 570 | 1.0000 | 0.0000 | 0.6920 | 0.0000 | 0.6920 |  |  |
| H5H6-E02 | BasicMotions | 600 | 1.0000 | 0.0000 | 0.6509 | 0.0000 | 0.6509 |  |  |
| H5H6-E02 | Epilepsy | 618 | 1.0000 | 0.0000 | 0.6359 | 0.0000 | 0.6359 |  |  |
| H5H6-E02 | Computers | 720 | 1.0000 | 0.0000 | 0.5593 | 0.0000 | 0.5593 |  |  |
| H5H6-E02 | UWaveGestureLibraryAll | 945 | 1.0000 | 0.0000 | 0.7445 | 0.0000 | 0.7445 |  |  |
| H5H6-E02 | StarLightCurves | 1024 | 1.0000 | 0.0000 | 0.9178 | 0.0000 | 0.9178 |  |  |
| H5H6-E02 | NATOPS | 1224 | 1.0000 | 0.0000 | 0.6979 | 0.0000 | 0.6979 |  |  |
| H5H6-E02 | FingerMovements | 1400 | 1.0000 | 0.0000 | 0.4863 | 0.0000 | 0.4863 |  |  |
| H5H6-E02 | CinCECGTorso | 1639 | 1.0000 | 0.0000 | 0.8853 | 0.0000 | 0.8853 |  |  |
| H5H6-E02 | HandOutlines | 2709 | 1.0000 | 0.0000 | 0.8573 | 0.0000 | 0.8573 |  |  |
| H5H6-E02 | EthanolConcentration | 5253 | 1.0000 | 0.0000 | 0.4142 | 0.0000 | 0.4142 |  |  |
| H5H6-E02 | SelfRegulationSCP1 | 5376 | 1.0000 | 0.0000 | 0.8160 | 0.0000 | 0.8160 |  |  |
| H5H6-E02 | Heartbeat | 24705 | 1.0000 | 0.0000 | 0.6544 | 0.0000 | 0.6544 |  |  |
| H5H6-E02 | PEMS-SF | 138672 | 1.0000 | 0.0000 | 0.9585 | 0.0000 | 0.9585 |  |  |
| H5H6-E03 | PenDigits | 16 | 1.0000 | 1.0000 | 0.0000 | 5.3e-05 | 5.3e-05 | 5.3e-05 | 5.3e-05 |
| H5H6-E03 | ItalyPowerDemand | 24 | 1.0000 | 1.0000 | 0.0000 | 0.0052 | 0.0052 | 0.0052 | 0.0021 |
| H5H6-E03 | Crop | 46 | 1.0000 | 1.0000 | 0.0049 | -1.19e-05 | 0.0049 | -3.41e-05 | -3.41e-05 |
| H5H6-E03 | ProximalPhalanxOutlineCorrect | 80 | 1.0000 | 1.0000 | 0.0000 | -0.0023 | -0.0023 | -0.0023 | -0.0036 |
| H5H6-E03 | TwoLeadECG | 82 | 1.0000 | 1.0000 | 0.4449 | 0.0079 | 0.4527 | 0.0042 |  |
| H5H6-E03 | Libras | 90 | 1.0000 | 1.0000 | 0.0000 | -0.0066 | -0.0066 | -0.0066 | -0.0059 |
| H5H6-E03 | ElectricDevices | 96 | 1.0000 | 1.0000 | 0.2743 | 0.0032 | 0.2776 | 0.0069 | 0.0069 |
| H5H6-E03 | MedicalImages | 99 | 1.0000 | 1.0000 | 0.0000 | -0.0014 | -0.0014 | -0.0014 | 0.0026 |
| H5H6-E03 | ECG5000 | 140 | 1.0000 | 0.8000 | 0.4532 | 0.000302 | 0.4535 | 0.000515 | 0.0021 |
| H5H6-E03 | Wafer | 152 | 1.0000 | 0.0000 | 0.9888 | 0.0000 | 0.9888 |  |  |
| H5H6-E03 | ChlorineConcentration | 166 | 1.0000 | 0.0000 | 0.8714 | 0.0000 | 0.8714 |  |  |
| H5H6-E03 | Adiac | 176 | 1.0000 | 0.8000 | 0.2462 | 0.0197 | 0.2659 | 0.0356 | 0.0355 |
| H5H6-E03 | eodata | 182 | 1.0000 | 0.0000 | 0.5662 | 0.0000 | 0.5662 |  |  |
| H5H6-E03 | LSST | 216 | 1.0000 | 0.0000 | 0.3641 | 0.0000 | 0.3641 |  |  |
| H5H6-E03 | Strawberry | 235 | 1.0000 | 1.0000 | 0.0000 | -0.0048 | -0.0048 | -0.0048 | 0.0053 |
| H5H6-E03 | Coffee | 286 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | -1.11e-16 | 0.0000 | 0.0000 |
| H5H6-E03 | Ham | 431 | 1.0000 | 0.2000 | 0.5274 | 0.0106 | 0.5380 |  |  |
| H5H6-E03 | FordA | 500 | 1.0000 | 0.0000 | 0.5834 | 0.0000 | 0.5834 |  |  |
| H5H6-E03 | BeetleFly | 512 | 1.0000 | 1.0000 | 0.0000 | -0.0287 | -0.0287 | -0.0287 | 0.0170 |
| H5H6-E03 | Earthquakes | 512 | 1.0000 | 0.0000 | 0.7119 | 0.0000 | 0.7119 |  |  |
| H5H6-E03 | OliveOil | 570 | 1.0000 | 0.0000 | 0.6695 | 0.0000 | 0.6695 |  |  |
| H5H6-E03 | BasicMotions | 600 | 1.0000 | 0.0000 | 0.6543 | 0.0000 | 0.6543 |  |  |
| H5H6-E03 | Epilepsy | 618 | 1.0000 | 0.0000 | 0.6361 | 0.0000 | 0.6361 |  |  |
| H5H6-E03 | Computers | 720 | 1.0000 | 0.0000 | 0.6197 | 0.0000 | 0.6197 |  |  |
| H5H6-E03 | StarLightCurves | 1024 | 1.0000 | 0.0000 | 0.9233 | 0.0000 | 0.9233 |  |  |
| H5H6-E03 | NATOPS | 1224 | 1.0000 | 0.0000 | 0.6890 | 0.0000 | 0.6890 |  |  |
| H5H6-E03 | FingerMovements | 1400 | 1.0000 | 0.0000 | 0.4933 | 0.0000 | 0.4933 |  |  |
| H5H6-E03 | CinCECGTorso | 1639 | 1.0000 | 0.0000 | 0.8953 | 0.0000 | 0.8953 |  |  |

**Q2, reach model** (`tables/q2_reach_model.csv`; per-dataset reach in `q2_reach_by_dataset.csv`):

| grid | method | n_runs | n_datasets | reach_rate | b_log2d | b_log2d_lo | b_log2d_hi | b_log2budget | b_log2budget_lo | b_log2budget_hi | d50_at_median_budget | note |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H1-E02 | nsga2 | 40 | 8 | 0.150 | -16.508949832389316 | -19.652315902207317 | -4.241880313283328 | 20.15901282425834 | 5.016813201042707 | 24.038804200624487 | 171.70827124453595 |  |
| H1-E02 | nsga2_sparse | 40 | 8 | 1.000 |  |  |  |  |  |  |  | all runs alike; no fit |
| H5H6-E01 | nsga2 | 164 | 33 | 0.299 | -5.171079934325738 | -38.206988970284186 | -3.2553404952779026 | 2.359955508019632 | 1.5820331171871909 | 29.18772063973964 | 162.96772051127627 |  |
| H5H6-E01 | nsga2_sparse | 165 | 33 | 1.000 |  |  |  |  |  |  |  | all runs alike; no fit |
| H5H6-E01 | nsgaii_miip | 149 | 30 | 0.369 | -5.22548410710141 | -120.27593780340652 | -3.4945351601957 | 4.003602537524095 | 2.5307930107268155 | 94.21989940250434 | 208.0651261179273 |  |
| H5H6-E02 | nsga2 | 170 | 34 | 0.365 | -3.118669594062156 | -36.09514678356256 | -2.210197953723466 | 2.484929386568107 | 1.4555222699270502 | 31.64230378311644 | 212.2427289080276 |  |
| H5H6-E02 | nsga2_sparse | 195 | 39 | 1.000 |  |  |  |  |  |  |  | all runs alike; no fit |
| H5H6-E02 | nsgaii_miip | 160 | 32 | 0.463 | -5.313304947140881 | -653.3291081041672 | -3.6135079601839455 | 4.26372556447487 | 2.9091296327978595 | 568.0116657201733 | 268.3399263628072 |  |
| H5H6-E03 | nsga2 | 134 | 28 | 0.478 | -3.150239876483982 | -34.70866236206338 | -2.205490868881541 | 2.5875033409113515 | 1.2678047042316678 | 29.67716597651653 | 225.94199297030127 |  |
| H5H6-E03 | nsga2_sparse | 194 | 39 | 1.000 |  |  |  |  |  |  |  | all runs alike; no fit |
| H5H6-E03 | nsgaii_miip | 133 | 28 | 0.564 | -6.475889546563225 | -120.53241073368235 | -3.537328622412333 | 5.807596099590681 | 2.935930875110836 | 119.57242406584976 | 265.7575670377779 |  |

**Q7, time to reach** (`tables/q7_time_to_reach.csv`; per-dataset RMST tests in `q7_rmst.csv`):

| grid | method | n_runs | reached | reached_by_10pct | reached_by_25pct | reached_by_50pct | reached_by_100pct | median_share | median_seconds_reached | lost_reach |
|---|---|---|---|---|---|---|---|---|---|---|
| H1-E02 | nsga2 | 40 | 6 | 0.125 | 0.125 | 0.125 | 0.150 |  | 6.793 | 0 |
| H1-E02 | nsga2_sparse | 40 | 40 | 1.000 | 1.000 | 1.000 | 1.000 | 0.017 | 2.821 | 0 |
| H5H6-E01 | nsga2 | 164 | 49 | 0.067 | 0.171 | 0.201 | 0.299 |  | 26.558 | 0 |
| H5H6-E01 | nsga2_sparse | 165 | 165 | 1.000 | 1.000 | 1.000 | 1.000 | 0.017 | 1.170 | 0 |
| H5H6-E01 | nsgaii_miip | 149 | 55 | 0.101 | 0.201 | 0.275 | 0.369 |  | 27.851 | 0 |
| H5H6-E02 | nsga2 | 170 | 62 | 0.065 | 0.165 | 0.212 | 0.365 |  | 587.974 | 0 |
| H5H6-E02 | nsga2_sparse | 195 | 195 | 1.000 | 1.000 | 1.000 | 1.000 | 0.017 | 17.656 | 0 |
| H5H6-E02 | nsgaii_miip | 160 | 74 | 0.088 | 0.187 | 0.300 | 0.462 |  | 669.159 | 0 |
| H5H6-E03 | nsga2 | 134 | 64 | 0.090 | 0.216 | 0.269 | 0.478 |  | 354.928 | 0 |
| H5H6-E03 | nsga2_sparse | 194 | 194 | 1.000 | 1.000 | 1.000 | 1.000 | 0.017 | 8.657 | 0 |
| H5H6-E03 | nsgaii_miip | 133 | 75 | 0.098 | 0.226 | 0.346 | 0.564 | 0.770 | 340.060 | 0 |

**Q8, stagnation** (`tables/q8_stagnation.csv`; per dataset in `q8_by_dataset.csv`):

| grid | method | n_runs | stagnation | median_fits_share_at_stop | R_stopped | R_budget | median_repeat_share |
|---|---|---|---|---|---|---|---|
| H1-E02 | nsga2 | 40 | 0 |  |  | 0.150 | 0.098 |
| H1-E02 | nsga2_sparse | 40 | 0 |  |  | 1.000 | 0.992 |
| H5H6-E01 | nsga2 | 164 | 0 |  |  | 0.299 | 0.111 |
| H5H6-E01 | nsga2_sparse | 165 | 0 |  |  | 1.000 | 0.993 |
| H5H6-E01 | nsgaii_miip | 149 | 0 |  |  | 0.369 |  |
| H5H6-E02 | nsga2 | 170 | 10 | 0.751 | 1.000 | 0.325 | 0.184 |
| H5H6-E02 | nsga2_sparse | 195 | 72 | 0.088 | 1.000 | 1.000 | 0.966 |
| H5H6-E02 | nsgaii_miip | 160 | 11 | 0.502 | 1.000 | 0.423 |  |
| H5H6-E03 | nsga2 | 134 | 9 | 0.590 | 1.000 | 0.440 | 0.137 |
| H5H6-E03 | nsga2_sparse | 194 | 63 | 0.079 | 1.000 | 1.000 | 0.963 |
| H5H6-E03 | nsgaii_miip | 133 | 10 | 0.586 | 1.000 | 0.528 |  |

Q3 (three arms), Q4 (large-subset end), Q5 (sensitivity S0-S3) and Q6 (classifier) are in
`tables/q3_pairs.csv`, `q4_large_end.csv`, `q5_sensitivity.csv` and `q6_classifier.csv`.

Figures: F1 criterion, F2 reach against d, F3 three arms, F4 large-subset end, F5 missing-run
sensitivity, F6 time to reach, F7 repeats and stagnation, F8 classifier.

## 6. Reproduction

From a clean checkout at the commit that adds this report (the distilled logs are committed):

```
python -m pytest -q tests/test_h13_coverage.py
python experiments/h13_report.py        # -> experiments/reports/H13-E01/{tables,figures}
```
