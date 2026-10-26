#!/bin/bash
# One array task = one job of the experiment (experiments/hpc_jobs.py run):
# one dataset, one arm, one seed. The array index is the job's index in
# results/<ID>/jobs.json. submit.sh sets the indices, cores, memory, time
# limit, account and output path, and passes only REPO_DIR and EXPERIMENT.
#
# The Python environment is unpacked onto this node's local disk and removed
# at the end (env.sh); nothing is installed on or read file by file from Ceph.
#
# hpc_jobs.py stops the job at the experiment's per-run cap and records it as
# timed out; the SLURM time limit is set a little above the cap, so that it
# only ever catches a task that hangs outside the job itself.
#SBATCH --job-name=fastener
#SBATCH --ntasks=1
export PATH=/usr/bin:/bin
set -euo pipefail
. "$REPO_DIR/hpc/vega/config.sh"
cd "$REPO"
use_env
"$PY" experiments/hpc_jobs.py run --experiment "$EXPERIMENT" \
    --cpus "$SLURM_CPUS_PER_TASK"
