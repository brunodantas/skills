---
name: build-pr
description: Write the current branch's pull request description as a PR Map — a one-sentence summary, a review tier, evidence-backed claims, and every changed file bucketed by how hard it is to read. Opens the PR if none exists, refreshes it in place if one does, offers a few inline comments on the riskiest hunks, and never pushes. Use when the user says "build the PR", "write the PR description", or asks for a PR body.
argument-hint: "[base-branch or PR focus]"
allowed-tools: Bash(git *), Bash(gh *), Read, Grep, Glob
---

## Purpose

Write the current branch's PR description in the **PR Map** format and hand back the link. No
PR yet → open it first. One exists → refresh its description in place; never open a second.
The map is finished by up to five inline comments on the diff (step 6). Every reviewer on the PR
can see those and watchers are mailed about them, so they are proposed and posted only on a yes.

**Works best with** GitHub and an authenticated [`gh`](https://cli.github.com) (`gh auth
status`), which is how the PR gets created, edited, and annotated. Everything before that (the
diff, the base branch, the tier, the body) is plain `git`, so a missing `gh` or another forge
degrades rather than stops: see the end of step 3.

The format's job is to route attention: a reviewer who reads the description knows which files
to read hard, which to skim, and which to skip — and which claims have evidence behind them.

Two bundled references carry the detail:

- [`PR-MAP.md`](PR-MAP.md) — the body format, section by section, with the link rules.
- [`REVIEW-TIERS.md`](REVIEW-TIERS.md) — the default tier trigger lists, and how a repo overrides them.

This skill only writes the description. It never judges the diff, and it never produces the
evidence it cites — a review pass, a test run, or CI does that first.

## Principles

- **Never push.** Publishing the branch is the user's call, not a side effect of writing a
  description — and `gh pr create` must not smuggle one in. Branch not fully on the remote →
  stop, ask the user to push, re-run.
- **Nothing else reaches other people unasked.** Writing the description is the ask; the PR gets
  opened and edited for it. Anything beyond that which lands in someone's review queue, inline
  comments above all, is proposed first and sent on a yes.
- **Map, not transcript.** The diff is right there. A line earns its place only if the diff
  can't show it; never restate changes or explain *how* code works.
- **Only what you opened.** Read the load-bearing diffs before describing them — never infer a
  file's role from its name.
- **Don't run the checks.** Tests and builds already run in CI and in whatever review step
  preceded this; this one only writes.
- **Cite evidence, never generate it.** Claims point at evidence that already exists: session
  output, review findings, CI. A claim with nothing to point at is labelled `UNVERIFIED` — that
  label is the signal to go and get the evidence, not a blank to fill in here.

## Opinionated asks

Wherever this skill puts a decision to the user, lead with your pick: mark it `➡️`, give the
one-line grounds, then ask. The recommendation saves them composing an answer, it never stands in
for one, so wait for theirs either way. Where you have no grounds to pick, say so rather than
inventing one. The marker belongs in the conversation, never in a file you write.

## Process

### 1. Gather

Two facts that never depend on the base, resolved before you read this:

- Remote `HEAD`: !`git symbolic-ref refs/remotes/origin/HEAD --short`
- Current branch: !`git rev-parse --abbrev-ref HEAD`

Base = the argument if given, else the branch that remote `HEAD` names. With it settled:

```bash
git log <base>..HEAD --oneline
git diff <base>...HEAD --stat
```

If the remote `HEAD` line above is an error instead of a ref — some clones never set it — don't
hand over two options. Run `git remote set-head origin -a`, and mark what it resolves to as your
pick `➡️` before going further. Where that fails too, read `git branch -r` and the recent merge
commits for the branch the work actually lands on, name it as your pick, and ask. **Never assume
`main`**: a repo that merges to `dev` or `develop` would get a diff against the wrong base, and
every claim in the description would be computed from it.

Read the meaty diffs in full.

### 2. Compute the review tier

Match the changed files against the trigger lists in [`REVIEW-TIERS.md`](REVIEW-TIERS.md) —
unless the repo has its own review-tiers doc, in which case that one wins outright. Look for it
at `docs/agents/review-tiers.md`, `docs/review-tiers.md`, or `.github/review-tiers.md`, or
wherever the repo's agent-instructions file (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`)
points. First hit wins.

