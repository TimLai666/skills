# Composition Rules (Shared)

Rules every page-type output records in `compiled-spec.md` and the build must follow. Decks, animations and app prototypes apply them where noted.

## Legible Visuals

Every section and every slide shows its content in a picture the reader understands without reading the copy.

- **Three-second test**: someone who has not read the text can say what the main visual shows (a teacup, a mountain tea garden, a hand pouring water) within three seconds. A line with dots, a plain circle, or a color block fails as the main visual of a section about something concrete.
- **Processes and steps**: each step gets its own depiction of the action or the object involved (the cup being warmed, leaves on a scale, a kettle and a timer), with its label. A step is never only a marker on a line.
- **Products and places**: show the thing itself (the leaves, the brewed tea in a cup, the tea garden on the slope), not a symbol for it.
- **When no photos are available**, draw illustrations: inline SVG, CSS, canvas or WebGPU, in **one illustration style derived from the direction** (for example ink wash for a Taiwanese tea brand, engraving lines, cut paper, a film-still look). Anything can be drawn: people, faces, hands, named real products, landscapes, interiors, still lifes.
- **Illustrations carry brushwork**: brush edges, stippling, hatching, grain or washes, and every object has base, shadow and highlight. Outline-plus-flat-fill alone is not finished. Techniques and code: [../references/illustration-craft.md](../references/illustration-craft.md).
- Abstract geometry, large type and color fields support the main visual; they do not replace it.

## Richness

- Lead sections combine the main visual with at least two supporting details that carry content: a label, a number, a secondary illustration, a caption, a texture of the scene.
- Pages and decks feel populated from top to bottom. Richness comes from illustration, atmosphere and real content, never from a uniform card grid (see Shape Language).
- The direction's atmosphere (light, haze, film grain, motion) runs through the whole page, not only the hero.

## Section Rhythm

Mark every section in the spec as one of three weights:

| Weight | What it holds |
|--------|---------------|
| **Lead** | One legible main visual that fills the first viewport or most of the section: an illustration or image of the content, a scene, an object the reader can operate, with display type beside it |
| **Support** | A smaller legible visual with explanatory copy beside or under it |
| **Pause** | One sentence or one small element, used as a breath between heavier sections |

- At most **two pause sections per page**. Every lead and support section has one legible main visual (see Legible Visuals).
- Two pause sections never sit next to each other, and a pause never follows the hero directly.
- Vertical padding of a section stays proportional to its content: a pause section is not taller than one viewport at 1440×900.
- Decks: mark each slide the same way; a run of more than two pause slides fails.

Spec table:

| Section | Weight | Subject |
|---------|--------|---------|

## Depth Layer

Websites and landing pages carry at least one layer that shows distance or light: fog or haze, a light source, foreground and background planes moving or overlapping, a 3D object, a WebGPU or canvas atmosphere.

- Paper grain, noise or a flat texture alone does not count.
- A **Practical** direction may meet this with color planes that overlap or separate in front and behind each other, or a cast shadow that belongs to the direction; it does not need fog or glow.
- Slides, animations and app prototypes choose depth per direction; it is not required.
- When the depth layer is a WebGPU or canvas effect, follow [../references/webgpu-effects.md](../references/webgpu-effects.md), including the static fallback.

Spec table:

| Page | Depth carrier | Fallback without motion or GPU |
|------|---------------|--------------------------------|

## Shape Language

Radius, shadow and border are design decisions derived from the direction and written into `DESIGN.md` (`rounded`, elevation notes) before the build.

- No uniform rounded-card-plus-drop-shadow system: cards that all share one radius and one soft shadow are the default AI look.
- Cards do not lift (`translateY`) or grow their shadow on hover by default. Hover feedback comes from the direction: a color shift, an underline, an image change.
- No line icons inside circles or rounded squares as decoration. Use an icon only when it carries information the label does not.
- A shadow, when used, must have a source the direction explains (a light direction, a stacked paper, a lifted object), and stays consistent across the page.
- Mixing radii is allowed only as a stated rule (for example sharp containers, round media).

Spec table:

| Element | Radius | Shadow / border | Hover |
|---------|--------|-----------------|-------|

## Motion Budget

- At most one heavy interaction and two attention-seeking reveals per page.
- `fadeUp` (`opacity` + `translateY`) at most twice per page; adjacent sections do not reveal the same way.
- Scroll-driven effects use CSS scroll-driven animations, GSAP ScrollTrigger or IntersectionObserver; never a raw `window` scroll listener.
- A progress line may cue a hero that only moves on scroll. No decorative scroll labels.
