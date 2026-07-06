# Manuscrito

Dos artefactos, dos destinos:

- **`paper.md`** — borrador maestro del preprint (inglés, destino **arXiv cs.CL**, cross-list cs.HC). Contiene los placeholders `[RESULTS]`/`[VERIFY-CITE]`.
- **`preprint.html` → `palo-alto-bench-v0.1.pdf`** — versión **working paper v0.1 (pre-resultados)** con la identidad **quinde research** (Manrope, navy `#2a4b66` + verde corpus `#0f6e56`, wordmark `quinde.`), lista para **Zenodo**. Presenta el diseño + protocolo preregistrado sin placeholders; Zenodo versiona el DOI cuando llegue v1 con resultados. Hereda el sistema visual de `handoff/quinde-es` (plantilla `quinde - preprint.html` + `styles/quinde.css`).

## Regenerar el PDF

```bash
# Chromium headless de Playwright (ya instalado); Google Fonts requiere red
"$HOME/Library/Caches/ms-playwright/chromium_headless_shell-1228/chrome-headless-shell-mac-arm64/chrome-headless-shell" \
  --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=15000 \
  --print-to-pdf="palo-alto-bench-v0.1.pdf" "file://$PWD/preprint.html"
```

## Subir a Zenodo (acción de Diego)

1. zenodo.org → New upload → arrastrar `palo-alto-bench-v0.1.pdf`.
2. Los metadatos están preparados en [`../.zenodo.json`](../.zenodo.json) (título, ORCID, CC BY 4.0, keywords, versión 0.1) — copiar de ahí. Ese archivo también activa la integración automática GitHub→Zenodo si luego conectas el repo.
3. Marcar "Reserve DOI" antes de publicar si quieres poner el DOI dentro del PDF (regenerar con el DOI y volver a subir).
4. Al publicar: anotar el DOI en `docs/prereg-osf.md`, `CITATION.cff` y el README raíz.

## Estado

- **Completas:** Abstract (con placeholders), §1–6 (introducción, teoría, related-work-mapa, benchmark, setup, hipótesis), §8.2, §9–11 (limitaciones, ética, disponibilidad), referencias fuente verificadas.
- **`[RESULTS]`:** se llenan tras la corrida confirmatoria preregistrada (tablas 1–3 ya estructuradas en §7; ramas de interpretación pre-escritas en §8.1).
- **`[VERIFY-CITE]`:** ninguna cita entra sin verificar (misma política que citas-verificadas en yo-distribuido). Pendientes: anclas de mental-health NLP, pragmatics/ToM eval, sycophancy (Sharma et al.), LLM-as-judge (Zheng et al.). Un deep-research de una sesión las resuelve.
- **`[DOI]` / `[N]`:** se fijan al registrar en OSF y al pinnear modelos.

## Pipeline a arXiv

Markdown → LaTeX con pandoc cuando el contenido esté cerrado:

```bash
pandoc paper.md -o paper.tex --standalone
# ajustar preámbulo (documentclass article, natbib) y compilar
```

arXiv cs.CL no exige plantilla; una `article` limpia a una columna basta para preprint.
