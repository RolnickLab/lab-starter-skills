# Tech Stack & Anti-Patterns

## Recommended Stack
| Domain | Library | Rationale |
| :--- | :--- | :--- |
| **Deep Learning** | `PyTorch` | Industry standard, pythonic. |
| | `Lightning` | Removes boilerplate loops, organizes code. |
| **Classical ML** | `Scikit-learn` | Pipelines and preprocessing. |
| | `XGBoost` / `LightGBM` | SOTA for tabular gradients boosting. |
| **Data** | `Polars` | Fast Rust-based DataFrames. |
| **Tracking** | `WandB` / `MLFlow` | Visualization and registry. |
| **Serving** | `FastAPI` | Async serving wrapper. |
| | `Triton` | NVIDIA's high-perf inference server. |

## Forbidden Patterns
1.  **Global Scoping:** Training code in the global scope.
    *   *Why:* Breaks `multiprocessing` (needs `if __name__ == "__main__"`).
2.  **Magic Numbers:** `dropout=0.5` inside the model class.
    *   *Fix:* Pass via config object.
3.  **Variable Names:** `x`, `y`, `df`, `temp`.
    *   *Fix:* `input_tensor`, `target_labels`, `customer_df`.
4.  **Pickle:** `pickle.load()`.
    *   *Why:* Arbitrary code execution vulnerability.
    *   *Fix:* `safetensors`, `ONNX`.
5.  **Print to Stdout:** Using `print()` for metrics.
    *   *Why:* Unparseable, lost in logs.
    *   *Fix:* Use `logger` and Experiment Tracker.
