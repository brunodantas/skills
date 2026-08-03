#!/usr/bin/env python3
"""Validate the collection: skill frontmatter, and every relative link in every Markdown file.

Run from the repo root: python3 scripts/validate_skills.py
Exits 1 with a list of failures, 0 when the collection is clean.
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

# Skill descriptions are what the model matches a request against, so an empty or
# truncated one is a skill that never triggers.
MAX_DESCRIPTION = 1024

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
CODE_SPAN = re.compile(r"`[^`\n]*`")

failures = []


def fail(path, message):
    failures.append(f"{path.relative_to(ROOT)}: {message}")


def parse_frontmatter(text):
    """Return the frontmatter mapping. Raises ValueError if it is absent, unterminated, or not YAML.

    Frontmatter is parsed the way the loader parses it, with a real YAML parser: a hand-rolled
    line splitter accepts blocks a strict parser rejects, and a rejected block reaches the model
    with no fields at all.
    """
    if not text.startswith("---\n"):
        raise ValueError("missing or unterminated `---` frontmatter block")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError("missing or unterminated `---` frontmatter block")
    try:
        fields = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise ValueError(f"frontmatter is not valid YAML: {' '.join(str(exc).split())}") from exc
    if not isinstance(fields, dict):
        raise ValueError("frontmatter is not a YAML mapping")
    return fields


def check_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(skill_dir, "no SKILL.md")
        return None

    try:
        fields = parse_frontmatter(skill_md.read_text())
    except ValueError as exc:
        fail(skill_md, str(exc))
        return None

    name = fields.get("name")
    if not name:
        fail(skill_md, "frontmatter has no `name`")
    elif not isinstance(name, str):
        fail(skill_md, f"`name` is {type(name).__name__}, not a string; quote it")
        name = None
    elif name != skill_dir.name:
        fail(skill_md, f"`name: {name}` does not match directory `{skill_dir.name}`")

    description = fields.get("description", "")
    if not description:
        fail(skill_md, "frontmatter has no `description`")
    elif not isinstance(description, str):
        fail(skill_md, f"`description` is {type(description).__name__}, not a string; quote it")
    elif len(description) > MAX_DESCRIPTION:
        fail(skill_md, f"description is {len(description)} chars, over the {MAX_DESCRIPTION} limit")

    return name


def check_links(md_file):
    # Code carries example links and placeholders like [<filename>](<link>); only prose links
    # are meant to resolve.
    prose = CODE_SPAN.sub("", FENCE.sub("", md_file.read_text()))
    for target in LINK.findall(prose):
        target = target.split()[0]  # drop any "title" suffix
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (md_file.parent / target.split("#")[0]).resolve()
        if not resolved.exists():
            fail(md_file, f"broken link: {target}")


def main():
    if not SKILLS_DIR.is_dir():
        print("no skills/ directory", file=sys.stderr)
        return 1

    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skill_dirs:
        print("skills/ is empty", file=sys.stderr)
        return 1

    seen = {}
    for skill_dir in skill_dirs:
        name = check_skill(skill_dir)
        if name:
            if name in seen:
                fail(skill_dir / "SKILL.md", f"duplicate skill name `{name}`")
            seen[name] = skill_dir

    for md_file in sorted(ROOT.rglob("*.md")):
        if ".git" not in md_file.parts:
            check_links(md_file)

    # The README table is how anyone finds a skill; a skill missing from it is invisible.
    readme = (ROOT / "README.md").read_text()
    for name in seen:
        if f"skills/{name}/SKILL.md" not in readme:
            fail(ROOT / "README.md", f"`{name}` is not listed in the README")

    if failures:
        print(f"{len(failures)} problem(s):\n", file=sys.stderr)
        for line in failures:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"{len(seen)} skill(s) valid, all relative links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
