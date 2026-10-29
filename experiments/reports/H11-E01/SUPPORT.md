# H11-E01 -- supporting record

The record behind [REPORT.md](REPORT.md).

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H11-E01` |
| Hypothesis ID | H11 (post hoc, [DEC-48](../../DECISIONS.md#dec-48)) |
| Runs | none of its own; H10-E01 to -E03's 585 `fastener_seed_boruta` runs and 117 checkpoint runs (their ledger rows) |
| Comparison runs | H5H6-E01 to -E03's `fastener` and `boruta`; stock FASTENER's checkpoints from H7-E01 |
| Code commits | the H10 runs: experiments `9a04c0b` (E01), `d5907c6` (E02, E03); checkpoints `ef24f7c`; FASTENER `3be5697`. Tables made by `h10_report.py` at `241e5ed` |
| Dates | hypothesis and report 2026-10-29, after H10-E01 to -E03 were reported |
| Verdict | **not supported (post hoc)**: (c) fails under every classifier, (b) under LightGBM |

## 2. Hypothesis and criterion

As written in `experiments/HYPOTHESES.md`, H11, on 2026-10-29: H10's claim and
H10's registered criterion, unchanged, with `fastener_seed_boruta` as the
primary arm, read under each classifier, the verdict under LightGBM. Post hoc:
the claim was proposed after the H10 results had been read, so the criterion
is H10's to avoid choosing one after the fact.

## 3. Procedure

Nothing was recomputed. The numbers are the `fastener_seed_boruta` rows of
`experiments/reports/H10-E0{1,2,3}/tables/criterion.csv`, `beside.csv` and
`seed_costs.csv`, written by `h10_report.py` for the H10 reports, whose
SUPPORT files hold the runs, their checks and what happened.

**Deviations:** none from H10's criterion. The post-hoc status is the
difference from a registered experiment.

## 4. Evidence

| classifier | part | checkpoint | W-T-L | mean diff | p | Holm p | lower 95% | holds |
|---|---|---|---|---|---|---|---|---|
| LightGBM | (a) vs boruta | 100% | 31-0-8 | +0.0370 | 1.87e-05 | -- | -- | True |
| LightGBM | (b) vs fastener | 100% | 22-0-17 | +0.0025 | 0.154 | -- | -0.0079 | False |
| LightGBM | (c) vs fastener | 10% | 25-0-14 | +0.0041 | 0.185 | 0.241 | -- | False |
| LightGBM | (c) vs fastener | 25% | 25-0-14 | +0.0032 | 0.121 | 0.241 | -- | False |
| random forest | (a) vs boruta | 100% | 33-0-6 | +0.0524 | 2.57e-05 | -- | -- | True |
| random forest | (b) vs fastener | 100% | 24-0-15 | +0.0090 | 0.0661 | -- | +0.0023 | True |
| random forest | (c) vs fastener | 10% | 25-0-14 | +0.0079 | 0.108 | 0.108 | -- | False |
| random forest | (c) vs fastener | 25% | 26-0-13 | +0.0088 | 0.0149 | 0.0298 | -- | True |
| decision tree | (a) vs boruta | 100% | 23-0-16 | +0.0149 | 0.0197 | -- | -- | True |
| decision tree | (b) vs fastener | 100% | 21-0-18 | +0.0094 | 0.124 | -- | +0.0029 | True |
| decision tree | (c) vs fastener | 10% | 25-0-14 | +0.0005 | 0.395 | 0.790 | -- | False |
| decision tree | (c) vs fastener | 25% | 21-0-18 | +0.0026 | 0.624 | 0.790 | -- | False |

Beside the criterion: against the per-dataset better of Boruta and stock
FASTENER, 16-0-23 (-0.0079), 20-0-19 (-0.0009), 12-0-27 (-0.0036) under
LightGBM, the forest and the tree. Seed wall clock: 43.4 h of 143.6 h (30%),
3.3 h of 106.9 h (3%), 7.4 h of 19.1 h (39%); Boruta charged 8-99 fits per
run.

## 5. Reproduction

```
python experiments/h10_report.py --experiment H10-E01
python experiments/h10_report.py --experiment H10-E02
python experiments/h10_report.py --experiment H10-E03
```

and read the `fastener_seed_boruta` rows of each `tables/criterion.csv`.
