#!/usr/bin/env python3
"""Eleven text-free illustrations for news-image-20261120.

Flat editorial vector art drawn with PIL, one 1200x320 panel per
illustrated story (stories 1-11 of the 20 November 2026 front page).
No text anywhere in any panel: every story must read from shapes,
colour and recognisable subjects alone, at tile size (~242x64) and
at full size. The lead panel (#1, Kyiv bridges) is composed so its
key content sits inside y 60..260, the band the lead crop keeps.

Run: python3 vignettes.py  ->  writes candidates/NN-*.png
"""
import math
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "candidates")
W, H = 1200, 320

INK = (18, 18, 20)
NAVY = (26, 40, 72)
NAVY_DARK = (14, 24, 46)
OCHRE = (214, 162, 62)
OCHRE_DARK = (182, 126, 40)
PAPER = (250, 247, 240)
RED = (178, 36, 28)
TEAL = (44, 122, 104)
SKY = (166, 204, 224)
GOLD = (230, 188, 88)
WHITE = (255, 255, 255)
GREY = (118, 120, 124)
GREEN = (72, 138, 72)
ORANGE = (232, 120, 40)
SMOKE = (96, 92, 88)


def vertical_gradient(draw, top_rgb, bottom_rgb, y_top=0, y_bottom=H):
    """Fill the canvas with a smooth vertical colour blend."""
    span = max(1, y_bottom - y_top)
    for y in range(y_top, y_bottom):
        t = (y - y_top) / span
        colour = tuple(int(top_rgb[i] + (bottom_rgb[i] - top_rgb[i]) * t)
                       for i in range(3))
        draw.line([(0, y), (W, y)], fill=colour)


def disc(draw, cx, cy, radius, colour, outline=None, width=1):
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius),
                 fill=colour, outline=outline, width=width)


def tower(draw, x, base_y, width, height, colour, lit=True,
          window_colour=(250, 220, 140)):
    """A plain city block with a grid of lit windows."""
    draw.rectangle((x, base_y - height, x + width, base_y), fill=colour)
    if lit:
        for wy in range(base_y - height + 10, base_y - 6, 17):
            for wx in range(x + 7, x + width - 7, 15):
                draw.rectangle((wx, wy, wx + 6, wy + 8), fill=window_colour)


def pole(draw, x, base_y, height=140):
    draw.line((x, base_y, x, base_y - height), fill=(58, 58, 58), width=4)
    disc(draw, x, base_y - height - 2, 4, OCHRE)


def flag_poland(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h / 2), fill=WHITE)
    draw.rectangle((x, y + h / 2, x + w, y + h), fill=(220, 20, 60))


def flag_ukraine(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h / 2), fill=(0, 91, 172))
    draw.rectangle((x, y + h / 2, x + w, y + h), fill=(255, 213, 0))


def flag_eu(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=(0, 51, 153))
    cx, cy = x + w / 2, y + h / 2
    ring = min(w, h) * 0.30
    for k in range(12):
        a = math.radians(k * 30 - 90)
        disc(draw, cx + ring * math.cos(a), cy + ring * math.sin(a),
             max(2, int(h * 0.045)), (255, 204, 0))


def flag_uk(draw, x, y, w, h):
    draw.rectangle((x, y, x + w, y + h), fill=(1, 33, 105))
    draw.line((x, y, x + w, y + h), fill=WHITE, width=max(3, int(h * 0.18)))
    draw.line((x + w, y, x, y + h), fill=WHITE, width=max(3, int(h * 0.18)))
    draw.line((x, y, x + w, y + h), fill=(200, 16, 46), width=max(2, int(h * 0.07)))
    draw.line((x + w, y, x, y + h), fill=(200, 16, 46), width=max(2, int(h * 0.07)))
    draw.rectangle((x + w * 0.42, y, x + w * 0.58, y + h), fill=WHITE)
    draw.rectangle((x, y + h * 0.38, x + w, y + h * 0.62), fill=WHITE)
    draw.rectangle((x + w * 0.46, y, x + w * 0.54, y + h), fill=(200, 16, 46))
    draw.rectangle((x, y + h * 0.44, x + w, y + h * 0.56), fill=(200, 16, 46))


def flag_south_africa(draw, x, y, w, h):
    """Simplified South African flag: red/blue bands, green Y, black triangle."""
    draw.rectangle((x, y, x + w, y + h / 2), fill=(222, 45, 38))
    draw.rectangle((x, y + h / 2, x + w, y + h), fill=(0, 56, 137))
    draw.polygon([(x, y + h * 0.30), (x + w * 0.42, y + h / 2),
                  (x, y + h * 0.70)], fill=(0, 122, 61))
    draw.polygon([(x + w * 0.42, y + h / 2), (x + w, y + h * 0.28),
                  (x + w, y + h * 0.72)], fill=(0, 122, 61))
    draw.polygon([(x, y + h * 0.36), (x + w * 0.30, y + h / 2),
                  (x, y + h * 0.64)], fill=(0, 0, 0))
    draw.line((x, y + h * 0.30, x + w * 0.42, y + h / 2), fill=(255, 204, 0),
              width=2)
    draw.line((x, y + h * 0.70, x + w * 0.42, y + h / 2), fill=(255, 204, 0),
              width=2)


