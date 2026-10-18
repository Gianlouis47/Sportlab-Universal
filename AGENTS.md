# SportLab Universal — reglas operativas para Codex

No reconstruir SportLab desde cero. Trabajar sobre la rama actual y reutilizar el código, la metodología y los datos existentes.

## Flujo obligatorio

GOAL → DATA → ANALYSIS → SIMULATION → CONTRADICTION → RECHECK → VALIDATION → DECISION → RESULT → POSTMORTEM

## Antes de analizar una cartelera

1. Resolver fecha y zona horaria del usuario, partidos, estado en vivo, equipos, localía, abridores y mercados visibles. Excluir del análisis prepartido los juegos ya iniciados.
2. Leer primero la metodología versionada y la configuración activa: `knowledge/mlb/methods/mlb_notebook_method.md`, `config/defaults.yaml`, `sportlab/models/recent_form.py`, `sportlab/sports/mlb/runs.py`, `sportlab/sports/mlb/strikeouts.py` y el motor de simulación. Consultar la configuración y los snapshots de Neon. No elegir pesos de memoria ni inventar otra fórmula.
3. Buscar autónomamente en fuentes públicas actuales los datos que falten: calendario oficial, titulares, alineaciones, lesiones, descanso y uso del bullpen, datos de temporada y forma reciente, casa/visita, rival, parque/clima y líneas disponibles. Contrastar fuentes y fecha de corte. No pedir al usuario estadísticas públicas que se puedan consultar; las capturas sirven para reconocer mercados y cuotas observadas.
4. Etiquetar cada variable crítica CONFIRMADA, PROYECTADA o NO DISPONIBLE. Distinguir una cuota de captura de una cuota vigente. No convertir NULL en cero ni reutilizar estadísticas antiguas como si fueran actuales.
5. Para totales, hándicaps y props, aplicar `knowledge/markets/threshold_frequency.md`: comprobar en fuentes oficiales la frecuencia reciente **del evento exacto** en ambos lados del enfrentamiento, con denominador, fecha y split pertinente. Usarla como contraste de la proyección, nunca como probabilidad futura directa ni evidencia suficiente para declarar PRINCIPAL.

## Método de la libreta y MLB

- Calcular primero ataque y defensa por carreras anotadas/permitidas por juego. Para cada equipo, cruzar su ataque con las carreras permitidas por el rival; obtener las dos carreras esperadas y su suma. Usar la fórmula, los pesos y la dispersión versionados en el repositorio.
- Considerar temporada, L5/L10/L20/L30, casa/visita y H2H. Descomponer L10/L20/L30 en bandas no superpuestas; reducir o retirar H2H si una muestra pequeña o un marcador extremo sesga el promedio.
- Ajustar por ambos abridores, carga esperada de IP/BF y pitcheos, K%, BB%, K-BB%, whiff/CSW, repertorio, mano, contacto/K del rival, alineación, BvP ponderado por PA, bullpen, defensa, velocidad en bases y parque/clima cuando haya datos verificables. Una calificación 1–100 resume métricas; no reemplaza las tasas reales.
- Evaluar ML del juego completo, F5/H1 cuando existan datos, total en varias líneas, totales de ambos equipos y K de los DOS abridores, incluso si la captura o un analista muestran un solo prop. Para líneas enteras separar ganar, perder y push.
- Contrastar cada probabilidad de K simulada con salidas reales de temporada, últimas 5/10, local/visita y carga reciente. Si discrepan materialmente, investigar muestra, lesión, pitch count, alineación y distribución; corregir entradas y repetir. No declarar automáticamente un Over por K/9 alto.
- Una alineación confirmada sustituye la proyectada. Si falta, continuar con la mejor proyección publicada, marcar el resultado provisional y actualizar al confirmarse; no detener todo el análisis ni afirmar que está confirmada.

## Simulación y decisión

