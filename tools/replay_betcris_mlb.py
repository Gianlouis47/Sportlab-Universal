"""Replay the four 2026-10-03 Betcris markets against a dated MLB snapshot.

The result is an exploratory simulation audit, never a validated pick list.
Usage: python -m tools.replay_betcris_mlb > examples/betcris_mlb_2026_10_03/model_replay.json
"""

from __future__ import annotations

import json
import gzip
from dataclasses import replace
from pathlib import Path
import numpy as np

from sportlab.data.mlb_stats_api import game_input_from_snapshot
from sportlab.pipelines.mlb_parlay import simulate_mlb_parlay
from sportlab.pipelines.mlb_pregame import analyze_mlb_game
from sportlab.simulations.monte_carlo import gamma_poisson_counts
from sportlab.sports.mlb.runs import project_expected_runs
from tools.ingest_betcris_mlb import FILES, parse_source


ROOT = Path(__file__).resolve().parents[1]
MARKETS = ROOT / "examples" / "betcris_mlb_2026_10_03"
SNAPSHOT = ROOT / "examples" / "mlb_stats_api_2026-10-03_asof_2026-10-02.json.gz"
GAME_IDS = {"cws_cle": 849829, "atl_lad": 849828, "nyy_tb": 849835, "sd_mil": 849830}
LABELS = {
    "cws_cle": ("White Sox", "Guardians"),
    "atl_lad": ("Braves", "Dodgers"),
    "nyy_tb": ("Yankees", "Rays"),
    "sd_mil": ("Padres", "Brewers"),
}
SEED = 20261002
RUNS = 10_000


def lines_for(blocks: list[dict], phrase: str, *, subject: str | None = None) -> tuple[float, ...]:
    selected = [b for b in blocks if b["market"].split(": ", 1)[-1] == phrase]
    return tuple(sorted({q["line"] for b in selected for q in b["quotes"]
                         if "line" in q and (subject is None or q["subject"] == subject)}))


def lower_scoring_ticket(games: list, factor: float = .85) -> dict:
    """A 10,000-draw sensitivity test with both run means reduced by 15%."""
    legs = []
    for game in games:
        away_mu, home_mu, _ = project_expected_runs(game.away, game.home, game.away_pitcher, game.home_pitcher)
        away_mu, home_mu = away_mu * factor, home_mu * factor
        rng = np.random.default_rng(SEED + game.event_id + 42)
        away = gamma_poisson_counts(rng, away_mu, RUNS)
        home = gamma_poisson_counts(rng, home_mu, RUNS)
        for _ in range(20):
            ties = away == home
            if not np.any(ties):
                break
            count = int(np.count_nonzero(ties))
            away[ties] += rng.poisson(away_mu / 9 + .25, count)
            home[ties] += rng.poisson(home_mu / 9 + .25, count)
        ties = away == home
        if np.any(ties):
            home[ties] += rng.random(np.count_nonzero(ties)) < .5
            away[away == home] += 1
        legs.append(away + home > 5.5)
    return {"factor": factor, "simulations": RUNS,
            "leg_win_counts": [int(np.sum(x)) for x in legs],
            "full_win_count": int(np.sum(np.logical_and.reduce(legs)))}


def main() -> None:
    with gzip.open(SNAPSHOT, "rt", encoding="utf-8") as file:
        snapshot = json.load(file)
    alternatives = json.loads((MARKETS / "full_game_alternatives_from_screenshots.json").read_text())
    results = {}
    for key, filename in FILES.items():
        market = parse_source((MARKETS / filename).read_text())
        blocks = market["market_blocks"]
        row = next(g for g in snapshot["games"] if g["id"] == GAME_IDS[key])
        away_starter = snapshot["starters"].get(str(row["away_starter"]), {}).get("name")
        home_starter = snapshot["starters"].get(str(row["home_starter"]), {}).get("name")
        away_label, home_label = LABELS[key]
        game = game_input_from_snapshot(
            snapshot, GAME_IDS[key],
            total_lines=tuple(x["line"] for x in alternatives["games"][key]),
            away_pitcher_k_lines=lines_for(blocks, "Total de Ponches", subject=away_starter),
            home_pitcher_k_lines=lines_for(blocks, "Total de Ponches", subject=home_starter),
            away_team_hit_lines=lines_for(blocks, f"{away_label} Total de Hits"),
            home_team_hit_lines=lines_for(blocks, f"{home_label} Total de Hits"),
            away_pitcher_hits_allowed_lines=lines_for(blocks, "Total de Hits Permitidos por el Pitcher", subject=away_starter),
            home_pitcher_hits_allowed_lines=lines_for(blocks, "Total de Hits Permitidos por el Pitcher", subject=home_starter),
        )
        # Team run lines are read by team code from the copied Betcris blocks.
        away_name = snapshot["teams"][str(row["away"])]["name"]
        home_name = snapshot["teams"][str(row["home"])]["name"]
        game = replace(game, away_team_total_lines=lines_for(blocks, f"{away_label} Total del Equipo"),
                       home_team_total_lines=lines_for(blocks, f"{home_label} Total del Equipo"))
        result = analyze_mlb_game(game, RUNS, SEED)
        results[key] = {"event_id": GAME_IDS[key], "away": away_name, "home": home_name,
                        "starter_status": snapshot["starter_status"], "model": result.to_dict(),
                        "quoted_game_1": market["game_1_tokens"],
                        "quoted_relevant_markets": [b for b in blocks if any(word in b["market"] for word in
                            ("Total de Ponches", "Total de Hits Permitidos", "Total de Hits", "Total del Equipo"))
                            and "Entrada" not in b["market"]]}

    ids = (GAME_IDS["cws_cle"], GAME_IDS["nyy_tb"], GAME_IDS["sd_mil"])
    ticket = [{"event_id": event_id, "market": "game_total", "side": "over", "line": 5.5} for event_id in ids]
    ticket_games = [game_input_from_snapshot(snapshot, event_id) for event_id in ids]
    parlay = simulate_mlb_parlay(ticket_games, ticket, RUNS, SEED)
    print(json.dumps({"source_cutoff": snapshot["snapshot_utc"], "timezone": "America/Santo_Domingo",
                      "status": "EXPLORATORY_UNCALIBRATED", "simulations": RUNS, "seed": SEED,
                      "games": results, "example_three_game_total_parlay": parlay,
                      "example_three_game_total_parlay_lower_scoring": lower_scoring_ticket(ticket_games)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
