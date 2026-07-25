# Layout, States & Content Hard Rules (Shared)

Mechanical quality floors — failing any of these is shipping broken work, not a style choice. Each rule binds where its subject exists: output with no nav, hero, or form simply skips those clauses.

## Interactive states & forms

- LLMs default to "static successful state only". Always implement the full cycle: **loading** (skeleton loaders matching the final layout — not generic spinners), **empty** (beautifully composed, tells the user how to populate), **error** (inline for forms; toasts only for transient), **tactile** (`:active` gets `scale-[0.98]` or a 1px translate).
- **Button contrast check** — every CTA passes WCAG AA (4.5:1 body, 3:1 for 18px+). White-on-white buttons, transparent buttons with no border against the page, ghost buttons over photos without a scrim: all banned.
- **CTA wrap ban** — button text fits on one line at desktop. Primary CTA labels: 3 words max. Fix by shortening the label or widening the button.
- **One label per intent** — "Get in touch" + "Contact us" + "Let's talk" on one page is a fail. Pick one label per intent (contact / signup / portfolio…) and reuse it everywhere: nav, hero, footer.
- **Form contrast** — inputs, placeholders, focus rings, helper and error text all pass WCAG AA against the section background.
- Label ABOVE input; error text below; no placeholder-as-label, ever.

## Layout discipline

- **Hero fits the initial viewport**: headline ≤2 lines, subtext ≤20 words and ≤4 lines, CTAs visible without scrolling. If the copy doesn't fit, the value-prop is unclear — cut copy or reduce font scale, never overflow.
- **Hero stack: max 4 text elements** — (zero or one) eyebrow OR brand strip, headline, subtext, CTAs (1 primary + ≤1 secondary). Taglines under CTAs, trust micro-strips, pricing teasers, feature bullets, avatar rows: banned in the hero — they get their own sections below.
- Hero top padding cap ≈6rem (`pt-24`) at desktop. "Trusted by" logo walls go UNDER the hero, never inside it.
- **Navigation**: single line at desktop, height ≤80px (default 64–72px). A two-line desktop nav is broken.
- **Bento cell count = content count.** 3 items → 3 cells (1+2, 2+1, asymmetric trio). An empty filler tile means the grid was planned wrong — reshape it.
- **Layout-family repetition ban**: each layout family (3-col cards, full-width quote, split text-image…) appears at most ONCE per page; an 8-section page needs ≥4 families. **Zigzag cap**: max 2 consecutive image/text splits — the 3rd in a row is a fail.
- **Eyebrow restraint (the #1 violated rule)**: max 1 eyebrow per 3 sections, hero included. Mechanical check: count `uppercase tracking` labels above headlines; if count > ceil(sections/3), fail. Default fix: drop the eyebrow — the headline is enough.
- **Split-header ban by default**: "big headline left + small explainer right" section headers are banned unless the right column carries a real visual or interactive element. Stack vertically instead, body max-width 65ch.
- **Bento background diversity**: any multi-cell grid needs 2–3 cells with real visual variation (image, brand gradient, pattern, tint) — not 6 white-on-white text cards.
- **Explicit mobile collapse**: every multi-column layout declares its `<768px` fallback in the same component. No "Tailwind will handle it".

## Content density

- Default shape per section: headline ≤8 words + sub ≤25 words + one visual OR one CTA. More must be justified by the section's job.
- **No data dumps**: a 20-row table or 30-row list on a marketing page is the wrong layout. Use top 3–5 highlights + "view full list", a marquee/carousel, or a separate page.
- **Lists over 5 items need a different component, not a longer list**: grouped 2-col split, card grid, tabs/accordion, scroll-snap pills, carousel, marquee. A spec sheet with a hairline under every row is the worst default — group into 2–3 clusters, card-per-spec, or featured-vs-rest with a disclosure.
- **Fake-precise numbers**: from real data → fine; explicitly labeled mock → fine; AI-invented spec aesthetics (`5.8 mm`, `4.1×`) → banned.
- **One copy register per page** — don't mix technical mono, editorial prose and marketing punch unless the brand voice calls for it.
- **Copy self-audit (mandatory before ship)**: re-read every visible string — headlines, buttons, captions, alt text, footer, error messages. Rewrite anything grammatically broken, with unclear referents, or that reads like an LLM trying to sound thoughtful. When unsure, replace it with a plain functional sentence: AI-cute copy is worse than boring copy.
