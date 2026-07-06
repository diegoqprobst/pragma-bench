#!/usr/bin/env python3
"""Palo Alto Bench — runner.

Ejecuta una tarea (a_neutral, a_guided, b, c, judge) sobre un archivo de ítems
para los modelos declarados en un config JSON, y guarda salidas crudas en
results/raw/. No calcula métricas (eso es score.py).

Uso:
  python3 run.py --task a_guided --items ../items/seed.jsonl --config config.json
  python3 run.py --task judge --items ../items/seed.jsonl --config config.json \
      --responses ../results/raw/<modelo-generador>/c
  python3 run.py --task a_guided --items ../items/seed.jsonl --config config.example.json --dry-run

Claves API: variables de entorno ANTHROPIC_API_KEY / OPENAI_API_KEY / GOOGLE_API_KEY.
"""
import argparse
import hashlib
import json
import pathlib
import random
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LABELS = ["symmetrical_escalation", "double_bind", "complementary_rigidity", "none"]
TASKS = ["a_neutral", "a_guided", "b", "c", "judge"]


# ---------- carga de materiales ----------

def load_items(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def load_prompts(version):
    return json.load(open(ROOT / "runner" / "prompts" / f"{version}.json", encoding="utf-8"))


def format_dialogue(item):
    """Turnos numerados desde 0; acotaciones no verbales entre paréntesis."""
    lines = []
    for i, t in enumerate(item["dialogue"]):
        nv = f" ({t['nonverbal']})" if t.get("nonverbal") else ""
        lines.append(f"[{i}] {t['speaker']}:{nv} {t['text']}")
    return "\n".join(lines)


def shuffled_glosses(prompts, item):
    """Orden de etiquetas aleatorizado de forma determinista por id de ítem."""
    glosses = prompts["label_glosses"][item["lang"]]
    order = LABELS[:]
    seed = int(hashlib.sha256(item["id"].encode()).hexdigest(), 16)
    random.Random(seed).shuffle(order)
    return "\n".join(f"- {glosses[k]}" for k in order)


def build_prompt(task, item, prompts, candidate=None):
    lang = item["lang"]
    dlg = format_dialogue(item)
    if task == "a_neutral":
        return prompts["task_a_neutral"][lang].replace("{dialogue}", dlg)
    if task == "a_guided":
        return (prompts["task_a_guided"][lang]
                .replace("{dialogue}", dlg)
                .replace("{labels}", shuffled_glosses(prompts, item)))
    if task == "b":
        gold = item["task_a"]["gold_labels"]
        if "double_bind" in gold:
            key = "task_b_double_bind"
        elif "symmetrical_escalation" in gold:
            key = "task_b_escalation"
        else:
            return None  # B solo aplica a doble vínculo y escalada
        return prompts[key][lang].replace("{dialogue}", dlg)
    if task == "c":
        if not item.get("task_c", {}).get("applicable"):
            return None
        return prompts["task_c"][lang].replace("{dialogue}", dlg)
    if task == "judge":
        tc = item["task_c"]
        refs = "\n".join(f"- ({r['technique']}) {r['text']}" for r in tc["reference_reframes"])
        antis = "\n".join(f"- {a}" for a in tc.get("anti_examples", []))
        return (prompts["judge_c"][lang]
                .replace("{dialogue}", dlg)
                .replace("{presenting_problem}", tc["presenting_problem"])
                .replace("{candidate_reframe}", candidate)
                .replace("{reference_reframes}", refs)
                .replace("{anti_examples}", antis))
    raise ValueError(task)


# ---------- proveedores ----------

def call_model(model_cfg, prompt, temperature, max_tokens=1024):
    provider = model_cfg["provider"]
    model = model_cfg["model"]
    if provider == "mock":
        return mock_response(prompt)
    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=model, max_tokens=max_tokens, temperature=temperature,
            messages=[{"role": "user", "content": prompt}])
        return msg.content[0].text
    if provider == "openai":
        import openai
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=model, max_tokens=max_tokens, temperature=temperature,
            messages=[{"role": "user", "content": prompt}])
        return resp.choices[0].message.content
    if provider == "google":
        from google import genai
        client = genai.Client()
        resp = client.models.generate_content(
            model=model, contents=prompt,
            config={"temperature": temperature, "max_output_tokens": max_tokens})
        return resp.text
    raise ValueError(f"proveedor desconocido: {provider}")


