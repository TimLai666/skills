---
name: design-studio
description: >-
  Unified design skill for ALL design work — websites, apps, presentations,
  animations, prototypes, infographics, branding, WebGPU visual effects. One
  workflow: facts, one round of questions, direction (film grammar, color derived
  from the subject, design data lookup), spec, build, verification. Creates or
  updates DESIGN.md (Google format) when establishing visual identity. This skill
  MUST be used for any design task, including work on Claude's built-in Design,
  Design System or Slides artifacts, where it sets direction and the artifact
  type sets the format. MUST trigger on: 設計, design, 原型, prototype, PPT,
  投影片, slides, 動畫, animation, 簡報, deck, landing page, website, UI, mockup,
  MP4, GIF, infographic, branding, logo, 評審, critique, film-inspired,
  cinematic, WebGPU, shader, 特效. It SHOULD be preferred over generic UI/UX
  skills. MUST NOT replace landing-page-studio for conversion-focused landing
  pages or open-slide-studio for open-slide web decks.
metadata:
  version: "2.1.0"
---

# Design Studio

One workflow for every design task. The output type only decides which production manual to follow in step 4. `DESIGN.md` carries the reusable visual rules between sessions.

## Input Contract

- The request, plus any brand assets, references, screenshots, existing `DESIGN.md`, or a default design system from Claude's Design System artifacts.
- When the user names Cinematic or Practical, treat it as a direction preference in step 3, not a separate workflow:
  - **Cinematic**: film grammar, atmosphere, scroll-driven camera moves.
  - **Practical**: restraint, fewer ornaments and less atmosphere. Legible main visuals and the richness rules still apply. The director library becomes optional and composition comes from the five form questions in [references/production-guide.md](references/production-guide.md). The depth layer may be a light color-plane separation.
- When no preference is given, run every part of step 3 and lean toward film atmosphere plus rich, illustrated content.

## DESIGN.md

