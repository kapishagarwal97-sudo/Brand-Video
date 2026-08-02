#!/usr/bin/env python3
"""Layered keyframe animation toolkit for the TRYB Vox-style film.

The point of this module: a frame is not a picture that drifts. It is a STACK
OF LAYERS, each with its own keyframes and its own start time. Arrows draw
themselves on, paper strips snap in one after another, bars grow, counters
count up, cutouts pop in sequence. Everything is stepped on twos.
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "build", "fonts")

W, H = 1920, 1080
FPS = 12
PAD = 26          # shadow margin that paper() adds around its content

INK = (32, 26, 20)
ORANGE = (235, 100, 46)
CREAM = (244, 233, 213)
KRAFT = (214, 190, 152)
RED = (198, 48, 34)

TEAL = (24, 74, 78)
BRICK = (150, 46, 30)
MUSTARD = (206, 142, 26)
TRYB = (228, 88, 40)

F_HEAD = os.path.join(FONTS, "BigShoulders-Bold.ttf")
F_HAND = os.path.join(FONTS, "NothingYouCouldDo-Regular.ttf")
F_BODY = os.path.join(FONTS, "WorkSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ----------------------------------------------------------------- easing
def linear(t): return t
def out_cubic(t): return 1 - (1 - t) ** 3
def out_quint(t): return 1 - (1 - t) ** 5
def in_out(t): return t * t * (3 - 2 * t)


def back_out(t, s=1.9):
    """Overshoot — the snap that makes paper feel placed by hand."""
    t -= 1
    return t * t * ((s + 1) * t + s) + 1


def kf(t, t0, t1, a, b, ease=out_cubic):
    """Value of a property at shot-time t, animating a->b between t0 and t1."""
    if t <= t0:
        return a
    if t >= t1:
        return b
    return a + (b - a) * ease((t - t0) / (t1 - t0))


# ----------------------------------------------------------------- paper
def _torn_mask(w, h, seed, amp=7, step=11):
    """Irregular torn edge on all four sides."""
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    rnd = random.Random(seed)
    pts = []
    for x in range(0, w + step, step):
        pts.append((min(x, w), max(0, rnd.uniform(0, amp))))
    for y in range(0, h + step, step):
        pts.append((w - max(0, rnd.uniform(0, amp)), min(y, h)))
    for x in range(w, -step, -step):
        pts.append((max(x, 0), h - max(0, rnd.uniform(0, amp))))
    for y in range(h, -step, -step):
        pts.append((max(0, rnd.uniform(0, amp)), max(y, 0)))
    d.polygon(pts, fill=255)
    return m


def paper(w, h, colour, seed=0, torn=True, grain=True, shadow=True):
    """A rectangle of cardstock with torn edges and a soft drop shadow."""
    w, h = max(2, int(w)), max(2, int(h))
    base = Image.new("RGBA", (w, h), colour + (255,))
    if grain:
        n = Image.effect_noise((w, h), 9).convert("L")
        base = Image.composite(
            ImageEnhance.Brightness(base.convert("RGB")).enhance(1.03).convert("RGBA"),
            base, n.point(lambda v: 255 if v > 140 else 0))
    base.putalpha(_torn_mask(w, h, seed) if torn else Image.new("L", (w, h), 255))
    if not shadow:
        return base
    pad = 26
    out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.paste((25, 18, 12, 105), (pad + 3, pad + 7), base.getchannel("A"))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(11)))
    out.alpha_composite(base, (pad, pad))
    return out


def label(text, fnt, bg=CREAM, colour=INK, px=30, py=16, seed=0, torn=True):
    """Text on its own torn paper strip, padded correctly inside the shadow margin."""
    tl = text_layer(text, fnt, colour)
    card = paper(tl.width + px * 2, tl.height + py * 2, bg, seed, torn=torn)
    card.alpha_composite(tl, (PAD + px, PAD + py))
    return card


def circle_portrait(path, cx, cy, r, size=210, ring=CREAM):
    """Cut one circular portrait out of a larger collage.

    The supplied collage is already dot-screened, so this must NOT re-halftone
    it — doing so crushes the faces to black.
    """
    src = Image.open(os.path.join(ROOT, path)).convert("RGB")
    box = src.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r)))
    box = box.resize((size, size), Image.LANCZOS)
    box = ImageEnhance.Brightness(box).enhance(1.06)
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).ellipse([0, 0, size - 1, size - 1], fill=255)
    box = box.convert("RGBA")
    box.putalpha(m)

    ringw = 13
    out = Image.new("RGBA", (size + ringw * 2, size + ringw * 2), (0, 0, 0, 0))
    ImageDraw.Draw(out).ellipse([0, 0, out.width - 1, out.height - 1], fill=ring + (255,))
    out.alpha_composite(box, (ringw, ringw))

    pad = 22
    res = Image.new("RGBA", (out.width + pad * 2, out.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", res.size, (0, 0, 0, 0))
    sh.paste((25, 18, 12, 115), (pad + 3, pad + 8), out.getchannel("A"))
    res.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    res.alpha_composite(out, (pad, pad))
    return res


def tape(w=150, h=44, angle=-7, seed=0):
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rectangle([0, 0, w, h], fill=(230, 209, 165, 150))
    for i in range(0, w, 8):
        d.line([(i, 0), (i, h)], fill=(214, 190, 146, 60))
    rnd = random.Random(seed)
    for y in (0, h - 1):
        for x in range(0, w, 3):
            if rnd.random() < .6:
                d.rectangle([x, y, x + 2, y], fill=(0, 0, 0, 0))
    return t.rotate(angle, expand=True, resample=Image.BICUBIC)


# ----------------------------------------------------------------- photo
_HT_CACHE = {}


def halftone(path, w, cell=5, mono=True, contrast=1.25):
    """CMYK-style dot screen, like a newspaper photo. Cached per (path,w)."""
    key = (path, w, cell, mono)
    if key in _HT_CACHE:
        return _HT_CACHE[key]
    src = Image.open(os.path.join(ROOT, path)).convert("RGB")
    h = round(src.height * w / src.width)
    src = src.resize((w, h), Image.LANCZOS)
    src = ImageEnhance.Contrast(src).enhance(contrast)
    g = src.convert("L")
    small = g.resize((max(1, w // cell), max(1, h // cell)), Image.BOX)
    out = Image.new("RGB", (w, h), (247, 241, 227))
    d = ImageDraw.Draw(out)
    px = small.load()
    r_max = cell * 0.72
    for cy in range(small.height):
        for cx in range(small.width):
            v = px[cx, cy] / 255.0
            r = r_max * (1 - v) ** .85
            if r < .35:
                continue
            x, y = cx * cell + cell / 2, cy * cell + cell / 2
            d.ellipse([x - r, y - r, x + r, y + r], fill=(26, 22, 18))
    if not mono:
        out = Image.blend(out, src, 0.42)
    _HT_CACHE[key] = out
    return out


def photo_card(path, w, halftone_it=True, cell=5, border=18, seed=3, mono=True):
    """A torn photographic print, ready to be animated as one layer."""
    im = (halftone(path, w, cell, mono) if halftone_it
          else Image.open(os.path.join(ROOT, path)).convert("RGB"))
    if not halftone_it:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    cw, ch = im.width + border * 2, im.height + border * 2
    card = Image.new("RGBA", (cw, ch), (247, 241, 227, 255))
    card.paste(im, (border, border))
    card.putalpha(_torn_mask(cw, ch, seed, amp=6, step=13))
    pad = 26
    out = Image.new("RGBA", (cw + pad * 2, ch + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    sh.paste((25, 18, 12, 110), (pad + 3, pad + 8), card.getchannel("A"))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    out.alpha_composite(card, (pad, pad))
    return out


# ----------------------------------------------------------------- ink
def ink_path(pts, reveal=1.0, width=9, colour=INK, arrow=True, pad=60):
    """A hand-drawn stroke that DRAWS ITSELF ON as reveal goes 0->1."""
    if reveal <= 0:
        return None, (0, 0)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, y0 = min(xs) - pad, min(ys) - pad
    im = Image.new("RGBA", (int(max(xs) - x0 + pad), int(max(ys) - y0 + pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = [(x - x0, y - y0) for x, y in pts]

    # cumulative length so reveal is even along the stroke
    seg = [math.dist(P[i], P[i + 1]) for i in range(len(P) - 1)]
    total = sum(seg) or 1
    want = total * min(1.0, reveal)
    drawn, acc = [P[0]], 0.0
    for i, s in enumerate(seg):
        if acc + s <= want:
            drawn.append(P[i + 1]); acc += s
        else:
            f = (want - acc) / s
            drawn.append((P[i][0] + (P[i + 1][0] - P[i][0]) * f,
                          P[i][1] + (P[i + 1][1] - P[i][1]) * f))
            break
    if len(drawn) > 1:
        d.line(drawn, fill=colour, width=width, joint="curve")
        for p in drawn[::3]:                      # thicken like a marker
            d.ellipse([p[0] - width / 2, p[1] - width / 2,
                       p[0] + width / 2, p[1] + width / 2], fill=colour)
    if arrow and reveal > .93 and len(drawn) > 1:
        a, b = drawn[-2], drawn[-1]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        L, spread = width * 4.4, .46
        d.polygon([b,
                   (b[0] - L * math.cos(ang - spread), b[1] - L * math.sin(ang - spread)),
                   (b[0] - L * math.cos(ang + spread), b[1] - L * math.sin(ang + spread))],
                  fill=colour)
    return im, (x0, y0)


def ink_ellipse(cx, cy, rx, ry, reveal=1.0, width=8, colour=RED, turns=1.06):
    """An annotation circle scribbled around something."""
    pts = []
    n = 64
    for i in range(n + 1):
        a = -math.pi / 2 + turns * 2 * math.pi * i / n
        w = 1 + .035 * math.sin(i * .9)
        pts.append((cx + rx * w * math.cos(a), cy + ry * w * math.sin(a)))
    return ink_path(pts, reveal, width, colour, arrow=False)


# ----------------------------------------------------------------- type
def text_layer(text, fnt, colour=INK, spacing=1.02, align="left"):
    lines = text.split("\n")
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    wid = max(int(tmp.textlength(l, font=fnt)) for l in lines)
    lh = int(fnt.size * spacing)
    im = Image.new("RGBA", (wid + 8, lh * len(lines) + int(fnt.size * .45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        x = 0 if align == "left" else (wid - int(d.textlength(l, font=fnt))) // (
            2 if align == "center" else 1)
        d.text((x, i * lh), l, font=fnt, fill=colour)
    return im


def words_layer(text, fnt, reveal=1.0, colour=INK, spacing=1.02, per=0.55):
    """Words land one after another instead of the block fading in."""
    lines = [l.split(" ") for l in text.split("\n")]
    total = sum(len(l) for l in lines)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    wid = max(int(tmp.textlength(" ".join(l), font=fnt)) for l in lines)
    lh = int(fnt.size * spacing)
    im = Image.new("RGBA", (wid + 10, lh * len(lines) + int(fnt.size * .45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    k = 0
    span = 1.0 / max(1, total)
    for li, words in enumerate(lines):
        x = 0
        for wd in words:
            t0 = k * span * per
            a = max(0.0, min(1.0, (reveal - t0) / max(1e-6, span * per + .18)))
            if a > 0:
                dy = int(14 * (1 - out_cubic(a)))
                d.text((x, li * lh + dy), wd, font=fnt,
                       fill=colour + (int(255 * out_cubic(a)),))
            x += int(d.textlength(wd + " ", font=fnt))
            k += 1
    return im


def counter_layer(value, fnt, reveal, colour=INK, suffix=""):
    """A number that counts up rather than appearing."""
    cur = value * out_quint(max(0.0, min(1.0, reveal)))
    if isinstance(value, float):
        s = f"{cur:.1f}{suffix}"
    else:
        s = f"{int(round(cur))}{suffix}"
    return text_layer(s, fnt, colour)


# ----------------------------------------------------------------- ground
_FIELD = {}


def field(tint, seed=0):
    if tint in _FIELD:
        return _FIELD[tint]
    tex = Image.open(os.path.join(ROOT, "Blank cream paper texture.png")).convert("RGB")
    s = max(W / tex.width, H / tex.height)
    tex = tex.resize((math.ceil(tex.width * s), math.ceil(tex.height * s)), Image.LANCZOS)
    ox, oy = (tex.width - W) // 2, (tex.height - H) // 2
    tex = tex.crop((ox, oy, ox + W, oy + H))
    wash = Image.new("RGB", (W, H), tint)
    out = ImageChops.multiply(tex, wash)
    out = Image.blend(Image.new("RGB", (W, H), tint), out, 0.55)
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((int(-W * .3), int(-H * .4), int(W * 1.3), int(H * 1.4)), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(170))
    out = Image.composite(out, ImageEnhance.Brightness(out).enhance(.84), v)
    _FIELD[tint] = out
    return out


# ----------------------------------------------------------------- layers
class Layer:
    """One animated element. `img` is a PIL RGBA or a callable(t)->RGBA."""

    def __init__(self, img, x, y, anchor="c", anims=None, jitter=0, z=0):
        self.img, self.x, self.y = img, x, y
        self.anchor, self.anims, self.jitter, self.z = anchor, anims or {}, jitter, z

    def prop(self, name, t, default):
        spec = self.anims.get(name)
        if spec is None:
            return default
        v = default
        for (t0, t1, a, b, ease) in spec:
            v = kf(t, t0, t1, a, b, ease)
            if t < t1:
                break
        return v

    def render(self, frame, t, fidx):
        im = self.img(t) if callable(self.img) else self.img
        if im is None:
            return
        sc = self.prop("scale", t, 1.0)
        al = self.prop("alpha", t, 1.0)
        ro = self.prop("rot", t, 0.0)
        dx = self.prop("dx", t, 0.0)
        dy = self.prop("dy", t, 0.0)
        if al <= 0.003:
            return
        if abs(sc - 1) > 1e-3:
            im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))),
                           Image.LANCZOS)
        if abs(ro) > 1e-3:
            im = im.rotate(ro, expand=True, resample=Image.BICUBIC)
        if al < 0.997:
            im = im.copy()
            im.putalpha(im.getchannel("A").point(lambda v: int(v * al)))
        jx = jy = 0
        if self.jitter:
            r = random.Random(fidx * 31 + id(self) % 977)
            jx = r.randint(-self.jitter, self.jitter)
            jy = r.randint(-self.jitter, self.jitter)
        x, y = self.x + dx + jx, self.y + dy + jy
        if self.anchor == "c":
            pos = (round(x - im.width / 2), round(y - im.height / 2))
        elif self.anchor == "tl":
            pos = (round(x), round(y))
        elif self.anchor == "bl":
            pos = (round(x), round(y - im.height))
        else:                                    # bottom-centre
            pos = (round(x - im.width / 2), round(y - im.height))
        frame.alpha_composite(im, pos)


class Shot:
    def __init__(self, name, ground, dur, layers, whip=0.0):
        self.name, self.ground, self.dur, self.layers = name, ground, dur, layers
        self.whip = whip                          # horizontal exit speed for a whip cut

    def frame(self, t, fidx):
        fr = field(self.ground).convert("RGBA")
        for L in sorted(self.layers, key=lambda l: l.z):
            L.render(fr, t, fidx)
        return fr


# ----------------------------------------------------------------- grain
_GRAIN = []


def grain(i):
    if not _GRAIN:
        random.seed(5)
        for _ in range(8):
            g = Image.effect_noise((W // 2, H // 2), 22).convert("L")
            g = g.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(.5))
            _GRAIN.append(Image.merge("RGB", (g, g, g)))
    return _GRAIN[i % 8]


def finish(frame, i):
    rgb = frame.convert("RGB")
    return ImageChops.blend(rgb, ImageChops.overlay(rgb, grain(i)), .14)
