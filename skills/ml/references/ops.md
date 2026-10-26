# MLOps & Production

## Experiment Tracking
*   **Philosophy:** "If it isn't tracked, it didn't happen."
*   **Tools:** `WandB`, `MLFlow`, `Comet`.
*   **What to Track:**
    *   **Hyperparameters:** `lr`, `batch_size`, `dropout`.
    *   **Metrics:** Train/Val Loss, F1, AUC.
    *   **System:** GPU Usage, RAM, Disk I/O.
    *   **Artifacts:** The model weights (`.pt`), the dataset hash (Git SHA / DVC hash).

## Model Registry & Lifecycle
*   **Registry:** Central database of trained models.
*   **Stages:**
    *   **None/Dev:** Experimental.
    *   **Staging:** Passed automated tests, waiting for QA.
    *   **Production:** Live serving.
*   **Promotion:** Automated via CI/CD pipelines (e.g., if Metric > Threshold -> Promote to Staging).

## Serving
*   **API:** `FastAPI` is the standard Python wrapper.
*   **High-Performance:**
    *   **vLLM / TGI:** For LLM inference (continuous batching, PagedAttention).
    *   **Triton Inference Server:** For standard models (TensorRT, ONNX).
*   **Monitoring:**
    *   **Drift:** Monitor **Data Drift** (inputs changing) and **Concept Drift** (relationship changing).
    *   **Latency:** P95 and P99 latency. Average latency hides spikes.
