"""Testes unitários do cliente neutro de LLM (offline com mocks)."""
import io
import json
import unittest
from unittest.mock import MagicMock

from comum.cliente_llm import (
    ClienteHTTPAnthropic,
    ClienteHTTPGemini,
    ClienteHTTPOllama,
    ClienteHTTPOpenAICompativel,
    ClienteMockDeterministico,
    RespostaLLM,
    chamar_http_json,
    criar_cliente_por_ambiente,
)


def _fake_opener(resposta: dict, capturas: list):
    corpo = json.dumps(resposta).encode("utf-8")

    class _Resp(io.BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()

    def _abrir(req, timeout=30.0):
        capturas.append(
            {
                "url": req.full_url,
                "headers": {k.lower(): v for k, v in req.header_items()},
                "payload": json.loads(req.data.decode("utf-8")),
                "timeout": timeout,
            }
        )
        return _Resp(corpo)

    return _abrir


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

    def test_adaptadores_http_openai_anthropic_gemini_ollama_sem_rede(self):
        reqs_oai = []
        oai = ClienteHTTPOpenAICompativel(
            modelo="gpt-teste",
            api_key="sk-falso",
            opener=_fake_opener(
                {
                    "model": "gpt-teste",
                    "choices": [{"message": {"content": "ok openai"}}],
                    "usage": {
                        "prompt_tokens": 12,
                        "completion_tokens": 3,
                        "prompt_tokens_details": {"cached_tokens": 8},
                    },
                },
                reqs_oai,
            ),
        )
        r_oai = oai.completar("Olá", sistema="Regra")
        self.assertEqual(r_oai.texto, "ok openai")
        self.assertEqual(r_oai.tokens_cache, 8)
        self.assertEqual(reqs_oai[0]["headers"]["authorization"], "Bearer sk-falso")

        reqs_ant = []
        ant = ClienteHTTPAnthropic(
            api_key="ant-falsa",
            opener=_fake_opener(
                {
                    "model": "claude-sonnet-5-5",
                    "content": [{"type": "text", "text": "ok anthropic"}],
                    "usage": {"input_tokens": 10, "output_tokens": 4, "cache_read_input_tokens": 6},
                },
                reqs_ant,
            ),
        )
        r_ant = ant.completar("Olá", sistema="Regra")
        self.assertEqual(r_ant.texto, "ok anthropic")
        self.assertEqual(r_ant.tokens_cache, 6)
        self.assertEqual(reqs_ant[0]["headers"]["x-api-key"], "ant-falsa")
        self.assertEqual(reqs_ant[0]["headers"]["anthropic-version"], "2023-06-01")

        reqs_gem = []
        gem = ClienteHTTPGemini(
            api_key="gem-falsa",
            opener=_fake_opener(
                {
                    "candidates": [{"content": {"parts": [{"text": "ok gemini"}]}}],
                    "usageMetadata": {"promptTokenCount": 9, "candidatesTokenCount": 2, "cachedContentTokenCount": 5},
                },
                reqs_gem,
            ),
        )
        r_gem = gem.completar("Olá", sistema="Regra")
        self.assertEqual(r_gem.texto, "ok gemini")
        self.assertEqual(r_gem.tokens_cache, 5)
        self.assertEqual(reqs_gem[0]["headers"]["x-goog-api-key"], "gem-falsa")
        self.assertNotIn("key=", reqs_gem[0]["url"])

        reqs_oll = []
        oll = ClienteHTTPOllama(
            opener=_fake_opener(
                {"model": "qwen3:8b", "message": {"content": "ok ollama"}, "prompt_eval_count": 7, "eval_count": 3},
                reqs_oll,
            ),
        )
        r_oll = oll.completar("Olá")
        self.assertEqual(r_oll.texto, "ok ollama")
        self.assertEqual((r_oll.tokens_entrada, r_oll.tokens_saida), (7, 3))
        self.assertFalse(reqs_oll[0]["payload"]["stream"])
        self.assertTrue(reqs_oll[0]["url"].endswith("/api/chat"))

    def test_criar_cliente_por_ambiente(self):
        self.assertIsInstance(criar_cliente_por_ambiente(env={}), ClienteMockDeterministico)
        self.assertIsInstance(
            criar_cliente_por_ambiente(env={"OPENAI_API_KEY": "k1"}),
            ClienteHTTPOpenAICompativel,
        )
        self.assertIsInstance(
            criar_cliente_por_ambiente(env={"ANTHROPIC_API_KEY": "k2"}),
            ClienteHTTPAnthropic,
        )
        self.assertIsInstance(
            criar_cliente_por_ambiente(env={"GEMINI_API_KEY": "k3"}),
            ClienteHTTPGemini,
        )
        self.assertIsInstance(
            criar_cliente_por_ambiente(env={"OLLAMA_HOST": "http://127.0.0.1:11434"}),
            ClienteHTTPOllama,
        )
        self.assertIsInstance(criar_cliente_por_ambiente("ollama", env={}), ClienteHTTPOllama)
        with self.assertRaises(ValueError):
            criar_cliente_por_ambiente("openai", env={})
        with self.assertRaises(ValueError):
            criar_cliente_por_ambiente("desconhecido", env={})


if __name__ == "__main__":
    unittest.main()
