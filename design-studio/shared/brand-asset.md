# Brand Asset Protocol (Shared)

From huashu-design, adopted by cinematic-ui for any project involving real brands.

## Trigger

Two categories (both count):
1. **Making materials FOR a brand** (DJI launch animation, Stripe landing page...)
2. **Design SHOWS recognizable products/brands** — comparison, ranking, review, intro deck, listing multiple products side by side

**Iron rule**: If a recognizable product/brand name appears in the design, its official logo is a REQUIRED asset. Not "use if available, skip if not."

**Even in Fallback advisor mode**: Category 2 still applies. Fallback decides visual style, does NOT exempt collecting named product logos. Two parallel tracks, not either/or.

## Core Principle: Assets > Specs

Logo / product images / UI screenshots matter more than brand color values.

## 5-Step Hard Process

| Step | Action | Fallback |
|------|--------|----------|
| 1. Ask | One complete asset list (logo / product images / UI screenshots / palette / fonts /禁区) | — |
| 2. Search official channels | brand.com/brand, brand.<brand>.com, <brand>.com/press, Wikimedia | — |
| 3. Download assets | Three fallback paths per asset type (SVG → official HTML → product screenshots) | Try next path immediately on failure |
| 4. Verify + extract | Grep color values, cross-check logo/image authenticity | — |
| 5. Freeze as `brand-spec.md` | Template covering all asset paths (logo / product images / UI / palette / typeface /禁区 / tone) | — |

## Self-Check Gate

Before any build, confirm core assets are in place:
- Physical products → product images (not CSS silhouettes)
- Digital products → logo + UI screenshots
- Color values extracted from real HTML/SVG

Missing = stop and supplement. Don't hardcode without assets.

## Logo Sub-Gate (for comparison/ranking/review decks)

List every product/brand name that will appear. Confirm each has official logo embedded. One missing = STOP and supplement. Delivery format is single-file HTML → logos must be base64 inline.

## Fetch Script

```bash
python3 scripts/fetch_images.py --query "keyword1" "keyword2" --out project/assets/img --count 2 --width 1600
```

## Image Honesty Test

After getting an image: "If I remove this image, does information suffer?" If no → it's decoration = slop, don't add it.
