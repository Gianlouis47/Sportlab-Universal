"""Freeze a fresh 2026-10-03 pregame snapshot, adding Wild Card form.

Regular-season totals remain season baselines; completed Wild Card games are
appended only to the recent-form game logs. Historical snapshots stay intact.
Usage: python -m tools.refresh_mlb_oct3
"""

from __future__ import annotations

import datetime as dt
import gzip
import json
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "examples" / "mlb_stats_api_2026-10-03_asof_2026-10-02.json.gz"
OUT = ROOT / "examples" / "mlb_stats_api_2026-10-03_10am_rd.json.gz"
BASE = "https://statsapi.mlb.com/api/v1"


def get(path: str, **params) -> dict:
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    request = urllib.request.Request(url, headers={"User-Agent": "SportLab/0.1"})
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)


def main() -> None:
    with gzip.open(SOURCE, "rt", encoding="utf-8") as file:
        data = json.load(file)
    original_cutoff = data["snapshot_utc"]
    team_ids = {game[side] for game in data["games"] for side in ("away", "home")}
    wc_summary = {}
    for team_id in sorted(team_ids):
        rows = get("/schedule", sportId=1, teamId=team_id, startDate="2026-09-28",
                   endDate="2026-10-02", gameType="F")
        added = []
        for day in rows.get("dates", []):
            for game in day["games"]:
                away, home = game["teams"]["away"], game["teams"]["home"]
                own, opponent = (away, home) if away["team"]["id"] == team_id else (home, away)
                if game["status"]["abstractGameState"] != "Final" or "score" not in own or "score" not in opponent:
                    continue
                added.append({"date": day["date"], "for": own["score"], "against": opponent["score"],
                              "win": own["score"] > opponent["score"], "game_pk": game["gamePk"],
                              "game_type": "F"})
        data["teams"][str(team_id)]["games"].extend(added)
        data["teams"][str(team_id)]["games"].sort(key=lambda row: (row["date"], row.get("game_pk", 0)))
        wc_summary[str(team_id)] = added

    fresh = get("/schedule", sportId=1, date="2026-10-03", hydrate="probablePitcher,team")
    current_games = {game["gamePk"]: game for day in fresh.get("dates", []) for game in day["games"]}
    lineups = {}
    lineup_rates = {}
    weather = {}
    for game in data["games"]:
        live = current_games[game["id"]]
        game["status"] = live["status"]["detailedState"]
        game["start_utc"] = live["gameDate"]
        for side in ("away", "home"):
            game[side + "_starter"] = live["teams"][side].get("probablePitcher", {}).get("id")
        # The live feed has a different Stats API version and endpoint.
        request = urllib.request.Request(f"https://statsapi.mlb.com/api/v1.1/game/{game['id']}/feed/live",
                                         headers={"User-Agent": "SportLab/0.1"})
        with urllib.request.urlopen(request, timeout=25) as response:
            feed = json.load(response)
        lineups[str(game["id"])] = {side: feed.get("liveData", {}).get("boxscore", {}).get("teams", {})
                                    .get(side, {}).get("battingOrder", []) for side in ("away", "home")}
        lineup_rates[str(game["id"])] = {}
        for side, player_ids in lineups[str(game["id"])].items():
            if len(player_ids) != 9:
                continue
            players = []
            for player_id in player_ids:
                stats = get(f"/people/{player_id}/stats", stats="season", group="hitting",
                            season=2026, gameType="R")["stats"][0]["splits"]
                stat = stats[0]["stat"] if stats else {}
                players.append({"player_id": player_id, "pa": stat.get("plateAppearances", 0),
                                "k": stat.get("strikeOuts", 0)})
            total_pa = sum(p["pa"] for p in players)
            if total_pa:
                lineup_rates[str(game["id"])][side] = {"players": players,
                    "season_pa_weighted_k_rate": sum(p["k"] for p in players) / total_pa}
        weather[str(game["id"])] = feed.get("gameData", {}).get("weather", {})
    data["prior_snapshot_utc"] = original_cutoff
    data["snapshot_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    data["regular_season_as_of"] = data["as_of"]
    data["as_of"] = "2026-10-03"
    data["recent_form_scope"] = "regular-season games plus completed Wild Card games through 2026-10-02"
    data["wild_card_games_added"] = wc_summary
    data["lineups"] = lineups
    data["confirmed_lineup_k_rates"] = lineup_rates
    data["weather"] = weather
    OUT.write_bytes(gzip.compress((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), mtime=0))
    print(json.dumps({"snapshot_utc": data["snapshot_utc"], "wild_card_counts":
                      {data["teams"][tid]["name"]: len(rows) for tid, rows in wc_summary.items()},
                      "statuses": {str(g["id"]): g["status"] for g in data["games"]},
                      "lineups": lineups}, indent=2))


if __name__ == "__main__":
    main()
