#!/bin/bash
# The test job of a submission, before the arrays may start, in about five
# minutes instead of discovering a problem in 2,000 jobs:
#
# 1. one quick run of the real code with the experiment's options, on
#    Coffee: the environment unpacks and imports, the FASTENER clone and the
#    data are found, the forest runs, a run folder is written. Not evidence:
#    it runs without --experiment, as `vegatest`;
# 2. one real job of the experiment, the cheapest (Coffee, all features),
#    through hpc_jobs.py exactly as an array task runs it. The first
#    submission of H5H6-E02 passed step 1 and failed every array task in
#    hpc_jobs.py; this catches that. The job counts as done, as any other.
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
echo "step 1 passed: run_sota.py"

index="$("$PY" experiments/hpc_jobs.py indices --experiment "$EXPERIMENT" \
    --cells "${TEST_CELL:-Coffee:all_features}")"
index="${index%%[-,]*}"  # the cell's first job
if [ -z "$index" ]; then
    echo "step 2: no job of $EXPERIMENT in cell ${TEST_CELL:-Coffee:all_features}; set TEST_CELL" >&2
    exit 1
fi
echo "step 2: job $index of $EXPERIMENT through hpc_jobs.py"
"$PY" experiments/hpc_jobs.py run --experiment "$EXPERIMENT" --index "$index" \
    --cpus "$SLURM_CPUS_PER_TASK"
echo "test passed: $(date)"
