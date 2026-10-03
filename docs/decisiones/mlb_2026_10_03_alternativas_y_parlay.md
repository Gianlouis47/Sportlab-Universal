# MLB 3 de octubre de 2026: líneas alternativas y props

**Corte pregame:** 2 de octubre, 18:07 RD (22:07 UTC). Datos de temporada
regular 2026 de MLB Stats API; snapshot fechado en
`examples/mlb_stats_api_2026-10-03_asof_2026-10-02.json.gz`. Las cuotas son
las que copió el usuario de Betcris, sin hora exacta de captura. Los cuatro
textos originales están en `examples/betcris_mlb_2026_10_03/`; los totales
alternativos visibles en capturas previas están en
`full_game_alternatives_from_screenshots.json`. El replay exacto de 10,000
corridas está en `model_replay.json`; se genera con
`python -m tools.replay_betcris_mlb`. Semilla: `20261002`.

Estado MLB en el recheck: `Scheduled` para los cuatro juegos. Los abridores
son **probables**, no confirmados. CWS Hagen Smith @ CLE Parker Messick,
ATL abridor **NO DISPONIBLE** @ LAD Tarik Skubal, NYY Gerrit Cole @ TB Drew
Rasmussen y SD Robbie Ray @ MIL Jacob Misiorowski. Las alineaciones no están
confirmadas. Horarios RD: 1:00, 4:00, 6:30 y 8:30 p. m., respectivamente.

## Libreta: producción y prevención

Temporada regular 2026. L10 incluye sus propios diez juegos; no se suma a la
temporada. Ataque 1–10 ordena carreras anotadas por juego y defensa 1–10
ordena, en dirección inversa, carreras permitidas entre 30 equipos.

| Equipo | Carreras/G | Permitidas/G | L10 a favor/en contra | Ataque | Defensa |
| --- | ---: | ---: | ---: | ---: | ---: |
| White Sox | 4.79 | 4.44 | 6.50 / 4.30 | 8.8 | 5.7 |
| Guardians | 4.19 | 4.12 | 5.30 / 3.20 | 2.9 | 7.8 |
| Braves | 4.58 | 3.86 | 4.00 / 3.90 | 7.5 | 8.8 |
| Dodgers | 4.94 | 3.70 | 5.00 / 2.20 | 9.1 | 10.0 |
| Yankees | 4.59 | 3.73 | 4.60 / 4.50 | 7.8 | 9.7 |
| Rays | 4.54 | 4.01 | 3.80 / 3.20 | 6.6 | 8.4 |
| Padres | 4.46 | 4.20 | 6.30 / 4.50 | 5.3 | 7.5 |
| Brewers | 5.14 | 3.81 | 4.40 / 3.00 | 9.7 | 9.1 |

En robos por juego, Rays 1.012 y Yankees 0.950: Tampa fue ligeramente más
rápido en esta medida. No hay una medida verificada aquí de alcance de los
jardineros; por tanto, no se afirma que Tampa atrape más elevados. La
temporada favorece al ataque de Milwaukee, pero Padres promedió 6.30
carreras en L10: el abridor, bullpen y lineup pueden alterar el total.

## Comparación de alternativas visibles

Los valores son **aciertos del modelo exploratorio por 1,000 corridas**, no
probabilidades deportivas calibradas. En la prueba de sensibilidad se bajó
15 % la media de carreras de ambos equipos y se ejecutaron otras 10,000
corridas; no representa un pronóstico sobre el clima.

| Selección exacta visible | Cuota | Modelo base / 1,000 | Media −15 % / 1,000 | Decisión |
| --- | ---: | ---: | ---: | --- |
| CWS–CLE más de 5.5 carreras | −196 | 769 | 664 | NO APUESTA todavía |
| NYY–TB más de 5.5 carreras | −205 | 716 | 624 | NO APUESTA todavía |
| SD–MIL más de 5.5 carreras | −215 | 767 | 671 | NO APUESTA todavía |
| ATL–LAD más de 7 carreras | −196 | 524; push 114 | No calculado | NO APUESTA |

