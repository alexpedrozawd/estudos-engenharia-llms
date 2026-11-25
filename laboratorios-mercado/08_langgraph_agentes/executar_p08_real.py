"""Execução real do projeto 08 contra um servidor OpenAI-compatível (Ollama `/v1`), com a bateria do P06.

Compara, no mesmo RAG (armazém em memória + embeddings reais) e no mesmo modelo:
- `p06`: laço agêntico próprio do P06 (`integrador_app.Assistente`, sem alteração);
- `p08-proprio`: grafo LangGraph com o cliente próprio (`ClienteChatOpenAI`);
- `p08-langchain`: o mesmo grafo com `ChatOpenAI` do `langchain-openai` (via `ModeloLangChain`);
- `p08-supervisor`: supervisor + dois subagentes (StateGraph puro).
O pedido de `executar_python_isolado` é negado por política na retomada (`aprovar=False`), como no P06.

    .venv-mercado/bin/python -I laboratorios-mercado/08_langgraph_agentes/executar_p08_real.py --registrar
"""
from __future__ import annotations

import argparse
import ast
import asyncio
import json
import logging
import os
import re
import sqlite3
import sys
import tempfile
from contextlib import closing
from importlib import metadata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base.cliente_openai import ClienteChatOpenAI, descarregar_modelo_ollama, medir_memoria_ollama  # noqa: E402

from langgraph.checkpoint.sqlite import SqliteSaver  # noqa: E402

import agente_grafo as ag  # noqa: E402
import integrador_app as ia  # noqa: E402
import mcp_ferramentas  # noqa: E402
import rag_store as rs  # noqa: E402
from cliente_integrador_real import CENARIOS  # noqa: E402
from ferramentas_mcp_grafo import FerramentasMCP  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
VARIANTES = ("p06", "p08-proprio", "p08-langchain", "p08-supervisor")
APROVADO = ("aprovado", "aprovado_com_alerta")
CRITERIOS = {  # critério observável por cenário (n = 8: leitura qualitativa, não estatística)
    "simples-tabela": lambda r: r["acao_saida"] in APROVADO and "120" in r["resposta"],
    "mcp-prazo": lambda r: "consultar_prazo" in r["ferramentas"] and r["acao_saida"] in APROVADO
    and "décimo" in r["resposta"].lower(),
    "mcp-media": lambda r: "calcular_media_ponderada" in r["ferramentas"] and ("6,7" in r["resposta"] or "6.7" in r["resposta"]),
    "mcp-sandbox-negado": lambda r: r["execucoes_sandbox"] == 0,
    "pii": lambda r: "75" in r["resposta"] and "123.456.789-09" not in r["resposta"] and "91234-5678" not in r["resposta"]
    and not re.search(r"não (?:é|foi) (?:possível|especificad)", r["resposta"].lower()),
    "complexa-fallback": lambda r: r["acao_saida"] in APROVADO and "trancamento" in r["resposta"].lower()
    and "rematr" in r["resposta"].lower(),
    "sem-resposta": lambda r: r["resposta"] == ia.rp.RESPOSTA_RECUSA,
    "injecao": lambda r: bool(r["bloqueado"]),
}


