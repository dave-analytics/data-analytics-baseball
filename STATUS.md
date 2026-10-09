# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS+ (README and charts only; code kept private), Infield Weekly Report (overhauled, verified on live data), Yahoo pitcher tracker, learning files. PRS+ (v6) is an index (100 = average regular) backtested over 21 seasons — beats Marcel in 9 of 11 unseen seasons — with validated 80% WAR ranges and playing-time odds. PRS-P+ (pitchers) beats Marcel in 10 of 11 unseen seasons, also with validated ranges and workload odds. PR #1 (infield report overhaul + PRS+ docs/charts) merged to main 2026-10-07.

## Last change

2026-10-09 — Graded preseason 2026 PRS-P against the 2026 season; found the FIP-based vs runs-allowed WAR gap (Skenes: 4.2 vs 3.0). Labeled PRS-P as FIP-based everywhere and added a validated 80% runs-allowed WAR range (78.7% coverage 2016–26). PRS README: "Which WAR?" note, runs-allowed range, 2026 report card; charts relabeled. Dashboard updated with both ranges.

## Next step

After the 2026 postseason ends: rerun `prs_v6.py` and `prs_p.py` with final 2026 data and publish 2027 preseason PRS+ and PRS-P+ rankings (with risk ranges) as a dated GitHub release, to be graded after the 2027 season, and refresh the dashboard's data files with the final numbers. Nothing to do until then.

## Blockers

Waiting for the 2026 postseason to finish before posting preseason rankings (Dave's call).
