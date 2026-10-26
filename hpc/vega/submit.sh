#!/bin/bash
# Submit an experiment to Vega: a data job (download, verify, convert), then
# the experiment's jobs as SLURM arrays that start only once the data job has
# succeeded. Run on a login node (login.vega.izum.si), after setup.sh:
#
#   bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
#   SKIP_DATA=1 bash hpc/vega/submit.sh hpc/vega/h5h6e02.env   # data already there
#   MEM=32G SKIP_DATA=1 bash hpc/vega/submit.sh ...            # rerun with more memory
#
# Only unfinished jobs are submitted: a job already done or timed out is left
# alone, so a resubmission after an interruption, or after jobs failed for
# memory, schedules just the work left. Jobs run as two arrays: the cells in
# the experiment's HIGHMEM_CELLS file with HIGHMEM, all others with MEM.
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

NAME="fastener-$EXPERIMENT"
if [ "${FORCE:-0}" != 1 ] && [ -n "$(squeue -h -u "$USER" -n "$NAME,$NAME-data" -o %i)" ]; then
    echo "jobs of $EXPERIMENT are still queued or running (squeue -u $USER -n $NAME);" >&2
    echo "wait for them or scancel them first, so no job runs twice (FORCE=1 overrides)" >&2
    exit 1
fi

# shellcheck disable=SC2086  # RUN_ARGS is a list of arguments
"$PY" experiments/hpc_jobs.py emit --experiment "$EXPERIMENT" \
    --datasets "$DATASETS" --methods "$METHODS" --budgets "$BUDGETS" \
    --skip "@$SKIP" --timeout-hours "$TIMEOUT_HOURS" -- $RUN_ARGS
N="$("$PY" experiments/hpc_jobs.py count --experiment "$EXPERIMENT")"
if [ "$N" -gt $((MAX_ARRAY_INDEX + 1)) ]; then
    echo "$N jobs: more than one array can index ($((MAX_ARRAY_INDEX + 1)))" >&2
    exit 1
fi

highmem=(); [ -n "${HIGHMEM_CELLS:-}" ] && highmem=(--cells "@$HIGHMEM_CELLS")
normal_idx="$("$PY" experiments/hpc_jobs.py indices --experiment "$EXPERIMENT" \
    --unfinished "${highmem[@]}" ${HIGHMEM_CELLS:+--invert})"
high_idx=""
[ -n "${HIGHMEM_CELLS:-}" ] && high_idx="$("$PY" experiments/hpc_jobs.py indices \
    --experiment "$EXPERIMENT" --unfinished "${highmem[@]}")"
if [ -z "$normal_idx$high_idx" ]; then
    echo "every job of $EXPERIMENT is done or timed out; nothing to submit"
    exit 0
fi

OUT="$REPO/results/$EXPERIMENT/slurm"
mkdir -p "$OUT"
common=(--parsable --partition "$PARTITION" --export=ALL)
[ -n "$ACCOUNT" ] && common+=(--account "$ACCOUNT")
export REPO_DIR="$REPO" EXPERIMENT EXPERIMENT_FILE PY_BIN="$PY"

dep=()
if [ "${SKIP_DATA:-0}" != 1 ]; then
    data_job="$(sbatch "${common[@]}" --job-name "$NAME-data" \
        --output "$OUT/data_%j.out" "$REPO/hpc/vega/prepare_data.sbatch")"
    echo "data job: $data_job"
    dep=(--dependency "afterok:$data_job")
fi

# The SLURM limit: the experiment's cap plus 15 minutes for start-up and the
# final write, so that hpc_jobs.py, not SLURM, is what stops a long job.
limit="$("$PY" -c "m = int(round(float('$TIMEOUT_HOURS') * 60)) + 15; print(f'{m // 60:02d}:{m % 60:02d}:00')")"

submit() {  # $1 = array indices, $2 = memory
    [ -n "$1" ] || return 0
    local job
    job="$(sbatch "${common[@]}" "${dep[@]}" --job-name "$NAME" \
        --array "$1%$MAX_PARALLEL" \
        --cpus-per-task "$CPUS" --mem "$2" --time "$limit" \
        --output "$OUT/task_%A_%a.out" \
        "$REPO/hpc/vega/run_array.sbatch")"
    echo "array job $job: $(echo "$1" | tr ',' '\n' | awk -F- '{n += ($2 == "" ? 1 : $2 - $1 + 1)} END {print n}') jobs, $CPUS cores, $2"
}
submit "$normal_idx" "$MEM"
submit "$high_idx" "$HIGHMEM"

# The worst case for the budget: every submitted job running to the cap.
"$PY" - "$normal_idx" "$high_idx" "$CPUS" "$MEM" "$HIGHMEM" "$TIMEOUT_HOURS" <<'EOF'
import sys
def count(spec):
    return sum((int(b) - int(a) + 1) if b else 1
               for a, _, b in (r.partition("-") for r in spec.split(",") if r))
def gb(m):
    return float(m.rstrip("Gg"))
normal, high, cpus, mem, highmem, hours = sys.argv[1:]
cpus, hours = int(cpus), float(hours) + 0.25
# Billing: CPU 1.0 per core, memory 1.0 per GB; a job is billed for the
# larger of the two if SLURM uses MAX_TRES, the sum otherwise -- take the sum.
bill = count(normal) * (cpus + gb(mem)) + count(high) * (cpus + gb(highmem))
print(f"worst case, every job to the cap: {bill * hours / 256:,.0f} node-hours "
      f"of billing (256 per node); runs that finish early cost far less")
EOF
echo "progress: bash hpc/vega/status.sh $1"
