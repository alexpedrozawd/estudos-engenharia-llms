"""Travas determinísticas, disjuntor e reversão para agentes (Cap. 13).

Cada trava é verificável por teste, ao contrário de uma instrução no prompt:
lista de permissão, bloqueio de repetição idêntica, orçamento de tentativas,
simulação (dry-run) de ações destrutivas, disjuntor (circuit breaker) e
reversão (rollback) para o último estado bom quando um invariante quebra.
"""
import copy
from typing import Callable, Dict, List, Optional, Set, Tuple

PERMITIDOS = {"ler_arquivo", "listar_pasta", "gravar_relatorio", "atualizar_nota"}
DESTRUTIVOS = {"gravar_relatorio", "atualizar_nota"}


class Trava:
    def __init__(self, orcamento_tentativas: int = 3, simular: bool = True,
                 permitidos: Set[str] = PERMITIDOS, destrutivos: Set[str] = DESTRUTIVOS):
        self.restantes, self.simular = orcamento_tentativas, simular
        self.permitidos, self.destrutivos = permitidos, destrutivos
        self.vistos: Set[Tuple[str, str]] = set()

    def autorizar(self, acao: str, alvo: str) -> str:
        # EXERCICIO-INICIO: na ordem: lista de permissão, repetição idêntica, orçamento de tentativas e confirmação humana para ação destrutiva.
        if acao not in self.permitidos:
            return "bloqueado: fora da lista de permissão"
        if (acao, alvo) in self.vistos:
            return "bloqueado: repetição idêntica"
        if self.restantes == 0:
            return "parar: orçamento de tentativas esgotado"
        self.vistos.add((acao, alvo))
        self.restantes -= 1
        if acao in self.destrutivos and self.simular:
            return "simulado (dry-run): nada gravado"
        return "executar"
        # EXERCICIO-FIM


class Disjuntor:
    """Abre após `limite` falhas seguidas; após `espera` unidades de tempo, deixa passar um teste (meio-aberto)."""

    def __init__(self, limite: int = 3, espera: float = 30.0, relogio: Callable[[], float] = lambda: 0.0):
        self.limite, self.espera, self.relogio = limite, espera, relogio
        self.falhas, self.aberto_em, self.estado = 0, None, "fechado"

    def permitir(self) -> bool:
        if self.estado == "aberto" and self.relogio() - self.aberto_em >= self.espera:
            self.estado = "meio-aberto"
        return self.estado != "aberto"

    def registrar(self, sucesso: bool) -> None:
        # EXERCICIO-INICIO: sucesso zera falhas e fecha; falha soma e abre (guardando o horário) ao atingir o limite ou se estava meio-aberto.
        if sucesso:
            self.falhas, self.estado = 0, "fechado"
            return
        self.falhas += 1
        if self.estado == "meio-aberto" or self.falhas >= self.limite:
            self.estado, self.aberto_em = "aberto", self.relogio()
        # EXERCICIO-FIM


class Transacao:
    """Aplica ações sobre uma cópia; confirma só se o invariante valer, senão reverte ao estado anterior."""

    def __init__(self, estado: Dict, invariante: Callable[[Dict], bool]):
        self.estado, self.invariante = estado, invariante
        self.historico: List[Dict] = []

    def aplicar(self, mudanca: Callable[[Dict], None]) -> bool:
        ponto = copy.deepcopy(self.estado)
        mudanca(self.estado)
        if self.invariante(self.estado):
            self.historico.append(ponto)
            return True
        self.estado.clear()
        self.estado.update(ponto)
        return False

    def desfazer(self) -> bool:
        # EXERCICIO-INICIO: restaure o último estado do histórico no próprio dicionário; False se o histórico estiver vazio.
        if not self.historico:
            return False
        anterior = self.historico.pop()
        self.estado.clear()
        self.estado.update(anterior)
        return True
        # EXERCICIO-FIM


def simular_incidente(chamar: Callable[[], bool], tentativas: int, disjuntor: Optional[Disjuntor] = None) -> Dict[str, int]:
    """Agente que insiste numa ação que falha: conta chamadas reais com e sem disjuntor."""
    chamadas = barradas = 0
    for _ in range(tentativas):
        if disjuntor and not disjuntor.permitir():
            barradas += 1
            continue
        chamadas += 1
        ok = chamar()
        if disjuntor:
            disjuntor.registrar(ok)
    return {"chamadas": chamadas, "barradas": barradas}


def proporcionalidade(acerto_agente: float, custo_agente: float, acerto_script: float, custo_script: float,
                      valor_acerto: float, custo_erro: float) -> Dict[str, object]:
    """Valor líquido esperado por tarefa; o agente só fica se render mais que o script simples."""
    def liquido(acerto: float, custo: float) -> float:
        return acerto * valor_acerto - (1 - acerto) * custo_erro - custo

    a, s = liquido(acerto_agente, custo_agente), liquido(acerto_script, custo_script)
    return {"agente": round(a, 2), "script": round(s, 2), "escolha": "agente" if a > s else "script"}
