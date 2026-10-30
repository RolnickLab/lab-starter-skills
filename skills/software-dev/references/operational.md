# Operational Standards

## Dependency Management
Always use deterministic builds with lockfiles.
*   **Python:** `uv` or `poetry`.
*   **Rust:** `cargo`.
*   **Node/JS:** `pnpm` or `npm` (package-lock.json).
*   **Go:** `go mod`.

## Configuration
Use strict, schema-validated configuration.
*   **Rule:** Fail fast at startup if configuration is invalid.
*   **Pattern:** Load environment variables into a typed object/struct immediately.
*   **Tools:** `pydantic-settings` (Python), `zod` (Node), `envy` (Rust).

## Chesterton's Fence
Before recommending a rewrite or removal of code:
1.  Explain the likely reason the code exists.
2.  Demonstrate how the new design handles those same constraints.
3.  Only then propose the change.

## CI/CD Checklist
*   **Linting:** Automated style enforcement.
*   **Type Checking:** Static analysis before merge.
*   **Automated Testing:** Unit + Integration tests mandatory.
*   **Contract Testing:** Validate API boundaries.
