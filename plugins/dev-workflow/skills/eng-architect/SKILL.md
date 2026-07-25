---
name: eng-architect
description: "Design architecture, then cut the work into tickets. This skill MUST be used before implementation of a non-trivial feature begins, and MUST be used when a plan or spec has to become tickets. SHOULD be used whenever the user is unsure how to split modules. Tickets MUST be cut by what someone can do and MUST NOT be one per technical layer, so this skill MUST NOT be replaced by an ad hoc task list. Produces architecture diagrams, error maps, tickets with blocking edges, and convergence artifacts (ENG.md, delivery-status.md, AGENTS.md). Triggers on: 技術方案, 架構設計, 怎麼切模組, 拆任務, 切票, 拆成 ticket, 排開發順序, eng planning, architecture design, break into tickets, 技術規劃, 這個功能技術上怎麼做, design review, UI review, AI slop scan"
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
  version: "1.10.0"
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
  ! -name 'delivery-plan.md' \
  -not -path '*/.git/*' -not -path '*/node_modules/*' -exec ls -t {} + 2>/dev/null | head -1)
[ -n "$DESIGN" ] && echo "PLAN_DOC: $DESIGN" || echo "PLAN_DOC: none"
_R="${_ROOT:-.}"
[ -f "$_R/delivery-plan.md" ] && echo "LEGACY_STATUS_FILE: delivery-plan.md"
[ -f "$_R/ENG.md" ] && echo "ENG_MD: exists" || echo "ENG_MD: none"
[ -d "$_R/openspec" ] && echo "OPENSPEC_DIR: exists" || echo "OPENSPEC_DIR: none"
command -v openspec >/dev/null 2>&1 && echo "OPENSPEC_CLI: yes" || echo "OPENSPEC_CLI: no"
[ -f "$_R/Gemfile" ] && echo "STACK:ruby"
[ -f "$_R/package.json" ] && echo "STACK:node"
{ [ -f "$_R/requirements.txt" ] || [ -f "$_R/pyproject.toml" ]; } && echo "STACK:python"
[ -f "$_R/go.mod" ] && echo "STACK:go"
[ -f "$_R/Cargo.toml" ] && echo "STACK:rust"
git log --oneline -15 2>/dev/null
head -40 "$_R/ARCHITECTURE.md" 2>/dev/null
```

Every check is anchored to the repo root, not the current directory. Started from a subdirectory, an unanchored `[ -f ENG.md ]` reports `none` while Step 4 still writes to the root — the run would overwrite the previous `ENG.md` blind instead of updating it.

Read the plan document if it exists. Read all existing architecture docs before designing anything new. If `ENG_MD: exists`, read `ENG.md` too — this run updates it rather than replacing it (Step 4).

`ARCHITECTURE.md` is a convention some projects happen to carry; read it when present. Nothing in this toolchain writes it, so its absence means nothing.

`plan-grilling` defaults to `docs/plans/` but writes wherever the user asked it to, which is why the last glob sweeps the whole repo. It matches on the `*-plan.md` filename, not the directory.

The sweep excludes `delivery-plan.md`, which is what this skill's status file used to be called. The name was wrong twice over: it ends in `-plan.md`, so the sweep would pick up the status file and read a status report as the feature list, and "plan" invites exactly the roadmap content the file is forbidden to hold. It is `delivery-status.md` now. On `LEGACY_STATUS_FILE`, tell the user and `git mv` it before Step 5a writes anything, or the run leaves two status files disagreeing.

**Stack.** The `STACK:` lines answer this for an existing repo — take them and do not ask. Only when nothing is detected, which means a project with no code yet, ask the user once for the language, framework, database and deployment target, with a recommendation. Their answer constrains every flow drawn in Step 1, so it cannot wait until something needs it.

Step 5b writes tickets, and where they land is decided here rather than five steps later. `OPENSPEC_DIR: exists` plus `OPENSPEC_CLI: yes` means the project already runs OpenSpec — confirm once that tickets should be changes, then stop asking. Anything else means plain markdown under `docs/tickets/`; do not talk the user into installing OpenSpec to get tickets.

### One question at a time

Same rule as `plan-grilling`: ask one question, wait for answer, record decision, move on. Use multiple choice with recommendation when a decision is needed.

### Step 1 — Per-feature pass

Take the feature list from the plan document — the scope items, each already phrased as something a person can do. Work them one at a time, in the order the plan gives, and finish one before opening the next. The whole-system picture is Step 2; it is assembled from what these passes decide, not drawn ahead of them.

No plan document, or a list still written by module? Fix that first — turn it into a feature list and confirm it, otherwise every pass below inherits the technical axis and the tickets come out layered.

For each feature, run 1a through 1e, then move to the next feature.

#### 1a — How this feature flows

Entry point, what it touches, where it stores, what states it moves through.

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

Show it and ask the user to confirm or adjust before going further into this feature. Record the decision.

#### 1b — Error/rescue map (mandatory)

For every operation in this feature that can fail:

| Operation | Exception/Error | Who catches it | What user sees | Tested? |
|-----------|-----------------|----------------|----------------|---------|
| Stripe charge | `Stripe::CardError` | PaymentService | "Card declined" + retry | Plan: yes |
| DB write | Connection timeout | ActiveRecord | 500 + alert | Plan: yes |
| Email send | SMTP failure | EmailWorker | Silent retry x3 | Plan: yes |

Anti-pattern: `rescue StandardError` or `catch Exception` is a code smell. Call it out.

#### 1c — Shadow paths

For each data flow in this feature, trace all four paths:
- happy path
- nil/null/undefined input
- empty/zero/blank input
- upstream error

For each shadow path: does the plan handle it? If not, flag it.

#### 1d — Interaction edge cases

| Interaction | Edge case | Expected behavior | Covered? |
|-------------|-----------|-------------------|----------|
| Form submit | Double-click | Debounce / idempotency key | ? |
| Long operation | User navigates away | Background job continues | ? |
| Any form | Session expires mid-fill | Graceful redirect, data preserved | ? |
| List view | 0 results | Empty state with CTA | ? |
| List view | 10,000+ results | Pagination enforced | ? |

Flag any `?` as a gap.

#### 1e — How this feature gets tested

A seam is a place where behavior can be swapped without editing the code under test — where the fakes get injected. Decide where this feature is tested before deciding what kinds of tests to write.

- Prefer existing seams to new ones, including one an earlier feature already chose. A seam that exists only to make testing possible is an architecture change, not a test decision.
- Take the highest seam that still reaches the behavior. High seams survive internal refactors; low seams go red when a private method moves.
- If a new seam is needed, propose it at the highest point possible.

Example — "place order, then send confirmation email":

| Seam | What gets faked | Cost |
|------|-----------------|------|
| `POST /orders` | Email sender | Survives every refactor below the controller |
| `OrderService.create` | Email sender, order repo | Breaks when the service interface moves |
| One spec per collaborator | Validator, pricing, template, SMTP | Four sets of fakes, all red on any internal rename |

Ask the user to confirm this feature's seam before moving to the next feature. Record the decision, and mark it provisional — Step 2b compares it against every other feature's choice and may collapse several into one.

#### Where the 1b-1d tables go

They are per-path analysis, not project state. Each row gets exactly one owning ticket in Step 5b, where it becomes that ticket's acceptance criteria. Until then they are working notes — do not park a second copy in `ENG.md`, because a copy there and a copy on the tickets drift apart within one iteration.

---

### Step 2 — Consolidate

Runs once, after every feature has been through Step 1.

#### 2a — Architecture diagram

Assemble the per-feature flows into one picture: entry points, data flow, state transitions, service boundaries, trust boundaries, storage.

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

Ask the user to confirm or adjust. Record the decision.

This is where features that quietly disagree surface — two of them assuming different boundaries, different storage, or incompatible state names. Say which two, say what each assumed, and go back to the feature that has to give way. A confirmation that never sends anything back is theatre; the diagram earns its place by catching exactly this.

#### 2b — Collapse the seams

Put every provisional seam from 1e side by side. Fewer seams is better, one is ideal — every extra seam is another set of fakes that can drift from the real thing.

Where several features can share one higher seam, propose the collapse and say which per-feature answers it overrides. Only ask again where collapsing contradicts something the user already chose; a seam that survives untouched needs no second confirmation.

#### 2c — Fill the test matrix

Two rules before writing a single row:

- Test external behavior only. A test that breaks when internals are rewritten but behavior is unchanged is testing the wrong thing.
- Find prior art. Locate existing tests of the same shape in the codebase and follow their structure instead of inventing a new one.

| Test type | What to cover | Priority |
|-----------|---------------|----------|
| Unit | Core business logic, every branch | P0 |
| Integration | DB/API contracts, error paths | P0 |
| E2E | Happy path + top 3 error paths | P1 |
| Load | Estimated peak x3 | P2 if prod |

### Step 3 — Migration and deployment plan

If the change touches the DB:

```bash
ls db/migrate/ 2>/dev/null | tail -5
ls migrations/ 2>/dev/null | tail -5
```

For each migration: reversible? locks tables? needs backfill? can run while old code is live?

### Step 4 — Write ENG.md

Write to project root. `ENG.md` is a **state file**: one per project, updated in place. Never date-stamp or branch-stamp the filename — git already provides version history and branch isolation, and a second copy would leave re-sync with no single target to read.

**It holds only what is true across tickets.** Anything scoped to one path — the error map, shadow paths, interaction edge cases, per-ticket definition of done — belongs on the ticket that owns it (Step 5b), not here. What stays is the set of decisions a second run must not re-make from scratch: the architecture, the seam strategy, the standing assumptions, the migration sequence. Without them the same project gets a different seam every iteration, which is exactly what Step 2b exists to prevent.

**Who reads it.** The next `eng-architect` run, and any agent that arrives through `AGENTS.md` before touching architecture, seams or migrations. Step 5c is what puts it on that path — an `ENG.md` nobody registered is a file only its author will ever open.

**Read before writing.** If `ENG_MD: exists`, read it first and update the sections that changed. Do not regenerate from scratch — a re-sync that rewrites blind loses the prior run's seam decisions.

```markdown
# Engineering Plan: [project]
_[date] - eng-architect - [repo]:[branch]_

