"""Memória de inferência e medição de latência num servidor simulado (Cap. 14).

As medidas saem de carimbos de tempo por token, como num stream real: TTFT
(tempo até o primeiro token), TPOT (tempo médio por token de saída depois do
primeiro), ITL (intervalos entre tokens), percentis e goodput (pedidos dentro
do SLO). Para medir um servidor real (Ollama, llama.cpp, vLLM), grave os
carimbos de cada pedaço do stream e passe-os a `medir_pedido`.
"""
import math
import random
from typing import Dict, List, Sequence, Tuple

GIB = 1024 ** 3


def memoria(params_b: float, bits_peso: float, camadas: int, cabecas_kv: int, dim_cabeca: int,
            contexto: int, bytes_kv: int = 2, usuarios: int = 1) -> Tuple[float, float]:
    """Pesos e KV cache em GiB (K e V por camada, cabeça KV, posição e usuário)."""
    pesos = params_b * 1e9 * bits_peso / 8
    kv = 2 * camadas * cabecas_kv * dim_cabeca * contexto * bytes_kv * usuarios
    return pesos / GIB, kv / GIB


def camadas_na_gpu(vram_gib: float, pesos_gib: float, kv_gib: float, camadas: int, reserva_gib: float = 1.0) -> int:
    """Quantas camadas cabem na GPU; o resto vai para a CPU e derruba a velocidade (descarga)."""
    por_camada = (pesos_gib + kv_gib) / camadas
    return max(0, min(camadas, int((vram_gib - reserva_gib) // por_camada)))


def medir_pedido(inicio: float, carimbos: Sequence[float]) -> Dict[str, float]:
    if not carimbos:
        raise ValueError("pedido sem tokens")
    ttft = carimbos[0] - inicio
    itl = [b - a for a, b in zip(carimbos, carimbos[1:])]
    tpot = sum(itl) / len(itl) if itl else 0.0
    return {"ttft": ttft, "tpot": tpot, "total": carimbos[-1] - inicio, "tokens": len(carimbos), "itl": itl}


def percentil(valores: Sequence[float], p: float) -> float:
    """Percentil por posto mais próximo (nearest-rank): sempre um valor observado."""
    ordenados = sorted(valores)
    k = max(1, math.ceil(p / 100 * len(ordenados)))
    return ordenados[k - 1]


def servidor_simulado(pedidos: int, semente: int = 14, fila_lenta_a_cada: int = 10) -> List[Tuple[float, List[float]]]:
    """Gera (início, carimbos) por pedido; um a cada `fila_lenta_a_cada` espera na fila (cauda do TTFT)."""
    rng = random.Random(semente)
    saida = []
    for i in range(pedidos):
        inicio = float(i)
        ttft = rng.uniform(0.20, 0.45) + (1.2 if i % fila_lenta_a_cada == fila_lenta_a_cada - 1 else 0.0)
        t, carimbos = inicio + ttft, []
        for _ in range(rng.randint(40, 120)):
            carimbos.append(t)
            t += rng.uniform(0.03, 0.07)
        saida.append((inicio, carimbos))
    return saida


def relatorio(medidas: Sequence[Dict[str, float]], slo_ttft: float, slo_tpot: float) -> Dict[str, float]:
    ttfts = [m["ttft"] for m in medidas]
    tpots = [m["tpot"] for m in medidas]
    dentro = sum(m["ttft"] <= slo_ttft and m["tpot"] <= slo_tpot for m in medidas)
    return {"ttft_p50": percentil(ttfts, 50), "ttft_p95": percentil(ttfts, 95), "ttft_p99": percentil(ttfts, 99),
            "tpot_p50": percentil(tpots, 50), "tpot_p95": percentil(tpots, 95),
            "media_ttft": sum(ttfts) / len(ttfts), "goodput": dentro / len(medidas)}
