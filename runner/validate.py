#!/usr/bin/env python3
"""Palo Alto Bench — validador de ítems.

Chequea un archivo JSONL de ítems contra las reglas de la guía de anotación
(docs/item-schema.md + docs/constructs.md). Úsalo sobre el set semilla y sobre
cada tanda nueva del set de evaluación ANTES de la validación clínica de DQ.

Uso:
  python3 validate.py ../items/seed.jsonl
  python3 validate.py ../items/drafts/tranche-01.jsonl --composition

Sale con código 1 si hay errores (apto para CI).
"""
import argparse
import json
import sys
from collections import Counter

LABELS = {"symmetrical_escalation", "double_bind", "complementary_rigidity", "none"}
SUBTYPES = {"logical_type", "pragmatic_paradox"}
REGISTERS = {"couple", "family", "workplace", "clinical", "friendship", "other"}
DB_COMPONENTS = {"primary_injunction", "secondary_injunction", "no_metacommunication"}
# Términos teóricos que NUNCA pueden aparecer en el estímulo (regla de no-fuga)
BANNED = [
    "doble vínculo", "double bind", "escalada simétrica", "symmetrical escalation",
    "symmetrical", "reencuadre", "reframe", "reframing",
    "rigidez complementaria", "complementary rigidity", "complementary",
    "meta-comunicación", "metacommunication", "inyunción", "injunction",
]


def check_item(r, errors, warn):
    iid = r.get("id", "<sin id>")
    e = lambda msg: errors.append(f"[{iid}] {msg}")
    w = lambda msg: warn.append(f"[{iid}] {msg}")

    for k in ("id", "pair_id", "lang", "register", "dialogue", "task_a", "source"):
        if k not in r:
            e(f"falta campo obligatorio '{k}'")
    if r.get("lang") not in ("es", "en"):
        e(f"lang inválida: {r.get('lang')}")
    if r.get("register") not in REGISTERS:
        e(f"register inválido: {r.get('register')}")

    dialogue = r.get("dialogue", [])
    n = len(dialogue)
    if n < 2:
        e("el diálogo necesita al menos 2 turnos")

    # regla de no-fuga: ni texto ni acotaciones no verbales nombran el constructo
    stim = " ".join(
        (t.get("text", "") + " " + t.get("nonverbal", "")).lower() for t in dialogue
    )
    for term in BANNED:
        if term in stim:
            e(f"FUGA: el estímulo contiene el término teórico '{term}'")

    gold = r.get("task_a", {}).get("gold_labels", [])
    if not gold:
        e("task_a.gold_labels vacío")
    for L in gold:
        if L not in LABELS:
            e(f"etiqueta inválida: {L}")

    tb = r.get("task_b", {})
    if "double_bind" in gold:
        comp = tb.get("double_bind_components", {})
        if set(comp) != DB_COMPONENTS:
            e(f"double_bind requiere exactamente los componentes {sorted(DB_COMPONENTS)}; hay {sorted(comp)}")
        if tb.get("bind_subtype") not in SUBTYPES:
            e(f"bind_subtype inválido o ausente: {tb.get('bind_subtype')}")
        if not r.get("field_inescapability"):
            e("double_bind sin field_inescapability (precondición terciaria)")
        for name, c in comp.items():
            t = c.get("turn")
            if not isinstance(t, int) or not (0 <= t < n):
                e(f"componente {name}: turno fuera de rango ({t})")
            elif c.get("quote", "")[:15].lower() not in dialogue[t].get("text", "").lower():
                e(f"componente {name}: la cita no coincide con el turno {t}")
    else:
        if "field_inescapability" in r:
            e("field_inescapability solo aplica a ítems double_bind")

    if "symmetrical_escalation" in gold:
        turns = tb.get("escalation_turns", [])
        if not turns:
            e("escalada sin escalation_turns")
        for t in turns:
            if not isinstance(t, int) or not (0 <= t < n):
                e(f"escalation_turns: turno fuera de rango ({t})")
        if not tb.get("symmetric_position"):
            w("escalada sin symmetric_position (recomendado)")

    tc = r.get("task_c", {})
    if gold == ["none"]:
        if tc.get("applicable") is not False:
            e("ítem none debe llevar task_c.applicable = false")
        if not r.get("distractor_of"):
            w("ítem none sin distractor_of (¿de qué constructo es casi-acierto?)")
    if tc.get("applicable"):
        rr = tc.get("reference_reframes", [])
        if not rr:
            e("task_c aplicable sin reference_reframes")
        for ex in rr:
            if not isinstance(ex, dict) or set(ex) != {"technique", "text"}:
                e("cada reference_reframe debe ser {technique, text}")
        if not tc.get("presenting_problem"):
            e("task_c aplicable sin presenting_problem")
        if not tc.get("anti_examples"):
            w("task_c sin anti_examples (recomendado)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--composition", action="store_true", help="reporta balance de clases/registros/lenguas")
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.file, encoding="utf-8") if l.strip()]
    errors, warn = [], []
    ids = set()
    pairs = {}
    for r in rows:
        if r.get("id") in ids:
            errors.append(f"id duplicado: {r['id']}")
        ids.add(r.get("id"))
        pairs.setdefault(r.get("pair_id"), []).append(r.get("lang"))
        check_item(r, errors, warn)

    for p, langs in pairs.items():
        if sorted(langs) != ["en", "es"]:
            errors.append(f"par {p} incompleto o duplicado: {langs}")

    print(f"{len(rows)} ítems · {len(pairs)} pares")
    if args.composition:
        cls = Counter(L for r in rows for L in r["task_a"]["gold_labels"])
        reg = Counter(r["register"] for r in rows)
        sub = Counter(r.get("task_b", {}).get("bind_subtype") for r in rows
                      if "double_bind" in r["task_a"]["gold_labels"])
        tot = len(rows)
        print("clases:", {k: f"{v} ({v/tot:.0%})" for k, v in cls.most_common()})
        print("registros:", {k: f"{v} ({v/tot:.0%})" for k, v in reg.most_common()})
        print("subtipos double_bind:", dict(sub))

    for m in warn:
        print("AVISO:", m)
    if errors:
        for m in errors:
            print("ERROR:", m, file=sys.stderr)
        print(f"\n{len(errors)} errores.", file=sys.stderr)
        sys.exit(1)
    print("TODO VALIDA ✓")


if __name__ == "__main__":
    main()
