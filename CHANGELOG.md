# Changelog

All notable changes to this collection are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-03

First public release.

### Added

- Repo skeleton: MIT license, README, this changelog, and the `skills/<name>/SKILL.md` layout.
- `scripts/validate_skills.py`, run by a `validate` workflow on every push and pull request: it
  checks each skill's frontmatter (`name` matches its directory, `description` present and within
  the length limit, no duplicates) and that every relative Markdown link in the repo resolves.
- `ilities` — rank architectural characteristics at any scope (a whole system, a service, a module,
  or one live decision), name the trade-offs, flag any ranking that inverts the project default, and
  offer to land the call in `docs/architecture.md`.
- `to-cases` — derive a spec's numbered `## Cases` section from the behaviours it describes and a
  unit's acceptance criteria, then land it in a confirmed target: the spec, the file holding the
  unit, or a new spec file it offers to create.
- `to-tests` — freeze one unit of work's oracle: tests plus stub interfaces, offered as a single
  commit. Takes a ticket, an issue, or cases given directly, derives the list itself where no
  spec exists, and names `harden-tests` as an optional next step rather than running it.
- `harden-tests` — adversarially check tests against the cases they encode, in two bounded
  rounds, and write down what the pass could not close. Falls back to an in-context pass where
  sub-agents aren't available, labelled as degraded, and offers the tightening as a commit rather
  than landing one.
- `build-pr` — write the branch's PR description as a PR Map, with the format and the default
  review-tier trigger lists bundled as `PR-MAP.md` and `REVIEW-TIERS.md` inside the skill. Inline
  diff comments are proposed rather than posted, and a missing `gh` or a non-GitHub forge
  degrades to a body you paste instead of stopping the run.

Every skill runs with no configuration. Optional per-repo overrides are read from
`docs/agents/{cases,testing,review-tiers}.md` when present; see the README. No skill commits
without asking.
