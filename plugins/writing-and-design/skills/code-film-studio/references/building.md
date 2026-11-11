# Building things

Read before modelling, painting, lighting or animating.

## Code or software

The rule: if code you write yourself reaches the same result, use code. Use other software only where it is clearly better, and only software you can drive from a script. Never drive a tool that needs an account, a cloud service or a generative model unless the user asked for that.

| Stage | Use | Why |
|---|---|---|
| Rooms, furniture, hard-surface props | code: built from parts by your own scripts | props are a few lines of geometry each; in a film without realistic people, three.js with a path tracer renders them well |
| Human bodies, faces, hands | Blender through Python, with the MPFB add-on as the base | a parametric human starts out looking like a person, with skeleton, fingers and skin; output is CC0 |
| Rendering, when realistic people are in the film | Blender Cycles, driven by Python | dedicated skin scattering, hair shading and fine displacement; nothing in the browser matches it yet |
| Cloth | Blender cloth simulation, baked | a solver you would otherwise spend weeks rewriting |
| Body motion | code: key poses plus procedural layers, with motion-capture clips where the licence allows | see Motion below |
| Lip sync | code, timed by hand to the recorded line | automatic tools assume English |
| Materials | CC0 scans from Poly Haven and ambientCG where one fits; painted by you otherwise | both have open download APIs |
| Compositing, titles, subtitles, editing, sound | code and ffmpeg | equal to the tools, and reproducible |

**One renderer per film.** People must be lit by the same light as the room they stand in, so once realistic people need Cycles, the whole film is rendered there: build the set with Python scripts inside Blender instead of in three.js. You still only write code; Blender supplies the renderer, the human base, the skeleton, hair and cloth. Keep the three.js route for films without realistic people, for stylised films, and for a fast layout pass (stage 3).

### How Blender is installed: the application, run without its window

Decision: install the **Blender application** and run it headless (`blender -b -P script.py`, or `-b file.blend -P script.py`). Do not default to the pip package `bpy`.

Why the application:

- It carries its own Python, so there is no version to match. The pip package supports exactly one Python version per Blender release and fails on any other.
- Add-ons install the supported way (`blender --command extension install-file ...`). The human base (MPFB) is an add-on; getting add-ons to load inside the bare pip module is the least documented path.
- The user can open the `.blend` file and look at the scene themselves. With the pip package nothing can be opened by a person.
- It is the path the documentation, the forums and every tutorial assume, so errors have known answers.

The pip package stays as the fallback for a machine where an application cannot be installed (a server, no admin rights). It is smaller (about 250 MB against roughly 1 GB installed), and that is its only advantage here.

Rules that go with the decision:

- Ask before installing; say the size. Use the newest long-term-support release that the add-ons you need support, and write the exact version and the path to the executable in `STATE.md`. Do not trust a version number written in this file.
- You never click in the window. Everything is a script kept in the film folder (`blender/` next to `engine/`), so the film can be rebuilt from scripts alone.
- Save a `.blend` per shot or per asset as the scripts' output, so the user can open it.
- **Prove the route before building on it.** First session on a machine: one script that creates a human with the add-on, puts a light and a camera on it, renders one frame at film size on the GPU, and prints the seconds it took. If any step fails headless, fix or switch route now. That number, times the frame count, is the render time you tell the user.
- Neither route was tested when this was written. Treat the first run as the test and correct this section from what happens.

### Who installs what

The user does not install anything by hand. You do it, by command, after one approval that lists every item with its size and source:

| Item | What it is | Notes |
|---|---|---|
| Blender application | the renderer and everything around it | from blender.org; macOS `.dmg` copied to /Applications, Windows installer or zip, Linux tarball |
| MPFB add-on | the parametric human | download the release zip yourself and install it from the file with Blender's extension command, then enable it. Installing from a file does not depend on Blender's online access setting, which is off by default |
| MPFB asset packs | skins, eyes, hair, clothes | separate downloads, hundreds of megabytes; take only the packs the cast needs. Most are CC0; some hair packs need a credit: log each pack's licence when you download it |

