from __future__ import annotations
from sportlab.types import PitcherProfile

def project_pitcher_k_mean(p: PitcherProfile) -> float:
    components = []
    if p.season_k_per_9 is not None:
        components.append((p.season_k_per_9, 0.40))
    if p.recent_k_per_9 is not None:
        components.append((p.recent_k_per_9, 0.25))
    if p.opponent_k_per_9 is not None:
        components.append((p.opponent_k_per_9, 0.20))
    if not components:
        k9 = 8.0
    else:
        denom = sum(w for _, w in components)
        k9 = sum(v*w for v,w in components) / denom
    expected = k9 * max(1.0, p.expected_ip) / 9.0
    expected *= p.opponent_k_factor
    expected *= p.workload_factor
    return max(0.25, expected)
