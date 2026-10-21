# Instrucciones de ejecución para Hermes

## Objetivo inmediato

Conseguir las líneas reales de appuesta.do mediante el navegador del PC y completar las recomendaciones NBA/NHL contra esas líneas. Fecha de referencia: 2026-10-21, zona America/Santo_Domingo, UTC-4. Al ejecutar, comprobar fecha/hora y estado de los eventos; no tratar un partido ya iniciado como prepartido.

1. Leer AGENTS.md del repositorio y los documentos de método indicados en CONEXIONES.md.
2. Identificar capacidades reales del PC: navegador disponible, sesión actual, checkout y conexiones locales. No asumir herramientas, MCP ni claves por los nombres de este chat.
3. Abrir https://www.appuesta.do/sportsbook/prelive?page=sport&sportId=67 y entrar en el DETALLE del partido, no quedarse en el carrusel de ganador.
4. Abrir Crear Apuesta, desplegar cada mercado y los controles Más jugadores/Ver más. Leer ambos equipos, todos los jugadores listados, líneas fijas y cuotas de Más y Menos. Las cuotas son datos: no pulsarlas para añadirlas al boleto.
5. NBA: extraer total del partido, total de ambos equipos, puntos, rebotes, asistencias, triples anotados y tapones. Si aparecen robos, pérdidas y combinaciones, se pueden registrar por separado. Identificar período y si incluye prórroga.
6. NHL: extraer goles totales del partido y goles de ambos equipos. Registrar si incluye prórroga/shootout. No ampliar a props NHL individuales sin petición.
7. Registrar por categoría: OBSERVED, COLLAPSED_NOT_READ, CLOSED, NOT_OFFERED, LOGIN_REQUIRED o ACCESS_ERROR. Solo usar NOT_OFFERED cuando una lectura del catálogo lo respalde; un campo no leído no demuestra ausencia.
8. Si exige inicio de sesión, el usuario lo hace localmente; retomar después. No exportar cookies, contraseñas, códigos ni tráfico de autenticación. Ante bloqueo/CAPTCHA, registrar el bloqueo y usar la intervención normal del usuario; no evadirlo.
9. Completar markets.json según markets.schema.json y un RESUMEN.md con fecha, categorías cubiertas, faltantes, errores y enlaces a evidencias. Guardar capturas recortadas del encabezado y mercado sin saldo ni datos personales.
10. Recalcular historial exacto y revisar contexto ANTES de convertir los datos en una recomendación. Entregar selecciones reales, no solo quintetos o promedios sin interpretación.

## Orden práctico

Primero comprobar estos cuatro mercados para resolver la petición pendiente:
- Hawks (Atlanta)–Magic (Orlando): triples de Nickeil Alexander-Walker.
- Timberwolves (Minnesota)–Heat (Miami): rebotes de Bam Adebayo y triples de LaMelo Ball.
- Pacers (Indiana)–Pelicans (New Orleans): puntos de Pascal Siakam.

Los umbrales antiguos son referencias analíticas, no precios ni líneas ofrecidas. Capturar la fija real aunque sea distinta; recalcular ambos lados de ESA línea. Después cubrir el resto de la cartelera NBA y los dos encuentros NHL que sigan pendientes.

## Filtro de jugadores y cálculo

- Recomendar props NBA del quinteto titular del partido. Puede ser proyectado, identificado como tal; no bloquear toda la cartelera por esperar confirmación.
- Excepciones de banca: solo rendimiento destacado documentado en pretemporada Y rol/minutos actuales sustentados. No mezclar pretemporada en los promedios de temporada regular.
- Mostrar una única media L10 por categoría solicitada. Guardar temporada/L5/L10/L20/L30, n real, pérdidas, pushes y faltantes. DNP no cuenta como cero.
- Historial principal: cada jugador/equipo contra distintos oponentes. H2H secundario.
- Para equipos: base A=(anotado por A+permitido por B)/2; base B=(anotado por B+permitido por A)/2; total=base A+base B. Seguir pesos/modelos versionados cuando corresponda. No sumar estadísticas individuales a totales de equipo en unidades incompatibles.
- En props, revisar defensa comparable, minutos, oportunidades, lesiones, descansos, cambios de equipo/rol. El promedio de un jugador frente al total permitido del rival no constituye por sí solo un modelo de props.
- No llamar seguras a las selecciones ni convertir 8/10 en 80% futuro. No ejecutar simulaciones inventadas: 10,000 corridas solo con modelo/entradas defendibles y registro de seed; si no, análisis descriptivo provisional.
- Máximo 10 selecciones por SGP del mismo partido, sumando equipos y jugadores; no completar diez por obligación ni multiplicar frecuencias correlacionadas.
- Clasificar PRINCIPAL/SECUNDARIO/NO APUESTA según evidencia y precio. Una cuota o línea ausente sigue ausente, no cero.
- Nombres distintivos de equipo primero, ciudad después; nombres completos NHL.
- Neon guarda datos dinámicos compactos, GitHub guarda metodología. Conservar versiones y fallos originales.

## Entregables

En outputs/hermes/<fecha-hora-UTC>/:
- markets.json con registros exactos del sitio, más markets.csv si es útil.
- RESUMEN.md con totales de eventos/categorías leídos y bloqueados; URLs, captura horaria y motivo.
- evidencias/ con capturas de mercado recortadas.
- análisis de las líneas realmente observadas, fuente y corte, medias y L5/L10/L20/L30; terminar con tablas de selecciones.

Si no hay conexión Neon, entregar archivos locales para importación posterior; no bloquear la extracción ni afirmar guardado en la base.
No colocar apuestas, enviar dinero, depositar, retirar, cambiar ajustes ni comunicar mensajes a terceros.
