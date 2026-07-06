# Manuscrito

`paper.md` es el borrador del preprint (inglés, destino **arXiv cs.CL**, cross-list cs.HC).

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
