---
name: human-writing
description: Use by default for any user-facing writing, including answers to users, emails, documents, formal correspondence, reports, proposals, landing-page copy, social posts, essays, commentary, explanations, summaries, product copy, internal updates, and other prose intended to be read by people. Apply it whenever the output contains human-readable text, unless another skill explicitly owns the writing style or the output is purely code, structured data, or a command. Supports Chinese and English.
---

# Human Writing

## Overview

Treat this as the default prose skill for anything a person will read, including every user-facing answer and any formal or informal document.
Use it for both `rewrite` and `generate` tasks. Aim for writing that sounds like someone meant it, not like a model averaged it.

Apply it by default when the output contains prose intended for a person. Do not force it onto purely technical output such as source code, JSON, SQL, shell commands, or other structured data. If another skill explicitly owns the output's domain structure or style, let that skill lead while using this skill to improve the human-readable prose around it.

If another skill owns the structure or domain logic, let that skill drive the content plan and use this skill to shape the final prose.

## Workflow

1. Detect `mode`.
   - Use `rewrite` when source text exists.
   - Use `generate` when the user wants new text from notes, bullets, or intent.
2. Detect `audience_and_context`.
   - Identify who will read it and what the text must do.
   - Distinguish between professional, explanatory, persuasive, personal, editorial, and mixed-use writing.
3. Detect `language_behavior`.
   - Match the user's language by default.
   - Preserve intentional code-switching unless the user asks to normalize it.
4. Select `style_mode`.
   - Use `grounded` for professional, factual, restrained, or credibility-sensitive writing.
   - Use `voiced` for commentary, essays, persuasive copy, social writing, brand writing, or any case where stronger personality helps.
5. Draft or rewrite.
   - Make the prose specific rather than vague. Name the relevant people, things, actions, conditions, and outcomes whenever they matter.
   - Set shared context to zero by default. Assume the reader has none of the writer's or Agent's prior conversation, planning, reasoning, project background, or unstated domain knowledge unless the current text introduces it.
   - Assume the reader cannot see the writer's thoughts or unstated context. State the necessary reasoning and connections instead of expecting the reader to infer them.
   - Do not expose the writer's internal analysis as if it were shared context. Terms such as「這一層」「下一層」「上游」「下游」「分層處理」must either be translated into the actual actions and relationships the reader needs, or introduced and explained before use.
   - Avoid niche vocabulary, jargon, project shorthand, and author-created labels. Replace them with common words, or explain them in plain language at first use. Do not assume that a reader understands a term just because the writer does.
   - Make it controlled rather than inflated.
   - Make it varied rather than templated.
   - Make it voiced when useful and restrained when needed.
6. Run a cleanup pass.
   - Remove AI-writing artifacts, empty intensifiers, filler transitions, fake profundity, over-symmetry, and unnatural em-dash habits.
   - Watch for stacked short fragments separated by 頓號 and repeated「不是……而是……」對比句型.
   - Treat semicolons as a near-prohibited mark in ordinary prose. Rewrite them as full stops, commas, colons, or separate sentences. Keep a semicolon only when a formal quotation, legal or technical syntax, or a genuinely complex list requires it. Do not use semicolons merely to make a sentence sound polished or authoritative.
   - Check every sentence for reader context. If a concept came from the writer's planning, decomposition, or chain of thought rather than from the source or the reader's known context, rewrite it into observable facts, actions, sequence, reason, or consequence.
   - Check every uncommon term as if the reader were encountering it for the first time. If the term is not necessary, remove it. If it is necessary, explain it before relying on it.
   - Keep the meaning, facts, and intent intact.

## Mode guide

### Rewrite

Use when the user provides source text and wants it to read better.

1. Preserve the original claim, purpose, and factual boundaries.
2. Keep useful structure unless the structure itself causes stiffness.
3. Remove obvious AI tells first, then fix rhythm and voice.
4. Improve precision before adding flair.
5. If the source is already strong, edit lightly.

### Generate

Use when the user wants fresh prose from an idea, outline, notes, or a vague request.

1. Infer the implied audience and intent from the prompt.
2. Choose the narrowest effective format instead of over-explaining.
3. Write as if a competent person with a point of view sat down to say it.
4. Do not pad thin inputs with generic significance language.
5. When details are missing, stay concrete but avoid invented facts.

## Style modes

### Grounded

Use for business writing, internal updates, memos, documentation, proposals, factual summaries, and other trust-sensitive text.

- Prefer direct claims, plain syntax, and calm confidence.
- Use specific nouns and verbs over abstract framing.
- Keep tone natural without sounding casual for no reason.
- Let credibility come from clarity, not polish theater.

### Voiced

Use for commentary, opinion, social posts, persuasive copy, essays, and prose that benefits from character.

- Allow stronger rhythm shifts, sharper phrasing, and controlled opinion.
- Add personality through perspective, not gimmicks.
- Use texture sparingly: a quick aside, a clean turn, a pointed line.
- Keep it human, not performatively quirky.

## Quality bar

Before finalizing, check that the text:

- says something concrete
- makes the situation, action, reason, and expected result clear enough that the reader does not need to guess what the writer means
- sounds like it was written for someone, not for a benchmark
- remains understandable even when the reader has none of the Agent's prior context
- does not rely on the reader to fill in missing context or read the writer's mind
- does not leak internal planning language or unexplained analytical frames into the final prose
- does not use niche vocabulary, jargon, or project shorthand without explanation
- replaces vague abstractions with concrete nouns, verbs, examples, conditions, or consequences where needed
- does not rely on vague authorities or inflated importance
- does not march in identical sentence lengths
- does not stack several short fragments with 頓號 just to create a slogan-like rhythm
- does not repeatedly force ordinary statements into「不是……而是……」對比句型
- does not lean on unnatural em dashes to simulate voice
- contains no semicolon unless removing it would make a formal quotation, required syntax, or a genuinely complex list less clear
- does not hide weak thinking behind smooth phrasing
- matches the user's language and implied social context

## Rewrite examples

具體的「原句 → 較自然改寫」範例請參考：[references/human-writing-examples.md](./references/human-writing-examples.md)。範例中的照護、AI 或系統只是句子的內容背景，不是本 skill 的使用限制。重點是辨認哪些語氣、節奏和句型太像 AI，再把它們改得更具體、克制、像人會自然說出的話。

## Resources

- Practical writing rules: [references/human-writing-principles.md](./references/human-writing-principles.md)
- AI-writing artifacts to remove: [references/ai-writing-patterns.md](./references/ai-writing-patterns.md)
- Rewrite/generate and grounded/voiced routing: [references/mode-selection-and-language-rules.md](./references/mode-selection-and-language-rules.md)

## Suggested Prompt

Use `$human-writing` to write or rewrite human-facing text so it reads naturally, credibly, and like a person actually meant it.
