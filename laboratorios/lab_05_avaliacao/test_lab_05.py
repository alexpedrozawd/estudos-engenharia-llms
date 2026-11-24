"""Testes offline do Laboratório 05."""
import unittest

from comum.cliente_llm import ClienteMockDeterministico
from lab_05_avaliacao.pipeline_avaliacao import (
    avaliar_por_fatias,
    bootstrap_diferenca_media,
    comparar_pareado,
    entropia_e_perplexidade,
    intervalo_wilson,
    julgar_pareado_sem_vies_posicao,
)


class TestLab05Avaliacao(unittest.TestCase):
    def test_entropia_e_perplexidade(self):
        h, ppl2, pple = entropia_e_perplexidade([0.25, 0.25, 0.25, 0.25])
        self.assertAlmostEqual(h, 2.0, places=6)
        self.assertAlmostEqual(ppl2, 4.0, places=6)
        self.assertAlmostEqual(pple, 4.0, places=6)

    def test_wilson_bootstrap_e_pareado_aurora(self):
        inf, sup = intervalo_wilson(12, 16)
        self.assertLess(inf, 0.75)
        self.assertGreater(sup, 0.75)
        self.assertGreater(sup - inf, 0.30)

        v1 = [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1]  # 12/16
        v2 = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1]  # 14/16 (+3/-1)
        par = comparar_pareado(v1, v2)
        self.assertEqual(par["ganhos_v2"], 3)
        self.assertEqual(par["perdas_v2"], 1)
        self.assertEqual(par["saldo"], 2)

        boot = bootstrap_diferenca_media(v1, v2, rodadas=500, semente=42)
        self.assertAlmostEqual(boot["diferenca_observada"], 2 / 16, places=6)
        self.assertLessEqual(boot["ic95_inf"], boot["diferenca_observada"])
        self.assertGreaterEqual(boot["ic95_sup"], boot["diferenca_observada"])

    def test_slices_e_juiz_com_inversao_de_ordem(self):
        regs = [
            {"fatia": "normal", "passou": 1},
            {"fatia": "normal", "passou": 1},
            {"fatia": "recusa", "passou": 0},
        ]
        fatias = avaliar_por_fatias(regs)
        self.assertEqual(fatias["normal"]["taxa"], 1.0)
        self.assertEqual(fatias["recusa"]["taxa"], 0.0)

        cli_inconsistente = ClienteMockDeterministico(fallback="1")
        self.assertEqual(
            julgar_pareado_sem_vies_posicao("Prazo?", "Resp A", "Resp B", cli_inconsistente),
            "empate_ou_inconsistente",
        )
        cli_consistente = ClienteMockDeterministico({"[1] Resp A": "1", "[1] Resp B": "2"})
        self.assertEqual(
            julgar_pareado_sem_vies_posicao("Prazo?", "Resp A", "Resp B", cli_consistente),
            "vencedor_A",
        )


if __name__ == "__main__":
    unittest.main()
