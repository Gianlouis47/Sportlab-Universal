from __future__ import annotations
from statistics import mean
from sportlab.models.recent_form import recent_blend
from sportlab.types import H2HProfile, PitcherProfile, TeamProfile

def _available_mean(values: list[float | None], fallback: float) -> float:
    clean = [float(v) for v in values if v is not None]
    return mean(clean) if clean else fallback

def pitcher_run_factor(pitcher: PitcherProfile, league_era: float = 4.25) -> float:
    era = _available_mean([pitcher.season_era, pitcher.recent_era, pitcher.opponent_era], league_era)
    return min(1.35, max(0.70, era / league_era))

def project_expected_runs(away: TeamProfile, home: TeamProfile, away_pitcher: PitcherProfile, home_pitcher: PitcherProfile, h2h: H2HProfile | None = None) -> tuple[float, float, list[str]]:
    away_recent_off, away_recent_def = recent_blend(away)
    home_recent_off, home_recent_def = recent_blend(home)
    away_season = (away.season_offense + home.season_defense_allowed) / 2
    home_season = (home.season_offense + away.season_defense_allowed) / 2
    away_recent = (away_recent_off + home_recent_def) / 2
    home_recent = (home_recent_off + away_recent_def) / 2
    away_venue = ((away.venue_offense or away.season_offense) + (home.venue_defense_allowed or home.season_defense_allowed)) / 2
    home_venue = ((home.venue_offense or home.season_offense) + (away.venue_defense_allowed or away.season_defense_allowed)) / 2
    if h2h and h2h.games >= 2:
        away_h2h = h2h.away_runs_per_game
        home_h2h = h2h.home_runs_per_game
        h2h_w = 0.08 if h2h.games >= 5 else 0.04
    else:
        away_h2h, home_h2h, h2h_w = away_season, home_season, 0.0
    away_starter_component = away_season * pitcher_run_factor(home_pitcher)
    home_starter_component = home_season * pitcher_run_factor(away_pitcher)
    base_weights = {"season": 0.30, "recent": 0.30, "venue": 0.15, "starter": 0.17}
    remaining = 1.0 - h2h_w
    scale = remaining / sum(base_weights.values())
    w = {k: v * scale for k, v in base_weights.items()}
    away_mu = w["season"]*away_season + w["recent"]*away_recent + w["venue"]*away_venue + w["starter"]*away_starter_component + h2h_w*away_h2h
    home_mu = w["season"]*home_season + w["recent"]*home_recent + w["venue"]*home_venue + w["starter"]*home_starter_component + h2h_w*home_h2h
    contradictions = []
    if abs(away_recent_off - away.season_offense) >= 1.5:
        contradictions.append(f"{away.code}: recent offense materially differs from season baseline")
    if abs(home_recent_off - home.season_offense) >= 1.5:
        contradictions.append(f"{home.code}: recent offense materially differs from season baseline")
    if h2h and h2h.games < 5:
        contradictions.append("H2H sample is small and receives reduced weight")
    return max(0.35, away_mu), max(0.35, home_mu), contradictions
