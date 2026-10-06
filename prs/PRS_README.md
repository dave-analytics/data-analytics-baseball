# PRS — Player Reliability Score

**An original baseball statistic built from scratch in Python.**

## What Is PRS?

PRS (Player Reliability Score) measures the **offensive reliability** of MLB position players — not just how good they are, but how much good offense you can count on getting from them next season.

Most fantasy baseball and front office metrics measure peak performance. PRS measures *dependable* performance. A player who posts elite numbers in 90 games is less valuable than one who posts solid numbers in 155 games. PRS quantifies that gap.

## The Core Idea

PRS = **how well he hits** × **how much he plays**

1. **Hitting Quality** — on-base ability and power, measured over the last three seasons
2. **Age Adjustment** — accounts for the natural aging curve of MLB players
3. **Availability** — how many plate appearances the player has actually delivered over the last three seasons

The result is a single score that reflects both offensive value and how likely a player is to be in the lineup to provide it.

## Methodology

### Hitting Quality
On-base percentage and home run rate from the last three seasons, weighted toward the most recent season. Rates are regressed toward league average, so a hot 150 plate appearances doesn't outrank a proven full season. Each stat is standardized (z-scored) before blending, so every component counts as much as its weight says.

### Age Adjustment
Players are adjusted by their age during the season (MLB's June 30 convention): younger hitters are expected to improve, older hitters to decline.

### Availability
Plate appearances over the last three seasons, weighted toward the most recent. A missed season counts as zero — that's the reliability in Player Reliability Score.

## Validation

PRS is tested the hard way: build it using **only data available before a season**, then check how well it predicts that **next** season's WAR (Wins Above Replacement, Baseball Reference). The model was tuned on one season and tested on seasons it had never seen.

| PRS built from | Tested against | PRS v1 | **PRS v2** | Plain OPS |
|---|---|---|---|---|
| 2021–2023 | 2024 WAR | 0.43 | **0.58** *(tuning season)* | 0.32 |
| 2022–2024 | 2025 WAR | 0.46 | **0.57** | 0.35 |
| 2023–2025 | 2026 WAR* | 0.34 | **0.38** | 0.29 |

<sub>Pearson correlation (r), ~440–480 position players per season. \*2026 WAR is a partial-season snapshot (through late May), which lowers every correlation.</sub>

**Key findings:**
- PRS v2 predicts next-season WAR at **r ≈ 0.57 on data it was never tuned on**, clearly ahead of plain OPS.
- **Availability was the missing piece.** Adding it was the single biggest improvement over v1.
- The age adjustment adds real predictive value (about +0.05 r).
- **Prior-year WAR still predicts better (r = 0.66)** because WAR also credits defense, base-running, and position — things PRS deliberately leaves out. PRS is an offense-only reliability measure.

### What changed from v1
PRS v1 was validated against **same-season** 2026 WAR (r = 0.675), using a partial-season WAR file. That mostly confirmed that PRS and WAR were measuring the same two months of hitting, not that PRS predicts anything. Backtesting showed:
- v1's **resilience modifier** (OBP in the 15 games before vs. after an absence) did not improve predictions — 15-game windows are too small to separate a real bounce-back from luck — so it was removed.
- v1 had no true availability component; plate-appearance history alone predicted next-season WAR as well as v1 did.
- Batting average was dropped as largely redundant with OBP.

## Tech Stack

- **Python 3.14**
- **pandas** — data manipulation and weighted calculations
- **requests** — MLB Stats API calls (no authentication required)
- **MLB Stats API** — season stats and player bios
- **Baseball Reference** — WAR data for validation

## Sample Output — PRS v2, 2026

```
name               team                    age   PA   OBP   HR   prs
Juan Soto          New York Mets            27   482  .393   27  24.8
Shohei Ohtani      Los Angeles Dodgers      31   618  .377   30  23.5
Aaron Judge        New York Yankees         34   285  .360   18  22.4
Junior Caminero    Tampa Bay Rays           22   702  .360   42  20.8
James Wood         Washington Nationals     23   623  .388   30  19.6
```

## Dashboard (PRS v1, May 2026)

### PRS Rankings — Top 10 Players
![PRS Rankings Dashboard](PRS_Rankings_Dashboard.png)

### PRS vs WAR Correlation
![PRS vs WAR Scatter](PRS_vs_WAR_Scatter.png)

## What's Next

- **Updated dashboard** — rebuild the charts with PRS v2 and next-season validation
- **PRS-P** — a pitcher version using ERA, strikeout rate, and innings pitched
- **Tableau dashboard** — interactive PRS leaderboard by position
- **Performance Resilience Score** — revisit resilience with larger samples (e.g. full months, minor-league returns) and keep it only if it improves the backtest

## About

Built by Dave Goss as part of a self-directed data analytics learning journey targeting sports analytics roles in the Nashville market. This project applies Python, pandas, API integration, feature engineering, and out-of-sample validation to an original research question.

Portfolio: [github.com/dave-analytics/data-analytics-baseball](https://github.com/dave-analytics/data-analytics-baseball)  
LinkedIn: [linkedin.com/in/davidrgoss](https://linkedin.com/in/davidrgoss)

---

*Note: Full formula weights, tuning methodology, and implementation details are proprietary.*