def flag_argentina(draw, x, y, w, h):
    band = h / 3
    draw.rectangle((x, y, x + w, y + band), fill=(116, 172, 223))
    draw.rectangle((x, y + band, x + w, y + 2 * band), fill=WHITE)
    draw.rectangle((x, y + 2 * band, x + w, y + h), fill=(116, 172, 223))
    cx, cy = x + w / 2, y + h / 2
    for k in range(12):
        a = math.radians(k * 30)
        r0, r1 = band * 0.28, band * 0.48
        draw.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a),
                   cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                  fill=(246, 180, 60), width=2)
    disc(draw, cx, cy, band * 0.26, (246, 180, 60))


def cyclone(draw, cx, cy, radius, colour, width=8, arms=3, turns=2.5):
    """A spiral storm: several curved arms around a calm eye."""
    for arm in range(arms):
        pts = []
        steps = 90
        for i in range(steps + 1):
            t = i / steps
            ang = arm * 2 * math.pi / arms + t * turns * 2 * math.pi
            r = 12 + t * (radius - 12)
            pts.append((cx + r * math.cos(ang),
                        cy + r * math.sin(ang) * 0.82))
        draw.line(pts, fill=colour, width=width, joint="curve")
    disc(draw, cx, cy, 13, (240, 244, 248), outline=colour, width=3)


def sea_waves(draw, y_top, y_bottom, colour, amp=6, spacing=16):
    for y in range(y_top, y_bottom, spacing):
        pts = []
        for x in range(0, W + 46, 46):
            pts.append((x, y + amp * math.sin(x / 55.0 + y)))
        draw.line(pts, fill=colour, width=3, joint="curve")


def palm_tree(draw, x, base_y, scale=1.0, colour=(32, 106, 68)):
    """A small palm; (x, base_y) is the trunk base."""
    draw.line((x, base_y, x + 6 * scale, base_y - 68 * scale),
              fill=(108, 78, 48), width=max(3, int(5 * scale)))
    tx, ty = x + 6 * scale, base_y - 68 * scale
    for ang, ln in ((-160, 44), (-120, 50), (-80, 50), (-40, 44),
                    (-200, 38), (0, 38)):
        a = math.radians(ang)
        draw.line((tx, ty,
                   tx + ln * scale * math.cos(a),
                   ty + ln * scale * math.sin(a) * 0.55),
                  fill=colour, width=max(3, int(5 * scale)))


def explosion(draw, cx, cy, size):
    """Fireball + smoke column + sparks for a strike."""
    for r, c in ((size, (255, 176, 60)), (size * 0.66, (255, 120, 30)),
                 (size * 0.38, (255, 235, 160))):
        disc(draw, cx, cy, int(r), c)
    for k in range(10):
        a = math.radians(k * 36 + 12)
        r0, r1 = size * 1.05, size * (1.35 + (k % 3) * 0.18)
        draw.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a),
                   cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
                  fill=(255, 176, 60), width=4)
    # smoke column rising and drifting
    for i, (sx, sy, sr) in enumerate(((cx - 6, cy - size - 22, 20),
                                      (cx + 10, cy - size - 52, 26),
                                      (cx + 30, cy - size - 78, 32),
                                      (cx + 56, cy - size - 96, 36))):
        disc(draw, sx, sy, sr, (70 + i * 6, 66 + i * 6, 64 + i * 6))


def save_panel(img, name):
    img.save(os.path.join(OUT, name), optimize=True)
    print("saved", name)


