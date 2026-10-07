# Frecuencia de superación de líneas — método transversal

## Propósito y origen

Usar resultados históricos para investigar **el evento exacto que liquida un mercado**. Una captura compartida el 07/10/2026 sobre Once Caldas–Llaneros (partido anunciado para el 09/10/2026) muestra dos afirmaciones de terceros: 6/7 partidos de Llaneros como visitante con dos o más goles totales (85,7 % observado), y 12/13 partidos de Once Caldas recibiendo al menos un gol (92,3 % observado). Ambas cifras requieren comprobar partidos, competición, sede, fechas y resultados en fuentes oficiales antes de usarse para un pronóstico. La segunda frecuencia es **un gol recibido**, no la frecuencia de Over 1.5 del partido; no multiplicar ni promediar 6/7 y 12/13 como si fueran probabilidades independientes del mismo evento.

Este es un filtro de **investigación y contraste**, no un motor de probabilidades por sí solo. Nunca interpretar 6/7 como 85,7 % de probabilidad futura ni elevarlo automáticamente a PRINCIPAL.

## Procedimiento por partido y mercado

1. Definir deporte, torneo, temporada, evento, mercado, participante, período y regla de liquidación: línea, over/under o hándicap, prórroga/tiebreak/extra innings, y tratamiento de push o anulación. Ejemplo: más de 1,5 goles del partido en 90 minutos equivale a **dos goles o más**; «el local recibe un gol» es otro evento.
2. Reunir una muestra **anterior al comienzo del partido** de la misma temporada y competición; comprobar cada resultado contra el registro oficial. Informar aciertos, partidos elegibles, fechas de corte, fuente, sede y reglas de exclusión. Examinar temporada y ventanas L5/L10/L20/L30 sin sumar ventanas anidadas como muestras independientes. Si una ventana o split tiene pocos juegos, mostrarlo y ampliar el contexto sin mezclar temporadas a escondidas.
3. Calcular la frecuencia observada `aciertos / elegibles` por ambos lados: equipo/jugador que busca superar la línea **y** rival que permite el mismo evento. Verificar que el denominador y el evento sean iguales antes de comparar; una estadística relacionada pero distinta es solo evidencia contextual. Registrar además magnitudes reales, no solo aciertos: distribución de goles/carreras/puntos/juegos, márgenes, ceros, extremos y, si aplica, chances/xG, ritmo o posesiones.
4. Contrastar los splits pertinentes (casa/visita, superficie, titular, alineación, mano, minutos, rival y nivel de oponentes), forma reciente, lesiones, descanso, clima y reglas del torneo. Un registro de 6/7 es una muestra pequeña, sensible a un solo juego; ajustar la proyección hacia una base de liga/temporada validada y comprobar sensibilidad. Evitar seleccionar la mejor ventana o línea *después* de mirar resultados sin registrarlo.
5. Con entradas verificadas, estimar la **distribución del mercado exacto** mediante el modelo específico del deporte y, cuando esté validado, simulación reproducible. Separar frecuencia descriptiva, probabilidad calibrada y cuota implícita. Documentar pushes para líneas enteras. Buscar rutas de fallo (partido lento, titular ausente, defensa reforzada, marcador temprano que cambia el ritmo, etc.). Evaluar la cuota vigente al final y clasificar PRINCIPAL, SECUNDARIO o NO APUESTA según el resto de las reglas del proyecto.
6. Registrar los resultados y la calibración posteriormente: cada ventana, umbral y tipo de mercado por separado. No tratar dos mercados del mismo partido, ni selecciones de un parlay, como independientes por defecto.

## Aplicaciones por deporte y otros ámbitos de apuestas

| Deporte | Ejemplos de evento medible | Contexto y precaución específica |
| --- | --- | --- |
| Fútbol | Total de goles >1,5; goles de equipo >0,5; ambos anotan; tiros, tiros a puerta, córners, tarjetas; hándicap de goles | Separar 90 minutos de prórroga; rival que concede, xG/xGA, once y árbitro cuando corresponda. «Recibió ≥1» no demuestra «total ≥2». |
| MLB | Total de carreras, carreras de un equipo, F5, hándicap; ponches, hits, bases totales o bases por bolas de jugador | Separar F5 del partido completo; abridores, lineup, bullpen, parque y reglas de extra innings. Para K, contar salidas del abridor con participación y límite de pitcheos. |
| NFL/NCAAF | Total de puntos, puntos de equipo, hándicap; yardas de pase/carrera/recepción, recepciones, touchdowns y capturas | Analizar QB, ritmo, jugadas, volumen, clima y reglas de tiempo extra; un prop de jugador requiere rol y oportunidades. |
| NBA/WNBA/NCAAB | Total y puntos de equipo, hándicap; puntos, rebotes, asistencias, triples o robos de jugador | Normalizar por liga, posesiones, minutos, disponibilidad y rotaciones; props correlacionados por minutos/uso. |
| NHL | Total de goles, goles de equipo, hándicap; tiros, puntos de jugador y atajadas de portero | Portero confirmado, tiros/ocasiones, power play y reglas de prórroga/shootout, gol a portería vacía y liquidación. |
| Tenis | Total de juegos del partido, juegos individuales, hándicap de juegos/sets, aces, dobles faltas y breaks | Separar juegos propios y conjuntos, superficie, formato de sets, tie-break, retiro y reglas de liquidación. La frecuencia de Over de juegos no es la de victoria ML. |

Para cualquier mercado nuevo, la misma secuencia aplica: **definir evento → contar con fuente y denominador → contrastar el rival y el contexto → modelar → comprobar precio y liquidación → verificar resultados**. Un porcentaje histórico alto por sí solo no prueba superioridad deportiva, certeza ni valor apostable.
