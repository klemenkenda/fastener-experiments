# FASTENER experiments

Workspace for experiments on top of **FASTENER** (FeAture SelecTion ENabled by EntRopy).

This repository holds *only* the experiment code, notes and results. The FASTENER
algorithm itself is a separate, unmodified clone in `fastener/`, which this repo
ignores — so upstream stays clean and pullable while experiments live alongside it.

## Layout

```
FASTENER/
├── .git/            this repo — experiments only
├── .gitignore       ignores fastener/, data/, results/
├── README.md
├── TODO.md          the guided-feature-swap proposal and experiment plan
├── experiments/     experiment scripts
│   └── _bootstrap.py  puts fastener/ on sys.path
├── data/            inputs (ignored)
├── results/         outputs (ignored)
└── fastener/        upstream clone — SEPARATE git repo, not tracked here
```

## Setup

The `fastener/` directory is not part of this repository. Clone it if missing:

```bash
git clone https://github.com/klemenkenda/FASTENER fastener
```

Then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

`requirements.txt` covers everything except three optional baselines. The
ReliefF, Boruta and HSIC-Lasso arms in `experiments/sota_baselines.py` import
their libraries lazily, so the rest of the suite runs without them:

```bash
pip install Boruta skrebate pyHSICLasso   # only for those three arms
```

These are not yet verified against the numpy 2.x / scikit-learn 1.9 stack the
committed results were produced under — see the note in `requirements.txt`.

## Importing FASTENER

FASTENER uses flat top-level imports, so its directory must be on `sys.path`.
Import the bootstrap helper first:

```python
import _bootstrap  # noqa: F401  (adds ../fastener to sys.path)

from fastener import EvaluatorFactory, Config, random_fastener
from item import Item, Result
```

Run scripts from inside `experiments/`, or add that directory to `PYTHONPATH`.

## Working with the two repos

| Task | Where |
|---|---|
| Change experiment code, notes, results | this repo (`E:\Users\Klemen\FASTENER`) |
| Pull upstream FASTENER updates | `cd fastener && git pull` |
| Modify the algorithm itself | `fastener/` — commit and push to its own remote |

Keeping changes to the algorithm in `fastener/` and everything else here means the
upstream repo's history stays clean.
