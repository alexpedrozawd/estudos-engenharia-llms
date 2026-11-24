"""Testes offline do Laboratório 01."""
import io
import json
import math
import os
import unittest
from unittest.mock import patch

from lab_01_fundamentos.tokens_e_amostragem import (
    amostrar_token,
    estimar_tokens_idioma,
    filtrar_top_k_top_p,
    inspecionar_logprobs_remoto,
    softmax,
    tokenizar_didatico,
)


class TestLab01Fundamentos(unittest.TestCase):
    def test_tokenizacao_e_custo_relativo_por_idioma(self):
        tokens = tokenizar_didatico("reembolsável!")
        self.assertGreaterEqual(len(tokens), 3)
        texto = "Prazo oficial de matrícula"
        self.assertGreater(estimar_tokens_idioma(texto, "my"), estimar_tokens_idioma(texto, "en"))

    def test_softmax_temperatura_zero_e_alta(self):
        guloso = softmax([1.0, 3.0, 0.5], temperatura=0.0)
        self.assertEqual(guloso, [0.0, 1.0, 0.0])
        quente = softmax([1.0, 3.0, 0.5], temperatura=2.0)
        frio = softmax([1.0, 3.0, 0.5], temperatura=0.5)
        self.assertAlmostEqual(sum(quente), 1.0, places=6)
        self.assertGreater(frio[1], quente[1])

    def test_top_k_top_p_e_amostragem_deterministica(self):
        cands = [("cinco", 2.5), ("tres", 2.0), ("dez", 0.4), ("azul", -2.0)]
        filtrados = filtrar_top_k_top_p(cands, temperatura=1.0, top_k=2, top_p=0.95)
        self.assertEqual([t for t, _ in filtrados], ["cinco", "tres"])
        t1, lp1 = amostrar_token(cands, temperatura=0.8, top_k=3, top_p=0.9, semente=42)
        t2, lp2 = amostrar_token(cands, temperatura=0.8, top_k=3, top_p=0.9, semente=42)
        self.assertEqual((t1, lp1), (t2, lp2))
        self.assertLessEqual(lp1, 0.0)
        self.assertFalse(math.isnan(lp1))

    def test_inspecionar_logprobs_mock_e_http_mockado(self):
        res_off = inspecionar_logprobs_remoto("Contar token")
        self.assertEqual(res_off["modo"], "offline-mock")
        corpo = json.dumps(
            {
                "choices": [{"message": {"content": "cinco"}}],
                "usage": {"prompt_tokens": 5, "completion_tokens": 1},
            }
        ).encode("utf-8")

        class RespFake(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.close()

        with patch.dict(os.environ, {"OPENAI_API_KEY": "chave-teste"}):
            res_http = inspecionar_logprobs_remoto("Oi", opener=lambda req, timeout=15.0: RespFake(corpo))
        self.assertEqual(res_http["modo"], "http")
        self.assertEqual(res_http["texto"], "cinco")


if __name__ == "__main__":
    unittest.main()
