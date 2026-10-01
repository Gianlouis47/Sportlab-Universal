# SportLab knowledge layer

Store here durable, versioned knowledge that should not be high-frequency relational data.

Structure:

- `mlb/`: MLB frameworks, notebook method, pitcher profiles and sportsbook notes;
- future sport folders follow the same pattern;
- cross-sport architecture remains in `docs/`.

Good GitHub candidates:

- methodology and model notes;
- provider/source documentation;
- canonical mappings and aliases;
- small benchmark/fixture datasets;
- calibration reports and research summaries;
- postmortem writeups;
- model cards/version notes.

Keep in Neon:

- live/frequently changing event data;
- large historical stat tables;
- lineups/injuries/odds snapshots;
- simulation runs;
- results and structured postmortem rows;
- high-volume game logs.

Historical StrikeoutLab code and SQL belong in `legacy/strikeoutlab/`, not in the active knowledge layer.

Never commit secrets, credentials, personal information or giant raw dumps.
