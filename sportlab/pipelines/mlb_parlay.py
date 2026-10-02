"""Joint evaluation of exact MLB markets from shared game-level draws."""

from __future__ import annotations

import numpy as np

from sportlab.pipelines.mlb_pregame import simulate_mlb_game_draws
from sportlab.types import MLBGameInput


def _outcome(draws: dict, selection: dict) -> np.ndarray:
    market = selection["market"]
    if market == "home_ml":
        return draws["home_wins"].astype(np.int8)
    if market == "away_ml":
        return (~draws["home_wins"]).astype(np.int8)
    source = {
        "game_total": "totals", "away_team_total": "away_runs", "home_team_total": "home_runs",
        "away_pitcher_ks": "away_ks", "home_pitcher_ks": "home_ks",
    }
    if market == "hitter_hits":
        player_id = str(selection["player_id"])
        if player_id not in draws["hitter_hits"]:
            raise ValueError(f"hitter {player_id} has no confirmed-lineup hits distribution")
        values = draws["hitter_hits"][player_id]
    elif market in source:
        values = draws[source[market]]
        if values is None:
            raise ValueError(f"{market} is not estimable for this game")
    else:
        raise ValueError(f"unsupported market: {market}")
    direction = selection["side"]
    if direction not in ("over", "under"):
        raise ValueError("side must be over or under")
    line = float(selection["line"])
    wins = values > line if direction == "over" else values < line
    push = values == line if line.is_integer() else np.zeros(len(values), dtype=bool)
    return np.where(push, -1, wins.astype(np.int8))


def simulate_mlb_parlay(games: list[MLBGameInput], selections: list[dict],
                        simulations: int = 10_000, seed: int = 20261002) -> dict:
    """Report 13/13-style joint wins, pushes and each leg separately.

    Same-game side/team/game totals share their run draws. Pitcher K and hitter
    hit draws are currently independent of scoring, and games are independent.
    The returned rate is exploratory until those dependencies are calibrated.
    """
    if simulations < 1 or not selections:
        raise ValueError("simulations and selections must be positive")
    by_id = {g.event_id: g for g in games}
    if len(by_id) != len(games) or None in by_id:
        raise ValueError("each game requires a unique event_id")
    draws = {eid: simulate_mlb_game_draws(game, simulations, seed) for eid, game in by_id.items()}
    legs = []
    for leg in selections:
        event_id = leg["event_id"]
        if event_id not in draws:
            raise ValueError(f"event {event_id} absent from supplied games")
        legs.append(_outcome(draws[event_id], leg))
    matrix = np.stack(legs)
    all_wins = np.all(matrix == 1, axis=0)
    no_losses = np.all(matrix != 0, axis=0)
    push_no_loss = no_losses & ~all_wins
    return {"model_status": "EXPLORATORY_UNCALIBRATED", "simulations": simulations, "seed": seed,
            "full_win_count": int(np.sum(all_wins)),
            "full_win_per_1000": round(1000 * float(np.mean(all_wins)), 1),
            "push_no_loss_count": int(np.sum(push_no_loss)),
            "at_least_one_loss_count": int(np.sum(~no_losses)),
            "legs": [{"selection": leg, "win_pct": round(100 * float(np.mean(out == 1)), 2),
                      "push_pct": round(100 * float(np.mean(out == -1)), 2),
                      "loss_pct": round(100 * float(np.mean(out == 0)), 2)}
                     for leg, out in zip(selections, legs)],
            "assumptions": ["same-game ML, team total and game total share run draws",
                            "pitcher Ks and hitter hits independent of run scoring",
                            "different games independent", "extra innings approximated"]}