# ------------------------------------------------------------ 1 Kyiv (LEAD)
def v01_kyiv_bridges():
    img = Image.new("RGB", (W, H), NAVY_DARK)
    d = ImageDraw.Draw(img)
    # night sky lit orange by fire on the horizon
    vertical_gradient(d, (10, 16, 34), (120, 52, 32), 0, 235)
    disc(d, 1040, 62, 30, (244, 236, 210))  # moon
    disc(d, 1030, 54, 8, (212, 200, 172))
    # Kyiv skyline: Motherland Monument (tall figure with sword) + Lavra
    # bell tower + blocks, silhouetted against the glow
    base = 235
    for x, w, h in ((30, 42, 92), (86, 34, 66), (132, 48, 118),
                    (700, 40, 96), (756, 52, 130), (824, 36, 78),
                    (876, 44, 108), (1080, 40, 96), (1136, 42, 122)):
        tower(d, x, base, w, h, (10, 18, 36), lit=False)
    # Motherland Monument as a tall tapered obelisk on its pedestal
    d.rectangle((192, 176, 230, base), fill=(10, 18, 36))
    d.polygon([(198, 176), (206, 84), (216, 84), (224, 176)],
              fill=(10, 18, 36))
    d.line((211, 84, 211, 62), fill=(10, 18, 36), width=4)
    # Lavra bell tower with a golden dome seated on its roof
    d.rectangle((960, 150, 996, base), fill=(10, 18, 36))
    d.polygon([(952, 152), (978, 112), (1004, 152)], fill=(10, 18, 36))
    d.ellipse((966, 96, 990, 122), fill=GOLD)
    d.rectangle((976, 88, 980, 98), fill=GOLD)
    # the Dnipro river, wide, reflecting the fire
    d.rectangle((0, 235, W, H), fill=(20, 34, 58))
    for y in range(246, 312, 14):
        for x in range(0, W, 90):
            d.line((x, y, x + 44, y), fill=(255, 140, 60), width=2)
    # three bridges across the river: near (arch), middle (truss),
    # far (cable-stayed) — the struck crossings
    # far bridge, cable-stayed, upper left
    d.line((60, 268, 560, 268), fill=(200, 200, 200), width=5)
    d.line((300, 268, 300, 196), fill=(200, 200, 200), width=5)
    for dx in (-120, -70, -20, 30, 80, 130):
        d.line((300, 200, 300 + dx, 268), fill=(200, 200, 200), width=2)
    # middle bridge, truss, centre
    d.line((430, 286, 960, 286), fill=(190, 190, 190), width=6)
    for x in range(450, 950, 50):
        d.line((x, 286, x + 25, 252), fill=(190, 190, 190), width=3)
        d.line((x + 25, 252, x + 50, 286), fill=(190, 190, 190), width=3)
    d.line((430, 252, 960, 252), fill=(190, 190, 190), width=3)
    # near bridge, arch, lower right — broken span
    d.arc((700, 250, 1180, 360), 180, 360, fill=(210, 210, 210), width=7)
    d.line((700, 300, 940, 300), fill=(210, 210, 210), width=6)
    d.line((1060, 300, 1180, 300), fill=(210, 210, 210), width=6)
    d.line((940, 300, 980, 318), fill=(210, 210, 210), width=5)
    d.line((1060, 300, 1020, 318), fill=(210, 210, 210), width=5)
    # three explosions, one on each bridge
    explosion(d, 300, 250, 26)
    explosion(d, 700, 268, 30)
    explosion(d, 1000, 282, 24)
    # Ukrainian flag on the near bank
    pole(d, 60, 320, 96)
    flag_ukraine(d, 64, 226, 58, 38)
    save_panel(img, "01-kyiv-bridges.png")


# ------------------------------------------------------------ 2 Poland
def v02_poland_missile():
    img = Image.new("RGB", (W, H), (150, 190, 220))
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (140, 185, 220), (232, 226, 208), 0, 220)
    disc(d, 1050, 70, 36, (255, 214, 120))
    # flat Polish farmland + pine forest edge
    d.rectangle((0, 220, W, H), fill=(110, 150, 80))
    d.rectangle((0, 262, W, H), fill=(150, 120, 70))  # ploughed field
    for x in range(0, W, 26):
        d.line((x, 262, x - 14, H), fill=(128, 100, 58), width=2)
    for x in (30, 90, 150, 1060, 1120, 1180):
        d.polygon([(x, 222), (x + 16, 168), (x + 32, 222)], fill=(36, 96, 56))
        d.rectangle((x + 13, 218, x + 19, 232), fill=(90, 64, 40))
    # Kh-101 cruise missile diving in from the upper right
    mx, my = 830, 96
    d.polygon([(mx + 90, my - 26), (mx - 90, my + 26), (mx - 70, my + 40),
               (mx + 78, my - 8)], fill=(232, 232, 232))  # body
    d.polygon([(mx + 90, my - 26), (mx + 128, my - 36), (mx + 96, my - 10)],
              fill=(200, 40, 40))  # nose cone
    d.polygon([(mx - 60, my + 14), (mx - 30, my - 18), (mx - 6, my + 6)],
              fill=(180, 180, 180))  # wing
    d.polygon([(mx - 90, my + 26), (mx - 116, my + 6), (mx - 96, my + 44)],
              fill=(160, 160, 160))  # tail fin
    # vapour trail behind the missile
    for i in range(6):
        disc(d, mx - 130 - i * 42, my + 44 + i * 16, 12 - i,
             (240, 240, 240))
    # impact crater + fire + smoke in the field, centre-left
    d.ellipse((330, 250, 560, 296), fill=(60, 44, 30))
    d.ellipse((360, 256, 530, 288), fill=(30, 22, 16))
    explosion(d, 445, 236, 34)
    # Polish flag on a pole by a farmhouse, right
    d.rectangle((950, 196, 1040, 240), fill=(170, 60, 50))
    d.polygon([(940, 198), (995, 158), (1050, 198)], fill=(120, 44, 36))
    pole(d, 1080, 262, 130)
    flag_poland(d, 1084, 134, 64, 42)
    # a second distant smoke column on the horizon
    for i, (sx, sy, sr) in enumerate(((180, 190, 16), (196, 168, 20),
                                      (216, 148, 24))):
        disc(d, sx, sy, sr, (110 + i * 8, 106 + i * 8, 102 + i * 8))
    save_panel(img, "02-poland-missile.png")


