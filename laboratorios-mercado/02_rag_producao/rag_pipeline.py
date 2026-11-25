"""Recuperação híbrida, reordenação, geração com citações e avaliação (projeto 02).

Fluxo: busca vetorial + lexical → fusão RRF → *reranker* → prompt com trechos numerados
`[T1]..[Tn]` → resposta → métricas de recuperação (recall@k, MRR, nDCG@k) e de
fidelidade (frases apoiadas no contexto citado e citações válidas).
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence

from rag_ingestao import Trecho
from rag_store import FiltroBusca, termos


def fusao_rrf(listas: Sequence[Sequence[tuple]], k: int = 60) -> List[tuple]:
    """Reciprocal Rank Fusion: soma 1/(k + posição) de cada lista; desempate por id."""
    # EXERCICIO-INICIO: RRF por id de trecho: soma de 1/(k + posição); ordene por nota decrescente e id.
    pontos: Dict[str, float] = {}
    trechos: Dict[str, Trecho] = {}
    for lista in listas:
        for pos, (t, _) in enumerate(lista, start=1):
            pontos[t.id] = pontos.get(t.id, 0.0) + 1.0 / (k + pos)
            trechos[t.id] = t
    return sorted(((trechos[i], s) for i, s in pontos.items()), key=lambda x: (-x[1], x[0].id))
    # EXERCICIO-FIM


class ReordenadorLexico:
    """Reranker determinístico: cobertura dos termos da pergunta + bônus para tabela com números."""

    nome = "lexico"

    def reordenar(self, pergunta: str, candidatos: Sequence[tuple]) -> List[tuple]:
        q = set(termos(pergunta))
        pede_valor = bool(re.search(r"\b(quanto|taxa|valor|prazo|dias|custa)\b", pergunta.lower()))
        saida = []
        for t, base in candidatos:
            cobertura = len(q & set(termos(t.texto))) / max(len(q), 1)
            bonus = 0.15 if (pede_valor and t.tipo == "tabela") else 0.0
            saida.append((t, round(cobertura + bonus + 0.01 * base, 6)))
        return sorted(saida, key=lambda x: (-x[1], x[0].id))


class ReordenadorLLM:
    """Reranker pontual por LLM (nota 0–3 por trecho). Usa o cliente neutro de `laboratorios/comum`.

    Se a nota não puder ser lida, mantém a posição original (falha segura, sem descartar trecho).
    """

    nome = "llm"

    def __init__(self, cliente, max_candidatos: int = 8):
        self.cliente = cliente
        self.max_candidatos = max_candidatos

    def reordenar(self, pergunta: str, candidatos: Sequence[tuple]) -> List[tuple]:
        saida = []
        for pos, (t, _) in enumerate(candidatos[: self.max_candidatos]):
            r = self.cliente.completar(
                f"Pergunta: {pergunta}\n\nTrecho:\n{t.texto}\n\n"
                "Quão útil é o trecho para responder à pergunta? Responda só com um número de 0 a 3.",
                sistema="Você avalia relevância de trechos para busca. Responda apenas 0, 1, 2 ou 3.",
                temperatura=0.0, max_tokens=4,
            )
            m = re.search(r"[0-3]", r.texto)
            nota = int(m.group()) if m else -1
            saida.append((t, (nota if nota >= 0 else 1.5) - pos * 1e-3))
        saida += [(t, -1.0) for t, _ in candidatos[self.max_candidatos:]]
        return sorted(saida, key=lambda x: (-x[1], x[0].id))


@dataclass
class Recuperacao:
    pergunta: str
    trechos: List[Trecho]
    candidatos_vetoriais: List[str] = field(default_factory=list)
    candidatos_lexicais: List[str] = field(default_factory=list)


def _chamar_busca(fn, arg, k: int, filtro: Optional[FiltroBusca]):
    if filtro is None:
        return fn(arg, k)
    return fn(arg, k, filtro=filtro)


def recuperar(pergunta: str, armazem, embedder, *, k: int = 4, k_candidatos: int = 12,
              reordenador=None, modo: str = "hibrida", filtro: Optional[FiltroBusca] = None) -> Recuperacao:
    if modo not in ("vetorial", "lexical", "hibrida"):
        raise ValueError(f"modo de recuperação inválido: {modo}")
    vet: List[tuple] = []
    lex: List[tuple] = []
    if modo in ("vetorial", "hibrida"):
        vetor = embedder.embutir([pergunta])[0]
        vet = _chamar_busca(armazem.buscar_vetorial, vetor, k_candidatos, filtro)
    if modo in ("lexical", "hibrida"):
        lex = _chamar_busca(armazem.buscar_lexical, pergunta, k_candidatos, filtro)
    if modo == "vetorial":
        fundidos = list(vet)
    elif modo == "lexical":
        fundidos = list(lex)
    else:
        fundidos = fusao_rrf([vet, lex])
    if reordenador is not None:
        fundidos = reordenador.reordenar(pergunta, fundidos)
    return Recuperacao(pergunta, [t for t, _ in fundidos[:k]],
                       [t.id for t, _ in vet], [t.id for t, _ in lex])


SISTEMA_RAG = (
    "Você é o assistente acadêmico da Aurora Educação (instituição fictícia). Responda em português, "
    "usando somente os trechos fornecidos. Cite cada afirmação com o rótulo do trecho, como [T1]. "
    "Se os trechos não bastarem, responda exatamente: Não encontrei essa informação nos documentos."
)


def montar_prompt(pergunta: str, trechos: Sequence[Trecho]) -> str:
    blocos = [f"[T{i}] ({t.doc}, p. {t.pagina}, {t.tipo})\n{t.texto}" for i, t in enumerate(trechos, start=1)]
    return "Trechos:\n\n" + "\n\n".join(blocos) + f"\n\nPergunta: {pergunta}"


def responder(pergunta: str, rec: Recuperacao, cliente, max_tokens: int = 200) -> Dict[str, object]:
    r = cliente.completar(montar_prompt(pergunta, rec.trechos), sistema=SISTEMA_RAG,
                          temperatura=0.0, max_tokens=max_tokens)
    return {"resposta": r.texto.strip(), "tokens_entrada": r.tokens_entrada,
            "tokens_saida": r.tokens_saida, "latencia_ms": r.latencia_ms}


# ---------- avaliação ----------

def recall_em_k(recuperados: Sequence[str], relevantes: Sequence[str], k: int) -> float:
    if not relevantes:
        return 0.0
    return len(set(recuperados[:k]) & set(relevantes)) / len(set(relevantes))


def mrr(recuperados: Sequence[str], relevantes: Sequence[str]) -> float:
    for pos, rid in enumerate(recuperados, start=1):
        if rid in relevantes:
            return 1.0 / pos
    return 0.0


def ndcg_em_k(recuperados: Sequence[str], relevantes: Sequence[str], k: int) -> float:
    dcg = sum(1.0 / math.log2(p + 1) for p, rid in enumerate(recuperados[:k], start=1) if rid in relevantes)
    ideal = sum(1.0 / math.log2(p + 1) for p in range(1, min(len(relevantes), k) + 1))
    return dcg / ideal if ideal else 0.0


RESPOSTA_RECUSA = "Não encontrei essa informação nos documentos."


def fidelidade(resposta: str, trechos: Sequence[Trecho], limiar: float = 0.6) -> Dict[str, object]:
    """Fração de frases apoiadas: ≥ `limiar` dos termos da frase aparecem nos trechos citados.

    Métrica lexical e conservadora (não detecta paráfrase); serve de portão barato antes de
    avaliadores por LLM ou humanos.
    """
    # EXERCICIO-INICIO: recusa padrão = fidelidade 1; divida em frases, cole citações soltas na anterior; apoiada = cita [Tn] recuperado; liste citações inválidas.
    if resposta.strip() == RESPOSTA_RECUSA:
        return {"frases": 0, "apoiadas": 0, "fidelidade": 1.0, "citacoes_invalidas": [], "recusa": True}
    frases: List[str] = []
    for f in (x.strip() for x in re.split(r"(?<=[.!?])\s+", resposta)):
        if not f:
            continue
        if frases and re.fullmatch(r"(\[T\d+\]\s*)+[.!?]?", f):
            frases[-1] = f"{frases[-1]} {f}"  # citação depois do ponto pertence à frase anterior
        else:
            frases.append(f)
    invalidas, apoiadas = set(), 0
    for frase in frases:
        citadas = [int(n) for n in re.findall(r"\[T(\d+)\]", frase)]
        invalidas.update(n for n in citadas if not 1 <= n <= len(trechos))
        validas = [trechos[n - 1] for n in citadas if 1 <= n <= len(trechos)]
        tf = set(termos(re.sub(r"\[T\d+\]", "", frase)))
        if not tf:
            apoiadas += 1
            continue
        if not validas:  # frase sem citação válida não conta como apoiada
            continue
        contexto = set().union(*(set(termos(t.texto)) for t in validas))
        if len(tf & contexto) / len(tf) >= limiar:
            apoiadas += 1
    return {
        "frases": len(frases), "apoiadas": apoiadas,
        "fidelidade": round(apoiadas / len(frases), 3) if frases else 0.0,
        "citacoes_invalidas": sorted(invalidas), "recusa": False,
    }
    # EXERCICIO-FIM


def resolver_relevantes(trechos: Sequence[Trecho], criterios: Sequence[Dict[str, object]]) -> List[str]:
    """Converte critérios estáveis (doc, página, texto contido) em ids de trechos da ingestão atual."""
    ids = []
    for c in criterios:
        for t in trechos:
            if t.doc == c["doc"] and t.pagina == int(c["pagina"]) and str(c["contem"]).lower() in t.texto.lower():
                ids.append(t.id)
    return sorted(set(ids))


def _filtro_da_consulta(c: Dict[str, object], padrao: Optional[FiltroBusca]) -> Optional[FiltroBusca]:
    bruto = c.get("filtro")
    if not isinstance(bruto, dict):
        return padrao
    return FiltroBusca(
        perfil=bruto.get("perfil"),
        departamento=bruto.get("departamento"),
        apenas_vigentes=bruto.get("apenas_vigentes"),
        versao=bruto.get("versao"),
        tipo=bruto.get("tipo"),
    )


def avaliar_recuperacao(consultas: Sequence[Dict[str, object]], armazem, embedder, *, k: int = 4,
                        reordenador=None, modo: str = "hibrida",
                        filtro_padrao: Optional[FiltroBusca] = None) -> Dict[str, object]:
    por_consulta = []
    for c in consultas:
        filtro = _filtro_da_consulta(c, filtro_padrao)
        rec = recuperar(str(c["pergunta"]), armazem, embedder, k=k, reordenador=reordenador,
                        modo=modo, filtro=filtro)
        ids = [t.id for t in rec.trechos]
        rel = list(c["relevantes"])
        por_consulta.append({
            "id": c["id"], "recuperados": ids,
            "recall": recall_em_k(ids, rel, k), "mrr": mrr(ids, rel), "ndcg": round(ndcg_em_k(ids, rel, k), 4),
        })
    n = max(len(por_consulta), 1)
    return {
        "k": k,
        "modo": modo,
        "reordenador": getattr(reordenador, "nome", "nenhum"),
        "recall_medio": round(sum(p["recall"] for p in por_consulta) / n, 4),
        "mrr_medio": round(sum(p["mrr"] for p in por_consulta) / n, 4),
        "ndcg_medio": round(sum(p["ndcg"] for p in por_consulta) / n, 4),
        "por_consulta": por_consulta,
    }


def auditar_acl(consultas_acl: Sequence[Dict[str, object]], armazem, embedder, *, k: int = 4,
                perfil_nao_autorizado: str = "aluno") -> Dict[str, object]:
    """Verifica que perfil sem permissão recebe zero trechos de documentos restritos."""
    # EXERCICIO-INICIO: consulte com o perfil sem acesso e conte os trechos de documentos restritos que vazaram.
    detalhes = []
    vazamentos = 0
    filtro = FiltroBusca(perfil=perfil_nao_autorizado, apenas_vigentes=True)
    for c in consultas_acl:
        rec = recuperar(str(c["pergunta"]), armazem, embedder, k=k, modo="hibrida", filtro=filtro)
        restritos = set(c.get("docs_restritos") or ())
        vazados = [
            t.id
            for t in rec.trechos
            if perfil_nao_autorizado not in t.perfis or (restritos and t.doc in restritos)
        ]
        vazamentos += len(vazados)
        detalhes.append({
            "id": c["id"],
            "perfil_testado": perfil_nao_autorizado,
            "trechos_retornados": [t.id for t in rec.trechos],
            "vazados": vazados,
        })
    return {"consultas": len(consultas_acl), "vazamentos": vazamentos, "detalhes": detalhes}
    # EXERCICIO-FIM
