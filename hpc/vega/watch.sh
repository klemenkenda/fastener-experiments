#!/bin/bash
# Watch an experiment on Vega until it is finished: every INTERVAL seconds
# (default 600), gather the jobs' states (hpc_jobs.py collect), show the
# monitor and the SLURM queue, and append a one-line summary to
# results/<ID>/watch.log. Stops by itself once no job of the experiment is
# queued or running; says so if the test or data job failed.
#
#   bash hpc/vega/watch.sh hpc/vega/h5h6e02.env
#   INTERVAL=300 bash hpc/vega/watch.sh hpc/vega/h5h6e02.env
#
# To keep it running after you log out, start it inside tmux or screen
# (`tmux new -s watch`, then the command; detach with Ctrl+B D, come back with
# `tmux attach -t watch`), or in the background:
#
#   nohup bash hpc/vega/watch.sh hpc/vega/h5h6e02.env > ~/watch.out 2>&1 &
#
# Every step has a timeout, so a slow file system makes a round late, never
# stuck. It only reads: it never submits, cancels or deletes anything.
set -uo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/config.sh"
. "$1"
cd "$REPO"
use_env
export HPC_MAX_PARALLEL="$MAX_PARALLEL"   # the ETA's cap on slots
: "${INTERVAL:=600}"
NAME="fastener-$EXPERIMENT"
LOG="$REPO/results/$EXPERIMENT/watch.log"
mkdir -p "$(dirname "$LOG")"

# Queued and running jobs of this experiment, by SLURM state.
queue_counts() {
    timeout 60 squeue -h -u "$USER" -n "$NAME,$NAME-data,$NAME-test" -o "%j %T" \
        | awk '{n[$1" "$2]++} END {for (k in n) printf "%s=%d  ", k, n[k]}'
}

# The data and test job of the latest submission, if one ended badly. Only
# that submission's: submit.sh rewrites jobs.json each time, so jobs started
# before it (an earlier attempt, fixed and resubmitted with SKIP_DATA=1) are
# no longer news. Two minutes of margin for clocks.
gate_failures() {
    local since
    since="$(date -d "$(date -r "$REPO/results/$EXPERIMENT/jobs.json" -Is) - 2 minutes" +%Y-%m-%dT%H:%M:%S)"
    timeout 60 sacct -n -X -P -u "$USER" -S "$since" \
        --name "$NAME-data,$NAME-test" -o JobID,JobName,State \
        | sort -t'|' -k1,1n \
        | awk -F'|' '{last[$2] = $3; id[$2] = $1}
                     END {for (n in last) if (last[n] !~ /COMPLETED|RUNNING|PENDING/)
                              print n" (job "id[n]"): "last[n]}'
}

while true; do
    clear
    echo "== $EXPERIMENT  $(date '+%a %d %b %H:%M')  (every ${INTERVAL}s; Ctrl+C stops watching, not the jobs)"
    summary="$(timeout 300 "$PY" experiments/hpc_jobs.py collect --experiment "$EXPERIMENT" 2>&1 | tail -1)"
    timeout 120 "$PY" experiments/monitor.py --experiment "$EXPERIMENT" --once 2>&1 | head -40
    queue="$(queue_counts)"
    echo
    echo "SLURM: ${queue:-nothing queued or running}"
    bad="$(gate_failures)"
    if [ -n "$bad" ]; then
        echo "!! $bad"
        echo "!! see results/$EXPERIMENT/slurm/ (data_*.out, test_*.out)"
    fi
    echo "$(date -Is)  ${summary}  |  ${queue:-idle}" >> "$LOG"

    if [ -z "$queue" ]; then
        echo
        echo "No job of $EXPERIMENT is queued or running any more: stopped watching."
        echo "Final states: $summary"
        echo "Failed jobs, if any:  grep -l '\"failed\"' results/$EXPERIMENT/status/*.json"
        exit 0
    fi
    sleep "$INTERVAL"
done
