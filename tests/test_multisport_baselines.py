import pytest

from sportlab.models.offense_defense import TeamRates, matchup_baseline
from sportlab.sports.basketball.baseline import PlayerPerMinute, projected_player_box_score
from sportlab.sports.football.baseline import projected_points as football_points
from sportlab.sports.nhl.baseline import projected_goals as hockey_goals
from sportlab.sports.soccer.baseline import projected_goals as soccer_goals


def test_notebook_matchup_uses_both_defenses():
    away, home = TeamRates(5, 4), TeamRates(4, 5)
    result = matchup_baseline(away, home)
    assert (result.away, result.home, result.total) == (5, 4, 9)


def test_sport_wrappers_keep_units_and_two_sided_baseline():
    away, home = TeamRates(3, 2), TeamRates(2, 4)
    for model in (hockey_goals, soccer_goals, football_points):
        assert model(away, home).total == 5.5


def test_player_minutes_are_explicit_and_include_all_four_props():
    rates = PlayerPerMinute(points=.5, rebounds=.2, assists=.1, steals=.04)
    assert projected_player_box_score(rates, 30) == {
        "points": 15, "rebounds": 6, "assists": 3, "steals": 1.2
    }


def test_missing_or_invalid_rates_do_not_become_zeros():
    with pytest.raises((TypeError, ValueError)):
        TeamRates(None, 3)
    with pytest.raises(ValueError):
        projected_player_box_score(PlayerPerMinute(1, 1, 1, 1), float("nan"))
