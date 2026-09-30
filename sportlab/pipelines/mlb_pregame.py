from __future__ import annotations
import numpy as np
from sportlab.simulations.monte_carlo import gamma_poisson_counts, line_probabilities, poisson_counts, win_probabilities
from sportlab.sports.mlb.runs import project_expected_runs
from sportlab.sports.mlb.strikeouts import project_pitcher_k_mean
from sportlab.types import MLBGameInput, SimulationResult

MODEL_VERSION = "sportlab_mlb_v1"

def analyze_mlb_game(game: MLBGameInput, simulations: int = 10_000, seed: int = 20260930) -> SimulationResult:
    away_mu, home_mu, contradictions = project_expected_runs(game.away, game.home, game.away_pitcher, game.home_pitcher, game.h2h)
    away_k_mu = project_pitcher_k_mean(game.away_pitcher)
    home_k_mu = project_pitcher_k_mean(game.home_pitcher)
    rng = np.random.default_rng(seed)
    away_runs = gamma_poisson_counts(rng, away_mu, simulations)
    home_runs = gamma_poisson_counts(rng, home_mu, simulations)
    away_win, home_win = win_probabilities(away_runs, home_runs, rng)
    totals = away_runs + home_runs
    away_ks = poisson_counts(rng, away_k_mu, simulations)
    home_ks = poisson_counts(rng, home_k_mu, simulations)
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
        away_pitcher_ks=line_probabilities(away_ks, game.away_pitcher_k_lines),
        home_pitcher_ks=line_probabilities(home_ks, game.home_pitcher_k_lines),
        contradictions=contradictions,
    )
