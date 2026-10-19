# NBA: prioridad de props de jugadores

Actualización solicitada por el usuario: 2026-10-19.

En NBA investigar prioritariamente mercados de jugadores, además de totales y ganador: puntos, rebotes, asistencias, triples anotados, robos, tapones, pérdidas, dobles/triples dobles y combinaciones PR, PA, RA y PRA cuando haya datos y mercados pertinentes. No obliga a recomendar cada categoría ni a inventar líneas ofrecidas.

- Resolver jugador, equipo actual, rival, fecha y estado del evento. Separar temporada regular de pretemporada, playoffs y final NBA Cup (no integra los 82 partidos).
- Registrar estadística exacta, línea, dirección, período y liquidación. Comparar Over, Under y alternativas; sin línea observada, identificar umbral analítico y disponibilidad/cuota no verificada.
- Usar historial individual vs distintos rivales como base; H2H secundario. Calcular temporada/L5/L10/L20/L30 con denominadores reales y corte. DNP no es cero; cero observado con participación sí cuenta. No completar ventanas cortas.
- Contrastar minutos y oportunidades (tiros, rebotes disponibles, potenciales asistencias), rol, titularidad proyectada, lesiones, descanso, ritmo y producción permitida por el rival a un rol comparable. Totales de equipo permitidos son contexto, no tasas individuales ni por posición.
- Al comenzar temporada, etiquetar antecedentes de la temporada anterior y cambios de equipo/rol; las proyecciones externas son estimaciones. No convertir 8/10 o 30/30 en probabilidad futura ni certeza.
- Para combinaciones, sumar las estadísticas del mismo partido antes de contar. No multiplicar frecuencias de categorías correlacionadas ni presentar props del mismo jugador como independientes.
- Simular únicamente con modelo e inputs defendibles; conservar seed, versión y límites si se ejecuta. Si no hay modelo calibrado o variables críticas resueltas, análisis descriptivo PROVISIONAL, sin porcentaje futuro inventado.
- Registrar en Neon datos compactos, fuentes, fecha, faltantes, controles y versiones de líneas; conservar el historial. GitHub guarda el método.
- Cerrar con tablas por deporte y una tabla específica de props (jugador, equipo/rival, mercado exacto, L5/L10/L20/L30 y clasificación). Todas las notas antes de la última tabla.
