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

def strikeout_counts_from_bf(
    rng: np.random.Generator,
    bf_samples: tuple[int, ...],
    pitcher_k_rate: float,
    opponent_k_rate: float,
    league_k_rate: float,
    n: int,
    bf_shift: int = 0,
) -> np.ndarray:
    """Bootstrap starter BF; adjust K/BF for opponent K/PA on log odds.

    This is an exploratory matchup model. It preserves early-hook risk from
    observed starts and permits an explicit workload sensitivity scenario.
    """
    if not bf_samples or any(x <= 0 for x in bf_samples):
        raise ValueError("positive starter BF samples are required")
    if not all(0 < p < 1 for p in (pitcher_k_rate, opponent_k_rate, league_k_rate)):
        raise ValueError("K rates must lie strictly between zero and one")
    logit = lambda p: np.log(p / (1 - p))
    adjusted = 1 / (1 + np.exp(-(logit(pitcher_k_rate) + logit(opponent_k_rate) - logit(league_k_rate))))
    bf = rng.choice(np.asarray(bf_samples, dtype=int), size=n)
    return rng.binomial(np.maximum(1, bf + bf_shift), adjusted)

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
