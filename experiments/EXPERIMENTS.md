# Experiment ledger

Every experiment ID ever issued, one row each, appended when the experiment
starts -- not when it succeeds. Rows are never deleted. See
[`METHODOLOGY.md`](METHODOLOGY.md) for what the IDs and statuses mean.

Managed by `experiments/experiment_ids.py`; edit the status with
`python experiments/experiment_ids.py status <ID> <status>`.

Candidate time series classification datasets for later experiments, grouped
by examples × features, are in [`DATASETS_USED.md`](DATASETS_USED.md).

| experiment | hypothesis | started | run IDs | status | report |
|---|---|---|---|---|---|
| `H0-E01` | H0 | 2026-09-25 | `20260925T173306Z_h0_TOX_171`, `20260925T173442Z_h0_TOX_171`, `20260925T173442Z_h0_har`, `20260925T173442Z_h0_BASEHOCK`, `20260925T173442Z_h0_USPS`, `20260925T173443Z_h0_crop_mapping` | reported | [report](reports/H0-E01/REPORT.md) |
| `H0-E02` | H0 | 2026-09-25 | `20260925T203019Z_h0_miniboone`, `20260925T203020Z_h0_higgs`, `20260925T203020Z_h0_volkert`, `20260925T203021Z_h0_covertype`, `20260925T203021Z_h0_gas_drift`, `20260925T203021Z_h0_arcene`, `20260925T203021Z_h0_orlraws10P`, `20260925T203021Z_h0_GLI_85`, `20260925T203021Z_h0_nci9`, `20260925T203021Z_h0_CLL_SUB_111`, `20260925T203021Z_h0_gina`, `20260925T203022Z_h0_gisette`, `20260925T203022Z_h0_eodata`, `20260925T205420Z_h0_Isolet`, `20260925T210101Z_h0_RELATHE`, `20260925T213746Z_h0_PCMAC`, `20260925T214349Z_h0_ORL`, `20260925T214424Z_h0_COIL20`, `20260925T214451Z_h0_ALLAML`, `20260925T215100Z_h0_leukemia`, `20260925T215315Z_h0_Prostate_GE`, `20260925T215738Z_h0_warpAR10P`, `20260925T220723Z_h0_Yale`, `20260925T221410Z_h0_warpPIE10P`, `20260925T221542Z_h0_GLIOMA`, `20260925T222250Z_h0_colon`, `20260925T222339Z_h0_lymphoma`, `20260925T223950Z_h0_lung`, `20260925T224012Z_h0_satimage`, `20260925T224015Z_h0_lung_discrete`, `20260925T203021Z_h0_madelon` | reported | [report](reports/H0-E02/REPORT.md) |
| `H0-E03` | H0 | 2026-09-30 | `20260930T083615Z_h0_miniboone`, `20260930T083615Z_h0_covertype`, `20260930T083615Z_h0_gas_drift`, `20260930T083615Z_h0_har`, `20260930T083615Z_h0_CLL_SUB_111`, `20260930T083615Z_h0_arcene`, `20260930T083616Z_h0_nci9`, `20260930T083616Z_h0_USPS`, `20260930T083616Z_h0_volkert`, `20260930T083615Z_h0_higgs`, `20260930T083616Z_h0_crop_mapping`, `20260930T083617Z_h0_eodata`, `20260930T103505Z_h0_TOX_171`, `20260930T103930Z_h0_BASEHOCK`, `20260930T104434Z_h0_gisette`, `20260930T104517Z_h0_RELATHE`, `20260930T110026Z_h0_PCMAC`, `20260930T110329Z_h0_ORL`, `20260930T110848Z_h0_GLI_85`, `20260930T111735Z_h0_warpAR10P`, `20260930T114641Z_h0_warpPIE10P`, `20260930T120136Z_h0_orlraws10P`, `20260930T120227Z_h0_lung_discrete`, `20260930T120345Z_h0_madelon`, `20260930T120355Z_h0_gina`, `20260930T120710Z_h0_Isolet`, `20260930T121011Z_h0_COIL20`, `20260930T121839Z_h0_ALLAML`, `20260930T122502Z_h0_leukemia`, `20260930T123152Z_h0_Prostate_GE`, `20260930T123307Z_h0_Yale`, `20260930T123946Z_h0_GLIOMA`, `20260930T124816Z_h0_colon`, `20260930T124845Z_h0_lymphoma`, `20260930T125343Z_h0_lung`, `20260930T130619Z_h0_satimage` | reported | [report](reports/H0-E03/REPORT.md) |
| `H1-E01` | H1 | 2026-10-07 | `20261007T115349Z_h1e01_eodata_nsga2_s2020`, `20261007T115350Z_h1e01_eodata_nsga2_s2021`, `20261007T115352Z_h1e01_eodata_nsga2_s2022`, `20261007T115354Z_h1e01_eodata_nsga2_s2023`, `20261007T115356Z_h1e01_eodata_nsga2_s2024`, `20261007T115358Z_h1e01_eodata_nsga2_sparse_s2020`, `20261007T115359Z_h1e01_eodata_nsga2_sparse_s2021`, `20261007T115401Z_h1e01_eodata_nsga2_sparse_s2022`, `20261007T115403Z_h1e01_eodata_nsga2_sparse_s2023`, `20261007T115404Z_h1e01_eodata_nsga2_sparse_s2024` | failed | [report](reports/H1-E01/REPORT.md) |
| `H1-E02` | H1 | 2026-10-07 | `20261007T121628Z_h1e02_eodata_nsga2_s2020`, `20261007T121630Z_h1e02_eodata_nsga2_s2021`, `20261007T121632Z_h1e02_eodata_nsga2_s2022`, `20261007T121634Z_h1e02_eodata_nsga2_s2023`, `20261007T121636Z_h1e02_eodata_nsga2_s2024`, `20261007T121638Z_h1e02_eodata_nsga2_sparse_s2020`, `20261007T121640Z_h1e02_eodata_nsga2_sparse_s2021`, `20261007T121641Z_h1e02_eodata_nsga2_sparse_s2022`, `20261007T121643Z_h1e02_eodata_nsga2_sparse_s2023`, `20261007T121644Z_h1e02_eodata_nsga2_sparse_s2024`, `20261007T130505Z_h1e02_gisette_nsga2_s2020`, `20261007T130600Z_h1e02_gisette_nsga2_s2021`, `20261007T130907Z_h1e02_gisette_nsga2_s2022`, `20261007T130948Z_h1e02_gisette_nsga2_s2023`, `20261007T131250Z_h1e02_gisette_nsga2_s2024`, `20261007T172834Z_h1e02_gisette_nsga2_sparse_s2020`, `20261007T173030Z_h1e02_gisette_nsga2_sparse_s2021`, `20261007T174511Z_h1e02_gisette_nsga2_sparse_s2022`, `20261007T180002Z_h1e02_gisette_nsga2_sparse_s2023`, `20261007T180138Z_h1e02_gisette_nsga2_sparse_s2024`, `20261007T180650Z_h1e02_har_nsga2_s2020`, `20261007T180828Z_h1e02_har_nsga2_s2021`, `20261007T181210Z_h1e02_har_nsga2_s2022`, `20261007T181642Z_h1e02_har_nsga2_s2023`, `20261007T182315Z_h1e02_har_nsga2_s2024`, `20261007T182452Z_h1e02_har_nsga2_sparse_s2020`, `20261007T183149Z_h1e02_har_nsga2_sparse_s2021`, `20261007T183331Z_h1e02_har_nsga2_sparse_s2022`, `20261007T183607Z_h1e02_har_nsga2_sparse_s2023`, `20261007T183924Z_h1e02_har_nsga2_sparse_s2024`, `20261007T183931Z_h1e02_USPS_nsga2_s2020`, `20261007T184248Z_h1e02_USPS_nsga2_s2021`, `20261007T184319Z_h1e02_USPS_nsga2_s2022`, `20261007T184506Z_h1e02_USPS_nsga2_s2023`, `20261007T184733Z_h1e02_USPS_nsga2_s2024`, `20261007T193819Z_h1e02_USPS_nsga2_sparse_s2020`, `20261007T194241Z_h1e02_USPS_nsga2_sparse_s2021`, `20261007T194327Z_h1e02_USPS_nsga2_sparse_s2022`, `20261007T194729Z_h1e02_USPS_nsga2_sparse_s2023`, `20261007T194945Z_h1e02_USPS_nsga2_sparse_s2024`, `20261007T195127Z_h1e02_COIL20_nsga2_s2020`, `20261007T195219Z_h1e02_COIL20_nsga2_s2021`, `20261007T195225Z_h1e02_COIL20_nsga2_s2022`, `20261007T195507Z_h1e02_COIL20_nsga2_s2023`, `20261007T195959Z_h1e02_COIL20_nsga2_s2024`, `20261007T202212Z_h1e02_COIL20_nsga2_sparse_s2020`, `20261007T202219Z_h1e02_COIL20_nsga2_sparse_s2021`, `20261007T202245Z_h1e02_COIL20_nsga2_sparse_s2022`, `20261007T202302Z_h1e02_COIL20_nsga2_sparse_s2023`, `20261007T202454Z_h1e02_COIL20_nsga2_sparse_s2024`, `20261007T202510Z_h1e02_arcene_nsga2_s2020`, `20261007T202812Z_h1e02_arcene_nsga2_s2021`, `20261007T202834Z_h1e02_arcene_nsga2_s2022`, `20261007T202855Z_h1e02_arcene_nsga2_s2023`, `20261007T203142Z_h1e02_arcene_nsga2_s2024`, `20261007T204159Z_h1e02_arcene_nsga2_sparse_s2020`, `20261007T204236Z_h1e02_arcene_nsga2_sparse_s2021`, `20261007T204946Z_h1e02_arcene_nsga2_sparse_s2022`, `20261007T205236Z_h1e02_arcene_nsga2_sparse_s2023`, `20261007T205257Z_h1e02_arcene_nsga2_sparse_s2024`, `20261007T205259Z_h1e02_satimage_nsga2_s2020`, `20261007T205516Z_h1e02_satimage_nsga2_s2021`, `20261007T205633Z_h1e02_satimage_nsga2_s2022`, `20261007T205700Z_h1e02_satimage_nsga2_s2023`, `20261007T205737Z_h1e02_satimage_nsga2_s2024`, `20261007T205854Z_h1e02_satimage_nsga2_sparse_s2020`, `20261007T205925Z_h1e02_satimage_nsga2_sparse_s2021`, `20261007T210005Z_h1e02_satimage_nsga2_sparse_s2022`, `20261007T210114Z_h1e02_satimage_nsga2_sparse_s2023`, `20261007T210135Z_h1e02_satimage_nsga2_sparse_s2024`, `20261007T210228Z_h1e02_Prostate_GE_nsga2_s2020`, `20261007T210330Z_h1e02_Prostate_GE_nsga2_s2021`, `20261007T210346Z_h1e02_Prostate_GE_nsga2_s2022`, `20261007T210508Z_h1e02_Prostate_GE_nsga2_s2023`, `20261007T210610Z_h1e02_Prostate_GE_nsga2_s2024`, `20261007T210627Z_h1e02_Prostate_GE_nsga2_sparse_s2020`, `20261007T210749Z_h1e02_Prostate_GE_nsga2_sparse_s2021`, `20261007T210830Z_h1e02_Prostate_GE_nsga2_sparse_s2022`, `20261007T210853Z_h1e02_Prostate_GE_nsga2_sparse_s2023`, `20261007T210946Z_h1e02_Prostate_GE_nsga2_sparse_s2024` | reported | [report](reports/H1-E02/REPORT.md) |
| `H2H3-E01` | H2, H3 | 2026-10-09 | -- | running | -- |

