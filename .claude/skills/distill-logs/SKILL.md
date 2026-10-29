---
name: distill-logs
description: Distill an experiment's job logs (results/<ID>/logs/*.log, hundreds to thousands of files, from Vega or the workstation queue) into a short digest -- errors and warnings grouped by signature with counts and an example log, logs that never finished with their job state, stop reasons and wall time -- and turn it into the "What happened" part of SUPPORT.md or an answer to the user. Use when an experiment has finished or failed, when jobs failed, timed out or ran out of memory, when the user asks what went wrong, what is in the logs, or to summarise, check or distill logs.
---

# Distill logs

An experiment leaves one log per job. Nobody reads 2,000 of them, and they
mostly say the same few things. The digest says each thing once, with how
many logs say it. Interpreter: `C:\Users\klemen\.conda\envs\fastener-exp\python.exe`.

## 1. Run the digest

```
python experiments/distill_logs.py --experiment <ID>
python experiments/distill_logs.py --experiment <ID> --top 60 --json <scratch>/digest.json
python experiments/distill_logs.py "results/<ID>/logs/*_PEMS-SF_*.log"      # a subset
```

It reads only; a few seconds for 2,000 logs. Run it on the fetched copy
(`fetch.sh` brings `results/<ID>/logs/` home; the SLURM outputs stay on
Vega). On Vega, the same command after `. hpc/vega/config.sh; use_env`, with
`"$PY"`, also reads logs before fetching.

The digest has four parts:

| part | what it groups | by |
|---|---|---|
| Errors | tracebacks (by their final exception line), `FAILED`, out of memory, `Killed`, time limit, cancelled | signature |
| Warnings | Python warnings and other warning lines | signature |
| Incomplete logs | logs without the closing `manifest:` line | job state + last line |
| Runs | `stopped_on` counts; wall time per log | -- |

A signature is the line with paths, run IDs, numbers and hex replaced by
`<path>`, `<run>`, `<n>`, `<hex>`, so the same message from different jobs
counts once.

## 2. Read it

For each part, decide what it means; read whole logs only where the digest
points to them:

- **An error signature.** Open its example log, and one or two more (`--json`
  lists none beyond the first; grep the logs for the signature's fixed
  words). Find out whether it killed the job, a seed, or nothing; whether all
  its logs share a dataset, arm or node; and whether the job was rerun.
- **A warning signature.** Usually harmless (e.g. matplotlib's "No artists
  with labels" from runs without a legend). Say so in one line. A warning
  about convergence, numerics or data (NaN, empty class, deprecated
  behaviour that changes results) is a finding: check how many runs it
  touched.
- **Incomplete logs.** Expected state `timeout` (the 6-hour cap stops a job
  mid-run, so the log just ends); compare the count with the timeouts the
  queue reports. Look harder at `done` (the job finished but its log did
  not -- a log written elsewhere or truncated), `failed`, `running` (the job
  was killed and never rerun), and `no status` (the job was never recorded).
- **Runs.** `stopped_on` should be the stop rule the design expects (e.g.
  `fit_budget` for every search); any other value needs a sentence. The wall
  time per log is a cross-check on the queue's timings, not a replacement.

Check the counts against the experiment's own record before writing: the
number of logs against the job count (`hpc_jobs.py count` or `queue.json`),
the timeouts against the monitor, the failures against the status files.

## 3. Write it up

**In SUPPORT.md's *What happened*** (with the `experiment-report` skill), a
short paragraph or a small table, never the raw digest:

- one line per error signature that mattered: what, how many jobs, which
  cells, why, what was done (rerun with more memory, timed out, ignored);
- one line for the harmless warnings together ("47 logs carry matplotlib's
  empty-legend warning, from filter runs; no effect");
- the incomplete logs, matched to the timeouts or explained;
- anything in Runs that differs from the design.

Numbers in the write-up must match the digest. Leave the digest itself in a
scratch file; do not commit it (results/ stays uncommitted).

**In an answer to the user**, lead with the verdict -- "nothing went wrong
beyond the 71 timeouts" or "12 jobs ran out of memory on PEMS-SF" -- then
the few signatures that matter, then what to do about them.

## 4. If the digest misses something

The patterns are in `distill_logs.py` (`ERROR`, `WARNING`, `CLOSING`,
`SEED_SECONDS`). A new kind of failure that the digest did not group belongs
there: add its pattern, rerun, and commit the change with the report.
