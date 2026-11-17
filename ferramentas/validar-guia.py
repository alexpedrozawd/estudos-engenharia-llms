"""Roteiro de validação estática do guia HTML (somente leitura).

Uso (Python com -I, só biblioteca padrão):
    python -I validar-guia.py --guia <caminho>/guia-engenharia-llms.html

Verifica: idioma e viewport; textos exatos da capa; links internos (#id) e para arquivos locais;
ausência de dependências externas; um gabarito por questão (grupo de radios com 4 alternativas
e uma marcada data-correta="true"); consistência básica do sumário; links web com target=_blank e
rel=noopener; blocos de código (figure.bloco-codigo, pre.codigo e pre.saida com role=region, pre.codigo com
tabindex, rótulo, data-executavel e legenda coerente) e rolagem horizontal só dentro do bloco.

Não verifica (exige navegador): reflow em 320 px CSS sem rolagem horizontal, conforto nos
aparelhos reais e aparência. Esses itens ficam como pendentes no registro de validação.
"""
import argparse
import os
import re
import sys
from html import unescape
from html.parser import HTMLParser

CAPA = [
    "Guia para Engenharia de LLMs",
    "Criado por Alexandre Pedroza & LLMs",
]


class Coletor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.viewport = False
        self.ids = set()
        self.hrefs = []
        self.externos = []
        self.radios = {}
        self.texto = []
        self._skip = 0
        self.numeros = []
        self._num = False
        self.fieldsets = 0
        self.regioes = 0
        self.explicacoes = {}
        self.css = []
        self._css = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classe = a.get("class", "") or ""
        if tag == "span" and "page-number" in classe.split():
            self._num = True
        if tag == "fieldset" and "questao" in classe.split():
            self.fieldsets += 1
        if tag == "div" and "retorno" in classe.split() and a.get("role") == "status" and a.get("aria-live"):
            self.regioes += 1
        if tag == "input" and a.get("type") == "radio":
            self.explicacoes.setdefault(a.get("name", ""), []).append(
                (a.get("data-correta") == "true", (a.get("data-explicacao") or "").strip())
            )
        if tag == "style":
            self._css = True
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "meta" and a.get("name") == "viewport":
            self.viewport = True
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
        for attr in ("src", "href"):
            v = a.get(attr, "")
            if tag in ("script", "img", "iframe", "source") and attr == "src" and v:
                if re.match(r"^(https?:)?//", v):
                    self.externos.append(f"<{tag} {attr}={v}>")
            if tag == "link" and attr == "href" and v and re.match(r"^(https?:)?//", v):
                self.externos.append(f"<link href={v}>")
        if tag == "input" and a.get("type") == "radio":
            nome = a.get("name", "")
            self.radios.setdefault(nome, []).append(a.get("data-correta") == "true")
        if tag in ("style", "script"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("style", "script") and self._skip:
            self._skip -= 1
        if tag == "style":
            self._css = False
        if tag == "span":
            self._num = False

    def handle_data(self, data):
        if self._css:
            self.css.append(data)
        if self._num and data.strip().isdigit():
            self.numeros.append(int(data.strip()))
        if not self._skip:
            self.texto.append(data)


def checar(guia_path):
    with open(guia_path, encoding="utf-8") as arq:
        bruto = arq.read()
    c = Coletor()
    c.feed(bruto)
    pasta = os.path.dirname(os.path.abspath(guia_path))
    resultados = []

    def reg(nome, ok, detalhe=""):
        resultados.append((nome, ok, detalhe))

    reg("idioma pt-BR", c.lang is not None and c.lang.lower().startswith("pt"), f"lang={c.lang!r}")
    reg("meta viewport presente", c.viewport)

    texto = unescape(" ".join(c.texto))
    texto = re.sub(r"\s+", " ", texto)
    for t in CAPA:
        reg(f"texto exato da capa: {t}", t in texto)

    quebrados = []
    for href in c.hrefs:
        if href.startswith("#"):
            if href[1:] not in c.ids:
                quebrados.append(href)
        elif re.match(r"^[a-z]+:", href, re.I) or href.startswith("//"):
            continue  # esquemas externos tratados pelo critério de dependências
        else:
            caminho = os.path.normpath(os.path.join(pasta, unescape(href.split("#")[0])))
            if href.split("#")[0] and not os.path.exists(caminho):
                quebrados.append(href)
    reg("links internos e locais válidos", not quebrados, ", ".join(quebrados))

    sem_alvo = [m for m in re.findall(r"<a\b[^>]*>", bruto)
                if re.search(r'href="https?://', m)
                and not (re.search(r'target="_blank"', m) and re.search(r'rel="[^"]*noopener[^"]*"', m))]
    reg("links web com target=_blank e rel=noopener", not sem_alvo, f"{len(sem_alvo)} sem a regra" if sem_alvo else "")

    links_externos = [h for h in c.hrefs if re.match(r"^https?://", h)]
    reg("sem dependências externas de carregamento", not c.externos, "; ".join(c.externos))
    reg("links para a web (texto, não carregados)", True, f"{len(links_externos)} encontrados")

    if not c.radios:
        reg("um gabarito por questão", True, "nenhuma questão no guia ainda (ok até o Bloco 2)")
    else:
        erros = []
        for nome, marcas in c.radios.items():
            if len(marcas) != 4 or sum(marcas) != 1:
                erros.append(f"{nome}: {len(marcas)} alternativas, {sum(marcas)} correta(s)")
        reg("um gabarito por questão", not erros, "; ".join(erros))

        # Questões de fechamento do capítulo usam nomes q1..q6, c2q1..c2q5; as perguntas de
        # compreensão de cada parte usam p<parte> e não entram nesta contagem.
        por_capitulo = {}
        for nome in c.radios:
            if nome.startswith("p"):
                continue
            prefixo = re.sub(r"\d+$", "", nome)
            por_capitulo[prefixo] = por_capitulo.get(prefixo, 0) + 1
        fora = {k: v for k, v in por_capitulo.items() if v not in (5, 6)}
        reg("de cinco ou seis questões de fechamento por capítulo", not fora,
            "; ".join(f"{k}: {v}" for k, v in por_capitulo.items()))
        reg("uma região de retorno aria-live por questão", c.regioes == len(c.radios) == c.fieldsets,
            f"{c.regioes} regiões, {len(c.radios)} questões, {c.fieldsets} fieldsets")
        faltas = []
        for nome, alts in c.explicacoes.items():
            for correta, texto in alts:
                if not texto:
                    faltas.append(f"{nome}: alternativa sem explicação")
                if correta and not texto.startswith("Correta."):
                    faltas.append(f"{nome}: a explicação da correta deve começar por 'Correta.'")
                if not correta and not texto.startswith("Incorreta."):
                    faltas.append(f"{nome}: a explicação da incorreta deve começar por 'Incorreta.'")
        reg("explicação coerente com o gabarito em cada alternativa", not faltas, "; ".join(faltas[:4]))
        reg("redução de movimento tratada no CSS", "prefers-reduced-motion" in "".join(c.css))

    # Blocos de código (convenção do Capítulo 2): <figure class="bloco-codigo"> com <figcaption> que declara se o
    # trecho foi executado, e <pre class="codigo" data-executavel="true|false" tabindex="0" aria-label=...>.
    todos_pre = re.findall(r"<pre\b[^>]*>", bruto)
    pre_codigo = [p for p in todos_pre if re.search(r'class="[^"]*\bcodigo\b', p)]
    if not pre_codigo:
        reg("blocos de código conforme a convenção", True, "nenhum bloco de código no guia ainda")
    else:
        erros = []
        figuras = re.findall(r'<figure\b[^>]*class="[^"]*\bbloco-codigo\b[^"]*"[^>]*>(.*?)</figure>', bruto, re.S)
        if len(figuras) != len(pre_codigo):
            erros.append(f"{len(pre_codigo)} blocos <pre class=codigo> e {len(figuras)} <figure class=bloco-codigo>")
        for p in todos_pre:
            if re.search(r'class="[^"]*\bsaida\b', p) and 'role="region"' not in p:
                alvo = re.search(r'data-saida-de="([^"]+)"', p)
                erros.append("saída " + (alvo.group(1) if alvo else "(sem data-saida-de)") + ": sem role=region")
        for fig in figuras:
            pre = re.search(r"<pre\b[^>]*>", fig)
            if not pre:
                erros.append("figure sem <pre>")
                continue
            tag = pre.group(0)
            ident = re.search(r'\bid="([^"]+)"', tag)
            nome = ident.group(1) if ident else "(sem id)"
            if not ident:
                erros.append(f"{nome}: sem id")
            if 'tabindex="0"' not in tag:
                erros.append(f"{nome}: sem tabindex=0 (rolagem por teclado)")
            if "aria-label=" not in tag and "aria-labelledby=" not in tag:
                erros.append(f"{nome}: sem rótulo acessível")
            if 'role="region"' not in tag:
                erros.append(f"{nome}: sem role=region (aria-label em <pre> sem papel é pouco suportado)")
            marca = re.search(r'data-executavel="(true|false)"', tag)
            legenda = re.search(r"<figcaption\b[^>]*>(.*?)</figcaption>", fig, re.S)
            texto_legenda = re.sub(r"<[^>]+>", "", legenda.group(1)).lower() if legenda else ""
            if not marca:
                erros.append(f"{nome}: sem data-executavel")
            elif marca.group(1) == "true" and "executado e conferido" not in texto_legenda:
                erros.append(f"{nome}: legenda deve dizer 'executado e conferido'")
            elif marca.group(1) == "false" and "ilustrativo, não executado" not in texto_legenda:
                erros.append(f"{nome}: legenda deve dizer 'ilustrativo, não executado'")
            if not re.search(r'<code\b[^>]*class="[^"]*language-', fig):
                erros.append(f"{nome}: <code> sem class language-*")
        reg("blocos de código conforme a convenção", not erros, "; ".join(erros[:4]))
        css = "".join(c.css)
        reg("rolagem horizontal só dentro do bloco de código",
            bool(re.search(r"pre\.codigo[^{]*\{[^}]*overflow-x\s*:\s*auto", css)),
            "" if re.search(r"pre\.codigo[^{]*\{[^}]*overflow-x\s*:\s*auto", css) else "esperado pre.codigo { overflow-x: auto }")

    esperado = list(range(1, len(c.numeros) + 1))
    reg("páginas numeradas em sequência a partir de 1", c.numeros == esperado, f"{c.numeros}")

    return resultados


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--guia", required=True)
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    resultados = checar(args.guia)
    falhas = 0
    for nome, ok, detalhe in resultados:
        marca = "OK    " if ok else "FALHA "
        print(f"{marca}{nome}" + (f" — {detalhe}" if detalhe else ""))
        if not ok:
            falhas += 1
    print()
    print("Pendentes por natureza (exigem navegador ou aparelhos reais): reflow em 320 px sem rolagem horizontal; conforto nos três aparelhos.")
    print(f"Resultado: {len(resultados) - falhas} OK, {falhas} FALHA.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