## Experiment designs

Each experiment's design, registered before its runs started. What every
experiment of a hypothesis shares -- the claim, the arms, the measure -- is in
[`HYPOTHESES.md`](HYPOTHESES.md); what one experiment adds or changes is here.
Moved here from `HYPOTHESES.md` on 2026-10-07, the text unchanged but for links; the
versions in force when each experiment ran are in `HYPOTHESES.md` at its
pre-registration commit, which its report names.

### `H0-E01` -- H0 on five datasets

The design is [H0](HYPOTHESES.md#h0----the-bug-fixed-fastener-converges-faster-than-the-2020-code) itself: five datasets (crop_mapping, USPS, har,
BASEHOCK, TOX_171), their budgets and splits, and the 4-of-5-seeds criterion
are all written there.

### `H0-E02` -- H0 on every other dataset

*Added 2026-09-25, after H0-E01 had finished and been reported. See*
[Revisions](HYPOTHESES.md#revisions).

**Why.** H0-E01 was not supported, and its five datasets split. The fixed code
reached the common target sooner in at least 4 of 5 seeds on TOX_171 (5 of 5)
and USPS (4 of 5); the 2020 code did on BASEHOCK (4 of 5); crop mapping and har
went neither way (2 against 3 each). Five datasets cannot say which pattern is
the general one. This experiment asks the same question on every other dataset
on disk.

**Which datasets: all 31 others.** Every dataset `datasets.load` knows except
H0-E01's five. Taking all of them, rather than choosing, is what keeps a choice
made after seeing results from steering the outcome.

| group | datasets | budget per run | split |
|---|---|---:|---|
| Earth observation | eodata | 1,000 fits | EO split, as crop mapping in H0 |
| Earth observation, small | satimage (6,430 rows) | 1,000 fits | protocol 60/20/20; too few rows for the EO split |
| other tall sets | covertype, miniboone, higgs, volkert, gas_drift | 6,000 fits | 50,000-row cap, 60/20/20 |
| challenge sets | madelon, gina | 6,000 fits | protocol 60/20/20 |
| paper benchmarks | the other 22 of the 25 | 6,000 fits | protocol 60/20/20 |

The budget rule is H0's: Earth-observation sets get the paper's EO budget of
1,000 fits, every other set gets 6,000. Arms, seeds, the fixed-target measure
and the target itself are exactly as in H0.

**Primary analysis: datasets as the unit.** With 31 datasets the per-dataset
4-of-5 rule is no longer the useful test; the question is whether the datasets
lean one way. Per dataset and seed, the effect is log2 of the ratio of the fits
each arm needed to reach the common target, 2020 over fixed. It is positive when
the fixed code was faster, zero on a tie. Per dataset, the effect is the mean
of its 5 seeds.

**Falsification criterion.** Supported if the per-dataset effects are
positive on more datasets than negative **and** a two-sided Wilcoxon
signed-rank test over the per-dataset effects is significant at alpha = 0.05.
Reversed -- the fixes slowed convergence -- if the same holds with the signs
swapped. Otherwise not supported: no consistent difference is detected over
these datasets. Datasets with a zero effect drop out of the test, as the
Wilcoxon test requires, and their count is reported.

**Incomplete datasets.** A dataset whose runs fail, or have fewer than 5 seeds
for both arms when the experiment is stopped, is left out of the test and
listed. If more than 6 of the 31 are left out, the result is reported as
incomplete rather than as a verdict.

**Reported beside it, as secondary:** H0's per-dataset 4-of-5 counts for every
dataset; the effect per dataset group from the table above; the same test over
all 36 datasets, H0-E01's five included, labelled as including datasets seen
before this experiment was registered; and final test AUF (K = 10) per arm.

**How it runs.** Several datasets at once, so the whole experiment fits in a
weekend. Runs then compete for the CPU, so wall clock is not comparable
between arms or datasets. Fits, which decide the result, are not affected.
Every tiny paper benchmark carries the caveat of *What the small sets can
support*: on the smallest, validation is 10-20 rows, and ties are common.

**Relation to H0-E01.** H0-E01's verdict stands on its own criterion and is
reported first. This experiment is separate evidence about the same claim.
Neither result is read as overriding the other; if they disagree, both are
reported with the disagreement stated.

### `H0-E03` -- H0 repeated with the top genes kept

Registered 2026-09-30, after H0-E01 and H0-E02 were reported and before any of
this experiment's runs started.

**Why.** After H0-E02 the fixed code was changed to keep the top genes
(`include_top_genes=True`, Revisions, 2026-09-30), and the protocol budget was
doubled on the 11 datasets whose search had not converged. H0-E01 and H0-E02
tested a fixed arm that no longer exists. This experiment asks H0's question of
the current code.

**Arms.** `fastener`, now `include_top_genes=True, allow_self_mating=False`:
it differs from the 2020 code only in drawing the mating pool without
replacement, so no item is mated with itself. `fastener_2020` is unchanged.
The claim tested is therefore narrower than H0-E02's: that removing
self-mating alone makes FASTENER converge faster.

**Datasets: all 36 of H0-E01 and H0-E02**, with their splits. Budgets: the three
Earth-observation sets that had 1,000 fits keep 1,000 (crop_mapping, eodata
and satimage); every other dataset gets `protocol.fit_budget`, which is 12,000
fits on the 11 in `protocol.LONG_BUDGET_DATASETS` and 6,000 on the rest.
Seeds, the fixed-target measure and the target are exactly as in H0.

**Primary analysis and falsification criterion.** As in H0-E02, over all 36
datasets: the per-dataset effect is the mean over 5 seeds of log2(fits the
2020 arm needed / fits the fixed arm needed). Supported if the effects are
positive on more datasets than negative **and** a two-sided Wilcoxon
signed-rank test over them is significant at alpha = 0.05; reversed if the same
holds with the signs swapped; otherwise not supported. Zero effects drop out of
the test and are counted.

**Incomplete datasets.** As in H0-E02. If more than 7 of the 36 are left out
(the same one in five), the result is reported as incomplete.

**Reported beside it, as secondary:** H0's per-dataset 4-of-5 counts; the
effect per dataset group; final test AUF (K = 10) per arm; and, labelled as
comparisons across experiments and not as tests, each dataset's effect here
beside its effect in H0-E01 or H0-E02. On the 11 long-budget datasets the
budget differs from the earlier experiments, so their effects are not
comparable one to one.

**How it runs.** As H0-E02: several datasets at once, so wall clock is not
comparable between arms; fits are unaffected.

**Relation to H0-E01 and H0-E02.** Their verdicts stand, about the code they
tested. This one is about the current code.

### `H1-E01` -- H1 on eight datasets

The design is [H1](HYPOTHESES.md#h1----nsga-iis-weakness-at-small-k-is-an-initialisation-artifact)
itself: `nsga2` against `nsga2_sparse` on the eight datasets listed there, 5
seeds, `protocol.fit_budget` fits per run, and the 4-of-5-seeds criterion on
EOData and at least one other dataset.

**How it ran.** `run_queue.py` at `3e1ce0c`, one `run_sota.py` process per
dataset, arm and seed, ten at a time. Stopped by the PI after 13 minutes, with
the ten EOData runs started and none finished, to restart with a monitor that
shows every job at once. Failed; see its report.

### `H1-E02` -- H1 on eight datasets, restarted

Registered 2026-10-07, after `H1-E01` was stopped and before any of this
experiment's runs started. No result of `H1-E01` was read.

**Design.** Exactly `H1-E01`'s: the arms, datasets, seeds, budgets and
criterion in [H1](HYPOTHESES.md#h1----nsga-iis-weakness-at-small-k-is-an-initialisation-artifact).

**How it runs.** `run_queue.py`, one `run_sota.py --seed` process per dataset,
arm and seed -- 80 jobs -- at most ten at a time, slowest datasets first. The
jobs compete for the CPU, so wall clock is not comparable between arms; fits,
which the criterion is stated in, are not affected. A seed run alone gives the
same front as the same seed inside a five-seed run (checked on madelon before
the run), so the split changes no result. Watched with
`monitor.py --experiment H1-E02`.

### `H2H3-E01` -- H2 and H3 on 39 datasets

Registered 2026-10-09, after DEC-33 and before any of this experiment's runs
started. No result of a swap arm from this round exists. The budget table
below is filled in from the calibration, and committed, before the first run;
nothing else in this design changes after it.

**Design.** [H2](HYPOTHESES.md#h2----a-size-preserving-move-changes-the-front-at-all-guided-or-not)
and [H3](HYPOTHESES.md#h3----the-guided-swap-improves-fastener-at-small-k) as
revised on 2026-10-09 ([DEC-33](DECISIONS.md#dec-33)), run together, as the
two hypotheses share their stock arm:

| | |
|---|---|
| arms | `fastener` (stock), `fastener_swap_random`, `fastener_swap_guided`, all on FASTENER clone `b7e724d` with the fixed mating |
| datasets | 39: EOData at the 50,000-row cap, and the UCR/UEA sets of [`DATASETS_USED.md`](DATASETS_USED.md) except DuckDuckGeese ([DEC-34](DECISIONS.md#dec-34)) |
| seeds | 2020, 2021, 2022, 2023, 2024 |
| budget | per dataset, the same for all three arms; see *Budgets* |
| primary metric | test AUF, K = 10 |
| H2 | per dataset, mean over seeds of AUF(`fastener_swap_random`) minus AUF(`fastener`); supported if positive on more datasets than negative and a two-sided Wilcoxon signed-rank test over them gives p < 0.05; reversed if the same with signs swapped |
| H3 | the same with `fastener_swap_guided`; the guidance is credited only if the guided arm also beats the random-swap arm by the same test (secondary) |
| incomplete | a dataset with fewer than 5 seeds for any arm it is read on is left out; more than 6 of 39 left out makes the reading incomplete |
| read by | `make_report.py` (`DATASET_UNIT`), H2 first, then H3 |

**Budgets.** Set by the rule in H2, *Fit budget*, from the calibration queue
`h2h3-calibration`: one Boruta run and one 12,000-fit stock FASTENER run per
dataset, seed 1999, validation scores only, started 2026-10-09 at `9fa04b7`
and read by `calibrate_budget.py`. Its run IDs are in
`results/h2h3-calibration/budgets.json`. Calibration runs are not runs of this
experiment and are not listed in its ledger row.

*Pending: the per-dataset table (dataset, Boruta validation AUF, FASTENER
validation AUF at 1k-12k fits, settled at, budget, flag), copied from
`budgets.csv` when the calibration has finished.*

**How it runs.** `run_queue.py --experiment H2H3-E01`, one `run_sota.py --seed`
process per dataset, arm and seed -- 585 jobs -- at most ten at a time,
slowest datasets first, each job given its own dataset's budget. The jobs
compete for the CPU, so wall clock is not comparable between arms; fits, which
the budget and the criterion are stated in, are not affected. Watched with
`monitor.py --experiment H2H3-E01`.

**Expected cost.** Estimated from the calibration's times per fit once it has
finished, and added here with the budgets.
