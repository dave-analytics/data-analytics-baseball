# data-analytics-baseball

Sports Analytics Portfolio | Dave Goss
Python · SQL · pandas · Excel · MLB Stats API

linkedin.com/in/davidrgoss

---

## About

Self-directed data analytics learning journey targeting sports analyst 
roles in the Nashville market. This repo documents the full progression 
from Python fundamentals through original statistical research.

---

## Projects

### PRS — Player Reliability Score
An original MLB statistic measuring reliable all-around value:
how good a player is × how much he actually plays.
Combines three-season hitting quality (with minor-league stats
for young players), an age curve, base-running, defense, positional
value, and plate-appearance availability. Backtested out of sample:
predicts next-season WAR at r = 0.67 — slightly better than prior-year WAR.

📁 [/prs](./prs)

### Infield Weekly Report
Weekly fantasy rankings for C, 1B, 2B, 3B, and SS from the live
MLB Stats API. Scores on-base ability, power, and expected starts
(z-scored, regressed to the mean), filters out injured players,
and runs for any week: `python infield_report.py --start 2026-05-04`.

📁 [/infield-report](./infield-report)

### Pitcher Tracker
Yahoo Fantasy API integration tracking pitcher usage 
and performance using OAuth2 authentication.

📁 [/pitcher-tracker](./pitcher-tracker)

### Learning Files
Python, pandas, and SQL review files documenting 
Phase 1 and Phase 2 of the analytics roadmap.

📁 [/learning](./learning)

---

## Dashboard

### PRS Rankings — 2026 Top 10 (v4)
![PRS Rankings Dashboard](prs/PRS_Rankings_Dashboard.png)

### Does PRS Predict Next Season? (built from 2022–24, tested on 2025 WAR)
![PRS vs WAR Scatter](prs/PRS_vs_WAR_Scatter.png)

---

## Tech Stack
- Python 3.14
- pandas · matplotlib · requests
- MLB Stats API · Baseball Reference
