"""Testes determinísticos de ferramentas/livros.py (sem ler livros reais nem gastar LLM).

Uso (Python com -I, só biblioteca padrão):
    python -I ferramentas/testar-livros.py
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
spec = importlib.util.spec_from_file_location("livros", os.path.join(AQUI, "livros.py"))
livros = importlib.util.module_from_spec(spec)
spec.loader.exec_module(livros)


def criar_pdf_sintetico(caminho, textos_por_pagina):
    """Gera um PDF 1.4 mínimo válido com N páginas de texto simples (sem dependências externas)."""
    objetos = [None] * (3 + 2 * len(textos_por_pagina))
    paginas_ids = []
    font_id = 3
    for i, texto in enumerate(textos_por_pagina):
        page_id = 4 + 2 * i
        content_id = 5 + 2 * i
        paginas_ids.append(f"{page_id} 0 R")
        esc = texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream = f"BT /F1 12 Tf 72 720 Td ({esc}) Tj ET\n".encode("latin-1", errors="replace")
        objetos[page_id - 1] = (
            f"{page_id} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>\nendobj\n"
        ).encode("ascii")
        objetos[content_id - 1] = (
            f"{content_id} 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"endstream\nendobj\n"
        )
    objetos[0] = b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    objetos[1] = f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(paginas_ids)}] /Count {len(paginas_ids)} >>\nendobj\n".encode("ascii")
    objetos[2] = b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"

    corpo = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objetos:
        offsets.append(len(corpo))
        corpo.extend(obj)
    xref_pos = len(corpo)
    corpo.extend(f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode("ascii"))
    for off in offsets[1:]:
        corpo.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    corpo.extend(f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii"))
    with open(caminho, "wb") as f:
        f.write(corpo)


class LivrosTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="livros-teste-")
        cls.pdfs = os.path.join(cls.tmp, "pdfs")
        cls.saida = os.path.join(cls.tmp, "cache")
        os.makedirs(cls.pdfs, exist_ok=True)
        cls.pdf_path = os.path.join(cls.pdfs, "Livro Teste.pdf")
        criar_pdf_sintetico(cls.pdf_path, [
            "Table of Contents Chapter 1 Intro",
            "Prompt evaluation metrics and perplexity",
            "Data drift and continuous monitoring",
        ])
        cls.catalogo = {"teste": "Livro Teste*.pdf"}

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_extrair_ler_achar_e_png(self):
        rc = livros.cmd_extrair(diretorio=self.pdfs, saida=self.saida, catalogo=self.catalogo)
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.exists(os.path.join(self.saida, "teste.txt")))
        with open(os.path.join(self.saida, "indice.json"), encoding="utf-8") as f:
            ind = json.load(f)
        self.assertEqual(ind["teste"]["paginas"], 3)

        pags = livros.carregar_paginas("teste", saida=self.saida)
        self.assertEqual(len(pags), 3)
        self.assertIn("Prompt evaluation", pags[1])

        res, total = livros.achar_em_paginas(pags, "data drift monitoring", n=2)
        self.assertEqual(total, 3)
        self.assertEqual(res[0][1], 3)

        layout = livros.ler_layout_pdf(self.pdf_path, 2, 2)
        self.assertEqual(layout[0][0], 2)
        self.assertIn("perplexity", layout[0][1])

        png_dest = os.path.join(self.tmp, "p2.png")
        self.assertEqual(livros.cmd_pagina_png("teste", 2, destino=png_dest, saida=self.saida), 0)
        self.assertTrue(os.path.exists(png_dest))
        self.assertGreater(os.path.getsize(png_dest), 500)

    def test_cache_livros_ignorado_pelo_git(self):
        for caminho in ("cache-fontes/livros/ai-engineering.txt", "cache-fontes/livros/paginas/x.png"):
            r = subprocess.run(["git", "check-ignore", "-q", caminho], cwd=RAIZ)
            self.assertEqual(r.returncode, 0, caminho)


if __name__ == "__main__":
    unittest.main(verbosity=2)
