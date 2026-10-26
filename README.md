# lab-starter-skills

A starter kit of agent instructions and domain skills for Claude Code (and anything else that reads `SKILL.md` files). It captures a lab working style: fast experimentation, POC-grade deliverables, terse communication, and strict engineering conventions.

Use it as-is, or fork it and tune it to your own preferences.

## Read Before You Install

Skills are instructions your agent executes with its full permissions. Treat installing one like installing software:

- **Read everything before you install.** Every `SKILL.md`, `references/*.md`, and script you copy becomes standing instructions or executable code for your agent. The frontmatter `name` and `description` are injected into the system prompt of every session; the body is loaded whenever the skill triggers. Skim before, not after.
- **Treat third-party skills as untrusted code.** A skill can steer the agent toward prompt injection, data exfiltration, or misuse of the tools it can reach (shell, files, network, MCP servers). Be extra careful with skills that trigger on untrusted input such as web pages, issues, or emails.
- **Audit scripts before running them.** `code-review/scripts/run_qa.py` shells out to pre-commit, Makefile targets, and linters. It inherits the agent's permissions, so read any script before letting the agent execute it, and re-read it after updates.
- **Scope installs narrowly.** Prefer project-level installs over personal ones when testing a new skill, so it cannot affect every repository.
- **Fork and pin.** For anything you keep, own a copy in your own repo. Updates then happen only when you review and merge them. Avoid `curl | bash` style installs.
- This repo is MIT-licensed and meant to be audited line by line. Read the files, delete what you disagree with, and the kit becomes yours.

## Contents

```
example_CLAUDE.md          # Top-level instructions (CLAUDE.md) template
skills/
  code-review/             # Two-phase code review: automated QA script, then blunt manual review
  geospatial/              # Vector/raster processing, CRS, remote sensing, sensors, geospatial ML
  ml/                      # ML engineering and MLOps: training, evaluation, reproducibility
  planning/                # Three-phase planning workflow: Formal Design -> Spec -> Tasks, TDD-driven
  root-cause-analysis/     # Disciplined debugging: evidence first, fix root causes not symptoms
  software-dev/            # Full-stack engineering: architecture, backend, frontend, databases, infra, Bash/Python
```

Each skill is a directory containing:

- `SKILL.md`: the always-loaded core rules, with frontmatter (`name`, `description`) used for auto-triggering.
- `references/`: optional deep-dive docs that the SKILL.md links to and the agent reads on demand.
- `scripts/`: optional helper scripts (e.g. `code-review/scripts/run_qa.py` runs pre-commit, Makefile targets, or per-language lint/type/test chains).

## Installation

Skills are discovered by convention: a `skills/` directory where each subdirectory holds one `SKILL.md`. Copy the whole `skills/` folder, or just the skills you want.

### Claude Code

Personal (all projects):

```bash
cp -r skills/* ~/.claude/skills/
```

Project-level (this repo only):

```bash
cp -r skills/* .claude/skills/
```

### Top-level instructions

`example_CLAUDE.md` holds the standing user/project preferences (communication style, workflow gates, Python conventions, etc.). Rename and place it where Claude Code loads it:

| Scope | Location |
|-------|----------|
| Personal (all projects) | `~/.claude/CLAUDE.md` |
| Per project | `./CLAUDE.md` |

## Usage

No activation step is needed once installed. The agent matches each skill's `description` against the task and loads that `SKILL.md` automatically; deep-dive references are read only when the SKILL.md points at them. You can also invoke a skill explicitly (for example, ask the agent to "use the code-review skill on this diff").

## Notes

- The `planning` skill writes artifacts to `docs/agents/planning/<subject>/` in your project. Keep the paths in the skill and in `example_CLAUDE.md` in sync if you change that convention.
- `code-review/scripts/run_qa.py` needs Python 3 and runs whatever QA tools the target project already has configured.

## Further reading

- [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), Anthropic's official guide for writing effective skills.

## License

MIT. See [LICENSE](LICENSE).
