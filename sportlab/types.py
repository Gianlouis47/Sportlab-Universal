from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass(frozen=True)
class WindowForm:
    games: int
    offense: float
    defense_allowed: float
    win_rate: float | None = None

@dataclass(frozen=True)
class TeamProfile:
    code: str
    season_offense: float
    season_defense_allowed: float
    venue_offense: float | None = None
    venue_defense_allowed: float | None = None
    l5: WindowForm | None = None
    l10: WindowForm | None = None
    l20: WindowForm | None = None
    l30: WindowForm | None = None

@dataclass(frozen=True)
class PitcherProfile:
    name: str
    season_era: float | None = None
    recent_era: float | None = None
    opponent_era: float | None = None
    season_k_per_9: float | None = None
    recent_k_per_9: float | None = None
    opponent_k_per_9: float | None = None
    expected_ip: float = 5.5
    expected_bf: float | None = None
    opponent_k_factor: float = 1.0
    workload_factor: float = 1.0
    # Optional observed inputs for the BF-based strikeout simulation.
    season_k_rate: float | None = None  # strikeouts / batters faced
    opponent_k_rate: float | None = None  # opposing hitters' strikeouts / PA
    league_k_rate: float | None = None
    bf_samples: tuple[int, ...] = ()  # starts only, never relief appearances

@dataclass(frozen=True)
class H2HProfile:
    games: int
    away_runs_per_game: float
    home_runs_per_game: float

@dataclass(frozen=True)
class MLBGameInput:
    event_id: int | None
    away: TeamProfile
    home: TeamProfile
    away_pitcher: PitcherProfile
    home_pitcher: PitcherProfile
    h2h: H2HProfile | None = None
    total_lines: tuple[float, ...] = (6.5, 7.0, 7.5, 8.0, 8.5)
    away_team_total_lines: tuple[float, ...] = (2.5, 3.5, 4.5)
    home_team_total_lines: tuple[float, ...] = (2.5, 3.5, 4.5)
    away_pitcher_k_lines: tuple[float, ...] = (4.5, 5.0, 5.5, 6.0, 6.5)
    home_pitcher_k_lines: tuple[float, ...] = (4.5, 5.0, 5.5, 6.0, 6.5)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class SimulationResult:
    model_version: str
    simulations: int
    seed: int
    expected_away_runs: float
    expected_home_runs: float
    away_win: float
    home_win: float
    total_markets: dict[str, dict[str, float]]
    away_team_totals: dict[str, dict[str, float]]
    home_team_totals: dict[str, dict[str, float]]
    away_pitcher_ks: dict[str, dict[str, float]]
    home_pitcher_ks: dict[str, dict[str, float]]
    contradictions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
