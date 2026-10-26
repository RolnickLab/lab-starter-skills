# Good vs. Bad Tests

## The Core Question
A test is valuable if it catches real regressions and costs little to maintain. A test is brittle if it breaks when you refactor internals without changing behavior.

---

## Brittle Test Patterns (Bad)

### Testing Implementation Details
```python
# BAD: breaks if you rename the private method
def test_calculates_discount():
    order = Order(items=[item(price=100)])
    order._apply_percentage_discount(0.1)
    assert order._discount_amount == 10
```

### Overspecified Mocks
```python
# BAD: asserts call order and argument details unrelated to the outcome
mock_repo.save.assert_called_once_with(order, flush=True, commit=True)
```

### Testing the Framework
```python
# BAD: tests SQLAlchemy's behavior, not yours
def test_model_has_id_column():
    assert hasattr(User, "id")
```

### Redundant Coverage Without Scenario Value
```python
# BAD: duplicate of another test, adds zero new behavior signal
def test_add_2():
    assert add(2, 3) == 5
def test_add_3():
    assert add(2, 3) == 5
```

---

## High-Signal Behavior Tests (Good)

### Test Observable Outcomes
```python
# GOOD: behavior is verified through the public result
def test_discount_reduces_order_total():
    order = Order(items=[item(price=100)], discount_pct=10)
    assert order.total() == 90
```

### Test at the Right Granularity
| Scope | When to use |
|---|---|
| Integration (module boundary) | Default starting point for a new feature |
| Unit | Isolated pure functions, complex algorithms, edge cases |
| End-to-end | Critical user journeys, smoke tests only |

### Behavior-per-Test Structure
Each test should answer: *"Given [context], when [action], then [outcome]."*

```python
def test_checkout_applies_loyalty_discount_for_returning_customers():
    # Given
    customer = Customer(purchases=5)
    cart = Cart(items=[item(price=200)])
    # When
    invoice = checkout(customer, cart)
    # Then
    assert invoice.total < 200
```

---

## Smell Checklist
- [ ] Does the test break when you rename a private method? → Brittle
- [ ] Does the test pass even when the behavior is wrong? → Weak assertion
- [ ] Does the test require understanding internals to interpret a failure? → Too coupled
- [ ] Does the test name describe a business rule? → Good signal
- [ ] Would deleting this test let a real bug through? → Worth keeping
