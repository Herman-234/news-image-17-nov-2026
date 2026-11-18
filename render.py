#!/usr/bin/env python3
"""Render the 17 November 2026 world-news summary image (1024x1024 PNG).

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
GOLD = (232, 196, 104)
RED = (178, 34, 34)
CARD = (255, 255, 255)
BORDER = (214, 205, 184)
SKY = (135, 206, 235)
SEA = (46, 111, 164)
FLAME = (255, 122, 26)
FLAME2 = (255, 196, 0)


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

def icon_tanker(d, x, y, s):
    # sea
    d.rectangle([x, y + s * 0.72, x + s, y + s * 0.95], fill=SEA)
    d.arc([x, y + s * 0.80, x + s, y + s * 1.05], 0, 180, fill=(255, 255, 255), width=3)
    # hull
    d.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.92, y + s * 0.55),
               (x + s * 0.84, y + s * 0.74), (x + s * 0.16, y + s * 0.74)], fill=(60, 60, 60))
    # containers
    d.rectangle([x + s * 0.18, y + s * 0.38, x + s * 0.40, y + s * 0.55], fill=RED)
    d.rectangle([x + s * 0.44, y + s * 0.38, x + s * 0.66, y + s * 0.55], fill=GOLD)
    d.rectangle([x + s * 0.70, y + s * 0.44, x + s * 0.84, y + s * 0.55], fill=(120, 120, 120))
    # flame
    d.polygon([(x + s * 0.24, y + s * 0.38), (x + s * 0.32, y + s * 0.12),
               (x + s * 0.40, y + s * 0.38)], fill=FLAME)
    d.polygon([(x + s * 0.50, y + s * 0.38), (x + s * 0.58, y + s * 0.18),
               (x + s * 0.66, y + s * 0.38)], fill=FLAME2)


def icon_missile(d, x, y, s):
    # vertical rocket: nose cone, body, fins, flame
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


def icon_chip(d, x, y, s):
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                fill=NAVY, outline=GOLD, width=3)
    d.rectangle([x + s * 0.40, y + s * 0.40, x + s * 0.60, y + s * 0.60], fill=GOLD)
    for i in range(3):
        off = s * (0.32 + i * 0.18)
        d.line([x + off, y + s * 0.08, x + off, y + s * 0.22], fill=NAVY, width=4)
        d.line([x + off, y + s * 0.78, x + off, y + s * 0.92], fill=NAVY, width=4)
        d.line([x + s * 0.08, y + off, x + s * 0.22, y + off], fill=NAVY, width=4)
        d.line([x + s * 0.78, y + off, x + s * 0.92, y + off], fill=NAVY, width=4)


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
    pad = 18
    tx = x + pad
    ty = y + pad
    icon_w = 92 if icon else 0
    text_w = w - pad * 2 - icon_w
    kf = font("bold", 16)
    draw.text((tx, ty), kicker, font=kf, fill=kcolor)
    ty += 26
    hf = font("bold", 27)
    lines = wrap(draw, headline, hf, text_w)
    ty = draw_text_block(draw, tx, ty, lines[:2], hf, INK, 32)
    ty += 6
    bf = font("regular", 18)
    blines = wrap(draw, body, bf, text_w)
    draw_text_block(draw, tx, ty, blines[:3], bf, MUTED, 22)
    if icon:
        icon(draw, x + w - pad - 88, y + pad + 8, 88)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 104], fill=NAVY)
    tf = font("bold", 46)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 10), title, font=tf, fill=(255, 255, 255))
    df = font("bold", 27)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 62), date, font=df, fill=GOLD)
    d.rectangle([0, 104, W, 108], fill=GOLD)

    # lead story: Hormuz
    lx, ly, lw, lh = 16, 120, 992, 248
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10, fill=CARD,
                        outline=BORDER, width=2)
    d.rectangle([lx, ly, lx + 8, ly + lh], fill=RED)
    tx, ty = lx + 28, ly + 18
    kf = font("bold", 17)
    d.text((tx, ty), "US-IRAN  ·  STRAIT OF HORMUZ", font=kf, fill=RED)
    ty += 30
    hf = font("bold", 38)
    lines = wrap(d, "FOURTH TANKER IN 24 HOURS HITS A MINE", hf, 590)
    ty = draw_text_block(d, tx, ty, lines, hf, INK, 44)
    ty += 8
    bf = font("regular", 22)
    body = ("Iran's navy reports another tanker ablaze after striking a mine; "
            "a US drone is seized and an attack on a US base in Bahrain is intercepted.")
    blines = wrap(d, body, bf, 590)
    draw_text_block(d, tx, ty, blines, bf, MUTED, 28)
    icon_tanker(d, lx + 660, ly + 30, 300)

    # grid: 2 columns x 3 rows
    gx0, gx1 = 16, 520
    gw = 488
    rows = [(380, 200), (592, 200), (804, 200)]
    stories = [
        ("UKRAINE  ·  WAR", RED,
         "KYIV HIT BY MISSILES; CRIMEA BRIDGE CLOSED",
         "Russian missiles strike Kyiv's heat, water and bridges; Ukraine hits the Crimean Bridge.",
         icon_missile),
        ("DIPLOMACY  ·  APEC", NAVY,
         "XI, TRUMP AND PUTIN TO MEET THURSDAY",
         "China confirms a first-ever three-leader summit in Shenzhen on the APEC sidelines.",
         icon_summit),
        ("GAZA  ·  SANCTIONS", (0, 110, 70),
         "UK, AUSTRALIA SANCTION 8 FIRMS",
         "London sanctions eight Israeli firms over settlements; allies urge Israel to open Gaza aid.",
         icon_scales),
        ("TECH  ·  TRADE", NAVY,
         "US TIGHTENS AI CHIP EXPORT BAN ON CHINA",
         "Washington closes a chip-sale loophole as Nvidia reports earnings without Jensen Huang.",
         icon_chip),
        ("CLIMATE  ·  COP31", (0, 110, 70),
         "COP31 DRAFT: FASTER END TO FOSSIL FUELS",
         "Antalya negotiators propose a faster fossil-fuel phase-out and $120bn a year in climate finance.",
         icon_globe),
        (None, None, None, None, None),
    ]
    # row 1
    card(d, gx0, rows[0][0], gw, rows[0][1], stories[0][0], stories[0][1],
         stories[0][2], stories[0][3], stories[0][4])
    card(d, gx1, rows[0][0], gw, rows[0][1], stories[1][0], stories[1][1],
         stories[1][2], stories[1][3], stories[1][4])
    # row 2
    card(d, gx0, rows[1][0], gw, rows[1][1], stories[2][0], stories[2][1],
         stories[2][2], stories[2][3], stories[2][4])
    card(d, gx1, rows[1][0], gw, rows[1][1], stories[3][0], stories[3][1],
         stories[3][2], stories[3][3], stories[3][4])
    # row 3: COP31 + In brief panel
    card(d, gx0, rows[2][0], gw, rows[2][1], stories[4][0], stories[4][1],
         stories[4][2], stories[4][3], stories[4][4])
    bx, by, bw, bh = gx1, rows[2][0], gw, rows[2][1]
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=(240, 236, 224),
                        outline=BORDER, width=2)
    kf = font("bold", 16)
    d.text((bx + 18, by + 16), "IN BRIEF", font=kf, fill=NAVY)
    bf = font("regular", 19)
    briefs = [
        "France: 146,000 march for higher wages.",
        "Japan scrambles jets as Russian planes enter its airspace.",
        "Depardieu drops appeal in sex-assault case.",
    ]
    yy = by + 46
    for item in briefs:
        d.ellipse([bx + 20, yy + 7, bx + 30, yy + 17], fill=RED)
        for ln in wrap(d, item, bf, bw - 62):
            d.text((bx + 40, yy), ln, font=bf, fill=INK)
            yy += 24
        yy += 4
    sf = font("regular", 14)
    d.text((bx + 18, by + bh - 26),
           "Compiled from wire reports published 17 Nov 2026.",
           font=sf, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
