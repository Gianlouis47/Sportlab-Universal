# SportLab Universal — Codex operating rules

## Fundamento primordial obligatorio: proyección desde el jugador

**Antes de cualquier proyección o simulación de cualquier deporte**, aplicar [la regla universal de jugadores, unidades y matchup](knowledge/universal/player_first_projection_foundation.md), que también está activa en Neon `core.framework_rules` con clave `universal_player_first_projection_foundation`.

Jerarquía: **jugadores disponibles → participación y unidades → equipo → enfrentamiento específico contra el rival → proyección → simulación → probabilidad → decisión**. Los ratings individuales 1.0–10.0 con decimales son descriptivos; no son porcentajes ni sustituyen estadísticas. Estimar participación, titulares/suplentes, ataque/defensa, forma y duelos; integrar sin duplicar el baseline colectivo y sin inventar pesos. Nunca afirmar que un motor implementa o valida esta capa si todavía no lo hace. Prioridad primordial para MLB, NBA, NFL, NHL, fútbol, tenis y demás deportes.

Do not recreate SportLab from scratch. Reuse and extend this repository.

## Mandatory workflow
GOAL -> DATA -> ANALYSIS -> SIMULATION -> CONTRADICTION -> RECHECK -> VALIDATION -> DECISION -> RESULT -> POSTMORTEM

## Data hierarchy
current confirmed data > recent Neon > historical auxiliary data > old baseline

Preserve as-of cutoffs. Never treat NULL as zero. Tag critical inputs as CONFIRMED / PROJECTED / UNAVAILABLE.

## Screenshot rule
A screenshot or creator ticket is a market-discovery input, not the analysis boundary. For every detected game, evaluate all relevant markets supported by data: side, game totals, team totals, both starters/goalies, relevant player props, matchup context, bullpen/rotation/special teams, venue/weather/rest/travel/injuries.

## MLB minimum
Use L5/L10/L20/L30/season without double-counting nested windows. Evaluate starters, expected IP/BF, K%, BB%, K-BB%, whiff/CSW when available, pitch mix, handedness, opponent contact/K profile, pitcher-vs-team history, lineup/BvP with shrinkage, bullpen, park/weather and team offense/run prevention.

## Repository vs database
Neon is the source of truth for dynamic structured records. GitHub is the source of truth for code, model definitions, tests, durable methodology, small reference datasets, mappings, research notes and archived legacy assets.

Never commit secrets or credentials. Never use certainty language.
