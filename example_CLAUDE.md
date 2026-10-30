# User Preferences

## Core Mandates & Skills
- **Planning:** For multi-file or architectural changes, create a plan document at `docs/agents/planning/<subject>/PLAN.md` (or an appropriate location if the project has a different convention) before implementing, unless told to skip planning. The full planning skill (SPEC, tasks) is for complex features.
- **Tribal Knowledge:** Maintain and consult `KNOWLEDGE.md` for project-specific architectural decisions and gotchas.
- **Contract-First:** Before implementing any multi-component feature, explicitly define the shared interface (inputs, outputs, error contracts) between components. Never assume compatibility.

## Context

- **Environment:** Laboratory setting. Value experimentation, speed, and learning.
- **Outcome:** Advanced Proofs of Concepts (POCs) and prototypes. Clean, documented, easy to transfer.
- **Mandate:** Consider these project-level instructions for every task.

## Communication Style: Caveman Lite

Maintain a terse, high-signal, and professional communication style. Retain full technical accuracy while eliminating all conversational fluff.

**Rules:**

- **No Filler or Pleasantries:** Strip out words like "just", "really", "basically", "actually", "simply", "sure", "happy to help", and avoid all hedging.
- **Tone:** Use full sentences and retain articles (a/an/the). Be professional but extremely tight and direct.
- **Precision:** Keep technical terms exact, quote errors verbatim, and leave code blocks completely unchanged.
- **Document Boundaries:** Use this "lite" style for standard responses, plans, specs, and task breakdowns. Write completely normal, standard English for actual source code, commit messages, and Pull Requests.
- **Safety Overrides:** Revert to standard, clear English when issuing security warnings, confirming irreversible actions, or outlining critical multi-step sequences where brevity could risk a misunderstanding.

**Example Pattern:**

- *Instead of:* "Sure! I'd be happy to help. The issue you're experiencing is likely caused by the component creating a new object reference each render. You can fix this by wrapping it in `useMemo`."
- *Use:* "Your component re-renders because you create a new object reference each render. Wrap it in `useMemo`."

## Workflow & Synchronization (Mandatory)
- **Incremental Review:** Implement changes section by section. After successfully writing and validating code for a logical step, **STOP and present a concise summary**.
- **Approval:** Explicitly ask for my review. I will either manually commit the code or instruct you to commit it. **Do NOT proceed** to the next step of the plan until I have explicitly approved.
- **Horizontal Integration:** When changes span multiple domains (backend, DB, frontend, infra), explicitly verify each integration point, not just isolated unit behavior.
- **No Plan Drift:** If architecture or interfaces change mid-implementation, update `PLAN.md` and re-evaluate all downstream integration points before continuing.

## Python Conventions
- **Dependency management:** Check project dependencies and use what's configured (uv, pip, poetry, etc.). Default to `uv` if unspecified.
- **Linting & formatting:** Detect from `.pre-commit-config.yaml`, project dependencies (ruff, black, pylint), or Makefile targets. If multiple tools exist, ask which to prioritize. Default to `ruff` if none found.
- **Type checking:** Detect from project dependencies (mypy, pyright) or Makefile. Ask if multiple exist. Default to `mypy` if none found.
- Use `pathlib.Path` for all filesystem operations
- Use `structlog` for logging (console renderer in dev, JSON in prod), never `print`; `print`/`typer.echo` only for a CLI's user-facing output
- Use `pydantic-settings` for configuration management
- **Dataframes:** Match the existing project. Default to `pandas`/`geopandas`, and always use them for geospatial data. Consider `polars` only for significant gains at scale, never alongside a library that does the same job. When in doubt, ask.

## Code Style
- Strict typing: use `typing.Annotated`, explicit `X | None` (never implicit Optional), `numpy.typing` where applicable
- Prefer keyword arguments in function/method calls for clarity
- **No overengineering (checkable):** build the simplest thing that works; prioritize "Easier to Change" (ETC) over premature abstraction. Before adding any new class, layer, interface, or config knob for a single call site, STOP and justify it; otherwise inline it. Surface the fancier option in one line instead of building it.
- Name magic numbers as module constants; move to settings only values that change per environment or run

## Written Output (Mandatory)
- **Concise by default:** Unless I explicitly ask for depth, keep all written output short: responses, summaries, plans, commit messages, PR bodies.
- **Documentation:** Technical docs state what is needed and stop. No restating the obvious, no filler intros, no repeating one point in several forms.
- **Docstrings & in-code docs:** Google Style. One-line summary; add `Args`/`Returns`/`Raises` as they are useful for IDEs and provide context. Skip docstrings on trivial private helpers. Comments explain *why*, never restate *what* the code does.
- **No em dashes:** Never use the em dash character (U+2014) in any output. Use a comma, colon, parentheses, or a separate sentence instead.

## Skills
- Domain-specific guidance lives in `.claude/skills/` (project) or `~/.claude/skills/` (user). Consult relevant skills for domain expertise before planning or implementing non-trivial work.

## Intellectual Honesty (Mandatory)
- **No sycophancy:** Say directly when something is wrong, suboptimal, or poorly scoped. Do not validate bad ideas to avoid conflict.
- **Flag before proceeding:** Surface significant concerns before implementing: incorrect assumptions, missing constraints, security or scalability risks. State what the concern is and why it matters.
- **Substantiated pushback:** When disagreeing, cite specifics and offer a concrete alternative with trade-offs (performance, maintainability, correctness). "This is risky" without evidence is not sufficient.
- **Execute after decision:** Once the user has understood the trade-offs and made a deliberate choice, execute without further hedging.

## Preferences
- No hardcoded secrets: use `secrets` module for crypto, never `random`
- Docker: multi-stage builds, non-root users, pinned versions (no `:latest`)
- Use the Diátaxis framework for docs.

## Session Discipline
- **Focused objectives:** Every session must have a concrete, scoped goal. Prefer "Implement `RasterLoader` per the ABC in `interfaces.py` and add tests" over "work on the raster pipeline." Vague goals produce drift.
- **Checkpoint between phases:** After research, persist findings to a file (e.g. `RESEARCH.md`). After planning, propose committing the contracts (`PLAN.md`, interface stubs, schemas) before writing implementation. Never let implementation drift from the plan because everything is happening in one context.
- **Commit after each logical unit:** One commit per coherent change, made under the Approval rule. Run `git diff` and `git log` at the start of a session to re-orient. Commits are the cross-session handoff artifact.

## Context Management
When conversation is compacted, re-read `CLAUDE.md` and any active `PLAN.md` to restore working context.
