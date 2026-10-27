# Tech Stack & Anti-Patterns

## Recommended Stack
| Domain | Library | Rationale |
| :--- | :--- | :--- |
| **Deep Learning** | `PyTorch` | Research standard, pythonic. |
| | `Lightning` | Optional. Adopt when you need multi-GPU, checkpoint/resume or early stopping; a plain loop is fine before that. |
| **Pretrained Models** | `timm`, `huggingface_hub` | Backbones and weight distribution. For remote sensing, `torchgeo` (see `domains.md`). |
| **Classical ML** | `scikit-learn`, `LightGBM` / `XGBoost` | Pipelines, CV, tabular SOTA. |
| **Tables** | `pandas` / `geopandas` | Match the project; do not add a second dataframe library. |
| **Gridded Data** | `xarray` + `zarr` / netCDF, `dask` | Labelled N-D arrays for climate and imagery, lazy and chunked. |
| **Config** | `pydantic`, `pydantic-settings`, `Hydra` (optional) | Validated schema; see below. |
| **Tracking** | `WandB` / `MLflow` | Metrics, configs, artifacts. |
| **Inference** | `ONNX Runtime`, `FastAPI` | Portable inference; FastAPI only when a partner needs a service. See `operationalization.md`. |

## Configuration
*   **Two layers:** Per-machine values (paths, credentials) in a git-ignored `.env`, read with `pydantic-settings`. Per-run values (hyperparameters, model/dataset choice) in committed YAML. Anything that changes results belongs in the per-run layer.
*   **Schema is the contract:** Every YAML file validates against Pydantic models.
    ```python
    class OptimizerConfig(BaseModel):
        model_config = ConfigDict(frozen=True, extra="forbid")
        name: Literal["adam", "sgd"] = "adam"
        lr: float = Field(default=1e-3, gt=0.0)
    ```
    *   `extra="forbid"`: a typo'd key fails at load instead of being silently ignored.
    *   `frozen=True`: a run cannot mutate its config mid-flight.
    *   `Field` bounds and `Literal` for fields that select code paths: invalid values fail before data loading, not hours into a job.
    *   New parameter: add the schema field first, then set it in YAML.
*   **Composition:** Shared blocks per group (`model/`, `dataset/`, `optimizer/`) merged through a `defaults:` list (`- group: name` entries, `_self_` last so the experiment's own keys win); one short file per experiment.
*   **Without Hydra:** A small loader resolves that subset (load each group file, deep-merge in list order) before validation. Keep group files flat and reject Hydra-only syntax (`${...}` interpolation, `defaults:` inside group files) with a clear error, so the same YAML composes identically with or without Hydra.
*   **Record:** Log the merged, validated config at startup and send it to the tracker as the run config.
*   **Hydra (optional):** Use it for CLI overrides, `--multirun` sweeps and SLURM launchers (`submitit`). Hydra owns the entry point and feeds the same schema: `Config(**OmegaConf.to_container(cfg, resolve=True))`. Do not add Hydra structured configs alongside Pydantic: one schema only.

## Forbidden Patterns
1.  **Global Scoping:** Training code in the global scope.
    *   *Why:* Breaks `multiprocessing` (needs `if __name__ == "__main__"`).
2.  **Magic Numbers:** `dropout=0.5` inside the model class.
    *   *Fix:* Pass via the config schema.
3.  **Untyped Configs:** Raw `dict` / `DictConfig` passed deep into code (`cfg["lr"]`).
    *   *Fix:* Validate once at the entry point, pass typed config objects.
4.  **Pickle from Others:** `pickle.load()` / `torch.load(weights_only=False)` on files you did not create.
    *   *Why:* Arbitrary code execution.
    *   *Fix:* `safetensors`, `ONNX`.
5.  **Print to Stdout:** Using `print()` for metrics.
    *   *Fix:* `structlog` for events, the experiment tracker for metrics.
