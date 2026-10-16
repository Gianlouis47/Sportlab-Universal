from __future__ import annotations
from dataclasses import dataclass
from math import erf, sqrt

def percentile_from_z(z: float) -> float:
    pct = 50.0 * (1.0 + erf(z / sqrt(2.0)))
    return max(1.0, min(100.0, pct))

def league_percentile(value: float, league_mean: float, league_std: float, higher_is_better: bool = True) -> float:
    if league_std <= 0:
        return 50.0
    z = (value - league_mean) / league_std
    if not higher_is_better:
        z = -z
    return percentile_from_z(z)

def display_1_to_10(rating_1_to_100: float) -> float:
    return round(max(1.0, min(100.0, rating_1_to_100)) / 10.0, 1)

@dataclass(frozen=True)
class MLBTeamRatings:
    offense: float
    run_prevention: float
    contact: float | None = None
    power: float | None = None
    plate_discipline: float | None = None
    baserunning_speed: float | None = None
    stolen_base_pressure: float | None = None
    outfield_range: float | None = None
    infield_range: float | None = None
    defensive_conversion: float | None = None
    bullpen: float | None = None

@dataclass(frozen=True)
class PitcherStyle:
    strikeout_orientation: float
    label: str

def classify_pitcher_style(k_pct_rating: float, whiff_rating: float | None = None, csw_rating: float | None = None) -> PitcherStyle:
    parts = [(k_pct_rating, 0.55)]
    if whiff_rating is not None:
        parts.append((whiff_rating, 0.30))
    if csw_rating is not None:
        parts.append((csw_rating, 0.15))
    denom = sum(w for _, w in parts)
    score = sum(v*w for v,w in parts) / denom
    if score >= 67:
        label = "STRIKEOUT"
    elif score <= 40:
        label = "CONTACT"
    else:
        label = "HYBRID"
    return PitcherStyle(strikeout_orientation=round(score,2), label=label)
