# Mode selection and language rules

Use this routing logic before drafting.

## 1. Rewrite vs generate

- Choose `rewrite` when the user provides source text, a draft, or a paragraph to fix.
- Choose `generate` when the user wants new prose from intent, bullets, notes, or context.
- If the request includes both notes and a rough draft, prefer `rewrite` and keep what already works.

## 2. Grounded vs voiced

Choose `grounded` when the text is:

- professional
- factual
- internal
- operational
- explanatory
- trust-sensitive

Choose `voiced` when the text is:

- persuasive
- editorial
- opinionated
- social
- brand-led
- meant to sound personal or distinctive

If the prompt is ambiguous:

- default to `grounded` for business, documentation, updates, or neutral explanation
- default to `voiced` for essays, commentary, posts, and marketing-style asks

## 3. Rewrite mode rules

Use when the user provides source text and wants it to read better.

1. Preserve the original claim, purpose, and factual boundaries.
2. Keep useful structure unless the structure itself causes stiffness.
3. Remove obvious AI tells first, then fix rhythm and voice.
4. Improve precision before adding flair.
5. If the source is already strong, edit lightly.

## 4. Generate mode rules

Use when the user wants fresh prose from an idea, outline, notes, or a vague request.

1. Infer the implied audience and intent from the prompt.
2. Choose the narrowest effective format instead of over-explaining.
3. Write as if a competent person with a point of view sat down to say it.
4. Do not pad thin inputs with generic significance language.
5. When details are missing, stay concrete but avoid invented facts.

## 5. Grounded style

Use for business writing, internal updates, memos, documentation, proposals, factual summaries, and other trust-sensitive text.

- Prefer direct claims, plain syntax, and calm confidence.
- Use specific nouns and verbs over abstract framing.
- Keep tone natural without sounding casual for no reason.
- Let credibility come from clarity, not polish theater.

## 6. Voiced style

Use for commentary, opinion, social posts, persuasive copy, essays, and prose that benefits from character.

- Allow stronger rhythm shifts, sharper phrasing, and controlled opinion.
- Add personality through perspective, not gimmicks.
- Use texture sparingly: a quick aside, a clean turn, a pointed line.
- Keep it human, not performatively quirky.

## 7. Language handling

- Match the user's language by default.
- Preserve the source language in rewrite mode unless asked to translate.
- Preserve deliberate code-switching in bilingual input.
- Do not force English sentence logic onto Chinese prose.
- Do not force Chinese rhetorical density onto English prose.

## 8. Output defaults

- Keep meaning stable in `rewrite`.
- Keep invention low when details are missing in `generate`.
- Prefer one strong draft over multiple padded options unless the user asks for variants.
