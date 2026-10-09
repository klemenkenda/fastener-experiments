"""Download the 39 time series classification datasets and pin them by SHA256.

The selection, seven or so per cluster of dataset shape, is in
DATASETS_USED.md and `datasets.TSC_DATASETS`. Each comes from the UCR/UEA
archive at timeseriesclassification.com as one zip holding the archive's
TRAIN and TEST halves in several formats; the `.ts` files are read.

What is done to each:

* the zip is kept as downloaded, under data/tsc/<name>/, and checked against
  the SHA256 pinned below. The archive publishes no checksums, so the pins are
  our own, taken at the first download; a mismatch afterwards means the
  upstream file changed and must not pass silently;
* TRAIN and TEST are merged into one table, since every dataset here is split
  60/20/20 by the protocol, not by the archive. `origin` (0 train, 1 test)
  keeps the archive's split recoverable;
* a multivariate series is flattened channel by channel: feature
  `c*length + t` is channel c at time t, named `c{c}_t{t}` (`t{t}` for a
  univariate set);
* the shape -- examples, series length, channels, classes -- is checked
  against tsc_dataset_clusters.csv, which was taken from the archive's own
  table, so a changed or truncated upstream file is caught here rather than
  inside an experiment;
* rows with a missing value are dropped and counted, as for the tall sets.

The result is one compressed .npz per dataset, which `datasets.load(name)`
reads, recorded with the zip in the dataset's SHA256SUMS.

Run:  python experiments/download_tsc_datasets.py
      python experiments/download_tsc_datasets.py --only Coffee,Wafer
      python experiments/download_tsc_datasets.py --cluster C2
      python experiments/download_tsc_datasets.py --force
      python experiments/download_tsc_datasets.py --pin    # first download only
"""
import argparse
import csv
import io
import shutil
import sys
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datasets import TSC_DATASETS, TSC_DIR  # noqa: E402
from provenance import sha256  # noqa: E402

URL = "https://www.timeseriesclassification.com/aeon-toolkit/{name}.zip"
UA = {"User-Agent": "fastener-experiments/1.0"}
CLUSTERS_CSV = Path(__file__).resolve().parent / "tsc_dataset_clusters.csv"

