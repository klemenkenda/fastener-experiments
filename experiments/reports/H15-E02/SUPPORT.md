# H15-E02 -- supporting record

The record behind [REPORT.md](REPORT.md).

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H15-E02` |
| Hypothesis ID | H15 (confirmatory, for P2) |
| Run IDs | the 35 in the ledger row (`h15e02_<dataset>_p2_obl_reach_s<seed>`), each with `status: ok`, `evidence: true` |
| Algorithm IDs | `p2_obl_reach@f47c368+047e1fb#<config>`; one config hash per dataset, because the config holds the dataset's fit cap (Isolet `6965`, ORL `7f21`, crop_mapping `3c4b`, gas_drift `d14b`, gina `0347`, madelon `39c8`, volkert `f736`) |
| Pre-registration | H15: `experiments/HYPOTHESES.md` at `9b9ac09`; H15-E01's design at `9b9ac09`, H15-E02's at `ce9e379` (DEC-60); `h15_report.py` and `h15_budgets.json` at `9b9ac09` |
| Code commits | every run at experiments `f47c368`, FASTENER `047e1fb`, `code_dirty: false` |
| Dates | runs 2026-11-03T14:55:20 to 2026-11-04T06:03:22 UTC (15 h 8 min); report 2026-11-04 |
| Verdict | **supported** on (i), (ii) and (iii); the slope's interval excludes the predicted exponent (`tables/verdict.json`) |

## 2. Hypothesis

Quoted verbatim from `experiments/HYPOTHESES.md` at `9b9ac09`:

> ## H15 -- The fits the OBL start needs to reach k <= 10 grow with d as H14 predicts
>
> *(2026-11-03; proposed by the PI for paper P2 after H14-E02 was reported.
> **Confirmatory**: the prediction is fitted on H14-E02 and tested on seven
> datasets on which no NSGA-II arm has run, with new seeds; see
> [DEC-59](DECISIONS.md#dec-59).)*
>
> **Claim.** In plain NSGA-II with the NSGAII-MIIP port's operators, started
> from OBL (every individual near d/2 features), the fits until the archive
> first holds a subset of at most 10 features follow the relation fitted on
> H14-E02, F(d) = exp(-0.9607 + 1.8765 ln d), about 0.38 d^1.88: faster than
> linearly in d.
>
> **Why it might hold.** H14-E02 (F2): at 10x the budget the OBL start
> reached k <= 10 in all 20 runs, after 6.1-8.5 thousand fits at d = 176
> and 74.5-87.1 thousand at d = 720. The four dataset medians lie within 14%
> of the fitted line, and the seeds within a dataset spread by a log SD of
> 0.24. Selection has to walk the population from d/2 to 10 features, and
> balanced mutation flips about one bit per child at k = d/2, so the walk
> lengthens with d.
>
> **Why it might not.** The fit is in-sample on four datasets, and its slope
> is poorly fixed: resampling the datasets puts it anywhere in [0.97, 2.27].
> All four are time-series datasets; the walk may depend on the data as well
> as on d, for example on how much validation F1 drops as features are
> removed, on the number of rows, or on the number of classes. On the
> datasets with at most 50 test rows the OBL start reached earlier than the
> line predicts (BeetleFly, d = 512: under the tree in 1 of 4 seeds by
> 12,000 fits, about a quarter of F(d); under the forest and LightGBM in 5 of
> 5; H13-E01), which is why H15 uses only datasets with more than 50 test
> rows (DEC-57's threshold). The row cap (50,000 rows) makes the two tall
> datasets' fits slow; whether it changes the walk is part of what is tested.
>
> **Arm.** `p2_obl_reach`: H14's `p2_obl` (population 100, balanced
> mutation at rate 1/d, separate random streams, every scored subset
> logged, the stagnation stop of DEC-41), stopped after the generation in
> which it first scores a subset of 1-10 features (`run_nsga2`'s
> `stop_at_size = 10`). A trajectory does not depend on the budget (H14-E02:
> in 20 of 20 pairs the 1x run was the start of the 10x run), so stopping
> there ends a run at the fits-to-reach a longer run would also record. The
> budget is a cap only: 4 F(d), rounded up to 1,000 (`h15_budgets.json`).
>
> **Datasets.** Seven on which no NSGA-II arm has run, with d from 128 to
> 1,024 and more than 50 test rows each, under the protocol split and the
> row cap:
>
> | dataset | d | rows used (train / val / test) | classes | F(d) | cap |
> |---|---:|---|---:|---:|---:|
> | gas_drift | 128 | 8,346 / 2,782 / 2,782 | 6 | 3,444 | 14,000 |
> | crop_mapping | 174 | 30,002 / 9,999 / 9,999 (capped) | 7 | 6,127 | 25,000 |
> | volkert | 180 | 30,002 / 9,998 / 9,998 (capped) | 10 | 6,530 | 27,000 |
> | madelon | 500 | 1,560 / 520 / 520 | 2 | 44,412 | 178,000 |
> | Isolet | 617 | 936 / 312 / 312 | 26 | 65,896 | 264,000 |
> | gina | 970 | 2,080 / 694 / 694 | 2 | 154,019 | 617,000 |
> | ORL | 1,024 | 240 / 80 / 80 | 40 | 170,501 | 683,000 |
>
> **Criterion.** Fits-to-reach is H13-E01's measure: the fits at the end of
> the generation in which the archive first held a subset of at most 10
> features. A run that does not reach (cap, stagnation stop, the 24-hour
> timeout, or a crash) is censored; in a median it counts as larger than
> every value reached. T is a dataset's median over its five seeds.
>
> * (i) Reach: on every dataset, at least 4 of 5 seeds reach before the cap.
> * (ii) Magnitude: |ln(T / F(d))| <= ln 2, i.e. within a factor 2 of the
>   prediction, on at least 5 of the 7 datasets.
> * (iii) Shape: the OLS slope of ln T on ln d over the datasets with a
>   finite T (at least 5 needed) has a bootstrap 95% interval (datasets
>   resampled, 10,000 times, seed 20200) whose lower end is above 1.
>
> Supported if (i), (ii) and (iii) hold; not supported otherwise, with each
> part reported. Mechanical reading by `h15_report.py`, committed before the
> runs.
>
> **Reported beside it:** the per-seed ratios to the prediction; the slope
> fitted on H15 alone and on H14 and H15 together; residuals against rows
> and classes; Kaplan-Meier curves of reach in multiples of F(d); the front
> at the stop; wall clock per fit beside fits; stop reasons.

## 3. Evaluation criteria and design

The criterion is in the hypothesis above. H15-E01's design, which H15-E02 repeats, and H15-E02's own entry, verbatim from `experiments/EXPERIMENTS.md` at `ce9e379`:

> ### `H15-E01` -- H15: the OBL start's fits-to-reach against d, on seven datasets no NSGA-II arm had run on
>
> Registered 2026-11-03, before any of this experiment's runs
> ([DEC-59](DECISIONS.md#dec-59)).
>
> **Design.** [H15](HYPOTHESES.md#h15----the-fits-the-obl-start-needs-to-reach-k--10-grow-with-d-as-h14-predicts)
> as written: one arm, `p2_obl_reach`; gas_drift, crop_mapping, volkert,
> madelon, Isolet, gina and ORL; the decision tree; seeds 2030-2034 (unused
> by any earlier experiment); the caps in `h15_budgets.json`; the
> stagnation stop; a 24-hour timeout per run; Sentinel with 10 processes;
> H15's criterion, read by `h15_report.py`. 35 runs. Every run starts from
> the commit that issues this experiment; nothing is committed while the
> queue runs.
>
> **Already seen.** No NSGA-II result on any of the seven. Other methods'
> results on them: FASTENER in H0-E02 (gas_drift, volkert, madelon, gina,
> Isolet, ORL) and H0-E01 (crop_mapping), FASTENER and FS-SDS in H4 (Isolet,
> ORL), FASTENER's H8 arms (gas_drift, crop_mapping), the LLM probes of H12
> (crop_mapping). Their manifests carry `run_sota.py`'s NSGA-II parameters,
> but no NSGA-II arm ran. None of it bears on how fast the OBL start walks
> down. Before H1-E02 a run alone and inside a five-seed run were
> checked to give the same front on madelon (`EXPERIMENTS.md`, H1-E02); that
> check's numbers were not reported. The prediction and the caps come from
> H14-E02 alone. The H15 test job, `20261102T232217Z_h15test`, ran
> `p2_obl_reach` on Adiac with seed 2025, an H14 cell: it stopped on reach
> after 7,559 fits, exactly H14-E02's fits-to-reach for that cell, from the
> same start (`3cb57eddea746b97`).
>
> **How it runs.**
>
> ```
> python experiments/run_queue.py --experiment H15-E01     --datasets gina,ORL,crop_mapping,Isolet,volkert,madelon,gas_drift     --methods p2_obl_reach --seeds 2030,2031,2032,2033,2034     --budgets experiments/h15_budgets.json --max-procs 10 --timeout-hours 24
> ```
>
> **Expected cost.** From single fits timed at k = d/2 on Sentinel
> (0.2-0.3 s on madelon, Isolet, gina and ORL; 2.3-3.4 s on the two capped
> tall sets), the pre-reach mean of 0.55 times that measured on the test
> job, and H14-E02's slowdown of about 1.2x at 10 processes: if T equals the
> prediction, about 140 CPU-hours and 13-14 hours of wall clock, with gina
> (about 8 h a run) and ORL (about 7 h) the longest. If T is twice the
> prediction, about 28 hours. The 24-hour timeout binds before the cap only
> on gina, at about 2.9 F(d).

> ### `H15-E02` -- H15: rerun of H15-E01, which no run started
>
> Registered 2026-11-03, after H15-E01's jobs were refused and before any of
> this experiment's runs ([DEC-60](DECISIONS.md#dec-60)).
>
> **Design.** H15-E01's design, unchanged, with every run from the commit
> that issues this experiment and nothing committed while the queue runs.
>
> **Changed since H15-E01.** Nothing H15 runs or reads. An untracked helper
> script is excluded locally so that the dirty-tree check passes.
>
> **Already seen.** As H15-E01; H15-E01 itself produced nothing.
>
> **How it runs.**
>
> ```
> python experiments/run_queue.py --experiment H15-E02     --datasets gina,ORL,crop_mapping,Isolet,volkert,madelon,gas_drift     --methods p2_obl_reach --seeds 2030,2031,2032,2033,2034     --budgets experiments/h15_budgets.json --max-procs 10 --timeout-hours 24
> ```
>
> **Expected cost.** As H15-E01: about 140 CPU-hours and 13-14 hours of wall
> clock if the prediction holds, about 28 hours at twice the prediction.

## 4. Description of the experiment

**Setup.** As registered. The arm, in plain words: plain NSGA-II with the NSGAII-MIIP port's tournament, crossover and balanced mutation (rate 1/d), population 100, started from OBL (50 random bit strings and their complements), with separate random streams for the start and the operators and every scored subset logged; it stops after the generation in which it first scores a subset of 1-10 features (`stop_at_size = 10`), at its fit cap, on the stagnation stop (50 generations without a new subset) or at the 24-hour timeout, whichever comes first.

**Deviations from the protocol.** None in the runs. After the runs, `h15_report.py` was changed in presentation only: F1's legend names the experiment plotted (it said H15-E01), F2's y-axis and F3's x-axis limits were set so that no point sits on the frame. The criterion code is as committed in `9b9ac09`.

**What happened.**

* One queue on Sentinel, 10 processes, costliest first (gina, ORL, crop_mapping, Isolet, volkert, madelon, gas_drift): 14:55:20 UTC 2026-11-03 to 06:03:22 UTC 2026-11-04, 15 h 8 min, against the 13-14 h estimated at the prediction. 35 of 35 jobs finished (`ok`); none failed or timed out. 138 CPU-hours in all (sum of run times), against about 140 estimated.
* Every run at `f47c368` + FASTENER `047e1fb` with `code_dirty: false`.
* Every run stopped on reach (`stopped_on: reach`); none at the cap, on stagnation or at the timeout. The most any run used was 0.50 of its cap (Isolet, seed 2031). Every final front holds a subset of at most 10 features.
* Before this experiment: H15-E01, whose 35 jobs were all refused by the dirty-tree check (an untracked helper script; its report), and the unregistered test job `20261102T232217Z_h15test` (Adiac, seed 2025, an H14 cell, which reproduced H14-E02's 7,559 fits-to-reach). Neither is part of this evidence.

## 5. Evidence

**Per dataset** (`tables/per_dataset.csv`; predicted from H14-E02, ratio = median / predicted; seconds per fit up to reach, medians, 10 processes at a time):

| dataset | d | n_train | predicted | reached | median_fits_to_reach | ratio | min_fits | max_fits | seconds_per_fit_median | i_holds | ii_holds |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gas_drift | 128 | 8346 | 3443.769 | 5 | 5276.000 | 1.532 | 3251 | 6109 | 0.355 | True | True |
| crop_mapping | 174 | 30002 | 6127.052 | 5 | 9758.000 | 1.593 | 8389 | 11975 | 2.093 | True | True |
| volkert | 180 | 30002 | 6529.509 | 5 | 7986.000 | 1.223 | 7602 | 12213 | 1.407 | True | True |
| madelon | 500 | 1560 | 44411.984 | 5 | 54892.000 | 1.236 | 33916 | 75882 | 0.106 | True | True |
| Isolet | 617 | 936 | 65895.758 | 5 | 70482.000 | 1.070 | 63906 | 132956 | 0.128 | True | True |
| gina | 970 | 2080 | 154018.875 | 5 | 183226.000 | 1.190 | 153828 | 202233 | 0.151 | True | True |
| ORL | 1024 | 240 | 170500.551 | 5 | 162597.000 | 0.954 | 153897 | 214244 | 0.120 | True | True |

**Slope** (`tables/slope.csv`): | n_datasets | slope | intercept | lo | hi | n_boot |
|---|---|---|---|---|---|
| 7 | 1.7026 | 0.2887 | 1.6072 | 1.8190 | 10000 |

Mechanical reading: {"i": true, "datasets_i": 7, "ii": true, "datasets_ii": 7, "iii": true, "slope": 1.7025543481340235, "slope_lo": 1.6071697272709078, "slope_hi": 1.8190385862523422, "slope_datasets": 7, "prediction_slope": 1.8765480534645083, "supported": true, "n_runs": 35}

**Per run** (`tables/runs.csv`):

| dataset | seed | ttr_fits | fits | cap | seconds | stopped_on | front_reach | algorithm_id |
|---|---|---|---|---|---|---|---|---|
| gas_drift | 2030 | 3675 | 3675 | 14000 | 1431.6 | reach | True | p2_obl_reach@f47c368+047e1fb#d14b |
| gas_drift | 2031 | 6109 | 6109 | 14000 | 2183.9 | reach | True | p2_obl_reach@f47c368+047e1fb#d14b |
| gas_drift | 2032 | 5886 | 5886 | 14000 | 2077.5 | reach | True | p2_obl_reach@f47c368+047e1fb#d14b |
| gas_drift | 2033 | 5276 | 5276 | 14000 | 1709.9 | reach | True | p2_obl_reach@f47c368+047e1fb#d14b |
| gas_drift | 2034 | 3251 | 3251 | 14000 | 1183.3 | reach | True | p2_obl_reach@f47c368+047e1fb#d14b |
| crop_mapping | 2030 | 8502 | 8502 | 25000 | 19370.6 | reach | True | p2_obl_reach@f47c368+047e1fb#3c4b |
| crop_mapping | 2031 | 11975 | 11975 | 25000 | 25026.5 | reach | True | p2_obl_reach@f47c368+047e1fb#3c4b |
| crop_mapping | 2032 | 9758 | 9758 | 25000 | 20717.5 | reach | True | p2_obl_reach@f47c368+047e1fb#3c4b |
| crop_mapping | 2033 | 10260 | 10260 | 25000 | 20928.2 | reach | True | p2_obl_reach@f47c368+047e1fb#3c4b |
| crop_mapping | 2034 | 8389 | 8389 | 25000 | 17684.7 | reach | True | p2_obl_reach@f47c368+047e1fb#3c4b |
| volkert | 2030 | 8542 | 8542 | 27000 | 12115.6 | reach | True | p2_obl_reach@f47c368+047e1fb#f736 |
| volkert | 2031 | 7602 | 7602 | 27000 | 11788.0 | reach | True | p2_obl_reach@f47c368+047e1fb#f736 |
| volkert | 2032 | 7986 | 7986 | 27000 | 12184.8 | reach | True | p2_obl_reach@f47c368+047e1fb#f736 |
| volkert | 2033 | 12213 | 12213 | 27000 | 16164.8 | reach | True | p2_obl_reach@f47c368+047e1fb#f736 |
| volkert | 2034 | 7931 | 7931 | 27000 | 10459.4 | reach | True | p2_obl_reach@f47c368+047e1fb#f736 |
| madelon | 2030 | 70877 | 70877 | 178000 | 8017.4 | reach | True | p2_obl_reach@f47c368+047e1fb#39c8 |
| madelon | 2031 | 75882 | 75882 | 178000 | 8800.0 | reach | True | p2_obl_reach@f47c368+047e1fb#39c8 |
| madelon | 2032 | 39963 | 39963 | 178000 | 3952.9 | reach | True | p2_obl_reach@f47c368+047e1fb#39c8 |
| madelon | 2033 | 33916 | 33916 | 178000 | 3156.4 | reach | True | p2_obl_reach@f47c368+047e1fb#39c8 |
| madelon | 2034 | 54892 | 54892 | 178000 | 5805.8 | reach | True | p2_obl_reach@f47c368+047e1fb#39c8 |
| Isolet | 2030 | 69471 | 69471 | 264000 | 9045.2 | reach | True | p2_obl_reach@f47c368+047e1fb#6965 |
| Isolet | 2031 | 132956 | 132956 | 264000 | 16368.0 | reach | True | p2_obl_reach@f47c368+047e1fb#6965 |
| Isolet | 2032 | 63906 | 63906 | 264000 | 6529.5 | reach | True | p2_obl_reach@f47c368+047e1fb#6965 |
| Isolet | 2033 | 70482 | 70482 | 264000 | 9171.6 | reach | True | p2_obl_reach@f47c368+047e1fb#6965 |
| Isolet | 2034 | 98908 | 98908 | 264000 | 12622.4 | reach | True | p2_obl_reach@f47c368+047e1fb#6965 |
| gina | 2030 | 202233 | 202233 | 617000 | 28275.5 | reach | True | p2_obl_reach@f47c368+047e1fb#0347 |
| gina | 2031 | 161070 | 161070 | 617000 | 18283.5 | reach | True | p2_obl_reach@f47c368+047e1fb#0347 |
| gina | 2032 | 183226 | 183226 | 617000 | 30857.0 | reach | True | p2_obl_reach@f47c368+047e1fb#0347 |
| gina | 2033 | 192876 | 192876 | 617000 | 29109.1 | reach | True | p2_obl_reach@f47c368+047e1fb#0347 |
| gina | 2034 | 153828 | 153828 | 617000 | 28065.4 | reach | True | p2_obl_reach@f47c368+047e1fb#0347 |
| ORL | 2030 | 153897 | 153897 | 683000 | 16743.0 | reach | True | p2_obl_reach@f47c368+047e1fb#7f21 |
| ORL | 2031 | 162597 | 162597 | 683000 | 21232.2 | reach | True | p2_obl_reach@f47c368+047e1fb#7f21 |
| ORL | 2032 | 175936 | 175936 | 683000 | 24802.9 | reach | True | p2_obl_reach@f47c368+047e1fb#7f21 |
| ORL | 2033 | 159483 | 159483 | 683000 | 19201.8 | reach | True | p2_obl_reach@f47c368+047e1fb#7f21 |
| ORL | 2034 | 214244 | 214244 | 683000 | 23344.8 | reach | True | p2_obl_reach@f47c368+047e1fb#7f21 |

Beside the criterion (computed from these tables in the report's scratch analysis, not by `h15_report.py`): per-seed slope 1.74; H14-E02 and H15-E02 dataset medians pooled, slope 1.75 [1.63, 1.93] (11 datasets, the same bootstrap); Spearman correlation of the log ratio with d -0.89, with training rows +0.77, with classes -0.54 (7 datasets); within-dataset log SD of fits-to-reach 0.12-0.35.

Figures: F1 fits-to-reach against d, F2 ratio to the prediction, F3 Kaplan-Meier reach.

## 6. Reproduction

From a clean checkout at `f47c368` (runs) and the commit that adds this report (analysis):

```
python experiments/run_queue.py --experiment H15-E02 \
    --datasets gina,ORL,crop_mapping,Isolet,volkert,madelon,gas_drift \
    --methods p2_obl_reach --seeds 2030,2031,2032,2033,2034 \
    --budgets experiments/h15_budgets.json --max-procs 10 --timeout-hours 24
python experiments/distill_results.py
python experiments/h15_report.py        # -> experiments/reports/H15-E02/{tables,figures}
```