# ------------------------------------------------------------ 3 Akvan
def v03_akvan_landfall():
    img = Image.new("RGB", (W, H), (42, 72, 92))
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (88, 118, 138), (202, 192, 162), 0, 200)
    # Bay of Bengal + Odisha coast curving in from the right
    d.rectangle((0, 200, W, H), fill=(28, 98, 122))
    d.polygon([(740, 200), (880, 200), (960, 252), (1010, 320), (1200, 320),
               (1200, 200)], fill=(118, 148, 94))
    d.polygon([(740, 200), (880, 200), (960, 252), (1010, 320), (1200, 320),
               (1200, 200)], outline=(224, 214, 182), width=3)
    for tx, ty in ((820, 214), (940, 236), (1070, 252)):
        disc(d, tx, ty, 16, (50, 108, 64))
    # cyclone spiral offshore, large, centre-left
    cyclone(d, 380, 138, 98, (246, 246, 246), width=8)
    cyclone(d, 380, 138, 98, (182, 202, 212), width=3)
    sea_waves(d, 224, 306, (200, 228, 235), amp=7)
    # waves run the full width, so redraw the coast on top of them
    d.polygon([(740, 200), (880, 200), (960, 252), (1010, 320), (1200, 320),
               (1200, 200)], fill=(118, 148, 94))
    d.polygon([(740, 200), (880, 200), (960, 252), (1010, 320), (1200, 320),
               (1200, 200)], outline=(224, 214, 182), width=3)
    for tx, ty in ((820, 214), (940, 236), (1070, 252)):
        disc(d, tx, ty, 16, (50, 108, 64))
    # evacuation bus on the coast road + people heading to shelter
    d.rectangle((830, 268, 990, 306), fill=(214, 160, 40))
    d.rectangle((830, 268, 990, 282), fill=(240, 240, 240))
    for wx in range(842, 978, 26):
        d.rectangle((wx, 272, wx + 16, 280), fill=SKY)
    disc(d, 862, 306, 10, (30, 30, 30))
    disc(d, 958, 306, 10, (30, 30, 30))
    # shelter building with a red cross-ish roof marker
    d.rectangle((1060, 236, 1170, 292), fill=(240, 236, 220))
    d.polygon([(1050, 238), (1115, 196), (1180, 238)], fill=(178, 60, 50))
    d.rectangle((1108, 208, 1122, 232), fill=WHITE)
    d.rectangle((1100, 216, 1130, 224), fill=WHITE)
    # rain streaks over the sea
    for x in range(60, 760, 58):
        d.line((x, 100, x - 12, 142), fill=(206, 219, 229), width=2)
    save_panel(img, "03-akvan-landfall.png")


# ------------------------------------------------------------ 4 Xavier
def v04_xavier_cook_islands():
    img = Image.new("RGB", (W, H), (34, 64, 84))
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (58, 88, 112), (158, 176, 184), 0, 208)
    d.ellipse((-40, 18, 320, 88), fill=(72, 90, 106))
    d.ellipse((220, 6, 560, 72), fill=(86, 102, 118))
    d.ellipse((830, 14, 1240, 86), fill=(72, 90, 106))
    # Pacific ocean
    d.rectangle((0, 208, W, H), fill=(26, 94, 116))
    sea_waves(d, 228, 308, (178, 218, 228), amp=5)
    # weakening cyclone: smaller, paler spiral, centre-left
    cyclone(d, 400, 146, 82, (232, 236, 238), width=6)
    cyclone(d, 400, 146, 82, (170, 190, 200), width=2)
    # a small atoll island with a hut and palms, right
    d.ellipse((800, 224, 1160, 288), fill=(88, 152, 86))
    d.rectangle((930, 204, 1050, 232), fill=(172, 122, 72))
    d.polygon([(916, 206), (990, 166), (1064, 206)], fill=(152, 72, 52))
    d.rectangle((976, 212, 1004, 232), fill=(62, 42, 26))
    palm_tree(d, 872, 240, 1.0)
    palm_tree(d, 1108, 242, 0.85)
    # rain streaks, lighter than Akvan's
    for x in range(40, 1180, 64):
        d.line((x, 118, x - 12, 160), fill=(202, 216, 226), width=2)
    save_panel(img, "04-xavier-cook-islands.png")


