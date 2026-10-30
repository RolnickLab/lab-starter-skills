# lab-starter-skills

A starter kit of agent instructions and domain skills for Claude Code (and anything else that reads `SKILL.md` files). It captures a lab working style: fast experimentation, POC-grade deliverables, terse communication, and strict engineering conventions.

Use it as-is, or fork it and tune it to your own preferences.

## Read Before You Install

Skills are instructions your agent executes with its full permissions. Treat installing one like installing software:

- **Read everything before you install.** Every `SKILL.md`, `references/*.md`, and script you copy becomes standing instructions or executable code for your agent. The frontmatter `name` and `description` are injected into the system prompt of every session; the body is loaded whenever the skill triggers. Skim before, not after.
- **Treat third-party skills as untrusted code.** A skill can steer the agent toward prompt injection, data exfiltration, or misuse of the tools it can reach (shell, files, network, MCP servers). Be extra careful with skills that trigger on untrusted input such as web pages, issues, or emails.
- **Audit scripts before running them.** `code-review/scripts/run_qa.py` shells out to pre-commit, Makefile targets, and linters. It inherits the agent's permissions, so read any script before letting the agent execute it, and re-read it after updates.
- **Scope installs narrowly.** Prefer project-level installs over user-level ones when testing a new skill, so it cannot affect every repository.
- **Fork and pin.** For anything you keep, own a copy in your own repo. Updates then happen only when you review and merge them. Avoid `curl | bash` style installs.
- This repo is MIT-licensed and meant to be audited line by line. Read the files, delete what you disagree with, and the kit becomes yours.

## Contents

```
example_CLAUDE.md          # User-level instructions template (~/.claude/CLAUDE.md)
skills/
  code-review/             # Two-phase code review: automated QA script, then blunt manual review
  geospatial/              # Vector/raster processing, CRS, remote sensing, sensors, geospatial ML
  ml/                      # ML research engineering: evaluation under shift, reproducibility, SLURM, partner handoff (TRL 6-7)
  planning/                # Three-phase planning workflow: Formal Design -> Spec -> Tasks, TDD-driven
  root-cause-analysis/     # Disciplined debugging: evidence first, fix root causes not symptoms
  software-dev/            # Full-stack engineering: architecture, backend, frontend, databases, infra, Bash/Python
```

Each skill is a directory containing:

- `SKILL.md`: the always-loaded core rules, with frontmatter (`name`, `description`) used for auto-triggering.
- `references/`: optional deep-dive docs that the SKILL.md links to and the agent reads on demand.
- `scripts/`: optional helper scripts (e.g. `code-review/scripts/run_qa.py` runs pre-commit, Makefile targets, or per-language lint/type/test chains).

## Installation

### User-level vs project-level

Claude Code reads instructions and skills from two scopes:

| Scope | Location | Applies to | Shared with | Use it for |
|-------|----------|------------|-------------|------------|
| User-level | `~/.claude/` | Every project you open on this machine | Nobody (local to your account) | Personal preferences, and skills you want everywhere |
| Project-level | `.claude/` and `CLAUDE.md` at the repository root, committed | That repository only | Everyone who clones it | Project facts (stack, commands, paths), and skills the project relies on |

What goes where in this kit:

| File | Scope | Why |
|------|-------|-----|
| `example_CLAUDE.md` | **User-level only** | It holds personal preferences (communication style, approval gates, conventions), written in the first person. Claude Code loads every `CLAUDE.md` it finds (user, parent directories, project) and none overrides another, so a project copy duplicates your user-level one, imposes your preferences on collaborators, and drifts. Keep the project `CLAUDE.md` for project facts; `/init` drafts one. |
| `skills/` | **Either** | User-level: your personal toolkit, available in every project. Project-level: committed with the repository, so every collaborator gets the same skills at the same version. If a skill exists at both levels, the user-level one wins. |

### Instructions (user-level)

