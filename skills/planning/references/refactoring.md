# Refactoring After Green

## When to Refactor
Only refactor when all tests are green. A failing test means you are still in the Red or Green phase. Refactoring on red mixes two activities and makes failures harder to diagnose.

---

## Code Smells to Address

### Long Method
**Signal:** A method exceeds ~20 lines or requires a comment to explain each section.
**Fix:** Extract private methods named after the *intent* of each section, not the mechanics.

```python
# Before
def process_order(order):
    # validate
    if not order.items:
        raise ValueError(...)
    # calculate
    total = sum(i.price for i in order.items)
    tax = total * 0.2
    # persist
    db.save(Order(total=total + tax))

# After
def process_order(order):
    _validate(order)
    invoice = _calculate(order)
    _persist(invoice)
```

---

### Feature Envy
**Signal:** A method accesses data from another object more than its own.
**Fix:** Move the method closer to the data it uses.

```python
# Smell: Order knows too much about Item internals
def total(order):
    return sum(item.price * item.quantity * (1 - item.discount) for item in order.items)

# Fix: Item owns its own line total
class Item:
    def line_total(self) -> Decimal: ...
```

---

### Primitive Obsession
**Signal:** Using raw strings, ints, or dicts to represent domain concepts.
**Fix:** Introduce a value object or dataclass.

```python
# Smell
def apply_discount(price: float, discount: float) -> float: ...

# Fix: units are explicit, invalid values are impossible
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

@dataclass(frozen=True)
class DiscountPct:
    value: float  # validated 0–100
```

---

### Duplicated Logic
**Signal:** The same conditional or calculation appears in two or more places.
**Fix:** Extract to a single named function. Do not abstract until you see the pattern at least twice.

---

### Data Clump
**Signal:** The same group of parameters (e.g., `lat, lon, altitude`) always travels together.
**Fix:** Bundle them into a value object (`Coordinate`).

---

### God Class
**Signal:** A class has >7 public methods or touches >3 unrelated concerns.
**Fix:** Apply Single Responsibility: split into collaborators connected by DI.

---

## Refactoring Rules

1. **One smell, one commit.** Mix of mechanical refactors obscures history and makes bisect harder.
2. **Run tests after every extract.** If a rename breaks a test, the test was testing the name, not the behavior; fix the test.
3. **No behavior changes during refactor.** If you need to change behavior, add a test first, then make it green, then refactor.
4. **Stop when the tests still pass and the code is clearer.** Refactoring has diminishing returns; perfectionism is a code smell too.