## Architecture
[ASCII diagram]

## Data flow
[Main flows, happy path]

## Test seams
[Chosen seam per flow, what gets faked, why this level]

## Test matrix
[Table]

## Migration plan
[If applicable]

## Hidden assumptions
- [assumption] - risk: [consequence]
```

The title names the project, not the feature. One file serves every feature in the repo, so a feature name in the heading goes stale the moment the next run touches it.

### Step 5 — Convergence artifacts (mandatory)

This step runs every time eng completes.

Check for existing artifacts:

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
[ -f "$_ROOT/delivery-status.md" ] && echo "DELIVERY_PLAN: exists" || echo "DELIVERY_PLAN: missing"
[ -f "$_ROOT/AGENTS.md" ] && echo "AGENTS_MD: exists" || echo "AGENTS_MD: missing"
[ -f "$_ROOT/CLAUDE.md" ] && echo "CLAUDE_MD: exists" || echo "CLAUDE_MD: missing"
head -40 "$_ROOT/delivery-status.md" 2>/dev/null
head -20 "$_ROOT/AGENTS.md" 2>/dev/null
```

All three live at the repo root, alongside `ENG.md`. Anchor the check to the root rather than the current directory — a run started from a subdirectory would otherwise report `missing` and create a second copy.

#### 5a — Create or update `delivery-status.md`

