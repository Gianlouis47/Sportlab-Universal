# SportLab Universal — five primary sports

SportLab prioritizes MLB, NHL, basketball (NBA/WNBA/NCAAB), American football
(NFL/NCAAF) and soccer. These are domain checklists, not assertions that every
feature is implemented or that a data provider currently supplies it.

## Common contract

For each game preserve `sport`, league, season, event ID, timezone-aware
start, away/home, as-of timestamp, source, sample size and status
(CONFIRMED / PROJECTED / UNAVAILABLE). Compute scoring for and allowed in the
same units and season. Keep L5, L10, L20, L30, season, away/home and opponent
context; remove nested-window overlap before assigning weights. A NULL input
never becomes zero. For offense/defense, the notebook baseline is:

- away = (away scored per game + home allowed per game) / 2;
- home = (home scored per game + away allowed per game) / 2;
- total = away + home.

Use this only as a baseline: the sum of two offenses alone is not a game total,
because it ignores opposing run/goal/point prevention. Never equate a team
strength percentile with a win probability; 1–100 is the stored rating and
1–10 a derived display. Rate and compare home/away from real splits, never a
universal fixed home bonus. All weights require backtesting and calibration.

Analysis order: current confirmed lineup/roster -> historical form/matchup ->
context -> simulation -> contradictions/recheck -> price and available markets ->
classification. The currently available deterministic baselines are not Monte
Carlo models and cannot by themselves yield PRINCIPAL/SECUNDARIO selections.

## MLB

Runs: offense (runs scored, OBP, SLG, wOBA/wRC+ if sourced), run prevention,
season and nonoverlapping recent form, real venue splits, H2H with sample/date,
park/weather, defense, baserunning, starter innings and bullpen.

Starter: handedness; ERA, FIP/xFIP/xERA where sourced; K%, BB%, K-BB%,
whiff/CSW, pitch mix and velocity; pitch count, expected IP/BF, rest, health,
opponent handedness/contact and previous opponent starts with PA/IP and dates.
Lineup: expected PA by batting order, batter AVG/OBP/SLG and K% by handedness,
pitch-mix match, BvP with sample shrinkage, substitutions and availability.
Fielding: outfield/infield range, defensive conversion and errors; speed:
sprint speed, stolen-base pressure and baserunning. Team anecdotes such as
"Tampa is fast" are hypotheses until measured per roster/date and opponent.

Code: `sportlab/sports/mlb/matchups.py` computes PA-weighted Ks using lineup
strikeout rates and pitcher K%, shrinks BvP to the baseline and errors on
missing lineup. The existing MLB simulator uses that mean only when pitcher
K% and the opposing lineup are provided; otherwise it retains the K/9 baseline
and emits a contradiction. Its pitcher K distribution is still Poisson and
is not yet calibrated by pitch count, bullpen, lineup handedness or pitch mix.
Its runs model likewise does not yet adjust for defense, baserunning, weather
or bullpen. Never label these missing effects as included.

## NHL

Measure GF/G, GA/G, xGF/xGA, shots, high-danger chances, goalie save%
and confirmed starter, goalie workload/rest, team 5v5 play, lines/defensive
pairs, PP/PK, injuries/scratches, travel and B2B. Markets: regulation/including
overtime as separately defined, ML, totals, team goals, player shots/points,
goalie saves. Keep empty-net and overtime rules specific to the provider.
`sportlab/sports/nhl/baseline.py` currently only computes GF/GA baseline:
no goalie adjustment, score distribution or picks.

## Basketball

Team: points scored/allowed, possessions, pace, offensive/defensive rating,
effective FG%, turnovers, offensive boards, free throws, 3P frequency, paint,
matchup by position, lineup combinations, rest, travel and blowout risk.
Players: CONFIRMED availability and starts, expected minutes, per-minute
points/rebounds/assists/steals, usage, shot attempts, assists chances, rebound
chances, opponent scheme, fouls and rotation/injury limitations. Points,
rebounds, assists and steals are correlated through minutes and usage; do not
multiply prop probabilities as if independent. NBA/WNBA/NCAAB use separate
league baselines and game-length rules. `basketball/baseline.py` currently
offers only team points for/allowed and minutes-times-rate player means; no
variance, correlation or prop probabilities.

## American football

NFL/NCAAF: points for/allowed plus possessions, EPA/play, success and
explosive rates, red-zone and third-down performance, QB availability/health,
OL/DL match, pass rush, coverage/secondary, RB/WR/TE usage, turnovers,
special teams, injuries, weather, travel and short rest. For passing/rushing
and receiving props, model attempts, participation and role before efficiency;
never infer player props from the team points baseline. Leagues/years have
distinct rule and scoring environments. `football/baseline.py` is points
for/allowed only, not a full NFL model.

## Soccer

Use xG/xGA and goals for/against separately; shots, big chances, shot quality,
finishing/goalkeeping regression, confirmed XI/goalkeeper, pressing, formation,
set pieces, injuries/suspensions, rest, travel, home/away, league and
competition. Distinguish 90-minute 1X2 from draw-no-bet, qualification and
extra-time markets. A goals baseline is not a 1X2 probability: draw and
low-scoring distribution require their own calibrated model.
`soccer/baseline.py` operates in the input units supplied (goals or xG).

## Data and validation gates

Only current, authorized data may enter live analysis. Dynamic player/team
snapshots and market quotes belong in Neon; durable schema definitions and
model decisions belong in GitHub. Keep provider name, market identifier,
selection, side, line, price, capture time and settlement rules, including
Star Sport/Betcris/Superbets; do not assume that alternate K lines exist.

Next implementation gates for each sport: validated typed input and ingestion;
source/temporal checks; sport-specific calibrated model; seeded 10,000-draw
simulation with pushes when applicable; contradiction tests; actual quoted
price and settlement; historical backtest/calibration; then betting decision.
Missing critical inputs mean a provisional report or NO APUESTA.
