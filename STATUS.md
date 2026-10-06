# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS (write-up and charts only, code not in repo), Infield Weekly Report, Yahoo Fantasy pitcher tracker, and learning files. The infield report's accuracy overhaul is done and verified against the live MLB Stats API (May 4–10, 2026 output committed); the cloud environment now allows statsapi.mlb.com.

## Last change

2026-10-06 — Infield report overhaul: z-scored weights (OBP/HR/starts now truly 50/30/20), regression to the mean, PA-weighted recent form, active-roster (IL) filter, paginated pulls, postponed games skipped, positions from games actually fielded in the period (min 5 games), no future-data leakage, `--start`/`--out-dir` CLI. Re-ran May 4–10 live and replaced the old CSV/PNG.

## Next step

PRS stays private (not in this repo). Backtest done privately: PRS v2 predicts next-season WAR at r ≈ 0.57 out-of-sample vs 0.46 for v1. Next: Dave decides whether to adopt v2, then update `prs/PRS_README.md` — its "r = 0.675 vs 2026 WAR" claim was same-season against a partial (~May) 2026 WAR file. Merge PR #1 (infield report).

## Blockers

None.
