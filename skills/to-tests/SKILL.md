---
name: to-tests
description: Turn one unit of work into its frozen oracle — the tests plus the stub interfaces they import, offered as a single freeze commit. Use once per unit (a ticket, an issue, a described change), after its cases are settled and before any implementation, when the user says "to-tests", "freeze the oracle", or "write the tests first".
argument-hint: "[ticket or issue path, or the cases themselves]"
allowed-tools: Bash, Read, Grep, Glob, Write, Edit
---

# To Tests

Write one unit of work's tests before the code they test exists, then **freeze** them.

Runs once per unit, after its cases are settled and before anyone implements it. The point is
authorship: the **frozen oracle** is written by a session that has never seen an implementation,
so it encodes what the spec asked for rather than what some code happens to do. The implementing
session then works in a fresh context, against a target it did not write and may not weaken.

That is what separates this from an interactive red-green loop, where the same session writes a
test and then the code that satisfies it. Here the whole oracle lands first, in one commit, and
the authorship boundary is the deliverable.

A "unit" is whatever names the work: a ticket, a GitHub issue, or a change the user described in
the chat. Where this file says *unit*, any of those will do.

If you arrived here on your own reading of the task rather than because the user named this
skill, propose it before starting: it writes test and stub files and ends in a commit, which is
more than someone asking a question about tests is expecting. Wait for their yes.

## What you read

- The **spec**, if the repo keeps one, and inside it the numbered `## Cases` section. That list
  is the contract you encode, one test per case.
- The **unit** itself, whose acceptance criteria the cases must cover.
- **Sibling test modules** in the same area, plus wherever the repo keeps shared fixtures and
  helpers (a `conftest.py`, a test-utils module, a factories package) for real fixture names and
  the local conventions: naming, one test module per source module, where test files live.
- The project's testing docs, its domain-language doc, and any architecture decision record in
  the area, so names match the domain language.

Read **no implementation of the code under test**. Where the surface is new, none exists, and
that absence is the mechanism. Where the unit changes code that already exists, read its public
signatures and stop there: the bodies are what the oracle must stay independent of.

## How much oracle the unit needs

A unit that names an existing suite as its own proof (a prefactoring, an extraction, a move,
anything whose acceptance criteria include *the existing tests pass unmodified*) gets a **thin
oracle covering only its new surface**. That suite is already the oracle for everything being
moved; re-pinning it writes a second one nobody asked for, and every case in it then drags a
stub and a set of fixes behind it.

The test for whether a case belongs: **would it still fail if the existing suite were the only
oracle?** If no, drop it. On an extraction that usually leaves the new seam's shape (the halves
being callable separately, the result type, the outcome the old code had no way to report) and
little else.

Say which shape you are writing, and roughly how many cases, before you write any. A
prefactoring that lands twenty-nine tests has misread its unit.

## Opinionated asks

Wherever this skill puts a decision to the user, lead with your pick: mark it `➡️`, give the
one-line grounds, then ask. The recommendation saves them composing an answer, it never stands in
for one, so wait for theirs either way. Where you have no grounds to pick, say so rather than
inventing one. The marker belongs in the conversation, never in a file you write.

## Process

### 1. Ground, and settle the case list

Read the sources above. The case list is the spec's numbered `## Cases`; failing that, the
unit's acceptance criteria; failing that, the cases the user hands you directly. Whichever it
is, it has to be complete enough to encode: every acceptance criterion covered by at least one
case, and every case naming a precondition, an action, and an outcome a caller can observe.

Where a spec exists but its list has holes, **run `/to-cases`** and let it land the corrections
in the spec, which is where the next unit will read them.

Where there is no spec at all, derive the list here. Show it, with any holes you found, and
**wait for a yes before encoding anything**. That confirmation is the safeguard: a requirement
invented at test-writing time lives in a test file, where the next unit never reads it, and the
oracle is answerable to the contract rather than the other way round. Once it is confirmed,
offer `/to-cases` to give the list a durable home, but do not hold up the oracle for it.

### 2. Stub the new surface only

