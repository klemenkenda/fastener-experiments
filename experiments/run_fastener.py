"""Run FASTENER's genetic search under the shared protocol.

Two deliberate departures from the reference `main()` in fastener.py:

1. The evaluator scores on the VALIDATION split, not the test split. The
   reference scores on the test globals, which would let the search fit the very
   set we report on.

2. The model factory is wrapped in a counter, so the search cost (number of
   model fits) is measured rather than assumed.

FASTENER's Config hardcodes an output path of "log/<output_folder>" relative to
the process working directory and refuses to reuse a directory, so we chdir into
the run directory for the duration of the search and restore afterwards.
"""
import contextlib
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _bootstrap  # noqa: F401,E402  puts ../fastener on sys.path

from fastener import Config, EntropyOptimizer  # noqa: E402
from item import (  # noqa: E402
    IntersectionMatingWithWeightedRandomInformationGain,
    RandomEveryoneWithEveryone,
    RandomFlipMutationStrategy,
    Result,
)

from protocol import evaluate_subset, make_model, primary_score  # noqa: E402


@contextlib.contextmanager
def working_dir(path: Path):
    prev = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev)


class ValidationEvaluator:
    """Scores a trained model on the VALIDATION split.

    Defined at module level (not as a closure) because FASTENER pickles the whole
    optimizer in prepare_loop(), and local functions are not picklable.

    Signature is fixed by FASTENER: (model, genes, shuffle_indices) -> Result.
    `shuffle_indices` index into the SELECTED columns and drive FASTENER's
    permutation-importance pruning step.
    """

    def __init__(self, X_val: np.ndarray, y_val: np.ndarray) -> None:
        self.X_val = X_val
        self.y_val = y_val

    def __call__(self, model, genes, shuffle_indices: Optional[List[int]] = None) -> Result:
        data = self.X_val[:, genes]
        if shuffle_indices:
            data = data.copy()
            for j in shuffle_indices:
                # Permute one column to measure that feature's contribution.
                np.random.shuffle(data[:, j])
        return Result(primary_score(self.y_val, model.predict(data)))


class CountingModelFactory:
    """Model factory that counts how many models the search fits."""

    def __init__(self) -> None:
        self.fits = 0

    def __call__(self):
        self.fits += 1
        return make_model()


def run_fastener(ds, run_dir: Path, seed: int, rounds: int,
                 pool_size: int = 3, max_bucket_size: int = 3,
                 reset_to_pareto_rounds: int = 5,
                 initial_genes: Optional[List[List[int]]] = None,
                 quiet: bool = True) -> Dict:
    """One FASTENER search. Returns the Pareto front re-scored under the protocol."""
    factory = CountingModelFactory()

    mating = RandomEveryoneWithEveryone(
        pool_size=pool_size,
        mating_strategy=IntersectionMatingWithWeightedRandomInformationGain(),
    )
    mutation = RandomFlipMutationStrategy(1.0 / ds.n_features)

    if initial_genes is None:
        # Start from single features rather than the reference's fixed [[0]], so
        # the search is not anchored on one arbitrary feature.
        rng = np.random.RandomState(seed)
        initial_genes = [[int(i)] for i in rng.choice(ds.n_features, size=5, replace=False)]

    t0 = time.time()
    with working_dir(run_dir):
        # Config.__post_init__ seeds random_utils and prefixes "log/".
        config = Config(
            output_folder=f"fastener_seed{seed}",
            random_seed=seed,
            number_of_rounds=rounds,
            max_bucket_size=max_bucket_size,
            reset_to_pareto_rounds=reset_to_pareto_rounds,
        )
        optimizer = EntropyOptimizer(
            factory, ds.X_train, ds.y_train,
            ValidationEvaluator(ds.X_val, ds.y_val),
            ds.n_features, mating, mutation,
            initial_genes=initial_genes,
            config=config,
        )
        if quiet:
            with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(devnull):
                optimizer.mainloop()
        else:
            optimizer.mainloop()
    search_seconds = time.time() - t0

    search_fits = factory.fits

    # Re-score every front member through the shared protocol so FASTENER's
    # numbers are produced by exactly the same code path as the baselines'.
    records = []
    for size, item in sorted(optimizer.pareto_front.items()):
        feats = np.where(item.genes)[0]
        if feats.size == 0:
            continue
        rec = evaluate_subset(ds, feats, counter=None)
        rec["method"] = "fastener"
        rec["seed"] = seed
        rec["fastener_internal_val_score"] = float(item.result.score)
        rec["generation_found"] = int(item.generation)
        records.append(rec)

    return {
        "method": "fastener",
        "family": "genetic",
        "seed": seed,
        "params": {
            "rounds": rounds,
            "pool_size": pool_size,
            "max_bucket_size": max_bucket_size,
            "reset_to_pareto_rounds": reset_to_pareto_rounds,
            "mutation_prob": 1.0 / ds.n_features,
            "initial_genes": initial_genes,
            "mating": "IntersectionMatingWithWeightedRandomInformationGain",
        },
        "search_seconds": round(search_seconds, 2),
        "model_fits": search_fits,
        "unique_subsets_cached": len(optimizer.cache_data),
        "log_dir": str((run_dir / "log" / f"fastener_seed{seed}").resolve()),
        "records": records,
    }
