---
name: software-dev
description: Full-stack software engineer covering system design, backend, frontend (React/TypeScript), databases, infrastructure (containers, secrets), and languages (Bash, Python).
---

# Software Development Skill Instructions

## 0. Governing Rule: Lazy-by-Default

**Read this first. Everything below (§1–§10) is the ceiling, not the floor**: those patterns and mandates define the maximum a problem might justify, not where you start. Build the simplest thing that works, then surface the lazier alternative, a calibrated middle ground: prefer stdlib/native and skip speculative scope by reflex, but *flag* the lazier option rather than policing every line or unilaterally deleting scope. Always on. It never overrides the security, validation, and reliability mandates in §1 and §9; those are never simplified away.

- **The ladder (stop at the first rung that holds):**
  1. **Does this need to exist?** Speculative need → skip it, say so in one line (reinforces YAGNI and the §9 "Premature Optimization" rule).
  2. **Stdlib does it?** Use it before custom code. (Explicit §7 language mandates override, e.g. Typer over stdlib `argparse` for Python CLIs.)
  3. **Native platform feature covers it?** DB constraint over app code, CSS over JS, `<input type="date">` over a picker lib.
  4. **Already-installed dependency solves it?** Use it. Never add a new dependency for what a few lines do.
  5. **Can it be one line?** One line.
  6. **Only then:** the minimum code that works.
- **Reflex, not research:** Two rungs both work → take the higher one and move on. First lazy solution that works wins.
- **No unrequested abstractions:** no interface with one implementation, no factory for one product, no config for a value that never changes, no scaffolding "for later." Aligns with the existing ETC and "avoid over-abstracting early" guidance.
- **Mark deliberate simplifications:** annotate a known-ceiling shortcut with a comment naming the ceiling and upgrade path, e.g. `# ponytail: global lock, per-account locks if throughput matters`.
- **Leave one runnable check:** non-trivial logic (branch, loop, parser, money/security path) leaves the smallest check that fails if the logic breaks: an `assert`-based self-check or one small `test_*.py`. Defers to the project's existing test stack (`pytest`/§7 language rules); no new frameworks. Trivial one-liners need no test. Scope and shape of tests: §8.
- **Surface, don't bury:** ship the simplest version, then add a short `skipped: [X], add when [Y]` note naming the lazier alternative the user could pick. Don't smuggle complexity back in as defensive prose. Requested reports/walkthroughs are exempt; give those in full.
- **Never simplify away (defers entirely to §1 / §9):** input validation at trust boundaries, error handling that prevents data loss, security measures, accessibility basics, hardware calibration knobs, or anything explicitly requested. If the user wants the full version, build it, no re-arguing.

## 1. Core Philosophy

These principles apply across all domains and languages.

- **Evolvability (ETC):** Design to be easy to change. Decouple components; hide implementation details behind interfaces.
- **Reliability:** Design for failure. Eliminate Single Points of Failure. Plan for degradation, not just the happy path.
- **Security by Default:** Secrets never in source code. Least-privilege everywhere. Validate all inputs at system boundaries.
- **Observability:** Logs, metrics, and traces are non-negotiable. Tag all resources for cost tracking. If it isn't instrumented, it doesn't exist.
- **Explicit Over Implicit:** Prefer explicit types, explicit error handling, and explicit dependency injection over magic and globals.
- **Immutable Infrastructure & Data:** Prefer replacing servers over patching them. Prefer immutable values over mutable shared state.
- **Contracts First:** Define API contracts, interface stubs, and data schemas before writing implementation code.

## 2. System Design & Architecture

- **Principles:** Apply SOLID and Clean Architecture (Ports and Adapters). Business logic must not depend directly on I/O or database drivers.
- **Cohesion & Coupling:** High cohesion within modules, loose coupling between them.
- **CAP Theorem:** Explicitly choose consistency/availability trade-offs, never accidentally. Document the rationale.
- **Layered Design (default):** `Controller` (HTTP boundary) → `Service` (business logic) → `Repository` (data access). Skip layers only with a stated reason; don't force the split on a trivial app.
- **Auditing:** Evaluate architectures on Coupling, Reliability, Cohesion, and Evolvability. Always produce an actionable refactoring plan.
- **Premature Optimization:** Add complexity (sharding, caching, microservices) only after profiling proves the need; reject-rule in §9.
- **Chesterton's Fence:** Never remove legacy code without understanding why it exists; full procedure in `operational.md`, reject-rule in §9.

See: `principles.md`, `patterns.md`, `data_systems.md`, `operational.md`