After installing, run the proof script from the section above. Only when it has rendered a frame is the setup done.

The exact commands are not written here because they were not run when this was written, and a guessed installer is worse than none. The first time the setup works on a machine, save the commands that worked as `scripts/setup_blender.sh` (or `.ps1`) in this skill, with the versions they were run against, and replace this paragraph with a pointer to that script. From then on the setup is one command.

If the user wants no extra software at all, everything can stay in code. Say what that costs: characters will take far more rounds and will read as stylised or game-like in close-up.

Avoid: Blender bridge servers that execute whatever is sent to an open socket (known remote-execution holes); image-to-3D and text-to-3D generators unless the user asks; anything whose licence forbids commercial use (see the table at the end).

## References: look, blend, add your own

- Collect several references for anything that matters. Different people, different angles, different light.
- Study them: proportions, where colour changes, how the surface catches light, what makes it look used.
- Build from what you learned. Never trace or copy one image. Blending several and adding your own design gives something that belongs to the film.
- Looking at an image puts none of its pixels in the film, so any image can be a reference. Putting image pixels into a frame (as a texture or a backdrop) is different: it needs a licence that allows it and a credit, and the user must have agreed to that method.
- Ask the user which they want: everything painted by you, or scanned materials allowed for surfaces. Record the answer in `STATE.md`.

## Ways to build, from lightest to heaviest

Climb only as far as the shot needs. Change rungs when rounds stop helping.