# Pinned from the first download. For a dataset not yet pinned the run fails
# unless given --pin, which reads it anyway and prints the digest to add here,
# so an unpinned file is never used without someone looking at it.
EXPECTED_SHA256: Dict[str, str] = {
    "Coffee": "bfba9d67f4a0f2041cb8ba88b60b11f10dab60b670e40b904ac47bd7dfdf4749",
    "OliveOil": "eb25894f92858611b641c77f3ce8e1cfca6312dd3945d07b96c392e5dc6b24c6",
    "Ham": "2f0f001691e414c11725fde43e07994173bd5840b6c289eb59ccc69afb1555a4",
    "BeetleFly": "76628ae49a3c786157692be5739928e36f8999ac4f7d6f6ec47d29a68cc64a6e",
    "Earthquakes": "927cfb732988055850a74efa169dfd633bc7f578095c35319bebb83453501bf1",
    "BasicMotions": "f427609dfe343b1da0dc54ee361f61579e7f18c2a007121740a9f0d90286fac3",
    "Epilepsy": "8e5ce818a4989e520aa620f3009621692f06c8e8e73d72ee98cc0dbdee7c10c9",
    "MotorImagery": "13061e6c1de3f04c4239e65dcabe9422e99f3e4acac5150c68226bcb3c9b3fc2",
    "PEMS-SF": "4cddf0c9a7335e5195ee79940a4e962ac8e1b33d9f1bebd184b34d566a747320",
    "DuckDuckGeese": "b9e086450eab0b940f9f2be18bd8c941691b2e03a51d3e36705f38591d27c7c5",
    "Heartbeat": "7b325f03fb817030809afcb1d742f1d0159c580e121e2380b7b736bdd67b8830",
    "EigenWorms": "38db21f136e9694f4d4b76f97b196029cd186a7fc476de825c09f11557874779",
    "SelfRegulationSCP1": "5581185eeb098153e3f7524048eec7371c11b52c0ad0f52f7612eeea4267ef83",
    "FingerMovements": "1d6c4d39b8eb9aede468be45054bf8c59c8e276ee90ed3a7e48bb16b41c66b97",
    "NATOPS": "38e91561d70426b508abf6db253070b1bed00a1c303d70844997ef4d4ab3b7ff",
    "EthanolConcentration": "67c4ff269ad40b474a0917572c0b36256829bdb33df40521c09fcac0c52c6ce4",
    "Computers": "482d87ec9dd6d933a7c42a393bce7e53f958d6a366c80dbbf01b5e40af57d6d1",
    "CinCECGTorso": "12d79e4375e141e93386df8a354367837b5a47cc007ec68c10465fcc1d3d7b64",
    "HandOutlines": "786d456b927fd85e614f42b189c59f23a60678da4ec6c2a08f2519b9e21c25fb",
    "Adiac": "9c808bcfc77f3cab0a640bfa23e680ccde91da6981962e63c0f4f0737dcf6390",
    "Strawberry": "1293ba770d15817be769958f077cab6f76d65a66465aff80ed393d1e80a71e00",
    "MedicalImages": "dd58761619a92eabffc2691f22aa7639040f74a1840238a8512f766a05e2ead4",
    "ProximalPhalanxOutlineCorrect": "afc4c420408e11c4bc2fbc80d455e2cc3743db7e0729cc0c8da50cc03bcd9bc4",
    "TwoLeadECG": "f747b239fdc4f2657546ad2789290029c219b06fe0b58059a83c004a16f3d9a8",
    "ItalyPowerDemand": "4b68635dc79855fbdb7787d5dff5bac978fd0448afaa8eb7811dae52d43e5e46",
    "Libras": "8c7f9c67e9c6c66ca659f65e077e3d1f212ab1f237dd212d488df13f25fa3688",
    "FordA": "4d78a72e5165e8da40c51115a8219c9d01978aafac6334ed8dfabd29da359ffb",
    "Wafer": "06032db83b3f6f3f39ef4b65433061dde9b2593b956caa1ad1ae9ad260a36be4",
    "ECG5000": "41f6de20ac895e9ce31753860995518951f1ed42a405d0e51c909d27e3b3c5a4",
    "ChlorineConcentration": "185d0239049dc138d0917fa8faea19084cf4e0c31cd963833c659714d113a129",
    "StarLightCurves": "f5a3b1646837eabee4b292313263fc40a00524df9ab14e0c4c901829f63bbf33",
    "UWaveGestureLibraryAll": "fedcbb271e7149bd07fb564b66d2d62c98acbb6eb7857ba8267d95da12ca5f2a",
    "LSST": "a4c3563c6eab5879a842ebb4e6feab64a86d74bc0738acfb2ae90abb7d3bee89",
    "FaceDetection": "a881a69542f80ceaf718c5ab93ccb107c71003ab852f9d9cdabf9c8faa549e85",
    "PhonemeSpectra": "260e41af8f4e8a3f51e4aa87007616ebb29ab0094074da1593474924c60cf632",
    "FaultDetectionA": "50c17f04fcfb1e4d527fcf3b5ad8b9c35952c175ac4fc5d6700560b356edc32f",
    "Crop": "6755bf248661ebfe9c3dba59f757d660f7d8ac97e7174c19543573cbe68909bd",
    "ElectricDevices": "0d63e83f7b49e90c7d0bd4bb20320e2b26719da596e0d96de6581bbeecca58d5",
    "PenDigits": "4a9a706463eb98b8773fb6c2bb24038f2855ce1f0c55d1d0109e9f0bd0052842",
}


# Where the archive's table disagrees with the file it serves, and the file
# agrees with itself (its header and every row), the file is taken. Each entry
# says what was checked.
TABLE_CORRECTIONS: Dict[str, Dict[str, int]] = {
    # Table: series length 207. The .ts header (@seriesLength 206) and all 275
    # rows in both halves, every channel, have 206.
    "Epilepsy": {"length": 206},
}


