"""Ferramenta única de manutenção do guia, sem LLM: mapa, contagens, verificação, PDF e fechamento.

Uso (Python com -I, só biblioteca padrão):
    python -I guia.py mapa 13.2 [--guia G]        # id, linhas e palavras das partes cujo id começa por unidade-13-2
    python -I guia.py contar [--guia G]           # contagens estruturais em JSON
    python -I guia.py verificar [--guia G]        # renumerar (conferir) + validar + executar trechos + checagens próprias
    python -I guia.py pdf [--guia G] [--chrome C] [--saida P] [--substituir --motivo M]
    python -I guia.py fechar [--guia G] [--pdf]   # verificar + contar + hashes + esqueleto de changelog

Saída curta de propósito: só falhas e números, para não gastar contexto de quem lê.
O PDF é gerado em arquivo temporário e conferido com pdfinfo; só substitui o original com --substituir,
depois de copiar o atual para arquivo/antes-<motivo>-<data>/ (nada é apagado). Nunca altera o HTML.
Código de saída 1 se houver falha.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
GUIA_PADRAO = os.path.join(RAIZ, "guia-engenharia-llms.html")
PDF_PADRAO = os.path.join(RAIZ, "guia-engenharia-llms.pdf")


class Estrutura(HTMLParser):
    """Uma passada pelo HTML: seções, ids, tabelas, questões, glossário, dfn e sumário."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.secoes = []  # dicts: id, linha, palavras
        self.ids = []
        self.tabelas = 0
        self.rolagens = 0
        self.radios = set()
        self.corretas = 0
        self.termos_glossario = []
        self.dfn = []
        self.links_sumario = set()
        self.links_web = set()
        self._sec = None
        self._ignorar = 0
        self._em_dfn = False
        self._dfn_buf = []
        self._em_dt = False
        self._dt_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        linha = self.getpos()[0]
        if a.get("id"):
            self.ids.append(a["id"])
        if tag in ("script", "style"):
            self._ignorar += 1
        if tag == "section" and "page" in (a.get("class") or "").split():
            self._sec = {"id": a.get("id") or "", "linha": linha, "palavras": 0}
            self.secoes.append(self._sec)
        if tag == "table":
            self.tabelas += 1
        if "rolagem" in (a.get("class") or "").split():
            self.rolagens += 1
        if tag == "input" and a.get("type") == "radio":
            self.radios.add(a.get("name"))
            if a.get("data-correta") == "true":
                self.corretas += 1
        if tag == "dfn":
            self._em_dfn, self._dfn_buf = True, []
        if tag == "dt" and self._sec and self._sec["id"] == "glossario":
            self._em_dt, self._dt_buf = True, []
        if tag == "a":
            href = a.get("href") or ""
            if self._sec and self._sec["id"] == "sumario" and href.startswith("#"):
                self.links_sumario.add(href[1:])
            if href.startswith(("http://", "https://")):
                self.links_web.add(href)

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._ignorar:
            self._ignorar -= 1
        if tag == "dfn" and self._em_dfn:
            self._em_dfn = False
            self.dfn.append(" ".join("".join(self._dfn_buf).split()))
        if tag == "dt" and self._em_dt:
            self._em_dt = False
            self.termos_glossario.append(" ".join("".join(self._dt_buf).split()))

    def handle_data(self, data):
        if self._ignorar:
            return
        if self._sec is not None:
            self._sec["palavras"] += len(data.split())
        if self._em_dfn:
            self._dfn_buf.append(data)
        if self._em_dt:
            self._dt_buf.append(data)


def ler(guia):
    with open(guia, encoding="utf-8") as f:
        texto = f.read()
    e = Estrutura()
    e.feed(texto)
    return texto, e


