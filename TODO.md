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

**Budget.** *Done.* Equal rounds is not equal budget: the swap arms buy extra fits per generation. `Config.max_model_fits` now stops a run at a fixed number of unique model fits, checked inside `_fitness_function` so the cap is exact rather than per-generation; cache hits and permutation scoring are not charged, every swap candidate is. `run_experiment.py --max-fits` applies one budget to every arm, records `stopped_on` per run, and warns when several arms are run without it.

**Measurement.** *Mostly done.* `analysis.hypervolume` scores a front by the area it dominates in (few features, high score), against a fixed reference point of all features at score 0, so the all-features non-solution contributes zero; `hypervolume_by_seed` gives one row per (arm, seed) and `paired_hypervolume` the seed-paired t-test and Wilcoxon against the published algorithm. Selection stays on validation, measurement on test. Elapsed time already includes permutation scoring, since `search_seconds` wraps the whole mainloop.

*Still open:* fix the seed count explicitly. The runner defaults to 5, which is thin for a paired test -- at \(n=5\) an arm can be genuinely better and still not show it. Use `--seeds 10` or more for an arm comparison; the default is shared with the baseline experiment and was left alone.

**Splits.** [`protocol.py`](experiments/protocol.py) already covers this: three-way stratified train/val/test, `pareto_front` selecting on `val_score`, test untouched during search. It matters more than it sounds -- the reference [`eval_fun`](fastener/fastener.py#L329) scores on `XX_test`, the same data that drives selection, so paper-style FASTENER numbers are optimistic and ours will come in lower. Say so explicitly when reporting, or the comparison will look like a regression.

If an Earth-observation dataset is added, split by spatial blocks or regions.

**The EO dataset is named and confirmed:** [Šircelj, Kenda & Koprivec (2020), "Land Patch Samples", PANGAEA](https://doi.org/10.1594/PANGAEA.914271) -- the dataset behind the FASTENER paper itself. Slovenia 2017, 480×10³ pixel samples, 182 features (4 raw Sentinel-2 bands + 6 vegetation indices over 10 time steps, 18 derived indices, plus DEM height and inclination), 24 classes (23 LPIS-derived agricultural classes grouped from 177 originals, plus non-agricultural). CC-BY-4.0, single 1.3 GB ARFF at `https://hs.pangaea.de/sat/LPIS/FASTENER_dataset.arff`.

Two things to settle before it goes in `data/`: the download host throttles large files (503 "Please wait…" pages, so the fetcher needs retry-with-backoff, not a single `urlopen`), and the spatial split needs a parcel or coordinate column to block on -- whether the ARFF carries one has to be checked against the actual file, since the paper says edge pixels were dropped per land plot but does not say the plot id survives into the published table. Note that 480k rows × 182 features is ~100× MADELON, so a wrapper search over it is a different cost regime.

**Baselines.** Implemented so far: MI / ANOVA-F / tree-importance rankers, RFE, random subsets, all-features, plus mRMR, ReliefF, Boruta, HSIC-Lasso, NSGA-II, POSS ([`poss.py`](experiments/poss.py) -- Qian, Yu & Zhou 2015, the Pareto-archive method closest in shape to FASTENER, so it is the control for what crossover, information guidance and pruning are worth on top of archiving alone) and FS-SDS ([`fs_sds.py`](experiments/fs_sds.py) -- Alhakbani & al-Rifaie 2017). **POSS and FS-SDS are the FASTENER paper's own wrapper comparators, its references [11] and [12]**, so the SotA run now covers the paper's own comparison under a protocol that scores every method identically. NSGAII-MIIP was confirmed to exist and is ported from the authors' MATLAB (see `experiments/README.md`). **BGR-FS is dropped from the plan**: it is paywalled with no public code, and implementing it from the abstract would produce a strawman that says more about the reimplementation than about the method.

## Prior art for the swap: FS-SDS

**Found while implementing the baseline, and it narrows the claim.** FS-SDS's diffusion move is exactly the proposed swap: copy a good agent's subset, drop one selected feature at random, add one unselected feature at random. Uniform at both ends, size-preserving by construction ([`swap_once`](experiments/fs_sds.py)). It was published in 2017 and is cited by the FASTENER paper itself as reference [12].

Three consequences:

- **The `fastener_swap_random` arm is not novel as an operator.** It is FS-SDS's diffusion move relocated into FASTENER's pruning step. That is still a worthwhile ablation -- the question of what the operator does *inside FASTENER* is open -- but it should be described as a known move, with a citation, not as a new one.
- **The guided arm is where the claim now lives.** FS-SDS has no information-gain term anywhere; both ends of its swap are uniform. Choosing \(i\) by permutation importance and \(j\) by mutual information, reusing quantities FASTENER already computes, is the part with no published precedent found so far.
- **The "no FASTENER operator preserves subset size" argument survives intact** -- it is an argument about FASTENER, not about novelty -- but it should now be phrased as "FASTENER lacks the size-preserving move that FS-SDS builds its whole search on", which is both more accurate and a stronger motivation.

A literature check for the guided variant specifically (permutation-importance-weighted removal plus MI-weighted insertion) is still worth doing before any write-up claims novelty.

## Scope of the claim

Swap search itself is established -- add/drop/swap is the standard local-search neighbourhood -- so frame the contribution narrowly: reuse the permutation scores *and* the mutual-information vector FASTENER already computes, to make replacement search nearly free. That is a simple, testable improvement, not yet evidence of a new SotA.
