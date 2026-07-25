# Performance, Accessibility & Dark Mode Guardrails (Shared)

These bind every route at build time — not only at final verification.

## Motion & Performance

- Animate **only `transform` and `opacity`** — never `top` / `left` / `width` / `height`. Use `will-change` sparingly, only on elements that actually animate.
- Any non-trivial motion MUST honor `prefers-reduced-motion`: gate behind `@media (prefers-reduced-motion: no-preference)` or degrade to static. Infinite loops, parallax, and scroll-hijack collapse to static under reduced motion.
- Grain / noise filters go exclusively on fixed `pointer-events-none` pseudo-elements — never on scrolling containers; continuous GPU repaints destroy mobile FPS.
- Lazy-load anything below the fold. Motion libraries and Three.js are not small.
- Z-index only for systemic layers (sticky nav, modals, overlays, grain). No arbitrary `z-50` spam — document the scale.

## Core Web Vitals

- LCP < 2.5s (preload the hero image), INP < 200ms, CLS < 0.1 (reserve space for images, fonts, embeds).
- Run Lighthouse before declaring a page done.

## Dark Mode (dual-mode by default)

- Design **both modes from the start** for any consumer-facing web page. Skip only when the brief is print-emulating editorial, the user says so, or the chosen film/style language commits to a single mode (record it in `DESIGN.md`). Single-theme exhibits — decks, animations, prototypes, brand boards — default to one theme unless the brief says otherwise.
- Pick ONE token strategy per project and stick to it: Tailwind `dark:` variants, or CSS semantic variables (`--surface`, `--text-primary`…) swapped under `[data-theme="dark"]` / `prefers-color-scheme`.
- The brief and brand decide the actual colors. Enforced here: WCAG AA contrast (AAA for hero copy), hierarchy parity across modes, the brand color stays recognisable, no pure `#000000` / `#ffffff` — off-black and off-white keep depth.
- Default to system preference; add a manual toggle if either mode would lose key brand expression.
- **Page theme lock** — the page has ONE theme; sections do not invert mid-scroll (no warm-paper section inside a dark page). Set the theme once at the page root; section tints within the same family are fine (`zinc-950` next to `zinc-900`). A deliberate full theme switch is allowed at most once per page, and only when the brief calls for it.
- **Test in both modes before finishing.** Never ship a page seen in only one mode.
