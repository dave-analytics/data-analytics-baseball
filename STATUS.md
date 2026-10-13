# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS+ (README and charts only; code kept private), Infield Weekly Report, Yahoo pitcher tracker, learning files. PRS+ v7 (hitters) and PRS-P+ v2 (pitchers) are backtested over 21 seasons against Marcel. Projected WAR now blends PRS with Marcel. Playing-time and workload odds use injured-list history. The 80% ranges are recalibrated: 80% coverage for hitters, 79% for pitchers, and 79% for pitcher aces.

## Last change

2026-10-13 — Built PRS v7 and PRS-P v2 (private scripts sent to Dave, not in the repo). Changes: Marcel blend (65/35 for hitters, 90/10 for pitchers); IL-history features for odds only, since they didn't help WAR forecasts; top-tier ranges pooled across ages using the last 5 seasons. Reran the 2026 rankings, refreshed 6 charts, and updated PRS_README (blend, IL history, new coverage numbers, honest gaps, version history). Dashboard now runs on the v7/v2 data.

## Next step

After the 2026 postseason, rerun `prs_v7.py` and `prs_p2.py` with final data and publish 2027 preseason rankings as a dated GitHub release.

## Blockers

Preseason rankings are waiting for the postseason to end (Dave's call).
