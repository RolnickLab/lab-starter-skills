# Reviewing Tests

## Flag
- Tests asserting on mocks rather than behavior (checking a mock returns what the test configured it to return).
- Mocking internals (own classes, private functions). Mock only at system boundaries: network, third-party services, clock, randomness. Prefer a real DB via Testcontainers over a mocked one.
- New logic with no test; bug fix without a regression test that fails before the fix.
- Missing edge cases: empty, None/null, boundaries, unicode, large inputs, error paths.
- Flakiness sources: `sleep`, wall-clock time, unseeded randomness, test-order dependence, shared global state, real network.
- Tests that execute code without meaningful assertions (coverage padding).
- One test covering several unrelated behaviors; names that do not state the expected behavior.

## Expectations
- Integration tests over a real path (real DB, real files, in-process HTTP) by default; unit tests for crunchy logic (parsers, money/unit math, auth, concurrency, edge cases); few E2E tests (Playwright) on critical user flows.
- Property-based tests (Hypothesis, fast-check, proptest) for parsers, serializers and invariants (round-trip, idempotence).
- Coverage is a diagnostic for untested branches that matter, never a target.
- Flaky tests are worse than none: quarantine and fix, never retry-until-green.
- CI: lint and unit tests on every push, E2E on merge or nightly, red blocks merge.
- Pre-commit includes secret detection (`gitleaks` or `detect-secrets`).
