# MLB notebook method — offense, defense and matchup ratings

The notebook method is preserved, but ratings are derived from real metrics rather than subjective manual scores.

## Primary raw values

For every team and cutoff:
- runs scored per game;
- runs allowed per game;
- run differential per game;
- scoring environment = runs scored + runs allowed;
- win rate;
- L5 / L10 / L20 / L30 / season;
- home and away splits;
- H2H current season;
- opponent-specific context.

The simplest baseline total is:

team_A_expected = (A_runs_scored + B_runs_allowed) / 2
team_B_expected = (B_runs_scored + A_runs_allowed) / 2
baseline_total = team_A_expected + team_B_expected

This is only a baseline. The production model then adds recent form, venue, starters, bullpen, lineup, park/weather and matchup effects.

## Rating scale

Store ratings on 1–100 for precision and interpretability.

Examples:
- offense_rating
- run_prevention_rating
- contact_rating
- power_rating
- plate_discipline_rating
- baserunning_speed_rating
- stolen_base_pressure_rating
- outfield_range_rating
- infield_range_rating
- defensive_conversion_rating
- bullpen_rating
- starter_rating

The rating should normally be a league-relative percentile from underlying metrics, not an arbitrary opinion.

Display may optionally show 1–10 as round(1–100 / 10), but the model uses raw metrics and/or 1–100 percentiles.

## Team traits

Traits such as "Tampa Bay is fast and covers the outfield well" must be represented by measurable components whenever data exists:
- sprint speed / team speed percentile;
- extra bases taken;
- stolen-base attempt rate and success;
- outs above average / range metrics;
- outfielder jump/range;
- defensive runs saved when available;
- balls-in-play conversion;
- contact rate / strikeout rate;
- baserunning value.

Narrative traits are stored as evidence-backed tags with source, date cutoff and confidence:
CONFIRMED / PROJECTED / UNAVAILABLE.

## Why ratings do not replace raw numbers

A 92/100 offense rating is useful for explanation, but the simulation should still use the underlying run rates, matchup and distributions. Ratings are summaries, not substitutes for data.
