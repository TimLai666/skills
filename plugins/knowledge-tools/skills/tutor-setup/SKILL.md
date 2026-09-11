---
name: tutor-setup
description: |
  Transforms knowledge sources into an Obsidian StudyVault. This skill MUST be used when the user asks to build a StudyVault from documents, a codebase, or an llm-wiki. Three modes: (1) Document Mode — PDF/text/web sources → study notes with practice questions. (2) Codebase Mode — source code project → onboarding vault for new developers. (3) Wiki Mode — llm-wiki knowledge base → StudyVault with incremental sync. Mode is auto-detected based on project markers and wiki presence.
metadata:
  version: "1.2.0"
---

# Tutor Setup — Knowledge to Obsidian StudyVault

## CWD Boundary Rule (Document Mode & Codebase Mode)

> **NEVER access files outside the current working directory (CWD).**
> All source scanning, reading, and vault output MUST stay within CWD and its subdirectories.
> If the user provides an external path, ask them to copy the files into CWD first.

**Wiki Mode exception:** Wiki Mode reads from a user-specified wiki path, which may
be outside CWD. StudyVault output (sync target) still goes into CWD.

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

## Mode Workflows

After completing mode detection and confirmation above, read the chosen workflow
in full before beginning. It defines the phases, source checks and completion criteria.

| Mode | Workflow | Templates |
|---|---|---|
| Document | [Document workflow](references/document-workflow.md) | [Study notes, dashboard, practice and manifest templates](references/templates.md) |
| Codebase | [Codebase workflow](references/codebase-workflow.md) | [Module, architecture and exercise templates](references/codebase-templates.md) |
| Wiki | [Wiki workflow](references/wiki-workflow.md) | [Study notes and sync manifest](references/templates.md) |

Before analyzing content or generating notes and questions, read
[Learning Depth and Practice](references/learning-quality.md). Before reporting
completion, apply the selected mode's [Quality Checklist](references/quality-checklist.md).

## Source and Progress Protection

- Verify actual source content and its mapping to notes; never infer topics solely from filenames.
- Preserve sources, existing learning records and handwritten notes. Read affected content before updating it.
- Wiki synchronization uses the manifest for incremental changes. Follow the Wiki workflow's reconciliation step for source renames, deletions, splits or edits overlapping user content.
- Keep answers folded and cross-links intact. Report actual changes, validation and unresolved gaps.

## Language

- Match source material language (Korean → Korean notes, etc.)
- **Tags/keywords**: ALWAYS English
