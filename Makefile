# Version helpers for lab-starter-skills. The repository holds only skill
# files, so versions are plain annotated git tags and no version string is
# stored anywhere else. Tags are `X.Y.Z` (no `v` prefix), matching the
# CHANGES.md section links, same convention as lab-advanced-template.

# Bump rules, pick the target that matches the change:
#   bump-major  a skill was removed, renamed, or guidance reversed.
#               Users must re-read or re-edit their installed copies.
#   bump-minor  a new skill or new guidance was added.
#               Existing copies stay valid, just weaker.
#   bump-patch  wording, links, or typo fixes.

# Release workflow:
#   1. Keep ongoing changes as list items under [Unreleased] in CHANGES.md.
#   2. At release time, insert the new version header directly below the
#      [Unreleased] separator so the existing items fall under it:

#          <!-- (New changes here in list form) -->

#          ## [X.Y.Z](REPOSITORY_URL/tree/X.Y.Z) (YYYY-MM-DD)

#          ______________________________________________________________________

#      Commit the result.
#   3. Run the matching target, for example `make bump-minor`.
#      Add DRY=1 to preview without tagging.
#   4. Push with `make push`.

# The next version is derived from the newest existing tag, so the CHANGES.md
# header from step 2 must match the target chosen in step 3.

SHELL := /bin/bash
.DEFAULT_GOAL := help

VERSION_RE := ^[0-9]+\.[0-9]+\.[0-9]+$$
# uvx runs pre-commit in a cached throwaway env: uv is the only requirement.
PRE_COMMIT := uvx pre-commit@4.7.0

.PHONY: help status check bump-major bump-minor bump-patch push

help: ## List available targets
	@grep -hE '^[a-zA-Z0-9 ._-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-32s %s\n", $$1, $$2}'

status: ## Show the latest version tag and any commits since it
	@set -euo pipefail; \
	last=$$(git tag --sort=-v:refname | grep -E '$(VERSION_RE)' | head -1 || true); \
	if [[ -z $$last ]]; then \
		echo "No version tags yet. Next: bump-minor yields 0.1.0."; \
		git log --oneline -10; \
	else \
		echo "Latest tag: $$last"; \
		git log --oneline $$last..HEAD; \
	fi

check: ## Run all pre-commit hooks on every file
	@$(PRE_COMMIT) run --all-files

bump-major bump-minor bump-patch: ## Tag the next version, see bump rules at top
	@set -euo pipefail; \
	cur=$$(git tag --sort=-v:refname | grep -E '$(VERSION_RE)' | head -1 || true); \
	cur=$${cur:-0.0.0}; \
	IFS=. read -r major minor patch <<<"$$cur"; \
	case $@ in \
		bump-major) major=$$((major+1)); minor=0; patch=0 ;; \
		bump-minor) minor=$$((minor+1)); patch=0 ;; \
		bump-patch) patch=$$((patch+1)) ;; \
	esac; \
	next="$$major.$$minor.$$patch"; \
	if git rev-parse -q --verify "refs/tags/$$next" >/dev/null; then \
		echo "$$next already exists. Did the last release fail to push?"; exit 1; \
	fi; \
	if ! grep -q "^## \[$$next\]" CHANGES.md; then \
		echo "CHANGES.md has no '## [$$next]' header."; \
		echo "Insert it per the release workflow (step 2) and commit first."; exit 1; \
	fi; \
	if [[ -n $${DRY:-} ]]; then \
		echo "DRY: would tag $$next"; \
	else \
		git tag -a "$$next" -m "$$next" && echo "Tagged $$next. Push with: make push"; \
	fi

push: ## Push the current branch and its annotated tags
	@git push && git push --follow-tags
