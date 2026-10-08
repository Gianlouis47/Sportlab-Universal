# Uso conjunto de Neon y Supabase

## Responsabilidades

| Base | Uso en SportLab Universal | Límite |
| --- | --- | --- |
| Neon `small-leaf-72827293` / `sportlab` | Identidad de eventos, equipos y atletas; estado vigente, alineaciones, líneas, snapshots actuales, reglas, simulaciones y resultados del modelo. | No interpretar un snapshot antiguo como estado confirmado del día. |
| Supabase `xuebtkafypivqygyqgcv` / `strikeoutlab` | Historial MLB de StrikeoutLab: salidas reales de abridores y ponches (`public.game_logs`), tasas del rival (`public.team_k`), splits y análisis históricos que todavía no estén completos en Neon. Consultas históricas de solo lectura. | No tomar predicciones/picks antiguos como resultados; no sobrescribir en bloque Neon con copias de Supabase ni asumir que Supabase cubre NFL, NHL, tenis o fútbol. |

El repositorio conserva los métodos y adaptadores. **El método de frecuencia es una regla activa en Neon** (`core.framework_rules.cross_sport_exact_threshold_frequency`) y la implementación está en `sportlab/models/threshold_frequency.py`; no hace falta duplicar la misma regla en la base histórica de Supabase.

## Secuencia para un evento MLB

1. Leer en Neon la identidad, calendario, perfiles recientes, estado actual y reglas, con fecha de corte anterior al evento.
2. Para la frecuencia de ponches, consultar los resultados de cada salida real del abridor en Supabase `game_logs` por temporada, fecha anterior al evento, línea exacta y participación efectiva. Consultar también la frecuencia de esa misma línea que han permitido los bateadores rivales frente a abridores; verificar que el historial cubre el período y el rival correspondiente. `team_k` y splits sirven como contexto adicional, no como sustituto automático de resultados por salida.
3. Si Neon contiene el mismo resultado real, resolver por ID de juego, MLB ID de jugador, temporada y fecha; preferir el registro oficial más reciente. Registrar procedencia y corte de cada muestra, evitar contar duplicados o partidos posteriores. Completar huecos con la fuente oficial MLB antes de inferir un porcentaje.
4. Ejecutar el filtro de frecuencias y después el modelo deportivo que incluye carga de trabajo, pitcher, alineación, bullpen y defensa; validar contradicciones, precio y reglas de push. Guardar el análisis/simulación nueva en Neon, no en ambas bases.

El adaptador de Supabase requiere una conexión **solo del lado del servidor** mediante `SPORTLAB_SUPABASE_DATABASE_URL`; no poner credenciales en GitHub ni en clientes públicos. Si la base está inactiva o la conexión falla, reportar `NO DISPONIBLE` para esa fuente y buscar los mismos resultados en MLB antes de clasificar. No usar un dato vencido como actual.

Una vez configurada la conexión, `sportlab mlb-k-frequency --pitcher 'Nombre' --opponent NYY --as-of 2026-08-30 --season 2026 --line 5.5` consulta únicamente salidas anteriores al corte y ejecuta la calculadora exploratoria. La conexión SQL inicia una transacción de solo lectura. Las líneas enteras necesitan liquidación de push por separado y el comando las rechaza. Validar cobertura e identidad del pitcher frente a MLB antes de usar ese resultado en una apuesta.

El estado de conexión se verifica en cada sesión que lo necesite. La reactivación del 08/10/2026 fue solicitada para aprovechar la base histórica; comprobar que llegó a `ACTIVE` y que las filas siguen disponibles antes de usarla.