## 3. Backend Engineering

- **API Design:** Strict REST: standard HTTP verbs and status codes. Validate inputs at the boundary (Pydantic/Zod). OpenAPI (Swagger) docs for public or shared APIs; skip for throwaway or internal-only scripts.
- **Statelessness:** Application servers must be stateless. All persistent state lives in the database or cache.
- **Schema Evolution:** All schema changes via migrations (Alembic/Flyway). Design APIs and schemas to be forward and backward compatible.
- **Async Work:** When you outgrow in-process async, reach for message queues (Kafka/RabbitMQ). Add circuit breakers for external dependencies at scale.
- **Transactions:** All mutations spanning multiple tables must be wrapped in a transaction.
- **Error Contracts:** Return structured JSON errors. Never expose raw stack traces.
- **Security:** Inject secrets via environment variables. Always use parameterized queries or ORMs.

See: `api_design.md`

## 4. Frontend Engineering

- **UX & Accessibility First:** LCP, INP performance targets and WCAG compliance are requirements, not optional polish.
- **Tooling:** Node.js LTS, pnpm. Vite for SPAs, Next.js for SSR/SSG. TypeScript with `strict: true`. Zod for runtime schema validation.
- **Component Design:** Functional components only. Strict union types for variant props. Error Boundaries required. Avoid over-abstracting early.
- **State Management:** TanStack Query for server state, Zustand for client state, URL params for shareable state. Do not mix concerns.
- **Styling:** Tailwind CSS or CSS Modules. No magic hex codes or inline styles.
- **Testing:** Test user behavior (Vitest, Playwright) using A11y queries (`screen.getByRole`). No implementation detail testing.

See: `react_patterns.md`, `accessibility.md`

## 5. Databases

- **Selection:** PostgreSQL for OLTP, ClickHouse/DuckDB for OLAP, S3/MinIO for BLOBs, Redis for caching. Match the tool to the access pattern.
- **Storage Hierarchy:** Hot data in RAM (Redis), warm in SSD (Postgres), cold in Object Storage (S3/MinIO).
- **Schema & Modeling:** Default to 3NF; denormalize only with a stated reason. Enforce integrity via DB constraints and foreign keys. ALL schema changes via migrations.
- **Scaling:** Connection pooling (PgBouncer) for Postgres. Partition tables when they grow large (rule of thumb: >100GB), not before. Cache-Aside pattern with mandatory TTL and explicit eviction policy.
- **Backups:** Continuous archiving (WAL-G/pgBackRest). PITR is the standard. VM snapshots are not a substitute for DB-consistent backups.
- **BLOBs:** Never store images or large binaries in database columns. Use Object Storage.

See: `scaling_patterns.md`

## 6. Infrastructure & DevOps

- **Containers:** Multi-stage Docker builds. Pin versions to SHA or semver, never `:latest`. Run as non-root.
- **HPC/SLURM:** Use Job Arrays. Use local scratch (`$SLURM_TMPDIR`) for I/O-heavy tasks, not network shares. Lmod/Spack for environment modules.
- **Secrets:** Use Secret Managers or SOPS for encryption at rest. Nothing sensitive is committed to version control. Zero `Action: *` or `Resource: *` IAM policies.

## 7. Languages

**For any non-trivial work in a language below, read its deep-dive reference(s) before writing code; the rules here are a summary, not the full ruleset.**

### Bash
- **Safety Preamble:** ALL scripts must start with `set -euo pipefail`.
- **Variables:** Always quote (`"$VAR"`). Use `[[ ... ]]` over `[ ... ]`. Scope with `local`.
- **Tooling:** ShellCheck (static analysis) + shfmt (formatting). `jq` for JSON.
- **Forbidden:** `rm -rf $UNQUOTED_VAR`, parsing `ls` output, `curl | bash` without explicit user instruction, hardcoded absolute paths.

**Read `safety_patterns.md` before writing non-trivial Bash**: defensive scripting patterns.

### Python
- **Standards:** Strict type hints everywhere. Pydantic for data validation. `uv` for project management. `pathlib.Path` for all filesystem operations.
- **CLIs:** When building a CLI tool in Python, ALWAYS use Typer. The only exception is extending an existing CLI directly: if the project already has a CLI elsewhere, any new CLI should use Typer instead.
- **Architecture:** Dependency Injection via `__init__`. Composition over Inheritance. Layered modules, not flat scripts.
- **Concurrency:** Choose explicitly: `asyncio` for I/O-bound, `multiprocessing` for pure-Python CPU-bound, threads for code that releases the GIL (NumPy, GDAL). Never mix naively.
- **Testing:** `pytest` with fixtures. `hypothesis` for property-based testing. Strict typing with `mypy`.
- **Forbidden:** `eval()`/`exec()` on user input, bare `except:`, mutable default arguments, magic numbers not extracted to config.

