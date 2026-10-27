# PLAN: Update `skills/ml` for the Rolnick Lab

## Goal

Retarget `skills/ml` from industry MLOps to the lab's actual path: student research code that reaches
TRL 6-7 (validated in a relevant environment, demonstrated as a prototype that partners can integrate).
Two audiences: students learning while using coding agents, and partners integrating our models.

## Decisions (approved)

- Full layout (below).
- Config: template-agnostic (no repo-specific paths or class names). A validated Pydantic schema is the
  contract (`extra="forbid"`, frozen, typed bounds, `Literal` for dispatch fields, one root config per run,
  logged at startup). YAML files stay Hydra-compatible; `defaults:` composition works without Hydra via a
  minimal loader for the subset both read identically. Hydra is a **suggestion** for CLI overrides and
  sweeps, converging on the same schema (`Config(**OmegaConf.to_container(cfg, resolve=True))`).
  Layers kept separate: per-machine env (`.env`, pydantic-settings) vs per-run experiment config.
- Clusters: Mila + DRAC.
- Drop LLM serving/quantization content.
- Keep production concerns, framed as operationalization (TRL 6-7), not enterprise MLOps.

## Constraints

- `SKILL.md` <= ~50 lines; each reference <= ~45 lines. Terse bullets, no filler, no em dashes.
- Self-contained: copy the geospatial ML essentials (spatial CV, chipping, tiled inference, RS backbones) into `ml`
  instead of linking to `skills/geospatial`; agents do not reliably read both skills. Keep both copies in sync.
- Cluster specifics (partitions, quotas) go stale: state the principle, link official docs.
- Do not contradict `example_CLAUDE.md` (pandas/geopandas, pydantic-settings, structlog, pathlib).

## Layout and contents

| File | Action | Contents |
|---|---|---|
| `SKILL.md` | Rewrite | Philosophy (valid eval > SOTA number; reproducible; built to be integrated). Agent guardrails as forbidden patterns: no split/metric/test changes to fix results, no unrun numbers, no test-set tuning, no single-seed claims. Sanity ladder. Opt-in learning mode. Reference index. |
| `references/evaluation.md` | New | Group/site/time splits, geographic transfer (ID vs OOD), open-set, baselines first, equal tuning budget, seeds + CIs, long-tail metrics, calibration. |
| `references/pytorch.md` | Fix | Grad clipping as config, `weights_only=True` + safetensors for releases, full determinism, drop LLM section, sanity checks, checkpoint/resume hooks. |
| `references/classical.md` | Fix | Group-aware CV, long-tail/imbalance metrics; keep pipelines + Parquet. |
| `references/stack.md` | Fix | pandas/geopandas, xarray + zarr/netCDF; Lightning optional; config section per Decisions (Pydantic contract, optional Hydra); W&B; drop Polars/Triton/vLLM; trim forbidden list. |
| `references/cluster.md` | New | Mila + DRAC: `$SLURM_TMPDIR` staging, checkpoint/resume on preemption/time limit, W&B offline on DRAC, CPUs from allocation, smoke test before sweeps, job arrays. |
| `references/operationalization.md` | New, replaces `ops.md` | TRL 6-7 checklist: pinned env, reproduce-table command, inference API boundary (typed I/O schema, batch + tiled inference), packaged weights (HF Hub/Zenodo, safetensors, optional ONNX), model/dataset cards + license, Docker, input validation, shift checks when deploying to new regions/sites, CI on fixtures, partner handoff doc. |
| `references/domains.md` | New | Biodiversity/camera traps, SDM, climate/scientific ML, remote sensing (chipping, normalization, backbones, augmentation), GNNs/materials. |
| `references/ops.md` | Delete | Content folded into `operationalization.md` and `cluster.md`. |
| `README.md`, `CHANGES.md` | Update | Skill description line; changelog entry. |

## Steps (one review stop per step, all done)

1. `SKILL.md`
2. `evaluation.md`
3. `pytorch.md` + `classical.md`
4. `stack.md`
5. `cluster.md`
6. `operationalization.md` (+ delete `ops.md`)
7. `domains.md`
8. `README.md`, `CHANGES.md`, final consistency pass (cross-links, line budgets, no em dashes)
