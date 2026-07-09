# Verification Protocol (Shared)

Both skills enforce verification before delivery. Use all applicable checks.

## Browser Verification (Both Skills)

### Playwright Screenshot
```bash
npx playwright screenshot file:///path/to/output.html out.png --viewport-size=1440,900
```
For PPTX/deck output: `--viewport-size=1920,1080`

### Console Error Check
```bash
npx playwright test --reporter=list
```
Or manual: open in browser, check DevTools console for `pageerror` entries. Zero tolerance for `pageerror` in delivery.

## Anti-Pattern Detection (cinematic-ui)

After first build passes visual inspection:
```bash
npx impeccable detect <output-dir-or-file>
```
Fix all flagged issues (overused fonts, purple gradients, nested cards, bounce easing, low-contrast text, flat type hierarchy, side-tab borders, icon-tile stacking).

## Verify Script (huashu-design)

```bash
python3 scripts/verify.py
```
Wraps Playwright for automated checks.

## Video Export Verification (huashu-design)

For animation outputs:
```bash
ffprobe -select_streams a output.mp4
```
Must show audio stream. No audio = half-finished product.

## QA Checklist Before Delivery

1. Visual inspection: open in browser, check every section/slide
2. Console errors: zero `pageerror` entries
3. Anti-pattern detector: all flags resolved
4. Responsive/reduced-motion: basic handling present
5. Brand assets: all named products have logos embedded
6. Typography: no generic fallback fonts in display positions
7. Color: all colors from spec, no invented colors
8. Content: no fabricated stats/quotes/data as decoration
