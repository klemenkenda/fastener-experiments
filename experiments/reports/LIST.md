# Completed experiments

One experiment per hypothesis: the one to consider. Duration is wall clock from
the first run's start to the last run's end. Every experiment ever started is
in the ledger, [`EXPERIMENTS.md`](../EXPERIMENTS.md).

| hypothesis | experiment | duration | result | report |
|---|---|---|---|---|
| H0 | `H0-E03` | 8 h 22 min | not confirmed | [REPORT.md](H0-E03/REPORT.md) |
| H1 | `H1-E02` | 14 h 47 min | confirmed | [REPORT.md](H1-E02/REPORT.md) |

## Why some hypotheses have more than one experiment

**H0 -- three experiments; consider `H0-E03`.** `H0-E01` tested five datasets,
and they split: the fixed code was faster on two, the 2020 code on one. Five
datasets could not say which pattern was general, so `H0-E02` repeated the test
on all 31 other datasets, with datasets as the unit. It was confirmed narrowly.
The fixed FASTENER was then changed to keep the top genes (DEC-23), so the code
both had tested no longer existed. `H0-E03` asked the same question of the
current code, on all 36 datasets. It is the result that applies to the
FASTENER used in every later experiment. The two earlier verdicts stand, but
only for the code they tested.

**H1 -- two experiments; consider `H1-E02`.** `H1-E01` was stopped after 13
minutes, before any run finished, so that it could be restarted with
monitoring of all jobs. Its dataset change had not yet been written into the
registration either. `H1-E02` ran the same design to the end.

## Superseded and failed experiments

| hypothesis | experiment | duration | status | result | replaced by | report |
|---|---|---|---|---|---|---|
| H0 | `H0-E01` | 1 h 42 min | superseded | not confirmed | `H0-E03` | [REPORT.md](H0-E01/REPORT.md) |
| H0 | `H0-E02` | 7 h 40 min | superseded | confirmed, narrowly | `H0-E03` | [REPORT.md](H0-E02/REPORT.md) |
| H1 | `H1-E01` | 13 min | failed: stopped before any run finished | -- | `H1-E02` | [REPORT.md](H1-E01/REPORT.md) |
