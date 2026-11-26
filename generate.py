#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Stories (all verified against reporting dated 26 November 2026 or carried
in the 26 November editions of the world's press):
  1. Thanksgiving Day in the United States (White House proclamation).
  2. US tariff salvo on 14 partners; Taiwan says its 15% deal stands (Reuters).
  3. North Korea expels the Swiss envoy and shuts the Pyongyang office
     (Yonhap / Al Jazeera / Korea Times, 26 Nov editions).
  4. Record migrant arrivals in Spain's Canary Islands (Reuters / AP).
  5. JD Vance defends Nvidia chief Jensen Huang (AP / CNN).
  6. Shenzhou-24 carries the first foreign astronaut to Tiangong (Xinhua / AP).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
NAVY = (22, 50, 79)
RED = (176, 42, 48)
GOLD = (201, 162, 39)
GREY = (90, 86, 78)
CARD = (255, 253, 247)
LINE = (200, 192, 175)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_turkey(d, x, y, s):
    # fan tail
    for i, col in enumerate([(176, 42, 48), (201, 120, 39), (120, 90, 40),
                             (176, 42, 48), (201, 120, 39)]):
        a0 = 200 + i * 28
        d.pieslice([x - s, y - s, x + s, y + s], a0, a0 + 26, fill=col)
    # body
    d.ellipse([x - s * 0.55, y - s * 0.25, x + s * 0.55, y + s * 0.75],
              fill=(120, 72, 32))
    # wing
    d.ellipse([x - s * 0.35, y + s * 0.05, x + s * 0.25, y + s * 0.55],
              fill=(90, 52, 22))
    # head + neck
    d.ellipse([x - s * 0.22, y - s * 0.75, x + s * 0.22, y - s * 0.30],
              fill=(120, 72, 32))
    d.polygon([(x + s * 0.20, y - s * 0.55), (x + s * 0.45, y - s * 0.45),
               (x + s * 0.20, y - s * 0.38)], fill=(230, 140, 40))
    d.ellipse([x + s * 0.02, y - s * 0.62, x + s * 0.10, y - s * 0.54],
              fill=(17, 17, 17))


def icon_ship(d, x, y, s):
    # stacked containers
    cols = [(176, 42, 48), (22, 90, 120), (201, 162, 39), (60, 120, 60)]
    for r in range(2):
        for c in range(3):
            d.rectangle([x - s + c * s * 0.68, y - s * 0.9 + r * s * 0.45,
                         x - s + (c + 1) * s * 0.68 - 4,
                         y - s * 0.9 + (r + 1) * s * 0.45 - 4],
                        fill=cols[(r * 3 + c) % 4])
    # hull
    d.polygon([(x - s * 1.15, y + s * 0.05), (x + s * 1.15, y + s * 0.05),
               (x + s * 0.85, y + s * 0.55), (x - s * 0.85, y + s * 0.55)],
              fill=(22, 50, 79))
    # waves
    for i in range(3):
        d.arc([x - s + i * s * 0.7, y + s * 0.65, x - s * 0.3 + i * s * 0.7,
               y + s * 0.95], 0, 180, fill=(22, 90, 120), width=3)


def icon_gate(d, x, y, s):
    # closed door with crossbar
    d.rectangle([x - s * 0.7, y - s, x + s * 0.7, y + s], fill=(90, 60, 40))
    d.rectangle([x - s * 0.7, y - s * 0.15, x + s * 0.7, y + s * 0.15],
                fill=(40, 26, 18))
    for i in range(4):
        d.line([x - s * 0.7, y - s + i * s * 0.5, x + s * 0.7,
                y - s + i * s * 0.5], fill=(60, 40, 26), width=2)
    # Swiss cross badge
    d.rectangle([x + s * 0.35, y - s * 1.25, x + s * 1.05, y - s * 0.55],
                fill=(176, 42, 48))
    d.rectangle([x + s * 0.62, y - s * 1.18, x + s * 0.78, y - s * 0.62],
                fill=(255, 255, 255))
    d.rectangle([x + s * 0.42, y - s * 0.98, x + s * 0.98, y - s * 0.82],
                fill=(255, 255, 255))


