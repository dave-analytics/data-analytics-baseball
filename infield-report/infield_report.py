"""
Infield Weekly Report — ranks MLB infielders (C, 1B, 2B, 3B, SS) for a
fantasy week using the MLB Stats API.

Usage:
    python infield_report.py                      # week starting this Monday
    python infield_report.py --start 2026-05-04   # any week (Mon-Sun)
    python infield_report.py --out-dir reports --show

Score = 50% OBP + 30% HR rate + 20% expected starts, where each part is
converted to a z-score first so the weights mean what they say.
"""

import argparse
import os
from datetime import date, datetime, timedelta

import pandas as pd
import requests

API = "https://statsapi.mlb.com/api/v1"

# ─────────────────────────────────────────
# MODEL SETTINGS
# ─────────────────────────────────────────
INFIELD_POSITIONS = ['C', '1B', '2B', '3B', 'SS']

WEIGHTS = {'obp': 0.50, 'hr_rate': 0.30, 'starts': 0.20}

MIN_PA = 50                # minimum season plate appearances to be ranked

# Regression to the mean: each stat is pulled toward the league average by
# this many "phantom" PA of league-average performance. These are the PA at
# which the stat becomes ~50% signal / 50% noise (Russell Carleton's
# stabilization research): OBP ~460 PA, HR rate ~170 PA.
OBP_STABILIZE_PA = 460
HR_STABILIZE_PA = 170

# Recent form gets at most this share of the OBP estimate, scaled down when
# the player has fewer than RECENT_FULL_PA plate appearances in the window.
RECENT_DAYS = 14
RECENT_WEIGHT = 0.25
RECENT_FULL_PA = 50

CATCHER_START_RATE = 0.60  # catchers start ~60% of team games
REST_DAYS_PER_WEEK = 1     # other regulars sit about once a week


# ─────────────────────────────────────────
# API HELPERS
# ─────────────────────────────────────────
def get_json(url, params=None):
    """GET with a timeout and one retry."""
    for attempt in (1, 2):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                raise
            print(f"  Request failed ({e}) — retrying...")


def get_all_splits(params):
    """Pull every page of a /stats query (the API caps each page)."""
    splits = []
    page_size = 500
    offset = 0
    while True:
        data = get_json(f"{API}/stats", {**params, 'limit': page_size, 'offset': offset})
        block = data.get('stats', [{}])[0]
        page = block.get('splits', [])
        splits.extend(page)
        total = block.get('totalSplits')
        offset += page_size
        if not page or len(page) < page_size or (total is not None and len(splits) >= total):
            break
    return splits


# ─────────────────────────────────────────
# STAT HELPERS
# ─────────────────────────────────────────
COUNT_FIELDS = ['atBats', 'hits', 'homeRuns', 'baseOnBalls', 'hitByPitch',
                'sacFlies', 'plateAppearances', 'gamesPlayed']


def counting_stats(stat):
    c = {f: int(stat.get(f, 0) or 0) for f in COUNT_FIELDS}
    # Fall back to a computed PA if the API omits it
    if c['plateAppearances'] == 0:
        c['plateAppearances'] = c['atBats'] + c['baseOnBalls'] + c['hitByPitch'] + c['sacFlies']
    return c


def stats_by_player(splits):
    """One row of counting stats per player.

    Players traded mid-season can come back as one split per team, sometimes
    plus a combined split with no team attached. Use the combined split when
    present, otherwise add the per-team splits together.
    """
    grouped = {}
    for split in splits:
        grouped.setdefault(split['player']['id'], []).append(split)

    players = {}
    for player_id, rows in grouped.items():
        combined = [r for r in rows if 'team' not in r]
        use = combined[:1] if combined else rows
        totals = {f: 0 for f in COUNT_FIELDS}
        for r in use:
            for f, v in counting_stats(r['stat']).items():
                totals[f] += v
        first = rows[0]
        totals['name'] = first['player']['fullName']
        totals['position'] = first.get('position', {}).get('abbreviation', '')
        players[player_id] = totals
    return players


def on_base(s):
    return s['hits'] + s['baseOnBalls'] + s['hitByPitch']


def obp_denominator(s):
    # Official OBP denominator: AB + BB + HBP + SF
    return s['atBats'] + s['baseOnBalls'] + s['hitByPitch'] + s['sacFlies']


def zscore(series):
    std = series.std(ddof=0)
    return (series - series.mean()) / std if std > 0 else series * 0


