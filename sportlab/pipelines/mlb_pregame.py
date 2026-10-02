from __future__ import annotations
import numpy as np
from sportlab.simulations.monte_carlo import count_distribution, gamma_poisson_counts, hitter_hits_counts, line_probabilities, poisson_counts, strikeout_counts_from_bf
from sportlab.sports.mlb.runs import project_expected_runs
from sportlab.sports.mlb.strikeouts import project_pitcher_k_mean
from sportlab.types import MLBGameInput, SimulationResult

MODEL_VERSION = "sportlab_mlb_v1_bf_hitter_optional"

def _simulate_pitcher_ks(rng: np.random.Generator, p, n: int) -> np.ndarray | None:
    if p.bf_samples and all(x is not None for x in (p.season_k_rate, p.opponent_k_rate, p.league_k_rate)):
        return strikeout_counts_from_bf(rng, p.bf_samples, p.season_k_rate, p.opponent_k_rate, p.league_k_rate, n)
    mean = project_pitcher_k_mean(p)
    return poisson_counts(rng, mean, n) if mean is not None else None

def simulate_mlb_game_draws(game: MLBGameInput, simulations: int = 10_000, seed: int = 20260930):
    """Return one joint sample per simulated game for side and total markets.

    Pitcher K and hitter hits are sampled independently of run scoring in this
    exploratory model; same-game parlays involving them need that caveat.
    """
    away_mu, home_mu, contradictions = project_expected_runs(game.away, game.home, game.away_pitcher, game.home_pitcher, game.h2h)
    for side, pitcher in (("away", game.away_pitcher), ("home", game.home_pitcher)):
        if pitcher.name == "UNAVAILABLE":
            contradictions.append(f"{side} starter unavailable; run model uses league-average fallback")
        elif game.metadata.get(f"{side}_starter_sample", 10) < 10:
            contradictions.append(f"{side} starter has fewer than 10 starts; K market is not estimated")
    rng = np.random.default_rng(seed + (game.event_id or 0))
    away_runs = gamma_poisson_counts(rng, away_mu, simulations)
    home_runs = gamma_poisson_counts(rng, home_mu, simulations)
    # Simplified extra innings: sample both offenses until the tie breaks.
    # The +0.25 run per team is a scenario proxy for the automatic runner;
    # it is uncalibrated and must be disclosed for full-game totals.
    for _ in range(20):
        ties = away_runs == home_runs
        if not np.any(ties):
            break
        count = int(np.count_nonzero(ties))
        away_runs[ties] += rng.poisson(away_mu / 9 + .25, count)
        home_runs[ties] += rng.poisson(home_mu / 9 + .25, count)
    ties = away_runs == home_runs
    if np.any(ties):
        home_runs[ties] += rng.random(np.count_nonzero(ties)) < .5
        away_runs[away_runs == home_runs] += 1
    home_wins = home_runs > away_runs
    totals = away_runs + home_runs
    away_ks = _simulate_pitcher_ks(rng, game.away_pitcher, simulations)
    home_ks = _simulate_pitcher_ks(rng, game.home_pitcher, simulations)
    hits = {}
    for hitter in game.hitters:
        if hitter.lineup_status == "CONFIRMED":
            hits[str(hitter.player_id)] = hitter_hits_counts(rng, hitter.hits, hitter.at_bats,
                                                             hitter.ab_samples, simulations)
        else:
            contradictions.append(f"{hitter.name}: hitter hits not estimated without confirmed lineup")
    return {"away_runs": away_runs, "home_runs": home_runs, "totals": totals,
            "home_wins": home_wins, "away_ks": away_ks, "home_ks": home_ks,
            "hitter_hits": hits, "contradictions": contradictions}

def analyze_mlb_game(game: MLBGameInput, simulations: int = 10_000, seed: int = 20260930) -> SimulationResult:
    draws = simulate_mlb_game_draws(game, simulations, seed)
    away_runs, home_runs, totals = draws["away_runs"], draws["home_runs"], draws["totals"]
    away_ks, home_ks = draws["away_ks"], draws["home_ks"]
    hitter_markets = {pid: line_probabilities(samples, game.hitter_hit_lines.get(int(pid), (0.5, 1.5)))
                      for pid, samples in draws["hitter_hits"].items()}
    distributions = {"away_runs": count_distribution(away_runs), "home_runs": count_distribution(home_runs),
                     "total_runs": count_distribution(totals)}
    if away_ks is not None:
        distributions["away_pitcher_ks"] = count_distribution(away_ks)
    if home_ks is not None:
        distributions["home_pitcher_ks"] = count_distribution(home_ks)
    for pid, samples in draws["hitter_hits"].items():
        distributions[f"hitter_{pid}_hits"] = count_distribution(samples)
    return SimulationResult(
        model_version=MODEL_VERSION,
        simulations=simulations,
        seed=seed,
        expected_away_runs=float(np.mean(away_runs)),
        expected_home_runs=float(np.mean(home_runs)),
        away_win=float(np.mean(~draws["home_wins"])),
        home_win=float(np.mean(draws["home_wins"])),
        total_markets=line_probabilities(totals, game.total_lines),
        away_team_totals=line_probabilities(away_runs, game.away_team_total_lines),
        home_team_totals=line_probabilities(home_runs, game.home_team_total_lines),
        away_pitcher_ks=line_probabilities(away_ks, game.away_pitcher_k_lines) if away_ks is not None else {},
        home_pitcher_ks=line_probabilities(home_ks, game.home_pitcher_k_lines) if home_ks is not None else {},
        distributions=distributions,
        hitter_hits=hitter_markets,
        contradictions=draws["contradictions"],
    )
