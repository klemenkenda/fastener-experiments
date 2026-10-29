#!/bin/bash
# Download an experiment's datasets, check them against their pinned SHA256s,
# and build the .npz files the runs read. Run as the first job of a
# submission (prepare_data.sbatch), or by hand on a login node:
#
#   bash hpc/vega/prepare_data.sh hpc/vega/h5h6e02.env
#
# Every download is skipped when its file is already there and verified, so
# running it again costs little.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/config.sh"
. "$1"
cd "$REPO"
use_env

# Each dataset to its own downloader: the time series, the tall sets and
# H8's OpenML sets; eodata below.
read -r tsc_list tall_list h8_list <<< "$("$PY" - "$DATASETS" <<'EOF'
import sys
sys.path.insert(0, "experiments")
from datasets import H8_DATASETS, TALL_DATASETS
groups = {"tsc": [], "tall": [], "h8": []}
for d in filter(None, sys.argv[1].split(",")):
    if d == "eodata":
        continue
    groups["tall" if d in TALL_DATASETS else "h8" if d in H8_DATASETS else "tsc"].append(d)
print(" ".join(",".join(g) or "-" for g in groups.values()))
EOF
)"
[ "$tsc_list" = - ] || "$PY" experiments/download_tsc_datasets.py --only "$tsc_list"
[ "$tall_list" = - ] || "$PY" experiments/download_tall_datasets.py --only "$tall_list"
[ "$h8_list" = - ] || "$PY" experiments/download_h8_datasets.py --only "$h8_list"
case ",$DATASETS," in
    *,eodata,*)
        # --convert builds data/eodata/eodata.npz now, once: otherwise every
        # array task would parse the 1.4 GB ARFF at the same time.
        "$PY" experiments/download_eodata.py --convert ;;
esac
echo "datasets ready: $DATASETS"
