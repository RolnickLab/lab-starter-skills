# Core Architectural Principles

## SOLID Principles
*   **S (Single Responsibility):** A class/module should have one reason to change.
*   **O (Open/Closed):** Software entities should be open for extension but closed for modification.
*   **L (Liskov Substitution):** Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.
*   **I (Interface Segregation):** No client should be forced to depend on methods it does not use.
*   **D (Dependency Inversion):** Depend on abstractions, not concretions. High-level modules should not depend on low-level modules.

## Clean Architecture / Hexagonal
*   **Dependency Rule:** Dependencies must point **inward** toward the Domain Logic.
*   **Entities:** Core business logic/rules.
*   **Use Cases:** Application-specific business rules.
*   **Interface Adapters:** Conversion of data between external formats (DB, Web) and the Domain.
*   **Infrastructure (Frameworks & Drivers):** External tools like DBs, UI, and external APIs.

## The Pragmatic Philosophy (PragProg)
*   **ETC (Easier to Change):** The ultimate metric for design quality.
*   **Orthogonality:** Minimize side-effects between unrelated components.
*   **Tracer Bullets:** Build thin, end-to-end skeletons early to validate architecture.
*   **Broken Windows:** No unmarked hacks. A deliberate shortcut carries a comment naming its ceiling and upgrade path (`SKILL.md` §0).