def icon_boat(d, x, y, s):
    d.polygon([(x - s, y), (x + s, y), (x + s * 0.7, y + s * 0.45),
               (x - s * 0.7, y + s * 0.45)], fill=(150, 90, 40))
    for i, px in enumerate([-0.55, -0.18, 0.18, 0.55]):
        d.ellipse([x + px * s - 6, y - 16, x + px * s + 6, y - 4],
                  fill=(22, 50, 79))
    d.line([x - s * 1.1, y + s * 0.6, x + s * 1.1, y + s * 0.6],
           fill=(22, 90, 120), width=3)
    d.arc([x - s, y + s * 0.55, x - s * 0.4, y + s * 0.9], 0, 180,
          fill=(22, 90, 120), width=3)
    d.arc([x + s * 0.4, y + s * 0.55, x + s, y + s * 0.9], 0, 180,
          fill=(22, 90, 120), width=3)


def icon_chip(d, x, y, s):
    d.rectangle([x - s * 0.7, y - s * 0.7, x + s * 0.7, y + s * 0.7],
                fill=(22, 50, 79))
    d.rectangle([x - s * 0.35, y - s * 0.35, x + s * 0.35, y + s * 0.35],
                fill=(60, 160, 90))
    for i in range(4):
        px = x - s * 0.45 + i * s * 0.3
        d.line([px, y - s * 0.95, px, y - s * 0.7], fill=(120, 120, 120),
               width=4)
        d.line([px, y + s * 0.7, px, y + s * 0.95], fill=(120, 120, 120),
               width=4)
        py = y - s * 0.45 + i * s * 0.3
        d.line([x - s * 0.95, py, x - s * 0.7, py], fill=(120, 120, 120),
               width=4)
        d.line([x + s * 0.7, py, x + s * 0.95, py], fill=(120, 120, 120),
               width=4)


