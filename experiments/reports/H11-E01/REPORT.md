# H11-E01 -- report (post hoc)

*Hypothesis H11. **Post hoc**: the claim was formed after the results it is judged on had been read ([DEC-48](../../DECISIONS.md#dec-48)), so this report says how the Boruta seed fares under H10's registered criterion; it does not confirm anything. The record is in [SUPPORT.md](SUPPORT.md).*

## 1. In brief

### The hypothesis

H10 tested FASTENER started from a filter's best 1-10 features, with mRMR as
the primary seed and Boruta as a secondary one expected to be weaker. In the
event the Boruta seed did better under all three classifiers. H11 asks
whether the Boruta seed, had it been the primary arm, would have met H10's
claim: better than Boruta alone, no worse than stock FASTENER at the end of
the budget, and ahead of it part-way through.

**How it is judged.** By H10's criterion, unchanged, so that nothing is
chosen after seeing the results: (a) more wins than losses against Boruta
alone and Wilcoxon p < 0.05; (b) the one-sided 95% lower bound of the mean
difference to stock FASTENER above -0.005; (c) ahead of stock FASTENER at
10% and 25% of the budget, Wilcoxon after Holm. All three, under LightGBM
for the verdict (as H10), the forest and the tree beside it. No new runs:
the numbers are H10-E01 to -E03's.

### The answer: not confirmed

The Boruta seed passes (a) under every classifier and (b) under the forest
and the tree, but (c) under none: its lead at 10% of the budget is
+0.000 to +0.008 and never significant. Under LightGBM, which gives the
verdict, it also misses (b) (lower bound -0.008), on one dataset.

![H11 under LightGBM](../H10-E01/figures/F1_H10_criterion.png)

*H10-E01's criterion figure; the Boruta seed is the orange column in each panel.*

## 2. Findings

### F1 -- Under H10's criterion the Boruta seed fails (c) under every classifier, and (b) under LightGBM

| classifier | (a) vs Boruta alone | (b) vs stock FASTENER, 100% | (c) 10% | (c) 25% |
|---|---|---|---|---|
| LightGBM (verdict) | 31-0-8, +0.037, **p < 0.0001** | 22-0-17, +0.003, lower bound -0.008 | 25-0-14, +0.004, p = 0.24 | 25-0-14, +0.003, p = 0.24 |
| random forest | 33-0-6, +0.052, **p < 0.0001** | 24-0-15, +0.009, **lower bound +0.002** | 25-0-14, +0.008, p = 0.11 | 26-0-13, +0.009, **p = 0.030** |
| decision tree | 23-0-16, +0.015, **p = 0.020** | 21-0-18, +0.009, **lower bound +0.003** | 25-0-14, +0.000, p = 0.79 | 21-0-18, +0.003, p = 0.79 |

*Wins-ties-losses over 39 datasets, mean AUF (K = 10) difference, p (Holm over the two checkpoints in (c)); from each H10 report's `tables/criterion.csv`.*

Read as registered for H10, H11 is not supported: (c) fails under all three
classifiers. Under LightGBM, (b)'s interval is widened by OliveOil, where
the Boruta seed is 0.175 behind stock FASTENER; without it the mean
difference is +0.007 (H10-E01, F1).

![F1](../H10-E01/figures/F1_H10_criterion.png)

*H10-E01 (LightGBM): each seeded arm minus its filter (a), minus stock FASTENER at 100% (b) and at 10% and 25% (c), one point per dataset; filled = holds. The same figure for the forest and the tree: [H10-E02](../H10-E02/figures/F1_H10_criterion.png), [H10-E03](../H10-E03/figures/F1_H10_criterion.png).*

### F2 -- Read without (c), the Boruta seed is better than Boruta and no worse than stock FASTENER under two classifiers of three

(a) and (b) together, H10's claim without the early lead, hold under the
forest and the tree and fail under LightGBM. At the end of the budget the
Boruta seed is ahead of stock FASTENER on average under all three
(+0.003, +0.009, +0.009), but not as good as the per-dataset better of
Boruta and stock FASTENER (16-0-23, 20-0-19, 12-0-27; each H10 report's
SUPPORT section 5). This reading is descriptive: it drops a part of the
registered criterion after the results were seen.

![F2](../H10-E02/figures/F2_auf_by_checkpoint.png)

*H10-E02 (random forest): mean test AUF of stock FASTENER and the two seeded arms at 10-100% of the budget, filters alone dotted. LightGBM and tree: [H10-E01](../H10-E01/figures/F2_auf_by_checkpoint.png), [H10-E03](../H10-E03/figures/F2_auf_by_checkpoint.png).*

### F3 -- The seed's cost depends on the classifier: 30% of the arm's wall clock under LightGBM, 3% under the forest, 39% under the tree

Boruta charges at most 99 fits to a run's budget, but its time is its own:
43.4 h of 143.6 h under LightGBM, 3.3 h of 106.9 h under the forest, and 7.4
h of 19.1 h under the tree (single core). Any use of the Boruta seed has to
count that time.

![F3](../H10-E01/figures/F4_seed_cost.png)

*H10-E01 (LightGBM): seed and search wall clock per dataset, median over seeds. Forest and tree: [H10-E02](../H10-E02/figures/F4_seed_cost.png), [H10-E03](../H10-E03/figures/F4_seed_cost.png).*

## 3. Assessment

**H11 is not supported, post hoc.** Judged by H10's registered criterion,
the Boruta seed fails under every classifier, on the early lead (c), and
under LightGBM also on non-inferiority (b) (F1). That the Boruta seed did
better than the mRMR seed does not make it meet H10's claim.

**What can be said.** On these runs, starting FASTENER from Boruta's ranking
is reliably better than Boruta alone and, under the forest and the tree, no
worse than stock FASTENER (F2), at a time cost that ranges from negligible
to a third of the run (F3). None of this is confirmed: the hypothesis was
formed from these numbers, and any reading of them is biased towards it.

**Limits.** Those of H10-E01 to -E03 (one split per dataset, the smallest
test splits 8-12 rows, five seeds, budgets calibrated for stock FASTENER),
and the post-hoc status above.

**What follows.** The PI's choice: a confirmatory test on runs not yet
seen -- H9's new datasets, or new seeds on these -- registered before they
run, with the seed's time cost in the criterion; or leave H11 as an
exploratory note.
