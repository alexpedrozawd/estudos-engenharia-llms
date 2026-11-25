"""Modo exercício dos laboratórios: copia os labs e troca os trechos marcados por `raise NotImplementedError`.

Nos originais, cada função de exercício tem o corpo entre `# EXERCICIO-INICIO: <dica>` e `# EXERCICIO-FIM`.
O gerador copia `laboratorios/` e `laboratorios-mercado/` para o destino (padrão `rascunho-local/exercicios/`,
fora do Git) e, nos módulos de cada lab (não nos testes), troca o corpo marcado por um `raise` com a dica.
Os originais nunca são alterados.

Uso (Python com -I, só biblioteca padrão):
    python3 -I ferramentas/gerar-exercicios.py                      # gera a cópia (recusa se já existir)
    python3 -I ferramentas/gerar-exercicios.py --alvo lab_05_avaliacao --forcar   # refaz só um lab
    python3 -I ferramentas/gerar-exercicios.py --checar             # só valida os marcadores dos originais
    python3 -I ferramentas/gerar-exercicios.py --verificar labs     # cada trecho, sozinho, derruba um teste
    .venv-mercado/bin/python -I ferramentas/gerar-exercicios.py --verificar mercado

Na cópia, rode os mesmos runners: `rascunho-local/exercicios/laboratorios/executar_labs.py --alvo <lab>` e
`rascunho-local/exercicios/laboratorios-mercado/executar_smoke.py --alvo <projeto>`.
Código de saída 1 se houver falha.
"""
import argparse
import ast
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DESTINO_PADRAO = os.path.join(RAIZ, "rascunho-local", "exercicios")
CAMADAS = {
    "laboratorios": {"runner": "executar_labs.py", "unidades": ("lab_*", "projeto_integrador")},
    "laboratorios-mercado": {"runner": "executar_smoke.py", "unidades": ("[0-9][0-9]_*",)},
}
IGNORAR = shutil.ignore_patterns("__pycache__", "*.pyc", "*.egg-info", "modelos", "adaptador*", "build",
                                 ".venv*", "antes*.json", "depois*.json")
INICIO = re.compile(r"^(?P<ind>[ \t]*)# EXERCICIO-INICIO:(?P<dica>.*)$")
FIM = re.compile(r"^(?P<ind>[ \t]*)# EXERCICIO-FIM\s*$")
MIN_TRECHOS, MAX_TRECHOS = 2, 4
DEF = re.compile(r"^(?P<ind>[ \t]*)(?:async\s+)?def\s+(?P<nome>\w+)")


class ErroMarcador(ValueError):
    pass


def trechos(texto, arquivo="<texto>"):
    """Lista (inicio, fim, recuo, dica, funcao) dos trechos marcados; índices de linha base 0."""
    linhas = texto.split("\n")
    achados, aberto = [], None
    for i, linha in enumerate(linhas):
        mi, mf = INICIO.match(linha), FIM.match(linha)
        if mi:
            if aberto is not None:
                raise ErroMarcador(f"{arquivo}:{i + 1}: EXERCICIO-INICIO aninhado")
            dica = mi.group("dica").strip()
            if not dica:
                raise ErroMarcador(f"{arquivo}:{i + 1}: EXERCICIO-INICIO sem dica")
            aberto = (i, mi.group("ind"), dica)
        elif mf:
            if aberto is None:
                raise ErroMarcador(f"{arquivo}:{i + 1}: EXERCICIO-FIM sem INICIO")
            if mf.group("ind") != aberto[1]:
                raise ErroMarcador(f"{arquivo}:{i + 1}: EXERCICIO-FIM com recuo diferente do INICIO")
            if i == aberto[0] + 1:
                raise ErroMarcador(f"{arquivo}:{i + 1}: trecho vazio")
            funcao = "?"
            for j in range(aberto[0] - 1, -1, -1):
                md = DEF.match(linhas[j])
                if md and len(md.group("ind")) < len(aberto[1]):
                    funcao = md.group("nome")
                    break
            achados.append((aberto[0], i, aberto[1], aberto[2], funcao))
            aberto = None
    if aberto is not None:
        raise ErroMarcador(f"{arquivo}:{aberto[0] + 1}: EXERCICIO-INICIO sem FIM")
    return achados


