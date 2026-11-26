"""Execução real do projeto 02: PDFs → pgvector → ACL + modos (vetorial, lexical, híbrida RRF, rerankers) → avaliação.

Exemplo:
    PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
    .venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/executar_rag_real.py \
        --embed-base-url http://127.0.0.1:8082/v1 --embed-modelo qwen3-embedding-0.6b \
        --llm-base-url http://127.0.0.1:8081/v1 --llm-modelo qwen3-4b-instruct --registrar
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base import dados_sinteticos as ds  # noqa: E402
from mercado_base import estatistica as est  # noqa: E402
from mercado_base.cliente_openai import ClienteChatComCache, ClienteChatOpenAI, medir_memoria_ollama  # noqa: E402

import corpus_aurora  # noqa: E402
import rag_ingestao as ing  # noqa: E402
import rag_pipeline as rp  # noqa: E402
import rag_store as rs  # noqa: E402


def dividir_selecao_teste(ids, fracao: float, semente: str):
    """Separa perguntas por hash: a seleção escolhe a variante; o teste mede, sem ter influído na escolha."""
    if not 0.0 <= fracao < 1.0:
        raise ValueError("fracao de seleção fora de [0, 1)")
    ordem = sorted(ids, key=lambda i: hashlib.sha256((semente + str(i)).encode()).hexdigest())
    n = round(len(ordem) * fracao)
    return set(ordem[:n]), set(ordem[n:])


def mrr_medio(avaliacao: dict, ids) -> float:
    vals = [p["mrr"] for p in avaliacao["por_consulta"] if p["id"] in ids]
    return round(sum(vals) / len(vals), 4) if vals else 0.0


def estatistica_recuperacao(avaliacoes: dict, escolhida: str, ids=None) -> dict:
    """Acerto@k por pergunta (ao menos um trecho relevante no top-k): Wilson 95% por variante; a escolhida
    contra cada outra com McNemar exato no acerto@k e bootstrap pareado no MRR. Com `ids`, só essas
    perguntas entram (o conjunto de teste, separado do que escolheu a variante)."""
    def consultas(nome):
        return [p for p in avaliacoes[nome]["por_consulta"] if ids is None or p["id"] in ids]

    def acerto(nome):
        return {p["id"]: p["recall"] > 0 for p in consultas(nome)}

    def mrrs(nome):
        return [p["mrr"] for p in consultas(nome)]

    saida = {"acerto_em_k": {}, "escolhida": escolhida, "comparacoes": {}}
    for nome in avaliacoes:
        a = acerto(nome)
        saida["acerto_em_k"][nome] = {"n": len(a), "acertos": sum(a.values()),
                                      "wilson95": est.wilson(sum(a.values()), len(a))}
    for nome in avaliacoes:
        if nome == escolhida:
            continue
        cmp = est.comparar_binario(acerto(nome), acerto(escolhida))
        cmp["bootstrap_mrr"] = est.bootstrap_diferenca(mrrs(nome), mrrs(escolhida))
        saida["comparacoes"][f"{escolhida}_vs_{nome}"] = cmp
    return saida


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dsn", default=os.environ.get("PGVECTOR_DSN", ""))
    ap.add_argument("--embed-base-url", default=os.environ.get("EMBED_BASE_URL", "http://127.0.0.1:8082/v1"))
    ap.add_argument("--embed-modelo", default=os.environ.get("EMBED_MODELO", "embed-local"))
    ap.add_argument("--llm-base-url", default=os.environ.get("LLM_BASE_URL", ""))
    ap.add_argument("--llm-modelo", default=os.environ.get("LLM_MODELO", "modelo-local"))
    ap.add_argument("--llm-reasoning-effort", default=os.environ.get("LLM_REASONING_EFFORT", ""))
    ap.add_argument("--ollama-host", default=os.environ.get("OLLAMA_HOST", ""))
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--max-palavras", type=int, default=40)
    ap.add_argument("--corpus", choices=("base", "ampliado"), default="ampliado",
                    help="base: 12 documentos e 28 perguntas; ampliado: 57 documentos e 151 perguntas (Etapa 3)")
    ap.add_argument("--fracao-selecao", type=float, default=0.5,
                    help="fração das perguntas que escolhe a variante; o resto testa (0 = escolher e testar nas mesmas)")
    ap.add_argument("--semente-selecao", default="aurora-selecao-v1")
    ap.add_argument("--cache-llm", default="", help="arquivo de cache das chamadas ao LLM (execução retomável)")
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    ampliado = args.corpus == "ampliado"
    if not args.dsn:
        ap.error("defina --dsn ou PGVECTOR_DSN (a senha não é gravada no registro)")

    t0 = time.perf_counter()
    with tempfile.TemporaryDirectory() as pasta:
        pdfs = corpus_aurora.gerar_pdfs(pasta, ampliado=ampliado)
        trechos = []
        for doc, caminho in pdfs.items():
            meta = corpus_aurora.metadados_doc(doc)
            trechos += ing.segmentar(
                ing.extrair_paginas_pdf(caminho),
                doc,
                max_palavras=args.max_palavras,
                sobreposicao=8,
                perfis=meta["perfis"],
                departamento=meta["departamento"],
                versao=meta["versao"],
                vigente=meta["vigente"],
            )
    embedder = rs.EmbedderOpenAICompativel(args.embed_base_url, args.embed_modelo)
    vetores = embedder.embutir([t.texto for t in trechos])
    armazem = rs.ArmazemPgvector(args.dsn)
    armazem.criar_esquema(embedder.dim, recriar=True)
    armazem.inserir(trechos, vetores)
    t_ingestao = time.perf_counter() - t0
    memoria_ingestao = medir_memoria_ollama(args.ollama_host) if args.ollama_host else {}

    consultas = corpus_aurora.carregar_consultas(ampliado=ampliado)
    com_resposta = [
        dict(c, relevantes=rp.resolver_relevantes(trechos, c["relevantes"]))
        for c in consultas
        if not c.get("sem_resposta")
    ]
    consultas_acl = [c for c in consultas if c.get("categoria") == "acl"]
    filtro_padrao = rs.FiltroBusca(perfil="aluno", apenas_vigentes=True)

    cliente = None
    variantes = [
        ("vetorial", "vetorial", None),
        ("lexical", "lexical", None),
        ("hibrida_rrf", "hibrida", None),
        ("hibrida_reranker_lexico", "hibrida", rp.ReordenadorLexico()),
    ]
    if args.llm_base_url:
        cliente = ClienteChatOpenAI(
            base_url=args.llm_base_url,
            modelo=args.llm_modelo,
            provedor="openai-compativel-local",
            timeout_s=180.0,
            reasoning_effort=args.llm_reasoning_effort or None,
        )
        if args.cache_llm:
            cliente = ClienteChatComCache(cliente, args.cache_llm)
        variantes.append(("hibrida_reranker_llm", "hibrida", rp.ReordenadorLLM(cliente)))

    avaliacoes = {
        nome: rp.avaliar_recuperacao(
            com_resposta, armazem, embedder, k=args.k, reordenador=reord, modo=modo, filtro_padrao=filtro_padrao
        )
        for nome, modo, reord in variantes
    }
    auditoria_acl = rp.auditar_acl(consultas_acl, armazem, embedder, k=args.k, perfil_nao_autorizado="aluno")

    todos_ids = [c["id"] for c in com_resposta]
    if args.fracao_selecao > 0:
        ids_selecao, ids_teste = dividir_selecao_teste(todos_ids, args.fracao_selecao, args.semente_selecao)
    else:
        ids_selecao = ids_teste = set(todos_ids)
    mrr_selecao = {nome: mrr_medio(avaliacoes[nome], ids_selecao) for nome, _, _ in variantes}
    melhor = max(range(len(variantes)), key=lambda i: (mrr_selecao[variantes[i][0]], -i))
    nome_melhor, modo_melhor, reord_melhor = variantes[melhor]

    geracao = []
    if cliente is not None:
        for c in consultas:
            filtro = rp._filtro_da_consulta(c, filtro_padrao)
            rec = rp.recuperar(
                c["pergunta"], armazem, embedder, k=args.k, reordenador=reord_melhor, modo=modo_melhor, filtro=filtro
            )
            out = rp.responder(c["pergunta"], rec, cliente)
            fid = rp.fidelidade(out["resposta"], rec.trechos)
            esperado = [e for e in c.get("resposta_esperada_contem", [])
                        if ds.normalizar(e) not in ds.normalizar(out["resposta"])]
            geracao.append({
                "id": c["id"],
                "categoria": c.get("categoria"),
                "resposta": out["resposta"],
                "latencia_ms": out["latencia_ms"],
                "tokens_saida": out["tokens_saida"],
                "fidelidade": fid,
                "faltou_esperado": esperado,
                "recusou_corretamente": (fid["recusa"] if c.get("sem_resposta") else None),
            })

    memoria = medir_memoria_ollama(args.ollama_host) if args.ollama_host else {}
    resultado = {
        "configuracao": {
            "embed_base_url": args.embed_base_url,
            "embed_modelo": args.embed_modelo,
            "dimensao": embedder.dim,
            "llm_base_url": args.llm_base_url or None,
            "llm_modelo": args.llm_modelo,
            "llm_reasoning_effort": args.llm_reasoning_effort or None,
            "k": args.k,
            "max_palavras": args.max_palavras,
            "corpus": args.corpus,
            "dsn": "postgresql://***@pgvector",
        },
        "ingestao": {
            "documentos": len(corpus_aurora.documentos(ampliado)),
            "trechos": len(trechos),
            "trechos_tabela": sum(1 for t in trechos if t.tipo == "tabela"),
            "trechos_restritos": sum(1 for t in trechos if "aluno" not in t.perfis),
            "trechos_revogados": sum(1 for t in trechos if not t.vigente),
            "segundos": round(t_ingestao, 3),
        },
        "recuperacao": {n: {k: v for k, v in a.items() if k != "por_consulta"} for n, a in avaliacoes.items()},
        "auditoria_acl": auditoria_acl,
        "variante_escolhida_para_geracao": nome_melhor,
        "recuperacao_por_consulta": avaliacoes[nome_melhor]["por_consulta"],
        "selecao_da_variante": {
            "criterio": "maior MRR nas perguntas de seleção; estatística só nas de teste",
            "fracao_selecao": args.fracao_selecao, "n_selecao": len(ids_selecao), "n_teste": len(ids_teste),
            "mesmo_conjunto": ids_selecao == ids_teste, "mrr_selecao": mrr_selecao,
        },
        "estatistica_recuperacao": estatistica_recuperacao(avaliacoes, nome_melhor, ids_teste),
        "geracao": geracao,
    }
    if isinstance(cliente, ClienteChatComCache) and cliente.chamadas_reais == 0:
        memoria_ingestao, memoria = {}, {}  # só cache: /api/ps não descreveria esta execução
    if memoria_ingestao or memoria:
        resultado["memoria"] = {"ingestao": memoria_ingestao, "geracao": memoria}
    if geracao:
        respondidas = [g for g in geracao if g["recusou_corretamente"] is None]
        resultado["geracao_resumo"] = {
            "fidelidade_media": round(sum(g["fidelidade"]["fidelidade"] for g in respondidas) / max(len(respondidas), 1), 3),
            "acerto_conteudo_esperado": sum(1 for g in respondidas if not g["faltou_esperado"]),
            "respondidas": len(respondidas),
            "recusas_corretas": sum(1 for g in geracao if g["recusou_corretamente"]),
            "perguntas_sem_resposta": sum(1 for g in geracao if g["recusou_corretamente"] is not None),
            "latencia_ms": mb.resumir_latencias_ms([float(g["latencia_ms"]) for g in geracao]),
        }
        r = resultado["geracao_resumo"]
        r["wilson95_conteudo_esperado"] = est.wilson(r["acerto_conteudo_esperado"], r["respondidas"])
        r["wilson95_recusas"] = est.wilson(r["recusas_corretas"], r["perguntas_sem_resposta"])
    if isinstance(cliente, ClienteChatComCache):
        resultado["cache_llm"] = {"reaproveitadas": cliente.acertos_cache, "chamadas_reais": cliente.chamadas_reais}
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p02-rag-pgvector", resultado))
    return 0


if __name__ == "__main__":
    sys.exit(main())
