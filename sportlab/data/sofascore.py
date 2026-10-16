"""Read the versioned API of a user's self-hosted SofaScore Scraper."""
from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

SPORTS = {"MLB": "baseball", "NHL": "ice-hockey", "NFL": "american-football",
          "NBA": "basketball", "SOCCER": "football", "TENNIS": "tennis"}


class SofaScoreUnavailable(RuntimeError):
    pass


class SofaScoreClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000", token: str | None = None):
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Use an HTTP(S) service URL without embedded credentials")
        if parsed.scheme == "http" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Remote services require HTTPS")
        self.base_url = base_url.rstrip("/")
        self.token = token

    def get(self, path: str, **params) -> dict:
        query = urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(f"{self.base_url}/api/v1/{path}" + (f"?{query}" if query else ""), headers=headers)
        try:
            with urlopen(request, timeout=20) as response:
                result = json.load(response)
        except HTTPError as exc:
            raise SofaScoreUnavailable(f"SofaScore service HTTP {exc.code}; no data imported") from None
        except (URLError, TimeoutError, OSError, ValueError) as exc:
            raise SofaScoreUnavailable("SofaScore service unavailable or invalid JSON; no data imported") from exc
        if not isinstance(result, dict) or "error" in result or "data" not in result:
            raise SofaScoreUnavailable("Unexpected SofaScore API envelope")
        return result

    def events(self, sport: str, *, participant: int | None = None, before: str | None = None,
               max_pages: int = 5) -> dict:
        if sport not in SPORTS or max_pages < 1:
            raise ValueError("Unsupported sport or invalid page budget")
        items, cursor, seen = [], None, set()
        for _ in range(max_pages):
            page = self.get("events", sport=SPORTS[sport], participant=participant,
                            status="completed", sort="-start_utc", limit=200, cursor=cursor,
                            **{"to": before})
            if not isinstance(page["data"], list):
                raise SofaScoreUnavailable("Expected an event list")
            for event in page["data"]:
                if event["id"] not in seen:
                    items.append(event)
                    seen.add(event["id"])
            next_cursor = page.get("page", {}).get("next_cursor")
            if not next_cursor:
                return {"source": "sofascore_scraper_api_v1", "events": items, "truncated": False}
            if next_cursor == cursor:
                raise SofaScoreUnavailable("Repeated pagination cursor")
            cursor = next_cursor
        return {"source": "sofascore_scraper_api_v1", "events": items, "truncated": True}

    def statistics(self, event_id: int) -> dict:
        if event_id < 1:
            raise ValueError("event_id must be positive")
        data = self.get(f"events/{event_id}/slices/statistics")["data"]
        if data.get("state") != "ok" or not data.get("has_payload"):
            raise SofaScoreUnavailable("Statistics missing, stale or failed; never treated as zero")
        return data


def threshold_history(rows: list[dict], *, event_key: str, line: float, direction: str,
                      as_of: str, window: int = 10) -> dict:
    """Rows are explicitly mapped numeric observations, not guessed score fields."""
    if not event_key.strip() or direction not in {"over", "under"} or not math.isfinite(line) or window < 1:
        raise ValueError("Specify exact market/period/settlement, finite line, direction and positive window")
    def timestamp(value):
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            raise ValueError("Timestamps must include a timezone")
        return result
    cutoff = timestamp(as_of)
    selected = {}
    for row in rows:
        if row["event_key"] != event_key:
            raise ValueError("Mixed settlement events are not comparable")
        if row["status"] != "completed" or timestamp(row["start_utc"]) >= cutoff:
            continue
        old = selected.get(row["event_id"])
        if old is not None and old != row:
            raise ValueError("Conflicting duplicate observations")
        selected[row["event_id"]] = row
    recent = sorted(selected.values(), key=lambda r: timestamp(r["start_utc"]), reverse=True)[:window]
    observed, missing = [], []
    for row in recent:
        value = row.get("value")
        if value is None:
            missing.append(row["event_id"])
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("Observations must be finite numbers or null")
        outcome = "push" if value == line else "win" if ((value > line) == (direction == "over")) else "loss"
        observed.append({**row, "outcome": outcome})
    wins = sum(row["outcome"] == "win" for row in observed)
    pushes = sum(row["outcome"] == "push" for row in observed)
    return {"event_key": event_key, "line": line, "direction": direction, "as_of": as_of,
            "window_requested": window, "games_in_window": len(recent), "observed": len(observed),
            "wins": wins, "losses": len(observed)-wins-pushes, "pushes": pushes,
            "missing_event_ids": missing, "observed_hit_rate": wins/len(observed) if observed else None,
            "interpretation": "Historical frequency only; not a future probability or pick",
            "gamelog": observed}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=os.getenv("SPORTLAB_SOFASCORE_URL", "http://127.0.0.1:8000"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("health")
    events = sub.add_parser("events")
    events.add_argument("--sport", choices=SPORTS, required=True)
    events.add_argument("--participant", type=int)
    events.add_argument("--before")
    stats = sub.add_parser("statistics")
    stats.add_argument("--event-id", type=int, required=True)
    trend = sub.add_parser("trend")
    trend.add_argument("--input", required=True)
    trend.add_argument("--event-key", required=True)
    trend.add_argument("--line", type=float, required=True)
    trend.add_argument("--direction", choices=["over", "under"], required=True)
    trend.add_argument("--as-of", required=True)
    trend.add_argument("--window", type=int, default=10)
    args = parser.parse_args()
    try:
        if args.command == "trend":
            with open(args.input, encoding="utf-8") as handle:
                result = threshold_history(json.load(handle), event_key=args.event_key, line=args.line,
                                           direction=args.direction, as_of=args.as_of, window=args.window)
        else:
            client = SofaScoreClient(args.url, os.getenv("SPORTLAB_SOFASCORE_TOKEN"))
            if args.command == "events":
                result = client.events(args.sport, participant=args.participant, before=args.before)
            elif args.command == "statistics":
                result = client.statistics(args.event_id)
            else:
                result = client.get("health")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (SofaScoreUnavailable, ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
