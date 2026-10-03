from __future__ import annotations
import numpy as np
from sportlab.simulations.monte_carlo import count_distribution, gamma_poisson_counts, hitter_hit_and_bases_counts, hitter_hits_counts, line_probabilities, poisson_counts, strikeout_counts_from_bf
from sportlab.sports.mlb.hits import expected_team_hits, pooled_hit_dispersion
from sportlab.sports.mlb.runs import project_expected_runs
from sportlab.sports.mlb.strikeouts import project_pitcher_k_mean
from sportlab.types import MLBGameInput, SimulationResult

MODEL_VERSION = "sportlab_mlb_v1_bf_hitter_optional"

def _simulate_pitcher_ks(rng: np.random.Generator, p, n: int) -> np.ndarray | None:
    if p.bf_samples and all(x is not None for x in (p.season_k_rate, p.opponent_k_rate, p.league_k_rate)):
        return strikeout_counts_from_bf(rng, p.bf_samples, p.season_k_rate, p.opponent_k_rate, p.league_k_rate, n)
    mean = project_pitcher_k_mean(p)
    return poisson_counts(rng, mean, n) if mean is not None else None

def _simulate_pitcher_hits_allowed(rng: np.random.Generator, p, n: int) -> np.ndarray | None:
    if p.bf_samples and all(x is not None for x in
                            (p.season_hits_allowed_rate, p.opponent_hit_rate, p.league_hit_rate)):
        return strikeout_counts_from_bf(rng, p.bf_samples, p.season_hits_allowed_rate,
                                        p.opponent_hit_rate, p.league_hit_rate, n)
    return None

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
    away_pitcher_hits = _simulate_pitcher_hits_allowed(rng, game.away_pitcher, simulations)
    home_pitcher_hits = _simulate_pitcher_hits_allowed(rng, game.home_pitcher, simulations)
    hit_dispersion = pooled_hit_dispersion(game.away, game.home)
    away_hit_mu = expected_team_hits(game.away, game.home, game.home_pitcher)
    home_hit_mu = expected_team_hits(game.home, game.away, game.away_pitcher)
    away_team_hits = (gamma_poisson_counts(rng, away_hit_mu, simulations, hit_dispersion)
                      if away_hit_mu is not None and hit_dispersion is not None else None)
    home_team_hits = (gamma_poisson_counts(rng, home_hit_mu, simulations, hit_dispersion)
                      if home_hit_mu is not None and hit_dispersion is not None else None)
    hits = {}
    bases = {}
    for hitter in game.hitters:
        if hitter.lineup_status == "CONFIRMED":
            if hitter.total_base_probs:
                h, tb = hitter_hit_and_bases_counts(rng, hitter.ab_samples,
                                                    hitter.total_base_probs, simulations)
                hits[str(hitter.player_id)], bases[str(hitter.player_id)] = h, tb
            else:
                hits[str(hitter.player_id)] = hitter_hits_counts(rng, hitter.hits, hitter.at_bats,
                                                                 hitter.ab_samples, simulations)
        else:
            contradictions.append(f"{hitter.name}: hitter hits not estimated without confirmed lineup")
    return {"away_runs": away_runs, "home_runs": home_runs, "totals": totals,
            "home_wins": home_wins, "away_ks": away_ks, "home_ks": home_ks,
            "away_team_hits": away_team_hits, "home_team_hits": home_team_hits,
            "away_pitcher_hits_allowed": away_pitcher_hits,
            "home_pitcher_hits_allowed": home_pitcher_hits,
            "hitter_hits": hits, "hitter_total_bases": bases, "contradictions": contradictions}

def analyze_mlb_game(game: MLBGameInput, simulations: int = 10_000, seed: int = 20260930) -> SimulationResult:
    draws = simulate_mlb_game_draws(game, simulations, seed)
    away_runs, home_runs, totals = draws["away_runs"], draws["home_runs"], draws["totals"]
    away_ks, home_ks = draws["away_ks"], draws["home_ks"]
    hitter_markets = {pid: line_probabilities(samples, game.hitter_hit_lines.get(int(pid), (0.5, 1.5)))
                      for pid, samples in draws["hitter_hits"].items()}
    base_markets = {pid: line_probabilities(samples, game.hitter_total_base_lines.get(int(pid), (0.5, 1.5)))
                    for pid, samples in draws["hitter_total_bases"].items()}
    distributions = {"away_runs": count_distribution(away_runs), "home_runs": count_distribution(home_runs),
                     "total_runs": count_distribution(totals)}
    if away_ks is not None:
        distributions["away_pitcher_ks"] = count_distribution(away_ks)
    if home_ks is not None:
        distributions["home_pitcher_ks"] = count_distribution(home_ks)
    for pid, samples in draws["hitter_hits"].items():
        distributions[f"hitter_{pid}_hits"] = count_distribution(samples)
    for name in ("away_team_hits", "home_team_hits", "away_pitcher_hits_allowed", "home_pitcher_hits_allowed"):
        if draws[name] is not None:
            distributions[name] = count_distribution(draws[name])
    for pid, samples in draws["hitter_total_bases"].items():
        distributions[f"hitter_{pid}_total_bases"] = count_distribution(samples)
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
        hitter_total_bases=base_markets,
        away_team_hits=line_probabilities(draws["away_team_hits"], game.away_team_hit_lines)
        if draws["away_team_hits"] is not None else {},
        home_team_hits=line_probabilities(draws["home_team_hits"], game.home_team_hit_lines)
        if draws["home_team_hits"] is not None else {},
        away_pitcher_hits_allowed=line_probabilities(draws["away_pitcher_hits_allowed"], game.away_pitcher_hits_allowed_lines)
        if draws["away_pitcher_hits_allowed"] is not None else {},
        home_pitcher_hits_allowed=line_probabilities(draws["home_pitcher_hits_allowed"], game.home_pitcher_hits_allowed_lines)
        if draws["home_pitcher_hits_allowed"] is not None else {},
        contradictions=draws["contradictions"],
    )
