# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS (write-up and charts only, code not in repo), Infield Weekly Report, Yahoo Fantasy pitcher tracker, and learning files. The infield report's accuracy overhaul is done and verified against the live MLB Stats API (May 4–10, 2026 output committed); the cloud environment now allows statsapi.mlb.com.

## Last change

2026-10-06 — Infield report overhaul: z-scored weights (OBP/HR/starts now truly 50/30/20), regression to the mean, PA-weighted recent form, active-roster (IL) filter, paginated pulls, postponed games skipped, positions from games actually fielded in the period (min 5 games), no future-data leakage, `--start`/`--out-dir` CLI. Re-ran May 4–10 live and replaced the old CSV/PNG.

## Next step

Push the PRS source script to `prs/` so its validation can be redone out-of-sample (tune weights on 2024, test against 2025 WAR / next-season WAR instead of same-season WAR).

## Blockers

PRS review is blocked until the PRS source code is added to the repo.
