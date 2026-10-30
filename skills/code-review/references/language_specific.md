# Language-Specific Security Patterns

## Python
- Never on untrusted input: `eval`, `exec`, `pickle`, `yaml.load` (use `safe_load`), `torch.load` without `weights_only=True`.
- `subprocess` with argument lists, never `shell=True` with interpolated input.
- `tarfile` extraction: path traversal and link tricks; pass `filter="data"` (default since 3.14; check `hasattr(tarfile, "data_filter")` on older versions). `zipfile.extractall` has no `filter`: it strips `..` and absolute paths itself; cap total extracted size (zip bombs).
- `requests`/`httpx`: always set `timeout`; never `verify=False`.
- `secrets` for tokens, never `random`.
- `assert` is stripped under `-O`: never use it for security checks.

## JavaScript / TypeScript
- Never on untrusted input: `eval`, `new Function`, `child_process.exec` (use `execFile` with an argument array).
- Prototype pollution: reject `__proto__`/`constructor`/`prototype` keys when merging user objects; use `Map` or `Object.create(null)`.
- XSS: no `innerHTML` or `dangerouslySetInnerHTML` with user data; DOMPurify if unavoidable.
- Validate request bodies at the boundary (zod or equivalent).
