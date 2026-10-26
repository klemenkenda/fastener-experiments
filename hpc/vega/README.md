# Running an experiment on HPC Vega

These scripts run an experiment's grid on Vega (SLURM). Each job is one
dataset, one arm and one seed, run as one SLURM array task. They were written
for `H5H6-E02`, H5H6-E01's grid with the protocol random forest (DEC-41).

The jobs are the ones `run_queue.py` would run locally, built by the same
code: `experiments/hpc_jobs.py` drives the arrays. Every run is recorded as
usual: a run folder under `results/` and a row in the ledger,
`experiments/EXPERIMENTS.md`.

## Rules learned on 2026-10-26

These scripts follow three rules:

- **No Python environment as loose files on Ceph.** A Miniforge install of
  tens of thousands of small files into the home directory took an hour,
  hung, and could not be deleted. The environment is built on local disk and
  kept on Ceph as one archive, `.hpc/env.tar.gz`. Every job unpacks it onto
  its node's NVMe `/tmp` in seconds, and removes it at the end.
- **Jobs start from a clean environment:** `PATH=/usr/bin:/bin`, and only
  `HOME`, `USER` and the job's own settings passed in. A `PATH` entry on a
  hung mount froze `which`, and every command that searched `PATH` with it.
- **A five-minute test job runs before the 2,000.**

## 1. Once: set up

On a login node (`ssh kendak@login.vega.izum.si`):

```bash
cd ~                                   # or your project space
git clone https://github.com/klemenkenda/fastener-experiments.git
cd fastener-experiments
bash hpc/vega/setup.sh                 # a few minutes
```

`setup.sh` does four things:

1. Builds Python 3.11 and `requirements.txt` in the login node's `/tmp`, with
   one `micromamba` binary.
2. Packs the result into `.hpc/env.tar.gz`: one file on Ceph.
3. Clones FASTENER at `3be5697`.
4. Checks that everything imports.

It ends with `setup done`, after `code clean`.

If the login node is busy, run it as a job instead:

```bash
sbatch -p cpu -A s26t11-01-users -t 00:30:00 -c 4 --mem=8G \
    -o setup-%j.out --wrap "bash $PWD/hpc/vega/setup.sh"
```

The defaults in `config.sh` follow the S26T11-01 allocation: account
`s26t11-01-users`, partition `cpu`, 8 cores and 8 GB per job, at most 200
tasks at once. Put any change in `hpc/vega/config.local.sh`, which git
ignores (runs refuse to start from uncommitted code):

```bash
echo 'MAX_PARALLEL=100' > hpc/vega/config.local.sh
```

## 2. Submit

```bash
bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
```

`submit.sh` writes the job list (`results/H5H6-E02/jobs.json`, 2,202 jobs,
as H5H6-E01's grid). It then submits a chain in which each step starts only
if the one before it succeeded:

| Step | What it does | Output |
|---|---|---|
| data job | downloads the 38 UCR/UEA datasets and EOData, checks their pinned SHA256s, converts them to `.npz` | `results/H5H6-E02/slurm/data_<id>.out` |
| test job | about 5 minutes: unpacks the environment and runs the real code on Coffee with the forest (an ANOVA ranker, Boruta, sparse NSGA-II, guided FASTENER) | `results/H5H6-E02/slurm/test_<id>.out`, ending `test passed` |
| arrays | the experiment's jobs | `results/H5H6-E02/slurm/task_<id>_<index>.out` |

The jobs run as two arrays:

| Array | Jobs | Cores | Memory |
|---|---|---|---|
| most jobs | 2,190 | 8 | 8 GB (1 GB per core; Vega bills memory like cores) |
| high-memory | the 12 jobs in [`h5h6e02_highmem.txt`](h5h6e02_highmem.txt): HSIC Lasso on the wide sets, ReliefF on EOData, NSGAII-MIIP on Heartbeat | 8 | 64 GB |

Each job is limited to 6 hours: `hpc_jobs.py` stops a job at the cap and
records it as `timeout`. The SLURM time limit is the cap plus 15 minutes.

Before finishing, `submit.sh` prints a worst case: about 880 node-hours if
all 2,202 jobs ran to the cap, against the allocation's 5,000. Most runs
finish far sooner. Check what's been used with:

```bash
sreport -t hours cluster AccountUtilizationByUser account=s26t11-01-users start=2026-10-16
```

## 3. Watch

```bash
bash hpc/vega/watch.sh hpc/vega/h5h6e02.env
```

Every 10 minutes (`INTERVAL=300` for 5), `watch.sh`:

- gathers the jobs' states and shows the monitor (done, running, failed,
  timed out, and the time left) and the SLURM queue;
- appends a line to `results/H5H6-E02/watch.log`;
- flags a failed data or test job.

It stops by itself when no job of the experiment is queued or running.
Ctrl+C stops the watching, not the jobs.

To keep it running after you log out, start it in `tmux`:

```bash
tmux new -s watch
bash hpc/vega/watch.sh hpc/vega/h5h6e02.env
# detach: Ctrl+B, then D.  Back later: tmux attach -t watch
```

For a single look without the loop:

```bash
bash hpc/vega/status.sh hpc/vega/h5h6e02.env
squeue -u $USER
```

## 4. After an interruption, or a job out of memory

Run `submit.sh` again. It submits only the jobs not yet done or timed out,
and refuses while jobs of the experiment are still queued or running, so that
no job runs twice. On a resubmission the data and test jobs can be skipped:

```bash
SKIP_DATA=1 SKIP_TEST=1 bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
```

A job killed for memory shows as `failed`. Rerun the failed jobs with more:

```bash
MEM=32G SKIP_DATA=1 SKIP_TEST=1 bash hpc/vega/submit.sh hpc/vega/h5h6e02.env
```

`sacct -u $USER --state=FAILED,OUT_OF_MEMORY --format=JobID,JobName,State,MaxRSS,Elapsed`
shows which tasks failed and how much memory they used.

## 5. Bringing the results home

Run `fetch.sh` on your own machine, in your clone of this repository. Git
Bash on Windows works: it needs only `ssh` and `tar`.

```bash
VEGA_HOST=kendak@login.vega.izum.si VEGA_REPO=/ceph/hpc/home/kendak/fastener-experiments \
    bash hpc/vega/fetch.sh hpc/vega/h5h6e02.env
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

Then write the report as usual:

```bash
python experiments/make_report.py --experiment H5H6-E02
```

## Clean-up of the first, broken install

The Miniforge install of 2026-10-26, renamed to `.hpc-broken`, still holds
tens of thousands of small files. Do not delete it from a login shell. Either
ask support@sling.si to remove it on the storage side, or let a small
low-priority job do it slowly:

```bash
sbatch -p cpu -A s26t11-01-users -t 12:00:00 -c 1 --mem=1G \
    -o ~/rm-hpc-%j.out --wrap "rm -rf $HOME/fastener-experiments/.hpc-broken"
```
