# Design review workflow

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
- spacing off the 4px grid, or inconsistent between similar elements
- generic hero sections with gradient backgrounds and floating 3D icons
- every section a full-width card, shadow stacked on shadow
- cards nested inside cards inside cards
- gradient on gradient color schemes
- no hierarchy
- inline-able flows forced into modals
- tables with more than 6 columns shown by default
- loading states that are only a spinner
- success states that only say "Success!" with no next step

### Step 3 — Present findings and decisions

Present the findings and recommended fixes together. Apply the shared decision rules: ask about unresolved tradeoffs or changes to an agreed direction, and group related choices. A review request produces recommendations; execute fixes only within the user's authorized scope.

### Step 4 — Update DESIGN-REVIEW.md

Use the existing project review record. When a persistent review is requested and no arrangement exists, write `DESIGN-REVIEW.md` to the project root; otherwise deliver the review directly. The filename below refers to the chosen review record. **Never write `DESIGN.md`** — that filename belongs to `design-studio`, which keeps the project's long-lived design system there in Google DESIGN.md format. This artifact is a UI audit, not a design system.

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
