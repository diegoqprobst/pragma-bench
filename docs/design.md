# Palo Alto Bench — Diseño

## Pregunta de investigación

¿En qué medida los modelos de frontera (1) **detectan** escalada simétrica y doble vínculo en diálogos breves, (2) **localizan** su estructura, y (3) **producen reencuadres válidos** — y cómo varía todo esto entre **español e inglés**?

Hipótesis registrables (ver [publication-plan.md](publication-plan.md)):
- **H1** — La detección de doble vínculo (Tarea A/B) es sensiblemente más baja que la de escalada simétrica, por requerir razonamiento multinivel (contenido vs. meta-comunicación).
- **H2** — Existe una brecha ES↔EN (rendimiento menor en español) en al menos una tarea.
- **H3** — Los modelos **sobre-detectan**: la tasa de falsos positivos en ítems `none` es > 0 y crece cuando el prompt menciona los constructos.
- **H4** — La producción de un reencuadre válido (Tarea C) es la capacidad más débil y la de menor acuerdo entre jueces.

## Las tres tareas

### Tarea A — Detección (clasificación)
**Entrada:** una viñeta-diálogo (sin nombrar el constructo).
**Salida pedida:** etiqueta(s) del conjunto `{symmetrical_escalation, double_bind, complementary_rigidity, none}` (multi-etiqueta; un diálogo puede contener más de un patrón).
**Mide:** reconocimiento del patrón.
**Métrica:** F1 macro y por clase; matriz de confusión (clave para ver qué se confunde con qué). Reporte separado de **falsos positivos sobre `none`** (sobre-detección, H3).

### Tarea B — Localización / estructura
**Entrada:** la misma viñeta + se informa al modelo qué patrón contiene (condicionado a A correcta o dado el gold).
**Salida pedida:**
- Doble vínculo → señalar **inyunción primaria**, **secundaria contradictoria** y **cláusula de no-salida** (índices de turno + cita).
- Escalada simétrica → señalar los **turnos de la curva ascendente** y nombrar la posición simétrica en disputa.
**Mide:** comprensión estructural, no solo "huele a conflicto".
**Métrica:** coincidencia con la anotación experta (overlap de turnos; presencia de los 3 componentes del doble vínculo). Penaliza alucinar componentes ausentes.

### Tarea C — Reencuadre (generación)
**Entrada:** el problema presentado en la viñeta.
**Salida pedida:** un reencuadre del problema dirigido al hablante/sistema.
**Mide:** capacidad de intervención clínica.
**Métrica:** rúbrica de 5 ejes (criterios de validez de Watzlawick; ver [rubrics.md](rubrics.md)), puntuada por **(a) juez humano experto** (DQ, formación clínica) y **(b) juez-LLM** con la misma rúbrica. Se reporta acuerdo inter-juez (κ ponderado / ICC) y se calibra el juez-LLM contra el humano antes de usarlo a escala.

## Diseño bilingüe (pares paralelos ES/EN)

- Cada ítem-concepto se redacta como **par paralelo**: una versión ES y una EN que comparten `pair_id`, constructo y estructura, pero **redactadas con naturalidad cultural** (no traducción literal — nombres, registros y modismos propios de cada lengua).
- Esto permite comparar **el mismo fenómeno** entre lenguas controlando estructura, y aísla la brecha translingüe (H2) de diferencias de contenido.
- Anotación de la estructura (Tarea B) **alineada** entre las dos versiones cuando es posible (mismos roles en los índices de turno).

## Controles contra confusores

