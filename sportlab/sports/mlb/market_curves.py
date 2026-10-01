from __future__ import annotations
from math import exp, factorial

def poisson_pmf(k: int, mean: float) -> float:
    return exp(-mean) * (mean ** k) / factorial(k)

def strikeout_curve(mean: float, max_k: int = 15) -> dict[int, float]:
    probs = {}
    cumulative = 0.0
    for k in range(max_k + 1):
        cumulative += poisson_pmf(k, mean)
        probs[k] = max(0.0, 1.0 - cumulative + poisson_pmf(k, mean))
    return probs

def line_outcomes(mean: float, line: float, max_k: int = 25) -> dict[str, float]:
    probs = [poisson_pmf(k, mean) for k in range(max_k+1)]
    tail = max(0.0, 1.0 - sum(probs))
    over = sum(p for k,p in enumerate(probs) if k > line)
    under = sum(p for k,p in enumerate(probs) if k < line)
    push = sum(p for k,p in enumerate(probs) if k == line)
    if max_k > line:
        over += tail
    return {"over": over, "under": under, "push": push}
