# SLURM Clusters (Mila, DRAC)

Partitions, quotas, purge policies and hardware change. Check the official docs before relying on a number:
[Mila](https://docs.mila.quebec/), [DRAC](https://docs.alliancecan.ca/).

## Ground Rules
*   **Login nodes:** Edit, install, submit. Never train or preprocess there.
*   **Interactive first:** Debug in a short `salloc` session, then submit with `sbatch`.
*   **Smoke test:** Run the exact job script for a few steps on 1 GPU before launching a long job or a sweep.
*   **Request what you use:** Ask for the GPUs, CPUs, memory and time the smoke test showed. Shorter jobs schedule sooner. Check usage with `seff <jobid>`.
*   **CPUs:** Size `num_workers` from `len(os.sched_getaffinity(0))`, never `os.cpu_count()` (whole node). `SLURM_CPUS_PER_TASK` is unset unless the job requests `--cpus-per-task`.

## Storage
*   **`$SLURM_TMPDIR`:** Fast node-local disk, wiped when the job ends. Copy or extract the dataset there at job start; write checkpoints elsewhere.
*   **Scratch:** Large and fast, not backed up, purged after inactivity. Use for checkpoints and run outputs; never the only copy of anything.
*   **Home / project:** Backed up, small or shared. Code, final results, shared datasets.
*   **File counts:** Network filesystems choke on many small files and enforce file-count quotas. Ship datasets as archives (`tar`), zarr stores, HDF5 or WebDataset shards.

## Preemption and Time Limits
*   **Assume the job dies:** Preemptible partitions and wall-time limits will kill jobs. Checkpoint on a schedule (every N minutes or steps), not only at epoch end.
*   **Signals:** Request a warning signal (`#SBATCH --signal=B:USR1@300`), trap it, save a checkpoint, then requeue (`scontrol requeue $SLURM_JOB_ID`) or exit cleanly. Lightning's `SLURMEnvironment(auto_requeue=True)` does this. With `B:`, only the batch shell gets the signal: `exec` the Python command, or trap and forward it.
*   **Resume is automatic:** On start, load the latest checkpoint if one exists, including the tracker run ID, so a resumed job continues the same run.

## Mila vs DRAC Differences
*   **Internet:** Mila compute nodes have internet access. Most DRAC compute nodes do not.
*   **Offline on DRAC:**
    *   Download datasets and pretrained weights on a login node first.
    *   Point `HF_HOME` / `TORCH_HOME` to project or scratch, and set `HF_HUB_OFFLINE=1` in jobs.
    *   Run W&B with `WANDB_MODE=offline`, then `wandb sync` from a login node.
*   **Environments on DRAC:** Load modules (`module load python cuda`) before creating the environment. Prefer the Alliance wheelhouse (`pip install --no-index`) where it has the package.
*   **Accounts on DRAC:** Pass `--account=<def|rrg>-<pi>`. Allocation priority depends on the account's usage.

## Sweeps and Many Runs
*   **Job arrays:** `#SBATCH --array=0-N%K` with the index selecting a config or seed. `%K` caps concurrent jobs.
*   **Hydra launchers:** `hydra-submitit-launcher` works well on Mila. Plain arrays are simpler and more robust on DRAC.
*   **One run per job:** Keep each seed and config in its own job, so a failure costs one run.