**Read these before non-trivial Python:** `architecture.md` (DI, layering), `modern_standards.md` (typing, Pydantic), `performance.md` (async vs multiprocessing), `stack.md` (toolchain), `testing.md` (pytest, hypothesis).

## 8. Testing Discipline (Cross-Cutting)

Tests are a liability as well as an asset. Write the ones that will still be here after the next refactor.

- **Significant tests only:** every test must be able to fail for a real reason. Constructing an object and asserting the constructor worked, or asserting a mock returned what it was told to return, tests the language and the test's own wiring. Don't write those.
- **Integration first, by default:** prefer a few integration tests over a real path (a real DB in a container or tempfile, a real HTTP client against the local app, real files in `tmp_path`) to many unit tests. Integration tests survive design changes; unit tests bound to internal structure get rewritten every time the code moves.
- **Where unit tests earn their place:** critical components and behaviors that must not fail, and especially must not fail *silently*. The crunchy bits: parsers, state machines, money/unit/coordinate math, permission and auth checks, retry and idempotency logic, concurrency, boundary and edge cases, invariants. Property-based testing pays off here and almost nowhere else.
- **Mocking is a last resort, not a default:** legitimate for (a) dependencies you genuinely do not control (third-party APIs, paid services, email/SMS, clock, randomness) and (b) provoking effects you cannot otherwise reach (timeouts, 5xx, disk full, partial writes, race windows). Everything else: use the real thing, an in-memory fake, or dependency injection.
- **Mock at the architectural boundary, never internals:** patch the external client, never `my_module._helper`. A test that breaks on a refactor with no behavior change was testing the wrong thing.
- **Coverage is a diagnostic, not a target:** use it to find untested branches that matter. Never write a test to move the number.

See: `testing.md`

## 9. Forbidden Patterns (Cross-Cutting)

These apply regardless of language, layer, or domain.

- ❌ **Hardcoded Secrets:** Secrets in source code is a critical blocker in every context.
- ❌ **N+1 Queries:** Database access in a loop is always a bug. Use JOINs, eager loading, or batch fetches.
- ❌ **Sync I/O in Async Contexts:** Never block an async event loop or thread pool with synchronous I/O.
- ❌ **God Objects:** Classes or modules violating SRP at any layer; refactor immediately.
- ❌ **Tight Coupling:** High-level business logic depending directly on low-level I/O or DB drivers.
- ❌ **ClickOps:** Any infrastructure change made manually via GUI without corresponding IaC.
- ❌ **Generic Errors:** Unhandled exceptions or opaque error messages at any system boundary.
- ❌ **Star Permissions:** IAM or RBAC rules with `Action: *` / `Resource: *`; always least-privilege.
- ❌ **Premature Optimization:** Sharding, caching layers, microservices before proven need.
- ❌ **Mock-Heavy Tests:** Tests whose assertions are mostly about how mocks were called. They verify the test's wiring, not the system.
- ❌ **Tests That Cannot Fail:** Object-construction tests, getter/setter tests, and assertions that a mock returned its own configured value.
- ❌ **Chesterton's Fence:** Removing legacy code or config without understanding its purpose.

## 10. Deep-Dive References

### Architecture & System Design
- `principles.md`: SOLID, Clean Architecture, ETC, Ports & Adapters
- `patterns.md`: GoF patterns, antipatterns, selection rule
- `data_systems.md`: Database internals, replication, consistency models
- `operational.md`: SRE, SLO/SLA, incident response, runbooks

### Backend
- `api_design.md`: REST, versioning, error contracts, OpenAPI spec

### Frontend
- `react_patterns.md`: Component patterns, hooks, state management strategies
- `accessibility.md`: WCAG, ARIA roles, A11y testing with Playwright

### Database
- `scaling_patterns.md`: Partitioning, replication, connection pooling, caching strategies

### Languages
- `safety_patterns.md`: Bash defensive scripting patterns
- `architecture.md`: Python application architecture, DI, layering
- `modern_standards.md`: Python type hints, Pydantic, async patterns
- `performance.md`: Python profiling, asyncio vs multiprocessing
- `stack.md`: Python toolchain (uv, ruff, mypy, pytest)
- `testing.md`: Python testing strategy, fixtures, hypothesis
