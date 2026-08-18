---
name: to-cases
description: Give a spec the numbered `## Cases` section that a test-writing session can encode — derived from the behaviours the spec describes and the unit's acceptance criteria, checked for holes, confirmed with the user, then landed in a durable file. Use when a spec has no cases, when its cases miss an acceptance criterion, or when the user says "to-cases", "derive the cases", or "the spec has no cases".
argument-hint: "[spec path] [ticket or issue path]"
allowed-tools: Read, Grep, Glob, Write, Edit
---

# To Cases

Turn a spec's prose into the numbered list of cases a later session can encode one-for-one.

`## Cases` is the contract between a spec and its tests. Where a spec has none, or has a list
with holes in it, the session writing tests has to invent the missing requirement, and an
invented requirement lands in test files, where the next unit of work never sees it. This skill
puts it back in the contract.

Runs before `/to-tests`, either on its own or because `/to-tests` found no usable case list. It
also runs *after* one: a `/to-tests` session that derived its cases inline can hand them here for
a durable home.

## The case format

A case names a precondition (Given), an action (When), and an outcome stated in terms a caller
can observe (Then): a response body, a resulting state, a returned value, or a raised
exception.

```md
1. **Expired token is rejected**
   - Given: a price token issued more than its lifetime ago
   - When: a caller verifies it
   - Then: verification raises the expiry error, and no booking row is created
```

A bare status code is not an outcome. A handler that saves the row and then answers 403
satisfies "returns 403", so where the action could change state, the outcome names the state
the action must leave behind.

If the repo documents its own spec format, at `docs/agents/cases.md` or wherever its
agent-instructions file points, that doc governs the section's heading and placement, and this
format is the fallback.

## What you read

- The **spec**: what it says the system does, its implementation decisions, and its out-of-scope
  list if it keeps one. That last one matters as much as the first: a case for something the
  spec excluded is a case someone will implement.
- The **unit of work** (a ticket, an issue), if one exists, whose acceptance criteria the list
  must cover.
- The repo's **spec-format doc** (`docs/agents/cases.md` or whatever its agent-instructions file
  names), if it has one. If that file or the agent-instructions file points at a domain-language
  doc, read that too, so case names use the domain's words, but don't go hunting for one.

Read no implementation. Cases state what the spec asked for; existing code is at best a
paraphrase of that and at worst the bug.

## Opinionated asks

Wherever this skill puts a decision to the user, lead with your pick: mark it `➡️`, give the
one-line grounds, then ask. The recommendation saves them composing an answer, it never stands in
for one, so wait for theirs either way. Where you have no grounds to pick, say so rather than
inventing one. The marker belongs in the conversation, never in a file you write.

## Process

### 1. Locate the sources

The spec is the path you were given; failing that, the one `docs/agents/cases.md` names, if the
repo has that file; failing that, ask the user. Never guess at a conventional location: a case
list written into the wrong file is worse than one question.

Work with no spec at all, only a ticket or an issue, still has a case list to derive. The
acceptance criteria become the whole source, and where the list should live becomes one more
thing you take to step 4.

### 2. Derive the list

**One case per behaviour the spec describes, and one per way that behaviour can be refused:** the
expired input, the missing permission, the duplicate submission. The rejections are half the
contract and the half a spec most often leaves implicit.

Specs carry those behaviours in whatever shape their author chose. User stories are the common
one, and each branch of a story is a behaviour. A requirements list, a prose description, or a
table of endpoints all work the same way: read what the system is being asked to do, and
enumerate the ways each of those can go.

Then one case for every acceptance criterion in the unit that no behaviour already covers.

Group them the way the spec groups itself, and number them straight through. The numbering is
load-bearing: later sessions cite cases by number, one test per case.

### 3. Check it for holes

Before showing it to anyone:

- Every acceptance criterion in the unit maps to at least one case.
- Every case names a precondition, an action, and an observable outcome, per the format above.
- No case restates a bare status code as its outcome.
- Where the spec keeps an out-of-scope list, no case covers something on it.

A behaviour whose refusals you cannot enumerate without guessing is a hole in the spec, not
something to paper over: name it in step 4, with the answer you would give, and let the user rule.

### 4. Confirm the list, and where it goes

Show the list and the holes you found. Write nothing until the answer comes back. A derived list
is a proposal: the user is the one who knows which branch the spec deliberately left out and
which omission was an accident.

The holes are why this comes first. A guessed case that lands in the spec ahead of the question
is the next session's requirement, and nobody re-litigates a list they find already written.

**Every hole is an opinionated ask.** Give each one the answer you would write if the call were
yours, marked `➡️`, and the one line that makes it your pick: what in the spec, the surrounding
code, or the sibling behaviours points that way. A hole handed over bare makes the user do the
deriving you were invoked to do. Where nothing in the material points either way, say that and ask
straight; a manufactured pick on a genuine unknown is worse than no pick at all.

**Propose one target in the same breath**, marked `➡️`, and confirm it:

| What the repo has | Proposed target |
|---|---|
| A spec | That file. The spec owns the contract. |
| No spec, but a local file holding the unit | That file, beside its acceptance criteria. |
| Neither | Offer to create a spec file, and say where. Don't create a `docs/` layout the repo never chose without asking. |

A **remote** issue or ticket body (GitHub, Linear, Jira) is only edited on an explicit yes. It is
a durable home, but writing to it is an outward-facing action, and deriving a list is not.

### 5. Land it

Write the numbered section, with their corrections folded in, **into the file they confirmed**.
Never into the chat alone, and never only into test files: the contract outlives the session, and
the next unit of work inherits the cases from wherever you put them.

Where the target already has a `## Cases` section, extend and correct it in place. Keep the
existing numbering stable so citations elsewhere survive, and append rather than reflow.
Rewriting a list wholesale loses the decisions someone already made in it.

Then name the next step: `/to-tests`, which encodes this list one test per case. If the list came
back from a `/to-tests` session that already derived it, there is no next step; it is already
encoded, and this run gave it a home.

## What this skill does not do

No tests, no stubs, no commits. It changes one file and it stops there.
