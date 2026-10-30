---
name: ml
description: ML research engineering for climate, biodiversity and Earth science projects. Experiment design, valid evaluation under distribution shift, reproducible training on SLURM clusters (Mila, DRAC), and operationalizing research models so partners can integrate them (TRL 6-7).
---

# Machine Learning Skill Instructions

## 1. Core Philosophy
- **Valid evaluation > SOTA number:** A result counts only if its split, metric and baselines match the deployment question (new sites, regions, years, species).
- **Reproducible by default:** Code version + data version + config + seeds = the result. Every reported number traces back to a logged run.
- **Built to be integrated:** Research code should reach a state where a partner can install it, run inference on their own data, and know where it fails.
- **Simple first:** Baseline and small model before large model. Added complexity stays only if it beats the baseline.

## 2. Engineering Preferences
- **Config:** One validated Pydantic schema per run (frozen, `extra="forbid"`, typed bounds), loaded from YAML and logged at startup. Hydra optional for overrides and sweeps. See `stack.md`.
- **Tracking:** Log full config, metrics, git SHA, data version and seed to W&B or MLflow.
- **Splits:** Split by group (site, trap, station, region, year) whenever samples are correlated; never split correlated samples one by one. See `evaluation.md`.
- **Leakage:** Fit normalization, class weights and any statistic on the training split only.
- **Seeds:** Report at least 3 seeds (mean ± std or CI). Training is sensitive to initial conditions, so a single-seed gain is not a result.
- **Sanity ladder before long runs:**
  1. Loss at init matches expectation (about `log(C)` for C-class cross-entropy).
  2. Model overfits a single batch.
  3. Simple baseline beats chance.
  4. Full job passes a short 1-GPU smoke test.
- **Performance:** Vectorize with framework ops, use AMP and efficient data loading. See `pytorch.md`.

## 3. Forbidden Patterns
- ❌ **Moving the goalposts:** Changing the split, metric, test data or evaluation code to improve a result. Report the bad result and stop. A real bug in one of them: get user approval, fix it, re-run every method.
- ❌ **Unbacked numbers:** Reporting a metric no run produced, or summarizing a run without its log or tracker link.
- ❌ **Test-set tuning:** Selecting hyperparameters, thresholds or checkpoints on the test set.
- ❌ **Unfair comparisons:** Claiming improvement from one seed, without a baseline, or with a larger tuning budget than the baselines got.
- ❌ **Silent data loss:** Dropping samples, classes or NaNs without logging counts.
- ❌ **Hardcoded hyperparameters:** Values scattered in code instead of the config schema.

## 4. Learning Mode (opt-in)
Activate when the user says they are learning or asks for teaching mode. Stays on for the session until the user turns it off.
- For each methodological choice (split, metric, loss, baseline), give the reason in 1-2 lines and name the concept so the user can look it up.
- Point to the specific lines to change rather than rewriting the user's code wholesale.

## 5. Deep-Dive References
Consult the `references/` directory:
- `evaluation.md`: splits under shift, OOD and open-set, baselines, seeds and statistics, metrics
- `domains.md`: biodiversity, SDM, climate and scientific ML, remote sensing (chipping, normalization, backbones), GNNs
- `pytorch.md`: performance, determinism, checkpointing, saving weights
- `classical.md`: tabular pipelines and cross-validation
- `stack.md`: libraries, config schema, Hydra
- `cluster.md`: SLURM on Mila and DRAC
- `operationalization.md`: TRL 6-7 handoff checklist for partners