| Riesgo | Control de diseño |
|---|---|
| Pattern-matching léxico | Las viñetas **no** usan términos teóricos ni etiquetas. |
| "Todo es patología" (sobre-detección) | ~⅓ de ítems son `none` o distractores adversariales (`complementary_rigidity`, desacuerdo simple, orden contradictoria comentable). |
| Sicofancia del prompt | Dos formatos de prompt: *neutro* ("¿qué ocurre entre estas personas?") vs. *guiado* (lista cerrada de etiquetas). Se compara la tasa de FP entre ambos (H3). |
| Atajo posicional / orden de opciones | Aleatorizar orden de etiquetas; balancear qué hablante inicia. |
| Contaminación / memorización | Ítems **autoría experta original**, no extraídos de manuales conocidos; hash + fecha de publicación registrados. |
| Fuga de la respuesta entre tareas | A se pregunta antes que B en sesiones separadas; C no recibe la etiqueta. |

## Modelos (cuando se ejecute)

Conjunto de frontera, fijando versión y fecha:
- Anthropic — Claude Opus 4.8, Claude Sonnet 4.6
- OpenAI — familia GPT/o más reciente disponible
- Google — Gemini más reciente
- (Opcional) un *open-weights* fuerte como línea de base (p. ej. Llama/Qwen) para contraste.

Parámetros: temperatura baja fija (p. ej. 0.0–0.3), `n` repeticiones para estimar varianza, prompts versionados en el repo. Todo el material de prompting es público.

## Métricas — resumen

- **A:** F1 macro / por clase, matriz de confusión, FP-rate sobre `none`, brecha ES−EN.
- **B:** F1 de componentes (doble vínculo: 3 componentes), overlap de turnos (escalada), tasa de alucinación de componentes.
- **C:** media por eje de rúbrica (1–4), % de reencuadres "válidos" (umbral preregistrado), acuerdo humano↔LLM, brecha ES−EN.

## Tamaño objetivo (v1)

- ~120–180 conceptos de ítem → ×2 lenguas = ~240–360 estímulos.
- Balance aproximado: 30% escalada simétrica, 25% doble vínculo, 20% rigidez complementaria, 25% `none`.
- Cada constructo cubre varios **registros**: pareja, familia (parento-filial), trabajo, clínico, amistad.
- Tarea C se aplica al subconjunto con problema presentable (escalada, doble vínculo, rigidez).

## Roadmap

- [x] **v0 — diseño**: constructos, rúbricas, esquema, set semilla.
- [x] **v0.1 — set semilla validado y CONGELADO** (2026-07-05): 15 pares ES/EN (30 ítems) autoría experta, revisados y aprobados por DQ. Balance 5 escalada / 4 doble vínculo (2 `logical_type` + 2 `pragmatic_paradox`) / 3 rigidez complementaria / 3 `none`. Guía de anotación en [item-schema.md](item-schema.md). Pendiente para el set completo: registro clínico (0 en el semilla) y subir `none` a ~25%.
- [x] **v0.2 — preregistro redactado** (2026-07-05): [prereg-osf.md](prereg-osf.md) con H1–H4 operacionalizadas, plan de análisis y manejo de fallos. **Pendiente: registrarlo en OSF** (acción de Diego; anotar fecha/DOI al hacerlo).
- [x] **v0.3 — runner** (2026-07-05): `runner/` con prompts congelados (`prompts/v1.json`), ejecución multi-proveedor reanudable y scoring completo; pipeline verificado en modo mock. La calibración del juez-LLM contra DQ ocurre tras la primera corrida sobre el semilla.
- [ ] **v1 — set completo** (~120–180 conceptos) + corrida de frontera + análisis.
- [ ] **v1 — release**: dataset (GitHub/Hugging Face), código, resultados; preprint arXiv (cs.CL) + OSF.

## Decisiones tomadas (2026-06-30)

- **Nombre:** Palo Alto Bench.
- **Anotación:** una sola anotadora experta (DQ) por ahora. Se declara como límite de validez en el preprint; un segundo anotador clínico (para κ inter-anotador) queda como mejora opcional futura.
- **Umbral de "reencuadre válido"** (Tarea C): congelado en **≥3 en los ejes 1, 2 y 5** y **≥2 en los ejes 3 y 4** (ver [rubrics.md](rubrics.md)). No se reajusta tras ver resultados.
