# CHANGES.md

## [Unreleased](https://github.com/f-PLT/lab-starter-skills/tree/main) (latest)

______________________________________________________________________

- **Breaking:** rename the `code-review` skill to `strict-review`, so it no longer clashes with Claude
  Code's built-in `/code-review` and the Gemini CLI `code-review` extension. Delete your old copy
  (`~/.claude/skills/code-review` or `.claude/skills/code-review`) after installing the new one.
- `strict-review`: review changes of any size (change map, architecture review, triage, line-level
  pass) and write one tiered report. Run the project's own QA instead of `scripts/run_qa.py`. New
  references for Rust, Java, Bash, ML artifact loading, path traversal and infrastructure.
- **Breaking:** `planning`: four phases. New Phase 0 (PLAN Outline) scopes the work with the user
  and cuts it into stages. New layout: `<subject>/PLAN.md` plus
  `<subject>/NN-<slug>/{DESIGN.md, SPEC.md, tasks/}`; the FDD is now `DESIGN.md`. Move existing
  plans to the new layout.
- `planning`: add task-by-task execution in dependency order, with an approval gate per task, and
  resume an existing `PLAN.md`.
- `software-dev`: add `references/refactoring_legacy.md` for safely restructuring existing code.
- `example_CLAUDE.md`, `software-dev`, `planning`: call out bad design and outgrown patterns in the
  code the task touches; the user decides whether to fix, defer or keep.
- `planning`, `strict-review`, `root-cause-analysis`, `software-dev`, `geospatial`, `ml`: each
  shows structure as a small text view (shape diff of file or call tree, failing call path, or
  pipeline steps with CRS or tensor shape), adapted from humanlayer's `show-me` skill.

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
