# Sportsbook market profiles

SportLab must model the market actually available to the user, not an idealized market.

Each sportsbook/provider can expose different alternate lines and bet directions.

Store provider profiles as configuration, not hard-coded assumptions.

For every observed market snapshot record:
- provider;
- timestamp;
- event;
- market type;
- player/team;
- line;
- over price;
- under price;
- whether alternate lines exist;
- whether both directions are offered;
- source/status.

Examples of provider differences may include:
- one book offering only a main strikeout line;
- another exposing alternate strikeout totals;
- some providers restricting one side/direction in a given interface.

SportLab should never assume availability from memory. The current screenshot/API/website snapshot wins.

The engine should calculate a full probability curve anyway:
P(K >= 3), P(K >= 4), P(K >= 5), ...
Then the market adapter maps that curve to whatever lines are actually offered.
