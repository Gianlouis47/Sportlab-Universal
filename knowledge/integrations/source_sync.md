# Fuentes y actualización de SportLab

Decisión del usuario, 2026-10-16: preferir fuentes gratuitas, de varios deportes y
con poca fricción. El transporte MCP no garantiza cobertura, calidad ni gratuidad.
No depender de BALLDONTLIE ni de proveedores con token pendiente.

Linemate y SofaScore son referencias prioritarias de consulta cuando el dato es
accesible y verificable. No se ha validado su ingestión automática. Una portada
HTTP 200 no demuestra acceso a estadísticas ni ausencia de antibot. No suponer
API pública ni replicación instantánea. SofaScore declara que no comparte sus
fuentes como endpoints: https://sofascore.helpscoutdocs.com/article/129-sports-data-api-availability.
Linemate: https://linemate.io/ requiere JavaScript para la interfaz.
No usar proxies rotativos, evasión de CAPTCHA ni reintentos tras 401/403/429.

## Ingestión implementada

`python -m sportlab.data.source_sync --date YYYY-MM-DD --days 2 --save`

Usa lecturas públicas ESPN sin clave para MLB, NHL, NFL, NBA, ATP y fútbol
(EPL, LaLiga, Serie A, Bundesliga, Ligue 1 y Champions). Se valida cada respuesta;
un fallo no borra lecturas válidas de otros deportes. Máximo 31 fechas y 100
resúmenes por liga por ejecución; predeterminado 20. El calendario ATP puede ser
un contenedor de torneo: nunca contarlo como un partido ni sumar sus marcadores
como juegos de un tenista. ESPN no es una API contractual garantizada.

Aplicar `migrations/20261016_source_snapshots.sql` antes de `--save`. Usa el adaptador
existente `SPORTLAB_DATABASE_URL`, exclusivamente como secreto de entorno.
`core.source_snapshots` conserva versiones de calendario/box score, hora de primera
lectura y última comprobación, URL, hash e IDs ESPN. No confundir con IDs de otros
proveedores. El mismo contenido no crea otra versión consecutiva; una corrección
A→B→A conserva las tres. No importar noticias, medios, cuotas o play-by-play.
El límite de resúmenes puede dejar partidos fuera: no afirmar temporada completa.

Primera carga verificada: 13 recursos ESPN del 15/10/2026, seis categorías de
consulta (EPL sin partidos ese día; ATP contiene torneo). Se cargaron calendarios
y estadísticas de equipo, sin importar props individuales en esta carga inicial.
Los registros llevan `initial_team_stats_v1_player_props_not_imported`.
No confundir recursos consultados con partidos completos ni con cobertura de props.
La conexión directa desde este entorno a Neon falló por DNS; carga realizada y
consultada mediante el conector Neon, con prueba de repetición sin duplicados.

## Tendencias y método de la libreta

`historical_trends` recibe observaciones del MISMO evento de liquidación, unidad,
periodo, sujeto, competición y split. El llamador debe resolver esa identidad antes
de combinar muestras. Cortar por fecha del partido Y fecha de conocimiento;
reconciliar fuentes antes de contar. L5/L10/L20/L30 son ventanas de comparación,
no cuatro muestras independientes para sumarlas. Seleccionar ventana antes de
excluir faltantes: no sustituirlos por partidos más antiguos. Mostrar hits,
losses, pushes, missing, observados, solicitados y fracción; 8/10 es frecuencia
histórica, no probabilidad de 80% en el siguiente encuentro.

Para la presentación, usar ataque y defensa de 1 a 10 con métricas y referencia
comparables dentro de deporte, liga, temporada y unidad. Conservar las tasas
reales: `matchup_baseline` cruza ataque de cada equipo con producción permitida
por el rival. Esa proyección alimenta el modelo específico y su simulación;
no sumar puntos porcentuales por una nota ni contar dos veces sus mismas métricas.
No se añade un modelo probabilístico calibrado nuevo en esta integración.
Nombres NHL: ciudad más nombre del equipo. Registrar faltantes como NULL, no cero.

La actualización periódica detecta cambios al consultar: no hay webhook verificado
de Linemate/SofaScore. En cada ejecución informar cobertura, nuevos registros,
fallos y recursos truncados; nunca marcar una fuente como sincronizada sin lectura
y escritura verificadas. El plugin que el usuario declinó no se utiliza ni se sugiere.

## Líneas observadas de Appuesta.do — 2026-10-21

Aplicar [la integración de Appuesta](appuesta.md). El detalle público NBA y los totales NHL sí fueron leídos; la cobertura de otros deportes se verifica por separado. Conservar líneas, cuotas, períodos, horas y versiones en Neon; comparar cada nueva consulta con la anterior. El fixture pequeño de NBA y el contrato están en el repositorio a petición expresa del usuario. No confundir una regla/documentación o una tarea periódica con un recolector permanente ni afirmar acceso universal.
