"""Mini pipeline de RAG híbrido, offline e determinístico (Cap. 7).

BM25 para termos exatos, "embedding" local por hashing de palavras (didático, sem
modelo), fusão RRF (k = 60), métricas de recuperação (recall@K, MRR, NDCG@K) e
checagem de fidelidade: a resposta só pode citar trechos recuperados.
"""
import hashlib
import json
import math
import os
import re
from typing import Dict, List, Sequence, Tuple

from comum.cliente_llm import ClienteMockDeterministico

DADOS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dados", "politicas_aurora.json")


def carregar_documentos(caminho: str = DADOS) -> Dict[str, str]:
    with open(caminho, encoding="utf-8") as arq:
        dados = json.load(arq)
    return {p["id"]: p["titulo"] + ". " + p["texto"] for p in dados["politicas"]}


def tokenizar(texto: str) -> List[str]:
    return re.findall(r"\w+", texto.lower())


def fatiar(palavras: Sequence[str], tamanho: int, sobreposicao: int) -> List[str]:
    if not 0 <= sobreposicao < tamanho:
        raise ValueError("sobreposição deve ficar entre 0 e tamanho - 1")
    passo = tamanho - sobreposicao
    return [" ".join(palavras[i:i + tamanho]) for i in range(0, max(1, len(palavras) - sobreposicao), passo)]


class BM25:
    def __init__(self, docs: Dict[str, str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tokens = {d: tokenizar(t) for d, t in docs.items()}
        self.media = sum(len(t) for t in self.tokens.values()) / max(1, len(self.tokens))
        self.df: Dict[str, int] = {}
        for t in self.tokens.values():
            for termo in set(t):
                self.df[termo] = self.df.get(termo, 0) + 1

    def idf(self, termo: str) -> float:
        n, df = len(self.tokens), self.df.get(termo, 0)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def ranking(self, consulta: str) -> List[Tuple[str, float]]:
        # EXERCICIO-INICIO: some idf·f·(k1+1)/(f + k1·(1 − b + b·|d|/média)) por termo; descarte nota 0; ordene por nota decrescente e id.
        notas = []
        for d, t in self.tokens.items():
            s = 0.0
            for termo in tokenizar(consulta):
                f = t.count(termo)
                if f:
                    s += self.idf(termo) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(t) / self.media))
            notas.append((d, s))
        return sorted([x for x in notas if x[1] > 0], key=lambda x: (-x[1], x[0]))
        # EXERCICIO-FIM


def vetor(texto: str, dim: int = 64) -> List[float]:
    """Embedding didático por hashing de palavras (truque de hashing do DMLS, cap. 5)."""
    v = [0.0] * dim
    for termo in tokenizar(texto):
        h = int(hashlib.md5(termo.encode("utf-8")).hexdigest(), 16)
        v[h % dim] += 1.0
    norma = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norma for x in v]


def ranking_vetorial(consulta: str, docs: Dict[str, str]) -> List[Tuple[str, float]]:
    q = vetor(consulta)
    notas = [(d, sum(a * b for a, b in zip(q, vetor(t)))) for d, t in docs.items()]
    return sorted([x for x in notas if x[1] > 0], key=lambda x: (-x[1], x[0]))


def rrf(rankings: Sequence[Sequence[str]], k: int = 60) -> List[Tuple[str, float]]:
    # EXERCICIO-INICIO: nota(doc) = soma de 1/(k + posição) em cada ranking (posição começa em 1); ordene por nota decrescente e id.
    nota: Dict[str, float] = {}
    for ranking in rankings:
        for pos, doc in enumerate(ranking, start=1):
            nota[doc] = nota.get(doc, 0.0) + 1.0 / (k + pos)
    return sorted(nota.items(), key=lambda x: (-x[1], x[0]))
    # EXERCICIO-FIM


def buscar_hibrido(consulta: str, docs: Dict[str, str], top: int = 3) -> List[str]:
    lex = [d for d, _ in BM25(docs).ranking(consulta)]
    vet = [d for d, _ in ranking_vetorial(consulta, docs)]
    return [d for d, _ in rrf([lex, vet])][:top]


def recall_at_k(recuperados: Sequence[str], relevantes: Sequence[str], k: int) -> float:
    rel = set(relevantes)
    return len(set(recuperados[:k]) & rel) / len(rel) if rel else 1.0


def mrr(recuperados: Sequence[str], relevantes: Sequence[str]) -> float:
    # EXERCICIO-INICIO: 1/posição do primeiro documento relevante; 0.0 se nenhum.
    for pos, d in enumerate(recuperados, start=1):
        if d in relevantes:
            return 1.0 / pos
    return 0.0
    # EXERCICIO-FIM


def ndcg_at_k(recuperados: Sequence[str], relevantes: Sequence[str], k: int) -> float:
    # EXERCICIO-INICIO: DCG = soma de 1/log2(pos + 1) dos relevantes no top-k, dividido pelo DCG ideal; 0.0 sem ideal.
    dcg = sum(1.0 / math.log2(p + 1) for p, d in enumerate(recuperados[:k], start=1) if d in relevantes)
    ideal = sum(1.0 / math.log2(p + 1) for p in range(1, min(k, len(relevantes)) + 1))
    return dcg / ideal if ideal else 0.0
    # EXERCICIO-FIM


def responder_com_fontes(consulta: str, docs: Dict[str, str], cliente: ClienteMockDeterministico) -> Dict[str, object]:
    """Gera resposta ancorada e confere se as citações [POL-xx] vieram da recuperação."""
    ids = buscar_hibrido(consulta, docs)
    contexto = "\n".join(f"[{d}] {docs[d]}" for d in ids)
    resp = cliente.completar(f"Pergunta: {consulta}\nTrechos:\n{contexto}", sistema="Cite os trechos usados entre colchetes.")
    citados = re.findall(r"\[(POL-\d+)\]", resp.texto)
    return {"recuperados": ids, "citados": citados, "fiel": bool(citados) and set(citados) <= set(ids), "texto": resp.texto}
