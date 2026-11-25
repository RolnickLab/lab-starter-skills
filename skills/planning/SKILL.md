---
name: planning
description: Four-phase planning workflow (PLAN Outline → Formal Design → Spec → Tasks) with TDD woven into every phase. Starts by working with the user on what they really need and how to cut it into stages. Use for complex features, architecture decisions, refactors, or any multi-step implementation.
---

# Planning Skill Instructions

## 1. Core Philosophy
- **Need Before Design:** Phase 0 settles what the user needs and why before any design work.
- **User Owns Scope:** The user decides how big a stage is and whether to split. The agent asks, challenges and records; it does not judge size on its own.
- **One Stage at a Time:** Design only the active stage. Later stages stay one-liners until their turn, so they can absorb what earlier ones taught.
- **Plan Before Code:** No implementation until Phases 1-3 of the active stage are approved.
- **TDD as the Spine:** Every artifact (DESIGN to SPEC to tasks) is oriented around the failing tests that will drive implementation.
- **Gate on Approval:** Each phase ends with a single approval question. Never advance without explicit user sign-off.
- **Write Back Upstream:** When a later phase changes something an earlier artifact states (step order, interface, test plan, scope), update that artifact (`DESIGN.md`, `SPEC.md`, `PLAN.md`) in the same phase, before its gate. Artifacts must never disagree.
- **Surface Your Own Decisions:** At every phase gate, list each decision in that phase's artifact the user did not state (assumptions, defaults, interpretations, added checks) and ask the user to confirm or change each. Mark them "(to confirm)" in the artifact until confirmed; record confirmed ones that affect later phases or stages in `PLAN.md` Decisions & Learnings.
- **Measurable Outcomes:** Every AC is a future passing test. Plans that can't be verified don't exist.

## 2. Layout
```
docs/agents/planning/<subject>/
  PLAN.md              # Phase 0 outline, stages list
  01-<slug>/           # one folder per stage, created when it becomes active
    DESIGN.md          # Phase 1
    SPEC.md            # Phase 2
    tasks/             # Phase 3
```
A single-stage plan still uses `01-<slug>/`, so tooling finds tasks in one place.

## 3. The Phases

### Phase 0: PLAN Outline
Work back and forth with the user, then write `PLAN.md` using `references/plan_outline_template.md`.

- **Discover:** Cover the problem, who has it, why now, what success looks like, the smallest version that is useful, constraints, what they do not want. Read the relevant code first so questions and options are grounded in it.
- **Ask interactively:** Use the `AskUserQuestion` tool when available (other agents: use your equivalent question tool, e.g. `ask_question` in Antigravity, `question` in OpenCode): one topic per question, 2-4 concrete options drawn from what you read (recommended one first, marked "(Recommended)"); the tool adds a free-form "Other" automatically. Every option must be a complete answer on its own; never offer an option that only makes sense with extra detail ("Mixed", "Depends", "Describe in Other"). If an answer still needs detail, ask a follow-up question before using it. Send up to 4 questions per call, then follow up on the answers. Skip questions the code or earlier answers already settle. Without the tool, ask the same questions as a numbered text batch.
- **Challenge:** If the request is a solution, ask for the need behind it. Reflect back what you heard ("so the real need is X, not Y?"). Say plainly when an idea seems unnecessary.
- **Guard scope:** Every idea that is not core goes to Non-goals or the Parking Lot, with the user's agreement.
- **Stages:** Ask the user whether to deliver in one stage or several, and help them name each one's goal and "done when". Do not split, merge or resize on your own.
- **Stage contracts:** With several stages, question the user about each boundary until it is unambiguous, so later stages do not undo earlier work:
  - What does each stage produce that a later one consumes (data, schema, API, files, behavior)?
  - Does a later stage impose requirements on an earlier stage's outputs or inputs (format, scale, CRS, auth, performance)?
  - Could a later stage change something an earlier one treats as fixed? If so, should that stage come first, or should the earlier stage leave that part open?
  - Which parts of a contract are frozen and which may still change?
  Use the answers to confirm or reorder stages with the user. Record each boundary in Stage Contracts.
- **Trivial exit:** If discovery shows the work is a small change (one or two files, no new interface), say so and propose skipping Phases 1-3: `PLAN.md` alone is enough.
- End with: *"Shall I proceed to Phase 1: Formal Design for stage 01-<slug>?"*

### Phase 1: Formal Design Document (DESIGN)
Write a five-section DESIGN to `<subject>/<NN>-<slug>/DESIGN.md` using `references/fdd_template.md`. Scope is the active stage only.

