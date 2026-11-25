"""Operação em produção: rastros, desvio, canário e métricas de incidente (Cap. 17).

Os rastros usam nomes de atributos das convenções semânticas GenAI do
OpenTelemetry (`gen_ai.operation.name`, `gen_ai.request.model`,
`gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`), sem depender do SDK:
cada span é um dicionário que poderia ser exportado. O relógio é injetado para
os testes serem determinísticos.
"""
import hashlib
import math
from contextlib import contextmanager
from typing import Callable, Dict, Iterator, List, Optional, Sequence


class Rastreador:
    def __init__(self, relogio: Callable[[], float]):
        self.relogio = relogio
        self.spans: List[Dict[str, object]] = []
        self._pilha: List[str] = []
        self._n = 0

    @contextmanager
    def span(self, nome: str, trace_id: str, **atributos) -> Iterator[Dict[str, object]]:
        self._n += 1
        registro = {"name": nome, "trace_id": trace_id, "span_id": f"s{self._n:04d}",
                    "parent_id": self._pilha[-1] if self._pilha else None,
                    "start": self.relogio(), "attributes": dict(atributos), "status": "OK"}
        self._pilha.append(registro["span_id"])
        try:
            yield registro
        except Exception as exc:
            registro["status"] = "ERROR"
            registro["attributes"]["error.type"] = type(exc).__name__
            raise
        finally:
            self._pilha.pop()
            registro["end"] = self.relogio()
            self.spans.append(registro)

    def resumo(self, trace_id: str) -> Dict[str, object]:
        spans = [s for s in self.spans if s["trace_id"] == trace_id]
        llm = [s for s in spans if s["attributes"].get("gen_ai.operation.name") == "chat"]
        return {"spans": len(spans), "erros": sum(s["status"] == "ERROR" for s in spans),
                "tokens_entrada": sum(s["attributes"].get("gen_ai.usage.input_tokens", 0) for s in llm),
                "tokens_saida": sum(s["attributes"].get("gen_ai.usage.output_tokens", 0) for s in llm),
                "duracao": max(s["end"] for s in spans) - min(s["start"] for s in spans)}


def distribuicao(rotulos: Sequence[str]) -> Dict[str, float]:
    total = len(rotulos)
    contagem: Dict[str, int] = {}
    for r in rotulos:
        contagem[r] = contagem.get(r, 0) + 1
    return {k: v / total for k, v in sorted(contagem.items())}


def psi(referencia: Dict[str, float], atual: Dict[str, float], piso: float = 1e-4) -> float:
    """Índice de estabilidade da população; considera faixas que só aparecem num dos lados."""
    # EXERCICIO-INICIO: soma de (atual − ref)·ln(atual/ref) por faixa, com piso nas faixas vazias; 3 casas.
    total = 0.0
    for faixa in set(referencia) | set(atual):
        r = max(referencia.get(faixa, 0.0), piso)
        a = max(atual.get(faixa, 0.0), piso)
        total += (a - r) * math.log(a / r)
    return round(total, 3)
    # EXERCICIO-FIM


def grupo(usuario: str, fracao_canario: float = 0.05, sal: str = "canario-v2") -> str:
    """Sorteio determinístico por hash: o mesmo usuário cai sempre no mesmo grupo nesta rodada (sal)."""
    # EXERCICIO-INICIO: sha256 de "sal:usuario", 8 primeiros hex / 0xFFFFFFFF; abaixo da fração = "canario", senão "controle".
    h = int(hashlib.sha256(f"{sal}:{usuario}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    return "canario" if h < fracao_canario else "controle"
    # EXERCICIO-FIM


def decidir_canario(controle: Dict[str, float], canario: Dict[str, float], n_canario: int, n_minimo: int = 200,
                    max_piora_acerto: float = 0.02, max_aumento_latencia: float = 0.10) -> str:
    """Promover, reverter ou esperar mais dados (métricas: acerto e latência p95)."""
    # EXERCICIO-INICIO: reverta se o acerto cair ou a p95 subir além do tolerado; promova com amostra mínima; senão espere.
    if canario["acerto"] < controle["acerto"] - max_piora_acerto:
        return "reverter"
    if canario["latencia_p95"] > controle["latencia_p95"] * (1 + max_aumento_latencia):
        return "reverter"
    return "promover" if n_canario >= n_minimo else "esperar"
    # EXERCICIO-FIM


def metricas_operacao(incidentes: Sequence[Dict[str, float]], mudancas: int) -> Dict[str, Optional[float]]:
    """MTTD (início→detecção), MTTR (início→restauração) e CFR (mudanças com falha / mudanças)."""
    if not incidentes:
        return {"mttd": None, "mttr": None, "cfr": 0.0 if mudancas else None}
    n = len(incidentes)
    mttd = sum(i["detectado"] - i["inicio"] for i in incidentes) / n
    mttr = sum(i["restaurado"] - i["inicio"] for i in incidentes) / n
    com_falha = sum(1 for i in incidentes if i.get("causado_por_mudanca"))
    return {"mttd": mttd, "mttr": mttr, "cfr": com_falha / mudancas if mudancas else None}
