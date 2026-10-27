#!/bin/bash
# Bring an experiment's results home from Vega. Run on YOUR machine, in this
# repository: Git Bash on Windows, or any Linux/macOS shell. It needs only
# ssh and tar, so no rsync or WinSCP.
#
#   VEGA_HOST=kendak@login.vega.izum.si \
#   VEGA_REPO=/ceph/hpc/home/kendak/fastener-experiments \
#   PYTHON=/c/Users/klemen/.conda/envs/fastener-exp/python.exe \
#   bash hpc/vega/fetch.sh hpc/vega/h5h6e02.env
#
# One compressed tar stream over ssh, in this order:
#
# 1. every run folder, results/*_<id>_*, without FASTENER's experiment.pickle
#    (its start-of-run state, which nothing reads: tens of MB a run, and
#    under H5H6-E02's first FASTENER jobs gigabytes);
# 2. the experiment's queue folder, results/<ID>/ -- job list, status files,
#    logs -- without the SLURM outputs (one per task attempt, thousands).
#
# Then it records each job's latest run in the local experiments/EXPERIMENTS.md
# row, from the status files, so nothing has to be committed or pushed from
# the cluster. Running it again fetches everything again and adds only the
# runs not yet in the ledger.
#
# NO_TRAJECTORIES=1 also leaves out the per-run trajectories/ folders. The
# report's progress and timeout figures need them.
#
# On 2026-10-27 H5H6-E02's results -- 2,359 run folders and 2,202 logs --
# came home this way in about 25 minutes.
set -euo pipefail
: "${VEGA_HOST:?set VEGA_HOST, e.g. kendak@login.vega.izum.si}"
: "${VEGA_REPO:?set VEGA_REPO, path of the repository on Vega}"
. "$1"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PY="${PYTHON:-python}"
prefix="$(echo "$EXPERIMENT" | tr '[:upper:]' '[:lower:]' | tr -d -- '-')"

excludes="--exclude='*/experiment.pickle' --exclude='results/$EXPERIMENT/slurm'"
[ "${NO_TRAJECTORIES:-0}" = 1 ] && excludes="$excludes --exclude='*/trajectories'"

cd "$REPO"   # unpack relative to the repository (tar would read "E:" as a host)
mkdir -p results
echo "fetching $EXPERIMENT from $VEGA_HOST:$VEGA_REPO (passphrase and 2FA next)"
# shellcheck disable=SC2029  # expanded here on purpose
ssh "$VEGA_HOST" "cd '$VEGA_REPO' && tar czf - $excludes \$(ls -d results/*_${prefix}_*) results/$EXPERIMENT" \
    | tar xzvf - | awk 'NR % 500 == 0 {print NR " files..."; fflush()}'
echo "results: $(ls -d results/*_"${prefix}"_* 2>/dev/null | wc -l) run folders, and results/$EXPERIMENT"

# The runs, from the status files just fetched: each job's latest run. Not
# from Vega's ledger, where the jobs of the first submissions recorded
# themselves -- among them FASTENER runs replaced by reruns (DEC-42).
"$PY" experiments/hpc_jobs.py ledger --experiment "$EXPERIMENT"
echo "next: python experiments/make_report.py --experiment $EXPERIMENT"
