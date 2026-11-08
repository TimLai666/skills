# Cinematic Slides: Compositions And Ornaments

Film-driven decks keep the director and film from workflow step 3 and translate them into slide composition and small ornaments. The deck itself is built as an HTML deck (`slide-decks.md`), exported to PDF, and to editable PPTX with `editable-pptx.md` when asked. Everything here is written so it survives that export.

## Medium Mapping: Film → Slide

| Web concept | Slide equivalent |
|---|---|
| Full-bleed hero section | Cover slide: dominant panel + oversized type |
| Section reveal / entrance | Composition hierarchy inside the slide (export drops animation) |
| Motion / parallax | Static tension: diagonal crop, asymmetric weight |
| Navigation bar | Chapter strip or top rule line, the same on every content slide |
| Page rhythm (spectacle → info → rest) | Slide rhythm (cover → argument → data → verdict → summary) |
| Atmospheric layer | Semi-transparent panel or tinted band behind the content |

## A Legible Main Visual On Every Slide

Every slide carries a picture of its content that passes the three-second test in `shared/composition-rules.md`: the teacup, the tea garden, the hand pouring water. Ornaments, rule lines and large numbers frame that picture; they never replace it. Process slides show each step as its own drawn action.

## Three Layers Per Content Slide

1. **Structure**: background color, panels, rule lines, the chapter strip.
2. **Content**: headings, text, tables, formulas.
3. **Accent**: verdict box, pull-quote bar, chapter tag.

A slide with only the content layer is not finished. A slide with only structure and accent has nothing to say.

## Ornaments

Small, repeated marks that make a deck feel directed. Pick two or three per deck and use them the same way on every slide that has them.

| Ornament | What it is | Rule |
|---|---|---|
| Chapter strip | A narrow band on the left or top edge carrying the chapter name. On the left edge, set CJK vertically (`writing-mode: vertical-rl`) and Latin as a small rotated label; on the top edge, set it horizontally | Same position and width on every content slide; text is the real chapter name, not a number code |
| Chapter tag | Small monospace label above the heading, letter-spaced | Names the topic in plain words; one per slide |
| Rule lines | Thin lines in the accent or muted token dividing panels | One weight across the deck; never decoration on top of content |
| Verdict box | Tinted box with a solid edge bar holding the decision or key result | Only on slides that state a decision or result |
| Pull-quote bar | Accent bar beside one quoted or emphasized line | At most one per slide |
| Footer rule | A hairline above the footer area | Footer holds source notes; the slide number comes from the deck shell, never hand-written on the slide |
| Corner mark | A small film-derived mark (frame corner, registration mark, aperture) in one corner | Same corner throughout; skip it if the film offers no fitting mark |

Export rules for ornaments (from `editable-pptx.md`):

- Build every ornament as a real element with its text inside `<p>` or `<h*>`; no `::before` / `::after` content, no background-image text.
- Rotated Latin labels may render differently in LibreOffice previews; check them in the PDF export.
- When an ornament cannot survive PPTX export, keep it in the HTML and PDF and say in the delivery note what the PPTX loses.

## Composition Families

Choose one per deck. Do not mix families.

| Family | Description | Best for |
|---|---|---|
| **Editorial split** | Picture panel + text column, rule divider; the picture panel takes 50–65% so the main visual stays legible | Academic, research, analytical, brand stories |
| **Monumental type** | Oversized heading dominates, data in a subordinate zone | Thesis-driven, keynote |
| **Archive wall** | Tight grid of data blocks, dark frame, specimen-card feel | Data-heavy, taxonomy |
| **Corridor** | Full-width dark band top and bottom, content in a lit center | Cinematic, dramatic |
| **Cover poster** | Left half solid dark, right half light, editorial title | Journal, dispatch, report |

## Color Discipline

- Extract four tokens from the film palette before building: background, primary, accent, muted.
- No more than four colors for type, panels, rules and ornaments; rule lines and borders count. Illustrations may use lighter and darker mixes of those tokens plus natural colors the subject needs (skin, wood, tea), so objects can carry base, shadow and highlight.
- Dark backgrounds belong on the cover and verdict or summary slides; content slides use the light background unless the film commits to dark. Dark bands that are part of the composition family (Corridor) are structure, not a dark background.
- The accent marks decisions, key results and chapter tags. It is not decoration.

## Typography

| Role | Direction | Notes |
|---|---|---|
| Deck title | Serif display from the film's type direction | Not centered unless the family is Corridor |
| Section heading | Same serif, bold | Left-aligned |
| Chapter tag | Monospace, small, letter-spaced | Uppercase for Latin |
| Formula / code | Monospace | The monospace is part of the cinematic signal |
| Body | Sans from `DESIGN.md` | Size floors from `content-guidelines.md` (slides ≥24px body at 1920×1080) |

## Slide Rhythm

```
Cover (spectacle)
  → Problem / data slides (information, two-column split)
  → Derivation slides (step progression)
  → Verdict slides (decision, dark accent)
  → Summary (echoes the cover)
```

Do not default to Title → Bullet → Bullet → Thank you. Mark each slide lead, support or pause (`shared/composition-rules.md`).

## Compiled Spec For Decks

Decks fill `compiled-spec.md` with the slide sequence, composition per slide, the chosen ornaments, the four color tokens, and the rhythm and shape tables. Entrance maps and per-section CSS/JS fields are `none (static deck)` unless the deck is presented live with animation.

## Checklist

- [ ] One composition family across the deck
- [ ] Every content slide has structure, content and accent layers
- [ ] Two or three ornaments chosen, used identically on every slide that has them
- [ ] Verdict boxes on every decision or key-result slide
- [ ] No hand-written slide numbers; the deck shell carries them
- [ ] Color stays within four tokens
- [ ] PDF export checked; PPTX losses listed when PPTX was requested
