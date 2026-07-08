---
name: ship-it
version: 1.0.0
description: "Prepare and ship a feature branch. Sync, test, open PR. Triggers on: 可以上了嗎, 準備上線, 開 PR, ship this, deploy, release, 上線, merge, push this, 準備好了嗎, ready to go"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
---

## Auto-trigger

When the user says something is ready, wants to deploy, or asks if it can ship, activate immediately.

---

## Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
[ -z "$_BASE" ] && git rev-parse --verify origin/master >/dev/null 2>&1 && _BASE="master"
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
echo "REPO: $_REPO"
_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
echo "$_REMOTE" | grep -q "github.com" && echo "PLATFORM=github"
echo "$_REMOTE" | grep -q "gitlab" && echo "PLATFORM=gitlab"
which gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo "GH_CLI=true" || echo "GH_CLI=false"
git fetch origin $_BASE --quiet 2>/dev/null || true
git diff origin/$_BASE --stat 2>/dev/null | tail -3
git log origin/$_BASE..HEAD --oneline 2>/dev/null
DIFF_LINES=$(git diff origin/$_BASE --stat 2>/dev/null | tail -1 | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
echo "DIFF_LINES: $DIFF_LINES"
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
git fetch origin $_BASE
git merge origin/$_BASE --no-edit
```

If merge conflicts: show each conflict and ask whether to keep mine, keep theirs, or show both.

---

## Step 3 — Run tests

Detect and run:

```bash
[ -f package.json ] && npm test 2>&1 | tee /tmp/mystack_tests.txt
[ -f Gemfile ] && bundle exec rspec 2>&1 | tee /tmp/mystack_tests.txt
[ -f go.mod ] && go test ./... 2>&1 | tee /tmp/mystack_tests.txt
[ -f Cargo.toml ] && cargo test 2>&1 | tee /tmp/mystack_tests.txt
[ -f requirements.txt ] && python -m pytest 2>&1 | tee /tmp/mystack_tests.txt
[ -f pyproject.toml ] && python -m pytest 2>&1 | tee /tmp/mystack_tests.txt
```

Test failure triage:
- in-branch failure → stop, fix before shipping
- pre-existing failure → ask how to handle

---

## Step 4 — Coverage audit

Goal: 100% of new code paths have at least one test.

```bash
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" -o -name "*_spec.*" | grep -v node_modules | wc -l
```

For each changed file, search for corresponding test coverage. Rate:
- **strong** — behavior + edge cases + error paths
- **medium** — happy path only
- **weak** — implementation tests
- **none** — no tests

---

## Step 5 — Pre-landing check (if no prior review)

If no code review has been run on this branch, do a lightweight inline check:
- SQL injection
- race conditions
- auth boundaries
- missing error handling
- obvious security issues

If critical issues found: fix or get approval before pushing.

---

## Step 6 — Push and open PR

```bash
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

部署完成後建議跑：
  diff-inspector              確認 production 狀態
  project-memory              記下這次學到的
```

---

## Step 8 — Ship report

```text
## Ship Report [branch] [date]

Tests: N passed, N failed
Coverage: [summary]
Pre-landing review: [SKIPPED / N issues found, N fixed]
PR: [URL or "ready — push manually"]

Status: shipped
```

---

## Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"ship-it\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
