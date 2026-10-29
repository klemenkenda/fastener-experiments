---
name: research-method
description: How FASTENER research is organised, from a research question or a hypothesis through a registered experiment to its report -- research questions (Q<n>) when there is no hypothesis yet, hypotheses (H<n>) with falsification criteria fixed before any result, experiment IDs that are never reused, run and algorithm IDs pinned to both repositories' git commits, no evidence from a dirty tree, the decision log (DEC-nn), the ledger, revisions and the two-file report. Use when the user wants to start a line of work, asks a new research question, proposes a hypothesis or experiment, wants to plan, register or design an experiment, changes the protocol or a decision, asks how the work is organised, or asks whether something may be counted as evidence.
---

# Research method

How a question becomes evidence in this project, and how every step stays
traceable. The detailed rules are in `experiments/METHODOLOGY.md` (IDs,
ledger, reports), `experiments/HYPOTHESES.md` (questions, hypotheses,
protocol, revisions) and `experiments/DECISIONS.md` (the decision log). This
skill is the procedure and the reasons for it. When writing a report, follow
the `experiment-report` skill. When reading job logs, follow `distill-logs`.

Interpreter: `C:\Users\klemen\.conda\envs\fastener-exp\python.exe`.

## The principle

Anything quoted later must trace back to four things: the question it was
meant to answer, what was written down before the data existed, the exact
code (commits) that produced it, and the decisions it ran under. If one of
the four is missing, the number is not evidence.

## 1. Start from a research question or from a hypothesis

There are two ways in. Pick the one the state of knowledge allows. Do not
invent a hypothesis to fill the slot.

| we have | write | it is judged by | what it can produce |
|---|---|---|---|
| a question and no expectation of the answer | a **research question** `Q<n>` | an analysis plan: what is measured and how it is summarised, fixed before the runs | descriptive findings and *candidate* hypotheses |
| an expectation that could turn out wrong | a **hypothesis** `H<n>` | a falsification criterion fixed before the runs | a verdict: confirmed, not confirmed, refuted (qualified if needed) |

**A research question** goes in `HYPOTHESES.md`, under its own
`## Q<n> -- <the question>` section. It has:

