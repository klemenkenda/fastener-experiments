#!/bin/bash
# One array task = one job of the experiment (experiments/hpc_jobs.py run):
# one dataset, one arm, one seed. The array index is the job's index in
# results/<ID>/jobs.json. submit.sh sets the indices, cores, memory, time
# limit, account and output path.
#
# hpc_jobs.py stops the job at the experiment's per-run cap and records it as
# timed out; the SLURM time limit is set a little above the cap, so that it
# only ever catches a task that hangs outside the job itself.
#SBATCH --job-name=fastener
#SBATCH --ntasks=1
set -euo pipefail
cd "$REPO_DIR"
"$PY_BIN" experiments/hpc_jobs.py run \
    --experiment "$EXPERIMENT" --cpus "$SLURM_CPUS_PER_TASK"
