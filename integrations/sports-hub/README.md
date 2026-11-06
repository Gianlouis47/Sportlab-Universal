# SportLab Sports Hub

Sustituye la integración retirada de SofaScore. No contiene llamadas a SofaScore.

Site privado: https://sportlab-sports-hub.snug-comet-5125.chatgpt.site
MCP: https://sportlab-sports-hub.snug-comet-5125.chatgpt.site/mcp

Se reutilizan los módulos MIT de Sports Leader v0.3.0 (57c31d27b5b06d69508fef6e226418fae97178cc)
y los módulos NHL/MLB de MCP Sports Hub v1.4.1 (5ecd395836d0cd3e0ae4e202ad3e5f9f878d3c45).
HTTP adaptado a Workers; licencias y fuentes están en el repositorio del Site.
No es una instalación de los 410 módulos de Sports Hub: son los 26 de NHL/MLB.
Sports Leader aporta 20 lecturas (se excluye espn_fetch); 53 herramientas en total.

Pruebas reales locales: leader_get_scoreboard devolvió 11 partidos NHL; hub_mlb_get_schedule
respondió con calendario MLB; hub_nhl_get_schedule respondió con gameWeek NHL.
La publicación y la prueba MCP en producción se registran al completarse.

BALLDONTLIE: adaptador de lectura al MCP oficial https://mcp.balldontlie.io/mcp.
Requiere secreto de servidor BALLDONTLIE_API_KEY. No está autenticado, no se creó
cuenta ni se contrató plan. ATP: partidos requieren ALL-STAR y estadísticas GOAT
según https://atp.balldontlie.io/. No afirmar que todo sea gratis.

Linemate/Outlier/Scout Picks: sitios de investigación complementarios; no se encontró
API/MCP público documentado. Aparecen como referencias, no como proveedores conectados.
Sportmonks: https://github.com/SportMonks/MCP es oficial pero requiere token/plan;
Broadage: API de varios deportes con token de cliente; StatsFC: API de fútbol con clave;
AnWP/Scoremer/Rotascore: plugins WordPress, no conectores ChatGPT por sí solos.
Bindsport: no se identificó de forma inequívoca. Enigma2 no se instala en SportLab.

Cada resultado mantiene fuente, hora de consulta e IDs del proveedor. No mezclar
IDs ESPN/NHL/MLB/BDL. Las frecuencias L5/L10/L20/L30 requieren valores del mercado
exacto y corte temporal; faltantes no son cero, retiros no son partidos completos.
Frecuencia histórica no es probabilidad futura. No inventar datos ni claves.


Fuente publicada del Site: f9a645b61a94485ea1c75ee647cbd7333023ef24.
Publicación confirmada (has_mcp=true): 2026-10-16 03:05:59 UTC.
No se conservan adaptadores, pruebas, compose ni documentación operativa de SofaScore en la rama vigente.
