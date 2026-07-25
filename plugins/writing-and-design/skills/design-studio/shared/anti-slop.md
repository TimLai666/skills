# Anti-AI Slop Rules (Shared)

Both cinematic-ui and huashu-design enforce these rules. Read this before any build phase.

## What is AI Slop?

AI slop = the visual lowest common denominator from training data. It's not ugly — it's **unbranded**. Every brand gets diluted into "another AI page."

## What to Avoid

| Element | Why it's slop | Exception |
|---------|--------------|-----------|
| Aggressive purple gradients | The universal "tech feel" formula across SaaS/AI/web3 | Brand actually uses it (e.g. Linear) |
| Emoji as icons | The "not professional enough, add emoji" disease | Brand uses it (e.g. Notion), children's audience |
| Rounded cards + left color border accent | 2020-2024 Material/Tailwind爛大街 combo | User explicitly requests it |
| SVG-drawn imagery (faces/scenes) | AI SVG faces always have wrong proportions | Almost never — use real images or honest placeholders |
| CSS silhouettes / SVG hand-drawn代替真實產品圖 | Generic "tech animation" — black + orange accent + rounded bars, zero brand recognition | Use real product images from brand protocol; honest placeholder as last resort |
| Inter/Roboto/Arial/system fonts as display | Too common, reader can't tell if this is a designed product or a demo | Brand spec explicitly uses them |
| GitHub-dark lazy fix: uniform deep blue `#0D1117` + generic cyan/purple neon glow | One specific combo that's爛大街 in SaaS/AI landing pages — not all dark is banned | Developer tool product where brand actually goes this direction |

## AI Tells (Forbidden Patterns)

Empirical signatures of LLM-generated design — hard bans as default moves. Override a specific tell only when the brief or brand spec calls for it, or the documented style direction explicitly features that device — and record the override in `DESIGN.md`. A default reach is the tell; a recorded choice is design.

**Visual & type**
- No neon / outer glows by default — inner borders or subtle tinted shadows instead
- No gradient text-fill on large headers; no custom mouse cursors
- No oversized screaming H1 — control hierarchy with weight and color, not raw scale
- No serif on data/UI layers — dashboards, tables, and dense product UI stay sans/mono; display-level serif is a style-direction decision, not a premium reflex
- No `<br>`-broken italicized headline splits as a default move
- No em-dash (`—`) as a design element; use plain hyphens in English copy (full-width Chinese dashes are punctuation, not a tell)

**Layout micro-labels**
- No version labels as hero eyebrows (`V0.6`, `BETA`, `EARLY ACCESS`) unless the brief is about launch status
- No section-number eyebrows (`00 / INDEX`, `001 · Capabilities`) — name the topic in plain language
- No `01 / 4` pagination on tiles; no `Scroll · 001` cues; no rotated vertical text as agency flourish
- Middle-dot (`·`) rationed: max 1 per metadata line, never the default separator
- No decorative colored status dots on every list / nav / badge — dots only for real semantic state
- No crosshair / hairline grid lines drawn purely as decoration

**Content & data (the "Jane Doe" effect)**
- No generic names ("John Doe", "Sarah Chan") — creative, locale-appropriate names
- No egg / generic-user-icon avatars — believable photo placeholders
- No fake-perfect numbers (`99.99%`, `50%`) — organic messy data (`47.2%`)
- No startup-slop brand names ("Acme", "Nexus", "SmartFlow") — invent contextual names that sound real
- No filler verbs ("Elevate", "Seamless", "Unleash", "Next-Gen") — concrete verbs only
- No "Quietly in use at" social-proof headers; no poetic section labels ("From the field") — plain functional labels

**Fake previews & assets**
- No div-based fake product UI (fake terminal / dashboard / task list) to simulate a screenshot — real or generated images, or none
- No fake version footers inside mock screenshots (`v0.6.2-rc.1`, `last sync 4s ago`)
- No broken Unsplash hotlinks — `https://picsum.photos/seed/{descriptive}/{w}/{h}`, generated images, or real assets

## What to Do Instead

- `text-wrap: pretty` + CSS Grid + advanced CSS: typography details are the "taste tax" AI can't fake
- Use `oklch()` or spec-existing colors — never invent new colors from thin air
- Prefer AI-generated images (Gemini/Flash/Lovart) over SVG hand-drawn; HTML screenshots only for precise data tables
- Use「」quotes for Chinese, not "" — typographic proof of human review
- One detail at 120%, everything else at 80%: taste = knowing where to be precise, not uniform effort

## Judgment Boundary

"Brand actually uses it" is the strongest exception. If brand spec says purple gradient, use it — it's brand signature, not slop.
