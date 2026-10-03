# Revisión MLB, 3 de octubre de 2026, 10:09 a. m. RD

Datos oficiales congelados a las 14:09:44 UTC. Todas las horas son de
`America/Santo_Domingo`. Las cuotas son las que el usuario copió de Betcris;
su hora exacta de captura no consta y no se verificó una cuota posterior.

## GOAL → DATA

| Juego (hora RD) | Estado MLB | Abridor visitante / local | Alineaciones |
|---|---|---|---|
| CWS @ CLE, 1:00 p. m. | Pre-Game | Hagen Smith / Parker Messick, probables | Nueve de CWS publicados; CLE no |
| ATL @ LAD, 4:00 p. m. | Scheduled | ATL sin probable / Tarik Skubal probable | Ninguna |
| NYY @ TB, 6:30 p. m. | Scheduled | Gerrit Cole / Drew Rasmussen, probables | Ninguna |
| SD @ MIL, 8:30 p. m. | Scheduled | Robbie Ray / Jacob Misiorowski, probables | Ninguna |

Hagen Smith tiene una sola apertura de temporada en el snapshot; no se
estima una prop de ponches para él. El calendario oficial no publica un
abridor de Atlanta; para la proyección de carreras de Dodgers se usa un
reemplazo de liga, que no basta para recomendarla.

