# H1-E01 -- report

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H1-E01` |
| Hypothesis ID | H1 |
| Run IDs | `20261007T115349Z_h1e01_eodata_nsga2_s2020`<br>`20261007T115350Z_h1e01_eodata_nsga2_s2021`<br>`20261007T115352Z_h1e01_eodata_nsga2_s2022`<br>`20261007T115354Z_h1e01_eodata_nsga2_s2023`<br>`20261007T115356Z_h1e01_eodata_nsga2_s2024`<br>`20261007T115358Z_h1e01_eodata_nsga2_sparse_s2020`<br>`20261007T115359Z_h1e01_eodata_nsga2_sparse_s2021`<br>`20261007T115401Z_h1e01_eodata_nsga2_sparse_s2022`<br>`20261007T115403Z_h1e01_eodata_nsga2_sparse_s2023`<br>`20261007T115404Z_h1e01_eodata_nsga2_sparse_s2024`<br>all stopped, none finished, NOT evidence |
| Algorithm IDs | none recorded: a run registers its arms' IDs when it finishes, and these were stopped first; each manifest says `failed` (`KeyboardInterrupt`) |
| Pre-registration | `experiments/HYPOTHESES.md` at `3e1ce0c`, which still named the four development sets (see section 3) |
| Code commits | `3e1ce0c` |
| Dates | runs 2026-10-07 11:53:49 to about 12:06 UTC; report 2026-10-07 |
| Verdict | **failed**: stopped before any run finished; no verdict on H1 |

## 2. Hypothesis

H1 as registered in
[`HYPOTHESES.md`](../../HYPOTHESES.md#h1----nsga-iis-weakness-at-small-k-is-an-initialisation-artifact):
NSGA-II trails at small feature counts because of where it starts, not because
the search is worse.

## 3. What was attempted

`nsga2` against `nsga2_sparse` on eight datasets chosen by feature count --
satimage, eodata, USPS, har, COIL20, gisette, Prostate_GE and arcene -- with 5
seeds each: 80 runs, started by `run_queue.py` as one `run_sota.py --seed`
process each, ten at a time, EOData first.

The choice of the eight had been made by the PI and committed in `3e1ce0c`
with the code, but not yet written into H1's *Datasets* line and criterion,
which still read "the four development sets". The experiment was therefore
started against a registration that did not describe it.

## 4. What happened

The ten EOData runs started at 11:53-11:54 UTC. The PI stopped all of them at
about 12:06, to restart with a monitor that shows every job at once. At the
stop, each `nsga2` run had finished its first generation (100 fits, about 665
s each, ten processes sharing the machine) and the `nsga2_sparse` runs had
987-1,493 fits of 6,000. No run reached its end, so none wrote results or a
front. On the stop, each wrote its manifest with status `failed` and error
`KeyboardInterrupt`, ended 12:06:17-12:06:22 UTC. No score was read.

The run directories are kept under `results/`, as the methodology requires.
Their manifests are committed; their `progress.json` and trajectories are not
(`.gitignore`).

## 5. What changed before the next attempt

* H1's *Datasets* and criterion in `HYPOTHESES.md` name the eight datasets,
  with a dated revision entry (2026-10-07) that records this experiment.
* `make_report.py` reads H1 on the eight (`H1_SETS`); it had read H1 on the
  four development sets only, so it would have ignored six of the eight.
* `run_queue.py` writes `results/<ID>/queue.json`, and
  `monitor.py --experiment <ID>` shows every job of a queued experiment in one
  view.
* `experiment_ids.py` no longer drops text added above the ledger table when it
  rewrites the ledger. Issuing `H1-E01` had removed the pointer to
  `DATASETS_USED.md`; it is restored.

`H1-E02` restarts the same design from the commit that makes these changes.

## 6. Limitations

None for H1: this experiment produced no result. The one number it did produce
-- seconds per fit with ten processes running -- is a timing observation, not
evidence.
