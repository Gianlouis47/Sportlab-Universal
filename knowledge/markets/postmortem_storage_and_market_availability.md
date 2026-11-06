# Cierre de resultados, almacenamiento y líneas ejecutables
Actualizado: 2026-10-19. Política operativa; no es un modelo de predicción.

## Conservar la evidencia original
- Liquidar cada línea publicada por versión y corte temporal. Mantener separadas la primera recomendación, revisiones posteriores y alternativas no priorizadas.
- No reemplazar una pérdida original por una línea posterior ganadora. Un over inferior y un under superior del mismo partido no son apuestas independientes.
- Guardar partido completo, regulación, prórroga/shootout y pushes según el mercado exacto. El horario UTC puede caer al día siguiente; conservar la fecha local del evento.
- Resultado personal y ROI requieren boleto, línea ejecutada, cuota y monto. Una inclinación al ganador sin apuesta confirmada no es un boleto ganado/perdido.
- Para aprender, separar datos observados, hipótesis y reglas validadas. Una jornada no justifica ajustar pesos ni adoptar “siempre under/over”.

## Distinguir umbral analítico de selección ejecutable
1. Registrar el umbral propuesto, su fuente, si fue priorizado y si su disponibilidad/precio están observados.
2. Buscar las líneas reales accesibles; si la banca ofrece otra línea, contar y evaluar ese mercado exacto antes de sustituirlo. No tratar más de 27.5 como equivalente a más de 35.5.
3. La posibilidad de modificar líneas no demuestra que exista todo umbral. Si una línea no está disponible, continuar con alternativas observadas o dejar ese umbral como analítico; no elevar su etiqueta a selección ejecutable por frecuencia histórica.
4. Un over ganado por 0.5 no demuestra buena calibración. Conservar el margen respecto a la línea, la media descriptiva y sus errores, pero no convertirlos en una probabilidad calibrada.
5. Para NFL, revisar eficiencia por serie, conversiones de zona roja/tercer down, QB, pérdidas, capturas y puntos de defensa/equipos especiales. Para NHL, participación del portero real, volumen/calidad de ocasiones y power play; no atribuir el resultado solo a la media de goles.
6. El postmortem explica mecanismos observados. No afirmar que una lesión, descanso o rotación causó por sí solo una derrota sin evidencia.

## Persistencia compacta e idempotente
Datos dinámicos en Neon:
- `core.events`: un estado canónico vigente por (sport_code, external_id), con identidad del proveedor, marcador, fase FINAL y fecha local. Upsert para correcciones verificadas; no reinterpretar IDs de otro proveedor.
- `core.team_event_production`: un registro por (event_id, team_id, normalization_unit). Guardar producción a favor/permitida, rival y métricas compactas, no páginas HTML ni crónicas completas.
- `core.postmortems`: un cierre por evento y review_key; las líneas de cada versión quedan dentro de actual_result. El índice parcial de abajo permite repetir sin duplicar. Las correcciones de hechos finales actualizan ese cierre; las recomendaciones PREGAME siguen en sus snapshots originales.
- `core.form_strength_snapshots`: temporada y ventanas LAST_N 5/10/20/30 por equipo, fecha, unidad y fórmula. Conservar n real, temporadas incluidas, IDs de muestra y corte.
- `core.source_snapshots`: evidencia prepartido y cambios materiales con procedencia; guardar resumen/punteros cuando el resultado ya está normalizado. No copiar en cada snapshot toda la historia, boxscore y HTML.

Índice aplicado el 2026-10-19:
```sql
CREATE UNIQUE INDEX IF NOT EXISTS idx_postmortems_event_review_key
ON core.postmortems(event_id, (actual_result->>'review_key'))
WHERE actual_result ? 'review_key';
```

Una ventana L30 cambia de miembros: entra el partido nuevo y sale el más antiguo de la ventana, no del registro histórico canónico. El cálculo histórico para una fecha debe filtrar por corte ANTES de seleccionar los últimos N; no usar snapshots posteriores para simular información previa.

Evitar duplicados con claves naturales y upserts. No borrar prepartidos ni resultados útiles para ahorrar unas pocas filas. La depuración de raw/duplicados debe tener una política de retención explícita que preserve auditoría, calibración y resultados. No se aplicó ningún borrado en esta actualización.

## Calidad de fuentes
Conservar discrepancias de estadísticas, fuente y hora; dejar NULL la métrica canónica discutida hasta resolverla. Un cero confirmado es distinto de un dato ausente. Calendario/marcador identificados prevalecen sobre un día de semana erróneo en la crónica. No fusionar cifras incompatibles de crónica y boxscore.

## Repositorio
GitHub conserva método, SQL pequeño/documentación, versiones y síntesis de aprendizajes. Los resultados detallados, ventanas y métricas de muchos partidos permanecen en Neon. Cambios a un motor requieren pruebas y validación cronológica; una documentación de postmortem no significa que el predictor haya sido recalibrado.
