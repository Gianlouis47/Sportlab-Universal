"""Archive dated MLB hitter inputs for every Betcris yes-hit quote.

Usage: python -m tools.fetch_hitter_yes_snapshots
This command contacts MLB Stats API. The replay command uses only saved files.
"""

from __future__ import annotations

import json
import gzip
import re
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from sportlab.data.mlb_stats_api import fetch_hitter_snapshot
from tools.ingest_betcris_mlb import FILES, parse_source


ROOT = Path(__file__).resolve().parents[1]
MARKETS = ROOT / "examples" / "betcris_mlb_2026_10_03"
OUT = MARKETS / "hitter_yes_inputs.json.gz"
AS_OF = "2026-10-02"
OPPONENT = {
    "cws_cle": {145: (800048, "L"), 114: (696146, "L")},
    "atl_lad": {144: (669373, "L"), 119: (None, None)},
    "nyy_tb": {147: (656876, "R"), 139: (543037, "R")},
    "sd_mil": {135: (694819, "R"), 158: (592662, "L")},
}


def normalized(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", ascii_name)


def get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "SportLab/0.1"})
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)


def quoted_players() -> list[dict]:
    records = []
    for game_key, filename in FILES.items():
        blocks = parse_source((MARKETS / filename).read_text())["market_blocks"]
        total_bases = {}
        for block in blocks:
            if block["market"].endswith(": Bases Totales en el Partido"):
                for quote in block["quotes"]:
                    if quote["side"] == "over" and quote["line"] == .5:
                        total_bases[normalized(quote["subject"])] = quote["american_odds"]
        for block in blocks:
            if block["market"].endswith(": Jugador Batea al menos un Hit"):
                yes = next((quote for quote in block["quotes"] if quote["side"] == "yes"), None)
                if yes:
                    records.append({"game": game_key, "betcris_name": yes["subject"],
                                    "yes_hit_odds": yes["american_odds"],
                                    "over_0_5_total_bases_odds": total_bases.get(normalized(yes["subject"]))})
    return records


def main() -> None:
    people = get_json("https://statsapi.mlb.com/api/v1/sports/1/players?season=2026")["people"]
    by_name: dict[str, list[dict]] = {}
    for person in people:
        by_name.setdefault(normalized(person["fullName"]), []).append(person)
    quotes = quoted_players()

    def fetch(record: dict) -> dict:
        output = dict(record)
        candidates = by_name.get(normalized(record["betcris_name"]), [])
        person = next((person for person in candidates if person.get("currentTeam", {}).get("id")
                       in OPPONENT[record["game"]]), None)
        if not person:
            output["status"] = "NO_MATCHING_MLB_PLAYER_ON_GAME_TEAM"
            return output
        team_id = person.get("currentTeam", {}).get("id")
        pitcher_id, hand = OPPONENT[record["game"]][team_id]
        try:
            profile = fetch_hitter_snapshot(person["id"], team_id, AS_OF, hand)
            logs = get_json(f"https://statsapi.mlb.com/api/v1/people/{person['id']}/stats"
                            "?stats=gameLog&group=hitting&season=2026&gameType=R")["stats"][0]["splits"]
            appearances = [row for row in logs if row["date"] <= AS_OF]
            if not appearances:
                output["status"] = "NO_APPEARANCE_SAMPLE"
                return output
            output.update({"status": "PROJECTED_STARTER", "mlb_name": person["fullName"],
                           "player_id": person["id"], "team_id": team_id,
                           "opponent_pitcher_id": pitcher_id, "opponent_pitcher_hand": hand,
                           "appearance_sample": len(appearances),
                           "appearance_hit_yes_count": sum(row["stat"].get("hits", 0) > 0 for row in appearances),
                           "ab_samples": profile["ab_samples"],
                           "total_base_probs": profile["total_base_probs"]})
        except (KeyError, ValueError, IndexError, urllib.error.URLError) as error:
            output["status"] = "MLB_DATA_UNAVAILABLE"
            output["error_type"] = type(error).__name__
        return output

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(fetch, quotes))
    payload = json.dumps({"source": "MLB Stats API season/gameLog/statSplits and user Betcris text",
                          "as_of": AS_OF, "lineup_status": "PROJECTED",
                          "pitcher_exposure_assumption": .6, "players": results},
                         ensure_ascii=False, indent=2) + "\n"
    OUT.write_bytes(gzip.compress(payload.encode("utf-8"), mtime=0))
    print(f"{len(results)} quotes archived; statuses: " +
          str({status: sum(row["status"] == status for row in results)
               for status in sorted({row["status"] for row in results})}))


if __name__ == "__main__":
    main()
