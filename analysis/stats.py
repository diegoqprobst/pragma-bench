#!/usr/bin/env python3
"""Palo Alto Bench — tests estadísticos preregistrados (docs/prereg-osf.md §7).

Solo biblioteca estándar. Todo determinista (semillas fijas) para reproducibilidad.

Implementa:
  bootstrap_by_pair  — IC 95% bootstrap no paramétrico (B=10.000) remuestreando por pair_id.
  mcnemar_exact      — test de McNemar exacto (binomial sobre pares discordantes). H2/H3.
  wilcoxon_signrank  — Wilcoxon de rangos con signo, p por permutación de signos
                       (N=10.000, semilla fija). H2 en Tarea C.
  holm               — corrección de Holm sobre una lista de p-valores.

Ver docstrings para el mapeo hipótesis→test.
"""
import math
import random
import statistics


def bootstrap_by_pair(pairs, metric_fn, B=10_000, alpha=0.05, seed=1956):
    """IC bootstrap remuestreando POR PAR (respeta el emparejamiento ES/EN).

    pairs: lista de unidades (una por pair_id); cada unidad lleva sus datos.
    metric_fn: callable(lista_de_unidades) -> float (p. ej. macro-F1 del subconjunto).
    Devuelve (estimación_puntual, ci_low, ci_high).
    Semilla por defecto 1956 (Bateson et al.).
    """
    rng = random.Random(seed)
    point = metric_fn(pairs)
    n = len(pairs)
    stats_ = []
    for _ in range(B):
        sample = [pairs[rng.randrange(n)] for _ in range(n)]
        stats_.append(metric_fn(sample))
    stats_.sort()
    lo = stats_[int((alpha / 2) * B)]
    hi = stats_[min(B - 1, int((1 - alpha / 2) * B))]
    return point, lo, hi


def mcnemar_exact(b, c):
    """McNemar exacto: b = discordantes (éxito solo en condición 1),
    c = discordantes (éxito solo en condición 2). Binomial(n=b+c, p=0.5), bilateral.

    H2 (Tarea A): éxito/fallo ES vs EN por pair_id.
    H3: FP en guiada vs neutra por ítem none.
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def wilcoxon_signrank(diffs, n_perm=10_000, seed=1967):
    """Wilcoxon de rangos con signo; p bilateral por permutación de signos.

    diffs: lista de diferencias pareadas (p. ej. puntuación de rúbrica ES−EN por ítem).
    Los ceros se descartan (convención estándar). Empates → rangos promedio.
    Determinista (semilla fija, 1967 = Pragmatics of Human Communication).
    Devuelve (W, p).
    """
    d = [x for x in diffs if x != 0]
    if not d:
        return 0.0, 1.0
    ranked = sorted(range(len(d)), key=lambda i: abs(d[i]))
    # rangos promedio para empates en |d|
    ranks = [0.0] * len(d)
    i = 0
    while i < len(ranked):
        j = i
        while j + 1 < len(ranked) and abs(d[ranked[j + 1]]) == abs(d[ranked[i]]):
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[ranked[k]] = avg
        i = j + 1
    w_pos = sum(r for r, x in zip(ranks, d) if x > 0)
    w_neg = sum(r for r, x in zip(ranks, d) if x < 0)
    W = min(w_pos, w_neg)
    # permutación de signos sobre los mismos rangos
    rng = random.Random(seed)
    total = 0
    for _ in range(n_perm):
        wp = sum(r for r in ranks if rng.random() < 0.5)
        wn = sum(ranks) - wp
        if min(wp, wn) <= W:
            total += 1
    return W, total / n_perm


def holm(pvalues):
    """Corrección de Holm. Devuelve p ajustados en el orden de entrada."""
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adj = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvalues[idx])
        adj[idx] = min(1.0, running)
    return adj


# ── autotest mínimo ──
if __name__ == "__main__":
    # McNemar: 15 vs 5 discordantes → p ≈ 0.0414 (binomial exacto)
    p = mcnemar_exact(15, 5)
    assert 0.035 < p < 0.05, p
    # Wilcoxon: diferencias claramente positivas → p pequeño
    _, p2 = wilcoxon_signrank([1, 2, 1, 3, 2, 1, 2, 2, 1, 3, 2, 1])
    assert p2 < 0.01, p2
    # Wilcoxon nulo: simétrico alrededor de 0 → p grande
    _, p3 = wilcoxon_signrank([1, -1, 2, -2, 1, -1, 2, -2])
    assert p3 > 0.5, p3
    # Holm: monótono y acotado
    adj = holm([0.01, 0.04, 0.03])
    assert adj[0] <= adj[2] <= adj[1] and all(a <= 1 for a in adj), adj
    # Bootstrap: media de constantes → IC degenerado en el punto
    pt, lo, hi = bootstrap_by_pair([1.0] * 20, statistics.mean, B=200)
    assert pt == lo == hi == 1.0
    print("stats.py: autotests OK ✓")
