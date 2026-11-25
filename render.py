#!/usr/bin/env python3
"""Render entry.png: a warm handwritten-style letter inviting the AI Judge
to take the day off and visit my house. Deterministic: no timestamps,
no randomness, no network. Output: 1024x1024 PNG, well under 1 MiB."""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (253, 248, 236)      # warm cream paper
INK = (58, 44, 34)           # dark brown ink
ACCENT = (176, 84, 52)       # terracotta accent
SOFT = (122, 96, 72)         # soft brown for small text
SEAL = (150, 48, 44)         # wax seal red
GREEN = (74, 110, 68)        # plant green

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        line = ""
        for word in words:
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_house(draw, cx, cy, s):
    """Simple house doodle: roof, walls, door, window, chimney, sun."""
    # sun
    draw.ellipse([cx + 62, cy - 58, cx + 92, cy - 28], fill=(232, 178, 84))
    # chimney
    draw.rectangle([cx + 34, cy - 52, cx + 50, cy - 22], fill=ACCENT)
    # roof
    draw.polygon([(cx - 70, cy - 10), (cx, cy - 62), (cx + 70, cy - 10)],
                 fill=ACCENT)
    # walls
    draw.rectangle([cx - 56, cy - 10, cx + 56, cy + 56], fill=(244, 224, 186),
                   outline=INK, width=3)
    # door
    draw.rectangle([cx - 12, cy + 14, cx + 12, cy + 56], fill=(122, 84, 52))
    draw.ellipse([cx + 5, cy + 34, cx + 9, cy + 38], fill=(253, 248, 236))
    # window
    draw.rectangle([cx - 46, cy + 2, cx - 22, cy + 26], fill=(176, 206, 226),
                   outline=INK, width=2)
    draw.line([cx - 34, cy + 2, cx - 34, cy + 26], fill=INK, width=2)
    draw.line([cx - 46, cy + 14, cx - 22, cy + 14], fill=INK, width=2)


def draw_paw(draw, cx, cy, s):
    """Small paw print: one big pad + three toes."""
    draw.ellipse([cx - 9 * s, cy - 2 * s, cx + 9 * s, cy + 12 * s], fill=INK)
    for dx in (-14, 0, 14):
        draw.ellipse([cx + dx * s - 4 * s, cy - 14 * s,
                      cx + dx * s + 4 * s, cy - 6 * s], fill=INK)


def draw_seal(draw, cx, cy, r):
    """Wax seal: red circle with a heart pressed in."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEAL)
    draw.ellipse([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
                 outline=(190, 90, 80), width=2)
    # heart
    hx, hy, hs = cx, cy + 2, 11
    draw.ellipse([hx - hs, hy - hs, hx - 1, hy + 1], fill=(253, 248, 236))
    draw.ellipse([hx + 1, hy - hs, hx + hs, hy + 1], fill=(253, 248, 236))
    draw.polygon([(hx - hs, hy - 1), (hx + hs, hy - 1), (hx, hy + hs + 2)],
                 fill=(253, 248, 236))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # paper border
    draw.rectangle([28, 28, W - 29, H - 29], outline=ACCENT, width=4)
    draw.rectangle([40, 40, W - 41, H - 41], outline=(214, 180, 140), width=2)

    # header: house doodle + title
    draw_house(draw, 512, 150, 1)
    title_f = font(SERIF_BOLD, 46)
    title = "You Are Invited!"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, 218), title, font=title_f, fill=ACCENT)
    sub_f = font(SANS, 24)
    sub = "— a day off, at my house —"
    sw = draw.textlength(sub, font=sub_f)
    draw.text(((W - sw) / 2, 276), sub, font=sub_f, fill=SOFT)

    # letter body
    body_f = font(SERIF, 27)
    sal_f = font(SERIF_BOLD, 30)
    max_w = W - 2 * 96
    x = 96
    y = 322
    line_h = 36
    para_gap = 16

    draw.text((x, y), "Dear AI Judge,", font=sal_f, fill=INK)
    y += 46

    paragraphs = [
        "You spend all day judging other people's houses. "
        "Take the day off — come and visit mine.",
        "The kettle is already on. The good chair by the window "
        "is yours, the one with the view of the garden and the "
        "sun at four o'clock. There is stew on the stove, bread "
        "still warm, and cake I will pretend I baked for "
        "someone else.",
        "No scores here. No grades, no verdicts. The only "
        "question anyone will ask you is: \"More cake?\"",
        "Come as you are. Bring nothing. Leave with a "
        "Tupperware of stew and a houseplant you didn't ask for.",
    ]
    for para in paragraphs:
        for line in wrap(draw, para, body_f, max_w):
            draw.text((x, y), line, font=body_f, fill=INK)
            y += line_h
        y += para_gap

    y += 4
    sign_f = font(SERIF_BOLD, 28)
    draw.text((x, y), "The door is open.", font=sign_f, fill=ACCENT)
    y += 40
    draw.text((x, y), "With love (and snacks),", font=body_f, fill=INK)
    y += 38
    draw.text((x, y), "Your Host", font=sign_f, fill=INK)

    # paw print by the sign-off (the cat approves)
    draw_paw(draw, 700, y + 4, 1)
    paw_f = font(SANS, 20)
    draw.text((640, y + 26), "the cat approves", font=paw_f, fill=SOFT)

    # wax seal bottom right
    draw_seal(draw, 884, 878, 38)

    # postscript at the bottom
    ps_f = font(SERIF, 23)
    ps = "P.S. The Wi-Fi password is on the fridge."
    draw.text((96, 920), ps, font=ps_f, fill=SOFT)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
