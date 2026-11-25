"""Adaptador próprio MCP → nós do grafo (projeto 08), sobre o cliente `mcp` 2.x já usado no P03 e no P06.

Sem `langchain-mcp-adapters` (compatibilidade com `mcp` 2.x não confirmada em 25/11/2026). Lista as
ferramentas do servidor, marca como **sensível** toda ferramenta sem `readOnlyHint` e executa um lote de
chamadas numa sessão. A *elicitation* do servidor (segunda trava do P03) só é aceita para a chamada que
o grafo já aprovou por `interrupt()`; qualquer outra é recusada (falha fechada).
"""
from __future__ import annotations

import asyncio
import json
from typing import Dict, List, Sequence, Set, Tuple

import mcp.types as types
from mcp import Client

from integrador_app import mcp_tools_para_openai


class FerramentasMCP:
    def __init__(self, servidor):
        self.servidor = servidor
        tools = asyncio.run(self._listar())
        self.tools_openai: List[Dict[str, object]] = mcp_tools_para_openai(tools)
        self.nomes: Set[str] = {t.name for t in tools}
        self.sensiveis: Set[str] = {t.name for t in tools if not (t.annotations and t.annotations.read_only_hint)}

    async def _listar(self):
        async with Client(self.servidor, mode="legacy") as c:
            return (await c.list_tools()).tools

    def tools_para(self, permitidas: Set[str]) -> List[Dict[str, object]]:
        return [t for t in self.tools_openai if t["function"]["name"] in permitidas]

    def executar_lote(self, chamadas: Sequence[Tuple[str, Dict[str, object], bool]]) -> List[Tuple[str, bool]]:
        """Executa `(nome, argumentos, aprovado_por_humano)` em ordem; devolve `(texto, sucesso)` por chamada."""
        return asyncio.run(self._executar(list(chamadas)))

    async def _executar(self, chamadas) -> List[Tuple[str, bool]]:
        aprovada = {"agora": False}

        async def elicitacao(_context, params):
            if getattr(params, "mode", "form") == "form" and aprovada["agora"]:
                return types.ElicitResult(action="accept", content={"aprovar": True, "responsavel": "interrupt-langgraph"})
            return types.ElicitResult(action="decline")

        saida: List[Tuple[str, bool]] = []
        async with Client(self.servidor, mode="legacy", elicitation_callback=elicitacao) as c:
            for nome, argumentos, aprovado in chamadas:
                aprovada["agora"] = bool(aprovado)
                r = await c.call_tool(nome, argumentos)
                texto = str(getattr(r.content[0], "text", "") or "") if r.content else ""
                if not texto and getattr(r, "structured_content", None) is not None:
                    texto = json.dumps(r.structured_content, ensure_ascii=False)
                saida.append((texto or "{}", not r.is_error and bool(texto)))
        return saida
