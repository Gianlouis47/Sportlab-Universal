# Protocolo de revisión de mercados — SportLab Universal

Este documento conecta los métodos existentes de [frecuencia del evento exacto](threshold_frequency.md), [ataque/defensa de la libreta](../mlb/methods/mlb_notebook_method.md) y los modelos `sportlab/models/offense_defense.py` y `sportlab/models/threshold_frequency.py`. Se aplica a todos los deportes compatibles. Es una regla de investigación; no declara una apuesta ganadora.

## Secuencia obligatoria

1. **Identidad y liquidación.** Resolver fecha y zona del usuario, partido, local/visitante, estado, período, prórroga, tanda de penales, línea y push. La cuota es opcional en el análisis predictivo solicitado por el usuario. La captura de un tipster es una hipótesis con marca temporal, no una fuente de resultados ni una orden de copiar su selección.
2. **Ataque (+) y defensa (−).** Recoger las tasas anotadas `O_A`, `O_B` y permitidas `D_A`, `D_B` en la misma unidad, temporada, competición y corte previo al juego. Una defensa fuerte permite **menos**, por lo que su fuerza relativa es `μ − D` (con `μ` como media de liga). La ventaja ofensiva es `O − μ`. El cruce determinista existente es `E_A = (O_A + D_B)/2 = μ + ((O_A−μ) − (μ−D_B))/2`, análogamente para B, y `E_total = E_A + E_B`. Así el ataque superior suma y la defensa rival superior resta. La fortaleza neta descriptiva de un equipo es `O − D`; `O + D` describe el entorno de anotación, no fortaleza. No restar dos veces una defensa que ya está representada por goles/carreras/puntos permitidos. Estos valores no son probabilidades.
3. **Frecuencia comprobada.** Para cada línea exacta, contar `aciertos/elegibles` del sujeto y el **mismo evento permitido por el rival**, con temporada, fuente oficial, sede y fecha de corte. Revisar temporada, L5/L10/L20/L30 en bandas no superpuestas, casa/visita y H2H como contexto. Un 6/7 no es una probabilidad de 85,7 % del siguiente partido. Ajustar muestras pequeñas con referencia de liga obtenida del mismo mercado; el promedio beta de `sportlab threshold` sigue siendo exploratorio y no calibrado.
4. **Contexto que cambia el cruce.** Investigar titular o portero, alineación, lesiones, carga, descanso, ritmo, juego especial, condiciones de sede y calidad de rivales. Marcar cada variable CONFIRMADA, PROYECTADA o NO DISPONIBLE. Reducir confianza si la defensa o el ataque cambió desde la muestra histórica.
5. **Alternativas en ambos sentidos.** Evaluar la línea mostrada por el tipster y las líneas cercanas de Over y Under, totales de equipo, hándicaps y ganador cuando existan. Si el total original no se sostiene, indicar la **línea alternativa exacta y la razón**; si ninguna se sostiene, NO APUESTA. Priorizar la dirección y el umbral respaldados por datos sin exigir cuotas para entregar la conclusión predictiva. Evaluar precio y probabilidad implícita solo si el usuario solicita valor económico; no confundir mayor probabilidad de cumplimiento con rentabilidad. Nunca inventar disponibilidad o precio en una casa.
6. **Modelo, contradicción y seguimiento.** Comparar frecuencias y ataque/defensa con una distribución del deporte y mercado que haya pasado validación cronológica. Simular 10 000 veces con semilla e inputs guardados cuando el modelo y datos lo permitan; no equiparar número de partidos históricos a corridas, ni llamar simulación a una media. Buscar rutas de derrota, revalidar datos críticos, clasificar PRINCIPAL/SECUNDARIO/NO APUESTA, registrar resultado y calibración por umbral.

## Períodos y datos ambiguos

Nunca contar un marcador final con prórroga como si fuera resultado de tiempo reglamentario. Por ejemplo, un 3–2 final decidido en prórroga pudo terminar 2–2 a los 60 minutos; sería derrota para Over 4.5 reglamentario. Obtener desglose oficial por período. Si solo hay marcador final, informar un intervalo de frecuencia o NO DISPONIBLE, no una tasa exacta. La regla publicada de Appuesta.do para totales de hockey señala tiempo reglamentario salvo indicación distinta en el mercado: https://www.appuesta.do/rules. La regla de Betcris u otra casa se verifica por separado.

## Bases de datos y versión

Neon `core.framework_rules` conserva este protocolo activo con `rule_key = 'cross_sport_market_review_protocol'`; el repositorio conserva el texto y el código. Los snapshots y resultados con procedencia pertenecen a Neon. Supabase StrikeoutLab se consulta como historial MLB de solo lectura cuando corresponde, conforme a `docs/data_sources.md`; no duplicar allí reglas activas ni usarla como historial NHL. Si la regla de Neon o la versión de código cambia, actualizar este documento y comprobar la consulta de la regla antes del siguiente análisis.

## Preferencia del usuario — 8 de octubre de 2026

El usuario prioriza qué resultado es más probable y la línea exacta que lo representa. No condicionar la conclusión deportiva a disponer de cuotas ni solicitarlas por defecto. Considerar líneas alternativas y las propuestas por el usuario; la foto es evidencia del mercado visible, no de su probabilidad. Mostrar frecuencia histórica, estimación calibrada cuando exista, incertidumbre y rutas de derrota. PRINCIPAL y SECUNDARIO describen aquí solidez predictiva, no valor económico certificado. No prometer qué ocurrirá con certeza.

La captura de ejemplo muestra totales MLB «incl. extra innings», con líneas de 5 a 10 en incrementos de 0.5. No identifica el partido: no atribuirle equipos o fecha. Respetar el alcance del mercado; separar victorias, derrotas y pushes en líneas enteras conforme a sus reglas. No trasladar la inclusión de entradas extra a hockey o tenis.

## Escala de la libreta: ataque y defensa de 1 a 10

Mostrar ataque y defensa por separado en L5/L10/L20/L30 y temporada cuando haya datos comparables. Dentro de la misma liga, temporada, ventana y corte, calcular ataque = 1 + 9 × rango percentil de la tasa ofensiva; defensa = 1 + 9 × rango percentil de la tasa permitida invertida. Usar rango medio para empates y unidades normalizadas por deporte. 10 significa mejor ataque o mejor prevención; 5.5 es el centro. Si falta muestra o referencia, NO DISPONIBLE; no inventar puntuaciones.

Conservar tasas originales, tamaño muestral, procedencia y corte junto a las notas. Las notas son descriptivas y no probabilidades. No sumar ataque y defensa para declarar automáticamente un ganador: cruzar tasas con el rival, frecuencia exacta, titulares, localía, descanso y contradicciones. La defensa fuerte resta al ataque rival; no restarla dos veces. La conclusión de Over/Under debe indicar umbral exacto y alcance reglamentario/prórroga, independientemente de la cuota.

## Finalización obligatoria

Aplicar el [bucle de investigación y finalización](research_completion_loop.md) en toda cartelera: completar cada evento o documentar un bloqueo observado. Una tabla vacía exige buscar fuentes externas; un análisis pendiente no equivale a NO APUESTA. Loop-engineering se aplica al software, no a garantizar pronósticos.
