#!/usr/bin/env python3
"""Render the TRYB Vox-collage brand film — 40-second cut.

Design rules this build obeys:
  * Every still is shown WHOLE. Nothing is cropped and nothing zooms in; stills
    that aren't 16:9 sit as paper cards on a textured cream field, scaled down
    to fit (zoom-out only).
  * Exactly ONE motion effect per shot, and never the same effect on two
    consecutive shots.
  * On-screen text carries the argument between the frames' own typography.

Frames render at 12 fps and encode to 24, so the stop-motion cadence is in the
footage rather than applied as a filter.
"""
import os, shutil, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "build", "fonts")
OUT = os.path.join(ROOT, "frames")
TEXTURE = os.path.join(ROOT, "Blank cream paper texture.png")

W, H = 1920, 1080
FPS = 12

INK = (34, 28, 21)
ORANGE = (235, 100, 46)

F_HEAD = os.path.join(FONTS, "BigShoulders-Bold.ttf")
F_HAND = os.path.join(FONTS, "NothingYouCouldDo-Regular.ttf")

# scene ground colours, washed faintly into the cream field so the arc still reads
SCENE_TINT = {1: (74, 122, 128), 2: (188, 96, 74), 3: (222, 170, 74),
              4: (238, 132, 84), 5: (240, 140, 92), 6: (240, 140, 92)}

# file, scene, layout, effect, secs, headline, handwritten kicker
EDIT = [
    ("01-hook-thumbnail.png",       1, "split", "zoom_out",      3.0,
     "We've never been\nmore connected.", "and never further apart"),
    ("01-hook-thumbnail3.png",      1, "full",  "rotate_settle", 2.5, None, None),
    ("02-endless-scroll.png",       1, "split", "drift_up",      3.0,
     "Hours vanish into\na feed with no end.", "just five more minutes"),
    ("03-dead-group-chat.png",      1, "split", "zoom_out",      3.0,
     "The group chat lives on.\nThe plans quietly die.", "next time, for sure"),

    ("04-couple-apart.png1.png",    2, "split", "drift_side",    2.9,
     "Closeness became\nsomething we postpone.", "text back later"),
    ("05-data-decline.png",         2, "full",  "zoom_out",      2.9, None, None),
    ("01-hook-thumbnail2.png",      2, "full",  "rotate_settle", 2.6,
     "This is what\nit replaced.", None),

    ("06-tryb-reveal.png",          3, "full",  "fade",          2.3, None, None),
    ("07-what-energizes-you.png",   3, "split", "zoom_out",      2.9,
     "So tryb starts with\na better question.", "not who you look like"),
    ("09-curated-matches.png",      4, "split", "drift_up",      2.9,
     "Then it finds the people\nwho love the same things.", "five, not five thousand"),
    ("10-invitation-gathering.png", 4, "full",  "zoom_out",      3.0, None, None),

    ("11-real-connection1.png",     5, "split", "drift_side",    2.9,
     "No feed. No scrolling.\nAn evening you remember.", "this is the whole point"),
    ("12-endcard.png",              6, "full",  "rotate_settle", 2.7, None, None),
    ("12-endcard1.png",             6, "full",  "hold",          2.9, None, None),
]

BOX = {"split": (700, 58, 1164, 964), "full": (250, 50, 1420, 980)}
TEXT_COL = (96, 548)          # x-start, max width — keeps clear of the card box

# stills built with their own negative space: drop the line straight into it
TEXT_OVERRIDE = {"01-hook-thumbnail2.png": (990, 250, 480)}
ZOOM_START = 1.06


def build_field(tint):
    """Cream cardstock field: the table the whole film is assembled on."""
    tex = Image.open(TEXTURE).convert("RGB")
    s = max(W / tex.width, H / tex.height)
    tex = tex.resize((math.ceil(tex.width * s), math.ceil(tex.height * s)), Image.LANCZOS)
    ox, oy = (tex.width - W) // 2, (tex.height - H) // 2
    tex = tex.crop((ox, oy, ox + W, oy + H))
    tex = ImageEnhance.Brightness(tex).enhance(1.09)
    wash = Image.new("RGB", (W, H), tint)
    tex = Image.blend(tex, ImageChops.multiply(tex, wash), 0.10)
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((int(-W * .32), int(-H * .42), int(W * 1.32), int(H * 1.42)), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(150))
    return Image.composite(tex, ImageEnhance.Brightness(tex).enhance(.87), v)


def build_card(path, box_w, box_h):
    """The whole still, cream paper border, torn edge, drop shadow. Never cropped."""
    im = Image.open(os.path.join(ROOT, path)).convert("RGB")
    bleed = 16
    s = min((box_w - bleed * 2) / im.width, (box_h - bleed * 2) / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)

    cw, ch = im.width + bleed * 2, im.height + bleed * 2
    card = Image.new("RGBA", (cw, ch), (247, 240, 226, 255))
    card.paste(im, (bleed, bleed))
    d = ImageDraw.Draw(card)
    random.seed(abs(hash(path)) & 0xFFFF)
    for _ in range(60):                     # nick the border so it isn't a clean rectangle
        x, y = random.randint(0, cw - 1), random.choice([0, ch - 1])
        d.rectangle([x, y, min(cw - 1, x + random.randint(1, 5)), y], fill=(0, 0, 0, 0))
    for _ in range(60):
        y, x = random.randint(0, ch - 1), random.choice([0, cw - 1])
        d.rectangle([x, y, x, min(ch - 1, y + random.randint(1, 5))], fill=(0, 0, 0, 0))

    pad = 48
    out = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([pad + 5, pad + 11, pad + cw + 5, pad + ch + 13],
                                fill=(40, 30, 20, 120))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    out.alpha_composite(card, (pad, pad))
    return out


