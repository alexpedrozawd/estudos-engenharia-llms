"""Testes offline do Laboratório 14."""
import unittest

from lab_14_inferencia.medicao import (camadas_na_gpu, medir_pedido, memoria, percentil, relatorio,
                                       servidor_simulado)


class TestLab14Inferencia(unittest.TestCase):
    def test_memoria_reproduz_o_capitulo(self):
        p, kv = memoria(27, 4.8, 40, 8, 128, 32768, usuarios=4)
        self.assertAlmostEqual(p, 15.09, places=2)
        self.assertAlmostEqual(kv, 20.0, places=6)
        self.assertEqual(memoria(27, 4.8, 40, 8, 128, 131072)[1], kv)  # 4 x 32k = 1 x 128k

    def test_descarga_para_cpu(self):
        p, kv = memoria(27, 4.8, 40, 8, 128, 32768)
        self.assertEqual(camadas_na_gpu(24, p, kv, 40), 40)
        self.assertLess(camadas_na_gpu(12, p, kv, 40), 40)

    def test_medir_pedido_de_carimbos(self):
        m = medir_pedido(0.0, [0.3, 0.35, 0.40, 0.45])
        self.assertAlmostEqual(m["ttft"], 0.3)
        self.assertAlmostEqual(m["tpot"], 0.05)
        self.assertEqual(m["tokens"], 4)
        with self.assertRaises(ValueError):
            medir_pedido(0.0, [])

    def test_percentil_posto_mais_proximo(self):
        v = list(range(1, 101))
        self.assertEqual(percentil(v, 50), 50)
        self.assertEqual(percentil(v, 95), 95)
        self.assertEqual(percentil([7], 99), 7)

    def test_cauda_aparece_no_p95_e_nao_na_mediana(self):
        medidas = [medir_pedido(i, c) for i, c in servidor_simulado(100)]
        r = relatorio(medidas, slo_ttft=0.5, slo_tpot=0.08)
        self.assertLess(r["ttft_p50"], 0.5)
        self.assertGreater(r["ttft_p95"], 1.0)
        self.assertAlmostEqual(r["goodput"], 0.90)
        self.assertEqual(relatorio(medidas, 0.5, 0.08), r)  # determinístico pela semente


if __name__ == "__main__":
    unittest.main()
