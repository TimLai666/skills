## Document Mode

> Transforms knowledge sources (PDF, text, web, epub) into study notes.
> Templates: [templates.md](templates.md)

### Phase D1: Source Discovery & Extraction

1. **Auto-scan CWD** for `**/*.pdf`, `**/*.txt`, `**/*.md`, `**/*.html`, `**/*.epub` (exclude `node_modules/`, `.git/`, `dist/`, `build/`, `StudyVault/`). Present for user confirmation.
2. **Extract source content with tools suited to the format**:
   - Text-based PDF: use a text extractor such as `pdftotext` when it preserves the needed structure. Follow the CWD boundary for temporary extraction output too.
   - Scanned pages, diagrams, tables or formulas: inspect the source pages visually and use OCR where useful. Compare extracted text against the original for critical symbols, labels and layout.
   - If extraction is incomplete or garbled, switch methods rather than treating missing text as absent content. Use available tools first; identify missing dependencies before arranging installation.
   - URL → WebFetch. Other text formats → Read. For EPUB, use an available reader or extractor preserving chapter order.
3. **Read and verify the extracted content**, using source-page inspection wherever text alone cannot establish the meaning. Record unreadable or uncertain content instead of inventing it.
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

> **Learning depth**: Follow [Learning Depth and Practice](learning-quality.md). Fully explain core concepts and required prerequisites; determine supporting detail by its role in understanding, not by how briefly the source mentions it.

6. **Classification completeness**: When source enumerates categories ("3 types of X"), cover every member and explain meaningful distinctions; group related members or create dedicated notes according to learning needs. Scan for: "types of", "幾種", "幾類", "categories", "there are N".
7. **Source-to-note cross-verification (MANDATORY)**: Record which source file(s) and page range(s) cover each topic. Flag untraceable topics as "source not available".

### Phase D3: Tag Standard

Define tag vocabulary before creating notes:

- **Format**: English, lowercase, kebab-case (e.g., `#data-hazard`)
- **Hierarchy**: top-level → domain → detail → technique → note-type
- **Registry**: Only registered tags allowed. Detail tags co-attach parent domain tag.

### Phase D4: Vault Structure

Create `StudyVault/` with numbered folders per [templates.md](templates.md). Group 3-5 related concepts per file.

### Phase D5: Dashboard Creation

Create `00-Dashboard/`: MOC, Quick Reference, Exam Traps. See [templates.md](templates.md).

- **MOC**: Topic Map + Practice Notes + Study Tools + Tag Index (with rules) + Weak Areas (with links) + Non-core Topic Policy
- **Quick Reference**: every heading includes `→ [[Concept Note]]` link; all key formulas
- **Exam Traps**: per-topic trap points in fold callouts, linked to concept notes

### Phase D6: Concept Notes

Per [templates.md](templates.md). Key rules:

- YAML frontmatter: `source_pdf`, `part`, `keywords` (MANDATORY)
- **source_pdf MUST match verified Phase D1 mapping** — never guess from filename
- If unavailable: `source_pdf: 未持有原文`
- `[[wiki-links]]`, callouts (`[!tip]`, `[!important]`, `[!warning]`), comparison tables > prose
- ASCII diagrams for processes/flows/sequences
- **Simplification-with-exceptions**: general statements must note edge cases

### Phase D7: Practice Questions

Per [templates.md](templates.md). Key rules:

- Every topic folder MUST have a practice file; use [Learning Depth and Practice](learning-quality.md) for coverage and default question counts.
- **Active recall**: answers use `> [!answer]- 查看答案` fold callout
- Patterns use `> [!hint]-` / `> [!summary]-` fold callouts
- **Question type diversity**: follow the shared recall/application/analysis criteria in [Learning Depth and Practice](learning-quality.md).
- `## Related Concepts` with `[[wiki-links]]`

### Phase D8: Interlinking

1. `## Related Notes` on every concept note
2. MOC links to every concept + practice note
3. Cross-link concept ↔ practice; siblings reference each other
4. Quick Reference sections → `[[Concept Note]]` links
5. Weak Areas → relevant note + Exam Traps; Exam Traps → concept notes

### Phase D9: Self-Review (MANDATORY)

Verify against [quality-checklist.md](quality-checklist.md) **Document Mode** section. Fix and re-verify until all checks pass.

