"""Executa os trechos de código do guia marcados como executáveis e compara a saída declarada.

Uso (Python com -I, só biblioteca padrão):
    python -I executar-trechos-de-codigo.py --guia <caminho>/guia-engenharia-llms.html [--tempo 10]

Convenção no HTML:
    <pre class="codigo" id="cod-2-1-a" data-executavel="true"><code class="language-python">...</code></pre>
    <pre class="saida" data-saida-de="cod-2-1-a"><code>saída esperada</code></pre>   (opcional)

Só executa blocos com data-executavel="true"; os demais são contados como ilustrativos, não executados.
Segurança (defesa em profundidade, não é sandbox): antes de rodar, cada trecho passa por uma lista
fechada de módulos importáveis (análise AST) e é recusado se usar open, eval, exec, compile, input,
__import__ ou atributos de execução de processo. Cada trecho roda em subprocesso `python -I`, com
pasta temporária vazia como diretório de trabalho, entrada nula, ambiente mínimo e tempo limite.
Não usa rede por construção (sem módulos de rede na lista). Não escreve nem lê arquivos do projeto.
Código de saída 1 se algum trecho falhar.
"""
import argparse
import ast
import os
import subprocess
import sys
import tempfile
from html import unescape
from html.parser import HTMLParser

PERMITIDOS = {
    "asyncio", "collections", "contextlib", "dataclasses", "datetime", "decimal", "enum", "functools",
    "hashlib", "itertools", "json", "math", "re", "sqlite3", "textwrap", "time", "typing", "unittest",
    "unittest.mock", "sys", "io", "random", "string", "fractions", "operator", "abc", "traceback",
}
PROIBIDOS_NOMES = {"open", "eval", "exec", "compile", "input", "__import__", "breakpoint", "exit", "quit"}
PROIBIDOS_ATRIBUTOS = {"system", "popen", "spawn", "fork", "remove", "rmdir", "unlink", "rename", "open"}


class Blocos(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.codigos = []  # (id, executavel, texto)
        self.saidas = {}  # id do código -> texto
        self.sem_marca = 0
        self._pre = None
        self._code = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "pre":
            classes = (a.get("class") or "").split()
            self._pre = {"classes": classes, "id": a.get("id"), "exec": a.get("data-executavel") == "true",
                         "saida_de": a.get("data-saida-de")}
            self._buf = []
        elif tag == "code" and self._pre is not None:
            self._code = True

    def handle_endtag(self, tag):
        if tag == "code":
            self._code = False
        elif tag == "pre" and self._pre is not None:
            texto = "".join(self._buf)
            p = self._pre
            if "saida" in p["classes"] and p["saida_de"]:
                self.saidas[p["saida_de"]] = texto
            elif "codigo" in p["classes"]:
                self.codigos.append((p["id"], p["exec"], texto))
            else:
                self.sem_marca += 1
            self._pre = None

    def handle_data(self, data):
        if self._pre is not None:
            self._buf.append(data)


def checar_ast(codigo):
    try:
        arvore = ast.parse(codigo)
    except SyntaxError as erro:
        return f"erro de sintaxe: {erro}"
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            for alias in no.names:
                if alias.name not in PERMITIDOS and alias.name.split(".")[0] not in PERMITIDOS:
                    return f"import não permitido: {alias.name}"
        elif isinstance(no, ast.ImportFrom):
            modulo = no.module or ""
            if modulo not in PERMITIDOS and modulo.split(".")[0] not in PERMITIDOS:
                return f"import não permitido: {modulo}"
        elif isinstance(no, ast.Name) and no.id in PROIBIDOS_NOMES:
            return f"uso não permitido: {no.id}"
        elif isinstance(no, ast.Attribute) and no.attr in PROIBIDOS_ATRIBUTOS:
            return f"atributo não permitido: {no.attr}"
    return None


def normalizar_saida(texto):
    return "\n".join(linha.rstrip() for linha in texto.strip().splitlines())


def executar(codigo, tempo):
    with tempfile.TemporaryDirectory(prefix="trecho-") as pasta:
        script = os.path.join(pasta, "trecho.py")
        with open(script, "w", encoding="utf-8", newline="\n") as arq:
            arq.write(codigo)
        ambiente = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1",
                    "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""), "PATH": os.environ.get("PATH", "")}
        try:
            # -I ignora variáveis PYTHON*; a codificação UTF-8 precisa ir pela opção -X utf8.
            r = subprocess.run([sys.executable, "-I", "-X", "utf8", script], cwd=pasta, env=ambiente, input="",
                               capture_output=True, text=True, encoding="utf-8", timeout=tempo)
        except subprocess.TimeoutExpired:
            return None, "", f"tempo limite de {tempo} s"
        return r.returncode, r.stdout or "", r.stderr or ""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--guia", required=True)
    parser.add_argument("--tempo", type=int, default=10)
    args = parser.parse_args()
    with open(args.guia, encoding="utf-8") as arq:
        coletor = Blocos()
        coletor.feed(arq.read())

    ok = falhas = ilustrativos = 0
    for id_, executavel, texto in coletor.codigos:
        nome = id_ or "(sem id)"
        if not executavel:
            ilustrativos += 1
            print(f"ILUSTRATIVO {nome}: não executado")
            continue
        if not id_:
            falhas += 1
            print(f"FALHA       {nome}: bloco executável sem id")
            continue
        codigo = unescape(texto)
        problema = checar_ast(codigo)
        if problema:
            falhas += 1
            print(f"FALHA       {nome}: {problema}")
            continue
        codigo_saida, saida, erro = executar(codigo, args.tempo)
        if codigo_saida != 0:
            falhas += 1
            resumo = (erro or "").strip().splitlines()[-1:] or ["sem detalhe"]
            print(f"FALHA       {nome}: código de saída {codigo_saida}; {resumo[0]}")
            continue
        esperado = coletor.saidas.get(id_)
        if esperado is None:
            ok += 1
            print(f"OK          {nome}: executou sem erro (sem saída declarada para comparar)")
        elif normalizar_saida(saida) == normalizar_saida(unescape(esperado)):
            ok += 1
            print(f"OK          {nome}: saída igual à declarada")
        else:
            falhas += 1
            print(f"FALHA       {nome}: saída diferente da declarada")
            print("  obtida:   " + repr(normalizar_saida(saida))[:300])
            print("  esperada: " + repr(normalizar_saida(unescape(esperado)))[:300])
    sem_ref = [i for i in coletor.saidas if i not in {c[0] for c in coletor.codigos}]
    for i in sem_ref:
        falhas += 1
        print(f"FALHA       saída órfã: nenhum bloco de código com id {i}")
    print()
    print(f"Python {sys.version.split()[0]}. {ok} OK, {falhas} FALHA, {ilustrativos} ilustrativos (não executados), "
          f"{coletor.sem_marca} blocos <pre> sem classe codigo/saida.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
