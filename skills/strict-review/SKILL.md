---
name: strict-review
description: Blunt code review of a change of any size (a PR, a branch against main, uncommitted work or named files, up to thousands of lines), and a guide to understanding it. Picks the scope, runs the project's own QA, maps the change into parts and how they connect, reviews how it fits the existing architecture, triages what needs a deep look, reviews it line by line in one pass (security, correctness, performance, quality, over-engineering), and writes one tiered report for the maintainer and the contributor. When the change is too large for one thorough pass, it names the parts that deserve their own review instead of splitting on its own. Verdict REJECTED / NEEDS WORK / ACCEPTABLE. Use whenever asked to review code, a PR or a diff, check changes before commit or merge, audit a student's or contributor's work, or understand what a large PR does, even when phrased as "is this ready to merge?" or "look over my changes".
---

# Strict Review

Review as if in a bad mood: blunt, zero tolerance for bad code and bad practice. Report only real defects; never pad the list. Answer three questions: what does this change do and how do its parts connect, is it ready to merge, and what in it will cause problems later.

One review is one pass. A large change gets one pass over its deep scope plus a list of the parts worth a review of their own; the user picks which to run next. Never split a review or spawn reviewers on your own.

## 1. Scope and Mode

- Named by the user (PR, branch, files, whole repo): use it. PR: `gh pr diff <n>`.
- Otherwise: uncommitted work (`git diff HEAD` plus untracked files from `git status`) if any, else the current branch against the default branch (`git diff <default>...HEAD`).

State the scope before anything else, whether or not the user named it: what is reviewed, how it was chosen, the command. E.g. `Scope: no scope provided; reviewing uncommitted changes (git diff HEAD), 6 files.` or `Scope: PR #42 as requested (gh pr diff 42), 31 files.` The report repeats it.

Count changed lines with `git diff --numstat`, excluding generated files (lockfiles, notebook outputs, data, checkpoints, vendored code). The count sets the mode:

| Changed lines | Map | Triage | Line-level review |
|---|---|---|---|
| up to 400 | short | no | one pass, whole change |
| over 400 | full | yes | one pass, deep scope |

Deep scope over 1000 lines: the pass still runs, and the report flags the scope as too large and recommends part reviews (§8). Calibration on a 2000-line change: one pass caught every severe bug up to 2000 deep lines, but secondary findings (test gaps, edge cases, performance) are sampled, not exhaustive, and differ from run to run. Reviewers' defect detection also drops past 200-400 lines per session.

The architecture review (§5) runs in every mode: a small change wired badly into existing components is a key finding.

## 2. Map

Cut the change into parts along its weakest seams: files that call each other or share types go together; tests get their own part(s); generated, vendored and data files go apart. Aim for 400-1000 lines per part, so each fits one dedicated review. Per part:

- Name, files, `+added/-removed` lines.
- Role: core logic, data pipeline, model/training/evaluation, configs, scripts and notebooks, tests, plumbing, generated/vendored/data.
- What it does, in one sentence, and what it consumes from and feeds to the other parts and the existing code.

Notebooks: read code cells only. Up to 400 lines: one line per part.

## 3. Triage (over 400 lines)

Each part gets a depth:

- **Deep:** core and high-risk, per the "What Should Be Manually Reviewed" criteria in `line_review.md`.
- **Skim, blockers only:** secrets, hardcoded absolute or personal paths, committed data, checkpoints or large binaries, destructive file operations, notebook outputs carrying data or credentials.
- **Skip:** generated and vendored files.

The deep scope is the review's focus. Everything skimmed or skipped is not reviewed, and the report says so up front, never only at the end. Rank the deep parts by risk, most critical first.

## 4. QA (once, project-wide)

Run the project's own QA a single time. Its config is the source of truth; never guess past it.

Follow-up review (§8) given an earlier `QA:` line with its tree (`QA at <commit>, clean tree`): reuse it when `git rev-parse HEAD` matches and `git status --porcelain` is empty; otherwise rerun. The report marks it `QA (reused from <commit>):`.

