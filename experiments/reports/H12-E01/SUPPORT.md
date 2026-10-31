# H12-E01 -- Support

## Record

| | |
|---|---|
| experiment | `H12-E01` (H12) |
| run | `20261031T053237Z_h12e01_probes` (status ok, evidence true) |
| method ID | `h12_probes@343635e+047e1fb#5582` |
| pre-registration commit | `343635e` (H12, the H12-E01 design, DEC-54, `h12_probes.py`), pushed before the run |
| truth | `h12_probes.py truth`, from commit `343635e`, started right after the run; deterministic, outside a `provenance.Run` (no manifest of its own) |
| machine | the workstation (sentinel), Windows 11, Python 3.11 (`fastener-exp`) |
| calls | 1,396 sent, 8 replayed, 0 failed pairs; $3.80 (cap $10) |
| wall time | probes 24 min 19 s (05:32:37-05:56:56 UTC); truth in parallel, ending before the probes |
| outputs (committed) | `h12/calls.jsonl` (every request and full response), `h12/probes/<dataset>__<model>.json` (192), `h12/truth/<dataset>.json` (16) |
| tables | `tables/probes.csv` (one row per dataset and model), `tables/criterion.csv` (per model, the registered criterion), `tables/readings.csv` (unplanned readings: mutual information, identified vs not) |

## Hypothesis and criterion, as registered (HYPOTHESES.md, H12, commit `343635e`)

> **Claim.** Large language models recognise the H8 datasets and know which of
> their features are relevant, as knowledge of *the dataset*, not only of the
> physical or domain phenomenon its features describe: (A) given a dataset's
> name, a model reproduces its features; (B) given only the name and the
> features' positions in the original column order -- no feature names -- its
> relevance scores agree with the relevance measured on the data, more than the
> same prompt with a fictitious name; and (C, the strict form) given the
> feature names, adding the dataset's name lets it track the measured relevance
> beyond what it predicts from the names alone.

> **Falsification criterion.** Per model, the unit is the dataset (16).
> (A) P2 recalls at least half of the dataset's variables (one-to-one name
> match after normalisation, difflib ratio >= 0.85) on at least 8 datasets.
> (B) Per dataset, d = rho(P3, truth) - rho(P3f, truth) (Spearman; a flat score
> counts as rho 0); more datasets positive than negative and a two-sided
> Wilcoxon p < 0.05 after Holm over the twelve models.
> (C) Per dataset, the partial Spearman correlation of P4 with the truth,
> controlling for P5; the same test as B.
> H12 holds for a model if A and B hold. **H12 is supported if it holds for at
> least 7 of the 12 models**, and is called **dataset-specific** if C holds as
> well for at least 7. Otherwise not supported; reversed if B's effect is
> significantly negative for at least 7 models.

Mechanical reading: A holds for 4 models, B for 0, C for 0. H12 holds for
0 of 12, so H12 is **not supported**. It is not reversed: no model has a
significantly negative B.

## Setup

**Probes** (`h12_probes.py`; system prompts `SCORE_SYSTEM`, `IDENTIFY_SYSTEM`, `SCHEMA_SYSTEM`):

| probe | the model is shown | it returns |
|---|---|---|
| P1a | rows (before the cap), feature count, class names | the dataset's name and source |
| P1b | the feature names, in order | the dataset's name and source |
| P2 | the dataset's name and source (`IDENTITY[...]["name"]`) | its features, in order, as named in the distributed file |
| P3 | the name, the feature count, the left-out columns; features as bare indices 0..p-1 | a score 0-1 per index |
| P3f | `FAKE_NAME` ("'Brenner field survey 2019' (an internal, unpublished data set)") and the feature count | a score 0-1 per index |
| P4 | the name, the class names, the features with their names | a score 0-1 per feature |
| P5 | the class names, the features with their names | a score 0-1 per feature |

