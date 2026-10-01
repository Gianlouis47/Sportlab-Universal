# SportLab Universal — Architecture

## Language decision

Python is the authoritative quantitative engine.

Why:
- Monte Carlo, distributions, calibration, statistical modeling and data pipelines are simpler and more mature in Python.
- Codex can run the engine locally without deploying a web app.
- NumPy/Pandas/SciPy/Polars/Statsmodels/sklearn can be added as needed.
- The same engine can serve MLB, NHL, NBA, NFL, soccer, tennis and combat sports.

TypeScript remains useful for:
- legacy StrikeoutLab code that already has tests;
- parsers/adapters or future interfaces;
- strongly typed schemas at integration boundaries.

Rule: business/model logic has one source of truth. New quantitative formulas belong in Python. Useful TypeScript logic is migrated to Python with parity tests before the legacy version is retired.

## Local execution

No Vercel deployment is required.

Codex workflow:
1. ingest screenshot/text/market lines;
2. normalize teams, players and market names;
3. query Neon SportLab;
4. fetch/verify fresh public data when required;
5. build a typed game input;
6. run the local Python engine;
7. simulate normally 10,000 times;
8. run contradiction checks;
9. compare against the exact sportsbook line/price;
10. save outputs/results/postmortem to Neon;
11. save durable model/research artifacts to GitHub when appropriate.

## Data boundary

Neon = dynamic structured facts.
GitHub = code, model definitions, mappings, methodology, small reference datasets, calibration reports and versioned knowledge.

Never store secrets in GitHub.
