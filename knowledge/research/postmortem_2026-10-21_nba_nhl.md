# Postmortem NBA y NHL — 21 de octubre de 2026

Revisado el 22 de octubre de 2026. Fecha de cartelera en America/Santo_Domingo.
Estado de aprendizaje: **OBSERVACION**. El predictor no fue recalibrado.

## Resultados por versión

| Cohorte publicada | Aciertos | Fallos |
| --- | ---: | ---: |
| NBA última lista, 14 líneas | 10 | 4 |
| NBA 11 candidatas de esa lista | 9 | 2 |
| NBA tres líneas condicionadas por rol | 1 | 2 |
| NBA lista anterior de 44 props, incluidos dos SOLO_REVISAR | 28 | 16 |
| NBA lista anterior excluyendo esos dos SOLO_REVISAR | 26 | 16 |
| NBA seis inclinaciones de total del partido | 4 | 2 |
| NHL ocho referencias publicadas | 6 | 2 |

Las versiones comparten selecciones: no sumar sus resultados como muestras independientes.
Los 44 umbrales analíticos NBA por equipo hicieron 34–10, pero no fueron líneas ejecutables verificadas.
En NHL, más de3.5 y menos de8.5 eran referencias alternativas; la captura posterior solo confirmó5.5 para el total central.
No se conoce el boleto, cuota ejecutada ni monto del usuario; no se calcula ROI.

## Fallos que deben conservarse

- Davion Mitchell menos de0.5 tapones: hizo1 en33minutos.
- Jalen Green menos de0.5 tapones: hizo1 en25minutos.
- Jaxson Hayes menos de1.5 asistencias, condicionado: hizo3 en26minutos.
- Rui Hachimura menos de1.5 pérdidas, condicionado: cometió3 en32minutos.
- Bucks–Wizards menos de239.5: total244; la captura de Appuesta238.5 también pierde.
- Jazz–Grizzlies más de241.5: total226; la captura de Appuesta242.5 también pierde.
- Buffalo Sabres más de1.5 goles: hizo1.
- Florida Panthers más de1.5 goles: hizo1.

## Mecanismos observados y límites

Philadelphia Flyers ganó3–1: Dan Vladar detuvo27 de28 tiros.
Ottawa Senators ganó5–1: tiros30–19; Ullmark detuvo17/18 y Ersson1/1 en relevo.
La producción de un solo equipo puede quedarse corta aunque el total conjunto cumpla.

Hayes pasó de una muestra antigua con18.3minutos de media a26minutos como titular de Utah.
La advertencia de cambio de rol era pertinente; un partido no cuantifica un ajuste ni valida una regla universal.
Un solo tapón derrota el Under0.5: frecuencia alta y cuota negativa no establecen probabilidad futura ni rentabilidad.
Una muestra L30/L50 amplia tampoco sustituye minutos, rol, rival y precio actuales.

## Evidencia y persistencia

ESPN mediante SportLab Sports Hub:13 finales verificados; marcador de calendario y resumen concuerdan en13/13.
La aritmética individual NBA de puntos, tiros de campo, triples y libres coincide con los puntos registrados.
Optimal no había actualizado esos game logs al21 de octubre; dos llamadas devolvieronHTTP503.
No se usaron registros de abril/mayo como resultados del21 de octubre.

- Neon: core.events, core.team_event_production y core.postmortems.
- review_key: sportlab:2026-10-21:full-slate:v1.
- Resumen: core.source_snapshots / SportLab_Universal / postmortem:2026-10-21:nba-nhl:full-slate:v1.
- PREGAME preservados: slate:2026-10-21:nba-nhl:conditional-selections:v1; slate:2026-10-21:nba:player-props-four-per-game:v1; slate:2026-10-21:nba:all-starters-wide-screen:v1.
- NBA: https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261021&limit=100
- NHL: https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard?dates=20261021&limit=100

No se borraron recomendaciones ni se reconstruyeron probabilidades a posteriori.
