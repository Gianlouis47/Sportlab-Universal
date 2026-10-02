"""Dated MLB Stats API inputs for the existing SportLab MLB pipeline.

The API names probable starters; this adapter never upgrades them to confirmed.
No network call or database write happens when loading an existing snapshot.
"""

from __future__ import annotations

import datetime as dt
import json
import urllib.parse
import urllib.request
from statistics import mean

from sportlab.types import MLBGameInput, PitcherProfile, TeamProfile, WindowForm

BASE = "https://statsapi.mlb.com/api/v1"


def _get(path: str, **params):
    url = BASE + path + ("?" + urllib.parse.urlencode(params) if params else "")
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "SportLab/0.1"}), timeout=25) as response:
        return json.load(response)


def _stat(tid: int, group: str):
    rows = _get(f"/teams/{tid}/stats", stats="season", group=group, season=2026, gameType="R")["stats"][0]["splits"]
    return rows[0]["stat"] if rows else None


def _team_games(tid: int, as_of: str):
    data = _get("/schedule", sportId=1, teamId=tid, startDate="2026-03-01", endDate=as_of, gameType="R")
    rows = []
    for day in data["dates"]:
        for game in day["games"]:
            away, home = game["teams"]["away"], game["teams"]["home"]
            own, other = (away, home) if away["team"]["id"] == tid else (home, away)
            if game["status"]["abstractGameState"] == "Final" and "score" in own and "score" in other:
                rows.append({"date": day["date"], "for": own["score"], "against": other["score"],
                             "win": own["score"] > other["score"]})
    return sorted(rows, key=lambda x: x["date"])


def _pitcher(pid: int):
    season = _get(f"/people/{pid}/stats", stats="season", group="pitching", season=2026, gameType="R")
    logs = _get(f"/people/{pid}/stats", stats="gameLog", group="pitching", season=2026, gameType="R")
    splits = season["stats"][0]["splits"]
    starts = [
        {"date": x["date"], "bf": x["stat"]["battersFaced"], "ip": x["stat"]["inningsPitched"],
         "k": x["stat"]["strikeOuts"], "pitches": x["stat"].get("numberOfPitches")}
        for x in logs["stats"][0]["splits"] if x["stat"].get("gamesStarted")
    ]
    return {"season": splits[0]["stat"] if splits else None, "starts": sorted(starts, key=lambda x: x["date"])}


def fetch_snapshot(date: str) -> dict:
    """Fetch a 2026 postseason pregame snapshot after the regular season ended."""
    dt.date.fromisoformat(date)
    if date < "2026-09-29" or date > "2026-11-15":
        raise ValueError("this adapter currently supports only the 2026 postseason")
    schedule = _get("/schedule", sportId=1, date=date, hydrate="probablePitcher,team")
    games = schedule["dates"][0]["games"] if schedule["dates"] else []
    # No game on this day is represented by an empty list, never fabricated teams.
    ids = {g["teams"][side]["team"]["id"] for g in games for side in ("away", "home")}
    as_of = (dt.date.fromisoformat(date) - dt.timedelta(days=1)).isoformat()
    teams = {str(tid): {"name": next(g["teams"][side]["team"]["abbreviation"] for g in games for side in ("away", "home")
                                     if g["teams"][side]["team"]["id"] == tid),
                        "hitting": _stat(tid, "hitting"), "pitching": _stat(tid, "pitching"),
                        "games": _team_games(tid, as_of)} for tid in ids}
    starters = {}
    for game in games:
        for side in ("away", "home"):
            p = game["teams"][side].get("probablePitcher")
            if p and str(p["id"]) not in starters:
                starters[str(p["id"])] = {"name": p["fullName"], **_pitcher(p["id"])}
    all_teams = _get("/teams", sportId=1, season=2026)["teams"]
    hitting = [_stat(t["id"], "hitting") for t in all_teams]
    hitting = [x for x in hitting if x and x.get("plateAppearances")]
    league_k_rate = sum(x["strikeOuts"] for x in hitting) / sum(x["plateAppearances"] for x in hitting)
    return {"source": BASE, "snapshot_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "date": date,
            "as_of": as_of, "team_status": "CONFIRMED_HISTORICAL", "starter_status": "PROJECTED",
            "games": [{"id": g["gamePk"], "start_utc": g["gameDate"], "status": g["status"]["detailedState"],
                       "away": g["teams"]["away"]["team"]["id"], "home": g["teams"]["home"]["team"]["id"],
                       "away_starter": g["teams"]["away"].get("probablePitcher", {}).get("id"),
                       "home_starter": g["teams"]["home"].get("probablePitcher", {}).get("id")}
                      for g in games], "teams": teams, "starters": starters, "league_k_rate": league_k_rate}


