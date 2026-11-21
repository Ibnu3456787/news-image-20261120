#!/usr/bin/env python3
"""Build the news-image-20261120 front page (1024x1024) — layout D.

A newspaper front page for Friday 20 November 2026: masthead with a
big dateline, a full-width lead band for the Kyiv bridge strikes,
a 4-column grid of the other ten illustrated stories, a world map
with 11 numbered pins, and a two-column index of stories 12-35.

All story text follows research-notes.md exactly (with the two
coordinator adjustments: Kyiv toll "at least 8 killed" per Reuters,
and no precise Nasdaq year-to-date figure). The 11 illustrations are
the text-free panels drawn by vignettes.py; the map is drawn from
Natural Earth 110m land polygons (public data, ne_110m_land.geojson).

Usage: python3 compose.py
Outputs: entry.png (1024x1024) in this directory, plus a 300px
preview under layouts/. Prints "no warnings" when nothing clipped,
overflowed or hit a shrink floor.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "candidates")
LAYOUTS = os.path.join(HERE, "layouts")
W, H = 1024, 1024

PAPER = (250, 247, 240)
CARD = (255, 255, 255)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RULE = (215, 210, 198)
RED = (179, 38, 30)
NAVY = (27, 42, 74)
SEA = (220, 233, 242)
LAND = (232, 224, 208)
LAND_EDGE = (190, 180, 158)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

MARGIN, GAP = 12, 8


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns the list of lines."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def crop_cover(img, target_w, target_h, anchor=(0.5, 0.5)):
    """Centre-crop (or anchor-crop) an image to an aspect ratio, then
    resize to the target size with a high-quality filter."""
    iw, ih = img.size
    want = target_w / target_h
    have = iw / ih
    if have > want:
        new_w = int(ih * want)
        x = int((iw - new_w) * anchor[0])
        img = img.crop((x, 0, x + new_w, ih))
    else:
        new_h = int(iw / want)
        y = int((ih - new_h) * anchor[1])
        img = img.crop((0, y, iw, y + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


# ------------------------------------------------------------------ stories
# Headlines are set in caps; subs are one line in the tiles. Figures are
# the verified 20 Nov figures from research-notes.md.
STORIES = [
    dict(num=1, panel="01-kyiv-bridges.png", region="EUROPE",
         headline="RUSSIA STRIKES THREE KYIV BRIDGES",
         sub="Biggest strikes on the Dnipro crossings since the war "
             "began; at least 8 killed across Ukraine.",
         lat=50.45, lon=30.52),
    dict(num=2, panel="02-poland-missile.png", region="EUROPE",
         headline="RUSSIAN MISSILES LAND IN POLAND",
         sub="Kh-101 hits Nowy Lipowiec; no one hurt.",
         lat=50.44, lon=22.83),
    dict(num=3, panel="03-akvan-landfall.png", region="ASIA",
         headline="CYCLONE AKVAN HITS INDIA",
         sub="Landfall at Gopalpur; 300,000+ evacuated.",
         lat=19.26, lon=84.91),
    dict(num=4, panel="04-xavier-cook-islands.png", region="OCEANIA",
         headline="CYCLONE XAVIER WEAKENS",
         sub="Cat 3 to Cat 1 over the Cook Islands.",
         lat=-11.4, lon=-162.9),
    dict(num=5, panel="05-gta-record.png", region="NORTH AMERICA",
         headline="GTA VI: $3.79B DAY ONE",
         sub="Biggest launch ever; 32.5M pre-ordered.",
         lat=40.72, lon=-74.00),
    dict(num=6, panel="06-eu-uk-summit.png", region="EUROPE",
         headline="EU\u2013UK RESET DEALS SEALED",
         sub="SPS area, youth scheme, Erasmus+ return.",
         lat=50.85, lon=4.35),
    dict(num=7, panel="07-peru-quake.png", region="SOUTH AMERICA",
         headline="M6.7 QUAKE SHAKES PERU",
         sub="Felt in Lima; no casualties reported.",
         lat=-10.85, lon=-75.98),
    dict(num=8, panel="08-mlambo-memorial.png", region="AFRICA",
         headline="PHUMZILE MLAMBO-NGCUKA DIES, 71",
         sub="Led UN Women; deputy president 2005\u201308.",
         lat=-25.75, lon=28.19),
    dict(num=9, panel="09-wall-street-rout.png", region="NORTH AMERICA",
         headline="WALL STREET ROUT",
         sub="Nasdaq -5.28%; S&P 500 enters correction.",
         lat=40.71, lon=-74.01),
    dict(num=10, panel="10-tesla-argentina.png", region="SOUTH AMERICA",
         headline="TESLA OPENS IN ARGENTINA",
         sub="First store at Unicenter, Buenos Aires.",
         lat=-34.51, lon=-58.52),
    dict(num=11, panel="11-cop31-overtime.png", region="EUROPE",
         headline="COP31 INTO OVERTIME, NO DEAL",
         sub="Talks miss deadline; draft due Saturday.",
         lat=36.90, lon=30.71),
]

INDEX = [
    (12, "Anthropic day 2: shares -8.5% to $88.91; IPO closes."),
    (13, "Nvidia -14% as SEC examines its accounting."),
    (14, "Trump holds 90-minute White House news conference."),
    (15, "Tanker hit by projectile near Strait of Hormuz."),
    (16, "Saudi-led coalition strikes Hodeidah port."),
    (17, "Gaza: Israeli strikes kill six, civil defence says."),
    (18, "Nikkei plunges 5.06% to 56,436.65."),
    (19, "Japan October CPI 2.3%, an 11-month high."),
    (20, "Prabowo\u2013Xi meet in Shenzhen; $15B in deals."),
    (21, "Indonesia revokes RAPP\u2019s 338,536-ha forestry licence."),
    (22, "Xi\u2013Albanese hail \u2018comprehensive turnaround\u2019."),
    (23, "India\u2013NZ 1st Test: Nicholls 175*; India 159/1."),
    (24, "Oceania Challenge bowls: Australia takes 3 gold."),
    (25, "Estonia to close its border with Russia from 1 Dec."),
    (26, "UNICEF: 1,144 children killed or injured in Ukraine."),
    (27, "ATP Finals: Alcaraz and Medvedev into the semis."),
    (28, "Ukraine confirms Druzhba pipeline strike in Tatarstan."),
    (29, "Las Vegas GP: Russell fastest in FP3."),
    (30, "Space radiation changes brain immune cells, study finds."),
    (31, "Billie Jean King Cup: Canada and Brazil tied 1\u20131."),
    (32, "Tunisia: Ben Sedrine sentenced to 5 more years."),
    (33, "South Africa: 5,590 murders in a quarter."),
    (34, "Mahama defends ban on chiefs in party politics."),
    (35, "Kenya launches judiciary report; judges\u2019 scorecards unblocked."),
]

SOURCES = ("Sources: Reuters, AP, AFP, Xinhua, USGS, IMD, Fiji Met, "
           "NASA, UNICEF, ATP, Formula 1. The day\u2019s news, "
           "Friday 20 November 2026. Original drawings.")

JUDGE_LINE = ("Every story below happened, or was first reported, "
              "on 20 November 2026.")

PANEL_IMAGES = {s["panel"]: Image.open(os.path.join(PANELS, s["panel"]))
                .convert("RGB") for s in STORIES}

with open(os.path.join(HERE, "ne_110m_land.geojson")) as handle:
    GEO = json.load(handle)

LAT_TOP, LAT_BOTTOM = 74.0, -56.0

# Pin nudges, as fractions of map width / height, with leader lines to
# the true spot. #5 (Take-Two, NYC) and #9 (NYSE) are nearly identical;
# #1 Kyiv and #2 Poland share a latitude; #1 and #11 Antalya share a
# longitude. Without nudges the pins would overlap.
PIN_NUDGE = {
    1: (0.015, -0.07),    # Kyiv: up-right, away from Poland + Antalya
    2: (0.0, 0.06),       # Poland: down, away from Kyiv (left would
                          # push it into Brussels #6)
    5: (-0.02, -0.10),    # Take-Two NYC: up-left, away from NYSE
    9: (0.02, 0.12),      # NYSE: down-right, away from Take-Two
    11: (0.012, 0.09),    # Antalya: down-right, away from Kyiv + Poland
}


# ------------------------------------------------------------------ page
class FrontPage:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.warnings = []

    def masthead(self, rule_y):
        d = self.d
        f_title = font(SERIF_BOLD, 58)
        title = "THE WORLD TODAY"
        d.text(((W - d.textlength(title, font=f_title)) / 2, 2), title,
               fill=INK, font=f_title)
        f_date = font(SANS_BOLD, 17)
        dateline = "FRIDAY 20 NOVEMBER 2026"
        d.text(((W - d.textlength(dateline, font=f_date)) / 2, 62),
               dateline, fill=INK, font=f_date)
        f_count = font(SANS_BOLD, 15)
        count = "35 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY"
        d.text(((W - d.textlength(count, font=f_count)) / 2, 84), count,
               fill=RED, font=f_count)
        f_judge = font(SERIF_ITALIC, 13)
        d.text(((W - d.textlength(JUDGE_LINE, font=f_judge)) / 2, 104),
               JUDGE_LINE, fill=GREY, font=f_judge)
        d.line((MARGIN, rule_y, W - MARGIN, rule_y), fill=INK, width=2)

    def number_badge(self, x, y, radius, num, text_size=14):
        d = self.d
        cx, cy = x + radius, y + radius
        d.ellipse((cx - radius, cy - radius, cx + radius, cy + radius),
                  fill=RED)
        f = font(SANS_BOLD, text_size)
        label = str(num)
        d.text((cx - d.textlength(label, font=f) / 2,
                cy - text_size / 2 - 1), label, fill=CARD, font=f)

    def story_tile(self, box, story, pic_h, head_size=15, sub_size=11,
                   badge_radius=12):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in box)
        d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RULE, width=1)
        width = x1 - x0
        pic = crop_cover(PANEL_IMAGES[story["panel"]], width - 2, pic_h)
        self.img.paste(pic, (x0 + 1, y0 + 1))
        self.number_badge(x0 + 6, y0 + 6, badge_radius, story["num"])
        ty = y0 + 1 + pic_h + 5
        d.text((x0 + 6, ty), story["region"], fill=NAVY,
               font=font(SANS_BOLD, 10))
        ty += 13
        size = head_size
        while size > 10:
            f_head = font(SANS_BOLD, size)
            if len(wrap(d, story["headline"], f_head, width - 12)) <= 2:
                break
            size -= 1
        if size <= 10:
            self.warnings.append(
                f"tile {story['num']}: headline hit shrink floor")
        f_head = font(SANS_BOLD, size)
        for line in wrap(d, story["headline"], f_head, width - 12)[:2]:
            if ty + size > y1 - 2:
                self.warnings.append(f"tile {story['num']}: headline clipped")
                break
            d.text((x0 + 6, ty), line, fill=INK, font=f_head)
            ty += size + 2
        size = sub_size
        while size > 9:
            f_sub = font(SANS, size)
            if len(wrap(d, story["sub"], f_sub, width - 12)) <= 1:
                break
            size -= 1
        if size <= 9:
            self.warnings.append(
                f"tile {story['num']}: sub hit shrink floor")
        f_sub = font(SANS, size)
        for line in wrap(d, story["sub"], f_sub, width - 12)[:1]:
            if ty + size > y1 - 2:
                self.warnings.append(f"tile {story['num']}: sub clipped")
                break
            d.text((x0 + 6, ty), line, fill=GREY, font=f_sub)
            ty += size + 2

    def lead_band(self, pic_box, text_box):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in pic_box)
        d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RULE, width=1)
        # Anchor the crop low: the bridges and explosions sit in the
        # lower two-thirds of the Kyiv panel, the sky above them is
        # expendable.
        pic = crop_cover(PANEL_IMAGES[STORIES[0]["panel"]], x1 - x0 - 2,
                         y1 - y0 - 2, anchor=(0.5, 0.85))
        self.img.paste(pic, (x0 + 1, y0 + 1))
        self.number_badge(x0 + 6, y0 + 6, 14, 1, text_size=16)
        x0, y0, x1, y1 = (int(v) for v in text_box)
        d.rectangle((x0, y0, x1, y1), fill=CARD, outline=RULE, width=1)
        tx, ty = x0 + 10, y0 + 6
        d.text((tx, ty), "EUROPE", fill=NAVY, font=font(SANS_BOLD, 11))
        ty += 16
        f_head = font(SANS_BOLD, 26)
        for line in wrap(d, STORIES[0]["headline"], f_head, x1 - tx - 10):
            d.text((tx, ty), line, fill=INK, font=f_head)
            ty += 30
        f_sub = font(SANS, 13)
        for line in wrap(d, STORIES[0]["sub"], f_sub, x1 - tx - 10):
            if ty + 13 > y1 - 4:
                self.warnings.append("lead band: sub clipped")
                break
            d.text((tx, ty), line, fill=GREY, font=f_sub)
            ty += 17

    def map_panel(self, box, pin_radius=9):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in box)
        f_title = font(SANS_BOLD, 15)
        d.text((x0, y0), "WHERE IT HAPPENED", fill=NAVY, font=f_title)
        d.text((x0 + d.textlength("WHERE IT HAPPENED", font=f_title) + 10,
                y0 + 2), "the 11 pictured stories, numbered", fill=GREY,
               font=font(SANS, 12))
        top = y0 + 22
        mw, mh = x1 - x0, y1 - top
        d.rectangle((x0, top, x1, y1), fill=SEA, outline=RULE, width=1)

        def project(lon, lat):
            px = x0 + (lon + 180.0) / 360.0 * mw
            py = top + (LAT_TOP - lat) / (LAT_TOP - LAT_BOTTOM) * mh
            return (px, py)

        for feature in GEO["features"]:
            geom = feature["geometry"]
            rings = []
            if geom["type"] == "Polygon":
                rings = geom["coordinates"]
            elif geom["type"] == "MultiPolygon":
                for part in geom["coordinates"]:
                    rings.extend(part)
            for ring in rings:
                pts, prev_lon = [], None
                for lon, lat in ring:
                    if lat > LAT_TOP or lat < LAT_BOTTOM:
                        continue
                    if prev_lon is not None and abs(lon - prev_lon) > 180:
                        if len(pts) > 2:
                            d.polygon(pts, fill=LAND, outline=LAND_EDGE)
                        pts = []
                    pts.append(project(lon, lat))
                    prev_lon = lon
                if len(pts) > 2:
                    d.polygon(pts, fill=LAND, outline=LAND_EDGE)

        f_pin = font(SANS_BOLD, 11 if pin_radius <= 9 else 13)
        for story in STORIES:
            cx, cy = project(story["lon"], story["lat"])
            fx, fy = PIN_NUDGE.get(story["num"], (0.0, 0.0))
            px, py = cx + fx * mw, cy + fy * mh
            if (fx, fy) != (0.0, 0.0):
                d.line((cx, cy, px, py), fill=RED, width=1)
            d.ellipse((px - pin_radius - 1, py - pin_radius - 1,
                       px + pin_radius + 1, py + pin_radius + 1), fill=CARD)
            d.ellipse((px - pin_radius, py - pin_radius,
                       px + pin_radius, py + pin_radius), fill=RED)
            label = str(story["num"])
            tw = d.textlength(label, font=f_pin)
            d.text((px - tw / 2, py - f_pin.size / 2 - 1), label, fill=CARD,
                   font=f_pin)

    def index_panel(self, box, columns, size, row_height):
        d = self.d
        x0, y0, x1, y1 = (int(v) for v in box)
        f_title = font(SANS_BOLD, 15)
        d.text((x0, y0), "ALSO ON THIS DAY", fill=NAVY, font=f_title)
        d.text((x0 + d.textlength("ALSO ON THIS DAY", font=f_title) + 10,
                y0 + 2), "stories 12-35", fill=GREY, font=font(SANS, 12))
        top = y0 + 22
        f_num = font(SANS_BOLD, size)
        f_text = font(SANS, size)
        col_w = (x1 - x0 - (columns - 1) * 16) / columns
        per_col = (len(INDEX) + columns - 1) // columns
        for i, (num, text) in enumerate(INDEX):
            col, row = divmod(i, per_col)
            cx = x0 + col * (col_w + 16)
            cy = top + row * row_height
            if cy + size > y1:
                self.warnings.append(f"index {num}: row past box bottom")
            d.text((cx, cy), f"{num}.", fill=RED, font=f_num)
            num_w = d.textlength(f"{num}. ", font=f_num)
            text_w = d.textlength(text, font=f_text)
            if text_w > col_w - num_w:
                self.warnings.append(
                    f"index {num}: line too wide "
                    f"({text_w:.0f}px > {col_w - num_w:.0f}px)")
            d.text((cx + num_w, cy), text, fill=INK, font=f_text)

    def sources_line(self, y):
        d = self.d
        d.line((MARGIN, y - 6, W - MARGIN, y - 6), fill=RULE, width=1)
        f_src = font(SANS, 11)
        for j, line in enumerate(wrap(d, SOURCES, f_src, W - 2 * MARGIN)):
            d.text((MARGIN, y + j * 14), line, fill=GREY, font=f_src)


# ---------------------------------------------------------------- layout D
def column_x(col, col_w):
    return MARGIN + col * (col_w + GAP)


def build_page():
    """Lead band + 4-column hybrid: full-width lead image + headline
    band; two rows of four tiles; a third row of two tiles + the map
    (two columns wide); two-column index; sources line."""
    page = FrontPage()
    page.masthead(122)
    page.lead_band((MARGIN, 130, W - MARGIN, 290),
                   (MARGIN, 290, W - MARGIN, 360))
    col_w = (W - 2 * MARGIN - 3 * GAP) / 4  # 244
    for c in range(4):
        page.story_tile((column_x(c, col_w), 368,
                         column_x(c, col_w) + col_w, 500), STORIES[1 + c],
                        pic_h=64)
    for c in range(4):
        page.story_tile((column_x(c, col_w), 508,
                         column_x(c, col_w) + col_w, 640), STORIES[5 + c],
                        pic_h=64)
    for c in range(2):
        page.story_tile((column_x(c, col_w), 648,
                         column_x(c, col_w) + col_w, 776), STORIES[9 + c],
                        pic_h=62)
    page.map_panel((column_x(2, col_w), 648, W - MARGIN, 776), pin_radius=9)
    page.index_panel((MARGIN, 784, W - MARGIN, 968), columns=2, size=11,
                     row_height=13.5)
    page.sources_line(974)
    return page


def main():
    os.makedirs(LAYOUTS, exist_ok=True)
    page = build_page()
    page.img.save(os.path.join(LAYOUTS, "layout-d.png"), optimize=True)
    page.img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(LAYOUTS, "layout-d-300.png"))
    entry = os.path.join(HERE, "entry.png")
    page.img.save(entry, optimize=True)
    size = os.path.getsize(entry)
    status = "OK <=1MiB" if size <= 1048576 else "OVER 1MiB!"
    print(f"entry.png: {size:,} bytes ({status})")
    for warning in page.warnings:
        print(f"  WARNING: {warning}")
    if not page.warnings:
        print("  no warnings")


if __name__ == "__main__":
    main()
