from __future__ import annotations
import numpy as np
from sportlab.simulations.monte_carlo import gamma_poisson_counts, line_probabilities, poisson_counts, strikeout_counts_from_bf, win_probabilities
from sportlab.sports.mlb.runs import project_expected_runs
from sportlab.sports.mlb.strikeouts import project_pitcher_k_mean
from sportlab.types import MLBGameInput, SimulationResult

MODEL_VERSION = "sportlab_mlb_v1_bf_optional"

def _simulate_pitcher_ks(rng: np.random.Generator, p, n: int) -> np.ndarray | None:
    if p.bf_samples and all(x is not None for x in (p.season_k_rate, p.opponent_k_rate, p.league_k_rate)):
        return strikeout_counts_from_bf(rng, p.bf_samples, p.season_k_rate, p.opponent_k_rate, p.league_k_rate, n)
    mean = project_pitcher_k_mean(p)
    return poisson_counts(rng, mean, n) if mean is not None else None

def analyze_mlb_game(game: MLBGameInput, simulations: int = 10_000, seed: int = 20260930) -> SimulationResult:
    away_mu, home_mu, contradictions = project_expected_runs(game.away, game.home, game.away_pitcher, game.home_pitcher, game.h2h)
    for side, pitcher in (("away", game.away_pitcher), ("home", game.home_pitcher)):
        if pitcher.name == "UNAVAILABLE":
            contradictions.append(f"{side} starter unavailable; run model uses league-average fallback")
        elif game.metadata.get(f"{side}_starter_sample", 10) < 10:
            contradictions.append(f"{side} starter has fewer than 10 starts; K market is not estimated")
    rng = np.random.default_rng(seed)
    away_runs = gamma_poisson_counts(rng, away_mu, simulations)
    home_runs = gamma_poisson_counts(rng, home_mu, simulations)
    away_win, home_win = win_probabilities(away_runs, home_runs, rng)
    totals = away_runs + home_runs
    away_ks = _simulate_pitcher_ks(rng, game.away_pitcher, simulations)
    home_ks = _simulate_pitcher_ks(rng, game.home_pitcher, simulations)
    return SimulationResult(
        model_version=MODEL_VERSION,
        simulations=simulations,
        seed=seed,
        expected_away_runs=float(np.mean(away_runs)),
        expected_home_runs=float(np.mean(home_runs)),
        away_win=away_win,
        home_win=home_win,
        total_markets=line_probabilities(totals, game.total_lines),
        away_team_totals=line_probabilities(away_runs, game.away_team_total_lines),
        home_team_totals=line_probabilities(home_runs, game.home_team_total_lines),
        away_pitcher_ks=line_probabilities(away_ks, game.away_pitcher_k_lines) if away_ks is not None else {},
        home_pitcher_ks=line_probabilities(home_ks, game.home_pitcher_k_lines) if home_ks is not None else {},
        contradictions=contradictions,
    )
