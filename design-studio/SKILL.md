---
name: design-studio
description: 'Unified design skill for ALL design work — websites, apps, presentations, animations, prototypes, infographics, branding. Every session produces or evolves a DESIGN.md (Google format). Routes to cinematic-ui or huashu-design sub-skills based on task. Triggers: 設計, design, 原型, prototype, PPT, 幻燈片, slides, 動畫, animation, 簡報, deck, landing page, website, UI, mockup, MP4, GIF, infographic, branding, logo, 評審, critique, film-inspired, cinematic.'
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
| DESIGN.md exists, user says "redesign" / "重新設計" | Rewrite from scratch, replacing all tokens and rationale |
| DESIGN.md exists, user wants changes | **Read first**, then expand/modify specific sections. Preserve unchanged tokens. |
| DESIGN.md exists, new task on same project | **Read first**, stay consistent with existing tokens unless user says otherwise |

**Iron rule**: Always read existing DESIGN.md before starting work. The design grows from what's already there, not from zero.

## Route Decision

After reading DESIGN.md (or deciding to create one), route to the right engine:

| Signal | Engine | Sub-skill |
|--------|--------|-----------|
| Director, film, cinema, editorial feel | **Cinematic** | `cinematic-ui/SKILL.md` |
| High-end static website with visual narrative | **Cinematic** | `cinematic-ui/SKILL.md` |
| Prototype, mockup, interactive demo | **Practical** | `huashu-design/SKILL.md` |
| PPT, slides, deck, 簡報 | **Practical** | `huashu-design/SKILL.md` |
| Animation, motion, MP4, GIF | **Practical** | `huashu-design/SKILL.md` |
| Expert review, critique, scoring | **Practical** | `huashu-design/SKILL.md` |
| Infographic, data visualization | **Practical** | `huashu-design/SKILL.md` |
| App/iOS/Android prototype | **Practical** | `huashu-design/SKILL.md` |
| Quick design variants (3 directions) | **Practical** | `huashu-design/SKILL.md` |
| Ambiguous / "make something good" | **Practical** (Fallback advisor) | `huashu-design/SKILL.md` |
| Brand materials with specific brand | **Either** — use shared brand protocol | Depends on output type |

**Ambiguous**: Ask one question: "Do you have a film or director in mind as visual reference, or want me to recommend directions?"

## Shared Rules (Read Before Any Route)

- `shared/anti-slop.md` — AI slop avoidance
- `shared/brand-asset.md` — Brand asset 5-step protocol
- `shared/verification.md` — Quality checks before delivery

## Design Session Workflow

1. **Check for DESIGN.md** in project root. If exists → read it. This is your design context.
2. **Route** to cinematic-ui or huashu-design based on task.
3. **During design**: Extract tokens (colors, typography, spacing, components) from decisions and write them into DESIGN.md.
4. **After delivery**: Ensure DESIGN.md is complete and accurate. It should reflect the final design, not just the initial plan.
5. **On revisit**: Read DESIGN.md first. Expand, don't restart.

## Sub-Skill Details

### Cinematic → `cinematic-ui/SKILL.md`

Director + film → cinematic grammar → web structure. 4 phases: decisions → storyboard → compiled-spec → build. Best for: landing pages, brand websites, editorial layouts. References: `cinematic-ui/references/` (200 directors, hero archetypes, compositions, color grades).

### Practical → `huashu-design/SKILL.md`

Task router → brand protocol → Fallback advisor → Junior Designer. Best for: prototypes, presentations, animations, reviews, infographics. References: `huashu-design/references/` (40 styles, animation pitfalls, slide decks, critique guide).

## Hybrid Tasks

When both engines apply, pick the one matching the **primary output**. Reference the other's principles where useful. Never mix workflows.

## PPTX

Both engines produce PPTX. Cinematic uses PptxGenJS natively. Practical uses HTML deck → PptxGenJS export. Read the PPTX reference from the chosen route.
