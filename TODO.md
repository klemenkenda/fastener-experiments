# TODO - FASTENER IMPROVEMENT

Add a guided feature swap to FASTENER’s existing pruning step. It offers a plausible improvement in search efficiency; beating current SotA would still need experiments.

FASTENER already combines a Pareto archive, information-guided crossover, random mutation, and pruning using permutation importance. The useful opening is in pruning: it identifies a weak feature and tests deleting it, but does not directly test replacing it with another feature. [FASTENER, Sections 3.2–3.4](https://ailab.ijs.si/wp-content/uploads/2021/04/fastener.pdf)

## The proposed change
Whenever FASTENER prunes a subset \(S\):
1. Identify its least important feature \(i\), using the permutation scores already computed.
2. Evaluate the usual deletion candidate: \(S\setminus\{i\}\).
3. Also sample one feature \(j\notin S\), uniformly, and evaluate:\[
   S_{\mathrm{swap}}=(S\setminus\{i\})\cup\{j\}.
   \]
4. Pass both candidates through the existing Pareto update.

This adds one candidate evaluation per pruned subset, with no extra importance calculation, model type, or tuning parameter. Keep the original mutation and crossover.

## Why it could help
A feature can be worth replacing even when deleting it alone hurts accuracy. The swap tests that replacement directly while preserving the feature count.
There is also a concrete search imbalance: with \(k\) selected features among \(d\), FASTENER’s basic \(1/d\) bit mutation produces, on average, \((d-k)/d\) additions but only \(k/d\) deletions. For 10 selected features out of 200, that is 0.95 additions versus 0.05 deletions. Crossover and pruning partly compensate; the proposed swap explicitly searches for better subsets of the same size. These expectations follow directly from the paper’s mutation rule. [FASTENER, Section 3.2](https://ailab.ijs.si/wp-content/uploads/2021/04/fastener.pdf)

Hypothesis is therefore: better accuracy at small feature counts, reached with fewer evaluations, especially when an early selection contains a useful but replaceable feature.

## The clean experiment

Compare three versions under identical total training budgets:
- Original FASTENER.
- FASTENER with random swaps.
- FASTENER with the guided swaps above.

Measure the accuracy–feature-count Pareto front, elapsed time including permutation scoring, and variability across seeds. Use an untouched outer test set; for Earth observation, split by spatial blocks or regions. Count every added swap evaluation against the budget.

For a current SotA claim, include recent evolutionary baselines such as NSGAII-MIIP (2025) and BGR-FS (2026), which already incorporate relevance/redundancy guidance. NSGAII-MIIP, BGR-FS

Swap search itself is established, so I would frame the contribution narrowly: reuse FASTENER’s existing pruning information to make replacement search inexpensive. That is a simple, testable improvement—not yet evidence of a new SotA.