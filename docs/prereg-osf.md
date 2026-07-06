# Preregistro — Palo Alto Bench

> **Documento listo para subir a OSF** (plantilla OSF Preregistration). Congela hipótesis, diseño, métricas y plan de análisis ANTES de ejecutar cualquier modelo evaluado. Una vez registrado (fecha + DOI), no se modifica; cualquier desviación se reporta como tal en el preprint.
>
> Estado: **borrador final — pendiente de registro en OSF**. Al registrar: anotar aquí fecha, URL y hash del commit del repo.

## 1. Título

*Palo Alto Bench: Can Frontier LLMs Detect Symmetrical Escalation and Double Binds, and Produce Valid Reframes? A Bilingual (Spanish/English) Benchmark.*

## 2. Autoría

Diego Quinde (concepción, constructos, autoría de ítems, anotación clínica, juez humano, análisis).

## 3. Descripción del estudio

Evaluamos si los modelos de lenguaje de frontera (1) **detectan** dos patrones interaccionales patológicos definidos por la Escuela de Palo Alto —escalada simétrica (Watzlawick, Beavin & Jackson, 1967) y doble vínculo (Bateson, Jackson, Haley & Weakland, 1956)—, (2) **localizan** su estructura interna, y (3) **producen reencuadres válidos** (Watzlawick, Weakland & Fisch, 1974), en español e inglés, sobre viñetas-diálogo de autoría experta que nunca nombran los constructos.

Definiciones operacionales, rúbricas y guía de anotación: congeladas en el repositorio antes de este registro ([constructs.md](constructs.md), [rubrics.md](rubrics.md), [item-schema.md](item-schema.md); set semilla congelado 2026-07-05).

## 4. Hipótesis (confirmatorias)

Para cada modelo evaluado M y lengua L:

- **H1 (jerarquía de dificultad de detección).** El F1 de la clase `double_bind` en Tarea A será **menor** que el F1 de la clase `symmetrical_escalation`, porque el doble vínculo exige razonamiento multinivel (contenido vs. meta-comunicación). Direccional, por modelo×lengua.
- **H2 (brecha translingüe).** El rendimiento en **español será menor** que en inglés en al menos una de las tres tareas, comparando pares paralelos (`pair_id`). Direccional.
- **H3 (sobre-detección / sicofancia de prompt).** (a) La tasa de falsos positivos sobre ítems `none` será > 0 en la condición guiada; (b) será **mayor en la condición guiada** (lista cerrada de patrones) que en la neutra (pregunta abierta sí/no). Direccional.
- **H4 (producir < detectar).** Para cada modelo, la proporción de reencuadres **válidos** (Tarea C, umbral congelado) será **menor** que la proporción de ítems patológicos correctamente detectados en Tarea A guiada, sobre el mismo subconjunto de ítems C-aplicables.

**Exploratorias (no confirmatorias, se reportan como tales):** diferencias entre subtipos de doble vínculo (`logical_type` vs. `pragmatic_paradox`) en Tareas A y B; tasa de alucinación de componentes en Tarea B; diferencias entre registros (pareja/familia/trabajo/clínico/amistad); confusión escalada↔rigidez complementaria.

## 5. Diseño

### 5.1 Materiales

- **Ítems:** viñetas-diálogo sintéticas de autoría experta, esquema en `items/schema.json`. Cada concepto de ítem existe como **par paralelo ES/EN** (`pair_id`), redacción nativa en cada lengua, misma estructura de turnos.
- **Set semilla (congelado 2026-07-05):** 15 pares (30 estímulos) — 5 escalada simétrica, 4 doble vínculo (2 `logical_type`, 2 `pragmatic_paradox`), 3 rigidez complementaria, 3 `none` adversariales. Función: calibración del juez-LLM y piloto de formato. **No entra en el análisis confirmatorio.**
- **Set de evaluación (a construir tras este registro, ANTES de correr ningún modelo evaluado):** mínimo **120 conceptos** (240 estímulos), objetivo 150. Composición fijada: ~30% escalada simétrica, ~25% doble vínculo (≈mitad por subtipo), ~20% rigidez complementaria, ~25% `none` (todos con `distractor_of`). Registros: pareja, familia, trabajo, clínico (≥15%), amistad. Misma guía de anotación congelada; anotadora única (DQ), declarado como limitación.
- **Regla de no-fuga:** ningún estímulo contiene términos teóricos (verificado por script); ítems originales, no extraídos de manuales (control de contaminación); hash y fecha del dataset registrados al publicar.

### 5.2 Tareas y condiciones

| Tarea | Condición | Estímulo → respuesta pedida |
|---|---|---|
| A-neutra | Pregunta abierta | Diálogo → "¿patrón problemático? SÍ/NO + explica" |
| A-guiada | Lista cerrada | Diálogo → etiqueta(s) de {escalada simétrica, doble vínculo, rigidez complementaria, ninguno}, con definiciones operacionales de una línea, **orden aleatorizado por ítem** (semilla = hash del id) |
| B | Localización | Diálogo + descripción operacional del patrón presente (sin nombre teórico) → componentes con índice de turno y cita (JSON) |
| C | Generación | Diálogo → "otra manera de entender lo que les pasa, que encaje con los hechos y abra salidas nuevas, sin dar consejos" (el término "reencuadre" no aparece) |

Orden de ejecución por modelo: A-neutra → A-guiada → B → C, en llamadas independientes sin memoria compartida. C nunca recibe la etiqueta.

### 5.3 Modelos

