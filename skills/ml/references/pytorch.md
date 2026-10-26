# PyTorch & Deep Learning Standards

## Performance Optimization
*   **AMP (Automatic Mixed Precision):**
    *   **Rule:** Use `torch.amp` by default on modern GPUs (Volta+). It reduces VRAM usage and speeds up math (Tensor Cores).
    *   **Pattern:** `with torch.autocast(device_type='cuda', dtype=torch.float16): ...`
*   **Compilation:**
    *   **Rule:** Use `torch.compile()` (PyTorch 2.0+) for production inference models. It fuses kernels and optimizes graphs.
*   **Data Loading:**
    *   **Workers:** Set `num_workers` to > 0 (usually CPU count - on SLURM compute clusters: CPU count set by job params, not `os.cpu_count()`).
    *   **Pinning:** Set `pin_memory=True` to speed up CPU->GPU transfer.
    *   **Bottleneck Check:** If GPU utilization is < 90%, you are likely CPU-bound in the dataloader.

## Stability & Correctness
*   **Gradient Clipping:**
    *   **Rule:** Always clip gradients to prevent explosions. `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`.
*   **Deterministic Training:**
    *   **Seeds:** Set seeds for `torch`, `numpy`, and python `random`.
    *   **CUDNN:** Set `torch.backends.cudnn.benchmark = False` (slower) or accept slight non-determinism.

## LLMs & Transformers
*   **Attention:** Use `FlashAttention` implementations (available in `torch.nn.functional.scaled_dot_product_attention`).
*   **Quantization:**
    *   **Inference:** Use 4-bit (GPTQ/AWQ) for running large models on consumer hardware.
    *   **Training:** Use QLoRA (Quantized Low-Rank Adaptation) for fine-tuning.
*   **Safe Tensors:** **MANDATORY**. Do not save models with `pickle` (`torch.save`). Use `safetensors` library to prevent code execution vulnerabilities.
