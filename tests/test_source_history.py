from datetime import datetime, timezone
from sportlab.data.source_history import stat_value, team_observations


def test_numeric_path_missing_zero_and_combined_display():
    assert stat_value([{'name':'shotsTotal','displayValue':'0'}], ('shotsTotal',)) == 0
    assert stat_value([], ('shotsTotal',)) is None
    assert stat_value([{'name':'thirdDownEff','displayValue':'6-15'}], ('thirdDownEff',)) is None
    assert stat_value([{'name':'batting','stats':[{'name':'strikeouts','value':13}]}], ('batting','strikeouts')) == 13


def test_event_identity_and_full_final_status_are_retained():
    row={'source_url':'https://example.com','fetched_at':datetime.now(timezone.utc),
         'payload':{'header':{'id':'1','competitions':[{'date':'2026-10-15T23:00:00Z',
         'competitors':[{'id':'21'}], 'status':{'type':{'completed':True}}}]},
         'boxscore':{'teams':[{'team':{'id':'21'},'statistics':[{'name':'shotsTotal','displayValue':'23'}]}]}}}
    observations=team_observations([row], '21', ('shotsTotal',))
    assert len(observations)==1 and observations[0].value==23 and observations[0].completed
    assert not team_observations([row], '99', ('shotsTotal',))
