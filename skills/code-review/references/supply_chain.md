# Supply Chain & Dependencies

## New Dependencies
- Verify the package exists, is the intended one, and is maintained. Typosquatting (`lodas` vs `lodash`) and AI-hallucinated package names (slopsquatting) are active attack vectors.
- Flag libraries with no release in >2 years.

## Pinning & Integrity
- Lockfile committed: **mandatory** (`uv.lock`, `poetry.lock`, `package-lock.json`, `pnpm-lock.yaml`, `Cargo.lock`, `go.sum`).
- Hash-verified installs where supported (`uv sync --locked`, `pip install --require-hashes`, `npm ci`).
- Vendoring for high-security or air-gapped environments.

## Vulnerability Scanning
- `pip-audit`, `npm audit`, `cargo audit`, `govulncheck`, or Dependabot/Renovate/Snyk on every PR.

## CI/CD
- GitHub Actions pinned to full commit SHA, not tags (tags are mutable: tj-actions/changed-files compromise, 2025).
- Workflow `permissions:` least privilege, default `contents: read`.
- Never check out untrusted PR code in `pull_request_target` workflows.
- Cloud auth via OIDC federation, not long-lived secrets. Secrets masked in logs.
- `npm ci --ignore-scripts` when install scripts are not needed.
- SAST and SCA on every PR; fixed versions for runners and build tools.
