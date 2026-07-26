# TRYB — "Alone, Together" · Vox-style collage film

**Delivered:** `tryb-vox-collage-40s.mp4` — 39.6 s · 1920×1080 · 24 fps (animated on twos) · 15 MB
**Also:** `tryb-vox-collage-40s-720p.mp4` (1280×720, 4.3 MB) · `poster.jpg` · `storyboard.html` (edit sheet)
**Rebuild:** `python3 build/render.py`, then the encode command at the bottom

---

## Three rules this cut obeys

**1 · Every still is shown whole — nothing crops, nothing zooms in.**
None of the supplied stills are 16:9 (natives run 0.75 to 1.50). Each one is now placed as a paper
card on a textured cream cardstock field, scaled *down* to fit. Where a card moves, it only ever
zooms **out** (starts 6% oversized, settles to fit). The field is the real
`Blank cream paper texture.png` you supplied, warmed slightly and washed with the scene's ground
colour at 10% so the cold→warm arc still reads underneath. Cards get a cream paper border, a nicked
(non-digital) edge, a soft drop shadow, and a strip of tape — so the letterbox space became part of
the design rather than something to hide.

**2 · One effect per shot, never the same effect twice in a row.**
Each shot animates exactly one property — no combined moves.

| Effect | What moves |
|--------|-----------|
| `zoom_out` | scale 1.06 → 1.00 |
| `drift_up` | vertical position, ±16 px |
| `drift_side` | horizontal position, ±18 px |
| `rotate_settle` | rotation 1.8° → 0° (paper being laid down) |
| `fade` | opacity 0 → 1 |
| `hold` | nothing at all (final card) |

The renderer asserts on any repeat, so the rule can't break silently. Text rides its own track, so
adding a caption never counts as a second effect on the picture.

**3 · Text carries the argument.** Eight shots now have a headline in `Big Shoulders` (condensed
bold — the closest match to the newspaper cutout type inside your collages), an orange hand-drawn
rule, and a marker-script kicker in `Nothing You Could Do`. The six statement frames that already
carry their own typography stay clean.

---

## The cut — 14 shots, 39.6 seconds

| # | TC | Dur | Source | Layout | Effect | On-screen text |
|---|-----|-----|--------|--------|--------|----------------|
| 1 | 0:00 | 3.0 | `01-hook-thumbnail.png` | split | zoom out | **We've never been more connected.** · *and never further apart* |
| 2 | 0:03 | 2.5 | `01-hook-thumbnail3.png` | full | rotate settle | — (own headline) |
| 3 | 0:05 | 3.0 | `02-endless-scroll.png` | split | drift up | **Hours vanish into a feed with no end.** · *just five more minutes* |
| 4 | 0:08 | 3.0 | `03-dead-group-chat.png` | split | zoom out | **The group chat lives on. The plans quietly die.** · *next time, for sure* |
| 5 | 0:11 | 2.9 | `04-couple-apart.png1.png` | split | drift side | **Closeness became something we postpone.** · *text back later* |
| 6 | 0:14 | 2.9 | `05-data-decline.png` | full | zoom out | — (own labels) |
| 7 | 0:17 | 2.6 | `01-hook-thumbnail2.png` | full | rotate settle | **This is what it replaced.** — set inside the still's own white space |
| 8 | 0:19 | 2.3 | `06-tryb-reveal.png` | full | fade | — (wordmark alone) |
| 9 | 0:22 | 2.9 | `07-what-energizes-you.png` | split | zoom out | **So tryb starts with a better question.** · *not who you look like* |
| 10 | 0:25 | 2.9 | `09-curated-matches.png` | split | drift up | **Then it finds the people who love the same things.** · *five, not five thousand* |
| 11 | 0:28 | 3.0 | `10-invitation-gathering.png` | full | zoom out | — (own headline) |
| 12 | 0:31 | 2.9 | `11-real-connection1.png` | split | drift side | **No feed. No scrolling. An evening you remember.** · *this is the whole point* |
| 13 | 0:34 | 2.7 | `12-endcard.png` | full | rotate settle | — (own headline) |
| 14 | 0:36 | 2.9 | `12-endcard1.png` | full | hold | — (own CTA) |

