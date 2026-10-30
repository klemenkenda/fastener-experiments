# Templates

Copy and fill. Dates are absolute (`2026-10-29`). Field names are kept, so the
record can be searched.

## Research question (in the plan)

```markdown
## Q<n> -- <the question, as one sentence>

*(added <date>; asked by <who>)*

**Question.** <Specific enough that a figure could answer it.>

**Why we ask.** <What is unknown; what we would do differently depending on
the answer.>

**Already seen.** <What of these data had been looked at when this was
written: none / summaries / earlier results, which.>

**What will be measured.** <Metrics, splits, datasets, arms, budget, seeds.
How results are summarised: per-seed points, ranges, curves against the
budget unit.> The protocol applies unless stated otherwise.

**What it cannot answer.** <Limits set by seeds, datasets, budget, design.>

**Experiments.**
* `Q<n>-E01` -- <one line; after the report: what it found, one sentence>
```

## Hypothesis (in the plan)

```markdown
## H<n> -- <the claim, as one sentence>

*(added <date>; proposed by <who>; from <Q<m>-E<nn> F<k>, or "a priori">)*

**Claim.** <What is expected, at which settings. Claim type: descriptive /
associational / predictive / causal.>

**Why it might hold.** <Mechanism or prior evidence.>

**Why it might not.** <Rival explanations: artefact, leakage, harness bug,
unequal compute or tuning, confounding, chance, overfitting to validation.>

**Arms.** <Each arm, what makes it differ. The control.>

**Budget.** <Unit and amount, equal across arms or why not.>

**Falsification criterion.** Unit of analysis: <datasets / seeds / folds>.
Effect per unit: <definition>. **Supported** if <...>. **Reversed** if <...>.
Otherwise **not supported**: <what that means at this n>. Ties and missing
units: <rule>.

**Experiments.**
* `H<n>-E01` -- <one line; after the report: the verdict, one sentence>
```

## Experiment design (in the ledger, under *Experiment designs*)

```markdown
### `<ID>` -- <what it does, one line>

*Added <date>, <before any run / after <ID> was reported>.*

**Why.** <What this experiment adds; what the previous attempt left open.>

**Datasets.** <List, versions, row caps, why these and not others.>

**Arms, seeds, budget.** <As the parent, or the differences.>

**Criterion / plan.** <As the parent, or what it adds. Fixed before the runs.>

**Runs on.** <Machine, parallelism, expected duration.>
```

## Ledger row

```markdown
| experiment | parent | started | run IDs | status | report |
|---|---|---|---|---|---|
| `H4-E03` | H4 | 2026-10-12 | `20261012T081500Z_h4` | reported | [report](reports/H4-E03/REPORT.md) |
```

Status: `running`, `failed` (did not finish), `invalid` (finished, but a defect
makes it unusable), `reported`. Rows are never deleted.

## Decision entry

```markdown
### DEC-<nn>

**<date> -- <the decision, as one line>.**

- **Why:** <the reason>.
- **Detail:** <what exactly, with numbers>.
- **By:** <owner: what they decided>; <assistant: what it proposed or
  implemented>.
- **Taken before any <ID> result was read.** / **Taken after <result>, which
  showed <...>.**
- **Source:** <commits; plan section>.
- **Applies to:** <experiment IDs, or Q/H not yet run>.
- **Replaces:** DEC-<mm>. *(if it does; the old entry gains `Replaced by`)*
```

Index row: `| [DEC-<nn>](#dec-<nn>) | <date> | <title> | <applies to> |`.

*By experiment* row:
`| <ID> | <status: verdict> | <DECs ran under> | <DECs led to> | <report> |`.

## Revision (bottom of the plan)

```markdown
**<date> -- <what changed>.** <Changed from ... to ...>. Why: <...>.
Seen at the time: <which results, or none>. Experiments under the old
version: <IDs>; under the new: <IDs>. See DEC-<nn>.
```

## REPORT.md

```markdown
# <ID> -- <short title>

## In brief

**The hypothesis / The question.** <Two or three plain sentences.>
**How it is judged.** <The criterion or plan, in plain words.>

**The answer: <confirmed / not confirmed / reversed / as found>.** <Two to four
sentences with the one deciding number.>

![](figures/F1_<...>.png)
*<One-line caption.>*

## Findings

### F1 -- <The result on the registered criterion, as one specific sentence.>

<What was measured, the numbers (ranges over seeds), what they mean.>

![F1](figures/F1_<...>.png)
*<What is plotted, axes, split, what the points or band show.>*

### F2 -- <...> *(not planned)*

## Assessment

<As for a paper's discussion: what is supported and how strongly, effect sizes
with spread, what is not shown, limits from n, datasets, budget, and what
follows. Refers to findings by number; no new numbers. For a question: end
with candidate hypotheses and the data a fair test needs.>
```

## SUPPORT.md

Six sections, none dropped; one with nothing to say says so in one line.

1. **Header**: experiment ID, parent, run IDs with status, method IDs, the
   pre-registration commit, code commits, dates, the mechanical reading of
   the criterion.
2. **Question / hypothesis**: quoted verbatim from the pre-registration commit.
3. **Evaluation criteria / plan**: quoted verbatim, with any revisions.
4. **Description**: *Setup* (datasets with sizes, arms with method IDs, seeds,
   budget, splits, command lines, deviations or "none") and *What happened*
   (timeline, budget used and wall clock per arm, why each stopped, missing,
   duplicate or excluded runs, anomalies, defects and the commit that fixed
   them).
5. **Evidence**: the generated tables the criterion is read from, per unit;
   no interpretation.
6. **Reproduction**: commands, from a clean checkout at the recorded commits,
   that rerun each run and regenerate every table and figure.

## reports/LIST.md

```markdown
# Completed experiments

| parent | experiment | duration | result | why this one | report |
|---|---|---|---|---|---|

## Superseded and failed

| parent | experiment | duration | status | result | why | report |
|---|---|---|---|---|---|---|
```

Every cell a few words.
