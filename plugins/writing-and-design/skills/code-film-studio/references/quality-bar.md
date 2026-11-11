# The quality bar

Read this at stage 4 (the bar shot) and whenever the user asks why something looks wrong.

## The bar shot

1. Choose the shot the film depends on most. It is usually the hardest one: a face in close-up at the turn of the story.
2. Build only what that shot needs, at the highest level you can reach, with the full quality loop (SKILL.md).
3. Show it twice: one still at final size, and two to four seconds of it moving.
4. Tell the user what is still below what you wanted, and how many rounds it has had.
5. Their "yes, this level" fixes the bar. Record the still's path in `STATE.md` as the bar. Every later asset and shot is put beside it before it is shown.

If you cannot bring the bar shot to a level the user accepts, stop and say so before building more. Offer the routes in `building.md` (a different method, a different framing of the same moment, a stylised treatment). A film that changes its approach at shot one costs a day. A film that changes it at shot thirty costs everything.

## What "finished" means

| Element | Not finished | Finished |
|---|---|---|
| Face | built from a few dozen shapes, judged from the front only, expressions made by swapping whole heads | proportions checked against several references from front, three-quarter and profile; continuous expression controls (brows, lids, jaw, lip corners); eyes with cornea highlight, wet edge, lashes; skin with colour zones and fine surface detail; asymmetry |
| Body | limbs as separate rigid capsules | one skin over a skeleton, joints that bend without gaps, shoulders and hips that move with the limbs |
| Hands | mitten shapes, one pose | five fingers with joints, posed for each contact (holding, pressing, resting) |
| Hair | one hard shell | strands or layered cards with flyaways, a hairline that fades into skin |
| Clothes | colour painted on the body | separate cloth with thickness, folds at joints, a hem that hangs |
| Props | primitive shapes with flat colour | the object's real parts, bevelled edges, wear where hands touch, material that varies across the surface |
| Set | clean walls and a floor texture | what a real room accumulates: stains, cables, things left on surfaces, light switches, uneven edges |
| Motion | poses blended in a straight line; limbs through furniture or the floor; a joint bent the wrong way | weight shifts before a step, feet that stay planted, anticipation and settle, hands that arrive and stay, eyes that lead, breathing while still |
| Light | a few lamps and a fill | light that bounces, soft shadows with contact darkening, colour picked up from surfaces, exposure checked on a phone-sized image |
| Lip sync | mouth opens on a timer | mouth shapes matched to each syllable of the recorded line, jaw and lips separate |

A row counts as finished only when you have looked at it at film size and cannot name a difference from the references that a viewer would notice.

## Limit or effort

When the user asks why something looks unreal, answer in this shape. Fill both columns honestly; an empty "effort" column is almost never true.

| What they see | Limit of the method | What I have not done yet |
|---|---|---|
| (their words) | (what this route cannot do, and which route can) | (the specific work still missing, with how long it takes) |

Known limits, so you do not overpromise:

- **Realistic human faces in close-up** are the hardest thing in this craft. Public work by language-model agents shows strong scenes, objects and light; it does not show a photoreal face built from scratch. Start faces from a parametric human base and adjust it against references, rather than sculpting from nothing (`building.md`).
- **Browser path tracing** now handles hard-surface interiors well. Skin, hair and cloth are better in Blender Cycles, which has dedicated skin scattering and hair shading.
- **You see through small images.** Fine errors in a face can be invisible to you and obvious to the user. Ask them to look at crops.
- **You cannot hear.**

Known effort traps, because they were all fallen into once:

- stopping a face after a handful of rounds because the pace felt urgent,
- rendering at interactive speed when a minute per frame was affordable,
- building every shot roughly instead of one shot well,
- using no reference at all and adjusting numbers from imagination,
- leaving every material as procedural noise,
- calling the result a draft.

## Checks before anything is shown

- Brightness: measure it (`scripts/qc.py bright`). A film whose brightest tenth is near black reads as mud on a phone, however good the mood looked on a large monitor. Do this on a few test frames before any long render, not after.
- Look at a phone-sized copy.
- For motion: the penetration and joint-limit check over every frame of the shot (`building.md`, Bodies that obey the room) must come back empty, then a strip of frames across the action (`scripts/qc.py strip`) checked by eye for sliding feet and pops.
- Beside the bar: put the new still next to the bar still. If it is visibly below, it is not ready.
- The second pair of eyes (SKILL.md, the quality loop): a fresh reviewer's list of differences, not your own impression, decides whether something is ready to show.
