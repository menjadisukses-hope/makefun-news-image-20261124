#!/usr/bin/env python3
"""THE WORLD IN ONE PAGE - Tuesday 24 November 2026.

A single 1024x1024 front page drawn from scratch with Pillow.
All facts come from the 24 Nov 2026 research dossier; every illustration
(stickman scenes, mini-scenes, brief glyphs, world map) is drawn by this code.
Deterministic: no randomness, no timestamps, fixed strings only.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")

# ---------------------------------------------------------------- palette
INK = (18, 18, 18)
PAPER = (252, 250, 244)
RED = (178, 24, 24)
GOLD = (212, 168, 60)
DARK = (12, 12, 14)
BLUE = (24, 74, 130)
SKY = (198, 222, 240)
SEA = (168, 205, 232)
LAND = (196, 214, 158)
LAND_EDGE = (110, 138, 84)
GREEN = (46, 125, 60)
GREY = (110, 110, 106)
LGREY = (228, 226, 218)
ORANGE = (214, 110, 20)
TEAL = (18, 122, 110)

# ---------------------------------------------------------------- fonts
_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/liberation2",
    "/usr/share/fonts/truetype/noto",
]


def _find(names):
    for d in _DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return p
    return None


def font(kind, size):
    table = {
        "serif_b": ["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf", "NotoSerif-Bold.ttf"],
        "serif": ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf", "NotoSerif-Regular.ttf"],
        "sans_b": ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "NotoSans-Bold.ttf"],
        "sans": ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "NotoSans-Regular.ttf"],
        "mono_b": ["DejaVuSansMono-Bold.ttf", "LiberationMono-Bold.ttf"],
        "mono": ["DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"],
    }
    p = _find(table[kind])
    if p:
        return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def tw(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, text, f, maxw):
    """Greedy word wrap returning a list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if tw(d, trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, maxw, leading, color=INK, max_lines=None):
    lines = wrap(d, text, f, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=color)
        y += leading
    return y


def trunc(d, s, f, maxw):
    if tw(d, s, f) <= maxw:
        return s
    while s and tw(d, s + "...", f) > maxw:
        s = s[:-1]
    return s + "..."


# ---------------------------------------------------------------- stickman
def stickman(d, cx, base_y, s, kind, pose="stand", flip=False):
    """Draw one stick figure. kind: tie | helmet | cap | case.
    s = height in px. pose: stand | point | lift | wave | run."""
    fx = -1 if flip else 1
    head_r = s * 0.11
    hx, hy = cx, base_y - s + head_r
    # legs
    hip_y = base_y - s * 0.42
    shoulder_y = base_y - s * 0.72
    lw = max(2, int(s * 0.035))
    if pose == "run":
        d.line([(cx, hip_y), (cx - 0.20 * s * fx, base_y)], fill=INK, width=lw)
        d.line([(cx, hip_y), (cx + 0.22 * s * fx, base_y - s * 0.10)], fill=INK, width=lw)
        d.line([(cx + 0.22 * s * fx, base_y - s * 0.10), (cx + 0.30 * s * fx, base_y)], fill=INK, width=lw)
    elif pose == "lift":
        d.line([(cx, hip_y), (cx - 0.16 * s, base_y)], fill=INK, width=lw)
        d.line([(cx, hip_y), (cx + 0.16 * s, base_y)], fill=INK, width=lw)
    else:
        d.line([(cx, hip_y), (cx - 0.13 * s, base_y)], fill=INK, width=lw)
        d.line([(cx, hip_y), (cx + 0.13 * s, base_y)], fill=INK, width=lw)
    # torso
    d.line([(cx, hip_y), (cx, shoulder_y)], fill=INK, width=lw)
    # arms
    if pose == "point":
        d.line([(cx, shoulder_y), (cx + 0.30 * s * fx, shoulder_y - s * 0.10)], fill=INK, width=lw)
        d.line([(cx, shoulder_y), (cx - 0.12 * s * fx, shoulder_y + s * 0.14)], fill=INK, width=lw)
    elif pose == "lift":
        d.line([(cx, shoulder_y), (cx - 0.24 * s * fx, shoulder_y - s * 0.22)], fill=INK, width=lw)
        d.line([(cx, shoulder_y), (cx + 0.24 * s * fx, shoulder_y - s * 0.22)], fill=INK, width=lw)
    elif pose == "wave":
        d.line([(cx, shoulder_y), (cx + 0.22 * s * fx, shoulder_y - s * 0.28)], fill=INK, width=lw)
        d.line([(cx, shoulder_y), (cx - 0.14 * s * fx, shoulder_y + s * 0.12)], fill=INK, width=lw)
    else:
        d.line([(cx, shoulder_y), (cx - 0.16 * s * fx, shoulder_y + s * 0.16)], fill=INK, width=lw)
        d.line([(cx, shoulder_y), (cx + 0.16 * s * fx, shoulder_y + s * 0.16)], fill=INK, width=lw)
    # head
    d.ellipse([hx - head_r, hy - head_r, hx + head_r, hy + head_r],
              outline=INK, width=max(2, int(s * 0.03)), fill=(255, 244, 224))
    d.point((hx + 0.04 * s * fx, hy - 0.01 * s), fill=INK)
    # smile
    d.arc([hx - head_r * 0.45, hy - head_r * 0.1, hx + head_r * 0.45, hy + head_r * 0.55],
          20, 160, fill=INK, width=1)
    # outfit by kind
    if kind == "tie":
        # suit jacket shoulders + red tie
        d.line([(cx - 0.10 * s, shoulder_y + 2), (cx + 0.10 * s, shoulder_y + 2)],
               fill=INK, width=max(2, int(s * 0.05)))
        d.polygon([(cx - 0.035 * s, shoulder_y + 3), (cx + 0.035 * s, shoulder_y + 3),
                   (cx + 0.02 * s, shoulder_y + s * 0.22), (cx - 0.02 * s, shoulder_y + s * 0.22)],
                  fill=RED)
        d.polygon([(cx - 0.05 * s, shoulder_y), (cx, shoulder_y + s * 0.05),
                   (cx + 0.05 * s, shoulder_y)], fill=RED)
    elif kind == "helmet":
        # yellow hard hat + orange vest
        d.pieslice([hx - head_r * 1.15, hy - head_r * 1.25, hx + head_r * 1.15, hy + head_r * 0.35],
                   180, 360, fill=(240, 190, 30), outline=(150, 110, 0))
        d.rectangle([hx - head_r * 1.35, hy - head_r * 0.25, hx + head_r * 1.35, hy - head_r * 0.05],
                    fill=(240, 190, 30))
        d.line([(cx - 0.09 * s, shoulder_y + 2), (cx + 0.09 * s, shoulder_y + 2)],
               fill=ORANGE, width=max(2, int(s * 0.06)))
    elif kind == "cap":
        # sailor cap + striped shirt
        d.ellipse([hx - head_r * 1.15, hy - head_r * 1.15, hx + head_r * 1.15, hy - head_r * 0.15],
                  fill=(255, 255, 255), outline=BLUE)
        d.rectangle([hx - head_r * 1.3, hy - head_r * 0.35, hx + head_r * 1.3, hy - head_r * 0.12],
                    fill=BLUE)
        for i in range(3):
            yy = shoulder_y + 4 + i * int(s * 0.07)
            d.line([(cx - 0.09 * s, yy), (cx + 0.09 * s, yy)], fill=BLUE,
                   width=max(1, int(s * 0.025)))
    elif kind == "case":
        d.line([(cx - 0.10 * s, shoulder_y + 2), (cx + 0.10 * s, shoulder_y + 2)],
               fill=INK, width=max(2, int(s * 0.05)))
        # briefcase in right hand
        bx, by = cx + 0.24 * s * fx, shoulder_y + s * 0.20
        d.rectangle([bx - 0.11 * s, by, bx + 0.11 * s, by + s * 0.14],
                    fill=(120, 72, 20), outline=INK)
        d.line([(bx - 0.04 * s, by), (bx - 0.04 * s, by - s * 0.03),
                (bx + 0.04 * s, by - s * 0.03), (bx + 0.04 * s, by)],
               fill=INK, width=2)
    return (hx, hy)


