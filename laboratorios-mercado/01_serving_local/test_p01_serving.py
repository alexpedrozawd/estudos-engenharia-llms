"""Smoke-tests offline do projeto 01 (sem rede: httpx.MockTransport e relógio falso)."""
import asyncio
import json
import os
import tempfile
import unittest

import httpx

import mercado_base as mb
import serving_bench as sb


class RelogioFalso:
    """Avança 10 ms a cada leitura: tempos determinísticos."""

    def __init__(self):
        self.t = 0.0

    def __call__(self):
        self.t += 0.010
        return self.t


def corpo_sse(pedacos, usage=None, raciocinio=()):
    linhas = []
    for r in raciocinio:
        linhas.append("data: " + json.dumps({"choices": [{"delta": {"reasoning": r}}]}))
    for p in pedacos:
        linhas.append("data: " + json.dumps({"choices": [{"delta": {"content": p}}]}))
    if usage:
        linhas.append("data: " + json.dumps({"choices": [], "usage": usage}))
    linhas.append("data: [DONE]")
    return ("\n\n".join(linhas) + "\n\n").encode("utf-8")


class TestMetricas(unittest.TestCase):
    def test_percentil_interpolado(self):
        self.assertEqual(mb.percentil([10, 20, 30, 40], 50), 25.0)
        self.assertAlmostEqual(mb.percentil([10, 20, 30, 40], 95), 38.5)
        self.assertEqual(mb.percentil([7], 95), 7.0)

    def test_ttft_tpot_e_goodput(self):
        a = sb.Amostra(inicio=0.0, primeiro_token=0.5, fim=1.4, tokens_saida=10)
        self.assertAlmostEqual(a.ttft_ms, 500.0)
        self.assertAlmostEqual(a.tpot_ms, 100.0)
        lenta = sb.Amostra(inicio=0.0, primeiro_token=3.0, fim=4.0, tokens_saida=5)
        falha = sb.Amostra(inicio=0.0, fim=0.1, ok=False, erro="HTTP 500")
        r = sb.resumir([a, lenta, falha], duracao_s=2.0, slo=sb.SLO(ttft_ms=2000, tpot_ms=150))
        self.assertEqual(r["requisicoes"], 3)
        self.assertEqual(r["falhas"], 1)
        self.assertEqual(r["goodput_req_s"], 0.5)
        self.assertEqual(r["requisicoes_s"], 1.0)
        self.assertEqual(r["tokens_saida_total"], 15)
        self.assertAlmostEqual(r["fracao_dentro_do_slo"], 0.333)


class TestStream(unittest.TestCase):
    def _transport(self, corpo, status=200):
        def handler(request):
            payload = json.loads(request.content)
            self.assertTrue(payload["stream"])
            self.assertEqual(payload["stream_options"], {"include_usage": True})
            return httpx.Response(status, content=corpo, headers={"content-type": "text/event-stream"})
        return httpx.MockTransport(handler)

    def test_usage_prevalece_sobre_contagem(self):
        corpo = corpo_sse(["Re", "ma", "trícula"], usage={"completion_tokens": 4})
        amostras, _ = asyncio.run(sb.executar_benchmark(
            "http://servico.invalido/v1", "m", ["oi"], requisicoes=3, concorrencia=2,
            transport=self._transport(corpo), relogio=RelogioFalso()))
        self.assertEqual(len(amostras), 3)
        for a in amostras:
            self.assertTrue(a.ok, a.erro)
            self.assertEqual(a.tokens_saida, 4)
            self.assertEqual(a.tokens_fonte, "usage")
            self.assertEqual(a.texto, "Rematrícula")
            self.assertIsNotNone(a.ttft_ms)

    def test_raciocinio_conta_no_ttft_sem_usage(self):
        corpo = corpo_sse(["ok"], raciocinio=["pensando"])
        amostras, _ = asyncio.run(sb.executar_benchmark(
            "http://servico.invalido/v1", "m", ["oi"], requisicoes=1, concorrencia=1,
            transport=self._transport(corpo), relogio=RelogioFalso()))
        self.assertEqual(amostras[0].tokens_saida, 2)
        self.assertEqual(amostras[0].tokens_fonte, "contagem_de_eventos")
        self.assertEqual(amostras[0].texto, "ok")

    def test_erro_http_vira_falha(self):
        amostras, _ = asyncio.run(sb.executar_benchmark(
            "http://servico.invalido/v1", "m", ["oi"], requisicoes=1, concorrencia=1,
            transport=self._transport(b"sobrecarga", status=503), relogio=RelogioFalso()))
        self.assertFalse(amostras[0].ok)
        self.assertIn("HTTP 503", amostras[0].erro)

    def test_parametros_invalidos(self):
        with self.assertRaises(ValueError):
            asyncio.run(sb.executar_benchmark("http://x/v1", "m", ["oi"], requisicoes=1, concorrencia=0))


class TestMemoria(unittest.TestCase):
    def test_ollama_ps(self):
        def handler(request):
            self.assertEqual(request.url.path, "/api/ps")
            return httpx.Response(200, json={"models": [{"name": "qwen3:4b", "size": 3000, "size_vram": 1000}]})
        m = sb.medir_memoria_ollama("http://servico.invalido", transport=httpx.MockTransport(handler))
        self.assertEqual(m["modelos"], [{"modelo": "qwen3:4b", "bytes": 3000, "bytes_vram": 1000}])

    def test_proc_status(self):
        with tempfile.TemporaryDirectory() as raiz:
            os.makedirs(os.path.join(raiz, "42"))
            with open(os.path.join(raiz, "42", "status"), "w", encoding="utf-8") as f:
                f.write("Name:\tllama-server\nVmHWM:\t  2048 kB\nVmRSS:\t  1024 kB\n")
            m = sb.medir_memoria_pid(42, raiz_proc=raiz)
        self.assertEqual(m["vmrss_kib"], 1024)
        self.assertEqual(m["vmhwm_kib"], 2048)


if __name__ == "__main__":
    unittest.main()
