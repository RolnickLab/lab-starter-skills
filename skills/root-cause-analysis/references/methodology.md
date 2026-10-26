# Root Cause Analysis Methodology

This document outlines a structured approach to identifying and resolving software failures by focusing on the underlying "why" rather than just the "how."

## 1. The 5 Whys Framework
When an error occurs, ask "Why?" until the foundational cause is reached.
- **Example:** "The server crashed."
- **Why?** "It ran out of memory."
- **Why?** "A specific process consumed all available RAM."
- **Why?** "It was processing a large file in a single chunk instead of streaming."
- **Why?** "The original implementation didn't account for files > 100MB." (Root Cause)

## 2. Evidence-Based Investigation
- **Log Analysis:** Search for tracebacks, error codes, and preceding state transitions.
- **State Capture:** Identify the values of variables and environment state at the moment of failure.
- **Comparative Analysis:** What changed recently? Compare working vs. failing environments/inputs.

## 3. Reproduction & Isolation
- **Minimal Reproducible Example (MRE):** Strip away unrelated code until the error still triggers but the scope is minimal.
- **Binary Search (Git Bisect):** If it's a regression, identify the exact commit that introduced the failure.
- **Constraint Testing:** Change one variable at a time (input size, network speed, user permissions) to see if it affects the failure.

## 4. Common Failure Categories
- **Logical Flaws:** Incorrect assumptions about data flow or edge cases.
- **Resource Constraints:** Memory leaks, disk space, CPU throttling.
- **Concurrency Issues:** Race conditions, deadlocks, stale state.
- **Integration Failures:** Protocol mismatches, API timeouts, dependency versioning.
- **Environmental Factors:** Permissions, environment variables, OS-specific behavior.

## 5. Permanent Remediations
- **Prevention:** Add validation, improve types, or use safer abstractions.
- **Detection:** Add logging or metrics to catch similar issues earlier.
- **Testing:** Add a regression test that specifically triggers this scenario.
