# Review tiers — bundled defaults

Every PR carries a scrutiny tier, and the tier is computed from **trigger lists**, never from a
per-PR judgment call. That is what makes it useful: a reviewer can predict the tier before
reading the description, so a surprising one is itself a signal.

These are the defaults `/build-pr` uses when the repo has no review-tiers doc of its own.

## The tiers

| Tier | Ritual | Triggers |
|---|---|---|
| **1** | Line review | Migrations; auth and permissions; money; outbound sends (email, SMS, push, webhooks); public API contracts |
| **2** | Tests + hotspots | Everything else. The reviewer reads the test diff plus the map's **Read hard** bucket, never the whole implementation |
| **3** | Green checks only | Docs-only; test-only; chore-scoped dependency bumps |

## Resolution rules

1. **Highest tier touched wins.** Tier 1 is the highest. A docs change that also edits a
   migration is tier 1, not tier 3.
2. **An unverified behaviour claim escalates a tier-2 PR to tier 1.** Automatic, not a judgment
   call: a claim with no verifying test in the diff is exactly the thing a tests-plus-hotspots
   read would miss. A repo with no test suite will therefore see tier 1 on every PR — that is
   the intended reading, not a bug: with nothing to verify a claim, the diff gets read by hand.
3. **Tier 3 requires the whole diff to qualify.** One production file drags the PR to tier 2.
   A commit that adds tests *and* the stubs they import is not test-only.

## Overriding these in your repo

Copy this file to `docs/agents/review-tiers.md` — alongside whatever other agent config the repo
keeps — then edit the trigger lists to name your own risk surfaces. `docs/review-tiers.md` and
`.github/review-tiers.md` are honoured too, as is any path your agent-instructions file
(`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`) points at.

When such a doc exists, it wins outright: `/build-pr` uses its lists and ignores these. Keep the
three-tier shape and the resolution rules, and change only what counts as a trigger. A repo with
no money path and no migrations should say so rather than inheriting rows that never fire.
