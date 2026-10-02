"""Replay exact Betcris yes-hit props under projected MLB starting lineups.

Usage: python -m tools.replay_hitter_yes > examples/betcris_mlb_2026_10_03/hitter_yes_replay.json
The estimated rates are exploratory and conditional on the player starting.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np

from sportlab.simulations.monte_carlo import hitter_hit_and_bases_counts


ROOT = Path(__file__).resolve().parents[1]
MARKETS = ROOT / "examples" / "betcris_mlb_2026_10_03"
SNAPSHOT = ROOT / "examples" / "mlb_stats_api_2026-10-03_asof_2026-10-02.json.gz"
SEED = 20261002
RUNS = 10_000


def odds_to_decimal(american: int) -> float:
    return 1 + (american / 100 if american > 0 else 100 / -american)


def _logit(probability: float) -> float:
    return float(np.log(probability / (1 - probability)))


def adjusted_probabilities(record: dict, mlb: dict) -> tuple[tuple[float, ...], dict]:
    probabilities = np.array(record["total_base_probs"], dtype=float)
    baseline_hit = 1 - probabilities[0]
    pid = record["opponent_pitcher_id"]
    pitcher = mlb["starters"].get(str(pid)) if pid else None
    league_rate = mlb["league_hit_rate"]
    if pitcher is None or len(pitcher["starts"]) < 10:
        return tuple(probabilities), {"pitcher_hit_rate": None,
                                      "pitcher_adjustment": "UNAVAILABLE_OR_FEWER_THAN_10_STARTS"}
    stat = pitcher["season"]
    # Shrink the pitcher's hits/BF to the league rate with a 200-BF prior.
    pitcher_rate = (stat["hits"] + 200 * league_rate) / (stat["battersFaced"] + 200)
    pitcher_hit = 1 / (1 + np.exp(-(_logit(baseline_hit) + _logit(pitcher_rate) - _logit(league_rate))))
    mixed_hit = .6 * pitcher_hit + .4 * baseline_hit
    probabilities[1:] *= mixed_hit / baseline_hit
    probabilities[0] = 1 - mixed_hit
    return tuple(probabilities), {"pitcher_hit_rate": round(pitcher_rate, 4),
                                  "pitcher_adjustment": "200_BF_SHRINKAGE_60_PERCENT_EXPOSURE"}


def main() -> None:
    with gzip.open(SNAPSHOT, "rt", encoding="utf-8") as file:
        mlb = json.load(file)
    with gzip.open(MARKETS / "hitter_yes_inputs.json.gz", "rt", encoding="utf-8") as file:
        source = json.load(file)
    players = []
    draws = {}
    short_draws = {}
    for player in source["players"]:
        if player["status"] != "PROJECTED_STARTER":
            players.append({"name": player["betcris_name"], "status": "NO_ESTIMABLE"})
            continue
        probs, pitcher_info = adjusted_probabilities(player, mlb)
        rng = np.random.default_rng(SEED + player["player_id"])
        hits, _ = hitter_hit_and_bases_counts(rng, tuple(player["ab_samples"]), probs, RUNS)
        rng_short = np.random.default_rng(SEED + player["player_id"] + 1)
        one_fewer_ab = tuple(max(0, ab - 1) for ab in player["ab_samples"])
        short_hits, _ = hitter_hit_and_bases_counts(rng_short, one_fewer_ab, probs, RUNS)
        key = player["game"] + ":" + str(player["player_id"])
        draws[key] = hits >= 1
        short_draws[key] = short_hits >= 1
        yes_odds = player["yes_hit_odds"]
        total_bases_odds = player["over_0_5_total_bases_odds"]
        best_odds = max(yes_odds, total_bases_odds) if total_bases_odds is not None else yes_odds
        rate = float(np.mean(hits >= 1))
        empirical = player["appearance_hit_yes_count"] / player["appearance_sample"]
        players.append({"game": player["game"], "name": player["mlb_name"], "player_id": player["player_id"],
                        "status": "PROJECTED_STARTER_NOT_OFFICIAL", "appearance_sample": player["appearance_sample"],
                        "empirical_hit_yes": round(empirical, 4), "model_hit_yes": round(rate, 4),
                        "one_fewer_ab_hit_yes": round(float(np.mean(short_hits >= 1)), 4),
                        "yes_hit_odds": yes_odds, "over_0_5_total_bases_odds": total_bases_odds,
                        "best_equivalent_odds": best_odds,
                        "best_equivalent_break_even": round(1 / odds_to_decimal(best_odds), 4),
                        "candidate_if_starts": bool(empirical >= .70 and rate >= .70),
                        **pitcher_info})
    # Players are in different games. This calculation still assumes their hit
    # outcomes and plate-appearance counts are independent across games.
    candidate_names = ("Jackson Chourio", "Chandler Simpson")
    selections = [next(p for p in players if p.get("name") == name) for name in candidate_names]
    keys = [p["game"] + ":" + str(p["player_id"]) for p in selections]
    parlay = {"selections": candidate_names, "independence_between_games": True,
              "full_win_count": int(np.sum(draws[keys[0]] & draws[keys[1]])),
              "one_fewer_ab_each_full_win_count": int(np.sum(short_draws[keys[0]] & short_draws[keys[1]])),
              "decimal_odds": round(float(np.prod([odds_to_decimal(p["best_equivalent_odds"]) for p in selections])), 4)}
    parlay["break_even"] = round(1 / parlay["decimal_odds"], 4)
    print(json.dumps({"source_as_of": source["as_of"], "lineup_status": "PROJECTED",
                      "model_status": "EXPLORATORY_UNCALIBRATED", "seed": SEED, "simulations": RUNS,
                      "assumptions": ["historical AB sample from 2026 appearances",
                                      "batter hit-type rates adjusted to pitcher hand",
                                      "pitcher hits/BF shrunk with 200 BF prior",
                                      "60% of AB assumed against probable starter",
                                      "pitcher adjustment omitted when fewer than 10 starts",
                                      "one fewer AB sensitivity for lineup-order changes"],
                      "players": players, "example_two_hit_parlay": parlay}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