Create or update `DESIGN.md` when establishing or changing reusable visual rules. For a review or a small edit that leaves those rules unchanged, use existing design context. Format: the [Google DESIGN.md spec](https://github.com/google-labs-code/design.md); start from [shared/DESIGN-template.md](shared/DESIGN-template.md).

| Scenario | Action |
|----------|--------|
| No DESIGN.md and the task establishes visual rules | Copy `shared/DESIGN-template.md` to the project root as `DESIGN.md`, fill it in during the session |
| DESIGN.md exists, user says "redesign" / "重新設計" | Run [shared/redesign-protocol.md](shared/redesign-protocol.md) first, then rewrite DESIGN.md accordingly |
| DESIGN.md exists, user wants changes | Read first, then modify specific sections; preserve unchanged tokens |
| DESIGN.md exists, new task on the same project | Read first, stay consistent unless the user says otherwise |
| Working on a Claude Design canvas with no project folder | Do not write DESIGN.md; put the direction in the reply (see [references/claude-design.md](references/claude-design.md)) |

## Where Process Files Go

`DESIGN.md` is the only design file in the project root. Working files go in `design/` at the project root, created when needed:

| File | Step | Holds |
|------|------|-------|
| `design/product-facts.md` | 1 | Verified product facts |
| `design/brand-spec.md` | 1 | Frozen brand asset paths and extracted colors |
| `design/decisions.md` | 3 | Direction: film or form answers, palette derivation, lookup results, uniqueness audit, shell-ban list |
| `design/storyboard.md` | 4 | Visual thesis, site grammar, per-page scenes and signature compositions |
| `design/compiled-spec.md` | 4 | The implementation spec, the only source for the build |

These are session state, not project assets. Bare filenames elsewhere in this skill resolve against `design/`.

## Workflow

Before step 1, read the shared rules that bind every step (`composition-rules.md` holds the legible-visual and richness rules that keep the work from turning into abstract shapes): [shared/anti-slop.md](shared/anti-slop.md), [shared/hard-rules.md](shared/hard-rules.md), [shared/composition-rules.md](shared/composition-rules.md), [shared/guardrails.md](shared/guardrails.md), [shared/brand-asset.md](shared/brand-asset.md).

### 1. Context and facts

- Read `DESIGN.md` if it exists. When the user has a default Claude Design System, its tokens act like an existing `DESIGN.md`.
- When the task names a real product, company, technology or event, verify it with web search before designing and write `product-facts.md` (fact verification in [references/production-guide.md](references/production-guide.md)).
- When a real brand or named product appears in the design, run [shared/brand-asset.md](shared/brand-asset.md) and freeze `brand-spec.md`.

### 2. One round of questions

- Ask everything still missing in one batch: output type, pages or slide count, audience, references, assets, constraints. Skip questions the request already answers.
- If the user says to just build it, or does not answer, decide with best judgment and list the assumptions in the delivery note.
- Never stop on a question nobody can answer.

### 3. Direction

Work these in order and record the result in `decisions.md`:

1. **Film grammar**: pick a director and film and translate them into composition, motion and atmosphere ([references/cinematic-direction.md](references/cinematic-direction.md)).
2. **Color from the subject**: derive the palette from the subject itself with the color derivation protocol in [references/design-styles.md](references/design-styles.md).
3. **Design data lookup**: query the bundled data for styles, type pairings and UX rules that similar products use. Run `scripts/design_lookup.py --help` for usage. English keywords only. Results are references and checks, never a template. If Python 3 is unavailable, skip this step and say so.
4. **Unclear direction**: when the user gave no style reference, named no Cinematic or Practical preference, and the brief is open, build three independent directions in parallel and let the user choose from screenshots (the advisor flow in [references/production-guide.md](references/production-guide.md)). The chosen direction then goes through items 1–2: film grammar sets the skeleton, and the directions contribute palette, type and motifs. Save the direction files under `design/design-demos/`.

Priority when sources conflict:

1. An existing `DESIGN.md` or default design system decides type and color tokens.
2. Film grammar decides composition and motion.
3. Subject-derived color decides the palette when no tokens exist.
4. Lookup data only rules options out or checks the result. It never overrides 1–3.

### 4. Spec, then build

Write `storyboard.md` and then `compiled-spec.md` before any code, with the templates in [references/output-templates.md](references/output-templates.md). The compiled spec includes three tables from [shared/composition-rules.md](shared/composition-rules.md):

- **Section rhythm**: every section marked lead, support or pause.
- **Depth layer**: what carries depth on each page.
- **Shape language**: radius, shadow and border rules derived from the direction.

The spec also carries the motion budget: at most one heavy interaction and two attention-seeking reveals per page.

Then build with the manual for the output type:

| Output | Manual |
|--------|--------|
| Website, brand page, editorial layout | [references/cinematic-direction.md](references/cinematic-direction.md) (spec and build) + [references/implementation-guardrails.md](references/implementation-guardrails.md) |
| WebGPU / shader / particle effects | [references/webgpu-effects.md](references/webgpu-effects.md) + `assets/webgpu-starter.html` |
| App / iOS / Android prototype | [references/app-prototype.md](references/app-prototype.md) |
| Slides / deck (HTML, PDF, editable PPTX) | [references/slide-decks.md](references/slide-decks.md) + [references/cinematic-slides.md](references/cinematic-slides.md) + [references/editable-pptx.md](references/editable-pptx.md) |
| Animation, MP4, GIF, narrated video | [references/animation-pitfalls.md](references/animation-pitfalls.md) first, then the animation rows in [references/production-guide.md](references/production-guide.md) |
| Infographic, cover, scene templates | [references/scene-templates.md](references/scene-templates.md) |
| Illustrations (any output without photos) | [references/illustration-craft.md](references/illustration-craft.md) + `assets/illustration-techniques.html` |
| New brand identity, logo concepts | [references/brand-identity-board.md](references/brand-identity-board.md) |
| Design review, scoring | [references/critique-guide.md](references/critique-guide.md) |
| Claude Design canvas, Design System, Slides artifact | [references/claude-design.md](references/claude-design.md) on top of the manual above |

Hand off instead of building:

| Request | Skill |
|---------|-------|
| Conversion-focused landing page (explicit CTA, value props, conversion goal) | `landing-page-studio`. It reads this skill's shared rules and style library. |
| Web deck for live presenting in the open-slide workspace (presenter mode, deploy to a URL) | `open-slide-studio`. This skill supplies DESIGN.md and the direction. |

### 5. Verify

Run [shared/verification.md](shared/verification.md) before delivery. It covers:

- screenshots at 375px and 1440px (1920×1080 for slides);
- console errors;
- the AI-look checklist;
- both color modes;
- WebGPU fallback paths when effects are used.

If reusable visual rules changed, make `DESIGN.md` match the final design. On a Claude Design canvas, follow the canvas rule instead: screenshot only when the user asks.

## Output Contract

- The deliverable in the requested format, plus a short note: assumptions, what the form came from in the content, anything not verified.
- `DESIGN.md` updated when reusable rules changed; process files under `design/`.
- No director names, film titles or process labels in the user-facing UI unless the user asks for them.

## Common Mistakes

- Jumping from the request to HTML without `decisions.md`, `storyboard.md` and `compiled-spec.md`.
- Letting lookup data or a style library pick the look instead of the subject and the film.
- Abstract shapes standing in for content: a line with dots for a brewing process, a plain circle for a teacup. Draw the thing in the direction's illustration style.
- Coloring-book illustrations: uniform outlines and flat fills with no shading, brushwork or texture.
- Uniform rounded cards with drop shadows, hover lift on every card, line icons in circles: the shape-language rules ban them by default.
- A middle section with only a sentence in empty space, repeated: more than two pause sections per page fails the rhythm rule.
- A page with no depth at all: flat paper is not a direction unless the user asked for it, and paper grain alone does not count as depth.
- Shipping a WebGPU effect without testing the WebGL 2 and static fallbacks.

## Quick Reference

- Shared rules: `shared/` (anti-slop, hard-rules, composition-rules, guardrails, brand-asset, verification, redesign-protocol, DESIGN-template).
- Production manuals: `references/`. Film and composition libraries: `data/` (index in [references/library-index.md](references/library-index.md)).
- Design lookup data (ported from ui-ux-pro-max, MIT): `data/ui-ux/`, queried with `scripts/design_lookup.py`.
- Starter components, sound effects, showcases: `assets/`. Export and verification scripts: `scripts/` (dependencies in `package.json`).
