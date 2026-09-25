# Why this replication differs from the FASTENER paper

Investigation of the gap between `run_paper_replication.py` and Table 3 of
Koprivec, Kenda & Šircelj, *Entropy* 2020, 22(11), 1198.

Every test below re-grades the subsets each replication unit stored. None of it
re-runs a search, so the searches are held fixed and only the measurement
changes.

## The gap

Across the data sets finished so far, under the replication's own settings
(decision tree, weighted F1):

| method | mean AUF vs paper | above paper on | rank correlation |
|---|---|---|---|
| FASTENER | **+0.099** | 11/11 | 0.71 |
| FS-SDS | **+0.242** | 10/10 | 0.79 |

A uniform positive offset with a high rank correlation is the signature of a
measurement difference, not of a different search: the replication orders the
data sets by difficulty much as the paper does, it just scores everything
higher. The two offsets turn out to have **different causes**.

## FASTENER: a grading artefact, and it reconciles

Searching the protocol choices Section 5.1 leaves open
(`reverse_engineer_protocol.py`):

| classifier | F1 average | mean Δ | mean \|Δ\| |
|---|---|---|---|
| tree, `min_samples_leaf=2` | binary | +0.026 | **0.045** |
| tree, default | binary | +0.037 | 0.050 |
| tree, default | weighted *(replication default)* | +0.110 | 0.110 |

Both ingredients are genuine ambiguities in the paper:

* *"a requirement of keeping, at a minimum, two examples in a split"*.
  `min_samples_split=2` is scikit-learn's **default**, which would make the
  sentence say nothing; `min_samples_leaf=2` is **not** the default and
  regularises every tree. The second reading is the one that makes the sentence
  informative, and it is the one that matches the numbers.
* *"the F1 score"*, with no average named. Binary is the least generous on a
  two-class problem.

Under both readings FASTENER's column essentially reconciles (residual +0.026).
**FASTENER is replicated.**

## FS-SDS: not a grading artefact

No grading configuration explains FS-SDS. Best of all nine combinations:
mean |Δ| **0.194**. The most paper-faithful reconstruction available — the
search *driven* by the ELM and the subsets *graded* by the ELM, which is what
Section 5.1 describes — is **0.221** off. Two further hypotheses were tested and
rejected:

**Rejected: the noisy objective.** The authors' reference implementation
re-splits the data on every evaluation, so the same subset has no fixed score.
Reproducing that faithfully (`run_fs_sds(use_cache=False)` with a fresh 80:20
split per call) changes nothing systematic:

| data set | deterministic | re-split each eval | paper |
|---|---|---|---|
| colon | 0.870 | 0.926 | 0.658 |
| ALLAML | 0.945 | 0.943 | 0.643 |
| GLIOMA | 0.797 | 0.735 | 0.549 |

Mean Δ +0.254 against +0.251. The hypothesis was plausible and is wrong.

**Rejected: unscaled ELM inputs.** An ELM on raw gene-expression columns
saturates its sigmoids. Removing the standardisation moves the mean gap from
+0.24 to +0.179 but inconsistently (+0.05 on GLIOMA, +0.33 on leukemia). Not the
cause.

## FS-SDS: the cause is AUF coverage at small k

AUF is `(1/K)·Σ_{k=1..K} opt(k)` with `opt(k) = max{score : |subset| ≤ k}` and
K = 20. **A k at which a method offers no subset contributes zero.** So a front
that starts at k = 8 forfeits 7/20 of the measure before any classifier runs.

Restricting our FS-SDS fronts to subsets of size ≥ t reproduces the paper's
column closely, at a consistent threshold:

| data set | t=1 | t=5 | t=6 | t=8 | t=10 | paper | best t |
|---|---|---|---|---|---|---|---|
| ALLAML | 0.952 | 0.764 | 0.721 | **0.615** | 0.515 | 0.643 | 8 |
| BASEHOCK | 0.810 | 0.673 | 0.637 | **0.553** | 0.451 | 0.580 | 8 |
| CLL_SUB_111 | 0.767 | 0.638 | 0.611 | **0.521** | 0.435 | 0.537 | 8 |
| COIL20 | 0.863 | 0.735 | **0.693** | 0.603 | 0.512 | 0.655 | 6 |
| GLIOMA | 0.821 | 0.677 | 0.636 | **0.538** | 0.474 | 0.549 | 8 |
| GLI_85 | 0.878 | 0.692 | **0.640** | 0.561 | 0.467 | 0.659 | 6 |
| arcene | 0.830 | 0.683 | **0.617** | 0.541 | 0.458 | 0.608 | 6 |
| colon | 0.876 | 0.685 | **0.641** | 0.549 | 0.449 | 0.658 | 6 |
| leukemia | 0.969 | 0.774 | 0.733 | **0.608** | 0.518 | 0.620 | 8 |
| lung | 0.888 | 0.740 | **0.675** | 0.594 | 0.502 | 0.663 | 6 |
| lung_discrete | 0.778 | 0.649 | 0.622 | **0.548** | 0.422 | 0.533 | 8 |
| lymphoma | 0.843 | 0.690 | 0.646 | **0.557** | 0.476 | 0.539 | 8 |
| Isolet | 0.579 | 0.521 | 0.496 | 0.439 | **0.379** | 0.365 | 10 |
| nci9 | 0.563 | 0.453 | 0.420 | 0.377 | **0.306** | 0.331 | 10 |

Median best threshold **8**, range 6–10, over 14 data sets. The same analysis on
FASTENER gives a median threshold of 1–3: its fronts already reach k = 1, so it
needs no such correction.

This is consistent with what the paper says about the method. FS-SDS fixes the
subset size for a whole run, so a curve over k costs one run per k — and the
paper notes FS-SDS is *"rigid when selecting the feature subset size"* and that
*"changing (FS-SDS) subset size is computationally expensive"* (Section 5.4). At
30,000 evaluations per k, covering k = 1…20 would have cost 600,000 evaluations
per data set per split. Covering only the larger sizes is the natural economy,
and the AUF then charges zeros for every small k not covered.

## Conclusion

Two different things were happening.

1. **FASTENER's +0.10 is measurement.** Two unstated choices — the tree's
   `min_samples_leaf` and the F1 average — account for it, and under the
   readings that make the paper's own sentences informative, the column
   reconciles to +0.026. The paper's FASTENER results replicate.

2. **FS-SDS's +0.24 is coverage, not search quality.** The published FS-SDS
   column is depressed by AUF zeros at small k, which follow from a budget
   decision the paper explains, not from the SDS search being weak. Given full
   k = 1…20 coverage at a fifth of the paper's per-k budget, FS-SDS scores far
   higher — and beats FASTENER on every data set under ~200 rows.

**What this means for the paper's headline claim.** "FASTENER outperforms FS-SDS
on 24 of 25" holds under the paper's own measurement, but a large part of the
margin is the coverage asymmetry rather than a difference in the subsets found.
A like-for-like comparison — both methods covering the same k range — is much
closer, and on small-sample data sets it reverses. That is a statement about the
AUF metric applied to a fixed-k method, and it does not touch FASTENER's
efficiency claim, which replicated cleanly: FASTENER produces its whole front in
~12,000 evaluations where FS-SDS needs a run per k.

## Reproducing this

```bash
python experiments/reverse_engineer_protocol.py   # the grading search
python experiments/diagnose_gap.py                # the candidate walk-through
python experiments/report_replication.py          # the tables and comparison
```
