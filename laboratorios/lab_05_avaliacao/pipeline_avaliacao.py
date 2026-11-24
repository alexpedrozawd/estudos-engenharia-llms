"""Pipeline determinístico de avaliação e estatística reproduzível (L4)."""
import math
import random
from typing import Dict, List, Sequence, Tuple

from comum.cliente_llm import ClienteMockDeterministico


def entropia_e_perplexidade(probs: Sequence[float]) -> Tuple[float, float, float]:
    """Calcula entropia em bits H(P) e perplexidade em base 2 e base e."""
    if not probs:
        raise ValueError("distribuição vazia")
    soma = sum(probs)
    if abs(soma - 1.0) > 1e-6:
        raise ValueError("probabilidades devem somar 1")
    h_bits = -sum(p * math.log2(p) for p in probs if p > 0)
    h_nats = -sum(p * math.log(p) for p in probs if p > 0)
    return h_bits, 2.0 ** h_bits, math.exp(h_nats)


def intervalo_wilson(acertos: int, total: int, z: float = 1.96) -> Tuple[float, float]:
    """Calcula intervalo de confiança de Wilson para proporção binomial."""
    if total <= 0 or not (0 <= acertos <= total):
        raise ValueError("contagens inválidas")
    p_hat = acertos / total
    z2 = z * z
    denom = 1.0 + z2 / total
    centro = (p_hat + z2 / (2.0 * total)) / denom
    margem = (z * math.sqrt((p_hat * (1.0 - p_hat) + z2 / (4.0 * total)) / total)) / denom
    return max(0.0, centro - margem), min(1.0, centro + margem)


def bootstrap_diferenca_media(
    v1: Sequence[int],
    v2: Sequence[int],
    *,
    rodadas: int = 1000,
    semente: int = 42,
) -> Dict[str, float]:
    """Estima IC 95% por bootstrap pareado da diferença (v2 - v1)."""
    if len(v1) != len(v2) or not v1:
        raise ValueError("listas pareadas devem ter mesmo tamanho > 0")
    diffs = [b - a for a, b in zip(v1, v2)]
    n = len(diffs)
    rng = random.Random(semente)
    medias: List[float] = []
    for _ in range(rodadas):
        amostra = [diffs[rng.randrange(n)] for _ in range(n)]
        medias.append(sum(amostra) / n)
    medias.sort()
    idx_inf = max(0, int(0.025 * rodadas))
    idx_sup = min(rodadas - 1, int(0.975 * rodadas))
    return {
        "diferenca_observada": sum(diffs) / n,
        "ic95_inf": medias[idx_inf],
        "ic95_sup": medias[idx_sup],
    }


def comparar_pareado(v1: Sequence[int], v2: Sequence[int]) -> Dict[str, int]:
    """Conta ganhos, perdas e empates caso a caso entre v1 e v2."""
    if len(v1) != len(v2):
        raise ValueError("tamanhos distintos")
    ganhos = perdas = ambos_ok = ambos_falha = 0
    for a, b in zip(v1, v2):
        if a == 0 and b == 1:
            ganhos += 1
        elif a == 1 and b == 0:
            perdas += 1
        elif a == 1 and b == 1:
            ambos_ok += 1
        else:
            ambos_falha += 1
    return {
        "ganhos_v2": ganhos,
        "perdas_v2": perdas,
        "saldo": ganhos - perdas,
        "ambos_ok": ambos_ok,
        "ambos_falha": ambos_falha,
    }


def avaliar_por_fatias(registros: Sequence[Dict[str, object]]) -> Dict[str, Dict[str, float]]:
    """Agrupa taxa de acerto por fatia (slice) para evitar Paradoxo de Simpson."""
    grupos: Dict[str, List[int]] = {}
    for item in registros:
        fatia = str(item["fatia"])
        grupos.setdefault(fatia, []).append(int(item["passou"]))
    return {
        fatia: {
            "total": float(len(vals)),
            "taxa": sum(vals) / len(vals),
        }
        for fatia, vals in grupos.items()
    }


def julgar_pareado_sem_vies_posicao(
    pergunta: str,
    resp_a: str,
    resp_b: str,
    cliente: ClienteMockDeterministico,
) -> str:
    """Roda juiz nas duas ordens (A/B e B/A) para detectar viés de posição."""
    ordem_1 = cliente.completar(f"Pergunta: {pergunta}\n[1] {resp_a}\n[2] {resp_b}").texto.strip()
    ordem_2 = cliente.completar(f"Pergunta: {pergunta}\n[1] {resp_b}\n[2] {resp_a}").texto.strip()
    if ordem_1 == "1" and ordem_2 == "2":
        return "vencedor_A"
    if ordem_1 == "2" and ordem_2 == "1":
        return "vencedor_B"
    return "empate_ou_inconsistente"
