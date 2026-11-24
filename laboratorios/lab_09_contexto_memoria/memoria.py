"""Orçamento de janela, memória de longo prazo e feedback conversacional (Cap. 9).

- Janela por pares de turno, com instruções fixas e resumo do que sai (em vez
  de cortar turnos soltos por recência).
- Notas de sessão em SQLite, com consolidação de fatos que mudam (mesma chave
  substitui o valor anterior e guarda o histórico).
- Extrator determinístico de sinais implícitos de feedback, agregados por versão.
"""
import re
import sqlite3
from collections import Counter, defaultdict
from typing import Dict, List, Sequence, Tuple

from comum.cliente_llm import ClienteMockDeterministico


def tokens(texto: str) -> int:
    return len(texto.split())


def janela_por_recencia(sistema: str, turnos: Sequence[str], pergunta: str, limite: int) -> List[str]:
    usados, mantidos = tokens(sistema) + tokens(pergunta), []
    for t in reversed(turnos):
        if usados + tokens(t) > limite:
            break
        mantidos.insert(0, t)
        usados += tokens(t)
    return mantidos


def janela_por_pares(sistema: str, pares: Sequence[Tuple[str, str]], pergunta: str, limite: int,
                     cliente: ClienteMockDeterministico, reserva_resumo: int = 10) -> Dict[str, object]:
    """Mantém pares completos mais recentes dentro de `limite - reserva_resumo`;
    o que sai vira um resumo de até `reserva_resumo` tokens, cortado se o modelo exceder."""
    usados, mantidos = tokens(sistema) + tokens(pergunta), []
    orcamento = limite - reserva_resumo
    corte = len(pares)
    for i in range(len(pares) - 1, -1, -1):
        custo = tokens(pares[i][0]) + tokens(pares[i][1])
        if usados + custo > orcamento:
            break
        mantidos.insert(0, pares[i])
        usados += custo
        corte = i
    resumo = ""
    if corte > 0:
        antigos = " | ".join(f"{u} / {a}" for u, a in pares[:corte])
        resumo = cliente.completar("Resuma em uma frase: " + antigos, esforco="low", max_tokens=reserva_resumo).texto
        resumo = " ".join(resumo.split()[:reserva_resumo])
    return {"sistema": sistema, "resumo": resumo, "pares": mantidos, "tokens": usados + tokens(resumo)}


class NotasSessao:
    def __init__(self, caminho: str = ":memory:"):
        self.db = sqlite3.connect(caminho)
        self.db.execute("CREATE TABLE IF NOT EXISTS nota (aluno TEXT, chave TEXT, valor TEXT, versao INTEGER, "
                        "PRIMARY KEY (aluno, chave, versao))")

    def fechar(self) -> None:
        self.db.close()

    def lembrar(self, aluno: str, chave: str, valor: str) -> int:
        atual = self.db.execute("SELECT MAX(versao) FROM nota WHERE aluno = ? AND chave = ?", (aluno, chave)).fetchone()[0]
        versao = (atual or 0) + 1
        self.db.execute("INSERT INTO nota VALUES (?, ?, ?, ?)", (aluno, chave, valor, versao))
        return versao

    def fatos(self, aluno: str) -> Dict[str, str]:
        linhas = self.db.execute(
            "SELECT chave, valor FROM nota n WHERE aluno = ? AND versao = "
            "(SELECT MAX(versao) FROM nota WHERE aluno = n.aluno AND chave = n.chave) ORDER BY chave", (aluno,)).fetchall()
        return dict(linhas)

    def historico(self, aluno: str, chave: str) -> List[str]:
        return [v for (v,) in self.db.execute(
            "SELECT valor FROM nota WHERE aluno = ? AND chave = ? ORDER BY versao", (aluno, chave))]


SINAIS = {
    "correcao": r"^(não|nao)\b|eu quis dizer",
    "pede_fonte": r"tem certeza|qual a fonte",
    "interrompe": r"\b(pare|chega)\b",
    "agradece": r"\b(obrigad[oa]|valeu)\b",
}


def sinais(mensagem: str) -> List[str]:
    m = mensagem.lower().strip()
    return [nome for nome, p in SINAIS.items() if re.search(p, m)] or ["neutro"]


def taxas_por_versao(registros: Sequence[Tuple[str, str]]) -> Dict[str, Dict[str, float]]:
    """registros: (versao_prompt, mensagem_do_usuario). Devolve taxa de cada sinal por versão."""
    por: Dict[str, Counter] = defaultdict(Counter)
    totais: Counter = Counter()
    for versao, msg in registros:
        totais[versao] += 1
        for s in sinais(msg):
            por[versao][s] += 1
    return {v: {s: round(c / totais[v], 3) for s, c in sorted(por[v].items())} for v in sorted(totais)}
