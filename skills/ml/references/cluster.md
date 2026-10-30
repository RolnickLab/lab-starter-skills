# SLURM Clusters (Mila, DRAC)

Partitions, quotas, purge policies and hardware change. Check the official docs before relying on a number:
[Mila](https://docs.mila.quebec/), [DRAC](https://docs.alliancecan.ca/). The DRAC wiki blocks automated fetches; use Mila's [DRAC summary](https://docs.mila.quebec/technical_reference/clusters/drac/) or ask the user.

## Ground Rules
*   **Login nodes:** Edit, install, submit. Never train or preprocess there.
*   **Interactive first:** Debug in a short `salloc` session, then submit with `sbatch`.
*   **Smoke test:** Run the exact job script for a few steps on 1 GPU (a MIG slice such as `1g.10gb` on DRAC H100s) before launching a long job or a sweep.
*   **Request what you use:** Ask for the GPUs, CPUs, memory and time the smoke test showed. Shorter jobs schedule sooner. Check usage with `seff <jobid>` (DRAC) or `sacct -j <jobid> -o MaxRSS,ReqMem,Elapsed`.
*   **CPUs:** Size `num_workers` from `len(os.sched_getaffinity(0))` (or `os.process_cpu_count()` on Python 3.13+), never `os.cpu_count()` (whole node). `SLURM_CPUS_PER_TASK` is unset unless the job requests `--cpus-per-task`.

## Storage
*   **`$SLURM_TMPDIR`:** Fast node-local disk, wiped when the job ends. Copy or extract the dataset there at job start; write checkpoints elsewhere.
*   **Scratch:** Large and fast, not backed up, purged after inactivity. Use for checkpoints and run outputs; never the only copy of anything.
*   **Home / project:** Backed up, small or shared. Code, final results, shared datasets.
*   **Curated data on Mila:** Check `/network/datasets` and `/network/weights` (read-only) before downloading.
*   **File counts:** Network filesystems choke on many small files and enforce file-count quotas. Ship datasets as archives (`tar`), zarr stores, HDF5 or WebDataset shards.

## Preemption and Time Limits
*   **Assume the job dies:** Checkpoint on a schedule (every N minutes or steps), not only at epoch end. On Mila's default partitions (e.g. `long`), preemption kills the job without notice and requeues it; only periodic checkpoints survive. `-grace` partitions (`main-grace`, `long-grace`) send SIGTERM 120 s before SIGKILL but do not requeue.
*   **Wall-time signal:** `--signal` fires only before the time limit, not on preemption. Request it, trap it (and SIGTERM), save a checkpoint, then requeue (`#SBATCH --requeue` plus `scontrol requeue $SLURM_JOB_ID`) or exit cleanly.
    *   `srun python ...`: use `--signal=USR1@300` (no `B:`), so the job step gets it. Lightning's `SLURMEnvironment(auto_requeue=True)` expects this setup.
    *   `exec python ...` without `srun`: use `--signal=B:USR1@300`, since only the batch shell gets `B:` signals.
*   **Resume is automatic:** On start, load the latest checkpoint if one exists, including the tracker run ID, so a resumed job continues the same run. Requeued jobs keep their ID: key the run directory on `$SLURM_JOB_ID`, or `${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}` for arrays.

## Mila vs DRAC Differences
*   **Internet:** Mila compute nodes have it. On DRAC it varies by cluster (Fir and Nibi yes; Narval, Rorqual, Trillium, TamIA no). Write jobs to run offline so they port across clusters.
*   **Offline:**
    *   Download datasets and pretrained weights on a login node first.
    *   Point `HF_HOME` / `TORCH_HOME` to project or scratch, and set `HF_HUB_OFFLINE=1` in jobs.
    *   Run W&B with `WANDB_MODE=offline`, then `wandb sync` from a login node. `module load httpproxy` exists on some clusters, but W&B can hang behind it.
*   **Environments on Mila:** `uv` with a committed `uv.lock`; jobs call `uv run python ...`.
*   **Environments on DRAC:** `uv` works, though DRAC only documents pip. Setup details: [Rolnick lab guide](https://rolnicklab.github.io/best-practices-documentation/sections/clusters/env_creation_drac/).
    *   Use the module's Python (`module load python/3.12`), never a uv-downloaded one: set `python-preference = "system"` in `~/.config/uv/uv.toml`.
    *   Create the venv with `virtualenv --no-download .venv` in the project, not `uv venv` (reported to break on DRAC), then `uv sync` into it.
    *   `uv sync` targets the project's `.venv` and ignores an activated venv elsewhere. For a venv at another path, pass `--active` or set `UV_PROJECT_ENVIRONMENT=<path>`.
    *   uv ignores the Alliance wheelhouse unless it is an index. In the same `uv.toml` (user-level: `/cvmfs` exists only on DRAC), add `format = "flat"` `[[index]]` entries for `/cvmfs/soft.computecanada.ca/custom/python/wheelhouse/{gentoo2023/x86-64-v3,gentoo2023/generic,generic}` and `index-strategy = "unsafe-best-match"`.
    *   A `uv.lock` resolved against the wheelhouse pins `+computecanada` versions that only exist on DRAC, while a PyPI lock ignores the wheelhouse. One committed lock cannot serve both. Ask the user which option fits:
        1.  Commit the PyPI lock (Mila, laptops). On DRAC, let `uv sync` re-resolve and keep that lock out of commits (`git update-index --skip-worktree uv.lock`). Simplest; DRAC versions may drift from the lock.
        2.  Commit the DRAC lock, for projects that run only on DRAC. Other machines cannot install it.
        3.  One dependency group per cluster, with per-group sources and `[tool.uv] conflicts`. One lock for both, but harder to set up and maintain, and locking needs the `/cvmfs` paths.
    *   Run `uv sync` on a login node and `uv run --offline` (or `UV_OFFLINE=1`) in jobs. Point `UV_CACHE_DIR` to `$SCRATCH` to spare the home quota.
    *   Plain pip alternative: `virtualenv --no-download $SLURM_TMPDIR/env` inside the job, then `pip install --no-index`.
*   **Accounts on DRAC:** Pass `--account`: `def-<pi>` (default), `rrg-<pi>-<suffix>` (e.g. Mila's `rrg-bengioy-ad`). PAICE clusters (TamIA, Killarney, Vulcan) need `aip-<pi>`; other allocations do not work there, and TamIA allocates whole nodes. Priority depends on the account's usage.
*   **DRAC job length:** Production jobs should run at least 1 hour; the maximum is 7 days.

## Sweeps and Many Runs
*   **Job arrays:** `#SBATCH --array=0-N%K` with the index selecting a config or seed. `%K` caps concurrent jobs.
*   **Hydra launchers:** `hydra-submitit-launcher` works well on Mila. Plain arrays are simpler and more robust on DRAC.
*   **Several clusters:** [`cluv`](https://mila-iqia.github.io/cluv/) syncs a uv project to Mila and DRAC clusters, runs `uv sync` there, submits jobs (`cluv submit <cluster> job.sh`) and provides a Hydra launcher. The project must live under `$HOME`.
    *   On DRAC, `cluv` skips the setup above: no `module load python` and no `virtualenv`; `uv` picks or downloads its own Python. It builds every cluster's venv from one committed PyPI `uv.lock` (lock option 1) and installs PyPI wheels unless you add the wheelhouse `uv.toml` yourself.
    *   With that `uv.toml`, its plain `uv sync` will likely rewrite `uv.lock` in the cluster checkout, and the next `cluv sync` (`git pull`) can fail when `uv.lock` also changed upstream (untested). If it does, discard the cluster's `uv.lock` changes (`git checkout uv.lock`) before syncing.
*   **One run per job:** Keep each seed and config in its own job, so a failure costs one run. Pack runs shorter than the DRAC 1-hour minimum several per job.
