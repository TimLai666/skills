---
name: diff-inspector
version: 1.0.0
description: "Inspect a diff before merging. Scope drift check, critical code review, specialist parallel dispatch, adversarial review. Triggers on: 幫我看 diff, 看一下改了什麼, review 一下, PR review, diff review, 幫我看看這個, code review, 看看有沒有問題"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---

## Auto-trigger

When the user shows a diff, pastes code changes, or asks to review something, activate immediately. Do not ask which mode.

---

## Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
[ -z "$_BASE" ] && git rev-parse --verify origin/master >/dev/null 2>&1 && _BASE="master"
_BASE="${_BASE:-main}"
echo "BASE: $_BASE"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
[ -f Cargo.toml ] && echo "STACK:rust"
git fetch origin $_BASE --quiet 2>/dev/null || true
DIFF_INS=$(git diff origin/$_BASE --stat 2>/dev/null | tail -1 | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
DIFF_DEL=$(git diff origin/$_BASE --stat 2>/dev/null | tail -1 | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
DIFF_TOTAL=$((DIFF_INS + DIFF_DEL))
echo "DIFF_LINES: $DIFF_TOTAL"
[ -f delivery-plan.md ] && echo "DELIVERY_PLAN: exists" || echo "DELIVERY_PLAN: missing"
[ -f delivery-plan.md ] && head -20 delivery-plan.md
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(auth|login|session|token|password|permission|role|access)' && echo "SCOPE_AUTH=true" || echo "SCOPE_AUTH=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '\.(rb|py|go|rs|java|cs|php)$' && echo "SCOPE_BACKEND=true" || echo "SCOPE_BACKEND=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '\.(tsx?|jsx?|vue|svelte|css|scss)$' && echo "SCOPE_FRONTEND=true" || echo "SCOPE_FRONTEND=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(migration|schema|\.sql)' && echo "SCOPE_MIGRATIONS=true" || echo "SCOPE_MIGRATIONS=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(api|routes|endpoints|controllers)' && echo "SCOPE_API=true" || echo "SCOPE_API=false"
```

If on the base branch with no diff: "Nothing to review — you're on the base branch."

If `DELIVERY_PLAN: exists`: read the `Next Verifiable Output` and `Current Phase` sections. If the current diff does not match what the plan says should be worked on, flag it:

```text
⚠ delivery-plan.md says the next output is: [X]
But this diff appears to be doing: [Y]
Is this intentional? Consider updating delivery-plan.md after review.
```

---

## Step 1 — Scope drift check

Before reviewing code quality, check whether they built what was requested:

```bash
git log origin/$_BASE..HEAD --oneline 2>/dev/null
cat TODOS.md 2>/dev/null | head -20
cat PLAN.md 2>/dev/null | head -30
```

Compare stated intent vs. actual diff:

```text
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary>
Delivered: <1-line summary>
[If drift: each out-of-scope change]
[If missing: each unaddressed requirement]
```

Informational only — do not block.

---

## Step 2 — Critical pass

Apply against the full diff:

**SQL and data safety:**
- string interpolation in SQL
- user-controlled input in WHERE/ORDER BY without parameterization
- missing DB transactions on multi-step writes
- unbounded queries
- non-reversible migrations

**Race conditions:**
- check-then-act without atomic locking
- `find_or_create_by` without uniqueness constraints
- shared mutable state
- `await` inside loops where `Promise.all` is possible

**Auth and trust boundaries:**
- new routes missing auth middleware
- authorization defaulting to allow
- direct object reference
- token validation without expiration

**Error handling:**
- promises without `.catch()` or `try/catch`
- catch-all handlers
- swallowed errors
- external API calls without timeout
- missing null/undefined guards

**Completeness gaps:**
- new enum/status values not handled everywhere
- new API response fields not handled in consumers
- new code paths with no tests

### Confidence calibration

Every finding must include a confidence score:

| Score | Meaning | Action |
|-------|---------|--------|
| 9-10 | Verified by reading specific code | Show normally |
| 7-8 | High-confidence pattern match | Show normally |
| 5-6 | Moderate | Show with caveat |
| 3-4 | Low confidence | Appendix only |
| 1-2 | Speculation | Only report if P0 |

Format: `[P0/P1/P2] (confidence: N/10) file:line - description`

---

## Step 3 — Specialist dispatch (parallel)

When `DIFF_LINES >= 50`, dispatch specialists in parallel via Agent:

1. **Testing specialist** — always
2. **Maintainability specialist** — always
3. **Security specialist** — if `SCOPE_AUTH=true` or backend diff > 100 lines
4. **Performance specialist** — if backend or frontend scope exists
5. **Data migration specialist** — if `SCOPE_MIGRATIONS=true`
6. **API contract specialist** — if `SCOPE_API=true`

When `DIFF_LINES < 50`: skip specialists, print `Small diff ($DIFF_LINES lines) — specialists skipped.`

Each specialist gets:
- the relevant checklist
- stack context
- JSON-lines output format
- `NO FINDINGS` when clean

Specialist checklists:

**Testing:** missing negative-path tests, missing edge-case coverage, test isolation violations, flaky test patterns, new public functions with zero coverage

**Security:** missing input validation at trust boundaries, auth/authz defaulting to allow, direct object reference, role escalation, weak hashing, non-constant-time comparison on secrets, secrets in source code, XSS with user data, command injection, SSRF, path traversal

**Performance:** N+1 queries, missing DB indexes, O(n^2) patterns, string concatenation in loops, heavy new dependencies, barrel imports, fetch waterfalls, unbounded list endpoints

**Data migration:** non-reversible migrations, table-locking ALTER TABLE, missing indexes on new foreign keys, data backfill in migration, old schema removed before old code is gone

**API contract:** response shape changed without version bump, new required request field without default, error response shape changed, pagination contract changed

Deduplicate findings by `path:line:category`, keep highest confidence.

### Adversarial subagent (always runs)

```text
You are an adversarial reviewer. Read the diff with `git diff origin/<BASE>`.

Think like an attacker and a chaos engineer. Find ways this code will fail in
production — not style issues, not missing tests, actual breakage or security holes.

Look specifically for:
- race conditions
- auth bypasses
- silent data corruption
- resource leaks
- swallowed failures
- trust boundary violations

For each finding: describe the exact failure scenario and classify as
FIXABLE or INVESTIGATE.
```

---

## Step 4 — Classify and fix

Output summary:

```text
Pre-Landing Review: N issues (X critical, Y informational) — Quality: N/10
```

Classify as AUTO-FIX or ASK:

**AUTO-FIX:** missing `.catch()`, missing null guard, missing `LIMIT` on unbounded query, obvious typo

**ASK:** auth checks, race-condition fixes, API contract changes, anything touching payments/sessions

For AUTO-FIX: apply fix, commit with `git commit -m "fix: [description] (diff-inspector)"`, report what was done.

For ASK: batch into one question with recommendation.

---

## Step 5 — Documentation staleness

```bash
for doc in README.md ARCHITECTURE.md CONTRIBUTING.md CLAUDE.md; do
  [ -f "$doc" ] && echo "DOC: $doc" || true
done
```

If the diff changes behavior described in a doc that was not updated, flag as informational.

---

## Final output

```text
## Diff Inspector [branch] [date]
Scope Check: [CLEAN / DRIFT / MISSING]
Diff: N lines (+N/-N across N files)
Specialists: [list dispatched]
Quality Score: N/10

### AUTO-FIXED (N issues)
- file:line - description - what was done

### NEEDS DECISION (N issues)
[batched question with recommendation]

### INFORMATIONAL NOTES
- file:line - observation

### Looks good
- [things done well]

### Adversarial review
[Findings or "No additional issues found"]
```

---

## Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"diff-inspector\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
