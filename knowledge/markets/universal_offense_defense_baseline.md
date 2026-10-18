# Cruce universal de producción ofensiva y permitida
Fecha: 2026-10-18. Regla operativa permanente solicitada por el usuario.

## Aplicación obligatoria
Antes de analizar un total, total de equipo, ganador, hándicap o prop, calcular por separado la producción a favor y permitida de ambos participantes cuando sean métricas comparables. Reutilizar `sportlab/models/offense_defense.py`; no reconstruir el motor ni reemplazar modelos específicos existentes.

O_A = suma de producción a favor de A / partidos u oportunidades observadas.
D_A = suma de producción permitida por A / partidos u oportunidades observadas.
E_A = (O_A + D_B) / 2.
E_B = (O_B + D_A) / 2.
Total base = E_A + E_B.
Margen base = E_A - E_B.

Mostrar tasas originales, denominadores, unidad, período, fecha de corte y fuente. Una producción permitida menor representa mejor prevención. O+D describe el entorno de anotación; no mide fuerza. El margen indica una inclinación descriptiva al ganador, no una probabilidad de victoria ni valor de apuesta.

## Adaptación por deporte y mercado
- MLB: carreras anotadas/permitidas por juego; separar juego completo de F5/H1 y ajustar por ambos abridores, alineaciones y bullpen.
- NFL: puntos anotados/permitidos por partido; contrastar eficiencia por posesión, quarterback, lesiones, localía, descanso y rivales.
- NBA/WNBA: mostrar puntos anotados/permitidos por partido y contrastar eficiencia por 100 posesiones y ritmo. No sumar tasas por 100 posesiones y llamarlas puntos por partido.
- NHL: goles anotados/permitidos por juego, portería, equipos especiales y métricas por 60 minutos cuando existan. Usar nombres completos.
- Fútbol: goles por partido/per 90 y xG/xGA como contraste separado. Corners, tarjetas y tiros necesitan sus propias tasas producidas/permitidas; los goles no sustituyen estas métricas.
- Tenis: adaptar ataque/defensa a servicio/devolución y superficie. Los juegos ganados/cedidos describen la muestra; no permiten aplicar directamente la fórmula aditiva para pronosticar juegos, sets o ML. Modelar las oportunidades de saque/devolución y reglas del formato.
- Jugadores: utilizar la estadística exacta del prop, oportunidades previstas y producción que permite el rival a un rol comparable. Puntos, rebotes, asistencias, hits, bases totales, K, tiros y goles tienen denominadores distintos. Promedio por AB no equivale a probabilidad de 1+ hit por partido. No dividir ni promediar tasas con unidades incompatibles ni aplicar ciegamente la fórmula de equipos a jugadores.

## Contraste de líneas
Comprobar ambas direcciones y alternativas exactas, temporada y L5/L10/L20/L30 con n real, ganar/perder/push/faltante y corte previo al evento. Separar historial de cada participante de H2H. No sumar ventanas solapadas ni tratar dos historiales con partidos comunes como una muestra independiente.
Si faltan partidos para una ventana, mostrar n recuperado; no rellenar con ceros. Etiquetar temporadas previas y diferencias de plantilla, superficie, localía o rol.
La frecuencia histórica no es probabilidad futura. Un promedio no determina la distribución del total. Ajustar contexto, simular solo con modelo defendible y ejecutar realmente las corridas declaradas, contrastar contradicciones y después revisar precio.

## Cobertura y decisión
Para una cartelera solicitada, analizar todos los eventos prepartido. En NFL el usuario prioriza totales y pide además inclinación matemática al ganador. Esto no obliga a apostar todos los partidos ni a una única combinada.
Las alternativas no observadas en la banca se presentan como umbrales analíticos condicionados. Sin precio vigente no afirmar rentabilidad. Clasificar PRINCIPAL, SECUNDARIO o NO APUESTA; conservar PROVISIONAL cuando la evidencia o el contexto lo requieran. Una baja crítica afecta el mercado correspondiente; continuar el resto del análisis.
