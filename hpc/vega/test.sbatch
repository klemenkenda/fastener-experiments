#!/bin/bash
# The test job of a submission: one quick run of the real code with the
# experiment's options, on Coffee, before the arrays may start. It checks
# what the experiment's jobs need -- the environment unpacks and imports,
# the FASTENER clone and the data are found, the forest runs, a run folder
# is written -- in about five minutes instead of discovering a problem in
# 2,000 jobs. Not evidence: it runs without --experiment, as `vegatest`.
#SBATCH --job-name=fastener-test
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --time=00:30:00
export PATH=/usr/bin:/bin
set -euo pipefail
. "$REPO_DIR/hpc/vega/config.sh"
. "$EXPERIMENT_FILE"
cd "$REPO"
echo "node: $(hostname)  $(date)"
t0=$(date +%s)
use_env
echo "environment unpacked in $(( $(date +%s) - t0 )) s"
# shellcheck disable=SC2086  # RUN_ARGS is a list of arguments
"$PY" experiments/run_sota.py --dataset Coffee --quick --seed 2020 \
    --methods kbest_anova_f,boruta,nsga2_sparse --fastener-arm guided \
    --name vegatest --model-jobs "$SLURM_CPUS_PER_TASK" \
    --n-jobs "$SLURM_CPUS_PER_TASK" $RUN_ARGS
echo "test passed: $(date)"
