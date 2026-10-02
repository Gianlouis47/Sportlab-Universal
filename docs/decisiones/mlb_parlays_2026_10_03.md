# MLB parlays — metodología acordada para el 3 de octubre de 2026

Estado: reglas de análisis; **no son picks ni líneas actuales de Betcris**.
Zona horaria de eventos y seguimiento: `America/Santo_Domingo` (UTC−4).

## Flujo

GOAL → DATA → ANALYSIS → SIMULATION → CONTRADICTION → RECHECK → VALIDATION → DECISION → RESULT → POSTMORTEM.

1. Identificar el evento y mercado exacto de Betcris, con línea, cuota, hora y captura. Una alternativa
   sugerida se etiqueta `NO VERIFICADA EN BETCRIS` hasta que aparezca en la plataforma.
2. Comprobar estado `PREGAME/LIVE/FINAL`, abridores `CONFIRMADO/PROYECTADO/NO DISPONIBLE`,
   alineaciones, bajas, bullpen, descanso, estadio y clima. No mezclar estadísticas live con la predicción pregame.
3. Comparar **ambos** equipos con la libreta: carreras anotadas y permitidas por juego en temporada,
   L5/L10/L20/L30 sin duplicar ventanas, local/visitante, calidad de oponentes y matchup específico.
   Ataque alto significa más carreras; defensa fuerte significa menos carreras concedidas.
4. Mostrar notas observables 1–10 de ataque, prevención de carreras, poder, contacto y velocidad,
   con alcance de liga y fecha. Las notas no son probabilidades ni sustituyen información de jardineros,
   bullpen o abridor. La hipótesis de ventaja local de 1.2 carreras requiere validación.
5. Simular 10,000 corridas solo cuando los insumos permitan un modelo reproducible. Guardar snapshot,
   versión, semilla, distribuciones, percentiles y escenarios de sensibilidad. El mínimo/máximo
   observado en una corrida **no** es un límite garantizado. Usar p10/p50/p90 y probabilidad de la línea exacta.

## Mercados a evaluar por juego

| Familia | Salida requerida | Riesgo que debe contrastarse |
| --- | --- | --- |
| ML + total del juego | Probabilidad individual de ambos mercados y conjunta del mismo juego | Correlación entre ganar y ritmo de carreras; extra innings |
| Total de cada equipo | Distribución de carreras propia, líneas alternativas y push | Abridor rival, bullpen y producción tardía |
| Ponches de ambos abridores | K/BF, K rival/PA, distribución BF por apertura, p10/p50/p90 K y línea exacta | Salida temprana como Hunter Brown ante CWS el 30/09: 9 BF, 2 K, 4 R |
| Hits de bateador | Hits/AB, oportunidades de turno, orden y alineación confirmada | Si no está confirmado en lineup: `NO ESTIMABLE` |
| Remolcadas de bateador | Turnos con corredores en posición de anotar, orden y lineup | Sin modelo de oportunidades: `NO ESTIMABLE` |

Para una combinada, tomar los resultados **conjuntos de cada corrida**. Reportar por separado
probabilidad de cada selección, 13/13 (o N/N), pushes sin derrotas y escenarios perdedores.
No multiplicar probabilidades como si las selecciones del mismo juego fueran independientes.
El motor actual comparte las carreras para ML/totales, pero modela K y hits independientes de carreras;
sus porcentajes de parlay son `EXPLORATORY_UNCALIBRATED` hasta calibrar esas dependencias.

`PRINCIPAL` exige al menos 70 % de probabilidad deportiva **validada para el mercado exacto**;
preferencia 80 % o más. La cuota se examina después. Si no hay datos, `NO ESTIMABLE / NO APUESTA`.

## Seguimiento del sábado

Partidos oficiales previstos en RD: CWS @ CLE 1:00 p. m.; ATL @ LAD 4:00 p. m.;
NYY @ TB 6:30 p. m.; SD @ MIL 8:30 p. m. A la apertura de cada juego, registrar
el pronóstico pregame sellado y el marcador live por separado. Al finalizar,
liquidar cada mercado según reglas Betcris, comparar resultado con percentiles
y registrar fallo de abridor, lineup, bullpen, bateo, parque o modelo. No reescribir
el pronóstico original tras ver el resultado.
