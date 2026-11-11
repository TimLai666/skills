# Pipeline: frames, renders, checks, long jobs

Read before the first render.

## What the machine needs

Node 22+, Python 3, ffmpeg, Chrome. Check them, and the free disk space, before promising anything. Blender only if the film uses it: the application, run headless, not the pip package (`building.md` says why); ask before installing. Say the numbers to the user: how much disk is free, how much a render needs.

To move a film to another computer: copy the film folder, install the above, open a chat in the folder and continue from `STATE.md`.

## Every frame is a function of time

Frame `i` shows time `i / fps`, and nothing else decides what it looks like: no clocks, no unseeded randomness, no state carried from the previous frame. Then any frame can be rendered alone, out of order, in parallel, and again later with identical pixels. This is what makes re-rendering one fixed shot cheap.

For the browser route, a page exposes:

```js
window.READY               // a Promise; resolves to { frames, fps, width, height } when everything is loaded
window.renderFrame(i)      // draws frame i
window.captureFrame(i, type, quality)   // draws frame i and returns it as a data URL
```

`assets/engine/film.html` is a starting page that already does this. One page for the whole film, with a table of shots that each set the camera and the scene for their span of time, works well: a still, a sheet of one frame per shot, and the full render all come from the same code.

For the Blender route the same idea holds: a script that takes a frame range and renders exactly those frames.

## Rendering

```
node scripts/capture.mjs --url engine/film.html --probe                      # which GPU, does the page load
node scripts/capture.mjs --url engine/film.html --out review/still --frames "4800" --params "w=1920&h=1080"
node scripts/capture.mjs --url engine/film.html --out renders/frames --video renders/picture.mp4 --crf 17 --maxrate 10M --status renders/status.json --params "w=1920&h=1080"
```

- `--video` pipes frames straight into the encoder and leaves no frame files. Use it when disk is tight.
- Look before long renders: a still, then a sheet with one frame per shot, then a low-frame-rate pass of the whole film, then the real render. Each catches a different kind of mistake at a fraction of the cost.
- Spend render time. Measure seconds per frame on one frame of the heaviest shot, multiply by the frame count, and tell the user the total. Several hours of rendering for a film that looks right is a good trade; say so and let them decide.
- Render static parts once (a baked or painted background for a locked shot) and only the moving parts per frame.
- One heavy render at a time. Run it in the background with `--status`, record the command in `STATE.md`, and report progress from the status file.

## Checks

`scripts/qc.py` has the mechanical ones; run them on every cut before it is shown and report what they say:

```
python3 scripts/qc.py bright film.mp4     # how dark; the share of near-black
python3 scripts/qc.py black film.mp4      # black intervals
python3 scripts/qc.py freeze film.mp4     # frozen stretches
python3 scripts/qc.py loud film.mp4       # loudness, peaks, silences
python3 scripts/qc.py sheet film.mp4 4 10 # contact sheet, one frame every 4 s
python3 scripts/qc.py strip film.mp4 83.0 # a motion strip at a moment
python3 scripts/qc.py all film.mp4
```

Then the checks no script can do: the storyboard test on the cut (`story.md`), the comparison with the bar shot (`quality-bar.md`), and the user's ears (`sound.md`).

Three kinds of looking, each for a different fault, and none replaces the others:

- **Every frame, by numbers:** limbs through the floor or furniture and joints past their limits are found by the frame-by-frame check (`building.md`), never by eye. A sheet shows 60 moments of a film that has thousands.
- **Dense strips of one action:** whether a movement slides, pops or floats shows only in consecutive frames (`qc.py strip`, 8 to 12 frames per second across the action).
- **Overview sheets:** story, continuity and odd proportions. Keep each tile at least about 320 pixels wide; at 200 pixels a neck that was plainly too long went unnoticed through four drafts. A scene-change keyframe extractor (for example the `crv` tool, if the user has it) gives larger tiles at the moments something changes and is a good second view.

Look at small copies of images (`qc.py thumb`) when you only need the gist, and full-size crops when judging quality. Large images kept in the chat are re-read at every step.

## Delivery

The film as `<title>.mp4` at the top of its folder, plus a copy small enough for a phone if the main file is large. With it, in the message: length and format, what the checks said, the weakest three moments with times, what to listen for, and credits for anything from outside (libraries, sounds, voice service) for the user to paste where they publish. Ask before deleting intermediate files.

## Failures already met

| What happened | Cause | Fix |
|---|---|---|
| "page never defined window.READY" although the page was fine | the page built heavy models before defining `READY`; the capture tool waits 30 s for it | define `READY` and `captureFrame` in a small script at the top of the page before any module loads, resolve it after the build (the template does this) and let load errors reject it so they are reported |
| "Chrome did not start" | the machine was overloaded by other jobs | check the load, retry; it is not the film |
| "no space left on device" mid-render | free space swings when other jobs write | check free space right before each render; render with `--video`; delete frame folders as soon as they are encoded |
| A render "hung" for minutes | the command was waiting on a page that never became ready | always give long commands a log file and a status file; do not wait blind |
| The whole film came out near black | the look was judged on a mood board, not measured | measure brightness on test frames before the long render |
| The master lifted every background noise | the mix was 20 dB too quiet and the limiter made up the difference | mix near final loudness |
| A sound landed late | leading silence inside the file | trim it |
| A text replace changed the wrong number | a pattern matched more than one place in a generated table | patch exact unique strings and assert the count |
| Helpers could not be started | a guard from another skill in the same session blocked them | read the error; follow that skill's required brief format or start the helper from a session without it |
| The chat grew past hundreds of thousands of tokens | one chat for the whole film | update `STATE.md` at each gate and continue in a new chat |
