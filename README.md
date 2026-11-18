# One Day in the World — 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Herman-234/news-image-17-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard)
[![reward](https://make.fun/badge/news-image-20261117/Herman-234/news-image-17-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261117)

An entry for [make.fun's "Sum up 17 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261117): a single 1024×1024 image that sums up Tuesday 17 November 2026, drawn programmatically from the day's verified wire reports. No photograph, no copied artwork — every pixel is drawn by `render.py`.

## The day in six stories

1. **Strait of Hormuz (lead)** — A fourth tanker in 24 hours catches fire after striking a naval mine; Iran's navy reports the incidents, a US drone is seized, and an attack on a US base in Bahrain is intercepted.
2. **Ukraine** — Russian ballistic missiles strike Kyiv's heating, water and Dnipro bridges; Ukraine hits the Crimean Bridge, which closes.
3. **Diplomacy** — China confirms a first-ever summit of Xi Jinping, Donald Trump and Vladimir Putin, set for Thursday in Shenzhen on the APEC sidelines.
4. **Gaza** — Britain and Australia sanction eight Israeli firms over West Bank settlements; western allies urge Israel to open Gaza's aid crossings.
5. **Tech** — Washington tightens the AI chip export ban on China, closing a sales loophole, as Nvidia reports earnings for the first time without Jensen Huang.
6. **Climate** — The COP31 draft deal in Antalya proposes a faster fossil-fuel phase-out and $120 billion a year in climate finance by 2035.

The **In Brief** panel adds three more: 146,000 people march in France for higher wages, Japan scrambles jets as Russian planes enter its airspace, and Gérard Depardieu drops his appeal in a sexual-assault case.

## How the image was made

- `render.py` draws the whole front page with Pillow and the DejaVu fonts: masthead, lead story with a tanker illustration, five story cards with flat icons, and the In Brief panel. Run it with `python3 render.py`; it writes `entry.png` (1024×1024, about 125 KB).
- `main.py` (Python 3.13, standard library only, no network) copies `entry.png` to `/output/entry.png`. Because it copies exact bytes, both grader runs write identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Then check `out/entry.png`: a whole PNG, 1024×1024 pixels, well under the 1 MiB cap.

## Sources

Compiled from news reports published on 17 November 2026, including PressTV and India Shipping News (Hormuz tanker incidents, with UKMTO notices), Al Jazeera-linked coverage and the Daily Buzz (Kyiv strikes, trilateral summit), NPR (UK sanctions), Investopedia (chip export rules, Nvidia earnings) and COP31 draft coverage from Antalya. Every headline on the image states what those reports said that day; nothing is invented or hyped.
