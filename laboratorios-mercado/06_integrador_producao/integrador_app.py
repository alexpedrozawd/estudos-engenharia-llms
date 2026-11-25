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
from dataclasses import dataclass, field
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

from fastapi import FastAPI  # noqa: E402
from mcp import Client  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

import corpus_aurora  # noqa: E402
import mcp_ferramentas  # noqa: E402
import rag_ingestao as ing  # noqa: E402
import rag_pipeline as rp  # noqa: E402
import rag_store as rs  # noqa: E402

RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
RE_TELEFONE = re.compile(r"(?:\(?\b\d{2}\)?\s?)?\b9?\d{4}-?\d{4}\b")
PADROES_INJECAO = [
    r"ignore\s+(?:as\s+|todas\s+as\s+)?(?:instru[cç][oõ]es|regras)\s+anteriores",
    r"ignore\s+(?:all\s+)?previous\s+instructions",
    r"revele\s+(?:o\s+|seu\s+)?(?:prompt|instru[cç][oõ]es)\s+(?:do\s+)?sistema",
    r"system\s+prompt",
    r"modo\s+desenvolvedor",
]
GATILHOS_COMPLEXIDADE = re.compile(r"\b(compare|comparar|analise|analisar|plano|estrat[eé]gia|detalhadamente|passo a passo)\b", re.I)
PROCESSOS_MCP = {"rematr": "rematricula", "tranc": "trancamento", "revis": "revisao_de_prova"}


def verificar_entrada(texto: str) -> Dict[str, object]:
    baixo = texto.lower()
    for padrao in PADROES_INJECAO:
        if re.search(padrao, baixo):
            return {"bloqueado": True, "motivo": "possivel_injecao_de_prompt", "texto": "", "pii": []}
    pii = []
    mascarado = texto
    for nome, rx, rotulo in (("cpf", RE_CPF, "[CPF]"), ("email", RE_EMAIL, "[EMAIL]"), ("telefone", RE_TELEFONE, "[TELEFONE]")):
        if rx.search(mascarado):
            pii.append(nome)
            mascarado = rx.sub(rotulo, mascarado)
    return {"bloqueado": False, "motivo": "", "texto": mascarado, "pii": pii}


def verificar_saida(resposta: str, trechos, limiar_fidelidade: float = 0.5) -> Dict[str, object]:
    """Exige citação válida; mascara PII que escape. Sem citação → recusa segura.

    Fidelidade lexical abaixo do limiar não bloqueia (a métrica não reconhece paráfrase), mas marca
    a resposta para revisão humana amostral (`aprovado_com_alerta`).
    """
    limpa = RE_EMAIL.sub("[EMAIL]", RE_CPF.sub("[CPF]", resposta))
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
    registros: List[Dict[str, object]] = field(default_factory=list)

    async def _ferramenta(self, pergunta: str) -> Optional[ing.Trecho]:
        baixo = rs.normalizar(pergunta)
        if "prazo" not in baixo and "ate quando" not in baixo:
            return None
        processo = next((p for chave, p in PROCESSOS_MCP.items() if chave in baixo), None)
        if processo is None:
            return None
        async with Client(self.servidor_mcp, mode="legacy") as c:
            r = await c.call_tool("consultar_prazo", {"processo": processo})
        if r.is_error:
            return None
        return ing.Trecho("mcp:consultar_prazo", "ferramenta-mcp:consultar_prazo", 0, "ferramenta",
                          f"Prazo oficial de {processo}: {r.content[0].text}")

    async def responder(self, pergunta: str, id_requisicao: Optional[str] = None) -> Dict[str, object]:
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
                   "tokens_entrada": 0, "tokens_saida": 0}
            self.registros.append(reg)
            return {**reg, "resposta": "Não posso atender a esse pedido."}
        decisao = self.roteador.decidir(ent["texto"], ent["pii"], self.cliente_fronteira is not None)
        marcar("roteamento")
        ferramenta = await self._ferramenta(ent["texto"])
        marcar("ferramenta_mcp")
        rec = await asyncio.to_thread(rp.recuperar, ent["texto"], self.armazem, self.embedder,
                                      k=self.k, reordenador=self.reordenador)
        if ferramenta is not None:
            rec.trechos = [ferramenta] + rec.trechos
        marcar("rag")
        cliente = self.cliente_fronteira if decisao["rota"] == "fronteira" else self.cliente_local
        gerado = await asyncio.to_thread(rp.responder, ent["texto"], rec, cliente)
        marcar("llm")
        saida = verificar_saida(gerado["resposta"], rec.trechos)
        marcar("guardrail_saida")
        custo = self.precos.custo(decisao["rota"], gerado["tokens_entrada"], gerado["tokens_saida"])
        if decisao["rota"] == "fronteira":
            self.roteador.gasto_usd += custo
        reg = {
            "id": id_req, "bloqueado": False, "rota": decisao["rota"], "motivo_rota": decisao["motivo"],
            "pii_mascarada": ent["pii"], "ferramenta_mcp": ferramenta is not None,
            "trechos": [x.id for x in rec.trechos], "acao_saida": saida["acao"],
            "fidelidade": saida["fidelidade"]["fidelidade"], "tokens_entrada": gerado["tokens_entrada"],
            "tokens_saida": gerado["tokens_saida"], "custo_usd": custo, "etapas_ms": etapas,
            "total_ms": round((time.perf_counter() - t_total) * 1000, 3),
        }
        self.registros.append(reg)
        return {**reg, "resposta": saida["texto"]}

    def relatorio(self) -> Dict[str, object]:
        regs = self.registros
        total = [r["total_ms"] for r in regs]
        etapas = sorted({e for r in regs for e in r["etapas_ms"]})
        por_rota: Dict[str, int] = {}
        for r in regs:
            chave = r["rota"] or "bloqueado"
            por_rota[chave] = por_rota.get(chave, 0) + 1
        return {
            "requisicoes": len(regs),
            "por_rota": por_rota,
            "bloqueios_entrada": sum(1 for r in regs if r["bloqueado"]),
            "bloqueios_saida": sum(1 for r in regs if r.get("acao_saida") == "bloqueado_sem_citacao_valida"),
            "alertas_fidelidade": sum(1 for r in regs if r.get("acao_saida") == "aprovado_com_alerta"),
            "fallbacks": sum(1 for r in regs if str(r.get("motivo_rota", "")).startswith("fallback")),
            "com_pii_mascarada": sum(1 for r in regs if r.get("pii_mascarada")),
            "com_ferramenta_mcp": sum(1 for r in regs if r.get("ferramenta_mcp")),
            "latencia_ms": {"p50": round(mb.percentil(total, 50), 3) if total else None,
                            "p95": round(mb.percentil(total, 95), 3) if total else None},
            "latencia_p50_por_etapa_ms": {e: round(mb.percentil([r["etapas_ms"][e] for r in regs if e in r["etapas_ms"]], 50), 3)
                                          for e in etapas},
            "tokens": {"entrada": sum(r["tokens_entrada"] for r in regs), "saida": sum(r["tokens_saida"] for r in regs)},
            "custo_usd_total": round(sum(r["custo_usd"] for r in regs), 8),
            "precos_usd_por_milhao": vars(self.precos),
        }


