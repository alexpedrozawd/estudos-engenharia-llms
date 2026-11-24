"""Testes offline do Laboratório 17."""
import itertools
import unittest

from comum.cliente_llm import ClienteMockDeterministico
from lab_17_llmops.operacao import (Rastreador, decidir_canario, distribuicao, grupo, metricas_operacao, psi)


class TestLab17LLMOps(unittest.TestCase):
    def test_rastro_aninhado_com_atributos_genai(self):
        tempo = itertools.count(0.0, 0.1)
        r = Rastreador(relogio=lambda: next(tempo))
        cli = ClienteMockDeterministico(fallback="O prazo é de 7 dias.")
        with r.span("atender", "t1"):
            with r.span("buscar", "t1", **{"aurora.etapa": "busca"}):
                pass
            with r.span("chat modelo-didatico-v1", "t1", **{"gen_ai.operation.name": "chat",
                                                            "gen_ai.request.model": cli.modelo}) as s:
                resp = cli.completar("Qual o prazo?")
                s["attributes"]["gen_ai.usage.input_tokens"] = resp.tokens_entrada
                s["attributes"]["gen_ai.usage.output_tokens"] = resp.tokens_saida
        raiz = [s for s in r.spans if s["name"] == "atender"][0]
        filhos = [s for s in r.spans if s["parent_id"] == raiz["span_id"]]
        self.assertEqual(len(filhos), 2)
        res = r.resumo("t1")
        self.assertEqual((res["spans"], res["erros"], res["tokens_saida"]), (3, 0, 6))
        self.assertGreater(res["duracao"], 0)

    def test_erro_fica_no_span(self):
        r = Rastreador(relogio=lambda: 0.0)
        with self.assertRaises(TimeoutError):
            with r.span("chat", "t2", **{"gen_ai.operation.name": "chat"}):
                raise TimeoutError("provedor lento")
        self.assertEqual(r.spans[0]["status"], "ERROR")
        self.assertEqual(r.spans[0]["attributes"]["error.type"], "TimeoutError")

    def test_psi_reproduz_o_capitulo(self):
        ref = {"prazo": 0.40, "financeiro": 0.30, "conteudo": 0.25, "outros": 0.05}
        self.assertEqual(psi(ref, {"prazo": 0.38, "financeiro": 0.31, "conteudo": 0.26, "outros": 0.05}), 0.002)
        self.assertEqual(psi(ref, {"prazo": 0.15, "financeiro": 0.55, "conteudo": 0.20, "outros": 0.10}), 0.443)
        self.assertGreater(psi(ref, {**ref, "novo_tema": 0.2}), 0.2)   # faixa nova também conta
        self.assertEqual(distribuicao(["a", "b", "a", "a"]), {"a": 0.75, "b": 0.25})

    def test_canario_estavel_e_decisao(self):
        usuarios = [f"aluno-{i}" for i in range(2000)]
        n = sum(grupo(u) == "canario" for u in usuarios)
        self.assertTrue(60 <= n <= 140, n)
        self.assertEqual({grupo("aluno-7") for _ in range(5)}, {grupo("aluno-7")})
        base = {"acerto": 0.90, "latencia_p95": 2.0}
        self.assertEqual(decidir_canario(base, {"acerto": 0.86, "latencia_p95": 2.0}, 500), "reverter")
        self.assertEqual(decidir_canario(base, {"acerto": 0.90, "latencia_p95": 2.5}, 500), "reverter")
        self.assertEqual(decidir_canario(base, {"acerto": 0.91, "latencia_p95": 2.1}, 50), "esperar")
        self.assertEqual(decidir_canario(base, {"acerto": 0.91, "latencia_p95": 2.1}, 500), "promover")

    def test_mttd_mttr_cfr(self):
        inc = [{"inicio": 0, "detectado": 10, "restaurado": 40, "causado_por_mudanca": True},
               {"inicio": 100, "detectado": 130, "restaurado": 160}]
        self.assertEqual(metricas_operacao(inc, mudancas=10), {"mttd": 20.0, "mttr": 50.0, "cfr": 0.1})
        self.assertEqual(metricas_operacao([], 0), {"mttd": None, "mttr": None, "cfr": None})


if __name__ == "__main__":
    unittest.main()