# ─────────────────────────────────────────
# MAIN REPORT
# ─────────────────────────────────────────
def build_report(start_date):
    end_date = start_date + timedelta(days=6)
    recent_end = start_date - timedelta(days=1)
    recent_start = start_date - timedelta(days=RECENT_DAYS)
    season = start_date.year

    # ── Schedule: games per team this week (skip postponed/cancelled) ──
    schedule = get_json(f"{API}/schedule", {
        'sportId': 1, 'gameType': 'R',
        'startDate': start_date.isoformat(), 'endDate': end_date.isoformat(),
    })

    games_by_team = {}
    team_names = {}
    skipped = 0
    for date_entry in schedule.get('dates', []):
        for game in date_entry['games']:
            state = game.get('status', {}).get('detailedState', '')
            if state.startswith(('Postponed', 'Cancelled', 'Suspended')):
                skipped += 1
                continue
            for side in ('away', 'home'):
                team = game['teams'][side]['team']
                games_by_team[team['id']] = games_by_team.get(team['id'], 0) + 1
                team_names[team['id']] = team['name']

    print(f"Games this week: {sum(games_by_team.values()) // 2} "
          f"({skipped} postponed/cancelled skipped)")

    # ── Active rosters: drops IL players and gives each player's current team ──
    roster_params = {'rosterType': 'active'}
    if start_date <= date.today():
        roster_params['date'] = start_date.isoformat()

    current_team = {}
    roster_position = {}
    teams = get_json(f"{API}/teams", {'sportId': 1, 'season': season}).get('teams', [])
    for team in teams:
        team_names.setdefault(team['id'], team['name'])
        roster = get_json(f"{API}/teams/{team['id']}/roster", roster_params)
        for entry in roster.get('roster', []):
            current_team[entry['person']['id']] = team['id']
            roster_position[entry['person']['id']] = entry.get('position', {}).get('abbreviation', '')
    print(f"Players on active rosters: {len(current_team)}")

    # ── Season and recent stats (all pages) ──
    base_params = {'group': 'hitting', 'gameType': 'R', 'playerPool': 'All', 'season': season}
    season_splits = get_all_splits({**base_params, 'stats': 'byDateRange',
                                    'startDate': f"{season}-01-01",
                                    'endDate': recent_end.isoformat()})
    recent_splits = get_all_splits({**base_params, 'stats': 'byDateRange',
                                    'startDate': recent_start.isoformat(),
                                    'endDate': recent_end.isoformat()})
    season_stats = stats_by_player(season_splits)
    recent_stats = stats_by_player(recent_splits)
    print(f"Hitters with season stats: {len(season_stats)} | "
          f"last {RECENT_DAYS} days: {len(recent_stats)}")

    # ── League averages (all hitters) for regression to the mean ──
    lg_obp = sum(on_base(s) for s in season_stats.values()) / \
        max(1, sum(obp_denominator(s) for s in season_stats.values()))
    lg_hr_rate = sum(s['homeRuns'] for s in season_stats.values()) / \
        max(1, sum(s['plateAppearances'] for s in season_stats.values()))
    print(f"League OBP: {lg_obp:.3f} | League HR/PA: {lg_hr_rate:.4f}")

    # ── Build infielder table ──
    rows = []
    for player_id, s in season_stats.items():
        if player_id not in current_team:       # injured, minors, or released
            continue
        position = roster_position.get(player_id) or s['position']
        if position not in INFIELD_POSITIONS:
            continue
        if s['plateAppearances'] < MIN_PA:
            continue

        denom = obp_denominator(s)
        obp = on_base(s) / denom if denom else 0
        hr_rate = s['homeRuns'] / s['plateAppearances']

        # Regress season numbers toward league average
        obp_reg = (on_base(s) + OBP_STABILIZE_PA * lg_obp) / (denom + OBP_STABILIZE_PA)
        hr_reg = (s['homeRuns'] + HR_STABILIZE_PA * lg_hr_rate) / \
            (s['plateAppearances'] + HR_STABILIZE_PA)

        # Blend in recent form, weighted by how much recent data there is
        r = recent_stats.get(player_id)
        recent_pa = r['plateAppearances'] if r else 0
        recent_obp = on_base(r) / obp_denominator(r) if r and obp_denominator(r) else None
        w = RECENT_WEIGHT * min(1, recent_pa / RECENT_FULL_PA) if recent_obp is not None else 0
        obp_est = obp_reg * (1 - w) + (recent_obp or 0) * w

        team_id = current_team[player_id]
        games = games_by_team.get(team_id, 0)
        if position == 'C':
            expected_starts = games * CATCHER_START_RATE
        else:
            expected_starts = max(0, games - REST_DAYS_PER_WEEK)

        rows.append({
            'name': s['name'], 'position': position, 'team': team_names.get(team_id, ''),
            'plate_appearances': s['plateAppearances'], 'hr': s['homeRuns'],
            'obp': obp, 'hr_rate': hr_rate,
            'recent_pa': recent_pa, 'recent_obp': recent_obp,
            'obp_est': obp_est, 'hr_rate_est': hr_reg,
            'games_this_week': games, 'expected_starts': expected_starts,
        })

    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No infielders found — check the dates and API responses.")

    # ── Weekly score: weighted z-scores, rescaled so 50 = average infielder ──
    df['z_obp'] = zscore(df['obp_est'])
    df['z_hr'] = zscore(df['hr_rate_est'])
    df['z_starts'] = zscore(df['expected_starts'])
    weighted = (WEIGHTS['obp'] * df['z_obp'] +
                WEIGHTS['hr_rate'] * df['z_hr'] +
                WEIGHTS['starts'] * df['z_starts'])
    df['weekly_score'] = 50 + 10 * weighted
    return df.sort_values('weekly_score', ascending=False).reset_index(drop=True)


