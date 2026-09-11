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
   - **DELETED**: manifest entry has no matching wiki page → pending reconciliation; preserve the StudyVault note and progress until the approved handling is completed

The script at `scripts/sha256_wiki.py` handles frontmatter extraction automatically.
For the initial sync (no manifest yet), compute sha256 for all wiki pages and write
the full manifest.

### Reconcile source changes before modifying existing notes

Read each affected StudyVault note and its progress records. A manifest entry
identifies a generated file but does not prove it contains no user edits.
For changed pages, preserve handwritten additions and learning history while
updating source-derived content. If those parts cannot be distinguished, stop
that overwrite and present the concrete conflict.

For missing, renamed or split sources, report old/new source paths, matched
StudyVault notes, affected links and progress, and the proposed action. Reuse
existing authorization for that exact action; otherwise obtain confirmation
before moving, archiving or deleting existing work. Keep unresolved notes and
manifest mappings intact, report them as pending, and continue independent safe
imports. Write successful manifest updates only after the corresponding note
changes are verified. Never alter the source wiki during synchronization.

### Phase W4: Concept Grouping

Wiki already has topic-based structure. Use it directly:

1. Read wiki's `topics/` directory — each subdirectory is a research topic.
2. Read each topic's `index.md` to understand its scope.
3. Map wiki topics to StudyVault folders (`topics/ai-safety/` → `01-AI-Safety/`, etc.).
4. Global `concepts/` and `entities/` (cross-topic pages) → map to a "Cross-Topic" StudyVault folder or distribute to relevant topic folders based on tags.
5. User can override mapping via manifest `grouping.tag_to_folder` config.

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

- Generate practice per learning topic, covering its concept notes, following [Learning Depth and Practice](learning-quality.md). Use the shared default count and recall/application/analysis criteria.
- Apply zero-hint policy from the `tutor` skill's `references/quiz-rules.md`
- High-risk content (`contested: true`, `confidence: low`) → prioritize analysis questions

### Phase W6: Dashboard Update + Manifest Write

1. **Dashboard**: Recalculate proficiency table from `concepts/{area}.md`.
   - New topics default to ⬜ (unmeasured).
   - Existing topics retain their progress.
   - Update MOC Topic Map to link all concept notes.
2. **Sync manifest**: Write/update `StudyVault/.sync-manifest.json` with:
   - All wiki page paths + sha256 + vault_path + synced_at timestamp
3. **Report**: List additions, updates, confirmed moves or removals, and unresolved source changes. Do not mark pending actions as synchronized.

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
| Wiki page renamed                         | Compare content, links and manifest history to identify the existing note. Propose the exact mapping, preserve progress, and update paths only after the handling is confirmed; tags alone do not prove identity. |
| Wiki page split                           | Reported as orphaned during sync. User decides how to regroup.                                                   |
| User adds manual notes in StudyVault      | Not tracked by manifest. Sync will not touch them.                                                               |
| Wiki and StudyVault on different machines | Not supported. Wiki path must be accessible from the same environment.                                           |
| Wiki page exceeds 200 lines               | Assess distinct ideas and learning structure. Length alone neither blocks import nor requires splitting; preserve a coherent long explanation when useful.                            |

