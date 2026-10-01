# SportLab Universal roadmap

Primary sports: MLB, NHL, basketball (NBA/WNBA/NCAAB), American football
(NFL/NCAAF) and soccer. See `docs/primary_sports.md` for field-level scope and
the difference between a baseline and a complete, validated model.

## MLB 2.0

- [x] Season, non-overlapping L10/L20/L30, venue and historical H2H baseline.
- [x] 10,000-draw runs/K simulation; moneyline, totals, team totals and both starters' K lines.
- [x] PA-weighted opposing lineup K% and pitcher K%, with BvP sample shrinkage when supplied.
- [x] Missing-lineup K fallback explicitly noted as a contradiction.
- [ ] Automatic confirmed lineup ingestion, expected PA and workload/pitch-count calibration.
- [ ] Bullpen availability/fatigue and starter/bullpen run prevention.
- [ ] Batter handedness, pitch mix, whiff/CSW and expected contact.
- [ ] Fielding range, speed/baserunning, park and weather inputs with calibrated effects.
- [ ] Market calibration, backtesting and real-provider line/price validation.
- [ ] Explicit provisional/validated statuses and decision gate.

## NHL

- [x] Goals for/against deterministic matchup baseline.
- [ ] Confirmed goalie, 5v5 xGF/xGA, shots/high-danger and PP/PK.
- [ ] Rest, roster, lines, travel, 10,000 calibrated goal simulations.
- [ ] ML/regulation, totals, team totals and player/goalie props.

## Basketball

- [x] Points for/allowed baseline and minutes-based points/rebounds/assists/steals means.
- [ ] Pace, possession/efficiency, lineup and injury inputs by league.
- [ ] Correlated minutes/usage and player-stat simulation, price and calibration.

## American football

- [x] Points for/allowed baseline.
- [ ] QB, OL/DL, coverage, EPA, pace, personnel, weather and injuries.
- [ ] NFL/NCAAF calibrated score and player-usage simulations.

## Soccer

- [x] Goals or xG/xGA baseline.
- [ ] Confirmed XI, goalkeeper, league splits, finishing, set pieces and schedule.
- [ ] Calibrated low-scoring and draw model; regulation market settlement.

## Other sports

Tennis has a typed 1–10 offense/defense/consistency assessment and a side-by-side
comparison table; see `knowledge/tennis/ratings_method.md`. These editorial
ratings do not yield match probabilities or picks. Next: source current
surface-specific serve/return/variation metrics, calibrate against match logs,
then model points, games and sets with backtests and market settlement.
MMA/boxing, volleyball, handball and others follow after the five primary
sports have trustworthy data coverage and backtests.
