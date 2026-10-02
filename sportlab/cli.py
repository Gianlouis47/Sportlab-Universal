from __future__ import annotations
import argparse, json
from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_pregame import analyze_mlb_game

def main() -> None:
    parser = argparse.ArgumentParser(prog="sportlab")
    sub = parser.add_subparsers(dest="command", required=True)
    mlb = sub.add_parser("mlb")
    mlb.add_argument("--input", required=True)
    mlb.add_argument("--sims", type=int, default=10_000)
    mlb.add_argument("--seed", type=int, default=20260930)
    api = sub.add_parser("mlb-api", help="2026 postseason MLB Stats API snapshot and exploratory model")
    api.add_argument("--date", help="MLB schedule date, e.g. 2026-10-03")
    api.add_argument("--snapshot", help="load saved snapshot JSON without network calls")
    api.add_argument("--save", help="save a dated input snapshot JSON")
    api.add_argument("--game-id", required=True, type=int)
    api.add_argument("--total-lines", type=float, nargs="+", default=[6.5, 7.0, 8.5])
    api.add_argument("--away-k-lines", type=float, nargs="+", default=[4.5, 5.5, 6.5])
    api.add_argument("--home-k-lines", type=float, nargs="+", default=[4.5, 5.5, 6.5])
    api.add_argument("--sims", type=int, default=10_000)
    api.add_argument("--seed", type=int, default=20261002)
    args = parser.parse_args()
    if args.command == "mlb":
        game = load_mlb_game(args.input)
        result = analyze_mlb_game(game, simulations=args.sims, seed=args.seed)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    elif args.command == "mlb-api":
        from pathlib import Path
        from sportlab.data.mlb_stats_api import fetch_snapshot, game_input_from_snapshot
        if not args.snapshot and not args.date:
            parser.error("mlb-api requires --date or --snapshot")
        snapshot = json.loads(Path(args.snapshot).read_text()) if args.snapshot else fetch_snapshot(args.date)
        if args.save:
            Path(args.save).write_text(json.dumps(snapshot, indent=2))
        game = game_input_from_snapshot(snapshot, args.game_id, total_lines=args.total_lines,
                                        away_pitcher_k_lines=args.away_k_lines,
                                        home_pitcher_k_lines=args.home_k_lines)
        result = analyze_mlb_game(game, simulations=args.sims, seed=args.seed)
        print(json.dumps({"metadata": game.metadata, "status": "EXPLORATORY_UNCALIBRATED",
                          "result": result.to_dict()}, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
