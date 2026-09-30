import pytest

from sportlab.sports.mlb.matchups import BatterMatchup, project_lineup_strikeouts


def test_pitcher_lineup_projection_weights_expected_plate_appearances():
    batters = [
        BatterMatchup(expected_pa=3, strikeout_rate=.30),
        BatterMatchup(expected_pa=2, strikeout_rate=.10),
    ]
    assert project_lineup_strikeouts(.20, batters) == pytest.approx(1.15)


def test_small_bvp_sample_is_shrunk_toward_baseline():
    batter = BatterMatchup(expected_pa=4, strikeout_rate=.20, bvp_pa=1, bvp_strikeouts=1)
    result = project_lineup_strikeouts(.20, [batter], bvp_prior_pa=99)
    assert result == pytest.approx(4 * (.99 * .20 + .01))


def test_missing_lineup_and_invalid_sample_fail_explicitly():
    with pytest.raises(ValueError):
        project_lineup_strikeouts(.2, [])
    with pytest.raises(ValueError):
        BatterMatchup(expected_pa=4, strikeout_rate=.2, bvp_pa=1, bvp_strikeouts=2)
