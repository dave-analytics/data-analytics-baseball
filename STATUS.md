# Status — data-analytics-baseball

## Current state

Public sports analytics portfolio: PRS (Player Reliability Score — write-up and charts only, code not in repo), Infield Weekly Report, Yahoo Fantasy pitcher tracker, and learning files. The infield report was just rewritten for accuracy; it passes a mocked end-to-end test but has not yet been run against the live MLB Stats API.

## Last change

2026-10-06 — Infield report accuracy overhaul: z-scored weights (OBP/HR/starts now actually 50/30/20), regression to the mean, PA-weighted recent form (max 25%), active-roster filter drops IL players, paginated stats pulls, postponed games skipped, team-ID merge, traded-player handling, no future-data leakage for past weeks, `--start`/`--out-dir` CLI args instead of hardcoded dates and Desktop paths.

## Next step

Dave: run `python infield-report/infield_report.py --start 2026-05-04` locally (the MLB API is blocked from the cloud sandbox), sanity-check the rankings against the old May 4–10 CSV, then commit the new output. After that, push the PRS script so its validation can be redone out-of-sample (tune on 2024, test on 2025 WAR).

## Blockers

PRS review is blocked until the PRS source code is added to the repo.
