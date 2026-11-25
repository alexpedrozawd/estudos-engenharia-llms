"""Base comum da Camada 3 (laboratorios-mercado).

Prepara `sys.path` para os seis projetos (pastas `01_*`..`06_*`, que não são pacotes
importáveis por começarem com dígito) e para `laboratorios/comum` (cliente neutro
reutilizado), e oferece utilidades determinísticas compartilhadas.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from typing import Dict, Iterable, Iterator, List, Optional, Sequence

RAIZ_MERCADO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ_REPO = os.path.dirname(RAIZ_MERCADO)
PASTA_LABS = os.path.join(RAIZ_REPO, "laboratorios")
PASTA_EXECUCOES = os.path.join(RAIZ_MERCADO, "execucoes")
PROJETOS = (
    "01_serving_local",
    "02_rag_producao",
    "03_mcp_sandbox",
    "04_qlora_peft",
    "05_api_llmops",
    "06_integrador_producao",
)


def preparar_caminhos() -> None:
    """Insere raiz da Camada 3, pastas dos projetos e `laboratorios/` em `sys.path` (idempotente)."""
    caminhos = [RAIZ_MERCADO, PASTA_LABS] + [os.path.join(RAIZ_MERCADO, p) for p in PROJETOS]
    for caminho in reversed(caminhos):
        if os.path.isdir(caminho) and caminho not in sys.path:
            sys.path.insert(0, caminho)


preparar_caminhos()


def percentil(valores: Sequence[float], p: float) -> float:
    """Percentil com interpolação linear (mesma convenção de `numpy.percentile` padrão)."""
    if not valores:
        return float("nan")
    if not 0.0 <= p <= 100.0:
        raise ValueError("p deve estar entre 0 e 100")
    ordenados = sorted(valores)
    if len(ordenados) == 1:
        return float(ordenados[0])
    pos = (len(ordenados) - 1) * p / 100.0
    baixo = math.floor(pos)
    alto = math.ceil(pos)
    if baixo == alto:
        return float(ordenados[int(pos)])
    return float(ordenados[baixo] + (ordenados[alto] - ordenados[baixo]) * (pos - baixo))


def sha256_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def sha256_arquivo(caminho: str) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def registrar_execucao(nome: str, dados: Dict[str, object], pasta: Optional[str] = None) -> str:
    """Grava o registro JSON de uma execução real em `execucoes/` e devolve o caminho."""
    destino = pasta or PASTA_EXECUCOES
    os.makedirs(destino, exist_ok=True)
    carimbo = time.strftime("%Y-%m-%dT%H-%M-%S%z")
    caminho = os.path.join(destino, f"{nome}-{carimbo}.json")
    registro = {"execucao": nome, "carimbo": carimbo, **dados}
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return caminho


def iterar_eventos_sse(linhas: Iterable[str]) -> Iterator[Dict[str, object]]:
    """Converte linhas `data: {...}` de streaming compatível com OpenAI em dicionários.

    Ignora comentários, linhas vazias e o marcador final `[DONE]`.
    """
    for linha in linhas:
        linha = linha.strip()
        if not linha.startswith("data:"):
            continue
        conteudo = linha[len("data:"):].strip()
        if not conteudo or conteudo == "[DONE]":
            continue
        try:
            yield json.loads(conteudo)
        except json.JSONDecodeError:
            continue


def extrair_delta(evento: Dict[str, object]) -> Dict[str, str]:
    """Separa conteúdo visível e raciocínio de um evento de streaming OpenAI-compatível."""
    escolhas = evento.get("choices") or []
    if not escolhas:
        return {"conteudo": "", "raciocinio": ""}
    delta = (escolhas[0] or {}).get("delta") or {}
    raciocinio = delta.get("reasoning_content") or delta.get("reasoning") or ""
    return {"conteudo": str(delta.get("content") or ""), "raciocinio": str(raciocinio)}


def _escapar_pdf(texto: str) -> str:
    return texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def gerar_pdf_texto(paginas: List[List[object]]) -> bytes:
    """Gera um PDF mínimo válido, sem dependências, com texto posicionado.

    Cada página é uma lista de linhas; cada linha é `str` (texto corrido) ou
    lista de células (`list[str]`), posicionadas em colunas fixas para simular tabela.
    Só caracteres Latin-1 (WinAnsi) são suportados, o que cobre o português.
    """
    objetos: List[bytes] = []

    def adicionar(corpo: bytes) -> int:
        objetos.append(corpo)
        return len(objetos)

    fonte = adicionar(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    id_paginas = len(objetos) + 1
    objetos.append(b"")  # placeholder de /Pages
    kids: List[int] = []
    for linhas in paginas:
        comandos = ["BT", "/F1 11 Tf", "14 TL"]
        y = 800
        for linha in linhas:
            celulas = linha if isinstance(linha, list) else [linha]
            for i, celula in enumerate(celulas):
                x = 50 + i * 150 if isinstance(linha, list) else 50
                comandos.append(f"1 0 0 1 {x} {y} Tm ({_escapar_pdf(str(celula))}) Tj")
            y -= 16
        comandos.append("ET")
        fluxo = "\n".join(comandos).encode("latin-1")
        conteudo = adicionar(b"<< /Length %d >>\nstream\n" % len(fluxo) + fluxo + b"\nendstream")
        pagina = adicionar(
            (
                f"<< /Type /Page /Parent {id_paginas} 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 {fonte} 0 R >> >> /Contents {conteudo} 0 R >>"
            ).encode("ascii")
        )
        kids.append(pagina)
    objetos[id_paginas - 1] = (
        f"<< /Type /Pages /Kids [{' '.join(f'{k} 0 R' for k in kids)}] /Count {len(kids)} >>"
    ).encode("ascii")
    catalogo = adicionar(f"<< /Type /Catalog /Pages {id_paginas} 0 R >>".encode("ascii"))

    saida = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    deslocamentos = []
    for i, corpo in enumerate(objetos, start=1):
        deslocamentos.append(len(saida))
        saida += f"{i} 0 obj\n".encode("ascii") + corpo + b"\nendobj\n"
    inicio_xref = len(saida)
    saida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode("ascii")
    for d in deslocamentos:
        saida += f"{d:010d} 00000 n \n".encode("ascii")
    saida += (
        f"trailer\n<< /Size {len(objetos) + 1} /Root {catalogo} 0 R >>\nstartxref\n{inicio_xref}\n%%EOF\n"
    ).encode("ascii")
    return bytes(saida)
