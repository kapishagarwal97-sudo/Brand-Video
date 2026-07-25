# TRYB — "Alone, Together" · Vox-style collage film

**Delivered:** `tryb-vox-collage-90s.mp4` — 87 s · 1920×1080 · 24 fps (animated on twos) · 26 MB
**Also:** `tryb-vox-collage-720p.mp4` (1280×720, 7 MB) for social/email · `poster.jpg` · `storyboard.html` (edit sheet)
**Rebuild:** `python3 build/render.py` then encode (command at the bottom)

---

## The cut — 17 shots, 87 seconds

| # | TC | Dur | Source | Beat | Move |
|---|-----|-----|--------|------|------|
| 1 | 0:00 | 4.5 | `01-hook-thumbnail.png` | A room full of people, all gone | push in |
| 2 | 0:04 | 3.5 | `01-hook-thumbnail3.png` | **ALONE, TOGETHER.** | slow push |
| 3 | 0:08 | 6.5 | `02-endless-scroll.png` | just five more minutes | pan down |
| 4 | 0:14 | 6.0 | `03-dead-group-chat.png` | the plans that never happen | pan down |
| 5 | 0:20 | 4.5 | `04-couple-apart.png` | close, and nowhere near | push in |
| 6 | 0:25 | 4.5 | `04-couple-apart.png1.png` | text back later. | slow push |
| 7 | 0:29 | 5.5 | `05-data-decline.png` | 7h 42m | pan down |
| 8 | 0:35 | 3.5 | `01-hook-thumbnail2.png` | what it replaced | pull out |
| 9 | 0:38 | 4.0 | `06-tryb-reveal.png` | **tryb** | slow push |
| 10 | 0:42 | 6.0 | `07-what-energizes-you.png` | what energizes you? | pan down |
| 11 | 0:48 | 5.0 | `08-real-experiences.png` | you're invited | push in |
| 12 | 0:53 | 5.0 | `09-curated-matches.png` | matched on what you love | pan down |
| 13 | 0:58 | 6.0 | `10-invitation-gathering.png` | **from screen to table** | pan right |
| 14 | 1:04 | 6.0 | `11-real-connection1.png` | joyful bonding | push in |
| 15 | 1:10 | 5.0 | `11-real-connection.png` | real people, real experiences | pan right |
| 16 | 1:15 | 5.0 | `12-endcard.png` | YOUR PEOPLE ARE OUT THERE | slow push |
| 17 | 1:20 | 6.5 | `12-endcard1.png` | JOIN TRYB | hold |

Scene map: **1 Hook** 0:00–0:20 · **2 Problem** 0:20–0:38 · **3 Idea** 0:38–0:53 ·
**4 How it works** 0:53–1:04 · **5 Emotion** 1:04–1:15 · **6 Ending** 1:15–1:27

---

## Colour arc

The film never mixes grounds — one flat colour per scene is what makes 17 separately
generated images read as a single production.

| Ground | Hex | Where |
|--------|-----|-------|
| Hook teal | `#123F45` | Scene 1 |
| Overload brick | `#A93A24` | Scene 2 |
| Turn mustard | `#D9971A` | Scene 3 |
| tryb orange | `#EB642E` | Scenes 4–6 |
| Stock cream | `#F2DCC4` | throughout |
| Ink | `#1F1A14` | annotation |

Orange and cream are read directly off `Brand Palette Background Color.png`.

---

## Every asset you supplied

**In the cut (17):** `01-hook-thumbnail.png`, `01-hook-thumbnail2.png`, `01-hook-thumbnail3.png`,
`02-endless-scroll.png`, `03-dead-group-chat.png`, `04-couple-apart.png`, `04-couple-apart.png1.png`,
`05-data-decline.png`, `06-tryb-reveal.png`, `07-what-energizes-you.png`, `08-real-experiences.png`,
`09-curated-matches.png`, `10-invitation-gathering.png`, `11-real-connection.png`,
`11-real-connection1.png`, `12-endcard.png`, `12-endcard1.png`

**Held as alternates (3):**
- `01-hook-thumbnail.png1.png` — wider crowd, faces less legible than the version used.
- `08-real-experiences1.png` — teal "You're invited". Beautiful, but teal belongs to Scene 1 in this
  arc; using it at 0:48 would break the warm turn. Strong as a standalone social still.
- `10-invitation-gathering1.png` — orange variant with cleaner UI. Genuinely close call against the
  mustard one; swap it in if you'd rather the pivot land on brand colour a beat earlier.

**Supporting assets (4):** `Blank cream paper texture.png`, `Brand Palette Background Color.png`
(+ duplicate `(1)`), `transparent PNG cutouts (arrows, tape, hearts).png`, `LOGO.jpg`

---

## Production notes

**Nothing arrived at 16:9.** Native ratios ran 0.75 (portrait) to 1.50 — none matched the 1.78 the
film needed. Cropping would have cut text off compositions that were designed as whole layouts, so
instead: tall frames became vertical pans, and frames that must read all at once (`06`, `12`, `12-1`)
sit on a field extended from their own matched edge colour, which is seamless because those
backgrounds are flat paper. On `02` the constraint turned into the best move in the film — the pan
follows the feed down to the pile on the floor.

**Two visual registers, used deliberately.** Some shots came back photoreal, some as true paper
collage. That is how Vox actually works, so the cut alternates: photoreal states the fact, collage
argues about it. Shots 5 and 6 run the same beat both ways, back to back.

**Rendered on twos.** Frames are generated at 12 fps and encoded to 24, so the stop-motion stutter is
in the footage rather than applied as a filter. Grain is composited per frame from a rotating pool of
eight tiles so it flickers like film instead of sitting static.

**Silent by design.** Every frame carries its own typography, so no captions were burned in — they
would fight the paper. The film wants a music bed and optionally sparse VO; it does not want
lower-thirds.

### Two things worth fixing before the next round

1. **The cutout sheet isn't transparent.** `transparent PNG cutouts (arrows, tape, hearts).png` has a
   baked olive-gradient background, so the arrows/tape/hearts can't be layered over frames as-is.
   Re-render on true alpha and they become animatable overlays.
2. **Two logo colourways are in play.** The wordmark is cream on `06`/`12`/`12-1` and orange on
   `07`/`09`/`10`. Both read fine in sequence, but worth locking one rule.

---

## Rebuild

```bash
pip install pillow imageio-ffmpeg
python3 build/render.py                      # writes 1044 PNG frames at 12 fps
ffmpeg -y -framerate 12 -i frames/f%05d.png \
  -c:v libx264 -preset slower -crf 24 -tune grain \
  -pix_fmt yuv420p -r 24 -movflags +faststart \
  tryb-vox-collage-90s.mp4
```

Edit `EDIT` at the top of `build/render.py` to change shot order, duration, framing mode
(`fill` = motion crop, `fit` = whole composition) or move (`push_in`, `push_out`, `pan_down`,
`pan_right`, `hold_push`).
