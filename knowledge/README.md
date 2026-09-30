# SportLab knowledge layer

Store here durable, versioned knowledge that should not be high-frequency relational data.

Good GitHub candidates:
- methodology and model notes
- provider/source documentation
- canonical mappings and aliases
- small benchmark/fixture datasets
- calibration reports and research summaries
- postmortem writeups
- model cards/version notes
- legacy SQL/functions for audit or migration

Keep in Neon:
- live/frequently changing event data
- large historical stat tables
- lineups/injuries/odds snapshots
- simulation runs
- results and structured postmortem rows
- high-volume game logs

Never commit secrets, credentials, personal information or giant raw dumps.
