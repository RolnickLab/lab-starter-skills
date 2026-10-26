# Formal Design Document: Annotated Template

Use this template verbatim whenever the planning skill is active.
Copy the five headers exactly, including emoji prefixes.

---

## 1. 🎯 Scope & Context

**Purpose:** Anchor the reader immediately. State what problem is being solved,
what the current state is, and any hard constraints (time, tech stack, team size).

**Target length:** 2–4 sentences.

**Checklist:**
- [ ] Names the specific problem or feature being addressed
- [ ] Calls out constraints that will shape the design (e.g., "must remain backward-compatible")
- [ ] Does NOT propose solutions yet

---

## 2. 🧠 Architectural Approach (Trade-offs & Strategy)

**Purpose:** Justify *why* this approach was chosen over alternatives.
Reference established principles and be explicit about trade-offs accepted.

**Target length:** 3–6 bullet points or short paragraphs.

**Checklist:**
- [ ] Names the chosen pattern/strategy (e.g., event-driven, layered, CQRS)
- [ ] Cites a principle that supports the choice (SOLID, idempotency, CAP theorem)
- [ ] Acknowledges at least one rejected alternative and why it was rejected
- [ ] States accepted trade-offs (e.g., "higher memory usage for lower latency")

---

## 3. 🛡️ Verification & Failure Modes (FMEA)

**Purpose:** Prove the design is testable and identify how it can fail before
anyone writes a line of code.

**Target length:** 2–4 bullets per sub-section.

**Sub-sections:**
- **Test Strategy**: unit, integration, contract, E2E coverage points
- **Known Risks**: bottlenecks, edge cases, security considerations, data integrity

**Checklist:**
- [ ] At least one concrete test type is named per critical component
- [ ] At least one failure mode is listed per external dependency
- [ ] Security surface is acknowledged (auth, input validation, secrets handling)

---

## 4. 📋 Granular Implementation Steps

**Purpose:** Give a numbered, actionable task list. Each step is one modular
chunk of work that can be reviewed independently.

**Target length:** 4–10 steps depending on scope.

**Format:**
```
1. **Action verb + subject**: one-line description of outcome
2. **Action verb + subject**: one-line description of outcome
```

**Checklist:**
- [ ] Every step starts with an imperative verb (Create, Add, Refactor, Wire, Test)
- [ ] Steps are ordered by dependency (no step assumes a later step is done)
- [ ] Each step is small enough to review in a single diff

---

## 5. ⏭️ Next Step

**Purpose:** Maintain momentum by ending with a single, focused approval request.
Do not ask multiple questions.

**Format:**
> Shall I proceed with Step 1: [brief description of Step 1]?

**Checklist:**
- [ ] Exactly one question
- [ ] References Step 1 by name/description so the user knows what they are approving
- [ ] No trailing commentary after the question
