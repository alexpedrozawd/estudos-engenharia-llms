"""Testes offline do Laboratório 18."""
import unittest

from lab_18_economia.custos import (custo_sessao, decidir_lote, invalidacoes_maximas, leituras_para_compensar,
                                    orcamento_mensal, varrer)

BASE = dict(prefixo=20000, turnos=30, tokens_turno=300, saida_turno=400)


class TestLab18Economia(unittest.TestCase):
    def test_reproduz_o_bloco_do_capitulo(self):
        sem = custo_sessao(**BASE)
        com = custo_sessao(**BASE, mult_leitura=0.1, mult_gravacao=1.25)
        quebrado = custo_sessao(**BASE, mult_leitura=0.1, mult_gravacao=1.25, invalidacoes=10)
        self.assertEqual(round(1 - com / sem, 2), 0.79)
        self.assertLess(quebrado - com, (sem - com) * 0.55)          # perde quase metade da economia
        self.assertGreater(quebrado - com, (sem - com) * 0.40)
        self.assertEqual((round(sem), round(com), round(quebrado)), (657000, 140000, 370000))
        self.assertEqual(round(sem * 0.5), 328500)

    def test_ponto_de_equilibrio_do_cache(self):
        self.assertEqual(leituras_para_compensar(1.25, 0.1), 1)
        self.assertEqual(leituras_para_compensar(2.0, 0.1), 2)
        self.assertEqual(invalidacoes_maximas(BASE, 0.1, 1.25), 22)  # cada invalidação troca leitura 0,1 por gravação 1,25
        self.assertEqual(invalidacoes_maximas(BASE, 0.1, 2.0), 13)

    def test_lote_so_fora_do_interativo(self):
        self.assertTrue(decidir_lote(prazo_horas=36, interativo=False))
        self.assertFalse(decidir_lote(prazo_horas=36, interativo=True))
        self.assertFalse(decidir_lote(prazo_horas=2, interativo=False))

    def test_sensibilidade_e_orcamento(self):
        linhas = varrer(BASE, "turnos", [2, 10, 30, 80])
        economias = [x["economia"] for x in linhas]
        self.assertEqual(economias, sorted(economias))               # mais turnos, mais leituras do prefixo
        self.assertEqual(orcamento_mensal(1000, 100000, 3.0), 9000.0)


if __name__ == "__main__":
    unittest.main()
