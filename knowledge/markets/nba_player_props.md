# NBA: prioridad de props de jugadores

Actualización solicitada por el usuario: 2026-10-19.

En NBA investigar prioritariamente mercados de jugadores, además de totales y ganador: puntos, rebotes, asistencias, triples anotados, robos, tapones, pérdidas, dobles/triples dobles y combinaciones PR, PA, RA y PRA cuando haya datos y mercados pertinentes. No obliga a recomendar cada categoría ni a inventar líneas ofrecidas.

- Resolver jugador, equipo actual, rival, fecha y estado del evento. Separar temporada regular de pretemporada, playoffs y final NBA Cup (no integra los 82 partidos).
- Registrar estadística exacta, línea, dirección, período y liquidación. Comparar Over y Under frente a la línea observada; aplicar el modo de líneas fijas de appuesta.do definido abajo. Evaluar alternativas como ejecutables únicamente cuando el usuario confirme que vuelven a estar disponibles.
- Usar historial individual vs distintos rivales como base; H2H secundario. Calcular temporada/L5/L10/L20/L30 con denominadores reales y corte. DNP no es cero; cero observado con participación sí cuenta. No completar ventanas cortas.
- Contrastar minutos y oportunidades (tiros, rebotes disponibles, potenciales asistencias), rol, titularidad proyectada, lesiones, descanso, ritmo y producción permitida por el rival a un rol comparable. Totales de equipo permitidos son contexto, no tasas individuales ni por posición.
- Al comenzar temporada, etiquetar antecedentes de la temporada anterior y cambios de equipo/rol; las proyecciones externas son estimaciones. No convertir 8/10 o 30/30 en probabilidad futura ni certeza.
- Para combinaciones, sumar las estadísticas del mismo partido antes de contar. No multiplicar frecuencias de categorías correlacionadas ni presentar props del mismo jugador como independientes.
- Simular únicamente con modelo e inputs defendibles; conservar seed, versión y límites si se ejecuta. Si no hay modelo calibrado o variables críticas resueltas, análisis descriptivo PROVISIONAL, sin porcentaje futuro inventado.
- Registrar en Neon datos compactos, fuentes, fecha, faltantes, controles y versiones de líneas; conservar el historial. GitHub guarda el método.
- Cerrar con tablas por deporte y una tabla específica de props (jugador, equipo/rival, mercado exacto, L5/L10/L20/L30 y clasificación). Todas las notas antes de la última tabla.


## Appuesta.do: modo de líneas fijas — 2026-10-20

Preferencia operativa expresa del usuario, vigente hasta que él avise que vuelven las alternativas modificables. Aplicar la regla activa `sportlab_appuesta_fixed_lines_and_bet_builder` de Neon.

- En NBA, trabajar por defecto con la línea fija realmente observada en appuesta.do. No seguir proponiendo como ejecutables los umbrales alternativos de respuestas anteriores. Conservar esos pronósticos para auditoría, etiquetados como referencias analíticas históricas.
- Para cada mercado mostrar jugador/equipo/rival, estadística, período y prórroga, línea fija y cuota observada con fecha de captura, un solo promedio visible por categoría (L10 por defecto, según la sección de presentación aprobada abajo), proyección actual separada cuando sea necesaria e inclinación Más/Menos. Calcular temporada/L5/L10/L20/L30 para análisis y conservarlos en Neon sin volcarlos todos en cada casilla. Un promedio no es una línea ni una probabilidad futura.
- Recalcular tanto Más como Menos frente a esa misma línea exacta en L5/L10/L20/L30; conservar denominadores, pushes y faltantes. No trasladar el 30/30 de una alternativa baja a la línea fija más exigente.
- Contrastar ataque individual, prevención rival comparable, minutos, rol y oportunidades. Un cambio de equipo o titularidad exige etiquetar el historial anterior; si promedio y proyección discrepan o el margen es pequeño, explicarlo y no forzar un pick.
- El reporte debe permitir elegir entre Más, Menos o NO APUESTA. La inclinación estadística no certifica valor sin estimación defendible y precio.
- En "Crear apuesta", el usuario reporta un máximo de 10 selecciones en total por un mismo partido, aplicable a todos los deportes. Es un límite de la plataforma reportado por el usuario, no una obligación de completar diez ni autorización para aumentar automáticamente un ticket. Distinguir este límite por evento de una combinada entre partidos.
- Evaluar la dependencia entre props, totales y ganador del mismo evento. No multiplicar frecuencias marginales ni presentar selecciones correlacionadas como apuestas independientes.
- No pedir imágenes de todas las categorías. Usar las capturas disponibles y buscar autónomamente datos públicos. Una categoría cerrada en la captura tiene línea NO OBSERVADA, no cero ni una línea adivinada. Sin acceso a la línea de appuesta.do, dar promedios/proyecciones de referencia; una línea de otra casa se identifica como externa.
- El motivo "por inicio de temporada" es una explicación sugerida por el usuario, no una regla verificada de la banca. Guardar los valores concretos de las capturas en Neon, sin copiar saldos o datos personales innecesarios al repositorio.


