from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class RunBaseline:
    away_expected: float
    home_expected: float
    total_expected: float

def notebook_run_baseline(
    away_runs_scored_per_game: float,
    away_runs_allowed_per_game: float,
    home_runs_scored_per_game: float,
    home_runs_allowed_per_game: float,
) -> RunBaseline:
    away = (away_runs_scored_per_game + home_runs_allowed_per_game) / 2.0
    home = (home_runs_scored_per_game + away_runs_allowed_per_game) / 2.0
    return RunBaseline(away_expected=away, home_expected=home, total_expected=away+home)
