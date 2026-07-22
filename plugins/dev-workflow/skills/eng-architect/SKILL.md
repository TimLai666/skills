---
name: eng-architect
description: "Design architecture and lock technical decisions for a feature. This skill MUST be used before implementation of a non-trivial feature begins, and SHOULD be used whenever the user is unsure how to split modules. Produces architecture diagrams, error maps, and convergence artifacts (delivery-plan.md, AGENTS.md, OpenSpec proposals). Triggers on: 技術方案, 架構設計, 怎麼切模組, eng planning, architecture design, 技術規劃, 這個功能技術上怎麼做, design review, UI review, AI slop scan"
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
metadata:
  version: "1.8.0"
---

## Command routing

- 「技術方案」「架構設計」「怎麼切模組」 → **eng mode**
- 「幫我看 UI」「設計有問題嗎」「AI slop」 → **design mode**
- No mode specified → ask which mode

---

## Eng mode

### Preamble

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
_BRANCH=$(git branch --show-current 2>/dev/null | tr '/' '-')
[ -z "$_BRANCH" ] && _BRANCH="unknown"
_REPO=$(basename "$_ROOT" 2>/dev/null)
echo "BRANCH: $_BRANCH"
echo "REPO: ${_REPO:-unknown}"
_DIR="$_ROOT/docs/plans"
DESIGN=$(find "$_DIR" -maxdepth 1 -name "*-$_BRANCH-*-plan.md" -type f -exec ls -t {} + 2>/dev/null | head -1)
[ -z "$DESIGN" ] && DESIGN=$(find "$_DIR" -maxdepth 1 -name '*-plan.md' -type f -exec ls -t {} + 2>/dev/null | head -1)
[ -z "$DESIGN" ] && [ -n "$_ROOT" ] && DESIGN=$(find "$_ROOT" -name '*-plan.md' -type f \
  -not -path '*/.git/*' -not -path '*/node_modules/*' -exec ls -t {} + 2>/dev/null | head -1)
[ -n "$DESIGN" ] && echo "PLAN_DOC: $DESIGN" || echo "PLAN_DOC: none"
[ -f ENG.md ] && echo "ENG_MD: exists" || echo "ENG_MD: none"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
[ -f Cargo.toml ] && echo "STACK:rust"
git log --oneline -15 2>/dev/null
cat ARCHITECTURE.md 2>/dev/null | head -40
```

Read the plan document if it exists. Read all existing architecture docs before designing anything new. If `ENG_MD: exists`, read `ENG.md` too — this run updates it rather than replacing it (Step 7).

`ARCHITECTURE.md` is a convention some projects happen to carry; read it when present. Nothing in this toolchain writes it, so its absence means nothing.

`plan-grilling` defaults to `docs/plans/` but writes wherever the user asked it to, which is why the last glob sweeps the whole repo. It matches on the `*-plan.md` filename, not the directory.

### One question at a time

Same rule as `plan-grilling`: ask one question, wait for answer, record decision, move on. Use multiple choice with recommendation when a decision is needed.

### Step 1 — Architecture diagram

Draw an ASCII diagram showing:
- entry points
- data flow
- state transitions
- service boundaries
- trust boundaries
- storage

```text
[Browser] --POST /api/payment--> [PaymentController]
                                   validate inputs
                                   [PaymentService] --> [Stripe API]
                                   [DB: payments] success/failure
                                   [EmailWorker] --> [Email]
                             (async)

