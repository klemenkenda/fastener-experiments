#!/bin/bash
# One-time setup: the Python environment, as ONE archive on Ceph, and the
# FASTENER clone. Run on a login node, which has the internet:
#
#   bash hpc/vega/setup.sh
#
# or as a short job, if the login node is busy:
#
#   sbatch -p cpu -A s26t11-01-users -t 00:30:00 -c 4 --mem=8G \
#       -o setup-%j.out --wrap "bash $PWD/hpc/vega/setup.sh"
#
# The environment is built on local disk ($LOCAL_TMP), packed with conda-pack
# into .hpc/env.tar.gz, and the build folder deleted. Nothing but that one
# file is written to Ceph: on 2026-10-26 an install of tens of thousands of
# small files straight into the home directory took an hour and hung. Every
# job unpacks the archive onto its node's local disk (env.sh). Run again to
# rebuild it, e.g. after requirements.txt changes.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/config.sh"
cd "$REPO"

BUILD="$(mktemp -d "$LOCAL_TMP/fastener-build-$USER.XXXXXX")"
trap 'rm -rf "$BUILD"' EXIT
echo "building in $BUILD (local disk)"

# --- micromamba: one static binary.
curl -fsSL "$MICROMAMBA_URL" -o "$BUILD/mm.tar.bz2"
tar -xjf "$BUILD/mm.tar.bz2" -C "$BUILD" bin/micromamba
export MAMBA_ROOT_PREFIX="$BUILD/mamba"

# --- Python, conda-pack and LightGBM from conda-forge, everything else from
# pip, as on the machine that ran H5H6-E01 (requirements.txt). LightGBM comes
# from conda-forge so that the OpenMP runtime it links to comes with it,
# rather than from the compute nodes' system libraries.
"$BUILD/bin/micromamba" create -y -q -p "$BUILD/env" -c conda-forge \
    "python=$PYTHON_VERSION" pip conda-pack "lightgbm>=4.0"
"$BUILD/env/bin/python" -m pip install --no-cache-dir -q -r requirements.txt
"$BUILD/env/bin/python" -c "import numpy, scipy, sklearn, pandas, boruta, skrebate, pyHSICLasso, lightgbm; print('python ok: sklearn', sklearn.__version__, 'numpy', numpy.__version__, 'lightgbm', lightgbm.__version__)"

# --- Pack, then copy the single file to Ceph.
"$BUILD/env/bin/conda-pack" -q -p "$BUILD/env" -o "$BUILD/env.tar.gz" \
    --n-threads 4 --compress-level 4
mkdir -p "$(dirname "$ENV_ARCHIVE")"
cp "$BUILD/env.tar.gz" "$ENV_ARCHIVE.tmp"
mv "$ENV_ARCHIVE.tmp" "$ENV_ARCHIVE"
echo "environment: $ENV_ARCHIVE ($(du -h "$ENV_ARCHIVE" | cut -f1))"

# --- FASTENER at the commit the experiments use (a few dozen files).
if [ ! -d fastener/.git ]; then
    git clone -q "$FASTENER_URL" fastener
fi
git -C fastener fetch -q origin
git -C fastener checkout -q "$FASTENER_COMMIT"
echo "fastener: $(git -C fastener log --oneline -1)"

# --- Check that it unpacks and runs, as a job would.
rm -rf "$BUILD"
trap - EXIT
use_env
"$PY" -c "import sys; sys.path.insert(0, 'experiments'); import _bootstrap, protocol, run_sota; print('experiments import ok')"
"$PY" - <<'EOF'
import sys
sys.path.insert(0, "experiments")
from provenance import NON_CODE_PATHS, REPO_ROOT, git_state
s = git_state(REPO_ROOT, NON_CODE_PATHS)
print("code clean" if not s.get("code_dirty") else
      "WARNING: uncommitted code; runs with --experiment will refuse:\n  "
      + "\n  ".join(s["code_dirty_files"]))
EOF
echo "setup done"
