"""Execução real do projeto 02: PDFs → pgvector → busca híbrida → reranker → resposta → avaliação.

Pré-requisitos (ver README): `compose.yaml` com perfis `rag` (PostgreSQL + pgvector) e
`serving` (llama-server de embeddings e de chat) ou qualquer endpoint OpenAI-compatível.

Exemplo:
    PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
    .venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/executar_rag_real.py \
        --embed-base-url http://127.0.0.1:8082/v1 --embed-modelo qwen3-embedding-0.6b \
        --llm-base-url http://127.0.0.1:8081/v1 --llm-modelo qwen3-4b --registrar
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

from comum.cliente_llm import ClienteHTTPOpenAICompativel  # noqa: E402
import corpus_aurora  # noqa: E402
import rag_ingestao as ing  # noqa: E402
import rag_pipeline as rp  # noqa: E402
import rag_store as rs  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dsn", default=os.environ.get("PGVECTOR_DSN", ""))
    ap.add_argument("--embed-base-url", default=os.environ.get("EMBED_BASE_URL", "http://127.0.0.1:8082/v1"))
    ap.add_argument("--embed-modelo", default=os.environ.get("EMBED_MODELO", "embed-local"))
    ap.add_argument("--llm-base-url", default=os.environ.get("LLM_BASE_URL", ""))
    ap.add_argument("--llm-modelo", default=os.environ.get("LLM_MODELO", "modelo-local"))
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--max-palavras", type=int, default=40)
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    if not args.dsn:
        ap.error("defina --dsn ou PGVECTOR_DSN (a senha não é gravada no registro)")

    t0 = time.perf_counter()
    with tempfile.TemporaryDirectory() as pasta:
        pdfs = corpus_aurora.gerar_pdfs(pasta)
        trechos = []
        for doc, caminho in pdfs.items():
            trechos += ing.segmentar(ing.extrair_paginas_pdf(caminho), doc,
                                     max_palavras=args.max_palavras, sobreposicao=8)
    embedder = rs.EmbedderOpenAICompativel(args.embed_base_url, args.embed_modelo)
    vetores = embedder.embutir([t.texto for t in trechos])
    armazem = rs.ArmazemPgvector(args.dsn)
    armazem.criar_esquema(embedder.dim, recriar=True)
    armazem.inserir(trechos, vetores)
    t_ingestao = time.perf_counter() - t0

    consultas = corpus_aurora.carregar_consultas()
    com_resposta = [dict(c, relevantes=rp.resolver_relevantes(trechos, c["relevantes"]))
                    for c in consultas if not c.get("sem_resposta")]
    cliente = None
    variantes = [("sem_reranker", None), ("reranker_lexico", rp.ReordenadorLexico())]
    if args.llm_base_url:
        cliente = ClienteHTTPOpenAICompativel(modelo=args.llm_modelo, base_url=args.llm_base_url,
                                              provedor="openai-compativel-local", timeout_s=180.0)
        variantes.append(("reranker_llm", rp.ReordenadorLLM(cliente)))
    avaliacoes = {
        nome: rp.avaliar_recuperacao(com_resposta, armazem, embedder, k=args.k, reordenador=r)
        for nome, r in variantes
    }
    # A geração usa a variante com melhor MRR medido (empate: a mais simples, que vem antes).
    melhor = max(range(len(variantes)), key=lambda i: (avaliacoes[variantes[i][0]]["mrr_medio"], -i))
    nome_melhor, reord_melhor = variantes[melhor]

    geracao = []
    if cliente is not None:
        for c in consultas:
            rec = rp.recuperar(c["pergunta"], armazem, embedder, k=args.k, reordenador=reord_melhor)
            out = rp.responder(c["pergunta"], rec, cliente)
            fid = rp.fidelidade(out["resposta"], rec.trechos)
            esperado = [e for e in c.get("resposta_esperada_contem", []) if e.lower() not in out["resposta"].lower()]
            geracao.append({
                "id": c["id"], "resposta": out["resposta"], "latencia_ms": out["latencia_ms"],
                "tokens_saida": out["tokens_saida"], "fidelidade": fid,
                "faltou_esperado": esperado,
                "recusou_corretamente": (fid["recusa"] if c.get("sem_resposta") else None),
            })

    resultado = {
        "configuracao": {"embed_modelo": args.embed_modelo, "dimensao": embedder.dim, "llm_modelo": args.llm_modelo,
                         "k": args.k, "max_palavras": args.max_palavras, "dsn": "postgresql://***@pgvector"},
        "ingestao": {"documentos": len(corpus_aurora.DOCUMENTOS), "trechos": len(trechos),
                     "trechos_tabela": sum(1 for t in trechos if t.tipo == "tabela"),
                     "segundos": round(t_ingestao, 3)},
        "recuperacao": {n: {k: v for k, v in a.items() if k != "por_consulta"} for n, a in avaliacoes.items()},
        "variante_escolhida_para_geracao": nome_melhor,
        "recuperacao_por_consulta": avaliacoes[nome_melhor]["por_consulta"],
        "geracao": geracao,
    }
    if geracao:
        respondidas = [g for g in geracao if g["recusou_corretamente"] is None]
        resultado["geracao_resumo"] = {
            "fidelidade_media": round(sum(g["fidelidade"]["fidelidade"] for g in respondidas) / max(len(respondidas), 1), 3),
            "acerto_conteudo_esperado": sum(1 for g in respondidas if not g["faltou_esperado"]),
            "respondidas": len(respondidas),
            "recusas_corretas": sum(1 for g in geracao if g["recusou_corretamente"]),
            "perguntas_sem_resposta": sum(1 for g in geracao if g["recusou_corretamente"] is not None),
        }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p02-rag-pgvector", resultado))
    return 0


if __name__ == "__main__":
    sys.exit(main())