Fuentes: [calendario MLB](https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-10-03&hydrate=probablePitcher,team),
[lineup CWS-CLE](https://statsapi.mlb.com/api/v1.1/game/849829/feed/live),
[boxscore CWS 30/9](https://statsapi.mlb.com/api/v1/game/849846/boxscore),
[boxscore ATL 1/10](https://statsapi.mlb.com/api/v1/game/849844/boxscore),
[boxscore NYY 30/9](https://statsapi.mlb.com/api/v1/game/849848/boxscore),
[boxscore SD 30/9](https://statsapi.mlb.com/api/v1/game/849842/boxscore).

Los últimos relevos registrados fueron: CWS Brazobán 16 lanzamientos, Kay 11,
Hicks 21 y Fedde 34 el 30/9; ATL Holmes 28, Suarez 11, Fuentes 13, Dodd 14 y
Sale 21 el 1/10; NYY Warren 19, Headrick 3 y Bednar 22 el 30/9; SD Rodríguez
21, Adam 11, Morejón 29 y Miller 19 el 30/9. CLE, LAD, TB y MIL no jugaron
Wild Card; el modelo no aplica un ajuste cuantificado de bullpen.

## ANALYSIS: libreta

Ataque = carreras anotadas por juego; defensa = carreras permitidas por juego
(menor es mejor). Las notas 1–10 son percentiles aproximados entre los 30
equipos de temporada regular, no probabilidades. L10 incluye Wild Card
terminados antes del corte; los promedios de temporada regular no se alteran.

| Equipo | Ataque R/J (nota) | Defensa RA/J (nota) | L10 R/RA | L20 R/RA | L30 R/RA |
|---|---:|---:|---:|---:|---:|
| CWS | 4.79 (8.8) | 4.44 (5.7) | 6.70/3.70 | 5.30/4.30 | 4.70/4.17 |
| CLE | 4.19 (2.9) | 4.12 (7.8) | 5.30/3.20 | 5.05/4.05 | 4.90/4.30 |
| ATL | 4.58 (7.5) | 3.86 (8.8) | 3.80/3.50 | 4.50/4.10 | 4.17/3.97 |
| LAD | 4.94 (9.1) | 3.70 (10.0) | 5.00/2.20 | 5.15/2.60 | 4.83/3.13 |
| NYY | 4.59 (7.8) | 3.73 (9.7) | 5.10/4.00 | 5.55/3.70 | 5.37/3.57 |
| TB | 4.54 (6.6) | 4.01 (8.4) | 3.80/3.20 | 4.75/2.90 | 4.80/3.40 |
| SD | 4.46 (5.3) | 4.20 (7.5) | 5.80/4.20 | 6.45/4.30 | 5.50/4.33 |
| MIL | 5.14 (9.7) | 3.82 (9.1) | 4.40/3.00 | 5.85/3.85 | 6.00/4.20 |

Contradicciones: CWS y SD llegan con ataque reciente superior a su temporada,
pero CLE y MIL conceden menos recientemente. Tampa llega con ataque L10 de
3.8, aunque la defensa NYY es fuerte; eso reduce la convicción en su total.
ATL debe enfrentar a Skubal, pero su rival al bate no tiene abridor conocido.

## SIMULATION → CONTRADICTION → RECHECK

Se ejecutaron **10,000** corridas por juego, semilla base **20261002** más
identificador MLB de cada partido. El modelo mezcla ataque propio con carreras
concedidas por rival, temporada/L5/L10/L20/L30, factor de abridor y localía
observada, y genera carreras con distribución gamma-Poisson (dispersión 0.28).
Los ponches se generan con distribución binomial a partir de una muestra de
bateadores enfrentados por apertura y una tasa K/BF que combina lanzador,
rival y liga. Para Messick se sustituyó la tasa de ponches de todo CWS (24.1%)
por la tasa histórica ponderada de los nueve bateadores anunciados (26.7%).
No se simulan por separado disponibilidad de relevistas, cambios tácticos,
posición en el orden, fuerza de rivales L10, clima o el abridor desconocido
de ATL. El esquema de extrainnings es aproximado y el modelo no está calibrado
contra temporadas anteriores; porcentajes siguientes son **exploratorios**.

### Todas las líneas exactas de ponches copiadas

Cada porcentaje es la frecuencia en 10,000 corridas. Las líneas fraccionarias
no tienen push. Ambas cuotas son snapshots de Betcris. En todas la decisión es
**NO APUESTA**: ninguna dirección llega a 70% y varios abridores son probables.

| Juego / lanzador | Línea | Más: cuota / P | Menos: cuota / P | Ruta de fallo del lado más probable |
|---|---:|---:|---:|---|
| CWS-CLE Messick | 6.5 | +110 / 59.7% | −140 / 40.3% | Sale antes o CWS hace contacto; con 4 BF menos el over cae aprox. a 39% |
| ATL-LAD Skubal | 6.5 | −119 / 57.3% | −111 / 42.8% | ATL alarga turnos y limita sus BF |
| NYY-TB Cole | 5.5 | +134 / 40.1% | −168 / 59.9% | El under falla si TB persigue lanzamientos y Cole trabaja profundo |
| NYY-TB Rasmussen | 6.5 | +121 / 47.6% | −151 / 52.4% | El under falla si NYY acumula K y aumenta su carga |
| SD-MIL Ray | 4.5 | +110 / 46.5% | −140 / 53.5% | El under falla con 5+ K; la cuota de over difiere del texto anterior que decía −105 |
| SD-MIL Misiorowski | 8.5 | +120 / 45.7% | −150 / 54.3% | El under falla si llega a 9 K con una salida larga |

No existe evidencia de líneas alternativas de ponches para estos partidos.

### Todas las líneas exactas de carreras por equipo copiadas

`P+` = probabilidad de más; `P−` = probabilidad de menos. Los pushes en línea
entera devuelven esa selección, sujeto a reglas Betcris. Todas las decisiones
son **NO APUESTA**: ninguna dirección supera 70%; LAD además no tiene abridor
rival anunciado. Las rutas de fallo se refieren al lado con mayor probabilidad
de cobro, no a una recomendación.

| Equipo | Línea | Más: cuota / P+ | Push | Menos: cuota / P− | Ruta de fallo del lado más probable |
|---|---:|---:|---:|---:|---|
| CWS | 3 | −105 / 55.2% | 14.8% | −114 / 29.9% | Messick y bullpen de CLE limitan a 0–2; 3 devuelve |
| CLE | 3.5 | −103 / 56.8% | 0% | −116 / 43.2% | Smith o relevos de CWS contienen a 0–3 |
| ATL | 3 | −112 / 46.6% | 16.1% | −107 / 37.3% | Skubal y bullpen LAD contienen a 0–2; 3 devuelve |
| LAD | 5 | +103 / 32.9% | 11.2% | −123 / 56.0% | El under falla con 6+ ante abridor ATL aún desconocido |
| NYY | 3 | −121 / 52.0% | 14.5% | +101 / 33.5% | Rasmussen y relevo TB contienen a 0–2; 3 devuelve |
| TB | 3.5 | −107 / 51.4% | 0% | −112 / 48.6% | Cole y bullpen NYY contienen a 0–3 |
| SD | 2.5 | −116 / 67.6% | 0% | −103 / 32.4% | Misiorowski y bullpen MIL dejan a SD en 0–2 |
| MIL | 4 | −121 / 46.1% | 13.5% | +101 / 40.4% | Ray y bullpen SD contienen a 0–3; 4 devuelve |

## VALIDATION → DECISION: alternativa visible y combinada ilustrativa

Los tres **totales completos alternativos** de más de 5.5 estaban visibles
en capturas, con cuotas −196 (CWS-CLE), −205 (NYY-TB) y −215 (SD-MIL).
Ninguna es alternativa de K. El modelo arroja 76.4%, 71.2% y 76.3%
respectivamente; fallan si ambos equipos suman cinco carreras o menos.
Al bajar simultáneamente 15% las medias de carreras, esas frecuencias caen
a 66.6%, 62.3% y 66.9%: **no son PRINCIPALES robustas**.

La combinada ilustrativa de esas tres líneas completas cobra **4,149 de
10,000** veces (41.49%) en el escenario base; **2,781 de 10,000** (27.81%)
con −15% de carreras y **5,545 de 10,000** (55.45%) con +15%. Cuota decimal
combinada de snapshot ≈3.292, punto de equilibrio ≈30.38%; la sensibilidad
baja por debajo de ese punto. Los partidos se suponen independientes; dentro
de cada partido, los mercados de carreras comparten las mismas corridas.
No hay push en estas tres líneas de 5.5. **Decisión: NO APUESTA** con el
estado actual del modelo. El intervalo binomial de Monte Carlo del 41.49%
es aproximadamente 40.5–42.5%; no incluye incertidumbre del modelo.

## RESULT → POSTMORTEM

Respecto al 2/10, se incorporaron dos juegos Wild Card de CWS, tres de ATL,
dos de NYY y dos de SD a ventanas recientes; se confirmó lineup de CWS y su
K/PA proyectado subió de 24.1% a 26.7%. Messick over 6.5 K pasó de 49.1%
a 59.7%, aún bajo el umbral. Padres over 2.5 pasó de 67.4% a 67.6%.
ATL sigue sin abridor anunciado; persiste el límite del modelo de carreras.
La comparación definitiva con marcadores reales queda pendiente de que
finalicen los juegos. La corrida no valida por sí sola un pronóstico.