def transformar(texto, arquivo="<texto>", apenas=None):
    """Troca o corpo de cada trecho (ou só do trecho `apenas`) por `raise NotImplementedError(<dica>)`."""
    linhas = texto.split("\n")
    lista = trechos(texto, arquivo)
    for k, (ini, fim, ind, dica, _) in reversed(list(enumerate(lista))):
        if apenas is not None and k != apenas:
            continue
        linhas[ini + 1:fim] = [f"{ind}raise NotImplementedError({('Exercício: ' + dica)!r})"]
    novo = "\n".join(linhas)
    ast.parse(novo, filename=arquivo)
    return novo, len(lista) if apenas is None else 1


def unidades(base, camada):
    pastas = []
    for padrao in CAMADAS[camada]["unidades"]:
        pastas += [p for p in glob.glob(os.path.join(base, camada, padrao)) if os.path.isdir(p)]
    return sorted(pastas)


def modulos(pasta):
    return sorted(p for p in glob.glob(os.path.join(pasta, "*.py")) if not os.path.basename(p).startswith("test_"))


def inventario(base=RAIZ):
    """{camada: {unidade: [(arquivo, trechos)]}} dos originais, validando os limites por lab."""
    inv, erros = {}, []
    for camada in CAMADAS:
        inv[camada] = {}
        for pasta in unidades(base, camada):
            nome = os.path.basename(pasta)
            itens = []
            for arq in modulos(pasta):
                texto = open(arq, encoding="utf-8").read()
                try:
                    lista = trechos(texto, os.path.relpath(arq, base))
                    if lista:
                        transformar(texto, arq)
                except (ErroMarcador, SyntaxError) as exc:
                    erros.append(str(exc))
                    continue
                if lista:
                    itens.append((arq, lista))
            total = sum(len(t) for _, t in itens)
            if not MIN_TRECHOS <= total <= MAX_TRECHOS:
                erros.append(f"{camada}/{nome}: {total} trechos (esperado de {MIN_TRECHOS} a {MAX_TRECHOS})")
            inv[camada][nome] = itens
    return inv, erros


def _destino_seguro(destino):
    """Aceita destino fora do projeto ou dentro de rascunho-local/ (fora do Git); nunca ancestral do projeto."""
    d, r = os.path.realpath(destino), os.path.realpath(RAIZ)
    rascunho = os.path.join(r, "rascunho-local")
    if d == r or r.startswith(d + os.sep) or d == rascunho or (d.startswith(r + os.sep) and not d.startswith(rascunho + os.sep)):
        raise SystemExit(f"FALHA destino inseguro (use rascunho-local/ ou uma pasta fora do projeto): {destino}")
    return d


def _apagar_copia(destino):
    """Só apaga pasta vazia ou cópia gerada por este script (tem EXERCICIOS.md)."""
    if os.listdir(destino) and not os.path.isfile(os.path.join(destino, "EXERCICIOS.md")):
        raise SystemExit(f"FALHA {destino} não parece uma cópia de exercícios (sem EXERCICIOS.md); nada foi apagado")
    shutil.rmtree(destino)


def _copiar_camada(base_origem, destino, camada):
    shutil.copytree(os.path.join(base_origem, camada), os.path.join(destino, camada), ignore=IGNORAR)


def _transformar_pasta(pasta):
    n = 0
    for arq in modulos(pasta):
        texto = open(arq, encoding="utf-8").read()
        if "# EXERCICIO-INICIO:" not in texto:
            continue
        novo, k = transformar(texto, arq)
        with open(arq, "w", encoding="utf-8") as f:
            f.write(novo)
        n += k
    return n