# ------------------------------------------------------------ 5 GTA VI
def v05_gta_record():
    img = Image.new("RGB", (W, H), (26, 12, 50))
    d = ImageDraw.Draw(img)
    # Vice City neon dusk
    vertical_gradient(d, (44, 18, 82), (212, 72, 138), 0, 232)
    disc(d, 980, 100, 44, (245, 238, 214))
    disc(d, 968, 90, 10, (214, 203, 175))
    # art-deco skyline with neon windows
    for x, w, h, c in ((20, 60, 148, (56, 30, 94)), (95, 44, 108, (70, 38, 108)),
                       (155, 70, 182, (46, 24, 82)), (240, 40, 118, (64, 34, 102)),
                       (700, 66, 168, (50, 28, 88)), (782, 44, 118, (68, 36, 106)),
                       (842, 58, 148, (44, 24, 80)), (1080, 60, 138, (58, 32, 96))):
        d.rectangle((x, 232 - h, x + w, 232), fill=c)
        for wy in range(232 - h + 10, 228, 20):
            for wx in range(x + 7, x + w - 6, 14):
                d.rectangle((wx, wy, wx + 5, wy + 8),
                            fill=(255, 118, 188) if (wx + wy) % 3
                            else (255, 208, 108))
    # neon horizon strip + ocean reflection
    d.rectangle((0, 230, W, 238), fill=(255, 108, 168))
    d.rectangle((0, 238, W, H), fill=(22, 14, 64))
    for i, y in enumerate(range(248, 314, 12)):
        ln = 300 - i * 18
        d.line((600 - ln, y, 600 + ln, y), fill=(255, 108, 168), width=3)
    # the record motif: a giant gold disc (platinum record) rising over
    # the bay, centre — the "biggest launch ever" hook, no text
    cx, cy, r = 500, 168, 86
    disc(d, cx, cy, r, GOLD, outline=(255, 226, 150), width=4)
    disc(d, cx, cy, r - 18, (206, 158, 60))
    disc(d, cx, cy, 16, (26, 12, 50))
    for rr in (34, 52, 70):
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr),
                  outline=(255, 226, 150), width=2)
    # sparkle stars around the disc
    for sx, sy, sr in ((392, 96, 10), (610, 88, 8), (622, 176, 9),
                       (388, 190, 7)):
        d.polygon([(sx, sy - sr), (sx + sr * 0.3, sy - sr * 0.3),
                   (sx + sr, sy), (sx + sr * 0.3, sy + sr * 0.3),
                   (sx, sy + sr), (sx - sr * 0.3, sy + sr * 0.3),
                   (sx - sr, sy), (sx - sr * 0.3, sy - sr * 0.3)],
                  fill=(255, 240, 180))
    # palms framing the scene
    palm_tree(d, 330, 244, 1.1, colour=(18, 58, 44))
    palm_tree(d, 1120, 244, 0.9, colour=(18, 58, 44))
    palm_tree(d, 60, 248, 0.8, colour=(18, 58, 44))
    save_panel(img, "05-gta-record.png")


# ------------------------------------------------------------ 6 EU-UK summit
def v06_eu_uk_summit():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (150, 194, 224), (246, 228, 202), 0, 232)
    disc(d, 1080, 78, 36, (255, 208, 110))
    # Brussels skyline: Berlaymont-style curved HQ + Atomium spheres
    d.rectangle((60, 150, 300, 232), fill=(120, 130, 140))
    d.arc((60, 110, 300, 232), 180, 360, fill=(150, 160, 172), width=14)
    for wy in range(160, 228, 16):
        for wx in range(74, 290, 18):
            d.rectangle((wx, wy, wx + 9, wy + 8), fill=(250, 220, 140))
    # Atomium: spheres on struts, right
    for sx, sy in ((980, 96), (1040, 150), (920, 150), (1040, 210),
                   (920, 210)):
        d.line((980, 150, sx, sy), fill=(170, 180, 190), width=5)
    for sx, sy, sr in ((980, 96, 22), (1040, 150, 22), (920, 150, 22),
                       (980, 150, 26), (1040, 210, 20), (920, 210, 20)):
        disc(d, sx, sy, sr, (200, 210, 220), outline=(140, 150, 160), width=2)
    d.rectangle((0, 232, W, H), fill=(96, 140, 92))
    # summit table with two flags behind it, centre
    pole(d, 420, 268, 150)
    flag_eu(d, 424, 120, 78, 52)
    pole(d, 740, 268, 150)
    flag_uk(d, 744, 120, 78, 52)
    d.rectangle((460, 236, 740, 252), fill=(120, 80, 50))
    d.line((480, 252, 480, 300), fill=(120, 80, 50), width=7)
    d.line((720, 252, 720, 300), fill=(120, 80, 50), width=7)
    # handshake above the table: two forearms rising to a clasp, centre
    d.line((500, 232, 588, 192), fill=(52, 80, 130), width=18)
    d.line((700, 232, 612, 192), fill=(120, 40, 36), width=18)
    d.ellipse((582, 178, 618, 206), fill=(232, 188, 150))
    d.line((588, 192, 612, 192), fill=(210, 165, 128), width=4)
    # papers + pens on the table
    d.rectangle((490, 222, 556, 236), fill=WHITE)
    d.rectangle((644, 222, 710, 236), fill=WHITE)
    d.line((494, 227, 552, 227), fill=(100, 110, 120), width=2)
    d.line((648, 227, 706, 227), fill=(100, 110, 120), width=2)
    save_panel(img, "06-eu-uk-summit.png")


