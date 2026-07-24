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
  version: "1.2.3"
---

# Human Writing

## Overview

Treat this as the default prose skill for anything a person will read, including every user-facing answer and any formal or informal document.
Use it for both `rewrite` and `generate` tasks. Aim for writing that sounds like someone meant it, not like a model averaged it.

Apply it by default when the output contains prose intended for a person. Do not force it onto purely technical output such as source code, JSON, SQL, shell commands, or other structured data. If another skill explicitly owns the output's domain structure or style, let that skill drive the content plan and use this skill to shape the final prose.

This file only defines the process. The actual rules live in the reference files, and each workflow step names the file to read at that stage. Read the file at that step and follow it. Do not substitute a remembered summary for the file's content.

## Workflow

1. Route the task.
   Read [references/mode-selection-and-language-rules.md](./references/mode-selection-and-language-rules.md).
   Decide `rewrite` or `generate`, identify the audience and what the text must do, settle language handling, and pick `grounded` or `voiced`. The same file then gives the working rules for the mode and style you picked.

2. Draft or rewrite.
   Read [references/human-writing-principles.md](./references/human-writing-principles.md) and write under all of its principles. They cover specificity, anchoring actions and objects, zero shared reader context, abstract adjectives and adverbs, argument structure, vocabulary, rhythm, tone, and punctuation.

3. Calibrate against examples.
   While drafting or rewriting, consult [references/human-writing-examples.md](./references/human-writing-examples.md) to see what each principle looks like when applied to real sentences, including cases where a first rewrite is still not concrete enough. The scenarios in the examples are only sentence content, not a limit on when this skill applies.

4. Run a cleanup pass.
   Read [references/ai-writing-patterns.md](./references/ai-writing-patterns.md) and remove every artifact it lists from the draft, keeping the meaning, facts, and intent intact.

5. Final check.
   Read [references/final-checklist.md](./references/final-checklist.md) and run every item against the finished text. Fix whatever fails, then run it again until everything passes.

## Resources

- Mode and style routing, mode rules, language handling: [references/mode-selection-and-language-rules.md](./references/mode-selection-and-language-rules.md)
- Writing principles: [references/human-writing-principles.md](./references/human-writing-principles.md)
- Pre-delivery checklist: [references/final-checklist.md](./references/final-checklist.md)
- Rewrite examples with original and improved sentences: [references/human-writing-examples.md](./references/human-writing-examples.md)
- AI-writing artifacts to remove: [references/ai-writing-patterns.md](./references/ai-writing-patterns.md)

## Suggested Prompt

Use `$human-writing` to write or rewrite human-facing text so it reads naturally, credibly, and like a person actually meant it.