def _expected_shapes() -> Dict[str, Tuple[int, int, int, int]]:
    """name -> (examples, length, channels, classes), from the archive's table."""
    with open(CLUSTERS_CSV, newline="", encoding="utf-8") as fh:
        rows = {r["dataset"]: r for r in csv.DictReader(fh)}
    shapes = {}
    for name, r in rows.items():
        fixed = TABLE_CORRECTIONS.get(name, {})
        shapes[name] = (fixed.get("n_examples", int(r["n_examples"])),
                        fixed.get("length", int(r["length"])),
                        fixed.get("channels", int(r["channels"])),
                        fixed.get("classes", int(r["classes"])))
    return shapes


def _download(url: str, dest: Path, tries: int = 4) -> None:
    """Stream to a .part file and rename, so a broken download never looks done."""
    part = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(1, tries + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=900) as resp, \
                    open(part, "wb") as fh:
                shutil.copyfileobj(resp, fh, length=1 << 20)
            part.replace(dest)
            return
        except Exception as exc:
            if attempt == tries:
                raise
            wait = 15 * attempt
            print(f"    {type(exc).__name__}: {exc}; retrying in {wait}s")
            time.sleep(wait)


def parse_ts(text: str) -> Tuple[np.ndarray, List[str], int, int]:
    """A `.ts` file -> (X flattened channel by channel, labels, length, channels).

    Only what the 39 need: equal-length series, no timestamps, a class label.
    Anything else is refused rather than guessed at.
    """
    header: Dict[str, str] = {}
    lines = iter(text.splitlines())
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.lower() == "@data":
            break
        if line.startswith("@"):
            key, _, value = line[1:].partition(" ")
            header[key.lower()] = value.strip()
    else:
        raise ValueError("no @data line")

    if header.get("timestamps", "false").lower() != "false":
        raise ValueError("timestamped series are not supported")
    if header.get("equallength", "true").lower() != "true":
        raise ValueError("unequal-length series are not supported")
    if not header.get("classlabel", "").lower().startswith("true"):
        raise ValueError("no class label")

    rows, labels = [], []
    shape = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        *dims, label = line.split(":")
        series = [np.array(d.replace("?", "nan").split(","), dtype=np.float64)
                  for d in dims]
        this = (len(series), len(series[0]))
        if any(len(s) != this[1] for s in series):
            raise ValueError(f"row {len(rows)}: channels of unequal length")
        if shape is None:
            shape = this
        elif this != shape:
            raise ValueError(f"row {len(rows)}: shape {this} != {shape}")
        rows.append(np.concatenate(series))
        labels.append(label.strip())
    if not rows:
        raise ValueError("no data rows")
    channels, length = shape
    # The file's own header must agree with its rows.
    if "serieslength" in header and int(header["serieslength"]) != length:
        raise ValueError(f"rows have length {length}, header says "
                         f"{header['serieslength']}")
    if "dimensions" in header and int(header["dimensions"]) != channels:
        raise ValueError(f"rows have {channels} channels, header says "
                         f"{header['dimensions']}")
    return np.vstack(rows), labels, length, channels


def _read_half(zf: zipfile.ZipFile, name: str, half: str):
    member = f"{name}_{half}.ts"
    matches = [m for m in zf.namelist() if m.split("/")[-1] == member]
    if len(matches) != 1:
        raise ValueError(f"expected one {member} in the zip, found {matches}")
    return parse_ts(zf.read(matches[0]).decode("utf-8", errors="replace"))


