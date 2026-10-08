from __future__ import annotations
import argparse, json
from sportlab.io import load_mlb_game
from sportlab.pipelines.mlb_pregame import analyze_mlb_game
from sportlab.models.threshold_frequency import EventFrequency, estimate_threshold

def main() -> None:
    parser = argparse.ArgumentParser(prog="sportlab")
    sub = parser.add_subparsers(dest="command", required=True)
    mlb = sub.add_parser("mlb")
    mlb.add_argument("--input", required=True)
    mlb.add_argument("--sims", type=int, default=10_000)
    mlb.add_argument("--seed", type=int, default=20260930)
    threshold = sub.add_parser("threshold", help="Exploratory frequency for one precisely defined market")
    threshold.add_argument("--event", required=True, help="Canonical settlement event, period and market")
    threshold.add_argument("--opponent-event", required=True,
                           help="Canonical event opponent allows; must match --event exactly")
    threshold.add_argument("--subject-hits", type=int, required=True)
    threshold.add_argument("--subject-games", type=int, required=True)
    threshold.add_argument("--opponent-allowed-hits", type=int, required=True)
    threshold.add_argument("--opponent-games", type=int, required=True)
    threshold.add_argument("--league-rate", type=float, required=True)
    threshold.add_argument("--prior-games", type=float, default=20.0)
    threshold.add_argument("--sims", type=int, default=10_000)
    threshold.add_argument("--seed", type=int, default=20261008)
    args = parser.parse_args()
    if args.command == "mlb":
        game = load_mlb_game(args.input)
        result = analyze_mlb_game(game, simulations=args.sims, seed=args.seed)
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    elif args.command == "threshold":
        result = estimate_threshold(
            EventFrequency(args.subject_hits, args.subject_games, args.event),
            EventFrequency(args.opponent_allowed_hits, args.opponent_games, args.opponent_event),
            args.league_rate, prior_games=args.prior_games, simulations=args.sims, seed=args.seed,
        )
        print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
