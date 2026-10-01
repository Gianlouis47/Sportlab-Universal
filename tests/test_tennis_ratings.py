from datetime import date

import pytest

from sportlab.sports.tennis.ratings import TennisRatings, comparison_rows


def test_comparison_does_not_invent_missing_attack_or_defense():
    munar = TennisRatings("Jaume Munar", date(2026, 10, 1), "external editorial rating", "hard", consistency=7.5)
    faria = TennisRatings("Jaime Faria", date(2026, 10, 1), "external editorial rating", "hard", consistency=5.5)

    assert comparison_rows(munar, faria) == [
        {"facet": "offense", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "defense", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "serve", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "return_rating", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "volley", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "consistency", "Jaume Munar": 7.5, "Jaime Faria": 5.5},
        {"facet": "recent_form", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "surface_fit", "Jaume Munar": None, "Jaime Faria": None},
        {"facet": "preferred_surface", "Jaume Munar": None, "Jaime Faria": None},
    ]


def test_tokyo_editorial_ratings_keep_surface_preference_separate_from_fit():
    today = date(2026, 10, 1)
    munar = TennisRatings("Jaume Munar", today, "Google editorial", "hard", offense=5.5, defense=8.5,
                          serve=6, volley=6.5, consistency=7.5, surface_fit=6.5, preferred_surface="clay")
    faria = TennisRatings("Jaime Faria", today, "Google editorial", "hard", offense=7.5, defense=6,
                          serve=7.5, volley=6.5, consistency=5.5, surface_fit=8.0, preferred_surface="hard")
    rows = comparison_rows(munar, faria)
    assert rows[0] == {"facet": "offense", "Jaume Munar": 5.5, "Jaime Faria": 7.5}
    assert rows[3] == {"facet": "return_rating", "Jaume Munar": None, "Jaime Faria": None}
    assert rows[-2] == {"facet": "surface_fit", "Jaume Munar": 6.5, "Jaime Faria": 8.0}
    assert rows[-1] == {"facet": "preferred_surface", "Jaume Munar": "clay", "Jaime Faria": "hard"}


def test_rejects_invalid_rating_and_cross_surface_comparison():
    today = date(2026, 10, 1)
    with pytest.raises(ValueError, match="between 1 and 10"):
        TennisRatings("A", today, "source", "hard", consistency=float("nan"))
    with pytest.raises(ValueError, match="between 1 and 10"):
        TennisRatings("A", today, "source", "hard", return_rating=11)
    with pytest.raises(ValueError, match="between 1 and 10"):
        TennisRatings("A", today, "source", "hard", recent_form=0)
    with pytest.raises(ValueError, match="sample size"):
        TennisRatings("A", today, "source", "hard", sample_size=-1)
    hard = TennisRatings("A", today, "source", "hard", offense=8)
    clay = TennisRatings("B", today, "source", "clay", defense=7)
    with pytest.raises(ValueError, match="same surface"):
        comparison_rows(hard, clay)
