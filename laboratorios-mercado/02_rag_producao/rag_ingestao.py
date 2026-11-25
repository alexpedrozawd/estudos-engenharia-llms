"""Ingestão de PDFs com tabelas para RAG (projeto 02).

Lição de produção: tabelas não podem ser fatiadas no meio de uma linha nem perder o
cabeçalho. Aqui o PDF é lido em modo `layout` (pypdf preserva o alinhamento das colunas),
blocos com 2+ linhas consecutivas em colunas viram trechos do tipo `tabela` em Markdown,
com o cabeçalho repetido em cada pedaço, e o texto corrido é fatiado por palavras com
sobreposição.

Limite declarado: PDFs escaneados (imagem) e tabelas sem alinhamento textual exigem OCR
ou extratores de layout dedicados; ficam fora deste laboratório.
"""
from __future__ import annotations

import io
import re
from dataclasses import dataclass
from typing import List, Sequence, Tuple, Union

from pypdf import PdfReader

SEPARADOR_COLUNAS = re.compile(r"\s{3,}")
PERFIS_PADRAO: Tuple[str, ...] = ("publico", "aluno", "docente", "coordenacao", "admin")


@dataclass(frozen=True)
class Trecho:
    id: str
    doc: str
    pagina: int
    tipo: str  # "texto" ou "tabela"
    texto: str
    perfis: Tuple[str, ...] = PERFIS_PADRAO
    departamento: str = "geral"
    versao: str = "2026"
    vigente: bool = True


def extrair_paginas_pdf(origem: Union[str, bytes]) -> List[str]:
    """Extrai o texto de cada página preservando o alinhamento horizontal."""
    fluxo = io.BytesIO(origem) if isinstance(origem, (bytes, bytearray)) else open(origem, "rb")
    with fluxo:
        leitor = PdfReader(fluxo)
        return [p.extract_text(extraction_mode="layout") or "" for p in leitor.pages]


def _celulas(linha: str) -> List[str]:
    return [c.strip() for c in SEPARADOR_COLUNAS.split(linha.strip()) if c.strip()]


def separar_blocos(texto_pagina: str) -> List[tuple]:
    """Divide a página em blocos ("texto", linhas) e ("tabela", linhas de células)."""
    blocos: List[tuple] = []
    atual_tipo, atual = None, []
    for linha in texto_pagina.splitlines():
        if not linha.strip():
            continue
        cels = _celulas(linha)
        tipo = "tabela" if len(cels) >= 2 else "texto"
        if tipo != atual_tipo and atual:
            blocos.append((atual_tipo, atual))
            atual = []
        atual_tipo = tipo
        atual.append(cels if tipo == "tabela" else linha.strip())
    if atual:
        blocos.append((atual_tipo, atual))
    # Uma "tabela" de uma linha só é texto com espaçamento largo, não tabela.
    normalizados = []
    for tipo, linhas in blocos:
        if tipo == "tabela" and len(linhas) < 2:
            normalizados.append(("texto", ["  ".join(linhas[0])]))
        else:
            normalizados.append((tipo, linhas))
    return normalizados


def tabela_markdown(cabecalho: Sequence[str], linhas: Sequence[Sequence[str]]) -> str:
    def fmt(cels: Sequence[str]) -> str:
        return "| " + " | ".join(cels) + " |"

    return "\n".join([fmt(cabecalho), fmt(["---"] * len(cabecalho))] + [fmt(l) for l in linhas])


def fatiar_texto(palavras: List[str], max_palavras: int, sobreposicao: int) -> List[str]:
    # EXERCICIO-INICIO: janelas de max_palavras que avançam max_palavras − sobreposicao; valide max_palavras > sobreposicao.
    if max_palavras <= sobreposicao:
        raise ValueError("max_palavras deve ser maior que sobreposicao")
    pedacos, i = [], 0
    while i < len(palavras):
        pedacos.append(" ".join(palavras[i:i + max_palavras]))
        if i + max_palavras >= len(palavras):
            break
        i += max_palavras - sobreposicao
    return pedacos
    # EXERCICIO-FIM


def segmentar(
    paginas: Sequence[str],
    doc: str,
    *,
    max_palavras: int = 80,
    sobreposicao: int = 15,
    max_linhas_tabela: int = 8,
    perfis: Sequence[str] = PERFIS_PADRAO,
    departamento: str = "geral",
    versao: str = "2026",
    vigente: bool = True,
) -> List[Trecho]:
    """Gera trechos estáveis (`doc:p<página>:<n>`) de texto e de tabela com metadados e ACL."""
    perfis_t = tuple(perfis)
    trechos: List[Trecho] = []
    for num, texto in enumerate(paginas, start=1):
        n = 0
        for tipo, linhas in separar_blocos(texto):
            if tipo == "tabela":
                cab, corpo = linhas[0], linhas[1:]
                for i in range(0, len(corpo), max_linhas_tabela):
                    n += 1
                    trechos.append(
                        Trecho(
                            f"{doc}:p{num}:{n}",
                            doc,
                            num,
                            "tabela",
                            tabela_markdown(cab, corpo[i:i + max_linhas_tabela]),
                            perfis=perfis_t,
                            departamento=departamento,
                            versao=versao,
                            vigente=vigente,
                        )
                    )
            else:
                for pedaco in fatiar_texto(" ".join(linhas).split(), max_palavras, sobreposicao):
                    n += 1
                    trechos.append(
                        Trecho(
                            f"{doc}:p{num}:{n}",
                            doc,
                            num,
                            "texto",
                            pedaco,
                            perfis=perfis_t,
                            departamento=departamento,
                            versao=versao,
                            vigente=vigente,
                        )
                    )
    return trechos