Read [references/delivery-status-guidelines.md](./references/delivery-status-guidelines.md) before writing.

Required sections:

```md
# Delivery Status

## Current Phase
## Stage Objective
## Active Workstreams
## Milestones
## Current Blockers
## Next Verifiable Output
## Next Ticket
## Decision Log
## Source Links
## Handoff Notes
```

Rules:
- State current phase in one line
- Keep it short enough that a new agent can scan it first and act second
- Must not become roadmap copy or changelog dump
- `Source Links` must point at `ENG.md` whenever it exists. It is how a later agent reaches the seam strategy, the test matrix and the standing assumptions before changing any of them.
- In OpenSpec mode, `Milestones` is also where the blocking edges live — OpenSpec has no dependency relationship between changes, so the milestone order is the sequence.

#### 5b — Cut the work into tickets

Read [references/ticket-breakdown-guidelines.md](./references/ticket-breakdown-guidelines.md) before slicing anything.

Cut by what someone can do, not by which layer the code sits in. Each ticket is one narrow path through every layer it needs, verifiable on its own, labelled with its Epic and User Story, and declaring the tickets that block it. Shared foundations collapse into one ticket the others depend on; a wide refactor goes expand → migrate in batches → contract. Then run the coverage check: every row from the per-feature pass (1b-1d) gets exactly one owning ticket, and every story has at least one ticket.

