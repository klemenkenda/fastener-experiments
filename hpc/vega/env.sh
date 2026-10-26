# The Python environment, unpacked onto local disk. Sourced by config.sh.
#
#   use_env          unpack $ENV_ARCHIVE (once) and set PY and PATH
#
# Inside a SLURM job the environment goes into a folder of its own under
# $LOCAL_TMP, removed when the job ends: one read of one file from Ceph, a few
# seconds of unpacking onto the node's NVMe disk. Outside a job (a login node)
# it goes into $LOCAL_TMP/fastener-env-$USER and is kept, and unpacked again
# only when the archive is newer than it.

env_dir() {
    if [ -n "${SLURM_JOB_ID:-}" ]; then
        echo "$LOCAL_TMP/fastener-${USER:-$(id -un)}-$SLURM_JOB_ID${SLURM_ARRAY_TASK_ID:+-$SLURM_ARRAY_TASK_ID}"
    else
        echo "$LOCAL_TMP/fastener-env-${USER:-$(id -un)}"
    fi
}

use_env() {
    if [ ! -f "$ENV_ARCHIVE" ]; then
        echo "no environment at $ENV_ARCHIVE; run hpc/vega/setup.sh first" >&2
        return 1
    fi
    local dir
    dir="$(env_dir)"
    if [ ! -f "$dir/.unpacked" ] || [ "$ENV_ARCHIVE" -nt "$dir/.unpacked" ]; then
        rm -rf "$dir"
        mkdir -p "$dir"
        tar -xzf "$ENV_ARCHIVE" -C "$dir"
        # conda-pack's fix-up: rewrite the build prefix to this one.
        "$dir/bin/python" "$dir/bin/conda-unpack"
        touch "$dir/.unpacked"
    fi
    PY="$dir/bin/python"
    if [ -n "${SLURM_JOB_ID:-}" ]; then
        # shellcheck disable=SC2064  # expand $dir now
        trap "rm -rf '$dir'" EXIT
        export PATH="$dir/bin:/usr/bin:/bin"
    else
        export PATH="$dir/bin:$PATH"
    fi
    # Byte-code caches go to local disk too, not into the repository on Ceph
    # from 200 jobs at once.
    export PYTHONPYCACHEPREFIX="$dir/pycache"
}
