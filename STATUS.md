# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS+ (README and charts only; code kept private), Infield Weekly Report (overhauled, verified on live data), Yahoo pitcher tracker, learning files. PRS+ (v6) is an index (100 = average regular) backtested over 21 seasons — beats Marcel in 9 of 11 unseen seasons — with validated 80% WAR ranges and playing-time odds. PRS-P+ (pitchers) beats Marcel in 10 of 11 unseen seasons, also with validated ranges and workload odds. PR #1 (infield report overhaul + PRS+ docs/charts) merged to main 2026-10-07.

## Last change

2026-10-08 — PRS-P+ (pitchers): 21-season backtest vs Marcel (beats Marcel 10 of 11 unseen seasons, smaller average miss 11 of 11), then pitcher risk: 80% WAR ranges (79.6% coverage on 2016–26) and role-specific workload odds (150+ IP SP / 50+ IP RP) with durability labels. PRS README + 4 pitcher charts. (Earlier today: PR #1 merged.)

## Next step

After the 2026 postseason ends: rerun `prs_v6.py` and `prs_p.py` with final 2026 data and publish 2027 preseason PRS+ and PRS-P+ rankings (with risk ranges) as a dated GitHub release, to be graded after the 2027 season. Nothing to do until then.

## Blockers

Waiting for the 2026 postseason to finish before posting preseason rankings (Dave's call).