Los mínimos para equilibrar esas primeras tres cuotas, ignorando margen y
push, son 662, 672 y 683 aciertos por 1,000. En el escenario de menor
anotación, Yankees–Rays y Padres–Brewers quedan por debajo. Los totales
principales de 7 carreras son otro mercado: más de 7 cobra solo con 8 o más;
exactamente 7 puede devolver. Bajar la línea aumenta la frecuencia de acierto
y también encarece la cuota.

| Juego | ML favorito en Betcris | ML modelo / 1,000 | Total principal más de / 1,000 |
| --- | ---: | ---: | ---: |
| CWS @ CLE | CLE −155 | CLE 518 | 7: 576; push 113 |
| ATL @ LAD | LAD −223 | LAD 572 | 8.5: 443 |
| NYY @ TB | TB −130 | TB 505 | 7: 507; push 121 |
| SD @ MIL | MIL −208 | MIL 557 | 7: 581; push 108 |

El abridor de Atlanta está sin anunciar; el modelo de carreras usa un
reemplazo promedio para él. Estos ML no dan ventaja clara frente al precio.

## Props exactos del texto Betcris

| Mercado | Cuota | Modelo / 1,000 | Ruta de fallo |
| --- | ---: | ---: | --- |
| Messick más de 6.5 K | +110 | 491 | Pocos bateadores enfrentados o contacto de CWS |
| Skubal más de 6.5 K | −119 | 570 | Atlanta reduce K; salida acortada |
| Cole menos de 5.5 K | −168 | 600 | Tampa ofrece más turnos y Cole llega a 6 K |
| Rasmussen menos de 6.5 K | −151 | 521 | Yankees acumula K pese a una salida normal |
| Ray más de 4.5 K | +110 | 463 | Salida temprana; esta cuota cambia respecto al texto previo (−105) |
| Misiorowski más de 8.5 K | +120 | 457 | Necesita 9; un límite de lanzamientos lo frena |
| White Sox más de 6.5 hits | −140 | 581 | Messick y relevistas reducen contacto |
| Guardians más de 7.5 hits | −130 | 535 | Smith y relevistas mantienen hits en 7 o menos |
| Braves más de 7.5 hits | +105 | 495 | Skubal limita hits |
| Dodgers más de 8.5 hits | +115 | 430 | Abridor ATL aún desconocido; modelo débil |
| Yankees más de 6.5 hits | −130 | 526 | Rasmussen puede controlar el contacto |
| Rays más de 7.5 hits | −130 | 580 | Cole puede ir profundo |
| Padres más de 6.5 hits | −110 | 389 | Misiorowski y relevo limitan hits |
| Brewers más de 7.5 hits | −130 | 528 | Ray y relevo pueden limitar hits |
| Cole más de 4.5 hits permitidos | −159 | 679 | Una salida más corta reduce la exposición |
| Ray más de 3.5 hits permitidos | −120 | 705 | Cuatro bateadores menos bajan el modelo a ≈557 |

También están archivados ambos lados de cada línea, los hits permitidos de
Messick, Skubal, Rasmussen y Misiorowski, y los totales de carreras de cada
equipo. Ningún prop de ponches supera el umbral deportivo de 70 %. El 705/1,000
de Ray es frágil ante su duración; **no se clasifica PRINCIPAL**. Hagen Smith
tiene menos de diez aperturas en la muestra y Betcris no mostró un prop suyo.

Los mercados de hit de bateador, bases totales, hits+carreras+impulsadas,
primeras cinco entradas y entradas individuales se conservaron textualmente.
Por instrucción del usuario, los bateadores habituales se tratan como
**titulares proyectados** para la sección siguiente; la MLB aún no publicó el
orden al bate. Hits+carreras+impulsadas y parciales requieren un modelo
conjunto que todavía no existe: `NO ESTIMABLE / NO APUESTA`.
Más de 0.5 bases totales implica al menos un hit, sujeto a las mismas reglas
de elegibilidad de Betcris. No se presume que haya líneas alternativas de K:
solo se usan las seis que figuran en los textos.

## Bateadores habituales: principales proyectadas

