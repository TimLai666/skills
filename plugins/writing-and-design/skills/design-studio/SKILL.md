---
name: design-studio
description: >-
  Unified design skill for ALL design work — websites, apps, presentations,
  animations, prototypes, infographics, branding. Every session produces or
  evolves a DESIGN.md (Google format). Routes to cinematic-ui or huashu-design
  engines based on task. This skill MUST be used for any design task. MUST
  trigger on: 設計, design, 原型, prototype, PPT, 幻燈片, slides, 動畫, animation, 簡報,
  deck, landing page, website, UI, mockup, MP4, GIF, infographic, branding,
  logo, 評審, critique, film-inspired, cinematic.
metadata:
  version: "1.7.0"
---

# Design Studio

Unified design skill. One entry point, two engines, one design system file.

## DESIGN.md: The Design System File

Every design session MUST produce or evolve a `DESIGN.md` in the project root. This file is the single source of truth for the project's visual identity.

### Format

Follow the [Google DESIGN.md spec](https://github.com/google-labs-code/design.md). Structure:

```markdown
---
version: alpha
name: <Project Name>
colors:
  primary: "#hex"
  secondary: "#hex"
  tertiary: "#hex"
  neutral: "#hex"
typography:
  h1:
    fontFamily: <Font Name>
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
  body-md:
    fontFamily: <Font Name>
    fontSize: 16px
    fontWeight: 400
rounded:
  sm: 4px
  md: 8px
spacing:
  sm: 8px
  md: 16px
  lg: 32px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#fff"
---

## Overview
<Brand personality, audience, emotional intent>

## Colors
<Palette rationale and usage rules>

## Typography
<Type hierarchy and pairing logic>

## Layout
<Grid system, spacing rhythm>

## Elevation & Depth
<Shadows, layers, or flat alternatives>

## Shapes
<Corner radius language>

## Components
<Button, card, input, chip specs with token refs>

## Do's and Don'ts
<Guardrails>
```

### DESIGN.md Lifecycle

| Scenario | Action |
|----------|--------|
| No DESIGN.md exists | Copy `shared/DESIGN-template.md` to project root, rename to `DESIGN.md`, fill in during session |
| DESIGN.md exists, user says "redesign" / "重新設計" | Run `shared/redesign-protocol.md` first — detect Preserve vs Overhaul, audit the current state — then rewrite DESIGN.md accordingly |
| DESIGN.md exists, user wants changes | **Read first**, then expand/modify specific sections. Preserve unchanged tokens. |
| DESIGN.md exists, new task on same project | **Read first**, stay consistent with existing tokens unless user says otherwise |

**Iron rule**: Always read existing DESIGN.md before starting work. The design grows from what's already there, not from zero.

## Where Process Files Go

`DESIGN.md` is the only design file that belongs in the project root. Every working file a design session produces goes in `docs/design/`:

| File | Engine | Holds |
|------|--------|-------|
| `docs/design/decisions.md` | cinematic-ui | Phase 1 — director, film reference, shell-ban list, uniqueness audit |
| `docs/design/storyboard.md` | cinematic-ui | Phase 2 — scene-by-scene treatment |
| `docs/design/compiled-spec.md` | cinematic-ui | Phase 3 — the sole implementation source (web) |
| `docs/design/slide-spec.md` | cinematic-ui | Phase 3 — replaces compiled-spec.md for PPTX |
| `docs/design/product-facts.md` | huashu-design | Verified product facts gathered before designing |
| `docs/design/brand-spec.md` | shared | Frozen brand asset paths and extracted colors |

Create the directory if it does not exist. Bare filenames elsewhere in this skill and its sub-skills resolve against `docs/design/`.

These are session working state, not project assets. A user opening the repo root should see `DESIGN.md` and their own files, not six intermediate artifacts from one design run.

## Route Decision

After reading DESIGN.md (or deciding to create one), route to the right engine:

| Signal | Engine | Sub-skill |
|--------|--------|-----------|
| Director, film, cinema, editorial feel | **Cinematic** | `cinematic-ui/GUIDE.md` |
| High-end static website with visual narrative | **Cinematic** | `cinematic-ui/GUIDE.md` |
| Prototype, mockup, interactive demo | **Practical** | `huashu-design/GUIDE.md` |
| PPT, slides, deck, 簡報 | **Practical** | `huashu-design/GUIDE.md` |
| Animation, motion, MP4, GIF | **Practical** | `huashu-design/GUIDE.md` |
| Expert review, critique, scoring | **Practical** | `huashu-design/GUIDE.md` |
| Infographic, data visualization | **Practical** | `huashu-design/GUIDE.md` |
| App/iOS/Android prototype | **Practical** | `huashu-design/GUIDE.md` |
| Quick design variants (3 directions) | **Practical** | `huashu-design/GUIDE.md` |
| Ambiguous / "make something good" | **Practical** (Fallback advisor) | `huashu-design/GUIDE.md` |
| Brand materials with specific brand | **Either** — use shared brand protocol | Depends on output type |

**Ambiguous**: Ask one question: "Do you have a film or director in mind as visual reference, or want me to recommend directions?"

## Session Flow (this file drives every session)

1. **Context** — Read `DESIGN.md` if it exists (lifecycle table above); otherwise copy `shared/DESIGN-template.md`.
2. **Shared rules** — Read `shared/anti-slop.md`, `shared/hard-rules.md`, `shared/guardrails.md`, `shared/brand-asset.md`, `shared/verification.md`. They bind every route.
3. **Route** — Pick the engine from the Route Decision table, then read **only** that engine's GUIDE and run its workflow:
   - **Cinematic** → `cinematic-ui/GUIDE.md` — director + film → cinematic grammar → web structure, in 4 phases: decisions → storyboard → compiled-spec → build. Best for landing pages, brand websites, editorial layouts. References: `cinematic-ui/references/` (200 directors, hero archetypes, compositions, color grades).
   - **Practical** → `huashu-design/GUIDE.md` — task router → brand protocol → Fallback advisor → Junior Designer. Best for prototypes, presentations, animations, reviews, infographics. References: `huashu-design/references/` (40 styles, animation pitfalls, slide decks, critique guide).

   A GUIDE is an execution manual, not a separate skill: it runs inside this session, under the shared rules and the `DESIGN.md` context already loaded. This file stays in charge of steps 4–6.
4. **During design** — Extract tokens (colors, typography, spacing, components) from decisions into `DESIGN.md`.
5. **Before delivery** — Run `shared/verification.md`; make `DESIGN.md` reflect the final design, not the initial plan.
6. **On revisit** — Read `DESIGN.md` first. Expand, don't restart.

## Hybrid Tasks

When both engines apply, pick the one matching the **primary output**. Reference the other's principles where useful. Never mix workflows.

## PPTX

Both engines produce PPTX. Cinematic uses PptxGenJS natively. Practical uses HTML deck → PptxGenJS export. Read the PPTX reference from the chosen route.
