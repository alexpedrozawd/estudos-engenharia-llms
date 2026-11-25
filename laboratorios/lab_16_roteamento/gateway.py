"""Gateway de roteamento entre um modelo local rápido e um modelo de fronteira (Cap. 16).

Regras: fora de escopo é recusado sem chamar modelo; risco alto vai à fronteira
e, se ela cair, à fila humana (nunca é rebaixado); tarefa longa prefere a
fronteira; o resto começa no rápido. Modelo e esforço ficam fixos por conversa;
a troca no meio só ocorre como contingência (rota fora do ar) ou quando o risco
não admite o modelo fixado, sempre registrada e com sessão nova. Cada decisão
vira uma linha de registro em JSON.
"""
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from comum.cliente_llm import ClienteMockDeterministico

ESFORCO = {"rapido": "low", "fronteira": "high"}


def rotas(pedido: Dict[str, object]) -> List[str]:
    if pedido.get("fora_de_escopo"):
        return ["recusar"]
    if pedido.get("risco") == "alto":
        return ["fronteira", "fila_humana"]
    if int(pedido.get("passos", 1)) > 3:
        return ["fronteira", "rapido"]
    return ["rapido", "fronteira"]


def custo_cascata(custo_rapido: float, custo_fronteira: float, taxa_reprovacao: float) -> float:
    """Tenta o rápido; o verificador reprova uma fração, que vai à fronteira."""
    # EXERCICIO-INICIO: custo esperado = custo_rapido + taxa_reprovacao·custo_fronteira.
    return custo_rapido + taxa_reprovacao * custo_fronteira
    # EXERCICIO-FIM


def taxa_maxima_cascata(custo_rapido: float, custo_fronteira: float) -> float:
    """Acima desta taxa de reprovação, mandar tudo direto à fronteira sai mais barato."""
    # EXERCICIO-INICIO: a cascata compensa enquanto a reprovação for menor que 1 − custo_rapido/custo_fronteira.
    return 1 - custo_rapido / custo_fronteira
    # EXERCICIO-FIM


@dataclass
class Gateway:
    modelos: Dict[str, ClienteMockDeterministico]
    custos: Dict[str, float]
    indisponiveis: Set[str] = field(default_factory=set)
    fixados: Dict[str, str] = field(default_factory=dict)
    registro: List[str] = field(default_factory=list)

    def _log(self, **campos) -> None:
        self.registro.append(json.dumps(campos, ensure_ascii=False, sort_keys=True))

    def _destino(self, conversa: str, pedido: Dict[str, object]) -> str:
        # EXERCICIO-INICIO: mantenha o modelo fixado na conversa se disponível; senão o primeiro candidato disponível; nenhum = "fila_humana".
        candidatos = rotas(pedido)
        fixo = self.fixados.get(conversa)
        if fixo and fixo in candidatos and fixo not in self.indisponiveis:
            return fixo  # estabilidade: mesmo modelo e esforço durante a conversa
        for destino in candidatos:
            if destino not in self.indisponiveis:
                return destino
        return "fila_humana"
        # EXERCICIO-FIM

    def atender(self, conversa: str, pedido: Dict[str, object]) -> Dict[str, object]:
        destino = self._destino(conversa, pedido)
        fixo = self.fixados.get(conversa)
        if destino == fixo:
            motivo = "conversa fixada"
        elif destino == rotas(pedido)[0]:
            motivo = "regra"
        else:
            motivo = "contingência"
        if destino in ("recusar", "fila_humana"):
            self._log(conversa=conversa, destino=destino, motivo=motivo, custo=0)
            return {"destino": destino, "texto": None, "custo": 0, "nova_sessao": False}
        # Troca no meio da conversa (falha da rota ou risco que não admite o modelo fixado):
        # registra e abre sessão nova com resumo, sem prometer continuidade (16.6).
        nova_sessao = bool(fixo) and destino != fixo
        self.fixados[conversa] = destino
        resp = self.modelos[destino].completar(str(pedido.get("texto", "")), esforco=ESFORCO[destino])
        self._log(conversa=conversa, destino=destino, esforco=ESFORCO[destino], motivo=motivo,
                  nova_sessao=nova_sessao, custo=self.custos[destino], tokens_saida=resp.tokens_saida)
        return {"destino": destino, "texto": resp.texto, "custo": self.custos[destino], "nova_sessao": nova_sessao}

    def custo_total(self) -> float:
        return sum(json.loads(linha)["custo"] for linha in self.registro)


def gateway_aurora(indisponiveis: Optional[Set[str]] = None) -> Gateway:
    return Gateway(
        modelos={"rapido": ClienteMockDeterministico(fallback="Resposta do modelo local.", modelo="local-rapido"),
                 "fronteira": ClienteMockDeterministico(fallback="Resposta do modelo de fronteira.", modelo="fronteira")},
        custos={"rapido": 1.0, "fronteira": 12.0},
        indisponiveis=set(indisponiveis or ()))
