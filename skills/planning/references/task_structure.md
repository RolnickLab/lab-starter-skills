# Task Document: Annotated Template

Use this template verbatim for every task file produced in Phase 3 of the planning skill.
File naming convention: `tasks/TASK-NNN-<slug>.md` (NNN = zero-padded dependency order).

---

```markdown
# TASK-NNN: <Title: imperative verb + subject>

## 1. Goal
One or two sentences. State the observable outcome, not the mechanism.
Bad: "Add a database migration file."
Good: "Persist user preferences across sessions via a new `preferences` table."

## 2. Context & References
- **Plan section:** Link or quote the relevant excerpt from PLAN.md / SPEC.md.
- **Upstream tasks:** List any TASK-NNN this depends on, and inline the relevant
  interface/schema excerpt so this task is self-contained.
- **Key files:** Paths to existing files this task touches or extends.
- **Relevant skills:** List skills whose principles apply (e.g., `software-dev`, `ml`, `geospatial`).

## 3. Subtasks
Granular, atomic steps ordered by dependency. Each step is one logical unit of work.

- [ ] 1. <Imperative verb + subject>: one-line outcome description
- [ ] 2. <Imperative verb + subject>: one-line outcome description
- [ ] 3. Write failing test(s) covering the AC before implementation (TDD Red step)
- [ ] 4. Implement until tests pass (TDD Green step)
- [ ] 5. Refactor while keeping tests green

## 4. Requirements & Constraints
- **Technical:** Specific library versions, API contracts, data formats, performance budgets.
- **Business:** Rules that must hold (e.g., "idempotent on retry", "backward-compatible").
- **Out of scope:** Explicitly state what this task does NOT cover.

## 5. Acceptance Criteria
Pass/fail statements. If all are true, the task is done.

- [ ] AC-1: <Measurable, binary condition>
- [ ] AC-2: <Measurable, binary condition>
- [ ] AC-3: All new code passes the project's linting and type-checking tools with zero errors.
- [ ] AC-4: Test suite passes with no regressions (`pytest -x`).

## 6. Testing & Validation
Concrete commands, copy-pasteable, not prose.

```bash
# Run targeted tests
pytest tests/path/to/test_module.py -v

# Type-check
mypy src/module/file.py

# Lint
ruff check src/module/file.py

# Integration smoke test (if applicable)
<command that exercises the full slice end-to-end>
```

Expected output or exit codes for each command when the task is complete.

## 7. Completion Protocol
Mandatory steps before marking this task done:

1. Verify every AC is checked off in Section 5.
2. Run all commands in Section 6 and confirm expected output.
3. Update this file: check off completed subtasks and ACs, note any deviations.
4. Notify the user with a concise summary, propose the commit, and request approval before the next task:
   ```bash
   git add <specific files>
   git commit -m "feat(scope): <what was done> (closes TASK-NNN)"
   ```
   Commit only when the user says so.
```

---

## Per-Section Guidance

### Section 1: Goal
The goal is the north star. It should be readable without any other context. If a
reviewer cannot tell whether the task is done from the goal alone, rewrite it.

### Section 2: Context & References
Self-containment is non-negotiable. Copy the relevant interface signature or schema
fragment inline; do not just link to another task file. Links rot; inline excerpts travel.

### Section 3: Subtasks
Always include the TDD Red/Green/Refactor triplet when writing new behavior. The
failing test must come before the implementation subtask in the list.

### Section 4: Requirements & Constraints
The "out of scope" line prevents scope creep. Be explicit: "This task does NOT handle
authentication, see TASK-005."

### Section 5: Acceptance Criteria
Each AC must be binary (pass/fail). If it requires judgment ("the UI looks clean"),
convert it to an objective proxy ("Lighthouse accessibility score ≥ 90").

### Section 6: Testing & Validation
Paste the exact commands a reviewer would run. Include expected exit codes or output
snippets so there is no ambiguity about what "passing" means.

### Section 7: Completion Protocol
The commit message format (`feat(scope): ... (closes TASK-NNN)`) provides a machine-
readable link between commits and tasks. Never skip the user-approval step; it is the
cross-session handoff artifact.
