"""Custo por sessão, cache de prefixo, lote e pontos de equilíbrio (Cap. 18).

Tudo em "tokens equivalentes de entrada": multiplicadores, não preços, porque
preços mudam em semanas. Os multiplicadores de gravação (1,25) e leitura (0,1)
do cache e o desconto de lote (50%) seguem a ordem de grandeza vista no
capítulo, como proposta didática; confira a página de preços do provedor.
"""
import math
from typing import Dict, List, Sequence


def custo_sessao(prefixo: int, turnos: int, tokens_turno: int, saida_turno: int, mult_leitura: float = 1.0,
                 mult_gravacao: float = 1.0, invalidacoes: int = 0, mult_saida: float = 4.0) -> float:
    """O prefixo é gravado 1 + invalidacoes vezes e lido nos demais turnos."""
    # EXERCICIO-INICIO: gravações = min(turnos, 1 + invalidações); os outros turnos leem o prefixo; some prefixo, turnos e saída com seus multiplicadores.
    gravacoes = min(turnos, 1 + invalidacoes)
    leituras = turnos - gravacoes
    entrada = (gravacoes * prefixo * mult_gravacao + leituras * prefixo * mult_leitura + turnos * tokens_turno)
    return entrada + turnos * saida_turno * mult_saida
    # EXERCICIO-FIM


def leituras_para_compensar(mult_gravacao: float, mult_leitura: float) -> float:
    """Leituras mínimas para o cache sair mais barato que reenviar o prefixo sem cache."""
    # EXERCICIO-INICIO: ceil((mult_gravacao − 1)/(1 − mult_leitura)), no mínimo 1; infinito se a leitura não for mais barata.
    if mult_leitura >= 1:
        return math.inf
    return max(1, math.ceil((mult_gravacao - 1) / (1 - mult_leitura)))
    # EXERCICIO-FIM


def invalidacoes_maximas(base: Dict[str, int], mult_leitura: float, mult_gravacao: float) -> int:
    """Maior número de invalidações em que o cache ainda economiza na sessão."""
    sem = custo_sessao(**base)
    melhor = -1
    for k in range(base["turnos"]):
        if custo_sessao(**base, mult_leitura=mult_leitura, mult_gravacao=mult_gravacao, invalidacoes=k) < sem:
            melhor = k
    return melhor


def decidir_lote(prazo_horas: float, interativo: bool, janela_lote_horas: float = 24.0) -> bool:
    """Lote só quando ninguém espera na tela e o prazo comporta a janela do lote."""
    # EXERCICIO-INICIO: lote só para pedido não interativo com prazo >= janela do lote.
    return not interativo and prazo_horas >= janela_lote_horas
    # EXERCICIO-FIM


def varrer(base: Dict[str, int], campo: str, valores: Sequence[int], mult_leitura: float = 0.1,
           mult_gravacao: float = 1.25) -> List[Dict[str, float]]:
    """Sensibilidade: economia do cache ao variar um parâmetro da sessão."""
    linhas = []
    for v in valores:
        cfg = {**base, campo: v}
        sem = custo_sessao(**cfg)
        com = custo_sessao(**cfg, mult_leitura=mult_leitura, mult_gravacao=mult_gravacao)
        linhas.append({campo: v, "sem_cache": sem, "com_cache": com, "economia": round(1 - com / sem, 3)})
    return linhas


def orcamento_mensal(sessoes_dia: int, custo_sessao_tokens: float, preco_por_milhao: float, dias: int = 30) -> float:
    """Converte tokens equivalentes de entrada em dinheiro com o preço de entrada do modelo escolhido."""
    return round(sessoes_dia * dias * custo_sessao_tokens / 1e6 * preco_por_milhao, 2)