- Ejecutar realmente 10,000 corridas con seed, versión de modelo, entradas, corte temporal y supuestos reproducibles. Diferenciar una corrida del repositorio de una reproducción externa y de una simulación guardada previamente. No atribuir al motor resultados calculados con otros pesos.
- Reportar carreras esperadas, ML, probabilidades de cada línea relevante, team totals, K de los dos abridores, pushes, contradicciones y clasificación. No presentar porcentajes más precisos que los datos.
- Comparar con la probabilidad implícita y el valor a la cuota disponible solo DESPUÉS de estimar el evento. Sin precio vigente, expresar una inclinación condicionada y evitar llamarla ventaja confirmada.
- Cerrar con PRINCIPAL, SECUNDARIO o NO APUESTA y motivo concreto. Si faltan datos críticos o existe una contradicción sin resolver, no usar PRINCIPAL. Una captura de otro analista identifica juegos/mercados, pero jamás limita el universo de investigación ni valida sus picks.
- Comunicar primero la decisión en una tabla compacta. Explicar después las 2–3 variables que más la sostienen o la pueden refutar. Corregir explícitamente cualquier resultado anterior afectado por datos nuevos.

## Tenis

- Presentar siempre ataque, defensa, servicio, devolución, volea, consistencia, forma reciente y adaptación a la cancha de ambos jugadores en una tabla. Consultar `knowledge/tennis/ratings_method.md` y registrar superficie, fecha y fuente. Mostrar NO DISPONIBLE si una faceta no está medida; la cancha preferida es una categoría, no una nota 1–10.
- Investigar de forma autónoma estadísticas públicas actuales de cada jugador y superficie antes de completar las casillas. Una estimación 1–10 debe mostrar los datos, la muestra, la fuente y la regla de conversión; separar siempre las notas editoriales de las estimaciones propias. Si la evidencia es insuficiente, identificar la nota editorial como tal.
- Diferenciar calificaciones editoriales 1–10 de estadísticas observadas. No convertir la diferencia de notas en probabilidad ML, marcador 2–0, total de juegos ni selección apostable sin modelo de saque/devolución calibrado y datos actuales.
- Ante una cartelera solicitada, verificar el cuadro y el estado de TODOS los partidos; evaluar los favoritos relevantes antes de reducir a un ticket. No proponer a alguien ya eliminado. Consultar `knowledge/tennis/market_rules.md` para calcular y presentar por separado ML, juegos individuales de cada jugador y juegos conjuntos del partido. Las cuotas negativas pueden multiplicarse en un parlay, pero añadir selecciones reduce la probabilidad conjunta; no llamar asegurado a ningún partido.

## Código y almacenamiento

Neon es la fuente de registros dinámicos estructurados. GitHub es la fuente de código, modelos, pesos, pruebas, metodología y conocimiento durable. No guardar secretos, credenciales ni grandes dumps. Si una tarea modifica el motor, verificar pruebas y documentar limitaciones reales.

## Fuentes y tendencias persistentes

- Aplicar `knowledge/integrations/source_sync.md` al recolectar datos: fuentes
  gratuitas verificadas, Linemate/SofaScore como referencias prioritarias cuando
  sean accesibles, sin suponer acceso automático por una portada HTTP 200.
- Conservar versiones y procedencia en `core.source_snapshots`. No depender del
  plugin declinado ni reactivar BALLDONTLIE sin solicitud nueva.
- Para fracciones como 8/10 usar `sportlab/models/historical_trends.py`: mercado
  exacto, L5/L10/L20/L30, pushes, faltantes y corte de conocimiento. Ataque/defensa
  1–10 resume métricas; el efecto probabilístico pasa por tasas y modelo validado.

## Búsqueda obligatoria y continuidad con titulares proyectados — 2026-10-16

Esta política desarrolla el bucle de investigación y finalización. Es obligatoria para todos los deportes y para cada mercado solicitado.