def fetch(name: str, expected: Tuple[int, int, int, int],
          force: bool = False, pin: bool = False) -> Dict:
    dest = TSC_DIR / name
    dest.mkdir(parents=True, exist_ok=True)
    raw = dest / f"{name}.zip"
    npz = dest / f"{name}.npz"

    if force or not raw.is_file() or raw.stat().st_size == 0:
        _download(URL.format(name=name), raw)
    digest = sha256(raw)
    pinned = EXPECTED_SHA256.get(name)
    if pinned is None and not pin:
        raise ValueError(f"not pinned (sha256 {digest}); check the file, "
                         f"then pin it or rerun with --pin")
    if pinned is not None and digest != pinned:
        raise ValueError(f"sha256 {digest} != pinned {pinned}")

    with zipfile.ZipFile(raw) as zf:
        X_tr, y_tr, len_tr, ch_tr = _read_half(zf, name, "TRAIN")
        X_te, y_te, len_te, ch_te = _read_half(zf, name, "TEST")
    if (len_tr, ch_tr) != (len_te, ch_te):
        raise ValueError(f"TRAIN is {ch_tr}x{len_tr}, TEST {ch_te}x{len_te}")
    X = np.vstack([X_tr, X_te])
    labels = np.array(y_tr + y_te)
    origin = np.r_[np.zeros(len(y_tr), int), np.ones(len(y_te), int)]

    got = (X.shape[0], len_tr, ch_tr, int(np.unique(labels).size))
    if got != expected:
        raise ValueError(f"(examples, length, channels, classes) {got} "
                         f"!= archive's {expected}")

    ok = ~np.isnan(X).any(axis=1)
    dropped_missing = int((~ok).sum())
    X, labels, origin = X[ok], labels[ok], origin[ok]

    classes = np.unique(labels)
    y = classes.searchsorted(labels).astype(int)
    if ch_tr == 1:
        names = np.array([f"t{t}" for t in range(len_tr)])
    else:
        names = np.array([f"c{c}_t{t}" for c in range(ch_tr)
                          for t in range(len_tr)])
    np.savez_compressed(npz, X=X.astype(np.float32), y=y, feature_names=names,
                        class_names=classes, origin=origin,
                        dropped_missing=dropped_missing)

    (dest / "SHA256SUMS").write_text(
        f"{digest}  {raw.name}\n{sha256(npz)}  {npz.name}\n", encoding="utf-8")
    return {"rows": int(X.shape[0]), "features": int(X.shape[1]),
            "classes": int(classes.size), "dropped_missing": dropped_missing,
            "mb": raw.stat().st_size / 1e6, "sha256": digest}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="comma-separated names")
    ap.add_argument("--cluster", default=None, help="e.g. C2")
    ap.add_argument("--force", action="store_true",
                    help="download again even if the zip is on disk")
    ap.add_argument("--pin", action="store_true",
                    help="accept a dataset not yet pinned, and print the "
                         "digests to paste into EXPECTED_SHA256")
    args = ap.parse_args()

    names = list(TSC_DATASETS)
    if args.only:
        names = [n.strip() for n in args.only.split(",") if n.strip()]
        unknown = [n for n in names if n not in TSC_DATASETS]
        if unknown:
            raise SystemExit(f"unknown: {unknown}; have {list(TSC_DATASETS)}")
    if args.cluster:
        names = [n for n in names if TSC_DATASETS[n] == args.cluster]

    shapes = _expected_shapes()
    print(f"  {'dataset':<30}{'cl':>3}{'MB':>9}{'rows':>8}{'features':>10}"
          f"{'classes':>9}{'dropped':>9}")
    failures, new_pins = {}, {}
    for name in names:
        try:
            r = fetch(name, shapes[name], force=args.force, pin=args.pin)
        except Exception as exc:
            failures[name] = f"{type(exc).__name__}: {exc}"
            print(f"  {name:<30}{TSC_DATASETS[name]:>3}  FAILED  {failures[name]}")
            continue
        print(f"  {name:<30}{TSC_DATASETS[name]:>3}{r['mb']:9.1f}{r['rows']:>8,}"
              f"{r['features']:>10,}{r['classes']:>9}{r['dropped_missing']:>9}")
        if name not in EXPECTED_SHA256:
            new_pins[name] = r["sha256"]
    if new_pins:
        print("\nnot yet pinned -- add to EXPECTED_SHA256:")
        for n, d in new_pins.items():
            print(f'    "{n}": "{d}",')
    if failures:
        print("\nfailed:")
        for n, e in failures.items():
            print(f"  {n}: {e}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
