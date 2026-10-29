"""Download H8's ten OpenML datasets: tabular data with named features.

H8 asks whether an LLM's knowledge of what the features mean speeds up
FASTENER, so its datasets need meaningful feature names (DATASETS_USED.md,
"H8: datasets with named features"). Six are already on disk (eodata,
covertype, higgs, har, crop_mapping, gas_drift); these ten come from OpenML:

  spambase       4,601 x  57, 2 classes  OpenML 44     email word frequencies
  heloc         10,000 x  22, 2 classes  OpenML 45026  FICO credit risk
  mice_protein   1,080 x  77, 8 classes  OpenML 40966  protein expression
  ozone_8hr      2,534 x  72, 2 classes  OpenML 1487   meteorology
  qsar_biodeg    1,055 x  41, 2 classes  OpenML 1494   molecular descriptors
  eye_movements  7,608 x  20, 2 classes  OpenML 44130  eye tracking
  phishing      11,055 x  30, 2 classes  OpenML 4534   web page attributes
  pc4            1,458 x  37, 2 classes  OpenML 1049   software code metrics
  diabetes130  101,766 x  ~49, 3 classes OpenML 4541   hospital readmission
  adult         48,842 x  14, 2 classes  OpenML 1590   census income

Each ARFF is kept as downloaded and checked against OpenML's md5, then
converted once to data/<name>/<name>.npz (X, y, feature_names, class_names,
dropped_missing, and an `encoding` JSON string saying what was done), read by
`datasets.load(name)`. Both files are pinned by SHA256 in SHA256SUMS.

Conversion, the same for every set:

* columns OpenML marks as row identifier or to ignore are dropped (MiceProtein:
  MouseID, and Genotype, Treatment, Behavior, which together are the class),
  and so are the ID columns listed in `drop` (diabetes130's encounter_id and
  patient_nbr);
* a nominal column with more than MAX_CATEGORIES values is dropped
  (diabetes130's three diagnosis codes and medical_specialty, adult's
  native-country): one-hot it would add hundreds of columns;
* a nominal column whose values are all numbers (phishing's -1/0/1) is kept
  as that number; one with two values becomes one 0/1 column named after it
  (1 = its second value); any other becomes one 0/1 column per value, named
  "column=value";
* a missing numeric value is replaced by its column's median over all rows,
  and counted; a missing nominal value sets none of its 0/1 columns.

Run:  python experiments/download_h8_datasets.py [--only spambase,heloc] [--force]
"""
import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from provenance import DATA_DIR, sha256  # noqa: E402

UA = {"User-Agent": "fastener-experiments/1.0"}
MAX_CATEGORIES = 30

# name -> OpenML source. `shape` is (rows, columns before conversion, classes)
# as OpenML states it, target excluded; the download is checked against it.
SOURCES: Dict[str, Dict] = {
    "spambase": {"id": 44, "target": "class", "md5": "d9ace01aeac3461e326a8e1b2d53fd84",
                 "url": "https://openml.org/data/v1/download/44/spambase.arff",
                 "shape": (4_601, 57, 2)},
    "heloc": {"id": 45026, "target": "RiskPerformance", "md5": "c77d0c9ea34bcba6574629b99355a125",
              "url": "https://openml.org/data/v1/download/22111912/heloc.arff",
              "shape": (10_000, 22, 2)},
    "mice_protein": {"id": 40966, "target": "class", "md5": "3c479a6885bfa0438971388283a1ce32",
                     "url": "https://openml.org/data/v1/download/17928620/MiceProtein.arff",
                     "drop": ["MouseID", "Genotype", "Treatment", "Behavior"],
                     "shape": (1_080, 81, 8)},
    "ozone_8hr": {"id": 1487, "target": "Class", "md5": "6e6b7aeb382e30ae79149e4e5845cf2d",
                  "url": "https://openml.org/data/v1/download/1592279/ozone-level-8hr.arff",
                  "shape": (2_534, 72, 2)},
    "qsar_biodeg": {"id": 1494, "target": "Class", "md5": "a2c189cd65511103fa540d7186155c24",
                    "url": "https://openml.org/data/v1/download/1592286/qsar-biodeg.arff",
                    "shape": (1_055, 41, 2)},
    "eye_movements": {"id": 44130, "target": "label", "md5": "0b18833a0ad388d310a6b97dd2e34d0e",
                      "url": "https://openml.org/data/v1/download/22103255/eye_movements.arff",
                      "shape": (7_608, 20, 2)},
    "phishing": {"id": 4534, "target": "Result", "md5": "fa52215c3e8caba4b765afa33bc92657",
                 "url": "https://openml.org/data/v1/download/1798106/PhishingWebsites.arff",
                 "shape": (11_055, 30, 2)},
    "pc4": {"id": 1049, "target": "c", "md5": "907e332da09127c2b25620051ff7dbd3",
            "url": "https://openml.org/data/v1/download/53932/pc4.arff",
            "shape": (1_458, 37, 2)},
    "diabetes130": {"id": 4541, "target": "readmitted", "md5": "6608dee4fb68f6bdb8abdf4135d56330",
                    "url": "https://openml.org/data/v1/download/1798768/Diabetes130US.arff",
                    "drop": ["encounter_id", "patient_nbr"],
                    "shape": (101_766, 49, 3)},
    "adult": {"id": 1590, "target": "class", "md5": "bb6510925e5d4b23d136715febb2cdf5",
              "url": "https://openml.org/data/v1/download/1595261/adult.arff",
              "shape": (48_842, 14, 2)},
}


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=900) as resp:
        return resp.read()


