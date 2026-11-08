# Verification Protocol (Shared)

Step 5 of the workflow. Run every check that applies to the output type before delivery. On a Claude Design canvas, follow the canvas rule in `references/claude-design.md`: screenshot and render checks only when the user asks; the AI-look checklist is applied to `compiled-spec.md` before writing the artboards.

## Browser Checks

Screenshot every page at 375px and 1440px wide (slides at 1920×1080). Look at the screenshots, not only the code.

```bash
python3 scripts/verify.py path/to/output.html
```

`scripts/verify.py` screenshots 1440×900 and 375×812, checks horizontal overflow and collects page and console errors (needs `pip install playwright`; it falls back to the local Chrome when Playwright's browser is not installed; usage: `--help`). Zero `pageerror` entries and no horizontal overflow at delivery. Detailed browser checks: `references/verification.md`.

Then run the deterministic anti-pattern detector when it is available:

```bash
npx impeccable detect <output-dir-or-file>
```

If the detector cannot run, say so and apply the AI-look checklist by hand.

## AI-Look Checklist

Answer each item against the screenshots. Any "yes" is a fix before delivery, unless `DESIGN.md` records the direction choosing it on purpose.

1. Does any section or slide fail the three-second test, or use abstract shapes (dots on a line, plain circles, color blocks) as its main visual (`shared/composition-rules.md` Legible Visuals)?
2. Is any lead section missing two supporting details, or does the page feel sparse?
3. Are illustrations only uniform outlines with flat fills, without shading, brushwork or texture (`references/illustration-craft.md`)?
4. Do most cards share one radius and one soft drop shadow?
5. Do cards or buttons lift or grow a shadow on hover by default?
6. Are there line icons inside circles or rounded squares that repeat the label?
7. Are there more than two pause sections, or a pause right after the hero (`shared/composition-rules.md`)?
8. Is there no depth layer on a website or landing page, or only paper grain?
9. Purple-blue gradients, neon glow, emoji icons, or a left-border accent card (`shared/anti-slop.md`)?
10. Inter, Roboto, Arial or a system font in display positions?
11. A section-number eyebrow, a version label, or `Scroll · 001` style cues?
12. Invented stats, testimonials or fake product UI used as decoration?
13. Copy that reads like an LLM trying to sound thoughtful (`shared/hard-rules.md` copy self-audit)?
14. Could the hero swap into a different product's page without anyone noticing? If yes, the form did not come from the content.

## WebGPU Effects

When the page uses a WebGPU, WebGL or canvas effect:

```bash
node scripts/verify_webgpu.mjs path/to/output.html
```

It screenshots the WebGPU path, the forced WebGL 2 path and the reduced-motion static path, and reports frame times. All three must look finished. Thresholds and details: `references/webgpu-effects.md`.

## Video Export

For animation outputs that require audio:

```bash
ffprobe -select_streams a output.mp4
```

Confirm the required audio stream is present, then listen for intelligibility, synchronization and clipping. For intentionally silent delivery, verify the visual output against the agreed use and format; an audio stream is not required.

## QA Checklist Before Delivery

1. Visual inspection: every section or slide seen in a screenshot at both widths
2. Console errors: zero `pageerror` entries
3. AI-look checklist: every item answered, fixes applied
4. Anti-pattern detector: flags resolved, or recorded as not run
5. Responsive and reduced motion: layout holds at 375px, motion collapses to static
6. Brand assets: all named products have logos embedded
7. Typography: no generic fallback fonts in display positions
8. Color: all colors from the spec, no invented colors
9. Content: no fabricated stats, quotes or data as decoration
10. Dark mode: page checked in both modes (see `guardrails.md`)
11. Copy self-audit done (see `hard-rules.md`)
12. WebGPU effects: all three paths checked when used
