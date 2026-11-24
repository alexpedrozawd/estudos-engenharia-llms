"""Testes determinísticos das ferramentas de manutenção do guia (sem LLM, sem rede).

Uso (Python com -I, só biblioteca padrão):
    python -I ferramentas/testar-ferramentas.py            # golden, mutação, idempotência e PDF
    python -I ferramentas/testar-ferramentas.py --rapido   # sem a geração de PDF

Golden: cada número do guia.py é comparado a uma contagem independente (regex e pdfinfo).
Mutação: cópias do guia em pasta temporária recebem um defeito cada; a verificação tem de reprovar
com a mensagem esperada, e a cópia sem defeito (controle) tem de passar. O guia original não é tocado
(hash conferido antes e depois).
"""
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
GUIA = os.path.join(RAIZ, "guia-engenharia-llms.html")
PDF = os.path.join(RAIZ, "guia-engenharia-llms.pdf")
RAPIDO = "--rapido" in sys.argv

spec = importlib.util.spec_from_file_location("guia", os.path.join(AQUI, "guia.py"))
guia = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guia)


def ler_texto(caminho, modo="r"):
    with open(caminho, modo, **({} if "b" in modo else {"encoding": "utf-8", "errors": "replace"})) as f:
        return f.read()


def sha(caminho):
    with open(caminho, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def executar(*args):
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "guia.py"), *args],
                       capture_output=True, text=True, encoding="utf-8", timeout=600)
    return r.returncode, r.stdout + r.stderr


class Golden(unittest.TestCase):
    def test_contagens_conferem_com_contagem_independente(self):
        texto = ler_texto(GUIA)
        c = guia.contagens(GUIA)
        self.assertEqual(c["partes"], len(re.findall(r'<section class="page"', texto)))
        self.assertEqual(c["tabelas"], texto.count("<table"))
        self.assertEqual(c["questoes"], len(set(re.findall(r'<input type="radio" name="([^"]+)"', texto))))
        self.assertEqual(c["gabaritos"], len(re.findall(r'<input type="radio"[^>]*data-correta="true"', texto)))
        self.assertEqual(c["bytes_html"], os.path.getsize(GUIA))
        glos = re.search(r'<section class="page" id="glossario".*?</section>', texto, re.S).group(0)
        self.assertEqual(c["glossario_termos"], len(re.findall(r"<dt[ >]", glos)))
        self.assertEqual(c["diagramas_svg"], len(re.findall(r"<svg\b", texto)))
        self.assertEqual(c["molduras_imagem"], len(re.findall(r'data-imagem="[^"]+"', texto)))

    def test_mapa_devolve_as_partes_do_prefixo(self):
        rc, out = executar("mapa", "14.2")
        self.assertEqual(rc, 0)
        ids = [l.split("\t")[0] for l in out.strip().splitlines()]
        self.assertEqual(ids, ["unidade-14-2a", "unidade-14-2b", "unidade-14-2c"])
        linha_ini = int(out.splitlines()[0].split("\t")[1].split("-")[0])
        self.assertIn('id="unidade-14-2a"', ler_texto(GUIA).splitlines()[linha_ini - 1])

    def test_mapa_respeita_fronteira_de_numero(self):
        rc, out = executar("mapa", "1")
        self.assertEqual(rc, 0)
        ids = [l.split("\t")[0] for l in out.strip().splitlines()]
        self.assertIn("capitulo-1", ids)
        self.assertIn("questoes-capitulo-1", ids)
        self.assertNotIn("capitulo-10", ids)
        self.assertNotIn("unidade-10-1a", ids)

    def test_mapa_prefixo_inexistente_falha(self):
        rc, _ = executar("mapa", "99.9")
        self.assertEqual(rc, 1)

    def test_verificar_aprova_o_guia_atual_e_e_idempotente(self):
        antes = sha(GUIA)
        rc1, out1 = executar("verificar")
        rc2, out2 = executar("verificar")
        self.assertEqual((rc1, rc2), (0, 0), out1)
        self.assertEqual(out1, out2)
        self.assertEqual(sha(GUIA), antes)


class Mutacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pasta = tempfile.mkdtemp(prefix="guia-mutacao-")
        cls.texto = ler_texto(GUIA)
        # links locais do guia são relativos à raiz do projeto: copia também a pasta para o controle passar
        for nome in os.listdir(RAIZ):
            if nome.endswith(".md"):
                shutil.copy2(os.path.join(RAIZ, nome), cls.pasta)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.pasta, ignore_errors=True)

    def rodar(self, texto, nome):
        caminho = os.path.join(self.pasta, nome + ".html")
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
        rc, out = executar("verificar", "--guia", caminho)
        return rc, out

    def trocar(self, antigo, novo, vezes=1):
        self.assertIn(antigo, self.texto, f"âncora do teste ausente: {antigo[:50]}")
        return self.texto.replace(antigo, novo, vezes)

    def test_controle_sem_defeito_passa(self):
        rc, out = self.rodar(self.texto, "controle")
        self.assertEqual(rc, 0, out)

    def esperar_falha(self, texto, nome, trecho):
        rc, out = self.rodar(texto, nome)
        self.assertEqual(rc, 1, out)
        self.assertIn(trecho, out)

    def test_id_duplicado(self):
        self.esperar_falha(self.trocar('id="unidade-1-1b"', 'id="unidade-1-1a"'), "iddup", "FALHA ids únicos")

    def test_gabarito_removido(self):
        self.esperar_falha(self.trocar('data-correta="true"', 'data-correta="false"'), "gab", "FALHA")

    def test_link_interno_quebrado(self):
        self.esperar_falha(self.trocar('href="#capitulo-2"', 'href="#capitulo-2-inexistente"'), "link", "FALHA")

    def test_pagina_fora_de_ordem(self):
        achado = re.search(r'(<span class="page-number" role="img" aria-label="Página 5">)5(</span>)', self.texto)
        self.assertIsNotNone(achado)
        self.esperar_falha(self.texto.replace(achado.group(0), achado.group(1) + "55" + achado.group(2), 1), "pag", "FALHA numeração")

    def test_dfn_repetido(self):
        achado = re.search(r"<dfn>([^<]+)</dfn>", self.texto)
        self.assertIsNotNone(achado)
        novo = self.texto.replace(achado.group(0), achado.group(0) + " e " + achado.group(0), 1)
        self.esperar_falha(novo, "dfn", "FALHA cada termo definido uma vez")

    def test_tabela_sem_rolagem(self):
        novo = self.trocar("</main>", "<table><tr><td>x</td></tr></table></main>")
        self.esperar_falha(novo, "tab", "FALHA toda tabela dentro de .rolagem")

    def test_unidade_fora_do_sumario(self):
        # tira do sumário o link da primeira parte da unidade 2.1 (a seção continua existindo)
        novo = self.trocar('<a href="#unidade-2-1a"', '<a href="#capitulo-2"', 1)
        self.esperar_falha(novo, "sum", "FALHA capítulos, questões e primeira parte")

    def test_svg_sem_role_img(self):
        novo = self.trocar('<svg role="img"', '<svg', 1)
        self.esperar_falha(novo, "svg_role", "FALHA")

    def test_svg_sem_desc(self):
        achado = re.search(r"<desc\b[^>]*>.*?</desc>", self.texto, re.S)
        self.assertIsNotNone(achado)
        self.esperar_falha(self.texto.replace(achado.group(0), "", 1), "svg_desc", "FALHA")

    def test_svg_sem_viewbox(self):
        achado = re.search(r'<svg\b[^>]*?(viewBox="[^"]+")', self.texto)
        self.assertIsNotNone(achado)
        self.esperar_falha(self.texto.replace(achado.group(1), "", 1), "svg_vb", "FALHA")

    def test_svg_com_script(self):
        novo = self.trocar("</svg>", "<script></script></svg>", 1)
        self.esperar_falha(novo, "svg_scr", "FALHA")


@unittest.skipIf(RAPIDO, "geração de PDF desligada por --rapido")
class Pdf(unittest.TestCase):
    def test_pdf_tem_as_mesmas_paginas_do_pdf_versionado(self):
        saida = os.path.join(tempfile.mkdtemp(prefix="guia-pdf-teste-"), "g.pdf")
        antes = sha(PDF)
        rc, out = executar("pdf", "--saida", saida)
        self.assertEqual(rc, 0, out)
        self.assertEqual(guia.paginas_pdf(saida), guia.paginas_pdf(PDF))
        self.assertEqual(sha(PDF), antes, "pdf sem --substituir não pode tocar no PDF do projeto")

    def test_substituir_exige_motivo_e_faz_copia(self):
        rc, _ = executar("pdf", "--substituir")
        self.assertEqual(rc, 1)
        tmp = tempfile.mkdtemp(prefix="guia-subst-")
        try:
            antigo = os.path.join(tmp, "guia-engenharia-llms.pdf")
            with open(antigo, "wb") as f:
                f.write(b"%PDF-antigo")
            guia.RAIZ, guia.PDF_PADRAO = tmp, antigo
            self.assertEqual(guia.cmd_pdf(GUIA, None, None, True, "teste"), 0)
            copias = [os.path.join(d, n) for d, _, ns in os.walk(os.path.join(tmp, "arquivo")) for n in ns]
            self.assertEqual(len(copias), 1)
            self.assertEqual(ler_texto(copias[0], "rb"), b"%PDF-antigo")
            self.assertGreater(os.path.getsize(antigo), 1000)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.argv = [a for a in sys.argv if a != "--rapido"]
    unittest.main(verbosity=2)
