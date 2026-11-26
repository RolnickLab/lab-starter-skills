# PLAN Outline: Annotated Template

Use for Phase 0. Stored at `docs/agents/planning/<subject>/PLAN.md`. Keep it short: this is the
core idea and the why, not the design. Design lives in each stage's `DESIGN.md`.

---

```markdown
# PLAN: <Subject>

## 1. Problem & Why
What hurts today, for whom, and why it matters now. 2-4 sentences. No solutions.

## 2. Outcome & Success Criteria
What is true when this is done. Observable, checkable statements.
- [ ] ...

## 3. Constraints
Hard limits: tech stack, compatibility, deadlines, data, team.

## 4. Non-goals
What this plan deliberately does not do. Each line closes a door.

## 5. Stages
| # | Slug | Goal | Done when | Depends on | Status |
|---|------|------|-----------|------------|--------|
| 01 | <slug> | <one line> | <one checkable line> | - | active |
| 02 | <slug> | <one line> | <one checkable line> | 01 | later |

Status values: `active`, `later`, `done`, `dropped`. Two stages may be `active` together only
if marked `parallel-ok` in "Depends on" with a one-line reason, and the user approved it.

## 6. Stage Contracts
One entry per boundary. Omit for a single-stage plan.

### 01 → 02
- **01 provides:** <data, schema, API, files, behavior>
- **02 requires of 01:** <constraints on 01's outputs or inputs>
- **Frozen:** <what 02 may rely on unchanged>
- **Open:** <what 01 deliberately leaves for 02 to decide>

## 7. Parking Lot
Ideas raised during discovery or implementation that are not in scope. Not commitments.
- ...

## 8. Decisions & Learnings
Dated, one line each. Record why a choice was made or what a stage taught us.
- YYYY-MM-DD: ...
```

---

## Checklist (before asking for approval)
- [ ] Problem states a need, not a solution
- [ ] Every success criterion is checkable
- [ ] Non-goals exist (an empty list usually means scope was not discussed)
- [ ] Stages were defined or confirmed by the user, not by the agent alone
- [ ] Only the active stage has detail; later ones are one-liners
- [ ] Every stage boundary has a contract; no "Requires" item is a guess
- [ ] Stage order follows the contracts (no stage depends on a later one)
- [ ] Ideas cut during discovery are in the Parking Lot, not silently dropped
- [ ] Every agent-made decision is marked "(to confirm)" and was put to the user
