"""Read-only StrikeoutLab pitcher logs as historical SportLab evidence."""

from __future__ import annotations

import os
from datetime import date

from sportlab.models.threshold_frequency import EventFrequency, estimate_threshold


def pitcher_strikeout_frequency(
    pitcher: str,
    opponent_code: str,
    as_of: date,
    season: int,
    line: float,
    *,
    prior_games: float = 20.0,
    simulations: int = 10_000,
    seed: int = 20261008,
) -> dict:
    """Compare the pitcher's K outings with K allowed to opposing starters.

    The line must be a half-integer: a whole-number line may push and cannot
    be represented as a binary event without separate push handling.
    """
    if not pitcher.strip() or not opponent_code.strip():
        raise ValueError("pitcher and opponent_code are required")
    if season < 2000 or as_of.year < season or line < 0 or line % 1 != 0.5:
        raise ValueError("require a valid season, pregame cutoff and half-integer K line")

    url = os.environ.get("SPORTLAB_SUPABASE_DATABASE_URL")
    if not url:
        raise RuntimeError("SPORTLAB_SUPABASE_DATABASE_URL is not set")

    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise RuntimeError("Install psycopg[binary] to read Supabase history") from exc

    query = """
    WITH tagged AS (
        SELECT pitcher, rival, k, game_pk,
               count(*) OVER (PARTITION BY game_pk, rival) AS rows_per_game_and_rival
        FROM public.game_logs
        WHERE fecha >= make_date(%s, 1, 1) AND fecha < %s
          AND k IS NOT NULL
    ), eligible AS (
        SELECT pitcher, rival, k FROM tagged
        WHERE game_pk IS NOT NULL AND rows_per_game_and_rival = 1
    )
    SELECT
        (SELECT count(*) FROM eligible WHERE pitcher = %s) AS pitcher_games,
        (SELECT count(*) FROM eligible WHERE pitcher = %s AND k > %s) AS pitcher_hits,
        (SELECT count(*) FROM eligible WHERE rival = normalizar_equipo(%s)) AS opponent_games,
        (SELECT count(*) FROM eligible WHERE rival = normalizar_equipo(%s) AND k > %s) AS opponent_hits,
        (SELECT count(*) FROM eligible) AS league_games,
        (SELECT count(*) FROM eligible WHERE k > %s) AS league_hits,
        (SELECT count(*) FROM tagged WHERE game_pk IS NOT NULL AND rows_per_game_and_rival > 1) AS ambiguous_rows_excluded,
        (SELECT count(*) FROM tagged WHERE game_pk IS NULL) AS missing_game_id_rows_excluded
    """
    with psycopg.connect(url) as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SET TRANSACTION READ ONLY")
            cur.execute(query, (season, as_of, pitcher, pitcher, line,
                                opponent_code, opponent_code, line, line))
            counts = cur.fetchone()

    if not counts or min(counts["pitcher_games"], counts["opponent_games"], counts["league_games"]) == 0:
        raise ValueError("Supabase has insufficient eligible pitcher, opponent or league logs")
    event_key = f"MLB:{season}:pitcher_strikeouts:full_game:over_{line}"
    result = estimate_threshold(
        EventFrequency(counts["pitcher_hits"], counts["pitcher_games"], event_key),
        EventFrequency(counts["opponent_hits"], counts["opponent_games"], event_key),
        counts["league_hits"] / counts["league_games"],
        prior_games=prior_games, simulations=simulations, seed=seed,
    )
    return {
        **result,
        "pitcher": pitcher,
        "opponent": opponent_code,
        "as_of_exclusive": as_of.isoformat(),
        "source": "Supabase StrikeoutLab public.game_logs (historical MLB only)",
        "league_games": counts["league_games"],
        "ambiguous_rows_excluded": counts["ambiguous_rows_excluded"],
        "missing_game_id_rows_excluded": counts["missing_game_id_rows_excluded"],
    }
