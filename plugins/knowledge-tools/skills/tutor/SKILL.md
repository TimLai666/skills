---
name: tutor
description: |
  Interactive quiz tutor for Obsidian StudyVault learning. This skill MUST be used when the user wants to: (1) Take a diagnostic assessment of their knowledge, (2) Study or review specific sections/topics, (3) Drill weak areas identified in previous sessions, (4) Check their learning progress or dashboard, or says things like "quiz me", "test me", "let's study", "/tutor", "學習", "測驗", "評量".
metadata:
  version: "1.2.0"
---

# Tutor Skill

Quiz-based tutor that tracks what the user knows and doesn't know at the **concept level**. The goal is helping users discover their blind spots through questions.

## File Structure

```
StudyVault/
├── *dashboard*              ← Compact overview: proficiency table + stats
└── concepts/
    ├── {area-name}.md       ← Per-area concept tracking (attempts, status, error notes)
    └── ...
```

- **Dashboard**: Only aggregated numbers. Links to concept files. Stays small forever.
- **Concept files**: One per area. Tracks each concept with attempts, correct count, date, status, and error notes. Grows proportionally to unique concepts tested (bounded).

## Workflow

### Phase 0: Detect Language

Detect user's language from their message → `{LANG}`. All output and file content in `{LANG}`.

### Phase 1: Discover Vault

1. Glob `**/StudyVault/` in project
2. List section directories
3. Glob `**/StudyVault/*dashboard*` to find dashboard
4. If found, read it. Preserve existing file path regardless of language.
5. If not found, read [Tracking Templates](references/tracking-templates.md) and create from the dashboard template

If no StudyVault exists, inform user and stop.

### Phase 2: Determine Session Type

Use the scope and session type already specified by the user. For example,
“quiz me on chapter 3” goes directly to that chapter; do not ask the user to
choose it again. If the request is only to view progress, report the dashboard
and relevant concept records without starting a quiz.

When the goal is unclear, read the dashboard and offer relevant choices:
- Unmeasured areas (⬜): diagnostic assessment.
- Weak areas (🟥/🟨): drill the weakest named areas.
- A section chosen by the user.
- All areas 🟩/🟦: hard-mode review.

Ask concisely using an available suitable input tool or plain text, then wait
for the user's choice before selecting the quiz scope.

### Phase 3: Build Questions

1. Read markdown files in the target sections.
2. For weak-area drills, read `concepts/{area}.md` for unresolved concepts.
3. Before crafting any question, read [Quiz Design Rules](references/quiz-rules.md) in full. Follow its zero-hint policy, question design and new-context drill rules.

### Phase 4: Present Quiz

Follow [Quiz Presentation](references/quiz-rules.md#quiz-presentation): four
questions per round, four options per question, one answer each. Adapt the
presentation to the available tool without changing those quiz requirements.

### Phase 5: Grade & Explain

1. Show results table (question / correct answer / user answer / result)
2. Wrong answers: concise explanation
3. Map each question to its area

### Phase 6: Update Files

#### 1. Update concept file (`concepts/{area}.md`)

Before first creating a concept file, read [Tracking Templates](references/tracking-templates.md). For each question answered:
- **New concept**: Add row to table + if wrong, add error note under `### 錯題筆記` (or localized equivalent)
- **Existing 🔴 concept answered correctly**: Increment attempts & correct, change status to 🟢, keep error note (learning history)
- **Existing 🟢 concept answered wrong again**: Increment attempts, change status back to 🔴, update error note

Table format:
```markdown
| Concept | Attempts | Correct | Last Tested | Status |
|---------|----------|---------|-------------|--------|
| concept name | 2 | 1 | 2026-02-24 | 🔴 |
```

Error notes format (only for wrong answers):
```markdown
### Error Notes

**concept name**
- Confusion: what the user mixed up
- Key point: the correct understanding
```

#### 2. Update dashboard

- Recalculate per-area stats from concept files (sum attempts/correct across all concepts in that area)
- Update proficiency badges: 🟥 0-39% · 🟨 40-69% · 🟩 70-89% · 🟦 90-100% · ⬜ no data
- Update stats: total questions, cumulative rate, unresolved/resolved counts, weakest/strongest

Dashboard stays compact — no session logs, no per-question details.