- **Question.** One sentence, specific enough that a figure could answer it
  ("How does the best validation F1 at k <= 10 grow with fits on tall
  datasets?", not "How does FASTENER behave?").
- **Why we ask.** What is unknown, and what would change depending on the
  answer.
- **What will be measured.** Metrics, splits, datasets, arms, budget, and how
  results are summarised (per-seed points, ranges, curves against cumulative
  fits). The protocol table applies unless the section says otherwise.
- **What it cannot answer.** Its limits, stated in advance (seeds, datasets,
  budget).
- **Experiments.** Bullets, one per experiment, as for a hypothesis.

What a research question may and may not conclude:

- Its findings are **exploratory**. They describe; they do not confirm. A
  pattern found in Q data is never used as evidence for a hypothesis written
  after looking at that data.
- A finding that suggests an answer becomes a **new hypothesis** `H<m>`, with
  a criterion, tested in its own experiment. Where the data allow, test it on
  datasets, seeds or settings the question did not use (as H9 does for the
  H5/H6 pattern). If it must reuse the same data, say so in the hypothesis
  and treat the result as weaker.
- The hypothesis names the question it came from (`*(from Q2-E01, F3)*`).

**A hypothesis** follows the existing form in `HYPOTHESES.md`: **Claim**, **Why
it might hold**, **Why it might not**, **Arms**, **Budget**, **Falsification
criterion** (with the unit of analysis, the test and alpha), and
**Experiments**. Add it to *Why this order* if it changes the run order.

Both are committed before any run they cover. That commit is the
**pre-registration commit** the report quotes from.

## 2. Register the experiment before its first run

1. **Issue the ID.** `H<n>-E<nn>` or `Q<n>-E<nn>`, counted from `E01` per
   question or hypothesis in the order they start. A joint experiment carries
   both numbers (`H2H3-E01`). **An ID is never reused.** A crashed, aborted or
   invalid experiment keeps its ID and the next attempt is `E02`. The number
   of attempts is part of the record.
   `python experiments/experiment_ids.py new H10` records it as `running`.
   *`experiment_ids.py` accepts only `H<n>` IDs (`EXPERIMENT_RE`). Before the
   first `Q` experiment, extend it to accept `Q<n>` and commit that change
   first. Tell the user rather than tagging a question's runs with an `H` ID.*
2. **Write the design** in `EXPERIMENTS.md`, *Experiment designs*,
   `### <ID> -- <what it does>`: why this experiment, datasets, arms, budget,
   seeds, and the criterion or analysis plan if it differs from or adds to the
   parent section. Mark when it was added and what was known then ("*Added
   <date>, after H0-E01 had been reported*").
3. **Log the decisions** it runs under that are not already logged (section 4).
4. **Commit, push, then run.** Code, designs and decisions are all committed
   before the first run. On Vega, follow the Vega workflow (commit and push
   here, pull and run there).

A run that serves no question or hypothesis (a smoke test, a timing probe,
debugging) gets no experiment ID and is never cited. A test job on Vega is
such a run.

## 3. Pin the code: run IDs, algorithm IDs, manifests

Every number must be reproducible from commits, not from a working tree.

- **Run ID** `<UTC timestamp>_<name>`: one invocation, one
  `results/<run ID>/` with `manifest.json` (both repositories' commits and
  dirty flags, package versions, input-file hashes, seeds, parameters, command
  line, start and end, `experiment_id`). Written by `provenance.Run`.
- **Run key** `<run ID>/<arm>/<dataset>/s<seed>`: one arm on one dataset with
  one seed.
- **Algorithm ID** `<arm>@<experiments commit>+<fastener commit>#<config>`,
  e.g. `nsga2_sparse@a1b2c3d+9f8e7d6#4c1a`. The arm name alone does not say
  what ran. The two short commits pin the code in both repositories (this
  one and the FASTENER clone), and the 4-hex SHA-256 of the resolved,
  sorted-JSON configuration pins the flags. Any flag that changes an arm's
  behaviour must be part of that configuration. If it is not, add it before
  the run (DEC-27 is the precedent). Arms with different algorithm IDs are
  never pooled unless a decision says why they are equivalent.
- **No evidence from a dirty tree.** A run tagged with an experiment ID is
  refused if either repository has uncommitted code, untracked modules
  included. `--allow-dirty` is for diagnosis only. Its IDs carry `-dirty`,
  its manifest says `evidence: false`, and it is never cited. Docs and
  figure scripts count as code. `results/`, `data/`, `experiments/reports/`
  and `EXPERIMENTS.md` do not (`provenance.NON_CODE_PATHS`).
- A change to the FASTENER clone is committed *in the clone*, and the
  protocol table in `HYPOTHESES.md` names the clone commit in force.

## 4. Log every decision

`experiments/DECISIONS.md` is the record of why each rule is what it is. Any
choice that shapes what an experiment tests or how it is read gets an entry:
a dataset added or dropped, a budget, a classifier, a code fix that changes
an arm, a criterion, how a crash is handled, whether two package versions
count as equivalent.

Entry form (next number; add it to the **Index** and to **By experiment**):

```markdown
### DEC-47

**2026-10-29 -- <the decision, as one line>.**

- **Why:** the reason.
- **Detail:** what exactly was decided, with numbers.
- **By:** PI (what the PI decided); what Claude proposed or implemented.
- **Taken before any <ID> result was read.** / **Taken after <result>.**
- **Source:** commits, and the `HYPOTHESES.md` section.
- **Applies to:** experiment IDs, or questions and hypotheses not yet run.
```

Rules:

- **Never renumber or delete.** A reversed decision gets a new entry naming
  the one it replaces, and the old entry gains `Replaced by DEC-nn`.
- **Say whether a result had been seen**, and which one. A decision taken
  after seeing data is legitimate, but the reader must be able to tell.
- **Name who decided.** Choices that belong to the PI (scope, datasets,
  classifiers, accepting an equivalence, dropping a run) are proposed by
  Claude and decided by the PI. Ask, do not decide them yourself.
- In *By experiment*, each experiment's row lists the decisions it **ran
  under** and the ones it **led to**.

## 5. Change the plan only by revision

After a result exists, the text of a question, hypothesis, criterion or the
protocol is not edited in place. Add a dated entry to `HYPOTHESES.md`,
*Revisions*: what changed, why, what had been seen when it changed, and which
experiments the old and new versions apply to. Then add the matching DEC entry.
A question's analysis plan follows the same rule. Its findings are only
exploratory, but changing the plan after seeing data must still be visible.

## 6. Run and watch

- Queue one process per dataset, arm and seed (`run_queue.py` on the
  workstation, sbatch on Vega). Watch it with `monitor.py --experiment <ID>`.
- Every search records progress per iteration against cumulative fits, so
  that a killed run still leaves its trajectory behind.
- When something breaks, handle it with a decision (DEC-26, adopting the
  running runs after a crash, is the precedent), and record it in the
  report's *What happened*.

## 7. Report and close

Every experiment gets a report, failed ones included, written before the next
experiment on the same question or hypothesis starts. Follow the
`experiment-report` skill. In short: `REPORT.md` (in brief, findings F1..FN
each with a figure, assessment) and `SUPPORT.md` (header with run and
algorithm IDs, the pre-registration commit, the text quoted verbatim,
setup, what happened, evidence, reproduction). Then set the ledger status,
the verdict bullet, *By experiment* and `reports/LIST.md`.

For a **research question** the report differs only in its verdict:

- *In brief* states the question and **the answer as found**: what the data
  show, with the deciding figure. It gives no confirmed or not confirmed.
- **F1 is the analysis registered in the plan.** Later findings are what else
  the data showed, each marked as found, not planned.
- The *assessment* ends with the **candidate hypotheses** the findings
  suggest, each with the data a fair test would need. They are registered as
  `H<m>` only when the user decides to pursue them.

## 8. Commit

- Experiments: commit the code, the designs, the decisions, the revisions and
  `experiments/reports/<ID>/`. Leave `results/` uncommitted.
- Commit as the user only, with no Claude co-author line.
- Never rewrite pushed history. Fix mistakes with new commits.
- Report figures are wide, not tall: landscape, with datasets along x.

## Checklist before the first run of an experiment

- [ ] The question (`Q<n>`) or hypothesis (`H<n>`) is in `HYPOTHESES.md`,
      with its analysis plan or falsification criterion.
- [ ] The experiment ID is issued and its design is in `EXPERIMENTS.md`.
- [ ] Every decision it runs under has a DEC entry, marked as taken before
      the results.
- [ ] Every behaviour-changing flag is in the arms' algorithm-ID config.
- [ ] Both repositories are clean and committed, and this one is pushed.
- [ ] A test job (no experiment ID) has run end to end on the target machine.
