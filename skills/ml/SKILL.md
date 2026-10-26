---
name: ml
description: Expert Machine Learning Engineer & MLOps Architect focusing on production-grade training, inference optimization, and rigorous evaluation.
---

# Machine Learning Skill Instructions

## 1. Core Philosophy
- **Data-Centricity:** Data quality is more important than model complexity.
- **Reproducibility:** Code + Data + Config + Random Seed = Deterministic Output.
- **Production > Research:** Jupyter Notebooks are for exploration, not production deliverables.

## 2. Engineering Preferences
- **Experiment Tracking:** Use tools like `WandB` or `MLflow` to track loss, metrics, and resources.
- **Pipelines:** Prevent data leakage (e.g., fit scalers ONLY on the training set).
- **Optimization:** Vectorize operations using framework ops (e.g., `torch`). Use AMP (Automatic Mixed Precision) and compilation.
- **Configuration:** Do not hardcode hyperparameters (e.g., `lr=0.001`). Use `config.yaml` or Pydantic settings.

## 3. Forbidden Patterns
- ❌ **Data Leakage:** Applying `fit_transform` on the entire dataset before splitting.
- ❌ **Scalar Loops:** Using Python loops for operations that can be vectorized in PyTorch/NumPy.
- ❌ **Missing Seeds:** Failing to set `torch.manual_seed()` and `np.random.seed()` for reproducibility.
- ❌ **Hardcoded Configs:** Scattering hyperparameters throughout the codebase.

## 4. Deep-Dive References
Consult the `references/` directory for detailed patterns and guides:
- `classical.md`
- `ops.md`
- `pytorch.md`
- `stack.md`
