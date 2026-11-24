"""Testes offline do Laboratório 15."""
import unittest

from lab_15_finetuning.ajuste import (comparar_por_fatia, manifesto, memoria_treino, parada_antecipada,
                                      quantizar_int8, tarefa_sintetica, treinar_lora)


class TestLab15Finetuning(unittest.TestCase):
    def test_memoria_reproduz_o_capitulo(self):
        c = memoria_treino(7)
        self.assertEqual((c["pesos"], c["grad_e_adam"]), (14, 42))
        lora = memoria_treino(7, "lora")
        self.assertLess(lora["grad_e_adam"], 1)
        self.assertGreaterEqual(lora["pesos"], 14)          # pesos congelados continuam na memória
        self.assertEqual(memoria_treino(13, "qlora")["pesos"], 6.76)  # 6,5 GB em 4 bits + adaptador
        self.assertEqual(memoria_treino(7, ativacoes_gb=8)["total"], 64)
        with self.assertRaises(ValueError):
            memoria_treino(7, "magico")

    def test_lora_aprende_a_mudanca_de_posto_baixo(self):
        w, treino, val = tarefa_sintetica()
        r = treinar_lora(w, treino, val)
        self.assertLess(r["val_depois"], r["val_antes"] * 0.05)
        self.assertEqual(r["parametros_treinaveis"], 8)      # 2·d·r contra d·d = 16 da base
        self.assertLess(r["epocas_rodadas"], 500)            # parou antes do teto: a validação deixou de melhorar
        self.assertEqual(r["melhor_epoca"], r["epocas_rodadas"] - 5)
        self.assertEqual(treinar_lora(w, treino, val)["val_depois"], r["val_depois"])  # determinístico

    def test_parada_antecipada(self):
        self.assertEqual(parada_antecipada([1.0, 0.6, 0.5, 0.55, 0.4]), 3)
        self.assertEqual(parada_antecipada([1.0, 0.6, 0.5, 0.55, 0.4], paciencia=2), 5)

    def test_quantizacao_por_bloco_reduz_erro(self):
        pesos = [0.82, -0.31, 0.05, -1.27, 0.40, 0.003, 0.02, -0.01]
        q, escalas, erro_global = quantizar_int8(pesos)
        self.assertEqual(len(escalas), 1)
        self.assertTrue(all(-127 <= v <= 127 for v in q))
        _, escalas_b, erro_bloco = quantizar_int8(pesos, bloco=2)
        self.assertEqual(len(escalas_b), 4)
        self.assertLess(erro_bloco, erro_global)

    def test_fatias_e_manifesto(self):
        regs = ([{"fatia": "conselho", "base": 1, "ajustado": 1}] * 4
                + [{"fatia": "colegiado", "base": 1, "ajustado": 0}, {"fatia": "colegiado", "base": 0, "ajustado": 0}])
        r = comparar_por_fatia(regs)
        self.assertEqual(r["pioras"], ["colegiado"])
        self.assertFalse(r["aprovar"])
        m1 = manifesto([{"ata": 1}], "base-pequeno-v1", "lora-atas-v3", {"r": 16, "lr": 1e-4})
        m2 = manifesto([{"ata": 2}], "base-pequeno-v1", "lora-atas-v3", {"r": 16, "lr": 1e-4})
        self.assertNotEqual(m1["conjunto_sha256"], m2["conjunto_sha256"])


if __name__ == "__main__":
    unittest.main()