Twelve models (OpenRouter IDs in `h12_probes.MODELS`), temperature 0, seed
20200, max 16,000 output tokens (phi-4 8,000). The score probes run in chunks
of 300, with one retry for a chunk missing over 20% of its features. A
feature the model leaves out gets the lowest score the model gave. All 192
(dataset, model) pairs ran in parallel, 16 at a time.

**Variables.** The original columns. adult's 63 one-hot columns are 13
variables and diabetes130's 132 are 43. Elsewhere one column is one
variable (har 561, eodata 182, crop_mapping 174, ...).

**Truth** (`h12/truth/`). LightGBM with the protocol's settings (100 trees,
`min_child_samples` from the training size, 8 threads), fitted once on the
training split with the 50,000-row cap and the protocol split. Permutation
importance is the drop in validation weighted F1 when a variable's columns
are permuted together, the mean of five permutations (seeds 2020-2024).
Mutual information is computed on the training split: `fast_mi` for single
columns, a discrete estimate on the category code for one-hot groups, the
mean over seeds 2020-2024.

| dataset | variables | LightGBM val. weighted F1 | MI across seeds, min rho | rho(perm. imp., MI) | variables with perm. imp. > 0 |
|---|---:|---:|---:|---:|---:|
| adult | 13 | 0.870 | 0.95 | 0.64 | 12 |
| covertype | 54 | 0.831 | 0.90 | 0.74 | 48 |
| crop_mapping | 174 | 0.994 | 1.00 | 0.15 | 111 |
| diabetes130 | 43 | 0.547 | 0.50 | 0.47 | 19 |
| eodata | 182 | 0.734 | 1.00 | 0.43 | 151 |
| eye_movements | 20 | 0.620 | 0.80 | 0.19 | 17 |
| gas_drift | 128 | 0.996 | 1.00 | 0.19 | 74 |
| har | 561 | 0.988 | 1.00 | 0.04 | 105 |
| heloc | 22 | 0.721 | 0.81 | 0.38 | 13 |
| higgs | 28 | 0.710 | 0.70 | 0.44 | 22 |
| mice_protein | 77 | 0.981 | 1.00 | 0.46 | 28 |
| ozone_8hr | 72 | 0.937 | 0.86 | -0.29 | 37 |
| pc4 | 37 | 0.900 | 0.81 | 0.32 | 25 |
| phishing | 30 | 0.962 | 0.61 | 0.72 | 28 |
| qsar_biodeg | 41 | 0.846 | 0.86 | 0.08 | 15 |
| spambase | 57 | 0.952 | 0.94 | 0.73 | 46 |

## Deviations

None from the registered design. Three execution points:

- **Retries that repeated the request.** When a chunk's reply left out
  every feature, the retry asked for the same features, so it was the
  identical request and was answered from the call log rather than sent
  again. This happened 8 times: DeepSeek V4 Flash P3 on diabetes130, har and
  pc4; Gemini 2.5 Flash-Lite P3f on eye_movements, ozone_8hr, phishing and
  qsar_biodeg; Qwen3 14B P5 on spambase. These scores are flat, which counts
  as rho 0, as registered. The same happens in H8's prior code
  (`LLMFeaturePrior`).
- **Empty replies.** 11 in all: DeepSeek V4 Flash 9 (P1a 3, P1b 1, P2 2,
  P3 3) and Qwen3 14B 2 (P2, P5). Each one spent the whole output budget on
  reasoning; the 16,000 output tokens include that reasoning. Each is scored
  as registered: not identified, recall 0, or flat.
- **The truth outside a run manifest.** It was computed by the committed
  code at `343635e` and saved with its inputs' summaries. A rerun
  reproduces it.

## What happened

- 2026-10-31, before registration: a pilot on spambase and adult with Gemma
  3 27B and DeepSeek V4 Flash (`20261031T051842Z_h12_pilot`, $0.01, not
  evidence; output in the session scratchpad, not kept). It checked the
  prompts and the parsing, and its output was seen (DEC-54).
