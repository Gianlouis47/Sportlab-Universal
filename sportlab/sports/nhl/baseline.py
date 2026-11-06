from sportlab.models.offense_defense import MatchupBaseline, TeamRates, matchup_baseline


def projected_goals(away: TeamRates, home: TeamRates) -> MatchupBaseline:
    """Goals for/against baseline; goalie, xG, PP/PK and rest require separate inputs."""
    return matchup_baseline(away, home)
