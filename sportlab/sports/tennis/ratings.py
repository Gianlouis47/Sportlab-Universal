from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from math import isfinite


@dataclass(frozen=True)
class TennisRatings:
    player: str
    as_of: date
    source: str
    surface: str
    sample_size: int | None = None
    offense: float | None = None
    defense: float | None = None
    serve: float | None = None
    volley: float | None = None
    consistency: float | None = None
    surface_fit: float | None = None
    preferred_surface: str | None = None

    def __post_init__(self) -> None:
        if not self.player.strip() or not self.source.strip() or not self.surface.strip():
            raise ValueError("player, source and surface are required")
        if self.sample_size is not None and self.sample_size < 0:
            raise ValueError("sample size cannot be negative")
        for rating in (self.offense, self.defense, self.serve, self.volley, self.consistency, self.surface_fit):
            if rating is not None and (not isfinite(rating) or not 1 <= rating <= 10):
                raise ValueError("ratings must be between 1 and 10")


def comparison_rows(first: TennisRatings, second: TennisRatings) -> list[dict[str, str | float | None]]:
    """Display assessments side by side; missing facets remain unavailable."""
    if first.surface != second.surface:
        raise ValueError("compare ratings from the same surface")
    return [
        {"facet": facet, first.player: getattr(first, facet), second.player: getattr(second, facet)}
        for facet in ("offense", "defense", "serve", "volley", "consistency", "surface_fit", "preferred_surface")
    ]
