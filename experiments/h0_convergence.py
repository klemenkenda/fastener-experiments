"""H0: does the bug-fixed FASTENER converge faster than the 2020 code?

Reads finished `run_sota.py` runs -- one per dataset, each holding the
`fastener` and `fastener_2020` arms -- and applies H0 exactly as
HYPOTHESES.md fixes it:

1. From every progress snapshot, AUF (K = 10) on VALIDATION F1 is computed from
   the front the snapshot stores. Over a run this is a step curve of score
   against cumulative unique fits.
2. Per dataset and seed, the target is the lower of the two arms' final values.
   Both arms reach it by construction.
3. Each arm's result is the cumulative fits at the first snapshot at or above
   the target. Fewer is faster; an equal count is a tie.

A dataset counts for an arm when that arm is faster in at least 4 of 5 seeds.
H0 is supported when the fixed arm counts on crop mapping and on at least one
other dataset. The reverse outcome -- the 2020 arm counting on crop mapping and
one other -- is reported as the fixes slowing convergence.

Secondary, reported beside it: the area under the validation curve over the
budget, final test AUF (K = 10 and 20) and hypervolume from auf.json, and the
generations and wall clock each arm used.

Validation only, up to the final test values that the run already wrote: the
test split plays no part in the target or the fit counts.

Usage:
    python experiments/h0_convergence.py results/<run crop_mapping> \\
        results/<run USPS> results/<run har> ... [--out results/h0_summary]
"""
import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import trajectory as trajectory_io  # noqa: E402

FIXED = "fastener"
ORIGINAL = "fastener_2020"
K = 10
MIN_WINS = 4
N_SEEDS = 5
REQUIRED_DATASET = "crop_mapping"

Curve = List[Tuple[int, float]]


# ---------------------------------------------------------------- the measure
def val_auf(front: Sequence[Dict], K: int = K) -> float:
    """AUF (K) on validation F1 from a trajectory front.

    opt(k) is the best validation F1 among front items of size <= k, and 0
    where there is none -- the same reading `analysis.auf` gives test scores.
    """
    values = []
    for k in range(1, K + 1):
        scores = [f["val_f1"] for f in front if f["size"] <= k]
        values.append(max(scores) if scores else 0.0)
    return float(np.mean(values))


def curve(snaps: Sequence[Dict], K: int = K) -> Curve:
    """(cumulative fits, validation AUF) at every snapshot, in order.

    The snapshots need their fronts filled in (`trajectory.read` does that).
    """
    return [(int(s["fits"]), val_auf(s["front"], K)) for s in snaps]


def fits_to_target(c: Curve, target: float) -> Optional[int]:
    """Cumulative fits at the first snapshot at or above `target`."""
    for fits, value in c:
        if value >= target - 1e-12:
            return fits
    return None


def area_under_curve(c: Curve, budget: int) -> float:
    """Mean of the step curve over fits 0..budget; 0 before the first point.

    Combines speed and level in one number: higher is better, and an arm that
    gets high early scores higher than one that gets there late.
    """
    if budget <= 0:
        raise ValueError("budget must be positive")
    area, prev_fits, prev_value = 0.0, 0, 0.0
    for fits, value in c:
        fits = min(fits, budget)
        area += prev_value * (fits - prev_fits)
        prev_fits, prev_value = fits, value
    area += prev_value * (budget - prev_fits)
    return area / budget


def compare_seed(fixed: Curve, original: Curve) -> Dict:
    """The fixed-target comparison for one dataset and seed."""
    if not fixed or not original:
        raise ValueError("both arms need at least one snapshot")
    final_fixed, final_original = fixed[-1][1], original[-1][1]
    target = min(final_fixed, final_original)
    f_fixed = fits_to_target(fixed, target)
    f_original = fits_to_target(original, target)
    if f_fixed < f_original:
        faster = FIXED
    elif f_original < f_fixed:
        faster = ORIGINAL
    else:
        faster = "tie"
    return {"target": target,
            "final_val_auf_fixed": final_fixed,
            "final_val_auf_2020": final_original,
            "fits_to_target_fixed": f_fixed,
            "fits_to_target_2020": f_original,
            "faster": faster}