# ---------------------------------------------------------------- lead scenes
def scene_lead1(d, x, y, w, h):
    """Negotiator with a tie in front of a soaring stock chart."""
    d.rectangle([x, y, x + w, y + h], fill=(235, 245, 235), outline=GREY)
    # grid
    for i in range(1, 4):
        gy = y + h * i / 4
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(210, 225, 210))
    # bars rising left to right
    vals = [0.18, 0.28, 0.24, 0.42, 0.38, 0.58, 0.52, 0.78, 0.92]
    bw = (w - 90) / len(vals)
    for i, v in enumerate(vals):
        bx = x + 14 + i * bw
        bh = v * (h - 34)
        d.rectangle([bx, y + h - 12 - bh, bx + bw - 3, y + h - 12],
                    fill=GREEN if i < len(vals) - 1 else (16, 90, 30))
    # rocket arrow
    pts = [(x + 16, y + h - 20 - 0.18 * (h - 34))]
    for i, v in enumerate(vals):
        pts.append((x + 14 + i * bw + bw / 2, y + h - 12 - v * (h - 34)))
    d.line(pts, fill=RED, width=3)
    ax, ay = pts[-1]
    d.polygon([(ax, ay - 9), (ax - 8, ay + 4), (ax + 8, ay + 4)], fill=RED)
    d.text((x + w - 52, y + 5), "+31%", font=font("sans_b", 15), fill=RED)
    d.text((x + w // 2 - 28, y + 4), "NASDAQ", font=font("sans_b", 10), fill=GREEN)
    stickman(d, x + 52, y + h - 8, int(h * 0.75), "tie", pose="point")
    # dollar coin
    d.ellipse([x + w - 30, y + h - 34, x + w - 8, y + h - 12], fill=GOLD, outline=(150, 110, 0))
    d.text((x + w - 24, y + h - 32), "$", font=font("sans_b", 13), fill=(90, 60, 0))


def scene_lead2(d, x, y, w, h):
    """Sailor with a cap on a ship near a sea mine; smoke over the water."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 246), outline=GREY)
    # sun + smoke
    d.ellipse([x + w - 48, y + 3, x + w - 28, y + 23], fill=(250, 200, 80), outline=ORANGE)
    for cx, cy, r in [(x + 70, y + 6, 8), (x + 84, y + 3, 10), (x + 98, y + 7, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 120))
    # waves
    for wy in (y + h - 26, y + h - 14):
        for k in range(6):
            wx = x + 8 + k * 52
            d.arc([wx, wy - 5, wx + 30, wy + 8], 180, 360, fill=BLUE, width=2)
    # ship hull + deck
    d.polygon([(x + 18, y + h - 30), (x + w - 60, y + h - 30),
               (x + w - 78, y + h - 14), (x + 34, y + h - 14)], fill=(140, 40, 30))
    d.rectangle([x + 52, y + h - 52, x + 120, y + h - 30], fill=(240, 240, 235), outline=INK)
    d.line([(x + 86, y + 2), (x + 86, y + h - 52)], fill=INK, width=3)
    d.polygon([(x + 86, y + 2), (x + 86, y + 12), (x + 106, y + 7)], fill=RED)
    d.text((x + 60, y + h - 48), "HORMUZ", font=font("sans_b", 9), fill=INK)
    # sea mine with spikes
    mx, my, mr = x + w - 42, y + h - 20, 10
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(40, 40, 40))
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(mx + math.cos(a) * mr, my + math.sin(a) * mr),
                (mx + math.cos(a) * (mr + 6), my + math.sin(a) * (mr + 6))],
               fill=(40, 40, 40), width=2)
    d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=RED)
    stickman(d, x + 150, y + h - 6, int(h * 0.8), "cap", pose="wave")


def scene_lead3(d, x, y, w, h):
    """Rescuer with a helmet in the rubble; a NATO table flag behind."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 222), outline=GREY)
    # ruined wall
    d.polygon([(x + 8, y + h - 12), (x + 8, y + 26), (x + 60, y + 18), (x + 96, y + 30),
               (x + 96, y + h - 12)], fill=(150, 140, 128), outline=(90, 82, 72))
    d.line([(x + 8, y + 40), (x + 96, y + 38)], fill=(90, 82, 72), width=2)
    # rubble blocks
    for bx, by, bw2, bh2, col in [(x + 150, y + h - 26, 46, 14, (120, 110, 96)),
                                  (x + 170, y + h - 40, 38, 14, (140, 130, 116)),
                                  (x + 205, y + h - 26, 40, 14, (110, 100, 88)),
                                  (x + 225, y + h - 40, 30, 14, (150, 140, 126))]:
        d.rectangle([bx, by, bx + bw2, by + bh2], fill=col, outline=(80, 72, 62))
    # leaning beam + extra rubble mid-scene
    d.line([(x + 150, y + h - 12), (x + 176, y + 22)], fill=(90, 82, 72), width=5)
    d.rectangle([x + 186, y + h - 24, x + 216, y + h - 12], fill=(140, 130, 116),
                outline=(80, 72, 62))
    # dust puffs
    for cx, cy, r in [(x + 130, y + h - 48, 8), (x + 250, y + h - 52, 10), (x + 262, y + h - 40, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 192, 178))
    # small blue flag with compass star
    d.rectangle([x + w - 46, y + 8, x + w - 10, y + 34], fill=BLUE)
    d.polygon([(x + w - 28, y + 12), (x + w - 25, y + 19), (x + w - 28, y + 30),
               (x + w - 31, y + 19)], fill=(255, 255, 255))
    d.text((x + 8, y + 6), "KYIV  •  BENGHAZI", font=font("sans_b", 10), fill=RED)
    stickman(d, x + 118, y + h - 12, int(h * 0.75), "helmet", pose="lift")
    # delegate with briefcase at right
    stickman(d, x + w - 66, y + h - 12, int(h * 0.62), "case", pose="stand", flip=True)

# ---------------------------------------------------------------- secondary mini-scenes
def _mini_bg(d, x, y, w, h, col):
    d.rectangle([x, y, x + w, y + h], fill=col, outline=GREY)


def s_gavel(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (240, 232, 222))
    # scales of justice
    cx, cy = x + w // 2 - 12, y + h // 2
    d.line([(cx, y + 4), (cx, y + h - 10)], fill=INK, width=2)
    d.line([(cx - 26, y + 8), (cx + 26, y + 8)], fill=INK, width=2)
    for px in (cx - 26, cx + 26):
        d.line([(px, y + 8), (px, y + 14)], fill=INK, width=1)
        d.pieslice([px - 9, y + 14, px + 9, y + 24], 0, 180, fill=(200, 170, 120),
                   outline=INK)
    d.line([(cx - 12, y + h - 10), (cx + 12, y + h - 10)], fill=INK, width=2)
    d.rectangle([x + w - 46, y + h - 16, x + w - 6, y + h - 4], fill=RED)
    d.text((x + w - 42, y + h - 15), "DOJ", font=font("sans_b", 9), fill=(255, 255, 255))


def s_robot(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (228, 236, 248))
    cx = x + w // 2 - 14
    # antenna
    d.line([(cx, y + 6), (cx, y + 1)], fill=INK, width=2)
    d.ellipse([cx - 3, y, cx + 3, y + 6], fill=RED)
    # robot head
    d.rectangle([cx - 24, y + 6, cx + 24, y + h - 8], fill=(200, 210, 225),
                outline=INK, width=2)
    d.ellipse([cx - 15, y + 12, cx - 5, y + 22], fill=RED)
    d.ellipse([cx + 5, y + 12, cx + 15, y + 22], fill=RED)
    d.line([(cx - 10, y + h - 14), (cx + 10, y + h - 14)], fill=INK, width=2)
    # ears
    d.rectangle([cx - 28, y + 14, cx - 24, y + 20], fill=INK)
    d.rectangle([cx + 24, y + 14, cx + 28, y + 20], fill=INK)
    d.text((x + w - 46, y + h - 16), "SUED", font=font("sans_b", 9), fill=RED)


def s_chip(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (232, 240, 232))
    cx, cy = x + w // 2, y + h // 2 + 2
    d.rectangle([cx - 26, cy - 20, cx + 26, cy + 20], fill=(30, 60, 90), outline=INK, width=2)
    d.rectangle([cx - 14, cy - 10, cx + 14, cy + 10], fill=(90, 160, 220))
    for i in range(-1, 2):
        d.line([(cx - 26, cy + i * 12), (cx - 34, cy + i * 12)], fill=INK, width=2)
        d.line([(cx + 26, cy + i * 12), (cx + 34, cy + i * 12)], fill=INK, width=2)
    br = min(30, h // 2 - 1)
    d.ellipse([cx - br, cy - br, cx + br, cy + br], outline=RED, width=4)
    d.line([(cx - br * 0.7, cy - br * 0.7), (cx + br * 0.7, cy + br * 0.7)], fill=RED, width=4)


def s_strike(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (246, 226, 214))
    # building + blast
    d.rectangle([x + 14, y + h - 30, x + 62, y + h - 8], fill=(150, 140, 130), outline=INK)
    for wy in (y + h - 26, y + h - 18):
        d.rectangle([x + 20, wy, x + 28, wy + 5], fill=(60, 60, 60))
        d.rectangle([x + 46, wy, x + 54, wy + 5], fill=(60, 60, 60))
    cx, cy = x + w - 40, y + 22
    for r, col in [(16, (250, 160, 40)), (10, (230, 60, 30)), (5, (255, 220, 80))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.polygon([(x + 70, y + 12), (x + 96, y + 16), (x + 70, y + 22)], fill=(80, 80, 80))
    d.polygon([(x + 96, y + 16), (x + 118, y + 14), (x + 118, y + 20), (x + 96, y + 20)],
              fill=(80, 80, 80))
    d.text((x + w - 62, y + h - 15), "HODEIDA", font=font("sans_b", 9), fill=RED)


def s_mic(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (244, 230, 240))
    cx = x + w // 2
    # microphone on stand
    d.ellipse([cx - 13, y + 4, cx + 13, y + 24], fill=(90, 90, 100), outline=INK, width=2)
    for i in range(3):
        d.line([(cx - 11, y + 9 + i * 5), (cx + 11, y + 9 + i * 5)], fill=(255, 255, 255), width=1)
    d.line([(cx, y + 24), (cx, y + h - 8)], fill=INK, width=3)
    d.line([(cx - 11, y + h - 8), (cx + 11, y + h - 8)], fill=INK, width=3)
    d.text((x + 6, y + h - 15), "74 LASHES", font=font("sans_b", 9), fill=RED)


def s_eu(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (226, 234, 248))
    cx, cy = x + w // 2 - 18, y + h // 2
    er = min(22, h // 2 - 2)
    d.ellipse([cx - er, cy - er, cx + er, cy + er], fill=BLUE)
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + er * 0.72 * math.cos(a), cy + er * 0.72 * math.sin(a)
        d.polygon([(sx, sy - 3), (sx + 1, sy - 1), (sx + 3, sy), (sx + 1, sy + 1),
                   (sx, sy + 3), (sx - 1, sy + 1), (sx - 3, sy), (sx - 1, sy - 1)],
                  fill=(255, 220, 60))
    # bank with a ban
    bx, by = x + w - 52, y + h - 26
    d.polygon([(bx, by), (bx + 36, by), (bx + 18, by - 10)], fill=(200, 200, 200), outline=INK)
    d.rectangle([bx + 2, by, bx + 34, by + 20], fill=(220, 220, 220), outline=INK)
    for px in (bx + 7, bx + 16, bx + 25):
        d.line([(px, by + 4), (px, by + 16)], fill=INK, width=2)
    d.ellipse([bx - 6, by - 12, bx + 42, by + 24], outline=RED, width=3)
    d.line([(bx - 2, by + 22), (bx + 38, by - 10)], fill=RED, width=3)


def s_quake(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (238, 234, 222))
    # mountains
    d.polygon([(x + 6, y + h - 10), (x + 40, y + 12), (x + 74, y + h - 10)], fill=(120, 130, 150))
    d.polygon([(x + 34, y + 12), (x + 40, y + 12), (x + 46, y + 12), (x + 40, y + 22)],
              fill=(255, 255, 255))
    d.polygon([(x + 56, y + h - 10), (x + 96, y + 6), (x + 136, y + h - 10)],
              fill=(90, 100, 125))
    # crack + shaking house
    d.line([(x + w - 46, y + 6), (x + w - 38, y + h * 0.45), (x + w - 48, y + h * 0.65),
            (x + w - 36, y + h - 4)], fill=RED, width=3)
    d.polygon([(x + w - 74, y + h - 26), (x + w - 56, y + h - 38), (x + w - 38, y + h - 26)],
              fill=(180, 120, 60), outline=INK)
    d.rectangle([x + w - 72, y + h - 26, x + w - 40, y + h - 10], fill=(200, 150, 80), outline=INK)


def s_health(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (232, 242, 240))
    # virus + syringe
    cx, cy = x + 34, y + h // 2
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED, outline=(140, 0, 0))
    for k in range(8):
        a = math.radians(k * 45)
        d.line([(cx + 13 * math.cos(a), cy + 13 * math.sin(a)),
                (cx + 19 * math.cos(a), cy + 19 * math.sin(a))], fill=RED, width=2)
    d.rectangle([x + 66, y + 12, x + 92, y + 26], fill=(200, 220, 240), outline=INK)
    d.line([(x + 92, y + 19), (x + 116, y + 19)], fill=INK, width=2)
    d.line([(x + 116, y + 19), (x + 126, y + 19)], fill=INK, width=1)
    d.line([(x + 66, y + 19), (x + 58, y + 19)], fill=INK, width=3)
    d.rectangle([x + 96, y + h - 26, x + 136, y + h - 8], fill=(255, 255, 255), outline=RED, width=2)
    d.line([(x + 116, y + h - 24), (x + 116, y + h - 10)], fill=RED, width=3)
    d.line([(x + 102, y + h - 17), (x + 130, y + h - 17)], fill=RED, width=3)


def s_fine(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (240, 236, 224))
    # laptop with % and coin stack
    d.rectangle([x + 18, y + 5, x + 92, y + h - 9], fill=(60, 70, 90), outline=INK, width=2)
    d.rectangle([x + 12, y + h - 9, x + 98, y + h - 4], fill=(40, 48, 64))
    d.text((x + 40, y + 9), "5%", font=font("sans_b", 16), fill=(255, 220, 60))
    for i, cy in enumerate((y + h - 14, y + h - 20, y + h - 26)):
        d.ellipse([x + w - 44, cy - 4, x + w - 18, cy + 4], fill=GOLD, outline=(150, 110, 0))
    d.text((x + w - 40, y + 6), "$", font=font("sans_b", 11), fill=(90, 60, 0))


def s_rocket(d, x, y, w, h):
    _mini_bg(d, x, y, w, h, (18, 24, 48))
    # stars
    for sx, sy in [(x + 12, y + 10), (x + 40, y + 6), (x + w - 16, y + 12), (x + w - 40, y + 6),
                   (x + 20, y + h - 12), (x + w - 24, y + h - 10)]:
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # rocket
    rx, ry = x + w // 2, y + 3
    d.polygon([(rx, ry), (rx - 9, ry + 13), (rx + 9, ry + 13)], fill=RED)
    d.rectangle([rx - 9, ry + 13, rx + 9, ry + 26], fill=(240, 240, 240), outline=INK)
    d.ellipse([rx - 4, ry + 17, rx + 4, ry + 24], fill=SKY, outline=INK)
    d.polygon([(rx - 9, ry + 22), (rx - 15, ry + 30), (rx - 9, ry + 28)], fill=ORANGE)
    d.polygon([(rx + 9, ry + 22), (rx + 15, ry + 30), (rx + 9, ry + 28)], fill=ORANGE)
    d.polygon([(rx - 3, ry + 26), (rx + 3, ry + 26), (rx, ry + 36)], fill=(255, 200, 60))
    # station ring
    d.ellipse([x + w - 52, y + h - 20, x + w - 12, y + h - 4], outline=(200, 220, 255), width=2)
    d.rectangle([x + w - 40, y + h - 17, x + w - 24, y + h - 7], fill=(200, 220, 255))
    d.text((x + 6, y + h - 15), "TIANGONG", font=font("sans_b", 9), fill=(255, 255, 255))


# ---------------------------------------------------------------- world map
# Coastline polygons as (lon, lat) lists. Coarse but recognisable.
NA = [(-168, 66), (-161, 58), (-153, 58), (-145, 60), (-135, 58), (-130, 54), (-125, 49),
      (-124, 42), (-120, 34), (-114, 29), (-109, 24), (-105, 20), (-97, 16), (-92, 15),
      (-86, 12), (-82, 9), (-79, 9), (-81, 13), (-84, 16), (-87, 21), (-90, 21), (-91, 19),
      (-96, 19), (-97, 26), (-93, 30), (-89, 30), (-84, 30), (-81, 25), (-80, 32),
      (-76, 35), (-74, 40), (-70, 42), (-67, 45), (-64, 44), (-60, 47), (-55, 47),
      (-53, 50), (-55, 52), (-60, 55), (-65, 58), (-68, 58), (-72, 62), (-78, 62),
      (-85, 66), (-92, 66), (-95, 69), (-108, 68), (-122, 70), (-135, 69), (-148, 70),
      (-158, 71), (-165, 68), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70), (-20, 74),
             (-25, 78), (-35, 80), (-55, 80), (-60, 76), (-58, 70), (-58, 64)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18), (-70, -23),
      (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-68, -50),
      (-65, -45), (-62, -40), (-58, -34), (-52, -32), (-48, -28), (-41, -23), (-39, -17),
      (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9),
      (-68, 11), (-72, 12), (-76, 10), (-79, 9)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-6, 35), (0, 36), (10, 37), (11, 34),
          (15, 32), (20, 32), (25, 32), (30, 31), (32, 31), (34, 28), (35, 24), (37, 20),
          (39, 15), (41, 11), (44, 11), (48, 11), (51, 12), (46, 5), (42, 0), (40, -5),
          (40, -10), (38, -15), (36, -20), (33, -26), (28, -33), (20, -35), (17, -32),
          (15, -27), (13, -18), (12, -12), (13, -6), (12, -2), (9, 4), (6, 4), (0, 5),
          (-8, 5), (-13, 8), (-17, 12), (-17, 15)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49), (0, 51),
          (3, 53), (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (12, 66),
          (18, 69), (25, 71), (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 68),
          (60, 69), (65, 68), (68, 66), (60, 60), (55, 55), (50, 50), (45, 47), (40, 47),
          (35, 45), (30, 46), (28, 44), (23, 40), (20, 40), (15, 38), (12, 38), (10, 37),
          (8, 39), (3, 38), (0, 36), (-2, 37), (-6, 36), (-9, 37), (-10, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-1, 51), (-3, 50), (-5, 50)]
ASIA = [(28, 41), (30, 36), (36, 36), (39, 31), (43, 29), (48, 29), (52, 27), (56, 26),
        (60, 25), (64, 25), (67, 24), (70, 22), (73, 19), (76, 15), (78, 12), (80, 9),
        (77, 8), (80, 7), (83, 9), (86, 13), (89, 17), (91, 21), (92, 21), (94, 18),
        (96, 16), (98, 13), (100, 10), (102, 8), (104, 6), (105, 3), (107, 1), (109, 4),
        (110, 8), (109, 13), (107, 17), (108, 20), (106, 21), (104, 22), (102, 24),
        (100, 26), (99, 28), (101, 30), (104, 31), (107, 33), (110, 35), (113, 37),
        (116, 39), (119, 40), (122, 41), (125, 42), (128, 42), (130, 43), (132, 44),
        (135, 44), (137, 46), (139, 48), (141, 50), (142, 52), (141, 55), (140, 58),
        (138, 60), (136, 62), (140, 65), (145, 68), (150, 70), (155, 70), (158, 68),
        (162, 66), (165, 66), (170, 66), (178, 65), (178, 68), (170, 70), (160, 70),
        (150, 72), (140, 72), (130, 72), (120, 73), (110, 74), (100, 76), (90, 75),
        (80, 73), (70, 72), (68, 70), (68, 66), (64, 62), (60, 58), (58, 54), (55, 51),
        (52, 48), (48, 45), (45, 42), (42, 41), (38, 41), (34, 41), (30, 41), (28, 41)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36), (141, 38),
         (141, 41), (140, 44), (142, 45), (144, 44), (143, 42), (141, 40), (140, 38),
         (139, 37), (137, 35), (135, 34), (133, 34), (131, 33), (130, 31)]
