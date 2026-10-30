"""Check skill frontmatter and reference files under skills/."""

import re
import sys
from pathlib import Path

import yaml

SKILLS_DIR = Path("skills")
NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
MAX_DESCRIPTION_LEN = 1024
# Only bare or references/-prefixed names count; paths like docs/.../PLAN.md are examples.
REFERENCE_RE = re.compile(r"`(?:references/)?([a-z0-9_-]+\.md)`")


def check_skill(skill_dir: Path) -> list[str]:
    """Return the problems found in one skill directory."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir}: missing SKILL.md"]
    text = skill_file.read_text(encoding="utf-8")

    parts = text.split("---\n", maxsplit=2)
    if len(parts) < 3 or parts[0]:
        return [f"{skill_file}: missing frontmatter block"]
    try:
        meta = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        # A colon followed by a space in an unquoted value is the usual cause.
        return [f"{skill_file}: frontmatter is not valid YAML: {exc}"]
    if not isinstance(meta, dict):
        return [f"{skill_file}: frontmatter is not a mapping"]

    problems: list[str] = []
    name = meta.get("name")
    if name != skill_dir.name or not NAME_RE.match(skill_dir.name):
        problems.append(
            f"{skill_file}: name {name!r} must equal the directory name and match {NAME_RE.pattern}"
        )
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        problems.append(f"{skill_file}: description is missing or empty")
    elif len(description) > MAX_DESCRIPTION_LEN:
        problems.append(
            f"{skill_file}: description is {len(description)} chars, max {MAX_DESCRIPTION_LEN}"
        )

    mentioned = set(REFERENCE_RE.findall(text))
    present = {p.name for p in (skill_dir / "references").glob("*.md")}
    problems += [
        f"{skill_file}: mentions missing references/{n}"
        for n in sorted(mentioned - present)
    ]
    problems += [
        f"{skill_dir / 'references' / n}: not mentioned in SKILL.md"
        for n in sorted(present - mentioned)
    ]
    return problems


def main() -> int:
    problems = [
        p
        for d in sorted(SKILLS_DIR.iterdir())
        if d.is_dir()
        for p in check_skill(skill_dir=d)
    ]
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
