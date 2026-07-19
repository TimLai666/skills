---
name: llm-wiki
description: "Karpathy's LLM Wiki: build/query interlinked markdown KB with Zettelkasten note discipline. Triggers: 知識庫, 建 wiki, wiki 筆記, 研究筆記, ingest sources, knowledge base."
version: 3.0.0
license: MIT
platforms: [linux, macos, windows]
---

# Karpathy's LLM Wiki

Build and maintain a persistent, compounding knowledge base as interlinked markdown files.
Based on [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Unlike traditional RAG (which rediscovers knowledge from scratch per query), the wiki
compiles knowledge once and keeps it current. Cross-references are already there.
Contradictions have already been flagged. Synthesis reflects everything ingested.

**Division of labor:** The human curates sources and directs analysis. The agent
summarizes, cross-references, files, and maintains consistency.

## When This Skill Activates

Use this skill when the user:
- Wants to research a topic (auto-create wiki if none exists, then proceed with research)
- Asks to create, build, start, or structure a new wiki, note system, or knowledge base
- Asks to ingest, add, or process a source into their wiki
- Asks a question and an existing wiki is present
- Asks to lint, audit, or health-check their wiki
- References their wiki, knowledge base, or "notes" in a research context

**The wiki is research infrastructure, not the end goal.** Users want research
results; the wiki is the mechanism that makes research compounding and persistent.
When a user says "help me research X" and no wiki exists, create one and proceed
with the research.

## Wiki Location

The wiki is just a directory of markdown files — open it in Obsidian, VS Code, or
any editor. No database, no special tooling required.

### Path Resolution

1. **User specifies a path** — use it directly.
2. **No path given** — analyze the context to suggest paths:
   - What is the user researching? What kind of directory name fits this topic?
   - What does the CWD directory structure look like? Are there existing directories
     that suggest a naming convention?
   - Suggest 2-3 contextually appropriate options, then let the user confirm or
     provide their own.
3. **Never scan `~/`** — do not search the home directory for existing wikis.
4. **Never assume a default path** — always resolve explicitly.

```
User provides path → use it
    ↓ (no path)
Analyze context (topic, CWD structure, existing dirs)
    ↓
Suggest 2-3 fitting options → user confirms or gives own path
    ↓
Use confirmed path for all subsequent operations
```

## Architecture: Three Layers

```
wiki/
├── SCHEMA.md           # Conventions, structure rules, domain config
├── index.md            # Global catalog: topics + cross-topic pages
├── log.md              # Chronological action log (append-only, rotated at 500 entries)
├── raw/                # Layer 1: Immutable source material
│   ├── articles/       # Web articles, clippings
│   ├── papers/         # PDFs, arxiv papers
│   ├── transcripts/    # Meeting notes, interviews
│   └── assets/         # Images, diagrams referenced by sources
├── topics/             # Layer 2: Per-research-topic grouping
│   ├── {topic-slug}/
│   │   ├── concepts/   # Concepts specific to this topic
│   │   ├── entities/   # Entities specific to this topic
│   │   ├── comparisons/ # Comparisons specific to this topic
│   │   └── index.md    # Topic-level catalog
│   └── ...
├── concepts/           # Layer 2: Cross-topic concept pages
├── entities/           # Layer 2: Cross-topic entity pages
├── comparisons/        # Layer 2: Side-by-side analyses
└── queries/            # Layer 2: Filed query results worth keeping
```

**Layer 1 — Raw Sources:** Immutable. The agent reads but never modifies these.
**Layer 2 — The Wiki:** Agent-owned markdown files. Created, updated, and
cross-referenced by the agent. Organized by research topic.
**Layer 3 — The Schema:** `SCHEMA.md` defines structure, conventions, and tag taxonomy.

### Topic Grouping Rules

Each research topic gets its own subdirectory under `topics/`. When ingesting:

- **Single-topic page** (only relevant to one research area) → `topics/{topic}/concepts/`, `topics/{topic}/entities/`, or `topics/{topic}/comparisons/`
- **Cross-topic page** (relevant to 2+ research areas) → global `concepts/`, `entities/`, or `comparisons/`
- Topic pages use `[[wikilink]]` to reference global pages and vice versa

**判断标准:** When a new entity/concept appears in a source, check if it's already
referenced in another topic. If yes → global. If no → place in the current topic.

### Two-Level Index

- **Global `index.md`** — Lists all research topics (linking to their index) + cross-topic pages
- **Topic `index.md`** — Lists all pages within that specific topic

### Note Discipline (Zettelkasten)

Wiki pages follow Zettelkasten（卡片盒筆記法）discipline — refer to the
`zettelkasten` skill for the full method. Mapping:

- **Concept and entity pages are cards** — one page = one distinct idea/entity.
  Split by idea count, not just line count.
- **Global/topic `index.md` are structure notes** — navigation, atomicity does not
  apply. The structure-note role is carried entirely by the two-level index: don't
  create separate structure-note files in a wiki. Exception: a split remnant page
  ("summary + links", zettelkasten split procedure step 4) is a small concept-type
  page, not a structure-note violation.
- **Comparison and query pages are synthesis notes** — they exist to combine cards,
  so atomicity does not apply, but linking rules do. Ideas born inside a synthesis
  page that stand on their own must be promoted to concept pages (see Page
  Thresholds) — synthesis pages must not become a shelter from atomicity.
- **`raw/` plays the literature-note role** — sources stay immutable; wiki pages
  restate claims in their own words and cite provenance.

**Every page create or update runs this checklist before writing.** Authoritative
version with full split criteria and worked cases: the `zettelkasten` skill
(`references/02-split-and-checklist.md`); the core below is the fallback when
that skill is unavailable:

1. **Atomicity** — is this addition a single idea (entity pages: a single entity)?
2. **Split decision** — split when any criterion hits: the title needs "and" to
   cover the content; a passage could be cited independently from another context;
   the page answers more than one question; parts update at different rates;
   inbound links can't say which point they target. Don't split when pieces would
   lose self-containment, are only ever cited together, or are mere rephrasings
   or examples of the same idea. Length (~200 lines) is a warning to run these
   criteria, not a reason to split.
3. **Duplicate & conflict check** — search first. Existing idea → update that page.
   Conflicting information → don't merge-overwrite; follow the Update Policy
   (note both positions, mark `contradictions`/`contested`, link both ways).
4. **Links** — link terms in place where the text mentions them (1-2 real outbound
   links); relations the text doesn't naturally mention go in a labeled
   end-section; check whether linked pages need a link back. Backlink edits don't
   recurse: fixing a backlink doesn't trigger a checklist run on that page.
5. **Structure/index** — add or refresh the page's row in the topic/global index.
6. **Self-contained** — the page stands alone without the source context.
7. **Own words** — restate, don't paste; cite provenance.

This is a per-write discipline, not a lint-time cleanup.

**Deference:** this discipline governs llm-wiki wikis. When working in a notes
repository that is not an llm-wiki (no SCHEMA.md/index.md), follow that
repository's own conventions — mirroring the zettelkasten skill's 沿用現場 rule.

## Resuming an Existing Wiki (CRITICAL — do this every session)

When the user has an existing wiki, **always orient yourself before doing anything**:

① **Read `SCHEMA.md`** — understand the domain, conventions, and tag taxonomy.
② **Read `index.md`** — learn what pages exist and their summaries.
③ **Scan recent `log.md`** — read the last 20-30 entries to understand recent activity.
④ **Quick consistency probes** (cheap, catches drift before it compounds):
   compare the actual page count against the index header's "Total pages"; and
   spot-check the wiki's SCHEMA.md for rules superseded by the current skill
   canon (e.g., "split at 200 lines" as a criterion, "minimum 2 links", missing
   comparison/query exemptions). If either probe fails, suggest running lint or
   updating SCHEMA.md before writing.

```bash
# Orientation reads at session start (replace <wiki> with the resolved path)
read_file "<wiki>/SCHEMA.md"
read_file "<wiki>/index.md"
read_file "<wiki>/log.md" offset=<last 30 lines>
```

Only after orientation should you ingest, query, or lint. This prevents:
- Creating duplicate pages for entities that already exist
- Missing cross-references to existing content
- Contradicting the schema's conventions
- Repeating work already logged

For large wikis (100+ pages), also run a quick `search_files` for the topic
at hand before creating anything new.

## Initializing a New Wiki

When the user asks to create or start a wiki:

1. Resolve the wiki path (see Path Resolution above)
2. Create the directory structure above
3. Ask the user what domain the wiki covers — be specific
4. Ask what research topics they plan to work on (creates `topics/` subdirectories)
5. Write `SCHEMA.md` customized to the domain (see template below)
6. Write initial `index.md` with topic listings
7. Write initial `log.md` with creation entry
8. Confirm the wiki is ready and suggest first sources to ingest

### SCHEMA.md Template

Adapt to the user's domain. The schema constrains agent behavior and ensures consistency:

```markdown
# Wiki Schema

## Domain
[What this wiki covers — e.g., "AI/ML research", "personal health", "startup intelligence"]

## Topics
[List research topics. Each gets a subdirectory under `topics/`.]
- topic-slug: [description]
- topic-slug: [description]

## Topic Grouping Rules
- Each research topic = `topics/{topic-slug}/` with its own `concepts/`, `entities/`, `comparisons/`, `index.md`
- Only appears in one topic → place in that topic's subdirectory
- Appears in 2+ topics → place in global `concepts/` or `entities/`
- When unsure, check existing pages across topics before placing
- Cross-topic pages should link back to all relevant topics via `[[wikilink]]`

## Conventions
- **Markdown formatting:** Wiki pages use Obsidian Flavored Markdown. For wikilinks, embeds, callouts, frontmatter properties, and other Obsidian-specific syntax, refer to the `obsidian-markdown` skill.
- **Academic sources:** For arXiv paper search, Semantic Scholar citations, and BibTeX generation, refer to the `arxiv` skill.
- **Note discipline:** Every page write runs the full seven-item Zettelkasten change checklist (atomicity, split, duplicate, links, structure/index, self-contained, own words) — refer to the `zettelkasten` skill for split criteria and linking rules.
- File names: title as filename — English content: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`); Chinese content: use the Chinese title directly (e.g., `間隔重複比集中複習有效.md`), per the `zettelkasten` skill's naming convention
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (at least 1-2 real outbound links per page — link where the text mentions them, don't pad to hit a quota)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source. This lets a reader trace each
  claim back without re-reading the whole raw file. Optional on single-source pages where the
  `sources:` frontmatter is enough.

## Frontmatter
  ```yaml
  ---
  title: Page Title
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: entity | concept | comparison | query
  tags: [from taxonomy below]
  sources: [raw/articles/source-name.md]
  # Optional quality signals:
  confidence: high | medium | low        # how well-supported the claims are
  contested: true                        # set when the page has unresolved contradictions
  contradictions: [other-page-slug]      # pages this one conflicts with
  ---
  ```

`confidence` and `contested` are optional but recommended for opinion-heavy or fast-moving
topics. Lint surfaces `contested: true` and `confidence: low` pages for review so weak claims
don't silently harden into accepted wiki fact.

Type governance: adding a new `type` value requires three things at once — a one-line
definition, a title convention, and a lint mapping. Never add a bare enum value.

### raw/ Frontmatter

Raw sources ALSO get a small frontmatter block so re-ingests can detect drift:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

The `sha256:` lets a future re-ingest of the same URL skip processing when content is unchanged,
and flag drift when it has changed. Compute over the body only (everything after the closing
`---`), not the frontmatter itself.

## Tag Taxonomy
[Define 10-20 top-level tags for the domain. Add new tags here BEFORE using them.]

Example for AI/ML:
- Models: model, architecture, benchmark, training
- People/Orgs: person, company, lab, open-source
- Techniques: optimization, fine-tuning, inference, alignment, data
- Meta: comparison, timeline, controversy, prediction

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Promote synthesis-born ideas** — when a comparison/query page produces a claim that stands on its own (a mechanism, a generalizable conclusion), create a concept page for it and link it in place; wiki-internal origin counts toward page creation, not just source appearances
- **Split a page** when it covers 2+ distinct ideas (Zettelkasten atomicity — see the `zettelkasten` skill's split criteria) — break into atomic pages with cross-links. Length is a warning, not a criterion: run the split criteria on pages over ~200 lines, but a long single-idea page stays whole. Comparison, query, and index pages are exempt from atomicity
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
5. When a contradiction is resolved (user ruling or a decisive source): update both
   pages, clear `contested`, remove the pair from `contradictions:`, archive or mark
   the superseded claim, and log the resolution
```

### index.md Template

Two levels: global index (wiki root) and topic index (each topic subdirectory).

**Global index.md:**

```markdown
# Wiki Index

> Global catalog. Research topics and cross-topic pages.
> Last updated: YYYY-MM-DD | Topics: N | Total pages: N

## Topics

| Topic | Pages | Index |
|-------|-------|-------|
| [topic name] | N | [[topics/{slug}/index|→ index]] |

## Cross-Topic Concepts

| Page | Summary | Topics |
|------|---------|--------|
| [[page-name]] | One-line summary | topic-a, topic-b |

## Cross-Topic Entities

| Page | Summary | Topics |
|------|---------|--------|

## Comparisons

| Page | Summary |
|------|---------|

## Queries

| Page | Summary |
|------|---------|
```

**Topic index.md** (`topics/{slug}/index.md`):

```markdown
# {Topic Name} — Index

> Pages: N | Last updated: YYYY-MM-DD

## Concepts

| Page | Summary |
|------|---------|

## Entities

| Page | Summary |
|------|---------|

## Comparisons

| Page | Summary |
|------|---------|
```

**Scaling rule:** When any section exceeds 50 entries, split into sub-sections.

### log.md Template

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY-MM.md (year-month of rotation), start fresh.

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

## Core Operations

### 1. Ingest

When the user provides a source (URL, file, paste), integrate it into the wiki:

① **Capture the raw source:**
   - URL → use **defuddle** (run `npx defuddle <url>`) to extract clean markdown; fallback to `web_extract` if defuddle fails or is unavailable
   - PDF → use **defuddle** (handles PDFs natively); fallback to `web_extract`
   - Pasted text → save to appropriate `raw/` subdirectory
   - Name the file descriptively: `raw/articles/karpathy-llm-wiki-2026.md`
   - **Add raw frontmatter** (`source_url`, `ingested`, `sha256` of the body).
     On re-ingest of the same URL: recompute the sha256, compare to the stored value —
     skip if identical, flag drift and update if different. This is cheap enough to
     do on every re-ingest and catches silent source changes.

② **Discuss takeaways** with the user — what's interesting, what matters for
   the domain. (Skip this in automated/cron contexts — proceed directly.)

③ **Check what already exists** — search index.md and use `search_files` to find
   existing pages for mentioned entities/concepts. This is the difference between
   a growing wiki and a pile of duplicates.

④ **Write or update wiki pages:**
   - **Zettelkasten check (every page write):** Run the full seven-item change
     checklist from the `zettelkasten` skill (atomicity → split → duplicate →
     links → structure → self-contained → own words). Does the page now cover
     2+ distinct ideas → split into linked atomic pages, fix inbound links,
     update the index.
   - **New entities/concepts:** Create pages only if they meet the Page Thresholds
     in SCHEMA.md (2+ source mentions, or central to one source)
   - **Existing pages:** Add new information, update facts, bump `updated` date.
     When new info contradicts existing content, follow the Update Policy.
   - **Cross-reference:** Every new or updated page must link to at least 1-2 other
     pages via `[[wikilinks]]`, placed where the text mentions them — real
     relationships only. Check that existing pages link back.
   - **Tags:** Only use tags from the taxonomy in SCHEMA.md
   - **Provenance:** On pages synthesizing 3+ sources, append `^[raw/articles/source.md]`
     markers to paragraphs whose claims trace to a specific source.
   - **Confidence:** For opinion-heavy, fast-moving, or single-source claims, set
     `confidence: medium` or `low` in frontmatter. Don't mark `high` unless the
     claim is well-supported across multiple sources.

⑤ **Update navigation:**
   - Add new pages to `index.md` under the correct section, alphabetically
   - When updating an existing page, refresh its one-line summary in the index
     if the content meaningfully shifted
   - Update the "Total pages" count and "Last updated" date in index header
   - Append to `log.md`: `## [YYYY-MM-DD] ingest | Source Title`
   - List every file created or updated in the log entry
   - Record `split_decisions` in the log entry: pages split (which criterion hit)
     and borderline pages judged not-split (why) — this persists the zettelkasten
     Output Contract into the wiki so the next session can audit what was checked
   - Record `links_updated`: backlinks added, and backlink decisions declined
     with reasons (lint's symmetry check skips recorded declined pairs)

⑥ **Report what changed** — list every file created or updated, plus the
   `split_decisions` and `links_updated` records. If the ingest touched 10+
   pages, suggest running a light lint subset (broken links, index completeness,
   log reconciliation) before ending the session.

A single source can trigger updates across 5-15 wiki pages. This is normal
and desired — it's the compounding effect.

### Academic Sources (arXiv + Semantic Scholar)

For academic papers, use the **arxiv** skill to search and retrieve:

1. **Search**: `python arxiv/scripts/search_arxiv.py "topic" --sort date --max 10`
2. **Impact check**: Semantic Scholar API for citation counts
   ```bash
   curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=citationCount,influentialCitationCount"
   ```
3. **Read**: `npx defuddle https://arxiv.org/pdf/ID` (fallback: `web_extract`)
4. **Ingest** as normal — raw source goes to `raw/papers/`, wiki pages follow standard workflow

On wiki pages for papers, add optional frontmatter fields:
```yaml
arxiv_id: "2402.03300"
citation_count: 150
influential_citations: 12
```

### 2. Query

When the user asks a question about the wiki's domain:

① **Read `index.md`** to identify relevant pages.
② **For wikis with 100+ pages**, also `search_files` across all `.md` files
   for key terms — the index alone may miss relevant content.
③ **Read the relevant pages** using `read_file`.
④ **Synthesize an answer** from the compiled knowledge. Cite the wiki pages
   you drew from: "Based on [[page-a]] and [[page-b]]..."
⑤ **File valuable answers back** — if the answer is a substantial comparison,
   deep dive, or novel synthesis, create a page in `queries/` or `comparisons/`.
   Don't file trivial lookups — only answers that would be painful to re-derive.
⑥ **Update log.md** with the query and whether it was filed.

### 3. Lint

When the user asks to lint, health-check, or audit the wiki (also suggest it
proactively after any ingest touching 10+ pages — see ingest ⑥). Items marked
*(semantic, agent-run)* are judgment-based candidate reports, not mechanical
checks — expect false positives, report only:

① **Orphan pages:** Find pages with no inbound `[[wikilinks]]` from other pages.
```python
# Use execute_code for this — programmatic scan across all wiki pages
import os, re
from collections import defaultdict
wiki = "<wiki>"  # replace with resolved wiki path
# Scan all .md files in entities/, concepts/, comparisons/, queries/
# Extract all [[wikilinks]] — build inbound link map
# Pages with zero inbound links are orphans
```

② **Broken wikilinks:** Find `[[links]]` that point to pages that don't exist.

③ **Index completeness:** Every wiki page should appear in `index.md`. Compare
   the filesystem against index entries.

④ **Frontmatter validation:** Every wiki page must have all required fields
   (title, created, updated, type, tags, sources). Tags must be in the taxonomy.

⑤ **Stale content:** Pages whose `updated` date is >90 days older than the most
   recent source that mentions the same entities.

⑥ **Contradictions:** Pages on the same topic with conflicting claims. Look for
   pages that share tags/entities but state different facts. Surface all pages
   with `contested: true` or `contradictions:` frontmatter for user review.

⑦ **Quality signals:** List pages with `confidence: low` and any page that cites
   only a single source but has no confidence field set — these are candidates
   for either finding corroboration or demoting to `confidence: medium`.

⑧ **Source drift:** For each file in `raw/` with a `sha256:` frontmatter, recompute
   the hash and flag mismatches. Mismatches indicate the raw file was edited
   (shouldn't happen — raw/ is immutable) or ingested from a URL that has since
   changed. Not a hard error, but worth reporting.

⑨ **Page size & atomicity:** Flag pages covering 2+ distinct ideas — candidates
   for splitting per the `zettelkasten` skill's split criteria. Pages over ~200
   lines are a warning to run those criteria, not grounds to split by length
   alone. Skip index pages. For comparison/query pages, replace the atomicity
   check with a promotion spot-check *(semantic, agent-run)*: standalone ideas
   living only inside a synthesis page that were never promoted to concept
   pages (see Page Thresholds).

⑩ **Tag audit:** List all tags in use, flag any not in the SCHEMA.md taxonomy.

⑪ **Log rotation:** If log.md exceeds 500 entries, rotate it.

⑫ **Log reconciliation:** compare recent page `updated` dates against log entries —
   flag pages changed with no log record (writes that bypassed the discipline).

⑬ **Link symmetry:** build the bidirectional link map; report A→B edges where B
   doesn't link back, excluding pairs whose declined-backlink decision is recorded
   in the log (ingest ⑤). Backlinks are curation judgments — report for review,
   don't auto-fix. Exception: `contradictions` frontmatter must be mutual
   (A lists B ⇒ B lists A) — asymmetry there is a hard error.

⑭ **Frontmatter link fields:** verify every slug in `contradictions:` (and any
   other frontmatter field that references pages) resolves to an existing page —
   renames and archiving leave these dangling silently, since they are not
   `[[wikilinks]]` and no other check covers them.

⑮ **Misplacement & promote:** find `topics/{t}/` pages referenced from 2+ topics —
   candidates for promotion to global. Promote = move the file keeping the
   filename (filename-based `[[wikilinks]]` survive), fix any path-style links,
   update both indexes, log the move.

⑯ **Duplicate page detection** *(semantic, agent-run)*: near-duplicate titles or
   high content overlap between pages sharing tags/entities.

⑰ **Verbatim-copy check** *(semantic, agent-run)*: wiki pages whose paragraphs are
   near-verbatim from `raw/` — entity facts, figures, and provenance markers
   legitimately repeat, so candidates only.

⑱ **Title-form ↔ type spot check** *(semantic, agent-run)*: sample pages — concept
   pages should carry statement titles, entity pages name titles.

⑲ **Index summary drift:** sample index rows against current page content — flag
   stale one-line summaries.

⑳ **Report findings** with specific file paths and suggested actions, grouped by
   severity (broken links > orphans > dangling frontmatter slugs > source drift >
   contested pages > stale content > style issues).

㉑ **Append to log.md:** `## [YYYY-MM-DD] lint | N issues found`

## Working with the Wiki

### Searching

```bash
# Find pages by content (replace <wiki> with resolved path)
search_files "transformer" path="<wiki>" file_glob="*.md"

# Find pages by filename
search_files "*.md" target="files" path="<wiki>"

# Find pages by tag
search_files "tags:.*alignment" path="<wiki>" file_glob="*.md"

# Recent activity
read_file "<wiki>/log.md" offset=<last 20 lines>
```

### Bulk Ingest

When ingesting multiple sources at once, batch the updates:
1. Read all sources first
2. Identify all entities and concepts across all sources
3. Check existing pages for all of them (one search pass, not N)
4. Create/update pages in one pass (avoids redundant updates)
5. Update index.md once at the end
6. Append log entries per batch as you go — don't hold them all for the end
   (removes the interruption window); include per-page `split_decisions` and
   `links_updated`
7. Defer backlink decisions to a single pass at the end of the batch (one pass,
   not N — same principle as step 3)

### Archiving

When content is fully superseded or the domain scope changes:
1. Create `_archive/` directory if it doesn't exist
2. Move the page to `_archive/` with its original path (e.g., `_archive/entities/old-page.md`)
3. Remove from `index.md`
4. Update any pages that linked to it — replace wikilink with plain text + "(archived)";
   also remove or repoint its slug in any `contradictions:` or other frontmatter
   fields that reference it
5. Log the archive action

### Obsidian Integration

The wiki directory works as an Obsidian vault out of the box:
- `[[wikilinks]]` render as clickable links
- Graph View visualizes the knowledge network
- YAML frontmatter powers Dataview queries
- The `raw/assets/` folder holds images referenced via `![[image.png]]`

For best results:
- Set Obsidian's attachment folder to `raw/assets/`
- Enable "Wikilinks" in Obsidian settings (usually on by default)
- Install Dataview plugin for queries like `TABLE tags WHERE type = "entity" AND contains(tags, "company")` — query by frontmatter `type`, not by folder: `FROM "entities"` would miss `topics/*/entities/`

If using the Obsidian skill alongside this one, set `OBSIDIAN_VAULT_PATH` to the
same directory as the wiki path.

### Obsidian Headless (servers and headless machines)

On machines without a display, use `obsidian-headless` instead of the desktop app.
It syncs vaults via Obsidian Sync without a GUI — perfect for agents running on
servers that write to the wiki while Obsidian desktop reads it on another device.

**Setup:**
```bash
# Requires Node.js 22+
npm install -g obsidian-headless

# Login (requires Obsidian account with Sync subscription)
ob login --email <email> --password '<password>'

# Create a remote vault for the wiki
ob sync-create-remote --name "LLM Wiki"

# Connect the wiki directory to the vault
cd <wiki>
ob sync-setup --vault "<vault-id>"

# Initial sync
ob sync

# Continuous sync (foreground — use systemd for background)
ob sync --continuous
```

**Continuous background sync via systemd:**
```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=<wiki>
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
# Enable linger so sync survives logout:
sudo loginctl enable-linger $USER
```

This lets the agent write to the wiki on a server while you browse the same
vault in Obsidian on your laptop/phone — changes appear within seconds.

## Pitfalls

- **Never modify files in `raw/`** — sources are immutable. Corrections go in wiki pages.
- **Always orient first** — read SCHEMA + index + recent log before any operation in a new session.
  Skipping this causes duplicates and missed cross-references.
- **Always update index.md and log.md** — skipping this makes the wiki degrade. These are the
  navigational backbone.
- **Don't create pages for passing mentions** — follow the Page Thresholds in SCHEMA.md. A name
  appearing once in a footnote doesn't warrant an entity page.
- **Don't create pages without cross-references** — isolated pages are invisible. Every page must
  link to at least 1-2 other pages, via real relationships rather than quota-padding.
- **Frontmatter is required** — it enables search, filtering, and staleness detection.
- **Tags must come from the taxonomy** — freeform tags decay into noise. Add new tags to SCHEMA.md
  first, then use them.
- **Keep pages scannable** — a wiki page should be readable in 30 seconds. Split pages that
  cover 2+ distinct ideas; length (~200 lines) is a warning to run the split criteria, not a
  reason to split by itself. Move detailed analysis to dedicated deep-dive pages.
- **Run the Zettelkasten checklist on every page write** — atomicity and split decisions
  happen at write time, not only during lint. See the `zettelkasten` skill.
- **Ask before mass-updating** — if an ingest would touch 10+ existing pages, confirm
  the scope with the user first.
- **Rotate the log** — when log.md exceeds 500 entries, rename it `log-YYYY-MM.md` and start fresh.
  The agent should check log size during lint.
- **Handle contradictions explicitly** — don't silently overwrite. Note both claims with dates,
  mark in frontmatter, flag for user review.

## Related Tools

[llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) is a Node.js CLI that
compiles sources into a concept wiki with the same Karpathy inspiration. It's Obsidian-compatible,
so users who want a scheduled/CLI-driven compile pipeline can point it at the same vault this
skill maintains. Trade-offs: it owns page generation (replaces the agent's judgment on page
creation) and is tuned for small corpora. Use this skill when you want agent-in-the-loop curation;
use llmwiki when you want batch compile of a source directory.
