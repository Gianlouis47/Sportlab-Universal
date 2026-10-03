"""Index a user-supplied Betcris text export without inventing missing lines.

Usage: python tools/ingest_betcris_mlb.py SOURCE_DIR OUTPUT_JSON
SOURCE_DIR must contain cws_cle.txt, atl_lad.txt, nyy_tb.txt, sd_mil.txt.
The source files remain the authoritative record of every copied market.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


FILES = {
    "cws_cle": "cws_cle.txt",
    "atl_lad": "atl_lad.txt",
    "nyy_tb": "nyy_tb.txt",
    "sd_mil": "sd_mil.txt",
}
HEADING = re.compile(r"^.+ vs .+: .+$")
LINE = re.compile(r"^(Ov|Un) (\d+(?:\.\d+)?)$")
ODDS = re.compile(r"^[+-]\d+$")
HIT = re.compile(r"^(.+?) - (No|Sí|Yes)$")


def parse_source(raw: str) -> dict:
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if "Game 1" not in lines:
        raise ValueError("Game 1 section is missing")
    game_start = lines.index("Game 1")
    game_end = next((i for i in range(game_start + 1, len(lines)) if lines[i] == "First Half"), len(lines))
    game = lines[game_start:game_end]
    first_heading = next((i for i, line in enumerate(lines) if HEADING.match(line)), len(lines))
    blocks: list[dict] = []
    current: dict | None = None
    for line in lines[first_heading:]:
        if HEADING.match(line):
            current = {"market": line, "quotes": []}
            blocks.append(current)
        elif current is not None:
            current.setdefault("tokens", []).append(line)

    for block in blocks:
        tokens = block.pop("tokens", [])
        for i, token in enumerate(tokens[:-1]):
            match = LINE.match(token)
            hit = HIT.match(token)
            if match and ODDS.match(tokens[i + 1]):
                previous = tokens[i - 1] if i else None
                subject = previous if previous not in (None, "Over", "Under") and not ODDS.match(previous) else None
                block["quotes"].append({"subject": subject, "side": "over" if match[1] == "Ov" else "under",
                                         "line": float(match[2]), "american_odds": int(tokens[i + 1])})
            elif hit and ODDS.match(tokens[i + 1]):
                block["quotes"].append({"subject": hit[1], "side": "yes" if hit[2] in ("Sí", "Yes") else "no",
                                         "american_odds": int(tokens[i + 1])})
        # Nonstandard and unpriced markets remain readable in the source text.
    return {"game_1_tokens": game, "market_blocks": blocks,
            "parsed_line_quotes": sum(len(b["quotes"]) for b in blocks)}


def main() -> None:
    source = Path(sys.argv[1])
    out = Path(sys.argv[2])
    payload = {"source": "User supplied Betcris text; original odds are a dated snapshot, not a live feed",
               "timezone": "America/Santo_Domingo", "event_date_rd": "2026-10-03", "games": {}}
    for key, filename in FILES.items():
        raw = (source / filename).read_text(encoding="utf-8")
        payload["games"][key] = {"raw_source": str(source / filename), **parse_source(raw)}
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
