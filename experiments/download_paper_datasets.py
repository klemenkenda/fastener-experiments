"""Download the 25 benchmark datasets used in the FASTENER paper.

Source: Koprivec, Kenda & Sircelj, "FASTENER Feature Selection for Inference
from Earth Observation Data", Entropy 2020, 22(11), 1198. Table 1 lists 25
feature-selection benchmarks plus the authors' own EOData.

The paper takes those 25 from its reference [6] -- Li et al., "Feature
Selection: A Data Perspective", ACM Computing Surveys 2018 -- which is the
scikit-feature repository at ASU. Files are MATLAB .mat with an instance matrix
`X` and a label vector `Y`.

NOT covered here:
  EOData      Sentinel-2 land-cover data, 480,000 x 182. Not on scikit-feature;
              published separately as Sircelj, Kenda & Koprivec, "Land Patch
              Samples", PANGAEA 2020 (paper's reference [32]). It needs its own
              fetch and is far larger than everything else combined.

Note the paper does NOT use MADELON or GINA, the two datasets these experiments
have been running on. arcene and gisette are here and come from the same NIPS
2003 challenge as MADELON, but MADELON itself is not among the paper's 25.

Run:  python experiments/download_paper_datasets.py           # all 25
      python experiments/download_paper_datasets.py --only colon,Yale
      python experiments/download_paper_datasets.py --max-mb 20
"""
import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import DATA_DIR, sha256  # noqa: E402

BASE = "https://jundongl.github.io/scikit-feature/files/datasets"

# Name -> (instances, features, classes) exactly as the paper's Table 1 states
# them. Kept here so the download can be checked against what the paper claims
# rather than trusted blindly.
PAPER_TABLE_1 = {
    "ALLAML":       (72, 7129, 2),
    "arcene":       (200, 10000, 2),
    "BASEHOCK":     (1993, 4862, 2),
    "CLL_SUB_111":  (111, 11340, 3),
    "COIL20":       (1440, 1024, 20),
    "colon":        (62, 2000, 2),
    "gisette":      (7000, 5000, 2),
    "GLIOMA":       (50, 4434, 4),
    "GLI_85":       (85, 22283, 2),
    "Isolet":       (1560, 617, 26),
    "leukemia":     (72, 7070, 2),
    "lung":         (203, 3312, 5),
    "lung_discrete": (73, 325, 7),
    "lymphoma":     (96, 4026, 9),
    "nci9":         (60, 9712, 9),
    "ORL":          (400, 1024, 40),
    "orlraws10P":   (100, 10304, 10),
    "PCMAC":        (1943, 3289, 2),
    "Prostate_GE":  (102, 5966, 2),
    "RELATHE":      (1427, 4322, 2),
    "TOX_171":      (171, 5748, 4),
    "USPS":         (9298, 256, 10),
    "warpAR10P":    (130, 2400, 10),
    "warpPIE10P":   (210, 2420, 10),
    "Yale":         (165, 1024, 15),
}

DEST = DATA_DIR / "paper_benchmarks"


def fetch(name: str, force: bool = False) -> Path:
    DEST.mkdir(parents=True, exist_ok=True)
    path = DEST / f"{name}.mat"
    if path.exists() and not force and path.stat().st_size > 0:
        return path
    url = f"{BASE}/{name}.mat"
    req = urllib.request.Request(
        url, headers={"User-Agent": "fastener-experiments/1.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = resp.read()
    path.write_bytes(data)
    return path


def inspect(path: Path) -> Dict:
    """Read shape and class count straight from the .mat, to check the table."""
    from scipy.io import loadmat
    import numpy as np

    m = loadmat(path)
    X = m["X"]
    y = np.asarray(m["Y"]).ravel()
    return {"instances": int(X.shape[0]), "features": int(X.shape[1]),
            "classes": int(np.unique(y).size)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None,
                    help="comma-separated subset of dataset names")
    ap.add_argument("--max-mb", type=float, default=None,
                    help="skip datasets whose download exceeds this size")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    names = list(PAPER_TABLE_1)
    if args.only:
        wanted = [n.strip() for n in args.only.split(",") if n.strip()]
        unknown = [n for n in wanted if n not in PAPER_TABLE_1]
        if unknown:
            raise SystemExit(f"unknown dataset(s): {unknown}")
        names = wanted

    print(f"downloading {len(names)} datasets to {DEST}\n")
    print(f"  {'dataset':<16}{'MB':>7}  {'instances':>10}{'features':>10}"
          f"{'classes':>9}   vs paper")
    print("  " + "-" * 70)

    digests, failures, mismatches = {}, {}, []
    for name in names:
        try:
            path = fetch(name, force=args.force)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as exc:
            failures[name] = f"{type(exc).__name__}: {exc}"
            print(f"  {name:<16}  DOWNLOAD FAILED  {failures[name]}")
            continue

        mb = path.stat().st_size / 1e6
        if args.max_mb is not None and mb > args.max_mb:
            path.unlink()
            print(f"  {name:<16}{mb:7.1f}  skipped (over --max-mb)")
            continue

        try:
            got = inspect(path)
        except Exception as exc:
            failures[name] = f"unreadable: {type(exc).__name__}: {exc}"
            print(f"  {name:<16}{mb:7.1f}  UNREADABLE  {exc}")
            continue

        want = PAPER_TABLE_1[name]
        same = (got["instances"], got["features"], got["classes"]) == want
        verdict = "ok" if same else f"MISMATCH want {want}"
        if not same:
            mismatches.append((name, want,
                               (got["instances"], got["features"], got["classes"])))
        print(f"  {name:<16}{mb:7.1f}  {got['instances']:>10}"
              f"{got['features']:>10}{got['classes']:>9}   {verdict}")
        digests[name] = sha256(path)

    # Pin the exact bytes, the same way download_data.py does for MADELON.
    if digests:
        lines = [f"{d}  {n}.mat" for n, d in sorted(digests.items())]
        (DEST / "SHA256SUMS").write_text("\n".join(lines) + "\n",
                                         encoding="utf-8")
        print(f"\nwrote {DEST / 'SHA256SUMS'} ({len(digests)} files)")

    if mismatches:
        print("\nshape mismatches vs the paper's Table 1:")
        for name, want, got in mismatches:
            print(f"  {name}: paper says {want}, file has {got}")
    if failures:
        print("\nfailed:")
        for name, err in failures.items():
            print(f"  {name}: {err}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