- **Honor stage contracts:** The design must produce what `PLAN.md` Stage Contracts promise later stages, and consume only what earlier stages promised. If the design needs to change a contract, stop and amend `PLAN.md` with the user first.

- **Section 3 (Verification & FMEA)** must name the tracer-bullet integration test written first; this is the Red entry point for Phase 3.
- **Section 4 (Implementation Steps)** must be sequenced so each step maps to a Red-Green-Refactor cycle.
- End with: *"Shall I proceed to Phase 2: SPEC creation?"*

### Phase 2: Specification (SPEC)
Draft `<subject>/<NN>-<slug>/SPEC.md` using `references/spec_template.md`.

- **ACs must be written as test sentences**: each AC is a Red test waiting to be written.
- **Verification Plan** is the ordered list of tests matching DESIGN Section 4 steps.
- Gate: STOP. Get explicit sign-off before Phase 3.

### Phase 3: Task Decomposition
Decompose DESIGN Section 4 into atomic task documents at `<subject>/<NN>-<slug>/tasks/`. Use `references/task_structure.md` for the canonical 7-section format.

- **Context-Complete:** Each task document must contain everything needed for implementation; no cross-task lookups or memory reliance.
- **Vertical Slices:** Each task delivers a full slice (interface → implementation → test). Never horizontal layers (all DB tasks, then all API tasks).
- **Contract-First Ordering:** If tasks share an interface, the contract-definition task comes first.
- **Fail-Fast Validation:** Include concrete CLI commands (not prose) in the Testing & Validation section of each task.
- Each task follows **Red → Green → Refactor**:
  1. **Red**: Write failing test(s) defining the behavior.
  2. **Green**: Write minimum code to pass.
  3. **Refactor**: Clean up on green; consult `references/refactoring.md`.
- Tasks ordered by dependency; no task assumes a later one is done.

## 4. Stage Lifecycle
- **Start:** Only one stage is `active`. Another may run alongside only if `PLAN.md` marks it `parallel-ok` with a reason (no shared interfaces or files) and the user approved it.
- **Close:** When all tasks of a stage are done, update `PLAN.md`: set status `done`, add learnings to Decisions & Learnings, check the delivered outputs against Stage Contracts, and review later stages and the Parking Lot with the user. Then ask: *"Stage NN is done. Shall I start Phase 1 for stage NN+1-<slug>?"*
- **Scope change mid-stage:** New ideas go to the Parking Lot. Changing the active stage requires amending `PLAN.md` (and SPEC if already approved) and re-approval.

## 5. Forbidden Patterns
- ❌ **Skipping Phases:** No DESIGN before PLAN approval; no SPEC before DESIGN approval; no tasks before SPEC approval.
- ❌ **Designing Ahead:** No DESIGN, SPEC or tasks for a stage that is not active.
- ❌ **Fuzzy Boundaries:** Starting Phase 1 for a stage while a contract it touches is unclear.
- ❌ **Agent-Sized Scope:** Splitting, merging or resizing stages without the user deciding.
- ❌ **Upstream Drift:** Tasks, SPEC or DESIGN contradicting an earlier artifact that was not updated.
- ❌ **Silent Decisions:** Passing a phase gate with agent-made decisions the user has not seen.
- ❌ **Silent Scope Drop or Add:** Every cut idea goes to Non-goals or the Parking Lot; every addition goes through `PLAN.md`.
- ❌ **Vague ACs:** Every AC must have a clear pass/fail state.
- ❌ **Skipping Red:** For new testable behavior, never write implementation before a failing test. Config, IaC, docs and exploratory spikes are exempt.
- ❌ **Refactor on Red:** Only refactor after tests are green.
- ❌ **Mocking Internals:** Mock only at system boundaries. See `references/mocking_strategy.md`.
- ❌ **Horizontal Decomposition:** "Task 1: all models, Task 2: all endpoints"; always slice vertically.
- ❌ **Implicit Context:** Referencing "the schema from Task 2" without including the relevant excerpt inline.
- ❌ **Prose-Only Validation:** "Verify the feature works" is not a test; name the exact command and expected output.

## 6. Deep-Dive References
- `plan_outline_template.md`: PLAN outline template (Phase 0)
- `fdd_template.md`: Annotated Formal Design Document template (Phase 1)
- `spec_template.md`: Canonical SPEC template with pre-approval checklist
- `task_structure.md`: Canonical 7-section task document template
- `good_bad_tests.md`: Brittle vs. high-signal behavior tests
- `mocking_strategy.md`: Boundary classification and mock strategy
- `deep_modules.md`: Interface design for testability
- `interface_design.md`: Dependency Injection and Pure Functions
- `refactoring.md`: Code smells to address after green cycle
