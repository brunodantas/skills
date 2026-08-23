# brunodantas/skills

A collection of standalone [Agent Skills](https://agentskills.io) for the SDLC loop, including:
- Architecture
- Verification
- Review

## Installation

Copy the skills into a project, under whatever agent directory it uses:

```bash
npx skills@latest add brunodantas/skills
```

Or install them as a Claude Code plugin, which keeps one copy and updates in place:

```shell
/plugin marketplace add brunodantas/skills
/plugin install sdlc@brunodantas
```

Plugin skills are namespaced, so they run as `/sdlc:to-tests` rather than `/to-tests`. To hand a
whole team the collection, commit the marketplace to the project's `.claude/settings.json` and
they are prompted to install it on first trust of the repo:

```json
{
  "extraKnownMarketplaces": {
    "brunodantas": {
      "source": { "source": "github", "repo": "brunodantas/skills" }
    }
  },
  "enabledPlugins": { "sdlc@brunodantas": true }
}
```

## Skills

| Skill | What it does |
|---|---|
| [`ilities`](skills/ilities/SKILL.md) | Rank architectural characteristics at any scope, from a whole system down to one live decision, and offer to document the call. |
| [`to-cases`](skills/to-cases/SKILL.md) | Derive a spec's numbered `## Cases` section from the behaviours it describes and a unit's acceptance criteria, and land it in a durable file. |
| [`to-tests`](skills/to-tests/SKILL.md) | Turn one unit of work into a frozen oracle: tests plus stub interfaces, offered as one freeze commit. |
| [`harden-tests`](skills/harden-tests/SKILL.md) | Adversarially check tests against the cases they claim to encode, then write down what the pass could not close. Uses sub-agents where it can, and says so when it can't. |
| [`build-pr`](skills/build-pr/SKILL.md) | Write the branch's PR description as a PR Map: a review tier, evidence-backed claims, and every file bucketed read-hard / skim / skip. Best with GitHub and an authenticated `gh`; degrades to a body you paste. |
| [`unslop`](skills/unslop/SKILL.md) | Cut AI tells from any writing and add human voice: puffery, AI vocabulary, em-dash and boldface overuse, chatbot phrases, hedging. Adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack)'s `unslop` (MIT). |

`to-cases` → `to-tests` → `harden-tests` chain, but each runs on its own. Take `to-cases` alone
if all you want is a spec convention that spells out its cases, or `harden-tests` alone to
measure how weak an existing suite is.

## No setup required

Every skill here runs with zero configuration: the formats are bundled, and anything a skill
can't discover it asks you once. There is deliberately no setup skill to run first.

If you'd rather pin a convention than answer the question each time, drop a file at one of
these paths and the skills will read it instead:

| Path | Read by | What to put in it |
|---|---|---|
| `docs/agents/cases.md` | `to-cases` | Where specs live, and what your cases section is called if not `## Cases` |
| `docs/agents/testing.md` | `to-tests`, `harden-tests` | The command that runs **one** test file, and where tests and fixtures live |
| `docs/agents/review-tiers.md` | `build-pr` | Your own tier trigger lists — start by copying [`REVIEW-TIERS.md`](skills/build-pr/REVIEW-TIERS.md) |

`docs/review-tiers.md`, `.github/review-tiers.md`, and any path your `CLAUDE.md` / `AGENTS.md`
points at work too. `docs/agents/` is just a common place to keep per-repo agent config; nothing
here requires it.

## Non-duplication policy

No skill here shadows the name of one in a widely installed collection, [`mattpocock/skills`](https://github.com/mattpocock/skills)
above all. If an idea from this collection is absorbed elsewhere, the skill here is deprecated
with a pointer rather than maintained in parallel.

## Status

`0.4.1`: six skills, installable as files or as a plugin. They are used daily in private repos,
and the public collection is what that use has settled into. Expect the interfaces to keep moving
through `0.x`; see the [changelog](CHANGELOG.md).

## License

MIT. See [LICENSE](LICENSE).
