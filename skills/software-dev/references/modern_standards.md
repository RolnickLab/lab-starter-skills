# Modern Python Standards

## Type System & Validation
*   **Strict Typing:** Code must pass `mypy --strict`.
    *   No `Any` allowed in production logic. If dynamic types are needed, use `typing.Protocol` or `object` with explicit casting.
    *   Use `typing.Annotated` for metadata-rich types (e.g., `x: Annotated[int, Gt(0)]`).
    *   **Typing Style:** Prefer `X | Y` (Python 3.10+) over `Union[X, Y]`.
*   **Pydantic V2:** Use for **all** data boundaries.
    *   **Input:** API request bodies, CLI arguments.
    *   **Config:** Loading environment variables (`pydantic-settings`).
    *   **Output:** Serialization for API responses.
    *   *Why?* It guarantees that if the object exists, the data is valid.

## Filesystem Handling
*   **Pathlib Only:** `os.path` and string concatenation for paths are **forbidden**.
    *   *Bad:* `os.path.join(data_dir, "file.txt")`
    *   *Good:* `Path(data_dir) / "file.txt"`
*   **Atomic Writes:** Never write directly to the final file path if the process might fail.
    *   *Pattern:* Write to `file.tmp`, then `path.replace(file)`. This ensures partial files never corrupt the system.

## Project Management
*   **Tooling:**
    *   **Primary:** `uv` (Fastest, unified pip/venv/build).
    *   **Secondary:** `poetry` (Reliable dependency resolution).
*   **Configuration:** All tool config (`ruff`, `mypy`, `pytest`) belongs in `pyproject.toml`.
