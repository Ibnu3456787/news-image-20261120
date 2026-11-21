# Test report — news-image-20261120

Build: Sat 21 Nov 2026. Entry: `entry.png`, layout D front page for
Friday 20 November 2026. Format: test name / PASS–FAIL / evidence.

## 1. entry.png size and dimensions — PASS

- Evidence: `entry.png` is **299,626 bytes** (limit 1,048,576) and
  **1024×1024 px** (limit 1024×1024), RGB PNG. Verified with
  `ls -la` and PIL (`Image.open(...).size == (1024, 1024)`).
- sha256: `84c4d48185611e0c3f426daad75d3f48313a3538f0d07c74e581b2cf782950da`

## 2. main.py byte-identical reproduction — PASS

- Evidence: ran `main.py` twice into fresh directories
  (`/tmp/out1`, `/tmp/out2`); `cmp` of both outputs against
  `entry.png` reported identical, and all three sha256 digests
  match `84c4d481…950da`. A third run after the `main.py` revision
  (IHDR chunk-name check) also reproduced byte-identically.

## 3. compose.py warnings — PASS (no warnings)

- Evidence: `python3 compose.py` printed
  `entry.png: 299,626 bytes (OK <=1MiB)` followed by `no warnings`.
  The build checks every tile headline/sub for clipping and shrink
  floor, the lead sub for clipping, and every index line for width
  and box overflow; none fired.

## 4. Graded-run simulation (uid 65534, read-only parent) — PASS

- Evidence: repo copied to `/tmp/grade-sim/repo` (world-readable),
  parent dir mode 555, output dir mode 777, a stale file pre-seeded
  in the output dir **as uid 65534**, then run as
  `setpriv --reuid=65534 --regid=65534 --clear-groups env
  MAKEFUN_OUTPUT_DIR=/tmp/grade-sim/out timeout 10 python3 main.py`.
  Exit code **0**; output sha256 `84c4d481…950da`, byte-identical to
  the repo image; the pre-seeded stale file was left untouched.
  `main.py` never deletes anything: it only reads `entry.png` from
  the repo and writes `entry.png` inside the output directory.

## 5. No writes outside /output, no deletions, no network — PASS

- Evidence: `grep` of `main.py` for `rmtree|remove(|unlink|shutil|
  socket|urllib|requests|http` found no matches; the only writes are
  `os.makedirs(out_dir)` and the single `open(target, "wb")` inside
  the output dir. Same grep over `compose.py` and `vignettes.py`
  (build-time only, not run by the grader) found no matches.

## 6. Legibility at full size — PASS

- Evidence: viewed `entry.png` at 1024×1024. Masthead
  "THE WORLD TODAY", dateline "FRIDAY 20 NOVEMBER 2026", count line
  "35 STORIES · 6 CONTINENTS · ONE DAY" and the judge line are all
  crisp. Lead headline "RUSSIA STRIKES THREE KYIV BRIDGES" is the
  largest text on the page. All 10 tile headlines/subs, all 24 index
  lines and the sources line are readable with no overlap or
  clipping. All 11 map pins are visible and separated (verified in
  a 2× zoom of the map: pins 1/2/6/11 in Europe and 5/9 in New York
  are distinct, with leader lines to their true spots).

## 7. Legibility at ~300px — PASS

- Evidence: viewed `layouts/layout-d-300.png` (300×300). Masthead,
  date, count line and lead headline remain readable; the lead image
  (bridges + explosions) is instantly recognisable; tile images read
  as distinct coloured scenes; map pins are visible. Index text is
  small at this size, as expected — the composition still reads as
  one day's front page.

## 8. Illustration review at full size — PASS

- Evidence: each of the 11 panels in `candidates/` was viewed at
  1200×320. All are text-free and recognisable: #1 three bridges
  over the Dnipro with explosions, smoke, Kyiv skyline and Ukrainian
  flag; #2 Kh-101 missile, crater, Polish flag; #3 cyclone spiral,
  coast, evacuation bus and shelter; #4 weakening spiral over an
  atoll; #5 neon Vice City skyline with a gold record disc; #6 EU
  and UK flags with a handshake over a summit table; #7 Andes with
  tilted, cracked houses and shockwave rings; #8 dignified memorial
  silhouette with candles and South African flags; #9 NYSE facade
  with a plunging red chart; #10 red car with Argentine flag and
  showroom; #11 Antalya coast with negotiation table and a clock
  past midnight. Five fixes were made from this review and
  re-verified: #1 monument simplified to an obelisk, Lavra dome
  seated on its roof; #3 waves no longer cross the land; #6
  handshake redrawn as two arms meeting at a clasp; #8 candle halos
  reduced; #11 moon cut-out matched to the sky gradient.

## 9. Figure fidelity vs research-notes.md — PASS

- Evidence: every figure in `compose.py` was checked against
  `research-notes.md` plus the two coordinator adjustments in
  `verification-pass1.md`:
  - #1 uses **"at least 8 killed"** (Reuters nationwide), not
    "at least nine" (adjustment #1). Three bridges, biggest strikes
    on the Dnipro crossings since the war began.
  - #9 gives **Nasdaq -5.28%** and "S&P 500 enters correction" with
    **no** year-to-date figure (adjustment #2).
  - #3 uses **"300,000+ evacuated"** (notes: >300,000).
  - #5: **$3.79B** day one, **32.5M** pre-ordered (official
    Take-Two figures; superseded $2.36B/24.6M not used).
  - #7: **M6.7** (not 6.8); #12: **$88.91, -8.5%** (not $88.30);
    #18: **Nikkei -5.06% to 56,436.65** (closing, not intraday);
    #19: CPI **2.3%** YoY only; #21: **338,536-ha**; #26: **1,144**
    children; #33: **5,590** murders; #20: **$15B**; #23: Nicholls
    **175\***, India **159/1**; #2: Kh-101, Nowy Lipowiec, no one
    hurt; #28 framed as the **confirmation**, not the strike.
  - No figure from the notes' "Figures DROPPED" list appears
    anywhere in the entry (checked: no "nine killed", "6.8",
    "$88.30", "$2.36B", "24.6M", "1,600 fewer", "41 deaths",
    "130 kt", "0.4% GDP", youth age cap, "206/216", Sinner).
  - No third timezone-edge item was added (only #7 and #29, the
    two documented keeps).

## 10. Secrets check — PASS

- Evidence: `grep -rni` over all repo text files (`*.py`, `*.md`,
  `*.json`) for `api[_-]?key|password|secret|private[_-]?key|seed
  phrase|mnemonic|0x[0-9a-fA-F]{20,}|wallet` found no matches
  (research-notes.md excluded from the scan only because it is a
  research log, not shipped code — it holds no keys either).

## 11. File list (repo root) — complete

- `entry.png` — 299,626 bytes, sha256 `84c4d481…950da`
- `main.py` — entrypoint (stdlib-only copy pattern, revised twice)
- `compose.py` — front-page layout (layout D)
- `vignettes.py` — 11 text-free illustrations
- `candidates/` — the 11 rendered panels (`01-…` to `11-…`)
- `layouts/` — `layout-d.png` + `layout-d-300.png` previews
- `ne_110m_land.geojson` — Natural Earth 110m land (public data)
- `research-notes.md` — the 35 verified stories
- `README.md` — badges, run instructions, story table
- `LICENSE` — MIT (kit starter)
- `test-report.md` — this file
