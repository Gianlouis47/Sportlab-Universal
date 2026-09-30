from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _valid_rate(rate: float) -> bool:
    return isfinite(rate) and 0 <= rate <= 1


@dataclass(frozen=True)
class BatterMatchup:
    expected_pa: float
    strikeout_rate: float
    bvp_pa: int = 0
    bvp_strikeouts: int = 0

    def __post_init__(self) -> None:
        if not isfinite(self.expected_pa) or self.expected_pa < 0:
            raise ValueError("expected_pa must be finite and non-negative")
        if not _valid_rate(self.strikeout_rate):
            raise ValueError("strikeout_rate must be between zero and one")
        if self.bvp_pa < 0 or not 0 <= self.bvp_strikeouts <= self.bvp_pa:
            raise ValueError("invalid batter-vs-pitcher sample")


def project_lineup_strikeouts(
    pitcher_k_rate: float,
    batters: list[BatterMatchup],
    *,
    bvp_prior_pa: float = 75.0,
) -> float:
    """Expected pitcher Ks from PA-weighted lineup and shrunk batter-vs-pitcher history.

    The pitcher and batter strikeout rates each contribute half of the baseline.
    BvP modifies that baseline only in proportion to its historical sample.
    Expected PA must reflect the pitcher's workload; this function does not invent it.
    """
    if not _valid_rate(pitcher_k_rate):
        raise ValueError("pitcher_k_rate must be between zero and one")
    if not isfinite(bvp_prior_pa) or bvp_prior_pa <= 0:
        raise ValueError("bvp_prior_pa must be positive and finite")
    if not batters:
        raise ValueError("a projected opposing lineup is required")

    expected = 0.0
    for batter in batters:
        baseline = (pitcher_k_rate + batter.strikeout_rate) / 2
        if batter.bvp_pa:
            historical = batter.bvp_strikeouts / batter.bvp_pa
            weight = batter.bvp_pa / (batter.bvp_pa + bvp_prior_pa)
            baseline = (1 - weight) * baseline + weight * historical
        expected += batter.expected_pa * baseline
    return expected
