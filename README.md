# THE WORLD IN ONE PAGE — Tuesday 24 November 2026

[![News Image 24 Nov](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/menjadisukses-hope/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/menjadisukses-hope/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A one-page newspaper front page for **Tuesday 24 November 2026**: 38 sourced
stories from 7 regions, drawn entirely in code — no photographs, no copied
artwork.

## What's on the page

- **3 illustrated leads** — Nvidia's Jensen Huang returns as markets soar
  (Nasdaq +6.51%), three ships ablaze after mine strikes in the Strait of
  Hormuz, and the Ukraine war spilling into Libya as NATO sends AWACS to
  Poland. Each lead is a stickman scene acted out by a fixed character
  (negotiator with a tie, sailor with a cap, rescuer with a helmet).
- **10 illustrated secondaries** — the DOJ death-penalty directive, two states
  suing SpaceX over Grok, the Megaspeed blacklist, Saudi strikes in Yemen,
  the flogging of singer Parastoo Ahmadi, the EU's 22nd sanctions package,
  the Nepal quake, measles in Pennsylvania, Australia's tech fines, and
  Shenzhou-24 carrying the first Pakistani to Tiangong.
- **A proper world map** — recognisable continents, graticule, ocean labels,
  and 13 numbered pins at the story sites, with a pin index.
- **25 briefs**, each with its own drawn glyph, a 6-number markets strip, a
  region tally, and a **DATE CHECK** box for the 21–23 Nov stories that were
  deliberately not used as today's news.

## How it works

`generate.py` draws the whole 1024×1024 page from scratch with Pillow —
deterministic, no network, no timestamps. `main.py` copies `news.png` to the
entry output directory (`MAKEFUN_OUTPUT_DIR` or `/output`) as `entry.png`.

```sh
python3 generate.py   # renders news.png
python3 main.py       # writes /output/entry.png
```

## Sources

Horizon (daily 24 Nov), Reuters, AP, BBC, CNN, Al Jazeera, The Verge,
Ars Technica, Semafor, The Daily Edition No. 279, IQMIA, RSSignals,
Cutthroat News. Every fact on the page is dated 24 November 2026; earlier
events appear only in the DATE CHECK box.

Entry for the [make.fun News Image bounty, 24 Nov 2026](https://make.fun/bounty/news-image-20261124).
