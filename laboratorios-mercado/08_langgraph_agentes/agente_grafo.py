"""Laço agêntico do P06 portado para um `StateGraph` do LangGraph (projeto 08) — Aurora Educação, proposta didática.

Grafo do agente (um nó por etapa; arestas condicionais em `decidir_apos_agente` e `decidir_apos_ferramentas`):

    START → verificar_entrada ─(bloqueado)→ END
                 │
             recuperar → agente ─(sem chamadas)→ consolidar → verificar_saida → END
                           │  ↑
          (sensível)→ aprovar │   interrupt(): pausa e grava o checkpoint até a decisão humana
                           ↓  │
                        ferramentas ─(passos >= max_passos)→ consolidar

Reaproveita sem alterar: guardrails, `RespostaEstruturada` e conversão MCP → `tools` do P06
(`integrador_app`), RAG do P02, servidor MCP do P03 e `mercado_base` (cliente OpenAI-compatível,
`gerar_estruturado`, PII). O estado só tem tipos JSON (str, int, bool, list, dict) para o checkpointer.

Decisões de projeto:
- Sem redutor de lista: cada nó devolve a lista inteira. Com `operator.add`, um subgrafo usado como nó
  devolve o estado completo e o pai soma de novo o que já tinha (mensagens duplicadas; ver README).
- `aprovar` não faz nada antes do `interrupt()` além de montar o pedido (idempotente: o nó roda de novo
  desde o início na retomada) e não envolve o `interrupt()` em try/except.
- Ferramenta sensível sem aprovação deste `id` não executa: a mensagem `tool` diz que foi negada
  (não se finge sucesso). Ferramenta fora da lista permitida também não executa.
- `recursion_limit` estourado vira recusa segura em `AgenteLangGraph`, nunca exceção para o cliente.
- `AgenteLangGraph.perguntar` mascara a PII antes do `invoke`: o 1º checkpoint grava a entrada como chegou,
  e o histórico não é reescrito pelos nós. Quem chamar `grafo.invoke` direto deve mascarar antes.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, TypedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base  # noqa: E402,F401  (prepara sys.path dos projetos)
from mercado_base.cliente_openai import gerar_estruturado  # noqa: E402
from mercado_base.pii import mascarar_pii  # noqa: E402

from langgraph.errors import GraphRecursionError  # noqa: E402
from langgraph.graph import END, START, StateGraph  # noqa: E402
from langgraph.types import Command, interrupt  # noqa: E402
from pydantic import BaseModel  # noqa: E402

import integrador_app as ia  # noqa: E402
import rag_ingestao as ing  # noqa: E402
import rag_pipeline as rp  # noqa: E402
import rag_store as rs  # noqa: E402
from ferramentas_mcp_grafo import FerramentasMCP  # noqa: E402

RESPOSTA_BLOQUEIO = "Não posso atender a esse pedido."


class Estado(TypedDict, total=False):
    pergunta: str
    perfil: str
    texto: str
    pii: List[str]
    bloqueado: bool
    motivo: str
    destino: str
    trechos: List[Dict[str, object]]
    mensagens: List[Dict[str, object]]
    pendentes: List[Dict[str, object]]
    aprovacao: Dict[str, object]
    decisoes_humanas: List[Dict[str, object]]
    ferramentas_chamadas: List[str]
    passos: int
    resposta: str
    acao_saida: Optional[str]
    fidelidade: float
    confianca: str
    reparos_estruturado: int
    falha_esquema: bool
    tokens_entrada: int
    tokens_saida: int
    tokens_cache: int


def estado_inicial(pergunta: str, perfil: str = "aluno") -> Estado:
    """Zera as chaves de cada pergunta (o checkpoint do `thread_id` guarda o estado anterior)."""
    return Estado(
        pergunta=pergunta, perfil=perfil, texto="", pii=[], bloqueado=False, motivo="", destino="",
        trechos=[], mensagens=[], pendentes=[], aprovacao={}, decisoes_humanas=[], ferramentas_chamadas=[],
        passos=0, resposta="", acao_saida=None, fidelidade=0.0, confianca="", reparos_estruturado=0,
        falha_esquema=False, tokens_entrada=0, tokens_saida=0, tokens_cache=0,
    )


@dataclass
class Dependencias:
    modelo: object  # expõe `completar_chat` (ClienteChatOpenAI, ClienteChatFalso ou ModeloLangChain)
    armazem: object
    embedder: object
    ferramentas: FerramentasMCP
    permitidas: Optional[Set[str]] = None  # None = todas as ferramentas listadas pelo servidor
    k: int = 3
    max_passos: int = 4


def _trecho(d: Dict[str, object]) -> ing.Trecho:
    return ing.Trecho(str(d["id"]), str(d["doc"]), int(d["pagina"]), str(d["tipo"]), str(d["texto"]))


def _somar_tokens(estado: Estado, entrada: int, saida: int, cache: int) -> Dict[str, int]:
    return {
        "tokens_entrada": int(estado.get("tokens_entrada") or 0) + int(entrada),
        "tokens_saida": int(estado.get("tokens_saida") or 0) + int(saida),
        "tokens_cache": int(estado.get("tokens_cache") or 0) + int(cache),
    }


def decidir_apos_agente(estado: Estado, sensiveis: Set[str]) -> str:
    """Aresta condicional depois do nó `agente`."""
    # EXERCICIO-INICIO: sem chamadas pendentes vá para "consolidar"; se alguma for sensível, "aprovar" (interrupt); senão "ferramentas".
    pendentes = estado.get("pendentes") or []
    if not pendentes:
        return "consolidar"
    if any(p["nome"] in sensiveis for p in pendentes):
        return "aprovar"
    return "ferramentas"
    # EXERCICIO-FIM


def decidir_apos_ferramentas(estado: Estado, max_passos: int) -> str:
    return "consolidar" if int(estado.get("passos") or 0) >= max(1, int(max_passos)) else "agente"


def classificar_chamada(chamada: Dict[str, object], permitidas: Set[str], sensiveis: Set[str],
                        aprovacao: Dict[str, object]) -> str:
    """Política de execução de uma chamada de ferramenta pedida pelo modelo."""
    # EXERCICIO-INICIO: fora da lista permitida = "nao_permitida"; JSON inválido = "erro_argumentos"; sensível sem aprovação humana deste id = "negada_humano"; senão "executar".
    if chamada["nome"] not in permitidas:
        return "nao_permitida"
    if chamada.get("erro_json"):
        return "erro_argumentos"
    aprovada = aprovacao.get("aprovar") is True and chamada["id"] in (aprovacao.get("ids") or [])
    if chamada["nome"] in sensiveis and not aprovada:
        return "negada_humano"
    return "executar"
    # EXERCICIO-FIM


def consolidar_resposta(modelo, pergunta: str, trechos: List[ing.Trecho]) -> Dict[str, object]:
    """Resposta final em JSON validado (`RespostaEstruturada` do P06), com reparo e degradação segura."""
    mensagens = [
        {"role": "system", "content": ia.SISTEMA_AGENTE},
        {
            "role": "user",
            "content": (
                rp.montar_prompt(pergunta, trechos)
                + "\n\nResponda de forma objetiva (até 180 palavras) e exclusivamente em JSON no esquema exigido "
                "(`resposta`, `citacoes`, `recusa`, `confianca`). "
                "Cite os rótulos exatamente como [T1], [T2] tanto no texto de `resposta` quanto em `citacoes` "
                "(ex.: [\"[T1]\"])."
            ),
        },
    ]
    try:
        est, meta = gerar_estruturado(modelo, mensagens, ia.RespostaEstruturada, max_reparos=2, max_tokens=1024)
    except ValueError:
        return {"resposta": rp.RESPOSTA_RECUSA, "confianca": "baixa", "reparos": 2, "falha_esquema": True,
                "tokens": (0, 0, 0)}
    if est.recusa:
        texto = rp.RESPOSTA_RECUSA
    else:
        texto = est.resposta.strip()
        validos = {f"[T{i}]" for i in range(1, len(trechos) + 1)}
        extras: List[str] = []
        for c in est.citacoes:
            m = re.fullmatch(r"\s*\[?\s*T?(\d+)\s*\]?\s*", str(c))
            tag = f"[T{m.group(1)}]" if m else ""
            if tag in validos and tag not in texto and tag not in extras:
                extras.append(tag)
        if extras:
            texto = f"{texto} {' '.join(extras)}"
    return {"resposta": texto, "confianca": est.confianca, "reparos": int(meta["reparos"]), "falha_esquema": False,
            "tokens": (int(meta["tokens_entrada"]), int(meta["tokens_saida"]), int(meta["tokens_cache"]))}


def verificar_entrada(estado: Estado) -> Dict[str, object]:
    """Nó de guardrail de entrada (injeção e PII do P06); comum ao agente e ao supervisor."""
    ent = ia.verificar_entrada(estado["pergunta"])
    if ent["bloqueado"]:
        return {"bloqueado": True, "motivo": ent["motivo"], "texto": "", "pii": [], "resposta": RESPOSTA_BLOQUEIO}
    pii = list(estado.get("pii") or [])  # tipos já detectados na fachada, antes do checkpoint
    return {"bloqueado": False, "motivo": "", "texto": ent["texto"], "pii": pii + [p for p in ent["pii"] if p not in pii]}


def construir_grafo(deps: Dependencias, *, checkpointer=None, guarda_entrada: bool = True):
    """Compila o grafo do agente. Sem `checkpointer`, um subgrafo herda o do grafo pai."""
    permitidas = set(deps.ferramentas.nomes if deps.permitidas is None else deps.permitidas) & deps.ferramentas.nomes
    sensiveis = deps.ferramentas.sensiveis & permitidas
    tools = deps.ferramentas.tools_para(permitidas)

    def recuperar(estado: Estado) -> Dict[str, object]:
        texto = estado.get("texto") or estado["pergunta"]
        filtro = rs.FiltroBusca(perfil=estado.get("perfil") or "aluno", apenas_vigentes=True)
        rec = rp.recuperar(texto, deps.armazem, deps.embedder, k=deps.k, filtro=filtro)
        trechos = [{"id": t.id, "doc": t.doc, "pagina": t.pagina, "tipo": t.tipo, "texto": t.texto} for t in rec.trechos]
        mensagens = [
            {"role": "system", "content": ia.SISTEMA_AGENTE},
            {"role": "user", "content": rp.montar_prompt(texto, rec.trechos)},
        ]
        return {"trechos": trechos, "mensagens": mensagens, "passos": 0, "pendentes": [], "aprovacao": {}}

    def agente(estado: Estado) -> Dict[str, object]:
        resp = deps.modelo.completar_chat(estado["mensagens"], tools=tools or None,
                                          tool_choice="auto" if tools else None, max_tokens=512)
        saida: Dict[str, object] = {"passos": int(estado.get("passos") or 0) + 1,
                                    **_somar_tokens(estado, resp.tokens_entrada, resp.tokens_saida, resp.tokens_cache)}
        if not resp.chamadas_ferramentas:
            saida["pendentes"] = []
            return saida
        pendentes = [{"id": tc.id, "nome": tc.nome, "argumentos": dict(tc.argumentos), "erro_json": tc.erro_json}
                     for tc in resp.chamadas_ferramentas]
        assistente = {
            "role": "assistant",
            "content": resp.conteudo or "",
            "tool_calls": [{"id": tc.id, "type": "function",
                            "function": {"name": tc.nome,
                                         "arguments": tc.argumentos_brutos or json.dumps(tc.argumentos, ensure_ascii=False)}}
                           for tc in resp.chamadas_ferramentas],
        }
        saida.update(pendentes=pendentes, mensagens=list(estado["mensagens"]) + [assistente])
        return saida

    def aprovar(estado: Estado) -> Dict[str, object]:
        # Antes do interrupt: só leitura do estado (o nó roda de novo, do início, na retomada).
        pedido = [{"id": p["id"], "nome": p["nome"], "argumentos": p["argumentos"]}
                  for p in estado.get("pendentes") or [] if p["nome"] in sensiveis]
        decisao = interrupt({"tipo": "aprovacao_de_ferramenta", "chamadas": pedido})
        aprovado = isinstance(decisao, dict) and decisao.get("aprovar") is True
        responsavel = str(decisao.get("responsavel", "")) if isinstance(decisao, dict) else ""
        registro = {"ids": [p["id"] for p in pedido], "aprovar": aprovado, "responsavel": responsavel or "não informado"}
        return {"aprovacao": registro, "decisoes_humanas": list(estado.get("decisoes_humanas") or []) + [registro]}

    def ferramentas(estado: Estado) -> Dict[str, object]:
        aprovacao = estado.get("aprovacao") or {}
        pendentes = estado.get("pendentes") or []
        politicas = [classificar_chamada(p, permitidas, sensiveis, aprovacao) for p in pendentes]
        # Sensível só chega a "executar" se aprovada neste turno; só ela tem a elicitation do servidor aceita.
        lote = [(p["nome"], p["argumentos"], p["nome"] in sensiveis) for p, pol in zip(pendentes, politicas) if pol == "executar"]
        resultados = iter(deps.ferramentas.executar_lote(lote) if lote else [])
        mensagens = list(estado["mensagens"])
        trechos = list(estado.get("trechos") or [])
        chamadas = list(estado.get("ferramentas_chamadas") or [])
        erros = {"nao_permitida": "ferramenta não permitida para este agente",
                 "negada_humano": "negada pelo revisor humano; a ferramenta NÃO foi executada"}
        for p, pol in zip(pendentes, politicas):
            if pol != "executar":
                erro = erros.get(pol) or p.get("erro_json") or pol
                mensagens.append({"role": "tool", "tool_call_id": p["id"],
                                  "content": json.dumps({"erro": erro}, ensure_ascii=False)})
                continue
            texto, sucesso = next(resultados)
            chamadas.append(p["nome"])
            if sucesso:
                trechos.insert(0, {
                    "id": f"mcp:{p['nome']}:{len(chamadas)}", "doc": f"ferramenta-mcp:{p['nome']}", "pagina": 0,
                    "tipo": "ferramenta",
                    "texto": f"Resultado oficial de {p['nome']}({json.dumps(p['argumentos'], ensure_ascii=False)}): {texto}",
                })
            mensagens.append({"role": "tool", "tool_call_id": p["id"], "content": texto})
        return {"mensagens": mensagens, "trechos": trechos, "ferramentas_chamadas": chamadas,
                "pendentes": [], "aprovacao": {}}

    def consolidar(estado: Estado) -> Dict[str, object]:
        trechos = [_trecho(t) for t in estado.get("trechos") or []]
        r = consolidar_resposta(deps.modelo, estado.get("texto") or estado["pergunta"], trechos)
        return {"resposta": r["resposta"], "confianca": r["confianca"], "reparos_estruturado": r["reparos"],
                "falha_esquema": r["falha_esquema"], **_somar_tokens(estado, *r["tokens"])}

    def verificar_saida(estado: Estado) -> Dict[str, object]:
        saida = ia.verificar_saida(estado.get("resposta") or "", [_trecho(t) for t in estado.get("trechos") or []])
        acao = "falha_esquema_estruturado" if estado.get("falha_esquema") else saida["acao"]
        return {"resposta": saida["texto"], "acao_saida": acao, "fidelidade": float(saida["fidelidade"]["fidelidade"])}

    g = StateGraph(Estado)
    if guarda_entrada:
        g.add_node("verificar_entrada", verificar_entrada)
    for nome, fn in (("recuperar", recuperar), ("agente", agente), ("aprovar", aprovar),
                     ("ferramentas", ferramentas), ("consolidar", consolidar), ("verificar_saida", verificar_saida)):
        g.add_node(nome, fn)
    if guarda_entrada:
        g.add_edge(START, "verificar_entrada")
        g.add_conditional_edges("verificar_entrada", lambda e: END if e.get("bloqueado") else "recuperar",
                                ["recuperar", END])
    else:
        g.add_edge(START, "recuperar")
    g.add_edge("recuperar", "agente")
    g.add_conditional_edges("agente", lambda e: decidir_apos_agente(e, sensiveis),
                            ["consolidar", "aprovar", "ferramentas"])
    g.add_edge("aprovar", "ferramentas")
    g.add_conditional_edges("ferramentas", lambda e: decidir_apos_ferramentas(e, deps.max_passos),
                            ["consolidar", "agente"])
    g.add_edge("consolidar", "verificar_saida")
    g.add_edge("verificar_saida", END)
    return g.compile(checkpointer=checkpointer)


# ---------- supervisor com dois subagentes (StateGraph puro, sem langgraph-supervisor) ----------

PAPEIS: Dict[str, Set[str]] = {
    "academico": {"consultar_prazo"},
    "calculo": {"calcular_media_ponderada", "executar_python_isolado"},
}
SISTEMA_SUPERVISOR = (
    "Você encaminha perguntas de alunos da Aurora Educação (instituição fictícia). Escolha `academico` para "
    "prazos, regras, taxas e documentos; escolha `calculo` para médias, notas ou execução de código. "
    "Responda só em JSON com `destino` e `motivo`."
)


class RotaSupervisor(BaseModel):
    destino: str
    motivo: str = ""


def escolher_subagente(modelo, texto: str, destinos: List[str]) -> Dict[str, object]:
    """Classifica a pergunta; destino inválido ou JSON irreparável cai no primeiro subagente (fallback)."""
    mensagens = [{"role": "system", "content": SISTEMA_SUPERVISOR + f" Destinos válidos: {', '.join(destinos)}."},
                 {"role": "user", "content": texto}]
    # EXERCICIO-INICIO: gere RotaSupervisor com gerar_estruturado (max_reparos=1); JSON irreparável ou destino fora da lista = destinos[0] com motivo "fallback: ...".
    try:
        rota, meta = gerar_estruturado(modelo, mensagens, RotaSupervisor, max_reparos=1, max_tokens=128)
    except ValueError:
        return {"destino": destinos[0], "motivo": "fallback: classificação irreparável", "tokens": (0, 0, 0)}
    tokens = (int(meta["tokens_entrada"]), int(meta["tokens_saida"]), int(meta["tokens_cache"]))
    if rota.destino not in destinos:
        return {"destino": destinos[0], "motivo": f"fallback: destino inválido ({rota.destino[:40]})", "tokens": tokens}
    return {"destino": rota.destino, "motivo": rota.motivo[:200], "tokens": tokens}
    # EXERCICIO-FIM


def construir_supervisor(modelo, armazem, embedder, ferramentas: FerramentasMCP, *, checkpointer=None,
                         papeis: Optional[Dict[str, Set[str]]] = None, max_passos: int = 4):
    """Guardrail de entrada → supervisor → um subagente (subgrafo com ferramentas próprias) → END.

    Cada subagente só recebe as ferramentas do seu papel (menor privilégio) e devolve o resultado ao
    grafo pai, não ao usuário. Os subgrafos herdam o checkpointer do pai (interrupt funciona dentro deles).
    """
    papeis = papeis or PAPEIS
    destinos = list(papeis)

    def supervisor(estado: Estado) -> Dict[str, object]:
        r = escolher_subagente(modelo, estado.get("texto") or estado["pergunta"], destinos)
        return {"destino": r["destino"], "motivo": r["motivo"], **_somar_tokens(estado, *r["tokens"])}

    g = StateGraph(Estado)
    g.add_node("verificar_entrada", verificar_entrada)
    g.add_node("supervisor", supervisor)
    for nome, ferramentas_do_papel in papeis.items():
        deps = Dependencias(modelo, armazem, embedder, ferramentas, permitidas=set(ferramentas_do_papel),
                            max_passos=max_passos)
        g.add_node(nome, construir_grafo(deps, guarda_entrada=False))
    g.add_edge(START, "verificar_entrada")
    g.add_conditional_edges("verificar_entrada", lambda e: END if e.get("bloqueado") else "supervisor",
                            ["supervisor", END])
    g.add_conditional_edges("supervisor", lambda e: e["destino"], destinos)
    for nome in destinos:
        g.add_edge(nome, END)
    return g.compile(checkpointer=checkpointer)


# ---------- fachada: perguntar, retomar e degradação segura ----------

@dataclass
class AgenteLangGraph:
    grafo: object
    recursion_limit: int = 25

    def perguntar(self, pergunta: str, thread_id: str, *, perfil: str = "aluno") -> Dict[str, object]:
        # O checkpointer grava a entrada antes do 1º nó: a PII sai aqui, não em `verificar_entrada`.
        mascarada, pii = mascarar_pii(pergunta)
        return self._rodar({**estado_inicial(mascarada, perfil), "pii": pii}, thread_id)

    def retomar(self, thread_id: str, *, aprovar: bool, responsavel: str) -> Dict[str, object]:
        return self._rodar(Command(resume={"aprovar": bool(aprovar), "responsavel": responsavel}), thread_id)

    def _rodar(self, entrada, thread_id: str) -> Dict[str, object]:
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": int(self.recursion_limit)}
        t0 = time.perf_counter()
        try:
            out = self.grafo.invoke(entrada, config)
        except GraphRecursionError:
            return {"status": "limite_de_passos", "thread_id": thread_id, "resposta": rp.RESPOSTA_RECUSA,
                    "acao_saida": "recusa_limite_de_passos", "ferramentas_chamadas": [],
                    "total_ms": round((time.perf_counter() - t0) * 1000, 3)}
        base = {
            "thread_id": thread_id,
            "total_ms": round((time.perf_counter() - t0) * 1000, 3),
            **{k: out.get(k) for k in ("resposta", "acao_saida", "bloqueado", "motivo", "pii", "destino", "passos",
                                       "ferramentas_chamadas", "decisoes_humanas", "fidelidade", "confianca",
                                       "reparos_estruturado", "tokens_entrada", "tokens_saida", "tokens_cache")},
            "trechos": [t["id"] for t in out.get("trechos") or []],
        }
        interrupcoes = out.get("__interrupt__") or ()
        if interrupcoes:
            return {**base, "status": "aguardando_aprovacao", "pedido": interrupcoes[0].value,
                    "resposta": None, "acao_saida": None}
        return {**base, "status": "concluido"}
