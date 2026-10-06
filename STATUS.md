# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS (README only; code kept private), Infield Weekly Report (overhauled and verified on live MLB data), Yahoo pitcher tracker, and learning files. READMEs now describe PRS v3 (adds base-running, defense, positional value) and its out-of-sample validation (r ≈ 0.66 vs next-season WAR, matching prior-year WAR). Everything is on PR #1, awaiting merge.

## Last change

2026-10-06 — Infield report overhaul + live May 4–10 rerun; private PRS backtest and v2→v3 (v1 r 0.46 → v3 r 0.66 on 2024→2025 WAR); rewrote `prs/PRS_README.md` and root README to replace the same-season r = 0.675 claim with the backtest results.

## Next step

Merge PR #1. Then rebuild the PRS dashboard images (`prs/*.png`, still v1 from May 2026) using PRS v3 rankings and a next-season WAR scatter.

## Blockers

None.
