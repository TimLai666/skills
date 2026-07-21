---
name: test-and-fix
description: "Run tests, find failures, fix them, verify. Diff-aware: tests the routes/pages your changes affect. Triggers on: 跑測試, 測一下, 有沒有壞掉, run tests, test this, 跑一下 tests, 測試, check if broken, 有沒有問題"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.0.0"
---

## Auto-trigger

When the user asks to run tests, check if something is broken, or verify a fix, activate immediately.

---

## Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
echo "REPO: $_REPO"
[ "$_BRANCH" = "$_BASE" ] && echo "ON_BASE=true" || echo "ON_BASE=false"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
( [ -f requirements.txt ] || [ -f pyproject.toml ] ) && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
ls jest.config.* vitest.config.* playwright.config.* cypress.config.* .rspec pytest.ini 2>/dev/null
ls -d test/ tests/ spec/ __tests__/ e2e/ 2>/dev/null
[ -f delivery-plan.md ] && echo "DELIVERY_PLAN: exists" || echo "DELIVERY_PLAN: missing"
[ -f delivery-plan.md ] && head -20 delivery-plan.md
```

If on base branch with no URL: "You're on the base branch. Switch to a feature branch or provide a URL to test."

If `DELIVERY_PLAN: exists`: read the `Next Verifiable Output` section. If the tests you're about to run don't align with what the plan says should be verified, flag it:

```text
⚠ delivery-plan.md says the next output is: [X]
But you're testing: [Y]
Make sure this is the right thing to verify.
```

---

## Phase 1 — Analyze what changed

```bash
git fetch origin $_BASE --quiet
git diff origin/$_BASE --name-only
git log origin/$_BASE..HEAD --oneline
cat TODOS.md 2>/dev/null | head -20
```

Identify affected routes/pages from changed files:
- controller/route files → which URL paths
- view/template/component files → which pages render
- model/service files → which pages use those models
- API files → test endpoints directly

Framework detection:

```bash
grep -r "resources\|get\|post\|put\|delete\|patch" config/routes.rb 2>/dev/null | head -20
find . -name "*.ts" -o -name "*.js" | xargs grep -l "router\.\|app\." 2>/dev/null | head -10
grep -r "@app\.\|@router\." --include="*.py" 2>/dev/null | head -20
```

Detect running app:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null && echo "APP:3000" || \
curl -s -o /dev/null -w "%{http_code}" http://localhost:4000 2>/dev/null && echo "APP:4000" || \
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null && echo "APP:8080" || \
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null && echo "APP:5173" || \
echo "APP:not_found"
```

If no running app: ask the user for the URL or how to start it.

---

## Phase 2 — Build test plan

For each affected route/page:

| Route/Page | Change type | Tests to run | Priority |
|-----------|-------------|--------------|----------|
| `/payments/new` | Added validation | Submit empty, invalid, valid | P0 |
| `/api/users/:id` | Auth check added | Unauthenticated, wrong user, correct user | P0 |
| `/dashboard` | New component | Renders, empty state, error state | P1 |

Cross-reference commit messages and TODOs to verify the branch does what it was supposed to do.

---

## Phase 3 — Execute tests

Run existing test suite first:

```bash
[ -f package.json ] && npm test 2>&1
[ -f Gemfile ] && bundle exec rspec 2>&1
[ -f go.mod ] && go test ./... 2>&1
[ -f Cargo.toml ] && cargo test 2>&1
[ -f requirements.txt ] && python -m pytest 2>&1
[ -f pyproject.toml ] && python -m pytest 2>&1
```

Then test affected routes/pages manually:

```bash
curl -s -X POST http://localhost:3000/api/payments \
  -H "Content-Type: application/json" \
  -d '{}' | jq .

curl -s http://localhost:3000/api/users/2 \
  -H "Authorization: Bearer <user-1-token>" | jq .
```

For each test:
- **Pass** — describe what was verified
- **Fail** — exact symptom and evidence
- **Unexpected** — anything unplanned

---

## Phase 4 — Fix loop

For each failure:
1. Locate root cause first
2. Write the minimal fix
3. Write a regression test that would have caught this specific bug
4. Commit atomically:

```bash
git add -p
git commit -m "fix: [exact description]

Regression: [test name that covers this]"
```

5. Re-test the failing case

**Iron Law: every bug fixed must add one regression test.**

---

## Report

```text
## Test Report [feature/branch] [date]

### Summary
Tests run: N | Passed: N | Failed: N | Fixed: N (with regression tests)

### Changes tested
- [route/component] — [result]

### Bugs found & fixed
1. [description] — file:line — regression test: [test name]

### Issues found (not yet fixed)
1. [P0/P1/P2] [description] — blocking: [yes/no]

### Regression tests added
- [test file]: [test names]

### Recommendation
[SHIP / FIX FIRST / INVESTIGATE]
```

---

## Test framework bootstrap (if no tests exist)

```text
No test framework found. I can set one up.

RECOMMENDATION: A — add tests now. Every bug fix adds a regression test,
and without a framework, that is not possible.

A) Bootstrap the best-fit framework with a basic passing test
B) Skip — I'll add tests later
```

If A: scaffold and commit separately as `git commit -m "test: bootstrap [framework]"`.

---

## Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"test-and-fix\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