Trust boundary: everything right of [PaymentController] is internal
State machine: pending -> processing -> succeeded | failed | refunded
```

Ask the user to confirm or adjust. Record decision.

### Step 2 — Error/rescue map (mandatory)

For every new operation that can fail:

| Operation | Exception/Error | Who catches it | What user sees | Tested? |
|-----------|-----------------|----------------|----------------|---------|
| Stripe charge | `Stripe::CardError` | PaymentService | "Card declined" + retry | Plan: yes |
| DB write | Connection timeout | ActiveRecord | 500 + alert | Plan: yes |
| Email send | SMTP failure | EmailWorker | Silent retry x3 | Plan: yes |

Anti-pattern: `rescue StandardError` or `catch Exception` is a code smell. Call it out.

### Step 3 — Shadow path analysis

For every new data flow, trace all four paths:
- happy path
- nil/null/undefined input
- empty/zero/blank input
- upstream error

For each shadow path: does the plan handle it? If not, flag it.

### Step 4 — Edge cases: user interactions

| Interaction | Edge case | Expected behavior | Covered? |
|-------------|-----------|-------------------|----------|
| Form submit | Double-click | Debounce / idempotency key | ? |
| Long operation | User navigates away | Background job continues | ? |
| Any form | Session expires mid-fill | Graceful redirect, data preserved | ? |
| List view | 0 results | Empty state with CTA | ? |
| List view | 10,000+ results | Pagination enforced | ? |

Flag any `?` as a gap.

### Step 5 — Test seams and matrix

#### 5a — Pick the seams first

A seam is a place where behavior can be swapped without editing the code under test — where the fakes get injected. Decide where the feature is tested before deciding what kinds of tests to write.

- Prefer existing seams to new ones. A seam that exists only to make testing possible is an architecture change, not a test decision.
- Take the highest seam that still reaches the behavior. High seams survive internal refactors; low seams go red when a private method moves.
- Fewer seams is better, one is ideal. Every extra seam is another set of fakes that can drift from the real thing.
- If a new seam is needed, propose it at the highest point possible.

Example — "place order, then send confirmation email":

| Seam | What gets faked | Cost |
|------|-----------------|------|
| `POST /orders` | Email sender | Survives every refactor below the controller |
| `OrderService.create` | Email sender, order repo | Breaks when the service interface moves |
| One spec per collaborator | Validator, pricing, template, SMTP | Four sets of fakes, all red on any internal rename |

Ask the user to confirm the seams before filling the matrix. Record decision.

#### 5b — Fill the matrix

Two rules before writing a single row:

- Test external behavior only. A test that breaks when internals are rewritten but behavior is unchanged is testing the wrong thing.
- Find prior art. Locate existing tests of the same shape in the codebase and follow their structure instead of inventing a new one.

| Test type | What to cover | Priority |
|-----------|---------------|----------|
| Unit | Core business logic, every branch | P0 |
| Integration | DB/API contracts, error paths | P0 |
| E2E | Happy path + top 3 error paths | P1 |
| Load | Estimated peak x3 | P2 if prod |

### Step 6 — Migration and deployment plan

If the change touches the DB:

```bash
ls db/migrate/ 2>/dev/null | tail -5
ls migrations/ 2>/dev/null | tail -5
```

For each migration: reversible? locks tables? needs backfill? can run while old code is live?

### Step 7 — Write ENG.md

Write to project root. `ENG.md` is a **state file**: one per project, updated in place. Never date-stamp or branch-stamp the filename — git already provides version history and branch isolation, and a second copy would leave re-sync with no single target to read.

**Read before writing.** If `ENG_MD: exists`, read it first and update the sections that changed. Do not regenerate from scratch — a re-sync that rewrites blind loses the prior run's error map and seam decisions.

```markdown
# Engineering Plan: [feature]
_[date] - eng-architect - [repo]:[branch]_

## Architecture
[ASCII diagram]

## Data flow
[Happy path]

## Error/rescue map
[Table]

## Shadow paths
[Per-flow analysis]

## Interaction edge cases
[Table]

## Test seams
[Chosen seam per flow, what gets faked, why this level]

## Test matrix
[Table]

## Migration plan
[If applicable]

## Hidden assumptions
- [assumption] - risk: [consequence]

## Definition of done
- [ ] All tests pass
- [ ] Every error path handled and tested
- [ ] Migration is reversible
- [ ] Deployed to staging, smoke-tested
- [ ] Docs updated
```

### Step 8 — Convergence artifacts (mandatory)

This step runs every time eng completes.

Check for existing artifacts:

```bash
[ -f delivery-plan.md ] && echo "DELIVERY_PLAN: exists" || echo "DELIVERY_PLAN: missing"
[ -f AGENTS.md ] && echo "AGENTS_MD: exists" || echo "AGENTS_MD: missing"
[ -f CLAUDE.md ] && echo "CLAUDE_MD: exists" || echo "CLAUDE_MD: missing"
cat delivery-plan.md 2>/dev/null | head -40
cat AGENTS.md 2>/dev/null | head -20
```

#### 8a — Create or update `delivery-plan.md`

Read [references/delivery-plan-guidelines.md](./references/delivery-plan-guidelines.md) before writing.

Required sections:

```md
# Delivery Plan