Se archivaron las 60 líneas de «al menos un hit» del texto Betcris y sus
entradas de MLB en `hitter_yes_inputs.json.gz`; se reproducen con
`python -m tools.replay_hitter_yes` en `hitter_yes_replay.json`. La simulación
usa 10,000 corridas, semilla `20261002 + player_id`, distribución histórica
de turnos al bate, frecuencia de tipos de hit, split por mano del abridor y
un ajuste al hits/BF de ese abridor con prior de 200 BF. Se supone 60 % de
turnos frente al abridor. Para Atlanta no hay abridor anunciado; para Hagen
Smith, con menos de diez aperturas, se omite ese ajuste. Es un modelo
exploratorio **sin calibración fuera de muestra**; las cifras suponen que el
jugador comienza el partido.
El roster `active` de MLB para el 3 de octubre incluye a Chourio y Simpson
con estatus `A`; esto respalda su disponibilidad proyectada, pero el orden
al bate de ambos juegos aún aparece vacío en el feed oficial.

| Apuesta exacta | Cuota | Juegos con hit / apariciones 2026 | L10/L20/L30 con hit | Modelo / 1,000 | Si pierde un turno / 1,000 | Clasificación |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Jackson Chourio, sí hit vs Padres | −220 | 94/127 (74.0 %) | 7/10, 14/20, 22/30 | 747 | 641 | PRINCIPAL PROYECTADA, solo si inicia |
| Chandler Simpson, sí hit vs Yankees | −224 | 107/151 (70.9 %) | 8/10, 14/20, 22/30 | 731 | 618 | PRINCIPAL PROYECTADA, solo si inicia |
| Yandy Díaz, sí hit vs Yankees | −238 | 106/154 (68.8 %) | No usado | 745 | 642 | SECUNDARIA: temporada bajo 70 % |
| Junior Caminero, sí hit vs Yankees | −235 | 119/162 (73.5 %) | No usado | 699 | 576 | SECUNDARIA: modelo bajo 70 % |
| Fernando Tatis Jr., sí hit vs Brewers | −190 | 113/159 (71.1 %) | No usado | 665 | 551 | NO APUESTA: Misiorowski reduce el escenario |
| Shohei Ohtani, sí hit vs Braves | −235 | 92/135 (68.1 %) | No usado | 696 | 580 | NO APUESTA: abridor ATL desconocido |

El nombre famoso o la cuota negativa no sustituye el umbral. La posición en
el orden puede cambiar los turnos: al restar uno a cada jugador, los dos
principales proyectados bajan de 70 %. Son selecciones **individuales** bajo
la hipótesis de turnos habituales, no una garantía de que jugarán o pegarán
hit. Ninguna línea alternativa de más de 0.5 bases totales para esos dos
apareció en los textos.

Una combinada de Chourio sí hit y Simpson sí hit a las cuotas copiadas tendría
precio decimal ≈2.104 y exige 475/1,000 para equilibrar. El replay produjo
5,473/10,000 (547/1,000) con turnos habituales y 3,942/10,000
(394/1,000) si ambos pierden un turno. Son partidos distintos y se supuso
independencia entre ellos. **No se recomienda unirlos** antes de revisar
posición de bateo y precio final.

## Criba completa de mercados modelables y boleto de hasta 15

Se aplicó el corte de 70 % a cada lado exacto de los ML, run lines, totales
completos alternativos visibles, totales e hits de equipo, ponches e hits
permitidos de abridor, 60 mercados sí/no hit y los mercados de bases totales
de esos bateadores. La misma jugada «sí hit» y «más de 0.5 bases totales» se
cuenta una sola vez si coinciden sus reglas de liquidación. Este es el
**conjunto completo de selecciones distintas que superó 70 % en el modelo
base**, no una lista de principales:

| Selección | Cuota | Modelo base / 1,000 | Contradicción decisiva |
| --- | ---: | ---: | --- |
| CWS–CLE más de 5.5 carreras | −196 | 769 | Con medias −15 %: 664 |
| NYY–TB más de 5.5 carreras | −205 | 716 | Con medias −15 %: 624 |
| SD–MIL más de 5.5 carreras | −215 | 767 | Con medias −15 %: 671 |
| Robbie Ray más de 3.5 hits permitidos | −120 | 705 | Cuatro BF menos: ≈557 |
| Chase DeLauter sí hit | −190 | 711 | Histórico: 654; un AB menos: 593 |
| Chase Meidroth sí hit | −170 | 702 | Histórico: 682; un AB menos: 583 |
| Freddie Freeman sí hit | −220 | 706 | Histórico: 673; abridor ATL desconocido |
| Michael Harris II sí hit / más de 0.5 bases | −180 | 703 | Histórico: 677; un AB menos: 586 |
| Chandler Simpson sí hit | −224 | 731 | Histórico: 709; un AB menos: 618 |
| Yandy Díaz sí hit | −238 | 745 | Histórico: 688; un AB menos: 642 |
| Jackson Chourio sí hit | −220 | 747 | Histórico: 740; un AB menos: 641 |
| Steven Kwan menos de 1.5 bases | −183 | 704 | Histórico: 642; rival Smith solo una apertura |
| Manny Machado menos de 1.5 bases | −210 | 709 | Histórico: 646; modelo más alto que temporada |

Para Kwan y Machado, un turno menos aumenta la frecuencia del **under**, pero
su histórico de temporada no llega a 70 %. Ningún ML, run line, total de
equipo, hit de equipo o ponche cruzó 70 % en su línea exacta. Los mercados de
entradas, primeras cinco, impulsadas, H+R+RBI, bases robadas y otras
proposiciones del texto que carecen de un modelo conjunto quedan
`NO ESTIMABLE / NO APUESTA`; no se les asignó un porcentaje usando la cuota.

Si se añadiesen a la combinada los tres overs alternativos de 5.5 a Simpson
sí hit y Chourio sí hit, sería un boleto de **cinco**, dentro del máximo 15.
La correlación entre hit y over del mismo partido se aproximó con los pares
observados de 2026 (Chourio: 74 coincidencias de 127 juegos; Simpson: 81 de
151), archivados en `hitter_total_historical_pairs.json`. Los partidos
distintos se trataron como independientes. `python -m tools.replay_five_leg`
reproduce 10,000 corridas de resultados conjuntos:

| Boleto de cinco | Combinación completa / 10,000 | Por 1,000 |
| --- | ---: | ---: |
| Medias y turnos habituales | 2,417 | 242 |
| 15 % menos carreras y un AB menos por bateador | 1,141 | 114 |

Cuotas del snapshot: −196, −205, −215, −224 y −220; decimal combinado
≈6.926, umbral de equilibrio ≈144/1,000. El escenario adverso queda bajo
ese precio. **No es una combinada PRINCIPAL ni una recomendación de cinco
selecciones**. Añadir más piernas para llegar a 15 reduciría todavía más la
probabilidad de cobrar todas.

## Boleto de estudio, no selección recomendada

Tres overs **visibles** de 5.5 carreras: CWS–CLE −196, NYY–TB −205 y
SD–MIL −215. Las cuotas combinadas del snapshot equivalen aproximadamente
a decimal 3.292 y requieren 303.8 aciertos de cada 1,000 para equilibrar.

| Escenario | Tres de tres en 10,000 | Equivalente por 1,000 | Al menos una falla |
| --- | ---: | ---: | ---: |
| Modelo base, semilla 20261002 | 4,244 | 424 | 5,756 |
| Medias de carrera −15 %, semilla 20261002 + id + 42 | 2,801 | 280 | 7,199 |

Los tres juegos se simulan independientemente. El modelo comparte carreras
para ML y totales dentro de un juego, pero K, hits de equipo y hits permitidos
no están acoplados con las carreras; por ello no se propone un parlay de esos
mercados como si su probabilidad conjunta estuviera validada. Los 4,244 y
2,801 son conteos realmente ejecutados, **no** garantía de cobro. La brecha
entre escenarios supera ampliamente el error de muestreo de 10,000 corridas.

**Decisión pregame:** Chourio sí hit y Simpson sí hit son las dos
`PRINCIPALES PROYECTADAS` porque el histórico y el modelo de cada mercado
superan 70 % bajo turnos habituales. No hay principal para ML, total del
juego, total de equipo o ponches. Los dos boletos combinados ilustrados están
en `NO APUESTA` por sensibilidad a turnos o carreras; las cuotas pueden
cambiar. Al inicio se sella este corte como pregame;
después se registran live y final por separado y se hace postmortem.