**Confirm the set before writing any of it.** Show the proposal as a numbered list — title, blocked by, what it delivers — and ask three things, one at a time: is the granularity right, is every blocking edge a real gate rather than a preferred order, and should anything be merged or split further. Iterate until the user approves. A ticket set is cheap to redraw now and expensive to redraw once half of it is built.

Tickets land where the Preamble established:

- **Plain markdown** — one file per ticket under `docs/tickets/`, numbered in dependency order. Point `dev-task-loop` at that directory when it asks where the backlog lives.
- **OpenSpec** — one ticket is one change, never one task. Map each change to one milestone id in `delivery-status.md`; that milestone order carries the blocking edges, because OpenSpec has none between changes. Use the `openspec` skill for CLI commands, delta syntax, validation and archive flow if it is installed; if it is not, say so and fall back to plain markdown rather than hand-rolling the directory layout.

Either way the ordering lives on the tickets, not in `ENG.md`.

#### 5c — Create or update `AGENTS.md` and `CLAUDE.md`

Read [references/agent-context-files.md](./references/agent-context-files.md) first.

`AGENTS.md` must contain:
- required artifacts — name each one and say when to read it, not just that it exists
- handoff expectations
- planning discipline
- update rules
- project-specific constraints

The artifact registry is what gives `ENG.md` a reader. `CLAUDE.md` sends every agent to `AGENTS.md`, so an artifact named there is on a path someone walks; an artifact named nowhere is a file only its author opens. Register all three:

```md
## Required artifacts
- `ENG.md` — architecture, test seam strategy, standing assumptions, migration sequence.
  Read it before changing architecture, picking a test seam, or writing a migration.
- `delivery-status.md` — current phase, blockers, next verifiable output, next ticket.
  Read it first on arrival; it says where the project is.
- `docs/tickets/` (or `openspec/changes/`) — the tickets and their blocking edges.
  Pick up anything whose blockers are all done.
```

**`AGENTS.md` is shared. Own your sections, leave the rest alone.** Other skills maintain their own sections in the same file and none of them announce themselves here:

| Section | Owner |
|---|---|
| The five items above | this skill |
| `## Follow-ups` | `software-engineering-guidelines` |
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
| `delivery-status.md` | phase, blockers, next output, next ticket | roadmap copy or changelog dump |
| Tickets | one user-visible slice each, with its blocking edges | one ticket per layer, or one per phase |
| `ENG.md` | what holds across tickets: architecture, seams, assumptions, migration order | a second copy of anything that lives on a ticket |
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
- [ ] State next ticket
- [ ] State decision delta since previous handoff
- [ ] Include source links for critical context
- [ ] Confirm `delivery-status.md` was updated
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
