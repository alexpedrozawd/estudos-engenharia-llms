"""Smoke-tests offline do projeto 02 (PDF gerado na hora, armazém em memória, SQL em conexão falsa)."""
import json
import os
import tempfile
import unittest

import httpx

import corpus_aurora
import mercado_base as mb
import rag_ingestao as ing
import rag_pipeline as rp
import rag_store as rs
from comum.cliente_llm import ClienteMockDeterministico


def ingerir_corpus(max_palavras=40):
    trechos = []
    with tempfile.TemporaryDirectory() as pasta:
        for doc, caminho in corpus_aurora.gerar_pdfs(pasta).items():
            meta = corpus_aurora.metadados_doc(doc)
            trechos += ing.segmentar(
                ing.extrair_paginas_pdf(caminho),
                doc,
                max_palavras=max_palavras,
                sobreposicao=8,
                perfis=meta["perfis"],
                departamento=meta["departamento"],
                versao=meta["versao"],
                vigente=meta["vigente"],
            )
    return trechos


class TestIngestao(unittest.TestCase):
    def test_tabela_vira_markdown_com_cabecalho(self):
        trechos = ingerir_corpus()
        self.assertGreaterEqual(len(trechos), 35)
        tabelas = [t for t in trechos if t.tipo == "tabela"]
        self.assertGreaterEqual(len(tabelas), 4)
        tab_serv = next(t for t in tabelas if t.doc == "tabela-de-servicos")
        linhas = tab_serv.texto.splitlines()
        self.assertEqual(linhas[0], "| Servico | Prazo (dias uteis) | Taxa (R$) |")
        self.assertIn("| Segunda via do diploma | 30 | 120,00 |", linhas)
        self.assertEqual(len(linhas), 2 + 5)

    def test_tabela_longa_repete_cabecalho(self):
        pagina = ["Cab A      Cab B"] + [f"linha {i}      {i}" for i in range(5)]
        trechos = ing.segmentar(["\n".join(pagina)], "d", max_linhas_tabela=2)
        self.assertEqual([t.tipo for t in trechos], ["tabela"] * 3)
        self.assertTrue(all(t.texto.startswith("| Cab A | Cab B |") for t in trechos))

    def test_ids_estaveis_e_sobreposicao(self):
        a, b = ingerir_corpus(), ingerir_corpus()
        self.assertEqual([t.id for t in a], [t.id for t in b])
        pedacos = ing.fatiar_texto([str(i) for i in range(10)], 4, 1)
        self.assertEqual(pedacos, ["0 1 2 3", "3 4 5 6", "6 7 8 9"])
        with self.assertRaises(ValueError):
            ing.fatiar_texto(["a"], 2, 2)


class FakeCursor:
    def __init__(self, log, linhas):
        self.log, self.linhas = log, linhas

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def execute(self, sql, params=None):
        self.log.append((sql, params))

    def executemany(self, sql, seq):
        self.log.append((sql, list(seq)))

    def fetchall(self):
        return self.linhas


class FakeConexao:
    def __init__(self, log, linhas=()):
        self.log, self.linhas = log, list(linhas)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def cursor(self):
        return FakeCursor(self.log, self.linhas)


class TestPgvectorSQL(unittest.TestCase):
    def test_esquema_insercao_e_busca(self):
        log = []
        linha = ("d:p1:1", "d", 1, "texto", "conteúdo", ["aluno", "admin"], "academico", "2026", True, 0.9)
        arm = rs.ArmazemPgvector(conectar=lambda: FakeConexao(log, [linha]))
        arm.criar_esquema(3, recriar=True)
        sqls = [s for s, _ in log]
        self.assertEqual(sqls[0], "CREATE EXTENSION IF NOT EXISTS vector")
        self.assertIn("embedding vector(3) NOT NULL", sqls[2])
        self.assertIn("perfis text[] NOT NULL", sqls[2])
        self.assertIn("USING hnsw (embedding vector_cosine_ops)", sqls[3])
        self.assertIn("USING gin (perfis)", sqls[5])
        self.assertIn("to_tsvector('portuguese', texto_busca)", sqls[2])
        log.clear()
        arm.inserir(
            [ing.Trecho("d:p1:1", "d", 1, "texto", "Matrícula", perfis=("docente",), departamento="academico", versao="2026", vigente=True)],
            [[0.1, 0.2, 0.3]],
        )
        sql, linhas = log[0]
        self.assertIn("ON CONFLICT (id) DO UPDATE", sql)
        self.assertEqual(linhas[0][5], "matricula")
        self.assertEqual(linhas[0][6], ["docente"])
        self.assertEqual(linhas[0][10], "[0.1,0.2,0.3]")
        log.clear()
        filtro = rs.FiltroBusca(perfil="docente", apenas_vigentes=True)
        res = arm.buscar_vetorial([1, 0, 0], 2, filtro=filtro)
        self.assertIn("WHERE %s = ANY(perfis) AND vigente = %s", log[0][0])
        self.assertIn("ORDER BY embedding <=> %s::vector", log[0][0])
        self.assertEqual(log[0][1], ("[1,0,0]", "docente", True, "[1,0,0]", 2))
        self.assertEqual(res[0][0].id, "d:p1:1")
        self.assertEqual(res[0][0].perfis, ("aluno", "admin"))
        log.clear()
        arm.buscar_lexical("Qual a taxa do histórico?", 2, filtro=filtro)
        self.assertIn("lexico @@ q AND %s = ANY(perfis) AND vigente = %s", log[0][0])
        self.assertEqual(log[0][1], ("taxa | historico", "docente", True, 2))
        self.assertEqual(arm.buscar_lexical("a de o", 2), [])

    def test_dimensao_invalida(self):
        with self.assertRaises(ValueError):
            rs.ArmazemPgvector(conectar=lambda: None).criar_esquema(0)


