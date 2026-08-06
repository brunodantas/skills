---
name: ilities
description: Rank a system's architectural characteristics (nonfunctional requirements, "-ilities") at any scope, from a whole system down to one live decision, name the trade-offs, and offer to document the call. Use when starting a project or service, when a nonfunctional conflict blocks the next step (performance against reliability, security against usability), or when the user says "-ilities", "architectural characteristics", "nonfunctional requirements", or "architecture doc".
argument-hint: "[scope: a system, a service, a module, or the decision in front of you]"
allowed-tools: Read, Grep, Glob, Write, Edit
---

## Purpose

Pin down what something must be *good at* (its architectural characteristics, a.k.a. nonfunctional
requirements, or "-ilities"), **rank** them, and name what the ranking costs. The output answers one
question a reviewer or future-you keeps re-asking: *when two designs conflict, which characteristic
wins here?*

That question arrives at every size. Sometimes it is a new service with nothing written down.
Sometimes it is a single pull request where the fix for a latency regression puts a second source of
truth in front of a critical read path. The method is the same; only the ceremony changes.

The output is short and opinionated. A list of twenty "-ilities" is worthless, because everything
cannot be the priority. The value is in the **ranking** and the **explicit trade-offs**.

## Scope

The scope is whatever you are pointed at, and it is the first thing to settle:

| Scope | Typical trigger |
|---|---|
| Whole system or service | Starting something new, or an architecture doc that never got written |
| Module or subsystem | One area has different forces than the system around it |
| One live decision | A conflict is blocking the next step and someone has to rule on it |

**This skill writes nothing on its own.** It produces the ranking, then offers to land it. Accepting
the offer is a separate step you take deliberately.

## Process

1. **Fix the scope.** Take it from the argument. Invoked bare, infer it from context (the decision
   under discussion, the current branch's diff, otherwise the repo as a whole), state it in one line,
   and confirm before ranking anything.
2. **Gather context.** Read the spec/PRD, the `README`, any domain doc the repo keeps (`CONTEXT.md`
   or equivalent), and any existing `docs/architecture.md`. Don't elicit what the docs already state,
   confirm and extend it. **If a project-level ranking exists, it is the default this scope starts
   from.**
3. **Elicit the candidates.** At system or service scope, offer the standard menu and have the user
   pick the few that actually drive it:
   - *Operational:* availability, reliability, scalability, elasticity, performance, recoverability,
     deployability, observability.
   - *Structural:* maintainability, testability, extensibility, modularity, portability, security,
     configurability.
   - *Cross-cutting:* usability, accessibility, cost, interoperability, compliance.

   At decision scope, skip the menu. The conflict already names its candidates. Add one only if a
   real force is genuinely missing from the framing.
4. **Rank what's in play.** System or service: force the **top 3** driving characteristics and push
   back on lists longer than ~7. "Less is more" is the rule, not a suggestion. Narrower: just order
   the characteristics actually in tension. Two is a legitimate answer.
5. **Name the trade-offs, and check them against the project ranking.** Every characteristic you
   prioritise costs another; call the tension out and say which side wins here and why. Then compare
   with the project-level ranking. If this scope **inverts** it, say so explicitly and justify it as
   a deliberate exception. That flag is the most valuable line in the output; an unflagged inversion
   is indistinguishable from drift.
6. **Make it measurable.** For a driving characteristic, write what "good" looks like as something
   you could *test*: a number, a budget, an SLO. "Fast" is not a characteristic; "p95 < 200ms under
   1k rps" is. For a one-off ruling, the useful measurable is different: what observation would tell
   you this call was wrong.
7. **Offer to land it.** Propose one target (see below), confirm, then write. Never write unattended.

## Output format

A narrow scope returns a compact block. Same vocabulary as the doc, so accepting the offer is a
paste rather than a rewrite.

```md
**Scope:** <what this ranking governs>
**In tension:** <A> against <B>
**Ruling:** <A> wins here, because <reason>.
**What would prove this wrong:** <the observation that would falsify the call>
**Project ranking:** applies | inverted (<why the local order differs>) | none on file
```

A system or service scope returns the full doc:

```md
# Architecture — <system/service>

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
- e.g. Elastic scale: traffic is bounded, we accept vertical scaling only.

## Scoped rankings
<Only when a module or subsystem has been ranked separately. Each one states whether it inverts the
ranking above, and why.>

## Known trade-offs
- <characteristic A> wins over <characteristic B> when they conflict, because <reason>.
```

## Landing it

Propose exactly one target, based on the scope and on whether the ranking inverted the project
default. Confirm before writing.

| Scope | Proposed target |
|---|---|
| Whole system or service | `docs/architecture.md` (create `docs/` if absent), plus a link from wherever the repo points agents and newcomers (`CONTEXT.md`, `CLAUDE.md`, `AGENTS.md`, or the `README`) |
| Module or subsystem | A scoped section under `## Scoped rankings` in the same doc, beneath the project ranking |
| One decision, ranking applied | One line under `## Known trade-offs` |
| One decision, ranking inverted | An ADR, but **only if the repo already keeps them** (`docs/adr/`, `docs/decisions/`), matching its existing style. With no convention on file, don't introduce one: write a fuller `## Known trade-offs` entry carrying the reasoning inline |

## Rules

- **Settle the scope first.** Everything downstream depends on what you are actually ranking.
- **Rank or it doesn't count.** An unranked list is just vocabulary.
- **Never write unattended.** The ranking is the deliverable; the file is an offer.
- **Flag every inversion.** A local ranking that contradicts the project one is either a deliberate
  exception or a mistake, and only the justification tells them apart.
- **Say what you're *not* optimising for.** The de-prioritised list is as valuable as the driving one.
- **Measurable over adjectival.** If you can't imagine a test, a number, or a falsifying observation
  for it, sharpen it until you can.
- **Be opinionated, then let the user override.** Propose a ranking from the context; don't hand them
  a blank menu.
- **Keep it short.** Resist the urge to be comprehensive.

## When not to reach for this

Unprompted, surface it only when a nonfunctional conflict genuinely **blocks** the next step. Every
line of code trades something off, and a skill that fires on all of them is an interruption you learn
to ignore. Explicit invocation, at any scope, is always fair game.

## Re-running

Invoked again on the same scope: read what's already on file, fold in new forces or decisions, and
re-rank if priorities shifted. A ranking that actually changed is an architecture decision, not an
edit, so it lands the same way an inversion does.
