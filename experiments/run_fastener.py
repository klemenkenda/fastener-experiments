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
import collections
import contextlib
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _bootstrap  # noqa: F401,E402  puts ../fastener on sys.path

from fastener import Config, EntropyOptimizer, FitBudgetExhausted  # noqa: E402
from item import (  # noqa: E402
    InformationGainSwapStrategy,
    Item,
    IntersectionMatingWithWeightedRandomInformationGain,
    RandomEveryoneWithEveryone,
    RandomFlipMutationStrategy,
    RandomSwapStrategy,
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
    """Model factory that counts how many models the search fits.

    `build` makes the classifier: the protocol tree by default, or the ELM
    (`paper_protocol.ELMClassifier`, H4-E02). Both are module-level, so the
    factory pickles with the optimizer.
    """

    def __init__(self, build=None) -> None:
        self.fits = 0
        self.build = build or make_model

    def __call__(self):
        self.fits += 1
        return self.build()


# The classifiers a FASTENER search can be driven by. "tree" is the protocol's
# and the default everywhere; "elm" is the FASTENER paper's FS-SDS classifier.
def search_model_factory(model: str):
    if model == "tree":
        return make_model
    if model == "elm":
        from paper_protocol import ELMClassifier
        return ELMClassifier
    raise ValueError(f"unknown search model {model!r}; have 'tree', 'elm'")


def model_nbytes(model) -> int:
    """About how much memory a fitted model holds: its trees' nodes and
    values for a tree or a forest, its booster's text for LightGBM (no
    `estimators_`, and arrays of its own count for nothing -- so without this
    the store would keep every LightGBM model), its arrays otherwise (the
    ELM)."""
    booster = getattr(model, "booster_", None)
    if booster is not None:
        return len(booster.model_to_string())
    trees = getattr(model, "estimators_", None)
    if trees is None and hasattr(model, "tree_"):
        trees = [model]
    if trees is not None:
        # sklearn's Node struct is 64 bytes; `value` holds the class counts.
        return int(sum(t.tree_.node_count * 64 + t.tree_.value.nbytes
                       for t in trees))
    return int(sum(v.nbytes for v in vars(model).values()
                   if isinstance(v, np.ndarray)))


def default_model_cache_mb() -> float:
    """How much memory a search may keep fitted models in.

    FASTENER_MODEL_CACHE_MB if set; inside a SLURM job 40% of its memory
    (SLURM_MEM_PER_NODE, in MB), leaving the rest to the data and the search;
    4 GB otherwise.
    """
    if os.environ.get("FASTENER_MODEL_CACHE_MB"):
        return float(os.environ["FASTENER_MODEL_CACHE_MB"])
    if os.environ.get("SLURM_MEM_PER_NODE"):
        return 0.4 * float(os.environ["SLURM_MEM_PER_NODE"])
    return 4096.0


class _Refit:
    """A model that is fitted again only when it is first used.

    Stands in for a model the store no longer holds. Most look-ups of a
    scored subset want only its score (Item.evaluate); only pruning predicts
    with the model, and only then is it refitted.
    """

    def __init__(self, optimizer, number, genes):
        self._opt, self._number, self._genes = optimizer, number, genes
        self._model = None

    def __getattr__(self, name):
        if self._model is None:
            self._model = self._opt._refit(self._number, self._genes)
        return getattr(self._model, name)


class TrackedOptimizer(EntropyOptimizer):
    """EntropyOptimizer that records the best score after every generation.

    Defined here, not in the upstream `fastener/` clone, so the published
    algorithm's code is unchanged: this only reads the front after each round.
    Iteration 0 is the front built from the initial genes, before round 1.

    The snapshot is taken in a `finally`, so the round the fit budget cuts short
    is recorded too. At that point the front may still hold entries the
    interrupted round had not yet pruned; the trajectory keeps only the best
    score per size and recomputes the Pareto front itself, so they do no harm.
    """

    trajectory = None
    # Called with the cumulative fit count after every generation, so a live
    # progress display can see how far a run is. Kept out of the pickled state.
    progress_cb = None
    # A CPU-time budget (H4): the search stops before the first fit after this
    # many seconds of process CPU time since `cpu_t0`. None: no time limit.
    max_cpu_seconds = None
    cpu_t0 = 0.0
    cpu_budget_hit = False
    # Fitted models kept for reuse, at most this many MB in all (None: no
    # limit). Upstream's cache keeps every fitted model with its score: a few
    # MB per run with the tree, but 53 MB per forest on ElectricDevices and
    # 440 MB on EOData, so H5H6-E02's FASTENER jobs ran into their 8 GB and
    # crawled (2026-10-27). Scores are still all kept; a model the store has
    # let go is refitted when pruning needs it. The protocol's models have a
    # fixed seed, so the refit is the same model, and it is not charged to
    # the fit budget: fits, fronts and scores are exactly as before.
    model_cache_bytes = None
    model_refits = 0

    def _store(self):
        if "_models" not in self.__dict__:
            self._models = collections.OrderedDict()
            self._model_bytes = 0
        return self._models

    def _keep(self, number, model) -> None:
        """Keep a model; past the limit, let go of the oldest -- first those
        not on the Pareto front, whose models pruning will not ask for."""
        models = self._store()
        size = model_nbytes(model)
        models[number] = (model, size)
        self._model_bytes += size
        cap = self.model_cache_bytes
        if cap is None or self._model_bytes <= cap:
            return
        front = {item.number for item in self.pareto_front.values()}
        for keep_front in (True, False):
            for key in list(models):
                if self._model_bytes <= cap:
                    return
                if key == number or (key in front) == keep_front:
                    continue
                self._model_bytes -= models.pop(key)[1]

    def _refit(self, number, genes):
        """The model of an already scored subset, fitted again: not a new
        evaluation, so not charged to the budget or the factory's count."""
        build = getattr(self._model, "build", self._model)
        model = build().fit(self.train_data[:, genes], self.train_target)
        self.model_refits += 1
        self._keep(number, model)
        return model

    def cached_fitness(self, genes):
        number = Item.to_number(genes)
        self.cache_counter[number] += 1
        hit = self.cache_data.get(number)
        if hit is None:
            result, model = self._fitness_function(genes)
            # The score is cached for good; the model goes to the store.
            self.cache_data[number] = (result, None)
            self._keep(number, model)
            return result, model
        entry = self._store().get(number)
        if entry is not None:
            self._models.move_to_end(number)
            return hit[0], entry[0]
        return hit[0], _Refit(self, number, genes.copy())

    def _fitness_function(self, genes):
        # Checked where every fit is charged, as the fit budget is, so a run
        # stops within one fit of its time budget rather than one generation.
        if self.max_cpu_seconds is not None and \
                time.process_time() - self.cpu_t0 >= self.max_cpu_seconds:
            self.cpu_budget_hit = True
            raise FitBudgetExhausted(
                f"CPU budget of {self.max_cpu_seconds} s is spent")
        return super()._fitness_function(genes)

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("progress_cb", None)
        # The kept models are a cache, refitted on demand: not part of the
        # state, and gigabytes of it under the forest.
        state.pop("_models", None)
        state.pop("_model_bytes", None)
        return state

    def _snapshot(self, iteration: int) -> None:
        for item in self.pareto_front.values():
            if getattr(item, "result", None) is not None:
                self.trajectory.observe(np.where(item.genes)[0],
                                        item.result.score)
        self.trajectory.step(iteration, self.model_fits,
                             prune_stats=dict(self.prune_stats),
                             front_from_swap=self.front_from_swap())
        if self.progress_cb is not None:
            self.progress_cb(self.model_fits)

    def run_round(self, round_n: int) -> None:
        if self.trajectory is None:
            return super().run_round(round_n)
        if round_n == 1:
            self._snapshot(0)
        try:
            super().run_round(round_n)
        finally:
            self._snapshot(round_n)


# The three arms of the swap experiment. "none" is the published algorithm and
# the default everywhere, so an existing call site keeps running exactly what it
# ran before.
SWAP_ARMS = {
    "none": None,
    "random": RandomSwapStrategy,
    "guided": InformationGainSwapStrategy,
}


# The mating step's behaviour (HYPOTHESES.md, H0). "fixed" is the clone's
# current default. "2020" sets the two flags the clone's README gives for
# reproducing the original code exactly -- the same fits and the same Pareto
# front for the same seed: the weighted information-gain mating always adds the
# top genes, and the mating pool is drawn with replacement, so an item can be
# mated with itself.
MATING_VERSIONS = {
    "fixed": {"include_top_genes": True, "allow_self_mating": False},
    "2020": {"include_top_genes": True, "allow_self_mating": True},
}


def make_mating(version: str, pool_size: int) -> RandomEveryoneWithEveryone:
    """The mating-selection strategy for a mating version."""
    if version not in MATING_VERSIONS:
        raise ValueError(f"unknown mating version {version!r}; expected one "
                         f"of {sorted(MATING_VERSIONS)}")
    flags = MATING_VERSIONS[version]
    return RandomEveryoneWithEveryone(
        pool_size=pool_size,
        allow_self_mating=flags["allow_self_mating"],
        mating_strategy=IntersectionMatingWithWeightedRandomInformationGain(
            include_top_genes=flags["include_top_genes"]),
    )


def make_swap_strategy(swap: Optional[str], number_of_swaps: int = 1):
    """Build the pruning-swap operator for an arm name, or None for the original."""
    if swap is None or swap == "none":
        return None
    if swap not in SWAP_ARMS:
        raise ValueError(f"unknown swap arm {swap!r}; expected one of {sorted(SWAP_ARMS)}")
    return SWAP_ARMS[swap](number_of_swaps=number_of_swaps)


def run_fastener(ds, run_dir: Path, seed: int, rounds: int,
                 pool_size: int = 3, max_bucket_size: int = 3,
                 reset_to_pareto_rounds: int = 5,
                 initial_genes: Optional[List[List[int]]] = None,
                 quiet: bool = True,
                 swap: Optional[str] = None,
                 number_of_swaps: int = 1,
                 max_fits: Optional[int] = None,
                 dump_logs: bool = True,
                 method_name: Optional[str] = None,
                 trajectory=None,
                 mating: str = "fixed",
                 progress_cb=None,
                 max_cpu_seconds: Optional[float] = None,
                 model: str = "tree",
                 model_cache_mb: Optional[float] = None) -> Dict:
    """One FASTENER search. Returns the Pareto front re-scored under the protocol.

    `swap` selects the pruning operator and defaults to the original algorithm:

    * ``None`` / ``"none"`` -- pruning only tests deleting the weakest feature.
    * ``"random"``          -- also tests replacing a random selected feature
                               with a uniformly random unselected one.
    * ``"guided"``          -- also tests replacing the permutation-weakest
                               feature with one sampled by mutual information.

    Each swap candidate costs one extra model fit per pruned subset, which
    `model_fits` in the returned dict accounts for.

    `dump_logs` controls FASTENER's own per-generation pickles. They hold the
    whole population plus the fitness cache -- megabytes per generation on a
    wide data set -- and nothing here reads them, so a batch of hundreds of runs
    passes False. The default preserves the reference behaviour.

    `max_fits` caps the number of unique subsets fitted and stops the search
    there, whatever `rounds` says. Comparing arms is only meaningful under a
    fit cap: the swap arms buy extra fits per generation, so at equal rounds
    they would simply have been given more compute. With a cap, set `rounds`
    high enough that the budget is what actually stops the run -- `stopped_on`
    in the result says which of the two did.

    `trajectory` (a `trajectory.Trajectory`) records the best score after every
    generation. It is created by the caller, who knows the run's k grid.

    `mating` is ``"fixed"`` (the clone's default) or ``"2020"``, the original
    mating behaviour the published results were produced with (H0). The 2020
    version without a swap is labelled ``fastener_2020``.

    `max_cpu_seconds` stops the search on process CPU time instead of, or as
    well as, fits (H4: equal compute between methods). Whichever limit is
    reached first stops it; `stopped_on` says which. A time-stopped run is not
    reproducible fit for fit, since where it stops depends on the machine;
    rerunning with `max_fits` set to its `model_fits` replays it exactly.

    `model` is the classifier that drives the search and scores the final
    front: "tree" (the protocol's) or "elm" (H4-E02). A non-tree model is
    appended to the method label, e.g. ``fastener_elm``.
    """
    build = search_model_factory(model)
    factory = CountingModelFactory(build)

    mating_version = mating
    mating = make_mating(mating_version, pool_size)
    mutation = RandomFlipMutationStrategy(1.0 / ds.n_features)
    swap_strategy = make_swap_strategy(swap, number_of_swaps)
    method = method_name or ("fastener" if swap_strategy is None
                             else f"fastener_swap_{swap}")
    if method_name is None and mating_version != "fixed":
        method += f"_{mating_version}"
    if method_name is None and model != "tree":
        method += f"_{model}"

    if initial_genes is None:
        # Start from single features rather than the reference's fixed [[0]], so
        # the search is not anchored on one arbitrary feature.
        rng = np.random.RandomState(seed)
        initial_genes = [[int(i)] for i in rng.choice(ds.n_features, size=5, replace=False)]

    t0 = time.time()
    with working_dir(run_dir):
        # Config.__post_init__ seeds random_utils and prefixes "log/".
        config = Config(
            output_folder=f"{method}_seed{seed}",
            random_seed=seed,
            number_of_rounds=rounds,
            max_bucket_size=max_bucket_size,
            reset_to_pareto_rounds=reset_to_pareto_rounds,
            max_model_fits=max_fits,
            dump_generation_logs=dump_logs,
        )
        optimizer = TrackedOptimizer(
            factory, ds.X_train, ds.y_train,
            ValidationEvaluator(ds.X_val, ds.y_val),
            ds.n_features, mating, mutation,
            initial_genes=initial_genes,
            config=config,
            swap_strategy=swap_strategy,
        )
        optimizer.trajectory = trajectory
        optimizer.progress_cb = progress_cb
        optimizer.max_cpu_seconds = max_cpu_seconds
        cache_mb = (default_model_cache_mb() if model_cache_mb is None
                    else model_cache_mb)
        optimizer.model_cache_bytes = int(cache_mb * 1e6)
        cpu0 = optimizer.cpu_t0 = time.process_time()
        if quiet:
            with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(devnull):
                optimizer.mainloop()
        else:
            optimizer.mainloop()
    search_seconds = time.time() - t0
    search_cpu_seconds = time.process_time() - cpu0
    stopped_on = ("cpu_budget" if optimizer.cpu_budget_hit
                  else optimizer.stop_reason)

    search_fits = factory.fits

    # Re-score every front member through the shared protocol so FASTENER's
    # numbers are produced by exactly the same code path as the baselines'.
    records = []
    for size, item in sorted(optimizer.pareto_front.items()):
        feats = np.where(item.genes)[0]
        if feats.size == 0:
            continue
        rec = evaluate_subset(ds, feats, counter=None, model_factory=build)
        rec["method"] = method
        rec["seed"] = seed
        rec["fastener_internal_val_score"] = float(item.result.score)
        rec["generation_found"] = int(item.generation)
        rec["from_swap"] = item.number in optimizer.swap_made
        records.append(rec)

    return {
        "method": method,
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
            "mating_version": mating_version,
            **MATING_VERSIONS[mating_version],
            "swap": swap or "none",
            "number_of_swaps": number_of_swaps if swap_strategy is not None else 0,
            "max_fits": max_fits,
            "max_cpu_seconds": max_cpu_seconds,
            "search_model": model,
        },
        "search_seconds": round(search_seconds, 2),
        # Process CPU time of the search: the unit of an equal-compute budget.
        "search_cpu_seconds": round(search_cpu_seconds, 2),
        "model_fits": search_fits,
        # Which limit ended the run: "fit_budget" or "rounds". An arm comparison
        # where some arms stopped on "rounds" was not run at equal budget.
        "stopped_on": stopped_on,
        "rounds_completed": optimizer.rounds_completed,
        "unique_subsets_cached": len(optimizer.cache_data),
        # Models refitted because the bounded store had let them go: extra
        # compute, not extra evaluations (TrackedOptimizer.model_cache_bytes).
        "model_refits": optimizer.model_refits,
        "model_cache_mb": cache_mb,
        # What pruning did over the run (cumulative), and how many entries of
        # the final front a swap put there. Zero swaps on the stock arm.
        "prune_stats": dict(optimizer.prune_stats),
        "front_from_swap": optimizer.front_from_swap(),
        "log_dir": str((run_dir / "log" / f"{method}_seed{seed}").resolve()),
        "records": records,
    }
