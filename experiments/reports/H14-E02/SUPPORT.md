# H14-E02 -- supporting record

The record behind [REPORT.md](REPORT.md).

## 1. Header

| field | content |
|---|---|
| Experiment ID | `H14-E02` |
| Hypothesis ID | H14 (pilot for P2) |
| Run IDs | the 200 in the ledger row (`h14e02_<dataset>_<arm>_s<seed>`), each with `status: ok`, `evidence: true` |
| Algorithm IDs | `<arm>@75e638d+047e1fb#<config>`; two config hashes per arm, because the config holds the fit budget (Strawberry 6,000, the other three 12,000; x3 and x10 for the sweep arms) |
| Pre-registration | H14: `experiments/HYPOTHESES.md` at `1152a8e`; H14-E02's design at `40bdb6d` (DEC-58) |
| Code commits | every run at experiments `75e638d`, FASTENER `047e1fb`, `code_dirty: false` |
| Dates | runs 2026-11-02T17:37:49 to 2026-11-02T21:46:37 UTC (4 h 9 min); report 2026-11-02 |
| Verdict | **not supported**: (i) for neither start, (ii) (ii-b fails), (iii) (`tables/verdict.json`) |

## 2. Hypothesis

Quoted verbatim from `experiments/HYPOTHESES.md` at `1152a8e`:

