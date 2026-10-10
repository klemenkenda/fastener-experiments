"""The dirty check that decides whether a run is evidence."""
import subprocess

import pytest

from provenance import NON_CODE_PATHS, git_state


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "t")
    (tmp_path / "experiments").mkdir()
    (tmp_path / "experiments" / "run.py").write_text("x = 1\n")
    (tmp_path / "experiments" / "EXPERIMENTS.md").write_text("ledger\n")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "init")
    return tmp_path


def test_the_ledger_lock_does_not_make_the_code_dirty(repo):
    (repo / "experiments" / "EXPERIMENTS.md.lock").write_text("12345")
    (repo / "experiments" / "EXPERIMENTS.md").write_text("ledger, one more run\n")
    st = git_state(repo, NON_CODE_PATHS)
    assert st["dirty"] and not st["code_dirty"]


def test_a_changed_script_still_does(repo):
    (repo / "experiments" / "run.py").write_text("x = 2\n")
    assert git_state(repo, NON_CODE_PATHS)["code_dirty"]
