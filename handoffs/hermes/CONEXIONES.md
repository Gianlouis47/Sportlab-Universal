# Conexiones conocidas y documentación

## GitHub y método

Repositorio: https://github.com/Gianlouis47/Sportlab-Universal
Rama: sportlab-universal-refactor.

Leer en este orden:
1. AGENTS.md.
2. knowledge/markets/universal_offense_defense_baseline.md.
3. knowledge/markets/nba_player_props.md.
4. knowledge/markets/threshold_frequency.md.
5. knowledge/markets/postmortem_storage_and_market_availability.md.
6. knowledge/integrations/source_sync.md y knowledge/integrations/sports_hub.md.
7. config/defaults.yaml y sportlab/models/historical_trends.py.
Para otros deportes, usar sus módulos y documentación existentes; no reconstruir el proyecto.

## Base Neon

Proyecto: small-leaf-72827293. Base: sportlab.
Tablas conocidas: core.framework_rules y core.source_snapshots.
La aplicación existente usa SPORTLAB_DATABASE_URL como secreto de entorno.
La consulta por conector en este chat NO proporciona una contraseña exportable.

sql/export_context.sql consulta reglas activas y versiones relevantes sin cambiar datos.
Reutilizar conexión local autorizada y las migraciones existentes. No crear otro proyecto, no vaciar tablas y no ejecutar DDL para esta extracción.

## MCP SportLab Sports Hub vigente

Endpoint documentado en la rama:
https://sportlab-sports-hub.snug-comet-5125.chatgpt.site/mcp

Cliente Hermes: configurar este remoto usando las capacidades/documentación de su instalación real. Hacer initialize/tools/list y una lectura de prueba. Registrar autenticación o errores; no declarar listo solo por HTTP 200.

API_CONTRACTS: api-contracts.json exporta los nombres/contratos vistos en ChatGPT. Los prefijos mcp__codex_apps__ son nombres del cliente, no rutas HTTP del servidor. El servidor remoto puede exponer otros nombres. Enumerarlos antes de mapear.

El endpoint mencionado al principio del chat fue:
https://sportlab-sofascore-plugin.snug-comet-5125.chatgpt.site/mcp
Estado en este paquete: LEGACY_NO_VERIFICADO. La rama vigente documenta su sustitución por Sports Hub. knowledge/integrations/sofascore.md devuelve 404 en esta rama; el documento actual es sports_hub.md. Algunas herramientas conservan alias SofaScore; verificar provider/source de cada respuesta. No pasar IDs ESPN a herramientas que esperan IDs SofaScore.

## Lecturas públicas ESPN utilizadas

No requieren una clave en los usos observados. Son endpoints públicos no contractuales, con disponibilidad no garantizada.

Calendario NBA:
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261021&limit=100

Calendario NHL:
https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard?dates=20261021&limit=100

Cambiar la fecha por la que corresponda; usar IDs retornados por cada proveedor.
Historial equipo NBA:
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/1/schedule?season=2026
Resumen NBA, ejemplo de ID verificado el 21/10:
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event=401909834

No atribuir datos ESPN a SofaScore. Comprobar fase de temporada por evento, cortes y partidos terminados; las respuestas pueden incluir fases distintas de la solicitada.

## Otros conectores

En ChatGPT se consultaron Optimal Sports Projections y SportLab Sports Hub; también hay herramientas de Flaim Fantasy, StatsHawk, SportsAPIs.dev, fútbol y béisbol.
No se dispone de sus claves API privadas ni de URLs de autenticación exportables aquí.
Hermes debe descubrir las conexiones instaladas en su PC; no inventar endpoints ni comprar planes.
Linemate y SofaScore son referencias cuando accesibles; no hay ingestión automática verificada por esta tarea.

## Credenciales

.env.example solo contiene nombres de configuración y valores públicos conocidos.
Si hace falta, el titular puede completar una copia PRIVADA en el PC o reutilizar variables/conexiones existentes. No sobrescribir .env existente. No meter credenciales en ZIP, capturas, commits o informes.
No se necesitan credenciales del sitio de apuestas para intentar la lectura pública inicial.