# ------------------------------------------------------------ 7 Peru quake
def v07_peru_quake():
    img = Image.new("RGB", (W, H), (168, 190, 210))
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (150, 186, 214), (244, 226, 196), 0, 226)
    disc(d, 150, 80, 38, (255, 204, 110))
    # the Andes: steep snow-capped peaks
    d.polygon([(0, 226), (200, 84), (380, 226)], fill=(110, 118, 128))
    d.polygon([(280, 226), (520, 58), (760, 226)], fill=(96, 104, 116))
    d.polygon([(640, 226), (900, 96), (1200, 226)], fill=(118, 126, 136))
    d.polygon([(168, 112), (200, 84), (232, 112), (214, 126), (200, 116),
               (186, 126)], fill=WHITE)
    d.polygon([(478, 94), (520, 58), (562, 94), (540, 112), (520, 100),
               (500, 112)], fill=WHITE)
    d.polygon([(862, 124), (900, 96), (938, 124), (918, 138), (900, 128),
               (882, 138)], fill=WHITE)
    d.rectangle((0, 226, W, H), fill=(150, 128, 92))
    # shaking town: tilted buildings with cracks + dust clouds
    def tilted_house(x, base, w, h, tilt, colour):
        d.polygon([(x, base), (x + tilt, base - h), (x + w + tilt, base - h),
                   (x + w, base)], fill=colour)
        d.polygon([(x - 6, base - h), (x + w / 2 + tilt, base - h - 30),
                   (x + w + 6 + tilt, base - h)], fill=(150, 60, 44))
        # crack
        d.line((x + w // 2 + tilt, base - h,
                x + w // 2 + tilt - 8, base - h + 22,
                x + w // 2 + tilt + 4, base - h + 40),
               fill=(60, 40, 30), width=3)
    tilted_house(180, 262, 90, 70, -10, (220, 200, 170))
    tilted_house(320, 262, 110, 96, 12, (200, 178, 150))
    tilted_house(560, 262, 100, 84, -14, (226, 206, 176))
    tilted_house(760, 262, 120, 104, 10, (196, 172, 144))
    tilted_house(980, 262, 96, 72, -8, (222, 202, 172))
    # dust clouds at the bases
    for cx, cy in ((240, 268), (430, 272), (640, 268), (860, 272),
                   (1060, 268)):
        disc(d, cx, cy, 22, (210, 196, 168))
        disc(d, cx + 26, cy + 4, 16, (220, 206, 180))
    # shockwave rings radiating from the epicentre, centre
    for r in (40, 80, 120):
        d.ellipse((600 - r, 210 - r * 0.55, 600 + r, 210 + r * 0.55),
                  outline=RED, width=4)
    disc(d, 600, 210, 12, RED)
    # falling roof tiles / debris
    for px, py in ((300, 150), (520, 130), (700, 150), (880, 140)):
        d.rectangle((px, py, px + 12, py + 8), fill=(150, 60, 44))
    save_panel(img, "07-peru-quake.png")


# ------------------------------------------------------------ 8 Memorial
def v08_mlambo_memorial():
    img = Image.new("RGB", (W, H), (22, 26, 44))
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (18, 22, 40), (52, 44, 60), 0, 260)
    # soft glow behind the portrait
    for r, c in ((150, (70, 60, 80)), (110, (90, 78, 96)),
                 (70, (112, 96, 112))):
        disc(d, 600, 150, r, c)
    # dignified portrait silhouette: head + shoulders, centred
    d.ellipse((540, 52, 660, 176), fill=(30, 32, 52))  # head
    d.ellipse((510, 176, 690, 320), fill=(30, 32, 52))  # shoulders
    # hair bun + earring detail in gold
    disc(d, 600, 44, 18, (30, 32, 52))
    disc(d, 548, 132, 5, GOLD)
    disc(d, 652, 132, 5, GOLD)
    # a white collar / scarf line at the neck
    d.arc((556, 150, 644, 210), 0, 180, fill=(220, 220, 220), width=5)
    # South African flag draped at the base, left and right
    flag_south_africa(d, 120, 236, 180, 60)
    flag_south_africa(d, 900, 236, 180, 60)
    # candles in a row along the bottom, flames glowing
    for cx in range(240, 981, 92):
        d.rectangle((cx - 7, 268, cx + 7, 306), fill=(240, 236, 220))
        d.ellipse((cx - 9, 244, cx + 9, 272), fill=(255, 176, 60))
        d.ellipse((cx - 4, 250, cx + 4, 268), fill=(255, 236, 160))
        disc(d, cx, 258, 19, (255, 176, 60))  # halo behind flame
        d.ellipse((cx - 9, 244, cx + 9, 272), fill=(255, 176, 60))
        d.ellipse((cx - 4, 250, cx + 4, 268), fill=(255, 236, 160))
    # white flowers at the foot of the portrait
    for fx, fy in ((470, 296), (520, 304), (690, 304), (740, 296)):
        for k in range(5):
            a = math.radians(k * 72)
            disc(d, fx + 10 * math.cos(a), fy + 10 * math.sin(a), 7, WHITE)
        disc(d, fx, fy, 5, GOLD)
    save_panel(img, "08-mlambo-memorial.png")


