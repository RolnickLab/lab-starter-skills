# OWASP Top 10 (2025)

Review checks per category. Source: https://owasp.org/Top10/2025/

## A01 Broken Access Control (incl. SSRF)
- Ownership/permission check on every request touching a resource (IDOR: `GET /account?id=123` returning another user's data). Deny by default.
- Authorization enforced server-side, never only in the UI.
- SSRF: server-side fetches of user-supplied URLs need an allowlist; block internal ranges and cloud metadata (`169.254.169.254`); re-validate after redirects.
- CORS: no `*` with credentials, no reflecting arbitrary `Origin`.

## A02 Security Misconfiguration
- `DEBUG`, verbose errors and stack traces off in production. No default accounts or credentials.
- XML parsers: disable DTDs and external entities (XXE). Prefer JSON.
- Security headers set: CSP, HSTS, `X-Content-Type-Options`.

## A03 Software Supply Chain Failures
See `supply_chain.md`.

## A04 Cryptographic Failures
- TLS 1.2+ in transit, HSTS. Sensitive columns encrypted at rest, keys in a KMS.
- Passwords: Argon2id, scrypt or bcrypt. Never MD5, SHA1, or unsalted fast hashes.
- Symmetric encryption: AES-GCM or ChaCha20-Poly1305. Never ECB, never hand-rolled crypto.
- Tokens and nonces from a CSPRNG (`secrets`, `crypto/rand`), never `random`/`Math.random`.
- No secrets in code, config or logs; use a secret manager (Vault, AWS Secrets Manager) or env vars.

## A05 Injection (SQL, NoSQL, OS, XSS, template)
- SQL/NoSQL: parameterized queries or ORM. Never string concatenation or f-strings.
- OS commands: argument lists, no shell (`shell=True`, `os.system`, `child_process.exec`).
- XSS: context-aware output encoding, auto-escaping templates, CSP. No `innerHTML`, `dangerouslySetInnerHTML` or `|safe` with user data.
- LLM features: treat untrusted input in prompts and model output as hostile (prompt injection); never pass model output to a shell, SQL or `eval`.

## A06 Insecure Design
- Rate limits on login, signup, password reset and expensive endpoints.
- Business-logic abuse: negative quantities, replayed requests, skipped workflow steps. Idempotency keys on payments.

## A07 Authentication Failures
- MFA for sensitive actions, preferably phishing-resistant (WebAuthn/passkeys). Rate limiting against credential stuffing.
- Session cookies `HttpOnly`, `Secure`, `SameSite`. Rotate session ID on login, invalidate on logout.
- Protocol specifics: `auth_protocols.md`.

## A08 Software or Data Integrity Failures
- No deserialization of untrusted data: `pickle`, `torch.load` without `weights_only=True`, `yaml.load`, Java native serialization. Use JSON or `safetensors`.
- Verify signatures/checksums on updates, build artifacts and downloaded models.

## A09 Security Logging and Monitoring Failures
- Log auth events, access-control failures and validation failures with enough context to investigate.
- Mask PII, card numbers, tokens and auth headers in logs.
- Logs centralized, with alerting on anomalies.

## A10 Mishandling of Exceptional Conditions
- Fail closed: an exception inside an auth or permission check must deny.
- No swallowed exceptions; no partial state after errors (transactions, rollback).
- Error responses never leak internals (stack traces, SQL, file paths).
- Resource limits: timeouts on outbound calls, upload size caps, pagination, ReDoS-safe regexes.