# ------------------------------------------------------------------- verdicts
def dataset_verdict(seed_rows: Sequence[Dict]) -> Dict:
    """Wins, ties and losses on one dataset, and which arm it counts for."""
    wins_fixed = sum(r["faster"] == FIXED for r in seed_rows)
    wins_original = sum(r["faster"] == ORIGINAL for r in seed_rows)
    ties = sum(r["faster"] == "tie" for r in seed_rows)
    complete = len(seed_rows) >= N_SEEDS
    if not complete:
        counts_for = "incomplete"
    elif wins_fixed >= MIN_WINS:
        counts_for = FIXED
    elif wins_original >= MIN_WINS:
        counts_for = ORIGINAL
    else:
        counts_for = "neither"
    return {"seeds": len(seed_rows), "faster_fixed": wins_fixed,
            "faster_2020": wins_original, "ties": ties,
            "counts_for": counts_for}


def h0_verdict(per_dataset: Dict[str, Dict]) -> str:
    """H0's outcome from the per-dataset verdicts (HYPOTHESES.md, H0)."""
    if REQUIRED_DATASET not in per_dataset:
        return f"incomplete: no run on {REQUIRED_DATASET}"
    if per_dataset[REQUIRED_DATASET]["counts_for"] == "incomplete":
        return f"incomplete: fewer than {N_SEEDS} seeds on {REQUIRED_DATASET}"
    others = {d: v for d, v in per_dataset.items() if d != REQUIRED_DATASET}
    for arm, outcome in ((FIXED, "supported"),
                         (ORIGINAL, "reversed: the fixes slowed convergence")):
        if (per_dataset[REQUIRED_DATASET]["counts_for"] == arm
                and any(v["counts_for"] == arm for v in others.values())):
            return outcome
    return "not supported"


# ---------------------------------------------------------------- run reading
def read_run(run_dir: Path, K: int = K) -> Tuple[str, List[Dict]]:
    """Per-seed rows for one run directory: (dataset, rows)."""
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    params = manifest["params"]
    dataset = params["dataset"]
    budget = int(params["evaluation_budget_per_seed"])

    auf_rows = {}
    auf_path = run_dir / "auf.json"
    if auf_path.is_file():
        for r in json.loads(auf_path.read_text(encoding="utf-8")):
            auf_rows[(r["method"], r["seed"])] = r

    rows = []
    for seed in params["seeds"]:
        paths = {arm: run_dir / "trajectories" / f"{arm}_seed{seed}.jsonl"
                 for arm in (FIXED, ORIGINAL)}
        if not all(p.is_file() for p in paths.values()):
            continue
        snaps = {arm: trajectory_io.read(p) for arm, p in paths.items()}
        curves = {arm: curve(s, K) for arm, s in snaps.items()}
        row = {"dataset": dataset, "seed": seed, "budget": budget,
               "split": params.get("split", "protocol"),
               **compare_seed(curves[FIXED], curves[ORIGINAL])}
        for arm, suffix in ((FIXED, "fixed"), (ORIGINAL, "2020")):
            last = snaps[arm][-1]
            row[f"area_{suffix}"] = area_under_curve(curves[arm], budget)
            row[f"fits_used_{suffix}"] = int(last["fits"])
            row[f"generations_{suffix}"] = int(last["iteration"])
            row[f"seconds_{suffix}"] = float(last["seconds"])
            a = auf_rows.get((arm, seed), {})
            row[f"test_auf10_{suffix}"] = a.get("auf10_f1_weighted")
            row[f"test_auf20_{suffix}"] = a.get("auf20_f1_weighted")
            row[f"hypervolume_{suffix}"] = a.get("hypervolume")
        rows.append(row)
    return dataset, rows


def summarise(run_dirs: Sequence[Path]) -> Dict:
    per_seed: List[Dict] = []
    for d in run_dirs:
        _, rows = read_run(Path(d))
        per_seed.extend(rows)
    datasets = sorted({r["dataset"] for r in per_seed})
    per_dataset = {d: dataset_verdict([r for r in per_seed if r["dataset"] == d])
                   for d in datasets}
    return {"per_seed": per_seed, "per_dataset": per_dataset,
            "verdict": h0_verdict(per_dataset)}


# ------------------------------------------ H0-E02: every other dataset
# HYPOTHESES.md, "H0 on every other dataset". Datasets are the unit: per
# dataset, the mean over seeds of log2(fits_2020 / fits_fixed) -- positive when
# the fixed code was faster -- tested with a two-sided Wilcoxon signed-rank test.
EXTENSION_ALPHA = 0.05
EXTENSION_MAX_MISSING = 6


