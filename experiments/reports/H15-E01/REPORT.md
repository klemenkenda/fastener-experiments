# H15-E01 -- report

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H15-E01` |
| Hypothesis ID | H15 |
| Run IDs | none: every job was refused before it created a run |
| Algorithm IDs | none recorded |
| Pre-registration | `experiments/HYPOTHESES.md` at `9b9ac09` (H15), design in `EXPERIMENTS.md` at the same commit; issued at `240a4e6` |
| Code commits | `240a4e6` |
| Dates | queue 2026-11-03 14:53:32 to about 14:54:30 local time; report 2026-11-03 |
| Verdict | **failed**: no run started; no verdict on H15 |

## 2. Hypothesis

H15 as registered in [`HYPOTHESES.md`](../../HYPOTHESES.md): the fits the
OBL start needs before its archive holds a subset of at most 10 features
follow exp(-0.9607 + 1.8765 ln d), fitted on H14-E02.

## 3. What was attempted

`p2_obl_reach` on gas_drift, crop_mapping, volkert, madelon, Isolet, gina
and ORL with seeds 2030-2034: 35 jobs on Sentinel, started by
`run_queue.py` ten at a time, gina and ORL first.

## 4. What happened

Every job's `run_sota.py` loaded its dataset and then refused to run,
because the working tree held an untracked file outside the code,
`openrouter-usage.ps1` (a PI's helper script in the repository root, never
committed): "refusing to run H15-E01 from uncommitted code". The queue
logged 20 refusals in about 20 seconds and was stopped by Claude about a
minute after it started. No run folder was created, no search started and
no score exists.

## 5. What changed before the next attempt

* `openrouter-usage.ps1` is excluded locally (`.git/info/exclude`), so the
  dirty-tree check no longer sees it; nothing tracked changed.
* `H15-E02` reruns the same design unchanged
  ([DEC-60](../../DECISIONS.md#dec-60)).
