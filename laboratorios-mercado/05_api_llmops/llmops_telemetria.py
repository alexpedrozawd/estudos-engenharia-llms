"""Telemetria (OpenTelemetry) e avaliação contínua do projeto 05.

Spans seguem as convenções semânticas de GenAI do OpenTelemetry (`gen_ai.*`, ainda em
estágio *development*), sem gravar o texto do prompt ou da resposta (só tamanhos e hashes),
para não vazar dados pessoais na observabilidade.

Exportadores: `console` (padrão), `otlp` (usa `OTEL_EXPORTER_OTLP_ENDPOINT`, ex.: Jaeger,
Phoenix ou Langfuse com OTLP/HTTP), `memoria` (testes) ou `nenhum`.
"""
from __future__ import annotations

import hashlib
import os
import sys
from typing import Dict, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mercado_base.pii import RE_CPF, RE_EMAIL, RE_TELEFONE, detectar_pii  # noqa: E402,F401

from opentelemetry.sdk.resources import Resource  # noqa: E402
from opentelemetry.sdk.trace import TracerProvider  # noqa: E402
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor  # noqa: E402
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter  # noqa: E402


def configurar_telemetria(modo: str = "console", servico: str = "aurora-api-llmops") -> Tuple[TracerProvider, Optional[InMemorySpanExporter]]:
    """Cria um `TracerProvider` próprio (sem tocar no global) e devolve o exportador em memória, se houver."""
    provider = TracerProvider(resource=Resource.create({"service.name": servico}))
    memoria = None
    if modo == "console":
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    elif modo == "otlp":
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    elif modo == "memoria":
        memoria = InMemorySpanExporter()
        provider.add_span_processor(SimpleSpanProcessor(memoria))
    elif modo != "nenhum":
        raise ValueError("modo de telemetria inválido")
    return provider, memoria


def hash_curto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:16]


class AvaliadorContinuo:
    """Amostra respostas de produção (determinístico por id) e aplica verificações baratas.

    Dispara `alerta` quando há ao menos `minimo_amostras` e a taxa de aprovação fica abaixo de `limiar`.
    """

    def __init__(self, taxa_amostragem: float = 1.0, limite_caracteres: int = 4000,
                 limiar: float = 0.9, minimo_amostras: int = 5):
        if not 0.0 <= taxa_amostragem <= 1.0:
            raise ValueError("taxa_amostragem fora de [0, 1]")
        self.taxa = taxa_amostragem
        self.limite = limite_caracteres
        self.limiar = limiar
        self.minimo = minimo_amostras
        self.avaliadas = 0
        self.aprovadas = 0
        self.falhas: Dict[str, int] = {"vazia": 0, "pii": 0, "longa_demais": 0}

    def amostrar(self, id_requisicao: str) -> bool:
        balde = int(hashlib.sha256(id_requisicao.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
        return balde < self.taxa

    def avaliar(self, id_requisicao: str, resposta: str) -> Optional[Dict[str, object]]:
        if not self.amostrar(id_requisicao):
            return None
        checagens = {
            "vazia": not resposta.strip(),
            "pii": bool(detectar_pii(resposta)),
            "longa_demais": len(resposta) > self.limite,
        }
        self.avaliadas += 1
        for nome, falhou in checagens.items():
            self.falhas[nome] += int(falhou)
        falhas = sorted(nome for nome, falhou in checagens.items() if falhou)
        if not falhas:
            self.aprovadas += 1
        return {"aprovada": not falhas, "falhas": falhas}

    def resumo(self) -> Dict[str, object]:
        taxa = self.aprovadas / self.avaliadas if self.avaliadas else None
        return {
            "avaliadas": self.avaliadas, "aprovadas": self.aprovadas, "falhas": dict(self.falhas),
            "taxa_aprovacao": round(taxa, 4) if taxa is not None else None,
            "alerta": bool(self.avaliadas >= self.minimo and taxa is not None and taxa < self.limiar),
        }
