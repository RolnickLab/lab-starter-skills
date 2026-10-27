# PyTorch & Deep Learning Standards

## Performance
*   **AMP:** `torch.autocast(device_type="cuda", dtype=torch.bfloat16)` on Ampere or newer (A100, L40S, H100), no `GradScaler` needed. On older GPUs (V100) use `float16` with `torch.amp.GradScaler`.
*   **Compilation:** Try `torch.compile()` for long runs and inference, and measure the gain. Skip it while debugging (compile time, harder tracebacks).
*   **Workers:** Size `num_workers` from the job's CPUs, not `os.cpu_count()` (see `cluster.md`). Set `pin_memory=True`, and `persistent_workers=True` when `num_workers > 0` (it raises at 0).
*   **Bottleneck check:** GPU utilization well below 90% usually means the loader is the bottleneck. Time the loader alone, or use `torch.profiler`.
*   **File handles:** Open file, HDF5 and GDAL handles lazily in the worker (in `worker_init_fn` or on first `__getitem__`), never in `Dataset.__init__`. Handles inherited across a fork corrupt reads.
*   **Storage layout:** Chunked formats (zarr, HDF5, WebDataset shards) over millions of small files. See `cluster.md`.

## Correctness
*   **Modes:** `model.train()` for training; `model.eval()` plus `torch.inference_mode()` for evaluation.
*   **Gradient norm:** Log it. Clip only if training is unstable, with `max_norm` set in config.
*   **NaN hunting:** `torch.autograd.set_detect_anomaly(True)` while debugging only (slow).
*   **Tests:** Unit-test a forward and backward pass on a tiny CPU batch: output shapes, no NaN, loss decreases over a few steps.

## Determinism
*   **Seeds:** Seed `random`, `numpy` and `torch` before building the model or the splits (`lightning.seed_everything` does all three).
*   **DataLoader:** Pass `generator=torch.Generator().manual_seed(seed)`. Each worker then reseeds `random`, global `numpy` and `torch` from it. RNG objects you build yourself (e.g. `np.random.default_rng()` in `Dataset.__init__`) are copied identically into every worker: reseed them in `worker_init_fn` from `torch.initial_seed()`.
*   **Bitwise reproducibility (debugging only):** `torch.use_deterministic_algorithms(True)`, `torch.backends.cudnn.benchmark = False`, env `CUBLAS_WORKSPACE_CONFIG=:4096:8`. Slower, and still not portable across GPU types. Report results over multiple seeds instead of relying on bitwise reproducibility.

## Checkpointing
*   **Contents:** Model, optimizer, scheduler, scaler, epoch/step, RNG states, full config, tracker run ID. Resuming must continue the same run. See `cluster.md` for preemption.
*   **Loading:** `torch.load(path, weights_only=True)` (default since PyTorch 2.6). Never pass `weights_only=False` on a file you did not create.
*   **Selection:** Pick the checkpoint on the validation metric, never the test metric.
*   **Release:** Publish weights as `safetensors` plus the config file, not full training checkpoints. See `operationalization.md`.
