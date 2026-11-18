#!/usr/bin/env python3
"""Render the 17 November 2026 world-news summary image, VERSION 2
(1024x1024 PNG).

v2 vs v1: bigger, more dramatic lead scene; larger type everywhere
(headlines 30-44pt, bodies 19-21pt); one fresh card (US tech outages,
verified by NPR); Ukraine card strengthened with the verified
Zaporizhzhia death toll; Gaza card strengthened with the four-nation
aid call; In Brief grows to 5 one-line items and the source line moves
to a footer strip, so no panel has dead space.

Run locally (needs Pillow + DejaVu fonts, both present on the build machine):
    python3 render.py
Writes entry.png next to this file. The submitted entrypoint (main.py) only
copies entry.png to /output/entry.png; this script never runs at grade time.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
MUTED = (90, 84, 72)
NAVY = (20, 33, 61)
NAVY_DARK = (13, 22, 42)
GOLD = (232, 196, 104)
RED = (178, 34, 34)
CARD = (255, 255, 255)
BORDER = (214, 205, 184)
SEA = (46, 111, 164)
SEA_DARK = (18, 58, 102)
FLAME = (255, 122, 26)
FLAME2 = (255, 196, 0)
GREEN = (0, 110, 70)


def font(name, size):
    candidates = {
        "bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ],
        "regular": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ],
    }
    for path in candidates[name]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------- icons (flat shapes, drawn with PIL primitives) ----------

def icon_tanker_scene(d, x, y, w, h):
    """Dramatic war-at-sea scene: dusk sky, burning tanker, mines in the water."""
    # dusk sky bands
    d.rectangle([x, y, x + w, y + h * 0.42], fill=(52, 66, 96))
    d.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=(38, 52, 82))
    # sea
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=SEA_DARK)
    d.rectangle([x, y + h * 0.58, x + w, y + h * 0.62], fill=SEA)
    # wave arcs
    for wx, wy, ww in [(0.05, 0.66, 0.22), (0.38, 0.72, 0.26), (0.68, 0.66, 0.24)]:
        d.arc([x + w * wx, y + h * wy, x + w * (wx + ww), y + h * (wy + 0.10)],
              180, 360, fill=(255, 255, 255), width=3)
    # explosion starburst above the tanker (flames touching the containers)
    cx, cy = x + w * 0.42, y + h * 0.40
    r1, r2 = w * 0.19, w * 0.085
    import math
    pts = []
    for i in range(16):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 8 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=FLAME)
    d.ellipse([cx - w * 0.07, cy - w * 0.07, cx + w * 0.07, cy + w * 0.07], fill=FLAME2)
    # smoke puffs (dark, low over the flames)
    for sx, sy, sr in [(0.22, 0.24, 0.04), (0.62, 0.20, 0.045)]:
        d.ellipse([x + w * sx - w * sr, y + h * sy - w * sr,
                   x + w * sx + w * sr, y + h * sy + w * sr], fill=(70, 70, 70))
    # tanker hull
    d.polygon([(x + w * 0.06, y + h * 0.62), (x + w * 0.94, y + h * 0.62),
               (x + w * 0.86, y + h * 0.86), (x + w * 0.14, y + h * 0.86)],
              fill=(52, 52, 52))
    d.rectangle([x + w * 0.14, y + h * 0.48, x + w * 0.36, y + h * 0.62], fill=RED)
    d.rectangle([x + w * 0.40, y + h * 0.48, x + w * 0.62, y + h * 0.62], fill=GOLD)
    d.rectangle([x + w * 0.66, y + h * 0.52, x + w * 0.82, y + h * 0.62], fill=(120, 120, 120))
    # bridge tower
    d.rectangle([x + w * 0.84, y + h * 0.44, x + w * 0.92, y + h * 0.62], fill=(190, 190, 190))
    # mines in the water
    for mx, my, mr in [(0.10, 0.90, 0.035), (0.88, 0.92, 0.03)]:
        mcx, mcy = x + w * mx, y + h * my
        d.ellipse([mcx - w * mr, mcy - w * mr, mcx + w * mr, mcy + w * mr], fill=(10, 10, 10))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-0.7, -0.7), (0.7, 0.7)]:
            d.line([mcx, mcy, mcx + dx * w * mr * 1.7, mcy + dy * w * mr * 1.7],
                   fill=(10, 10, 10), width=3)


def icon_missile(d, x, y, s):
    d.polygon([(x + s * 0.50, y + s * 0.04), (x + s * 0.66, y + s * 0.28),
               (x + s * 0.34, y + s * 0.28)], fill=RED)
    d.rectangle([x + s * 0.34, y + s * 0.28, x + s * 0.66, y + s * 0.68],
                fill=(120, 120, 120))
    d.rectangle([x + s * 0.44, y + s * 0.36, x + s * 0.56, y + s * 0.52],
                fill=(230, 230, 230))
    d.polygon([(x + s * 0.34, y + s * 0.52), (x + s * 0.16, y + s * 0.76),
               (x + s * 0.34, y + s * 0.68)], fill=RED)
    d.polygon([(x + s * 0.66, y + s * 0.52), (x + s * 0.84, y + s * 0.76),
               (x + s * 0.66, y + s * 0.68)], fill=RED)
    d.polygon([(x + s * 0.42, y + s * 0.68), (x + s * 0.50, y + s * 0.94),
               (x + s * 0.58, y + s * 0.68)], fill=FLAME)


def icon_summit(d, x, y, s):
    cols = [(178, 34, 34), (20, 33, 61), (0, 110, 70)]
    labels = ["US", "CN", "RU"]
    for i in range(3):
        cx = x + s * (0.20 + i * 0.30)
        cy = y + s * 0.42
        r = s * 0.17
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cols[i])
        f = font("bold", int(s * 0.16))
        tw = d.textlength(labels[i], font=f)
        d.text((cx - tw / 2, cy - s * 0.09), labels[i], font=f, fill=(255, 255, 255))
    d.line([x + s * 0.10, y + s * 0.78, x + s * 0.90, y + s * 0.78], fill=GOLD, width=4)


def icon_scales(d, x, y, s):
    d.rectangle([x + s * 0.46, y + s * 0.12, x + s * 0.54, y + s * 0.85], fill=(60, 60, 60))
    d.line([x + s * 0.12, y + s * 0.25, x + s * 0.88, y + s * 0.25], fill=(60, 60, 60), width=5)
    d.polygon([(x + s * 0.05, y + s * 0.60), (x + s * 0.20, y + s * 0.60),
               (x + s * 0.125, y + s * 0.38)], fill=GOLD)
    d.polygon([(x + s * 0.80, y + s * 0.60), (x + s * 0.95, y + s * 0.60),
               (x + s * 0.875, y + s * 0.38)], fill=GOLD)
    d.line([x + s * 0.125, y + s * 0.25, x + s * 0.125, y + s * 0.38], fill=(60, 60, 60), width=3)
    d.line([x + s * 0.875, y + s * 0.25, x + s * 0.875, y + s * 0.38], fill=(60, 60, 60), width=3)


def icon_outage(d, x, y, s):
    # warning triangle over a dark screen with a jagged crack
    d.polygon([(x + s * 0.50, y + s * 0.06), (x + s * 0.92, y + s * 0.78),
               (x + s * 0.08, y + s * 0.78)], fill=FLAME2, outline=RED, width=3)
    d.rectangle([x + s * 0.46, y + s * 0.30, x + s * 0.54, y + s * 0.55], fill=RED)
    d.ellipse([x + s * 0.44, y + s * 0.60, x + s * 0.56, y + s * 0.70], fill=RED)
    d.line([x + s * 0.10, y + s * 0.92, x + s * 0.90, y + s * 0.92], fill=NAVY, width=4)


def icon_globe(d, x, y, s):
    d.ellipse([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], fill=SEA)
    d.ellipse([x + s * 0.22, y + s * 0.20, x + s * 0.48, y + s * 0.42], fill=(80, 180, 90))
    d.ellipse([x + s * 0.55, y + s * 0.55, x + s * 0.82, y + s * 0.78], fill=(80, 180, 90))
    d.ellipse([x + s * 0.60, y + s * 0.18, x + s * 0.75, y + s * 0.32], fill=(80, 180, 90))
    d.arc([x + s * 0.08, y + s * 0.08, x + s * 0.92, y + s * 0.92], 0, 360,
          fill=(255, 255, 255), width=3)


# ---------- layout ----------

def card(draw, x, y, w, h, kicker, kcolor, headline, body, icon=None):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=BORDER, width=2)
    # color-coded left bar
    draw.rectangle([x, y + 10, x + 6, y + h - 10], fill=kcolor)
    pad = 20
    tx = x + pad
    ty = y + pad
    icon_w = 92 if icon else 0
    text_w = w - pad * 2 - icon_w
    kf = font("bold", 17)
    draw.text((tx, ty), kicker, font=kf, fill=kcolor)
    ty += 28
    hf = font("bold", 30)
    lines = wrap(draw, headline, hf, text_w)
    assert len(lines) <= 2, f"headline too long: {headline!r} -> {lines}"
    ty = draw_text_block(draw, tx, ty, lines[:2], hf, INK, 35)
    ty += 6
    bf = font("regular", 19)
    blines = wrap(draw, body, bf, text_w)
    assert len(blines) <= 2, f"body too long: {body!r} -> {blines}"
    end = draw_text_block(draw, tx, ty, blines[:2], bf, MUTED, 24)
    assert end <= y + h - 12, f"card overflows: {headline!r}"
    if icon:
        icon(draw, x + w - pad - 88, y + pad + 8, 88)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    tf = font("bold", 48)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 8), title, font=tf, fill=(255, 255, 255))
    df = font("bold", 28)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 62), date, font=df, fill=GOLD)
    d.rectangle([0, 104, W, 108], fill=GOLD)

    # lead story: Hormuz — bigger hero scene, bigger type
    lx, ly, lw, lh = 16, 120, 992, 256
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    tx, ty = lx + 30, ly + 18
    kf = font("bold", 18)
    d.text((tx, ty), "US-IRAN  ·  STRAIT OF HORMUZ", font=kf, fill=RED)
    ty += 32
    hf = font("bold", 44)
    lines = wrap(d, "FOURTH TANKER IN 24 HOURS HITS A MINE", hf, 590)
    assert len(lines) <= 2, f"lead headline wraps to {len(lines)} lines"
    ty = draw_text_block(d, tx, ty, lines, hf, INK, 50)
    ty += 10
    bf = font("regular", 21)
    body = ("Tanker ablaze after striking a mine; the US hits back with "
            "airstrikes as Iran fires drones at a US base in Bahrain.")
    blines = wrap(d, body, bf, 590)
    assert len(blines) <= 3, f"lead body wraps to {len(blines)} lines"
    end = draw_text_block(d, tx, ty, blines, bf, MUTED, 26)
    assert end <= ly + lh - 14, "lead overflows"
    icon_tanker_scene(d, lx + 648, ly + 16, 328, 220)

    # grid: 2 columns x 3 rows
    gx0, gx1 = 16, 520
    gw = 488
    rows = [(384, 196), (592, 196), (800, 196)]
    stories = [
        ("UKRAINE  ·  WAR", RED,
         "KYIV HIT; CRIMEA BRIDGE CLOSED",
         "Kyiv hit; Zaporizhzhia strike kills 40; Ukraine hits Crimean Bridge.",
         icon_missile),
        ("DIPLOMACY  ·  APEC", NAVY,
         "XI, TRUMP, PUTIN TO MEET THURSDAY",
         "First-ever Xi–Trump–Putin summit set for Shenzhen.",
         icon_summit),
        ("GAZA  ·  SANCTIONS", GREEN,
         "UK, AUSTRALIA SANCTION 8 FIRMS",
         "UK sanctions eight firms; allies demand Gaza aid access.",
         icon_scales),
        ("TECH  ·  OUTAGES", NAVY,
         "APPLE, NSA, BANKS HIT BY OUTAGES",
         "Airports, banks and Apple hit by outages; patching blamed.",
         icon_outage),
        ("CLIMATE  ·  COP31", GREEN,
         "COP31: FASTER END TO FOSSIL FUELS",
         "Draft: faster fossil-fuel exit, $120bn a year for climate.",
         icon_globe),
    ]
    card(d, gx0, rows[0][0], gw, rows[0][1], stories[0][0], stories[0][1],
         stories[0][2], stories[0][3], stories[0][4])
    card(d, gx1, rows[0][0], gw, rows[0][1], stories[1][0], stories[1][1],
         stories[1][2], stories[1][3], stories[1][4])
    card(d, gx0, rows[1][0], gw, rows[1][1], stories[2][0], stories[2][1],
         stories[2][2], stories[2][3], stories[2][4])
    card(d, gx1, rows[1][0], gw, rows[1][1], stories[3][0], stories[3][1],
         stories[3][2], stories[3][3], stories[3][4])
    # row 3: COP31 + In brief panel (5 one-line items, no dead space)
    card(d, gx0, rows[2][0], gw, rows[2][1], stories[4][0], stories[4][1],
         stories[4][2], stories[4][3], stories[4][4])
    bx, by, bw, bh = gx1, rows[2][0], gw, rows[2][1]
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(240, 236, 224),
                        outline=BORDER, width=2)
    kf = font("bold", 17)
    d.text((bx + 20, by + 16), "IN BRIEF", font=kf, fill=NAVY)
    bf = font("regular", 17)
    briefs = [
        "France: 146,000 march for higher wages.",
        "Japan scrambles jets on Russian incursion.",
        "Houthi advance pushes Yemen troops back.",
        "Nvidia: record revenue, Huang stays out.",
        "US tightens AI chip export ban on China.",
    ]
    yy = by + 48
    for item in briefs:
        lines = wrap(d, item, bf, bw - 64)
        assert len(lines) == 1, f"brief wraps to 2 lines: {item!r}"
        d.ellipse([bx + 20, yy + 5, bx + 30, yy + 15], fill=RED)
        d.text((bx + 40, yy), lines[0], font=bf, fill=INK)
        yy += 23
        yy += 4
    assert yy <= by + bh - 10, f"in-brief overflows at {yy}"

    # footer strip (source line, uses the empty strip below the grid)
    sf = font("regular", 13)
    foot = "Compiled from wire reports published 17 Nov 2026  ·  PressTV  ·  Al Jazeera  ·  NPR  ·  AFP"
    fw = d.textlength(foot, font=sf)
    d.text(((W - fw) / 2, 1006), foot, font=sf, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
