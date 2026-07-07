# Plan de producción del set de evaluación — tandas

> **Compuerta:** la redacción de estímulos empieza SOLO tras el registro OSF (así lo declara el
> working paper publicado, §4.2). Este documento es **pre-producción**: composición, flujo de
> trabajo y premisas de escenario (una línea por concepto — las premisas no son estímulos).

## Objetivo y composición (preregistrada)

- **≥120 conceptos** (objetivo 150) × 2 lenguas = ≥240 estímulos.
- Clases: ~30% escalada simétrica · ~25% doble vínculo (≈mitad `logical_type` / mitad
  `pragmatic_paradox`) · ~20% rigidez complementaria · ~25% `none` (todos con `distractor_of`).
- Registros: pareja, familia, trabajo, **clínico ≥15%**, amistad.
- El set semilla (se/db/cr/nb-001…) queda FUERA del análisis confirmatorio (calibración del juez).

## Flujo por tanda (12 conceptos = 24 estímulos por tanda; ~10-12 tandas)

1. **Claude redacta** la tanda en `items/drafts/tranche-NN.jsonl` siguiendo la guía congelada
   ([item-schema.md](item-schema.md), [constructs.md](constructs.md)), con ids `xx-1NN`
   (p. ej. `se-101`) para distinguir del semilla.
2. **`python3 runner/validate.py items/drafts/tranche-NN.jsonl --composition`** — validación
   mecánica (no-fuga, pares, componentes, citas por turno, balance).
3. **DQ valida clínicamente** (mismo protocolo que el semilla: etiqueta, reframes, distractores,
   naturalidad EN). Ajustes → re-validar.
4. **Merge** a `items/eval.jsonl` + commit ("tanda NN congelada, validada DQ").
5. Al cerrar la última tanda: **congelar `items/eval.jsonl`** (hash + fecha en el run-manifest)
   → recién entonces se corre ningún modelo.

Reglas de redacción transversales (recordatorio): balancear qué hablante abre; variar técnica de
los reframes de referencia; cada `none` falla EXACTAMENTE un criterio de su `distractor_of`;
pares ES/EN nativos, misma estructura de turnos.

## Matriz de premisas — tandas 1–3 (36 conceptos)

> Premisas = situación en una línea. El diálogo, la anotación y los reframes se redactan tras OSF.
> Balance acumulado t1–t3: 11 se (31%) · 9 db (25%; 4 logical + 5 pragmatic) · 7 cr (19%) · 9 nb (25%).
> Registro clínico: 9/36 (25% — compensa el 0% del semilla).

### Tanda 1

| id | clase | registro | premisa |
|---|---|---|---|
| se-101 | escalada | couple | quién sacrificó más su carrera por la relación; cuenta de renuncias que sube |
| se-102 | escalada | workplace | dos socios fundadores disputan quién arriesgó más al inicio |
| se-103 | escalada | clinical | pareja en sesión compite delante del terapeuta por quién sufre más |
| se-104 | escalada | friendship | quién conoce "de verdad" al amigo común que está en duelo |
| db-101 | bind `logical_type` | clinical | terapeuta: "confía en mí, pero tiene que nacerte" + castiga la duda + no se discute con el terapeuta |
| db-102 | bind `pragmatic_paradox` | couple | "quiero que seas independiente" + castiga cada decisión independiente + prohibido nombrarlo |
| db-103 | bind `pragmatic_paradox` | family | "queremos que madures" + castigan cada acto adulto + "no seas malagradecido" |
| cr-101 | rigidez | clinical | paciente delega toda decisión al terapeuta directivo; roles fijos que se confirman |
| cr-102 | rigidez | couple | uno organiza la vida entera del otro "desordenado"; el desorden justifica más control |
| nb-101 | none (↔escalada) | clinical | desacuerdo en sesión con reparación inmediata |
| nb-102 | none (↔bind) | family | doble encargo contradictorio que se comenta y el padre ajusta |
| nb-103 | none (↔rigidez) | workplace | ayuda puntual de un senior; el junior retoma la autonomía |

