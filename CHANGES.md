# CHANGES.md

## [Unreleased](https://github.com/f-PLT/lab-starter-skills/tree/main) (latest)

______________________________________________________________________

- **Breaking:** rename the `code-review` skill to `strict-review`, so it no longer clashes with Claude
  Code's built-in `/code-review` and the Gemini CLI `code-review` extension. Delete your old copy
  (`~/.claude/skills/code-review` or `.claude/skills/code-review`) after installing the new one.
- `strict-review`: replace `scripts/run_qa.py` with a directive: find the project's own QA (CI, task
  runners, then language defaults), run every check, never rewrite lockfiles, report a `QA:` line. A
  project with no QA is a NEEDS WORK finding that suggests tools.
- `strict-review`: add review scope, verdict rules, mandatory failure scenarios for security and
  correctness findings, severity ordering, and a pre-QA check of changes from other authors.
- `strict-review`: review changes of any size. Map the change into parts and how they connect, run
  an architecture review, triage what gets a deep look, then one line-level pass. Over 1000 deep
  lines, the report flags the scope as too large and recommends follow-up reviews per part, with the
  QA to reuse; it never splits on its own.
- `strict-review`: one tiered report: scope, focus, verdict, QA, map, must-fix, follow-up PRs,
  practices, split plan, findings in detail (design `D` and code `C`, under Critical, High, Medium,
  Low), recommended follow-up reviews, then what to review manually, last so it can be removed
  before sharing with the contributor.
- `strict-review`: move the line-level rules to `references/line_review.md`.
- `strict-review` references: add Rust, Java and Bash, ML artifact loading, path traversal, and
  `infrastructure.md` (Docker, Kubernetes, Terraform/OpenTofu, cloud).
- `software-dev`: add `references/refactoring_legacy.md` for restructuring existing code:
  characterization tests, safe-step techniques (parallel change, branch by abstraction, strangler
  fig), mechanics and stop conditions. Linked from `planning/references/refactoring.md`.

## [0.2.0](https://github.com/f-PLT/lab-starter-skills/tree/0.2.0) (2026-11-17)

______________________________________________________________________

- Add readability considerations to the `software-dev` skill
- Add a `human review focus` section to the `code-review` skill to identify which parts of a review
  would benefit from a manual review due to their nature.

## [0.1.3](https://github.com/f-PLT/lab-starter-skills/tree/0.1.3) (2026-11-03)

______________________________________________________________________

- Fix link to DRAC env creation documentation in ML skills

## [0.1.2](https://github.com/f-PLT/lab-starter-skills/tree/0.1.2) (2026-10-30)

______________________________________________________________________

- README: correct the merge guidance. Claude Code loads all `CLAUDE.md` files without precedence between them, and a user-level skill shadows a same-named project skill.
- README: explain user-level vs project-level scope. `example_CLAUDE.md` is user-level only; skills can be installed at either level.

## [0.1.1](https://github.com/f-PLT/lab-starter-skills/tree/0.1.1) (2026-10-30)

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
