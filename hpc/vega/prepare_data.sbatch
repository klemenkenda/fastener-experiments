#!/bin/bash
# The data job of a submission: downloads and converts the datasets
# (prepare_data.sh). submit.sh passes REPO_DIR and EXPERIMENT_FILE, the
# account and the output path; everything after it starts only if it
# succeeds.
#SBATCH --job-name=fastener-data
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=04:00:00
export PATH=/usr/bin:/bin
set -euo pipefail
bash "$REPO_DIR/hpc/vega/prepare_data.sh" "$EXPERIMENT_FILE"
