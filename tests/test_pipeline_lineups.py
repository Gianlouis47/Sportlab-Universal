from dataclasses import replace

from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_pregame import analyze_mlb_game
from sportlab.sports.mlb.matchups import BatterMatchup


def test_both_starters_use_opposing_lineup_and_actual_monte_carlo():
    game = load_mlb_game("examples/mlb_game.json")
    away_pitcher = replace(game.away_pitcher, pitcher_k_rate=.30)
    home_pitcher = replace(game.home_pitcher, pitcher_k_rate=.15)
    away_batters = tuple(BatterMatchup(expected_pa=3, strikeout_rate=.20) for _ in range(8))
    home_batters = tuple(BatterMatchup(expected_pa=3, strikeout_rate=.25) for _ in range(8))
    game = replace(game, away_pitcher=away_pitcher, home_pitcher=home_pitcher,
                   away_lineup=away_batters, home_lineup=home_batters)
    result = analyze_mlb_game(game, simulations=10_000, seed=12)
    assert result.simulations == 10_000
    assert abs(result.away_win + result.home_win - 1) < 1e-12
    assert result.away_pitcher_ks["6.5"]["over"] > result.home_pitcher_ks["5.5"]["over"]
    assert not any("lineup unavailable" in note for note in result.contradictions)


def test_example_explicitly_reports_missing_lineups():
    result = analyze_mlb_game(load_mlb_game("examples/mlb_game.json"), simulations=100, seed=1)
    assert sum("lineup unavailable" in note for note in result.contradictions) == 2
