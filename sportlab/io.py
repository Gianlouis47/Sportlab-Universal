from __future__ import annotations
import json
from pathlib import Path
from sportlab.types import H2HProfile, HitterProfile, MLBGameInput, PitcherProfile, TeamProfile, WindowForm

def _window(d):
    return WindowForm(**d) if d else None

def _team(d):
    x = dict(d)
    for k in ("l5","l10","l20","l30"):
        x[k] = _window(x.get(k))
    return TeamProfile(**x)

def _pitcher(d):
    return PitcherProfile(**d)

def load_mlb_game(path: str | Path) -> MLBGameInput:
    d = json.loads(Path(path).read_text())
    return MLBGameInput(
        event_id=d.get("event_id"),
        away=_team(d["away"]),
        home=_team(d["home"]),
        away_pitcher=_pitcher(d["away_pitcher"]),
        home_pitcher=_pitcher(d["home_pitcher"]),
        h2h=H2HProfile(**d["h2h"]) if d.get("h2h") else None,
        total_lines=tuple(d.get("total_lines",[6.5,7,7.5,8,8.5])),
        away_team_total_lines=tuple(d.get("away_team_total_lines",[2.5,3.5,4.5])),
        home_team_total_lines=tuple(d.get("home_team_total_lines",[2.5,3.5,4.5])),
        away_pitcher_k_lines=tuple(d.get("away_pitcher_k_lines",[4.5,5,5.5,6,6.5])),
        home_pitcher_k_lines=tuple(d.get("home_pitcher_k_lines",[4.5,5,5.5,6,6.5])),
        hitters=tuple(HitterProfile(**x) for x in d.get("hitters", [])),
        hitter_hit_lines={int(k): tuple(v) for k, v in d.get("hitter_hit_lines", {}).items()},
        metadata=d.get("metadata",{}),
    )
