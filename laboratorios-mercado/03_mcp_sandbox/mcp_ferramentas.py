"""Servidor MCP real da Aurora Educação (projeto 03), SDK oficial `mcp` 2.x.

Ferramentas:
- `consultar_prazo` (somente leitura): prazos acadêmicos fictícios.
- `calcular_media_ponderada` (somente leitura): entrada validada por Pydantic (notas 0–10, pesos > 0).
- `executar_python_isolado` (risco alto): só roda após **aprovação humana** pedida ao cliente por
  *elicitation* do MCP, vinculada ao hash exato do código; sem suporte do cliente ou sem
  aprovação, nega (falha fechada). Execução em container restrito (`mcp_sandbox_exec`).

Transportes:
    python -I mcp_ferramentas.py --transporte stdio
    python -I mcp_ferramentas.py --transporte streamable-http --porta 8765   # http://127.0.0.1:8765/mcp
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base  # noqa: E402,F401

import mcp.types as types  # noqa: E402
from mcp.server.mcpserver import Context, MCPServer  # noqa: E402

PRAZOS = {
    "rematricula": "Até o décimo dia útil do início das aulas.",
    "trancamento": "Até a metade do semestre letivo.",
    "revisao_de_prova": "Até 7 dias úteis após a divulgação da nota.",
}


class Nota(BaseModel):
    valor: Annotated[float, Field(ge=0, le=10, description="nota de 0 a 10")]
    peso: Annotated[float, Field(gt=0, le=100, description="peso relativo")]


class ResultadoMedia(BaseModel):
    media: float
    aprovado: bool
    regra: str


class Aprovacao(BaseModel):
    """Formulário de elicitation (só tipos primitivos, como exige a especificação)."""

    aprovar: bool = Field(description="Aprova a execução deste código exato?")
    responsavel: str = Field(default="", description="Nome de quem aprovou (auditoria)")


class ResultadoExecucao(BaseModel):
    executado: bool
    motivo: str
    sha256_codigo: str
    codigo_saida: Optional[int] = None
    saida: str = ""
    erro: str = ""
    aprovado_por: str = ""


def sha_codigo(codigo: str) -> str:
    return hashlib.sha256(codigo.encode("utf-8")).hexdigest()


def criar_servidor(executor=None, auditoria: Optional[List[dict]] = None) -> MCPServer:
    """Fábrica do servidor. `executor` (com `.executar(codigo)`) é injetável; padrão: container real."""
    srv = MCPServer("aurora-ferramentas", instructions="Ferramentas acadêmicas fictícias da Aurora Educação.")
    registro = auditoria if auditoria is not None else []

    @srv.tool(description="Consulta o prazo de um processo acadêmico.",
              annotations=types.ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False))
    def consultar_prazo(processo: Literal["rematricula", "trancamento", "revisao_de_prova"]) -> str:
        return PRAZOS[processo]

    @srv.tool(description="Calcula a média ponderada e aplica a regra de aprovação (>= 6,0).",
              annotations=types.ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False))
    def calcular_media_ponderada(notas: Annotated[List[Nota], Field(min_length=1, max_length=20)]) -> ResultadoMedia:
        total = sum(n.peso for n in notas)
        media = round(sum(n.valor * n.peso for n in notas) / total, 2)
        return ResultadoMedia(media=media, aprovado=media >= 6.0, regra="aprovado se média >= 6,0")

    @srv.tool(description="Executa código Python em container sem rede, só após aprovação humana.",
              annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True, openWorldHint=False))
    async def executar_python_isolado(
        codigo: Annotated[str, Field(min_length=1, max_length=2000)], ctx: Context
    ) -> ResultadoExecucao:
        digest = sha_codigo(codigo)
        try:
            resposta = await ctx.elicit(
                message=f"Aprovar a execução isolada deste código (sha256 {digest[:12]})?\n\n{codigo}",
                schema=Aprovacao,
            )
        except Exception as exc:  # cliente sem elicitation, transporte sem canal de volta etc.
            registro.append({"sha256": digest, "decisao": "negado", "motivo": type(exc).__name__})
            return ResultadoExecucao(executado=False, motivo="aprovação humana indisponível (negado por padrão)",
                                     sha256_codigo=digest)
        if resposta.action != "accept" or not resposta.data.aprovar:
            registro.append({"sha256": digest, "decisao": "negado", "motivo": resposta.action})
            return ResultadoExecucao(executado=False, motivo=f"não aprovado ({resposta.action})", sha256_codigo=digest)
        quem = resposta.data.responsavel.strip() or "não informado"
        registro.append({"sha256": digest, "decisao": "aprovado", "responsavel": quem})
        exe = executor
        if exe is None:
            from mcp_sandbox_exec import ExecutorConteiner
            exe = ExecutorConteiner()
        r = exe.executar(codigo)
        return ResultadoExecucao(executado=True, motivo="tempo limite" if r.expirou else "concluído",
                                 sha256_codigo=digest, codigo_saida=r.codigo_saida, saida=r.saida,
                                 erro=r.erro, aprovado_por=quem)

    return srv


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--transporte", choices=["stdio", "streamable-http"], default="stdio")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--porta", type=int, default=8765)
    args = ap.parse_args(argv)
    srv = criar_servidor()
    if args.transporte == "stdio":
        srv.run("stdio")
    else:
        srv.run("streamable-http", host=args.host, port=args.porta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
