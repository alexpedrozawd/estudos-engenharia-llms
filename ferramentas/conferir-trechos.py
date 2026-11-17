"""Confere se cada trecho literal do pacote de fontes existe no texto da fonte.

Uso (Python com -I, só biblioteca padrão):
    python -I conferir-trechos.py --pacote pacotes-de-fontes-capitulo-1.md --textos <pasta-textos> --projeto <pasta-do-projeto>

Fontes: <pasta-textos>/<chave>.txt (PDF e páginas extraídas) ou <pasta-projeto>/<chave>.md (contextos de estudo).
Linhas de tabela do pacote: ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho.
Comparação: remove quebras de linha com hifenização, espaços e diferenças de caixa.
Saída: aprovados e reprovados por trecho e por unidade. Código de saída 1 se houver reprovação.
"""
import argparse
import os
import re
import sys

COLUNAS = 8


def normalizar(texto):
    texto = re.sub(r"-\s+", "", texto)  # hifenização de fim de linha
    texto = re.sub(r"\s+", "", texto)  # espaços e quebras
    return texto.lower()


def ler_pacote(caminho):
    linhas_tabela = []
    unidade_atual = None
    with open(caminho, encoding="utf-8") as arq:
        for numero, linha in enumerate(arq, 1):
            s = linha.strip()
            if s.startswith("## "):
                unidade_atual = s[3:].strip()
            if not s.startswith("|"):
                continue
            celulas = [c.strip() for c in s.strip("|").split("|")]
            if len(celulas) != COLUNAS:
                continue
            if celulas[0] in ("ID",) or set(celulas[0]) <= set("-: "):
                continue
            linhas_tabela.append((numero, unidade_atual, celulas))
    return linhas_tabela


def localizar_fonte(chave, textos, projeto):
    for pasta, ext in ((textos, ".txt"), (projeto, ".md")):
        if not pasta:
            continue
        caminho = os.path.join(pasta, chave + ext)
        if os.path.isfile(caminho):
            with open(caminho, encoding="utf-8", errors="replace") as arq:
                return caminho, arq.read()
    return None, None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pacote", required=True)
    parser.add_argument("--textos", required=True)
    parser.add_argument("--projeto", required=True)
    args = parser.parse_args()

    linhas = ler_pacote(args.pacote)
    cache = {}
    resultados = {}
    for numero, unidade, cel in linhas:
        id_, _unid, tipo, fonte, local, _edicao, _qual, trecho = cel
        if tipo not in ("texto", "caso"):
            print(f"AVISO linha {numero}: tipo desconhecido '{tipo}' em {id_}")
        if fonte not in cache:
            cache[fonte] = localizar_fonte(fonte, args.textos, args.projeto)
        caminho, corpo = cache[fonte]
        if corpo is None:
            status, motivo = "REPROVADO", f"fonte '{fonte}' não encontrada"
        elif not trecho or trecho.startswith("("):
            status, motivo = "REPROVADO", f"trecho ausente na fonte ({trecho or 'vazio'})"
        elif normalizar(trecho) in normalizar(corpo):
            status, motivo = "APROVADO", ""
        else:
            status, motivo = "REPROVADO", "trecho não encontrado no texto da fonte"
        resultados.setdefault(unidade, []).append((id_, status, motivo, local))
        print(f"{status:9} {id_:6} {fonte:28} {local}" + (f"  -> {motivo}" if motivo else ""))

    aprovados = sum(1 for r in resultados.values() for x in r if x[1] == "APROVADO")
    reprovados = sum(1 for r in resultados.values() for x in r if x[1] == "REPROVADO")
    print()
    print("Pacotes por unidade:")
    for unidade, itens in resultados.items():
        ok = all(x[1] == "APROVADO" for x in itens)
        print(f"  {'APROVADO' if ok else 'REPROVADO':9} {unidade}")
    print()
    print(f"Trechos: {aprovados} aprovados, {reprovados} reprovados (total {aprovados + reprovados}).")
    return 1 if reprovados else 0


if __name__ == "__main__":
    sys.exit(main())
