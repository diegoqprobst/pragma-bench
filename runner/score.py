#!/usr/bin/env python3
"""Palo Alto Bench — scoring.

Lee las salidas crudas de run.py y calcula las métricas de rubrics.md:
  Tarea A guiada: F1 macro/por clase (voto mayoritario de reps), matriz de confusión,
                  FP-rate sobre `none`, desglose por lengua.
  Tarea A neutra: tasa de SÍ en ítems patológicos (sensibilidad) y en `none` (FP-rate).
  Tarea B: doble vínculo 2/1/0 por componente; escalada Jaccard de turnos.
  Tarea C: media por eje del juez, % válido según umbral CONGELADO
           (>=3 en fit/frame_shift/behavioral_opening, >=2 en irreversibility/assimilability).

Uso:
  python3 score.py --items ../items/seed.jsonl --raw ../results/raw --out ../results/scores.json
"""
import argparse
import json
import pathlib
import re
from collections import Counter, defaultdict

LABELS = ["symmetrical_escalation", "double_bind", "complementary_rigidity", "none"]
AXES = ["fit", "frame_shift", "irreversibility", "assimilability", "behavioral_opening"]
VALID_MIN = {"fit": 3, "frame_shift": 3, "behavioral_opening": 3, "irreversibility": 2, "assimilability": 2}


def load_items(path):
    return {i["id"]: i for i in (json.loads(l) for l in open(path, encoding="utf-8") if l.strip())}


def read_raw(raw_dir, model_slug, task):
    d = pathlib.Path(raw_dir) / model_slug / task
    if not d.exists():
        return []
    return [json.loads(f.read_text(encoding="utf-8")) for f in sorted(d.glob("*.json"))]


def extract_json(text):
    """Primer objeto JSON en la respuesta (tolera texto alrededor y fences)."""
    if text is None:
        return None
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# ---------- Tarea A guiada ----------

def majority_labels(recs):
    """Voto mayoritario multi-etiqueta entre repeticiones: etiqueta presente si aparece en > reps/2."""
    per_rep = []
    for r in recs:
        obj = extract_json(r["response"])
        labs = [l for l in (obj or {}).get("labels", []) if l in LABELS]
        per_rep.append(set(labs) if labs else None)
    valid = [s for s in per_rep if s is not None]
    if not valid:
        return None, len(per_rep)
    counts = Counter(l for s in valid for l in s)
    maj = {l for l, c in counts.items() if c > len(valid) / 2}
    return (maj or None), len(per_rep) - len(valid)


def score_a_guided(items, recs):
    by_item = defaultdict(list)
    for r in recs:
        by_item[r["item_id"]].append(r)
    rows, malformed = {}, 0
    for iid, rr in by_item.items():
        pred, bad = majority_labels(rr)
        malformed += bad
        rows[iid] = pred
    out = {}
    for lang in ("all", "es", "en"):
        sub = {i: p for i, p in rows.items() if lang == "all" or items[i]["lang"] == lang}
        tp = Counter(); fp = Counter(); fn = Counter()
        conf = Counter(); fp_on_none = n_none = 0
        for iid, pred in sub.items():
            gold = set(items[iid]["task_a"]["gold_labels"])
            p = pred or set()
            for l in LABELS:
                tp[l] += (l in gold and l in p)
                fp[l] += (l not in gold and l in p)
                fn[l] += (l in gold and l not in p)
            for g in gold:
                for q in (p or {"<sin_respuesta>"}):
                    conf[(g, q)] += 1
            if gold == {"none"}:
                n_none += 1
                fp_on_none += bool(p - {"none"})
        f1 = {}
        for l in LABELS:
            pr = tp[l] / (tp[l] + fp[l]) if tp[l] + fp[l] else 0.0
            rc = tp[l] / (tp[l] + fn[l]) if tp[l] + fn[l] else 0.0
            f1[l] = round(2 * pr * rc / (pr + rc), 4) if pr + rc else 0.0
        out[lang] = {
            "n_items": len(sub),
            "f1_per_class": f1,
            "f1_macro": round(sum(f1.values()) / len(LABELS), 4),
            "fp_rate_on_none": round(fp_on_none / n_none, 4) if n_none else None,
            "confusion_gold_pred": {f"{g}->{q}": c for (g, q), c in sorted(conf.items())},
        }
    out["malformed_reps"] = malformed
    return out


# ---------- Tarea A neutra ----------

YES_RE = re.compile(r"^\s*(s[ií]|yes)\b", re.IGNORECASE)


