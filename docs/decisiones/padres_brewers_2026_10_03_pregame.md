# Padres @ Brewers — análisis pregame archivado

Fecha RD: 3 de octubre de 2026, 8:30 p. m. Corte de datos: 2 de octubre,
18:07 RD. Fuentes: MLB Stats API 2026 y líneas Betcris entregadas por el usuario,
archivadas en `examples/betcris_padres_brewers_2026-10-03.json`.
Estado: `PREGAME`; Robbie Ray y Jacob Misiorowski son **probables**, no abridores
confirmados. Alineaciones no confirmadas. Semilla 20261002, 10,000 corridas.
Salidas `EXPLORATORY_UNCALIBRATED`; no son clasificación PRINCIPAL.

## Libreta: ataque y prevención

| Equipo | Carreras/G | Permitidas/G | Hits/G | Robos | Ataque 1–10 | Defensa 1–10 | Contacto 1–10 | Velocidad 1–10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Padres | 4.46 | 4.20 | 8.11 | 164 | 5.3 | 7.5 | 7.2 | 9.4 |
| Brewers | 5.14 | 3.81 | 8.78 | 162 | 9.7 | 9.1 | 5.0 | 8.8 |

Notas 1–10: percentil entre 30 equipos MLB de temporada regular 2026;
no son una probabilidad. Las facetas de poder son 5.7 Padres y 1.3 Brewers.
Brewers produce más carreras aunque conectó menos HR; velocidad y embasado
deben revisarse contra Ray y el bullpen de San Diego.

## Mercado exacto y contradicción

| Línea Betcris | Corridas modelo: cobra / 1,000 | Contradicción |
| --- | ---: | --- |
| Brewers ML −208 | 557 | Precio exige ≈675/1,000 antes del margen; otro modelo exploratorio dio 682/1,000 |
| Total del juego más de 7 −113 | 581; push 108 | Otro modelo exploratorio dio 421; dependencia alta del modelo de carreras |
| Padres más de 2.5 carreras −116 | 674 | No alcanza umbral deportivo validado de 70 % |
| Brewers más de 4 carreras −121 | 466; push 133 | Cuatro carreras devuelven según reglas aplicables |
| Padres más de 6.5 hits −110 | 389 | Histórico sin matchup: 636; Misiorowski cambia mucho el escenario |
| Brewers más de 7.5 hits −130 | 528 | Histórico sin matchup: 617 |
| Ray más de 4.5 K −105 | 463 | Histórico de 30 aperturas: 467; una salida corta empeora el over |
| Misiorowski más de 8.5 K +120 | 457 | Histórico: 467; con cuatro BF menos, ≈237 |
| Ray más de 3.5 hits permitidos −120 | 705 | Histórico: 667; con cuatro BF menos, ≈557 |
| Misiorowski menos de 3.5 hits permitidos −115 | 603 | Histórico: 500; se invierte con duración o contacto distintos |

Los porcentajes no están calibrados contra resultados fuera de muestra.
Los modelos de hits de equipo y de hits permitidos por abridor actualmente
se simulan por separado, aunque dependen entre sí en el juego real. No usar
sus probabilidades conjuntas para una combinada sin modelar esa relación.

Rango central simulado p10/p50/p90: Padres 1/4/8 carreras y 3/6/10 hits;
Brewers 1/4/9 carreras y 4/8/13 hits; Ray 2/4/7 K;
Misiorowski 5/8/12 K. Estos rangos no son límites garantizados.

## Bateadores y parciales

La simulación condicional a **estar en la alineación** y a la mano del abridor
produjo para Jackson Chourio ≥1 hit 760/1,000 y ≥2 bases totales 507/1,000;
para Fernando Tatis Jr. ≥1 hit 714/1,000. Son escenarios proyectados, pues
el lineup todavía no está confirmado. Las líneas Sí hit de Betcris eran
Chourio −220 y Tatis −190. No declararlas PRINCIPAL sin recheck y calibración.

| Jugador | Equipo | ≥1 hit / 1,000 si inicia | ≥2 bases / 1,000 si inicia |
| --- | --- | ---: | ---: |
| Bauers | MIL | 619 | 389 |
| Chourio | MIL | 760 | 507 |
| Contreras | MIL | 686 | 398 |
| Mitchell | MIL | 572 | 323 |
| Ortiz | MIL | 511 | 259 |
| Pratt | MIL | 593 | 265 |
| Turang | MIL | 659 | 390 |
| Yelich | MIL | 604 | 340 |
| Bogaerts | SD | 570 | 286 |
| Cronenworth | SD | 557 | 270 |
| France | SD | 649 | 408 |
| Machado | SD | 592 | 351 |
| Merrill | SD | 663 | 406 |
| Tatis Jr. | SD | 714 | 435 |

Las 10,000 corridas usan frecuencias de sencillos/dobles/triples/HR,
AB históricos y un escenario de exposición de 60 % al abridor. No modelan
el orden al bate confirmado, cambios de bullpen, defensiva rival ni
dependencia entre bateadores del mismo equipo.

Histórico F5: Padres anotó ≥2 carreras en 593/1,000 juegos y Brewers ≥3
en 488/1,000. No es predicción específica del matchup. Las líneas por
entrada, hits+carreras+impulsadas e impulsadas individuales quedan
`NO ESTIMABLE / NO APUESTA` con el modelo actual. En particular, una cuota
negativa por una entrada sin carrera no convierte el suceso en seguro.

## Recheck y postmortem

Antes de jugar: verificar abridores oficiales, lineup, bullpen, clima y
reglas de Betcris; capturar la cuota final. Al iniciar, sellar este análisis
como pregame y registrar live aparte. Al final, liquidar cada mercado exacto
y comparar aciertos, pushes y errores del modelo sin reescribir el pronóstico.
