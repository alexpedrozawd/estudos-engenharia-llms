"""Testes determinísticos do cliente local e do núcleo do benchmark (sem GPU: Ollama simulado em 127.0.0.1).

Uso (Python com -I, só biblioteca padrão):
    python -I ferramentas/testar-llm-local.py
"""
import http.server
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import threading
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def carregar(nome, arquivo):
    s = importlib.util.spec_from_file_location(nome, os.path.join(AQUI, arquivo))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


llm = carregar("llm", "llm-local.py")
bench = carregar("bench", "benchmark-llm-local.py")
RECEBIDOS = []
RESPOSTA = {"conteudo": '{"selecionados":[1],"sem_suporte":false}'}


class FakeOllama(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        RECEBIDOS.append(("GET", self.path, None))
        corpo = json.dumps({"models": []}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        RECEBIDOS.append(("POST", self.path, json.loads(self.rfile.read(n))))
        corpo = json.dumps({"message": {"content": RESPOSTA["conteudo"]}, "prompt_eval_count": 50, "eval_count": 9,
                            "load_duration": 1_000_000_000}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


class Cliente(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FakeOllama)
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.tmp = tempfile.mkdtemp(prefix="llm-teste-")
        llm.BASE = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        llm.LOG = os.path.join(cls.tmp, "chamadas.jsonl")
        llm.vram_usada_mb = lambda: 1800  # GPU livre simulada

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self):
        RECEBIDOS.clear()
        RESPOSTA["conteudo"] = '{"selecionados":[1],"sem_suporte":false}'
        llm.vram_usada_mb = lambda: 1800

    def test_payload_deterministico_e_estruturado(self):
        esquema = {"type": "object", "properties": {"selecionados": {"type": "array"}}}
        obj, info = llm.chat("qwen3.8:27b-ud-iq3_xxs", "sist", "SEGREDO-DO-PROMPT", esquema, tarefa="t")
        self.assertEqual(obj["selecionados"], [1])
        corpo = [r for r in RECEBIDOS if r[0] == "POST"][-1][2]
        self.assertEqual(corpo["model"], "qwen3.8:27b-ud-iq3_xxs")
        self.assertIs(corpo["think"], False)
        self.assertIs(corpo["stream"], False)
        self.assertEqual(corpo["format"], esquema)
        self.assertEqual(corpo["options"]["temperature"], 0)
        self.assertIn("seed", corpo["options"])
        self.assertEqual(info["prompt_tokens"], 50)

    def test_log_registra_tokens_mas_nao_o_texto_do_prompt(self):
        llm.chat("m", "s", "SEGREDO-DO-PROMPT", {"type": "object"}, tarefa="t")
        with open(llm.LOG, encoding="utf-8") as f:
            linha = f.read().splitlines()[-1]
        self.assertNotIn("SEGREDO-DO-PROMPT", linha)
        dados = json.loads(linha)
        self.assertEqual((dados["modelo"], dados["tarefa"], dados["prompt_tokens"], dados["saida_tokens"]), ("m", "t", 50, 9))

    def test_recusa_quando_outros_usam_muita_vram_e_nao_chama_o_modelo(self):
        llm.vram_usada_mb = lambda: 12000
        with self.assertRaises(llm.GpuOcupada):
            llm.chat("m", "s", "u", {"type": "object"})
        self.assertFalse([r for r in RECEBIDOS if r[0] == "POST"])

    def test_recusa_se_nao_consegue_ler_a_vram(self):
        llm.vram_usada_mb = lambda: None
        with self.assertRaises(llm.GpuOcupada):
            llm.chat("m", "s", "u", {"type": "object"})

    def test_resposta_que_nao_e_json_vira_erro_registrado(self):
        RESPOSTA["conteudo"] = "isto não é json"
        with self.assertRaises(ValueError):
            llm.chat("m", "s", "u", {"type": "object"}, tarefa="invalido")
        with open(llm.LOG, encoding="utf-8") as f:
            ultima = json.loads(f.read().splitlines()[-1])
        self.assertEqual(ultima.get("erro"), "json_invalido")

    def test_endereco_fixo_ignora_ollama_host(self):
        antigo = os.environ.get("OLLAMA_HOST")
        os.environ["OLLAMA_HOST"] = "http://servidor-externo.example:11434"
        try:
            novo = carregar("llm2", "llm-local.py")
            self.assertEqual(novo.BASE, "http://127.0.0.1:11434")
        finally:
            if antigo is None:
                os.environ.pop("OLLAMA_HOST", None)
            else:
                os.environ["OLLAMA_HOST"] = antigo


class Nucleo(unittest.TestCase):
    def test_wilson_valores_conhecidos(self):
        lo, hi = bench.wilson(0, 18)
        self.assertAlmostEqual(lo, 0.0, places=6)
        self.assertAlmostEqual(hi, 3.8416 / (18 + 3.8416), places=3)
        lo, hi = bench.wilson(18, 18)
        self.assertAlmostEqual(hi, 1.0, places=6)
        self.assertAlmostEqual(lo, 18 / (18 + 3.8416), places=3)
        self.assertEqual(bench.wilson(0, 0), (0.0, 0.0))

    def test_chunks_cobrem_todas_as_linhas(self):
        linhas = [f"linha numero {i} com algum texto de enchimento para ocupar espaço" for i in range(60)]
        chunks = bench.fazer_chunks("\n\n".join(linhas))
        for l in linhas:
            self.assertTrue(any(l in c for c in chunks), l)
        self.assertGreater(len(chunks), 5)

    def test_cobre_e_ranking_lexico(self):
        texto = "\n".join(["Introdução sem relação com o tema.", "O cache de prompt reduz o custo de leitura dos tokens repetidos.",
                           "Outro assunto qualquer sobre filas.", "Mais enchimento " * 40, "Nada aqui.", "Texto final."])
        chunks = bench.fazer_chunks(texto, alvo=120, passo=60)
        top = bench.ranking_lexico(chunks, "prompt cache cost reading tokens", 3)
        self.assertTrue(bench.cobre("O cache de prompt reduz o custo de leitura dos tokens repetidos.", chunks[top[0]]))
        self.assertTrue(all(abs(a - b) >= 2 for a in top for b in top if a != b))
        self.assertFalse(bench.cobre("A lua orbita a terra em vinte e sete dias.", chunks[top[0]]))
        self.assertEqual(bench.ranking_lexico(chunks, "xyzzy plugh", 3), [])

    def test_prompt_nao_pede_citacao_e_traz_afirmacao_e_trechos(self):
        p = bench.prompt("A afirmação X.", ["trecho zero", "trecho um"])
        self.assertIn("A afirmação X.", p)
        self.assertIn("[1] trecho um", p)
        self.assertIn("sem_suporte", p)


@unittest.skipUnless(os.path.isdir(bench.TEXTOS) and os.listdir(bench.TEXTOS), "cache-fontes/textos ausente (rode fontes.py baixar e extrair)")
class CorpusReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.casos = bench.montar_casos()

    def ler(self, fonte):
        with open(os.path.join(bench.TEXTOS, fonte + ".txt"), encoding="utf-8", errors="replace") as f:
            return f.read()

    def test_quantidade_de_casos(self):
        self.assertEqual(sum(c["tipo"] == "pos" for c in self.casos), 36)
        self.assertEqual(sum(c["tipo"] == "neg" for c in self.casos), 18)

    def test_o_gabarito_aparece_em_algum_trecho_da_propria_fonte(self):
        sem = [c["id"] for c in self.casos if c["tipo"] == "pos" and not any(bench.cobre(c["gold"], ch) for ch in bench.fazer_chunks(self.ler(c["fonte"])))]
        self.assertEqual(sem, [], "a fatiação perdeu o gabarito destes casos")

    def test_controles_negativos_nao_tem_o_gabarito_na_fonte_sorteada(self):
        ouro = {c["id"]: c["gold"] for c in self.casos if c["tipo"] == "pos"}
        for c in self.casos:
            if c["tipo"] != "neg":
                continue
            origem = c["id"].split("~")[0]
            achou = any(bench.cobre(ouro[origem], ch) for ch in bench.fazer_chunks(self.ler(c["fonte"])))
            self.assertFalse(achou, f"controle {c['id']} não é negativo: a fonte tem o trecho da afirmação")

    def test_negativos_usam_fonte_diferente_da_original(self):
        orig = {c["id"]: c["fonte"] for c in self.casos if c["tipo"] == "pos"}
        for c in self.casos:
            if c["tipo"] == "neg":
                self.assertNotEqual(orig[c["id"].split("~")[0]], c["fonte"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
