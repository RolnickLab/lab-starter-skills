# Performance & Concurrency

## Concurrency Models
*   **I/O Bound (Waiting for Network/Disk):**
    *   **Solution:** `asyncio` (coroutines).
    *   **Libraries:** `FastAPI`, `httpx`, `asyncpg`.
    *   **Why:** A single thread can handle thousands of waiting connections.
*   **CPU Bound (Number Crunching):**
    *   **Solution:** `multiprocessing` or `ProcessPoolExecutor`.
    *   **Why:** The Global Interpreter Lock (GIL) prevents threads from running Python bytecode in parallel on one core. You must spawn new processes.
    *   **Warning:** Process overhead is high. Only use for tasks taking > 100ms.

## Profiling (Stop Guessing)
*   **CPU:** Use **py-spy**. It is a sampling profiler that runs safely in production with low overhead.
    *   `py-spy record -o profile.svg --pid 12345`
*   **Memory:** Use **memray**. It tracks every allocation and can show you who is holding onto memory.
    *   `memray run my_script.py`

## Optimization Hierarchy
1.  **Algorithmic:** O(N^2) to O(N) beats any C-extension.
2.  **I/O:** Batch database queries, use async for API calls.
3.  **Interpreter:** Use `numpy` / `pandas` / `polars` to push loops to C/Rust.
4.  **Compiler:** Use `numba` or `cython` as a last resort.
