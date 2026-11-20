# Infrastructure & Cloud Review Checks

## Docker
- Non-root `USER` in the final stage. Multi-stage build: compilers and build-only files stay out of the final image.
- Base images pinned to a version, ideally a digest; never `:latest`. Minimal bases (distroless, `-slim`); Alpine's musl breaks many Python wheels.
- Secrets never in `ENV`, `ARG` or a copied file: all persist in image layers. Build time: `RUN --mount=type=secret`. Runtime: injected by the orchestrator or a secret manager.
- `COPY . .` needs a `.dockerignore` excluding `.git`, `.env`, credentials and local data.
- Image scanned in CI (`trivy`, `docker scout cves`).

## Kubernetes
- `securityContext`: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]`.
- No `privileged: true`, `hostPath`, `hostNetwork` or `hostPID` without a stated reason.
- RBAC: no `cluster-admin` or wildcard verbs/resources for workloads. Dedicated ServiceAccount; `automountServiceAccountToken: false` unless the pod calls the API.
- NetworkPolicy: deny by default, explicit allows.
- No plaintext `Secret` manifests in git (base64 is not encryption): SOPS, sealed-secrets or an external secret manager.
- Images by digest or immutable tag.

## Terraform / OpenTofu
- No secrets in `.tf`, `.tfvars` or outputs. `sensitive = true` only hides CLI output: state still holds the value in plaintext.
- Remote state, encrypted, locked, access-restricted.
- Provider and module versions pinned; registry modules pinned to a version, git modules to a commit.
- Plan scanned in CI (`checkov`, `trivy config`).
- IAM: no `Action: "*"` or `Resource: "*"`.

## Cloud (AWS/GCP/Azure)
- Buckets private with public access blocked; access via IAM.
- Firewall rules and security groups: no `0.0.0.0/0` on SSH, RDP or database ports.
- IMDSv2 required (AWS): blocks SSRF from stealing instance credentials.
- Encryption at rest on storage and databases, keys in a KMS.