The tier is computed from lists, never from a per-PR judgment call. That is the whole point:
a reviewer can predict the tier before reading the description, so a surprising one is a
signal.

### 3. Get the PR number

The map's diff anchors need `<N>`, which doesn't exist until the PR does.

```bash
gh pr view --json number,url -q '[.number,.url]|@tsv'
```

- **PR exists** → take its `<N>` and URL.
- **No PR** → the branch must be fully pushed: `git rev-parse --abbrev-ref @{u}` succeeds and
  `git log @{u}..HEAD --oneline` is empty. If not, **stop** and ask the user to push. If yes,
  create with a minimal body (the real one needs `<N>`):

```bash
gh pr create --base <base> --head <branch> --title "<plain-English title>" --body "<one-sentence summary>"
```

Title: plain-English phrase, plus a scope tag in parens if the work belongs to a named
milestone.

Pass `--head` even though it looks redundant: without it `gh` may fork the repo and push the
branch itself, which is exactly what this skill promises not to do.

**From a fork** — `origin` is your copy and the PR belongs upstream — point `gh` at the upstream
repo (`gh repo set-default <owner>/<repo>`, or `--repo <owner>/<repo>` on each call) and give the
head as `<your-user>:<branch>`. A clone with several remotes and no default set makes `gh pr
create` fail rather than guess. `gh` cannot express an org-owned fork this way, so a PR from one
has to be opened by hand; run this skill afterwards to fill in the description.

**No usable `gh`, or another forge.** Don't stop: everything up to here came from `git`, and the
body is worth having whoever pastes it. Ask for the PR number or URL if one already exists, so
the map's diff anchors resolve. If there is none, write the map with plain basenames and no
links, and say in your reply which section will need them once the PR is opened. Compose the
body as normal, hand it back for the user to paste, and skip steps 5 and 6.

### 4. Compose the body

Four sections, in order, nothing else: the summary, the tier line, `## Claims`, and
`## PR Map`, plus `## Also in this PR` when it has something to carry. Write them per
[`PR-MAP.md`](PR-MAP.md), which holds the rules for each and the link construction the map
depends on.

### 5. Set it

Pipe the body straight to `gh` — no scratch file:

```bash
gh pr edit <N> --body-file - <<'EOF'
<body>
EOF
```

### 6. Offer to annotate hot hunks

Inline comments mark the only hunks the reviewer reads line-by-line: those where your
confidence is low **or** the blast radius is high. Aim for ≤5 per PR; a hunk that is both
high-confidence and low-blast-radius gets none.

**Propose them before posting.** List each one as file, line, and the sentence you would write,
marked `➡️` as the set you would post, and send only the ones the user approves. These land in
every reviewer's queue, so they are the user's to authorise, not a side effect of asking for a
description.

```bash
gh api "repos/{owner}/{repo}/pulls/<N>/comments" \
  -f commit_id="$(git rev-parse HEAD)" -f path="<full-path>" -F line=<line> -f side=RIGHT \
  -f body="🔍 confidence: <low|medium> — <what breaks if this is wrong, one sentence>"
```

On a refresh, list existing comments first
(`gh api "repos/{owner}/{repo}/pulls/<N>/comments" -q '.[].body'`) and only add ones not
already there — never duplicate.

Return the PR URL.

**Done when** the description is live with the tier line, Claims and the bucketed PR Map, every
map entry is a working link built from the real `<N>`, whichever annotations the user approved
are posted, and the PR URL is in your reply. On the degraded path, done when the full body is in
your reply, ready to paste, with the missing links named.
