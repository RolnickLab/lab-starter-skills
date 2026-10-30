# Deep Modules and Testability

## Why This Matters for TDD
A **deep module** (small interface, large hidden implementation) is inherently easier to test. One public method means one test surface. Shallow modules force tests to orchestrate multi-step call sequences, coupling them to implementation details and violating the "test behavior, not mechanics" principle.

---

## Surface Area vs. Depth

```
Deep Module                     Shallow Module
┌────────────────────┐          ┌────────────────────┐
│  public interface  │          │ public interface   │
│  (small)           │          │ (large)            │
├────────────────────┤          ├────────────────────┤
│                    │          │                    │
│  implementation    │          │  implementation    │
│  complexity        │          │  (small)           │
│  (large)           │          │                    │
└────────────────────┘          └────────────────────┘
```

**Goal:** Maximize `complexity hidden / interface exposed`.

---

## Characteristics of a Deep Module

| Property | Description |
|---|---|
| Few public methods | Callers need to know as little as possible |
| Rich return types | One call returns everything needed; no chatty sequences |
| Encapsulated decisions | Implementation choices (caching, retry, batching) are invisible to callers |
| Stable interface | The public API changes rarely even as internals evolve |

---

## Examples

### Shallow (costly to test and use)
```python
class FileParser:
    def open(self, path: Path) -> None: ...
    def read_header(self) -> dict: ...
    def read_rows(self) -> list[dict]: ...
    def validate_row(self, row: dict) -> bool: ...
    def close(self) -> None: ...
```
Callers must know the correct call sequence and manage state. Every step is a test seam that exposes nothing worth testing independently.

### Deep (easy to test and use)
```python
class FileParser:
    def parse(self, path: Path) -> ParsedFile: ...
```
All sequencing, validation, and resource management is hidden. One call, one result, one test.

---

## Designing for Depth

1. **Identify the minimal result** the caller needs. Make that the return type.
2. **Push decisions inward.** If callers are choosing between variations of a method, merge those variations into one method with smarter defaults.
3. **Hide lifecycles.** Resource open/close, retry logic, and caching belong inside the module.
4. **Use context managers** to encapsulate setup/teardown rather than exposing it.

---

## TDD Signal
If writing a test for a module requires calling 3+ methods in a specific order, the module is too shallow. Refactor so a single method produces the observable outcome, then test that.
