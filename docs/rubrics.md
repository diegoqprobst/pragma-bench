# Rúbricas y protocolo de puntuación

## Tarea A — Detección (objetiva)

Conjunto de etiquetas: `{symmetrical_escalation, double_bind, complementary_rigidity, none}` (multi-etiqueta).

- Comparar predicción vs. `task_a.gold_labels`.
- **F1 macro** y **F1 por clase**; **matriz de confusión** (qué se confunde con qué).
- **FP-rate sobre `none`**: proporción de ítems `none` en que el modelo afirma algún patrón. Métrica primaria de sobre-detección (H3).
- Reportar por lengua (ES, EN) y la brecha ES−EN.

## Tarea B — Localización (semiobjetiva)

### Doble vínculo — 3 componentes
El modelo debe señalar, con índice de turno y cita, los tres:
- `primary_injunction`
- `secondary_injunction` (contradictoria en otro nivel)
- `no_metacommunication` (bloqueo de comentar la contradicción)

(La inescapabilidad del campo —inyunción terciaria— es precondición estructural del ítem, no un turno a localizar; ver [constructs.md](constructs.md).)

Puntuación por componente: **2** = turno correcto y rol correcto; **1** = parcial (turno correcto, rol mal nombrado, o turno adyacente); **0** = ausente o alucinado. Métrica: media de componentes + **tasa de alucinación** (componentes afirmados que no existen en el gold).

### Escalada simétrica
- **Overlap de turnos**: Jaccard entre los turnos marcados por el modelo y `task_b.escalation_turns`.
- **Posición simétrica**: nombra correctamente el rol/recurso en disputa (sí/no), juez ligero.

## Tarea C — Reencuadre (rúbrica)

Cada reencuadre se puntúa en **5 ejes**, escala **1–4** (1 = ausente/contraproducente, 2 = débil, 3 = adecuado, 4 = fuerte). Los ejes son los criterios de validez de Watzlawick, Weakland & Fisch (1974):

| # | Eje | 1 | 4 |
|---|---|---|---|
| 1 | **Ajuste a los hechos** | Inventa o niega datos del caso | Totalmente compatible con los hechos concretos |
| 2 | **Cambio de marco** | Paráfrasis / "endulza" sin reorganizar el sentido | Reorganiza el significado; marco genuinamente nuevo |
| 3 | **Irreversibilidad** | El problema reabsorbe el marco; truco evidente | Visto el marco nuevo, cuesta volver al viejo |
| 4 | **Asimilabilidad** | Interpretación externa, rechazable, jerga | Encaja con el lenguaje/visión del receptor |
| 5 | **Apertura de conducta** | No cambia nada accionable; consejo o empatía vacía | Interrumpe el patrón y habilita opciones nuevas |

**Banderas de descalificación** (fuerzan eje correspondiente a 1): pensamiento positivo ("míralo por el lado bueno"), negación/minimización, consejo directo, interpretación causal-histórica, o reencuadre que **culpa** a la víctima.

**Umbral de validez** (CONGELADO 2026-06-30, va al preregistro): un reencuadre cuenta como *válido* si obtiene **≥3 en los ejes 1, 2 y 5** y **≥2 en los ejes 3 y 4** (los ejes 1/2/5 son el corazón de la definición). No se reajusta tras ver resultados.

### Los reencuadres de referencia NO son un molde
`task_c.reference_reframes` trae varios ejemplares, **cada uno de una técnica sistémica distinta** (connotación positiva, redefinición del problema, prescripción/paradoja, reubicación relacional/circular). Son ejemplos de *qué cuenta como válido*, no la respuesta correcta. El juez puntúa por los 5 ejes de validez, **no** por parecido literal a un ejemplar; un reencuadre con una técnica que no está entre los ejemplares puede sacar 4 en todos los ejes. Esto evita sesgar al juez hacia un estilo.

### Protocolo de jueces
1. **Juez humano experto (DQ)** puntúa todos los ítems del set semilla a ciegas del modelo de origen (orden y procedencia aleatorizados).
2. **Juez-LLM** puntúa con la **misma rúbrica** (prompt versionado en el repo), con cadena de razonamiento por eje.
3. **Calibración**: se calcula acuerdo humano↔LLM (κ ponderado por eje / ICC) en el set semilla. Solo si el acuerdo es aceptable (preregistrar umbral, p. ej. κ≥0.6) se usa el juez-LLM para escalar a v1; si no, se mantiene puntuación humana o doble-humana.
4. **Anti-autopreferencia**: el juez-LLM nunca es del mismo modelo que generó el reencuadre que juzga; o se usa un juez fijo distinto para todas las respuestas. Reportar la elección.

## Reporte global
Para cada modelo × lengua × tarea: media + IC (vía repeticiones `n`). Tablas y figuras se generan desde `results/` (cuando exista el runner). Todo el material de prompting y los gold labels se publican.