def _indice(destino, inv, base_origem):
    linhas = ["# Exercícios dos laboratórios", "",
              "Gerado por `ferramentas/gerar-exercicios.py`. Implemente cada trecho na cópia, rode os testes do lab "
              "e compare com a solução no original (`diff -ru`).", ""]
    for camada, labs in inv.items():
        runner = CAMADAS[camada]["runner"]
        for nome, itens in labs.items():
            linhas.append(f"## {camada}/{nome}")
            linhas.append(f"Testar: `{camada}/{runner} --alvo {nome}`")
            for arq, lista in itens:
                rel = os.path.relpath(arq, base_origem)
                for _ini, _fim, _ind, dica, funcao in lista:
                    linhas.append(f"- `{rel}` → `{funcao}`: {dica}")
            linhas.append("")
    with open(os.path.join(destino, "EXERCICIOS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))


def gerar(destino=DESTINO_PADRAO, alvos=(), forcar=False, base_origem=RAIZ):
    inv, erros = inventario(base_origem)
    if erros:
        raise SystemExit("FALHA marcadores:\n" + "\n".join(erros))
    destino = _destino_seguro(destino)
    if not alvos:
        if os.path.exists(destino):
            if not forcar:
                raise SystemExit(f"FALHA destino já existe (seu trabalho pode estar lá); use --forcar ou --alvo: {destino}")
            _apagar_copia(destino)
        os.makedirs(destino)
        n = 0
        for camada in CAMADAS:
            _copiar_camada(base_origem, destino, camada)
            for pasta in unidades(destino, camada):
                n += _transformar_pasta(pasta)
        _indice(destino, inv, base_origem)
        return n
    n = 0
    for alvo in alvos:
        camada = next((c for c in CAMADAS if alvo in inv[c]), None)
        if camada is None:
            raise SystemExit(f"FALHA alvo desconhecido: {alvo}")
        if not os.path.isfile(os.path.join(destino, "EXERCICIOS.md")):
            raise SystemExit("FALHA gere a cópia completa antes de usar --alvo")
        pasta = os.path.join(destino, camada, alvo)
        if os.path.exists(pasta):
            if not forcar:
                raise SystemExit(f"FALHA {pasta} já existe; use --forcar para refazer só este lab")
            shutil.rmtree(pasta)
        shutil.copytree(os.path.join(base_origem, camada, alvo), pasta, ignore=IGNORAR)
        n += _transformar_pasta(pasta)
    return n


def _rodar(python, base, camada, alvo=None):
    cmd = [python, "-I", "-W", "error::ResourceWarning", os.path.join(base, camada, CAMADAS[camada]["runner"])]
    if alvo:
        cmd += ["--alvo", alvo]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=600, cwd=base)
    return r.returncode, r.stdout + r.stderr


def verificar(camada, python=sys.executable, base_origem=RAIZ):
    """Cada trecho, trocado sozinho, tem de derrubar o teste do seu lab; sem troca, tudo passa."""
    inv, erros = inventario(base_origem)
    if erros:
        return erros
    falhas = []
    with tempfile.TemporaryDirectory(prefix="exercicios-") as tmp:
        for c in CAMADAS:  # a camada 3 importa laboratorios/comum, então copia as duas
            _copiar_camada(base_origem, tmp, c)
        cod, saida = _rodar(python, tmp, camada)
        if cod != 0:
            return [f"controle: a cópia sem troca falhou\n{saida[-1500:]}"]
        for nome, itens in inv[camada].items():
            for arq, lista in itens:
                copia = os.path.join(tmp, os.path.relpath(arq, base_origem))
                original = open(copia, encoding="utf-8").read()
                for k, (ini, _f, _i, _d, funcao) in enumerate(lista):
                    with open(copia, "w", encoding="utf-8") as f:
                        f.write(transformar(original, copia, apenas=k)[0])
                    cod, saida = _rodar(python, tmp, camada, nome)
                    if cod == 0 or "NotImplementedError" not in saida:
                        falhas.append(f"{os.path.relpath(arq, base_origem)}:{ini + 1} {funcao}: nenhum teste detectou a remoção")
                with open(copia, "w", encoding="utf-8") as f:
                    f.write(original)
    return falhas


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--destino", default=DESTINO_PADRAO)
    ap.add_argument("--alvo", action="append", default=[], help="refaz só este lab/projeto na cópia (repetível)")
    ap.add_argument("--forcar", action="store_true", help="sobrescreve o destino (apaga o que você implementou nele)")
    ap.add_argument("--checar", action="store_true", help="só valida os marcadores dos originais")
    ap.add_argument("--verificar", choices=("labs", "mercado"))
    args = ap.parse_args()

    if args.checar:
        inv, erros = inventario()
        for e in erros:
            print("FALHA", e)
        total = sum(len(t) for labs in inv.values() for itens in labs.values() for _, t in itens)
        print(f"{'OK' if not erros else 'FALHA'} {total} trechos em {sum(len(l) for l in inv.values())} labs")
        return 1 if erros else 0
    if args.verificar:
        camada = "laboratorios" if args.verificar == "labs" else "laboratorios-mercado"
        falhas = verificar(camada)
        for f in falhas:
            print("FALHA", f)
        print("OK cada trecho é coberto por teste" if not falhas else f"FALHA {len(falhas)} trecho(s)")
        return 1 if falhas else 0
    n = gerar(args.destino, args.alvo, args.forcar)
    print(f"OK {n} trechos trocados em {os.path.relpath(os.path.realpath(args.destino), RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
