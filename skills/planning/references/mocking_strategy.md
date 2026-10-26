# Mocking Strategy

## The Rule
Mock only at **system boundaries**, the edges where your code hands control to infrastructure you do not own.

---

## Boundary Classification

| Boundary Type | Examples | Mock? |
|---|---|---|
| External HTTP / RPC | `httpx`, `requests`, gRPC stubs | Yes |
| Database / persistence | SQLAlchemy sessions, Redis clients | Yes, use a test DB or in-memory variant |
| Filesystem | File reads/writes crossing a module boundary | Yes, use `tmp_path` fixture |
| Time / randomness | `datetime.now()`, `uuid4()`, `secrets` | Yes, inject or patch at call site |
| Internal collaborators | Your own `OrderService`, `PriceCalculator` | **No** |
| Pure functions | Any function with no I/O | **No** |

---

## How to Mock at Boundaries

### Inject dependencies (prefer this)
```python
# Production
class NotificationService:
    def __init__(self, http_client: httpx.AsyncClient):
        self._client = http_client

# Test
async def test_sends_email_on_signup(respx_mock):
    respx_mock.post("https://email.api/send").mock(return_value=Response(200))
    client = httpx.AsyncClient()
    svc = NotificationService(http_client=client)
    await svc.notify_signup(email="a@b.com")
    assert respx_mock.calls.call_count == 1
```

### Patch at the call site (use sparingly)
```python
# Only when DI is not feasible (e.g., patching stdlib)
def test_invoice_uses_current_date(freezegun_freeze):
    with freeze_time("2024-01-15"):
        invoice = Invoice.create(order)
    assert invoice.issued_on == date(2024, 1, 15)
```

---

## Anti-Patterns

### Mocking internals (hides real failures)
```python
# BAD: if PriceCalculator has a bug, this test never catches it
with patch("myapp.orders.PriceCalculator.calculate") as mock_calc:
    mock_calc.return_value = Decimal("99.00")
    result = checkout(cart)
```

### Over-specified call assertions
```python
# BAD: couples the test to how the boundary is called, not what it produces
mock_db.session.add.assert_called_once_with(order)
mock_db.session.commit.assert_called_once()
# GOOD: assert on the persisted state instead
saved = db.query(Order).filter_by(id=order.id).one()
assert saved.status == "confirmed"
```

### Pyramid inversion (too many mocks, not enough real code)
A high mock-to-assertion ratio (>2:1) signals the system under test is too coupled to infrastructure. Refactor to push I/O to the boundary.

---

## Decision Tree
```
Does the code call something outside this codebase?
├── Yes → Mock at that boundary
└── No → Is it stateful infrastructure (DB, cache)?
    ├── Yes → Use a real test instance or in-memory variant
    └── No → Don't mock; use the real collaborator
```
