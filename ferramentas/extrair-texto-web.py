"""Converte páginas HTML e RFCs baixadas em texto simples para o conferir-trechos.py.

Uso (Python com -I, só biblioteca padrão):
    python -I extrair-texto-web.py --entrada <pasta-bruta> --saida <pasta-textos>

Para cada arquivo da pasta bruta gera <pasta-textos>/<nome-sem-extensão>.txt:
- .html: texto visível, sem script, style e navegação; blocos separados por quebra de linha;
- .txt (RFC em texto puro): remove cabeçalho, rodapé de página e quebras de página, que cortariam frases;
- .md: copiado como está.
Somente leitura da pasta bruta; não executa nada do conteúdo baixado e não acessa a rede.
"""
import argparse
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser

IGNORAR = {"script", "style", "noscript", "svg", "nav", "header", "footer", "template"}
BLOCOS = {"p", "div", "li", "ul", "ol", "br", "tr", "td", "th", "table", "pre", "section", "article",
          "h1", "h2", "h3", "h4", "h5", "h6", "dt", "dd", "dl", "blockquote", "main", "caption"}


class Texto(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.partes = []
        self._ignorar = 0

    def handle_starttag(self, tag, attrs):
        if tag in IGNORAR:
            self._ignorar += 1
        elif tag in BLOCOS:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if tag in IGNORAR and self._ignorar:
            self._ignorar -= 1
        elif tag in BLOCOS:
            self.partes.append("\n")

    def handle_data(self, data):
        if not self._ignorar:
            self.partes.append(data)


def de_html(bruto):
    p = Texto()
    p.feed(bruto)
    texto = unescape("".join(p.partes))
    texto = texto.replace("¶", "")  # marcador de âncora das docs do Python
    texto = re.sub(r"[ \t ]+", " ", texto)
    texto = re.sub(r"\n\s*\n+", "\n", texto)
    return texto.strip() + "\n"


def de_rfc(bruto):
    saida = []
    for linha in bruto.replace("\f", "\n").splitlines():
        if re.search(r"\[Page \d+\]\s*$", linha):
            continue
        if re.match(r"^RFC \d+\s+.+\s+\w+ \d{4}\s*$", linha):
            continue
        saida.append(linha)
    return "\n".join(saida) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--entrada", required=True)
    parser.add_argument("--saida", required=True)
    args = parser.parse_args()
    os.makedirs(args.saida, exist_ok=True)
    total = 0
    for nome in sorted(os.listdir(args.entrada)):
        caminho = os.path.join(args.entrada, nome)
        if not os.path.isfile(caminho):
            continue
        base, ext = os.path.splitext(nome)
        with open(caminho, encoding="utf-8", errors="replace") as arq:
            bruto = arq.read()
        if ext == ".html":
            texto = de_html(bruto)
        elif ext == ".txt":
            texto = de_rfc(bruto)
        elif ext == ".md":
            texto = bruto
        else:
            print(f"IGNORADO {nome}")
            continue
        destino = os.path.join(args.saida, base + ".txt")
        with open(destino, "w", encoding="utf-8", newline="\n") as arq:
            arq.write(texto)
        total += 1
        print(f"OK {nome} -> {base}.txt ({len(texto)} caracteres)")
    print(f"{total} arquivos convertidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
