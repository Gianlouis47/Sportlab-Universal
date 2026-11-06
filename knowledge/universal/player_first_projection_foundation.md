# SportLab Universal — fundamento primordial: proyección desde el jugador

**Estado:** regla metodológica ACTIVA y OBLIGATORIA; implementación y calibración pendientes por motor/deporte.  
**Establecida:** 2026-11-05.  
**Fuente de configuración viva:** Neon `sportlab.core.framework_rules`, clave `universal_player_first_projection_foundation`, versión 1.

## Principio irrenunciable

**JUGADORES/PARTICIPANTES → UNIDADES → EQUIPO → RIVAL → PROYECCIÓN → SIMULACIÓN → PROBABILIDAD → DECISIÓN.**

Un equipo es el resultado de quién juega, cuánto participa, qué hace bien y mal cada integrante, cómo se complementan y contra qué adversarios concretos se enfrenta. No se debe partir de la reputación del equipo ni limitarse a su media de anotación para derivar una probabilidad.

El modelo analiza primero la realidad deportiva; las cuotas se consultan únicamente después de proyectar y validar el evento.

## Contrato mínimo de un pronóstico

1. **Identidades y disponibilidad.** Resolver todos los jugadores relevantes, posición, club en la fecha del evento, titularidad/rotación/banquillo, lesiones, limitaciones y reemplazos. Estado: `CONFIRMADO`, `PROYECTADO` o `NO DISPONIBLE`. Un roster no confirma alineación.
2. **Perfil individual.** Registrar estadísticas por posición y rol, temporada actual, forma L5/L10/L20/L30, splits de local/visita, rival y superficie/escenario pertinente. Guardar muestra, denominador, fuente, fecha de corte y tasa normalizada (minutos, posesiones, snaps, PA, BF, TOI, sets o rounds).
3. **Calificaciones descriptivas 1.0–10.0.** Calcular ataque, defensa y facetas específicas con decimales; usar métricas verificables y reducción por tamaño muestral, calidad del oponente y antigüedad. Distinguir calidad/talento estimado, forma reciente y nota recibida *por un partido*. Las tres son variables distintas. No extrapolar indiscriminadamente una nota de SofaScore a otras ligas/deportes. **8.4/10 no equivale a 84%** de victoria ni de superar una línea.
4. **Participación esperada.** Proyectar minutos, snaps, posesiones, tiempo sobre hielo, oportunidades de bateo, entradas, cargas, servicios o rounds y la incertidumbre de presencia. Sin participación no se debe convertir habilidad en producción de partido.
5. **Unidades y sinergias.** Construir once titular, quintetos, cinco ofensivos/defensivos y equipos especiales, líneas y parejas, bateadores/abridor/bullpen u otras unidades. Modelar complementariedad, esquemas, suplentes y roles. **Nunca sumar ni promediar ratings individuales sin participación, contexto y función.**
6. **Matchup específico.** Enfrentar capacidades ofensivas propias a prevención rival y duelos jugador-vs-jugador/unidad; considerar coberturas, mano dominante, características, ritmo, estrategia, entrenador, fatiga, lesiones y campo. Contrastar los outputs con datos reales del equipo (ataque, concedido, diferencial, entorno, local/visita, forma y H2H vigente) sin usar la media colectiva como sustituto de los jugadores.
7. **Proyección y distribuciones.** Producir expectativas de anotación, rendimiento individual y dispersión, con dependencias/correlaciones realistas. Una predicción puntual no es probabilidad ni una simulación.
8. **Simulación y validación.** Cuando existan datos suficientes, ejecutar habitualmente 10,000 corridas reales reproducibles. Registrar seed, versión, entradas, fecha de corte, probabilidades, distribución, push, escenarios de bajas, contradicciones y validación time-forward. Revisar titulares y condiciones de partido; recalcular si cambian.
9. **Decisión y aprendizaje.** Sólo al final revisar línea y cuota, vig, margen de error y rutas de derrota. Clasificar PRINCIPAL / SECUNDARIO / NO APUESTA; registrar resultado y postmortem. Si faltan piezas importantes, limitar los mercados sensibles o marcar PROVISIONAL/NO APUESTA.