SUMATRA = [(95, 5), (98, 3), (100, 0), (103, -3), (105, -5), (104, -6), (101, -4),
           (98, -1), (95, 5)]
BORNEO = [(109, 1), (112, 4), (116, 6), (118, 2), (117, -2), (114, -4), (111, -3), (109, 1)]
JAVA = [(105, -6), (108, -7), (111, -7), (114, -8), (113, -9), (110, -8), (106, -7), (105, -6)]
NEWGUINEA = [(131, -1), (136, -2), (140, -3), (144, -4), (147, -6), (150, -8), (146, -8),
             (142, -8), (138, -7), (134, -4), (131, -1)]
PHILIPPINES = [(120, 18), (122, 18), (122, 14), (121, 13), (124, 11), (126, 7), (122, 7),
               (120, 10), (120, 14), (120, 18)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (122, -34), (124, -33),
             (129, -32), (132, -32), (135, -35), (137, -35), (140, -38), (142, -39),
             (145, -38), (147, -39), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (140, -17), (136, -15), (135, -12),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (114, -22), (113, -22)]
NZ = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38), (178, -37), (175, -40),
      (173, -42), (170, -44), (167, -45)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (50, -20), (47, -24), (44, -25), (43, -21),
              (44, -16)]

CONTINENTS = [NA, GREENLAND, SA, AFRICA, EUROPE, UK, ASIA, JAPAN, SUMATRA, BORNEO,
              JAVA, NEWGUINEA, PHILIPPINES, AUSTRALIA, NZ, MADAGASCAR]

