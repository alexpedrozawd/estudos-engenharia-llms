"""Testes determinísticos do fontes.py (sem internet: servidor HTTP local em 127.0.0.1).

Uso (Python com -I, só biblioteca padrão):
    python -I ferramentas/testar-fontes.py
"""
import contextlib
import glob
import http.server
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
spec = importlib.util.spec_from_file_location("fontes", os.path.join(AQUI, "fontes.py"))
fontes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fontes)

CABECALHOS = []


class Servidor(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        CABECALHOS.append(dict(self.headers))
        if self.path == "/ok.html":
            corpo = "<html><body><nav>menu</nav><p>Primeira linha.</p><p>O cache de prompt reduz o custo de leitura.</p></body></html>".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        elif self.path == "/grande":
            corpo = b"x" * 5000
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
        elif self.path == "/redireciona":
            self.send_response(302)
            self.send_header("Location", "http://dominio-nao-permitido.example/x")
            corpo = b""
        elif self.path == "/arquivo.pdf":
            corpo = b"%PDF-1.4 falso"
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
        else:
            self.send_response(404)
            corpo = b""
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


class Rede(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Servidor)
        cls.porta = cls.srv.server_address[1]
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.porta}"
        cls.permitidos = {"127.0.0.1"}

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def test_baixa_pagina_permitida_sem_dados_do_projeto(self):
        CABECALHOS.clear()
        corpo, tipo = fontes.baixar_url(self.base + "/ok.html", self.permitidos, permitir_http_local=True)
        self.assertIn(b"cache de prompt", corpo)
        self.assertEqual(tipo, "text/html")
        h = {k.lower(): v for k, v in CABECALHOS[-1].items()}
        self.assertEqual(h["user-agent"], fontes.AGENTE)
        for proibido in ("cookie", "authorization", "referer"):
            self.assertNotIn(proibido, h)
        tudo = " ".join(h.values()).lower()
        for nome in ("apsrv", "alexandre", "estudos-engenharia", "pedroza"):
            self.assertNotIn(nome, tudo)

    def test_recusa_http_fora_do_localhost_e_dominio_fora_da_lista(self):
        with self.assertRaises(ValueError):
            fontes.baixar_url("http://exemplo.com/x", {"exemplo.com"})
        with self.assertRaises(ValueError):
            fontes.baixar_url("https://outro.example/x", {"exemplo.com"})
        # sem a permissão explícita, o http local também é recusado
        with self.assertRaises(ValueError):
            fontes.baixar_url(self.base + "/ok.html", self.permitidos)

    def test_bloqueia_redirecionamento_para_dominio_nao_permitido(self):
        with self.assertRaises(urllib.error.URLError) as c:
            fontes.baixar_url(self.base + "/redireciona", self.permitidos, permitir_http_local=True)
        self.assertIn("bloqueado", str(c.exception))

    def test_limite_de_tamanho(self):
        with self.assertRaises(ValueError):
            fontes.baixar_url(self.base + "/grande", self.permitidos, permitir_http_local=True, limite=1000)

    def test_extensao_por_conteudo(self):
        corpo, tipo = fontes.baixar_url(self.base + "/arquivo.pdf", self.permitidos, permitir_http_local=True)
        self.assertEqual(fontes.extensao(self.base + "/arquivo.pdf", tipo, corpo), ".pdf")
        self.assertEqual(fontes.extensao("https://a.b/x", "text/html", b"<html>"), ".html")
        self.assertEqual(fontes.extensao("https://a.b/x.md", "text/plain", b"# t"), ".md")


class Manifesto(unittest.TestCase):
    def test_manifesto_confere_com_contagem_independente(self):
        total = 0
        for p in glob.glob(os.path.join(RAIZ, "pacote-de-fontes-*.md")):
            with open(p, encoding="utf-8") as f:
                for linha in f:
                    if re.match(r"^\| `[^`]+` \|.*https?://.*\| `[0-9a-f]{16}` \|\s*$", linha):
                        total += 1
        itens = fontes.manifesto()
        self.assertEqual(len(itens), total)
        self.assertGreater(total, 150)
        self.assertTrue(all(i["url"].startswith("https://") for i in itens))

    def test_cache_e_rascunhos_ficam_fora_do_git(self):
        for caminho in ("cache-fontes/bruto/x.html", "rascunho-local/saida.json"):
            r = subprocess.run(["git", "check-ignore", "-q", caminho], cwd=RAIZ)
            self.assertEqual(r.returncode, 0, caminho)


class Busca(unittest.TestCase):
    TEXTO = "\n".join(["Introdução geral ao assunto.", "", "O cache de prompt reduz o custo de leitura de tokens repetidos.",
                       "Outro tema sem relação.", "A janela de contexto limita o tamanho da entrada.", "Fim."])

    def test_achar_devolve_a_linha_certa_em_primeiro(self):
        res, total = fontes.achar(self.TEXTO, "custo de leitura do cache de prompt", n=3)
        self.assertEqual(res[0][1], 3)
        self.assertGreaterEqual(total, 4)

    def test_achar_ignora_acento_e_caixa(self):
        res, _ = fontes.achar(self.TEXTO, "JANELA DE CONTEXTO", n=1)
        self.assertEqual(res[0][1], 5)

    def test_achar_sem_termos_em_comum_nao_inventa(self):
        res, _ = fontes.achar(self.TEXTO, "xyzzy plugh", n=3)
        self.assertEqual(res, [])