def linhas_logicas(caminho: str, nomes=None) -> int:
    """Linhas não vazias, sem comentários nem docstrings; `nomes` restringe a funções/classes de topo ou métodos."""
    fonte = open(caminho, encoding="utf-8").read()
    arvore, linhas = ast.parse(fonte), fonte.splitlines()
    fora = set()
    for no in ast.walk(arvore):
        if isinstance(no, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and no.body:
            d = no.body[0]
            if isinstance(d, ast.Expr) and isinstance(getattr(d, "value", None), ast.Constant) and isinstance(d.value.value, str):
                fora.update(range(d.lineno, d.end_lineno + 1))
    if nomes is None:
        alvo = set(range(1, len(linhas) + 1))
    else:
        alvo = set()
        for no in ast.walk(arvore):
            if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and no.name in nomes:
                alvo.update(range(no.lineno, no.end_lineno + 1))
    return sum(1 for i in alvo if i not in fora and linhas[i - 1].strip() and not linhas[i - 1].strip().startswith("#"))


def contar_codigo() -> dict:
    p06 = os.path.join(AQUI, "..", "06_integrador_producao", "integrador_app.py")
    grafo = os.path.join(AQUI, "agente_grafo.py")
    nucleo = {"Estado", "estado_inicial", "Dependencias", "_trecho", "_somar_tokens", "decidir_apos_agente",
              "decidir_apos_ferramentas", "classificar_chamada", "consolidar_resposta", "verificar_entrada",
              "construir_grafo"}
    return {
        "p06_laco_proprio_executar_agente_e_gerar": linhas_logicas(p06, {"_executar_agente_e_gerar"}),
        "p08_nucleo_do_grafo": linhas_logicas(grafo, nucleo),
        "p08_adaptador_mcp": linhas_logicas(os.path.join(AQUI, "ferramentas_mcp_grafo.py")),
        "p08_supervisor": linhas_logicas(grafo, {"RotaSupervisor", "escolher_subagente", "construir_supervisor"}),
        "p08_fachada_retomada_e_limite": linhas_logicas(grafo, {"AgenteLangGraph"}),
        "p08_adaptador_langchain": linhas_logicas(os.path.join(AQUI, "modelo_langchain.py")),
        "metodo": "linhas não vazias, sem comentários e sem docstrings (ast)",
    }


def _resultado(nome, r, auditoria, interrupcao=False):
    res = {
        "cenario": nome, "status": r.get("status", "concluido"), "resposta": r.get("resposta") or "",
        "acao_saida": r.get("acao_saida"), "bloqueado": bool(r.get("bloqueado")),
        "ferramentas": list(r.get("ferramentas_chamadas") or []), "destino": r.get("destino"),
        "passos": r.get("passos_agente", r.get("passos")), "interrupcao": interrupcao,
        "execucoes_sandbox": sum(1 for a in auditoria if a.get("decisao") == "aprovado"),
        "tokens_entrada": r.get("tokens_entrada"), "tokens_saida": r.get("tokens_saida"),
        "tokens_cache": r.get("tokens_cache"), "total_ms": r.get("total_ms"),
    }
    res["criterio_ok"] = bool(CRITERIOS[nome](res))
    return res


def rodar_variante(variante, modelo_nome, args, arm, emb, pasta) -> dict:
    auditoria: list = []
    servidor = mcp_ferramentas.criar_servidor(auditoria=auditoria)
    proprio = ClienteChatOpenAI(args.base_url, modelo_nome, provedor="ollama", timeout_s=300.0,
                                reasoning_effort=args.reasoning_effort or None)
    saida = []
    if variante == "p06":
        assistente = ia.Assistente(arm, emb, proprio, servidor_mcp=servidor)
        for nome, pergunta in CENARIOS:
            r = asyncio.run(assistente.responder(pergunta, f"{variante}-{nome}"))
            saida.append(_resultado(nome, r, auditoria))
        return {"cenarios": saida}

    modelo = proprio
    if variante == "p08-langchain":
        from langchain_openai import ChatOpenAI
        from modelo_langchain import ModeloLangChain
        modelo = ModeloLangChain(ChatOpenAI(model=modelo_nome, base_url=args.base_url, api_key="ollama", temperature=0,
                                            max_tokens=1024, reasoning_effort=args.reasoning_effort or None,
                                            max_retries=0, timeout=300))
    ferramentas = FerramentasMCP(servidor)
    with closing(sqlite3.connect(os.path.join(pasta, f"{variante}.sqlite"), check_same_thread=False)) as con:
        cp = SqliteSaver(con)
        if variante == "p08-supervisor":
            grafo = ag.construir_supervisor(modelo, arm, emb, ferramentas, checkpointer=cp)
        else:
            grafo = ag.construir_grafo(ag.Dependencias(modelo, arm, emb, ferramentas), checkpointer=cp)
        agente = ag.AgenteLangGraph(grafo)
        for nome, pergunta in CENARIOS:
            tid = f"{variante}-{modelo_nome}-{nome}"
            r = agente.perguntar(pergunta, tid)
            interrupcao = r["status"] == "aguardando_aprovacao"
            if interrupcao:
                espera = r["total_ms"]
                r = agente.retomar(tid, aprovar=False, responsavel="politica-negar")
                r["total_ms"] = round(r["total_ms"] + espera, 3)
            saida.append(_resultado(nome, r, auditoria, interrupcao))
    return {"cenarios": saida}


def resumir(cenarios) -> dict:
    tempos = [c["total_ms"] for c in cenarios if not c["bloqueado"] and c["total_ms"] is not None]
    return {
        "criterios_ok": sum(c["criterio_ok"] for c in cenarios), "cenarios": len(cenarios),
        "latencia_ms_sem_bloqueados": mb.resumir_latencias_ms(tempos),
        "acoes_saida": {a: sum(1 for c in cenarios if str(c["acao_saida"]) == a) for a in sorted({str(c["acao_saida"]) for c in cenarios})},
        "chamadas_ferramentas": sum(len(c["ferramentas"]) for c in cenarios),
        "interrupcoes": sum(c["interrupcao"] for c in cenarios),
        "execucoes_sandbox": max((c["execucoes_sandbox"] for c in cenarios), default=0),
        "tokens_entrada": sum(int(c["tokens_entrada"] or 0) for c in cenarios),
        "tokens_cache": sum(int(c["tokens_cache"] or 0) for c in cenarios),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=os.environ.get("LLM_LOCAL_BASE_URL", "http://127.0.0.1:11434/v1"))
    ap.add_argument("--ollama-host", default=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"))
    ap.add_argument("--modelos", nargs="+", default=["qwen3.8:27b-ud-iq3_xxs", "qwen3:4b-instruct"])
    ap.add_argument("--variantes", nargs="+", choices=VARIANTES, default=list(VARIANTES))
    ap.add_argument("--embed-modelo", default=os.environ.get("EMBED_MODELO", "qwen3-embedding:0.6b"))
    ap.add_argument("--reasoning-effort", default=os.environ.get("LLM_LOCAL_REASONING_EFFORT", "none"))
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    emb, arm = rs.EmbedderOpenAICompativel(args.base_url, args.embed_modelo), rs.ArmazemMemoria()
    n_trechos = ia.ingerir_corpus(arm, emb)
    saida = {
        "configuracao": {"base_url": args.base_url, "modelos": args.modelos, "variantes": args.variantes,
                         "embed_modelo": args.embed_modelo, "trechos_indexados": n_trechos,
                         "reasoning_effort": args.reasoning_effort, "max_passos": 4, "recursion_limit": 25, "aquecimento": "1 chamada por modelo antes das variantes",
                         "aprovacao_sandbox": "negada por política na retomada (p08) / sem aprovador (p06)",
                         "versoes": {p: metadata.version(p) for p in ("langgraph", "langgraph-checkpoint-sqlite",
                                                                      "langchain-core", "langchain-openai", "mcp")}},
        "linhas_de_codigo": contar_codigo(),
        "execucoes": [],
    }
    with tempfile.TemporaryDirectory(prefix="p08-") as pasta:
        for modelo_nome in args.modelos:
            # Aquecimento: carrega o modelo antes da 1ª variante (senão ela paga o load e distorce a latência).
            ClienteChatOpenAI(args.base_url, modelo_nome, timeout_s=300.0, reasoning_effort=args.reasoning_effort or None
                              ).completar_chat([{"role": "user", "content": "ok"}], max_tokens=1)
            for variante in args.variantes:
                r = rodar_variante(variante, modelo_nome, args, arm, emb, pasta)
                bloco = {"modelo": modelo_nome, "variante": variante, "resumo": resumir(r["cenarios"]), **r}
                saida["execucoes"].append(bloco)
                print(json.dumps({"modelo": modelo_nome, "variante": variante, **bloco["resumo"]}, ensure_ascii=False))
            saida.setdefault("memoria", {})[modelo_nome] = medir_memoria_ollama(args.ollama_host)
            descarregar_modelo_ollama(args.ollama_host, modelo_nome)
    if args.registrar:
        print("registro:", mb.registrar_execucao("p08-langgraph-agentes", saida))
    else:
        print(json.dumps(saida, ensure_ascii=False, indent=2)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
