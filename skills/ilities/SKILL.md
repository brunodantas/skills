---
name: ilities
description: Elicit, rank, and document a project's architectural characteristics (nonfunctional requirements / "-ilities") into docs/architecture.md, and keep implementation leaning toward the top-ranked ones. Use when starting a project or service, choosing an architecture, weighing a nonfunctional trade-off, or when the user says "-ilities", "architectural characteristics", "nonfunctional requirements", or "architecture doc".
argument-hint: "[project/service name or focus]"
allowed-tools: Bash, Read, Grep, Glob, Write, Edit
---

## Purpose

Pin down what a system must be *good at* — its architectural characteristics (a.k.a. nonfunctional requirements, or "-ilities") — **rank** them, and write them to `docs/architecture.md` so every later implementation decision has a reference to lean on. The doc answers one question a reviewer or future-you keeps re-asking: *when two designs conflict, which characteristic wins here?*

The output is short and opinionated. A list of twenty "-ilities" is worthless — everything can't be the priority. The value is in the **ranking** and the **explicit trade-offs**.

## Process

1. **Gather context.** Read the spec/PRD, the `README`, any domain doc the repo keeps (`CONTEXT.md` or equivalent), and any existing `docs/architecture.md`. Don't elicit what the docs already state — confirm and extend it.
2. **Elicit the candidates.** Offer the standard menu and have the user pick the few that actually drive this system. Common characteristics:
   - *Operational:* availability, reliability, scalability, elasticity, performance, recoverability, deployability, observability.
   - *Structural:* maintainability, testability, extensibility, modularity, portability, security, configurability.
   - *Cross-cutting:* usability, accessibility, cost, interoperability, compliance.
3. **Force a ranking.** Make the user choose the **top 3 driving characteristics** — the ones the architecture is explicitly optimised for. Push back on lists longer than ~7; "less is more" is the rule, not a suggestion.
4. **Name the trade-offs.** Every characteristic you prioritise costs another. Call the tensions out explicitly (performance ↔ maintainability, security ↔ usability, scalability ↔ simplicity/cost). State which side wins here and why.
5. **Make them measurable.** For each driving characteristic, write what "good" looks like as something you could *test* — a number, a budget, an SLO — not an adjective. "Fast" is not a characteristic; "p95 < 200ms under 1k rps" is.
6. **Write `docs/architecture.md`** (lowercase, under `docs/`) in the format below. Create the `docs/` dir if absent.
7. **Link it.** Reference the doc from wherever the repo points agents and newcomers (`CONTEXT.md`, `CLAUDE.md`, `AGENTS.md`, or the `README`) so it's discoverable, and note that implementation should lean toward the top-ranked characteristics.

## Output format

```md
# Architecture — <project/service>

## Context
<1–3 sentences: what this system is, and the forces shaping it.>

## Driving characteristics (ranked)
| # | Characteristic | Why it matters here | "Good" looks like (measurable) |
|---|----------------|---------------------|--------------------------------|
| 1 | Reliability    | Bookings can't be lost | Zero dropped writes; every mutation idempotent |
| 2 | Observability  | On-call must diagnose fast | Every request traceable end-to-end |
| 3 | Maintainability| Small team, long horizon | New endpoint added without touching core |

## Explicitly de-prioritised
<What we are NOT optimising for, and the cost we accept. Saying this out loud prevents scope creep.>
- e.g. Elastic scale — traffic is bounded; we accept vertical scaling only.

## Known trade-offs
- <characteristic A> wins over <characteristic B> when they conflict, because <reason>.
```

## Rules

- **Rank or it doesn't count.** An unranked list is just vocabulary. The top 3 are the deliverable.
- **Say what you're *not* optimising for.** The de-prioritised list is as valuable as the driving one.
- **Measurable over adjectival.** If you can't imagine a test or a number for it, sharpen it until you can.
- **Be opinionated, then let the user override.** Propose a ranking from the context; don't hand them a blank menu.
- **Keep it short.** 3 driving, a handful de-prioritised, the real tensions. Resist the urge to be comprehensive.

## Re-running

Invoked again on the same project: read the existing `docs/architecture.md`, fold in new forces or decisions, re-rank if priorities shifted, and record an architecture decision record if a ranking actually changed — a reprioritised characteristic is an architecture decision, not an edit.
