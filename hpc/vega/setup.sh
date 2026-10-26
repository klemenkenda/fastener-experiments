#!/bin/bash
# One-time setup on a Vega login node (it needs the internet): the Python
# environment and the FASTENER clone, both inside the repository and both
# git-ignored, so the experiments tree stays clean.
#
#   bash hpc/vega/setup.sh
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/config.sh"
cd "$REPO"

# --- Python: Miniforge, so nothing depends on the cluster's module names.
if [ ! -x "$PY" ]; then
    if [ ! -x "$MINIFORGE_DIR/bin/conda" ]; then
        installer="$(mktemp -d)/miniforge.sh"
        curl -fsSL -o "$installer" \
            "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh"
        bash "$installer" -b -p "$MINIFORGE_DIR"
        rm -f "$installer"
    fi
    "$MINIFORGE_DIR/bin/conda" create -y -p "$ENV_DIR" "python=$PYTHON_VERSION" pip
fi
"$PY" -m pip install --upgrade pip
"$PY" -m pip install -r requirements.txt

# --- FASTENER at the commit the experiments use.
if [ ! -d fastener/.git ]; then
    git clone "$FASTENER_URL" fastener
fi
git -C fastener fetch --quiet origin
git -C fastener checkout --quiet "$FASTENER_COMMIT"

echo
echo "python:   $("$PY" --version) at $PY"
echo "fastener: $(git -C fastener log --oneline -1)"
"$PY" -c "import sklearn, numpy; print('sklearn', sklearn.__version__, 'numpy', numpy.__version__)"
if [ -n "$(git status --porcelain)" ]; then
    echo "WARNING: the experiments tree is not clean; runs with --experiment will refuse:"
    git status --porcelain
fi