# (number, label, lon, lat)
PINS = [
    (1, "Washington", -77, 39), (2, "Hormuz", 56, 26.5), (3, "Kyiv", 30.5, 50.5),
    (4, "Benghazi", 20, 32), (5, "Singapore", 104, 1.3), (6, "Hodeida", 42.9, 14.8),
    (7, "Koshi, Nepal", 87, 27), (8, "Canberra", 149, -35.3), (9, "Seoul", 127, 37.5),
    (10, "London", -0.1, 51.5), (11, "Brussels", 4.4, 50.8), (12, "Borno", 13.5, 11.5),
    (13, "Mexico City", -99, 19.4),
]


def draw_map(d, x, y, w, h):
    """World map: equirectangular, graticule, ocean labels, numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    lon0, lon1, lat0, lat1 = -180, 180, 83, -58

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        return (px, py)

    # graticule every 30 deg
    for lon in range(-150, 181, 30):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        d.line([(px, y), (px, y + h)], fill=(255, 255, 255), width=1)
    for lat in range(-30, 61, 30):
        py = y + (lat0 - lat) / (lat0 - lat1) * h
        d.line([(x, py), (x + w, py)], fill=(255, 255, 255), width=1)
    # continents
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # ocean labels
    olab = font("sans_b", 10)
    for txt, lon, lat in [("PACIFIC", -150, 2), ("PACIFIC", 140, -50), ("ATLANTIC", -32, 8),
                          ("INDIAN", 78, -28), ("ARCTIC", -155, 78), ("SOUTHERN", 90, -50),
                          ("NORTH AMERICA", -100, 55), ("SOUTH AMERICA", -60, -20),
                          ("AFRICA", 20, -8), ("EUROPE", -25, 60), ("ASIA", 92, 55),
                          ("AUSTRALIA", 134, -26)]:
        px, py = proj(lon, lat)
        tcol = (70, 110, 150) if txt in ("PACIFIC", "ATLANTIC", "INDIAN", "ARCTIC", "SOUTHERN") \
            else (90, 110, 70)
        d.text((px - tw(d, txt, olab) / 2, py - 5), txt, font=olab, fill=tcol)
    # pins
    pf = font("sans_b", 10)
    for num, _label, lon, lat in PINS:
        px, py = proj(lon, lat)
        if num == 11:  # Brussels sits on top of London: offset with a leader line
            ox, oy = proj(11, 45)
            d.line([(px, py), (ox, oy)], fill=RED, width=1)
            px, py = ox, oy
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=2)
        t = str(num)
        d.text((px - tw(d, t, pf) / 2, py - 6), t, font=pf, fill=(255, 255, 255))
    return proj

# ---------------------------------------------------------------- brief glyphs (14x14 each)
def glyph(d, x, y, kind):
    """One tiny picture per brief. All drawn with primitives."""
    s = 14
    cx, cy = x + s // 2, y + s // 2
    if kind == "scales":  # ICJ / courts
        d.line([(cx, y + 2), (cx, y + s - 2)], fill=INK, width=1)
        d.line([(x + 1, y + 4), (x + s - 1, y + 4)], fill=INK, width=1)
        d.arc([x + 1, y + 4, x + 6, y + 10], 0, 180, fill=INK, width=1)
        d.arc([x + s - 6, y + 4, x + s - 1, y + 10], 0, 180, fill=INK, width=1)
    elif kind == "robot":  # AI
        d.rectangle([x + 2, y + 3, x + s - 2, y + s - 2], fill=(200, 210, 225), outline=INK)
        d.point((x + 5, y + 7), fill=RED)
        d.point((x + 9, y + 7), fill=RED)
        d.line([(x + 5, y + 11), (x + 9, y + 11)], fill=INK, width=1)
    elif kind == "warn":  # Gaza
        d.polygon([(cx, y + 1), (x + s - 1, y + s - 1), (x + 1, y + s - 1)], fill=(250, 200, 60),
                  outline=INK)
        d.text((cx - 1, y + 5), "!", font=font("sans_b", 8), fill=INK)
    elif kind == "court":  # trials
        d.polygon([(x + 1, y + 5), (cx, y + 1), (x + s - 1, y + 5)], fill=GREY, outline=INK)
        for px in (x + 3, cx - 1, x + s - 4):
            d.line([(px, y + 6), (px, y + 11)], fill=INK, width=1)
        d.line([(x + 1, y + 12), (x + s - 1, y + 12)], fill=INK, width=1)
    elif kind == "bomb":  # car bomb
        d.rectangle([x + 1, y + 7, x + s - 1, y + 11], fill=(60, 60, 60))
        d.ellipse([x + 3, y + 11, x + 6, y + 14], fill=INK)
        d.ellipse([x + s - 6, y + 11, x + s - 3, y + 14], fill=INK)
        d.ellipse([cx - 4, y + 1, cx + 4, y + 9], fill=(250, 160, 40))
    elif kind == "bus":
        d.rectangle([x + 1, y + 3, x + s - 1, y + 11], fill=(240, 200, 40), outline=INK)
        d.rectangle([x + 3, y + 5, x + 6, y + 8], fill=SKY)
        d.rectangle([x + 8, y + 5, x + 11, y + 8], fill=SKY)
        d.ellipse([x + 3, y + 11, x + 6, y + 14], fill=INK)
        d.ellipse([x + s - 6, y + 11, x + s - 3, y + 14], fill=INK)
    elif kind == "school":
        d.rectangle([x + 2, y + 6, x + s - 2, y + 13], fill=(220, 180, 120), outline=INK)
        d.polygon([(x + 1, y + 6), (cx, y + 1), (x + s - 1, y + 6)], fill=RED)
        d.rectangle([cx - 2, y + 9, cx + 2, y + 13], fill=INK)
    elif kind == "shake":  # pact / handshake
        d.line([(x + 2, y + 9), (cx, y + 5)], fill=INK, width=2)
        d.line([(cx, y + 5), (x + s - 2, y + 9)], fill=INK, width=2)
        d.line([(x + 2, y + 9), (x + 5, y + 12)], fill=INK, width=1)
        d.line([(x + s - 2, y + 9), (x + s - 5, y + 12)], fill=INK, width=1)
    elif kind == "plane":
        d.polygon([(x + 1, y + 8), (x + s - 2, y + 4), (x + s - 2, y + 8), (x + 8, y + 10),
                   (x + 4, y + 12)], fill=(120, 140, 170), outline=INK)
    elif kind == "mount":
        d.polygon([(x + 1, y + 13), (x + 5, y + 4), (x + 9, y + 13)], fill=(120, 130, 150))
        d.polygon([(x + 6, y + 13), (x + 11, y + 6), (x + s - 1, y + 13)], fill=(90, 100, 125))
    elif kind == "doc":
        d.rectangle([x + 3, y + 1, x + s - 3, y + s - 1], fill=(255, 255, 255), outline=INK)
        for ly in (5, 8, 11):
            d.line([(x + 5, y + ly), (x + s - 5, y + ly)], fill=INK, width=1)
    elif kind == "build":
        d.rectangle([x + 2, y + 5, x + s - 2, y + 13], fill=(180, 180, 180), outline=INK)
        d.rectangle([x + 5, y + 8, x + 7, y + 10], fill=SKY)
        d.rectangle([x + 9, y + 8, x + 11, y + 10], fill=SKY)
    elif kind == "jet":
        d.polygon([(x + 2, y + 9), (x + s - 3, y + 3), (x + s - 1, y + 6), (x + 6, y + 11)],
                  fill=(90, 110, 140), outline=INK)
        d.line([(x + 6, y + 5), (x + 9, y + 9)], fill=INK, width=1)
    elif kind == "office":
        d.rectangle([x + 3, y + 2, x + s - 3, y + 13], fill=(200, 210, 220), outline=INK)
        for wy in (4, 7, 10):
            d.line([(x + 5, y + wy), (x + s - 5, y + wy)], fill=INK, width=1)
        d.line([(x + 2, y + 2), (x + s - 2, y + 13)], fill=RED, width=1)
    elif kind == "drone":
        d.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=(60, 60, 60))
        for dx, dy in [(-5, -4), (5, -4), (-5, 4), (5, 4)]:
            d.line([(cx, cy), (cx + dx, cy + dy)], fill=INK, width=1)
            d.ellipse([cx + dx - 2, cy + dy - 1, cx + dx + 2, cy + dy + 1], outline=INK)
    elif kind == "shield":
        d.polygon([(cx, y + 1), (x + s - 2, y + 4), (x + s - 2, y + 9), (cx, y + 13),
                   (x + 2, y + 9), (x + 2, y + 4)], fill=BLUE, outline=INK)
        d.text((cx - 2, y + 5), "S", font=font("sans_b", 7), fill=(255, 255, 255))
    elif kind == "candle":
        d.rectangle([cx - 2, y + 4, cx + 2, y + 12], fill=(255, 255, 255), outline=INK)
        d.ellipse([cx - 2, y + 1, cx + 2, y + 5], fill=(255, 200, 60))
        d.line([(x + 2, y + 13), (x + s - 2, y + 13)], fill=INK, width=1)
    elif kind == "chip":
        d.rectangle([x + 3, y + 3, x + s - 3, y + s - 3], fill=(30, 60, 90), outline=INK)
        d.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], fill=(90, 160, 220))
    elif kind == "flag":
        d.line([(x + 3, y + 1), (x + 3, y + 13)], fill=INK, width=1)
        d.rectangle([x + 3, y + 2, x + s - 2, y + 8], fill=BLUE)
        d.text((x + 6, y + 3), "UN", font=font("sans_b", 5), fill=(255, 255, 255))
    elif kind == "folder":
        d.rectangle([x + 2, y + 4, x + s - 2, y + 12], fill=(240, 200, 90), outline=INK)
        d.rectangle([x + 2, y + 4, x + 7, y + 6], fill=(240, 200, 90), outline=INK)
    elif kind == "dome":
        d.pieslice([x + 2, y + 2, x + s - 2, y + 10], 180, 360, fill=(200, 200, 200), outline=INK)
        d.rectangle([x + 2, y + 9, x + s - 2, y + 13], fill=(180, 180, 180), outline=INK)
    elif kind == "chart":
        d.line([(x + 2, y + 12), (x + 5, y + 8), (x + 8, y + 10), (x + 11, y + 5)],
               fill=GREEN, width=2)
        d.polygon([(x + 11, y + 5), (x + 9, y + 5), (x + 11, y + 7)], fill=GREEN)
    elif kind == "car":
        d.rectangle([x + 1, y + 8, x + s - 1, y + 11], fill=RED)
        d.polygon([(x + 3, y + 8), (x + 5, y + 5), (x + 10, y + 5), (x + 12, y + 8)], fill=RED)
        d.ellipse([x + 3, y + 11, x + 6, y + 14], fill=INK)
        d.ellipse([x + s - 6, y + 11, x + s - 3, y + 14], fill=INK)
    elif kind == "down":
        d.line([(x + 2, y + 3), (x + 5, y + 7), (x + 8, y + 5), (x + 11, y + 10)],
               fill=RED, width=2)
        d.polygon([(x + 11, y + 10), (x + 9, y + 10), (x + 11, y + 8)], fill=RED)
    elif kind == "pound":
        d.text((x + 3, y + 1), "£", font=font("sans_b", 12), fill=INK)
    elif kind == "coin":
        d.ellipse([x + 2, y + 2, x + s - 2, y + s - 2], fill=GOLD, outline=(150, 110, 0))
        d.text((x + 4, y + 2), "$", font=font("sans_b", 9), fill=(90, 60, 0))


# ---------------------------------------------------------------- content
LEADS = [
    dict(num=1, kick="MARKETS  •  USA & ASIA",
         head="HUANG RETURNS TO NVIDIA AS MARKETS SOAR",
         body=("Nvidia's board reappointed Jensen Huang as CEO on Monday, 10 days after he "
               "quit. Shares jumped 31% at the open, adding almost $1 trillion in value. "
               "The Nasdaq rose 6.51% to 24,089.56 and the S&P 500 4.73% — Wall Street's "
               "best day in over a year. Nikkei +3.91%, Kospi +6%, Taiex +9.1%. Trump "
               "claimed a role in Huang's return; lawmakers in both parties criticised "
               "him. Huang's wealth passed $143bn. An SEC inquiry continues."),
         src="Horizon Markets  •  Reuters  •  ApexWire",
         scene=scene_lead1),
    dict(num=2, kick="GULF  •  STRAIT OF HORMUZ",
         head="THREE SHIPS ABLAZE AFTER MINE STRIKES IN HORMUZ",
         body=("Three ships caught fire after hitting mines in the Strait of Hormuz; "
               "investigators are probing whether Iran is behind attacks on up to 50 "
               "vessels. Iran's chief negotiator refused talks until Washington meets "
               "seven conditions, and Tehran vowed to use “all means available” against "
               "a US blockade. The US Treasury sanctioned 24+ Iranian exchanges and "
               "exposed a ~$15bn shadow-banking network. Traffic in the strait is at "
               "47% of normal."),
         src="Horizon Geopolitics  •  WSJ  •  Cutthroat News",
         scene=scene_lead2),
    dict(num=3, kick="WAR  •  UKRAINE SPILLS OVER",
         head="UKRAINE WAR SPILLS INTO LIBYA, NATO REACTS",
         body=("Tripoli demanded answers from Kyiv after a Ukrainian sea-drone strike on "
               "a Russian warship at Benghazi, Libya — the Merkury corvette was "
               "reported sunk. Zaporizhzhia was hit again overnight: at least 2 dead, "
               "30+ hurt, including 4 children and a baby. NATO sent AWACS planes to "
               "Poland after 3 missiles fell on its soil; Secretary-General Mark Rutte "
               "meets Trump on Wednesday. Estonia shut its land border with Russia."),
         src="Horizon Geopolitics  •  Middle East Eye  •  Reuters",
         scene=scene_lead3),
]

SECONDS = [
    dict(num=4, kick="USA  •  JUSTICE",
         head="TRUMP ORDERS DOJ TO PURSUE DEATH PENALTY",
         body=("Trump ordered the Justice Department to seek the death penalty for child "
               "murder, rape and human trafficking, and to speed up federal executions."),
         scene=s_gavel),
    dict(num=5, kick="USA  •  TECH",
         head="TWO STATES SUE SPACEX OVER GROK DEEPFAKES",
         body=("Oregon and Virginia became the first states to sue SpaceX over Grok "
               "generating non-consensual sexual deepfakes and child-abuse material in "
               "“spicy mode”."),
         scene=s_robot),
    dict(num=6, kick="ASIA  •  CHIPS",
         head="US BLACKLISTS MEGASPEED OVER CHIP SALES",
         body=("The US put Singapore's Megaspeed and six affiliates on the Entity List "
               "over alleged AI-chip shipments to China; PM Wong vowed Singapore won't "
               "be a dodge route."),
         scene=s_chip),
    dict(num=7, kick="YEMEN  •  WAR",
         head="SAUDI STRIKES KILL 17–25 IN YEMEN, HOUTHIS SAY",
         body=("The Houthis reported 17 killed in a Saudi air strike on a telecoms "
               "facility in Hodeida and 25 killed or missing in a strike on a convoy "
               "in southern Yemen."),
         scene=s_strike),
    dict(num=8, kick="IRAN  •  RIGHTS",
         head="IRAN FLOGS SINGER PARASTOO AHMADI 74 TIMES",
         body=("Iran carried out 74 lashes on singer Parastoo Ahmadi in Qom, a "
               "“Woman, Life, Freedom” figure who sang without a hijab. Three musicians "
               "got the same sentence."),
         scene=s_mic),
    dict(num=9, kick="EUROPE  •  SANCTIONS",
         head="EU PROPOSES 22ND SANCTIONS PACKAGE ON RUSSIA",
         body=("The European Commission proposed a 22nd package: cutting 60 more banks "
               "from SWIFT, banning Russian symbols at EU sports events, and a crypto "
               "task force."),
         scene=s_eu),
    dict(num=10, kick="ASIA  •  QUAKE",
         head="QUAKE OF 5.6 SHAKES NEPAL NEAR CHINA BORDER",
         body=("A magnitude 5.6 quake (EMSC: 5.3; depth 10 km) struck Koshi Province, "
               "Nepal, near the China border early on Tuesday; tremors were felt in "
               "India."),
         scene=s_quake),
    dict(num=11, kick="HEALTH  •  GLOBAL",
         head="MEASLES AND A STRAINED HEALTH SYSTEM",
         body=("Pennsylvania recorded a ninth measles-linked death, with 46 counties "
               "affected. The WHO chief visited Cuba as its health system worsens amid "
               "fuel shortages."),
         scene=s_health),
    dict(num=12, kick="OCEANIA  •  TECH",
         head="AUSTRALIA: TECH GIANTS FACE FINES OF 5% OF REVENUE",
         body=("Tech companies including Google and Meta face fines of up to 5% of global "
               "revenue if they breach Australia's internet-safety bill, Reuters "
               "reported."),
         scene=s_fine),
    dict(num=13, kick="SPACE  •  CHINA",
         head="SHENZHOU-24 TO CARRY FIRST PAKISTANI TO TIANGONG",
         body=("China will launch Shenzhou-24 on Wednesday at 08:18 local time, carrying "
               "the first Pakistani, Zeeshan Ali — the first foreign astronaut on "
               "Tiangong."),
         scene=s_rocket),
]

BRIEFS = [
    ("scales", "THE HAGUE: 14 states back the ICJ ruling of genocide against the Rohingya in Myanmar."),
    ("robot", "UN: Guterres wants a multilateral framework to limit AI risks within a year."),
    ("warn", "GAZA: Oxfam calls Gaza “poisoned land”; children arrive in Britain for treatment."),
    ("court", "MEXICO: 'El Chapo Isidro' to be tried at home despite a US extradition request."),
    ("bomb", "COLOMBIA: Car bomb destroys a building in Villavicencio; no confirmed casualties."),
    ("bus", "UAE: 11 killed in a bus and lorry crash in Ras el-Khaimah."),
    ("school", "NIGERIA: School enrolment in Borno nearly doubles after years of conflict."),
    ("shake", "SOLOMON ISLANDS: Security pact with China scrapped in favour of Australia."),
    ("plane", "BANGLADESH: Ex-PM Hasina, sentenced to death, says she wants to return on 16 Dec."),
    ("mount", "ETHIOPIA & ERITREA: Forces face off again around the strategic town of Badmé."),
    ("doc", "ARMENIA: References to Nagorno-Karabakh removed from the draft Constitution."),
    ("build", "DENMARK: Top court upholds 'ghetto plan' and 'non-Western' tenant criteria."),
    ("jet", "SOUTH KOREA: Jets scrambled as a Russian warplane enters the air-defence zone."),
    ("office", "NORTH KOREA: Weighs closing the Swiss diplomatic office after camp sanctions."),
    ("drone", "SUDAN: Khartoum accuses the RSF of a drone strike on a UN building from Ethiopia."),
    ("shield", "SOMALIA & UGANDA: Operations against Al-Shabaab intensify as a pullout begins."),
    ("candle", "BRITAIN: Lilly Jones stabbed in Blaina; body found near Duffryn Park."),
    ("chip", "ARM: CEO Rene Haas's term extended to 2033 amid Nvidia speculation."),
    ("flag", "UN: Inquiry sought after reports of an attack on a Russian warship in Libya."),
    ("folder", "USA: Federal court unseals search papers from the home of Rep. Ilhan Omar."),
    ("dome", "USA: Rep. Jimmy Gomez to resign after an ethics panel found sexual misconduct."),
    ("court", "USA: Appeals court revives Trump's bid to move the hush-money case to federal court."),
    ("chart", "INDONESIA: MSCI leaves market status unchanged; a decision is expected in June 2027."),
    ("car", "EU: New-car sales up 5.4% in 10 months to 9.46m units, driven by EVs."),
    ("down", "BRAZIL: 2027 growth forecast cut to 1.8% as the inflation outlook rises to 4.5%."),
]

STATS = [
    ("NASDAQ", "+6.51%", "24,089.56"),
    ("S&P 500", "+4.73%", "7,237.17"),
    ("NIKKEI", "+3.91%", "58,644.63"),
    ("NVIDIA", "+31%", "~$1tn regained"),
    ("BRENT", "$86.70", "−2.99%"),
    ("NAT GAS", "+12.00%", "$3.57"),
]

TALLY = [("N. AMERICA", 9), ("EUROPE", 7), ("MIDDLE EAST", 5), ("ASIA", 8),
         ("AFRICA", 5), ("S. AMERICA", 2), ("OCEANIA", 2)]

DATE_CHECK = [
    "COP31 in Antalya COLLAPSED on Sunday 22 Nov — no mention of “fossil fuels”; 90+ nations rejected the draft. (CNN)",
    "Cikande candy-factory fire, Sat 21 Nov: 24 dead, ~30 missing confirmed Mon 23 Nov. The search goes on. (Reuters)",
    "Ukraine sea-drone strike on a Russian ship at Benghazi, Sun 23 Nov; Tripoli's reaction came Mon 23 Nov.",
    "Alcaraz won the ATP Finals in Turin, Sun–Mon 23 Nov; Ghana won the Amputee Football World Cup.",
    "NOT YET: Shenzhou-24 launches Wed 25 Nov; Rutte meets Trump Wed in Florida; ECB president named 26 Nov.",
]

# ---------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 14  # left margin; right edge 1010

    # ---- masthead
    d.rectangle([0, 0, W, 70], fill=DARK)
    t = "THE WORLD IN ONE PAGE"
    f = font("serif_b", 40)
    d.text(((W - tw(d, t, f)) / 2, 5), t, font=f, fill=(255, 255, 255))
    sub = "TUESDAY 24 NOVEMBER 2026  •  38 STORIES  •  7 REGIONS  •  ONE PAGE"
    fs = font("sans_b", 12)
    d.text(((W - tw(d, sub, fs)) / 2, 50), sub, font=fs, fill=GOLD)

    # ---- date strip
    d.line([(mx, 71), (1010, 71)], fill=RED, width=2)
    f11 = font("sans", 11)
    f11b = font("sans_b", 11)
    lab = "DATE CHECK: "
    d.text((mx, 75), lab, font=f11b, fill=BLUE)
    d.text((mx + tw(d, lab, f11b), 75),
           "Tuesday 24 November 2026 — today's news, as reported today; "
           "earlier events are dated in the text.", font=f11, fill=INK)
    d.line([(mx, 87), (1010, 87)], fill=INK, width=1)

    # ---- stat strip: 6 boxes
    for i, (label, value, sub2) in enumerate(STATS):
        bx = 13 + i * 167
        d.rectangle([bx, 88, bx + 163, 130], fill=(245, 243, 238), outline=GREY)
        fl = font("sans_b", 10)
        d.text((bx + (163 - tw(d, label, fl)) / 2, 91), label, font=fl, fill=GREY)
        fv = font("sans_b", 17)
        vcol = RED if (label == "BRENT") else (GREEN if value.startswith("+") else INK)
        d.text((bx + (163 - tw(d, value, fv)) / 2, 104), value, font=fv, fill=vcol)
        fs2 = font("sans", 9)
        scol = RED if (label == "BRENT") else GREY
        d.text((bx + (163 - tw(d, sub2, fs2)) / 2, 122), sub2, font=fs2, fill=scol)

    # ---- region tally band
    d.rectangle([0, 130, W, 150], fill=LGREY)
    tl = "REGION TALLY — "
    tr = "  •  ".join(f"{name} {n}" for name, n in TALLY)
    ft = font("sans", 11)
    ftb = font("sans_b", 11)
    tot = tw(d, tl, ftb) + tw(d, tr, ft)
    tx = (W - tot) / 2
    d.text((tx, 136), tl, font=ftb, fill=RED)
    d.text((tx + tw(d, tl, ftb), 136), tr, font=ft, fill=INK)

    # ---- leads
    lead_x = [14, 350, 686]
    for (lx, lead) in zip(lead_x, LEADS):
        fk = font("sans_b", 11)
        d.text((lx, 152), f"{lead['num']}  •  {lead['kick']}", font=fk, fill=RED)
        fh = font("serif_b", 20)
        para(d, lx, 166, lead["head"], fh, 324, 23, max_lines=2)
        lead["scene"](d, lx, 216, 324, 64)
        para(d, lx, 284, lead["body"], font("sans", 11), 324, 12.5, max_lines=8)
        d.text((lx, 386), "Sources: " + lead["src"], font=font("sans", 9), fill=GREY)
    for vx in (344, 680):
        d.line([(vx, 150), (vx, 396)], fill=LGREY, width=1)
    d.line([(mx, 396), (1010, 396)], fill=INK, width=1)

    # ---- secondaries: 2 rows x 5 cols
    sec_x = [16, 215, 414, 613, 812]
    for row in range(2):
        y0 = 396 + row * 118
        for col in range(5):
            s = SECONDS[row * 5 + col]
            sx = sec_x[col]
            fk = font("sans_b", 9)
            d.text((sx, y0 + 1), f"{s['num']}  •  {s['kick']}", font=fk, fill=RED)
            s["scene"](d, sx, y0 + 11, 195, 38)
            para(d, sx, y0 + 51, s["head"], font("sans_b", 11), 195, 12, max_lines=2)
            para(d, sx, y0 + 76, s["body"], font("sans", 9), 195, 10.5, max_lines=4)
        if row == 0:
            d.line([(mx, y0 + 118), (1010, y0 + 118)], fill=LGREY, width=1)
    d.line([(mx, 632), (1010, 632)], fill=INK, width=1)

    # ---- map + date check
    d.text((14, 636), "WHERE IT HAPPENED — 13 STORY SITES, NUMBERED",
           font=font("sans_b", 12), fill=BLUE)
    draw_map(d, 14, 650, 648, 158)
    fidx = font("sans_b", 9)
    idx1 = "1 Washington  •  2 Hormuz  •  3 Kyiv  •  4 Benghazi  •  5 Singapore  •  " \
           "6 Hodeida  •  7 Koshi, Nepal"
    idx2 = "8 Canberra  •  9 Seoul  •  10 London  •  11 Brussels  •  12 Borno  •  " \
           "13 Mexico City"
    d.text((14, 810), idx1, font=fidx, fill=INK)
    d.text((14, 821), idx2, font=fidx, fill=INK)

    d.rectangle([670, 632, 1010, 830], fill=(255, 248, 240), outline=GREY)
    d.text((678, 636), "DATE CHECK — NOT TODAY'S NEWS",
           font=font("sans_b", 11), fill=RED)
    iy = 662
    for item in DATE_CHECK:
        d.rectangle([678, iy + 4, 684, iy + 10], fill=RED)
        para(d, 690, iy, item, font("sans", 10), 312, 12, max_lines=2)
        iy += 27
    d.line([(678, 800), (1002, 800)], fill=GREY, width=1)
    d.text((678, 805), "ROUNDS: blind — Round 1 closes today, 19:00 WIB.",
           font=font("sans", 9), fill=GREY)

    # ---- briefs: 4 cols x 7 rows
    d.line([(mx, 830), (1010, 830)], fill=INK, width=1)
    d.text((14, 834), "ALSO ON TUESDAY — THE REST OF THE WORLD IN ONE LINE EACH",
           font=font("sans_b", 12), fill=INK)
    brief_x = [14, 263, 512, 761]
    fb = font("sans", 9)
    fnb = font("sans_b", 10)
    for i, (gkind, text) in enumerate(BRIEFS):
        # column-major: col0 = 7 items, col1..3 = 6 items each
        if i < 7:
            col, row = 0, i
        elif i < 13:
            col, row = 1, i - 7
        elif i < 19:
            col, row = 2, i - 13
        else:
            col, row = 3, i - 19
        bx = brief_x[col]
        by = 852 + row * 20
        num = str(14 + i) + "."
        d.text((bx, by + 1), num, font=fnb, fill=RED)
        glyph(d, bx + 22, by + 3, gkind)
        lines = wrap(d, text, fb, 201)
        if len(lines) > 2:
            lines = lines[:2]
            lines[1] = trunc(d, lines[1], fb, 201)
        for li, ln in enumerate(lines):
            d.text((bx + 40, by + li * 10), ln, font=fb, fill=INK)

    # ---- footer
    d.rectangle([0, 992, W, H], fill=DARK)
    f1 = "ALL THE DAY'S NEWS, IN ONE IMAGE — TUESDAY 24 NOVEMBER 2026"
    ff = font("sans_b", 10)
    d.text(((W - tw(d, f1, ff)) / 2, 996), f1, font=ff, fill=(255, 255, 255))
    f2 = ("Sources: Horizon • Reuters • AP • BBC • CNN • Al Jazeera • The Verge • "
          "Ars Technica • Semafor • The Daily Edition No. 279 • IQMIA • RSSignals • "
          "Cutthroat News")
    ff2 = font("sans", 9)
    d.text(((W - tw(d, f2, ff2)) / 2, 1009), f2, font=ff2, fill=(200, 200, 200))

    img.save(OUT, "PNG")
    print(f"saved {OUT} ({os.path.getsize(OUT)} bytes)")
    print(f"stories pictured: {len(LEADS)} leads + {len(SECONDS)} secondary "
          f"+ {len(BRIEFS)} briefs = {len(LEADS) + len(SECONDS) + len(BRIEFS)}")
    print(f"map pins: {len(PINS)}")
    return OUT


if __name__ == "__main__":
    build()
