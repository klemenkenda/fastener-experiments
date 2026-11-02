# Papers

Each potential paper of the [publication plan](PUBLICATION-PLAN.md) (v1.3, in Slovenian) has its own public repository. Only this index and the plan live here; the paper repositories are cloned into `papers/P<n> - <title>/`, which this repository ignores.

| paper | title | evidence | repository |
|---|---|---|---|
| P1 | Budget Choice in Comparing Feature Selectors | H4 | [fastener-p1-budget-fairness](https://github.com/klemenkenda/fastener-p1-budget-fairness) |
| P2 | Cardinality Coverage in Evolutionary Feature Selection | H1 + a possible new pilot | [fastener-p2-cardinality-coverage](https://github.com/klemenkenda/fastener-p2-cardinality-coverage) |
| P3 | A Broad Comparative Study of Feature Selectors | H5-H7 and H9 | [fastener-p3-selector-benchmark](https://github.com/klemenkenda/fastener-p3-selector-benchmark) |
| P4 | Mechanisms and Limits of LLM-Guided Evolutionary Search | H8-E01 to -E03 | [fastener-p4-llm-guided-search](https://github.com/klemenkenda/fastener-p4-llm-guided-search) |
| P5 | What LLMs Know About Benchmark Datasets | H12-E01 | [fastener-p5-llm-dataset-knowledge](https://github.com/klemenkenda/fastener-p5-llm-dataset-knowledge) |
| P6 | Seeding FASTENER with mRMR and Boruta | H10-E01 to -E03 + H11-E01 | [fastener-p6-filter-seeding](https://github.com/klemenkenda/fastener-p6-filter-seeding) |
| P7 | When Fixed-Size Feature Swaps Pay Off | H2/H3 | [fastener-p7-feature-swap](https://github.com/klemenkenda/fastener-p7-feature-swap) |
| P8 | FASTENER as an Open-Source Research Package | software | [fastener-p8-software](https://github.com/klemenkenda/fastener-p8-software) |
| P9 | A Curated Dataset of Feature-Selection Experiments | experimental data | [fastener-p9-experiment-data](https://github.com/klemenkenda/fastener-p9-experiment-data) |
| P10 | Guiding FASTENER with an LLM and a Knowledge Graph | a new line of work | [fastener-p10-llm-knowledge-graph](https://github.com/klemenkenda/fastener-p10-llm-knowledge-graph) |

P2 holds the preparatory assessment of H1; the others are placeholders. To get them all:

```powershell
cd papers
gh repo clone klemenkenda/fastener-p1-budget-fairness "P1 - Budget Choice in Comparing Feature Selectors"
gh repo clone klemenkenda/fastener-p2-cardinality-coverage "P2 - Cardinality Coverage in Evolutionary Feature Selection"
gh repo clone klemenkenda/fastener-p3-selector-benchmark "P3 - A Broad Comparative Study of Feature Selectors"
gh repo clone klemenkenda/fastener-p4-llm-guided-search "P4 - Mechanisms and Limits of LLM-Guided Evolutionary Search"
gh repo clone klemenkenda/fastener-p5-llm-dataset-knowledge "P5 - What LLMs Know About Benchmark Datasets"
gh repo clone klemenkenda/fastener-p6-filter-seeding "P6 - Seeding FASTENER with mRMR and Boruta"
gh repo clone klemenkenda/fastener-p7-feature-swap "P7 - When Fixed-Size Feature Swaps Pay Off"
gh repo clone klemenkenda/fastener-p8-software "P8 - FASTENER as an Open-Source Research Package"
gh repo clone klemenkenda/fastener-p9-experiment-data "P9 - A Curated Dataset of Feature-Selection Experiments"
gh repo clone klemenkenda/fastener-p10-llm-knowledge-graph "P10 - Guiding FASTENER with an LLM and a Knowledge Graph"
```
