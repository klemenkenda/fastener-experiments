# Running an experiment on HPC Vega

These scripts run an experiment's grid on Vega (SLURM). Each job is one
dataset, one arm and one seed, run as one SLURM array task. They were written
for `H5H6-E02`, H5H6-E01's grid with the protocol random forest (DEC-41).

The jobs are the ones `run_queue.py` would run locally, built by the same
code: `experiments/hpc_jobs.py` drives the arrays. Every run is recorded as
usual: a run folder under `results/` and a row in the ledger,
`experiments/EXPERIMENTS.md`.

## Once: set up

On a login node, in your project space. `$HOME` is small, and the data and
results take tens of GB.

```bash
cd /ceph/hpc/data/<project>        # or wherever your project space is
git clone https://github.com/klemenkenda/fastener-experiments.git
cd fastener-experiments
bash hpc/vega/setup.sh             # Miniforge env + FASTENER clone at 3be5697
```

Put local settings in `hpc/vega/config.local.sh`. Git ignores this file, so
the tree stays clean; runs refuse to start from uncommitted code.

```bash
ACCOUNT=<your SLURM account>       # if your allocation needs one
# CPUS=8  MEM=32G  MAX_PARALLEL=200  PARTITION=cpu   (defaults in config.sh)
```

## Submit

```bash
bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
```

`submit.sh` does three things:

1. **Writes the job list** to `results/H5H6-E02/jobs.json`: 2,202 jobs, as
   H5H6-E01's grid.
2. **Submits a data job.** It downloads the 38 UCR/UEA datasets and EOData,
   verifies them against their pinned SHA256s, and converts them to `.npz`
   (`prepare_data.sh`).
3. **Submits the jobs as arrays** of up to `ARRAY_CHUNK` tasks, which start
   once the data job has succeeded.

Each task gets `CPUS` cores (the forest's trees and NSGAII-MIIP's MI matrix
use them) and `MEM` memory. `hpc_jobs.py` stops a job at the 6-hour cap and
records it as `timeout`. The SLURM time limit is the cap plus 15 minutes.

If the compute nodes cannot reach the internet, the data job fails and the
arrays never start. In that case, prepare the data on the login node and
submit without the data job:

```bash
bash hpc/vega/prepare_data.sh hpc/vega/h5h6e02.env
SKIP_DATA=1 bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
```

## Watch

```bash
bash hpc/vega/status.sh hpc/vega/h5h6e02.env   # collect + monitor.py --once
squeue -u $USER
```

| What | Where |
|---|---|
| per-job state | `results/H5H6-E02/status/<job>.json` |
| per-job log | `results/H5H6-E02/logs/<job>.log` |
| SLURM output | `results/H5H6-E02/slurm/` |
| gathered state (`status.sh`) | `results/H5H6-E02/queue.json`, read by `monitor.py` and `make_report.py` |

## After an interruption

Run `submit.sh` again, with `SKIP_DATA=1` if the data is in place. It is
safe:

- the job list must match the one already written;
- jobs that ended `done` or `timeout` are skipped;
- everything else runs again from the start, as `run_queue.py --resume` does
  locally.

## Bringing the results home

Run `fetch.sh` on your own machine, in your clone of this repository. Git
Bash on Windows works: it needs only `ssh` and `tar`.

```bash
VEGA_HOST=<user>@login.vega.izum.si VEGA_REPO=/ceph/hpc/data/<project>/fastener-experiments bash hpc/vega/fetch.sh hpc/vega/h5h6e02.env
```

It copies two things into your local `results/`:

- `results/H5H6-E02/`: the job list, the states and the logs;
- every run folder, `results/*_h5h6e02_*`.

It then adds the runs listed in Vega's ledger to your local H5H6-E02 row in
`experiments/EXPERIMENTS.md`, so nothing needs committing or pushing from the
cluster. It is safe to run again: it fetches everything again and adds only
runs the ledger doesn't have yet.

`NO_TRAJECTORIES=1` leaves out the `trajectories/` folders, which are most of
the volume. The report's progress and timeout figures need them.

After that, write the report as usual:

```bash
python experiments/make_report.py --experiment H5H6-E02
```
