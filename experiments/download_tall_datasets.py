"""Download the tall datasets: many rows, relatively few features.

The 25 paper benchmarks are almost all the opposite shape -- tens to hundreds of
rows against thousands of features -- while FASTENER was built for EOData,
480,000 rows by 182 features. These eight fill that gap, so that the full-grid
comparison (H5, H6) does not rest almost entirely on wide, short data:

  crop_mapping  325,834 x 174, 7 classes  UCI 525, CC BY 4.0
  covertype     581,012 x  54, 7 classes  OpenML 1596
  satimage        6,430 x  36, 6 classes  OpenML 182
  har            10,299 x 561, 6 classes  OpenML 1478
  gas_drift      13,910 x 128, 6 classes  OpenML 1476
  volkert        58,310 x 180, 10 classes OpenML 41166
  miniboone     130,064 x  50, 2 classes  OpenML 41150
  higgs          98,050 x  28, 2 classes  OpenML 23512

Each source file is kept as downloaded, checked against the checksum its
repository publishes where there is one (OpenML's md5), then converted once to a
compressed .npz that `datasets.load(name)` reads. Both are pinned by SHA256 in
the dataset's own SHA256SUMS, as for every other dataset in data/.

Shapes are checked against the counts the repositories state, so a changed or
truncated upstream file is caught here rather than inside an experiment.

Run:  python experiments/download_tall_datasets.py
      python experiments/download_tall_datasets.py --only har,satimage
      python experiments/download_tall_datasets.py --force
"""
import argparse
import hashlib
import io
import re
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import DATA_DIR, sha256  # noqa: E402

UA = {"User-Agent": "fastener-experiments/1.0"}

# name -> source. `shape` is (rows, features, classes) as the repository states
# it, before any cleaning; the download is checked against it.
SOURCES: Dict[str, Dict] = {
    "crop_mapping": {
        "kind": "uci_zip",
        "url": ("https://archive.ics.uci.edu/static/public/525/"
                "crop+mapping+using+fused+optical+radar+data+set.zip"),
        "target": "label",
        "shape": (325_834, 174, 7),
        "citation": ("Crop mapping using fused optical-radar data set [Dataset]. "
                     "(2020). UCI Machine Learning Repository. "
                     "https://doi.org/10.24432/C5G89D (CC BY 4.0)"),
    },
    "covertype": {
        "kind": "openml", "id": 1596, "target": "class",
        "url": "https://openml.org/data/v1/download/1601911/covertype.arff",
        "md5": "521cdee1fd153f0b4e912435633e7ff5",
        "shape": (581_012, 54, 7),
    },
    "satimage": {
        "kind": "openml", "id": 182, "target": "class",
        "url": "https://openml.org/data/v1/download/3619/satimage.arff",
        "md5": "72857195d1f6c4c2171c386594f870b2",
        "shape": (6_430, 36, 6),
    },
    "har": {
        "kind": "openml", "id": 1478, "target": "Class",
        "url": "https://openml.org/data/v1/download/1589271/har.arff",
        "md5": "7b1e71116a88aa1d88b43e697f7c67ee",
        "shape": (10_299, 561, 6),
    },
    "gas_drift": {
        "kind": "openml", "id": 1476, "target": "Class",
        "url": "https://openml.org/data/v1/download/1588715/gas-drift.arff",
        "md5": "e205264c230a3e15c7546c18ddceedaf",
        "shape": (13_910, 128, 6),
    },
    "volkert": {
        "kind": "openml", "id": 41166, "target": "class",
        "url": "https://openml.org/data/v1/download/19335689/volkert.arff",
        "md5": "aea21c2b8ca8b42afbf35b28346dc6b7",
        "shape": (58_310, 180, 10),
    },
    "miniboone": {
        "kind": "openml", "id": 41150, "target": "signal",
        "url": "https://openml.org/data/v1/download/19335523/MiniBooNE.arff",
        "md5": "400fbfb8eaea0c1165ecedbafd517b98",
        "shape": (130_064, 50, 2),
    },
    "higgs": {
        "kind": "openml", "id": 23512, "target": "class",
        "url": "https://openml.org/data/v1/download/2063675/higgs.arff",
        "md5": "1a216f3bb3f6a961b4023179fca78452",
        "shape": (98_050, 28, 2),
    },
}


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=900) as resp:
        return resp.read()