def _window(rows: list[dict], n: int):
    if len(rows) < n:
        return None
    part = rows[-n:]
    return WindowForm(games=n, offense=mean(x["for"] for x in part),
                      defense_allowed=mean(x["against"] for x in part),
                      win_rate=mean(x["win"] for x in part))


def _team_profile(team: dict):
    hit, pitch = team["hitting"], team["pitching"]
    if not hit or not pitch or not hit.get("gamesPlayed") or not pitch.get("gamesPlayed"):
        raise ValueError(f"season team stats unavailable for {team['name']}")
    rows = team["games"]
    return TeamProfile(code=team["name"], season_offense=hit["runs"] / hit["gamesPlayed"],
                       season_defense_allowed=pitch["runs"] / pitch["gamesPlayed"],
                       l5=_window(rows, 5), l10=_window(rows, 10), l20=_window(rows, 20), l30=_window(rows, 30))


def _innings(value: str) -> float:
    whole, outs = value.split(".")
    return int(whole) + int(outs) / 3


def _pitcher_profile(entry: dict | None, opponent: dict, league_rate: float):
    if entry is None:
        return PitcherProfile(name="UNAVAILABLE")
    starts, season = entry["starts"], entry["season"]
    if not season or len(starts) < 10:
        return PitcherProfile(name=entry["name"])
    opp_hit = opponent["hitting"]
    return PitcherProfile(
        name=entry["name"], season_era=float(season["era"]),
        season_k_per_9=float(season["strikeoutsPer9Inn"]),
        expected_ip=mean(_innings(x["ip"]) for x in starts),
        expected_bf=mean(x["bf"] for x in starts),
        season_k_rate=season["strikeOuts"] / season["battersFaced"],
        opponent_k_rate=opp_hit["strikeOuts"] / opp_hit["plateAppearances"],
        league_k_rate=league_rate,
        bf_samples=tuple(x["bf"] for x in starts),
    )


def game_input_from_snapshot(snapshot: dict, game_id: int, *, total_lines=(6.5, 7.0, 8.5),
                             away_pitcher_k_lines=(4.5, 5.5, 6.5), home_pitcher_k_lines=(4.5, 5.5, 6.5)):
    game = next((g for g in snapshot["games"] if g["id"] == game_id), None)
    if game is None:
        raise ValueError(f"game {game_id} absent from snapshot")
    if game["status"] not in ("Scheduled", "Pre-Game", "Preview"):
        raise ValueError(f"game {game_id} is {game['status']}, not pregame")
    away, home = snapshot["teams"][str(game["away"])], snapshot["teams"][str(game["home"])]
    sp = snapshot["starters"]
    away_sp = sp.get(str(game["away_starter"])) if game["away_starter"] else None
    home_sp = sp.get(str(game["home_starter"])) if game["home_starter"] else None
    return MLBGameInput(event_id=game_id, away=_team_profile(away), home=_team_profile(home),
                        away_pitcher=_pitcher_profile(away_sp, home, snapshot["league_k_rate"]),
                        home_pitcher=_pitcher_profile(home_sp, away, snapshot["league_k_rate"]),
                        total_lines=tuple(total_lines), away_pitcher_k_lines=tuple(away_pitcher_k_lines),
                        home_pitcher_k_lines=tuple(home_pitcher_k_lines),
                        metadata={"source": snapshot["source"], "as_of": snapshot["as_of"],
                                  "snapshot_utc": snapshot["snapshot_utc"],
                                  "starter_status": snapshot["starter_status"],
                                  "away_starter_sample": len(away_sp["starts"]) if away_sp else 0,
                                  "home_starter_sample": len(home_sp["starts"]) if home_sp else 0})
