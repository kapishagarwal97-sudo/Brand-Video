# TRYB — "Alone, Together" · Vox-style motion film

**Delivered:** `tryb-vox-motion-40s.mp4` — 39.67 s · 1920×1080 · 24 fps (animated on twos) · 17 MB
**Also:** `tryb-vox-motion-40s-720p.mp4` (3.7 MB) · `poster.jpg` · `storyboard.html` (edit sheet)
**Rebuild:** `cd build && python3 film.py`, then the encode command at the bottom

---

## What changed: composed, not panned

The earlier cuts were stills with camera moves on them — a slideshow. A Vox explainer is not that.
It is a **stack of layers**, each with its own start time, easing and exit. This build is a small
animation engine (`build/vox.py`) plus a shot list written against it (`build/film.py`).

What actually moves now:

| Technique | Where |
|-----------|-------|
| Strips snap in staggered, overshoot and settle | title card, "YOUR PEOPLE ARE OUT THERE" |
| Ink strokes **draw themselves on** along their own path length | every arrow, the underlines, the calendar cross-out, the chart trend line |
| Bars grow from the baseline, one after another | the data shot |
| A number **counts up** rather than appearing | 0.0h → 7.7h |
| Elements land, then **exit** — fall and rotate away | the five "let's catch up soon" bubbles |
| A genuine looping scroll | the newsprint feed |
| Continuous idle animation | the pulsing typing dots |
| Word-by-word headline entrances | all eight headlines |
| Per-frame 1px jitter on paper elements | everywhere — the stop-motion "boil" |

Entrances use a **back-out overshoot** ease. That small bounce is what makes a cutout read as
physically placed rather than digitally faded.

---

## The cut — 14 shots, 39.67 seconds

| # | TC | Dur | Shot | What animates |
|---|-----|-----|------|---------------|
| 1 | 0:00 | 3.0 | hook | Crowd print slides down and settles; headline lands word by word; a red pen circles one figure |
| 2 | 0:03 | 2.6 | title | Two torn strips fly in from opposite sides 0.24 s apart; the red arrow draws on |
| 3 | 0:05 | 3.2 | feed | The newsprint feed scrolls continuously; five notification scraps pop in staggered |
| 4 | 0:08 | 3.2 | chat | Five bubbles land one by one, then drop out of frame; the calendar is crossed out in two strokes |
| 5 | 0:11 | 2.8 | postpone | The phone slides in over the embrace; the reply pops late; typing dots pulse |
| 6 | 0:14 | 3.2 | data | Bars grow staggered, trend arrow draws down, screen-time line draws up, counter runs to 7.7 h |
| 7 | 0:17 | 2.5 | replaced | The quiet beat — one print, one line, almost no motion |
| 8 | 0:20 | 2.2 | reveal | Wordmark snaps in with overshoot; two tape strips land after it |
| 9 | 0:22 | 3.0 | question | Phone slides up, four chips pop in sequence, the paper hand taps and the chip depresses |
| 10 | 0:25 | 3.0 | matched | Badge lands, five ink lines draw outward, a real face pops in at the end of each |
| 11 | 0:28 | 3.0 | pivot | The arrow draws left-to-right and the colour photo lands where it points |
| 12 | 0:31 | 2.6 | payoff | Two colour prints land at opposing angles; fourteen confetti squares cascade |
| 13 | 0:34 | 2.7 | yourpeople | Four cut strips drop from above 0.15 s apart, each to its own angle |
| 14 | 0:36 | 2.8 | join | Wordmark scales in, underline draws on, CTA strip snaps in, arrow points at it |

---

## Built from parts

`build/vox.py` generates the collage itself rather than relying on finished images:

- **`paper()`** — cardstock with procedurally torn edges, grain and drop shadow
- **`label()`** — text on its own torn strip
- **`halftone()`** — real CMYK-style dot screen applied to photographs
- **`circle_portrait()`** — cuts one circular face out of a larger collage
- **`ink_path()` / `ink_ellipse()`** — strokes that render progressively so they draw on
- **`counter_layer()`** — a number that counts up
- **`tape()`**, **`field()`**, **`grain()`** — tape strips, cardstock ground, film grain

Your original stills supply the photography: the crowd, the embrace, the group hug, the feed
ribbon, the five faces, the dinner and sunset photos. Everything else — type, paper, tape, arrows,
charts, confetti — is generated.

### Image fidelity

Two things were degrading the artwork and are now fixed:

- **No double dot-screening.** Your stills already carry their own halftone treatment, so running
  them through `halftone()` again was screening an already-screened image — that is what crushed
  the night crowd to near-black and turned the group hug blocky. Every supplied still is now placed
  as-is; `halftone()` remains available for raw photography.
- **Supersampled compositing.** Prints are built at up to 2× their display width and composited
  back down (`Layer(base=…)`), so rotation and in-between scales resample a larger source instead
  of smearing it. Torn edges are drawn at 3× and downsampled, so the paper edge is antialiased
  rather than a jagged polygon.

### The real wordmark

The mark is no longer re-lettered in a script font. `logo()` alpha-keys the actual tryb wordmark
out of `Brand Palette Background Color.png` by projecting each pixel onto the orange→cream axis,
which recovers a clean antialiased alpha, then tints it to whatever the frame needs — cream on
orange and mustard, orange on cream. It is used in all four places the mark appears (shots 8, 10,
13, 14). The letterforms are custom; they must never be approximated with a typeface.

### One number to replace

The **7.7 h** screen-time figure is illustrative, carried over from your `05-data-decline.png`.
Swap in a sourced statistic before this goes public, or cut the counter. Editing one line in
`build/film.py` changes it.

---

## Why Canva isn't in this cut

Canva AI returned a **presentation deck**, not film frames: invented statistics ("32% decline",
"70% rise") that were never in the brief, a placeholder contact slide
(`hello@reallygreatsite.com`), two non-film title/divider slides, and explanatory deck prose in
place of the one-line captions. Separately, this environment's network policy blocks every Canva
host — `design.canva.ai`, `media.canva.com` and `export-download.canva.com` all return 403 at the
proxy — so nothing could be downloaded to render, and the artwork could not be inspected.

The generated design is still in the account if you want it:
[Alone, Together, 15 pages](https://www.canva.com/d/zigmeQ4VqFXfkH-). Canva remains the better tool
for a static on-brand deck; it is not the tool for this.

---

## Rebuild

```bash
pip install pillow imageio-ffmpeg
cd build && python3 film.py               # writes 476 PNG frames at 12 fps
ffmpeg -y -framerate 12 -i frames/f%05d.png \
  -c:v libx264 -preset slower -crf 21 -tune grain \
  -pix_fmt yuv420p -r 24 -movflags +faststart \
  tryb-vox-motion-40s.mp4
```

Each shot is a function in `build/film.py` returning a `Shot` of `Layer`s. A layer takes keyframe
tracks for `dx`, `dy`, `scale`, `rot` and `alpha`; helpers `pop()`, `slide()`, `fade()` and
`stroke()` cover the common entrances. `build/render.py` and `build/render87.py` are the previous
card-based cuts, kept for reference.