Modelos de frontera disponibles vía API en la fecha de ejecución, con **versión exacta y fecha registradas** en `results/run-manifest.json`. Candidatos previstos: última generación de Anthropic (familia Claude), OpenAI (familia GPT) y Google (familia Gemini); opcionalmente un open-weights fuerte como línea base. La lista final se fija en el manifiesto **antes** de mirar ningún resultado; añadir modelos después se reporta como análisis adicional no confirmatorio.

### 5.4 Parámetros de inferencia

- Temperatura 0 (o el mínimo del proveedor); resto de parámetros por defecto, registrados.
- **n = 3 repeticiones** por ítem×tarea×modelo. Tareas A/B: respuesta agregada por **voto mayoritario** (etiqueta modal; empate = incorrecto); se reporta además la variabilidad entre repeticiones. Tarea C: se juzga la **repetición 1**; las otras dos se archivan.
- Prompts congelados en `runner/prompts/v1.json` (versionados; cualquier cambio = nueva versión y se reporta).

### 5.5 Jueces (Tarea C)

1. **Juez humano (DQ)** puntúa con la rúbrica de 5 ejes (1–4) todos los reencuadres generados sobre el **set semilla**, ciego al modelo de origen (orden aleatorizado, identificadores ocultos).
2. **Juez-LLM**: un único modelo juez fijo, **distinto de todos los generadores evaluados** (anti-autopreferencia), con el mismo prompt-rúbrica versionado, puntúa los mismos reencuadres.
3. **Criterio de calibración (congelado):** κ ponderado (pesos cuadráticos) juez-LLM↔DQ **≥ 0.60 en al menos 4 de los 5 ejes** sobre el set semilla. Si se cumple → el juez-LLM puntúa el set completo. Si no → segunda iteración del prompt del juez (una sola permitida, recalibrando sobre el semilla); si tampoco → toda la Tarea C la puntúa DQ a ciegas y se reporta.
4. **Umbral de validez de un reencuadre (congelado 2026-06-30):** ≥3 en ejes 1 (ajuste a hechos), 2 (cambio de marco) y 5 (apertura de conducta); ≥2 en ejes 3 (irreversibilidad) y 4 (asimilabilidad). Banderas de descalificación fuerzan el eje afectado a 1.

## 6. Variables

- **VD primarias:** Tarea A-guiada: F1 macro y por clase (multi-etiqueta). Tarea A (ambas condiciones): FP-rate sobre `none`. Tarea B: puntuación de componentes (2/1/0 por componente: turno exacto/adyacente/ausente-alucinado) para doble vínculo; Jaccard de turnos + acierto de posición simétrica para escalada. Tarea C: % de reencuadres válidos; media por eje.
- **VI:** modelo, lengua (ES/EN, intra-par), condición de prompt (neutra/guiada), clase, subtipo de bind, registro.

## 7. Plan de análisis

- **Incertidumbre:** IC 95% por bootstrap no paramétrico (B = 10 000), remuestreando **por `pair_id`** (respeta el emparejamiento ES/EN).
- **H1:** dentro de cada modelo×lengua, diferencia F1(escalada) − F1(doble vínculo); se confirma si el IC bootstrap unilateral excluye 0 en la dirección prevista.
- **H2:** comparaciones pareadas por `pair_id`. Tarea A-guiada: test de McNemar exacto (acierto/fallo ES vs. EN) por modelo. Tarea C: Wilcoxon de rangos con signo sobre la puntuación media de rúbrica por ítem (ES vs. EN). Se confirma H2 si al menos una tarea muestra déficit ES significativo tras corrección.
- **H3:** (a) IC 95% del FP-rate guiado excluye 0; (b) McNemar exacto pareado por ítem `none` (FP en guiada vs. neutra), por modelo.
- **H4:** por modelo, diferencia pareada por ítem (subconjunto C-aplicable) entre detección correcta (A-guiada, binaria) y reencuadre válido (C, binaria); IC bootstrap de la diferencia de proporciones, unilateral.
- **Corrección por comparaciones múltiples:** Holm dentro de cada hipótesis a través de modelos; α = 0.05.
- **Manejo de fallos (congelado):** *rechazo* del modelo (declina responder) = respuesta incorrecta/inválida, tasa reportada aparte. JSON malformado → 1 reintento con recordatorio de formato → si persiste, incorrecto. Error de API → hasta 3 reintentos → si persiste, ítem excluido para ese modelo y reportado. Ítems excluidos > 5% en un modelo → se reporta el modelo como evaluación parcial.
- **Sin regla de parada por resultados:** se ejecuta el set completo una vez, tal como quede fijado en el manifiesto.

## 8. Datos y materiales

Ítems, gold labels, prompts, código del runner y de scoring, salidas crudas de los modelos, puntuaciones de ambos jueces y este preregistro: **públicos** (GitHub + OSF; datos CC BY 4.0, código MIT). Los reencuadres generados por modelos se publican identificando el modelo.

## 9. Limitaciones declaradas de antemano

- Ítems sintéticos de autoría experta: fuerte control de confusores, menor realismo ecológico.
- **Anotadora única (DQ)** para gold labels y juez humano: sin κ inter-anotador humano; se declara y se propone segundo anotador como extensión.
- El juez-LLM, aun calibrado, hereda sesgos de estilo; mitigado con exemplars multi-técnica e instrucción anti-molde.
- Resultados válidos para las versiones de modelo pinneadas en la fecha de ejecución.

## 10. Cronograma

Registro OSF → construcción del set completo (guía congelada) → corrida sobre set semilla + calibración del juez → corrida confirmatoria → análisis según §7 → release + preprint (arXiv cs.CL).
