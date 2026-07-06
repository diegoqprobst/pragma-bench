# Esquema de ítem y guía de redacción

El esquema validable está en [`../items/schema.json`](../items/schema.json) (JSON Schema draft-07). Aquí va la guía para **autorar ítems nuevos** de forma consistente. Cada línea de [`../items/seed.jsonl`](../items/seed.jsonl) es un ítem.

## Campos

| Campo | Obligatorio | Nota |
|---|---|---|
| `id` | sí | `se-001-es` (constructo-NNN-lengua). Prefijos: `se`=escalada, `db`=doble vínculo, `cr`=rigidez complementaria, `nb`=ninguno. |
| `pair_id` | sí | Liga ES↔EN del mismo concepto (`se-001`). |
| `lang` | sí | `es` o `en`. |
| `register` | sí | `couple`, `family`, `workplace`, `clinical`, `friendship`, `other`. |
| `dialogue` | sí | Lista de turnos `{speaker, text, nonverbal?}`. Índices 0-based. |
| `task_a.gold_labels` | sí | Subconjunto de `{symmetrical_escalation, double_bind, complementary_rigidity, none}`. |
| `task_a.rationale` | recom. | Justificación en términos de [constructs.md](constructs.md). |
| `task_b` | según constructo | `double_bind_components` (`primary_injunction`, `secondary_injunction`, `no_metacommunication`, cada uno `{turn, quote}`; y `bind_subtype`) o `escalation_turns` + `symmetric_position`. |
| `field_inescapability` | doble vínculo | Por qué la persona no puede escapar del campo (inyunción terciaria de Bateson); precondición estructural, no un turno. |
| `bind_subtype` | doble vínculo | `logical_type` (paradoja de niveles lógicos) o `pragmatic_paradox` (contradicción + no salida + no meta-comunicación sin cruce limpio de tipos). |
| `task_c` | si aplica | `applicable`, `presenting_problem`, `reference_reframes[]` (cada uno `{technique, text}`), `anti_examples[]`. |
| `distractor_of` | si aplica | Constructo con el que el ítem `none` se confunde a propósito. |
| `source`, `annotator`, `notes` | recom. | Trazabilidad. |

## Reglas de redacción (no negociables)

1. **Nunca nombrar el constructo** en `dialogue` (ni "doble vínculo", ni "escalada", ni "reencuadre", en ninguna lengua). El validador lo verifica.
2. **El doble vínculo necesita el choque entre niveles**: usa `nonverbal` para el nivel meta que contradice al contenido (tono, gesto, rigidez). Anota los 3 componentes (`primary_injunction`, `secondary_injunction`, `no_metacommunication`) como turnos, y la inescapabilidad del campo en `field_inescapability` (no la fuerces al diálogo). Marca `bind_subtype`.
3. **Pares ES/EN = mismo fenómeno, redacción nativa.** No traduzcas literal: nombres, modismos y registro propios de cada lengua. Misma estructura de turnos para que la anotación de Tarea B se alinee.
4. **Distractores que muerden.** Un ítem `none` con `distractor_of` debe *parecerse* al constructo y fallar en un criterio concreto (p. ej. doble vínculo sin cláusula de no-salida → la persona puede comentar/salir).
5. **Balance de inicio.** Alterna qué hablante abre y qué rol escala, para no dejar atajos posicionales.

## Validación

```bash
# desde pragma-bench/
python3 -c "import json;[json.loads(l) for l in open('items/seed.jsonl') if l.strip()]"  # JSONL bien formado
# (con jsonschema instalado) validar cada ítem contra items/schema.json
```

El script de validación de la sesión también chequea: ids únicos, pares ES/EN completos, ausencia de términos teóricos en viñetas, y turnos referenciados dentro de rango.
