# Testing & Quality

Cross-cutting testing policy lives in `SKILL.md` §8. This file is the Python mechanics.

## What Is Worth Testing

*   **Decision rule:** write the test only if you can name the bug it would catch. If the answer is "none, it just checks the object exists", skip it.
*   **High value:** parsers and serializers, state machines, money/unit/coordinate math, permission and auth checks, retry/idempotency, concurrency, boundary conditions, and anything whose failure would be *silent* (wrong number, dropped record, stale cache).
*   **Low value (don't write):** constructing a Pydantic model and asserting the fields round-trip, getters/setters, thin delegating wrappers, framework behavior, and anything that restates the type signature.
*   **Shape:** a handful of integration tests over a real path beats a wall of unit tests bound to internal structure. Integration tests survive refactors; structural unit tests get rewritten every time the design moves.

## Integration Tests in Python

*   **Filesystem:** `tmp_path` / `tmp_path_factory` fixtures with real files. Never mock `pathlib`.
*   **Database:** `testcontainers` for a real Postgres, or SQLite for schema-agnostic logic. Wrap each test in a transaction that rolls back (`scope="function"` yield fixture).
*   **HTTP APIs:** drive the app in-process (`httpx.ASGITransport`, FastAPI `TestClient`). Real routing, real validation, real serialization, no server.
*   **Outbound HTTP:** `respx` or `responses` to stub the wire, not the client class. Tests the request you actually build.

## Framework
*   **Pytest:** The industry standard.
    *   Use `conftest.py` for shared fixtures.
    *   Use `pytest.mark.parametrize` to test multiple scenarios with one test function.

## Fixtures
*   **Philosophy:** Fixtures set up the "World" for the test.
*   **Scope:** Use `scope="session"` for expensive resources (like Docker containers), `scope="function"` for isolation (like DB transactions).
*   **Yield Fixtures:** Use `yield` to provide setup and teardown code in one block.
    ```python
    @pytest.fixture
    def db_session():
        session = create_session()
        yield session
        session.rollback()  # Clean up after test
    ```

## Property-Based Testing
*   **Hypothesis:** Don't just test examples (`add(2, 2) == 4`). Test properties (`add(a, b) == add(b, a)`).
*   **Use Case:** Finding edge cases (empty strings, huge integers, weird unicode) that you forgot to handle.
*   **Where it pays:** round-trip properties (`parse(render(x)) == x`), invariants, and commutativity in the crunchy logic above. Not worth it on CRUD.

## Mocking

Mocking is a last resort, not the default. It couples the test to a call graph, and a suite of mocks mostly asserts that the test was wired the way the test was wired.

*   **Justified for:** dependencies you do not control (third-party APIs, paid services, email/SMS), non-determinism (`time`, `random`, `uuid`), and provoking effects you cannot otherwise reach (timeouts, 5xx, disk full, partial writes).
*   **Not justified for:** your own modules, the filesystem (`tmp_path`), the database (a real one in a container), or anything a small fake or DI would cover.
*   **Preference order:** real dependency → in-memory fake / stub injected via `__init__` → stub at the wire (`respx`) → `unittest.mock`.
*   **Rule:** Mock at the **architectural boundary** (the public method of an external API client), never internal implementation details.
*   **Avoid:** `patch('my_module.internal_helper')`. Refactor the helper, break the test, learn nothing.
*   **Prefer:** dependency injection with a fake, or `patch('my_module.ExternalClient')`.
*   **Smell:** the test body has more `assert_called_once_with` than assertions about return values or observable state. Rewrite it as an integration test or delete it.

## Coverage

Coverage is a diagnostic, not a target. Use it to find untested branches that would hurt if they broke. Never write a test to move the percentage; a mock-padded suite at 95% catches less than a focused one at 60%.
