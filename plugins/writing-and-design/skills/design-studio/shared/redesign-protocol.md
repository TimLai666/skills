# Redesign Protocol (Shared)

Misclassifying the mode is the single biggest source of bad redesign output — run this before touching anything that already exists.

## Detect the mode (first action)

- **Greenfield** — no existing site or deck, or full overhaul approved.
- **Redesign – Preserve** — modernise without breaking the brand. Audit first, extract brand tokens, evolve gradually.
- **Redesign – Overhaul** — new visual language on existing content. Greenfield for visuals; preserve content and information architecture.

If ambiguous, ask once: "Should this redesign preserve the existing brand, or are we starting visually from scratch?"

## Audit before touching

Document the current state first:

- Brand tokens — colors, type stack, logo treatment, radii. These seed `DESIGN.md`.
- Information architecture — page tree, primary nav, key conversion paths.
- Content blocks — what exists, what's doing work, what's filler.
- Patterns to preserve — signature interactions, recognisable hero, copy voice.
- Patterns to retire — AI-slop tells, broken layouts, dead links, generic stock imagery, perf traps.
- SEO baseline — ranking pages, meta titles, structured data, OG cards. **SEO migration is the #1 redesign risk.**

## Preservation rules (Preserve mode)

- Don't change information architecture unless asked — keep slugs, anchor IDs, and nav labels stable.
- Extract brand colors before recalibrating — a brand that is already purple stays purple.
- Preserve copy voice unless asked for a rewrite. Visual modernisation ≠ content rewrite.
- Honor existing accessibility wins — never regress focus states, alt text, keyboard nav, contrast.
- Respect existing analytics events — don't rename buttons, form fields, or section IDs that downstream tracking depends on.

## Modernisation levers (apply in order, stop when the brief is satisfied)

1. Typography refresh — biggest visual lift per unit of risk.
2. Spacing & rhythm.
3. Color recalibration — desaturate, unify neutrals, keep the brand accent.
4. Motion layer — restrained micro-interactions on existing components.
5. Hero & key-section recomposition.
6. Full block replacement — only when the existing block is unsalvageable.

Decision tree: IA, content and SEO sound → **targeted evolution** (levers 1–4), ~70% of the value at ~40% of the risk. Structural visual debt (broken IA, no design system, broken mobile) → **full redesign** with strict content preservation. The brand itself is changing → greenfield.

## Never change silently

URL structure and slugs, primary nav labels, form field names or order, the logo or wordmark, legal and consent copy — only with explicit user approval.
