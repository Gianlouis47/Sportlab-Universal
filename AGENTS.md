# SportLab Universal — Codex operating rules

Do not recreate SportLab from scratch. Reuse and extend this repository.

## Mandatory workflow
GOAL -> DATA -> ANALYSIS -> SIMULATION -> CONTRADICTION -> RECHECK -> VALIDATION -> DECISION -> RESULT -> POSTMORTEM

## Data hierarchy
current confirmed data > recent Neon > historical auxiliary data > old baseline

Preserve as-of cutoffs. Never treat NULL as zero. Tag critical inputs as CONFIRMED / PROJECTED / UNAVAILABLE.

## Screenshot rule
A screenshot or creator ticket is a market-discovery input, not the analysis boundary. For every detected game, evaluate all relevant markets supported by data: side, game totals, team totals, both starters/goalies, relevant player props, matchup context, bullpen/rotation/special teams, venue/weather/rest/travel/injuries.

## MLB minimum
Use L5/L10/L20/L30/season without double-counting nested windows. Evaluate starters, expected IP/BF, K%, BB%, K-BB%, whiff/CSW when available, pitch mix, handedness, opponent contact/K profile, pitcher-vs-team history, lineup/BvP with shrinkage, bullpen, park/weather and team offense/run prevention.

## Repository vs database
Neon is the source of truth for dynamic structured records. GitHub is the source of truth for code, model definitions, tests, durable methodology, small reference datasets, mappings, research notes and archived legacy assets.

Never commit secrets or credentials. Never use certainty language.