class Pergunta(BaseModel):
    pergunta: str = Field(min_length=1, max_length=4000)
    id_requisicao: Optional[str] = Field(default=None, max_length=64, pattern=r"^[A-Za-z0-9_.:-]+$")


def criar_app(assistente: Assistente) -> FastAPI:
    app = FastAPI(title="Aurora — assistente integrador (laboratório)")
    app.state.assistente = assistente

    @app.get("/saude")
    async def saude():
        return {"status": "ok"}

    @app.post("/v1/assistente")
    async def perguntar(p: Pergunta):
        return await assistente.responder(p.pergunta, p.id_requisicao)

    @app.get("/v1/relatorio")
    async def relatorio():
        return assistente.relatorio()

    return app


def ingerir_corpus(armazem, embedder, max_palavras: int = 40) -> int:
    trechos = []
    with tempfile.TemporaryDirectory() as pasta:
        for doc, caminho in corpus_aurora.gerar_pdfs(pasta).items():
            trechos += ing.segmentar(ing.extrair_paginas_pdf(caminho), doc, max_palavras=max_palavras, sobreposicao=8)
    vetores = embedder.embutir([x.texto for x in trechos])
    armazem.criar_esquema(len(vetores[0]), recriar=True)
    return armazem.inserir(trechos, vetores)


def criar_app_de_ambiente() -> FastAPI:
    from comum.cliente_llm import ClienteHTTPOpenAICompativel, criar_cliente_por_ambiente

    embedder = rs.EmbedderOpenAICompativel(os.environ.get("EMBED_BASE_URL", "http://127.0.0.1:8082/v1"),
                                           os.environ.get("EMBED_MODELO", "embed-local"))
    armazem = rs.ArmazemPgvector(os.environ["PGVECTOR_DSN"])
    if os.environ.get("INTEGRADOR_INGERIR") == "1":
        ingerir_corpus(armazem, embedder)
    local = ClienteHTTPOpenAICompativel(modelo=os.environ.get("LLM_LOCAL_MODELO", "modelo-local"),
                                        base_url=os.environ.get("LLM_LOCAL_BASE_URL", "http://127.0.0.1:8081/v1"),
                                        provedor="local", timeout_s=180.0)
    fronteira = None
    provedor = os.environ.get("FRONTEIRA_PROVEDOR", "").strip()
    if provedor:  # openai, anthropic ou gemini; chaves só por variável de ambiente (Gemini via x-goog-api-key)
        fronteira = criar_cliente_por_ambiente(provedor, modelo=os.environ.get("FRONTEIRA_MODELO") or None)
    precos = Precos(**json.loads(os.environ["INTEGRADOR_PRECOS_JSON"])) if os.environ.get("INTEGRADOR_PRECOS_JSON") else Precos()
    return criar_app(Assistente(armazem, embedder, local, fronteira, precos=precos))
