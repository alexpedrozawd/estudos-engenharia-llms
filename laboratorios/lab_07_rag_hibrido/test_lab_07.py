"""Testes offline do Laboratório 07."""
import unittest

from comum.cliente_llm import ClienteMockDeterministico
from lab_07_rag_hibrido.rag import (
    BM25, buscar_hibrido, carregar_documentos, fatiar, mrr, ndcg_at_k, recall_at_k,
    responder_com_fontes, rrf,
)


class TestLab07Rag(unittest.TestCase):
    def setUp(self):
        self.docs = carregar_documentos()

    def test_fatiar_com_sobreposicao(self):
        palavras = "a b c d e f g h i j".split()
        self.assertEqual(fatiar(palavras, 4, 1), ["a b c d", "d e f g", "g h i j"])
        with self.assertRaises(ValueError):
            fatiar(palavras, 3, 3)

    def test_rrf_igual_ao_guia(self):
        fundido = rrf([["POL-01", "POL-07", "POL-03"], ["POL-03", "POL-01", "POL-09"]])
        self.assertEqual([d for d, _ in fundido], ["POL-01", "POL-03", "POL-07", "POL-09"])
        self.assertAlmostEqual(fundido[0][1], 1 / 61 + 1 / 62)

    def test_bm25_e_hibrido_acham_reembolso(self):
        self.assertEqual(BM25(self.docs).ranking("prazo de reembolso")[0][0], "POL-01")
        self.assertEqual(buscar_hibrido("cancelamento e reembolso em dias", self.docs)[0], "POL-01")
        self.assertEqual(buscar_hibrido("posso enviar CPF e notas", self.docs)[0], "POL-02")

    def test_metricas_de_recuperacao(self):
        rec = ["POL-03", "POL-01", "POL-02"]
        self.assertEqual(recall_at_k(rec, ["POL-01"], 1), 0.0)
        self.assertEqual(recall_at_k(rec, ["POL-01"], 2), 1.0)
        self.assertEqual(mrr(rec, ["POL-01"]), 0.5)
        self.assertAlmostEqual(ndcg_at_k(rec, ["POL-01"], 3), 1 / 1.5849625007211562, places=6)

    def test_fidelidade_das_citacoes(self):
        fiel = ClienteMockDeterministico(fallback="Até 7 dias corridos [POL-01].")
        r = responder_com_fontes("prazo de cancelamento", self.docs, fiel)
        self.assertTrue(r["fiel"])
        infiel = ClienteMockDeterministico(fallback="Depende do edital [POL-09].")
        self.assertFalse(responder_com_fontes("prazo de cancelamento", self.docs, infiel)["fiel"])


if __name__ == "__main__":
    unittest.main()
