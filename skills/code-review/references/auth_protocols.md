# Auth Protocols Review Checklist

## OAuth 2.0
- Authorization Code + PKCE for all clients, confidential ones included (RFC 9700).
- Implicit and Resource Owner Password Credentials flows: deprecated, reject.
- Client Credentials only for machine-to-machine.
- Exact-match `redirect_uri` validation, no wildcards. `state` or PKCE against CSRF.
- Least-privilege scopes (`read:profile`, not `admin:all`).

## OIDC
- ID token is for authentication only; never send it to APIs as an access token.
- Validate `nonce`, `iss`, `aud`, `exp`.

## JWT
- Validate signature, `exp`, `nbf`, `iss`, `aud` on every request.
- Pin accepted algorithms server-side; reject `alg: none` and algorithm confusion (HS256 with an RSA public key).
- Payload is only base64: no secrets or sensitive PII in it.
- Short-lived access tokens; refresh tokens rotated and revocable. Stateless tokens cannot be revoked without short expiry or a denylist.
- Signing keys rotated via JWKS with `kid`.
- Browser storage: `HttpOnly`, `Secure`, `SameSite` cookie plus CSRF protection. Not `localStorage` (readable by XSS).

## SAML
- Validate the signature on the assertion itself; guard against XML signature wrapping.
- Disable DTDs and external entities in the parser (XXE).
- Check `Audience`, `NotOnOrAfter`, `InResponseTo`; reject replayed assertions.

## General
- Passwords never stored in plaintext: Argon2id or bcrypt.
- API and signing keys scoped and rotatable. CI uses OIDC federation, not long-lived keys.
