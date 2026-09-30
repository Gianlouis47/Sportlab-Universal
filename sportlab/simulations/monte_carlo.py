from __future__ import annotations
from typing import Iterable
import numpy as np

def gamma_poisson_counts(rng: np.random.Generator, mean: float, n: int, dispersion: float = 0.28) -> np.ndarray:
    if mean <= 0:
        return np.zeros(n, dtype=int)
    if dispersion <= 1e-9:
        return rng.poisson(mean, n)
    shape = 1.0 / dispersion
    scale = mean * dispersion
    lam = rng.gamma(shape=shape, scale=scale, size=n)
    return rng.poisson(lam)

def poisson_counts(rng: np.random.Generator, mean: float, n: int) -> np.ndarray:
    return rng.poisson(max(0.0, mean), n)

def line_probabilities(values: np.ndarray, lines: Iterable[float]) -> dict[str, dict[str, float]]:
    out = {}
    n = len(values)
    for line in lines:
        over = float(np.count_nonzero(values > line) / n)
        under = float(np.count_nonzero(values < line) / n)
        push = float(np.count_nonzero(values == line) / n) if float(line).is_integer() else 0.0
        out[str(line)] = {"over": over, "under": under, "push": push}
    return out

def win_probabilities(away: np.ndarray, home: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    away_w = away > home
    home_w = home > away
    ties = away == home
    tie_draw = rng.random(np.count_nonzero(ties)) < 0.5
    away_count = int(np.count_nonzero(away_w)) + int(np.count_nonzero(tie_draw))
    home_count = int(np.count_nonzero(home_w)) + int(np.count_nonzero(~tie_draw))
    n = len(away)
    return away_count / n, home_count / n