1. **Parts and primitives.** Boxes, cylinders, lathes, extrusions, with bevels and real proportions. Right for furniture and most props.
2. **Blob sculpting.** Shapes made of many small volumes blended together, then turned into a mesh (`assets/engine/sdf.mjs`). Good for organic props and for stylised figures. For a realistic face it needs thousands of small shapes placed against references, and even then the evidence says it stays below a parametric base. Use it for faces only when the user wants no extra software.
3. **Parametric base, then adjust.** Generate a human with MPFB (age, build, proportions), then run the quality loop on its parameters and on local shape changes: render, compare with references, adjust. This is the route with evidence behind it.
4. **Painting with colour patches.** Colour belongs to the surface, and you can lay it down patch by patch: skin zones (redder cheeks and nose, cooler under the eyes, paler forehead), blemishes, veins, wear on wood, stains on a wall. Paint onto the model's surface or its texture, a few hundred to a few thousand patches, checking against references each round. Paint only the object's own colour; leave light and shadow to the renderer, or the surface will look wrong when the light changes. Be honest about its reach: painted patches read as illustration rather than photograph when they carry the whole surface, so use them on top of a base that already looks right (a parametric human's skin, a scanned material) and for things that are painted in real life (signs, a calendar page, a printed cloth, the artwork on an altar). Open skin scans for a specific kind of person rarely exist, so this is also how a face gets its own character.
5. **Painted backdrops for locked cameras.** When the camera does not move, the background can be one painted image projected onto simple geometry, with invisible stand-in surfaces to catch the characters' shadows. A backdrop may include light, because the light in that shot is fixed. Render or paint it at high quality once and reuse it for every frame of the shot. Most quiet films have many locked shots; this is the cheapest large gain in realism.
6. **Captured from reality.** Photogrammetry or splats from the user's own photos of a real place or object. Not generative. Splats keep the light they were captured in and do not receive new shadows well, so use meshes for anything the film's light touches.

## Characters

- A skeleton with one continuous skin. Limbs as separate rigid pieces always show at the joints.
- A face that changes continuously: controls for brows, lids, gaze, jaw, lip corners, lip press. Swapping whole head meshes pops.
- Eyes carry the face: a dark pupil, an iris with depth, a highlight on the cornea, a wet line on the lower lid, lashes, a slight redness at the corners. Eyes dart before the head turns; blinks are fast and irregular.
- Asymmetry everywhere. A perfectly mirrored face reads as a mask.
- Hands get fingers and a pose for every contact. A hand that hovers near an object instead of gripping it breaks the shot.
- Check the cast together at their true heights before any scene.
- If a story device depends on small objects (a tally, a token, which face of a block is up), make them readable by shape and colour at the size the widest shot shows them.

## Motion

Motion is where an early draft most obviously fails, and code is enough to fix most of it.

- Work from key poses, but add the layers that make a body alive: weight shifts onto a leg before the other lifts; the hips lead a step; the head lags a turn; a reach starts at the shoulder and settles at the fingers; breathing never stops.
- Feet stay where they land. Lock a planted foot's position and solve the leg to it (a two-joint solve is a few lines of code). Sliding feet are the most common giveaway.
- Hands that touch something stay on it; solve the arm to the contact point.
- Every action has anticipation, the action, and a settle. Nothing living moves at constant speed.
- Motion-capture clips can supply walks, sits and reaches. Check the licence of each library before using it; several well-known ones forbid commercial use. After applying a clip to your own skeleton, expect to fix foot sliding and hand contacts yourself.
- Small objects that fall or are thrown should follow simple physics, scripted or simulated, and must rest in stable positions.
- Judge motion on strips and short videos at film speed, never on single frames. The mechanical faults (through the floor, through an object, a joint bent the wrong way) are caught by the checks in the next section; what is left for your eye is whether it looks alive.

## Bodies that obey the room

A body animated by setting joint angles knows nothing about the floor, the furniture or its own anatomy. Left alone it will put a hand through a table, sink a foot into the floor and bend an elbow backwards, and none of that shows in a single still. Three mechanisms stop it. They are not optional for any shot where a body is seen moving.

1. **Joint limits.** Every joint has a range, and hinges (elbows, knees) bend one way only. Clamp every pose to the limits before it is applied (`assets/engine/bodycheck.mjs`: `clampPose`, `HUMAN_LIMITS`; in Blender, limit-rotation constraints on the rig). When a clamp fires, the animation is wrong: fix the pose rather than rely on the clamp.
2. **Solve limbs to contacts, with a pole.** Do not pose an arm by guessing shoulder and elbow angles. Say where the hand must be (on the table edge, around the chain) and where the elbow should point, and solve the two bones to it (`twoBone`; in Blender, an IK constraint with a pole target). The pole is what keeps an elbow from flipping to the wrong side. Do the same for legs: a planted foot keeps the position it landed on (`plantFoot`) and never goes below the floor. If the target is out of reach, the solver says so; move the body closer instead of stretching the arm.
3. **Check every frame for things passing through things.** Describe each body as capsules along its bones and the set as boxes, and run the whole shot through `checkFrames` before rendering. It lists every interval where a body part enters the floor, an object or another body part, with the depth. An empty list is the bar. A contact that is meant (a hand resting on a table) is declared, not ignored. In Blender, write the same check as a script over the armature's bones and the objects' bounding boxes.

Report the check's output to the user with the shot, the same way as any other check.

## Light

- Start from where light really comes from in the place: a window, a lamp, a doorway. One key, then what it bounces off.
- A mood board that looks rich on a monitor is often too dark to watch. Measure the brightness of test frames early.
- Let light bounce. Flat ambient fill is what makes CG look like CG.
- When light is fixed for a shot, bake it; spend the render time on what moves.

## Licence traps

Check the current terms before use; these were true when written and are the kind that change.

| Kind | Usable in a published film | Not usable (non-commercial or similar) |
|---|---|---|
| Human base | MPFB / MakeHuman output (CC0; two hair packs need credit), Blender human base meshes (CC0) | SMPL / SMPL-X, most free scanned head samples |
| Motion capture | 100STYLE (CC BY, walking only), Rokoko free packs, Mixamo (no redistribution of the files) | AMASS, Bandai Namco dataset, LAFAN1 |
| Materials, HDRIs | Poly Haven, ambientCG (CC0) | check every other library item by item |
| Reconstruction code | Brush, Spark | the original 3D Gaussian splatting code, nvdiffrast |
| Pose estimation from video | MediaPipe | OpenPose |
