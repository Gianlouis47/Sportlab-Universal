from dataclasses import replace

import numpy as np

from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_pregame import analyze_mlb_game
from sportlab.simulations.monte_carlo import hitter_hit_and_bases_counts
from sportlab.types import HitterProfile


def test_hit_and_half_total_base_are_same_event():
    hits, bases = hitter_hit_and_bases_counts(np.random.default_rng(7), (3, 4, 5),
                                              (.72, .19, .06, .01, .02), 10_000)
    assert np.array_equal(hits >= 1, bases >= 1)
    assert np.all(bases >= hits)


def test_no_team_hit_data_means_no_hit_market():
    game = load_mlb_game("examples/mlb_game.json")
    game = replace(game, away_team_hit_lines=(6.5,), home_pitcher_hits_allowed_lines=(3.5,))
    result = analyze_mlb_game(game, simulations=1000, seed=7)
    assert result.away_team_hits == {}
    assert result.home_pitcher_hits_allowed == {}


def test_unconfirmed_player_has_no_total_base_market():
    game = load_mlb_game("examples/mlb_game.json")
    hitter = HitterProfile(123, "Projected batter", 20, 100, (3, 4), "PROJECTED",
                           (.8, .15, .04, 0, .01))
    result = analyze_mlb_game(replace(game, hitters=(hitter,)), simulations=1000, seed=7)
    assert result.hitter_total_bases == {}
