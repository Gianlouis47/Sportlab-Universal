from datetime import datetime, timedelta, timezone
import pytest
from sportlab.models.historical_trends import Observation, historical_trends

CUT = datetime(2026, 10, 16, tzinfo=timezone.utc)


def obs(i, value, observed_at=None):
    return Observation(str(i), CUT-timedelta(days=i+1), observed_at or CUT, True, value, "test")


def test_exact_line_push_missing_no_fill_and_cutoff():
    rows = [obs(0, 8), obs(1, 7), obs(2, None), obs(3, 9), obs(4, 6), obs(5, 10)]
    rows += [Observation("future", CUT, CUT, True, 100, "test"), obs(7, 100, CUT+timedelta(seconds=1))]
    result = historical_trends(rows, event_key="soccer/corners/full_match", line=7,
                               direction="over", as_of=CUT, windows=(5,))["windows"]["L5"]
    assert (result["hits"], result["losses"], result["pushes"], result["missing"]) == (2, 1, 1, 1)
    assert result["fraction"] == "2/4" and result["decisive_frequency"] == 2/3


def test_correction_after_cutoff_is_excluded():
    old = obs(0, 5, CUT-timedelta(hours=2))
    corrected = obs(0, 10, CUT+timedelta(hours=2))
    result = historical_trends([old, old, corrected], event_key="shots", line=7.5,
                              direction="over", as_of=CUT)["windows"]["L10"]
    assert result["fraction"] == "0/1"


def test_empty_is_missing_not_zero():
    result = historical_trends([], event_key="shots", line=7.5, direction="over", as_of=CUT)
    assert result["windows"]["L10"]["historical_frequency"] is None


def test_conflicting_sources_fail_instead_of_double_counting():
    with pytest.raises(ValueError, match="Conflicting"):
        historical_trends([obs(0, 3), obs(0, 9)], event_key="shots", line=5,
                          direction="over", as_of=CUT)
