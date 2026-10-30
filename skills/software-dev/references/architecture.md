# Architecture & Design Patterns

## SOLID Principles
Canonical SOLID + Clean Architecture definitions live in `principles.md`. Python specifics:
*   **Interface Segregation:** prefer small `typing.Protocol` interfaces over monolithic ABCs.
*   **Open/Closed:** use Strategy/plugin objects instead of giant `if/else` blocks.

## Composition over Inheritance
*   **The Trap:** Deep inheritance hierarchies are brittle and hard to test.
*   **The Fix:** Use Composition. Inject behavior classes into the main class.
    *   *Instead of:* `class SpecializedService(BaseService): ...`
    *   *Use:* `class Service: def __init__(self, handler: HandlerProtocol): ...`

## Dependency Injection (DI)
*   **Rule:** Never instantiate heavy dependencies (DB clients, HTTP sessions) inside a class or function.
*   **Mechanism:** Pass them in via `__init__` or function arguments.
*   **Benefit:** Makes testing trivial. You can pass a `MockDatabase` without patching.

## Functional Core, Imperative Shell
*   **Pattern:** Push side-effects (I/O) to the edges of the program (the "Shell"). Keep the business logic pure (the "Core").
*   **Testing:** The Core can be tested with unit tests (fast, deterministic). The Shell requires integration tests.
