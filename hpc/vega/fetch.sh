#!/bin/bash
# Bring an experiment's results home from Vega. Run on YOUR machine, in this
# repository: Git Bash on Windows, or any Linux/macOS shell. It needs only
# ssh and tar, so no rsync or WinSCP.
#
#   VEGA_HOST=<user>@login.vega.izum.si \
#   VEGA_REPO=/ceph/hpc/data/<project>/fastener-experiments \
#   bash hpc/vega/fetch.sh hpc/vega/h5h6e02.env
#
# It copies the experiment's queue folder (results/<ID>/: job list, states,
# logs) and every run folder (results/*_<id>_*), streamed as one tar archive.
# Then it adds the experiment's runs from Vega's ledger to the local
# experiments/EXPERIMENTS.md row, so nothing has to be committed or pushed
# from the cluster. Running it again fetches everything again and adds only
# the runs not yet in the ledger.
#
# NO_TRAJECTORIES=1 leaves out the per-run trajectories/ folders, which are
# most of the volume. The report's progress and timeout figures need them.
set -euo pipefail
: "${VEGA_HOST:?set VEGA_HOST, e.g. user@login.vega.izum.si}"
: "${VEGA_REPO:?set VEGA_REPO, path of the repository on Vega}"
. "$1"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="${PYTHON:-python}"
prefix="$(echo "$EXPERIMENT" | tr 'A-Z' 'a-z' | tr -d '-')"

exclude=""
[ "${NO_TRAJECTORIES:-0}" = 1 ] && exclude="--exclude=*/trajectories"

cd "$REPO"   # unpack relative to the repository (tar would read "E:" as a host)
mkdir -p results
# shellcheck disable=SC2029  # expanded here on purpose
ssh "$VEGA_HOST" "cd '$VEGA_REPO' && tar czf - $exclude results/$EXPERIMENT \
    \$(ls -d results/*_${prefix}_* 2>/dev/null)" | tar xzf -
echo "results: $(ls -d results/*_"${prefix}"_* 2>/dev/null | wc -l) run folders, and results/$EXPERIMENT"

ledger="$(mktemp)"
ssh "$VEGA_HOST" "cat '$VEGA_REPO/experiments/EXPERIMENTS.md'" > "$ledger"
"$PY" experiments/hpc_jobs.py merge-ledger --experiment "$EXPERIMENT" --from "$ledger"
rm -f "$ledger"
echo "next: python experiments/make_report.py --experiment $EXPERIMENT"