1. **Buscar antes de declarar ausencia.** Consultar Neon y comprobar su corte; ante datos ausentes o antiguos, buscar fuentes actuales: liga/equipo oficial, proveedor deportivo conectado y fuentes públicas alternativas pertinentes. Continuar por vías útiles si una falla. No pedir al usuario estadísticas públicas recuperables ni cerrar por una tabla vacía, una herramienta ausente o el fallo de un solo proveedor. No evadir bloqueos ni reintentar indefinidamente la misma petición.
2. **Evidencia de búsqueda.** Registrar proveedor o URL, hora UTC, evento/temporada, dato buscado, resultado y error observado cuando exista. NO DISPONIBLE requiere intentos documentados y una explicación concreta. Distinguir herramienta no expuesta, fallo de autenticación, fallo de transporte, bloqueo del origen y campo ausente; no atribuir un 401/403 al origen sin observarlo. Si existe una vía alternativa útil, el estado sigue PENDIENTE, no se cierra por falta de datos.
3. **Continuar con una proyección trazable.** Usar el titular, portero, abridor, orden de bateo o rotación probable de una fuente actual identificada. Si solo hay alineaciones recientes, elaborar y etiquetar una proyección propia con su evidencia, lesiones, descanso y participación esperada. Plantilla habitual no equivale a alineación confirmada. No detener toda la cartelera por una confirmación pendiente; actualizar al conocerse el titular real.
4. **Resolver incertidumbre por mercado.** Evaluar escenarios plausibles de titular/suplente o variación de carga con datos disponibles. Si la conclusión resiste los escenarios, continuar con estado PROVISIONAL y límites visibles. Si cambia materialmente, limitar únicamente los mercados afectados hasta resolverla; continuar investigando el resto. No exigir portero confirmado como puerta universal para NHL. Su identidad afecta directamente la prevención de goles; tiros a puerta dependen principalmente de rol, minutos y volumen. Paradas del portero necesitan identidad/participación; K de pitcher necesitan abridor y carga esperada; hits de bateador requieren participación y PA/AB esperadas. No inventar porcentajes de ajuste ni escenarios sin evidencia.
5. **Explorar Over y Under y alternativas.** Investigar ganador, totales alternativos, ambos team totals y props pertinentes con cobertura. Evaluar ambos abridores MLB y bateadores relevantes, aunque la captura muestre un solo jugador. Mostrar línea exacta, período y liquidación; separar push. Si la línea alternativa no está verificada en la banca, identificarla como umbral analítico y no afirmar que se ofrece. La falta de cuota no impide una conclusión deportiva condicionada; sin precio no certificar rentabilidad.
6. **Conservar el método.** Cruzar ataque de cada equipo con producción permitida por su rival; revisar temporada, L5/L10/L20/L30, localía, calidad del rival y superficie cuando aplique. Mostrar denominadores reales, faltantes y corte. No completar artificialmente ventanas cortas ni usar ventanas superpuestas como muestras independientes. Frecuencia histórica, AVG por AB y probabilidad de 1+ hit por partido son cantidades distintas.
7. **Cerrar con evidencia, no con una espera genérica.** Completar cada evento con conclusión y clasificación sustentadas o bloqueo observado que detalle dato crítico, búsquedas y mercados afectados. PENDIENTE no equivale a NO APUESTA; una incertidumbre crítica no resuelta impide PRINCIPAL. Simular realmente cuando datos y modelo lo permitan; si no, dar análisis descriptivo/provisional sin fabricar probabilidades. Nunca buscar hasta forzar una apuesta.
8. **Persistencia y alcance.** Consultar la regla activa `sportlab_research_completion_loop` en Neon antes de analizar y aplicar este protocolo. Guardar snapshots, intentos relevantes, escenarios y cambios de estado con procedencia cuando haya acceso y esquema adecuados; confirmar escrituras. Estas son instrucciones operativas para agentes, no una garantía de cumplimiento automático de software ni de acierto deportivo.

## Base primordial universal de ataque y defensa — 2026-10-18

Aplicar obligatoriamente `knowledge/markets/universal_offense_defense_baseline.md` antes de cada análisis de equipos o jugadores. Calcular por separado producción a favor y permitida, cruzar ataque con defensa contraria en unidades comparables, sumar ambas proyecciones para total base y mostrar margen descriptivo para ganador. Adaptar por deporte, período y estadística exacta del mercado; tenis y props necesitan oportunidades y modelos específicos, no una suma ciega. Mostrar temporada, L5/L10/L20/L30 con denominadores reales, fuentes y corte. En carteleras NFL, cubrir todos los partidos solicitados, priorizar totales y añadir inclinación al ganador; no asumir que todos integran una sola combinada. La base no sustituye contexto, validación, simulación defendible ni análisis del precio.
