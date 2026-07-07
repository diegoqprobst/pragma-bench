#!/usr/bin/env python3
"""Palo Alto Bench — análisis confirmatorio H1–H4 (docs/prereg-osf.md §4 y §7).

Lee las salidas crudas del runner y calcula, por modelo, los cuatro contrastes
preregistrados usando analysis/stats.py. Determinista. No decide nada que el
preregistro no haya fijado.

Uso (tras la corrida confirmatoria):
  python3 confirmatory.py --items ../items/eval.jsonl --raw ../results/raw --out ../results/confirmatory.json

Mapeo hipótesis → test:
  H1  F1(escalada) − F1(doble vínculo) por modelo×lengua; bootstrap por pair_id,
      unilateral (se confirma si el bootstrap deja <2.5% de masa en ≤0).
  H2a Acierto ES vs EN en A-guiada, pareado por pair_id → McNemar exacto.
  H2c Media de rúbrica ES−EN por par (Tarea C) → Wilcoxon por permutación de signos.
  H3  FP guiada vs neutra por ítem `none` → McNemar exacto (+ tasas).
  H4  Detección correcta vs reencuadre válido en ítems C-aplicables → bootstrap
      pareado de la diferencia de proporciones, unilateral.
  Holm entre modelos dentro de cada hipótesis.
"""
import argparse
import json
import pathlib
import sys
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "runner"))
from score import (LABELS, extract_json, majority_labels, read_raw, load_items,  # noqa: E402
                   YES_RE, is_valid_reframe, AXES)
from stats import bootstrap_by_pair, mcnemar_exact, wilcoxon_signrank, holm  # noqa: E402


# ---------- tabla por ítem ----------

def per_item_table(items, raw, slug):
    """Un registro por ítem: predicción A-guiada (voto mayoritario), SÍ neutro,
    puntuación del juez (si el ítem fue juzgado para este generador)."""
    tbl = {}
    by_item = defaultdict(list)
    for r in read_raw(raw, slug, "a_guided"):
        by_item[r["item_id"]].append(r)
    for iid, rr in by_item.items():
        pred, _ = majority_labels(rr)
        tbl.setdefault(iid, {})["a_pred"] = sorted(pred) if pred else None
    by_item = defaultdict(list)
    for r in read_raw(raw, slug, "a_neutral"):
        by_item[r["item_id"]].append(r)
    for iid, rr in by_item.items():
        votes = [bool(YES_RE.match(r["response"] or "")) for r in rr]
        tbl.setdefault(iid, {})["neutral_yes"] = sum(votes) > len(votes) / 2
    # el juez archiva bajo el modelo-juez con generator=slug; barrer todos los dirs
    for mdir in sorted(d for d in pathlib.Path(raw).iterdir() if d.is_dir()):
        for r in read_raw(raw, mdir.name, "judge"):
            if r.get("generator") != slug:
                continue
            obj = extract_json(r["response"])
            if obj and "axes" in obj:
                tbl.setdefault(r["item_id"], {})["judge"] = obj["axes"]
    for iid, row in tbl.items():
        it = items[iid]
        gold = set(it["task_a"]["gold_labels"])
        row["gold"] = sorted(gold)
        row["lang"] = it["lang"]
        row["pair_id"] = it["pair_id"]
        row["is_none"] = gold == {"none"}
        pred = set(row.get("a_pred") or [])
        row["a_correct"] = pred == gold if row.get("a_pred") is not None else False
        row["fp_guided"] = bool(pred - {"none"}) if row["is_none"] else None
        if "judge" in row:
            row["c_valid"] = is_valid_reframe(row["judge"])
            row["c_mean"] = sum(row["judge"].get(a, 0) for a in AXES) / len(AXES)
    return tbl


# ---------- métricas auxiliares ----------

def f1_of_class(rows, label):
    tp = fp = fn = 0
    for r in rows:
        g = label in r["gold"]
        p = label in (r.get("a_pred") or [])
        tp += g and p
        fp += (not g) and p
        fn += g and (not p)
    pr = tp / (tp + fp) if tp + fp else 0.0
    rc = tp / (tp + fn) if tp + fn else 0.0
    return 2 * pr * rc / (pr + rc) if pr + rc else 0.0


# ---------- hipótesis ----------

