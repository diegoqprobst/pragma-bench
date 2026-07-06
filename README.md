# Palo Alto Bench

**¿Pueden los modelos de frontera reconocer patología interaccional y producir una intervención clínica válida?**

Un benchmark bilingüe (español / inglés) que evalúa tres capacidades sobre diálogos breves, ancladas en la teoría interaccional de la Escuela de Palo Alto (Watzlawick, Bateson):

1. **Detección de escalada simétrica** — reconocer el bucle de retroalimentación competitiva.
2. **Detección de doble vínculo** — reconocer la contradicción entre niveles lógicos + la imposibilidad de escapar o meta-comunicar.
3. **Producción de un reencuadre válido** — generar una reformulación del problema que ajuste a los hechos y cambie el marco de significado.

## Por qué importa

- Casi todos los benchmarks de PLN clínico son monolingües en inglés y se centran en clasificación de síntomas o riesgo. **Ninguno operacionaliza constructos sistémico-interaccionales** (escalada simétrica, doble vínculo, reencuadre).
- Estos constructos son *relacionales y multinivel*: no están en una sola frase sino en el patrón entre turnos. Son una prueba dura de comprensión pragmática, no de léxico.
- El diseño en pares paralelos ES/EN permite medir robustez translingüe en un dominio donde el español está infrarrepresentado.

## Estructura

```
pragma-bench/
├── README.md              ← este archivo
├── LICENSE                ← MIT (código) + nota CC BY 4.0 (datos)
├── CITATION.cff
├── docs/
│   ├── design.md          ← arquitectura del benchmark (3 tareas, scoring, controles)
│   ├── constructs.md      ← definiciones operacionales + criterios de validez + anclaje teórico
│   ├── rubrics.md         ← rúbricas de puntuación (A, B, C) y protocolo de jueces
│   ├── item-schema.md     ← esquema de cada ítem y guía de redacción
│   ├── prereg-osf.md      ← preregistro (hipótesis, diseño, plan de análisis) listo para OSF
│   └── publication-plan.md← preregistro OSF, release abierto, preprint arXiv
├── items/
│   ├── schema.json        ← JSON Schema validable de un ítem
│   └── seed.jsonl         ← set semilla congelado: 15 pares ES/EN (30 ítems)
├── paper/
│   └── paper.md           ← borrador del preprint (EN, arXiv cs.CL); [RESULTS] pendientes de la corrida
└── runner/
    ├── prompts/v1.json    ← prompts CONGELADOS (referenciados por el preregistro)
    ├── run.py             ← ejecución multi-proveedor, reanudable, con manifiesto
    ├── score.py           ← métricas de rubrics.md (A/B/C, umbral congelado)
    └── config.example.json
```

## Estado

`v0.3 — listo para preregistrar y correr`. Set semilla **congelado** (15 pares ES/EN, anotación experta DQ), preregistro redactado ([docs/prereg-osf.md](docs/prereg-osf.md)), prompts congelados y runner + scoring probados de punta a punta en modo mock. Sigue: registrar en OSF → construir set completo → corrida de frontera (ver [docs/design.md](docs/design.md) §Roadmap).

## Licencia

Código **MIT**; datos del benchmark (`items/`) **CC BY 4.0**. Ver [LICENSE](LICENSE).

## Cómo citar

Quinde Probst, D. A. (2026). *Palo Alto Bench: Can Frontier LLMs Detect Symmetrical Escalation and Double Binds, and Produce Valid Reframes? A Bilingual (Spanish/English) Benchmark* — Working Paper v0.1 (Design & Preregistered Protocol). Zenodo. https://doi.org/10.5281/zenodo.21223038
