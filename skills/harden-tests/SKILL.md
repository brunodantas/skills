---
name: harden-tests
description: Adversarially check tests against the cases they claim to encode — fresh sub-agents each name a wrong implementation that still passes, and every counterexample gets tightened away. Two bounded rounds, then a written list of what could not be closed. Use when the user says "harden the tests", "adversarial pass", or asks how weak a test file is.
argument-hint: "[test paths]"
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# Harden Tests

Ask one closed question of every test — *name a wrong implementation that passes this* — and
tighten whatever the answer finds.

Runs on tests that already exist and already run: after `/to-tests` has frozen an oracle, or on
its own against any suite whose weakness you suspect. A suite `/to-tests` froze has already had
every case refuted by a wrong implementation, so what is left to find here is an assertion that
binds loosely. A suite from anywhere else may still hold a test that asserts nothing, which this
pass reports as a counterexample like any other. Tightening strengthens a frozen oracle
rather than weakening it, so the fixes are offered as their own commit on top of the freeze.

## What you need before starting

- **The tests**, by path.
- **The list they encode**: the spec's numbered `## Cases`, or failing that the unit of work's
  acceptance criteria. The question needs a per-item subject, so a suite with nothing to be
  checked *against* gets `/to-cases` first.
- **The command that runs those files**: the repo's documented inner-loop command — the one
  `docs/agents/testing.md` names, or failing that its testing doc, contributing guide, or
  package scripts. Where no doc names one, ask rather than inferring a runner from the lockfile.

## Opinionated asks

Wherever this skill puts a decision to the user, lead with your pick: mark it `➡️`, give the
one-line grounds, then ask. The recommendation saves them composing an answer, it never stands in
for one, so wait for theirs either way. Where you have no grounds to pick, say so rather than
inventing one. The marker belongs in the conversation, never in a file you write.

## Process

**Two rounds, the first wide and parallel, the second narrow.** Then stop.

### Round one

Spawn one fresh `general-purpose` sub-agent per group of cases — the sections the list already
falls into, four or so agents over five or six cases each — in a single message so they run
concurrently. Each gets the whole case list and the paths of the test files for context,
answers only for its own group, and gets nothing from your conversation. The brief:

> For each numbered case, answer one question: name a wrong implementation that passes this
> test. Judge each case against the whole test file, not that test alone: an implementation
> refuted by a different test in the same file is not a counterexample, so answer `none`
> there. Answer with a counterexample sketch of two or three sentences, or the single word
> `none`. Confine the answer to that: no improvements, no extra cases, no style notes.

For every counterexample, tighten the test so it would fail against that implementation — or,
where the gap is in the spec rather than the test, add a case and take it back to the spec via
`/to-cases`.

Then re-run the files you changed and confirm two things: the tightening produced exactly the
failure you intended, and no other test changed state. A tightening that reddens a neighbour
has moved a requirement rather than sharpened one.

### Round two

One agent, over only the tests round one changed plus their class or module siblings.
Tightening one test can shift what a neighbour covers, and that is the only way an untouched
test goes stale. Same brief. Tighten, re-run, and stop.

Independent agents in one round beat the same agent run again: a fresh reader finds different
things whether or not the tests changed, so serial repetition buys diversity at full
wall-clock price, and four contexts reading six cases is a wider net than one reading
twenty-four.

### Where sub-agents aren't available

Some hosts can't spawn them, and some users switch them off. Run the same closed question
in-context instead, one case group at a time, and tighten as above.

**Say in the report that the pass was degraded.** The fresh reader is the mechanism: a context
that already knows why each assertion is there is the same context that failed to see the gap the
first time, so `none` from it is worth much less than `none` from a stranger. What survives is
the closed question itself, which still forces a concrete counterexample or an explicit `none`.
That is worth running. It is not worth reporting as if it were the real thing.

## Why the question is closed

An open-ended request to find gaps always finds some, and a reviewer that always reports
something teaches the reader to stop reading it. "Name a wrong implementation that passes" has
a `none`, so the report carries information.

For the same reason, **two rounds is the bound, not a target to converge from.** "Every case
answers `none`" is unreachable: no finite suite pins a function completely, so the question
always has an answer if you keep asking.

## What you leave behind

What survives round two goes in writing, under a **What the adversarial pass could not close**
heading — in the file holding the unit of work if there is one, otherwise wherever the suite's
decisions live. List the counterexamples you judged unreachable through the fixtures, out of
scope, or unencodable single-threaded, and say which of the three each one is. Naming them is
the deliverable; chasing them is not.

The written list stands as it is. Alongside it, **in the conversation only**, give the items you
judged *unreachable through the fixtures* a `➡️` pick: for each, either the fixture change that
would bring it back in range, or accept-and-why. They are the only bucket where a choice exists.
Out of scope and unencodable are terminal by their own definition, and a recommendation on those
is noise dressed as advice. Recommending a disposition is not chasing it.

If the pass ran without sub-agents, say so under the same heading. Both are statements about how
much this pass is worth, and a reader who takes a degraded one for the real thing will trust the
suite further than it earned.

## Offer the commit

Tightened tests are edits sitting in the working tree, and after a freeze they contradict a
commit that claims to be the oracle. Propose landing them, marked `➡️`: the test files you
changed, staged by explicit path, with a subject naming the hardening. Then let the user commit.

Never commit unattended. No skill in this collection does: `/to-tests` offers the freeze, and
this pass offers the tightening that strengthens it. Both are the user's to land.

## Batch the fixes

Edits to one file with non-overlapping anchors go in a single message together. A round
returning fifteen counterexamples should cost two or three turns, not fifteen.
