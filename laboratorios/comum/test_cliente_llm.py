"""Testes unitários do cliente neutro de LLM (offline com mocks)."""
import io
import json
import unittest
from unittest.mock import MagicMock

from comum.cliente_llm import ClienteMockDeterministico, RespostaLLM, chamar_http_json


class TestClienteLLM(unittest.TestCase):
    def test_mock_deterministico_registra_chamadas_e_custo_cache(self):
        cli = ClienteMockDeterministico(respostas={"prazo": "O prazo padrão é de 7 dias."})
        resp = cli.completar("Qual o prazo de entrega?", sistema="Você é atendente da Aurora Educação.", esforco="low")
        self.assertIsInstance(resp, RespostaLLM)
        self.assertEqual(resp.texto, "O prazo padrão é de 7 dias.")
        self.assertGreater(resp.tokens_cache, 0)
        self.assertLess(resp.custo_relativo_tokens, resp.tokens_entrada + 3.0 * resp.tokens_saida)
        self.assertEqual(len(cli.chamadas), 1)
        self.assertEqual(cli.chamadas[0]["esforco"], "low")

    def test_chamar_http_json_usa_mock_sem_rede(self):
        fake_resp = io.BytesIO(json.dumps({"ok": True, "modelo": "aurora-test"}).encode("utf-8"))
        ctx = MagicMock()
        ctx.__enter__.return_value = fake_resp
        ctx.__exit__.return_value = False
        opener = MagicMock(return_value=ctx)

        out = chamar_http_json(
            "https://api.exemplo.invalid/v1/responses",
            {"input": "olá"},
            cabecalhos={"Authorization": "Bearer chave-falsa"},
            opener=opener,
        )
        self.assertEqual(out, {"ok": True, "modelo": "aurora-test"})
        opener.assert_called_once()


if __name__ == "__main__":
    unittest.main()
