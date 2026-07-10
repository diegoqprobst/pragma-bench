# Estado al pausar (2026-07-11) y cómo reanudar

**Corrida semilla:** generación 100% completa (A-neutra, A-guiada, B y C en los 4 modelos;
resultados locales en `results/raw/`, gitignorados). **Falta solo: juez + scoring.**
Gastado ~$6.4 de $16; el juez costará ~$2-3 más.

## Reanudar (un comando, es reanudable — salta lo ya hecho)

```bash
cd pragma-bench/runner && ./corrida-semilla.sh
```

(Re-corre en segundos las tareas ya completas —no re-llama a la API— y ejecuta juez + scoring.
Requiere `runner/.env` con OPENROUTER_API_KEY, que ya está.)

## Después del scoring

1. Leer `results/scores-seed.json` (resultados semilla por modelo/tarea/lengua).
2. Armar el paquete de calibración para DQ: 96 reencuadres anonimizados en orden aleatorio
   + rúbrica → DQ puntúa a ciegas → κ vs juez-LLM (criterio prereg: ≥0.60 en ≥4/5 ejes).

## Pendiente de DQ (sin computadora, cuando tenga tiempo)

- **Validación clínica del set de evaluación**: 10 tandas en `items/drafts/tranche-01..10.jsonl`
  (120 pares, ya validados mecánicamente). Sugerencia: muestreo dirigido — pedir a Claude
  "preséntame los 20 ítems más delicados" (gemelos, clínicos-incómodos, subtipos).
- Tras aprobar: merge a `items/eval.jsonl` + congelar con hash → confirmatoria.
