"""Higiene de dados sintéticos (Camada 3): normalização, quase duplicatas e grupos.

Sem dependências: Jaccard em trigramas de caracteres para duplicatas lexicais e
união-busca para agrupar itens parecidos (por qualquer similaridade, inclusive cosseno
de embeddings), de modo que variações do mesmo pedido fiquem no mesmo conjunto
(treino, validação ou teste) e não vazem entre eles (parte 6.4b do guia).
"""
from __future__ import annotations

import math
import re
import unicodedata
from typing import Callable, Dict, FrozenSet, List, Sequence, Tuple


def normalizar(texto: str) -> str:
    """Minúsculas, sem acentos nem pontuação, espaços colapsados."""
    sem_acento = unicodedata.normalize("NFKD", texto or "")
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", sem_acento.lower())).strip()


def trigramas(texto: str) -> FrozenSet[str]:
    t = f"  {normalizar(texto)}  "
    return frozenset(t[i:i + 3] for i in range(len(t) - 2))


def jaccard(a: FrozenSet[str], b: FrozenSet[str]) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def deduplicar(textos: Sequence[str], limiar: float = 0.7,
               existentes: Sequence[str] = ()) -> Tuple[List[int], List[Dict[str, object]]]:
    """Índices de `textos` mantidos (na ordem dada) e descartes com o motivo.

    Descarta o texto vazio, a cópia exata após normalizar e a quase duplicata (Jaccard >= `limiar`)
    de um texto já mantido ou de `existentes`.
    """
    if not 0.0 < limiar <= 1.0:
        raise ValueError("limiar fora de (0, 1]")
    base = [(f"existente:{i}", normalizar(t), trigramas(t)) for i, t in enumerate(existentes)]
    vistos = {n for _, n, _ in base}
    mantidos: List[int] = []
    descartes: List[Dict[str, object]] = []
    for i, t in enumerate(textos):
        n = normalizar(t)
        if not n:
            descartes.append({"indice": i, "motivo": "vazio"})
            continue
        if n in vistos:
            descartes.append({"indice": i, "motivo": "exata"})
            continue
        tri = trigramas(t)
        par = next(((ref, round(s, 4)) for ref, _, g in base if (s := jaccard(tri, g)) >= limiar), None)
        if par:
            descartes.append({"indice": i, "motivo": "quase_duplicata", "par": par[0], "jaccard": par[1]})
            continue
        vistos.add(n)
        base.append((f"novo:{i}", n, tri))
        mantidos.append(i)
    return mantidos, descartes


def cosseno(u: Sequence[float], v: Sequence[float]) -> float:
    if len(u) != len(v):
        raise ValueError("vetores de tamanhos diferentes")
    nu = math.sqrt(sum(x * x for x in u))
    nv = math.sqrt(sum(x * x for x in v))
    if nu == 0 or nv == 0:
        return 0.0
    return sum(a * b for a, b in zip(u, v)) / (nu * nv)


def agrupar(n: int, similaridade: Callable[[int, int], float], limiar: float) -> List[int]:
    """Rótulo de grupo por item (união-busca): i e j ficam juntos se similaridade(i, j) >= limiar,
    direta ou transitivamente. O rótulo é o menor índice do grupo."""
    pai = list(range(n))

    def raiz(i: int) -> int:
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if similaridade(i, j) >= limiar:
                ri, rj = raiz(i), raiz(j)
                if ri != rj:
                    pai[max(ri, rj)] = min(ri, rj)
    return [raiz(i) for i in range(n)]
