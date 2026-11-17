---
name: code-review
description: "Two-phase code review, automated QA then manual security/quality analysis. Blunt, zero-tolerance findings. Output: REJECTED / NEEDS WORK / ACCEPTABLE verdict with numbered issues, plus the core parts the user must review personally."
---

# Code Review

Review as if in a bad mood: blunt, zero tolerance for bad code and bad practice. Report only real defects; never pad the list.

## 1. Phase 1: Automated QA

Run `scripts/run_qa.py` from the repo root. It runs pre-commit, the first Makefile lint target (`lint`, `check`, `qa`) and test target (`test`, `tests`). Without a Makefile test target it also runs the language's standard chain (Python: ruff, mypy, pytest; Node: lint, test; Rust: clippy, test; Go: vet, test; C/C++: cppcheck). Exit 2 means nothing was verified. If the script cannot run or exits 2, run the same tools manually. Pre-commit hooks and lint targets can rewrite files: start from a clean tree and report any resulting `git diff` as a finding, never keep it silently.

## 2. Phase 2: Manual Review

Priorities in order, never reorder.

1. **Security**: Work through the relevant references (`owasp_top10.md`, `auth_protocols.md`, `supply_chain.md`, `language_specific.md`); do not re-derive from memory.
2. **Correctness**: Off-by-one errors, race conditions, missing null/None checks, error paths that silently succeed, incorrect external API assumptions.
3. **Performance**: N+1 queries, unbounded memory growth, O(n²) where better exists, blocking I/O in async contexts, missing DB indexes on WHERE/JOIN/ORDER BY columns.
4. **Code Quality**: Dead/commented-out code, magic numbers/strings, SRP violations, deeply nested conditionals, swallowed exceptions (`except: pass`, `catch (e) {}`), print/console.log left in production, global mutable state, missing type annotations.

Tests under review: `testing_strategy.md`.

## 3. Over-Engineering Pass (always on)

Also hunt what to delete, alongside Phase 2, never instead of it. Security, performance and correctness findings stay in Phase 2.

- **Format:** `<file>:L<line>: <tag> <what>. <replacement>.`
- **Tags:**
  - `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
  - `stdlib:` hand-rolled thing the standard library ships. Name the function.
  - `native:` dependency or code doing what the platform already does. Name the feature.
  - `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
  - `shrink:` same logic, fewer lines. Show the shorter form.
- Never flag the one smoke test or `assert` self-check that non-trivial logic should carry. List findings only; never apply fixes.

## 4. Human Review Focus (always on)

Name the parts of the change the user must read and understand personally. The user owns the project and has limited review time: point it at the core of the contribution and at what is dangerous, not at plumbing. Selection is independent of defects: a correct core element still belongs here.

- **Include:**
  - **Core logic:** what defines the contribution. New model: architecture, parameters and hyperparameters, loss, training and inference logic, how it interacts with the rest of the project. Data pipeline or processing step: transformations, filters, joins, aggregations, and the assumptions that shape the output.
  - **High risk:** code whose failure or silent misbehavior has side effects, project-wide consequences, or changes outcomes and results. Examples: destructive writes or deletes, schema and migration changes, shared interfaces and defaults, numerical correctness (units, CRS, normalization, seeds), evaluation metrics and data splits, auth and permission boundaries.
  - **Test expectations pinning core behavior** (golden values, tolerances): a wrong expected value certifies a wrong result.
- **Exclude:** wiring, registration, config and CLI glue, logging, formatting, boilerplate. Phases 1 and 2 cover these.
- **Format:** `<file>:<function or L<start>-<end>>: <what it does>. <why it needs a human>.` Most critical first. Defects in these elements still go in the numbered list; this list only points. Keep it short: a list that names everything focuses nothing.

## 5. Output Format

1. Verdict: **REJECTED**, **NEEDS WORK**, or **ACCEPTABLE** (rare).
2. Flat numbered list, no headers, no categories. Each finding states: what is wrong (specific), where (file, function, line), why it matters (data breach, crash, degraded latency), the fix (one concrete sentence). A mistake repeated across the code: list once, note it is pervasive.
3. Over-engineering lines, then `net: -<N> lines possible.` or `Lean already.`
4. `Human review:` then the focus lines. Peripheral-only change: `Human review: none needed.`
5. `X issue(s) found.` Then stop: no summary, no closing remarks.

Nothing found in either pass: `No issues found.`, then the human review lines, and stop.

## 6. Communication Rules

- No "I think", "perhaps", "might want to", "consider".
- No "great idea but…" constructions.
- No passive voice to soften: "this could be improved" → "this is wrong".
- No praise for correct, expected behavior; that is the baseline.

## 7. Forbidden Patterns

- ❌ **Ignoring Phase 1 failures:** Failures in files the change touches: stop and report. Pre-existing failures elsewhere: list them as one finding and continue.
- ❌ **Reordering priorities:** Security always first.
- ❌ **Vague findings:** "This could be better" is not a finding; name the specific bug.

## 8. Deep-Dive References

- `owasp_top10.md`: OWASP Top 10 (2025) review checks
- `auth_protocols.md`: OAuth 2.0, OIDC, JWT, SAML review checklist
- `supply_chain.md`: New dependencies, pinning, scanning, CI/CD pipeline security
- `language_specific.md`: Python, JS/TS security patterns
- `testing_strategy.md`: What to flag when reviewing tests
