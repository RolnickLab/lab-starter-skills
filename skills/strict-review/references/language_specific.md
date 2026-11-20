# Language-Specific Security Patterns

## Python
- Never on untrusted input: `eval`, `exec`, `pickle`, `yaml.load` (use `safe_load`).
- ML artifacts are code: `torch.load(..., weights_only=False)` (default `True` since PyTorch 2.6; pass it explicitly on older versions), `joblib.load`, `pd.read_pickle`, `np.load(allow_pickle=True)`, `cloudpickle`/`dill` all run code from the file. Prefer `safetensors`.
- Hugging Face `trust_remote_code=True` runs the repo's Python: vetted repos only, pinned with `revision=<commit hash>`.
- `subprocess` with argument lists, never `shell=True` with interpolated input.
- Paths: `Path(base) / user_input` returns `user_input` when it is absolute. Resolve, then check `is_relative_to(base)`.
- `tarfile` extraction: path traversal and link tricks; pass `filter="data"` (default since 3.14; check `hasattr(tarfile, "data_filter")` on older versions). `zipfile.extractall` has no `filter`: it strips `..` and absolute paths itself; cap total extracted size (zip bombs).
- Untrusted XML: `defusedxml`, not the `xml.etree`/`lxml` defaults.
- Jinja2 `Environment()` has autoescape off: set `autoescape=select_autoescape()` for HTML.
- `requests`/`httpx`: always set `timeout`; never `verify=False`.
- `secrets` for tokens, never `random`.
- `assert` is stripped under `-O`: never use it for security checks.

## JavaScript / TypeScript
- Never on untrusted input: `eval`, `new Function`, `child_process.exec` (use `execFile` with an argument array).
- Prototype pollution: reject `__proto__`/`constructor`/`prototype` keys when merging user objects; use `Map` or `Object.create(null)`.
- XSS: no `innerHTML` or `dangerouslySetInnerHTML` with user data; DOMPurify if unavoidable.
- Validate request bodies at the boundary (zod or equivalent).

## Go
- `unsafe` package only when profiling proves the need.
- Every goroutine has a stop path (`context.Context`): leaks exhaust resources (DoS).
- Never discard errors from crypto or auth calls.

## Rust
- `unsafe` only with a `// SAFETY:` comment stating the invariant it relies on; check lengths and lifetimes at FFI boundaries.
- `unwrap`, `expect` and slice indexing on untrusted input panic (DoS); `as` casts truncate silently. Use `get`, `?`, `try_from`.
- Integer overflow wraps silently in release builds: `checked_*` or `saturating_*` for sizes and lengths from input.
- `Command::new("sh").arg("-c")` with interpolated input is injection: pass each argument with `.arg()`.
- Deserializing untrusted input (serde, bincode): cap size and nesting depth.

## Java
- Never `ObjectInputStream` on untrusted data. Jackson: no default typing (`activateDefaultTyping`, `@JsonTypeInfo(use = Id.CLASS)`) on untrusted JSON.
- `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory` process DTDs by default: set `disallow-doctype-decl` (XXE).
- JDBC/JPA: `PreparedStatement` or bound parameters; never concatenate into `createQuery`/`createNativeQuery`.
- `ProcessBuilder` with an argument list, never `Runtime.exec(String)` with input.
- `SecureRandom` for tokens, never `java.util.Random`.
- Log4j 2 below 2.17.1: Log4Shell, upgrade.
- Spring: no actuator `management.endpoints.web.exposure.include=*` in production; CSRF disabled only for stateless token APIs.

## Bash
- Quote every expansion (`"$var"`): unquoted variables split and glob.
- Never `eval`, `bash -c "$input"` or `source` on untrusted content; never `curl | bash`.
- `rm -rf "${dir:?}/"`: an empty variable must abort, not delete `/`.
- Temp files via `mktemp`, never fixed `/tmp` names.
- Secrets never as command-line arguments (visible in `ps`) or under `set -x` (echoed to logs).

## C / C++
- C++: `std::string` and `std::vector` over raw arrays.
- Never `gets`, `strcpy`, `strcat`, `sprintf`: use `snprintf` with the buffer size. `strncpy` leaves the string unterminated on truncation.
- Run AddressSanitizer (and MemorySanitizer under clang) in development and CI.
