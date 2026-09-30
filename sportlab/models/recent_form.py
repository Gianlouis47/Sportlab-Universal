from __future__ import annotations
from sportlab.types import TeamProfile

def _band(total_n: float, total_prev: float, n: int, prev_n: int) -> float:
    games = n - prev_n
    if games <= 0:
        raise ValueError("window sizes must increase")
    return (total_n * n - total_prev * prev_n) / games

def non_overlapping_recent_bands(team: TeamProfile) -> dict[str, tuple[float, float]]:
    if team.l10 and team.l20 and team.l30:
        return {
            "last10": (team.l10.offense, team.l10.defense_allowed),
            "previous10": (
                _band(team.l20.offense, team.l10.offense, 20, 10),
                _band(team.l20.defense_allowed, team.l10.defense_allowed, 20, 10),
            ),
            "third10": (
                _band(team.l30.offense, team.l20.offense, 30, 20),
                _band(team.l30.defense_allowed, team.l20.defense_allowed, 30, 20),
            ),
        }
    if team.l10:
        return {"last10": (team.l10.offense, team.l10.defense_allowed)}
    if team.l5:
        return {"last5": (team.l5.offense, team.l5.defense_allowed)}
    return {"season": (team.season_offense, team.season_defense_allowed)}

def recent_blend(team: TeamProfile, weights: dict[str, float] | None = None) -> tuple[float, float]:
    bands = non_overlapping_recent_bands(team)
    default = {"last10": 0.50, "previous10": 0.30, "third10": 0.20, "last5": 1.0, "season": 1.0}
    weights = weights or default
    raw = [(k, *v, weights.get(k, 0.0)) for k, v in bands.items()]
    total_w = sum(x[3] for x in raw)
    if total_w <= 0:
        raise ValueError("recent weights sum to zero")
    offense = sum(off * w for _, off, _, w in raw) / total_w
    defense = sum(defn * w for _, _, defn, w in raw) / total_w
    return offense, defense
