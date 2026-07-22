# Minimal canonical-input fixture

Three brands, five attributes, twenty synthetic reviews. The smallest corpus that still satisfies every contract check: at least three dimensions, at least two positioning attributes, all four theory families covered, every brand scored on every attribute.

It exists for one job: **prove that a change to the scripts did what you meant and nothing else.**

The repo has no test suite. Without a before/after run, a change to `positioning.py` or `io.py` can only be judged by reading it, and a statistics pipeline that produces plausible wrong numbers reads exactly like one that produces right numbers.

## Before/after procedure

```bash
pip install -r ../../requirements.txt

python3 build_fixture.py

python3 ../../scripts/run_review_mining_stp.py \
  --run-mode full --input-dir . --output-dir /tmp/stp-before

# make the change, then

python3 ../../scripts/run_review_mining_stp.py \
  --run-mode full --input-dir . --output-dir /tmp/stp-after

diff -r /tmp/stp-before /tmp/stp-after
```

Everything except the difference you intended should be identical. A renamed key should show up as a renamed key and nothing else; a moved number means the change did more than it claimed.

`perceptual_map.png` differs between runs on some matplotlib builds. Compare `perceptual_map_coordinates.csv` instead.

## Hand-checkable values

The fixture is small enough to verify the aggregation by hand. The product-level quality figure is the mean of per-review quality over the reviews that mentioned the attribute (`salience >= 1`):

| Check | Expected |
|---|---|
| `positioning_scorecard.csv`, ArcShield × anti_fog, axis `valence` | `8.4286` |
| Same figure computed from `review_scoring_table.csv` by hand | `8.4286` |

If those two ever disagree, the aggregation changed.

## Editing the fixture

Edit `build_fixture.py` and regenerate — do not hand-edit the CSV and JSON files. The generator keeps `attribute_catalog.csv`, `review_foundation.json` and the score table columns consistent with each other, and those three are cross-validated on load.

The reviews are written so each brand has a distinct profile: ArcShield wins on anti-fog and impact, VisorMax on comfort, ClearGuard on style and support. Without that separation the positioning map collapses and the fixture stops being able to catch a broken factor analysis.

The data is synthetic. It is not evidence about any real product.
