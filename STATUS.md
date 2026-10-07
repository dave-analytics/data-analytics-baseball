# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS+ (README and charts only; code kept private), Infield Weekly Report (overhauled, verified on live data), Yahoo pitcher tracker, learning files. PRS+ v5 is an index (100 = average regular) backtested over 21 seasons: tuned on 2006–15, beats Marcel in 9 of 11 unseen seasons (r 0.669 vs 0.644). All work is on PR #1, awaiting merge.

## Last change

2026-10-07 — PRS v5 / PRS+: pulled 2003–2026 MLB + minor-league data, built a 20-season backtest with a Marcel baseline, re-tuned on 2006–15 only, added the PRS+ index and batting runs; rewrote PRS README; new charts (PRS+ top 10, PRS vs Marcel by season, 2025 forecast scatter).

## Next step

Merge PR #1. Then build PRS+ risk ranges (80% projection range + playing-time odds, calibrated on 2006–2015, checked on 2016–2026), then PRS-P for pitchers.

## Blockers

None.