# ------------------------------------------------------------ 9 Wall Street rout
def v09_wall_street_rout():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (14, 24, 46), (52, 30, 36), 0, 240)
    # NYSE facade: pediment + columns, left
    d.rectangle((40, 120, 420, 240), fill=(200, 196, 184))
    d.polygon([(30, 122), (230, 52), (430, 122)], fill=(216, 212, 200))
    disc(d, 230, 100, 18, (150, 140, 120))
    for cx in range(80, 401, 64):
        d.rectangle((cx - 12, 128, cx + 12, 240), fill=(176, 172, 160))
        d.rectangle((cx - 16, 122, cx + 16, 130), fill=(160, 156, 144))
        d.rectangle((cx - 16, 232, cx + 16, 240), fill=(160, 156, 144))
    d.rectangle((40, 240, 420, 252), fill=(150, 146, 134))
    # US flag above the pediment
    pole(d, 230, 62, 52)
    d.rectangle((234, 12, 292, 34), fill=WHITE)
    for i in range(4):
        d.rectangle((234, 12 + i * 6, 292, 15 + i * 6), fill=RED)
    d.rectangle((234, 12, 258, 24), fill=(32, 54, 120))
    # the rout: a huge plunging red chart dominating the right half
    d.rectangle((470, 40, 1160, 250), fill=(16, 20, 34))
    d.rectangle((470, 40, 1160, 250), outline=(80, 80, 90), width=3)
    for gy in range(80, 251, 42):
        d.line((470, gy, 1160, gy), fill=(44, 48, 60), width=1)
    pts = [(490, 70), (560, 84), (630, 76), (700, 108), (770, 96),
           (840, 140), (910, 128), (980, 176), (1050, 168), (1120, 224)]
    d.line(pts, fill=(230, 50, 40), width=9, joint="curve")
    for x, y in pts:
        disc(d, x, y, 6, (255, 120, 100))
    # down arrow at the end of the plunge
    d.polygon([(1120, 224), (1146, 224), (1133, 248)], fill=(230, 50, 40))
    d.rectangle((1130, 200, 1136, 226), fill=(230, 50, 40))
    # falling red candlesticks under the chart line
    for x, y0, y1 in ((560, 110, 150), (700, 130, 176), (840, 160, 204),
                      (980, 190, 232)):
        d.rectangle((x, y0, x + 20, y1), fill=(200, 40, 34))
        d.line((x + 10, y0 - 12, x + 10, y1 + 10), fill=(200, 40, 34),
               width=3)
    # ground + scattered red tickers
    d.rectangle((0, 252, W, H), fill=(12, 18, 34))
    for tx, ty in ((520, 272), (700, 284), (880, 272), (1060, 284)):
        d.polygon([(tx, ty + 10), (tx + 10, ty), (tx + 20, ty + 10)],
                  fill=(230, 50, 40))
        d.rectangle((tx + 24, ty + 2, tx + 60, ty + 8), fill=(230, 50, 40))
    save_panel(img, "09-wall-street-rout.png")


