# Changelog

All notable changes to this collection are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-08-23

### Added

- `unslop`: cut AI tells from any writing (puffery, AI vocabulary, em-dash and boldface overuse,
  chatbot phrases, hedging, jargon) and add human voice. The body is adapted verbatim from the
  `unslop` skill in [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan
  (cursor/plugins, MIT); only the frontmatter is rewritten to this collection's conventions. The
  name matches upstream deliberately: pstack is Cursor-only, so nothing installable in Claude
  Code is shadowed.

## [0.3.0] - 2026-08-18

### Added

- Every skill states the **opinionated ask** convention: wherever it puts a decision to the user, it
  leads with its pick, marks it `➡️`, and waits for the answer anyway. Applied at ten decision
  points across the five skills. Where a skill has no grounds to pick, it says so rather than
  inventing one, which keeps the test-runner question in `to-tests` and `harden-tests` an honest
  ask.
- `to-cases` answers the holes it finds instead of only naming them, `to-tests` recommends whether
  the oracle is worth hardening and which files to point it at, `harden-tests` recommends a
  disposition for the counterexamples that are unreachable through the fixtures, and `build-pr`
  picks a base branch instead of offering two ways to find one.
- `docs/adr/0001-per-skill-duplication-over-a-shared-rules-file.md` records why the convention is
  repeated in five files rather than linked from one.

- `build-pr` resolves the remote `HEAD` and the current branch through `` !`command` `` injection,
  so both arrive with the skill instead of costing a round trip. Only the two base-independent
  facts are injected; everything computed from the base still runs once the base is settled.
- `harden-tests` declares `allowed-tools`, which it never had. It was the one skill in the
  collection paying a permission prompt for the test command it exists to run.
- `scripts/validate_skills.py` checks that every `allowed-tools` entry is a tool name with an
  optional `(...)` pattern, under either separator the field accepts. An unbalanced parenthesis
  survives YAML and reaches the permission layer as a grant that matches nothing.

### Changed

- `build-pr` narrows its blanket `Bash` grant to `Bash(git *)` and `Bash(gh *)`, the only two
  binaries it invokes. `to-tests` and `harden-tests` keep the blanket grant on purpose: the test
  command they run belongs to the consuming repo and cannot be enumerated here.
- `ilities` drops `Bash`, having never run a shell command.

### Fixed

- `scripts/validate_skills.py` reads frontmatter with a real YAML parser instead of splitting it
  line by line, so the block is validated the way the loader parses it. The unquoted colon that
  broke three descriptions in 0.2.0 passed the old check silently; it now fails with the parser's
  own error. Values that parse to a non-string (`description: yes`) are rejected too. The
  `validate` workflow installs PyYAML.

## [0.2.0] - 2026-08-03

### Added

- The collection installs as a Claude Code plugin as well as a file copy: `.claude-plugin/plugin.json`
  declares the repo root as the `sdlc` plugin, and `.claude-plugin/marketplace.json` publishes it
  under the `brunodantas` marketplace. A team can commit the marketplace to its project settings
  and get updates by pushing here, instead of re-copying the files.

### Fixed

- `to-cases`, `to-tests`, and `harden-tests` had a colon inside an unquoted `description:` scalar,
  which is a YAML parse error: strict parsers drop every frontmatter field, leaving the skill with
  no description to match a request against. `scripts/validate_skills.py` parses frontmatter line by
  line and could not see it.

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
