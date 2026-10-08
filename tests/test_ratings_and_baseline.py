from sportlab.models.ratings import classify_pitcher_style, display_1_to_10, league_percentile
from sportlab.sports.mlb.baselines import notebook_run_baseline

def test_notebook_run_baseline():
    r=notebook_run_baseline(5.0,4.0,4.0,5.0)
    assert r.away_expected==5.0
    assert r.home_expected==4.0
    assert r.total_expected==9.0

def test_rating_scale_and_pitcher_style():
    assert 49 <= league_percentile(10,10,2) <= 51
    assert display_1_to_10(87)==8.7
    assert classify_pitcher_style(85,80,75).label=="STRIKEOUT"
    assert classify_pitcher_style(25,30,35).label=="CONTACT"
