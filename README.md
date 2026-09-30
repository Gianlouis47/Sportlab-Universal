# SportLab Universal

SportLab Universal is the reusable research, modeling, simulation, validation and learning engine for sports analysis.

Core workflow:

GOAL -> DATA -> ANALYSIS -> SIMULATION -> CONTRADICTION -> RECHECK -> VALIDATION -> DECISION -> RESULT -> POSTMORTEM

## Scope

The architecture is sport-agnostic. The active implementation starts with MLB and is designed to add NHL, NBA/WNBA/NCAAB, NFL/NCAAF, soccer, tennis, combat sports and other sports with sufficient data.

A screenshot is only a discovery input. If a ticket shows one pitcher prop, SportLab still evaluates the whole matchup and nearby useful markets when data exists: moneyline, game total, team totals, both starting pitchers and relevant player props.

## Runtime architecture

Python is the authoritative quantitative engine. New models, simulations and calibration logic belong in `sportlab/`.

The tested TypeScript StrikeoutLab engine and its historical Supabase functions/migrations are preserved under `legacy/strikeoutlab/` for audit and parity migration. They are not the active architecture.

SportLab runs locally in Codex; no Vercel deployment is required.

```bash
python -m pip install -e '.[dev]'
pytest -q
sportlab mlb --input examples/mlb_game.json --sims 10000
```

## Source of truth

### Neon SportLab — dynamic/structured data

Project: `small-leaf-72827293`  
Database: `sportlab`

Use Neon for events, teams, athletes, live/current snapshots, odds/lines, simulations, results, postmortems, calibration tables and active learned rules.

### GitHub — code + durable knowledge

Use this repository for model code, simulation engines, weights/configuration, tests, mappings, research notes, methodology, small reference datasets, calibration reports and archived legacy assets.

MLB durable knowledge lives in `knowledge/mlb/`.

Do not store API keys, database passwords, authentication tokens, personal data or large raw dumps in Git.

## Design rules

- Sporting reality comes before odds.
- Preserve temporal cutoff.
- NULL is not zero.
- Separate CONFIRMED / PROJECTED / UNAVAILABLE.
- Never call a deterministic projection a simulation.
- Default Monte Carlo size is 10,000 when inputs are sufficient.
- Search for credible routes of failure before classification.
- Persist model version, seed, inputs, outputs, contradictions and postmortem.
- Historical information is context, not automatic prediction.
