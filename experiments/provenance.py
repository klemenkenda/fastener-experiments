"""Provenance capture: make every run reconstructible after the fact.

A run records, in its own timestamped directory:
  * the git commit of BOTH repos (experiments + the fastener clone), incl. dirty flag
  * the exact interpreter and versions of every relevant package
  * the dataset files actually used, by SHA256
  * every seed and hyperparameter
  * a wall-clock start/end and the command line

Nothing here imports FASTENER, so it is safe to use from any script.
"""
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
FASTENER_DIR = REPO_ROOT / "fastener"
RESULTS_DIR = REPO_ROOT / "results"
DATA_DIR = REPO_ROOT / "data"


def _git(repo: Path, *args: str) -> Optional[str]:
    """Run a git command in `repo`, returning stripped stdout or None."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(repo),
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def git_state(repo: Path) -> Dict[str, Any]:
    """Commit, branch, dirty flag and remote for one repository."""
    if not (repo / ".git").exists():
        return {"path": str(repo), "available": False}
    status = _git(repo, "status", "--porcelain")
    return {
        "path": str(repo),
        "available": True,
        "commit": _git(repo, "rev-parse", "HEAD"),
        "branch": _git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "remote": _git(repo, "config", "--get", "remote.origin.url"),
        # A dirty tree means the recorded commit does NOT fully describe the code.
        "dirty": bool(status),
        "dirty_files": status.splitlines() if status else [],
    }


def environment() -> Dict[str, Any]:
    """Interpreter and package versions."""
    pkgs: Dict[str, Optional[str]] = {}
    for name in ("numpy", "scipy", "sklearn", "pandas", "matplotlib"):
        try:
            mod = __import__(name)
            pkgs[name] = getattr(mod, "__version__", None)
        except ImportError:
            pkgs[name] = None
    return {
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "packages": pkgs,
    }


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hash_tree(root: Path, patterns=("*",)) -> Dict[str, Dict[str, Any]]:
    """SHA256 + size of every matching file under `root`, keyed by relative path."""
    out: Dict[str, Dict[str, Any]] = {}
    if not root.is_dir():
        return out
    for pattern in patterns:
        for p in sorted(root.rglob(pattern)):
            if p.is_file():
                rel = p.relative_to(root).as_posix()
                out[rel] = {"sha256": sha256(p), "bytes": p.stat().st_size}
    return out


class Run:
    """A single traceable experiment run backed by its own directory."""

    def __init__(self, name: str, params: Optional[Dict[str, Any]] = None,
                 root: Optional[Path] = None) -> None:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.name = name
        self.run_id = f"{stamp}_{name}"
        self.dir = (root or RESULTS_DIR) / self.run_id
        self.dir.mkdir(parents=True, exist_ok=False)
        self._t0 = time.time()
        self.manifest: Dict[str, Any] = {
            "run_id": self.run_id,
            "name": name,
            "started_utc": datetime.now(timezone.utc).isoformat(),
            "command": " ".join([Path(sys.argv[0]).name, *sys.argv[1:]]),
            "params": params or {},
            "git": {
                "experiments": git_state(REPO_ROOT),
                "fastener": git_state(FASTENER_DIR),
            },
            "environment": environment(),
        }

    def record(self, key: str, value: Any) -> None:
        self.manifest[key] = value

    def record_inputs(self, **files: Path) -> None:
        """Hash each input file so the run is pinned to exact data bytes."""
        self.manifest.setdefault("inputs", {})
        for label, path in files.items():
            path = Path(path)
            self.manifest["inputs"][label] = {
                "path": str(path),
                "sha256": sha256(path) if path.is_file() else None,
                "bytes": path.stat().st_size if path.is_file() else None,
            }

    def write_json(self, filename: str, obj: Any) -> Path:
        path = self.dir / filename
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2, default=str)
        return path

    def finish(self, status: str = "ok", error: Optional[str] = None) -> Path:
        self.manifest["status"] = status
        if error:
            self.manifest["error"] = error
        self.manifest["ended_utc"] = datetime.now(timezone.utc).isoformat()
        self.manifest["elapsed_seconds"] = round(time.time() - self._t0, 3)

        # Hash the summary outputs individually. FASTENER's per-generation
        # pickles are numerous (thousands per run) and would bloat the manifest,
        # so they are rolled up into one digest-of-digests instead: enough to
        # detect any change, without a 500KB manifest.
        outputs, bulk = {}, {}
        for path in sorted(self.dir.rglob("*")):
            if not path.is_file() or path.name == "manifest.json":
                continue
            rel = path.relative_to(self.dir).as_posix()
            entry = {"sha256": sha256(path), "bytes": path.stat().st_size}
            if rel.startswith("log/"):
                bulk[rel] = entry
            else:
                outputs[rel] = entry

        self.manifest["outputs"] = outputs
        if bulk:
            rollup = hashlib.sha256()
            for rel in sorted(bulk):
                rollup.update(rel.encode())
                rollup.update(bulk[rel]["sha256"].encode())
            self.manifest["bulk_outputs"] = {
                "prefix": "log/",
                "n_files": len(bulk),
                "total_bytes": sum(e["bytes"] for e in bulk.values()),
                "rollup_sha256": rollup.hexdigest(),
                "note": ("FASTENER per-generation pickles. Digest of the sorted "
                         "(path, sha256) pairs; recompute to verify."),
            }
        return self.write_json("manifest.json", self.manifest)

    def __enter__(self) -> "Run":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.finish(
            status="ok" if exc_type is None else "failed",
            error=None if exc is None else f"{exc_type.__name__}: {exc}",
        )
        return False
