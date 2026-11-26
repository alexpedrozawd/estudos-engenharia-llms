"""Estatística de avaliação compartilhada pela Camada 3 (P02 e P07; o P04 mantém a sua cópia de exercício).

- `wilson`: intervalo de 95% para uma proporção, válido em amostras pequenas (parte 5.6f do guia);
- `mcnemar_exato`: teste pareado para acerto/erro de dois sistemas nos mesmos casos;
- `bootstrap_diferenca`: intervalo da diferença média pareada (B − A) por reamostragem com semente;
- `comparar_binario`: os três acima de uma vez, para resultados por caso.
"""
from __future__ import annotations

import math
import random
from typing import Dict, Mapping, Sequence, Tuple


def wilson(acertos: int, n: int, z: float = 1.96) -> Tuple[float, float]:
    if n <= 0:
        return (0.0, 1.0)
    if not 0 <= acertos <= n:
        raise ValueError("acertos fora de [0, n]")
    p = acertos / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    margem = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (round(max(0.0, centro - margem), 4), round(min(1.0, centro + margem), 4))


def mcnemar_exato(ganhos: int, perdas: int) -> float:
    """p-valor bilateral exato: binomial(0,5) sobre os casos discordantes; sem discordantes, 1,0."""
    n = ganhos + perdas
    if n == 0:
        return 1.0
    k = min(ganhos, perdas)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)


def bootstrap_diferenca(a: Sequence[float], b: Sequence[float], *, n_amostras: int = 2000,
                        alfa: float = 0.05, semente: int = 42) -> Dict[str, float]:
    if len(a) != len(b) or not a:
        raise ValueError("a e b devem ter o mesmo tamanho (> 0)")
    difs = [float(y) - float(x) for x, y in zip(a, b)]
    n = len(difs)
    rng = random.Random(semente)
    medias = sorted(sum(difs[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_amostras))
    inf = medias[max(0, int(alfa / 2 * n_amostras))]
    sup = medias[min(n_amostras - 1, int((1 - alfa / 2) * n_amostras) - 1)]
    return {"diferenca_media": round(sum(difs) / n, 4), "ic_inferior": round(inf, 4), "ic_superior": round(sup, 4)}


def comparar_binario(a: Mapping[str, bool], b: Mapping[str, bool]) -> Dict[str, object]:
    """Compara acerto por caso de A e B (mesmos ids): Wilson de cada um, ganhos/perdas de B e McNemar."""
    if set(a) != set(b) or not a:
        raise ValueError("A e B precisam dos mesmos casos (> 0)")
    n = len(a)
    ganhos = sum(1 for i in a if b[i] and not a[i])
    perdas = sum(1 for i in a if a[i] and not b[i])
    ok_a, ok_b = sum(map(bool, a.values())), sum(map(bool, b.values()))
    return {"n": n, "acertos_a": ok_a, "acertos_b": ok_b, "wilson95_a": wilson(ok_a, n),
            "wilson95_b": wilson(ok_b, n), "ganhos_b": ganhos, "perdas_b": perdas,
            "p_valor_mcnemar_exato": mcnemar_exato(ganhos, perdas)}