def seed_effect(row: Dict) -> float:
    """log2(fits the 2020 arm needed / fits the fixed arm needed)."""
    return float(np.log2(row["fits_to_target_2020"]
                         / row["fits_to_target_fixed"]))


def extension_summary(run_dirs: Sequence[Path],
                      expected: Optional[Sequence[str]] = None,
                      groups: Optional[Dict[str, str]] = None,
                      earlier_run_dirs: Sequence[Path] = ()) -> Dict:
    """The H0-E02 analysis over finished runs.

    `expected` lists the datasets the experiment was registered with, so a
    dataset with no finished run is reported as missing. `groups` maps dataset
    to its group for the secondary breakdown. `earlier_run_dirs` are H0-E01's
    runs, used only for the secondary test over all datasets.
    """
    from scipy.stats import wilcoxon

    per_seed: List[Dict] = []
    for d in run_dirs:
        _, rows = read_run(Path(d))
        per_seed.extend(rows)
    for r in per_seed:
        r["effect_log2"] = seed_effect(r)

    def per_dataset_of(rows):
        out = {}
        for ds in sorted({r["dataset"] for r in rows}):
            mine = [r for r in rows if r["dataset"] == ds]
            v = dataset_verdict(mine)
            v["effect_log2"] = float(np.mean([r["effect_log2"] for r in mine]))
            v["test_auf10_fixed"] = _mean([r["test_auf10_fixed"] for r in mine])
            v["test_auf10_2020"] = _mean([r["test_auf10_2020"] for r in mine])
            if groups:
                v["group"] = groups.get(ds)
            out[ds] = v
        return out

    def test(per_dataset):
        complete = {d: v for d, v in per_dataset.items()
                    if v["counts_for"] != "incomplete"}
        effects = np.array([v["effect_log2"] for v in complete.values()])
        pos, neg = int((effects > 0).sum()), int((effects < 0).sum())
        res = {"n_datasets": len(complete), "positive": pos, "negative": neg,
               "zero": int((effects == 0).sum()),
               "median_effect_log2": float(np.median(effects)) if effects.size else None,
               "p_value": None}
        nonzero = effects[effects != 0]
        if nonzero.size >= 1:
            res["p_value"] = float(wilcoxon(nonzero).pvalue)
        return res

    per_dataset = per_dataset_of(per_seed)
    missing = sorted(set(expected or []) - set(per_dataset)) + sorted(
        d for d, v in per_dataset.items() if v["counts_for"] == "incomplete")
    primary = test(per_dataset)

    if len(missing) > EXTENSION_MAX_MISSING:
        verdict = f"incomplete: {len(missing)} datasets left out"
    elif (primary["p_value"] is not None and primary["p_value"] < EXTENSION_ALPHA
          and primary["positive"] > primary["negative"]):
        verdict = "supported"
    elif (primary["p_value"] is not None and primary["p_value"] < EXTENSION_ALPHA
          and primary["negative"] > primary["positive"]):
        verdict = "reversed: the fixes slowed convergence"
    else:
        verdict = "not supported: no consistent difference detected"

    secondary = {}
    if groups:
        by_group = {}
        for d, v in per_dataset.items():
            by_group.setdefault(v.get("group") or "other", []).append(v["effect_log2"])
        secondary["by_group"] = {
            g: {"n": len(e), "mean_effect_log2": float(np.mean(e)),
                "positive": int(sum(x > 0 for x in e)),
                "negative": int(sum(x < 0 for x in e))}
            for g, e in sorted(by_group.items())}
    if earlier_run_dirs:
        earlier = []
        for d in earlier_run_dirs:
            _, rows = read_run(Path(d))
            earlier.extend(rows)
        for r in earlier:
            r["effect_log2"] = seed_effect(r)
        secondary["all_datasets_including_H0_E01"] = test(
            per_dataset_of(per_seed + earlier))

    return {"per_seed": per_seed, "per_dataset": per_dataset,
            "missing": missing, "primary": primary, "secondary": secondary,
            "verdict": verdict}


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return float(np.mean(xs)) if xs else None


