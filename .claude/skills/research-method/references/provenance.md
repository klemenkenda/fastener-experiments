# Provenance: manifests, method IDs, the dirty-tree rule

Sandve et al.'s rules, made mechanical: track how every result was produced,
archive exact versions, version all code, record seeds, keep the data behind
every plot, and link every claim in the text to a result.

## What each run writes

`results/<run ID>/manifest.json`, written when the run starts and updated when
it ends:

| field | content |
|---|---|
| `run_id` | `<UTC timestamp>_<name>`, e.g. `20261029T081500Z_h4` |
| `experiment_id` | `H4-E03`, or `null` for a run that is not evidence |
| `git` | per repository: commit, short commit, branch, `dirty`, untracked files |
| `evidence` | `false` if any tree was dirty or the run was not tagged |
| `packages` | versions of the interpreter and every relevant library |
| `inputs` | path and SHA-256 of every input data file (or a data-tool version) |
| `seeds` | every seed used |
| `config` | the fully resolved configuration, after defaults and CLI flags |
| `methods` | the method ID of each arm |
| `command` | the exact command line |
| `host` | machine, CPU and GPU, thread settings |
| `started_utc`, `ended_utc`, `status` | `running`, `ok`, `failed` |

Results files carry the method ID on every row, so a table can never mix two
versions of an arm by accident.

## Method ID

`<arm>@<commit>[+<other repo commit>...]#<config hash>`

- The commits are 7-character short hashes of every repository whose code the
  arm runs: the analysis repo, a vendored library, a fork.
- The config hash is the first 4 hex digits of the SHA-256 of the arm's
  resolved configuration as sorted, compact JSON. It changes when a flag
  changes behaviour without a commit.
- A dirty tree adds the suffix `-dirty`.

## Minimal implementation

```python
import datetime, hashlib, json, platform, subprocess, sys
from importlib import metadata
from pathlib import Path

NON_CODE = ("results/", "data/", "reports/")   # outputs, not code


def git_state(repo="."):
    def g(*a):
        return subprocess.run(["git", "-C", repo, *a], capture_output=True,
                              text=True, check=True).stdout.strip()
    changed = [l[3:] for l in g("status", "--porcelain").splitlines()]
    code = [p for p in changed if not p.startswith(NON_CODE)
            and "__pycache__" not in p and not p.endswith(".pyc")]
    return {"commit": g("rev-parse", "HEAD"), "short": g("rev-parse", "--short=7", "HEAD"),
            "branch": g("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": bool(code), "changed": code}


def config_hash(config):
    blob = json.dumps(config, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:4]


def method_id(arm, config, repos):
    commits = "+".join(r["short"] for r in repos)
    dirty = "-dirty" if any(r["dirty"] for r in repos) else ""
    return f"{arm}@{commits}#{config_hash(config)}{dirty}"


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def start_run(name, experiment_id, arms, inputs, seeds, packages,
              repos=(".",), allow_dirty=False, root="results"):
    states = [git_state(r) for r in repos]
    if experiment_id and any(s["dirty"] for s in states) and not allow_dirty:
        raise SystemExit("uncommitted code: commit before running for evidence")
    run_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + f"_{name}"
    out = Path(root) / run_id
    out.mkdir(parents=True)
    manifest = {
        "run_id": run_id, "experiment_id": experiment_id,
        "evidence": bool(experiment_id) and not any(s["dirty"] for s in states),
        "git": dict(zip(repos, states)),
        "packages": {"python": sys.version.split()[0],
                     **{p: metadata.version(p) for p in packages}},
        "inputs": {str(p): file_hash(p) for p in inputs},
        "seeds": list(seeds),
        "config": arms, "methods": {a: method_id(a, c, states) for a, c in arms.items()},
        "command": sys.argv, "host": platform.node(),
        "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "running",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return out, manifest
```

Close the run by setting `ended_utc` and `status` in the same file. Add the
run ID to the experiment's ledger row, under a file lock if runs start in
parallel. Refuse runs for an experiment whose status is no longer `running`.

## What counts as code

Code: source, configs, the plan, the methodology, analysis and figure scripts,
untracked modules (they can be imported). Not code: what runs write
(`results/`, generated data, `reports/`, the ledger). Anything a reader would
need to regenerate a number must be committed.

## Tools that can do part of this

Experiment trackers (MLflow, Weights & Biases, Sacred, Aim) record parameters,
metrics and the git commit. Data-versioning tools (DVC, git-annex, LakeFS) pin
data. Either may replace parts of the manifest. They do not replace the plan,
the ledger, the decision log or the dirty-tree refusal. Record the tracker's
run ID in the manifest, and the manifest's run ID in the tracker.