## Presentación aprobada: un solo promedio L10 por categoría — 2026-10-20

Preferencia expresa del usuario, confirmada al aprobar la tabla completa de 53 jugadores. Consultar la regla activa `sportlab_nba_single_l10_average_display` en Neon. Esta sección actualiza el formato visible; no elimina el método de ataque/defensa ni los controles estadísticos.

- Al pedir promedios NBA, cubrir los jugadores pertinentes de los partidos solicitados, buscando datos públicos; no limitarse a los jugadores o mercados de una captura. Agrupar por equipo actual con el nombre distintivo primero y ciudad secundaria.
- Mostrar una sola media aritmética por jugador y categoría, con L10 como ventana predeterminada: `Jugador | Puntos | Asistencias | Rebotes | Triples anotados | Robos | Tapones | Pérdidas | Minutos`. No escribir `temporada / L10`, dos cifras ni varias ventanas dentro de una casilla, salvo petición expresa del usuario.
- L10 significa las últimas diez participaciones elegibles de temporada regular antes del corte, frente a distintos oponentes. Excluir pretemporada, playoffs, final NBA Cup y DNP. Un cero observado con participación sí cuenta. Si hay menos de diez observaciones o faltan campos, informar el denominador real; usar NO DISPONIBLE para ausencia de datos y no cero. Redondear solo al presentar, normalmente a un decimal.
- Identificar una sola vez ventana, temporada, fuente y fecha/hora de corte. En el inicio de 2026-27, los antecedentes 2025-26 siguen identificados como tales; no llamarlos estadísticas actuales de 2026-27. Etiquetar cambios de equipo/rol sin presentar el roster actual como equipo histórico de todos los registros.
- Conservar en Neon las observaciones disponibles y/o resúmenes compactos trazables de temporada/L5/L10/L20/L30, n, faltantes, jugador/ID, equipo actual e histórico, fase, fuente, fecha del último partido y corte. GitHub guarda este método, no dumps de estadísticas de todos los jugadores. Reutilizar el snapshot existente si coincide y guardar otra versión solo cuando cambie el dato o su interpretación.
- La tabla de promedios es descriptiva. Cuando se pidan selecciones, compararla con la línea fija exacta y dar Más/Menos/Pasar con contexto de rival, rol, minutos y oportunidades; no inventar líneas ni decidir únicamente porque la media esté por encima o debajo. Las frecuencias exactas L5/L10/L20/L30 y las proyecciones se muestran aparte cuando ayuden o se soliciten; no sustituyen ni se mezclan con la única media de cada categoría.
- No convertir esta preferencia de presentación en una media combinada arbitraria, una proyección nueva, una probabilidad futura, una garantía de participación ni una selección automática.

## Selección de jugadores: quinteto titular y excepciones de banca — 2026-10-21

Preferencia expresa del usuario: limitar las recomendaciones de props NBA a los cinco titulares del partido y, como excepción, a algunos suplentes destacados en pretemporada cuyo rol actual respalde participación suficiente. Esta sección acota qué jugadores son pertinentes en las secciones anteriores.

- Investigar primero el quinteto titular actual de cada equipo en una fuente identificada y con fecha de consulta. Distinguir TITULAR CONFIRMADO, TITULAR PROYECTADO, SUPLENTE y NO DISPONIBLE. Una plantilla, titularidad habitual o promedio antiguo de minutos no confirma el quinteto del día. Continuar el análisis con una proyección trazable y actualizar al confirmarse.
- Considerar suplentes solo como excepción documentada: rendimiento destacado en varios partidos de pretemporada, minutos y oportunidades observados, calidad de los rivales y evidencia actual de pertenencia a la rotación con participación suficiente para el mercado. Revisar lesiones, competencia por puesto y posibles restricciones de minutos. No elegirlos únicamente por un partido llamativo ni inventar un mínimo universal de minutos.
- Mantener los registros de pretemporada separados de temporada regular y de L5/L10/L20/L30. La pretemporada aporta contexto sobre rol y oportunidades; no sustituye los promedios regulares ni se combina con ellos sin un modelo validado.
- Para cada jugador elegible conservar ataque individual, defensa rival comparable, minutos/rol actuales, mercado y línea fija exactos, denominadores, corte y estado de la alineación. La titularidad es un filtro de selección; la dirección Más/Menos requiere el análisis completo y no es automática.
- Guardar en Neon la evidencia de titularidad, fuente/corte, minutos disponibles y motivo de cada excepción de banca, junto con las estadísticas compactas. GitHub conserva esta política. Revisar las recomendaciones afectadas cuando cambie el quinteto o la rotación, sin borrar versiones anteriores.
- Mantener el máximo de 10 selecciones totales por SGP de un mismo partido, sumando mercados de equipos y jugadores. No completar diez por obligación.
