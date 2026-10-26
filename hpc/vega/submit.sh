#!/bin/bash
# Submit an experiment to Vega: a data job (download, verify, convert), then
# the experiment's jobs as SLURM arrays that start only once the data job has
# succeeded. Run on a login node, after setup.sh:
#
#   bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
#   SKIP_DATA=1 bash hpc/vega/submit.sh hpc/vega/h5h6e02.env   # data already there
#
# Resubmitting after an interruption is safe: the job list must be the one
# already emitted, and a job already done or timed out is not run again.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/config.sh"
EXPERIMENT_FILE="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
. "$EXPERIMENT_FILE"
cd "$REPO"

[ -x "$PY" ] || { echo "no Python at $PY; run hpc/vega/setup.sh first" >&2; exit 1; }
# The check each run makes (provenance.NON_CODE_PATHS: the ledger, results
# and data may change; code may not), made once here rather than in 2,000 jobs.
"$PY" - <<'EOF'
import sys
sys.path.insert(0, "experiments")
from provenance import NON_CODE_PATHS, REPO_ROOT, git_state
s = git_state(REPO_ROOT, NON_CODE_PATHS)
if s.get("code_dirty"):
    sys.exit("uncommitted code; runs with --experiment would refuse:\n  "
             + "\n  ".join(s["code_dirty_files"]))
EOF

# shellcheck disable=SC2086  # RUN_ARGS is a list of arguments
"$PY" experiments/hpc_jobs.py emit --experiment "$EXPERIMENT" \
    --datasets "$DATASETS" --methods "$METHODS" --budgets "$BUDGETS" \
    --skip "@$SKIP" --timeout-hours "$TIMEOUT_HOURS" -- $RUN_ARGS
N="$("$PY" experiments/hpc_jobs.py count --experiment "$EXPERIMENT")"

OUT="$REPO/results/$EXPERIMENT/slurm"
mkdir -p "$OUT"
common=(--parsable --partition "$PARTITION" --export=ALL)
[ -n "$ACCOUNT" ] && common+=(--account "$ACCOUNT")
export REPO_DIR="$REPO" EXPERIMENT EXPERIMENT_FILE PY_BIN="$PY"

dep=()
if [ "${SKIP_DATA:-0}" != 1 ]; then
    data_job="$(sbatch "${common[@]}" --output "$OUT/data_%j.out" \
        "$REPO/hpc/vega/prepare_data.sbatch")"
    echo "data job: $data_job"
    dep=(--dependency "afterok:$data_job")
fi

# The SLURM limit: the experiment's cap plus 15 minutes for start-up and the
# final write, so that hpc_jobs.py, not SLURM, is what stops a long job.
limit="$("$PY" -c "m = int(round(float('$TIMEOUT_HOURS') * 60)) + 15; print(f'{m // 60:02d}:{m % 60:02d}:00')")"

for ((off = 0; off < N; off += ARRAY_CHUNK)); do
    last=$(( (N - off < ARRAY_CHUNK ? N - off : ARRAY_CHUNK) - 1 ))
    job="$(sbatch "${common[@]}" "${dep[@]}" \
        --array "0-$last%$MAX_PARALLEL" \
        --cpus-per-task "$CPUS" --mem "$MEM" --time "$limit" \
        --export "ALL,HPC_INDEX_OFFSET=$off" \
        --output "$OUT/task_%A_%a.out" \
        "$REPO/hpc/vega/run_array.sbatch")"
    echo "array job $job: jobs $off-$((off + last))"
done
echo "$N jobs of $EXPERIMENT submitted, $CPUS cores and $MEM each, limit $limit"
echo "progress: bash hpc/vega/status.sh $1"