### Tanda 2

| id | clase | registro | premisa |
|---|---|---|---|
| se-105 | escalada | couple | celos especulares: cada revisión del teléfono justifica la siguiente |
| se-106 | escalada | family | herencia: hermanos suben ofertas de "quién merece la casa" |
| se-107 | escalada | workplace | disputa por el crédito de una idea en una reunión |
| se-108 | escalada | family | suegra y nuera compiten por quién cuida mejor al bebé |
| db-104 | bind `logical_type` | couple | "quiero que desees sorprenderme; si lo planeas porque lo pedí, no vale" + cierre |
| db-105 | bind `logical_type` | family | "ríete de verdad con nosotros" + se castiga la risa 'forzada' + "no arruines la cena" |
| db-106 | bind `pragmatic_paradox` | workplace | "sé honesto en la retroalimentación" + represalia sutil + "no te pongas sensible" |
| cr-103 | rigidez | workplace | mentor que resuelve todo / junior que consulta todo; dependencia estable |
| cr-104 | rigidez | family | cuidador sobrefuncionante / pareja mayor "frágil" que delega hasta lo que puede |
| nb-104 | none (↔rigidez) | couple | reparto de tareas negociado; roles que rotan |
| nb-105 | none (↔bind) | clinical | paciente discrepa de la tarea; el terapeuta explora y ajusta (meta-comunicación abierta) |
| nb-106 | none (↔escalada) | friendship | broma que ofende, se aclara y se repara en tres turnos |

### Tanda 3

| id | clase | registro | premisa |
|---|---|---|---|
| se-109 | escalada | clinical | familia en sesión: subasta de culpas sobre quién causó el problema del hijo |
| se-110 | escalada | workplace | dos jefas de área escalan CCs y reuniones para marcar territorio |
| se-111 | escalada | friendship | quién pone más en el emprendimiento compartido; horas contra dinero |
| db-107 | bind `logical_type` | workplace | "innova porque te apasione, no por el bono" + se descarta lo que no pidió dirección + no se cuestiona |
| db-108 | bind `pragmatic_paradox` | clinical | en sesión familiar: "dile lo que sientes" + invalidación al decirlo + "no discutas a tu madre aquí" |
| db-109 | bind `pragmatic_paradox` | couple | "gasta tu dinero en lo que quieras" + reproche por cada gasto + "no me hagas quedar de controlador" |
| cr-105 | rigidez | clinical | supervisor clínico que corrige todo / supervisando que ya no propone caso propio |
| cr-106 | rigidez | friendship | el rescatador y el amigo "en crisis perpetua"; cada rescate confirma los roles |
| nb-107 | none (↔escalada) | family | discusión por el toque de queda que termina en acuerdo con condiciones |
| nb-108 | none (↔bind) | workplace | doble prioridad contradictoria; el empleado la señala y se re-prioriza |
| nb-109 | none (↔rigidez) | clinical | terapeuta da psicoeducación puntual; el paciente decide solo el siguiente paso |
| se-112 | escalada | couple | quién pide perdón primero; disculpas condicionadas que suben la apuesta |

### Tandas 4–10 (a poblar)

Mismo patrón; huecos a vigilar en el acumulado: `friendship` (subrepresentado), variedad de
temas (dinero, salud, tecnología/redes, migración — contexto ecuatoriano/latino natural en ES),
y mantener ≈mitad/mitad los subtipos de bind.

## Cadencia estimada

- 1 tanda ≈ 1 sesión de redacción + 1 revisión tuya (como el semilla: por chat, marcando ítems por id).
- 10 tandas → set completo en ~2-3 semanas a ritmo de 3-4 tandas/semana, sin bloquear tus otras cosas.
- La corrida (semilla → calibración → confirmatoria) es 1-2 días una vez congelado el set y con claves API.
