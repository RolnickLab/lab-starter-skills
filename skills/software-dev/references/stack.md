# Tech Stack & Anti-Patterns

## Recommended Stack
| Domain | Library | Rationale |
| :--- | :--- | :--- |
| **Web API** | `FastAPI` / `Litestar` | Async-native, auto-docs, Pydantic integration. |
| **CLI** | `Typer` | Type-hint driven, modern UX. |
| **Data Models** | `Pydantic V2` | Fast (Rust), strict, standard. |
| **Linting** | `Ruff` | Replaces flake8, isort, black, pyupgrade. 100x faster. |
| **Testing** | `pytest` | Powerful fixtures, ecosystem. |
| **Logs** | `structlog` | Structured JSON logging is required for observability. |

## Forbidden Patterns (Auto-Reject)
1.  **Mutable Defaults:** `def func(x=[])`.
    *   *Why:* The list is created *once* at definition time and shared across all calls.
    *   *Fix:* `def func(x=None): if x is None: x = []`.
2.  **Wildcard Imports:** `from module import *`.
    *   *Why:* Pollutes namespace, makes code unreadable, breaks static analysis.
3.  **Bare Except:** `except:`.
    *   *Why:* Catches `SystemExit` (sys.exit()) and `KeyboardInterrupt` (Ctrl+C). You can't stop the script.
    *   *Fix:* `except Exception:`.
4.  **Global State:** Using `global` variables.
    *   *Why:* Makes testing impossible (tests leak state into each other) and concurrency dangerous.
5.  **Print Debugging:** `print("here")`.
    *   *Why:* Not structural, goes to stdout, lost in production.
    *   *Fix:* Use `logger.debug()`.