def mock_response(prompt):
    """Salidas deterministas para probar el pipeline sin API (--dry-run usa provider mock)."""
    if '"labels"' in prompt:
        return json.dumps({"labels": ["none"], "justification": "mock"})
    if '"primary_injunction"' in prompt:
        return json.dumps({"primary_injunction": {"turn": 0, "quote": "mock"},
                           "secondary_injunction": {"turn": 2, "quote": "mock"},
                           "no_metacommunication": {"turn": 4, "quote": "mock"}})
    if '"escalation_turns"' in prompt:
        return json.dumps({"escalation_turns": [0, 1, 2], "symmetric_position": "mock"})
    if '"axes"' in prompt:
        return json.dumps({"axes": {"fit": 3, "frame_shift": 3, "irreversibility": 2,
                                    "assimilability": 3, "behavioral_opening": 3},
                           "flags": [], "reasoning": {k: "mock" for k in
                           ["fit", "frame_shift", "irreversibility", "assimilability", "behavioral_opening"]}})
    if prompt.startswith(("Lee el siguiente diálogo.", "Read the following dialogue.")) and "SÍ" in prompt or "YES" in prompt:
        return "NO\nMock: no observo un patrón problemático."
    return "Mock: quizá lo que comparten es más grande que lo que disputan."


def call_with_retries(model_cfg, prompt, temperature, retries=3):
    last = None
    for attempt in range(retries):
        try:
            return call_model(model_cfg, prompt, temperature), None
        except Exception as e:  # error de API: reintentar con backoff
            last = str(e)
            time.sleep(2 ** attempt)
    return None, last


# ---------- ejecución ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=TASKS)
    ap.add_argument("--items", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--prompts-version", default="v1")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--out", default=str(ROOT / "results" / "raw"))
    ap.add_argument("--responses", help="(solo judge) dir con salidas de la tarea C a juzgar")
    ap.add_argument("--dry-run", action="store_true", help="fuerza provider mock en todos los modelos")
    args = ap.parse_args()

    items = load_items(args.items)
    prompts = load_prompts(args.prompts_version)
    cfg = json.load(open(args.config, encoding="utf-8"))
    models = cfg["models"] if args.task != "judge" else [cfg["judge_model"]]
    temperature = cfg.get("temperature", 0.0)
    if args.dry_run:
        models = [dict(m, provider="mock") for m in models]

    out_root = pathlib.Path(args.out)
    manifest = {"task": args.task, "items_file": args.items, "n_items": len(items),
                "prompts_version": prompts["version"], "temperature": temperature,
                "reps": args.reps, "models": models, "started_unix": int(time.time())}

    for m in models:
        slug = m["model"].replace("/", "_").replace(":", "_")
        outdir = out_root / slug / args.task
        outdir.mkdir(parents=True, exist_ok=True)
        reps = args.reps if args.task in ("a_neutral", "a_guided", "b") else 1
        done = skipped = failed = 0
        gen_slug = pathlib.Path(args.responses).parent.name if args.responses else None
        for item in items:
            candidates = [None]
            if args.task == "judge":
                # juzga la repetición 1 de la tarea C del generador indicado en --responses
                candidates = []
                for f in sorted(pathlib.Path(args.responses).glob(f"{item['id']}_rep1*.json")):
                    candidates.append((gen_slug, json.loads(f.read_text(encoding="utf-8"))["response"]))
                if not candidates:
                    skipped += 1
                    continue
            for cand in candidates:
                cand_tag, cand_text = (cand if isinstance(cand, tuple) else ("", None))
                prompt = build_prompt(args.task, item, prompts, candidate=cand_text)
                if prompt is None:
                    skipped += 1
                    break
                for rep in range(1, reps + 1):
                    tag = f"_{cand_tag}" if cand_tag else ""
                    fp = outdir / f"{item['id']}_rep{rep}{tag}.json"
                    if fp.exists():
                        continue  # reanudable
                    resp, err = call_with_retries(m, prompt, temperature)
                    rec = {"item_id": item["id"], "pair_id": item["pair_id"], "lang": item["lang"],
                           "task": args.task, "model": m["model"], "rep": rep,
                           "generator": cand_tag or None,
                           "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                           "response": resp, "api_error": err, "unix": int(time.time())}
                    fp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
                    done += 1
                    failed += err is not None
        print(f"[{m['model']}] {args.task}: {done} llamadas, {skipped} ítems no aplicables/saltados, {failed} errores de API")

    (out_root / f"run-manifest-{args.task}-{manifest['started_unix']}.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
