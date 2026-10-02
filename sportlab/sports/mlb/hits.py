"""Exploratory MLB hit projections; lineups and bullpen effects remain external."""

from __future__ import annotations

from math import sqrt
from statistics import mean

from sportlab.types import PitcherProfile, TeamProfile


def expected_team_hits(offense: TeamProfile, defense: TeamProfile,
                       opposing_starter: PitcherProfile) -> float | None:
    if offense.season_hits_for is None or defense.season_hits_allowed is None:
        return None
    baseline = sqrt(offense.season_hits_for * defense.season_hits_allowed)
    h9 = opposing_starter.season_hits_per9
    if h9 is None or h9 <= 0 or defense.season_hits_allowed <= 0:
        return baseline
    share = min(.8, max(0.0, opposing_starter.expected_ip / 9))
    return baseline * (h9 / defense.season_hits_allowed) ** share


def pooled_hit_dispersion(away: TeamProfile, home: TeamProfile) -> float | None:
    samples = tuple(away.hit_game_samples) + tuple(home.hit_game_samples)
    if len(away.hit_game_samples) < 30 or len(home.hit_game_samples) < 30:
        return None
    avg = mean(samples)
    variance = mean((x - avg) ** 2 for x in samples)
    return min(.4, max(0.0, (variance - avg) / avg**2)) if avg > 0 else None
