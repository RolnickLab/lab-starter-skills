# CHANGES.md

## [Unreleased](https://github.com/f-PLT/lab-starter-skills/tree/main) (latest)

______________________________________________________________________

- CI: pre-commit on PRs and `main`, plus a full-history gitleaks scan.
- Weekly lychee link check on all Markdown.
- `check-skills` pre-commit hook: validates `SKILL.md` frontmatter and that `references/` files match their mentions.
- Fix `code-review` skill frontmatter: quote the description so it parses as YAML.

## [0.1.0](https://github.com/f-PLT/lab-starter-skills/tree/0.1.0) (2026-10-30)

______________________________________________________________________

- Initial skill set:
  - `example_CLAUDE.md`: top-level instructions template (communication style, workflow gates, Python conventions).
  - `code-review` skill: two-phase review workflow with automated QA script.
  - `geospatial` skill: vector/raster processing, CRS handling, sensor selection, remote sensing preprocessing, geospatial ML.
  - `ml` skill: ML research engineering for climate and biodiversity work: evaluation under distribution shift, agent guardrails, Pydantic config schemas (optional Hydra), SLURM on Mila and DRAC, domain pitfalls, and an operationalization checklist (TRL 6-7) for partner handoff.
  - `planning` skill: three-phase planning workflow (Formal Design, Spec, Tasks) with TDD.
  - `root-cause-analysis` skill: evidence-based debugging methodology.
  - `software-dev` skill: full-stack engineering standards with Bash and Python deep-dives.
