from dataclasses import replace

import numpy as np

from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_pregame import analyze_mlb_game
from sportlab.simulations.monte_carlo import strikeout_counts_from_bf
from sportlab.types import PitcherProfile


def test_shorter_start_reduces_k_over_rate():
    full = strikeout_counts_from_bf(np.random.default_rng(7), (24,), .30, .24, .22, 10_000)
    short = strikeout_counts_from_bf(np.random.default_rng(7), (9,), .30, .24, .22, 10_000)
    assert np.mean(full > 5.5) > np.mean(short > 5.5) + .45


def test_missing_pitcher_does_not_invent_k_probability():
    game = load_mlb_game("examples/mlb_game.json")
    game = replace(game, away_pitcher=PitcherProfile(name="UNAVAILABLE"))
    result = analyze_mlb_game(game, simulations=1000, seed=7)
    assert result.away_pitcher_ks == {}
    assert any("starter unavailable" in note for note in result.contradictions)