- 05:32:37 UTC: the probes started from `343635e`, widest datasets first.
  At about the same time the truth computation started.
- 05:56:56 UTC: the probes ended. All 192 pairs were done, with no failed
  pair. $3.80 was spent.
- The truth computation ended before the probes did.
- After the run, a reading of the P2 replies found the generic-header
  answers (REPORT.md F2). The grading was not changed. The adjusted count
  is reported beside the registered one only:

| model | A as registered | A with generic headers counted where the file has them |
|---|---:|---:|
| Opus 5.5 | 12 | 15 |
| Sonnet 5.5 | 11 | 15 |
| Haiku 5.5 | 10 | 11 |
| others | unchanged | unchanged |

- The permutation-importance truth is weak on har, crop_mapping and
  gas_drift (validation F1 0.99; rho with MI 0.04-0.19). This was seen when
  the truth finished, before scoring, and nothing was changed.

## Evidence

Per model, from `tables/criterion.csv` (permutation importance) and
`tables/readings.csv` (mutual information, unplanned):

| model | card id. | names id. | recall median | A | B + / - | B Holm p | C + / - | C Holm p | layout median | B (MI) Holm p |
|---|---:|---:|---:|---:|---|---:|---|---:|---:|---:|
| Opus 5.5 | 15 | 15 | 1.00 | 12 | 12-4 | 0.075 | 12-4 | 0.235 | 0.94 | 0.005 |
| Sonnet 5.5 | 16 | 15 | 1.00 | 11 | 10-6 | 0.837 | 13-3 | 0.186 | 0.81 | 0.008 |
| Haiku 5.5 | 13 | 13 | 0.95 | 10 | 12-4 | 0.443 | 10-6 | 1.000 | 0.18 | 0.164 |
| Llama 3.3 70B | 9 | 6 | 0.07 | 3 | 3-0 | 0.837 | 12-3 | 0.548 | 0.00 | 1.000 |
| Gemma 3 4B | 5 | 2 | 0.00 | 0 | 7-2 | 1.000 | 7-9 | 1.000 | 0.00 | 1.000 |
| Gemma 3 27B | 7 | 5 | 0.00 | 1 | 9-3 | 1.000 | 7-9 | 1.000 | -0.00 | 1.000 |
| Ministral 8B | 7 | 8 | 0.01 | 3 | 8-8 | 1.000 | 9-7 | 1.000 | 0.03 | 1.000 |
| Qwen3 14B | 8 | 6 | 0.00 | 2 | 9-4 | 1.000 | 10-6 | 1.000 | 0.01 | 1.000 |
| Phi-4 | 9 | 6 | 0.00 | 6 | 8-5 | 1.000 | 8-8 | 1.000 | 0.00 | 1.000 |
| DeepSeek V4 Flash | 13 | 8 | 0.00 | 7 | 5-2 | 1.000 | 8-8 | 1.000 | 0.00 | 1.000 |
| GPT-6 Luna | 13 | 10 | 0.95 | 11 | 11-2 | 0.175 | 6-10 | 1.000 | 0.28 | 0.107 |
| Gemini 2.5 Flash-Lite | 9 | 7 | 0.00 | 5 | 5-2 | 0.567 | 11-4 | 0.409 | 0.00 | 1.000 |

The per-dataset values are in `tables/probes.csv` and in the cells of F1, F2,
F3 and F5.

## Reproduce

```
python experiments/h12_probes.py truth                       # h12/truth/
python experiments/h12_probes.py probe --out <empty dir>     # not evidence: replays every call from h12/calls.jsonl
python experiments/h12_probes.py score                       # tables/probes.csv, criterion.csv
python experiments/h12_report.py                             # figures/, tables/readings.csv
```

`score` and `h12_report.py` read only the committed files in `h12/`, so they
reproduce every table and figure without the network.
