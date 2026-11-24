"""Testes offline do Laboratório 09."""
import unittest

from comum.cliente_llm import ClienteMockDeterministico
from lab_09_contexto_memoria.memoria import (
    NotasSessao, janela_por_pares, janela_por_recencia, sinais, taxas_por_versao,
)

PARES = [("aluno: quero trancar o curso", "assistente: o trancamento vale por seis meses"),
         ("aluno: e o reembolso?", "assistente: o reembolso integral vale por sete dias")]
SISTEMA = "Responda só com a política oficial."


class TestLab09Memoria(unittest.TestCase):
    def test_recencia_quebra_o_par_e_pares_preservam(self):
        soltos = [t for par in PARES for t in par]
        rec = janela_por_recencia(SISTEMA, soltos, "Posso pedir hoje?", 20)
        self.assertEqual(rec, ["assistente: o reembolso integral vale por sete dias"])
        cli = ClienteMockDeterministico(fallback="Aluno perguntou sobre trancamento (seis meses).")
        jan = janela_por_pares(SISTEMA, PARES, "Posso pedir hoje?", 32, cli)
        self.assertEqual(jan["pares"], [PARES[1]])
        self.assertLessEqual(jan["tokens"], 32)
        self.assertIn("trancamento", jan["resumo"])
        self.assertEqual(jan["sistema"], SISTEMA)
        self.assertEqual(len(cli.chamadas), 1)
        self.assertEqual(cli.chamadas[0]["esforco"], "low")

    def test_sem_corte_nao_chama_resumo(self):
        cli = ClienteMockDeterministico()
        jan = janela_por_pares(SISTEMA, PARES, "Posso pedir hoje?", 100, cli)
        self.assertEqual(jan["resumo"], "")
        self.assertEqual(cli.chamadas, [])

    def test_notas_consolidam_fato_que_muda(self):
        n = NotasSessao()
        n.lembrar("A07", "curso", "dados")
        n.lembrar("A07", "meta", "certificado em março")
        self.assertEqual(n.lembrar("A07", "curso", "engenharia de LLMs"), 2)
        self.assertEqual(n.fatos("A07"), {"curso": "engenharia de LLMs", "meta": "certificado em março"})
        self.assertEqual(n.historico("A07", "curso"), ["dados", "engenharia de LLMs"])
        self.assertEqual(n.fatos("A99"), {})
        n.fechar()

    def test_sinais_e_taxas_por_versao(self):
        self.assertEqual(sinais("Não, eu quis dizer o curso de dados"), ["correcao"])
        self.assertEqual(sinais("E o certificado?"), ["neutro"])
        regs = [("v3", "Valeu!"), ("v3", "E o prazo?"), ("v4", "Não, eu quis dizer outro"),
                ("v4", "Tem certeza?"), ("v4", "não era isso")]
        taxas = taxas_por_versao(regs)
        self.assertEqual(taxas["v3"], {"agradece": 0.5, "neutro": 0.5})
        self.assertAlmostEqual(taxas["v4"]["correcao"], 0.667)
        self.assertAlmostEqual(taxas["v4"]["pede_fonte"], 0.333)


if __name__ == "__main__":
    unittest.main()