# ─────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────
def print_report(df, label):
    print(f"\nTop 10 Infielders — {label}")
    print(f"  {'Name':<23} {'Pos':<5} {'Team':<25} {'OBP':<6} {'HR':<4} {'Games':<7} {'Score'}")
    print("-" * 85)
    for _, row in df.head(10).iterrows():
        print(f"  {row['name']:<23} {row['position']:<5} {row['team']:<25} "
              f"{row['obp']:.3f}  {row['hr']:<4} {int(row['games_this_week']):<7} {row['weekly_score']:.1f}")

    print("\n" + "=" * 60)
    print(f"TOP 5 BY POSITION — {label}")
    print("=" * 60)
    for pos in INFIELD_POSITIONS:
        pos_df = df[df['position'] == pos].head(5)
        print(f"\n--- {pos} ---")
        print(f"  {'Name':<25} {'Team':<25} {'OBP':<6} {'HR':<4} {'Games':<7} {'Score'}")
        print(f"  {'-'*70}")
        for _, row in pos_df.iterrows():
            print(f"  {row['name']:<25} {row['team']:<25} {row['obp']:.3f}  "
                  f"{row['hr']:<4} {int(row['games_this_week']):<7} {row['weekly_score']:.1f}")


def save_csv(df, path):
    cols = ['name', 'position', 'team', 'plate_appearances', 'obp', 'hr', 'hr_rate',
            'recent_pa', 'recent_obp', 'obp_est', 'hr_rate_est',
            'games_this_week', 'expected_starts', 'weekly_score']
    df[cols].round(4).to_csv(path, index=False)
    print(f"\nReport saved: {path}")


def save_chart(df, label, path, show=False):
    import matplotlib.pyplot as plt

    colors = {'C': '#2E75B6', '1B': '#E74C3C', '2B': '#27AE60', '3B': '#F39C12', 'SS': '#8E44AD'}

    fig, axes = plt.subplots(1, 5, figsize=(20, 8))
    fig.suptitle(
        f'Top 5 Infielders by Position — {label}\n'
        'Score: 50% OBP + 30% HR rate + 20% expected starts (z-scored; 50 = average infielder)',
        fontsize=13, fontweight='bold', y=1.02
    )
    x_max = df['weekly_score'].max() + 5

    for ax, pos in zip(axes, INFIELD_POSITIONS):
        pos_df = df[df['position'] == pos].head(5).sort_values('weekly_score')
        bars = ax.barh(pos_df['name'], pos_df['weekly_score'],
                       color=colors[pos], alpha=0.85, edgecolor='white', linewidth=0.5)

        for bar, score in zip(bars, pos_df['weekly_score']):
            ax.text(bar.get_width() - 0.5, bar.get_y() + bar.get_height() / 2, f'{score:.1f}',
                    va='center', ha='right', fontsize=8, color='white', fontweight='bold')

        for i, (_, row) in enumerate(pos_df.iterrows()):
            ax.text(0.5, i, f"{int(row['games_this_week'])}G",
                    va='center', ha='left', fontsize=7, color='white', alpha=0.9)

        ax.set_title(f'--- {pos} ---', fontweight='bold', color=colors[pos], fontsize=12)
        ax.set_xlabel('Weekly Score', fontsize=9)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='y', labelsize=8)
        ax.set_xlim(0, x_max)

    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Chart saved: {path}")
    if show:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Weekly MLB infielder rankings")
    parser.add_argument('--start', help="Week start date YYYY-MM-DD (default: this Monday)")
    parser.add_argument('--out-dir', default='.', help="Folder for the CSV and chart")
    parser.add_argument('--show', action='store_true', help="Open the chart window")
    args = parser.parse_args()

    if args.start:
        start_date = datetime.strptime(args.start, '%Y-%m-%d').date()
    else:
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    label = f"Week of {start_date:%b} {start_date.day} to {end_date:%b} {end_date.day}, {end_date.year}"

    print(f"\nInfield Analysis — {label}")
    print("=" * 60)

    df = build_report(start_date)
    print(f"\nRanked infielders: {len(df)}")
    print(df.groupby('position').size().to_string())
    print_report(df, label)

    os.makedirs(args.out_dir, exist_ok=True)
    stem = f"infield_rankings_{start_date.isoformat()}_{end_date.isoformat()}"
    save_csv(df, os.path.join(args.out_dir, f"{stem}.csv"))
    save_chart(df, label, os.path.join(args.out_dir, f"{stem}.png"), show=args.show)


if __name__ == '__main__':
    main()