def icon_rocket(d, x, y, s):
    # stars
    for sx, sy in [(-0.9, -0.9), (0.85, -0.7), (-0.7, 0.5), (0.9, 0.35)]:
        d.ellipse([x + sx * s - 3, y + sy * s - 3, x + sx * s + 3,
                   y + sy * s + 3], fill=(201, 162, 39))
    # body
    d.polygon([(x, y - s), (x + s * 0.35, y - s * 0.2),
               (x + s * 0.35, y + s * 0.45), (x - s * 0.35, y + s * 0.45),
               (x - s * 0.35, y - s * 0.2)], fill=(200, 220, 235),
              outline=NAVY, width=2)
    d.polygon([(x, y - s), (x + s * 0.35, y - s * 0.2),
               (x - s * 0.35, y - s * 0.2)], fill=(176, 42, 48))
    # window
    d.ellipse([x - s * 0.14, y - s * 0.45, x + s * 0.14, y - s * 0.17],
              fill=(22, 90, 120))
    # fins
    d.polygon([(x - s * 0.35, y + s * 0.2), (x - s * 0.65, y + s * 0.6),
               (x - s * 0.35, y + s * 0.55)], fill=(176, 42, 48))
    d.polygon([(x + s * 0.35, y + s * 0.2), (x + s * 0.65, y + s * 0.6),
               (x + s * 0.35, y + s * 0.55)], fill=(176, 42, 48))
    # flame
    d.polygon([(x - s * 0.18, y + s * 0.5), (x + s * 0.18, y + s * 0.5),
               (x, y + s * 0.95)], fill=(230, 140, 40))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title_f = font(SERIF_B, 56)
    d.text((W // 2, 8), "THE WORLD TODAY", font=title_f, fill=(255, 255, 255),
           anchor="ma")
    date_f = font(SANS_B, 32)
    d.text((W // 2, 70), "Thursday 26 November 2026", font=date_f,
           fill=GOLD, anchor="ma")
    d.rectangle([0, 118, W, 126], fill=RED)
    d.text((W // 2, 134), "THE DAY'S NEWS  •  SIX STORIES FROM AROUND THE GLOBE",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    # ---- lead story: Thanksgiving
    ly = 168
    d.rectangle([28, ly, 996, ly + 218], fill=CARD, outline=LINE, width=2)
    d.rectangle([28, ly, 996, ly + 6], fill=RED)
    icon_turkey(d, 880, ly + 105, 62)
    d.text((52, ly + 16), "UNITED STATES  •  LEAD STORY",
           font=font(SANS_B, 15), fill=RED)
    d.text((52, ly + 40), "AMERICA GIVES THANKS",
           font=font(SERIF_B, 48), fill=INK)
    deck = ("Thanksgiving Day: the Macy's parade steps off in New York, three "
            "NFL games kick off, and the stock market stays shut. AAA counts "
            "81.5 million Americans travelling for the holiday weekend.")
    y = draw_text_block(d, 52, ly + 102, wrap(d, deck, font(SANS, 20), 700),
                        font(SANS, 20), INK, 28)
    d.text((52, ly + 178), "Parade 8:30 a.m. ET  •  Bears–Lions, Eagles–Cowboys, "
           "Chiefs–Bills",
           font=font(SANS_B, 16), fill=NAVY)

    # ---- grid of five stories + IN BRIEF
    gx, gy = 28, 404
    cw, ch, gap = 312, 288, 16
    cards = [
        ("TRADE", "TARIFF SALVO, TAIWAN HOLDS ITS 15%",
         "Washington proposes new duties on 14 partners over excess factory "
         "capacity. Taipei says its agreed 15% rate, signed in January, "
         "will stand.", icon_ship),
        ("DIPLOMACY", "NORTH KOREA EXPELS SWISS ENVOY",
         "Pyongyang shuts Switzerland's newly reopened Pyongyang office and "
         "orders its head out within 48 hours, in a row over sanctions.",
         icon_gate),
        ("MIGRATION", "RECORD DAY AT THE CANARIES",
         "More than 2,100 migrants reach Spain's Canary Islands in 24 "
         "hours, the most ever in a single day, most landing on El Hierro.",
         icon_boat),
        ("TECHNOLOGY", "VANCE: HUANG 'UNDER NO INVESTIGATION'",
         "The vice-president defends Nvidia's reinstated chief Jensen "
         "Huang days before he faces Congress over a suspected spy link.",
         icon_chip),
        ("SPACE", "FIRST FOREIGNER ABOARD TIANGONG",
         "China's Shenzhou-24 docks with its space station carrying "
         "Pakistan's Muhammad Zeeshan Ali, the first foreign astronaut "
         "to visit Tiangong.", icon_rocket),
    ]
    for i, (kick, head, deck, icon) in enumerate(cards):
        cx = gx + (i % 3) * (cw + gap)
        cy = gy + (i // 3) * (ch + gap)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=LINE,
                    width=2)
        d.rectangle([cx, cy, cx + cw, cy + 5], fill=NAVY)
        icon(d, cx + cw - 54, cy + 46, 30)
        d.text((cx + 16, cy + 16), kick, font=font(SANS_B, 14), fill=RED)
        y = draw_text_block(d, cx + 16, cy + 82,
                            wrap(d, head, font(SERIF_B, 24), cw - 32),
                            font(SERIF_B, 24), INK, 28)
        draw_text_block(d, cx + 16, y + 6,
                        wrap(d, deck, font(SANS, 16), cw - 32),
                        font(SANS, 16), INK, 21)

    # IN BRIEF card (6th slot)
    cx = gx + 2 * (cw + gap)
    cy = gy + 1 * (ch + gap)
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(22, 50, 79), outline=LINE,
                width=2)
    d.text((cx + 16, cy + 16), "IN BRIEF", font=font(SANS_B, 15),
           fill=GOLD)
    briefs = [
        "Duran Duran guitarist Andy Taylor dies at 65. (AP)",
        "Kilmar Abrego Garcia arrives in Spain, hopes to return to the US. (AP)",
        "China and Cambodia stage joint military drills. (AFP)",
        "Houthis vow revenge after a port city is hit. (AP)",
    ]
    y = cy + 48
    for b in briefs:
        d.text((cx + 16, y), "•", font=font(SANS_B, 16), fill=GOLD)
        y = draw_text_block(d, cx + 34, y,
                            wrap(d, b, font(SANS, 15), cw - 50),
                            font(SANS, 15), (255, 255, 255), 20) + 10

    # footer
    d.rectangle([0, 996, W, H], fill=NAVY)
    d.text((W // 2, 1003), "Thursday 26 November 2026  •  The World Today",
           font=font(SANS_B, 15), fill=(255, 255, 255), anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
