#!/usr/bin/env python3
"""Validate the collection: skill frontmatter, and every relative link in every Markdown file.

Run from the repo root: python3 scripts/validate_skills.py
Exits 1 with a list of failures, 0 when the collection is clean.
"""

import re
import sys
from pathlib import Path

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
    """Return the flat key/value frontmatter block, or None if it is absent or unterminated."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith("#") or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def check_skill(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(skill_dir, "no SKILL.md")
        return None

    fields = parse_frontmatter(skill_md.read_text())
    if fields is None:
        fail(skill_md, "missing or unterminated `---` frontmatter block")
        return None

    name = fields.get("name")
    if not name:
        fail(skill_md, "frontmatter has no `name`")
    elif name != skill_dir.name:
        fail(skill_md, f"`name: {name}` does not match directory `{skill_dir.name}`")

    description = fields.get("description", "")
    if not description:
        fail(skill_md, "frontmatter has no `description`")
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
