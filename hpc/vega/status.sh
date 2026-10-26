#!/bin/bash
# Where an experiment on Vega stands: gathers the array tasks' states into
# results/<ID>/queue.json and shows it with the usual monitor.
#
#   bash hpc/vega/status.sh hpc/vega/h5h6e02.env
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/config.sh"
. "$1"
cd "$REPO"
use_env
export HPC_MAX_PARALLEL="$MAX_PARALLEL"   # the ETA's cap on slots
"$PY" experiments/hpc_jobs.py collect --experiment "$EXPERIMENT"
"$PY" experiments/monitor.py --experiment "$EXPERIMENT" --once