def sha16(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()[:16]


def contagens(guia):
    texto, e = ler(guia)
    ult = len(texto.splitlines())
    return {
        "partes": len(e.secoes),
        "palavras_partes": sum(s["palavras"] for s in e.secoes),
        "tabelas": e.tabelas,
        "tabelas_rolagem": e.rolagens,
        "questoes": len(e.radios),
        "gabaritos": e.corretas,
        "glossario_termos": len(e.termos_glossario),
        "dfn": len(e.dfn),
        "links_web_unicos": len(e.links_web),
        "linhas_html": ult,
        "bytes_html": os.path.getsize(guia),
    }


def checagens_proprias(guia):
    """Checagens que validar-guia.py não faz. Retorna lista de (ok, texto)."""
    _, e = ler(guia)
    res = []
    dup = sorted({i for i in e.ids if e.ids.count(i) > 1})
    res.append((not dup, "ids únicos" + (f" — duplicados: {', '.join(dup[:8])}" if dup else "")))
    dd = sorted({t for t in e.dfn if e.dfn.count(t) > 1})
    res.append((not dd, "cada termo definido uma vez em <dfn>" + (f" — repetidos: {', '.join(dd[:8])}" if dd else "")))
    dg = sorted({t for t in e.termos_glossario if e.termos_glossario.count(t) > 1})
    res.append((not dg, "termos do glossário sem repetição" + (f" — repetidos: {', '.join(dg[:8])}" if dg else "")))
    ids_sec = [s["id"] for s in e.secoes if s["id"] and s["id"] not in ("sumario",)]
    fora = [i for i in ids_sec if i not in e.links_sumario
            and re.fullmatch(r"(unidade-\d+-\d+a|capitulo-\d+|questoes-capitulo-\d+)", i)]
    res.append((not fora, "capítulos, questões e primeira parte de cada unidade listados no sumário" + (f" — fora do sumário: {', '.join(fora[:8])} (+{max(0, len(fora) - 8)})" if fora else "")))
    sem_rol = e.tabelas - e.rolagens
    res.append((sem_rol == 0, f"toda tabela dentro de .rolagem ({e.tabelas} tabelas)" + (f" — sem rolagem: {sem_rol}" if sem_rol else "")))
    res.append((e.corretas == len(e.radios), f"um gabarito por questão ({len(e.radios)} questões, {e.corretas} gabaritos)"))
    return res


def rodar(script, args, tempo=300):
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, script), *args], capture_output=True,
                       text=True, encoding="utf-8", timeout=tempo)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def cmd_verificar(guia):
    falhas = 0
    rc, out = rodar("renumerar-paginas.py", ["--guia", guia])
    ok = rc == 0 and "nada a mudar" in out
    print(("OK    " if ok else "FALHA ") + "numeração das páginas em sequência" + ("" if ok else " — " + out.strip().splitlines()[-1]))
    falhas += not ok
    rc, out = rodar("validar-guia.py", ["--guia", guia])
    resumo = [l for l in out.splitlines() if l.startswith("Resultado:")]
    ruins = [l[:200] for l in out.splitlines() if l.startswith("FALHA")]
    print(("OK    " if rc == 0 else "FALHA ") + "validar-guia.py — " + (resumo[0] if resumo else out.strip()[-120:]))
    for l in ruins:
        print("  " + l)
    falhas += rc != 0
    rc, out = rodar("executar-trechos-de-codigo.py", ["--guia", guia])
    ult = [l for l in out.splitlines() if "OK," in l]
    print(("OK    " if rc == 0 else "FALHA ") + "executar-trechos-de-codigo.py — " + (ult[-1].split(". ", 1)[-1] if ult else out.strip()[-120:]))
    for l in [l for l in out.splitlines() if l.startswith("FALHA")][:5]:
        print("  " + l[:200])
    falhas += rc != 0
    for ok, texto in checagens_proprias(guia):
        print(("OK    " if ok else "FALHA ") + texto)
        falhas += not ok
    return falhas


def achar_chrome(explicito):
    if explicito:
        return explicito
    if os.environ.get("GUIA_CHROME"):
        return os.environ["GUIA_CHROME"]
    c = os.path.expanduser("~/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome")
    if os.path.exists(c):
        return c
    achados = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux64/chrome")))
    return achados[-1] if achados else None


def paginas_pdf(caminho):
    r = subprocess.run(["pdfinfo", caminho], capture_output=True, text=True)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    return int(m.group(1)) if m else None


