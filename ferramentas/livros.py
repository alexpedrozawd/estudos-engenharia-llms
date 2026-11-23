"""Extração e leitura localizada de livros técnicos locais em PDF (sem gastar LLM e fora do Git).

Uso (Python com -I, só biblioteca padrão + poppler: pdfinfo, pdftotext, pdftoppm):
    python -I livros.py extrair [--dir DIR] [--forcar]
    python -I livros.py ler LIVRO --de P1 [--ate P2] [--layout]
    python -I livros.py achar LIVRO "palavras da consulta" [-n 5]
    python -I livros.py pagina-png LIVRO PAGINA [--saida CAMINHO]

LIVRO: ai-engineering | dmls (ou outro slug configurado).
Textos extraídos e PNGs ficam exclusivamente em cache-fontes/livros/ (ignorado no .gitignore).
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SAIDA = os.path.join(RAIZ, "cache-fontes", "livros")
PNGS = os.path.join(SAIDA, "paginas")
INDICE = os.path.join(SAIDA, "indice.json")

CATALOGO = {
    "ai-engineering": "AI Engineering*Chip Huyen*.pdf",
    "dmls": "Designing Machine Learning Systems*Chip Huyen*.pdf",
}


def dir_padrao():
    return os.environ.get("GUIA_LIVROS_DIR") or os.path.join(os.path.expanduser("~"), "Documentos")


def localizar_pdfs(diretorio=None, catalogo=None):
    """Mapeia slug -> caminho absoluto do PDF encontrado no diretório informado."""
    pasta = diretorio or dir_padrao()
    mapa = {}
    for slug, padrao in (catalogo or CATALOGO).items():
        achados = sorted(glob.glob(os.path.join(pasta, padrao)))
        if achados:
            mapa[slug] = achados[0]
    return mapa


def sha16(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()[:16]


def contar_paginas_pdf(caminho):
    r = subprocess.run(["pdfinfo", caminho], capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        return None
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    return int(m.group(1)) if m else None


def caminho_texto(slug, saida=SAIDA):
    return os.path.join(saida, f"{slug}.txt")


def carregar_paginas(slug, saida=SAIDA):
    arq = caminho_texto(slug, saida)
    if not os.path.exists(arq):
        raise FileNotFoundError(f"texto de '{slug}' não encontrado em cache-fontes/livros (rode extrair)")
    with open(arq, encoding="utf-8", errors="replace") as f:
        bruto = f.read()
    paginas = bruto.split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()
    return paginas


def carregar_indice(indice_path=INDICE):
    if not os.path.exists(indice_path):
        return {}
    with open(indice_path, encoding="utf-8") as f:
        return json.load(f)


def salvar_indice(dados, indice_path=INDICE):
    os.makedirs(os.path.dirname(indice_path), exist_ok=True)
    with open(indice_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def cmd_extrair(diretorio=None, forcar=False, saida=SAIDA, catalogo=None):
    pdfs = localizar_pdfs(diretorio, catalogo)
    if not pdfs:
        print("FALHA nenhum PDF encontrado para o catálogo no diretório informado")
        return 1
    os.makedirs(saida, exist_ok=True)
    indice_path = os.path.join(saida, "indice.json")
    indice = carregar_indice(indice_path)
    falhas = 0
    for slug, pdf in sorted(pdfs.items()):
        destino = caminho_texto(slug, saida)
        h = sha16(pdf)
        reg = indice.get(slug, {})
        if not forcar and os.path.exists(destino) and reg.get("sha16_pdf") == h:
            print(f"OK    {slug}: em cache ({reg.get('paginas')} páginas, sha {h})")
            continue
        r = subprocess.run(["pdftotext", pdf, destino], capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            print(f"FALHA {slug}: pdftotext {r.stderr[:120]}")
            falhas += 1
            continue
        paginas = carregar_paginas(slug, saida)
        total_pdf = contar_paginas_pdf(pdf)
        palavras = sum(len(p.split()) for p in paginas)
        indice[slug] = {
            "arquivo_pdf": os.path.basename(pdf),
            "caminho_pdf": pdf,
            "sha16_pdf": h,
            "paginas": total_pdf or len(paginas),
            "paginas_extraidas": len(paginas),
            "palavras": palavras,
            "bytes_txt": os.path.getsize(destino),
        }
        print(f"OK    {slug}: {len(paginas)} páginas extraídas, {palavras} palavras (sha {h})")
    salvar_indice(indice, indice_path)
    return 1 if falhas else 0


def ler_layout_pdf(pdf, de, ate):
    r = subprocess.run(["pdftotext", "-layout", "-f", str(de), "-l", str(ate), pdf, "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[:120] or "erro ao rodar pdftotext -layout")
    paginas = r.stdout.split("\f")
    if paginas and not paginas[-1].strip():
        paginas.pop()
    return [(de + i, txt) for i, txt in enumerate(paginas)]


def cmd_ler(slug, de, ate=None, layout=False, saida=SAIDA):
    ate = de if ate is None else ate
    if de < 1 or ate < de:
        print("FALHA intervalo inválido (--de >= 1 e --ate >= --de)")
        return 1
    if layout:
        indice = carregar_indice(os.path.join(saida, "indice.json"))
        pdf = (indice.get(slug) or {}).get("caminho_pdf") or localizar_pdfs().get(slug)
        if not pdf or not os.path.exists(pdf):
            print(f"FALHA PDF original de '{slug}' não encontrado para --layout")
            return 1
        pags = ler_layout_pdf(pdf, de, ate)
    else:
        todas = carregar_paginas(slug, saida)
        fim = min(ate, len(todas))
        if de > len(todas):
            print(f"FALHA página inicial {de} excede total de {len(todas)} páginas")
            return 1
        pags = [(n, todas[n - 1]) for n in range(de, fim + 1)]
    for num, texto in pags:
        print(f"=== {slug} | Página {num} ===")
        print(texto.strip())
    return 0


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def achar_em_paginas(paginas, consulta, n=5, largura=420):
    termos = {t for t in re.findall(r"\w+", sem_acento(consulta)) if len(t) > 2}
    if not termos:
        return [], 0
    achados = []
    for num, texto in enumerate(paginas, 1):
        linhas = texto.splitlines()
        melhor = None
        for i, linha in enumerate(linhas):
            bloco = " ".join(l.strip() for l in linhas[i:i + 3])
            if not bloco.strip():
                continue
            if not termos & set(re.findall(r"\w+", sem_acento(linha))):
                continue
            palavras = set(re.findall(r"\w+", sem_acento(bloco)))
            score = len(termos & palavras)
            cand = (score, num, i + 1, bloco[:largura])
            if melhor is None or cand[0] > melhor[0]:
                melhor = cand
        if melhor:
            achados.append(melhor)
    achados.sort(key=lambda x: (-x[0], x[1], x[2]))
    return achados[:n], len(termos)


def cmd_achar(slug, consulta, n=5, saida=SAIDA):
    paginas = carregar_paginas(slug, saida)
    res, total = achar_em_paginas(paginas, consulta, n)
    if not res:
        print("nenhum candidato")
        return 1
    for score, pag, linha, bloco in res:
        print(f"{slug}:p.{pag}:l.{linha} [{score}/{total}] {bloco}")
    return 0


def cmd_pagina_png(slug, pagina, destino=None, saida=SAIDA):
    if pagina < 1:
        print("FALHA página deve ser >= 1")
        return 1
    indice = carregar_indice(os.path.join(saida, "indice.json"))
    pdf = (indice.get(slug) or {}).get("caminho_pdf") or localizar_pdfs().get(slug)
    if not pdf or not os.path.exists(pdf):
        print(f"FALHA PDF original de '{slug}' não encontrado")
        return 1
    if destino:
        os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
        prefixo = os.path.splitext(destino)[0]
    else:
        os.makedirs(os.path.join(saida, "paginas"), exist_ok=True)
        prefixo = os.path.join(saida, "paginas", f"{slug}-p{pagina:04d}")
    r = subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", str(pagina), "-l", str(pagina), "-singlefile", pdf, prefixo],
                       capture_output=True, text=True, errors="replace")
    arquivo_png = prefixo + ".png"
    if r.returncode != 0 or not os.path.exists(arquivo_png):
        print(f"FALHA pdftoppm: {r.stderr[:120]}")
        return 1
    print(f"OK    {arquivo_png}")
    return 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="comando", required=True)

    pe = sub.add_parser("extrair")
    pe.add_argument("--dir", help="diretório onde estão os PDFs")
    pe.add_argument("--forcar", action="store_true")

    pl = sub.add_parser("ler")
    pl.add_argument("livro")
    pl.add_argument("--de", type=int, required=True)
    pl.add_argument("--ate", type=int)
    pl.add_argument("--layout", action="store_true")

    pa = sub.add_parser("achar")
    pa.add_argument("livro")
    pa.add_argument("consulta")
    pa.add_argument("-n", type=int, default=5)

    pp = sub.add_parser("pagina-png")
    pp.add_argument("livro")
    pp.add_argument("pagina", type=int)
    pp.add_argument("--saida")

    a = p.parse_args()
    if a.comando == "extrair":
        return cmd_extrair(a.dir, a.forcar)
    if a.comando == "ler":
        return cmd_ler(a.livro, a.de, a.ate, a.layout)
    if a.comando == "achar":
        return cmd_achar(a.livro, a.consulta, a.n)
    return cmd_pagina_png(a.livro, a.pagina, a.saida)


if __name__ == "__main__":
    sys.exit(main())
