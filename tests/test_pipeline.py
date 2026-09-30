from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_pregame import analyze_mlb_game

def test_example_pipeline_runs():
    game=load_mlb_game("examples/mlb_game.json")
    r=analyze_mlb_game(game,simulations=2000,seed=7)
    assert 0 <= r.away_win <= 1
    assert 0 <= r.home_win <= 1
    assert abs(r.away_win+r.home_win-1)<1e-9
    assert "6.5" in r.total_markets
    assert "3.5" in r.home_team_totals
    assert "6.5" in r.away_pitcher_ks
