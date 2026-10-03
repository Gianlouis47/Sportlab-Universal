"""Exploratory five-leg alternative-total and hitter-hit parlay replay.

Uses model sporting marginals, empirical same-game hit/total lift, and 10,000
joint outcome draws. It is a scenario comparison, not a calibrated forecast.
Usage: python -m tools.replay_five_leg
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from tools.replay_hitter_yes import odds_to_decimal


ROOT = Path(__file__).resolve().parents[1]
MARKETS = ROOT / "examples" / "betcris_mlb_2026_10_03"
RUNS = 10_000
SEED = 20261002


def pair_lift(row: dict) -> float:
    n = row["appearances"]
    return (row["both"] / n) / ((row["hit_games"] / n) * (row["over_5_5_games"] / n))


def pair_draw(rng: np.random.Generator, hit: float, total: float, lift: float) -> np.ndarray:
    joint = hit * total * lift
    if joint < max(0, hit + total - 1) or joint > min(hit, total):
        raise ValueError("empirical lift is incompatible with model marginals")
    pick = rng.random(RUNS)
    # Both occurs first. The other three outcomes complete the two marginals.
    return pick < joint


def main() -> None:
    game_model = json.loads((MARKETS / "model_replay.json").read_text())
    hitter_model = json.loads((MARKETS / "hitter_yes_replay.json").read_text())
    historical = json.loads((MARKETS / "hitter_total_historical_pairs.json").read_text())
    alternative_odds = json.loads((MARKETS / "full_game_alternatives_from_screenshots.json").read_text())
    hitters = {row["name"]: row for row in hitter_model["players"]}

    def scenario(reduced: bool) -> dict:
        rng = np.random.default_rng(SEED + (1 if reduced else 0))
        low = game_model["example_three_game_total_parlay_lower_scoring"]["leg_win_counts"]
        def over(game: str, index: int) -> float:
            return (low[index] / RUNS if reduced else
                    game_model["games"][game]["model"]["total_markets"]["5.5"]["over"])
        cws = rng.random(RUNS) < over("cws_cle", 0)
        simpson = hitters["Chandler Simpson"]
        chourio = hitters["Jackson Chourio"]
        tb = pair_draw(rng, simpson["one_fewer_ab_hit_yes"] if reduced else simpson["model_hit_yes"],
                       over("nyy_tb", 1), pair_lift(historical["players"]["Chandler Simpson"]))
        mil = pair_draw(rng, chourio["one_fewer_ab_hit_yes"] if reduced else chourio["model_hit_yes"],
                        over("sd_mil", 2), pair_lift(historical["players"]["Jackson Chourio"]))
        return {"full_win_count": int(np.sum(cws & tb & mil)),
                "win_per_1000": round(float(np.mean(cws & tb & mil) * 1000), 1),
                "assumption": "15% lower run means and one fewer AB per hitter" if reduced else
                              "base run and hitter models"}

    odds = [next(row["over"] for row in alternative_odds["games"][game] if row["line"] == 5.5)
            for game in ("cws_cle", "nyy_tb", "sd_mil")]
    odds += [hitters[name]["yes_hit_odds"] for name in ("Chandler Simpson", "Jackson Chourio")]
    decimal = float(np.prod([odds_to_decimal(odd) for odd in odds]))
    print(json.dumps({"status": "EXPLORATORY_UNCALIBRATED", "runs": RUNS, "seed": SEED,
                      "legs": ["CWS-CLE over 5.5", "NYY-TB over 5.5", "SD-MIL over 5.5",
                               "Chandler Simpson yes hit", "Jackson Chourio yes hit"],
                      "american_odds": odds, "combined_decimal_odds": round(decimal, 4),
                      "combined_break_even": round(1 / decimal, 4),
                      "same_game_pair_lifts": {name: round(pair_lift(row), 4)
                                               for name, row in historical["players"].items()},
                      "base": scenario(False), "lower_scoring_and_fewer_ab": scenario(True),
                      "different_games_independent": True}, indent=2))


if __name__ == "__main__":
    main()