# ------------------------------------------------------------ 10 Tesla Argentina
def v10_tesla_argentina():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (148, 192, 222), (248, 230, 198), 0, 228)
    disc(d, 1040, 74, 38, (255, 208, 110))
    # showroom building with a glass front, background
    d.rectangle((60, 110, 1140, 228), fill=(228, 228, 228))
    d.rectangle((60, 110, 1140, 132), fill=(40, 44, 52))
    for wx in range(90, 1120, 78):
        d.rectangle((wx, 146, wx + 56, 228), fill=(168, 205, 228))
    d.rectangle((0, 228, W, H), fill=(90, 92, 96))
    d.rectangle((0, 228, W, 240), fill=(200, 200, 200))
    # Argentine flag flying above the showroom, centre
    pole(d, 600, 116, 84)
    flag_argentina(d, 604, 34, 72, 48)
    # red Tesla-style car, large, centre-foreground
    # body: sleek fastback silhouette
    d.polygon([(300, 268), (330, 218), (430, 200), (560, 196), (700, 204),
               (800, 228), (880, 252), (880, 272), (300, 272)],
              fill=(178, 24, 20))
    d.polygon([(330, 218), (430, 200), (560, 196), (700, 204), (800, 228),
               (760, 232), (420, 232), (350, 230)], fill=(40, 44, 52))
    d.polygon([(440, 202), (556, 198), (640, 202), (600, 228), (470, 228)],
              fill=(140, 190, 220))  # glass roof
    # headlight + grille-less nose
    d.polygon([(860, 246), (880, 252), (880, 262), (856, 260)],
              fill=(255, 240, 180))
    # wheels with silver rims
    for cx in (420, 760):
        disc(d, cx, 272, 30, (20, 20, 20))
        disc(d, cx, 272, 16, (200, 200, 200))
        disc(d, cx, 272, 6, (120, 120, 120))
    # red carpet + ribbon across the entrance
    d.polygon([(560, 306), (640, 306), (660, 320), (540, 320)],
              fill=(178, 24, 20))
    # small crowd silhouettes admiring the car
    for px, py, c in ((180, 240, (40, 60, 90)), (230, 246, (90, 50, 60)),
                      (960, 240, (50, 80, 50)), (1010, 246, (80, 70, 40))):
        disc(d, px, py - 18, 9, c)
        d.rectangle((px - 10, py - 10, px + 10, py + 34), fill=c)
    save_panel(img, "10-tesla-argentina.png")


# ------------------------------------------------------------ 11 COP31 overtime
def v11_cop31_overtime():
    img = Image.new("RGB", (W, H), (122, 192, 206))
    d = ImageDraw.Draw(img)
    vertical_gradient(d, (140, 200, 226), (250, 230, 190), 0, 208)
    disc(d, 180, 92, 40, (255, 208, 110))
    # Taurus mountains + Antalya bay
    d.polygon([(0, 208), (180, 118), (360, 188), (520, 128), (700, 204),
               (700, 208), (0, 208)], fill=(88, 118, 128))
    d.polygon([(180, 118), (150, 146), (210, 146)], fill=WHITE)
    d.rectangle((0, 208, W, 258), fill=(38, 148, 168))
    for x in range(0, W, 60):
        d.line((x, 230, x + 34, 230), fill=(200, 235, 240), width=3)
    d.rectangle((0, 258, W, H), fill=(238, 220, 180))
    palm_tree(d, 90, 270, 1.0)
    palm_tree(d, 1120, 272, 0.9)
    # negotiation table with papers + flags, centre-left
    d.rectangle((330, 236, 760, 252), fill=(120, 80, 50))
    d.line((350, 252, 350, 306), fill=(120, 80, 50), width=7)
    d.line((740, 252, 740, 306), fill=(120, 80, 50), width=7)
    d.polygon([(380, 240), (400, 200), (500, 200), (482, 240)], fill=WHITE,
              outline=(180, 180, 180), width=2)
    d.polygon([(520, 240), (542, 204), (642, 204), (622, 240)],
              fill=(235, 240, 235), outline=(180, 180, 180), width=2)
    for lx, ly in ((412, 210), (416, 220), (552, 214), (556, 224)):
        d.line((lx, ly, lx + 52, ly), fill=(90, 110, 90), width=3)
    # green leaf sprig on the papers
    d.ellipse((560, 186, 596, 208), fill=(60, 140, 80))
    d.ellipse((594, 194, 624, 210), fill=(74, 160, 90))
    # the overtime hook: a big clock running past midnight, right
    cx, cy, r = 940, 150, 74
    disc(d, cx, cy, r, WHITE, outline=NAVY, width=6)
    for k in range(12):
        a = math.radians(k * 30)
        r0, r1 = r - 14, r - 6
        d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a),
                cx + r1 * math.cos(a), cy + r1 * math.sin(a)),
               fill=NAVY, width=3)
    # hands just past twelve: the deadline missed
    d.line((cx, cy, cx - 4, cy - r + 22), fill=INK, width=6)
    d.line((cx, cy, cx + r - 30, cy - 14), fill=RED, width=5)
    disc(d, cx, cy, 7, RED)
    # crescent moon above the clock: talks run into the night. The
    # cut-out disc matches the sky gradient at that height (y~46).
    disc(d, 940, 52, 22, (245, 238, 214))
    disc(d, 950, 46, 18, (167, 207, 217))
    save_panel(img, "11-cop31-overtime.png")


PANELS = (v01_kyiv_bridges, v02_poland_missile, v03_akvan_landfall,
          v04_xavier_cook_islands, v05_gta_record, v06_eu_uk_summit,
          v07_peru_quake, v08_mlambo_memorial, v09_wall_street_rout,
          v10_tesla_argentina, v11_cop31_overtime)


def main():
    os.makedirs(OUT, exist_ok=True)
    for fn in PANELS:
        fn()


if __name__ == "__main__":
    main()
