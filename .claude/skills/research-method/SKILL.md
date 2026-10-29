---
name: research-method
description: How to organise data-science and machine-learning research so every result is traceable -- start from a research question (exploratory) or a hypothesis (confirmatory), register the plan or falsification criterion before any result, give every experiment an ID that is never reused, pin every run to git commits, data hashes and a config hash, refuse evidence from a dirty tree, keep a decision log and a ledger, change plans only by dated revision, and report every experiment, failed ones included, as a reading and a record. Use when starting a research project or a new line of work, asking a research question, proposing a hypothesis, planning, designing or registering an experiment or benchmark, comparing methods, changing a protocol or taking a decision that shapes results, setting up experiment tracking in a repository, or asking whether a result counts as evidence.
---

# Research method for data science

A procedure for turning questions into evidence that someone else can check:
which question a number answers, what was written down before the data
existed, exactly which code and data produced it, and which decisions it ran
under. If one of those four is missing, the number is a hint, not evidence.

It combines pre-registration (registered plans and the confirmatory/exploratory
split), reproducible computational research (Sandve et al., *Ten Simple
Rules*, 2013), the structure of scientific hypothesis work (observation,
question, hypothesis, prediction and rival explanations kept apart), and
ML-specific practice (REFORMS; Kapoor and Narayanan's leakage taxonomy;
Demšar's tests for comparing methods over datasets).

Reference files, to be read when needed:

- [references/templates.md](references/templates.md): copy-ready templates for a
  question, a hypothesis, an experiment design, a decision entry, a revision,
  the ledger and both report files.
- [references/provenance.md](references/provenance.md): run manifests, method
  IDs, the dirty-tree rule, with a minimal Python implementation.
- [references/ml-pitfalls.md](references/ml-pitfalls.md): leakage, unfair
  comparisons, seeds and units of analysis, statistics over datasets, what a
  small n can answer.
- [references/fastener.md](references/fastener.md): how the FASTENER
  repository implements all of this (an example to imitate).

## 0. Find or set up the project's record

Before anything else, find where the project keeps these. Look for files such
as `METHODOLOGY.md`, `HYPOTHESES.md`, `QUESTIONS.md`, `EXPERIMENTS.md`,
`DECISIONS.md` and `reports/`. **If they exist, follow their conventions, not
this file's defaults.** Where they disagree with this skill, the project wins;
mention the difference to the user once.

If nothing exists, propose this layout, create it once the user agrees, and
commit it before the first experiment:

| file | holds |
|---|---|
| `research/METHODOLOGY.md` | this procedure, as adopted: IDs, statuses, report form |
| `research/PLAN.md` | the protocol (fixed for every experiment), the questions and hypotheses, and *Revisions* at the bottom |
| `research/EXPERIMENTS.md` | the ledger (one row per experiment ID) and each experiment's design |
| `research/DECISIONS.md` | the decision log |
| `research/reports/<ID>/` | `REPORT.md`, `SUPPORT.md`, `figures/`, `tables/` |
| `research/reports/LIST.md` | which experiment to read per question or hypothesis |
| `results/<run ID>/` | run outputs and `manifest.json`, usually not in git |

## 1. Start from a question or from a hypothesis

Keep the objects distinct. An **observation** is what was seen. A **research
question** is what we want to know. A **hypothesis** is a proposed answer that
could turn out wrong. A **prediction** is an observable consequence of a
hypothesis, derived before looking. **Evidence** is the data that bears on a
claim; it is never the claim itself.

There are two ways in. Pick the one the state of knowledge allows, and never
invent a hypothesis just to have one.

| we have | write | fixed before the runs | it produces |
|---|---|---|---|
| a question, and no defensible expectation of the answer | a **research question** `Q<n>` | an **analysis plan**: what is measured, on what, and how it is summarised | descriptive findings and *candidate* hypotheses |
| an expectation that could turn out wrong | a **hypothesis** `H<n>` | a **falsification criterion**: the unit of analysis, the test, the threshold, and what counts as supported, not supported or reversed | a verdict |

**A research question** is specific enough that a figure could answer it ("How
does validation F1 at k <= 10 grow with model fits on tall datasets?", not "How
does the method behave?"). It states why we ask, what would change depending
on the answer, what will be measured, and what it cannot answer.

**A hypothesis** states the claim, why it might hold, **why it might not**
(the rival explanations: a measurement artefact, leakage, a harness bug,
confounding with compute or tuning, chance), the arms or conditions, the
budget, and the criterion. Prefer criteria under which the rivals predict
different outcomes. Declare the claim type (descriptive, associational,
predictive, causal) and use no causal language a predictive design cannot
support.

**What exploratory findings may and may not do.** Findings of a question are
exploratory. A pattern found in data is never used as evidence for a hypothesis
written after looking at that same data (no HARKing). A promising finding
becomes a new hypothesis with its own criterion, tested on data the question
did not use: new datasets, seeds, a held-out split, or a later time period. If
the test must reuse the same data, the hypothesis says so and the result is
reported as weaker. The hypothesis names the finding it came from.

For data that already exist, record what had been seen when the plan was
written (raw outcomes, summaries, earlier results). A plan written after that
cannot make those observations prospective.

**Commit the question or hypothesis before any run it covers.** That commit is
its **pre-registration commit**, and every report quotes from it.

## 2. Fix the protocol once

Everything shared by all experiments goes in one protocol table, decided before
the first run: datasets and their versions, splits (fixed and seeded, with the
test split read once), the primary metric and its aggregate, seeds, budget and
its unit (fits, epochs, GPU hours), the model or evaluator, preprocessing, and
the statistical tests. Each row says why. An experiment may deviate from it only
if its design says how and why.

See [references/ml-pitfalls.md](references/ml-pitfalls.md) before fixing it:
equal budgets and equal tuning across arms, one evaluator for every method,
no information crossing from test to training, and the right unit of analysis.

## 3. Register each experiment before its first run

1. **Issue an ID.** `<Q or H number>-E<nn>`, e.g. `Q2-E01`, `H4-E03`, counted
   per question or hypothesis in the order experiments start. A joint
   experiment carries both numbers (`H2H3-E01`). **IDs are never reused.** A
   crashed, aborted or invalid experiment keeps its ID, and the next attempt
   is `E02`: the number of attempts is part of the record. Add the ledger row
   now, with status `running`.
2. **Write the design** in the ledger's *Experiment designs*: why this
   experiment, what was known when it was added, datasets, arms, seeds,
   budget, and the criterion or plan where it adds to the parent.
3. **Log the decisions** it runs under (section 5).
4. **Run a test job** end to end on the target machine. It carries no
   experiment ID and is never cited.
5. **Commit and push, then run.**

Runs that serve no question (smoke tests, timing probes, debugging) get no
experiment ID and are never evidence.

## 4. Pin code, data and configuration

The goal is that every number can be regenerated from a commit, never from a
working tree. Details and code are in [references/provenance.md](references/provenance.md).

- **Run ID** `<UTC timestamp>_<name>`. One invocation writes one
  `results/<run ID>/` with a `manifest.json`: commits and dirty flags of every
  repository involved, package versions, input-data hashes, seeds, the
  resolved configuration, the command line, host, start and end, status, and
  the experiment ID.
- **Run key** `<run ID>/<arm>/<dataset>/s<seed>`: one arm on one dataset with
  one seed.
- **Method ID** `<arm>@<commit>[+<commit of each other repo>]#<config hash>`,
  for example `xgb_tuned@a1b2c3d+9f8e7d6#4c1a`. The arm name alone does not
  say what ran. The commits pin the code, and the short hash of the resolved
  configuration (sorted JSON) pins every flag. Any option that changes
  behaviour must be part of that configuration. Results with different
  method IDs are never pooled unless a decision says why they are equivalent.
- **No evidence from a dirty tree.** A run tagged with an experiment ID is
  refused if any repository has uncommitted or untracked code. A forced
  diagnostic run is marked `-dirty` and `evidence: false`, and is never cited.
  Plan files, analysis and figure scripts count as code. The outputs runs
  write do not.
- **Data are versioned too**: a content hash per input file, or the version
  of a data-versioning tool, in every manifest.
- **No manual steps** between raw data and a reported number. Every table and
  figure comes from a committed script reading run directories, and the
  numbers behind each figure are saved beside it.

## 5. Keep a decision log

Every choice that shapes what an experiment tests or how it is read gets a
numbered entry `DEC-<nn>`: a dataset added or dropped, a budget, a metric, a
model, a bug fix that changes an arm, how a crash is handled, whether two
library versions count as equivalent. The template is in
[references/templates.md](references/templates.md). Every entry has:

- **date and title**, then **Why**, **Detail**, **By** (who decided, and what
  an assistant proposed or implemented), **Source** (commits, plan section)
  and **Applies to** (experiment IDs, or questions not yet run);
- **whether a result had been seen**, and which one. Decisions taken after
  seeing data are legitimate, but a reader must be able to tell.

Rules: never renumber or delete. A reversed decision gets a new entry naming
the one it replaces, and the old entry gains `Replaced by DEC-nn`. Keep an
index, and a *By experiment* table listing the decisions each experiment
**ran under** and **led to**.

**The owner decides; the assistant proposes.** Scope, datasets, models,
accepting an equivalence, excluding a run and changing a criterion belong to
the person who owns the research. Ask, and record who decided.

## 6. Change the plan only by revision

Once a result exists, the text of a question, hypothesis, criterion or the
protocol is not edited in place. Add a dated entry to *Revisions*: what
changed, why, what had been seen, and which experiments run under the old and
the new version. Add the matching decision entry. A deviation found during a
run (a crash, a dropped dataset, a changed budget) is logged the same way, with
its expected effect on the result.

## 7. Run and watch

- Prefer one process per arm, dataset and seed, so a failure costs one cell
  and cells can be rerun alone. A single cell run on its own reproduces the
  same cell run inside a batch.
- Log progress during the run (for searches: best score against cumulative
  budget), flushed as it goes, so a killed run still leaves a trajectory.
- Record wall clock beside the budget unit, and why each arm stopped (budget,
  convergence, error, time limit).
- Pin thread counts and hardware where timing is compared.
- Handle failures with a decision entry, and record them for the report.

## 8. Report every experiment

Every experiment gets a report, failed and invalid ones included, written
before the next experiment on the same question or hypothesis starts. Two
files in `reports/<ID>/` (templates in
[references/templates.md](references/templates.md)):

- **`REPORT.md`, the reading**, for someone who has not followed the work.
  *In brief*: the question or hypothesis and how it is judged, in plain words,
  then the answer with its deciding number and figure. *Findings* F1..FN:
  each a specific sentence, the numbers behind it, and a figure. F1 is the
  registered criterion or plan. Later findings that were not planned are
  marked as such. *Assessment*: what is supported and how strongly, effect
  sizes with their spread, what the result does not show, limits, and what
  follows.
- **`SUPPORT.md`, the record**: run IDs and method IDs, the pre-registration
  commit, the question or hypothesis and criterion **quoted verbatim**, the
  setup and its deviations, *what happened* (timeline, failures, anomalies),
  the evidence tables, and the commands that reproduce everything.

Rules: a claim no figure shows is not a finding. Seed or fold spread is on
every figure; a mean is never plotted alone. Every figure says which split it
shows. A null or negative result gets the same care as a positive one. Every
number in the prose matches a generated table; nothing is computed by hand.
Generate as much of both files as possible from the runs, then write the
prose.

**A hypothesis report** gives a verdict: confirmed, not confirmed, or reversed,
qualified if needed ("confirmed, narrowly"). Report a mechanical reading of the
criterion beside the verdict, so a defect the mechanics cannot see can still
overrule it. "Not detected at n = 5" is never written as "no effect".

**A question report** gives no verdict. *In brief* states the answer as found.
The *assessment* ends with **candidate hypotheses**, each with the data a fair
test needs. They become `H<m>` only when the owner decides to pursue them.

Then close the experiment: set its ledger status (`reported`, `failed`,
`invalid`; a row is never deleted), add the verdict to the parent's
*Experiments* bullets, update *By experiment* in the decision log, and update
`reports/LIST.md` (per question or hypothesis, the experiment to read, and
which ones were superseded or failed and why).

## 9. Commit

Commit plans, decisions, designs, code and reports. Never rewrite pushed
history; fix mistakes with new commits. Whether bulk run outputs go in git is
a project decision: log it as one.

## Checklist before an experiment's first run

- [ ] The question or hypothesis, with its plan or criterion, is committed.
- [ ] What had already been seen of the data is recorded.
- [ ] The experiment ID is issued and its design written in the ledger.
- [ ] Every decision it runs under is logged and marked as taken before the
      results.
- [ ] Every behaviour-changing option is in the method ID's config.
- [ ] Data hashes, seeds and package versions go into the manifest.
- [ ] Every repository is clean, committed and pushed.
- [ ] A test job has run end to end on the target machine.
- [ ] The leakage and fairness checks in `ml-pitfalls.md` pass.
