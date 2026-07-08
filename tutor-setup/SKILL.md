---
name: tutor-setup
description: >
  Transforms knowledge sources into an Obsidian StudyVault. Three modes:
  (1) Document Mode — PDF/text/web sources → study notes with practice questions.
  (2) Codebase Mode — source code project → onboarding vault for new developers.
  (3) Wiki Mode — llm-wiki knowledge base → StudyVault with incremental sync.
  Mode is auto-detected based on project markers and wiki presence.
---

# Tutor Setup — Knowledge to Obsidian StudyVault

## CWD Boundary Rule (ALL MODES)

> **NEVER access files outside the current working directory (CWD).**
> All source scanning, reading, and vault output MUST stay within CWD and its subdirectories.
> If the user provides an external path, ask them to copy the files into CWD first.

## Mode Detection

On invocation, detect mode automatically:

1. **Check for wiki indicators** in CWD:
   - `SCHEMA.md` + `index.md` present (llm-wiki structure)
   - `raw/` directory with `articles/` or `papers/` subdirectories
   - If found → **Wiki Mode** (confirm with user)
2. **Check for project markers** in CWD:
   - `package.json`, `pom.xml`, `build.gradle`, `Cargo.toml`, `go.mod`, `Makefile`,
     `*.sln`, `pyproject.toml`, `setup.py`, `Gemfile`
3. **If any marker found** → **Codebase Mode**
4. **If no marker found** → **Document Mode**
5. **Tie-break**: If `.git/` is the sole indicator and no source code files (`*.ts`, `*.py`, `*.java`, `*.go`, `*.rs`, etc.) exist, default to Document Mode.
6. Announce detected mode and ask user to confirm or override.

---

## Document Mode

> Transforms knowledge sources (PDF, text, web, epub) into study notes.
> Templates: [templates.md](references/templates.md)

### Phase D1: Source Discovery & Extraction

1. **Auto-scan CWD** for `**/*.pdf`, `**/*.txt`, `**/*.md`, `**/*.html`, `**/*.epub` (exclude `node_modules/`, `.git/`, `dist/`, `build/`, `StudyVault/`). Present for user confirmation.
2. **Extract text (MANDATORY tools)**:
   - **PDF → `pdftotext` CLI ONLY** (run via Bash tool). NEVER use the Read tool directly on PDF files — it renders pages as images and wastes 10-50x more tokens. Convert to `.txt` first, then Read the `.txt` file.
     ```bash
     pdftotext "source.pdf" "/tmp/source.txt"
     ```
   - If `pdftotext` is not installed, install it first: `brew install poppler` (macOS) or `apt-get install poppler-utils` (Linux).
   - URL → WebFetch
   - Other formats (`.md`, `.txt`, `.html`) → Read directly.
3. **Read extracted `.txt` files** — understand scope, structure, depth. Work exclusively from the converted text, never from the raw PDF.
4. **Source Content Mapping (MANDATORY for multi-file sources)**:
   - Read **cover page + TOC + 3+ sample pages from middle/end** for EVERY source file
   - **NEVER assume content from filename** — file numbering often ≠ chapter numbering
   - Build verified mapping: `{ source_file → actual_topics → page_ranges }`
   - Flag non-academic files and missing sources
   - Present mapping to user for verification before proceeding

### Phase D2: Content Analysis

1. Identify topic hierarchy — sections, chapters, domain divisions.
2. Separate concept content vs practice questions.
3. Map dependencies between topics.
4. Identify key patterns — comparisons, decision trees, formulas.
5. **Full topic checklist (MANDATORY)** — every topic/subtopic listed. Drives all subsequent phases.

> **Equal Depth Rule**: Even a briefly mentioned subtopic MUST get a full dedicated note supplemented with textbook-level knowledge.

6. **Classification completeness**: When source enumerates categories ("3 types of X"), every member gets a dedicated note. Scan for: "types of", "幾種", "幾類", "categories", "there are N".
7. **Source-to-note cross-verification (MANDATORY)**: Record which source file(s) and page range(s) cover each topic. Flag untraceable topics as "source not available".

### Phase D3: Tag Standard

Define tag vocabulary before creating notes:

- **Format**: English, lowercase, kebab-case (e.g., `#data-hazard`)
- **Hierarchy**: top-level → domain → detail → technique → note-type
- **Registry**: Only registered tags allowed. Detail tags co-attach parent domain tag.

### Phase D4: Vault Structure

