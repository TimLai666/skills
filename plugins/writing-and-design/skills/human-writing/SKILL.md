---
name: human-writing
description: >-
  This skill MUST be used by default for any user-facing writing, including
  answers to users, emails, documents, formal correspondence, reports,
  proposals, landing-page copy, social posts, essays, commentary,
  explanations, summaries, product copy, internal updates, and other prose
  intended to be read by people. Apply it whenever the output contains
  human-readable text. This skill MUST NOT be skipped unless another skill
  explicitly owns the writing style or the output is purely code, structured
  data, or a command. Supports Chinese and English.
metadata:
  version: "1.8.4"
---

# Human Writing

## Overview

Use this for prose that a person will read, whether you are writing from scratch or revising a draft. The goal is prose the reader can picture and act on, with no AI tells left in.

Do not apply it to code, JSON, SQL, shell commands, or other structured output. When another skill owns the format or subject matter, use that skill to plan the content and use this one for the prose.

This file gives the sequence. The rules are in the linked references. Read the reference named at each step instead of relying on a remembered summary.

## Workflow

1. Choose the mode.
   Read [references/mode-selection-and-language-rules.md](./references/mode-selection-and-language-rules.md).
   Decide between `rewrite` and `generate`, identify the reader and purpose, match the language, and choose `grounded` or `voiced`.

2. Write the draft.
   Read [references/human-writing-principles.md](./references/human-writing-principles.md). Use its rules for concrete detail, reader context, structure, vocabulary, rhythm, tone, and punctuation.

3. Check the examples.
   Consult [references/human-writing-examples.md](./references/human-writing-examples.md) while writing. They show how the rules work in sentences, including rewrites that still leave too much for the reader to infer.

4. Remove AI patterns.
   Read [references/ai-writing-patterns.md](./references/ai-writing-patterns.md). Remove every listed pattern without changing the meaning, facts, or intent.

5. Check the finished text.
   Read [references/final-checklist.md](./references/final-checklist.md). Test every item against the actual text, fix failures, and check it again.

## Suggested Prompt

Use `$human-writing` to write or rewrite human-facing text so it reads like a person actually meant it.
