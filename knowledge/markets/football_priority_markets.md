# Fútbol: ganador, tiros de esquina y tarjetas

Actualización solicitada por el usuario: 2026-10-19.

## Alcance obligatorio

En cada análisis de fútbol investigar, además de goles y sus alternativas:
- Ganador del partido: 1X2 (victoria local, empate, victoria visitante). Distinguir ganador en 90 minutos de clasificación, ganador con prórroga/penaltis, doble oportunidad y empate no apuesta cuando sean alternativas pertinentes.
- Tiros de esquina: totales del partido y por equipo; Over, Under y líneas alternativas.
- Tarjetas: totales del partido y por equipo; Over, Under y líneas alternativas. Props individuales solo cuando participación y datos pertinentes estén disponibles.

Investigar estos mercados no obliga a recomendar todos ni a inventar líneas, cuotas o datos. Una carencia en corners o tarjetas no bloquea el análisis de los otros mercados. Buscar fuentes actuales útiles antes de declarar un dato no disponible; registrar intentos y errores observados.

## Datos y método por mercado

1. Resolver evento, competición, temporada, fecha/hora RD, estado, localía, alineaciones confirmadas o proyectadas, bajas, descanso y nivel de rivales. Excluir partidos iniciados del análisis prepartido.
2. Ganador: cruzar ataque y prevención de goles de ambos equipos; contrastar xG/xGA si existen, localía y contexto. Mantener el empate como desenlace explícito; una diferencia de promedios no es probabilidad de victoria ni prueba de rentabilidad.
3. Corners: obtener por separado corners a favor y concedidos de ambos equipos, por partido o por 90 minutos en unidades comparables. El cruce de producción/concesión es una referencia descriptiva propia de corners, no una predicción derivada de goles. Revisar ritmo, volumen de tiros/centros, estilo, bandas y efecto del marcador cuando estén medidos.
4. Tarjetas: obtener tarjetas recibidas y las recibidas por los rivales en los partidos de cada equipo (provocadas como descripción del registro, no atribución causal). Separar amarillas, segundas amarillas, rojas y puntos por tarjetas según fuente. Contrastar árbitro designado y su muestra, faltas, intensidad competitiva y alineaciones cuando existan datos; no inventar ajuste por árbitro ni sustituir disciplina por producción de goles.
5. Conservar historial individual frente a distintos oponentes como base, H2H como apoyo secundario. Calcular temporada y L5/L10/L20/L30 para la estadística exacta, con denominadores reales, corte, fuente y splits casa/visita. Identificar cambios de división, competición, entrenador o plantilla.
6. Contar la línea exacta y ambos extremos: un umbral bajo para Over y uno alto para Under cuando haya respaldo. Registrar aciertos, fallos, pushes y faltantes; no sumar ventanas superpuestas ni duplicar partidos. Un dato ausente es NULL, nunca cero; una tarjeta/corner de cero confirmado sí cuenta.
7. Verificar período y liquidación de la banca: normalmente 90 minutos más añadido, sin asumir prórroga. Para corners distinguir concedidos/ejecutados y reglas de repetición si son relevantes; para tarjetas comprobar cómputo de roja/segunda amarilla, banquillo, cuerpo técnico, sanciones posteriores al pitido y si el mercado usa número de tarjetas o puntos. No mezclar unidades ni proveedores incompatibles.
8. Frecuencia histórica no equivale a probabilidad futura. Simular solo con datos y modelo defendibles y registrar la ejecución real. Buscar contradicciones, revisar el contexto y después comparar línea/cuota vigente. Sin mercado observado, presentar umbral analítico y precio/disponibilidad no verificados.
9. Clasificar PRINCIPAL, SECUNDARIO o NO APUESTA con motivo por mercado; mantener PROVISIONAL si procede. No llamar seguro al favorito ni forzar ganador cuando el empate o el rival tengan respaldo.
10. Guardar en Neon observaciones y resúmenes compactos con fuente, corte, claves de evento/equipo, mercado, unidad, período, línea y reglas de liquidación; conservar versiones y resultados originales. GitHub guarda el método. No afirmar que se implementó un recolector o una sincronización automática por guardar estas instrucciones.

## Presentación

Conservar explicación y evidencia antes del cierre. Terminar con tablas de selecciones por deporte; en fútbol incluir ganador y tablas o filas específicas de goles, corners y tarjetas, con línea exacta, frecuencias y clasificación. Identificar umbrales no observados y faltantes antes de la última tabla; no añadir texto después de ella.