Create `StudyVault/` with numbered folders per [templates.md](references/templates.md). Group 3-5 related concepts per file.

### Phase D5: Dashboard Creation

Create `00-Dashboard/`: MOC, Quick Reference, Exam Traps. See [templates.md](references/templates.md).

- **MOC**: Topic Map + Practice Notes + Study Tools + Tag Index (with rules) + Weak Areas (with links) + Non-core Topic Policy
- **Quick Reference**: every heading includes `→ [[Concept Note]]` link; all key formulas
- **Exam Traps**: per-topic trap points in fold callouts, linked to concept notes

### Phase D6: Concept Notes

Per [templates.md](references/templates.md). Key rules:

- YAML frontmatter: `source_pdf`, `part`, `keywords` (MANDATORY)
- **source_pdf MUST match verified Phase D1 mapping** — never guess from filename
- If unavailable: `source_pdf: 未持有原文`
- `[[wiki-links]]`, callouts (`[!tip]`, `[!important]`, `[!warning]`), comparison tables > prose
- ASCII diagrams for processes/flows/sequences
- **Simplification-with-exceptions**: general statements must note edge cases

### Phase D7: Practice Questions

Per [templates.md](references/templates.md). Key rules:

- Every topic folder MUST have a practice file (8+ questions)
- **Active recall**: answers use `> [!answer]- 查看答案` fold callout
- Patterns use `> [!hint]-` / `> [!summary]-` fold callouts
- **Question type diversity**: ≥60% recall, ≥20% application, ≥2 analysis per file
- `## Related Concepts` with `[[wiki-links]]`

### Phase D8: Interlinking

1. `## Related Notes` on every concept note
2. MOC links to every concept + practice note
3. Cross-link concept ↔ practice; siblings reference each other
4. Quick Reference sections → `[[Concept Note]]` links
5. Weak Areas → relevant note + Exam Traps; Exam Traps → concept notes

### Phase D9: Self-Review (MANDATORY)

Verify against [quality-checklist.md](references/quality-checklist.md) **Document Mode** section. Fix and re-verify until all checks pass.

---

## Codebase Mode

> Generates a new-developer onboarding StudyVault from a source code project.
> Full workflow: [codebase-workflow.md](references/codebase-workflow.md)
> Templates: [codebase-templates.md](references/codebase-templates.md)

### Phase Summary

| Phase | Name                  | Key Action                                                                                       |
| ----- | --------------------- | ------------------------------------------------------------------------------------------------ |
| C1    | Project Exploration   | Scan files, detect tech stack, read entry points, map directory layout                           |
| C2    | Architecture Analysis | Identify patterns, trace request flow, map module boundaries and data flow                       |
| C3    | Tag Standard          | Define `#arch-*`, `#module-*`, `#pattern-*`, `#api-*` tag registry                               |
| C4    | Vault Structure       | Create `StudyVault/` with Dashboard, Architecture, per-module, DevOps, Exercises folders         |
| C5    | Dashboard             | MOC (Module Map + API Surface + Getting Started + Onboarding Path) + Quick Reference             |
| C6    | Module Notes          | Per-module notes: Purpose, Key Files, Public Interface, Internal Flow, Dependencies              |
| C7    | Onboarding Exercises  | Code reading, configuration, debugging, extension exercises (5+ per major module)                |
| C8    | Interlinking          | Cross-link modules, architecture ↔ implementations, exercises ↔ modules                          |
| C9    | Self-Review           | Verify against [quality-checklist.md](references/quality-checklist.md) **Codebase Mode** section |

See [codebase-workflow.md](references/codebase-workflow.md) for detailed per-phase instructions.

---

## Wiki Mode

> Imports an llm-wiki knowledge base into a StudyVault for learning and progress tracking.
> Wiki pages become concept notes; practice questions are auto-generated from wiki content.
> Supports incremental sync — new/changed wiki pages are detected and synced without
> regenerating the entire StudyVault.

**Note:** Wiki Mode reads from a user-specified wiki path, which may be outside CWD.
This is the only mode that does not enforce the CWD Boundary Rule for source reads.
StudyVault output still goes into CWD.

### Phase W1: Locate Wiki

1. **User specifies wiki path** → use it.
2. **No path given** → scan CWD for wiki indicators (`SCHEMA.md` + `index.md`).
   - If found in CWD → confirm with user.
   - If not found → ask user for the wiki path.
3. **Verify wiki structure**: check for `SCHEMA.md`, `index.md`, `concepts/` directory.
   If incomplete, warn the user and ask whether to proceed.