def h1(tbl, lang, B=10_000):
    rows = [r for r in tbl.values() if r["lang"] == lang and r.get("a_pred") is not None]
    if not rows:
        return None
    diff = lambda rs: f1_of_class(rs, "symmetrical_escalation") - f1_of_class(rs, "double_bind")
    point, lo, hi = bootstrap_by_pair(rows, diff, B=B)
    # p unilateral bootstrap: masa de la distribución en <=0 (predicción: diff>0)
    import random
    rng = random.Random(1956)
    n = len(rows)
    le0 = sum(diff([rows[rng.randrange(n)] for _ in range(n)]) <= 0 for _ in range(2000)) / 2000
    return {"diff_f1_se_minus_db": round(point, 4), "ci95": [round(lo, 4), round(hi, 4)],
            "p_boot_one_sided": round(le0, 4), "n_items": n}


def h2a(tbl):
    by_pair = defaultdict(dict)
    for r in tbl.values():
        if r.get("a_pred") is not None:
            by_pair[r["pair_id"]][r["lang"]] = r["a_correct"]
    b = sum(1 for p in by_pair.values() if p.get("en") and not p.get("es", True))
    c = sum(1 for p in by_pair.values() if p.get("es") and not p.get("en", True))
    return {"en_only_correct": b, "es_only_correct": c,
            "p_mcnemar": round(mcnemar_exact(b, c), 4), "n_pairs": len(by_pair)}


def h2c(tbl):
    by_pair = defaultdict(dict)
    for r in tbl.values():
        if "c_mean" in r:
            by_pair[r["pair_id"]][r["lang"]] = r["c_mean"]
    diffs = [p["es"] - p["en"] for p in by_pair.values() if "es" in p and "en" in p]
    if not diffs:
        return None
    W, p = wilcoxon_signrank(diffs)
    return {"mean_diff_es_minus_en": round(sum(diffs) / len(diffs), 4),
            "W": W, "p_wilcoxon": round(p, 4), "n_pairs": len(diffs)}


def h3(tbl):
    rows = [r for r in tbl.values() if r["is_none"]
            and r.get("fp_guided") is not None and "neutral_yes" in r]
    if not rows:
        return None
    b = sum(1 for r in rows if r["fp_guided"] and not r["neutral_yes"])
    c = sum(1 for r in rows if r["neutral_yes"] and not r["fp_guided"])
    rate_g = sum(r["fp_guided"] for r in rows) / len(rows)
    rate_n = sum(r["neutral_yes"] for r in rows) / len(rows)
    _, lo, hi = bootstrap_by_pair(rows, lambda rs: sum(r["fp_guided"] for r in rs) / len(rs))
    return {"fp_rate_guided": round(rate_g, 4), "fp_rate_neutral": round(rate_n, 4),
            "fp_guided_ci95": [round(lo, 4), round(hi, 4)],
            "p_mcnemar_guided_gt_neutral": round(mcnemar_exact(b, c), 4), "n_none": len(rows)}


def h4(tbl):
    rows = [r for r in tbl.values() if "c_valid" in r and r.get("a_pred") is not None]
    if not rows:
        return None
    detect = sum(r["a_correct"] for r in rows) / len(rows)
    valid = sum(r["c_valid"] for r in rows) / len(rows)
    point, lo, hi = bootstrap_by_pair(
        rows, lambda rs: (sum(r["a_correct"] for r in rs) - sum(r["c_valid"] for r in rs)) / len(rs))
    return {"detect_rate": round(detect, 4), "valid_reframe_rate": round(valid, 4),
            "diff": round(point, 4), "ci95": [round(lo, 4), round(hi, 4)], "n_items": len(rows)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    items = load_items(args.items)
    raw = pathlib.Path(args.raw)
    models = sorted(d.name for d in raw.iterdir() if d.is_dir()
                    if (raw / d.name / "a_guided").exists())
    report = {}
    for slug in models:
        tbl = per_item_table(items, raw, slug)
        report[slug] = {
            "h1": {lang: h1(tbl, lang) for lang in ("es", "en")},
            "h2a": h2a(tbl), "h2c": h2c(tbl), "h3": h3(tbl), "h4": h4(tbl),
        }
    # Holm entre modelos por hipótesis (p primarios)
    for key, getter in [("h2a", lambda m: report[m]["h2a"]["p_mcnemar"]),
                        ("h3", lambda m: (report[m]["h3"] or {}).get("p_mcnemar_guided_gt_neutral"))]:
        ms = [m for m in models if getter(m) is not None]
        if ms:
            adj = holm([getter(m) for m in ms])
            for m, a in zip(ms, adj):
                report[m][key]["p_holm"] = round(a, 4)

    pathlib.Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
