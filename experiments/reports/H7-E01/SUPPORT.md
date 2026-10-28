# H7-E01 -- support

The record behind [REPORT.md](REPORT.md).

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H7-E01` |
| Hypothesis ID | H7 |
| Runs | 117, one per grid and dataset (section 4) |
| Code commits | experiments `e71bce8`, FASTENER `3be5697`; every run clean and verified (`evidence: true`) |
| Pre-registration | `experiments/HYPOTHESES.md`, H7, at `516ac8c`; design in `EXPERIMENTS.md` at `811a2f4` |
| Dates | runs 2026-10-28T15:52:03.420565+00:00 to 2026-10-28T18:03:19.514704+00:00; report 2026-10-28 |
| Sources | the runs of H5H6-E01 (decision tree), H5H6-E02 (random forest) and H5H6-E03 (LightGBM) |
| Verdict | **not supported**: no classifier meets all four comparisons; under the tree two of four hold (FASTENER over sparse NSGA-II at 10% and 25%), under the forest and LightGBM none |

## 2. Hypothesis and criterion, as registered

> ## H7 -- FASTENER reaches good small subsets in fewer fits than its co-leaders
>
> *(planned 2026-10-28; an analysis of the H5H6-E01, -E02 and -E03 runs, no new
> search runs)*
>
> **Claim.** Part-way through the budget, stock FASTENER offers better small
> subsets than sparse NSGA-II and POSS, the searches it ties with at the end of
> the budget (H5H6-E01 to -E03).
>
> **Why it might hold.** At equal fits FASTENER was ahead of FS-SDS on 18 of 25
> datasets (H4-E03): it uses each fit well. Its mating is guided by mutual
> information from the first generation; sparse NSGA-II and POSS start from
> random subsets and learn which features matter only from their fits. The
> end-of-budget grids cannot see this: by then all three have converged to the
> same flat top.
>
> **Why it might not.** POSS adds or removes one feature at a time from the
> empty set and so is strong at small k early; sparse NSGA-II starts at 1-30
> features, inside the k range. FASTENER starts from five single features and
> spends early fits on pruning.
>
> **Data.** The trajectories of the three grids, on disk: every snapshot stores
> the front, with each entry's features, against cumulative fits. No intermediate
> test score has been read or computed before this registration; the
> end-of-budget scores have been.
>
> **Procedure.** For each run of `fastener`, `nsga2_sparse` and `poss` and each
> checkpoint c in {10%, 25%} of the dataset's fit budget: take the last snapshot
> with at most c fits (a run that stopped earlier, on stagnation, contributes its
> final front); for each k = 1..10 the entry of size <= k with the best
> validation F1; refit it with the experiment's classifier on the training split
> and score it once on test; AUF (K = 10) as everywhere else. Per dataset, an
> arm's score is its mean over the 5 seeds.
>
> **Falsification criterion.** For each classifier separately, four
> comparisons -- FASTENER against each of the two rivals at each of the two
> checkpoints -- each with datasets as the unit: more datasets where FASTENER is
> ahead than behind, and a two-sided Wilcoxon signed-rank test significant after
> Holm correction over the four, at alpha = 0.05. H7 is **supported** if all
> four hold under at least two of the three classifiers; **reversed** if a rival
> meets the same condition against FASTENER; otherwise **not supported**. Only
> datasets where both arms have a result count (sparse NSGA-II has none on six
> datasets under the tree).
>
> **Reported beside it:** the same at 50% and 100% of the budget (100% is the
> end-of-budget grid, as a check of the procedure); the per-cluster picture;
> FS-SDS and the swap arms at the same checkpoints; wall clock to each
> checkpoint, since equal fits are not equal time (H1-E02).
>
> **Confirmed on new data** in H9.
>
> **Experiments.** Designs, runs and reports in [`EXPERIMENTS.md`](EXPERIMENTS.md).
>
> * `H7-E01` -- the analysis above on H5H6-E01 to -E03. Registered.

## 3. Procedure and parameters

| parameter | value |
|---|---|
| script | `experiments/h7_checkpoints.py` (refits), `experiments/h7_report.py` (criterion, tables, figures) |
| runs read | every finished run in the grids' `tables/run_keys.csv` of `fastener`, `nsga2_sparse`, `poss` (the criterion) and `fastener_swap_guided`, `fastener_swap_random` (beside it): 2,892 runs |
| checkpoints | 10%, 25% (criterion), 50%, 100% (beside it) of each run's fit budget (`evaluation_budget_per_seed` in its manifest) |
| front at a checkpoint | the last front the run's trajectory stored at or below that many fits; a run that ended earlier contributes its final front |
| scoring | each front entry of at most 10 features refitted with the grid's classifier (`protocol.set_model`, LightGBM's leaf from the training split) on the training split, scored on validation and once on test by `protocol.evaluate_subset`; AUF (K = 10) by `make_report.opt_curve` |
| data | `datasets.load(name, max_rows=protocol.ROW_CAP)`, the grids' split; each run checks its train/validation/test sizes against the source runs' manifests |
| cost | 45,024 refits (subsets refitted once per grid and dataset and shared across its checkpoints and runs), 11.3 process-hours on 12 processes of the workstation |
| tests | per classifier, datasets as the unit (mean over seeds), two-sided Wilcoxon (`make_report.wilcoxon_p`), Holm over the four comparisons of each direction |

**Deviations from the registration.** FS-SDS, which HYPOTHESES.md reports beside H7, is left out (stated in the design before the runs): it runs k = 1..20 one after another, so a share of its total fits has seen only the first k's. Otherwise none.

**Reproduction at 100%.** At the full budget the procedure must give each run's end-of-budget AUF. It does for 2,679 of the 2,892 runs exactly; the other 213 (175 POSS, 37 sparse NSGA-II, 1 guided-swap FASTENER) have the same validation curve over k = 1..10 as the final records, checked run by run, and differ only in which of several subsets with equal validation score is kept -- the trajectory keeps the first found, the final records a later one. On those runs the trajectory reading gives +0.004 AUF on average (0.035 in absolute value), so it does not favour FASTENER.

## 4. What happened

**Timeline (UTC, 28 Oct).** The runs kept span 15:52 to 18:03.

1. **Dry run (before registration).** Checkpoint 100% only, no experiment ID, four datasets (Coffee, Adiac, FordA, Heartbeat), 289 runs: 274 matched the grids' end-of-budget AUF and 15 were ties as above. No intermediate checkpoint was computed. The experiment was then registered (`811a2f4`).
2. **First attempt (15:07), stopped by provenance.** After 17 of 117 tasks, the analysis script `h7_report.py` was saved into the working tree; the tree was then uncommitted, and every further task refused to start as evidence. The 27 folders started are kept, unread, in `results/H7-E01/attempt1_stopped/`. `h7_report.py` was committed (`e4664ef`) and the run restarted.
3. **Second attempt (15:09), stopped by hand.** The loader in `h7_checkpoints.py` omitted the protocol's 50,000-row cap that `run_sota.py` applies, so EOData -- the only dataset over the cap -- was loaded at 480,000 rows: a different split from the grids', and a tree task that ran 30 minutes instead of one. It was stopped after 96 of 117 tasks; its 117 folders are kept, unread, in `results/H7-E01/attempt2_stopped/`. The loader now applies the cap and every task checks its split sizes against the source runs (`e71bce8`); a dry run at 100% on EOData, Crop and Coffee then reproduced all 25 EOData runs exactly.
4. **Third attempt (15:52-18:03).** All 117 tasks, one commit, every manifest `status: ok` and `evidence: true`; the runs were added to the ledger at the end. No intermediate score was read from either stopped attempt.

## 5. Evidence

Every comparison computed, the registered ones (10%, 25%) with their Holm p. Full table: [tables/criterion.csv](tables/criterion.csv); per dataset: [tables/per_dataset.csv](tables/per_dataset.csv); timings: [tables/seconds.csv](tables/seconds.csv).

| classifier | checkpoint | arm | opponent | datasets | W-T-L | mean diff | median diff | p | Holm p | holds |
|---|---|---|---|---|---|---|---|---|---|---|
| decision tree | 10% | fastener | nsga2_sparse | 33 | 27-0-6 | +0.0132 | +0.0049 | 0.000372 | 0.00149 | True |
| decision tree | 25% | fastener | nsga2_sparse | 33 | 24-0-9 | +0.0071 | +0.0030 | 0.00984 | 0.0295 | True |
| decision tree | 50% | fastener | nsga2_sparse | 33 | 19-0-14 | +0.0039 | +0.0012 | 0.257 | -- | -- |
| decision tree | 100% | fastener | nsga2_sparse | 33 | 17-0-16 | -0.0014 | +0.0004 | 0.304 | -- | -- |
| decision tree | 10% | fastener | poss | 39 | 23-0-16 | +0.0087 | +0.0013 | 0.15 | 0.3 | False |
| decision tree | 25% | fastener | poss | 39 | 21-0-18 | +0.0109 | +0.0002 | 0.185 | 0.3 | False |
| decision tree | 50% | fastener | poss | 39 | 25-0-14 | +0.0092 | +0.0018 | 0.127 | -- | -- |
| decision tree | 100% | fastener | poss | 39 | 23-0-16 | +0.0050 | +0.0015 | 0.427 | -- | -- |
| decision tree | 10% | nsga2_sparse | fastener | 33 | 6-0-27 | -0.0132 | -0.0049 | 0.000372 | 0.00149 | False |
| decision tree | 25% | nsga2_sparse | fastener | 33 | 9-0-24 | -0.0071 | -0.0030 | 0.00984 | 0.0295 | False |
| decision tree | 50% | nsga2_sparse | fastener | 33 | 14-0-19 | -0.0039 | -0.0012 | 0.257 | -- | -- |
| decision tree | 100% | nsga2_sparse | fastener | 33 | 16-0-17 | +0.0014 | -0.0004 | 0.304 | -- | -- |
| decision tree | 10% | poss | fastener | 39 | 16-0-23 | -0.0087 | -0.0013 | 0.15 | 0.3 | False |
| decision tree | 25% | poss | fastener | 39 | 18-0-21 | -0.0109 | -0.0002 | 0.185 | 0.3 | False |
| decision tree | 50% | poss | fastener | 39 | 14-0-25 | -0.0092 | -0.0018 | 0.127 | -- | -- |
| decision tree | 100% | poss | fastener | 39 | 16-0-23 | -0.0050 | -0.0015 | 0.427 | -- | -- |
| random forest | 10% | fastener | nsga2_sparse | 39 | 23-0-16 | +0.0100 | +0.0035 | 0.0704 | 0.211 | False |
| random forest | 25% | fastener | nsga2_sparse | 39 | 25-0-14 | +0.0014 | +0.0028 | 0.259 | 0.388 | False |
| random forest | 50% | fastener | nsga2_sparse | 39 | 20-0-19 | -0.0007 | +0.0002 | 0.972 | -- | -- |
| random forest | 100% | fastener | nsga2_sparse | 39 | 20-0-19 | -0.0020 | +0.0002 | 0.634 | -- | -- |
| random forest | 10% | fastener | poss | 39 | 24-0-15 | +0.0086 | +0.0019 | 0.194 | 0.388 | False |
| random forest | 25% | fastener | poss | 39 | 25-0-14 | +0.0106 | +0.0029 | 0.0347 | 0.139 | False |
| random forest | 50% | fastener | poss | 39 | 28-0-11 | +0.0092 | +0.0053 | 0.00684 | -- | -- |
| random forest | 100% | fastener | poss | 39 | 27-0-12 | +0.0062 | +0.0026 | 0.062 | -- | -- |
| random forest | 10% | nsga2_sparse | fastener | 39 | 16-0-23 | -0.0100 | -0.0035 | 0.0704 | 0.211 | False |
| random forest | 25% | nsga2_sparse | fastener | 39 | 14-0-25 | -0.0014 | -0.0028 | 0.259 | 0.388 | False |
| random forest | 50% | nsga2_sparse | fastener | 39 | 19-0-20 | +0.0007 | -0.0002 | 0.972 | -- | -- |
| random forest | 100% | nsga2_sparse | fastener | 39 | 19-0-20 | +0.0020 | -0.0002 | 0.634 | -- | -- |
| random forest | 10% | poss | fastener | 39 | 15-0-24 | -0.0086 | -0.0019 | 0.194 | 0.388 | False |
| random forest | 25% | poss | fastener | 39 | 14-0-25 | -0.0106 | -0.0029 | 0.0347 | 0.139 | False |
| random forest | 50% | poss | fastener | 39 | 11-0-28 | -0.0092 | -0.0053 | 0.00684 | -- | -- |
| random forest | 100% | poss | fastener | 39 | 12-0-27 | -0.0062 | -0.0026 | 0.062 | -- | -- |
| LightGBM | 10% | fastener | nsga2_sparse | 39 | 26-0-13 | +0.0068 | +0.0040 | 0.0774 | 0.232 | False |
| LightGBM | 25% | fastener | nsga2_sparse | 39 | 19-0-20 | +0.0015 | -0.0004 | 0.512 | 0.631 | False |
| LightGBM | 50% | fastener | nsga2_sparse | 39 | 14-0-25 | -0.0007 | -0.0019 | 0.176 | -- | -- |
| LightGBM | 100% | fastener | nsga2_sparse | 39 | 17-0-22 | +0.0006 | -0.0019 | 0.387 | -- | -- |
| LightGBM | 10% | fastener | poss | 39 | 27-0-12 | +0.0029 | +0.0013 | 0.0359 | 0.144 | False |
| LightGBM | 25% | fastener | poss | 39 | 25-0-14 | +0.0026 | +0.0013 | 0.315 | 0.631 | False |
| LightGBM | 50% | fastener | poss | 39 | 26-0-13 | +0.0014 | +0.0014 | 0.185 | -- | -- |
| LightGBM | 100% | fastener | poss | 39 | 20-0-19 | +0.0029 | +0.0002 | 0.557 | -- | -- |
| LightGBM | 10% | nsga2_sparse | fastener | 39 | 13-0-26 | -0.0068 | -0.0040 | 0.0774 | 0.232 | False |
| LightGBM | 25% | nsga2_sparse | fastener | 39 | 20-0-19 | -0.0015 | +0.0004 | 0.512 | 0.631 | False |
| LightGBM | 50% | nsga2_sparse | fastener | 39 | 25-0-14 | +0.0007 | +0.0019 | 0.176 | -- | -- |
| LightGBM | 100% | nsga2_sparse | fastener | 39 | 22-0-17 | -0.0006 | +0.0019 | 0.387 | -- | -- |
| LightGBM | 10% | poss | fastener | 39 | 12-0-27 | -0.0029 | -0.0013 | 0.0359 | 0.144 | False |
| LightGBM | 25% | poss | fastener | 39 | 14-0-25 | -0.0026 | -0.0013 | 0.315 | 0.631 | False |
| LightGBM | 50% | poss | fastener | 39 | 13-0-26 | -0.0014 | -0.0014 | 0.185 | -- | -- |
| LightGBM | 100% | poss | fastener | 39 | 19-0-20 | -0.0029 | -0.0002 | 0.557 | -- | -- |

Figures, in [figures/](figures/): `F1_H7_criterion.png`, `F2_auf_by_checkpoint.png`, `F3_by_cluster_10pct.png`, `F4_time_to_10pct.png`.

## 6. Runs

| run | grid | dataset | refits | elapsed (s) |
|---|---|---|---|---|
| `20261028T155203Z_h7e01_h5h6e01_Adiac` | H5H6-E01 | Adiac | 423 | 12 |
| `20261028T155203Z_h7e01_h5h6e01_BasicMotions` | H5H6-E01 | BasicMotions | 170 | 4 |
| `20261028T155203Z_h7e01_h5h6e01_BeetleFly` | H5H6-E01 | BeetleFly | 19 | 6 |
| `20261028T155203Z_h7e01_h5h6e01_ChlorineConcentration` | H5H6-E01 | ChlorineConcentration | 557 | 24 |
| `20261028T155203Z_h7e01_h5h6e01_CinCECGTorso` | H5H6-E01 | CinCECGTorso | 587 | 15 |
| `20261028T155203Z_h7e01_h5h6e01_Coffee` | H5H6-E01 | Coffee | 25 | 5 |
| `20261028T155203Z_h7e01_h5h6e01_Computers` | H5H6-E01 | Computers | 306 | 12 |
| `20261028T155203Z_h7e01_h5h6e01_Crop` | H5H6-E01 | Crop | 588 | 106 |
| `20261028T155203Z_h7e01_h5h6e01_ECG5000` | H5H6-E01 | ECG5000 | 395 | 18 |
| `20261028T155203Z_h7e01_h5h6e01_Earthquakes` | H5H6-E01 | Earthquakes | 360 | 13 |
| `20261028T155203Z_h7e01_h5h6e01_ElectricDevices` | H5H6-E01 | ElectricDevices | 598 | 94 |
| `20261028T155204Z_h7e01_h5h6e01_EigenWorms` | H5H6-E01 | EigenWorms | 307 | 7 |
| `20261028T155208Z_h7e01_h5h6e01_Epilepsy` | H5H6-E01 | Epilepsy | 417 | 11 |
| `20261028T155209Z_h7e01_h5h6e01_EthanolConcentration` | H5H6-E01 | EthanolConcentration | 309 | 33 |
| `20261028T155212Z_h7e01_h5h6e01_FaceDetection` | H5H6-E01 | FaceDetection | 367 | 53 |
| `20261028T155213Z_h7e01_h5h6e01_FaultDetectionA` | H5H6-E01 | FaultDetectionA | 524 | 47 |
| `20261028T155216Z_h7e01_h5h6e01_FingerMovements` | H5H6-E01 | FingerMovements | 281 | 10 |
| `20261028T155216Z_h7e01_h5h6e01_FordA` | H5H6-E01 | FordA | 418 | 21 |
| `20261028T155217Z_h7e01_h5h6e01_Ham` | H5H6-E01 | Ham | 255 | 13 |
| `20261028T155219Z_h7e01_h5h6e01_HandOutlines` | H5H6-E01 | HandOutlines | 397 | 23 |
| `20261028T155221Z_h7e01_h5h6e01_Heartbeat` | H5H6-E01 | Heartbeat | 270 | 7 |
| `20261028T155222Z_h7e01_h5h6e01_ItalyPowerDemand` | H5H6-E01 | ItalyPowerDemand | 65 | 3 |
| `20261028T155226Z_h7e01_h5h6e01_LSST` | H5H6-E01 | LSST | 515 | 29 |
| `20261028T155227Z_h7e01_h5h6e01_Libras` | H5H6-E01 | Libras | 386 | 9 |
| `20261028T155229Z_h7e01_h5h6e01_MedicalImages` | H5H6-E01 | MedicalImages | 239 | 9 |
| `20261028T155230Z_h7e01_h5h6e01_MotorImagery` | H5H6-E01 | MotorImagery | 185 | 5 |
| `20261028T155231Z_h7e01_h5h6e01_NATOPS` | H5H6-E01 | NATOPS | 485 | 13 |
| `20261028T155235Z_h7e01_h5h6e01_OliveOil` | H5H6-E01 | OliveOil | 86 | 4 |
| `20261028T155238Z_h7e01_h5h6e01_PEMS-SF` | H5H6-E01 | PEMS-SF | 227 | 4 |
| `20261028T155238Z_h7e01_h5h6e01_PenDigits` | H5H6-E01 | PenDigits | 275 | 12 |
| `20261028T155239Z_h7e01_h5h6e01_PhonemeSpectra` | H5H6-E01 | PhonemeSpectra | 417 | 39 |
| `20261028T155240Z_h7e01_h5h6e01_ProximalPhalanxOutlineCorrect` | H5H6-E01 | ProximalPhalanxOutlineCorrect | 300 | 10 |
| `20261028T155243Z_h7e01_h5h6e01_SelfRegulationSCP1` | H5H6-E01 | SelfRegulationSCP1 | 365 | 34 |
| `20261028T155243Z_h7e01_h5h6e01_StarLightCurves` | H5H6-E01 | StarLightCurves | 605 | 31 |
| `20261028T155243Z_h7e01_h5h6e01_Strawberry` | H5H6-E01 | Strawberry | 347 | 9 |
| `20261028T155244Z_h7e01_h5h6e01_TwoLeadECG` | H5H6-E01 | TwoLeadECG | 311 | 7 |
| `20261028T155251Z_h7e01_h5h6e01_UWaveGestureLibraryAll` | H5H6-E01 | UWaveGestureLibraryAll | 654 | 26 |
| `20261028T155251Z_h7e01_h5h6e01_Wafer` | H5H6-E01 | Wafer | 224 | 8 |
| `20261028T155253Z_h7e01_h5h6e02_Adiac` | H5H6-E02 | Adiac | 491 | 191 |
| `20261028T155254Z_h7e01_h5h6e01_eodata` | H5H6-E01 | eodata | 643 | 293 |
| `20261028T155256Z_h7e01_h5h6e02_BasicMotions` | H5H6-E02 | BasicMotions | 164 | 38 |
| `20261028T155300Z_h7e01_h5h6e02_BeetleFly` | H5H6-E02 | BeetleFly | 26 | 9 |
| `20261028T155302Z_h7e01_h5h6e02_ChlorineConcentration` | H5H6-E02 | ChlorineConcentration | 614 | 520 |
| `20261028T155306Z_h7e01_h5h6e02_CinCECGTorso` | H5H6-E02 | CinCECGTorso | 544 | 187 |
| `20261028T155310Z_h7e01_h5h6e02_Coffee` | H5H6-E02 | Coffee | 22 | 9 |
| `20261028T155314Z_h7e01_h5h6e02_Computers` | H5H6-E02 | Computers | 323 | 89 |
| `20261028T155318Z_h7e01_h5h6e02_Crop` | H5H6-E02 | Crop | 585 | 2399 |
| `20261028T155318Z_h7e01_h5h6e02_ECG5000` | H5H6-E02 | ECG5000 | 463 | 350 |
| `20261028T155318Z_h7e01_h5h6e02_Earthquakes` | H5H6-E02 | Earthquakes | 303 | 80 |
| `20261028T155321Z_h7e01_h5h6e02_EigenWorms` | H5H6-E02 | EigenWorms | 314 | 79 |
| `20261028T155335Z_h7e01_h5h6e02_ElectricDevices` | H5H6-E02 | ElectricDevices | 672 | 2147 |
| `20261028T155338Z_h7e01_h5h6e02_Epilepsy` | H5H6-E02 | Epilepsy | 496 | 124 |
| `20261028T155350Z_h7e01_h5h6e02_EthanolConcentration` | H5H6-E02 | EthanolConcentration | 290 | 79 |
| `20261028T155441Z_h7e01_h5h6e02_FaceDetection` | H5H6-E02 | FaceDetection | 488 | 792 |
| `20261028T155442Z_h7e01_h5h6e02_FaultDetectionA` | H5H6-E02 | FaultDetectionA | 689 | 1404 |
| `20261028T155444Z_h7e01_h5h6e02_FingerMovements` | H5H6-E02 | FingerMovements | 253 | 66 |
| `20261028T155510Z_h7e01_h5h6e02_FordA` | H5H6-E02 | FordA | 630 | 599 |
| `20261028T155543Z_h7e01_h5h6e02_Ham` | H5H6-E02 | Ham | 276 | 66 |
| `20261028T155551Z_h7e01_h5h6e02_HandOutlines` | H5H6-E02 | HandOutlines | 331 | 109 |
| `20261028T155605Z_h7e01_h5h6e02_Heartbeat` | H5H6-E02 | Heartbeat | 313 | 78 |
| `20261028T155614Z_h7e01_h5h6e02_ItalyPowerDemand` | H5H6-E02 | ItalyPowerDemand | 47 | 13 |
| `20261028T155627Z_h7e01_h5h6e02_LSST` | H5H6-E02 | LSST | 640 | 812 |
| `20261028T155650Z_h7e01_h5h6e02_Libras` | H5H6-E02 | Libras | 457 | 121 |
| `20261028T155724Z_h7e01_h5h6e02_MedicalImages` | H5H6-E02 | MedicalImages | 302 | 111 |
| `20261028T155742Z_h7e01_h5h6e02_MotorImagery` | H5H6-E02 | MotorImagery | 235 | 59 |
| `20261028T155748Z_h7e01_h5h6e02_NATOPS` | H5H6-E02 | NATOPS | 479 | 123 |
| `20261028T155841Z_h7e01_h5h6e02_OliveOil` | H5H6-E02 | OliveOil | 78 | 18 |
| `20261028T155853Z_h7e01_h5h6e02_PEMS-SF` | H5H6-E02 | PEMS-SF | 287 | 71 |
| `20261028T155859Z_h7e01_h5h6e02_PenDigits` | H5H6-E02 | PenDigits | 306 | 291 |
| `20261028T155909Z_h7e01_h5h6e02_PhonemeSpectra` | H5H6-E02 | PhonemeSpectra | 558 | 1411 |
| `20261028T155916Z_h7e01_h5h6e02_ProximalPhalanxOutlineCorrect` | H5H6-E02 | ProximalPhalanxOutlineCorrect | 337 | 98 |
| `20261028T155952Z_h7e01_h5h6e02_SelfRegulationSCP1` | H5H6-E02 | SelfRegulationSCP1 | 273 | 70 |
| `20261028T160006Z_h7e01_h5h6e02_StarLightCurves` | H5H6-E02 | StarLightCurves | 665 | 705 |
| `20261028T160055Z_h7e01_h5h6e02_Strawberry` | H5H6-E02 | Strawberry | 311 | 85 |
| `20261028T160103Z_h7e01_h5h6e02_TwoLeadECG` | H5H6-E02 | TwoLeadECG | 377 | 108 |
| `20261028T160143Z_h7e01_h5h6e02_UWaveGestureLibraryAll` | H5H6-E02 | UWaveGestureLibraryAll | 636 | 488 |
| `20261028T160221Z_h7e01_h5h6e02_Wafer` | H5H6-E02 | Wafer | 210 | 121 |
| `20261028T160254Z_h7e01_h5h6e02_eodata` | H5H6-E02 | eodata | 709 | 6517 |
| `20261028T160351Z_h7e01_h5h6e03_Adiac` | H5H6-E03 | Adiac | 508 | 792 |
| `20261028T160423Z_h7e01_h5h6e03_BasicMotions` | H5H6-E03 | BasicMotions | 151 | 13 |
| `20261028T160437Z_h7e01_h5h6e03_BeetleFly` | H5H6-E03 | BeetleFly | 20 | 5 |
| `20261028T160443Z_h7e01_h5h6e03_ChlorineConcentration` | H5H6-E03 | ChlorineConcentration | 597 | 224 |
| `20261028T160510Z_h7e01_h5h6e03_CinCECGTorso` | H5H6-E03 | CinCECGTorso | 547 | 205 |
| `20261028T160754Z_h7e01_h5h6e03_Coffee` | H5H6-E03 | Coffee | 18 | 7 |
| `20261028T160802Z_h7e01_h5h6e03_Computers` | H5H6-E03 | Computers | 348 | 23 |
| `20261028T160825Z_h7e01_h5h6e03_Crop` | H5H6-E03 | Crop | 538 | 3036 |
| `20261028T160828Z_h7e01_h5h6e03_ECG5000` | H5H6-E03 | ECG5000 | 523 | 357 |
| `20261028T160836Z_h7e01_h5h6e03_Earthquakes` | H5H6-E03 | Earthquakes | 364 | 26 |
| `20261028T160904Z_h7e01_h5h6e03_EigenWorms` | H5H6-E03 | EigenWorms | 433 | 90 |
| `20261028T160952Z_h7e01_h5h6e03_ElectricDevices` | H5H6-E03 | ElectricDevices | 675 | 1082 |
| `20261028T161000Z_h7e01_h5h6e03_Epilepsy` | H5H6-E03 | Epilepsy | 543 | 69 |
| `20261028T161035Z_h7e01_h5h6e03_EthanolConcentration` | H5H6-E03 | EthanolConcentration | 327 | 45 |
| `20261028T161112Z_h7e01_h5h6e03_FaceDetection` | H5H6-E03 | FaceDetection | 495 | 84 |
| `20261028T161122Z_h7e01_h5h6e03_FaultDetectionA` | H5H6-E03 | FaultDetectionA | 675 | 384 |
| `20261028T161151Z_h7e01_h5h6e03_FingerMovements` | H5H6-E03 | FingerMovements | 224 | 13 |
| `20261028T161205Z_h7e01_h5h6e03_FordA` | H5H6-E03 | FordA | 626 | 90 |
| `20261028T161237Z_h7e01_h5h6e03_Ham` | H5H6-E03 | Ham | 305 | 18 |
| `20261028T161256Z_h7e01_h5h6e03_HandOutlines` | H5H6-E03 | HandOutlines | 391 | 43 |
| `20261028T161336Z_h7e01_h5h6e03_Heartbeat` | H5H6-E03 | Heartbeat | 359 | 20 |
| `20261028T161340Z_h7e01_h5h6e03_ItalyPowerDemand` | H5H6-E03 | ItalyPowerDemand | 96 | 9 |
| `20261028T161350Z_h7e01_h5h6e03_LSST` | H5H6-E03 | LSST | 637 | 1155 |
| `20261028T161357Z_h7e01_h5h6e03_Libras` | H5H6-E03 | Libras | 497 | 220 |
| `20261028T161425Z_h7e01_h5h6e03_MedicalImages` | H5H6-E03 | MedicalImages | 368 | 308 |
| `20261028T161704Z_h7e01_h5h6e03_MotorImagery` | H5H6-E03 | MotorImagery | 285 | 15 |
| `20261028T161720Z_h7e01_h5h6e03_NATOPS` | H5H6-E03 | NATOPS | 497 | 117 |
| `20261028T161738Z_h7e01_h5h6e03_OliveOil` | H5H6-E03 | OliveOil | 81 | 6 |
| `20261028T161745Z_h7e01_h5h6e03_PEMS-SF` | H5H6-E03 | PEMS-SF | 247 | 52 |
| `20261028T161747Z_h7e01_h5h6e03_PenDigits` | H5H6-E03 | PenDigits | 287 | 439 |
| `20261028T161808Z_h7e01_h5h6e03_PhonemeSpectra` | H5H6-E03 | PhonemeSpectra | 578 | 2910 |
| `20261028T161838Z_h7e01_h5h6e03_ProximalPhalanxOutlineCorrect` | H5H6-E03 | ProximalPhalanxOutlineCorrect | 388 | 31 |
| `20261028T161910Z_h7e01_h5h6e03_SelfRegulationSCP1` | H5H6-E03 | SelfRegulationSCP1 | 372 | 23 |
| `20261028T161918Z_h7e01_h5h6e03_StarLightCurves` | H5H6-E03 | StarLightCurves | 684 | 311 |
| `20261028T161935Z_h7e01_h5h6e03_Strawberry` | H5H6-E03 | Strawberry | 314 | 26 |
| `20261028T161935Z_h7e01_h5h6e03_TwoLeadECG` | H5H6-E03 | TwoLeadECG | 360 | 34 |
| `20261028T162001Z_h7e01_h5h6e03_UWaveGestureLibraryAll` | H5H6-E03 | UWaveGestureLibraryAll | 695 | 650 |
| `20261028T162009Z_h7e01_h5h6e03_Wafer` | H5H6-E03 | Wafer | 183 | 25 |
| `20261028T162037Z_h7e01_h5h6e03_eodata` | H5H6-E03 | eodata | 692 | 6162 |

## 7. Reproduction

From a clean checkout at the commits in the header, with the three grids' run folders under `results/`:

```
python experiments/h7_checkpoints.py --experiment H7-E01 --jobs 12
python experiments/h7_report.py --experiment H7-E01
```