### Phase W2: Orient (MANDATORY)

Read the wiki before any operation:

① Read `SCHEMA.md` — understand domain, tag taxonomy, conventions.
② Read `index.md` — learn what pages exist.
③ Read last 20 entries of `log.md` — recent activity.

Only after orientation should you sync or create StudyVault content.

### Phase W3: Diff Detection

Check for existing sync state:

1. Look for `StudyVault/.sync-manifest.json`.
2. **If not found** → first-time sync (full import).
3. **If found** → read manifest, compute sha256 for each wiki page, compare:

```bash
# Single file sha256 (body only, frontmatter excluded)
python scripts/sha256_wiki.py "<wiki>/concepts/transformer.md"

# Batch — all .md files under wiki, outputs JSON
python scripts/sha256_wiki.py "<wiki>/concepts/"
```

4. Compare results with manifest:
   - **NEW**: wiki page not in manifest → needs import
   - **CHANGED**: sha256 differs → needs re-import (preserve learning progress)
   - **DELETED**: manifest entry has no matching wiki page → remove from StudyVault, archive learning progress

The script at `scripts/sha256_wiki.py` handles frontmatter extraction automatically.
For the initial sync (no manifest yet), compute sha256 for all wiki pages and write
the full manifest.

### Phase W4: Concept Grouping

Wiki concept pages are flat; StudyVault needs area-based grouping:

1. Read each wiki concept page's `tags` frontmatter.
2. Group by top-level domain tag (e.g., `model`, `training`, `optimization` → separate areas).
3. Map groups to StudyVault folder structure (`01-AI/`, `02-Marketing/`, etc.).
4. User can override grouping via manifest config.

### Phase W5: Transform & Generate

For each new or changed wiki page:

**Wiki page → StudyVault concept note mapping:**

| Wiki field                             | StudyVault field               |
| -------------------------------------- | ------------------------------ |
| `title`                                | Note title                     |
| `tags`                                 | `#tag` markers                 |
| `sources`                              | `source_pdf` frontmatter       |
| `confidence` / `contested`             | Flag as Exam Trap candidates   |
| Content (definition, state, questions) | Overview Table + Exam Patterns |
| `[[wikilinks]]`                        | `[[wiki-links]]` preserved     |

**Practice question generation:**

- Generate ≥8 questions per concept note
- Mix: ≥60% recall, ≥20% application, ≥2% analysis
- Apply zero-hint policy from `references/quiz-rules.md`
- High-risk content (`contested: true`, `confidence: low`) → prioritize analysis questions

### Phase W6: Dashboard Update + Manifest Write

1. **Dashboard**: Recalculate proficiency table from `concepts/{area}.md`.
   - New topics default to ⬜ (unmeasured).
   - Existing topics retain their progress.
   - Update MOC Topic Map to link all concept notes.
2. **Sync manifest**: Write/update `StudyVault/.sync-manifest.json` with:
   - All wiki page paths + sha256 + vault_path + synced_at timestamp
3. **Report**: List what was added, updated, and removed.

### Incremental Sync

When the user has new research to add:

1. New sources → ingest into wiki (via llm-wiki skill).
2. Run Wiki Mode again → diff detection finds new/changed pages → sync only those.
3. StudyVault expands automatically; dashboard updates; learning progress preserved.

### Sync Manifest Format

```json
{
  "version": 1,
  "wiki_path": "/path/to/wiki",
  "last_sync": "2026-07-09T10:00:00Z",
  "pages": {
    "concepts/transformer-architecture.md": {
      "sha256": "abc123...",
      "vault_path": "01-AI/transformer-architecture.md",
      "synced_at": "2026-07-09T10:00:00Z"
    }
  }
}
```

### Edge Cases

| Scenario                                  | Handling                                                                                                         |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Wiki page renamed                         | Manifest path mismatch → delete old + create new. Learning progress archived, auto-linked by tags when possible. |
| Wiki page split                           | Reported as orphaned during sync. User decides how to regroup.                                                   |
| User adds manual notes in StudyVault      | Not tracked by manifest. Sync will not touch them.                                                               |
| Wiki and StudyVault on different machines | Not supported. Wiki path must be accessible from the same environment.                                           |
| Wiki page exceeds 200 lines               | Wiki should split first (llm-wiki lint catches this). StudyVault does not re-process.                            |

---

## Language

- Match source material language (Korean → Korean notes, etc.)
- **Tags/keywords**: ALWAYS English
