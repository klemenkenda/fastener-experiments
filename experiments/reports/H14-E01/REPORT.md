# H14-E01 -- report

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H14-E01` |
| Hypothesis ID | H14 (pilot for P2) |
| Run IDs | `20261102T171622Z_h14e01_Computers_p2_obl_b10_s2025` to `_s2029` and `20261102T171632Z_h14e01_Computers_p2_obl_b3_s2025` to `_s2029`: the ten listed in the ledger |
| Algorithm IDs | none recorded: a run writes its manifest and its arms' IDs when it finishes, and these were stopped first. They started from experiments commit `0634f55` (FASTENER `047e1fb`) |
| Pre-registration | `experiments/HYPOTHESES.md` at `1152a8e` (H14), design in `EXPERIMENTS.md` at the same commit |
| Code commits | `0634f55` |
| Dates | runs 2026-11-02 17:16:22 to about 17:22 UTC; report 2026-11-02 |
| Verdict | **failed**: stopped before any run finished; no verdict on H14 |

## 2. Hypothesis

H14 as registered in [`HYPOTHESES.md`](../../HYPOTHESES.md): a start over
all subset sizes keeps the 1-30 start's reach without its large-end cost; the
OBL start's lack of reach is not only budget; a forced flip cuts the 1-30
start's repeats.

## 3. What was attempted

The ten `p2_*` arms on Adiac, Strawberry, Earthquakes and Computers with
seeds 2025-2029: 200 runs on Sentinel, started by `run_queue.py` as one
`run_sota.py --seed` process each, ten at a time, the costliest first
(Computers, at 10x and 3x the fit budget).

## 4. What happened

The ten Computers runs at 10x and 3x started at 17:16:22-17:16:38 UTC. While
they ran, `h14_report.py` (the analysis script, imported by no run) was
committed as `c83a2de`, so the 190 jobs still waiting would have started
from a different commit than the ten running. At about 17:22 the PI stopped
the queue to make a change to the repository first (DEC-57, a post hoc rule
for H13's part (b)) and then rerun. The ten runs were killed at 5,197-6,357
fits of their 36,000 or 120,000; none finished, none wrote a manifest, and no
score of any of them was read. Their partial folders stay in `results/`.

## 5. What changed before the next attempt

* DEC-57 (`354c307`): H13 only; it changes nothing H14 runs or reads. All
  four H14 datasets have more than 50 test rows (93-196).
* `H14-E02` reruns the same design from one commit, so that every run shares
  it ([DEC-58](../../DECISIONS.md#dec-58)); no commit is made while it runs.