Write the minimal public interface the tests import that **does not already exist**: signatures
only, each body raising the language's not-implemented error (`NotImplementedError`, `throw new
Error("not implemented")`, `panic("not implemented")`, or the local equivalent).

This is what makes the **red** honest. Without it the commit fails at import, which proves
nothing about the oracle and hands the implementer no target list. It also pins the interface at
spec time, so the implementer inherits a signature instead of inventing one.

**Never replace an existing body with a stub.** Where the surface is already there, the tests
import it as it stands, and the red comes from the missing behaviour instead.

### 3. Write the tests

One test per case, named for the case, asserting only what a caller can observe: a response
body, a resulting state, a returned value, a raised exception. Where the action could change
state, assert the state it left behind, as the case states it.

Test through the module's public interface, at the seams the spec named.

### 4. Verify the red

Run **only the test files you wrote**, with the repo's documented inner-loop command: the one
`docs/agents/testing.md` names, or failing that its testing doc, contributing guide, or package
scripts. Where no doc names one, ask the user rather than inferring a runner from the lockfile,
and offer to record their answer in `docs/agents/testing.md` so the next session need not ask.
Never the full suite: unrelated failures are noise you have to read past on every lap.

**Completion criterion:** each case has exactly one test, with no collection or import errors and
no test failing for a neighbour's reason. Each test either

- **fails** at its own assertion or on its own not-implemented error, or
- **passes**, because the behaviour it pins already exists.

A green test at freeze time is a **regression guard**: it passes because the behaviour it pins
already exists. List them by name when you report. The alternative reading is that the test is too
weak to distinguish anything, and step 5 is what tells the two apart.

### 5. Refute every case

A red test at this point failed on the stub's not-implemented error, not on anything the case
says. That red proves the import resolves and nothing else. A test that asserts nothing looks
exactly the same from here.

So refute each case: give the surface a **wrong implementation** that returns a plausible value
contradicting what the case states, and never raises. Run the oracle's files again. The case has
to fail **at its own assertion**. One that passes has **survived**, and a survivor blocks the
freeze.

Blocking, and every case rather than a sample. The failure this exists for is an oracle whose
tests assert nothing at all, and a sample walks straight past it.

**Read per-case results, or stop here.** This needs the runner to name which case failed. Where
step 4's output cannot tell them apart, nothing can be refuted and the freeze waits until the
tests run under a real test runner. A script that prints its results and exits 0 whatever
happened is the case in point: every test in it survives, because none of them can fail.

Red is what the runner reports, never what a test prints. Printed output can read as failure
while the run reports success, and that gap is the whole defect.

**The green tests get the same treatment from the other side.** A regression guard pins behaviour
that already exists, so mutate that body rather than a stub. This is the one time you replace a
working implementation, and only until the run finishes.

**One wrong implementation may refute several cases at once.** A case refuted as collateral still
counts, because its own test failed on its own assertion. Batch where a single mutation
contradicts a group, and keep the accounting per case rather than per run.

**Restore, then prove you restored.** Copy each file's exact bytes before you mutate it and `cmp`
against the copy afterwards. Mutate implementation and stub files only. A test file that changed
during this step means the check has damaged the thing it was checking.

**Completion criterion:** every case named with the wrong implementation that refuted it, and
every mutated file byte-identical to before. Report survivors by name, and fix them at step 3
before the freeze is offered again.

This gate asks whether an assertion binds at all. Whether it binds tightly is a different
question, and it belongs to `/harden-tests` after the freeze.

### 6. Offer the freeze commit

Prepare one commit, on the unit's topic branch, staging the test files and the stub files by
explicit path. Show the staged set and the subject you propose, marked `➡️`, and **land it only
on a yes**. The freeze is the one thing here you cannot quietly take back, which is exactly why
it is the user's to press.

The subject must contain the phrase:

```
freeze oracle for <unit>
```

`<unit>` is whatever names the work: a ticket number, an issue number, or a short slug. Prefix
the subject however the repo's recent log does (`git log --oneline -20` settles it) so a
Conventional Commits repo gets `test(<scope>): freeze oracle for <unit>` and a repo whose
commit-lint forbids that shape isn't handed a commit it will reject. The phrase itself is the
contract: it is how anyone, in this session or a later one, finds the freeze point, so confirm
once it lands that `git log --grep="freeze oracle for"` returns the commit.

**Check `git branch --show-current` before offering.** If it is the repo's default branch, don't
offer the commit at all: say so, offer to cut a topic branch from here, and wait.

Say two things when you offer. The commit touches production files too (the stubs), so it is not
a test-only change. And an oracle that is never committed is not frozen: it is a working tree
anyone can quietly edit, and the authorship boundary this skill exists to draw is the commit
itself. Declining is a real choice, not a deferral.

## After the freeze

Two things follow, and both belong to other sessions.

**Hardening is worth offering and never automatic.** `/harden-tests` spawns fresh sub-agents to
name wrong implementations that still pass, tightens what they find, and writes down what it
could not close. It is the difference between an oracle nobody attacked and one that survived
being attacked, and it costs several concurrent agents. Name it as the next step, say roughly
what it will spend, and mark your pick `➡️`: whether this oracle is worth a pass at all, and if
it is, which of the files you just wrote to point it at. Rank them by how much of the contract
rides on them against how little their assertions actually pin. If nothing in the suite looks
weak, recommending against the spend is the useful answer. A tightening pass strengthens the
oracle, so it may run after the freeze: it offers its changes as their own commit on top.

**Then implementation, in a fresh session.** The frozen oracle is not that session's to weaken.
The fresh context is the mechanism: a session that watched the oracle being written knows which
assertions were hard to satisfy.

## Re-freezing

A frozen oracle that turns out to be wrong is a decision for the user. When they call it, the
contract is corrected first, wherever it lives: through `/to-cases` into the spec if there is
one, otherwise re-derived and confirmed as in step 1. Then `/to-tests` runs again and lands a new
freeze commit. Correcting the test alone would leave the wrong requirement standing in the
contract, where the next unit inherits it.
