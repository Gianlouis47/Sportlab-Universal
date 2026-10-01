# Tennis: technical ratings (1–10)

Show a side-by-side table for both players with offense, defense, serve, return,
volley, consistency, recent form and fit to the actual match surface as separate facets. Record the
preferred surface as a category. Record assessment date, source and sample size.
An external editorial rating is an observation to check, not a measured statistic.
Unknown facets remain unavailable; never infer them from the other facets.

| Facet | Statistical evidence to collect | What it describes |
| --- | --- | --- |
| Offense | Serve points won, hold rate, first/second serve, ace/DF, winners and return attack | Point creation and pressure |
| Defense | Return points won, break rate, rally and neutral-ball survival, movement | Point prevention and recovery |
| Serve | First and second serve points won, hold rate, aces/DF and serve placement | Serve quality; overlaps with offense, so avoid double counting |
| Return | First and second return points won, break rate and opponent-adjusted return games | Quality of return, distinct from rally defense |
| Volley | Net points won and net attempts, with a minimum sample | Net play quality, not just how often a player approaches |
| Consistency | Set-to-set variation, unforced errors relative to rally length, service games with multiple DFs, performance against comparable rivals | Stability across matches and sets |
| Recent form | Recent nonoverlapping matches, opponent level, surface and physical load | Current performance; a single upset is insufficient to score it |
| Surface fit | Surface-specific serve/return and match performance, opponent quality and sample size | Ability on today's court; preferred surface alone is not a numeric fit score |

Compute rates separately by hard/clay/grass, level of opponent, season and
recent nonoverlapping matches. Shrink small samples towards a surface-appropriate
baseline. Judge a high-error attacking style alongside winners, rally length
and opponent pressure; raw unforced-error counts are not a consistency score.

For the 2026-10-01 Munar/Faria example, the Google editorial assessments supplied
by the user are offense 5.5/7.5, defense 8.5/6.0, serve 6.0/7.5,
volley 6.5/6.5, consistency 7.5/5.5, and Tokyo hard-court adaptation 6.5/8.0
(Munar/Faria). Google says their preferred surfaces are clay/hard respectively.
These are editorial estimates, not calibrated measurements. The 2026 hard-court
records cited in the October 1 review were 8–5 Munar and 14–8 Faria, across
potentially different competition levels; Munar won their 2025 hard-court H2H.
The user subsequently supplied editorial return ratings of 8.0/6.0 and recent
form ratings of 8.5/7.0 (Munar/Faria). They complete the eight display facets
but remain uncalibrated opinions; no verified return-point or recent-match
sample was provided with them. Fritz was world No. 12 at the Tokyo match,
not world No. 10; he was the tournament's third seed.
As of October 1 Munar beat Fritz 6-7, 6-4, 6-3 in Tokyo after qualifying;
Faria beat Fery 6-4, 3-6, 6-4. These are observations, not 1–10 ratings.
Store each dated player/surface observation in `tennis.player_snapshots` in Neon:
`metrics.ratings` holds the eight nullable numeric facets, `metrics.preferred_surface`
the categorical surface, and `metrics.observations` separately holds verified
results and source URLs. Record editorial provenance in `metrics.rating_provenance`;
never write an inferred score where no calibrated scale exists.
Do not treat the suggested court pace as measured without a tournament-specific
pace source. These inputs require independent verification and calibration.
Sources for this snapshot: user-provided Google assessment (2026-10-01),
https://www.atptour.com/en/players/atp-head-2-head/jaume-munar-vs-jaime-faria/mu94/f0f2
https://www.atptour.com/en/tournaments/tokyo/329/overview,
https://www.reuters.com/sports/tennis/atp-roundup-alexander-zverev-carlos-alcaraz-advance-asia--flm-2026-10-01/
and https://elpais.com/deportes/resultados/tenis/.
Do not turn a rating difference into a match-win probability, set score,
games total or betting edge. Those require a separately calibrated service and
return model, injury/rest checks, confirmed event and market lines.
