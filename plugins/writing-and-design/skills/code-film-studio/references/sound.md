# Sound

Read at stage 7. Start sound once the shot timings are stable; it does not have to wait for final pictures.

You cannot hear. You can measure loudness, timing and spectrum, and the user can listen. Build accordingly: decisions of taste go to their ears, in small pieces.

## Voices

- The user picks every voice by ear. Send two or three candidates per character as separate short files reading one line, and ask.
- Generate the remaining lines only in the voice they picked.
- Say which service or engine made the voice, since the line text is sent to it. Ask before using a paid one.
- Synthetic speech can drop or mangle words, especially in less common languages. You cannot tell. Ask the user to confirm each line is complete, and give the times.
- Measure where the speech actually falls inside each file (silence detection) and time mouth movement and subtitles to that, not to the script's estimate.
- No raw synthetic voice goes into the mix: clean it and place it in the room (`scripts/voice_treat.py`).

## Music

- Ask where the music comes from: an open-licence recording, the user's own track, written in code, or none.
- Whatever the source, the user picks by ear from two or three candidates.
- Less is usually better. A film can hold its music back until the turn.

## Effects and beds

- Recorded sounds read as more real than synthesised ones for physical events (wood on stone, cloth, steps, metal). Use open-licence recordings where you can and log each one's licence. Synthesise what must follow the picture exactly or sit in the music's key. If the user chose an all-synthesised palette, say that it will sound less real.
- One bed per place (room tone, what leaks in from outside). A change in the bed is a story tool: a hum that stops before something important, an exterior that is cut off when a door closes.
- Effects are accents on moments that mean something. Not every cut needs a sound.

## The event audit

Before mixing, list every event the viewer sees, in `review/sound-audit.md`:

```
- 0:01.5 · the blocks hit the floor · wood on stone, long rattle · clatter_slow
- 0:49 · hands circle over the burner · silent by choice: only the room · none
...
events 47 · sounded 44 · silent by choice 3
```

Nothing is silent by accident. `scripts/mix.py` refuses to mix without this file and its last line.

## Mix and master

- `scripts/mix.py audio/mix.json` mixes layers from a plan: file, start time, gain, bus (dialogue, foley, sfx, ambience, music), fades, pan, loops. Generate the plan from one script so a timing change is one edit.
- Build the mix near its final loudness. A mix that is far too quiet gets pushed up by the limiter at mastering, which lifts every hum and flattens the silences you wrote. Aim the dialogue around -20 LUFS in the mix.
- `scripts/master_audio.py mix.wav film.mp4 --video picture.mp4` masters to -14 LUFS and joins sound to picture.
- A sound file whose audible start is later than the file's start will play late. Trim leading silence or shift it.

## What to tell the user to listen for

With every cut, list the times that matter: each spoken line, the key effects, where music enters, each scripted silence. Ask one thing per item ("is the line complete?", "is the music too loud under the last line?").
