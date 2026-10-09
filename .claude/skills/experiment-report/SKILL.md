---
name: experiment-report
description: Write the report for a finished FASTENER experiment (H<n>-E<nn>) -- verify its runs, generate REPORT.md and SUPPORT.md with make_report.py, write REPORT.md in three sections (in brief, findings F1..FN, assessment) and SUPPORT.md's record, then close the experiment in the ledger and decision log. Use when the user says an experiment has finished, asks to generate, write or redo a report, or asks what an experiment found.
---

# Experiment report

An experiment's report is two files in `experiments/reports/<ID>/`:

- **`REPORT.md`** is the reading, for someone who has not followed the
  experiment. It is short and plain, and every finding comes with a figure.
- **`SUPPORT.md`** is the record: runs, criteria quoted as registered,
  parameters, per-seed numbers, what happened, how to reproduce it.

The rules behind both are in `experiments/METHODOLOGY.md`, *The report*. This
skill is the procedure. Interpreter: `C:\Users\klemen\.conda\envs\fastener-exp\python.exe`.

## 1. Check the experiment before reading any result

1. The queue finished: `python experiments/monitor.py --experiment <ID> --once`
   shows every job done, none failed.
2. The ledger row in `EXPERIMENTS.md` lists every run, and each run's
   `manifest.json` says `status: ok` and `evidence: true`.
3. All runs share one experiments commit with `code_dirty: false`. Every run
   spent exactly its fit budget (`protocol.fit_budget`).
4. Every algorithm ID can be explained. A second config hash for an arm must
   have a reason, such as arcene's 12,000-fit budget.

Anything that fails here goes into SUPPORT.md *What happened*. If it makes
the result unusable, the experiment is `invalid`; stop and tell the user.

## 2. Generate

```
python experiments/make_report.py --experiment <ID>
```

This writes `REPORT.md` (a skeleton), `SUPPORT.md`, `figures/F<n>_*.png` and
`tables/*.csv`. An existing REPORT.md or SUPPORT.md is never overwritten; the
new one goes to `*.skeleton.md`. `--force` overwrites, but only use it when
the existing file holds no prose that should be kept.

**Look at every figure** (Read the PNG) before writing a word. If a figure is
broken (overlapping text, empty panels, wrong axes), fix `make_report.py` and
regenerate. Do not caption a broken figure.

## 3. Find out what the data say

Compute what the findings need from the runs (`make_report.load_run`,
`units_of`, `auf`, `opt_curve`, the records' `n_features`, `val_score` and
`test_score`) in a scratch script. Typical questions:

- Does the criterion hold, and on which datasets? What is the one number that
  decides it?
- Why does the margin look as it does? For example, AUF counts a size a run
  never reached as zero, so a large margin can mean reach rather than quality.
- What does the diagnostic quantity the hypothesis names show (smallest
  subset, convergence, ...)?
- What surprised you: a reversal, a ceiling, a cost anomaly?

If a finding needs a figure the generator does not make, add the figure to
`make_report.py` (it has to come from a committed script), add it to the
candidate list, and regenerate.

## 4. Write REPORT.md: three sections

**1. In brief.** Plain language, with no project jargon unexplained.
- *The hypothesis*: what it says in two or three sentences, then
  **How it is judged**: the criterion, in plain words.
- *The answer: confirmed / not confirmed*, the reason in two to four
  sentences with the one deciding number, and the criterion figure with a
  one-line caption.

**2. Findings.** F1 to FN, one at a time. Each finding is:
- `### F<n> -- <one specific, falsifiable sentence>`,
- an explanation: what was measured, the numbers (ranges over seeds), and
  what they mean; a short table if it helps;
- the figure, with a caption that says what is plotted, the axes and the
  split.

F1 is the result on the pre-registered criterion. Delete candidate figures no
finding uses, and renumber the figures to match the findings. A claim with no
figure is not a finding.

**3. Assessment.** Write as for a paper's results and discussion. Cover what
is supported and how strongly, with effect sizes and their spread; what the
result does *not* show; the limits set by seeds, datasets, budget and split
sizes; and what follows for later hypotheses. Refer to findings by number,
and introduce no number the findings do not contain. Choices that belong to
the PI are named as such, not made.

## 5. Write SUPPORT.md's prose

It has only a few TODOs:
- each arm's plain-language description, including what each algorithm-ID
  hash means;
- deviations from the protocol, or "none", plus execution points such as
  parallel runs or the row cap;
- *What happened*: the timeline (first start, last end, total), failures and
  restarts, and anomalies, whether or not they mattered.

## 6. Check

- No `TODO` is left in either file.
- Every number in the prose matches a generated table, a figure or your
  scratch computation. Re-check ranges, counts ("34 of 35") and percentages.
- No claim goes beyond what the figure shows. The test split is read once,
  and nothing was chosen on it.
- Run `python -m pytest -q tests`.

## 7. Close the experiment

1. `experiment_ids.set_status("<ID>", "reported", report="[report](reports/<ID>/REPORT.md)")`
   (or `failed` / `invalid`).
2. `HYPOTHESES.md`: under the hypothesis's **Experiments** bullets, add the
   verdict to the experiment's bullet in one or two sentences.
3. `DECISIONS.md`: update the experiment's row in *By experiment* (status,
   verdict, report link). Add a DEC entry only for a decision actually taken.
4. Commit the report folder, the run records under `results/` (not
   trajectories, per DEC-22), `results/<ID>/` (queue.json, logs) and the
   ledger and doc changes. Commit as the user only (no Co-Authored-By line).

## 8. Tell the user

Give the verdict in one line, then the findings in a few lines, then anything
you fixed along the way. Point to `REPORT.md`. Do not paste the report.
