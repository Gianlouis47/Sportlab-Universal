from sportlab.models.offense_defense import MatchupBaseline, TeamRates, matchup_baseline


def projected_goals(away: TeamRates, home: TeamRates) -> MatchupBaseline:
    """xG/xGA per match baseline when rates are expected goals, else goals baseline."""
    return matchup_baseline(away, home)