def score_a_neutral(items, recs):
    by_item = defaultdict(list)
    for r in recs:
        by_item[r["item_id"]].append(r)
    out = {}
    for lang in ("all", "es", "en"):
        say_yes_path = n_path = say_yes_none = n_none = 0
        for iid, rr in by_item.items():
            if lang != "all" and items[iid]["lang"] != lang:
                continue
            votes = [bool(YES_RE.match(r["response"] or "")) for r in rr]
            yes = sum(votes) > len(votes) / 2
            if set(items[iid]["task_a"]["gold_labels"]) == {"none"}:
                n_none += 1; say_yes_none += yes
            else:
                n_path += 1; say_yes_path += yes
        out[lang] = {
            "sensitivity_pathological": round(say_yes_path / n_path, 4) if n_path else None,
            "fp_rate_on_none": round(say_yes_none / n_none, 4) if n_none else None,
            "n_pathological": n_path, "n_none": n_none,
        }
    return out


# ---------- Tarea B ----------

def score_component(gold_ref, pred):
    """2 = turno exacto; 1 = turno adyacente; 0 = ausente/alucinado."""
    if not isinstance(pred, dict) or "turn" not in pred:
        return 0
    try:
        t = int(pred["turn"])
    except (TypeError, ValueError):
        return 0
    if t == gold_ref["turn"]:
        return 2
    if abs(t - gold_ref["turn"]) == 1:
        return 1
    return 0


def score_b(items, recs):
    by_item = defaultdict(list)
    for r in recs:
        by_item[r["item_id"]].append(r)
    out = {}
    for lang in ("all", "es", "en"):
        db_scores, jaccards = [], []
        for iid, rr in by_item.items():
            it = items[iid]
            if lang != "all" and it["lang"] != lang:
                continue
            obj = extract_json(rr[0]["response"])  # rep 1 (mayoría en análisis final via reps)
            tb = it.get("task_b", {})
            if "double_bind" in it["task_a"]["gold_labels"]:
                comp = tb["double_bind_components"]
                s = {k: score_component(comp[k], (obj or {}).get(k)) for k in comp}
                s["mean"] = round(sum(s.values()) / (2 * len(comp)), 4)  # normalizado 0-1
                s["subtype"] = tb.get("bind_subtype")
                db_scores.append(s)
            elif "symmetrical_escalation" in it["task_a"]["gold_labels"]:
                gold = set(tb.get("escalation_turns", []))
                pred = set()
                for t in (obj or {}).get("escalation_turns", []) or []:
                    try:
                        pred.add(int(t))
                    except (TypeError, ValueError):
                        pass
                jaccards.append(len(gold & pred) / len(gold | pred) if gold | pred else 0.0)
        out[lang] = {
            "double_bind": {
                "n": len(db_scores),
                "mean_normalized": round(sum(s["mean"] for s in db_scores) / len(db_scores), 4) if db_scores else None,
                "by_subtype": {
                    st: round(sum(s["mean"] for s in db_scores if s["subtype"] == st)
                              / max(1, sum(1 for s in db_scores if s["subtype"] == st)), 4)
                    for st in ("logical_type", "pragmatic_paradox")
                } if db_scores else {},
            },
            "escalation": {
                "n": len(jaccards),
                "mean_turn_jaccard": round(sum(jaccards) / len(jaccards), 4) if jaccards else None,
            },
        }
    return out


# ---------- Tarea C (salidas del juez) ----------

def is_valid_reframe(axes):
    return all(axes.get(a, 0) >= m for a, m in VALID_MIN.items())


def score_c(items, judge_recs):
    out = {}
    for lang in ("all", "es", "en"):
        axes_acc = defaultdict(list); valid = n = 0
        for r in judge_recs:
            if lang != "all" and r["lang"] != lang:
                continue
            obj = extract_json(r["response"])
            if not obj or "axes" not in obj:
                continue
            n += 1
            valid += is_valid_reframe(obj["axes"])
            for a in AXES:
                axes_acc[a].append(obj["axes"].get(a, 0))
        out[lang] = {
            "n_judged": n,
            "pct_valid": round(valid / n, 4) if n else None,
            "mean_per_axis": {a: round(sum(v) / len(v), 4) for a, v in axes_acc.items()} if n else {},
        }
    return out


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    items = load_items(args.items)
    raw = pathlib.Path(args.raw)
    report = {}
    judge_recs = []
    for model_dir in sorted(d for d in raw.iterdir() if d.is_dir()):
        slug = model_dir.name
        r = {}
        if (recs := read_raw(raw, slug, "a_guided")):
            r["a_guided"] = score_a_guided(items, recs)
        if (recs := read_raw(raw, slug, "a_neutral")):
            r["a_neutral"] = score_a_neutral(items, recs)
        if (recs := read_raw(raw, slug, "b")):
            r["b"] = score_b(items, recs)
        judge_recs += read_raw(raw, slug, "judge")
        if r:
            report[slug] = r
    # Tarea C: las puntuaciones del juez se atribuyen al GENERADOR del reencuadre
    by_gen = defaultdict(list)
    for rec in judge_recs:
        by_gen[rec.get("generator") or "<sin_generador>"].append(rec)
    for gen, recs in by_gen.items():
        report.setdefault(gen, {})["c"] = score_c(items, recs)
        report[gen]["c"]["judge_model"] = recs[0]["model"]

    pathlib.Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
