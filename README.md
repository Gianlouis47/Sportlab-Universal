# SportLab Universal

SportLab Universal is the reusable research, modeling, simulation, validation and learning engine for sports analysis.

Core workflow:

GOAL -> DATA -> ANALYSIS -> SIMULATION -> CONTRADICTION -> RECHECK -> VALIDATION -> DECISION -> RESULT -> POSTMORTEM

## Scope

The architecture is sport-agnostic. Current implementation starts with MLB and is designed to add NHL, NBA/WNBA/NCAAB, NFL/NCAAF, soccer, tennis, combat sports and other sports with sufficient data.

A screenshot is only a discovery input. If a ticket shows one pitcher prop, SportLab still evaluates the whole matchup and nearby useful markets when data exists: moneyline, game total, team totals, both starting pitchers, and relevant player props.

## Source of truth

### Neon SportLab — dynamic/structured data
Project: small-leaf-72827293
Database: sportlab

Use Neon for events, teams, athletes, live/current snapshots, odds/lines, simulations, results, postmortems, calibration tables and active learned rules.

### GitHub — code + durable knowledge
Use this repository for model code, simulation engines, weights/configuration, tests, mappings, research notes, methodology, small reference datasets, calibration reports and archived legacy assets.

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

## Legacy StrikeoutLab

StrikeoutLab is retained only as legacy/reference material while useful logic is migrated into the universal engine. New development belongs in sportlab/.

## 2026 MLB postseason research adapter

`python -m sportlab.cli mlb-api --date 2026-10-03 --game-id 849835 --save outputs/mlb-2026-10-03.json`
fetches a dated MLB Stats API snapshot and runs the existing MLB pipeline.
Use `--snapshot outputs/mlb-2026-10-03.json` to reproduce it offline. Add exact
market thresholds with `--total-lines`, `--away-k-lines`, and `--home-k-lines`.
Raw snapshots and model output belong in `outputs/`, which is ignored by Git.

This adapter marks starters **PROJECTED**, records the cutoff and sample sizes,
and simulates strikeouts by resampling batters faced in starts and applying
pitcher K/BF against the opposing lineup's team K/PA. A pitcher with fewer than
ten starts, or an unavailable pitcher, gets no K estimate. Its run projections
still use an exploratory league-average fallback and list that contradiction.
The model is **not calibrated** for betting and its outputs cannot establish
the 70% PRINCIPAL threshold. Confirm lineups, workloads, bullpen, park/weather,
and the exact sportsbook rules before using it for a decision.

For a Betcris parlay, save the exact event and selections in a JSON file:

```json
{"selections": [
  {"event_id": 849835, "market": "home_ml"},
  {"event_id": 849835, "market": "game_total", "side": "over", "line": 6.5},
  {"event_id": 849835, "market": "home_pitcher_ks", "side": "over", "line": 4.5}
]}
```

`python -m sportlab.cli mlb-parlay --snapshot outputs/mlb-2026-10-03.json --ticket ticket.json`
reports each leg, full wins per 1,000, and pushes without losses from shared
game draws. Run distributions report simulated min/max and p05–p95; those are
**observed simulation values**, never guaranteed game bounds. Hitter hits are
supported only after lineup confirmation. Team hits, pitcher hits allowed and
hitter total bases have exploratory distributions when their inputs exist;
RBI and hits+runs+RBI remain unestimated until an opportunity model is implemented.
See [the MLB parlay decision rules](docs/decisiones/mlb_parlays_2026_10_03.md)
and the [archived Betcris Padres–Brewers lines](examples/betcris_padres_brewers_2026-10-03.json).
