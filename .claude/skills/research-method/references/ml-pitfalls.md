# ML pitfalls to rule out in the design

These cannot be fixed in the analysis, only in the design. Each item says what
to check before the first run. The sources are REFORMS (Kapoor et al., *Science
Advances*, 2024), Kapoor and Narayanan's leakage taxonomy (*Patterns*, 2023),
Demšar (*JMLR*, 2006) and Bouthillier et al. (*MLSys*, 2021).

## Leakage

- **The test set is read once**, for the final score. Model selection,
  early stopping, hyperparameters, feature selection, thresholds and "which
  experiment to report" are decided on validation or inner folds.
- **Preprocessing is fitted on training data only**: scaling, imputation,
  encoding, feature selection, resampling (SMOTE) and dimensionality reduction
  go inside the cross-validation loop or pipeline.
- **Splits respect structure**: group splits for repeated subjects or
  entities, time splits for temporal data (no future rows in training), and
  spatial blocks for spatially correlated data. Duplicates across splits are
  removed.
- **No feature is a proxy of the target** that would not exist at prediction
  time.
- **The split is fixed and seeded separately from the method's seed**, so
  seeds vary the method, not the data.

## Fair comparisons

- **Equal budget in a stated unit** (fits, epochs, evaluations, GPU hours),
  with wall clock recorded beside it, never substituted silently. When the
  unit differs between methods, say how it was matched.
- **Equal tuning effort.** A tuned new method against default baselines
  measures the tuning. Give each arm the same search budget, or none.
- **One evaluator.** When a method optimises for a model (a wrapper, a
  surrogate), every method is graded by the same model it searched with, or
  the comparison measures home-field advantage.
- **Baselines include the trivial ones**: majority class, all features, random
  subsets or random search, a strong standard method.
- **Reimplementations are labelled** as such, and checked against published
  numbers where possible. Departures from a method's usual configuration are
  labelled too.
- **Thread counts, hardware and library versions are pinned** when cost is
  compared.

## Units of analysis and replication

- **Know what n is.** Seeds of one dataset are replicates of the method's
  randomness, not of the problem. Claims about "datasets in general" need
  datasets as the unit. Folds of one dataset are not independent samples
  (Nadeau and Bengio's corrected t-test, or repeated CV with care).
- **Pseudoreplication**: 5 seeds x 30 datasets is n = 30 for a claim across
  datasets, not 150.
- **Nuisance factors are blocked or randomised**: run order, machine, batch
  and time are not aligned with the arm.
- **Seeds are fixed in advance** (e.g. 2020-2024), never chosen after seeing
  results.

## Statistics over methods and datasets

- **Two methods over many datasets**: Wilcoxon signed-rank on per-dataset
  differences, with wins, ties and losses reported. Zero differences drop out
  of the test; report their count.
- **Several methods**: Friedman test, then pairwise Wilcoxon with Holm
  correction (or Nemenyi), as a full matrix so every pair is visible.
  Critical-difference diagrams summarise it.
- **Per dataset with few seeds**: a per-seed sign or count rule ("better in at
  least 4 of 5 seeds") is honest. A t-test at n = 5 is not.
- **Effect sizes with spread** (median difference, range, bootstrap interval)
  beside every p-value. A p-value is not the probability that the hypothesis
  is true, nor a measure of importance.
- **Multiplicity is declared**: how many metrics, datasets, subgroups and
  looks, and how they are corrected. Secondary metrics are labelled secondary.

## What a small n can answer

Write this into the plan. With 5 seeds you can detect a difference that is large
relative to the seed spread, check a direction ("does X ever beat Y?"), or
find an effect present in every seed. You cannot resolve differences inside
the seed spread. A null result means "not detected at this n", never "no
effect". If a smaller effect matters, increase n, or report a power or
precision analysis before running.

## Reporting checks

- Seed or fold spread on every figure; never a mean alone.
- The split on every figure; test-set curves labelled secondary.
- Progress curves against the budget unit, not iterations, when methods'
  iterations differ.
- Each arm's stop reason (budget, convergence, error, time limit).
- Exclusions and missing runs, with reasons.
- Negative and null results reported with figures.
