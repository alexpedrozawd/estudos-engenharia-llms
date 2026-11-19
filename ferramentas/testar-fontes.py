"""Testes determinísticos do fontes.py (sem internet: servidor HTTP local em 127.0.0.1).

Uso (Python com -I, só biblioteca padrão):
    python -I ferramentas/testar-fontes.py
"""
import glob
import http.server
import importlib.util
import os
import re
import subprocess
import sys
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
            for linha in open(p, encoding="utf-8"):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
