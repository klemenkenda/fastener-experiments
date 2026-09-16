# TODO - FASTENER IMPROVEMENT

Add a guided feature swap to FASTENER's existing pruning step. It offers a plausible improvement in search efficiency; beating current SotA would still need experiments.

FASTENER already combines a Pareto archive, information-guided crossover, random mutation, and pruning using permutation importance. The useful opening is in pruning: it identifies a weak feature and tests deleting it, but does not directly test replacing it with another feature. Confirmed in the clone -- [`purge_item_with_information_gain`](fastener/fastener.py#L163) permutes each selected feature, sorts by score delta, unsets the weakest and evaluates, with no replacement candidate anywhere in the step. [FASTENER, Sections 3.2-3.4](https://ailab.ijs.si/wp-content/uploads/2021/04/fastener.pdf)

## The proposed change

Whenever FASTENER prunes a subset \(S\):
1. Identify its least important feature \(i\), using the permutation scores already computed.
2. Evaluate the usual deletion candidate: \(S\setminus\{i\}\).
3. Also sample one feature \(j\notin S\) and evaluate:\[
   S_{\mathrm{swap}}=(S\setminus\{i\})\cup\{j\}.
   \]
4. Pass both candidates through the existing Pareto update.

**Sample \(j\) weighted by mutual information, not uniformly.** [`IntersectionMatingWithInformationGain.use_data_information`](fastener/item.py#L155) already computes `mutual_info_classif` over all features once per run, and the weighted-random mating variant already samples from that vector. Reusing it keeps the "no new information" property while making the insertion guided rather than blind. Uniform \(j\) is the wrong default: on MADELON (\(d=500\), ~20 informative features) it lands on something useful about 4% of the time, and pruning only fires every `reset_to_pareto_rounds = 5` generations, once per front item. Too few draws at too low a hit rate to show an effect in either direction.

This adds one model **fit** per pruned subset, with no extra importance calculation, model type, or tuning parameter. (Each permutation score is only a `predict`; the swap candidate needs a `fit`. One extra fit against \(|S|\) predicts is the honest unit, not "one extra evaluation".) Keep the original mutation and crossover.

Two implementation notes, so they are not discovered mid-build:
- The information-gain vector lives on the mating strategy, not on the optimizer, so it needs plumbing through to the pruning step.
- [`purge_front_with_information_gain`](fastener/fastener.py#L139) asserts `new_item.size == num - 1` and assigns one item per size. The swap candidate has size \(|S|\), so the loop and the assertion must be restructured to carry two candidates of different sizes. The swap then competes directly against the incumbent front entry at that size, which is the intended comparison.

## Why it could help

A feature can be worth replacing even when deleting it alone hurts accuracy. The swap tests that replacement directly while preserving the feature count.

The sharper argument is that **no FASTENER operator preserves subset size.** Mating changes it -- `IntersectionMating` pulls a child toward \(m_{\min} + (m_{\max}-m_{\min})/2 + 1\), i.e. toward the middle -- and pruning strictly decreases it. Only mutation can hold size constant, and only by flipping two bits at once: with \(1/d\) per-bit flips that has probability \(\approx k(d-k)/d^2\), about 0.047 for \(k=10\) out of \(d=200\). Same-size exploration is therefore a second-order event with no dedicated operator behind it. The proposed swap is that missing operator.

(An earlier version of this section argued from the additions/deletions asymmetry: \((d-k)/d\) additions against \(k/d\) deletions per mutation, 0.95 against 0.05 at \(k=10\), \(d=200\). The arithmetic is right -- see [`RandomFlipMutationStrategy`](fastener/item.py#L315) -- but it does not imply runaway subset growth, because the population and the front are both keyed by size with per-size buckets, so large subsets cannot crowd out small ones. The size-preserving-move argument is the one that survives.)

Hypothesis is therefore: better accuracy at small feature counts, reached with fewer model fits, especially when an early selection contains a useful but replaceable feature.

## The clean experiment

Compare three versions:
- Original FASTENER.
- FASTENER with random swaps (random \(i\), uniform \(j\)).
- FASTENER with guided swaps (permutation-weakest \(i\), IG-weighted \(j\)).

The middle arm is the ablation that isolates the guidance. It only earns its place because the third arm guides both ends -- with uniform \(j\) the two swap arms would differ solely in the choice of \(i\), which is too thin to be worth the compute.

**Budget.** Equal rounds is not equal budget: the swap arms buy extra fits per generation. [`run_experiment.py`](experiments/run_experiment.py) currently fixes `--rounds` and counts fits after the fact via `CountingModelFactory`. Convert that into a fit-capped stopping condition so every arm halts at the same number of fits. `cached_fitness` makes repeated subsets free, so count *unique* fits, and count every added swap evaluation against the cap.

**Measurement.** Report the accuracy-feature-count Pareto front, and add a scalar so the arms are actually comparable: hypervolume (or attainment surface) over the front, with a paired test across seeds. [`analysis.py`](experiments/analysis.py) currently averages over seeds and tabulates by \(k\), with no test -- that needs adding. Fix the seed count explicitly; the runner defaults to 5, which is thin for a paired test. Also report elapsed time including permutation scoring.

**Splits.** [`protocol.py`](experiments/protocol.py) already covers this: three-way stratified train/val/test, `pareto_front` selecting on `val_score`, test untouched during search. It matters more than it sounds -- the reference [`eval_fun`](fastener/fastener.py#L329) scores on `XX_test`, the same data that drives selection, so paper-style FASTENER numbers are optimistic and ours will come in lower. Say so explicitly when reporting, or the comparison will look like a regression.

If an Earth-observation dataset is added, split by spatial blocks or regions. Right now only MADELON is in `data/`, so either name the EO dataset and fetch it or drop it from the plan.

**Baselines.** Implemented so far: MI / ANOVA-F / tree-importance rankers, RFE, random subsets, all-features. For a current-SotA claim, add recent evolutionary baselines that already incorporate relevance/redundancy guidance. NSGAII-MIIP and BGR-FS were noted as candidates but are neither cited nor implemented -- track down the actual references and confirm they exist before they go into the plan.

## Scope of the claim

Swap search itself is established -- add/drop/swap is the standard local-search neighbourhood -- so frame the contribution narrowly: reuse the permutation scores *and* the mutual-information vector FASTENER already computes, to make replacement search nearly free. That is a simple, testable improvement, not yet evidence of a new SotA.
