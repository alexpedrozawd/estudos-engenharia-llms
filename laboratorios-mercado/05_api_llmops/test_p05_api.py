"""Smoke-tests offline do projeto 05: provedores falsos, relógio/sono injetados e spans em memória."""
import asyncio
import json
import random
import unittest

import httpx
from fastapi.testclient import TestClient

import llmops_api as api
import llmops_resiliencia as res
import llmops_telemetria as tel


class ProvedorFalso:
    modelo = "falso-1"

    def __init__(self, tokens=("Olá", ", ", "aluno", "."), falhas_antes=0, erro=None, pii=False):
        self.tokens = list(tokens) + (["CPF 123.456.789-09"] if pii else [])
        self.falhas_antes = falhas_antes
        self.erro = erro or res.ErroTransitorio("HTTP 503")
        self.chamadas = 0
        self.fechados = 0
        self.entregues = 0

    async def completar(self, prompt, max_tokens):
        self.chamadas += 1
        if self.chamadas <= self.falhas_antes:
            raise self.erro
        return {"texto": "".join(self.tokens), "tokens_entrada": 3, "tokens_saida": len(self.tokens)}

    async def gerar(self, prompt, max_tokens):
        self.chamadas += 1
        if self.chamadas <= self.falhas_antes:
            raise self.erro
        try:
            for t in self.tokens:
                self.entregues += 1
                yield t
        finally:
            self.fechados += 1


async def sem_dormir(_s):
    return None


def cliente(provedor, **kw):
    tp, mem = tel.configurar_telemetria("memoria")
    app = api.criar_app(provedor, tracer_provider=tp, dormir=sem_dormir, rng=random.Random(0), **kw)
    return app, mem


def eventos_sse(corpo):
    saida = []
    for bloco in corpo.strip().split("\n\n"):
        linhas = dict(l.split(": ", 1) for l in bloco.splitlines())
        saida.append((linhas["event"], json.loads(linhas["data"])))
    return saida


class TestResiliencia(unittest.TestCase):
    def test_backoff_full_jitter_limitado(self):
        rng = random.Random(1)
        atrasos = [res.atraso_backoff(i, base_s=0.5, teto_s=4, rng=rng) for i in range(8)]
        self.assertTrue(all(0 <= a <= min(4, 0.5 * 2 ** i) for i, a in enumerate(atrasos)))

    def test_retry_respeita_retry_after_e_nao_repete_permanente(self):
        dormidas, n = [], {"c": 0}

        async def dormir(s):
            dormidas.append(s)

        async def falha_429():
            n["c"] += 1
            if n["c"] < 3:
                raise res.classificar_status(429, "2")
            return "ok"

        self.assertEqual(asyncio.run(res.com_retry(falha_429, tentativas=3, dormir=dormir)), "ok")
        self.assertEqual(dormidas, [2.0, 2.0])

        async def falha_400():
            n["c"] += 1
            raise res.classificar_status(400)

        n["c"] = 0
        with self.assertRaises(res.ErroPermanente):
            asyncio.run(res.com_retry(falha_400, tentativas=5, dormir=dormir))
        self.assertEqual(n["c"], 1)

    def test_disjuntor_ciclo_completo(self):
        t = {"agora": 0.0}
        d = res.Disjuntor(limite_falhas=2, tempo_aberto_s=10, relogio=lambda: t["agora"])
        d.registrar_falha()
        self.assertEqual(d.estado, "fechado")
        d.registrar_falha()
        self.assertEqual(d.estado, "aberto")
        with self.assertRaises(res.CircuitoAberto):
            d.permitir()
        t["agora"] = 10.0
        self.assertEqual(d.estado, "meio_aberto")
        d.permitir()  # uma sonda passa
        with self.assertRaises(res.CircuitoAberto):
            d.permitir()  # a segunda espera o resultado da sonda
        d.registrar_falha()
        self.assertEqual(d.estado, "aberto")
        t["agora"] = 25.0
        d.permitir()
        d.registrar_sucesso()
        self.assertEqual(d.estado, "fechado")