def _parse_arff(text: str, target: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Dense ARFF -> (X, y labels as strings, feature names).

    Attribute names are pulled by regex, so quoted names with spaces survive.
    pandas does the bulk read: 580,000 rows of Python-level splitting is minutes,
    read_csv is seconds.
    """
    import pandas as pd

    head_end = re.search(r"^\s*@data\s*$", text, flags=re.IGNORECASE | re.MULTILINE)
    if head_end is None:
        raise ValueError("no @data line")
    header, body = text[:head_end.start()], text[head_end.end():]
    attrs = [a or b or c for a, b, c in re.findall(
        r"^\s*@attribute\s+(?:'([^']*)'|\"([^\"]*)\"|(\S+))",
        header, flags=re.IGNORECASE | re.MULTILINE)]
    if body.lstrip().startswith("{"):
        raise ValueError("sparse ARFF is not supported")

    df = pd.read_csv(io.StringIO(body), header=None, names=attrs,
                     na_values=["?"], quotechar="'", skipinitialspace=True,
                     comment="%", low_memory=False)
    if target not in df.columns:
        raise ValueError(f"target {target!r} not among attributes")
    y = df.pop(target).astype(str).str.strip().to_numpy()
    X = df.to_numpy(dtype=np.float64)
    return X, y, np.array(df.columns, dtype=str)


def _parse_crop_zip(blob: bytes, target: str):
    import pandas as pd

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        members = [m for m in zf.namelist()
                   if m.lower().endswith((".txt", ".csv")) and not m.startswith("__")]
        if len(members) != 1:
            raise ValueError(f"expected one data file in the zip, found {members}")
        df = pd.read_csv(zf.open(members[0]))
    df.columns = [c.strip() for c in df.columns]
    y = df.pop(target).astype(str).str.strip().to_numpy()
    return df.to_numpy(dtype=np.float64), y, np.array(df.columns, dtype=str)


def fetch(name: str, force: bool = False) -> Dict:
    spec = SOURCES[name]
    dest = DATA_DIR / name
    dest.mkdir(parents=True, exist_ok=True)
    raw_name = f"{name}.arff" if spec["kind"] == "openml" else f"{name}.zip"
    raw = dest / raw_name
    npz = dest / f"{name}.npz"

    if force or not raw.is_file() or raw.stat().st_size == 0:
        blob = _get(spec["url"])
        if "md5" in spec:
            got = hashlib.md5(blob).hexdigest()
            if got != spec["md5"]:
                raise ValueError(f"md5 {got} != OpenML's {spec['md5']}")
        raw.write_bytes(blob)
    blob = raw.read_bytes()

    if spec["kind"] == "openml":
        X, labels, names = _parse_arff(blob.decode("utf-8", errors="replace"),
                                       spec["target"])
    else:
        X, labels, names = _parse_crop_zip(blob, spec["target"])

    stated = (X.shape[0], X.shape[1], int(np.unique(labels).size))
    if stated != spec["shape"]:
        raise ValueError(f"shape {stated} != repository's {spec['shape']}")

    # Rows with any missing value are dropped, and the count kept with the data
    # so the loader can report it. Only higgs has any.
    ok = ~np.isnan(X).any(axis=1)
    dropped_missing = int((~ok).sum())
    X, labels = X[ok], labels[ok]

    classes = np.unique(labels)
    y = classes.searchsorted(labels).astype(int)
    np.savez_compressed(npz, X=X.astype(np.float32), y=y, feature_names=names,
                        class_names=classes, dropped_missing=dropped_missing)

    (dest / "SHA256SUMS").write_text(
        f"{sha256(raw)}  {raw.name}\n{sha256(npz)}  {npz.name}\n", encoding="utf-8")
    return {"rows": int(X.shape[0]), "features": int(X.shape[1]),
            "classes": int(classes.size), "dropped_missing": dropped_missing,
            "mb": raw.stat().st_size / 1e6}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="comma-separated names")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    names = list(SOURCES)
    if args.only:
        names = [n.strip() for n in args.only.split(",") if n.strip()]
        unknown = [n for n in names if n not in SOURCES]
        if unknown:
            raise SystemExit(f"unknown: {unknown}; have {list(SOURCES)}")

    print(f"  {'dataset':<14}{'MB':>8}{'rows':>10}{'features':>10}{'classes':>9}"
          f"{'dropped':>9}")
    failures = {}
    for name in names:
        try:
            r = fetch(name, force=args.force)
        except Exception as exc:
            failures[name] = f"{type(exc).__name__}: {exc}"
            print(f"  {name:<14}  FAILED  {failures[name]}")
            continue
        print(f"  {name:<14}{r['mb']:8.1f}{r['rows']:>10,}{r['features']:>10}"
              f"{r['classes']:>9}{r['dropped_missing']:>9}")
    if failures:
        print("\nfailed:")
        for n, e in failures.items():
            print(f"  {n}: {e}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
