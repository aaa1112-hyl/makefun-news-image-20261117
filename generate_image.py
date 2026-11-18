#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

Pure Pillow, no network. Run: python3 generate_image.py
Writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 25)
GREY = (90, 86, 78)
RED = (158, 27, 27)
BLUE = (31, 78, 121)
GOLD = (176, 124, 20)
LINE = (25, 25, 25)
SOFT = (232, 226, 212)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit in width px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.28):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, text):
    f = font(SANS_B, 19)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 26


def rule(draw, x0, y, x1, w=2):
    draw.line([(x0, y), (x1, y)], fill=LINE, width=w)


def draw_bridge(draw, x0, y0, x1, y1):
    """Stylised bridge with a broken middle span over water."""
    draw.rectangle([x0, y0, x1, y1], fill=(219, 228, 236))
    draw.rectangle([x0, y0, x1, y0 + 8], fill=BLUE)
    mid = (x0 + x1) // 2
    # deck, left and right of the break
    draw.line([(x0 + 12, y0 + 78), (mid - 34, y0 + 78)], fill=INK, width=7)
    draw.line([(mid + 34, y0 + 78), (x1 - 12, y0 + 78)], fill=INK, width=7)
    # towers
    for tx in (x0 + 34, x1 - 40):
        draw.line([(tx, y0 + 22), (tx, y0 + 78)], fill=INK, width=6)
    # cables
    draw.line([(x0 + 34, y0 + 22), (mid - 34, y0 + 78)], fill=GREY, width=2)
    draw.line([(x1 - 40, y0 + 22), (mid + 34, y0 + 78)], fill=GREY, width=2)
    # broken span: a short deck piece dropping into the gap
    draw.line([(mid - 24, y0 + 78), (mid - 6, y0 + 104)], fill=RED, width=7)
    draw.line([(mid - 6, y0 + 104), (mid + 16, y0 + 108)], fill=RED, width=7)
    # blast burst
    cx, cy = mid, y0 + 74
    for dx, dy in ((-16, 0), (16, 0), (0, -14), (0, 14), (-11, -11), (11, -11)):
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=RED, width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED)
    # water
    for i, wy in enumerate((y1 - 34, y1 - 20, y1 - 6)):
        off = 0 if i % 2 == 0 else 14
        for wx in range(x0 + 8 + off, x1 - 20, 44):
            draw.arc([wx, wy, wx + 34, wy + 14], 0, 180, fill=BLUE, width=3)
    draw.text((x0 + 10, y1 - 52), "KERCH BRIDGE", font=font(SANS_B, 15), fill=BLUE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 44  # margin

    # --- masthead -------------------------------------------------------
    d.text((mx, 26), "THE WORLD", font=font(SERIF, 96), fill=INK)
    d.text((W - mx - 238, 52), "IN ONE DAY", font=font(SANS_B, 30), fill=RED)
    rule(d, mx, 148, W - mx, 3)
    d.text((mx, 160), "TUESDAY, 17 NOVEMBER 2026", font=font(SANS_B, 24), fill=INK)
    d.text((W - mx - 330, 162), "One day's news, in one picture",
           font=font(SERIF_R, 20), fill=GREY)
    rule(d, mx, 196, W - mx, 1)

    # --- lead story: the bridge war -------------------------------------
    y = 214
    y = kicker(d, mx, y, "EUROPE  |  WAR IN UKRAINE")
    head = "Ukraine hits Crimea bridge again \u2014 Russia strikes Kyiv's bridges"
    y = para(d, mx, y, head, font(SERIF, 40), 600, leading=1.12)
    y += 6
    deck = ("Kyiv says its forces severely damaged the Kerch link for a "
            "second day running; Zelenskyy calls it an \u201cunprecedented "
            "operation\u201d. Moscow hit Kyiv's two Dnipro bridges; "
            "both were shut.")
    y = para(d, mx, y, deck, font(SANS, 21), 600)
    # bridge graphic, right of the lead text
    draw_bridge(d, 692, 214, 980, 452)
    rule(d, mx, 492, W - mx, 1)

    # --- second row: two columns ----------------------------------------
    y = 508
    col_w = 448
    # left: Middle East
    x = mx
    y1 = kicker(d, x, y, "MIDDLE EAST")
    y1 = para(d, x, y1, "Iran drones target US radar in Bahrain",
              font(SERIF, 30), col_w, leading=1.12)
    y1 += 4
    y1 = para(d, x, y1,
              "Tehran says its Guards hit the radar at Sheikh Isa base; "
              "Bahrain says it intercepted the drones. No casualties "
              "were reported.",
              font(SANS, 19), col_w)
    y1 += 8
    y1 = para(d, x, y1,
              "US officials tell CNN Iran is weighing attacks on Trump "
              "officials; the White House: no credible threat.",
              font(SANS, 17), col_w, fill=GREY)
    # right: Asia
    x = mx + 488
    y2 = kicker(d, x, y, "ASIA  |  DIPLOMACY")
    y2 = para(d, x, y2, "Trump lands in Manila as a three-way summit is set",
              font(SERIF, 30), col_w, leading=1.12)
    y2 += 4
    y2 = para(d, x, y2,
              "Quad leaders meet in Manila; Xi, Trump and Putin are due "
              "in Shenzhen on Thursday for a first trilateral, on the "
              "APEC sidelines.",
              font(SANS, 19), col_w)
    y2 += 8
    y2 = para(d, x, y2,
              "Trump may also meet Kim Jong Un in China this week.",
              font(SANS, 17), col_w, fill=GREY)
    rule(d, mx, 736, W - mx, 1)

    # --- also today strip ------------------------------------------------
    y = 754
    d.text((mx, y), "ALSO TODAY", font=font(SANS_B, 20), fill=RED)
    d.text((W - mx - 300, y + 2), "Tuesday 17 November 2026",
           font=font(SERIF_R, 18), fill=GREY)
    y += 34
    items = [
        ("UK sanctions", "eight Israeli firms building West Bank settlements."),
        ("Japan scrambles jets", "after suspected Russian planes enter its airspace."),
        ("Mongolia's president", "says he will resign amid bribery claims."),
        ("China and Canada", "agree new tariff cuts and deeper ties."),
        ("UN talks in Geneva", "on banning lethal autonomous weapons."),
        ("Cyberattack", "hits 178 sites, including the BBC and CNN."),
    ]
    cw = 296
    for i, (lead, rest) in enumerate(items):
        cx = mx + (i % 3) * (cw + 16)
        cy = y + (i // 3) * 96
        d.rectangle([cx, cy + 4, cx + 10, cy + 14], fill=RED)
        tx = cx + 20
        ty = para(d, tx, cy, lead + " " + rest, font(SANS, 17),
                  cw - 20, leading=1.22)
    rule(d, mx, 952, W - mx, 1)
    d.text((mx, 964), "Sources: Reuters, BBC, CNN, Just Security, AP",
           font=font(SANS, 15), fill=GREY)
    d.text((W - mx - 268, 964), "Drawn from reports of 17 Nov 2026",
           font=font(SANS, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