class Vigencia(unittest.TestCase):
    def test_avaliar_vigencia_classifica_atuais_vencidas_divergentes_e_ausentes(self):
        itens = [
            {"chave": "ok", "hash_bruto": "aaaaaaaaaaaaaaaa"},
            {"chave": "vencida", "hash_bruto": "bbbbbbbbbbbbbbbb"},
            {"chave": "mudou", "hash_bruto": "cccccccccccccccc"},
            {"chave": "ausente", "hash_bruto": "dddddddddddddddd"},
        ]
        indice = {
            "ok": {"hash": "aaaaaaaaaaaaaaaa", "data": "2026-11-10"},
            "vencida": {"hash": "bbbbbbbbbbbbbbbb", "data": "2026-09-01"},
            "mudou": {"hash": "eeeeeeeeeeeeeeee", "data": "2026-11-18"},
        }
        res = fontes.avaliar_vigencia(itens, indice, dias=30, hoje="2026-11-23")
        self.assertEqual(res["total"], 4)
        self.assertEqual(res["atuais"], 1)
        self.assertEqual(res["ausentes"], ["ausente"])
        self.assertEqual([k for k, _, _ in res["vencidas"]], ["vencida"])
        self.assertEqual(res["divergentes"], [("mudou", "cccccccccccccccc", "eeeeeeeeeeeeeeee")])

    def test_cmd_vigencia_estrito_retorna_um_quando_ha_pendencia(self):
        tmp = tempfile.mkdtemp(prefix="fontes-vigencia-")
        try:
            ind = os.path.join(tmp, "indice.json")
            with open(ind, "w", encoding="utf-8") as f:
                json.dump({"bea": {"hash": "0000000000000000", "data": "2026-11-19"}}, f)
            with contextlib.redirect_stdout(io.StringIO()):
                rc = fontes.cmd_vigencia(
                    pacote="pacote-de-fontes-capitulo-14-selecao-e-roteamento-2026-11-17.md",
                    dias=30,
                    estrito=True,
                    indice_path=ind,
                    hoje="2026-11-23",
                )
            self.assertEqual(rc, 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class Importacao(unittest.TestCase):
    def test_importar_propaga_mesma_url_atualiza_indice_e_extrai(self):
        tmp = tempfile.mkdtemp(prefix="fontes-importar-")
        try:
            manuais = os.path.join(tmp, "manuais")
            bruto = os.path.join(tmp, "bruto")
            textos = os.path.join(tmp, "textos")
            ind = os.path.join(tmp, "indice.json")
            os.makedirs(manuais, exist_ok=True)
            html = "<html><body><p>Conteudo salvo pelo navegador.</p></body></html>"
            with open(os.path.join(manuais, "k1.htm"), "w", encoding="utf-8") as f:
                f.write(html)
            itens = [
                {"chave": "k1", "url": "https://exemplo.test/artigo", "hash_bruto": "0000000000000000"},
                {"chave": "k2", "url": "https://exemplo.test/artigo", "hash_bruto": "0000000000000000"},
            ]
            with contextlib.redirect_stdout(io.StringIO()):
                rc = fontes.cmd_importar(pasta=manuais, bruto=bruto, textos=textos, indice_path=ind, itens=itens)
            self.assertEqual(rc, 0)
            with open(ind, encoding="utf-8") as f:
                reg = json.load(f)
            self.assertEqual(set(reg), {"k1", "k2"})
            self.assertEqual(reg["k1"]["origem"], "manual")
            self.assertEqual(reg["k1"]["hash"], reg["k2"]["hash"])
            self.assertTrue(os.path.isfile(os.path.join(bruto, "k1.html")))
            self.assertTrue(os.path.isfile(os.path.join(bruto, "k2.html")))
            with open(os.path.join(textos, "k2.txt"), encoding="utf-8") as f:
                self.assertIn("Conteudo salvo pelo navegador.", f.read())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_importar_reprova_chave_fora_do_manifesto(self):
        tmp = tempfile.mkdtemp(prefix="fontes-importar-erro-")
        try:
            manuais = os.path.join(tmp, "manuais")
            os.makedirs(manuais, exist_ok=True)
            with open(os.path.join(manuais, "desconhecida.html"), "w", encoding="utf-8") as f:
                f.write("<html></html>")
            with contextlib.redirect_stdout(io.StringIO()):
                rc = fontes.cmd_importar(pasta=manuais, bruto=os.path.join(tmp, "b"), textos=os.path.join(tmp, "t"),
                                         indice_path=os.path.join(tmp, "i.json"), itens=[])
            self.assertEqual(rc, 1)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
