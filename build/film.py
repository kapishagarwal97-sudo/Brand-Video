#!/usr/bin/env python3
"""TRYB — "Alone, Together". The shot list, built as animated layer stacks.

Every shot composes independently-moving elements. Nothing here is a whole
picture drifting across the screen: strips snap in one after another, arrows
draw themselves on, bars grow, bubbles fall, counters count up.
"""
import math, os, random, shutil
from PIL import Image, ImageDraw
import vox as V
from vox import (Layer, Shot, paper, tape, label, photo_card, halftone, circle_portrait, logo,
                 ink_path, text_layer, words_layer, counter_layer, font, W, H, FPS, PAD,
                 INK, ORANGE, CREAM, KRAFT, RED, TEAL, BRICK, MUSTARD, TRYB,
                 F_HEAD, F_HAND, F_BODY, back_out, out_cubic, out_quint, linear)

OUT = os.path.join(V.ROOT, "frames")

DARK = {TEAL, BRICK, TRYB}                       # grounds that need cream type


def ink_for(ground):
    return CREAM if ground in DARK else INK


def hand_for(ground):
    return (247, 220, 198) if ground in DARK else (120, 104, 84)


# ----------------------------------------------------------------- builders
def headline(txt, ground, size=88, x=110, y=None, t0=.06, dur=.5):
    f = font(F_HEAD, size)
    col = ink_for(ground)
    return Layer(lambda t: words_layer(txt, f, max(0, (t - t0) / dur), col),
                 x, y if y is not None else H // 2, anchor="tl", z=40)


def rule(x, y, w, ground, t0=.42):
    col = ORANGE if ground not in (TRYB, BRICK) else CREAM

    def mk(t):
        r = max(0.0, min(1.0, (t - t0) / .32))
        pts = [(i, 6 + 2.0 * math.sin(i * .06)) for i in range(0, w, 10)]
        im, _ = ink_path(pts, r, 6, col, arrow=False, pad=14)
        return im
    return Layer(mk, x - 14, y - 14, anchor="tl", z=41)


def kicker(txt, x, y, ground, t0=.55):
    f = font(F_HAND, 46)
    col = hand_for(ground)
    return Layer(lambda t: words_layer(txt, f, max(0, (t - t0) / .4), col, per=.4),
                 x, y, anchor="tl", z=41)


def stroke(pts, t0, t1, width=9, colour=INK, arrow=True, z=60):
    _, off = ink_path(pts, 1.0, width, colour, arrow, 60)

    def mk(t):
        r = 0.0 if t <= t0 else (1.0 if t >= t1 else out_cubic((t - t0) / (t1 - t0)))
        im, _o = ink_path(pts, r, width, colour, arrow, 60)
        return im
    return Layer(mk, off[0], off[1], anchor="tl", z=z)


def photo(path, disp_w, **kw):
    """Build a print at up to 2x the display width; return (image, base scale)."""
    src_w = Image.open(os.path.join(V.ROOT, path)).width
    if kw.get("halftone_it", True):
        build = int(disp_w * 2)                 # dots are generated, so 2x is free
    else:
        build = int(min(disp_w * 2, max(disp_w, src_w)))   # never upscale a photo
    return photo_card(path, build, **kw), disp_w / build


def face(cx, cy, r, disp=200):
    build = int(min(disp * 2, 2 * r))
    return circle_portrait("09-curated-matches.png", cx, cy, r, build), disp / build


def annot_circle(cx, cy, rx, ry, t0, t1, colour=RED, width=8, z=60):
    """A pen circle scribbled around something, drawn on over time."""
    _, off = V.ink_ellipse(cx, cy, rx, ry, 1.0, width, colour)

    def mk(t):
        r = 0.0 if t <= t0 else (1.0 if t >= t1 else out_cubic((t - t0) / (t1 - t0)))
        im, _o = V.ink_ellipse(cx, cy, rx, ry, r, width, colour)
        return im
    return Layer(mk, off[0], off[1], anchor="tl", z=z)


def pop(t0, dur=.38, scale=1.0):
    """Snap in with overshoot — the signature paper-cutout entrance."""
    return {"scale": [(t0, t0 + dur, 0.62 * scale, scale, back_out)],
            "alpha": [(t0, t0 + dur * .35, 0, 1, linear)]}


def slide(t0, dx=0, dy=0, dur=.5):
    return {"dx": [(t0, t0 + dur, dx, 0, out_quint)],
            "dy": [(t0, t0 + dur, dy, 0, out_quint)],
            "alpha": [(t0, t0 + dur * .3, 0, 1, linear)]}


def fade(t0, dur=.5):
    return {"alpha": [(t0, t0 + dur, 0, 1, out_cubic)]}


# ══════════════════════════════════════════════════════════════════ SHOTS
def sc01_hook():
    """Crowd lands, headline lands word by word, one figure gets circled in red."""
    g = TEAL
    _hook_img, _hook_b = photo("01-hook-thumbnail.png", 980, halftone_it=False, seed=11)
    return Shot("hook", g, 3.0, [
        Layer(_hook_img, 1310, 470, base=_hook_b,
              anims={**slide(.05, dy=-70, dur=.55),
                     "rot": [(.05, .6, -2.4, -1.2, back_out)]}, jitter=1, z=10),
        Layer(tape(150, 44, -9, 2), 1310, 46, anims=pop(.42), z=30),
        headline("We've never been\nmore connected.", g, 92, 110, 370, t0=.28),
        rule(110, 600, 470, g, t0=.84),
        kicker("and never further apart", 116, 626, g, t0=1.0),
        annot_circle(1330, 640, 190, 150, 1.25, 1.95, RED, z=70),
    ])


def sc02_title():
    """Two torn strips snap in from opposite sides, then the arrow draws on."""
    g = TEAL
    f = font(F_HEAD, 132)
    return Shot("title", g, 2.6, [
        Layer(label("ALONE,", f, CREAM, INK, 45, 14, 4), 1060, 440,
              anims={**slide(.10, dx=-560, dur=.46),
                     "rot": [(.10, .56, -6, -1.8, back_out)]}, jitter=1, z=20),
        Layer(label("TOGETHER.", f, CREAM, INK, 45, 14, 9), 1010, 620,
              anims={**slide(.34, dx=620, dur=.46),
                     "rot": [(.34, .8, 6, 1.4, back_out)]}, jitter=1, z=21),
        stroke([(120, 690), (330, 640), (520, 556), (660, 500)], .78, 1.28, 15, RED, z=30),
    ])


def sc03_feed():
    """The feed genuinely scrolls; notification scraps pop in around it."""
    g = BRICK
    src = Image.open(os.path.join(V.ROOT, "02-endless-scroll.png")).convert("RGB")
    strip = src.resize((1100, round(src.height * 1100 / src.width)), Image.LANCZOS)
    strip = strip.crop((330, 720, 752, strip.height))      # just the unspooling ribbon
    tall = Image.new("RGB", (strip.width, strip.height * 2), (247, 241, 227))
    tall.paste(strip, (0, 0)); tall.paste(strip, (0, strip.height))
    band = 700

    def feed(t):
        off = int((t * 200) % strip.height)
        return tall.crop((0, off, tall.width, off + band)).convert("RGBA")

    L = [Layer(feed, 1130, 210, anchor="tl", anims=slide(.06, dy=90, dur=.5), z=10)]
    fb = font(F_BODY, 30)
    for i, (txt, x, y) in enumerate([("120 likes", 1035, 230), ("47 followers", 1700, 300),
                                     ("23 messages", 990, 430), ("9.8K views", 1760, 540),
                                     ("15 saved", 1010, 720)]):
        L.append(Layer(label(txt, fb, CREAM, INK, 23, 13, 20 + i), x, y,
                       anims=pop(.5 + i * .12), jitter=1, z=25))
    L += [headline("Hours vanish into\na feed with no end.", g, 84, 110, 390, t0=.22),
          rule(110, 590, 460, g, t0=.8),
          kicker("just five more minutes", 116, 616, g, t0=.96)]
    return Shot("feed", g, 3.2, L)


def sc04_chat():
    """Bubbles arrive one by one, then fall away. The calendar gets crossed out."""
    g = TEAL
    L = [Layer(paper(560, 720, (30, 34, 36), 31, torn=False), 1240, 540,
               anims=slide(.04, dy=80, dur=.5), z=10)]
    fb = font(F_BODY, 27)
    for i in range(5):
        b = label("let's catch up soon", fb, CREAM, INK, 26, 14, 40 + i)
        t0, fall = .28 + i * .12, 1.55 + i * .06
        L.append(Layer(b, 1180, 280 + i * 94, anims={
            **pop(t0, .32),
            "dy": [(t0, t0 + .32, -26, 0, back_out), (fall, fall + .9, 0, 560, out_cubic)],
            "rot": [(fall, fall + .9, 0, -18 + i * 8, out_cubic)],
            "alpha": [(t0, t0 + .12, 0, 1, linear), (fall + .35, fall + .8, 1, 0, linear)],
        }, jitter=1, z=20 + i))

    cal = paper(400, 470, CREAM, 60)
    d = ImageDraw.Draw(cal)
    d.text((PAD + 32, PAD + 26), "SATURDAY", font=font(F_HEAD, 42), fill=INK)
    for r in range(4):
        for c in range(6):
            d.rectangle([PAD + 30 + c * 57, PAD + 110 + r * 82,
                         PAD + 78 + c * 57, PAD + 172 + r * 82],
                        outline=(180, 168, 144), width=2)
    L.append(Layer(cal, 1690, 545, anims=slide(.52, dx=300, dur=.5), jitter=1, z=30))
    L.append(stroke([(1575, 390), (1800, 560)], 1.42, 1.68, 11, RED, arrow=False, z=40))
    L.append(stroke([(1800, 390), (1575, 560)], 1.62, 1.88, 11, RED, arrow=False, z=40))
    L += [headline("The group chat lives on.\nThe plans quietly die.", g, 74, 100, 410, t0=.18),
          rule(100, 580, 500, g, t0=.78),
          kicker("next time, for sure", 106, 606, g, t0=.94)]
    return Shot("chat", g, 3.2, L)


def sc05_postpone():
    """The phone tears across the embrace; the reply lands late; dots pulse."""
    g = MUSTARD
    _hug, _hugb = photo("04-couple-apart.png1.png", 980, halftone_it=False, seed=71)
    return Shot("postpone", g, 2.8, [
        Layer(_hug, 1130, 590, base=_hugb,
              anims={**slide(.05, dx=-110, dur=.55),
                     "rot": [(.05, .6, -2.6, -1.0, back_out)]}, jitter=1, z=10),
        annot_circle(1444, 567, 178, 74, 1.05, 1.75, RED, width=7, z=60),
        headline("Closeness became\nsomething we postpone.", g, 66, 100, 130, t0=.2),
        kicker("definitely soon", 106, 300, g, t0=1.0),
    ])


def sc06_data():
    """Bars grow one after another, the trend draws down, the counter counts up."""
    g = BRICK
    L = [Layer(label("TIME SPENT WITH\nFRIENDS IN PERSON", font(F_HEAD, 44),
                     CREAM, INK, 30, 18, 91), 330, 200, anims=pop(.08), z=30)]
    for i, hgt in enumerate([330, 268, 200, 132, 74]):
        bar = paper(96, hgt, CREAM, 100 + i)
        t0 = .30 + i * .10

        def mk(im=bar, tt0=t0):
            def f(t):
                r = 0.0 if t <= tt0 else (1.0 if t >= tt0 + .42 else out_cubic((t - tt0) / .42))
                if r <= .01:
                    return None
                nh = max(2, int(im.height * r))
                return im.crop((0, im.height - nh, im.width, im.height))
            return f
        L.append(Layer(mk(), 160 + i * 122, 830, anchor="b", jitter=1, z=20))
    L.append(stroke([(150, 470), (700, 745)], .85, 1.32, 10, CREAM, z=40))
    L.append(Layer(text_layer("VS.", font(F_HEAD, 118), CREAM), 900, 540,
                   anims=pop(1.18), z=40))
    L.append(Layer(paper(520, 660, CREAM, 120, torn=False), 1470, 560,
                   anims=slide(.5, dx=380, dur=.5), z=10))
    L.append(stroke([(1275 + i * 40, 790 - i * i * 1.8 - i * 7) for i in range(10)],
                    1.28, 1.95, 9, RED, arrow=False, z=30))
    fnum = font(F_HEAD, 96)
    L.append(Layer(lambda t: counter_layer(7.7, fnum, max(0, (t - 1.45) / .8), RED, "h"),
                   1330, 340, anchor="tl", anims=fade(1.42, .2), z=30))
    L.append(Layer(text_layer("DAILY SCREEN TIME", font(F_HEAD, 34), INK), 1330, 292,
                   anchor="tl", anims=fade(1.4), z=30))
    return Shot("data", g, 3.2, L)


def sc07_replaced():
    """The quiet beat. One photo, one line, almost no motion."""
    g = (236, 228, 208)
    _rep, _repb = photo("01-hook-thumbnail2.png", 1060, halftone_it=False, seed=131)
    return Shot("replaced", g, 2.5, [
        Layer(_rep, 630, 620, base=_repb,
              anims={**fade(.05, .8), "scale": [(.05, 1.6, 1.03, 1.0, out_cubic)]},
              jitter=1, z=10),
        headline("This is what\nit replaced.", g, 92, 1130, 270, t0=.5, dur=.7),
    ])


def sc08_reveal():
    """Brand turn: wordmark snaps in, tape lands after it."""
    g = MUSTARD
    return Shot("reveal", g, 2.2, [
        Layer(logo(820, CREAM), 960, 540, anims=pop(.10, .55), jitter=1, z=10),
        Layer(tape(140, 42, -12, 5), 600, 300, anims=pop(.58), z=30),
        Layer(tape(140, 42, 8, 6), 1330, 770, anims=pop(.70), z=30),
    ])


def sc09_question():
    """Chips arrive one by one; the paper hand taps and the chip depresses."""
    g = MUSTARD
    L = [Layer(paper(600, 790, CREAM, 141, torn=False), 1300, 540,
               anims=slide(.04, dy=110, dur=.5), z=10),
         Layer(text_layer("WHAT\nENERGIZES YOU?", font(F_HEAD, 56), INK), 1070, 230,
               anchor="tl", anims=fade(.28), z=20)]
    chips = [("deep conversations", KRAFT), ("outdoor adventures", (150, 166, 140)),
             ("creative expression", ORANGE), ("quiet time", (150, 176, 184))]
    tap = .92
    for i, (txt, col) in enumerate(chips):
        c = label(txt, font(F_BODY, 30), col, INK, 30, 20, 150 + i, torn=False)
        t0 = .40 + i * .12
        an = pop(t0, .34)
        if i == 2:
            an["scale"] = an["scale"] + [(tap, tap + .12, 1.0, .93, out_cubic),
                                         (tap + .12, tap + .32, .93, 1.0, back_out)]
        L.append(Layer(c, 1300, 410 + i * 100, anims=an, jitter=1, z=25))
    L.append(Layer(paper(180, 290, (234, 216, 188), 170, torn=False), 1600, 700,
                   anims=slide(.78, dx=260, dy=170, dur=.45), z=40))
    L += [headline("So tryb starts with\na better question.", g, 74, 100, 410, t0=.2),
          rule(100, 580, 470, g, t0=.8),
          kicker("not who you look like", 106, 606, g, t0=.95)]
    return Shot("question", g, 3.0, L)


def sc10_matched():
    """Badge lands, ink lines draw outward, portraits pop in around it."""
    g = TRYB
    L = [Layer(paper(210, 210, CREAM, 181, torn=False), 960, 560, anims=pop(.06, .45), z=40),
         Layer(logo(150, TRYB), 960, 566, anims=fade(.28), z=41)]
    # five real faces cut out of the supplied constellation collage
    faces = [(705, 180, 150), (290, 410, 150), (1115, 415, 150),
             (245, 880, 150), (1122, 887, 147)]
    R = 340
    for i, (cx, cy, r) in enumerate(faces):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        x, y = 960 + R * math.cos(a) * 1.5, 560 + R * math.sin(a)
        L.append(stroke([(960, 560), (x, y)], .42 + i * .09, .72 + i * .09, 6, CREAM,
                        arrow=False, z=20))
        fimg, fb = face(cx, cy, r, 200)
        L.append(Layer(fimg, x, y, base=fb,
                       anims=pop(.60 + i * .09, .36), jitter=1, z=30))
    L += [headline("Then it finds the people\nwho love the same things.", g, 62, 100, 110, t0=.15),
          kicker("five, not five thousand", 106, 290, g, t0=.88)]
    return Shot("matched", g, 3.0, L)


def sc11_pivot():
    """The arrow leaves the phone and the colour photo lands at the end of it."""
    g = MUSTARD
    ph = paper(500, 680, CREAM, 201, torn=False)
    ph.alpha_composite(text_layer("SATURDAY 7PM\nSUNSET DINNER", font(F_HEAD, 44), INK),
                       (PAD + 44, PAD + 130))
    ph.alpha_composite(text_layer("I'm in!", font(F_BODY, 30), ORANGE), (PAD + 44, PAD + 300))
    _piv, _pivb = photo("10-invitation-gathering.png", 800, halftone_it=False, seed=205)
    return Shot("pivot", g, 3.0, [
        Layer(ph, 430, 610, anims=slide(.05, dx=-360, dur=.5), jitter=1, z=10),
        stroke([(710, 570), (860, 505), (1010, 525)], .52, 1.0, 13, INK, z=30),
        Layer(_piv, 1370, 590, base=_pivb, anims={**pop(.98, .5),
                                "rot": [(.98, 1.46, 4, 1.2, back_out)]}, jitter=1, z=20),
        headline("From screen to table.", g, 82, 100, 170, t0=.2),
    ])


def sc12_payoff():
    """Full colour, no phones. Photos land, then confetti pops across the frame."""
    g = TRYB
    p1, b1 = photo("11-real-connection1.png", 880, halftone_it=False, seed=211)
    p2, b2 = photo("10-invitation-gathering1.png", 680, halftone_it=False, seed=213)
    L = [
        Layer(p1, 690, 580, base=b1,
              anims={**pop(.06, .5), "rot": [(.06, .56, -4, -1.5, back_out)]},
              jitter=1, z=10),
        Layer(p2, 1420, 650, base=b2,
              anims={**pop(.30, .5), "rot": [(.30, .8, 5, 2, back_out)]},
              jitter=1, z=11),
    ]
    rnd = random.Random(9)
    for i in range(14):
        L.append(Layer(paper(rnd.randint(14, 26), rnd.randint(14, 26),
                             rnd.choice([CREAM, MUSTARD, (150, 176, 184), KRAFT]),
                             220 + i, torn=False, shadow=False),
                       rnd.randint(120, 1820), rnd.randint(90, 990),
                       anims=pop(.66 + i * .035, .3), z=40))
    L += [headline("No feed. No scrolling.", g, 64, 100, 120, t0=.5),
          kicker("this is the whole point", 106, 250, g, t0=1.0)]
    return Shot("payoff", g, 2.6, L)


def sc13_yourpeople():
    """Four cut strips drop in staggered, each landing at its own angle."""
    g = TRYB
    f = font(F_HEAD, 116)
    L, y = [], 250
    for i, (wd, col, rot) in enumerate([("YOUR", CREAM, -3.0), ("PEOPLE", CREAM, 1.8),
                                        ("ARE", KRAFT, -1.6), ("OUT THERE", MUSTARD, 2.4)]):
        t0 = .08 + i * .15
        L.append(Layer(label(wd, f, col, INK, 42, 12, 240 + i), 880, y,
                       anims={**slide(t0, dy=-160, dur=.42),
                              "rot": [(t0, t0 + .42, rot * 3, rot, back_out)]},
                       jitter=1, z=20 + i))
        y += 150
    L.append(Layer(logo(300, CREAM), 960, 940, anims=pop(.84, .5), z=40))
    return Shot("yourpeople", g, 2.7, L)


def sc14_join():
    """Wordmark, underline draws on, then the CTA strip snaps in."""
    g = TRYB
    return Shot("join", g, 2.8, [
        Layer(logo(620, CREAM), 960, 390, anims=pop(.08, .55), z=20),
        stroke([(660, 560), (900, 576), (1180, 556), (1290, 568)], .52, .92, 7, CREAM,
               arrow=False, z=25),
        Layer(label("JOIN TRYB", font(F_HEAD, 84), KRAFT, INK, 55, 18, 251), 960, 790,
              anims=pop(.92, .45), jitter=1, z=30),
        stroke([(1420, 880), (1300, 812)], 1.35, 1.62, 8, INK, z=40),
    ])


SHOTS = [sc01_hook, sc02_title, sc03_feed, sc04_chat, sc05_postpone, sc06_data,
         sc07_replaced, sc08_reveal, sc09_question, sc10_matched, sc11_pivot,
         sc12_payoff, sc13_yourpeople, sc14_join]


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    built = [s() for s in SHOTS]
    total = sum(s.dur for s in built)
    print(f"  {len(built)} shots, {total:.2f}s total\n")
    assert total <= 40.0, f"cut is {total:.2f}s — over the 40s cap"
    n = 0
    for sh in built:
        for k in range(round(sh.dur * FPS)):
            V.finish(sh.frame(k / FPS, n), n).save(
                os.path.join(OUT, f"f{n:05d}.png"), compress_level=1)
            n += 1
        print(f"  {sh.name:<12} {sh.dur:4.1f}s -> {n/FPS:6.2f}s")
    print(f"\n{n} frames = {n/FPS:.2f}s @ {FPS}fps")


if __name__ == "__main__":
    main()
