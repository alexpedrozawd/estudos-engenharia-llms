"""Cliente neutro para provedores de LLM com modo mock determinístico offline.

Separa claramente o contrato de chamada (provedor, modelo, esforço de raciocínio,
mensagens e metadados de custo/latência) da camada de transporte HTTP opcional.
"""
from dataclasses import dataclass, field
import json
from typing import Callable, Dict, List, Optional
import urllib.request


@dataclass(frozen=True)
class RespostaLLM:
    """Resposta padronizada independente do provedor."""

    texto: str
    provedor: str
    modelo: str
    tokens_entrada: int
    tokens_saida: int
    latencia_ms: float
    tokens_cache: int = 0
    metadados: Dict[str, str] = field(default_factory=dict)

    @property
    def custo_relativo_tokens(self) -> float:
        """Estimativa neutra de custo relativo (saída ~3x entrada; cache ~0.25x)."""
        entrada_nao_cache = max(0, self.tokens_entrada - self.tokens_cache)
        return entrada_nao_cache + 0.25 * self.tokens_cache + 3.0 * self.tokens_saida


class ClienteMockDeterministico:
    """Simulador determinístico para testes unitários offline sem rede."""

    def __init__(
        self,
        respostas: Optional[Dict[str, str]] = None,
        fallback: str = "Resposta sintética padrão (modo offline).",
        provedor: str = "mock-aurora",
        modelo: str = "modelo-didatico-v1",
    ):
        self.respostas = dict(respostas or {})
        self.fallback = fallback
        self.provedor = provedor
        self.modelo = modelo
        self.chamadas: List[Dict[str, object]] = []

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: str = "medium",
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaLLM:
        self.chamadas.append(
            {
                "prompt": prompt,
                "sistema": sistema,
                "esforco": esforco,
                "temperatura": temperatura,
                "max_tokens": max_tokens,
            }
        )
        texto = self.fallback
        for chave, valor in self.respostas.items():
            if chave in prompt:
                texto = valor
                break
        tokens_in = max(1, len((sistema + " " + prompt).split()))
        tokens_out = max(1, len(texto.split()))
        return RespostaLLM(
            texto=texto,
            provedor=self.provedor,
            modelo=self.modelo,
            tokens_entrada=tokens_in,
            tokens_saida=tokens_out,
            latencia_ms=18.5 if esforco == "low" else 42.0,
            tokens_cache=max(0, len(sistema.split()) - 1) if sistema else 0,
            metadados={"esforco": esforco},
        )


def chamar_http_json(
    url: str,
    payload: Dict[str, object],
    cabecalhos: Optional[Dict[str, str]] = None,
    timeout_s: float = 15.0,
    opener: Optional[Callable[..., object]] = None,
) -> Dict[str, object]:
    """Envia requisição POST JSON sem acoplar bibliotecas externas.

    Permite injeção de `opener` para validação unitária via unittest.mock.
    """
    corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if cabecalhos:
        headers.update(cabecalhos)
    req = urllib.request.Request(url, data=corpo, headers=headers, method="POST")
    fn = opener or urllib.request.urlopen
    with fn(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))