class TestEmbedderHTTP(unittest.TestCase):
    def test_lotes_ordem_e_normalizacao(self):
        chamadas = []

        def handler(request):
            corpo = json.loads(request.content)
            chamadas.append(len(corpo["input"]))
            data = [{"index": i, "embedding": [3.0, 4.0]} for i in reversed(range(len(corpo["input"])))]
            return httpx.Response(200, json={"data": data})

        e = rs.EmbedderOpenAICompativel("http://servico.invalido/v1", "m", lote=2, transport=httpx.MockTransport(handler))
        v = e.embutir(["a", "b", "c"])
        self.assertEqual(chamadas, [2, 1])
        self.assertEqual(e.dim, 2)
        self.assertAlmostEqual(v[0][0], 0.6)


class TestRecuperacaoEAvaliacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trechos = ingerir_corpus()
        cls.emb = rs.EmbedderHash(256)
        cls.arm = rs.ArmazemMemoria()
        cls.arm.inserir(cls.trechos, cls.emb.embutir([t.texto for t in cls.trechos]))
        cls.consultas = [dict(c, relevantes=rp.resolver_relevantes(cls.trechos, c["relevantes"]))
                         for c in corpus_aurora.carregar_consultas() if not c.get("sem_resposta")]

    def test_relevantes_resolvidos(self):
        self.assertTrue(all(c["relevantes"] for c in self.consultas))

    def test_rrf_deterministico(self):
        t = {i: ing.Trecho(i, "d", 1, "texto", i) for i in "abc"}
        f = rp.fusao_rrf([[(t["a"], 1), (t["b"], 1)], [(t["b"], 1), (t["c"], 1)]])
        self.assertEqual([x.id for x, _ in f], ["b", "a", "c"])

    def test_metricas_de_recuperacao(self):
        self.assertEqual(rp.recall_em_k(["x", "a"], ["a", "b"], 2), 0.5)
        self.assertEqual(rp.mrr(["x", "a"], ["a"]), 0.5)
        self.assertAlmostEqual(rp.ndcg_em_k(["a"], ["a"], 3), 1.0)
        filtro = rs.FiltroBusca(perfil="aluno", apenas_vigentes=True)
        av_vet = rp.avaliar_recuperacao(self.consultas, self.arm, self.emb, k=4, modo="vetorial", filtro_padrao=filtro)
        av_lex = rp.avaliar_recuperacao(self.consultas, self.arm, self.emb, k=4, modo="lexical", filtro_padrao=filtro)
        av_hib = rp.avaliar_recuperacao(
            self.consultas, self.arm, self.emb, k=4, modo="hibrida", reordenador=rp.ReordenadorLexico(), filtro_padrao=filtro
        )
        self.assertGreaterEqual(av_hib["recall_medio"], 0.8)
        self.assertGreaterEqual(av_hib["mrr_medio"], 0.6)
        self.assertEqual(av_vet["modo"], "vetorial")
        self.assertEqual(av_lex["modo"], "lexical")

    def test_acl_e_versoes_conflitantes(self):
        consultas_acl = [c for c in corpus_aurora.carregar_consultas() if c.get("categoria") == "acl"]
        aud = rp.auditar_acl(consultas_acl, self.arm, self.emb, k=4, perfil_nao_autorizado="aluno")
        self.assertEqual(aud["vazamentos"], 0)
        self.assertEqual(aud["consultas"], 4)

        rec_admin = rp.recuperar(
            "código interno AUR-FIN-2026 estornos",
            self.arm, self.emb, k=2, filtro=rs.FiltroBusca(perfil="admin", apenas_vigentes=True),
        )
        self.assertTrue(any(t.doc == "manual-financeiro-administrativo" for t in rec_admin.trechos))

        rec_vig = rp.recuperar(
            "taxa do histórico escolar",
            self.arm, self.emb, k=4, filtro=rs.FiltroBusca(perfil="aluno", apenas_vigentes=True),
        )
        self.assertTrue(all(t.vigente for t in rec_vig.trechos))
        self.assertTrue(any(t.doc == "tabela-de-servicos" for t in rec_vig.trechos))

    def test_reranker_prioriza_tabela_em_pergunta_de_valor(self):
        rec = rp.recuperar("Qual a taxa do histórico escolar?", self.arm, self.emb, k=1, reordenador=rp.ReordenadorLexico())
        self.assertEqual(rec.trechos[0].tipo, "tabela")

    def test_reranker_llm_com_mock_e_falha_segura(self):
        cliente = ClienteMockDeterministico(respostas={"Segunda via": "3"}, fallback="sem nota")
        cand = [(t, 0.0) for t in self.trechos[:3]] + [(next(t for t in self.trechos if t.tipo == "tabela"), 0.0)]
        out = rp.ReordenadorLLM(cliente).reordenar("Quanto custa a segunda via?", cand)
        self.assertEqual(out[0][0].tipo, "tabela")
        self.assertEqual(len(out), len(cand))

    def test_geracao_com_citacoes_e_fidelidade(self):
        rec = rp.recuperar("Qual a taxa do histórico escolar?", self.arm, self.emb, k=2, reordenador=rp.ReordenadorLexico())
        cliente = ClienteMockDeterministico(fallback="A taxa do histórico escolar é R$ 25,00 [T1].")
        out = rp.responder("Qual a taxa do histórico escolar?", rec, cliente)
        self.assertIn("[T1] (tabela-de-servicos", cliente.chamadas[0]["prompt"])
        f = rp.fidelidade(out["resposta"], rec.trechos)
        self.assertEqual((f["frases"], f["apoiadas"], f["citacoes_invalidas"]), (1, 1, []))
        sem_cit = rp.fidelidade("A taxa é de R$ 25,00. Inventei isto [T9].", rec.trechos)
        self.assertEqual(sem_cit["apoiadas"], 0)
        self.assertEqual(sem_cit["citacoes_invalidas"], [9])
        self.assertTrue(rp.fidelidade(rp.RESPOSTA_RECUSA, rec.trechos)["recusa"])
        # Regressão: citação depois do ponto não vira frase separada.
        pos_ponto = rp.fidelidade("A taxa do histórico escolar é de R$ 25,00. [T1]", rec.trechos)
        self.assertEqual((pos_ponto["frases"], pos_ponto["apoiadas"]), (1, 1))

    def test_cliente_chat_openai_completar_com_reasoning_effort(self):
        from mercado_base.cliente_openai import ClienteChatOpenAI

        payloads = []

        def handler(request):
            payloads.append(json.loads(request.content))
            return httpx.Response(200, json={
                "model": "qwen3.8:27b-ud-iq3_xxs",
                "choices": [{"message": {"role": "assistant", "content": "3"}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 20, "completion_tokens": 1},
            })

        cli = ClienteChatOpenAI(
            "http://servico.invalido/v1",
            "qwen3.8:27b-ud-iq3_xxs",
            reasoning_effort="none",
            transport=httpx.MockTransport(handler),
        )
        r = cli.completar("Avalie.", sistema="Responda só 0-3.", max_tokens=4)
        self.assertEqual(r.texto, "3")
        self.assertEqual(payloads[0]["reasoning_effort"], "none")
        self.assertEqual(mb.resumir_latencias_ms([]), {"p50": None, "p95": None})
        self.assertEqual(mb.resumir_latencias_ms([10.0, 20.0, 30.0]), {"p50": 20.0, "p95": 29.0})


class TestPDFMinimo(unittest.TestCase):
    def test_pdf_valido_e_latin1(self):
        dados = mb.gerar_pdf_texto([["Olá, matrícula (teste)"]])
        self.assertTrue(dados.startswith(b"%PDF-1.4"))
        self.assertEqual(ing.extrair_paginas_pdf(dados)[0].strip(), "Olá, matrícula (teste)")
        with tempfile.TemporaryDirectory() as d:
            caminhos = corpus_aurora.gerar_pdfs(d)
            self.assertEqual(sorted(os.path.basename(c) for c in caminhos.values())[0], "calendario-academico-2026.pdf")
            self.assertEqual(len(caminhos), 12)


if __name__ == "__main__":
    unittest.main()
