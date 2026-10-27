# Interface Design for Testability

## Two Primary Techniques

### 1. Dependency Injection
Pass collaborators (especially those with I/O) through the constructor or function signature rather than constructing them internally.

```python
# Hard to test: creates its own dependency
class ReportGenerator:
    def __init__(self):
        self._db = Database(url=settings.DATABASE_URL)  # can't substitute in tests

# Testable: dependency is injected
class ReportGenerator:
    def __init__(self, db: Database):
        self._db = db
```

**Patterns:**
- **Constructor injection**: for long-lived collaborators (default choice)
- **Parameter injection**: for per-call dependencies (functions, short-lived operations)
- **Factory injection**: when the collaborator must be created lazily per request

**Avoid service locators** (hidden `get_dependency()` calls inside methods); they make dependencies invisible to tests.

---

### 2. Pure Functions
A pure function has no side effects and returns the same output for the same input. It is trivially testable.

```python
# Pure: no I/O, no state mutation
def apply_discount(price: Decimal, discount_pct: Decimal) -> Decimal:
    return price * (1 - discount_pct / 100)

# Impure: reads from DB, has side effects
def apply_discount(order_id: int) -> None:
    order = db.query(Order).get(order_id)
    order.total *= 0.9
    db.commit()
```

**Strategy:** Push impure I/O to the edges. The center of your domain logic should be pure functions. Wire them together with a thin impure shell that handles I/O.

```
┌──────────────────────────────────────┐
│  Impure shell (controllers, handlers)│
│  ┌────────────────────────────────┐  │
│  │  Pure domain functions         │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

---

## Interface Design Checklist

- [ ] Can the class be instantiated in a test without starting a database or server?
- [ ] Do constructors accept interfaces/protocols rather than concrete implementations?
- [ ] Are time, randomness, and external services injectable?
- [ ] Is business logic in pure functions separate from I/O orchestration?
- [ ] Does the public interface expose outcomes, not steps?

---

## Protocol-Based Typing (Python)

Use `typing.Protocol` to define injectable interfaces without coupling to a base class:

```python
from typing import Protocol

class UserRepository(Protocol):
    def find_by_id(self, user_id: int) -> User | None: ...
    def save(self, user: User) -> None: ...

class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo
```

In tests, pass a simple fake that implements the protocol, no mocking framework required:

```python
class FakeUserRepository:
    def __init__(self):
        self._store: dict[int, User] = {}

    def find_by_id(self, user_id: int) -> User | None:
        return self._store.get(user_id)

    def save(self, user: User) -> None:
        self._store[user.id] = user
```
