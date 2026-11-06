# Appuesta.do: captura y comparación de líneas

Actualización: 2026-10-21. Protocolo solicitado por el usuario. Regla activa: `sportlab_appuesta_line_history`.

## Acceso observado y cobertura

La navegación pública al detalle de un evento, «Crear Apuesta», los filtros de ambos equipos y «Más jugadores» permitió leer valores y cuotas. Los primeros intentos con instrucciones de navegación libres fallaron por tiempo de espera; el código de interacción directa sí funcionó. La sesión puede fallar y requerir una nueva apertura pública. Una portada HTTP 200 no demuestra lectura de mercados.

- NBA: 11 encuentros, siete categorías de jugador, 1,055 filas jugador/mercado de 153 nombres. La revisión actual encontró 110 titulares proyectados: 108 con líneas, 744 mercados de titulares y 1,488 evaluaciones de dirección.
- Categorías leídas: puntos, rebotes, asistencias, triples anotados, robos, tapones y pérdidas. Liquidación observada: incluye prórroga.
- NHL: la lectura anterior verificó Philadelphia Flyers–Buffalo Sabres y Florida Panthers–Ottawa Senators, total del partido y de equipos; sus etiquetas incluían prórroga y penaltis. Esta nueva captura de jugadores es exclusivamente NBA.
- NFL, fútbol, ATP/WTA, MLB y LIDOM pertenecen al alcance solicitado, pero no se ha verificado su detalle de líneas en esta revisión. Descubrir sus competiciones e IDs mediante navegación visible antes de declararlos accesibles.
- No se recorrieron todas las posiciones de los deslizadores, se seleccionaron cuotas ni se hicieron apuestas.

La captura pública de referencia, de 12:08 a 12:10 RD, está en `datasets/appuesta/2026-10-21_player_lines.json`. Es un fixture pequeño solicitado para el repositorio, sin saldo ni información de cuenta. No duplicar diariamente toda la base de jugadores en GitHub.

## Responsabilidades de almacenamiento

Neon conserva los registros dinámicos, sus versiones, errores, frecuencias y resultados. GitHub conserva este método, el contrato/configuración y el fixture pequeño de referencia. Nunca guardar claves, cookies, tokens, enlaces de sesión de navegador o datos del boleto personal en estos archivos.

`config/appuesta_tracking.json` declara el alcance y los IDs de deporte realmente observados. Un valor de ID ausente no equivale a cero ni autoriza a reutilizar un ID de ESPN/SofaScore.

## Contrato de observación

Guardar por captura: proveedor, liga/competición, ID del evento en la banca y mapping externo verificado, participantes, fecha de juego y hora UTC de lectura, URL, prepartido/en vivo, modo de apuesta, mercado original, unidad, sujeto, período, prórroga/penaltis, dirección, línea exacta, cuota americana y disponibilidad.

Para las capturas compactas de NBA, los diccionarios `categories` y `players` y la lista `columns` explican las filas. El índice de equipo es 0 visitante y 1 local. Una cuota ausente es NULL; una categoría sin desplegar es NO OBSERVADA.

## Historial y detección de cambios

1. Consultar el registro anterior antes de importar. Validar evento, fecha, mercado y reglas de liquidación; no comparar solo nombres de jugadores.
2. Para una línea fija del mismo evento, la identidad de serie incluye banca, liga, evento, sujeto/equipo, estadística, período, modo y liquidación. El valor de línea y la cuota son observaciones que pueden cambiar.
3. Guardar NUEVA_LINEA, CAMBIO_LINEA y CAMBIO_CUOTA por separado. Si línea y precio cambian juntos, conservar ambos valores, horas y motivo. Comparar cuotas de Más/Menos individualmente.
4. Entre partidos diferentes, registrar COMPARACION_OTRO_EVENTO, con nuevo rival/localía y rol. No describirlo como movimiento dentro del mismo mercado.
5. En alternativas simultáneas usar IDs nativos de mercado/selección si están visibles; si faltan, diferenciar umbrales concurrentes y no adivinar cuál sustituyó a cuál.
6. Canonizar y ordenar los valores para el hash de contenido; excluir el reloj de consulta. Si el contenido consecutivo no cambia, avanzar última comprobación sin duplicar otra versión. Una secuencia A→B→A conserva tres estados. No sobrescribir una observación más nueva con una lectura antigua.
7. Conservar toda versión publicada y su resultado. No borrar una recomendación fallida al cambiar la línea. No interpretar una categoría que desaparece temporalmente como resultado cero ni como retirada definitiva sin cobertura suficiente.

La comparación de las dos lecturas NBA del 21/10 detectó 32 cambios de umbral y 449 filas con cambios de precio. Son cambios de filas de mercado, no 481 partidos ni una garantía de permanencia de cuotas.

## Consulta y análisis

Abrir un evento público → «Crear Apuesta» → desplegar encabezados → cambiar equipo → «Más jugadores» → leer el contenido semántico del contenedor de mercados. Esperar controles visibles por carga asíncrona. El widget puede no aparecer íntegro en body.innerText; la captura semántica sí lo expuso. No usar endpoints privados adivinados, evadir CAPTCHA ni insistir tras bloqueos de autenticación o límite.

Cada análisis aplica ataque/defensa, historial individual contra rivales variados, localía/superficie y rol/minutos actuales. H2H es secundario. Una línea fija observada sustituye un umbral analítico anterior y obliga a recalcular su evento exacto. Frecuencia histórica no es probabilidad futura ni convierte un prop en PRINCIPAL.

En NBA aplicar `sportlab_nba_broad_history_filter`: L30, L50 y temporada recuperada como base amplia; L5/L10 como diagnóstico. No forzar cuatro apuestas por partido. Respetar titulares confirmados/proyectados y excepciones documentadas de banca. El máximo de 10 selecciones por SGP es un límite aportado por el usuario, no un objetivo.

Adaptar unidades y liquidación: NFL puntos y props específicos; fútbol goles/corners/tarjetas con cómputo y 90 minutos/prórroga; tenis juegos del jugador frente a juegos del partido, superficie y abandonos; MLB/LIDOM carreras, hits, bases totales y K de abridores con participación. LIDOM necesita identidad de su competición; no etiquetarla como MLB.

## Ejecución futura y errores

En cada consulta declarar cobertura real, juegos sin mercados y fuentes fallidas; conservar mensaje y hora. Un fallo de transporte no prueba un 401/403 del origen. Continuar por vías públicas útiles sin inventar datos.

Una tarea periódica ejecuta consultas discretas; no equivale a acceso permanente ni a un webhook. No prometer detección inmediata de todos los cambios. Validar lectura y escritura en cada ejecución, actualizar solo lo comprobado y notificar cambios o fallos concretos.