## Current Phase
## Stage Objective
## Active Workstreams
## Milestones
## Current Blockers
## Next Verifiable Output
## Next OpenSpec Change
## Decision Log
## Source Links
## Handoff Notes
```

Rules:
- State current phase in one line
- Keep it short enough that a new agent can scan it first and act second
- Must not become roadmap copy or changelog dump
- `Source Links` must point at `ENG.md` whenever it exists. That link is the only route by which a later agent reaches the error map, shadow paths and test matrix — without it those sections are written and never found again.

#### 8b — Create OpenSpec proposals for the active phase

Read [references/openspec-breakdown-guidelines.md](./references/openspec-breakdown-guidelines.md).

Break the implementation sequence into small proposals — one verifiable result per proposal. Map each proposal to one milestone id. The proposals and their milestone ids are where the ordering lives; do not keep a second copy of it in `ENG.md`.

**REQUIRED SUB-SKILL:** Use `openspec` for CLI commands, delta syntax, validation, and archive flow.

#### 8c — Create or update `AGENTS.md` and `CLAUDE.md`

Read [references/agent-context-files.md](./references/agent-context-files.md) first.

`AGENTS.md` must contain:
- required artifacts
- handoff expectations
- planning discipline
- update rules
- project-specific constraints

**`AGENTS.md` is shared. Own your sections, leave the rest alone.** Other skills maintain their own sections in the same file and none of them announce themselves here:

| Section | Owner |
|---|---|
| The five items above | this skill |
| `## Follow-ups` | `software-engineering-guidelines` |
| `## Active Issues` | `i-have-adhd` |
| `## Zeabur 部署規範` | `set-zeabur-conventions` |
| Anything else | the user, or a skill not listed here |

Update your own sections in place. Never delete or rewrite a section you do not own — an unfamiliar section is someone else's working state, not clutter. The "must not become a personal note file" rule below applies to the sections this skill owns, not to the whole file.

`CLAUDE.md` must contain only:

```md
Read `AGENTS.md` before doing any project work. Treat it as the project operating contract.
```

#### Convergence artifact contract

| Artifact | Must contain | Must not become |
|---|---|---|
| `delivery-plan.md` | phase, blockers, next output, next change | roadmap copy or changelog dump |
| OpenSpec proposals | fine-grained changes with one verifiable result each | one giant phase-level proposal |
| `AGENTS.md` | shared operating rules any agent can follow | a personal note file |
| `CLAUDE.md` | pointer to `AGENTS.md` | a second full operating manual |

#### Re-sync cadence

Re-run this step after:
- phase changes
- milestone status changes
- blocker appears or clears
- handoff to another agent

Read [references/handoff-and-feedback-loop.md](./references/handoff-and-feedback-loop.md) for the expected loop.

#### Handoff checklist

Before handing off to another agent:
- [ ] State current phase
- [ ] State blocker or explicitly say none
- [ ] State next verifiable output
- [ ] State next OpenSpec change
- [ ] State decision delta since previous handoff
- [ ] Include source links for critical context
- [ ] Confirm `delivery-plan.md` was updated
- [ ] Confirm `AGENTS.md` is current
- [ ] Confirm `CLAUDE.md` points to `AGENTS.md`

---

## Design mode

### When to use

When the user asks to review UI, check for AI slop, or audit design quality.

### Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
find . -name "*.fig" -o -name "*.sketch" -o -name "DESIGN.md" 2>/dev/null | grep -v node_modules | head -5
[ -f DESIGN-REVIEW.md ] && sed -n '/## Score history/,/^$/p' DESIGN-REVIEW.md
[ -f DESIGN-REVIEW.md ] && sed -n '/## Open slop flags/,/^## /p' DESIGN-REVIEW.md
```

A `DESIGN.md` found here is **input, not output**. It is `design-studio`'s design system file — read it and score against its tokens, never overwrite it. This mode writes `DESIGN-REVIEW.md` instead (Step 4).

If a prior `DESIGN-REVIEW.md` exists, read its score history and open slop flags before scoring. A dimension that scored 4 last time and 4 again means the fix never landed — say so, rather than reporting it as a fresh finding.

### What AI design slop looks like

- generic hero sections with gradient backgrounds and floating 3D icons
- every section a full-width card with shadow on shadow on shadow
- labels like "Submit" instead of the specific action
- empty states that say "No data found" instead of guiding the user forward
- everything the same visual weight
- inconsistent spacing
- modals for things that should be inline
- tables with 8+ equally wide columns

### Step 1 — Rate each dimension

For each of the 10 dimensions, give a score from 0 to 10 and describe what a 10 would look like:

| Dimension | Score | Current state | What 10 looks like here |
|-----------|-------|---------------|-------------------------|
| Hierarchy | ? | [describe] | One unmistakable primary action per screen |
| Whitespace | ? | | Elements breathe; nothing fights for space |
| Typography | ? | | Clear weights; size conveys importance only |
| Color | ? | | Semantic colors; each has a job; AA contrast |
| Consistency | ? | | Same component = same interaction everywhere |
| Copy | ? | | Every label names the action, not the widget |
| Empty states | ? | | Designed as onboarding, not error fallback |
| Error states | ? | | Human language; tells you what to do next |
| Motion | ? | | Purposeful only; explains state change |
| Mobile | ? | | One-thumb usable; touch targets >=44px |

### Step 2 — AI slop scan

Flag any present:
- labels: "Submit", "OK", "Cancel"
- empty states with no CTA or guidance
- errors like "An error occurred" or "Something went wrong"
- spacing off the 4px grid
- cards nested inside cards inside cards
- gradient on gradient color schemes
- no hierarchy
- inline-able flows forced into modals
- tables with more than 6 columns shown by default
- loading states that are only a spinner
- success states that only say "Success!" with no next step

### Step 3 — One question per fix

For any dimension scoring poorly or any slop flag raised, ask one question with options and recommendation. Wait for answer before moving on.

### Step 4 — Update DESIGN-REVIEW.md

Write to project root. **Never write `DESIGN.md`** — that filename belongs to `design-studio`, which keeps the project's long-lived design system there in Google DESIGN.md format. This artifact is a UI audit, not a design system.

`DESIGN-REVIEW.md` is a **state file**: one per project, updated in place, no date or branch in the filename. A UI audit is usually project-wide rather than branch-scoped, so a second dated copy would fragment the history that makes the scores comparable. Prior scores stay in the score history table; git holds the rest.

Update, do not replace:

| Section | On re-review |
|---|---|
| Score history | Append one row. Never rewrite past rows |
| Dimension scores | Overwrite with the current scores |
| Open slop flags | Keep only what is still unresolved. Delete the ones that got fixed |
| Component spec | Accumulate. Existing components stay unless the component itself is gone |

```markdown
# Design Review: [project]
_Last reviewed: [date] - eng-architect design - [branch]_

## Score history
| Date | Hier | White | Type | Color | Consist | Copy | Empty | Error | Motion | Mobile |
|------|------|-------|------|-------|---------|------|-------|-------|--------|--------|
[one row per review, oldest first]

## Dimension scores
| Dimension | Score | Notes |
|-----------|-------|-------|
[table]

## Open slop flags
[unresolved only]

## Component spec

### [Component name]
- **Copy:** [exact labels, error messages, empty states, tooltips]
- **States:** default | hover | active | disabled | loading | error | empty
- **Mobile:** [specific behavior]
- **Touch target:** [size in px]

## Token conformance
| Token | DESIGN.md value | Used as | Verdict |
|-------|-----------------|---------|---------|
[one row per violation only — matches are not worth listing]

## Motion
| Trigger | Animation | Duration | Purpose |
|---------|-----------|----------|---------|
```

**Do not define colors, spacing, or type scales here.** Those live in `DESIGN.md` and belong to `design-studio`. This mode scores the UI *against* them; a second set of tables here means two sources of truth and the UI ends up conforming to neither.

No `DESIGN.md` in the project? Then there is no baseline to score Color, Typography or Consistency against. Say so, score those three dimensions as ungraded rather than inventing a scale, and recommend running `design-studio` first.
