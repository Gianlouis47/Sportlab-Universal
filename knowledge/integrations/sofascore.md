# SofaScore: integración de datos y tendencias

Estado al 2026-10-16 UTC: adaptador implementado y probado con API HTTP local
de contrato; fuente real NO CONECTADA. La petición directa de este entorno a
`https://www.sofascore.com/api/v1/sport/tennis/scheduled-events/2026-10-15`
respondió HTTP 403. No se importaron partidos ni se calcularon tendencias reales.
Docker no está instalado aquí: no se pudo construir ni ejecutar el servicio.

## Fuente seleccionada

https://github.com/tunjayoff/sofascore_scraper

Versión declarada 3.1.0; revisión examinada y fijada:
`dd9f061be2c64f01a6d3a50fb34d55a102d7107b`.
Es software no oficial, no un plugin de ChatGPT. El directorio de plugins no
devolvió una integración SofaScore al buscarla. El plugin zKhadiri/Sofascore es
para Enigma2 y no es la integración de SportLab.

El proveedor declara football, basketball, tennis, american-football,
ice-hockey y baseball, entre otros deportes. La disponibilidad de cada liga,
jugador, estadística y período debe verificarse con datos reales. El código
es autohospedado; no implica acceso ilimitado ni continuidad del proveedor.

## Arranque en un equipo con Docker

Desde la raíz del repositorio:

```bash
docker compose -f deploy/sofascore.compose.yaml up -d --build
python -m sportlab.data.sofascore health
```

Abrir http://127.0.0.1:8000 y añadir una liga/equipo/jugador por nombre o ID,
elegir temporadas y estadísticas y descargar dentro del presupuesto de
solicitudes. Respetar los permisos y términos del proveedor; ante una negativa
persistente, detener las consultas. No habilitar proxies ni resolución de
desafíos para sortear el bloqueo observado.

El servicio queda limitado al equipo local. No publicar el puerto en Internet.
Para una instancia propia ya desplegada, usar HTTPS y las variables
`SPORTLAB_SOFASCORE_URL` y `SPORTLAB_SOFASCORE_TOKEN`. Este último corresponde al
token del servicio autohospedado, no a una cuenta SofaScore.

## Consultas reproducibles

```bash
python -m sportlab.data.sofascore events --sport NHL --before 2026-10-15
python -m sportlab.data.sofascore statistics --event-id ID_VERIFICADO
python -m sportlab.data.sofascore trend --input observaciones.json --event-key soccer:match:corners:90min --line 7.5 --direction over --as-of 2026-10-16T00:00:00Z --window 10
```

`events` lee el catálogo descargado del servicio, con hasta cinco páginas de
200 registros y marca `truncated` si no agotó el catálogo; no inicia descargas.
`statistics` devuelve el payload con fecha de extracción y rechaza estadísticas
ausentes o con error aunque exista una copia anterior.

`trend` recibe observaciones normalizadas explícitamente: no interpreta un
marcador de tenis como juegos ni deduce estadísticas de otro mercado. Ejemplo
de estructura (ilustrativo, no un partido real):

```json
[{"event_id":1,"start_utc":"2026-10-01T20:00:00Z","status":"completed","event_key":"soccer:match:corners:90min","value":8}]
```

Cada valor debe proceder del campo y período exactos de la estadística, y
acompañarse en su archivo de trabajo de URL/ID fuente, extracción y split.
Para localía, rival o superficie, filtrar la muestra antes del cálculo y usar
la misma definición de mercado. Aún no hay mapeo automático de todas las
estadísticas deportivas ni conexión MCP ni importación a Neon.

El cálculo admite L5/L10/L20/L30 mediante `--window`; muestra victorias,
derrotas, pushes, faltantes y el historial. Excluye encuentros no completados y
posteriores al corte. Deduplica IDs y rechaza registros contradictorios.
El denominador observado incluye pushes; los faltantes no son ceros ni se
reemplazan con partidos más antiguos para completar artificialmente la ventana.
Una frecuencia 8/10 es un hecho histórico, no una probabilidad futura ni un pick.

Neon sigue siendo el destino de datos dinámicos cuando la conexión real se
valide. GitHub conserva este adaptador, configuración, pruebas y documentación.