## Adaptadores por deporte

| Deporte | Jugadores y unidades | Enfrentamientos relevantes |
|---|---|---|
| Fútbol | XI titular, suplentes, posiciones, minutos, xG/xA, acciones ofensivas/defensivas | Delanteros vs centrales, bandas, presión, transición, balón parado y portero |
| NBA/WNBA/NCAAB | Quintetos, rotación, minutos, uso ofensivo, rebote, creación y defensa | Jugador-defensor, pintura/perímetro, cobertura, pace y unidades de banca |
| NFL/NCAAF | 11 ofensivos, 11 defensivos por snap y equipos especiales | QB+OL vs presión/coberturas; RB+OL vs front; WR/TE vs secundaria; red zone |
| NHL | Líneas, parejas defensivas, portero, TOI, PP/PK | Tiradores vs defensas/goalie, calidad de oportunidades, descanso y cambios de línea |
| MLB | Orden al bate, abridor, bullpen, defensa y corredores | Bateador vs mano/repertorio, PA previstas, abridor IP/BF/pitcheos, relevistas y parque |
| Tenis | Tenista individual, servicio, devolución, fondo, volea, consistencia y forma | Superficie, estilos, mano, fatiga, puntos al servicio/devolución y matchups |
| MMA/Boxeo | Atleta individual, striking, grappling, cardio, defensa y durabilidad | Estilos, distancia, alcance, cambios por round, clinch y takedown |
| Otros | Definir participación y unidad real de cada deporte | Medidas comparables, rival y contexto antes de proyectar |

## Reglas de calidad y de ingeniería

- **Primero el jugador; no exclusivamente el jugador.** Su contribución depende de contexto colectivo, tácticas, reemplazos y rival. Con plantillas incompletas se admite un baseline de equipo **etiquetado como provisional**, nunca como sustituto equivalente.
- **Evitar doble conteo.** L10, L20 y L30 se solapan; usar bloques no superpuestos u otra estrategia validada. Si una métrica de equipo ya agrega a los jugadores, no duplicarla como evidencia independiente.
- **Pesos calibrados, no inventados.** Los pesos de contribución y de atributos se estiman y evalúan fuera de muestra por deporte, rol y mercado. Una calificación relativa a una liga no se interpreta directamente como producción absoluta.
- **Preservar evidencia temporal.** Únicamente usar información conocida antes del partido; mantener corte, temporada, fuente, muestra, identificador del jugador/equipo y estado de disponibilidad. NULL no es cero.
- **Jerarquía de datos.** Actual confirmado > temporada actual > reciente > historial contra el rival actual > anteriores como priors de menor peso; no atribuir al pasado más peso que a bajas o cambios presentes.
- **No simular por apariencia.** Una distribución construida desde un promedio arbitrario y 10,000 muestras no valida el modelo. Separar simulación mecánica, respaldo estadístico, calibración y contradicción.
- **Sin implementación ficticia.** Esta es una regla metodológica persistente, no prueba de que el motor ya agregue perfiles de todos los jugadores ni que cada deporte tenga ratings contrastados.
- **Simplicidad y reutilización.** Extender código Python existente en `sportlab/` y adaptadores específicos sin reescribir el motor universal ni replicar lógica innecesariamente.

## Integración actual sin migraciones de esquema

Reutilizar `core.athletes`, `core.player_event_production`, `core.lineup_snapshots`, `core.form_strength_snapshots`, `core.form_matchup_snapshots` y `core.simulation_runs`. Extender contratos y motores sólo cuando haya una necesidad comprobada; mantener evidencia actual en Neon y metodología/código en GitHub.

**Compatibilidad:** el método ofensiva/defensa de la libreta, L5/L10/L20/L30, H2H y proyecciones de equipo permanecen como baselines, controles y evidencia complementaria. La nueva regla establece el orden de construcción, no elimina los métodos ya probados.

**Flujo SportLab completo:** GOAL → DATA → PLAYER → UNIT → TEAM → MATCHUP → ANALYSIS → PROJECTION → SIMULATION → CONTRADICTION → RECHECK → VALIDATION → DECISION → RESULT → POSTMORTEM.
