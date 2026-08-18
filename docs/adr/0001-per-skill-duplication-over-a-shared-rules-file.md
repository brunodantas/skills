# Per-skill duplication over a shared rules file

Every skill in this collection states its shared conventions in its own `SKILL.md`, repeated
verbatim, rather than linking a single file at the repo root. The README promises standalone
skills, installable one at a time with `npx skills add`, and a root-level file would not travel
with a skill that someone copies into their own project. Drift between the copies is the accepted
cost, and it is the reason `scripts/validate_skills.py` exists.

## Considered options

Two alternatives were rejected. A shared file at the repo root breaks standalone install, which is
the collection's whole distribution story. Copying that file into each skill directory keeps the
install working but leaves the same duplication with an extra layer of indirection over it, so a
reader has to open two files to learn one rule.

## Consequences

The **opinionated ask** convention (lead with your pick, mark it `➡️`, wait for the answer anyway)
is stated once per skill and applied at ten decision points across the five. A change to the
convention is a five-file edit, and nothing but review catches a copy left behind.