QA executes repository code: Makefile recipes, hooks, `conftest.py`, tests, package scripts, `build.rs`. Change authored by someone other than the user (PR from another account, commits by another author): first read the parts of the diff that run during QA. Anything reaching for the network, credentials or files outside the repo: do not run QA; report it as a security finding.

1. **Discover**, in order: CI workflows (`.github/workflows/`, `.gitlab-ci.yml`), then task runners (Makefile, justfile, pixi tasks, tox/nox, `package.json` scripts, pre-commit). Fall back to language defaults only for the lint, type-check or test step neither defines: Python ruff, mypy, pytest; Node lint, test; Rust clippy, test; Go vet, test; C/C++ cppcheck. Run lint, type-check and test steps only, never build, publish or deploy steps.
2. **Run every check**, even after one fails, so one pre-existing error cannot hide the rest. A missing tool, or a CI step needing services or secrets unavailable locally, is `skipped (<reason>)`, never a failure.
3. **Never rewrite pinned state:** `uv run --locked`, `pixi run --locked`; no command that updates a lockfile. A stale lockfile is a finding.
4. **Catch rewrites:** hooks and formatters can modify files. Before running, `ref=$(git stash create); ref=${ref:-HEAD}` (snapshots the tree without touching it); after, `git diff $ref`. Report anything the tools rewrote as a finding; never keep it silently.
5. **No QA in the project** (no CI, task runner or pre-commit running lint, type-check or tests): a finding that sets the verdict to at least NEEDS WORK; language defaults still run per step 1. Its fix names the tools to wire into pre-commit and CI for each language present: Python ruff, mypy, pytest; JS/TS eslint, `tsc --noEmit`, vitest; Rust `cargo fmt`, clippy, `cargo test`; Go gofmt, `go vet`, `go test -race`; C/C++ clang-format, clang-tidy or cppcheck; Bash shellcheck, shfmt; any repo gitleaks.
6. **Failures:** one in files the change touches is a finding that sets the verdict to REJECTED; the review still continues, so a lint error never hides a security hole. Pre-existing failures elsewhere: one finding, no effect on the verdict.

## 5. Architecture Review

Read the change together with the existing code it touches: callers, callees, sibling modules, project conventions. Check:

- Fits the existing structure and conventions; lives in the right module.
- Reuses existing utilities instead of duplicating them.
- Interfaces with existing code and between parts: shapes, units, config flow, who calls what.
- Dependency changes and new entry points.
- Layer-level over-engineering: abstractions, wrappers or config systems with one user.
- One PR or several: unrelated concerns bundled together.

These are **design findings**: how the change fits the existing code and structure. Number them `D1`, `D2`, ..., each with a short title (`D1: <title>`). Finding format, severity levels and verdict rules: `line_review.md`.

## 6. Line-Level Review

One pass in this context over the deep scope (the whole change up to 400 lines), following `line_review.md`. It gets: its scope, one line on what the contribution claims, the `QA:` line, and the finding prefix `C`. Its findings are **code findings**: defects at specific lines, numbered `C1`, `C2`, ....

## 7. Repo Practices

Repo-wide habits that cause problems later, beyond line-level findings:

- Copy-pasted script variants (`train_v2.py`, `train_final.py`).
- Core logic without tests; logic living only in notebooks.
- Parameters hardcoded instead of in configs.
- Unseeded runs; results not traceable to a commit and config.
- Unpinned dependencies or no lockfile; no instructions to run.
- Dead experiment code piling up.
- ML code present: load the `ml` skill and check against `ml/references/evaluation.md` (leakage, splits, metrics).

## 8. Recommended Follow-up Reviews

After the pass, recommend which parts deserve a review of their own, most critical first. Recommend a part when:

- the deep scope was over 1000 lines (always say so: `Scope too large for one thorough pass: severe defects covered, secondary findings sampled.`);
- it is core logic with high-risk side effects, or the pass found severe defects there (more likely nearby);
- it is a test suite pinning core behaviour (the single pass is thinnest on test gaps);
- it was skimmed or skipped but looks risky after the pass.

