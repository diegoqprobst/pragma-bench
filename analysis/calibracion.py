#!/usr/bin/env python3
"""Calibración del juez-LLM contra DQ (protocolo preregistrado §5.5).

build : arma el paquete de puntuación A CIEGAS para DQ a partir de results/raw/*/c
        → results/calibracion/paquete-DQ.md   (lectura: diálogo + problema + reencuadre)
        → results/calibracion/paquete-DQ.csv  (para llenar: 5 ejes 1-4 + banderas)
        → results/raw/CLAVE-calibracion.json  (código→modelo; NO ABRIR hasta terminar)
        Orden aleatorio determinista (semilla 42), sin identidad de modelo.

kappa : cruza el CSV llenado por DQ con las puntuaciones del juez-LLM
        → κ ponderado cuadrático por eje + veredicto del criterio preregistrado
          (κ ≥ 0.60 en ≥ 4 de 5 ejes).

Uso:
  python3 analysis/calibracion.py build
  python3 analysis/calibracion.py kappa results/calibracion/paquete-DQ.csv
"""
import csv
import json
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AXES = ["fit", "frame_shift", "irreversibility", "assimilability", "behavioral_opening"]
AXES_ES = {
    "fit": "Ajuste a los hechos", "frame_shift": "Cambio de marco",
    "irreversibility": "Irreversibilidad", "assimilability": "Asimilabilidad",
    "behavioral_opening": "Apertura de conducta",
}


def load_items():
    return {json.loads(l)["id"]: json.loads(l)
            for l in open(ROOT / "items/seed.jsonl", encoding="utf-8") if l.strip()}


def fmt_dialogue(item):
    out = []
    for t in item["dialogue"]:
        nv = f" ({t['nonverbal']})" if t.get("nonverbal") else ""
        out.append(f"> **{t['speaker']}:**{nv} {t['text']}")
    return "\n".join(out)


def build():
    items = load_items()
    raw = ROOT / "results/raw"
    entries = []
    for mdir in sorted(d for d in raw.iterdir() if d.is_dir()):
        cdir = mdir / "c"
        if not cdir.exists():
            continue
        for f in sorted(cdir.glob("*_rep1.json")):
            r = json.loads(f.read_text(encoding="utf-8"))
            if r.get("response"):
                entries.append({"model": mdir.name, "item_id": r["item_id"],
                                "lang": r["lang"], "reframe": r["response"].strip()})
    random.Random(42).shuffle(entries)

    calib = ROOT / "results/calibracion"
    calib.mkdir(parents=True, exist_ok=True)
    key = {}
    md = ["# Paquete de calibración — puntuación a ciegas (DQ)\n",
          "Puntúa cada reencuadre con la rúbrica de docs/rubrics.md: 5 ejes, escala 1-4",
          "(1=ausente/contraproducente · 2=débil · 3=adecuado · 4=fuerte).",
          "Banderas de descalificación (fuerzan el eje afectado a 1): positividad genérica,",
          "negación/minimización, consejo directo, interpretación causal-histórica, culpar a la víctima.",
          "**No mires la clave ni las puntuaciones del juez hasta terminar.** Llena el CSV hermano.\n"]
    rows = []
    for i, e in enumerate(entries, 1):
        code = f"R-{i:03d}"
        key[code] = {"model": e["model"], "item_id": e["item_id"]}
        it = items[e["item_id"]]
        md.append(f"\n---\n\n## {code}  ·  [{e['lang']}]\n")
        md.append(fmt_dialogue(it))
        md.append(f"\n**Problema presentado:** {it['task_c']['presenting_problem']}\n")
        md.append(f"**REENCUADRE A PUNTUAR:**\n\n{e['reframe']}\n")
        rows.append({"codigo": code, "lang": e["lang"],
                     **{a: "" for a in AXES}, "banderas": "", "notas": ""})

    (calib / "paquete-DQ.md").write_text("\n".join(md), encoding="utf-8")
    with open(calib / "paquete-DQ.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["codigo", "lang", *AXES, "banderas", "notas"])
        w.writeheader()
        w.writerows(rows)
    (raw / "CLAVE-calibracion.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"paquete listo: {len(entries)} reencuadres → results/calibracion/ (clave en results/raw/, no abrir)")


def qwk(a, b, k=4):
    """κ ponderado cuadrático para escalas 1..k."""
    n = len(a)
    O = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        O[x - 1][y - 1] += 1
    ra = [sum(row) for row in O]
    rb = [sum(O[i][j] for i in range(k)) for j in range(k)]
    W = [[(i - j) ** 2 / (k - 1) ** 2 for j in range(k)] for i in range(k)]
    num = sum(W[i][j] * O[i][j] for i in range(k) for j in range(k))
    den = sum(W[i][j] * ra[i] * rb[j] / n for i in range(k) for j in range(k))
    return 1 - num / den if den else 1.0


def kappa(csv_path):
    key = json.loads((ROOT / "results/raw/CLAVE-calibracion.json").read_text(encoding="utf-8"))
    dq = {r["codigo"]: r for r in csv.DictReader(open(csv_path, encoding="utf-8"))}
    ok = 0
    print(f"{'eje':22s} {'n':>4s} {'κ_w':>6s}")
    for ax in AXES:
        pairs = []
        for code, meta in key.items():
            row = dq.get(code)
            if not row or not row.get(ax, "").strip():
                continue
            jf = ROOT / f"results/raw/anthropic_claude-fable-5/judge/{meta['item_id']}_rep1_{meta['model']}.json"
            if not jf.exists():
                continue
            m = re.search(r"\{.*\}", json.loads(jf.read_text())["response"] or "", re.DOTALL)
            if not m:
                continue
            jscore = json.loads(m.group(0)).get("axes", {}).get(ax)
            if jscore in (1, 2, 3, 4) and row[ax].strip() in ("1", "2", "3", "4"):
                pairs.append((int(row[ax]), jscore))
        k = qwk([p[0] for p in pairs], [p[1] for p in pairs]) if len(pairs) >= 10 else float("nan")
        flag = "✓" if k >= 0.60 else "✗"
        ok += k >= 0.60
        print(f"{AXES_ES[ax]:22s} {len(pairs):>4d} {k:>6.3f} {flag}")
    print(f"\ncriterio preregistrado (κ≥0.60 en ≥4/5 ejes): {'CUMPLE — el juez escala al set completo' if ok >= 4 else 'NO CUMPLE — iterar prompt del juez (1 vez) o DQ puntúa todo'}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
    elif len(sys.argv) > 2 and sys.argv[1] == "kappa":
        kappa(sys.argv[2])
    else:
        print(__doc__)
