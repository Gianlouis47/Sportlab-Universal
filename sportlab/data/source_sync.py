"""Bounded public ESPN reads and content-addressed source snapshots."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timedelta, timezone
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from sportlab.data.neon import connect

LEAGUES = {
    "MLB": "baseball/mlb", "NHL": "hockey/nhl", "NFL": "football/nfl",
    "NBA": "basketball/nba", "ATP": "tennis/atp",
    "EPL": "soccer/eng.1", "LALIGA": "soccer/esp.1",
    "SERIEA": "soccer/ita.1", "BUNDESLIGA": "soccer/ger.1",
    "LIGUE1": "soccer/fra.1", "UCL": "soccer/uefa.champions",
}
BASE = "https://site.api.espn.com/apis/site/v2/sports/"


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def read_json(url: str) -> dict:
    if not url.startswith(BASE):
        raise ValueError("Only the configured ESPN host and path are allowed")
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "SportLab/0.1"})
    with build_opener(NoRedirect()).open(request, timeout=20) as response:
        raw = response.read(12_000_001)
        if len(raw) > 12_000_000:
            raise ValueError("Provider response exceeds size budget")
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise ValueError("Expected a JSON object")
        return payload


def compact_payload(payload: dict) -> dict:
    """Retain event identity, results and box scores, excluding media/play-by-play."""
    excluded = {"links", "logos", "logo", "headshot", "headshots", "image", "images",
                "news", "videos", "video", "odds", "oddsDetails", "broadcasts", "broadcast",
                "geoBroadcasts", "tickets", "ticketsInfo", "leaders", "featuredAthletes"}
    def clean(value):
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items() if k not in excluded}
        if isinstance(value, list):
            return [clean(v) for v in value]
        return value
    return {"projection": "event_boxscore_v1", **clean({k: v for k, v in payload.items()
            if k in {"header", "boxscore", "events", "season", "leagues", "day"}})}


def snapshot(resource_key: str, url: str, payload: dict, now: datetime) -> dict:
    payload = compact_payload(payload)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return {"provider": "espn", "resource_key": resource_key,
            "payload_hash": hashlib.sha256(encoded.encode()).hexdigest(),
            "fetched_at": now.isoformat(), "source_url": url, "payload": payload}


def collect(leagues: list[str], days: list[date], *, max_summaries: int = 20,
            fetch=read_json) -> tuple[list[dict], list[dict]]:
    """Keep raw provider statistics; a tournament is never counted as a tennis match."""
    if not 0 <= max_summaries <= 100:
        raise ValueError("max_summaries must be between zero and 100 per league")
    if not days or len(days) > 31:
        raise ValueError("Request between one and 31 dates")
    rows, errors = [], []
    for league in dict.fromkeys(leagues):
        path = LEAGUES[league]
        event_ids = []
        for day in sorted(set(days)):
            key = f"{league}/scoreboard/{day.isoformat()}"
            url = f"{BASE}{path}/scoreboard?dates={day:%Y%m%d}&limit=1000"
            try:
                payload = fetch(url)
                if not isinstance(payload.get("events"), list):
                    raise ValueError("Scoreboard is missing its events list")
                rows.append(snapshot(key, url, payload, datetime.now(timezone.utc)))
                for event in payload["events"]:
                    # ATP scoreboards contain tournament containers; their IDs are
                    # not accepted as individual summary/match identifiers.
                    if league != "ATP" and str(event.get("id", "")).isdigit():
                        event_ids.append(str(event["id"]))
            except (OSError, ValueError) as exc:
                errors.append({"resource": key, "error": str(exc)})
        for event_id in list(dict.fromkeys(event_ids))[-max_summaries:] if max_summaries else []:
            key = f"{league}/summary/{event_id}"
            url = f"{BASE}{path}/summary?event={event_id}"
            try:
                payload = fetch(url)
                competitions = payload.get("header", {}).get("competitions", [])
                if not competitions:
                    raise ValueError("Summary has no event header; not accepted as game data")
                if str(payload.get("header", {}).get("id")) != event_id:
                    raise ValueError("Summary event identity does not match the request")
                rows.append(snapshot(key, url, payload, datetime.now(timezone.utc)))
            except (OSError, ValueError) as exc:
                errors.append({"resource": key, "error": str(exc)})
    return rows, errors


def save(rows: list[dict], conn) -> int:
    changed = 0
    with conn.cursor() as cur:
        for row in rows:
            cur.execute("SELECT pg_advisory_xact_lock(hashtext(%s))",
                        (row["provider"] + "/" + row["resource_key"],))
            cur.execute("""
                SELECT payload_hash FROM core.source_snapshots
                WHERE provider=%s AND resource_key=%s
                ORDER BY fetched_at DESC LIMIT 1
            """, (row["provider"], row["resource_key"]))
            latest = cur.fetchone()
            if latest and latest[0] == row["payload_hash"]:
                cur.execute("""
                    UPDATE core.source_snapshots SET last_seen_at=GREATEST(last_seen_at,%s)
                    WHERE provider=%s AND resource_key=%s AND fetched_at=(
                        SELECT max(fetched_at) FROM core.source_snapshots
                        WHERE provider=%s AND resource_key=%s)
                """, (row["fetched_at"], row["provider"], row["resource_key"],
                      row["provider"], row["resource_key"]))
                continue
            cur.execute("""
                INSERT INTO core.source_snapshots
                  (provider,resource_key,payload_hash,fetched_at,last_seen_at,source_url,payload)
                VALUES (%s,%s,%s,%s,%s,%s,%s::jsonb)
                ON CONFLICT (provider,resource_key,fetched_at) DO NOTHING
            """, (row["provider"], row["resource_key"], row["payload_hash"],
                  row["fetched_at"], row["fetched_at"], row["source_url"],
                  json.dumps(row["payload"], allow_nan=False)))
            changed += cur.rowcount
    conn.commit()
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, required=True)
    parser.add_argument("--days", type=int, default=2, help="Days ending at --date, inclusive")
    parser.add_argument("--leagues", nargs="+", choices=LEAGUES, default=list(LEAGUES))
    parser.add_argument("--max-summaries", type=int, default=20)
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--output", help="Local JSON transport file; do not commit data dumps")
    args = parser.parse_args()
    if not 1 <= args.days <= 31:
        parser.error("--days must be between one and 31")
    days = [args.date - timedelta(days=i) for i in range(args.days)]
    rows, errors = collect(args.leagues, days, max_summaries=args.max_summaries)
    inserted = None
    if args.save:
        with connect() as conn:
            inserted = save(rows, conn)
    if args.output:
        with open(args.output, "w") as handle:
            json.dump(rows, handle)
    print(json.dumps({"resources_read": len(rows), "new_versions": inserted,
                      "errors": errors, "coverage": "bounded_public_snapshots_not_complete_history"}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
