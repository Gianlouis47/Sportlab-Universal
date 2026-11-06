# SportLab Universal: paquete para Hermes

Preparado el 21 de octubre de 2026. Repositorio: Gianlouis47/Sportlab-Universal.
Rama: sportlab-universal-refactor. Base de documentación: 1851881850820b335c60d0cc515c527989baf8d1.

## Arranque

Entrega a Hermes este mensaje:

> Continúa SportLab Universal desde este repositorio y rama. Lee AGENTS.md y handoffs/hermes/INSTRUCCIONES_HERMES.md. Tu primera tarea es extraer desde el navegador de mi PC las líneas reales de appuesta.do de los partidos NBA y NHL solicitados, abrir las categorías de jugadores y devolver mercados.json y RESUMEN.md con URL, hora y cobertura. Reutiliza el método y la base existentes. Trabaja en lectura: no coloques apuestas ni añadas selecciones al boleto. No me devuelvas únicamente nombres de titulares: quiero las selecciones y sus estadísticas contra las líneas reales. Reutiliza mis conexiones locales autorizadas; no publiques claves.

Clonar si todavía no existe un checkout:

```powershell
git clone --branch sportlab-universal-refactor --single-branch https://github.com/Gianlouis47/Sportlab-Universal.git
Set-Location Sportlab-Universal
```

Si ya existe, comprobar rama y cambios locales antes de actualizar. No resetear ni descartar trabajo.

## Contenido

- INSTRUCCIONES_HERMES.md: trabajo completo, prioridades y definición de terminado.
- CONEXIONES.md: endpoints conocidos, identificadores de Neon, credenciales necesarias y límites reales.
- ESTADO_2026-10-21.md: intentos de acceso y datos históricos ya disponibles.
- api-contracts.json: contratos MCP expuestos en este chat; no son una promesa de disponibilidad en otro cliente.
- markets.schema.json y markets.csv: estructura de retorno, sin líneas ficticias.
- sql/export_context.sql: consulta de reglas y snapshots existentes, solo lectura.
- .env.example: plantilla sin secretos.
- crear-paquete.ps1: copia explícita de documentación y código del checkout a una carpeta nueva y ZIP, incluyendo solo archivos versionados; las credenciales y datos locales sin versionar quedan fuera.

Para preparar el paquete independiente en Windows, desde el checkout:

```powershell
& .\handoffs\hermes\crear-paquete.ps1
```

El script escribe una carpeta nueva en el Escritorio y un ZIP junto a ella. Usa git archive sobre el commit local; no copia .env ni credenciales sin versionar. No ha podido ejecutarse en el entorno de este chat por un fallo de permisos del ejecutor; comprobar su ejecución en el PC. La carpeta del repositorio y los documentos sí quedan versionados.

Las credenciales OAuth de los conectores de ChatGPT no se pueden exportar como claves API. Hermes debe reutilizar conexiones locales o valores aportados por el titular en el entorno privado. Esta carpeta contiene configuración conocida y una plantilla, no claves inventadas.
