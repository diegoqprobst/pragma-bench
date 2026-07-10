#!/bin/zsh
# Corrida semilla completa: 4 tareas × 4 generadores + juez + scoring.
# Reanudable: re-lanzar salta lo ya guardado en results/raw/.
set -uo pipefail
cd "$(dirname "$0")"
set -a; source .env; set +a
PY=./.venv/bin/python3

echo "=== $(date '+%H:%M:%S') · tareas de generación ==="
for t in a_neutral a_guided b c; do
  echo "--- tarea $t ---"
  $PY run.py --task $t --items ../items/seed.jsonl --config config.json --out ../results/raw
done

echo "=== $(date '+%H:%M:%S') · juez (rep 1 de C, por generador) ==="
for g in anthropic_claude-opus-4.8 openai_gpt-5.5 google_gemini-3.1-pro-preview deepseek_deepseek-v4-pro; do
  echo "--- juez sobre $g ---"
  $PY run.py --task judge --items ../items/seed.jsonl --config config.json \
     --out ../results/raw --responses "../results/raw/$g/c"
done

echo "=== $(date '+%H:%M:%S') · scoring ==="
$PY score.py --items ../items/seed.jsonl --raw ../results/raw --out ../results/scores-seed.json > /dev/null
echo "=== $(date '+%H:%M:%S') · LISTO — resultados en results/scores-seed.json ==="