def tape_strip(angle=-6, w=134, h=42):
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rectangle([0, 0, w, h], fill=(228, 207, 162, 150))
    for i in range(0, w, 9):
        d.line([(i, 0), (i, h)], fill=(214, 191, 145, 64))
    for y in (0, h - 1):
        for x in range(0, w, 4):
            d.rectangle([x, y, x + 2, y], fill=(0, 0, 0, 0))
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


def wobble_rule(draw, x, y, w, colour, seed):
    random.seed(seed)
    pts = [(x + i, y + random.uniform(-1.8, 1.8)) for i in range(0, w, 12)]
    pts.append((x + w, y + random.uniform(-1.3, 1.3)))
    draw.line(pts, fill=colour, width=5, joint="curve")


def build_text(headline, kicker, seed, override=None):
    """Text as its own layer, so the picture still carries exactly one effect."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if not headline:
        return layer
    d = ImageDraw.Draw(layer)
    x, maxw = (override[0], override[2]) if override else TEXT_COL
    lines = headline.split("\n")

    size = 96
    while size > 44:
        f = ImageFont.truetype(F_HEAD, size)
        if max(d.textlength(l, font=f) for l in lines) <= maxw:
            break
        size -= 3
    f = ImageFont.truetype(F_HEAD, size)
    lh = int(size * 1.02)
    y = override[1] if override else (H - lh * len(lines)) // 2 - 40
    for l in lines:
        d.text((x, y), l, font=f, fill=INK)
        y += lh

    wr = int(min(maxw, max(d.textlength(l, font=f) for l in lines)))
    wobble_rule(d, x, y + 20, wr, ORANGE, seed)
    if kicker:
        d.text((x + 8, y + 54), kicker, font=ImageFont.truetype(F_HAND, 48),
               fill=(122, 106, 84))
    return layer


def ease(t):
    return t * t * (3 - 2 * t)


def place(frame, card, effect, t, box):
    """Composite the card animating exactly ONE property."""
    bx, by, bw, bh = box
    cx, cy = bx + bw / 2, by + bh / 2
    img = card
    scale = dx = dy = rot = 0.0
    scale, alpha = 1.0, 1.0

    if effect == "zoom_out":
        scale = ZOOM_START - (ZOOM_START - 1.0) * ease(t)   # only ever shrinks
    elif effect == "drift_up":
        dy = 16 - 32 * ease(t)
    elif effect == "drift_side":
        dx = -18 + 36 * ease(t)
    elif effect == "rotate_settle":
        rot = 1.8 * (1 - ease(t))
    elif effect == "fade":
        alpha = ease(min(1.0, t / 0.30))
    # "hold" animates nothing

    if abs(scale - 1.0) > 1e-4:
        img = img.resize((max(1, round(img.width * scale)),
                          max(1, round(img.height * scale))), Image.LANCZOS)
    if rot:
        img = img.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0:
        img = img.copy()
        img.putalpha(img.getchannel("A").point(lambda v: int(v * alpha)))

    frame.alpha_composite(img, (round(cx - img.width / 2 + dx),
                                round(cy - img.height / 2 + dy)))


random.seed(11)
GRAIN = [Image.merge("RGB", (g, g, g)) for g in (
    Image.effect_noise((W // 2, H // 2), 24).convert("L")
         .resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(.45))
    for _ in range(8))]


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    fields = {s: build_field(c) for s, c in SCENE_TINT.items()}
    n = 0
    prev = None
    for idx, (fn, scene, layout, effect, secs, head, kick) in enumerate(EDIT):
        assert effect != prev, f"{fn}: '{effect}' repeats the previous shot"
        prev = effect

        bx, by, bw, bh = BOX[layout]
        if effect == "zoom_out":            # keep the oversized start inside frame
            bw, bh = int(bw / ZOOM_START), int(bh / ZOOM_START)
            bx, by = bx + (BOX[layout][2] - bw) // 2, by + (BOX[layout][3] - bh) // 2
        box = (bx, by, bw, bh)

        card = build_card(fn, bw, bh)
        if effect != "fade":
            tp = tape_strip(angle=-7 if idx % 2 else 6)
            fx = card.width // 2 - tp.width // 2 if layout == "full" else (
                62 if idx % 2 else card.width - tp.width - 62)
            card.alpha_composite(tp, (fx, 8))
        text = build_text(head, kick, seed=idx * 7 + 3, override=TEXT_OVERRIDE.get(fn))

        count = round(secs * FPS)
        for k in range(count):
            t = k / max(1, count - 1)
            fr = fields[scene].convert("RGBA")
            place(fr, card, effect, t, box)
            if head:                        # text rides its own track
                tt = min(1.0, k / max(1, int(FPS * .45)))
                lay = text
                if tt < 1.0:
                    lay = text.copy()
                    lay.putalpha(text.getchannel("A").point(lambda v: int(v * ease(tt))))
                fr.alpha_composite(lay, (0, round(18 * (1 - ease(tt)))))
            rgb = fr.convert("RGB")
            rgb = ImageChops.blend(rgb, ImageChops.overlay(rgb, GRAIN[n % 8]), .15)
            rgb.save(os.path.join(OUT, f"f{n:05d}.png"), compress_level=1)
            n += 1
        print(f"  {idx+1:2d}. {fn:<30} sc{scene} {layout:5s} {effect:14s}"
              f"{secs:5.1f}s -> {n/FPS:5.2f}s")

    print(f"\n{n} frames = {n/FPS:.2f}s @ {FPS}fps")


if __name__ == "__main__":
    main()
