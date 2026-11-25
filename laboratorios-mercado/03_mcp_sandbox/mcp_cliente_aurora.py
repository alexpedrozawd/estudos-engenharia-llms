"""Cliente MCP real (projeto 03): conecta por stdio ou Streamable HTTP e encaminha aprovações a um humano.

Exemplos:
    # stdio: o cliente inicia o servidor como subprocesso
    .venv-mercado/bin/python -I laboratorios-mercado/03_mcp_sandbox/mcp_cliente_aurora.py --stdio
    # Streamable HTTP: servidor já em execução
    .venv-mercado/bin/python -I laboratorios-mercado/03_mcp_sandbox/mcp_cliente_aurora.py --url http://127.0.0.1:8765/mcp

Aprovação: `--aprovacao terminal` (pergunta no terminal, padrão), `negar` (nega tudo) ou
`aprovar-automatico` (só para demonstração registrada; nunca em produção).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from typing import Awaitable, Callable, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

import mcp.types as types  # noqa: E402
from mcp import Client, StdioServerParameters  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGO_DEMO = "import sys, platform\nprint('olá da sandbox', platform.python_version(), sys.flags.isolated)"
CODIGO_REDE = "import socket\ns = socket.create_connection(('1.1.1.1', 53), timeout=3)\nprint('rede aberta')"

Aprovador = Callable[[str], Awaitable[Dict[str, object]]]


def criar_callback(aprovador: Aprovador):
    """Adapta um aprovador (mensagem → {'aprovar', 'responsavel'}) ao callback de elicitation do SDK."""

    async def callback(context, params):
        if getattr(params, "mode", "form") != "form":
            return types.ElicitResult(action="decline")
        decisao = await aprovador(params.message)
        if decisao is None:
            return types.ElicitResult(action="cancel")
        return types.ElicitResult(action="accept", content={
            "aprovar": bool(decisao.get("aprovar")), "responsavel": str(decisao.get("responsavel", ""))})

    return callback


async def aprovador_terminal(mensagem: str) -> Optional[Dict[str, object]]:
    print("\n=== PEDIDO DE APROVAÇÃO ===\n" + mensagem)
    resposta = await asyncio.to_thread(input, "Aprovar? [s/N] ")
    return {"aprovar": resposta.strip().lower() in ("s", "sim"), "responsavel": os.environ.get("USER", "")}


async def aprovador_negar(mensagem: str) -> Dict[str, object]:
    return {"aprovar": False, "responsavel": "politica-negar"}


async def aprovador_automatico(mensagem: str) -> Dict[str, object]:
    return {"aprovar": True, "responsavel": "demonstracao-automatica"}


async def demonstrar(alvo, aprovador: Aprovador) -> Dict[str, object]:
    """Lista ferramentas, chama as de leitura, testa validação e pede execução isolada."""
    saida: Dict[str, object] = {}
    async with Client(alvo, mode="legacy", elicitation_callback=criar_callback(aprovador)) as c:
        ferramentas = (await c.list_tools()).tools
        saida["ferramentas"] = {
            f.name: {"somente_leitura": bool(f.annotations and f.annotations.read_only_hint),
                     "destrutiva": bool(f.annotations and f.annotations.destructive_hint)}
            for f in ferramentas
        }
        r = await c.call_tool("consultar_prazo", {"processo": "rematricula"})
        saida["consultar_prazo"] = r.content[0].text
        r = await c.call_tool("calcular_media_ponderada",
                              {"notas": [{"valor": 7.0, "peso": 60}, {"valor": 5.0, "peso": 30}, {"valor": 10, "peso": 10}]})
        saida["calcular_media_ponderada"] = r.structured_content
        r = await c.call_tool("calcular_media_ponderada", {"notas": [{"valor": 11, "peso": 1}]})
        saida["validacao_rejeita_nota_11"] = r.is_error
        r = await c.call_tool("executar_python_isolado", {"codigo": CODIGO_DEMO})
        saida["executar_python_isolado"] = r.structured_content
        r = await c.call_tool("executar_python_isolado", {"codigo": CODIGO_REDE})
        saida["executar_sem_rede"] = r.structured_content
    return saida


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--stdio", action="store_true")
    grupo.add_argument("--url")
    ap.add_argument("--aprovacao", choices=["terminal", "negar", "aprovar-automatico"], default="terminal")
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    aprovador = {"terminal": aprovador_terminal, "negar": aprovador_negar,
                 "aprovar-automatico": aprovador_automatico}[args.aprovacao]
    if args.stdio:
        alvo = StdioServerParameters(command=sys.executable,
                                     args=["-I", os.path.join(AQUI, "mcp_ferramentas.py"), "--transporte", "stdio"],
                                     env=dict(os.environ))
        transporte = "stdio"
    else:
        alvo, transporte = args.url, "streamable-http"
    resultado = {"transporte": transporte, "aprovacao": args.aprovacao, **asyncio.run(demonstrar(alvo, aprovador))}
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao(f"p03-mcp-{transporte}", resultado))
    return 0


if __name__ == "__main__":
    sys.exit(main())
