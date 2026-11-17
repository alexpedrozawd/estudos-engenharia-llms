"""Renumerador das páginas lógicas do guia (somente leitura por padrão).

Uso (Python com -I, só biblioteca padrão):
    python -I renumerar-paginas.py --guia <caminho>/guia-engenharia-llms.html          # confere
    python -I renumerar-paginas.py --guia <caminho>/guia-engenharia-llms.html --aplicar # grava

Percorre as seções `<section class="page">` na ordem do documento e reescreve cada
`<span class="page-number" aria-label="Página N">N</span>` com a sequência 1..N.
Não mexe em nenhum outro número: as referências textuais do guia são a partes («parte 9.2c»)
e a páginas de fontes («p. 13»), não a páginas lógicas.

Depois de fundir ou remover partes, rode este script e em seguida validar-guia.py, que confere
a sequência 1..N e os links internos. O modo --conferir só relata o que mudaria.
"""
import argparse
import re
import sys

SECAO_TXT = '<section class="page"'
SECAO = re.compile(SECAO_TXT)
NUMERO = re.compile(r'(<span class="page-number" aria-label="Página )(\d+)(">)(\d+)(</span>)')


def analisar(texto):
    partes = SECAO.split(texto)
    cabecalho, secoes = partes[0], partes[1:]
    return cabecalho, secoes


def renumerar(texto):
    """Devolve (novo_texto, total, alteracoes) com a sequência 1..N aplicada."""
    cabecalho, secoes = analisar(texto)
    alteracoes = []
    saida = [cabecalho]
    for indice, secao in enumerate(secoes, start=1):
        achados = NUMERO.findall(secao)

        def trocar(m, novo=indice):
            antigo = int(m.group(2))
            if antigo != novo or int(m.group(4)) != novo:
                alteracoes.append((antigo, novo))
            return f"{m.group(1)}{novo}{m.group(3)}{novo}{m.group(5)}"

        if achados:
            secao = NUMERO.sub(trocar, secao)
        saida.append(secao)
    return SECAO_TXT.join(saida), len(secoes), alteracoes


def main():
    ap = argparse.ArgumentParser(description="Renumera as páginas lógicas do guia HTML.")
    ap.add_argument("--guia", required=True, help="caminho do guia-engenharia-llms.html")
    ap.add_argument("--aplicar", action="store_true", help="grava o arquivo (padrão: só relata)")
    args = ap.parse_args()

    with open(args.guia, encoding="utf-8") as f:
        original = f.read()

    novo, total, alteracoes = renumerar(original)
    sem_marcador = []
    _, secoes = analisar(original)
    for indice, secao in enumerate(secoes, start=1):
        achados = NUMERO.findall(secao)
        if len(achados) != 1:
            identificador = re.search(r'id="([^"]+)"', secao[:400])
            sem_marcador.append((indice, identificador.group(1) if identificador else "?"))

    print(f"páginas encontradas: {total}")
    if sem_marcador:
        print("seções sem exatamente um marcador de página:")
        for indice, identificador in sem_marcador:
            print(f"  posição {indice}: {identificador}")
    if alteracoes:
        print(f"marcadores a corrigir: {len(alteracoes)}")
        for antigo, novo_num in alteracoes[:20]:
            print(f"  {antigo} → {novo_num}")
        if len(alteracoes) > 20:
            print(f"  ... e mais {len(alteracoes) - 20}")
    else:
        print("numeração já está em sequência 1..N; nada a mudar")

    if args.aplicar:
        if not alteracoes and not sem_marcador:
            print("arquivo não alterado")
        else:
            with open(args.guia, "w", encoding="utf-8") as f:
                f.write(novo)
            print(f"gravado: {args.guia}")
    return 0 if not sem_marcador else 1


if __name__ == "__main__":
    sys.exit(main())
