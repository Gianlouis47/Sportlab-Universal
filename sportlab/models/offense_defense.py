from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class TeamRates:
    """Rates per game in one sport and one comparable measurement unit."""
    offense: float
    allowed: float

    def __post_init__(self) -> None:
        if any(not isfinite(value) or value < 0 for value in (self.offense, self.allowed)):
            raise ValueError("offense and allowed must be finite, non-negative rates")


@dataclass(frozen=True)
class MatchupBaseline:
    away: float
    home: float
    total: float


def matchup_baseline(away: TeamRates, home: TeamRates) -> MatchupBaseline:
    """Notebook baseline: each attack against the opposing defense.

    This is a deterministic projection, not a simulation or a betting decision.
    Both teams must use the same unit (goals, points or runs per game).
    """
    away_expected = (away.offense + home.allowed) / 2
    home_expected = (home.offense + away.allowed) / 2
    return MatchupBaseline(
        away=away_expected,
        home=home_expected,
        total=away_expected + home_expected,
    )
