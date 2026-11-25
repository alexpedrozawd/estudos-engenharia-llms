"""Harness de agente ReAct, offline e determinístico (Cap. 11).

O "modelo" é o ClienteMockDeterministico: recebe a pergunta e a última
observação e devolve JSON com pensamento, ação e argumento. O harness valida a
resposta do modelo, chama a ferramenta, verifica a observação, grava cada passo
em JSON, para no teto de passos e permite retomar do último passo salvo.
"""
import json
from typing import Callable, Dict, List, Optional, Tuple

from comum.cliente_llm import ClienteMockDeterministico

ACOES = {"buscar", "responder"}


def erro_composto(acerto_por_passo: float, passos: int) -> float:
    # EXERCICIO-INICIO: chance de acertar todos os passos: acerto_por_passo elevado a passos.
    return acerto_por_passo ** passos
    # EXERCICIO-FIM


class Harness:
    def __init__(self, cliente: ClienteMockDeterministico, ferramentas: Dict[str, Callable[[str], str]],
                 verificar: Optional[Callable[[str, str], bool]] = None, teto: int = 5):
        self.cliente, self.ferramentas, self.teto = cliente, ferramentas, teto
        self.verificar = verificar or (lambda acao, obs: obs != "nada")
        self.registro: List[str] = []

    def _passo_modelo(self, pergunta: str, observacao: str) -> Tuple[Optional[Dict], str]:
        texto = self.cliente.completar(f"PERGUNTA: {pergunta}\nOBS: {observacao}", esforco="low").texto
        try:
            dado = json.loads(texto)
        except json.JSONDecodeError:
            return None, "resposta do modelo não é JSON"
        if not isinstance(dado, dict) or dado.get("acao") not in ACOES or "argumento" not in dado:
            return None, "resposta do modelo fora do contrato"
        if dado["acao"] != "responder" and dado["acao"] not in self.ferramentas:
            return None, "ferramenta inexistente"
        return dado, ""

    def _log(self, **campos) -> None:
        self.registro.append(json.dumps(campos, ensure_ascii=False, sort_keys=True))

    def executar(self, pergunta: str, estado: Optional[Dict] = None) -> Dict[str, object]:
        # EXERCICIO-INICIO: laço com teto de passos: chame o modelo, pare em falha, execute a ação pedida e encerre na resposta final, registrando cada passo.
        estado = dict(estado or {"passo": 0, "observacao": "inicio"})
        while estado["passo"] < self.teto:
            estado["passo"] += 1
            dado, falha = self._passo_modelo(pergunta, estado["observacao"])
            if falha:
                self._log(passo=estado["passo"], parada=falha)
                return {"status": "parado", "motivo": falha, "estado": estado}
            if dado["acao"] == "responder":
                self._log(passo=estado["passo"], acao="responder", saida=dado["argumento"])
                return {"status": "respondido", "resposta": dado["argumento"], "estado": estado}
            obs = self.ferramentas[dado["acao"]](dado["argumento"])
            if not self.verificar(dado["acao"], obs):
                self._log(passo=estado["passo"], acao=dado["acao"], obs=obs, parada="observação reprovada")
                return {"status": "escalonar", "motivo": "observação reprovada", "estado": estado}
            estado["observacao"] = obs
            self._log(passo=estado["passo"], pensou=dado.get("pensamento", ""), acao=dado["acao"], obs=obs)
        self._log(passo=estado["passo"], parada="teto de passos")
        return {"status": "teto", "estado": estado}
        # EXERCICIO-FIM


def roteiro_aurora() -> Dict[str, str]:
    return {
        "OBS: inicio": json.dumps({"pensamento": "preciso da política", "acao": "buscar", "argumento": "reembolso"}),
        "OBS: POL-01: 7 dias": json.dumps({"pensamento": "falta a data", "acao": "buscar", "argumento": "data da matrícula"}),
        "OBS: matrícula há 3 dias": json.dumps({"pensamento": "tenho tudo", "acao": "responder",
                                                "argumento": "Cabe reembolso: 3 de 7 dias usados (POL-01)."}),
    }


def ferramentas_aurora() -> Dict[str, Callable[[str], str]]:
    base = {"reembolso": "POL-01: 7 dias", "data da matrícula": "matrícula há 3 dias"}
    return {"buscar": lambda q: base.get(q, "nada")}
