#!/usr/bin/env python3
"""Render the TRYB Vox-collage brand film from the supplied stills.

Frames are generated at 12 fps (the Vox stop-motion cadence) and encoded to
24 fps, so the stutter is baked in rather than faked with a filter.
"""
import os, math, subprocess, shutil
from PIL import Image, ImageFilter, ImageChops
import random

SRC = "/tmp/claude-0/-home-user-Brand-Video/9007dc76-1736-5cf2-9d9a-3e2a752e7ce5/scratchpad/uploads"
OUT = "/tmp/claude-0/-home-user-Brand-Video/9007dc76-1736-5cf2-9d9a-3e2a752e7ce5/frames"
W, H = 1920, 1080
FPS = 12

# mode:  'fill' = cover frame, animate the crop window (pan/push)
#        'fit'  = whole composition visible, sides flat-filled with edge colour
# motion: (start_rect, end_rect) generated from the named move
EDIT = [
    # file,                          scene, mode,   move,        secs
    ("01-hook-thumbnail.png",          1, "fill", "push_in",     4.5),
    ("01-hook-thumbnail3.png",         1, "fill", "push_in_sm",  3.5),
    ("02-endless-scroll.png",          1, "fill", "pan_down",    6.5),
    ("03-dead-group-chat.png",         1, "fill", "pan_down",    6.0),

    ("04-couple-apart.png",            2, "fill", "push_in",     4.5),
    ("04-couple-apart.png1.png",       2, "fill", "push_in_sm",  4.5),
    ("05-data-decline.png",            2, "fill", "pan_down",    5.5),
    ("01-hook-thumbnail2.png",         2, "fill", "push_out",    3.5),

    ("06-tryb-reveal.png",             3, "fit",  "push_in_sm",  4.0),
    ("07-what-energizes-you.png",      3, "fill", "pan_down",    6.0),
    ("08-real-experiences.png",        3, "fill", "push_in",     5.0),

    ("09-curated-matches.png",         4, "fill", "pan_down",    5.0),
    ("10-invitation-gathering.png",    4, "fill", "pan_right",   6.0),

    ("11-real-connection1.png",        5, "fill", "push_in",     6.0),
    ("11-real-connection.png",         5, "fill", "pan_right",   5.0),

    ("12-endcard.png",                 6, "fit",  "push_in_sm",  5.0),
    ("12-endcard1.png",                6, "fit",  "hold_push",   6.5),
]


def edge_fill_color(im):
    """Median colour of a thin border band — matches the seam, not the average."""
    w, h = im.size
    px = []
    for x in range(0, w, 3):
        px += [im.getpixel((x, 1)), im.getpixel((x, h - 2))]
    for y in range(0, h, 3):
        px += [im.getpixel((1, y)), im.getpixel((w - 2, y))]
    px.sort(key=lambda c: c[0] * 0.299 + c[1] * 0.587 + c[2] * 0.114)
    return px[len(px) // 2]


def base_fill(im):
    """Scale so the image covers the frame; return the oversized canvas."""
    w, h = im.size
    s = max(W / w, H / h) * 1.06          # 6% headroom so pans have somewhere to go
    return im.resize((round(w * s), round(h * s)), Image.LANCZOS)


def base_fit(im):
    """Whole composition visible, sides extended with the matched edge colour."""
    w, h = im.size
    s = (H * 0.995) / h
    nw, nh = round(w * s), round(h * s)
    card = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), edge_fill_color(im))
    canvas.paste(card, ((W - nw) // 2, (H - nh) // 2))
    return canvas


def ease(t):
    """Slow in, slow out — no mechanical linear drift."""
    return t * t * (3 - 2 * t)


def crop_rect(base, move, t):
    """Return the crop box for progress t within a 'fill' clip."""
    bw, bh = base.size
    ar = W / H
    # widest 16:9 window that fits
    if bw / bh > ar:
        max_h, max_w = bh, bh * ar
    else:
        max_w, max_h = bw, bw / ar

    if move == "push_in":
        z0, z1 = 1.00, 0.86
    elif move == "push_in_sm":
        z0, z1 = 1.00, 0.93
    elif move == "push_out":
        z0, z1 = 0.86, 1.00
    else:
        z0 = z1 = 0.97

    z = z0 + (z1 - z0) * t
    cw, ch = max_w * z, max_h * z

    # travel
    fx = fy = 0.5
    if move == "pan_down":
        fy = 0.06 + 0.88 * t
    elif move == "pan_up":
        fy = 0.94 - 0.88 * t
    elif move == "pan_right":
        fx = 0.08 + 0.84 * t
    elif move == "hold_push":
        z = 1.0 - 0.04 * t
        cw, ch = max_w * z, max_h * z

    x = (bw - cw) * fx
    y = (bh - ch) * fy
    x = max(0, min(bw - cw, x))
    y = max(0, min(bh - ch, y))
    return (x, y, x + cw, y + ch)


# --- grain: a small pool of tiles, cycled, so it flickers like real film ---
random.seed(7)
GRAIN = []
for _ in range(8):
    g = Image.effect_noise((W // 2, H // 2), 26).convert("L")
    g = g.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.4))
    GRAIN.append(Image.merge("RGB", (g, g, g)))


def apply_grain(frame, i):
    return ImageChops.overlay(frame, GRAIN[i % len(GRAIN)]).point(
        lambda v: v)  # overlay is subtle at this noise sigma


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    n = 0
    manifest = []
    for fname, scene, mode, move, secs in EDIT:
        src = Image.open(os.path.join(SRC, fname)).convert("RGB")
        base = base_fill(src) if mode == "fill" else base_fit(src)
        count = round(secs * FPS)
        start = n / FPS
        for k in range(count):
            t = ease(k / max(1, count - 1))
            if mode == "fill":
                fr = base.crop(tuple(round(v) for v in crop_rect(base, move, t)))
                fr = fr.resize((W, H), Image.LANCZOS)
            else:
                # gentle push on a fitted card: scale about the centre
                z = 1.0 + (0.035 if move != "hold_push" else 0.02) * t
                zw, zh = round(W * z), round(H * z)
                fr = base.resize((zw, zh), Image.LANCZOS).crop(
                    ((zw - W) // 2, (zh - H) // 2, (zw - W) // 2 + W, (zh - H) // 2 + H))
            fr = ImageChops.blend(fr, apply_grain(fr, n), 0.16)
            fr.save(os.path.join(OUT, f"f{n:05d}.png"), compress_level=1)
            n += 1
        manifest.append((fname, scene, start, n / FPS))
        print(f"  {fname:<32} sc{scene}  {start:6.2f}s -> {n/FPS:6.2f}s  ({count} frames)")

    print(f"\n{n} frames = {n/FPS:.2f}s @ {FPS}fps")
    with open(os.path.join(os.path.dirname(OUT), "manifest.txt"), "w") as fh:
        for m in manifest:
            fh.write(f"{m[0]}\t{m[1]}\t{m[2]:.2f}\t{m[3]:.2f}\n")


if __name__ == "__main__":
    main()
