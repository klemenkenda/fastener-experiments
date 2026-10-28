# Contributions to methods

What this project changed or added in the methods: FASTENER itself, the
methods it is compared with, and how they are evaluated. For each, what it
is, why it was done, where it is recorded, what it did to results, and who
decided it.

**Attribution.** Every commit in this repository and in the FASTENER clone
since the 2020 initial commit (Filip Koprivec) is authored by Klemen Kenda,
the PI. *Decided by* quotes the decision's **By** line in
[`DECISIONS.md`](DECISIONS.md); "not recorded" means that decision's entry
names no one. Where the record says Claude proposed or implemented part of a
decision, that is stated. Results are summarised from the reports
([`reports/LIST.md`](reports/LIST.md)).

## 1. FASTENER

Changes in the clone (`fastener/`, now at `3be5697`; see its `CHANGELOG.md`).
Each behavioural change is behind a flag or verified to leave the search
unchanged, so the published 2020 algorithm can still be run exactly.

| contribution | what and why | where | effect | decided by |
|---|---|---|---|---|
| Move off the 2020 software stack | The 2020 pins no longer install; the code runs on current NumPy, scikit-learn and Python. | `ff313d1`; [DEC-06](DECISIONS.md#dec-06) | The `fastener_2020` arm reproduces the published algorithm on the new stack. | not recorded |
| Unit tests | Tests for the mating, pruning and swap strategies. | `b60e978`, `564eb8a` | Every later change is checked against them. | -- |
| Three mating bugs found and fixed | (1) Weighted information-gain mating always added the top-k genes, so a child got up to 2k genes back and the weighted sample rarely added anything; (2) an item could be mated with itself (about 13% of pairs at `pool_size=3`); (3) `pool_size=None` crashed. Flags `include_top_genes` and `allow_self_mating` restore the 2020 behaviour. | `564eb8a`; HYPOTHESES.md, H0 | Both fixes together: faster convergence, narrowly (H0-E02). | -- |
| Top genes kept by default | Fix 1 reverted by default, since H0 showed it changes the search, not just repairs it; only the self-mating fix remains. This is stock FASTENER in H1–H6. | `08e6acd`; [DEC-23](DECISIONS.md#dec-23) | Self-mating fix alone: no change in convergence or end result (H0-E03, p = 0.52). | PI |
| Size-preserving swap operator | FASTENER had no operator that changes a subset's content at the same size. `SwapStrategy` in the pruning step drops one feature and inserts another: `InformationGainSwapStrategy` drops the permutation-weakest and inserts by mutual information (reusing vectors FASTENER already computes); `RandomSwapStrategy` is its ablation. Opt-in. | `71281c0`; HYPOTHESES.md, H2, H3 | Random swap: no effect (H2). Guided swap: +0.003 median AUF, p = 0.040, on small datasets only (H3); not separable from stock FASTENER in H6. | not recorded |
| Fit-capped stopping | `Config.max_model_fits` stops a run exactly at a budget of unique fits, checked where the model is fitted; cache hits are free. Opt-in. | `71281c0`; [DEC-04](DECISIONS.md#dec-04) | Makes every equal-budget comparison exact. | not recorded |
| Pruning counters | Counts deletions and swaps proposed, fitted and kept. | `b7e724d` | Showed that about 1 swap in 100 wins its size slot (H2H3-E01). | -- |
| Vectorised gene bookkeeping | NumPy bookkeeping; identical fronts for the same seed. | `3877a1a`; [DEC-39](DECISIONS.md#dec-39) | Less CPU per fit; used from H4-E03 on. | PI (equal fits, fix the bookkeeping); implementation and checks by Claude |
| Fast mutual information | MI computed by sorting each feature: the same values, 5–11× faster. | `3be5697` | Lower start-up cost on wide datasets. | -- |
| Bounded model store (harness) | The harness kept every fitted model; under the random forest that grew runs to 3.4 GB and filled the cluster quota. Only the models on the front are kept; LightGBM models are sized by their booster. | `run_fastener.py`; [DEC-42](DECISIONS.md#dec-42), [DEC-44](DECISIONS.md#dec-44) | Memory flat; no result changes. | PI (rerun the FASTENER jobs, after the diagnosis); diagnosis, implementation and checks by Claude |

## 2. The methods FASTENER is compared with

| contribution | what and why | where | effect | decided by |
|---|---|---|---|---|
| NSGAII-MIIP port | A Python port of Li et al.'s MATLAB code (which needs MATLAB and Weka), labelled a reimplementation everywhere. | `nsgaii_miip.py`; [DEC-07](DECISIONS.md#dec-07) | In the H5/H6 field. | not recorded |
| Sparse-start NSGA-II | NSGA-II started from random subsets of 1–30 features instead of opposition-based initialisation at about p/2: a labelled control that separates "the search is worse" from "it started elsewhere". | `a62beff`, `2fba678`; [DEC-07](DECISIONS.md#dec-07) | H1 confirmed: the OBL start never reaches k ≤ 10 on datasets with 182 features or more; the sparse start always does. One of the four leaders in H5/H6. | not recorded |
| Stagnation stop for NSGA-II and NSGAII-MIIP | Stop after a number of generations that produce no new subset, as FS-SDS already did. Under the tree, 42 of 47 timeouts were converged NSGA-II runs re-proposing cached subsets for up to a million generations. | `sota_baselines.py`, `nsgaii_miip.py`; [DEC-41](DECISIONS.md#dec-41) | No timeouts under the forest; 93 runs ended on it. | PI; implementation by Claude |
| POSS, FS-SDS and the filters in one harness | POSS (Qian et al. 2015), FS-SDS (Alhakbani & al-Rifaie 2017), Boruta, RFE, mRMR, HSIC Lasso, ReliefF, the MI, ANOVA-F and tree-importance rankers and random subsets, all run through `run_sota.py` on the protocol classifier, with the same budget, split and score. | `sota_baselines.py`, `poss.py`, `fs_sds.py`, `run_sota.py` | The 17-selector field of H5/H6. | not recorded |
| Boruta follows the protocol model | Boruta's importances come from the protocol classifier (tree, forest or LightGBM), not a fixed forest. | [DEC-41](DECISIONS.md#dec-41) | -- | PI |
| ELM on both sides | FASTENER and FS-SDS both driven and scored by the ELM the 2020 paper used for FS-SDS. | [DEC-38](DECISIONS.md#dec-38) | Shows the classifier was not the confound that mattered in Table 3 (H4-E02). | PI |
| LightGBM with a scaled smallest leaf | `min_child_samples = min(20, max(1, n_train // 20))`: at LightGBM's default of 20 the smallest training splits (24–34 rows) barely split. | `protocol.py`; [DEC-44](DECISIONS.md#dec-44) | H5H6-E03, running. | PI (LightGBM; the scaled leaf; registering as H5H6-E03) |

## 3. How the methods are evaluated

| contribution | what and why | where | decided by |
|---|---|---|---|
| Pre-registration | Every hypothesis has a claim and a falsification criterion written before its experiment runs; revisions are dated and made before the runs they affect; every earlier result was discarded as evidence. | [DEC-09](DECISIONS.md#dec-09), [DEC-10](DECISIONS.md#dec-10); `HYPOTHESES.md` | not recorded |
| One protocol for every method | One classifier drives every search and scores every subset; a 60/20/20 split, selection on validation, test read once; weighted F1. Removes the per-method settings of the 2020 comparison. | [DEC-02](DECISIONS.md#dec-02), [DEC-03](DECISIONS.md#dec-03), [DEC-11](DECISIONS.md#dec-11), [DEC-12](DECISIONS.md#dec-12) | DEC-11: PI; DEC-12: PI (seeds); others not recorded |
| Budgets in unique model fits | Searches are compared at the same number of unique fits, not generations or rounds, with progress read against cumulative fits. | [DEC-04](DECISIONS.md#dec-04), [DEC-14](DECISIONS.md#dec-14) | not recorded |
| AUF (K) on validation-chosen subsets | For each k = 1..K, the best subset of at most k features chosen on validation, its test F1 read once; AUF is the mean, and a size never reached counts as zero, so it measures reach and quality together. | [DEC-12](DECISIONS.md#dec-12); `HYPOTHESES.md`, *Terms* | PI (seeds); rest not recorded |
| Fits to a common target | A convergence measure: the unique fits each arm needs to reach the lower of the two arms' final validation AUF, so a search that stalls early does not look fast. | [DEC-17](DECISIONS.md#dec-17) | not recorded |
| Per-dataset budget calibration | On a seed outside the experiment, the smallest budget at which stock FASTENER has converged and reaches Boruta's validation AUF, then one step up. | [DEC-24](DECISIONS.md#dec-24), [DEC-33](DECISIONS.md#dec-33) | PI; the convergence threshold proposed by Claude; the calibration with Boruta as the reference is the PI's |
| Equal CPU time against equal fits | H4 run both ways: equal process CPU time per dataset (single-threaded, DEC-37), and equal model fits. Separates what a method does per evaluation from what it does per unit of compute. | [DEC-36](DECISIONS.md#dec-36), [DEC-37](DECISIONS.md#dec-37), [DEC-39](DECISIONS.md#dec-39) | DEC-36, DEC-39: PI; DEC-37: Claude, at the PI's request |
| Datasets as the unit | Per-dataset effects averaged over seeds, a Wilcoxon signed-rank test over datasets, Holm correction across pairs (H5/H6). | [DEC-21](DECISIONS.md#dec-21), [DEC-33](DECISIONS.md#dec-33) | PI |
| Datasets chosen by shape | The UCR/UEA archive clustered on log(examples) and log(features) into seven clusters, datasets drawn from each, so results can be read by data shape; tall datasets added next to the wide paper benchmarks. | [DEC-13](DECISIONS.md#dec-13), [DEC-33](DECISIONS.md#dec-33); [`DATASETS_USED.md`](DATASETS_USED.md) | DEC-33: PI, from options Claude proposed; DEC-13 not recorded |
| A per-run cap with stated reasons | 6 hours per run; cells over it are skipped or timed out with the reason given, never silently dropped; tests read only the datasets both methods have. | [DEC-40](DECISIONS.md#dec-40) | PI (datasets, accepting missing cells with reasons, the 6 h cap); pilot, estimates and implementation by Claude |
| Provenance | Experiment, run and algorithm IDs, a ledger, a manifest per run, and no evidence from uncommitted code; on the cluster, commits read from `.git` and verified at submission. | [DEC-05](DECISIONS.md#dec-05), [DEC-15](DECISIONS.md#dec-15), [DEC-43](DECISIONS.md#dec-43) | DEC-43: PI (approach), implementation by Claude; others not recorded |
| Reports in two parts | A short reading (REPORT.md, every finding with a figure) and its record (SUPPORT.md). | [DEC-32](DECISIONS.md#dec-32) | PI |

## 4. What the method changes showed

- **FASTENER's 2020 lead over FS-SDS holds per evaluation, not per unit of
  compute** (H4-E01, H4-E03). The budget unit, not the classifier (H4-E02),
  decides the ordering.
- **NSGA-II's failure at small k is its initialisation** (H1); a sparse start
  removes it, and the result holds on the full grid (H5H6-E01, H5H6-E02).
- **A size-preserving move matters little in FASTENER**: random, none (H2);
  guided, a small gain on small data (H3).
- **Under one protocol no selector is best everywhere** (H5, H6): FASTENER is
  one of four population searches at the top, within 0.004 AUF of each other
  under the forest, and which method leads depends on the data cluster and
  the classifier.

## 5. Proposed, not yet done

From the outlook of the summary paper
([`reports/FASTENER_experiments_report.docx`](reports/FASTENER_experiments_report.docx),
Section 10). None is implemented or registered.

- FASTENER for **regression**: mutual information with a continuous target,
  R²-based AUF, regression forms of every competitor; a hypothesis H7.
- **LLM-guided selection**: an LLM prior mixed with mutual information in
  initialisation, mating and the swap; an LLM proposal operator paid from the
  fit budget; an LLM critic of the final front.
- **A feature knowledge graph with LLM reasoning**: graph-aware operators, a
  redundancy and acquisition-cost objective, surrogate scoring, proposals
  that must cite graph paths, and memory of what was selected where.
