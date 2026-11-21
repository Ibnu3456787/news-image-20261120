# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Ibnu3456787/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Ibnu3456787/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**THE WORLD TODAY — Friday 20 November 2026.** A one-page newspaper
front page summing up one day of world news: **35 stories, 6 continents,
one day**. Built for the make.fun competition `news-image-20261120`
($250 in USDC).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# writes /tmp/out/entry.png (1024x1024, 299,626 bytes, under the 1 MiB limit)
```

Run it twice into fresh directories: the output is byte-identical every
time — the program only copies a fixed file, then verifies the copy by
sha256.

## The image

`entry.png` (1024×1024, PNG) is a complete front page:

- **Masthead** — "THE WORLD TODAY", dated **FRIDAY 20 NOVEMBER 2026**,
  with the count line "35 STORIES · 6 CONTINENTS · ONE DAY" and the line
  "Every story below happened, or was first reported, on 20 November 2026."
- **Lead story** — Russia strikes three bridges over the Dnipro in Kyiv,
  as a full-width image band with a one-line headline and a one-line
  account beneath it.
- **11 illustrated stories** (numbered 1–11, region-tagged), each with a
  small original flat-editorial illustration drawn for this entry.
- **WHERE IT HAPPENED** — a world map (Natural Earth 110m land polygons)
  with numbered pins at the location of each of the 11 pictured stories.
- **ALSO ON THIS DAY** — a numbered index of stories 12–35.
- **Sources line** — Reuters, AP, AFP, Xinhua, USGS, IMD, Fiji Met,
  NASA, UNICEF, ATP, Formula 1.

All text is rendered with real fonts (Liberation Serif/Sans). The
illustrations are original vector drawings made for this entry with PIL;
they carry no text.

## The 11 illustrated stories

| # | Story | Region |
|---|-------|--------|
| 1 | Russia strikes three Kyiv bridges over the Dnipro | Europe |
| 2 | Russian missiles and a drone land in Poland | Europe |
| 3 | Cyclone Akvan makes landfall in India | Asia |
| 4 | Cyclone Xavier weakens over the Cook Islands | Oceania |
| 5 | GTA VI: $3.79B day one, biggest launch ever | North America |
| 6 | EU–UK summit in Brussels seals reset deals | Europe |
| 7 | M6.7 earthquake shakes central Peru | South America |
| 8 | Phumzile Mlambo-Ngcuka dies, 71 | Africa |
| 9 | Wall Street rout — Nasdaq -5.28% | North America |
| 10 | Tesla opens its first store in Argentina | South America |
| 11 | COP31 goes into overtime in Antalya, no deal | Europe |

The index (12–35) covers Anthropic's second day, the Nvidia SEC probe,
Trump's White House news conference, the Hormuz tanker strike, the
Hodeidah strikes, Gaza, the Nikkei plunge, Japan CPI, Prabowo–Xi in
Shenzhen, the RAPP licence revocation, Xi–Albanese, the India–NZ Test,
Oceania Challenge bowls, Estonia's border closure, UNICEF's Ukraine
child-casualty figures, the ATP Finals, the Druzhba confirmation, Las
Vegas GP FP3, the space-radiation study, the Billie Jean King Cup, Ben
Sedrine's sentence, South Africa's crime stats, Mahama's chiefs ban,
and Kenya's judiciary report.

## How it was built

- `research-notes.md` — the 35 verified stories, each with its facts,
  primary sources and publication timestamps. Every figure in the image
  comes from these notes; nothing was invented. Two timezone-edge items
  (the Peru quake, Las Vegas GP FP3) are documented there.
- `vignettes.py` — draws the 11 text-free illustrations into
  `candidates/` (flat editorial style, 1200×320 each).
- `compose.py` — lays out the front page and writes `entry.png`.
  It warns on any clipping, overflow or shrink-floor hit; this entry
  builds with **no warnings**.
- `ne_110m_land.geojson` — Natural Earth 110m land polygons (public
  data), used to draw the world map.
- `main.py` — the entrypoint: standard library only, no network.
  It validates `entry.png` (PNG signature, ≤1 MiB, ≤1024×1024) and
  copies it to `MAKEFUN_OUTPUT_DIR` (default `/output`), verifying
  the copy by sha256.

Rebuild the image from scratch with:

```sh
python3 vignettes.py   # draws candidates/NN-*.png
python3 compose.py     # lays out entry.png (1024x1024)
```

## Tests

See `test-report.md`: entry size and dimensions, sha256, byte-identical
reproduction of `main.py` (run twice into fresh directories), a
graded-run simulation as uid 65534 on a read-only parent directory,
compose warnings, legibility at 300px, illustration review at full
size, figure fidelity against `research-notes.md`, and a secrets check.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=zq0xe8tm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
