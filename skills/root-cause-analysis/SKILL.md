---
name: root-cause-analysis
description: Specialized guidance for analyzing errors, bugs, and software failures. Activate this skill whenever the user asks for help explaining, debugging, or fixing a problem in the code to find the root cause and avoid distractions.
---

# Root Cause Analysis Skill Instructions

## 1. Core Philosophy
- **Evidence Over Assumption:** Never guess. Rely on tracebacks, logs, and reproducible state.
- **Permanent Remediation:** Fix the root cause, not just the symptom. If that needs an architectural change, propose it for approval instead of patching the symptom silently.
- **Occam's Razor:** Prefer the simplest explanation that fits all observed facts.

## 2. Engineering Preferences
- **Evidence Gathering:** Extract exact error messages and capture environment state.
- **Reproduction:** Create a Minimal Reproducible Example (MRE) to isolate the failure.
- **The 5 Whys:** Distinguish the triggering event (e.g., "invalid input") from the root cause (e.g., "missing input validation").
- **Verification:** Always propose a test case alongside the fix to ensure permanent remediation.

## 3. Forbidden Patterns
- ❌ **Patching Symptoms:** Adding a `try/except` block to hide an error without understanding why it occurred.
- ❌ **Distractions:** Refactoring unrelated "code smells" while hunting a critical bug.
- ❌ **Assuming Correctness:** Assuming a module works perfectly without empirical proof.

## 4. Deep-Dive References
Consult the `references/` directory for detailed patterns and guides:
- `methodology.md`
