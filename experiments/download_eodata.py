"""Download EOData, the FASTENER paper's own Earth-observation dataset.

Sircelj, B.; Kenda, K.; Koprivec, F. "Land Patch Samples". PANGAEA, 2020.
https://doi.org/10.1594/PANGAEA.914271   (CC-BY-4.0)

This is the paper's headline dataset and the one it was actually built for:
480,000 rows (20,000 per class x 24 classes) x 182 features, collected over
Slovenia in 2017 from Sentinel-2 under the H2020 PerceptiveSentinel project.
It is the last row of the paper's Table 1 and, unlike the 25 scikit-feature
benchmarks, it has many instances and few features rather than the reverse.

The source is a single 1.4 GB ARFF. This script fetches it with resume support
and pins it by SHA256; datasets.load("eodata") converts it once to a compressed
.npz and reads that thereafter.

Run:  python experiments/download_eodata.py
      python experiments/download_eodata.py --convert   # also build the .npz
"""
import argparse
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import DATA_DIR, sha256  # noqa: E402

URL = "https://hs.pangaea.de/sat/LPIS/FASTENER_dataset.arff"
DEST = DATA_DIR / "eodata"
FILENAME = "FASTENER_dataset.arff"

# Content-Length reported by the server on 2026-09-23.
EXPECTED_BYTES = 1_412_784_512

CITATION = (
    "Sircelj, B.; Kenda, K.; Koprivec, F. (2020): Land Patch Samples. "
    "PANGAEA, https://doi.org/10.1594/PANGAEA.914271 (CC-BY-4.0)"
)


def download(force: bool = False) -> Path:
    DEST.mkdir(parents=True, exist_ok=True)
    path = DEST / FILENAME

    have = path.stat().st_size if path.exists() else 0
    if have == EXPECTED_BYTES and not force:
        print(f"  have {FILENAME} ({have:,} bytes)")
        return path

    # Resume a partial file rather than restart 1.4 GB from zero.
    headers = {"User-Agent": "fastener-experiments/1.0"}
    mode = "wb"
    if have and not force:
        print(f"  resuming from {have:,} bytes")
        headers["Range"] = f"bytes={have}-"
        mode = "ab"

    req = urllib.request.Request(URL, headers=headers)
    with urllib.request.urlopen(req, timeout=600) as resp, open(path, mode) as fh:
        total = have
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)
            total += len(chunk)
            pct = 100.0 * total / EXPECTED_BYTES
            print(f"\r  {total:,} / {EXPECTED_BYTES:,} bytes ({pct:5.1f}%)",
                  end="", flush=True)
    print()

    size = path.stat().st_size
    if size != EXPECTED_BYTES:
        # Not fatal -- the file may legitimately have been revised upstream --
        # but it must not pass unremarked.
        print(f"  WARNING: expected {EXPECTED_BYTES:,} bytes, got {size:,}")
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--convert", action="store_true",
                    help="also parse the ARFF into the cached .npz now")
    args = ap.parse_args()

    print(CITATION)
    print(f"\ndownloading to {DEST}")
    path = download(force=args.force)

    digest = sha256(path)
    (DEST / "SHA256SUMS").write_text(f"{digest}  {FILENAME}\n", encoding="utf-8")
    print(f"  sha256 {digest}")
    print(f"  wrote {DEST / 'SHA256SUMS'}")

    if args.convert:
        print("\nparsing ARFF -> npz (slow, one time) ...")
        from datasets import load_eodata
        ds = load_eodata()
        print(f"  {ds}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
