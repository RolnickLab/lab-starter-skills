# Language-Specific Security Patterns

## Python
- Never on untrusted input: `eval`, `exec`, `pickle`, `yaml.load` (use `safe_load`), `torch.load` without `weights_only=True`.
- `subprocess` with argument lists, never `shell=True` with interpolated input.
- `tarfile`/`zipfile` extraction: path traversal; use `extractall(filter="data")` (3.12+) or validate member paths.
- `requests`/`httpx`: always set `timeout`; never `verify=False`.
- `secrets` for tokens, never `random`.
- `assert` is stripped under `-O`: never use it for security checks.

## JavaScript / TypeScript
- Never on untrusted input: `eval`, `new Function`, `child_process.exec` (use `execFile` with an argument array).
- Prototype pollution: reject `__proto__`/`constructor`/`prototype` keys when merging user objects; use `Map` or `Object.create(null)`.
- XSS: no `innerHTML` or `dangerouslySetInnerHTML` with user data; DOMPurify if unavoidable.
- Validate request bodies at the boundary (zod or equivalent).
