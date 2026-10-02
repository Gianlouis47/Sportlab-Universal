from dataclasses import replace

from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_parlay import simulate_mlb_parlay
from sportlab.pipelines.mlb_pregame import analyze_mlb_game
from sportlab.types import HitterProfile


def test_same_game_parlay_is_joint_and_reproducible():
    game = load_mlb_game("examples/mlb_game.json")
    legs = [{"event_id": game.event_id, "market": "home_ml"},
            {"event_id": game.event_id, "market": "home_team_total", "side": "over", "line": 2.5}]
    result = simulate_mlb_parlay([game], legs, simulations=2000, seed=7)
    repeat = simulate_mlb_parlay([game], legs, simulations=2000, seed=7)
    assert result == repeat
    assert result["full_win_count"] <= min(round(x["win_pct"] * 20) for x in result["legs"]) + 1
    assert result["full_win_count"] + result["push_no_loss_count"] + result["at_least_one_loss_count"] == 2000


def test_unconfirmed_hitter_is_not_simulated():
    game = load_mlb_game("examples/mlb_game.json")
    hitter = HitterProfile(660271, "Example hitter", 100, 400, (3, 4, 5), "PROJECTED")
    game = replace(game, hitters=(hitter,))
    result = analyze_mlb_game(game, simulations=500, seed=7)
    assert result.hitter_hits == {}
    assert any("without confirmed lineup" in note for note in result.contradictions)