> ## H14 -- Pilot for P2: a start over all sizes keeps reach without its cost; OBL's lack of reach is not only budget; forced mutation cuts the repeats
>
> *(2026-11-02; proposed by the PI for paper P2 after H13-E01 was reported.
> A **pilot** on development datasets whose earlier results have been read
> (H5H6-E01 to -E03, H13-E01): its verdicts guide P2's design and are not a
> confirmation. New seeds, so no run's outcome has been seen; see
> [DEC-56](DECISIONS.md#dec-56).)*
>
> **Claim.** In plain NSGA-II with the NSGAII-MIIP port's operators: (i) a
> start whose subset sizes cover 1..d keeps the reach of the 1-30 start and
> recovers its large-end cost (H13-E01, F4); (ii) the OBL start's lack of
> reach at d >= 150 shrinks with budget but does not vanish at 10x; (iii) a
> mutation that always changes at least one feature cuts the repeats of
> small-subset populations (H13-E01, F7) and raises their AUF at small k.
>
> **Why it might hold.** H13-E01: reach carries the AUF gap, the OBL start
> needs selection to walk from d/2 to k <= 10, and the 1-30 start re-proposes
> subsets because balanced mutation flips about 2k/d bits per child.
>
> **Why it might not.** (i) A wide start dilutes the small sizes: the uniform
> start puts only 10/d of its mass at k <= 10. (ii) Selection may close the gap
> at 3x already. (iii) Repeats may come from crossover between near-identical
> parents, not from mutation; then the forced flip changes only the cost.
>
> **Arms.** Plain NSGA-II (`sota_baselines.run_nsga2`), population 100, with
> separate random streams for the start and the operators (arms that differ
> only in mutation start from the same population, checked by its hash), and
> every scored subset logged (`subset_log.py`). Controls, not the ported
> algorithm:
>
> | arm | start | mutation | budget |
> |---|---|---|---|
> | `p2_obl` | OBL, as `nsga2` | balanced, rate 1/d | 1x |
> | `p2_sparse` | 1-30, as `nsga2_sparse` | balanced | 1x |
> | `p2_uniform` | k ~ U{1..d}, then k features (`uniform_initialization`) | balanced | 1x |
> | `p2_loguniform` | P(k) proportional to 1/k on 1..d (`loguniform_initialization`) | balanced | 1x |
> | `p2_<start>_min1` | each of the four | balanced, then one forced flip in a child it left unchanged (`balanced_mutation_min1`: remove or add with probability 1/2, so zero expected drift; add only at k <= 1, remove only at k = d) | 1x |
> | `p2_obl_b3`, `p2_obl_b10` | OBL | balanced | 3x, 10x |
>
> **Criterion.** Four datasets cannot carry a test over datasets (the smallest
> two-sided Wilcoxon p at n = 4 is 0.125), so each part is read per seed, as
> H1: a comparison holds on a dataset if it holds in at least 4 of 5 seeds, and
> a part holds if it holds on at least 3 of the 4 datasets.
>
> * (i) For each of `p2_uniform` and `p2_loguniform` against `p2_sparse`:
>   (i-a) every seed's final front holds a subset of at most 10 features;
>   (i-b) best test F1 at any size (the front's validation-best subset) at
>   least `p2_sparse`'s; (i-c) AUF (K = 10) no more than 0.01 below
>   `p2_sparse`'s. Supported for a start if (i-a), (i-b) and (i-c) hold.
> * (ii) `p2_obl`, `p2_obl_b3`, `p2_obl_b10`: (ii-a) on every dataset, the
>   share of seeds whose final front reaches k <= 10 does not fall as the
>   budget grows; (ii-b) at 10x it is below 1 on at least one of Earthquakes
>   and Computers. Supported if both hold.
> * (iii) For `p2_sparse` and `p2_loguniform`, `_min1` against balanced:
>   (iii-a) the run's repeat share (cache hits / proposals, from the subset
>   log) at most half of balanced's; (iii-b) AUF (K = 10) higher. Supported if
>   (iii-a) and (iii-b) hold for both starts. The two dense starts are
>   reported beside it.
>
> Seeds are paired by number: the same seed gives `_min1` and balanced the
> same start, and (i) and (ii) compare arms run with the same seed.
>
> **Reported beside it:** time to reach k <= 10 (archive, Kaplan-Meier, as
> H13-E01 Q7) and the OBL fits-to-reach in multiples of the 1x budget;
> stagnation stops; flip histograms and repeat shares against 2k/d; AUF at
> K = 20 and K = d; matched-size differences (H13's definition); wall clock
> beside fits. The analysis is H13-E01's code where it applies.

## 3. Evaluation criteria and design

The criterion is in the hypothesis above. H14-E01's design, which H14-E02 repeats, and H14-E02's own entry,
verbatim from `experiments/EXPERIMENTS.md` at `40bdb6d`:

> ### `H14-E01` -- H14: P2's pilot, starts over all sizes, an OBL budget sweep and forced mutation, on four datasets
>
> Registered 2026-11-02, after H13-E01 was reported and before any of this
> experiment's runs ([DEC-56](DECISIONS.md#dec-56)).
>
> **Design.**
>
> | | |
> |---|---|
> | arms | H14's ten: `p2_obl`, `p2_sparse`, `p2_uniform`, `p2_loguniform`, each also `_min1`, and `p2_obl_b3`, `p2_obl_b10` (`run_sota.P2_SEARCHES`) |
> | datasets | Adiac (d 176, 156 test rows), Strawberry (235, 196), Earthquakes (512, 93), Computers (720, 100): H13-E01's transition band, all with at least 90 test rows (H13-E01's matched-size failure came from test sets of 8 and 11 rows) |
> | classifier | the protocol decision tree, one thread per numeric library (DEC-37), as H1-E02 and H5H6-E01 |
> | seeds | 2025-2029, new |
> | budget | each dataset's H2/H3 fit budget ([`h2h3_budgets.json`](h2h3_budgets.json)): Adiac, Earthquakes and Computers 12,000, Strawberry 6,000; `p2_obl_b3` and `p2_obl_b10` at 3x and 10x |
> | stop | DEC-41's stagnation stop (50 generations with no new subset) on every arm, the sweep included; 6-hour per-run cap, a timed-out run reported as censored |
> | runs | 10 arms x 4 datasets x 5 seeds = 200 |
> | logging | per run, `subsets/<arm>_seed<s>.npz` (`subset_log.py`): every newly scored subset (generation, packed bitset, size, validation score, fit seconds) and, per generation, proposals, empty children, cache hits, children equal to a member of the population, children mutation left unchanged, forced flips and the flip histogram (0, 1, 2, 3+); the archive trajectory as before |
> | where | Sentinel (16 logical cores, 256 GB), `run_queue.py`, 10 processes at once, as H5H6-E01, so its fit times carry over |
> | criterion | as registered in HYPOTHESES.md, H14 |
> | expected cost | from H5H6-E01's seconds per fit on these datasets under this tree: about 19 CPU-hours for the 160 runs at 1x and 25 for the 40 sweep runs, so about 5 hours of wall clock (3.5-6 h); the longest run about 1.6 h (Computers at 10x); about 300 MB of subset logs before compression |
>
> **Already seen.** The end-of-budget results of `nsga2`, `nsga2_sparse` and
> `nsgaii_miip` on these four datasets (seeds 2020-2024; H5H6-E01 to -E03,
> H13-E01). One unregistered test job, run `20261102T171310Z_h14test` (dirty
> tree, not evidence): `p2_uniform_min1` at 600 fits and `p2_obl_b3` at 1,800
> on Strawberry with seed 2025; its printed output showed AUF (K = 10) 0.835
> and 0.000 and best test F1 0.903 and 0.944. Those runs are not part of this
> experiment (other budgets).
>
> **How it runs.**
>
> ```
> python experiments/run_queue.py --experiment H14-E01 \
>     --datasets Computers,Adiac,Earthquakes,Strawberry \
>     --methods p2_obl_b10,p2_obl_b3,p2_obl,p2_obl_min1,p2_uniform,p2_uniform_min1,p2_sparse,p2_sparse_min1,p2_loguniform,p2_loguniform_min1 \
>     --seeds 2025,2026,2027,2028,2029 --budgets experiments/h2h3_budgets.json \
>     --max-procs 10 --timeout-hours 6
> ```

> ### `H14-E02` -- H14: P2's pilot, rerun of the stopped H14-E01
>
> Registered 2026-11-02, after H14-E01 was stopped and before any of this
> experiment's runs ([DEC-58](DECISIONS.md#dec-58)).
>
> **Design.** H14-E01's design, unchanged: the ten `p2_*` arms, Adiac,
> Strawberry, Earthquakes and Computers, the decision tree, seeds 2025-2029,
> the H2/H3 fit budgets (3x and 10x for the sweep), the stagnation stop on
> every arm, the 6-hour cap, the logging, Sentinel with 10 processes, and
> H14's criterion. Every run starts from the commit that registers this
> design; nothing is committed while the queue runs.
>
> **Changed since H14-E01.** Nothing H14 runs or reads. DEC-57 is a rule
> for H13 alone; all four datasets here have more than 50 test rows (93-196).
>
> **Already seen.** As H14-E01: the four datasets' earlier NSGA-II results
> (seeds 2020-2024) and the unregistered test job `20261102T171310Z_h14test`.
> H14-E01's ten stopped runs were never scored and nothing of them was read.
>
> **How it runs.**
>
> ```
> python experiments/run_queue.py --experiment H14-E02 \
>     --datasets Computers,Adiac,Earthquakes,Strawberry \
>     --methods p2_obl_b10,p2_obl_b3,p2_obl,p2_obl_min1,p2_uniform,p2_uniform_min1,p2_sparse,p2_sparse_min1,p2_loguniform,p2_loguniform_min1 \
>     --seeds 2025,2026,2027,2028,2029 --budgets experiments/h2h3_budgets.json \
>     --max-procs 10 --timeout-hours 6
> ```
>
> **Expected cost.** As H14-E01: about 45 CPU-hours, about 5 hours of wall
> clock (3.5-6 h).

## 4. Description of the experiment

**Setup.** As registered. The arms, in plain words: plain NSGA-II with the NSGAII-MIIP port's tournament,
crossover and balanced mutation (rate 1/d), population 100, started from OBL (50 random bit strings and
their complements), from 1-30 random features, from a size drawn uniformly from 1..d, or from a size drawn
with probability proportional to 1/k; each with balanced mutation or with `min1` (balanced mutation, then
one forced add-or-remove in a child it left unchanged); and OBL at 3x and 10x the budget. Start and
operators draw from separate random streams (`numpy.random.SeedSequence(seed).spawn(2)`), so a seed fixes
the start population for every arm with that start. Every newly scored subset is logged
(`subset_log.py`), and `h14_report.py` reduces the logs to `tables/subset_summary.csv`.

**Deviations from the protocol.** None in the runs. The analysis script was changed after the runs, in
presentation only: the experiment ID became an argument (H14-E02 as default), F2 shows one trajectory with
the 1x and 3x cut points instead of three overlapping curves, F3's legend moved, F5 (cost) and
`tables/pairs.csv` (per-pair differences, which the prose quotes) were added. The criterion code is as
committed in `c83a2de`, before any H14 run.

**Reading (i-a).** H14 says "every seed's final front holds a subset of at most 10 features" under a
per-seed rule of 4 of 5. Both new starts reached in 5 of 5 seeds on every dataset, so the two readings agree.

**What happened.**

* One queue on Sentinel, 10 processes, costliest first: 17:37:49 to 21:46:37 UTC, 4 h 9 min,
  inside the registered 3.5-6 h. 200 of 200 jobs finished (`ok`), none failed or timed out.
* Every run at `75e638d` + FASTENER `047e1fb` with `code_dirty: false`. 199 manifests flag the whole tree
  `dirty`: the ledger, which each finished run updates, counts there; it is not code.
* No run spent more than its budget. Runs that ended on the stagnation stop: `p2_sparse` 4, `p2_loguniform`
  3, `p2_obl_b10` 3 (all on Strawberry, after reaching), `p2_obl_b3` 1; every other run spent its budget.
* All 80 balanced/min1 pairs started from the same population (`tables/start_check.csv`).
* The sweep arms `p2_obl`, `_b3`, `_b10` share seeds and streams: in all 20 dataset-and-seed pairs the 1x
  run's trajectory is the start of the 10x run's. The three budget arms are one trajectory per seed read
  at three points.
* No run lost reach: every run whose archive held a subset of at most 10 features ended with one on its
  front.
* Empty children: 2.4 million of the balanced 1-30 start's 33.8 million proposals had no feature.
  `run_nsga2` gives an empty subset the worst score without a fit, as in every earlier run of this code.
  With min1 there were 934.
* Before the queue, the unregistered test job `20261102T171310Z_h14test` (Strawberry, seed 2025, other
  budgets) and H14-E01's ten stopped runs; neither is part of this evidence.

## 5. Evidence

**Criterion, per dataset** (`tables/criterion.csv`; seeds holding out of 5, a part holds on >= 3 of 4):

| part | a | b | dataset | n_seeds | seeds_holding | holds |
|---|---|---|---|---|---|---|
| i-a | p2_uniform | nan | Adiac | 5.0000 | 5.0000 | True |
| i-a | p2_uniform | nan | Strawberry | 5.0000 | 5.0000 | True |
| i-a | p2_uniform | nan | Earthquakes | 5.0000 | 5.0000 | True |
| i-a | p2_uniform | nan | Computers | 5.0000 | 5.0000 | True |
| i-b | p2_uniform | p2_sparse | Adiac | 5.0000 | 1.0000 | False |
| i-b | p2_uniform | p2_sparse | Strawberry | 5.0000 | 2.0000 | False |
| i-b | p2_uniform | p2_sparse | Earthquakes | 5.0000 | 2.0000 | False |
| i-b | p2_uniform | p2_sparse | Computers | 5.0000 | 2.0000 | False |
| i-c | p2_uniform | p2_sparse | Adiac | 5.0000 | 3.0000 | False |
| i-c | p2_uniform | p2_sparse | Strawberry | 5.0000 | 4.0000 | True |
| i-c | p2_uniform | p2_sparse | Earthquakes | 5.0000 | 3.0000 | False |
| i-c | p2_uniform | p2_sparse | Computers | 5.0000 | 3.0000 | False |
| i-a | p2_loguniform | nan | Adiac | 5.0000 | 5.0000 | True |
| i-a | p2_loguniform | nan | Strawberry | 5.0000 | 5.0000 | True |
| i-a | p2_loguniform | nan | Earthquakes | 5.0000 | 5.0000 | True |
| i-a | p2_loguniform | nan | Computers | 5.0000 | 5.0000 | True |
| i-b | p2_loguniform | p2_sparse | Adiac | 5.0000 | 1.0000 | False |
| i-b | p2_loguniform | p2_sparse | Strawberry | 5.0000 | 3.0000 | False |
| i-b | p2_loguniform | p2_sparse | Earthquakes | 5.0000 | 3.0000 | False |
| i-b | p2_loguniform | p2_sparse | Computers | 5.0000 | 1.0000 | False |
| i-c | p2_loguniform | p2_sparse | Adiac | 5.0000 | 3.0000 | False |
| i-c | p2_loguniform | p2_sparse | Strawberry | 5.0000 | 3.0000 | False |
| i-c | p2_loguniform | p2_sparse | Earthquakes | 5.0000 | 4.0000 | True |
| i-c | p2_loguniform | p2_sparse | Computers | 5.0000 | 1.0000 | False |
| iii-a | p2_sparse_min1 | p2_sparse | Adiac | 5.0000 | 0.0000 | False |
| iii-a | p2_sparse_min1 | p2_sparse | Strawberry | 5.0000 | 0.0000 | False |
| iii-a | p2_sparse_min1 | p2_sparse | Earthquakes | 5.0000 | 0.0000 | False |
| iii-a | p2_sparse_min1 | p2_sparse | Computers | 5.0000 | 0.0000 | False |
| iii-b | p2_sparse_min1 | p2_sparse | Adiac | 5.0000 | 1.0000 | False |
| iii-b | p2_sparse_min1 | p2_sparse | Strawberry | 5.0000 | 2.0000 | False |
| iii-b | p2_sparse_min1 | p2_sparse | Earthquakes | 5.0000 | 3.0000 | False |
| iii-b | p2_sparse_min1 | p2_sparse | Computers | 5.0000 | 2.0000 | False |
| iii-a | p2_loguniform_min1 | p2_loguniform | Adiac | 5.0000 | 0.0000 | False |
| iii-a | p2_loguniform_min1 | p2_loguniform | Strawberry | 5.0000 | 0.0000 | False |
| iii-a | p2_loguniform_min1 | p2_loguniform | Earthquakes | 5.0000 | 0.0000 | False |
| iii-a | p2_loguniform_min1 | p2_loguniform | Computers | 5.0000 | 0.0000 | False |
| iii-b | p2_loguniform_min1 | p2_loguniform | Adiac | 5.0000 | 3.0000 | False |
| iii-b | p2_loguniform_min1 | p2_loguniform | Strawberry | 5.0000 | 3.0000 | False |
| iii-b | p2_loguniform_min1 | p2_loguniform | Earthquakes | 5.0000 | 2.0000 | False |
| iii-b | p2_loguniform_min1 | p2_loguniform | Computers | 5.0000 | 1.0000 | False |
| beside iii-b | p2_obl_min1 | p2_obl | Adiac | 5.0000 | 3.0000 | False |
| beside iii-b | p2_obl_min1 | p2_obl | Strawberry | 5.0000 | 2.0000 | False |
| beside iii-b | p2_obl_min1 | p2_obl | Earthquakes | 5.0000 | 0.0000 | False |
| beside iii-b | p2_obl_min1 | p2_obl | Computers | 5.0000 | 0.0000 | False |
| beside iii-b | p2_uniform_min1 | p2_uniform | Adiac | 5.0000 | 3.0000 | False |
| beside iii-b | p2_uniform_min1 | p2_uniform | Strawberry | 5.0000 | 3.0000 | False |
| beside iii-b | p2_uniform_min1 | p2_uniform | Earthquakes | 5.0000 | 4.0000 | True |
| beside iii-b | p2_uniform_min1 | p2_uniform | Computers | 5.0000 | 2.0000 | False |

| part | a | dataset | holds | R_p2_obl | R_p2_obl_b3 | R_p2_obl_b10 | R_10x_Earthquakes | R_10x_Computers |
|---|---|---|---|---|---|---|---|---|
| ii-a | p2_obl..b10 | Adiac | True | 1.00 | 1.00 | 1.00 |  |  |
| ii-a | p2_obl..b10 | Strawberry | True | 0.20 | 1.00 | 1.00 |  |  |
| ii-a | p2_obl..b10 | Earthquakes | True | 0.00 | 0.00 | 1.00 |  |  |
| ii-a | p2_obl..b10 | Computers | True | 0.00 | 0.00 | 1.00 |  |  |
| ii-b | p2_obl_b10 | Earthquakes,Computers | False |  |  |  | 1.00 | 1.00 |

Mechanical reading: {"(i) p2_uniform": {"i-a": true, "i-b": false, "i-c": false, "supported": false}, "(i) p2_loguniform": {"i-a": true, "i-b": false, "i-c": false, "supported": false}, "(ii)": {"ii-a": true, "ii-b": false, "supported": false}, "(iii) p2_sparse": {"iii-a": false, "iii-b": false}, "(iii) p2_loguniform": {"iii-a": false, "iii-b": false}, "(iii)": {"supported": false}, "n_runs": 200}

**Per arm and dataset** (`tables/per_arm.csv`; means over 5 seeds, `max_front` and `fits` medians, repeat
and unchanged shares medians from the subset logs):

| dataset | method | R | auf_k10 | auf_k10_min | auf_k10_max | best_f1 | max_front | fits | stagnation | seconds_median | median_base_budgets_to_reach | repeat_share | unchanged_share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adiac | p2_loguniform | 1.0000 | 0.3903 | 0.3862 | 0.3948 | 0.4510 | 9.0000 | 12000.0000 | 0 | 287.5500 | 0.0083 | 0.9442 | 0.9567 |
| Computers | p2_loguniform | 1.0000 | 0.5541 | 0.5148 | 0.5752 | 0.5603 | 5.0000 | 9652.0000 | 3 | 1209.4700 | 0.0083 | 0.9395 | 0.9928 |
| Earthquakes | p2_loguniform | 1.0000 | 0.6760 | 0.6561 | 0.6916 | 0.7022 | 8.0000 | 12000.0000 | 0 | 545.1300 | 0.0083 | 0.9590 | 0.9859 |
| Strawberry | p2_loguniform | 1.0000 | 0.8947 | 0.8538 | 0.9166 | 0.9227 | 6.0000 | 6000.0000 | 0 | 155.5900 | 0.0167 | 0.9172 | 0.9742 |
| Adiac | p2_loguniform_min1 | 1.0000 | 0.3907 | 0.3694 | 0.4056 | 0.4521 | 8.0000 | 12000.0000 | 0 | 121.4900 | 0.0083 | 0.7934 | 0.9682 |
| Computers | p2_loguniform_min1 | 1.0000 | 0.5418 | 0.5113 | 0.5952 | 0.5549 | 5.0000 | 12000.0000 | 0 | 57.4200 | 0.0083 | 0.7025 | 0.9941 |
| Earthquakes | p2_loguniform_min1 | 1.0000 | 0.6824 | 0.6479 | 0.7366 | 0.7160 | 9.0000 | 12000.0000 | 0 | 49.6700 | 0.0083 | 0.6685 | 0.9891 |
| Strawberry | p2_loguniform_min1 | 1.0000 | 0.8991 | 0.8864 | 0.9107 | 0.9369 | 6.0000 | 6000.0000 | 0 | 34.5500 | 0.0167 | 0.6607 | 0.9764 |
| Adiac | p2_obl | 1.0000 | 0.3803 | 0.3215 | 0.4247 | 0.4771 | 26.0000 | 12000.0000 | 0 | 345.1200 | 0.5445 | 0.7926 | 0.8526 |
| Computers | p2_obl | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.6011 | 269.0000 | 12000.0000 | 0 | 633.1200 |  | 0.1868 | 0.4803 |
| Earthquakes | p2_obl | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.6860 | 165.0000 | 12000.0000 | 0 | 307.7400 |  | 0.1888 | 0.5213 |
| Strawberry | p2_obl | 0.2000 | 0.1808 | 0.0000 | 0.9038 | 0.9398 | 34.0000 | 6000.0000 | 0 | 138.3300 | 0.9120 | 0.1503 | 0.5884 |
| Adiac | p2_obl_b10 | 1.0000 | 0.3981 | 0.3842 | 0.4049 | 0.4981 | 18.0000 | 120000.0000 | 0 | 3630.1800 | 0.5445 | 0.9439 | 0.9298 |
| Computers | p2_obl_b10 | 1.0000 | 0.5788 | 0.5458 | 0.6436 | 0.5931 | 20.0000 | 120000.0000 | 0 | 4019.4700 | 7.1033 | 0.8994 | 0.9362 |
| Earthquakes | p2_obl_b10 | 1.0000 | 0.7007 | 0.6823 | 0.7126 | 0.6790 | 13.0000 | 120000.0000 | 0 | 4690.6700 | 3.9858 | 0.9471 | 0.9784 |
| Strawberry | p2_obl_b10 | 1.0000 | 0.8828 | 0.8482 | 0.8995 | 0.9262 | 6.0000 | 33531.0000 | 3 | 1479.8200 | 1.5487 | 0.9412 | 0.9741 |
| Adiac | p2_obl_b3 | 1.0000 | 0.4157 | 0.3842 | 0.4470 | 0.4920 | 18.0000 | 36000.0000 | 0 | 786.3300 | 0.5445 | 0.9044 | 0.9206 |
| Computers | p2_obl_b3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.5683 | 253.0000 | 36000.0000 | 0 | 1734.1000 |  | 0.3690 | 0.5169 |
| Earthquakes | p2_obl_b3 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.6823 | 124.0000 | 36000.0000 | 0 | 737.4300 |  | 0.4202 | 0.6185 |
| Strawberry | p2_obl_b3 | 1.0000 | 0.8113 | 0.4661 | 0.9066 | 0.9458 | 9.0000 | 18000.0000 | 1 | 410.6500 | 1.5487 | 0.9426 | 0.9607 |
| Adiac | p2_obl_min1 | 1.0000 | 0.3931 | 0.3842 | 0.4048 | 0.5017 | 19.0000 | 12000.0000 | 0 | 276.3400 | 0.4247 | 0.2535 | 0.8143 |
| Computers | p2_obl_min1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.6155 | 222.0000 | 12000.0000 | 0 | 560.5900 |  | 0.0002 | 0.5266 |
| Earthquakes | p2_obl_min1 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.6850 | 84.0000 | 12000.0000 | 0 | 254.1100 |  | 0.0004 | 0.5908 |
| Strawberry | p2_obl_min1 | 0.6000 | 0.2307 | 0.0000 | 0.8906 | 0.9427 | 37.0000 | 6000.0000 | 0 | 124.1300 | 0.9990 | 0.0010 | 0.6245 |
| Adiac | p2_sparse | 1.0000 | 0.4012 | 0.3853 | 0.4208 | 0.4625 | 10.0000 | 12000.0000 | 1 | 290.2600 | 0.0083 | 0.9466 | 0.9538 |
| Computers | p2_sparse | 1.0000 | 0.5612 | 0.5158 | 0.6035 | 0.5842 | 6.0000 | 12000.0000 | 1 | 906.6000 | 0.0083 | 0.9436 | 0.9920 |
| Earthquakes | p2_sparse | 1.0000 | 0.6732 | 0.6532 | 0.7004 | 0.6868 | 7.0000 | 12000.0000 | 1 | 847.4700 | 0.0083 | 0.9355 | 0.9891 |
| Strawberry | p2_sparse | 1.0000 | 0.8871 | 0.8717 | 0.9087 | 0.9225 | 6.0000 | 6000.0000 | 1 | 215.9500 | 0.0167 | 0.9122 | 0.9769 |
| Adiac | p2_sparse_min1 | 1.0000 | 0.3968 | 0.3734 | 0.4207 | 0.4554 | 12.0000 | 12000.0000 | 0 | 105.5900 | 0.0083 | 0.7131 | 0.9656 |
| Computers | p2_sparse_min1 | 1.0000 | 0.5444 | 0.5198 | 0.5686 | 0.5589 | 6.0000 | 12000.0000 | 0 | 53.5500 | 0.0083 | 0.7642 | 0.9956 |
| Earthquakes | p2_sparse_min1 | 1.0000 | 0.6846 | 0.6304 | 0.7231 | 0.6975 | 5.0000 | 12000.0000 | 0 | 52.2400 | 0.0083 | 0.7832 | 0.9928 |
| Strawberry | p2_sparse_min1 | 1.0000 | 0.8859 | 0.8712 | 0.9031 | 0.9197 | 6.0000 | 6000.0000 | 0 | 28.2900 | 0.0167 | 0.6261 | 0.9791 |
| Adiac | p2_uniform | 1.0000 | 0.3972 | 0.3704 | 0.4206 | 0.4429 | 11.0000 | 12000.0000 | 0 | 220.1400 | 0.0083 | 0.9353 | 0.9425 |
| Computers | p2_uniform | 1.0000 | 0.5428 | 0.5093 | 0.5794 | 0.5432 | 8.0000 | 12000.0000 | 0 | 747.5500 | 0.0083 | 0.9469 | 0.9897 |
| Earthquakes | p2_uniform | 1.0000 | 0.6923 | 0.6529 | 0.7301 | 0.6951 | 13.0000 | 12000.0000 | 0 | 313.8300 | 0.0083 | 0.9594 | 0.9811 |
| Strawberry | p2_uniform | 1.0000 | 0.8904 | 0.8696 | 0.9017 | 0.9199 | 8.0000 | 6000.0000 | 0 | 131.3100 | 0.0167 | 0.9270 | 0.9689 |
| Adiac | p2_uniform_min1 | 1.0000 | 0.4054 | 0.3888 | 0.4257 | 0.4992 | 9.0000 | 12000.0000 | 0 | 269.6500 | 0.0083 | 0.7572 | 0.9646 |
| Computers | p2_uniform_min1 | 1.0000 | 0.5423 | 0.5330 | 0.5504 | 0.5553 | 5.0000 | 12000.0000 | 0 | 86.6800 | 0.0083 | 0.7881 | 0.9913 |
| Earthquakes | p2_uniform_min1 | 1.0000 | 0.7090 | 0.6851 | 0.7516 | 0.7195 | 5.0000 | 12000.0000 | 0 | 71.3500 | 0.0083 | 0.5623 | 0.9751 |
| Strawberry | p2_uniform_min1 | 1.0000 | 0.8969 | 0.8887 | 0.9087 | 0.9337 | 7.0000 | 6000.0000 | 0 | 40.2700 | 0.0167 | 0.5476 | 0.9596 |

Per-pair differences paired by seed: `tables/pairs.csv`; subset-log totals per run:
`tables/subset_summary.csv`; matched-size differences against the 1-30 start: `tables/matched.csv`; per run:
`tables/run_measures.csv`.

Figures: F1 starts, F2 OBL budget sweep, F3 min1, F4 flips against 2k/d, F5 min1's cost.

## 6. Reproduction

From a clean checkout at `75e638d` (runs) and the commit that adds this report (analysis):

```
python experiments/run_queue.py --experiment H14-E02 \
    --datasets Computers,Adiac,Earthquakes,Strawberry \
    --methods p2_obl_b10,p2_obl_b3,p2_obl,p2_obl_min1,p2_uniform,p2_uniform_min1,p2_sparse,p2_sparse_min1,p2_loguniform,p2_loguniform_min1 \
    --seeds 2025,2026,2027,2028,2029 --budgets experiments/h2h3_budgets.json \
    --max-procs 10 --timeout-hours 6
python experiments/distill_results.py
python experiments/h14_report.py        # -> experiments/reports/H14-E02/{tables,figures}
```

The subset logs stay in `results/<run>/subsets/` (not committed); `tables/subset_summary.csv` holds what
the report reads from them, and `h14_report.py` uses it when the logs are not on disk.
