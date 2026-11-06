from sportlab.models.offense_defense import MatchupBaseline, TeamRates, matchup_baseline


def projected_points(away: TeamRates, home: TeamRates) -> MatchupBaseline:
    """NFL/NCAAF point baseline; no QB, personnel or pace adjustment is implied."""
    return matchup_baseline(away, home)
