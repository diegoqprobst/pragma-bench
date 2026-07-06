# Plan de publicación y apertura

Alineado con tu estrategia: el portero ya no es el peer-review sino el **portafolio público y verificable**. El preprint + dataset abierto + preregistro son, juntos, una pieza de portafolio fuerte y un foso difícil de copiar.

## Principios

- **Abierto desde el inicio.** Ítems, prompts, código de evaluación, gold labels y resultados crudos, todo público.
- **Preregistro antes de correr modelos.** Congelar hipótesis, métricas y umbrales en OSF para blindar la credibilidad sin depender de la puerta de credencial.
- **Reproducible.** Versiones de modelo y fecha fijadas; prompts versionados; semillas y parámetros registrados.

## Secuencia

1. **Set semilla validado** (12–20 ítems bilingües, anotación experta DQ, guía de anotación congelada).
2. **Preregistro en OSF** — hipótesis (H1–H4 en [design.md](design.md)), tareas, métricas, umbral de "reencuadre válido", plan de análisis, criterio de calibración del juez-LLM. Fecha y hash.
3. **Construcción del set completo** (~120–180 conceptos × 2 lenguas) siguiendo la guía congelada.
4. **Corrida de frontera** + análisis según el plan preregistrado.
5. **Release**:
   - **Dataset** → repositorio GitHub (`diegoqprobst/pragma-bench`) y, opcionalmente, Hugging Face Datasets con tarjeta.
   - **Datos/preregistro/materiales** → OSF (DOI).
   - **Preprint** → arXiv **cs.CL** (PLN / evaluación de LLMs es el encuadre más natural; cs.HC o cs.MA como cross-list). Evita el muro de credencial de PsyArXiv.
6. **Revista nicho** (opcional, segundo tiempo) — venue de PLN clínico / psicología computacional para el ítem peer-reviewed que persigues.

## Esqueleto del preprint

1. **Introducción** — los LLMs se usan ya en contextos de apoyo emocional; ¿entienden la *pragmática relacional*, no solo el contenido? Hueco: ningún benchmark mide constructos sistémicos (Palo Alto).
2. **Trasfondo** — escalada simétrica, doble vínculo, reencuadre (Watzlawick 1967; Bateson et al. 1956; Watzlawick et al. 1974).
3. **Palo Alto Bench** — diseño de 3 tareas, bilingüe, controles anti-confusión, rúbricas.
4. **Métodos** — modelos, prompts, jueces, calibración, preregistro.
5. **Resultados** — A/B/C × modelo × lengua; sobre-detección; brecha ES−EN; acuerdo de jueces.
6. **Discusión** — qué tipo de incomprensión pragmática revela; implicaciones para IA de apoyo emocional; límites (ítems sintéticos, una anotadora experta).
7. **Ética y límites** — no es una herramienta clínica; riesgo de uso indebido; los reencuadres del modelo no son terapia.

## Riesgos de validez a declarar por adelantado

- **Ítems sintéticos** (autoría experta) → fuerte en control de confusores, débil en realismo ecológico. Mitigar con varios registros y, si se puede, una submuestra inspirada en transcripciones reales anonimizadas.
- **Una sola anotadora experta (DQ)** → reportar como límite; idealmente sumar un segundo clínico para κ inter-anotador en el set semilla.
- **Juez-LLM** → solo se usa a escala si calibra contra DQ por encima del umbral preregistrado; declarar anti-autopreferencia.
- **Contaminación** → ítems originales no extraídos de manuales; registrar fecha/hash.

## Autoría y créditos

- Diego Quinde (concepción, constructos, anotación clínica, análisis).
- Colaboradores potenciales: segundo anotador clínico; alguien de PLN si hace falta para el runner/estadística.
