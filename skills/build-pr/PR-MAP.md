# The PR Map format

The body of a pull request description, as `/build-pr` writes it. Four sections, in this order,
and nothing else.

Together they define the reviewer's reading ritual: claims first, then the map's **Read hard**
bucket, then the inline hunk annotations — and nothing else line-by-line.

## Summary

No heading. One sentence, 25 words or fewer.

## Tier line

Directly under the summary:

```
**Review tier <1|2|3> — <line review|tests + hotspots|green checks only>**: <what triggered it, one fragment>
```

This line sets the reading ritual, so it names the trigger rather than asserting the tier. On
an escalation, name the unverified claim that caused it. See `REVIEW-TIERS.md` for the lists
the tier is computed from.

## `## Claims`

One bullet per behaviour this PR claims, each with its evidence:

```
- <behaviour statement> — <evidence>
```

Source the list from the spec or ticket if there is one, else from the PR's stated intent, plus
anything extra the diff does.

Evidence is one of: a verifying test (`path::test_name`), a command that ran green this session
(quote the one line that proves it), or behaviour evidence for user-facing changes (a
screenshot, or a driven walkthrough captured during review).

No evidence on record → end the bullet with **`UNVERIFIED`**. Never silently drop the claim:
the label is what escalates the tier, and a dropped claim escalates nothing.

If a review pass already produced a claims table this session, reuse it rather than rebuilding
it.

## `## PR Map`

Every changed file, bucketed by how hard it is to read:

- **Read hard** — a mistake here would hurt:
  `- [<filename>](<link>) — <one line: why it needs eyes>`
- **Skim** — load-bearing but mechanical:
  `- [<filename>](<link>) — <≤8-word fragment>`
- **Skip** — the rest: comma-separated basenames, no links.

Every changed file appears exactly once. A file you did not open cannot be in **Read hard**.

### Link construction

Link text is the basename. Prepend one parent segment only to disambiguate collisions
(`index.tsx` and friends).

**Markdown files** → the rendered blob at the head branch:

```
https://github.com/<owner>/<repo>/blob/<head-branch>/<full-path>
```

**Code and deleted files** → the PR diff anchor:

```
https://github.com/<owner>/<repo>/pull/<N>/files#diff-<hash>
```

where the hash is the SHA-256 of the path:

```bash
printf '%s' "<full-path>" | shasum -a 256 | cut -d' ' -f1   # or: sha256sum
```

`<N>` is the real PR number, which is why the map cannot be written before the PR exists.

Where no PR number is available at all (no `gh`, another forge, a PR not yet opened), write the
map with plain basenames and no links rather than guessing at anchors, and say which section
needs them once the number exists. An unlinked map still routes attention; a wrong link costs the
reviewer more than a missing one.

## `## Also in this PR`

At most 5 bullets, one short sentence each. Only what the map can't carry: a cross-cutting
decision, a deliberate deviation, a known gap. Omit the section entirely when it is empty.

## Ending

End the body with exactly:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

Unless the repo has said otherwise. Where the contributing guide or the agent-instructions file
(`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`) prescribes its own attribution wording or forbids
attribution outright, that wins. Absent any statement, the footer goes on.

## Worked shape

```md
Adds idempotency keys to the booking write path so retried submissions cannot double-book.

**Review tier 1 — line review**: touches the money path and a migration.

## Claims

- A retried submission with the same key returns the original booking — `tests/test_booking.py::test_retry_is_idempotent`
- The migration backfills existing rows without downtime — `make migrate-check` ran green: `0 rows locked`
- Concurrent submissions with the same key collapse to one booking — UNVERIFIED

## PR Map

**Read hard**
- [booking.py](https://github.com/acme/shop/pull/214/files#diff-9f2a…) — the key collision branch decides whether a second charge happens
- [0042_idempotency_key.py](https://github.com/acme/shop/pull/214/files#diff-71c4…) — backfill runs against live rows

**Skim**
- [serializers.py](https://github.com/acme/shop/pull/214/files#diff-3ab8…) — accepts and validates the new header

**Skip**
conftest.py, test_serializers.py, CHANGELOG.md

## Also in this PR

- The key is scoped per customer, not global: two customers may reuse a client-generated key.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
