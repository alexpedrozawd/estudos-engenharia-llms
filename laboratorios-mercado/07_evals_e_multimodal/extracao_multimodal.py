"""Extração multimodal de faturas/recibos em PDF via pdftoppm + payload image_url + Pydantic (Projeto 07)."""
from __future__ import annotations

import base64
import glob
import os
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base.cliente_openai import gerar_estruturado  # noqa: E402


class ItemFatura(BaseModel):
    descricao: str = Field(min_length=1)
    quantidade: int = Field(ge=1)
    valor_unitario: float = Field(ge=0.0)
    subtotal: float = Field(ge=0.0)


class FaturaExtraida(BaseModel):
    documento: str = Field(min_length=1)
    data_emissao: str = Field(min_length=4)
    itens: List[ItemFatura] = Field(min_length=1)
    total_informado: float = Field(ge=0.0)


def gerar_pdf_recibo_aurora(
    itens: Optional[Sequence[Tuple[str, int, float]]] = None,
    *,
    documento: str = "REC-2026-0042",
    data_emissao: str = "2026-11-24",
) -> bytes:
    """Gera um recibo didático em PDF para exercitar renderização PNG e extração multimodal."""
    lista = list(itens) if itens is not None else [
        ("Segunda via de diploma", 1, 120.00),
        ("Historico escolar", 2, 25.00),
        ("Cartao biblioteca", 1, 18.00),
    ]
    total = sum(q * v for _, q, v in lista)
    linhas: List[object] = [
        f"Aurora Educacao - Recibo de Servicos ({documento})",
        f"Data de emissao: {data_emissao}",
        ["Descricao", "Qtd", "Unitario (R$)", "Subtotal (R$)"],
    ]
    for desc, qtd, unit in lista:
        linhas.append([desc, str(qtd), f"{unit:.2f}", f"{qtd * unit:.2f}"])
    linhas.append(f"Total informado: R$ {total:.2f}")
    return mb.gerar_pdf_texto([linhas])


def renderizar_pdf_pngs(origem: Union[bytes, str], *, dpi: int = 150) -> List[bytes]:
    """Renderiza cada página do PDF para PNG usando `pdftoppm` (poppler-utils)."""
    with tempfile.TemporaryDirectory(prefix="vlm-pdf-") as tmp:
        if isinstance(origem, (bytes, bytearray)):
            caminho_pdf = os.path.join(tmp, "entrada.pdf")
            with open(caminho_pdf, "wb") as f:
                f.write(bytes(origem))
        else:
            caminho_pdf = str(origem)
        prefixo = os.path.join(tmp, "pagina")
        proc = subprocess.run(
            ["pdftoppm", "-png", "-r", str(dpi), caminho_pdf, prefixo],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"pdftoppm falhou ({proc.returncode}): {proc.stderr.strip()}")
        arquivos = sorted(glob.glob(f"{prefixo}*.png"))
        if not arquivos:
            raise RuntimeError("pdftoppm não produziu imagens PNG")
        saida: List[bytes] = []
        for arq in arquivos:
            with open(arq, "rb") as f:
                saida.append(f.read())
        return saida


def montar_mensagens_vlm(pngs: Sequence[bytes], instrucao: str) -> List[Dict[str, object]]:
    """Monta payload OpenAI multimodal (`image_url` em base64) a partir de PNGs renderizados."""
    if not pngs:
        raise ValueError("lista de imagens PNG vazia")
    conteudo: List[Dict[str, object]] = [{"type": "text", "text": instrucao}]
    for img in pngs:
        b64 = base64.b64encode(img).decode("ascii")
        conteudo.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"},
        })
    return [
        {
            "role": "system",
            "content": "Extraia os campos da fatura estritamente no esquema JSON solicitado, sem inventar valores.",
        },
        {"role": "user", "content": conteudo},
    ]


def validar_totais_fatura(fatura: FaturaExtraida, tolerancia: float = 0.01) -> Dict[str, object]:
    """Auditoria aritmética determinística (code-first): subtotais e soma total."""
    divergencias: List[str] = []
    soma_calculada = 0.0
    for idx, item in enumerate(fatura.itens, start=1):
        esperado_item = round(item.quantidade * item.valor_unitario, 2)
        if abs(esperado_item - item.subtotal) > tolerancia:
            divergencias.append(
                f"item {idx} ({item.descricao}): esperado {esperado_item:.2f}, extraido {item.subtotal:.2f}"
            )
        soma_calculada += item.subtotal
    soma_calculada = round(soma_calculada, 2)
    if abs(soma_calculada - fatura.total_informado) > tolerancia:
        divergencias.append(
            f"total: soma dos itens {soma_calculada:.2f} != total_informado {fatura.total_informado:.2f}"
        )
    return {
        "valido": not divergencias,
        "soma_calculada": soma_calculada,
        "total_informado": round(fatura.total_informado, 2),
        "divergencias": divergencias,
    }


def extrair_fatura_de_pdf(
    origem: Union[bytes, str],
    cliente_vlm,
    *,
    dpi: int = 150,
    max_reparos: int = 2,
) -> Dict[str, object]:
    """Pipeline completo: PDF -> PNG (pdftoppm) -> VLM estruturado (Pydantic) -> checagem matemática."""
    pngs = renderizar_pdf_pngs(origem, dpi=dpi)
    mensagens = montar_mensagens_vlm(
        pngs,
        "Extraia numero do documento, data de emissao, lista de itens (descricao, quantidade, "
        "valor_unitario, subtotal) e total_informado.",
    )
    fatura, meta = gerar_estruturado(cliente_vlm, mensagens, FaturaExtraida, max_reparos=max_reparos)
    auditoria = validar_totais_fatura(fatura)
    return {
        "fatura": fatura.model_dump(),
        "auditoria_totais": auditoria,
        "paginas_png": len(pngs),
        "bytes_png": [len(p) for p in pngs],
        "metadados_llm": meta,
    }
