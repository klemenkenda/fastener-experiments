#!/bin/bash
# The data job of a submission: downloads and converts the datasets
# (prepare_data.sh). submit.sh passes the experiment file, the account and
# the output path; the array jobs start only if this one succeeds.
#SBATCH --job-name=fastener-data
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=04:00:00
set -euo pipefail
bash "$REPO_DIR/hpc/vega/prepare_data.sh" "$EXPERIMENT_FILE"
