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
    args = parser.parse_args()
    if args.command == "mlb":
        game = load_mlb_game(args.input)
        result = analyze_mlb_game(game, simulations=args.sims, seed=args.seed)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
