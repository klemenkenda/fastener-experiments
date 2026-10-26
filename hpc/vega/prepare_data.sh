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

tsc=()
for ds in ${DATASETS//,/ }; do
    [ "$ds" = eodata ] || tsc+=("$ds")
done
if [ ${#tsc[@]} -gt 0 ]; then
    tsc_list="$(IFS=,; echo "${tsc[*]}")"
    "$PY" experiments/download_tsc_datasets.py --only "$tsc_list"
fi
case ",$DATASETS," in
    *,eodata,*)
        # --convert builds data/eodata/eodata.npz now, once: otherwise every
        # array task would parse the 1.4 GB ARFF at the same time.
        "$PY" experiments/download_eodata.py --convert ;;
esac
echo "datasets ready: $DATASETS"
