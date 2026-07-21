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
  version: "1.2.0"
---

## Command routing

- 「技術方案」「架構設計」「怎麼切模組」 → **eng mode**
- 「幫我看 UI」「設計有問題嗎」「AI slop」 → **design mode**
- No mode specified → ask which mode

---

## Eng mode

### Preamble

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_DIR=$(python3 "<project-memory skill dir>/scripts/memory.py" projectdir 2>/dev/null)
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
DESIGN=$(ls -t "$_DIR"/*-$_BRANCH-*-plan.md 2>/dev/null | head -1)
[ -z "$DESIGN" ] && DESIGN=$(ls -t "$_DIR"/*-plan.md 2>/dev/null | head -1)
[ -n "$DESIGN" ] && echo "PLAN_DOC: $DESIGN" || echo "PLAN_DOC: none"
[ -f PLAN.md ] && echo "PLAN_FILE: PLAN.md" || echo "PLAN_FILE: none"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
[ -f Cargo.toml ] && echo "STACK:rust"
git log --oneline -15 2>/dev/null
cat TODOS.md 2>/dev/null | head -30
cat ARCHITECTURE.md 2>/dev/null | head -40
```

Read the plan document or `PLAN.md` if they exist. Read all existing architecture docs before designing anything new.

### One question at a time

Same rule as feature-planner: ask one question, wait for answer, record decision, move on. Use multiple choice with recommendation when a decision is needed.

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

### Step 5 — Test matrix

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

Write to project root:

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

## Test matrix
[Table]

## Migration plan
[If applicable]

## Implementation order
1. [First]
2. [Second]
3. [Third]

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

#### 8b — Create OpenSpec proposals for the active phase

Read [references/openspec-breakdown-guidelines.md](./references/openspec-breakdown-guidelines.md).

Break implementation order items into small proposals — one verifiable result per proposal. Map each proposal to one milestone id.

**REQUIRED SUB-SKILL:** Use `openspec` for CLI commands, delta syntax, validation, and archive flow.

#### 8c — Create or update `AGENTS.md` and `CLAUDE.md`

Read [references/agent-context-files.md](./references/agent-context-files.md) first.

`AGENTS.md` must contain:
- required artifacts
- handoff expectations
- planning discipline
- update rules
- project-specific constraints

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
[ -f PLAN.md ] && echo "PLAN_FILE: PLAN.md" || echo "PLAN_FILE: none"
find . -name "*.fig" -o -name "*.sketch" -o -name "DESIGN.md" 2>/dev/null | grep -v node_modules | head -5
```

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

### Step 4 — Write DESIGN.md (or update PLAN.md)

```markdown
# Design: [feature]
_[date] - eng-architect design - [branch]_

## Dimension scores
| Dimension | Score | Notes |
|-----------|-------|-------|
[table]

## Slop flags resolved
[list]

## Component spec

### [Component name]
- **Copy:** [exact labels, error messages, empty states, tooltips]
- **States:** default | hover | active | disabled | loading | error | empty
- **Mobile:** [specific behavior]
- **Touch target:** [size in px]

## Color tokens
| Token | Hex | Usage |
|-------|-----|-------|
| --color-primary | #... | Primary actions only |
| --color-danger | #... | Destructive actions, error states |
| --color-surface | #... | Card backgrounds |
| --color-border | #... | Dividers, input borders |

## Spacing scale
4px base grid: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64

## Typography scale
| Role | Size | Weight | Usage |
|------|------|--------|-------|
| Heading | 24px | 600 | Page titles |
| Body | 16px | 400 | Content |
| Label | 14px | 500 | Form labels, nav |
| Caption | 12px | 400 | Timestamps, metadata |

## Motion
| Trigger | Animation | Duration | Purpose |
|---------|-----------|----------|---------|
```

---

## Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"eng-architect\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