def cmd_pdf(guia, chrome, saida, substituir, motivo):
    chrome = achar_chrome(chrome)
    if not chrome or not os.path.exists(chrome):
        print("FALHA Chrome não encontrado: informe --chrome ou GUIA_CHROME")
        return 1
    destino = saida or os.path.join(tempfile.mkdtemp(prefix="guia-pdf-"), "guia.pdf")
    comum = ["--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={destino}", "file://" + os.path.abspath(guia)]
    for extra in ([], ["--no-sandbox"]):
        r = subprocess.run([chrome, *extra, *comum], capture_output=True, text=True, timeout=540)
        if os.path.exists(destino) and os.path.getsize(destino) > 0:
            break
    if not os.path.exists(destino) or os.path.getsize(destino) == 0:
        print("FALHA o Chrome não gerou o PDF: " + (r.stderr or "")[-200:])
        return 1
    n = paginas_pdf(destino)
    print(f"OK    PDF gerado: {n} páginas, {os.path.getsize(destino)} bytes, sha256 {sha16(destino)} — {destino}")
    if n is None or n < 1:
        print("FALHA pdfinfo não leu o PDF")
        return 1
    if substituir:
        if not motivo:
            print("FALHA --substituir exige --motivo")
            return 1
        pasta = os.path.join(RAIZ, "arquivo", f"antes-{motivo}-{datetime.date.today().isoformat()}")
        os.makedirs(pasta, exist_ok=True)
        if os.path.exists(PDF_PADRAO):
            shutil.copy2(PDF_PADRAO, os.path.join(pasta, os.path.basename(PDF_PADRAO)))
        shutil.copy2(destino, PDF_PADRAO)
        print(f"OK    PDF substituído; cópia anterior em {os.path.relpath(pasta, RAIZ)}/")
    return 0


def cmd_fechar(guia, com_pdf):
    falhas = cmd_verificar(guia)
    c = contagens(guia)
    print("CONTAGENS " + json.dumps(c, ensure_ascii=False))
    print(f"HASH html {sha16(guia)}")
    pdf_info = ""
    if com_pdf:
        f = cmd_pdf(guia, None, None, False, None)
        falhas += f
    elif os.path.exists(PDF_PADRAO):
        pdf_info = f"pdf atual {paginas_pdf(PDF_PADRAO)} páginas, sha {sha16(PDF_PADRAO)}"
        print("HASH " + pdf_info)
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    print("\nESQUELETO DE CHANGELOG (fatos; complete o porquê e a assinatura)")
    print(f"- {hoje}: {c['partes']} partes; {c['questoes']} questões; {c['tabelas']} tabelas ({c['tabelas_rolagem']} com .rolagem); "
          f"{c['glossario_termos']} termos no glossário; HTML sha {sha16(guia)}; verificação: {'0 falhas' if not falhas else str(falhas) + ' falha(s)'}.")
    return 1 if falhas else 0


def cmd_mapa(guia, prefixo):
    texto, e = ler(guia)
    p = prefixo.strip().lower().replace(".", "-")
    if p:
        padrao = re.compile(r"(?:unidade|capitulo|questoes-capitulo)-" + re.escape(p) + r"(?:$|-|[a-z])")
    else:
        padrao = re.compile(r"^(?:capitulo-|introducao$|sumario$|glossario$|referencias$)")
    total = len(texto.splitlines())
    saida = 0
    for i, s in enumerate(e.secoes):
        if padrao.match(s["id"]):
            fim = e.secoes[i + 1]["linha"] - 1 if i + 1 < len(e.secoes) else total
            print(f"{s['id']}\t{s['linha']}-{fim}\t{s['palavras']}p")
            saida += 1
    if not saida:
        print("nenhuma parte com esse prefixo")
        return 1
    return 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("comando", choices=["mapa", "contar", "verificar", "pdf", "fechar"])
    p.add_argument("prefixo", nargs="?", default="")
    p.add_argument("--guia", default=GUIA_PADRAO)
    p.add_argument("--chrome")
    p.add_argument("--saida")
    p.add_argument("--substituir", action="store_true")
    p.add_argument("--motivo")
    p.add_argument("--pdf", action="store_true")
    a = p.parse_args()
    if a.comando == "mapa":
        return cmd_mapa(a.guia, a.prefixo)
    if a.comando == "contar":
        print(json.dumps(contagens(a.guia), ensure_ascii=False))
        return 0
    if a.comando == "verificar":
        return 1 if cmd_verificar(a.guia) else 0
    if a.comando == "pdf":
        return cmd_pdf(a.guia, a.chrome, a.saida, a.substituir, a.motivo)
    return cmd_fechar(a.guia, a.pdf)


if __name__ == "__main__":
    sys.exit(main())
