"""Read exact team-stat observations from versioned ESPN summaries."""
from datetime import datetime
from math import isfinite
import re

from sportlab.models.historical_trends import Observation


def stat_value(statistics: list[dict], path: tuple[str, ...]) -> float | None:
    """Path uses provider names, e.g. ('batting','strikeouts') or ('shotsTotal',)."""
    if not path:
        raise ValueError("Specify an exact provider statistic path")
    matches = [item for item in statistics if item.get("name") == path[0]]
    if len(matches) != 1:
        return None
    item = matches[0]
    if len(path) > 1:
        return stat_value(item.get("stats", []), path[1:])
    value = item.get("value")
    if isinstance(value, bool):
        return None
    if not isinstance(value, (int, float)):
        value = item.get("displayValue", "")
        if not isinstance(value, str) or not re.fullmatch(r"-?\d+(?:\.\d+)?", value):
            return None
        value = float(value)
    return float(value) if isfinite(value) else None


def team_observations(snapshots: list[dict], team_id: str,
                      metric_path: tuple[str, ...]) -> list[Observation]:
    observations = []
    for row in snapshots:
        payload = row["payload"]
        header = payload.get("header", {})
        competitions = header.get("competitions", [])
        if len(competitions) != 1:
            continue
        event = competitions[0]
        if not any(str(c.get("id")) == team_id for c in event.get("competitors", [])):
            continue
        teams = [t for t in payload.get("boxscore", {}).get("teams", [])
                 if str(t.get("team", {}).get("id")) == team_id]
        stats = teams[0].get("statistics", []) if len(teams) == 1 else []
        event_at = datetime.fromisoformat(event["date"].replace("Z", "+00:00"))
        observed_at = row["fetched_at"]
        if isinstance(observed_at, str):
            observed_at = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        observations.append(Observation(
            str(header["id"]), event_at, observed_at,
            event.get("status", {}).get("type", {}).get("completed") is True,
            stat_value(stats, metric_path), row["source_url"],
        ))
    return observations


def load_team_observations(conn, league: str, team_id: str,
                           metric_path: tuple[str, ...], as_of: datetime):
    from psycopg.rows import dict_row
    from sportlab.data.source_sync import LEAGUES
    if league not in LEAGUES or league == "ATP":
        raise ValueError("Use a supported team league; ATP needs individual match logs")
    if as_of.tzinfo is None or as_of.utcoffset() is None:
        raise ValueError("Timezone-aware cutoff is required")
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            SELECT DISTINCT ON (resource_key) payload,fetched_at,source_url
            FROM core.source_snapshots
            WHERE provider='espn' AND resource_key LIKE %s AND fetched_at <= %s
            ORDER BY resource_key,fetched_at DESC
        """, (league + "/summary/%", as_of))
        return team_observations(list(cur.fetchall()), team_id, metric_path)
