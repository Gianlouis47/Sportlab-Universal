"""Exact-line descriptive trends, with event and knowledge cutoffs."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import isfinite


@dataclass(frozen=True)
class Observation:
    event_id: str
    event_at: datetime
    observed_at: datetime
    completed: bool
    value: float | None
    source: str


def _aware(value: datetime):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone-aware timestamps are required")


def historical_trends(rows: list[Observation], *, event_key: str, line: float,
                      direction: str, as_of: datetime, windows=(5, 10, 20, 30)) -> dict:
    _aware(as_of)
    if not event_key.strip() or direction not in ("over", "under") or not isfinite(line):
        raise ValueError("Specify the exact event, finite line and over/under")
    if not windows or any(type(w) is not int or w < 1 for w in windows):
        raise ValueError("Windows must be positive integers")
    versions = {}
    for row in rows:
        _aware(row.event_at)
        _aware(row.observed_at)
        if not row.event_id or not row.source:
            raise ValueError("Event identity and source are required")
        if row.value is not None and (isinstance(row.value, bool) or not isfinite(row.value)):
            raise ValueError("Observed values must be finite or missing")
        if row.event_at >= as_of or row.observed_at > as_of:
            continue
        old = versions.get(row.event_id)
        if old and row.observed_at == old.observed_at and row != old:
            raise ValueError("Conflicting observations; reconcile sources before counting")
        if old is None or row.observed_at > old.observed_at:
            versions[row.event_id] = row
    completed = sorted((r for r in versions.values() if r.completed),
                       key=lambda r: (r.event_at, r.event_id), reverse=True)
    result = {}
    for window in windows:
        selected = completed[:window]
        values = [r.value for r in selected if r.value is not None]
        pushes = sum(v == line for v in values)
        hits = sum((v > line if direction == "over" else v < line) for v in values)
        result[f"L{window}"] = {
            "hits": hits, "losses": len(values) - hits - pushes, "pushes": pushes,
            "missing": len(selected) - len(values), "selected": len(selected),
            "observed": len(values), "requested": window,
            "fraction": f"{hits}/{len(values)}",
            "historical_frequency": hits / len(values) if values else None,
            "decisive_frequency": hits / (len(values)-pushes) if len(values)>pushes else None,
            "event_ids": [r.event_id for r in selected],
        }
    return {"event_key": event_key, "line": line, "direction": direction,
            "as_of": as_of.isoformat(), "type": "historical_not_future_probability", "windows": result}
