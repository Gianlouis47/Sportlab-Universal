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
- Para cada mercado mostrar jugador/equipo/rival, estadística, período y prórroga, línea fija y cuota observada con fecha de captura, promedio de temporada, promedios L5/L10/L20/L30, mediana cuando ayude, proyección actual separada e inclinación Más/Menos. Un promedio no es una línea ni una probabilidad futura.
- Recalcular tanto Más como Menos frente a esa misma línea exacta en L5/L10/L20/L30; conservar denominadores, pushes y faltantes. No trasladar el 30/30 de una alternativa baja a la línea fija más exigente.
- Contrastar ataque individual, prevención rival comparable, minutos, rol y oportunidades. Un cambio de equipo o titularidad exige etiquetar el historial anterior; si promedio y proyección discrepan o el margen es pequeño, explicarlo y no forzar un pick.
- El reporte debe permitir elegir entre Más, Menos o NO APUESTA. La inclinación estadística no certifica valor sin estimación defendible y precio.
- En "Crear apuesta", el usuario reporta un máximo de 10 selecciones en total por un mismo partido, aplicable a todos los deportes. Es un límite de la plataforma reportado por el usuario, no una obligación de completar diez ni autorización para aumentar automáticamente un ticket. Distinguir este límite por evento de una combinada entre partidos.
- Evaluar la dependencia entre props, totales y ganador del mismo evento. No multiplicar frecuencias marginales ni presentar selecciones correlacionadas como apuestas independientes.
- No pedir imágenes de todas las categorías. Usar las capturas disponibles y buscar autónomamente datos públicos. Una categoría cerrada en la captura tiene línea NO OBSERVADA, no cero ni una línea adivinada. Sin acceso a la línea de appuesta.do, dar promedios/proyecciones de referencia; una línea de otra casa se identifica como externa.
- El motivo "por inicio de temporada" es una explicación sugerida por el usuario, no una regla verificada de la banca. Guardar los valores concretos de las capturas en Neon, sin copiar saldos o datos personales innecesarios al repositorio.
