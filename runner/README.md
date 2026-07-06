# Runner

Ejecución y scoring del benchmark. Los prompts viven **congelados y versionados** en `prompts/v1.json` (referenciados por el preregistro; cambiarlos = crear `v2.json` y reportar la desviación).

## Instalación

```bash
pip install -r requirements.txt   # SDKs solo necesarios para los proveedores que uses
export ANTHROPIC_API_KEY=...      # y/o OPENAI_API_KEY, GOOGLE_API_KEY
```

## Flujo

```bash
cd runner
cp config.example.json config.json   # pinnear modelos y juez

# 1. Detección (neutra y guiada), localización y reencuadre
python3 run.py --task a_neutral --items ../items/seed.jsonl --config config.json
python3 run.py --task a_guided  --items ../items/seed.jsonl --config config.json
python3 run.py --task b         --items ../items/seed.jsonl --config config.json
python3 run.py --task c         --items ../items/seed.jsonl --config config.json

# 2. Juez-LLM sobre los reencuadres de cada generador (rep 1)
python3 run.py --task judge --items ../items/seed.jsonl --config config.json \
    --responses ../results/raw/<slug-del-generador>/c

# 3. Métricas
python3 score.py --items ../items/seed.jsonl --raw ../results/raw --out ../results/scores.json
```

Sin claves API, prueba el pipeline completo con `--dry-run` (provider mock determinista).

## Diseño

- **Reanudable:** cada llamada se guarda como un JSON individual en `results/raw/<modelo>/<tarea>/`; re-lanzar salta lo ya hecho.
- **Trazable:** cada registro guarda el SHA-256 del prompt exacto; cada corrida escribe un `run-manifest-*.json` con modelos, temperatura, versión de prompts y timestamp.
- **Reps:** 3 para A/B (voto mayoritario en scoring), 1 para C y judge — según el preregistro ([docs/prereg-osf.md](../docs/prereg-osf.md) §5.4).
- **Aleatorización:** el orden de las etiquetas en A-guiada se baraja de forma determinista por ítem (semilla = hash del id).
- El scoring implementa las métricas de [docs/rubrics.md](../docs/rubrics.md), incluido el umbral congelado de validez del reencuadre. Los tests estadísticos confirmatorios (bootstrap por `pair_id`, McNemar, Wilcoxon, Holm) se añaden en `analysis/` para la corrida confirmatoria.
