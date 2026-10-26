---
name: planning
description: Three-phase planning workflow (Formal Design → Spec → Tasks) with TDD woven into every phase. Use for complex features, architecture decisions, refactors, or any multi-step implementation.
---

# Planning Skill Instructions

## 1. Core Philosophy
- **Plan Before Code:** No implementation until all three phases are complete and approved.
- **TDD as the Spine:** Every artifact (FDD to SPEC to tasks) is oriented around the failing tests that will drive implementation.
- **Gate on Approval:** Each phase ends with a single approval question. Never advance without explicit user sign-off.
- **Measurable Outcomes:** Every AC is a future passing test. Plans that can't be verified don't exist.

## 2. The Three Phases

### Phase 1: Formal Design Document (FDD)
Produce a five-section FDD using `references/fdd_template.md`.

- **Section 3 (Verification & FMEA)** must name the tracer-bullet integration test written first; this is the Red entry point for Phase 3.
- **Section 4 (Implementation Steps)** must be sequenced so each step maps to a Red-Green-Refactor cycle.
- End with: *"Shall I proceed to Phase 2: SPEC creation?"*

### Phase 2: Specification (SPEC)
Draft `docs/agents/planning/<subject>/SPEC.md` using `references/spec_template.md`.

- **ACs must be written as test sentences**: each AC is a Red test waiting to be written.
- **Verification Plan** is the ordered list of tests matching FDD Section 4 steps.
- Gate: STOP. Get explicit sign-off before Phase 3.

### Phase 3: Task Decomposition
Decompose FDD Section 4 into atomic task documents at `docs/agents/planning/<subject>/tasks/`. Use `references/task_structure.md` for the canonical 7-section format.

- **Context-Complete:** Each task document must contain everything needed for implementation; no cross-task lookups or memory reliance.
- **Vertical Slices:** Each task delivers a full slice (interface → implementation → test). Never horizontal layers (all DB tasks, then all API tasks).
- **Contract-First Ordering:** If tasks share an interface, the contract-definition task comes first.
- **Fail-Fast Validation:** Include concrete CLI commands (not prose) in the Testing & Validation section of each task.
- Each task follows **Red → Green → Refactor**:
  1. **Red**: Write failing test(s) defining the behavior.
  2. **Green**: Write minimum code to pass.
  3. **Refactor**: Clean up on green; consult `references/refactoring.md`.
- Tasks ordered by dependency; no task assumes a later one is done.

## 3. Forbidden Patterns
- ❌ **Skipping Phases:** No SPEC before FDD approval; no tasks before SPEC approval.
- ❌ **Vague ACs:** Every AC must have a clear pass/fail state.
- ❌ **Skipping Red:** Never write implementation before a failing test.
- ❌ **Refactor on Red:** Only refactor after tests are green.
- ❌ **Scope Creep in Flight:** Mid-implementation requirement changes require SPEC amendment and re-approval.
- ❌ **Mocking Internals:** Mock only at system boundaries. See `references/mocking_strategy.md`.
- ❌ **Horizontal Decomposition:** "Task 1: all models, Task 2: all endpoints"; always slice vertically.
- ❌ **Implicit Context:** Referencing "the schema from Task 2" without including the relevant excerpt inline.
- ❌ **Prose-Only Validation:** "Verify the feature works" is not a test; name the exact command and expected output.

## 4. Deep-Dive References
- `fdd_template.md`: Annotated Formal Design Document template
- `spec_template.md`: Canonical SPEC template with pre-approval checklist
- `good_bad_tests.md`: Brittle vs. high-signal behavior tests
- `mocking_strategy.md`: Boundary classification and mock strategy
- `deep_modules.md`: Interface design for testability
- `interface_design.md`: Dependency Injection and Pure Functions
- `refactoring.md`: Code smells to address after green cycle
- `task_structure.md`: Canonical 7-section task document template
