---
name: test-and-fix
description: "Run tests, find failures, fix them, verify. Diff-aware: tests the routes/pages your changes affect. This skill MUST be invoked on the triggers below, and SHOULD be invoked after any code change the user has not yet verified. Triggers on: 跑測試, 測一下, 有沒有壞掉, run tests, test this, 跑一下 tests, 測試, check if broken"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.3.6"
---

## Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
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
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'); _BASE="${_BASE:-main}"
git fetch origin $_BASE --quiet
git diff origin/$_BASE --name-only
git log origin/$_BASE..HEAD --oneline
```

Identify affected routes/pages from changed files:
- controller/route files → which URL paths
- view/template/component files → which pages render
- model/service files → which pages use those models
- API files → test endpoints directly

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

Run the existing test suite first, then manually test the affected routes/pages against the running app, following the Phase 2 plan.

For each test:
- **Pass** — describe what was verified
- **Fail** — exact symptom and evidence
- **Unexpected** — anything unplanned

---

## Phase 4 — Fix loop

For each failure, locate the root cause first. If the cause cannot be proven on the spot from the changes just tested, invoke the **investigate** skill and follow it through — it ends with the same fix and regression-test discipline. When the cause is proven:

1. Write the minimal fix and commit it on its own
2. Write a regression test that would have caught this specific bug — it must fail without the fix and pass with it — and commit it separately
3. Re-test the failing case

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