Copy `example_CLAUDE.md` to `~/.claude/CLAUDE.md`. Already have one? Merge them instead (see [Merging With an Existing Setup](#merging-with-an-existing-setup)). Repeat on every machine you work on.

```bash
mkdir -p ~/.claude
cp -n example_CLAUDE.md ~/.claude/CLAUDE.md  # -n: never overwrites an existing file
```

### Skills (user-level or project-level)

Skills are discovered by convention: a `skills/` directory where each subdirectory holds one `SKILL.md`. Copy the whole `skills/` folder, or just the skills you want.

User-level (all your projects):

```bash
mkdir -p ~/.claude/skills
cp -r skills/* ~/.claude/skills/
```

Project-level (one repository, shared through git):

```bash
mkdir -p .claude/skills
cp -r skills/* .claude/skills/
```

### Merging With an Existing Setup

Already have a `CLAUDE.md` or other skills? Merge deliberately; never overwrite.

- **Inventory first.** List what you have: `ls ~/.claude/skills/ .claude/skills/`, and diff your `CLAUDE.md` sections against `example_CLAUDE.md`. Collisions usually land on communication style, workflow gates, and language conventions.
- **Name collisions.** Skills are keyed by directory name; a same-named skill shadows silently, and the user-level one (`~/.claude/skills/`) wins over the project one (`.claude/skills/`). Keep one, rename its directory, and update the frontmatter `name` to match.
- **One source of truth per topic.** When your rules and this repository's skills and instructions contradict (commit policy vs the approval gates, your test framework vs `software-dev` discipline), pick a winner and delete the loser. Contradictory rules produce unpredictable behavior; "the model will figure it out" is not a merge strategy.
- **Merge, don't concatenate.** Fold `example_CLAUDE.md` in section by section: adopt, adapt, or skip. A rule kept in two places drifts; keep each rule exactly once.
- **Layer by scope.** Personal taste (tone, verbosity) goes in `~/.claude/CLAUDE.md`, project reality (stack, conventions, paths) in `./CLAUDE.md`. Claude Code loads both (and any `CLAUDE.md` in parent directories) without either overriding the other; when two rules contradict, it may follow either one. Keep each rule in exactly one file.
- **Overlap is fine, contradiction is not.** Two skills with similar `description` fields can coexist as long as their rules only differ in style. Genuine contradictions (TDD-first vs prototype-freely) need narrowed `description` triggers, or one skill goes.
- **Verify after merging.** Run representative prompts and check which rules win, or ask the agent what instructions and skills it sees. Behavior, not files, is the source of truth.

As mentioned above, try new skills in a project first instead of installing them at the user level right away.

## Usage

No activation step is needed once installed. The agent matches each skill's `description` against the task and loads that `SKILL.md` automatically; deep-dive references are read only when the SKILL.md points at them. You can also invoke a skill explicitly (for example, ask the agent to "use the code-review skill on this diff").

## Notes

- The `planning` skill writes artifacts to `docs/agents/planning/<subject>/` in your project. Keep the paths in the skill and in `example_CLAUDE.md` in sync if you change that convention.
- `code-review/scripts/run_qa.py` needs Python 3 and runs whatever QA tools the target project already has configured.

## Further reading

- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), Anthropic's official guide for writing effective skills.

## Contributing

Checks run through [pre-commit](https://pre-commit.com/) and only need [uv](https://docs.astral.sh/uv/). Run them before committing:

```bash
make check
```

This catches whitespace and end-of-file issues, merge conflict markers, large files, private keys and secrets (gitleaks), em dashes, and zero-width or bidi control characters, which can hide text in a skill that a reviewer cannot see in the diff. Hooks are defined in [.pre-commit-config.yaml](.pre-commit-config.yaml).

To run them on every commit instead:

```bash
uvx pre-commit@4.7.0 install
```

To update hooks, run `uvx pre-commit@4.7.0 autoupdate --freeze`. It keeps them pinned to commit SHAs, since tags can be moved.

## Versioning

Versions are annotated git tags (`X.Y.Z`, no `v` prefix) documented in [CHANGES.md](CHANGES.md). Install or pin a release with `git clone --branch 0.1.0`. To find the last version that touched one skill: `git describe --tags --abbrev 0 -- $(git rev-list -1 HEAD -- skills/<name>/)`. Maintainers: run `make help`; bump rules and the release workflow are documented at the top of the [Makefile](Makefile).

## License

MIT. See [LICENSE](LICENSE).
