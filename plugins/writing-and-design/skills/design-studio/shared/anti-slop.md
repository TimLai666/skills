# Anti-AI Slop Rules (Shared)

Both cinematic-ui and huashu-design enforce these rules. Read this before any build phase.

## What is AI Slop?

AI slop = the visual lowest common denominator from training data. It's not ugly — it's **unbranded**. Every brand gets diluted into "another AI page."

## What to Avoid

| Element | Why it's slop | Exception |
|---------|--------------|-----------|
| Aggressive purple gradients | The universal "tech feel" formula across SaaS/AI/web3 | Brand actually uses it (e.g. Linear) |
| Emoji as icons | The "not professional enough, add emoji" disease | Brand uses it (e.g. Notion), children's audience |
| Rounded cards + left color border accent | 2020-2024 Material/Tailwind烂大街 combo | User explicitly requests it |
| SVG-drawn imagery (faces/scenes) | AI SVG faces always have wrong proportions | Almost never — use real images or honest placeholders |
| CSS silhouettes / SVG hand-drawn代替真实产品图 | Generic "tech animation" — black + orange accent + rounded bars, zero brand recognition | Use real product images from brand protocol; honest placeholder as last resort |
| Inter/Roboto/Arial/system fonts as display | Too common, reader can't tell if this is a designed product or a demo | Brand spec explicitly uses them |
| GitHub-dark lazy fix: uniform deep blue `#0D1117` + generic cyan/purple neon glow | One specific combo that's烂大街 in SaaS/AI landing pages — not all dark is banned | Developer tool product where brand actually goes this direction |

## What to Do Instead

- `text-wrap: pretty` + CSS Grid + advanced CSS: typography details are the "taste tax" AI can't fake
- Use `oklch()` or spec-existing colors — never invent new colors from thin air
- Prefer AI-generated images (Gemini/Flash/Lovart) over SVG hand-drawn; HTML screenshots only for precise data tables
- Use「」quotes for Chinese, not "" — typographic proof of human review
- One detail at 120%, everything else at 80%: taste = knowing where to be precise, not uniform effort

## Judgment Boundary

"Brand actually uses it" is the only valid exception. If brand spec says purple gradient, use it — it's brand signature, not slop.

## Anti-Slop Detector

After build, run:
```bash
npx impeccable detect <output-dir-or-file>
```
Fix all flagged issues before declaring done.
