"""Download the MADELON dataset and pin it by SHA256.

MADELON (NIPS 2003 feature-selection challenge) is used because it has a known
ground truth: of its 500 features exactly 20 are relevant (5 informative plus 15
redundant linear combinations) and the other 480 are pure noise. That lets us ask
not only "is accuracy good" but "did the method actually recover the real
features" -- the more honest question for a feature-selection algorithm.

The official test labels were never released, so we use the train (2000) and
validation (600) splits, 2600 labelled rows in total, and cut our own
train/val/test partitions from them in datasets.py.

Run:  python experiments/download_data.py
"""
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import DATA_DIR, sha256  # noqa: E402

BASE = "https://archive.ics.uci.edu/ml/machine-learning-databases/madelon"

FILES = {
    "madelon_train.data":   f"{BASE}/MADELON/madelon_train.data",
    "madelon_train.labels": f"{BASE}/MADELON/madelon_train.labels",
    "madelon_valid.data":   f"{BASE}/MADELON/madelon_valid.data",
    "madelon_valid.labels": f"{BASE}/madelon_valid.labels",
}

# Pinned on 2026-09-16 from the UCI archive. A mismatch means the upstream data
# changed under us, which must not pass silently.
EXPECTED_SHA256 = {
    "madelon_train.data":   "0b6e37711efdc7ab74250c51e7d6966bffd9f8f2b0e9971e882c3a7a380c2314",
    "madelon_train.labels": "10bffcc3b017467cb810d326b931951adcbde2b4870faf981da2991993b48689",
    "madelon_valid.data":   "cb9a46475147de1a58d9f15ef4c318e5b85de344e0f9ab92626fa446aa815dc9",
    "madelon_valid.labels": "fbac32fa87fac41ab731994a1c824e7b25396069bff6df242c01fe240fcb34dc",
}

DEST = DATA_DIR / "madelon"


def download(force: bool = False) -> dict:
    DEST.mkdir(parents=True, exist_ok=True)
    digests = {}
    for name, url in FILES.items():
        path = DEST / name
        if path.exists() and not force:
            print(f"  have     {name}")
        else:
            print(f"  fetching {name} ... ", end="", flush=True)
            req = urllib.request.Request(url, headers={"User-Agent": "fastener-experiments/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp, open(path, "wb") as fh:
                fh.write(resp.read())
            print(f"{path.stat().st_size:,} bytes")
        digests[name] = sha256(path)
    return digests


def main() -> int:
    force = "--force" in sys.argv
    print(f"MADELON -> {DEST}")
    digests = download(force=force)

    print("\nSHA256:")
    for name, digest in digests.items():
        print(f"  {digest}  {name}")

    mismatches = [
        name for name, digest in digests.items()
        if EXPECTED_SHA256.get(name) != digest
    ]
    if mismatches:
        print("\nERROR: checksum mismatch for: " + ", ".join(mismatches))
        print("The upstream dataset changed. Refusing to continue silently.")
        return 1

    # Write the digests next to the data so downstream runs can verify cheaply.
    (DEST / "SHA256SUMS").write_text(
        "".join(f"{d}  {n}\n" for n, d in sorted(digests.items())), encoding="utf-8"
    )
    print(f"\nWrote {DEST / 'SHA256SUMS'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
