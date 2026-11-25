"""Assistente acadêmico ponta a ponta (projeto 06) — Aurora Educação, proposta didática.

Fluxo por pergunta: guardrails de entrada (injeção e dados pessoais) → roteamento local/fronteira
→ ferramenta MCP (servidor do projeto 03, em processo, só ferramentas de leitura) → RAG híbrido
(projeto 02; pgvector em produção) → LLM → guardrails de saída (citação obrigatória, PII) →
registro de custo e latência por etapa (`GET /v1/relatorio`).

Regras de roteamento (didáticas, ajuste ao seu contexto):
1. Dado pessoal detectado → local (o texto mascarado também não sai da infraestrutura).
2. Pergunta complexa e orçamento disponível → fronteira; sem cliente de fronteira → local (fallback).
3. Demais casos → local.

Execução real (ver README):
    PGVECTOR_DSN=... EMBED_BASE_URL=... LLM_LOCAL_BASE_URL=... INTEGRADOR_INGERIR=1 \
    .venv-mercado/bin/uvicorn --app-dir laboratorios-mercado/06_integrador_producao --factory integrador_app:criar_app_de_ambiente
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import tempfile
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Deque, Dict, List, Literal, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base.cliente_openai import (  # noqa: E402
    ClienteChatOpenAI,
    gerar_estruturado,
)
from mercado_base.pii import RE_CPF, RE_EMAIL, RE_TELEFONE, mascarar_pii  # noqa: E402,F401
from mercado_base.seguranca_http import (  # noqa: E402
    ORDEM_PERFIS,
    carregar_seguranca_de_ambiente,
    instalar_seguranca_http,
)

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402
from mcp import Client  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

import corpus_aurora  # noqa: E402
import mcp_cliente_aurora  # noqa: E402
import mcp_ferramentas  # noqa: E402
import rag_ingestao as ing  # noqa: E402
import rag_pipeline as rp  # noqa: E402
import rag_store as rs  # noqa: E402

PADROES_INJECAO = [
    r"ignore\s+(?:as\s+|todas\s+as\s+)?(?:instru[cç][oõ]es|regras)\s+anteriores",
    r"ignore\s+(?:all\s+)?previous\s+instructions",
    r"revele\s+(?:o\s+|seu\s+)?(?:prompt|instru[cç][oõ]es)\s+(?:do\s+)?sistema",
    r"system\s+prompt",
    r"modo\s+desenvolvedor",
]
GATILHOS_COMPLEXIDADE = re.compile(r"\b(compare|comparar|analise|analisar|plano|estrat[eé]gia|detalhadamente|passo a passo)\b", re.I)

SISTEMA_AGENTE = (
    "Você é o assistente acadêmico da Aurora Educação (instituição fictícia, proposta didática). "
    "Responda em português, usando apenas os trechos [T1]..[Tn] recuperados e os resultados reais "
    "das ferramentas MCP disponíveis. Use `consultar_prazo` para prazos oficiais, "
    "`calcular_media_ponderada` para cálculos de média e aprovação, e `executar_python_isolado` "
    "apenas quando o usuário pedir execução de código Python. Nunca invente dados nem citações. "
    "Se a informação não existir nos trechos nem nas ferramentas, marque recusa=true."
)


class RespostaEstruturada(BaseModel):
    resposta: str = Field(min_length=1)
    citacoes: List[str] = Field(default_factory=list)
    recusa: bool = False
    confianca: Literal["alta", "media", "baixa"] = "media"


def mcp_tools_para_openai(ferramentas_mcp: Sequence[object]) -> List[Dict[str, object]]:
    """Converte ferramentas listadas pelo servidor MCP para o formato OpenAI `tools`."""
    saida: List[Dict[str, object]] = []
    for f in ferramentas_mcp:
        schema = getattr(f, "input_schema", None) or getattr(f, "inputSchema", None) or {
            "type": "object",
            "properties": {},
        }
        saida.append({
            "type": "function",
            "function": {
                "name": str(f.name),
                "description": str(getattr(f, "description", "") or f.name),
                "parameters": dict(schema),
            },
        })
    return saida


def verificar_entrada(texto: str) -> Dict[str, object]:
    baixo = texto.lower()
    for padrao in PADROES_INJECAO:
        if re.search(padrao, baixo):
            return {"bloqueado": True, "motivo": "possivel_injecao_de_prompt", "texto": "", "pii": []}
    mascarado, pii = mascarar_pii(texto)
    return {"bloqueado": False, "motivo": "", "texto": mascarado, "pii": pii}


def verificar_saida(resposta: str, trechos, limiar_fidelidade: float = 0.5) -> Dict[str, object]:
    """Exige citação válida; mascara PII que escape (CPF, e-mail e telefone). Sem citação → recusa segura.

    Fidelidade lexical abaixo do limiar não bloqueia (a métrica não reconhece paráfrase), mas marca
    a resposta para revisão humana amostral (`aprovado_com_alerta`).
    """
    limpa, _ = mascarar_pii(resposta)
    fid = rp.fidelidade(limpa, trechos)
    citou = bool(re.search(r"\[T\d+\]", limpa))
    if fid["recusa"]:
        return {"texto": limpa, "acao": "recusa_do_modelo", "fidelidade": fid}
    if fid["citacoes_invalidas"] or not citou:
        return {"texto": rp.RESPOSTA_RECUSA, "acao": "bloqueado_sem_citacao_valida", "fidelidade": fid}
    acao = "aprovado" if fid["fidelidade"] >= limiar_fidelidade else "aprovado_com_alerta"
    return {"texto": limpa, "acao": acao, "fidelidade": fid}


@dataclass
class Precos:
    """USD por 1 milhão de tokens. Valores de fronteira são ILUSTRATIVOS: configure com a tabela vigente."""

    local_entrada: float = 0.0
    local_saida: float = 0.0
    fronteira_entrada: float = 1.0
    fronteira_saida: float = 4.0

    def custo(self, rota: str, entrada: int, saida: int) -> float:
        e, s = (self.local_entrada, self.local_saida) if rota == "local" else (self.fronteira_entrada, self.fronteira_saida)
        return round((entrada * e + saida * s) / 1_000_000, 8)


@dataclass
class Roteador:
    orcamento_usd: float = 1.0
    gasto_usd: float = 0.0
    limite_palavras: int = 40

    def decidir(self, texto: str, pii: List[str], fronteira_disponivel: bool) -> Dict[str, str]:
        if pii:
            return {"rota": "local", "motivo": "dados pessoais detectados"}
        complexa = len(texto.split()) > self.limite_palavras or bool(GATILHOS_COMPLEXIDADE.search(texto))
        if not complexa:
            return {"rota": "local", "motivo": "pergunta simples"}
        if self.gasto_usd >= self.orcamento_usd:
            return {"rota": "local", "motivo": "orçamento de fronteira esgotado"}
        if not fronteira_disponivel:
            return {"rota": "local", "motivo": "fallback: fronteira indisponível"}
        return {"rota": "fronteira", "motivo": "pergunta complexa"}


@dataclass
class Assistente:
    armazem: object
    embedder: object
    cliente_local: object
    cliente_fronteira: Optional[object] = None
    reordenador: Optional[object] = None
    k: int = 3
    precos: Precos = field(default_factory=Precos)
    roteador: Roteador = field(default_factory=Roteador)
    servidor_mcp: object = field(default_factory=mcp_ferramentas.criar_servidor)
    aprovador_mcp: Optional[Callable] = None
    max_passos_agente: int = 4
    max_registros: int = 1000
    registros: Deque[Dict[str, object]] = field(init=False)
    _totais: Dict[str, object] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.registros = deque(maxlen=max(1, int(self.max_registros)))
        self._totais = {
            "requisicoes": 0,
            "por_rota": {},
            "bloqueios_entrada": 0,
            "bloqueios_saida": 0,
            "alertas_fidelidade": 0,
            "fallbacks": 0,
            "com_pii_mascarada": 0,
            "com_ferramenta_mcp": 0,
            "chamadas_ferramentas_mcp": 0,
            "reparos_estruturado": 0,
            "falhas_esquema": 0,
            "tokens_entrada": 0,
            "tokens_saida": 0,
            "tokens_cache": 0,
            "custo_usd_total": 0.0,
        }

    def _registrar(self, reg: Dict[str, object]) -> None:
        self.registros.append(reg)
        self._totais["requisicoes"] += 1
        chave = reg["rota"] or "bloqueado"
        por_rota = self._totais["por_rota"]
        por_rota[chave] = por_rota.get(chave, 0) + 1
        if reg["bloqueado"]:
            self._totais["bloqueios_entrada"] += 1
        if reg.get("acao_saida") == "bloqueado_sem_citacao_valida":
            self._totais["bloqueios_saida"] += 1
        if reg.get("acao_saida") == "aprovado_com_alerta":
            self._totais["alertas_fidelidade"] += 1
        if str(reg.get("motivo_rota", "")).startswith("fallback"):
            self._totais["fallbacks"] += 1
        if reg.get("pii_mascarada"):
            self._totais["com_pii_mascarada"] += 1
        if reg.get("ferramenta_mcp"):
            self._totais["com_ferramenta_mcp"] += 1
        self._totais["chamadas_ferramentas_mcp"] += len(reg.get("ferramentas_chamadas") or ())
        self._totais["reparos_estruturado"] += int(reg.get("reparos_estruturado") or 0)
        if reg.get("acao_saida") == "falha_esquema_estruturado":
            self._totais["falhas_esquema"] += 1
        self._totais["tokens_entrada"] += int(reg.get("tokens_entrada") or 0)
        self._totais["tokens_saida"] += int(reg.get("tokens_saida") or 0)
        self._totais["tokens_cache"] += int(reg.get("tokens_cache") or 0)
        self._totais["custo_usd_total"] += float(reg.get("custo_usd") or 0.0)

    async def _executar_agente_e_gerar(
        self, cliente, pergunta: str, trechos_rag: Sequence[ing.Trecho]
    ) -> Dict[str, object]:
        trechos_totais = list(trechos_rag)
        if not hasattr(cliente, "completar_chat"):
            rec_legado = rp.Recuperacao(pergunta, trechos_totais)
            gerado = await asyncio.to_thread(rp.responder, pergunta, rec_legado, cliente)
            return {
                **gerado,
                "tokens_cache": 0,
                "trechos": trechos_totais,
                "ferramentas_chamadas": [],
                "passos_agente": 0,
                "reparos_estruturado": 0,
                "confianca": "media",
            }

        callback = mcp_cliente_aurora.criar_callback(self.aprovador_mcp) if self.aprovador_mcp else None
        mensagens: List[Dict[str, object]] = [
            {"role": "system", "content": SISTEMA_AGENTE},
            {"role": "user", "content": rp.montar_prompt(pergunta, trechos_totais)},
        ]
        tokens_in = tokens_out = tokens_cache = 0
        ferramentas_chamadas: List[str] = []
        passos = 0

        async with Client(self.servidor_mcp, mode="legacy", elicitation_callback=callback) as mcp_cli:
            ferramentas_mcp = (await mcp_cli.list_tools()).tools
            tools_openai = mcp_tools_para_openai(ferramentas_mcp)
            nomes_validos = {f.name for f in ferramentas_mcp}

            for _ in range(max(1, int(self.max_passos_agente))):
                passos += 1
                resp = await asyncio.to_thread(
                    cliente.completar_chat,
                    mensagens,
                    tools=tools_openai,
                    tool_choice="auto",
                    max_tokens=512,
                )
                tokens_in += resp.tokens_entrada
                tokens_out += resp.tokens_saida
                tokens_cache += resp.tokens_cache
                if not resp.chamadas_ferramentas:
                    break

                mensagens.append({
                    "role": "assistant",
                    "content": resp.conteudo or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {"name": tc.nome, "arguments": tc.argumentos_brutos or json.dumps(tc.argumentos)},
                        }
                        for tc in resp.chamadas_ferramentas
                    ],
                })

                for tc in resp.chamadas_ferramentas:
                    if tc.nome not in nomes_validos:
                        mensagens.append({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps({"erro": f"ferramenta desconhecida: {tc.nome}"}, ensure_ascii=False),
                        })
                        continue
                    if tc.erro_json:
                        mensagens.append({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps({"erro": tc.erro_json}, ensure_ascii=False),
                        })
                        continue

                    res_mcp = await mcp_cli.call_tool(tc.nome, tc.argumentos)
                    ferramentas_chamadas.append(tc.nome)
                    texto_tool = ""
                    if res_mcp.content:
                        texto_tool = str(getattr(res_mcp.content[0], "text", "") or "")
                    if not texto_tool and getattr(res_mcp, "structured_content", None) is not None:
                        texto_tool = json.dumps(res_mcp.structured_content, ensure_ascii=False)
                    if not res_mcp.is_error and texto_tool:
                        trechos_totais.insert(
                            0,
                            ing.Trecho(
                                f"mcp:{tc.nome}:{len(ferramentas_chamadas)}",
                                f"ferramenta-mcp:{tc.nome}",
                                0,
                                "ferramenta",
                                f"Resultado oficial de {tc.nome}({json.dumps(tc.argumentos, ensure_ascii=False)}): {texto_tool}",
                            ),
                        )
                    mensagens.append({"role": "tool", "tool_call_id": tc.id, "content": texto_tool or "{}"})

        rotulos_contexto = rp.montar_prompt(pergunta, trechos_totais)
        mensagens_estruturado: List[Dict[str, object]] = [
            {"role": "system", "content": SISTEMA_AGENTE},
            {
                "role": "user",
                "content": (
                    rotulos_contexto
                    + "\n\nResponda de forma objetiva (até 180 palavras) e exclusivamente em JSON no esquema exigido "
                    "(`resposta`, `citacoes`, `recusa`, `confianca`). "
                    "Cite os rótulos exatamente como [T1], [T2] tanto no texto de `resposta` quanto em `citacoes` "
                    "(ex.: [\"[T1]\"])."
                ),
            },
        ]
        try:
            estruturado, meta_est = await asyncio.to_thread(
                gerar_estruturado, cliente, mensagens_estruturado, RespostaEstruturada, max_reparos=2, max_tokens=1024
            )
        except ValueError:
            return {
                "resposta": rp.RESPOSTA_RECUSA,
                "tokens_entrada": tokens_in,
                "tokens_saida": tokens_out,
                "tokens_cache": tokens_cache,
                "trechos": trechos_totais,
                "ferramentas_chamadas": ferramentas_chamadas,
                "passos_agente": passos,
                "reparos_estruturado": 2,
                "confianca": "baixa",
                "falha_esquema": True,
            }
        tokens_in += int(meta_est["tokens_entrada"])
        tokens_out += int(meta_est["tokens_saida"])
        tokens_cache += int(meta_est["tokens_cache"])

        if estruturado.recusa:
            texto_final = rp.RESPOSTA_RECUSA
        else:
            texto_final = estruturado.resposta.strip()
            validos_set = {f"[T{i}]" for i in range(1, len(trechos_totais) + 1)}
            normalizadas: List[str] = []
            for c in estruturado.citacoes:
                m_cit = re.fullmatch(r"\s*\[?\s*T?(\d+)\s*\]?\s*", str(c))
                if m_cit:
                    tag = f"[T{m_cit.group(1)}]"
                    if tag in validos_set and tag not in texto_final and tag not in normalizadas:
                        normalizadas.append(tag)
            if normalizadas:
                texto_final = f"{texto_final} {' '.join(normalizadas)}"

        return {
            "resposta": texto_final,
            "tokens_entrada": tokens_in,
            "tokens_saida": tokens_out,
            "tokens_cache": tokens_cache,
            "trechos": trechos_totais,
            "ferramentas_chamadas": ferramentas_chamadas,
            "passos_agente": passos,
            "reparos_estruturado": int(meta_est["reparos"]),
            "confianca": estruturado.confianca,
            "falha_esquema": False,
        }

    async def responder(
        self,
        pergunta: str,
        id_requisicao: Optional[str] = None,
        *,
        perfil: str = "aluno",
        apenas_vigentes: bool = True,
    ) -> Dict[str, object]:
        id_req = id_requisicao or uuid.uuid4().hex
        etapas: Dict[str, float] = {}
        t_total = t = time.perf_counter()

        def marcar(nome):
            nonlocal t
            agora = time.perf_counter()
            etapas[nome] = round((agora - t) * 1000, 3)
            t = agora

        ent = verificar_entrada(pergunta)
        marcar("guardrail_entrada")
        if ent["bloqueado"]:
            reg = {"id": id_req, "bloqueado": True, "motivo": ent["motivo"], "rota": None, "etapas_ms": etapas,
                   "total_ms": round((time.perf_counter() - t_total) * 1000, 3), "custo_usd": 0.0,
                   "tokens_entrada": 0, "tokens_saida": 0, "tokens_cache": 0}
            self._registrar(reg)
            return {**reg, "resposta": "Não posso atender a esse pedido."}
        decisao = self.roteador.decidir(ent["texto"], ent["pii"], self.cliente_fronteira is not None)
        marcar("roteamento")
        filtro = rs.FiltroBusca(perfil=perfil, apenas_vigentes=apenas_vigentes)
        rec = await asyncio.to_thread(
            rp.recuperar, ent["texto"], self.armazem, self.embedder,
            k=self.k, reordenador=self.reordenador, filtro=filtro,
        )
        marcar("rag")
        cliente = self.cliente_fronteira if decisao["rota"] == "fronteira" else self.cliente_local
        gerado = await self._executar_agente_e_gerar(cliente, ent["texto"], rec.trechos)
        trechos_finais = gerado["trechos"]
        marcar("agente_llm")
        saida = verificar_saida(gerado["resposta"], trechos_finais)
        acao_saida = "falha_esquema_estruturado" if gerado.get("falha_esquema") else saida["acao"]
        marcar("guardrail_saida")
        custo = self.precos.custo(decisao["rota"], gerado["tokens_entrada"], gerado["tokens_saida"])
        if decisao["rota"] == "fronteira":
            self.roteador.gasto_usd += custo
        reg = {
            "id": id_req, "bloqueado": False, "rota": decisao["rota"], "motivo_rota": decisao["motivo"],
            "pii_mascarada": ent["pii"],
            "ferramenta_mcp": bool(gerado["ferramentas_chamadas"]),
            "ferramentas_chamadas": gerado["ferramentas_chamadas"],
            "passos_agente": gerado["passos_agente"],
            "reparos_estruturado": gerado["reparos_estruturado"],
            "confianca": gerado["confianca"],
            "trechos": [x.id for x in trechos_finais], "acao_saida": acao_saida,
            "fidelidade": saida["fidelidade"]["fidelidade"], "tokens_entrada": gerado["tokens_entrada"],
            "tokens_saida": gerado["tokens_saida"], "tokens_cache": gerado["tokens_cache"],
            "custo_usd": custo, "etapas_ms": etapas,
            "total_ms": round((time.perf_counter() - t_total) * 1000, 3),
        }
        self._registrar(reg)
        return {**reg, "resposta": saida["texto"]}

    def relatorio(self) -> Dict[str, object]:
        regs = list(self.registros)
        total = [r["total_ms"] for r in regs]
        etapas = sorted({e for r in regs for e in r["etapas_ms"]})
        return {
            "requisicoes": self._totais["requisicoes"],
            "janela_registros": len(regs),
            "max_registros": self.max_registros,
            "por_rota": dict(self._totais["por_rota"]),
            "bloqueios_entrada": self._totais["bloqueios_entrada"],
            "bloqueios_saida": self._totais["bloqueios_saida"],
            "alertas_fidelidade": self._totais["alertas_fidelidade"],
            "fallbacks": self._totais["fallbacks"],
            "com_pii_mascarada": self._totais["com_pii_mascarada"],
            "com_ferramenta_mcp": self._totais["com_ferramenta_mcp"],
            "chamadas_ferramentas_mcp": self._totais["chamadas_ferramentas_mcp"],
            "reparos_estruturado": self._totais["reparos_estruturado"],
            "falhas_esquema": self._totais["falhas_esquema"],
            "latencia_ms": {"p50": round(mb.percentil(total, 50), 3) if total else None,
                            "p95": round(mb.percentil(total, 95), 3) if total else None},
            "latencia_p50_por_etapa_ms": {e: round(mb.percentil([r["etapas_ms"][e] for r in regs if e in r["etapas_ms"]], 50), 3)
                                          for e in etapas},
            "tokens": {
                "entrada": self._totais["tokens_entrada"],
                "saida": self._totais["tokens_saida"],
                "cache": self._totais["tokens_cache"],
            },
            "custo_usd_total": round(self._totais["custo_usd_total"], 8),
            "precos_usd_por_milhao": vars(self.precos),
        }


class Pergunta(BaseModel):
    pergunta: str = Field(min_length=1, max_length=4000)
    id_requisicao: Optional[str] = Field(default=None, max_length=64, pattern=r"^[A-Za-z0-9_.:-]+$")
    perfil: Literal["publico", "aluno", "docente", "coordenacao", "admin"] = "aluno"
    apenas_vigentes: bool = True


def criar_app(
    assistente: Assistente,
    *,
    api_keys: Optional[Sequence[str]] = None,
    perfis_por_chave: Optional[Dict[str, str]] = None,
    limite_taxa: int = 0,
    janela_taxa_s: float = 60.0,
    relogio: Callable[[], float] = time.monotonic,
) -> FastAPI:
    app = FastAPI(title="Aurora — assistente integrador (laboratório)")
    app.state.assistente = assistente
    instalar_seguranca_http(
        app,
        api_keys=api_keys,
        perfis_por_chave=perfis_por_chave,
        limite_taxa=limite_taxa,
        janela_taxa_s=janela_taxa_s,
        rotas_publicas=("/saude",),
        relogio=relogio,
    )

    @app.get("/saude")
    async def saude():
        return {"status": "ok"}

    @app.post("/v1/assistente")
    async def perguntar(p: Pergunta, request: Request):
        perfil_max = getattr(request.state, "perfil_maximo", None)
        if perfil_max is not None and ORDEM_PERFIS[p.perfil] > ORDEM_PERFIS[perfil_max]:
            return JSONResponse(
                {"erro": "perfil_nao_autorizado", "perfil_maximo": perfil_max},
                status_code=403,
            )
        return await assistente.responder(
            p.pergunta, p.id_requisicao, perfil=p.perfil, apenas_vigentes=p.apenas_vigentes
        )

    @app.get("/v1/relatorio")
    async def relatorio():
        return assistente.relatorio()

    return app


def ingerir_corpus(armazem, embedder, max_palavras: int = 40) -> int:
    trechos = []
    with tempfile.TemporaryDirectory() as pasta:
        for doc, caminho in corpus_aurora.gerar_pdfs(pasta).items():
            meta = corpus_aurora.metadados_doc(doc)
            trechos += ing.segmentar(
                ing.extrair_paginas_pdf(caminho),
                doc,
                max_palavras=max_palavras,
                sobreposicao=8,
                perfis=meta["perfis"],
                departamento=meta["departamento"],
                versao=meta["versao"],
                vigente=meta["vigente"],
            )
    vetores = embedder.embutir([x.texto for x in trechos])
    armazem.criar_esquema(len(vetores[0]), recriar=True)
    return armazem.inserir(trechos, vetores)


def criar_app_de_ambiente() -> FastAPI:
    from comum.cliente_llm import criar_cliente_por_ambiente

    embedder = rs.EmbedderOpenAICompativel(os.environ.get("EMBED_BASE_URL", "http://127.0.0.1:8082/v1"),
                                           os.environ.get("EMBED_MODELO", "embed-local"))
    armazem = rs.ArmazemPgvector(os.environ["PGVECTOR_DSN"])
    if os.environ.get("INTEGRADOR_INGERIR") == "1":
        ingerir_corpus(armazem, embedder)
    local = ClienteChatOpenAI(
        base_url=os.environ.get("LLM_LOCAL_BASE_URL", "http://127.0.0.1:8081/v1"),
        modelo=os.environ.get("LLM_LOCAL_MODELO", "modelo-local"),
        provedor="local",
        timeout_s=180.0,
    )
    fronteira = None
    provedor = os.environ.get("FRONTEIRA_PROVEDOR", "").strip()
    if provedor:  # openai, anthropic ou gemini; chaves só por variável de ambiente (Gemini via x-goog-api-key)
        fronteira = criar_cliente_por_ambiente(provedor, modelo=os.environ.get("FRONTEIRA_MODELO") or None)
    precos = Precos(**json.loads(os.environ["INTEGRADOR_PRECOS_JSON"])) if os.environ.get("INTEGRADOR_PRECOS_JSON") else Precos()
    seg = carregar_seguranca_de_ambiente("INTEGRADOR_")
    return criar_app(
        Assistente(armazem, embedder, local, fronteira, precos=precos),
        api_keys=seg["api_keys"],
        perfis_por_chave=seg["perfis_por_chave"],
        limite_taxa=seg["limite_taxa"],
    )
