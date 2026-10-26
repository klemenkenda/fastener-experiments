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

The defaults in `config.sh` follow the S26T11-01 allocation as checked on
2026-10-26: account `s26t11-01-users`, partition `cpu`, 8 cores and 8 GB per
job. Anything you change goes in `hpc/vega/config.local.sh`, which git
ignores, so the tree stays clean (runs refuse to start from uncommitted
code):

```bash
MAX_PARALLEL=100        # e.g. fewer tasks at once
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
3. **Submits the jobs as two arrays**, which start once the data job has
   succeeded. An array task's index is its job's index in the list, and at
   most `MAX_PARALLEL` tasks of an array run at once.

The two arrays differ only in memory:

| Array | Jobs | Cores | Memory |
|---|---|---|---|
| most jobs | every cell not listed below | 8 | 8 GB (1 GB per core) |
| high-memory | the 12 jobs in the 8 cells of [`h5h6e02_highmem.txt`](h5h6e02_highmem.txt): HSIC Lasso on the wide sets, ReliefF on EOData, NSGAII-MIIP on Heartbeat | 8 | 64 GB |

Each job is limited to 6 hours: `hpc_jobs.py` stops a job at the cap and
records it as `timeout`. The SLURM time limit is the cap plus 15 minutes.

**Billing.** Vega bills memory as well as cores (1 GB = 1 core), so jobs get
1 GB per core unless they need more. Before finishing, `submit.sh` prints a
worst case: about 880 node-hours if all 2,202 jobs ran to the cap. Most runs
finish far sooner. That is against 5,000 CPU node-hours, which SLURM does not
enforce; check what's used with:

```bash
sreport -t hours cluster AccountUtilizationByUser account=s26t11-01-users start=2026-10-16
```

**If the compute nodes cannot reach the internet**, the data job fails and
the arrays never start. Prepare the data on the login node and submit
without it:

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

## After an interruption, or a job out of memory

Run `submit.sh` again, with `SKIP_DATA=1` if the data is in place. It
submits only the jobs not yet done or timed out, and refuses while jobs of the
experiment are still queued or running, so that no job runs twice. A job
killed for memory shows as `failed`. Rerun the failed jobs with more memory:

```bash
MEM=32G SKIP_DATA=1 bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
```

`sacct -j <array job> --format=JobID,State,MaxRSS,Elapsed` shows which tasks
ran out of memory and how much they used.

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