Scene map: **1 Hook** 0:00–0:11 · **2 Problem** 0:11–0:19 · **3 Idea** 0:19–0:25 ·
**4 How it works** 0:25–0:31 · **5 Emotion** 0:31–0:34 · **6 Ending** 0:34–0:39

Cutting from 87 s to under 40 meant dropping three shots: `04-couple-apart.png` (the photoreal couch
— the collage version at shot 5 makes the same point harder), `08-real-experiences.png` (shots 10
and 11 already cover the invitation), and `11-real-connection.png` (kept the warmer of the two
payoff frames).

---

## Layouts

**split** — text column left (x 96, max 548 px), card centred in a 1164×964 box on the right. Used
for the eight explanatory beats.

**full** — card centred in a 1420×980 box, no added text. Used for the six frames whose own
typography is the message.

One override: shot 7's still is two-thirds negative space by design, so its headline sits *inside*
the card's white area rather than beside it (`TEXT_OVERRIDE` in `build/render.py`).

---

## Colour arc

| Field wash | Hex | Scene |
|-----------|-----|-------|
| cool teal | `#4A7A80` | 1 |
| warm brick | `#BC604A` | 2 |
| mustard | `#DEAA4A` | 3 |
| tryb orange | `#EE8454` → `#F08C5C` | 4–6 |

Washed into cream at 10% — enough to feel, not enough to fight the cards. Brand orange `#EB642E`
and cream `#F2DCC4` are read off `Brand Palette Background Color.png`.

---

## Assets

**In the cut (14):** `01-hook-thumbnail.png`, `01-hook-thumbnail2.png`, `01-hook-thumbnail3.png`,
`02-endless-scroll.png`, `03-dead-group-chat.png`, `04-couple-apart.png1.png`, `05-data-decline.png`,
`06-tryb-reveal.png`, `07-what-energizes-you.png`, `09-curated-matches.png`,
`10-invitation-gathering.png`, `11-real-connection1.png`, `12-endcard.png`, `12-endcard1.png`

**Held as alternates (6):** `01-hook-thumbnail.png1.png`, `04-couple-apart.png` (photoreal couch),
`08-real-experiences.png`, `08-real-experiences1.png`, `10-invitation-gathering1.png`,
`11-real-connection.png`

**Supporting:** `Blank cream paper texture.png` (now the field behind every frame),
`Brand Palette Background Color.png`, `transparent PNG cutouts (arrows, tape, hearts).png`, `LOGO.jpg`

### Still worth fixing

1. **The cutout sheet isn't transparent.** `transparent PNG cutouts (arrows, tape, hearts).png` has a
   baked olive-gradient background, so those arrows and tape can't be layered over frames. The tape
   strips in this cut are drawn procedurally instead. A true-alpha re-render would let the real ones
   animate on.
2. **Two logo colourways.** Cream on `06`/`12`/`12-1`, orange on `07`/`09`/`10`. Both read fine in
   sequence; worth locking one rule.

---

## Rebuild

```bash
pip install pillow imageio-ffmpeg
python3 build/render.py                      # writes 475 PNG frames at 12 fps
ffmpeg -y -framerate 12 -i frames/f%05d.png \
  -c:v libx264 -preset slower -crf 22 -tune grain \
  -pix_fmt yuv420p -r 24 -movflags +faststart \
  tryb-vox-collage-40s.mp4
```

Everything is driven by the `EDIT` table at the top of `build/render.py` — shot order, scene,
layout (`split`/`full`), effect, duration, headline and kicker. `build/render87.py` is the previous
87-second cut, kept for reference.