class TestAPI(unittest.TestCase):
    def test_resposta_com_retry_span_e_avaliacao(self):
        prov = ProvedorFalso(falhas_antes=2)
        app, mem = cliente(prov)
        with TestClient(app) as c:
            r = c.post("/v1/respostas", json={"prompt": "oi", "id_requisicao": "req-1"})
            self.assertEqual(r.status_code, 200, r.text)
            corpo = r.json()
            self.assertEqual(corpo["tentativas"], 3)
            self.assertEqual(corpo["texto"], "Olá, aluno.")
            self.assertEqual(corpo["avaliacao"], {"aprovada": True, "falhas": []})
            m = c.get("/v1/metricas").json()
        self.assertEqual(m["contadores"]["retries"], 2)
        span = mem.get_finished_spans()[0]
        self.assertEqual(span.attributes["gen_ai.operation.name"], "chat")
        self.assertEqual(span.attributes["gen_ai.usage.output_tokens"], 4)
        self.assertNotIn("oi", json.dumps(dict(span.attributes), ensure_ascii=False).replace("aurora", ""))

    def test_validacao_de_entrada(self):
        app, _ = cliente(ProvedorFalso())
        with TestClient(app) as c:
            self.assertEqual(c.post("/v1/respostas", json={"prompt": ""}).status_code, 422)
            self.assertEqual(c.post("/v1/respostas", json={"prompt": "x", "max_tokens": 99999}).status_code, 422)
            self.assertEqual(c.post("/v1/respostas", json={"prompt": "x", "id_requisicao": "a b"}).status_code, 422)

    def test_disjuntor_abre_e_responde_503(self):
        app, _ = cliente(ProvedorFalso(falhas_antes=99), disjuntor=res.Disjuntor(limite_falhas=2, tempo_aberto_s=60),
                         tentativas=1)
        with TestClient(app) as c:
            self.assertEqual(c.post("/v1/respostas", json={"prompt": "a"}).status_code, 502)
            self.assertEqual(c.post("/v1/respostas", json={"prompt": "a"}).status_code, 502)
            r = c.post("/v1/respostas", json={"prompt": "a"})
            self.assertEqual(r.status_code, 503)
            self.assertIn("Retry-After", r.headers)
            self.assertEqual(c.get("/saude").json()["disjuntor"], "aberto")

    def test_stream_sse_com_retry_antes_do_primeiro_token(self):
        prov = ProvedorFalso(falhas_antes=1)
        app, _ = cliente(prov)
        with TestClient(app) as c:
            r = c.post("/v1/respostas/stream", json={"prompt": "oi", "id_requisicao": "s-1"})
            self.assertEqual(r.headers["content-type"].split(";")[0], "text/event-stream")
            evs = eventos_sse(r.text)
        self.assertEqual([e for e, _ in evs], ["delta"] * 4 + ["fim"])
        self.assertEqual("".join(d["texto"] for e, d in evs if e == "delta"), "Olá, aluno.")
        self.assertEqual(evs[-1][1]["id_requisicao"], "s-1")
        self.assertEqual(prov.fechados, 1)

    def test_avaliacao_continua_detecta_pii(self):
        app, _ = cliente(ProvedorFalso(pii=True), avaliador=tel.AvaliadorContinuo(minimo_amostras=1))
        with TestClient(app) as c:
            r = c.post("/v1/respostas", json={"prompt": "dados"})
            self.assertEqual(r.json()["avaliacao"], {"aprovada": False, "falhas": ["pii"]})
            resumo = c.get("/v1/metricas").json()["avaliacao_continua"]
        self.assertEqual(resumo["falhas"]["pii"], 1)
        self.assertTrue(resumo["alerta"])


class TestCancelamento(unittest.TestCase):
    def test_desconexao_interrompe_upstream(self):
        prov = ProvedorFalso(tokens=[f"t{i}" for i in range(100)])
        contadores = {"sucessos": 0, "falhas": 0, "retries": 0, "cancelados": 0, "rejeitados_disjuntor": 0}
        tp, mem = tel.configurar_telemetria("memoria")
        estado = {"enviados": 0}

        async def desconectado():
            return estado["enviados"] >= 3

        async def consumir():
            gen = api.gerar_eventos(prov, api.PedidoResposta(prompt="oi"), "c-1", desconectado=desconectado,
                                    disjuntor=res.Disjuntor(), contadores=contadores,
                                    avaliador=tel.AvaliadorContinuo(), tracer=tp.get_tracer("t"), dormir=sem_dormir)
            async for _ in gen:
                estado["enviados"] += 1

        asyncio.run(consumir())
        self.assertEqual(estado["enviados"], 3)
        self.assertEqual(contadores["cancelados"], 1)
        self.assertEqual(prov.fechados, 1)
        self.assertLess(prov.entregues, 10)
        self.assertTrue(mem.get_finished_spans()[0].attributes["aurora.cancelado"])

    def test_provedor_http_stream_e_erros(self):
        def handler(request):
            corpo = json.loads(request.content)
            if corpo["messages"][0]["content"] == "falha":
                return httpx.Response(429, headers={"retry-after": "1"})
            sse = "".join("data: " + json.dumps({"choices": [{"delta": {"content": t}}]}) + "\n\n" for t in ("a", "b"))
            return httpx.Response(200, content=(sse + "data: [DONE]\n\n").encode())

        async def rodar():
            p = api.ProvedorOpenAICompativel("http://servico.invalido/v1", "m", transport=httpx.MockTransport(handler))
            try:
                tokens = [t async for t in p.gerar("oi", 5)]
                with self.assertRaises(res.ErroTransitorio) as cm:
                    [t async for t in p.gerar("falha", 5)]
                return tokens, cm.exception.retry_after_s
            finally:
                await p.fechar()

        self.assertEqual(asyncio.run(rodar()), (["a", "b"], 1.0))


if __name__ == "__main__":
    unittest.main()