def _is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def convert(text: str, spec: Dict):
    """ARFF text -> X, labels, names, encoding record (see the module doc)."""
    from sklearn.externals import _arff

    arff = _arff.loads(text, encode_nominal=False)
    attrs = arff["attributes"]
    names = [a[0] for a in attrs]
    data = arff["data"]
    if spec["target"] not in names:
        raise ValueError(f"target {spec['target']!r} not among attributes")
    t = names.index(spec["target"])
    labels = np.array([str(r[t]).strip() for r in data])
    stated = (len(data), len(attrs) - 1, int(np.unique(labels).size))
    if stated != spec["shape"]:
        raise ValueError(f"shape {stated} != OpenML's {spec['shape']}")

    record = {"dropped_columns": {}, "imputed_median": {}, "one_hot": {},
              "binary": {}, "numeric_codes": []}
    cols: List[np.ndarray] = []
    out_names: List[str] = []
    for j, (name, kind) in enumerate(attrs):
        if j == t:
            continue
        if name in spec.get("drop", []):
            record["dropped_columns"][name] = "identifier or part of the class"
            continue
        raw = [r[j] for r in data]
        if isinstance(kind, list):                      # nominal
            values = [str(v) for v in kind]
            if all(_is_number(v) for v in values):
                col = np.array([np.nan if v is None else float(v) for v in raw])
                record["numeric_codes"].append(name)
            elif len(values) > MAX_CATEGORIES:
                record["dropped_columns"][name] = f"{len(values)} categories"
                continue
            elif len(values) == 2:
                record["binary"][name] = values[1]
                cols.append(np.array([1.0 if (v is not None and str(v) == values[1]) else 0.0
                                      for v in raw]))
                out_names.append(name)
                continue
            else:
                record["one_hot"][name] = values
                arr = np.array(["" if v is None else str(v) for v in raw])
                for v in values:
                    cols.append((arr == v).astype(float))
                    out_names.append(f"{name}={v}")
                continue
        else:
            col = np.array([np.nan if v is None else float(v) for v in raw])
        miss = np.isnan(col)
        if miss.any():
            med = float(np.nanmedian(col)) if (~miss).any() else 0.0
            col[miss] = med
            record["imputed_median"][name] = int(miss.sum())
        cols.append(col)
        out_names.append(name)
    X = np.column_stack(cols)
    return X, labels, np.array(out_names, dtype=str), record


def fetch(name: str, force: bool = False) -> Dict:
    spec = SOURCES[name]
    dest = DATA_DIR / name
    dest.mkdir(parents=True, exist_ok=True)
    raw = dest / f"{name}.arff"
    npz = dest / f"{name}.npz"
    if force or not raw.is_file() or raw.stat().st_size == 0:
        blob = _get(spec["url"])
        got = hashlib.md5(blob).hexdigest()
        if got != spec["md5"]:
            raise ValueError(f"md5 {got} != OpenML's {spec['md5']}")
        raw.write_bytes(blob)
    X, labels, names, record = convert(raw.read_bytes().decode("utf-8", errors="replace"), spec)
    classes = np.unique(labels)
    y = classes.searchsorted(labels).astype(int)
    record.update({"openml_id": spec["id"], "md5": spec["md5"], "source_shape": spec["shape"]})
    np.savez_compressed(npz, X=X.astype(np.float32), y=y, feature_names=names,
                        class_names=classes, dropped_missing=0,
                        encoding=json.dumps(record))
    (dest / "SHA256SUMS").write_text(
        f"{sha256(raw)}  {raw.name}\n{sha256(npz)}  {npz.name}\n", encoding="utf-8")
    return {"rows": int(X.shape[0]), "features": int(X.shape[1]),
            "classes": int(classes.size),
            "dropped": len(record["dropped_columns"]),
            "imputed": sum(record["imputed_median"].values())}


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
    print(f"  {'dataset':<15}{'rows':>9}{'features':>10}{'classes':>9}"
          f"{'dropped':>9}{'imputed':>9}")
    failures = {}
    for name in names:
        try:
            r = fetch(name, args.force)
            print(f"  {name:<15}{r['rows']:>9}{r['features']:>10}{r['classes']:>9}"
                  f"{r['dropped']:>9}{r['imputed']:>9}")
        except Exception as exc:  # report every set, then fail
            failures[name] = f"{type(exc).__name__}: {exc}"
            print(f"  {name:<15}FAILED {failures[name]}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
