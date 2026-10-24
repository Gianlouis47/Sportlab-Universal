"""Exploratory frequency calculator for an exactly defined binary market event."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EventFrequency:
    hits: int
    games: int
    event_key: str

    def __post_init__(self) -> None:
        if (type(self.hits) is not int or type(self.games) is not int
                or self.games < 1 or not 0 <= self.hits <= self.games):
            raise ValueError("hits and games must satisfy 0 <= hits <= games, games >= 1")
        if not self.event_key.strip():
            raise ValueError("event_key must identify the exact settlement event")

    @property
    def observed(self) -> float:
        return self.hits / self.games


def estimate_threshold(
    subject: EventFrequency,
    opponent_allowed: EventFrequency,
    league_rate: float,
    *,
    prior_games: float = 20.0,
    simulations: int = 10_000,
    seed: int = 20261008,
) -> dict:
    """Pool matching event frequencies using a league-rate beta prior.

    `opponent_allowed` must count the very same settlement event permitted by
    the opponent, not a related stat. This is an uncalibrated screening model,
    not a game-level predictive model or a recommended wager.
    """
    if not 0 < league_rate < 1 or not np.isfinite(league_rate):
        raise ValueError("league_rate must lie strictly between zero and one")
    if prior_games <= 0 or not np.isfinite(prior_games):
        raise ValueError("prior_games must be positive and finite")
    if type(simulations) is not int or simulations < 1:
        raise ValueError("simulations must be a positive integer")
    if subject.event_key != opponent_allowed.event_key:
        raise ValueError("subject and opponent samples must describe the same settlement event")

    prior_successes = league_rate * prior_games
    prior_failures = (1 - league_rate) * prior_games

    def posterior(sample: EventFrequency) -> tuple[float, float]:
        return prior_successes + sample.hits, prior_failures + sample.games - sample.hits

    subject_a, subject_b = posterior(subject)
    opponent_a, opponent_b = posterior(opponent_allowed)
    subject_rate = subject_a / (subject_a + subject_b)
    opponent_rate = opponent_a / (opponent_a + opponent_b)
    matchup_rate = (subject_rate + opponent_rate) / 2

    rng = np.random.default_rng(seed)
    subject_draws = rng.beta(subject_a, subject_b, simulations)
    opponent_draws = rng.beta(opponent_a, opponent_b, simulations)
    matchup_draws = (subject_draws + opponent_draws) / 2
    simulated_hits = int(np.count_nonzero(rng.random(simulations) < matchup_draws))

    return {
        "model": "exploratory_beta_frequency_v1",
        "event_key": subject.event_key,
        "status": "UNCALIBRATED_SCREENING_ONLY",
        "subject": {"hits": subject.hits, "games": subject.games, "observed": subject.observed,
                    "smoothed": subject_rate},
        "opponent_allowed": {"hits": opponent_allowed.hits, "games": opponent_allowed.games,
                             "observed": opponent_allowed.observed, "smoothed": opponent_rate},
        "league_rate": league_rate,
        "prior_games": prior_games,
        "matchup_estimate": matchup_rate,
        "matchup_parameter_interval_90pct": [float(x) for x in np.quantile(matchup_draws, [0.05, 0.95])],
        "simulations": simulations,
        "seed": seed,
        "simulated_hits": simulated_hits,
        "simulated_frequency": simulated_hits / simulations,
    }
