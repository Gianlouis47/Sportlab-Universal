from sportlab.models.recent_form import non_overlapping_recent_bands
from sportlab.types import TeamProfile, WindowForm

def test_nested_windows_become_non_overlapping_bands():
    team = TeamProfile(code="X", season_offense=4, season_defense_allowed=4,
        l10=WindowForm(10,5,4), l20=WindowForm(20,4,5), l30=WindowForm(30,3,6))
    b = non_overlapping_recent_bands(team)
    assert b["last10"] == (5,4)
    assert b["previous10"] == (3,6)
    assert b["third10"] == (1,8)
