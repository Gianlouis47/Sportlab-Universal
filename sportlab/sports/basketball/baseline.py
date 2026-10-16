from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from sportlab.models.offense_defense import MatchupBaseline, TeamRates, matchup_baseline


def projected_points(away: TeamRates, home: TeamRates) -> MatchupBaseline:
    """Team points scored/allowed per game; pace/lineup effects are not assumed."""
    return matchup_baseline(away, home)


@dataclass(frozen=True)
class PlayerPerMinute:
    points: float
    rebounds: float
    assists: float
    steals: float

    def __post_init__(self) -> None:
        if any(not isfinite(value) or value < 0 for value in (
            self.points, self.rebounds, self.assists, self.steals
        )):
            raise ValueError("per-minute rates must be finite and non-negative")


def projected_player_box_score(rates: PlayerPerMinute, expected_minutes: float) -> dict[str, float]:
    """Minutes-based means only; no distributions or independent prop picks."""
    if not isfinite(expected_minutes) or expected_minutes < 0:
        raise ValueError("expected_minutes must be finite and non-negative")
    return {
        "points": rates.points * expected_minutes,
        "rebounds": rates.rebounds * expected_minutes,
        "assists": rates.assists * expected_minutes,
        "steals": rates.steals * expected_minutes,
    }
