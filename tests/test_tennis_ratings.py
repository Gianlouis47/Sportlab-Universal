from datetime import date

import pytest

from sportlab.sports.tennis.ratings import TennisRatings, comparison_rows


def test_comparison_does_not_invent_missing_attack_or_defense():
    munar = TennisRatings("Jaume Munar", date(2026, 10, 1), "external editorial rating", "hard", consistency=7.5)
    faria = TennisRatings("Jaime Faria", date(2026, 10, 1), "external editorial rating", "hard", consistency=5.5)

    assert comparison_rows(munar, faria) == [
        {"facet": "offense", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "defense", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "consistency", "Jaume Munar": 7.5, "Jaime Faria": 5.5},
    ]


def test_rejects_invalid_rating_and_cross_surface_comparison():
    today = date(2026, 10, 1)
    with pytest.raises(ValueError, match="between 1 and 10"):
        TennisRatings("A", today, "source", "hard", consistency=float("nan"))
    with pytest.raises(ValueError, match="sample size"):
        TennisRatings("A", today, "source", "hard", sample_size=-1)
    hard = TennisRatings("A", today, "source", "hard", offense=8)
    clay = TennisRatings("B", today, "source", "clay", defense=7)
    with pytest.raises(ValueError, match="same surface"):
        comparison_rows(hard, clay)
