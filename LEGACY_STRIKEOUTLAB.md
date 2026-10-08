# Legacy StrikeoutLab material

The original MLB-only StrikeoutLab assets are archived under `legacy/strikeoutlab/`.

Preserved material includes:

- the tested TypeScript strikeout, calibration, backtest and decision logic;
- historical Supabase Edge Functions;
- historical Supabase migrations and schema evolution.

Rules:

- do not add new universal features there;
- migrate useful logic into `sportlab/` with parity tests;
- Neon SportLab is the primary dynamic database;
- Supabase StrikeoutLab is historical/auxiliary only;
- do not execute old migrations against Neon;
- do not remove legacy assets until their useful behavior has been migrated and validated.
