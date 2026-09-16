"""Baseline experiment: FASTENER vs. standard feature selectors on MADELON.

Everything a run produces lands in one timestamped directory under results/,
together with a manifest recording the git commit of both repos, the package
versions, the dataset checksums, every seed, and the SHA256 of every output file.

Usage:
    python experiments/run_experiment.py                 # full run
    python experiments/run_experiment.py --quick         # small budget, for checking
    python experiments/run_experiment.py --rounds 600 --seeds 5
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analysis  # noqa: E402
import baselines  # noqa: E402
from datasets import MADELON_DIR, load_madelon  # noqa: E402
from protocol import FitCounter, MODEL_SEED  # noqa: E402
from provenance import Run  # noqa: E402
from run_fastener import run_fastener  # noqa: E402

# Feature budgets at which every method is compared. MADELON has 20 relevant
# features, so the grid is dense in that region.
K_GRID = [1, 2, 3, 5, 8, 10, 12, 15, 20, 25, 30, 50, 100, 200, 500]


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=600,
                    help="FASTENER generations per seed")
    ap.add_argument("--seeds", type=int, default=5,
                    help="number of FASTENER seeds (variability across restarts)")
    ap.add_argument("--quick", action="store_true",
                    help="tiny budget for a smoke check")
    ap.add_argument("--name", default="madelon_baseline")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    rounds = 60 if args.quick else args.rounds
    n_seeds = 2 if args.quick else args.seeds
    ks = [k for k in K_GRID if k <= 30] if args.quick else K_GRID
    seeds = [2020 + i for i in range(n_seeds)]

    ds = load_madelon()
    print(ds)

    params = {
        "dataset": "madelon",
        "fastener_rounds": rounds,
        "fastener_seeds": seeds,
        "k_grid": ks,
        "model": "DecisionTreeClassifier",
        "model_seed": MODEL_SEED,
        "primary_metric": "f1_weighted",
        "quick": args.quick,
    }

    with Run(args.name, params) as run:
        print(f"run dir: {run.dir}")
        run.record("dataset", ds.summary())
        run.record_inputs(**{
            p.name: p for p in sorted(MADELON_DIR.glob("madelon_*"))
        })

        all_results = []
        counter = FitCounter()

        # ---- baselines -------------------------------------------------
        print("\nbaselines:")
        res = baselines.run_all_features(ds, counter)
        print(f"  all_features            test_f1={res['records'][0]['test_score']:.4f}")
        all_results.append(res)

        for name in baselines.RANKERS:
            res = baselines.run_ranker(ds, name, ks, counter)
            best = max(res["records"], key=lambda r: r["val_score"])
            print(f"  {name:22s}  best test_f1={best['test_score']:.4f} "
                  f"@k={best['n_features']} ({res['elapsed_seconds']}s)")
            all_results.append(res)

        res = baselines.run_rfe(ds, [k for k in ks if k <= 100], counter)
        best = max(res["records"], key=lambda r: r["val_score"])
        print(f"  {'rfe_tree':22s}  best test_f1={best['test_score']:.4f} "
              f"@k={best['n_features']} ({res['elapsed_seconds']}s)")
        all_results.append(res)

        res = baselines.run_random(ds, ks, counter)
        best = max(res["records"], key=lambda r: r["val_score"])
        print(f"  {'random':22s}  best test_f1={best['test_score']:.4f} "
              f"@k={best['n_features']} ({res['elapsed_seconds']}s)")
        all_results.append(res)

        baseline_fits = counter.fits

        # ---- FASTENER --------------------------------------------------
        print(f"\nfastener ({rounds} rounds x {len(seeds)} seeds):")
        fastener_results = []
        for seed in seeds:
            res = run_fastener(ds, run.dir, seed=seed, rounds=rounds)
            best = max(res["records"], key=lambda r: r["val_score"])
            print(f"  seed {seed}: front={len(res['records']):2d} "
                  f"best test_f1={best['test_score']:.4f} @k={best['n_features']} "
                  f"fits={res['model_fits']} ({res['search_seconds']}s)")
            fastener_results.append(res)
            all_results.append(res)

        # ---- sanity check on which features carry signal ----------------
        print("\nprobing which features actually carry signal ...")
        probe = analysis.probe_relevant_features(ds)
        run.record("relevant_feature_probe", probe)
        print(f"  features with positive permutation importance: "
              f"{probe['n_features_with_positive_importance']} / {ds.n_features}")

        # ---- comparison --------------------------------------------------
        rows = analysis.comparison_table(all_results, ks)
        for r in rows:
            r["overlap"] = analysis.overlap_with_probe(
                r["features"], probe["top20_by_importance"]
            )["n_overlap_with_probe_top20"]

        csv_path = run.dir / "comparison.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=[
                "method", "seed", "budget_k", "n_features_used", "val_f1",
                "test_f1", "test_accuracy", "test_balanced_accuracy", "overlap",
            ], extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)

        sig = analysis.seed_significance(rows, ks)
        run.record("seed_significance", sig)
        run.write_json("seed_significance.json", sig)

        run.write_json("raw_results.json", all_results)
        run.write_json("comparison_rows.json", rows)

        plot_path = analysis.render_plot(
            rows, run.dir / "comparison.png",
            f"FASTENER vs baselines on MADELON "
            f"({ds.X_train.shape[0]} train / {ds.X_test.shape[0]} test, 500 features)",
        )

        run.record("cost", {
            "baseline_model_fits": baseline_fits,
            "fastener_model_fits_per_seed": [r["model_fits"] for r in fastener_results],
            "fastener_mean_search_seconds": round(
                float(np.mean([r["search_seconds"] for r in fastener_results])), 2),
        })

        # ---- headline ----------------------------------------------------
        print(f"\nwrote {csv_path.name}, raw_results.json, {plot_path.name}")
        summarise(rows, ks)
        summarise_significance(sig)

    print(f"\nmanifest: {run.dir / 'manifest.json'}")
    return 0


def summarise(rows, ks) -> None:
    methods = sorted({r["method"] for r in rows})
    print("\ntest weighted-F1 by feature budget (mean over seeds):")
    header = "  " + "method".ljust(20) + "".join(f"{k:>8}" for k in ks if k <= 50)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for m in methods:
        cells = []
        for k in ks:
            if k > 50:
                continue
            vals = [r["test_f1"] for r in rows if r["method"] == m and r["budget_k"] == k]
            cells.append(f"{np.mean(vals):8.3f}" if vals else " " * 8)
        print("  " + m.ljust(20) + "".join(cells))


def summarise_significance(sig) -> None:
    if not sig:
        return
    print("
fastener vs best deterministic baseline (test F1, across seeds):")
    print(f"  {'k':>4} {'mean':>7} {'sd':>7} {'baseline':>9} {'delta':>8} {'wins':>6} {'p':>7}")
    print("  " + "-" * 52)
    for r in sig:
        if r["budget_k"] > 50:
            continue
        print(f"  {r['budget_k']:>4} {r['mean_test_f1']:>7.3f} {r['sd_test_f1']:>7.3f} "
              f"{r['best_baseline_test_f1']:>9.3f} {r['delta_vs_baseline']:>+8.3f} "
              f"{r['seeds_beating_baseline']:>4}/{r['n_seeds']} {r['p_value']:>7.3f}")


if __name__ == "__main__":
    raise SystemExit(main())
