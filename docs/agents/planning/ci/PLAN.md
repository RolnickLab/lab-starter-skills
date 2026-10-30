# CI for lab-starter-skills

## Sections

1. **Skill check + CI workflow**
   - `scripts/check_skills.py`, run as a `local` pre-commit hook (`language: python`, `pyyaml`).
   - `.github/workflows/ci.yml`: `make check` on PRs and pushes to `main`.
2. **gitleaks job** in `ci.yml`: full-history scan. The pre-commit hook uses `--staged`, so it scans nothing under `run --all-files`. Release binary verified by a pinned SHA-256; version kept in sync with the pre-commit rev.
3. **lychee workflow**: `.github/workflows/links.yml`, weekly cron plus manual dispatch.

## Skill check contract

- Input: none. Scans `skills/*/SKILL.md` from the repo root.
- Rules per skill directory:
  - Frontmatter between leading `---` lines parses as a YAML mapping.
  - `name` equals the directory name and matches `^[a-z0-9-]{1,64}$`.
  - `description` is a non-empty string of at most 1024 characters.
  - Every backticked `name.md` or `references/name.md` in `SKILL.md` exists in `references/`.
  - Every file in `references/` is mentioned in `SKILL.md`.
- Output: one `path: problem` line per failure on stderr, exit 1. Silent exit 0 otherwise.

## CI conventions

- Actions pinned to commit SHA with a version comment.
- `permissions: contents: read`, `persist-credentials: false`.
