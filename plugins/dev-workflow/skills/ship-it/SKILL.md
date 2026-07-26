---
name: ship-it
description: "Prepare and ship a feature branch: sync, test, open PR. This skill MUST be invoked on the triggers below, and SHOULD be invoked when the user sounds ready to merge without saying so outright. Triggers on: 可以上了嗎, 準備上線, 開 PR, ship this, deploy, release, 上線, merge, push this, 準備好了嗎, ready to go"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.3.0"
---

## Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
[ -z "$_BASE" ] && git rev-parse --verify origin/master >/dev/null 2>&1 && _BASE="master"
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
which gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo "GH_CLI=true" || echo "GH_CLI=false"
[ -f delivery-plan.md ] && echo "DELIVERY_PLAN: exists" || echo "DELIVERY_PLAN: missing"
[ -f delivery-plan.md ] && head -20 delivery-plan.md
```

If `DELIVERY_PLAN: exists`: read the `Next Verifiable Output` and `Current Phase` sections. Before shipping, confirm:

```text
⚠ delivery-plan.md check:
- Current phase: [X]
- Next output: [Y]
- Does this diff match? [yes / no / no delivery-plan found]
```

If it doesn't match, ask the user whether to update delivery-plan.md before shipping.

---

## Step 1 — Pre-flight

1. If `BRANCH == BASE`: abort with "You're on the base branch. Ship from a feature branch."
2. `git status` — if uncommitted changes exist, describe them and ask whether to commit, stash, or abort.
3. Show what's being shipped:
   - `git diff origin/$_BASE --stat`
   - `git log origin/$_BASE..HEAD --oneline`

---

## Step 2 — Sync with base

```bash
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'); _BASE="${_BASE:-main}"
git fetch origin $_BASE
git merge origin/$_BASE --no-edit
```

If merge conflicts: show each conflict and ask whether to keep mine, keep theirs, or show both.

---

## Step 3 — Run tests

Run the project's full test suite.

Test failure triage:
- in-branch failure → stop, fix before shipping
- pre-existing failure → ask how to handle

---

## Step 4 — Coverage audit

Goal: 100% of new code paths have at least one test.

For each changed file, search for corresponding test coverage. Rate:
- **strong** — behavior + edge cases + error paths
- **medium** — happy path only
- **weak** — implementation tests
- **none** — no tests

---

## Step 5 — Pre-landing review (if no prior review)

If no code review has been run on this branch, run the **diff-inspector** skill on the outgoing diff. If P0 issues are found: fix or get user approval before pushing.

---

## Step 6 — Push and open PR

Before pushing, scan the outgoing diff for secrets (keys, tokens, credentials, connection strings). If found, stop and tell the user — do not push.

```bash
_BRANCH=$(git branch --show-current)
git push origin $_BRANCH
```

If GH CLI is available:

```bash
gh pr create \
  --title "[auto-detect from branch name and commits]" \
  --body "$(cat <<'EOF'
## What
[1-2 sentences: what does this change do]

## Why
[Why is this needed]

## How
[Brief technical description]

## Testing
- Tests run: N passed
- Coverage: [summary]

## Checklist
- [ ] Tests pass
- [ ] No secrets committed
- [ ] Migrations reversible (if applicable)
- [ ] Docs updated
EOF
)"
```

If no GH CLI: print the PR description for the user to copy.

---

## Step 7 — Post-ship reminders

```text
PR 已建立。接下來你可以：

  gh pr checks --watch        盯 CI 狀態
  gh run watch                盯部署進度
  或等 GitHub 通知
```

---

## Step 8 — Record what this ship taught

Run the **project-memory** skill now, not after deployment. Shipping is the
wrap-up checkpoint that skill names, and it is the last point where the session
still holds why things went the way they did.

Decide out loud whether this branch taught anything worth keeping, then write it
without asking permission first. "Nothing this time" is a valid answer, but say
it rather than passing over the step in silence.

The earlier steps are where the candidates usually are: a test that failed in
Step 3 for a reason nobody would guess from the code, a gap Step 4 or Step 5 kept
finding, a Step 2 conflict that came from how the project is laid out rather than
from bad luck.

---

## Step 9 — Ship report

```text
## Ship Report [branch] [date]

Tests: N passed, N failed
Coverage: [summary]
Pre-landing review: [SKIPPED / N issues found, N fixed]
PR: [URL or "ready — push manually"]
Learnings recorded: [key(s) written to project-memory, or "none this time"]

Status: shipped
```