def print_extension(summary: Dict) -> None:
    print("per dataset (effect = mean log2(fits 2020 / fits fixed); "
          "> 0 means the fixed code was faster):")
    print(f"  {'dataset':<14}{'group':<22}{'effect':>8}  fixed/2020/ties"
          f"{'test fixed':>12}{'test 2020':>10}")
    for d, v in sorted(summary["per_dataset"].items(),
                       key=lambda kv: -kv[1]["effect_log2"]):
        print(f"  {d:<14}{str(v.get('group') or ''):<22}{v['effect_log2']:>8.2f}"
              f"  {v['faster_fixed']}/{v['faster_2020']}/{v['ties']}"
              f"{' ' * 9}{_fmt(v['test_auf10_fixed'], '8.4f')}"
              f"  {_fmt(v['test_auf10_2020'], '8.4f')}")
    p = summary["primary"]
    print(f"\nprimary: {p['positive']} datasets favour the fixed code, "
          f"{p['negative']} the 2020 code, {p['zero']} tie; median effect "
          f"{_fmt(p['median_effect_log2'], '.3f')}; Wilcoxon p = "
          f"{_fmt(p['p_value'], '.4f')} (n = {p['n_datasets']})")
    if summary["missing"]:
        print(f"left out: {', '.join(summary['missing'])}")
    for g, v in summary["secondary"].get("by_group", {}).items():
        print(f"  group {g:<22} n={v['n']:>2}  mean effect "
              f"{v['mean_effect_log2']:+.2f}  +{v['positive']} / -{v['negative']}")
    allv = summary["secondary"].get("all_datasets_including_H0_E01")
    if allv:
        print(f"secondary, all datasets incl. H0-E01's five: +{allv['positive']}"
              f" / -{allv['negative']}, Wilcoxon p = "
              f"{_fmt(allv['p_value'], '.4f')} (n = {allv['n_datasets']})")
    print(f"\nH0-E02: {summary['verdict']}")


def write_extension_outputs(summary: Dict, out: Path,
                            runs: Sequence[Path]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    if summary["per_seed"]:
        with open(out / "h0_seeds.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(summary["per_seed"][0]))
            w.writeheader()
            w.writerows(summary["per_seed"])
    (out / "h0_extension_summary.json").write_text(
        json.dumps({**summary, "runs": [str(p) for p in runs]}, indent=2),
        encoding="utf-8")


def _fmt(x, spec):
    return "-" if x is None else format(x, spec)


def print_summary(summary: Dict) -> None:
    print("per seed (validation AUF, K = 10; fits to the common target):")
    print(f"  {'dataset':<14}{'seed':>6}{'target':>9}{'fixed':>8}{'2020':>8}"
          f"  faster        {'area fixed':>10}{'area 2020':>10}"
          f"{'test fixed':>11}{'test 2020':>10}")
    for r in summary["per_seed"]:
        print(f"  {r['dataset']:<14}{r['seed']:>6}{r['target']:>9.4f}"
              f"{r['fits_to_target_fixed']:>8}{r['fits_to_target_2020']:>8}"
              f"  {r['faster']:<14}{r['area_fixed']:>10.4f}{r['area_2020']:>10.4f}"
              f"{_fmt(r['test_auf10_fixed'], '11.4f')}"
              f"{_fmt(r['test_auf10_2020'], '10.4f')}")
    print("\nper dataset:")
    for d, v in summary["per_dataset"].items():
        print(f"  {d:<14} fixed faster {v['faster_fixed']}, 2020 faster "
              f"{v['faster_2020']}, ties {v['ties']} of {v['seeds']} "
              f"-> counts for {v['counts_for']}")
    print(f"\nH0: {summary['verdict']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("runs", nargs="+", type=Path,
                    help="run directories, one per dataset")
    ap.add_argument("--out", type=Path, default=None,
                    help="directory for h0_seeds.csv and h0_summary.json")
    args = ap.parse_args()

    summary = summarise(args.runs)
    if not summary["per_seed"]:
        raise SystemExit("no seed had trajectories for both arms")
    print_summary(summary)

    if args.out:
        write_outputs(summary, args.out, args.runs)
        print(f"\nwrote {args.out / 'h0_seeds.csv'} and h0_summary.json")
    return 0


def write_outputs(summary: Dict, out: Path, runs: Sequence[Path]) -> None:
    """h0_seeds.csv (one row per dataset and seed) and h0_summary.json."""
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "h0_seeds.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary["per_seed"][0]))
        w.writeheader()
        w.writerows(summary["per_seed"])
    (out / "h0_summary.json").write_text(
        json.dumps({**summary, "runs": [str(p) for p in runs]}, indent=2),
        encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