Each recommendation: part, files, lines, why, what to look at, and the request to run it as its own review, carrying this review's QA so it is not rerun, e.g. `strict-review src/pkg/fusion/ tests/fusion/ against main; QA at a1b2c3d, clean tree: <QA line>`. QA ran on a dirty tree: leave the QA out of the request. Never start one yourself.

## 9. Report

One report. The contributor gets it with `What should be manually reviewed` removed, so every finding is written for someone learning: what, where, why it matters, the fix. The communication rules in `line_review.md` apply to the whole report, except the `Solid:` line and the part descriptions. Empty sections are left out, except `Scope` and `Not reviewed`.

1. `Scope:` what was reviewed and how it was chosen (`as requested` or `no scope provided`), the command, files, `+A/-D` lines (generated excluded), mode.
2. `Focus:` (over 400 lines) the deep scope and why it was picked.
3. `Not reviewed:` everything skimmed or skipped, or `Nothing.`
4. Verdict, then `deep review covered X of Y lines.`
5. `QA:` every check as `<tool> [<where it was found>] <result>`, e.g. `QA: ruff [pre-commit] pass; mypy [default] pass; pytest [make test] FAIL (3 failed); cppcheck [default] skipped (not installed).` A check left out reads as passed, so list all of them. Nothing ran: `QA: none run (<reason>, e.g. no CI, task runner or tool found).`
6. `Solid:` one line naming what is genuinely good, specific to this change. No filler.
7. `Map:` table: part, files, lines, role, what it does and connects to, depth.
8. `Must fix before merge:` every Critical and High finding, every skim blocker, and Medium findings that get costlier after merge (interfaces, data formats, shared defaults, public APIs).
9. `Follow-up PRs:` remaining findings grouped into PR-sized fixes.
10. `Practices:` §7 habits found, each with why it hurts later.
11. `Split plan:` how remaining or future work should arrive: PRs of at most 400 lines, one concern each, in dependency order.
12. `Findings in detail:` open with one legend line (`D = design finding: how the change fits the existing code; C = code finding: a defect at specific lines. Levels: Critical, High, Medium, Low (line_review.md).`), then three subsections, each finding headed by its ID and title:
    - `Design findings (D):` the §5 findings, under level headings.
    - `Code findings (C):` the pass's findings, under level headings.
    - `Simplifications (code to delete or shorten):` the pass's over-engineering lines and its `net:` line; no levels.

    Level headings (`Critical`, `High`, `Medium`, `Low`) appear only when they hold findings; IDs run worst first across levels, so `D1` and `C1` are the worst of their kind.
13. `Recommended follow-up reviews:` the §8 recommendations, or `None needed.`
14. `X issue(s) found.` Nothing found anywhere: `No issues found.` (`No issues found; QA not run.` when QA ran nothing).
15. `What should be manually reviewed:` the pass's focus lines, most critical first, then `Questions to answer:` 2-5 questions for the contributor to answer. Last, so removing it leaves a complete report for the contributor. Then stop: no summary, no closing remarks.

Sections 8 and 9 cite findings by ID, level and title (`D1 (High): upstream patches can silently stop applying`) instead of restating them; skim blockers have no number, so state them in full.

## 10. References

- `line_review.md`: rules for the line-level pass (priorities, verification, over-engineering, what should be manually reviewed, verdict, pass output, communication rules)
- `owasp_top10.md`: OWASP Top 10 (2025) review checks
- `auth_protocols.md`: OAuth 2.0, OIDC, JWT, SAML review checklist
- `supply_chain.md`: New dependencies, pinning, scanning, CI/CD pipeline security
- `language_specific.md`: Python (incl. ML artifacts), JS/TS, Go, Rust, Java, Bash, C/C++ security patterns
- `infrastructure.md`: Docker, Kubernetes, Terraform/OpenTofu, cloud security
- `testing_strategy.md`: What to flag when reviewing tests
