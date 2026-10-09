# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS+ (README and charts only; code kept private), Infield Weekly Report (overhauled, verified on live data), Yahoo pitcher tracker, learning files. PRS+ (v6) is an index (100 = average regular) backtested over 21 seasons — beats Marcel in 9 of 11 unseen seasons — with validated 80% WAR ranges and playing-time odds. PRS-P+ (pitchers) beats Marcel in 10 of 11 unseen seasons, also with validated ranges and workload odds. PR #1 (infield report overhaul + PRS+ docs/charts) merged to main 2026-10-07.

## Last change

2026-10-09 — Graded preseason 2026 PRS-P against the actual 2026 season (r 0.625 vs Marcel 0.610; 79% of outcomes inside 80% ranges). Built a private PRS+ Dashboard on claude.ai (https://claude.ai/artifact/Dux6TFRtAHzz3oYBr9ZJ5j): Hitters and Pitchers tabs (2027 rankings, 80% ranges, durability, searchable tables) and an Accuracy tab (21-season backtest vs Marcel, range coverage, playing-time odds). Built from PRS outputs only, no formula. (2026-10-08: PR #2 merged — PRS-P+ with risk ranges.)

## Next step

After the 2026 postseason ends: rerun `prs_v6.py` and `prs_p.py` with final 2026 data and publish 2027 preseason PRS+ and PRS-P+ rankings (with risk ranges) as a dated GitHub release, to be graded after the 2027 season, and refresh the dashboard's data files with the final numbers. Nothing to do until then.

## Blockers

Waiting for the 2026 postseason to finish before posting preseason rankings (Dave's call).
