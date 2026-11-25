"""API de LLM pronta para operação (projeto 05): FastAPI + asyncio + SSE com cancelamento.

Endpoints:
- `POST /v1/respostas`: resposta completa, com retry/backoff, disjuntor e span OpenTelemetry.
- `POST /v1/respostas/stream`: SSE (`event: delta` ... `event: fim`); se o cliente desconecta,
  a geração no provedor é interrompida (fecha o stream upstream) e o cancelamento é contado.
  Retry só antes do primeiro token: repetir no meio duplicaria texto já enviado.
- `GET /v1/metricas`: contadores em JSON, estado do disjuntor e avaliação contínua.
- `GET /metrics`: métricas no formato Prometheus (OpenMetrics/text).
- `GET /saude`.

Execução real:
    LLM_BASE_URL=http://127.0.0.1:8081/v1 LLM_MODELO=modelo-local OTEL_EXPORTADOR=console \
    .venv-mercado/bin/uvicorn --app-dir laboratorios-mercado/05_api_llmops --factory llmops_api:criar_app_de_ambiente
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import sys
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Awaitable, Callable, Dict, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base.seguranca_http import carregar_seguranca_de_ambiente, instalar_seguranca_http  # noqa: E402

import httpx  # noqa: E402
from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse, PlainTextResponse, StreamingResponse  # noqa: E402
from opentelemetry.trace import Status, StatusCode  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from llmops_resiliencia import (  # noqa: E402
    CircuitoAberto, Disjuntor, ErroPermanente, ErroTransitorio, classificar_status, com_retry,
)
from llmops_telemetria import AvaliadorContinuo, configurar_telemetria, hash_curto  # noqa: E402


class PedidoResposta(BaseModel):
    prompt: str = Field(min_length=1, max_length=8000)
    max_tokens: int = Field(default=256, ge=1, le=2048)
    id_requisicao: Optional[str] = Field(default=None, max_length=64, pattern=r"^[A-Za-z0-9_.:-]+$")


class ProvedorOpenAICompativel:
    """Provedor assíncrono para `/v1/chat/completions` (llama-server, vLLM, Ollama, OpenAI)."""

    def __init__(self, base_url: str, modelo: str, api_key: str = "", timeout_s: float = 120.0,
                 transport: Optional[httpx.AsyncBaseTransport] = None):
        self.base_url = base_url.rstrip("/")
        self.modelo = modelo
        self.nome = "openai-compativel"
        cab = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self._cliente = httpx.AsyncClient(timeout=timeout_s, headers=cab, transport=transport)

    def _payload(self, prompt: str, max_tokens: int, stream: bool) -> Dict[str, object]:
        p: Dict[str, object] = {"model": self.modelo, "messages": [{"role": "user", "content": prompt}],
                                "max_tokens": max_tokens, "temperature": 0.0, "stream": stream}
        if stream:
            p["stream_options"] = {"include_usage": True}
        return p

    async def completar(self, prompt: str, max_tokens: int) -> Dict[str, object]:
        try:
            r = await self._cliente.post(f"{self.base_url}/chat/completions", json=self._payload(prompt, max_tokens, False))
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            raise ErroTransitorio(type(exc).__name__) from exc
        if r.status_code != 200:
            raise classificar_status(r.status_code, r.headers.get("retry-after"))
        d = r.json()
        uso = d.get("usage") or {}
        detalhes = uso.get("prompt_tokens_details") or {}
        timings = d.get("timings") or {}
        tokens_cache = int(detalhes.get("cached_tokens") or timings.get("cache_n") or 0)
        return {"texto": ((d.get("choices") or [{}])[0].get("message") or {}).get("content") or "",
                "tokens_entrada": int(uso.get("prompt_tokens") or 0),
                "tokens_saida": int(uso.get("completion_tokens") or 0),
                "tokens_cache": tokens_cache}

    async def gerar(self, prompt: str, max_tokens: int) -> AsyncIterator[str]:
        try:
            async with self._cliente.stream("POST", f"{self.base_url}/chat/completions",
                                            json=self._payload(prompt, max_tokens, True)) as r:
                if r.status_code != 200:
                    await r.aread()
                    raise classificar_status(r.status_code, r.headers.get("retry-after"))
                async for linha in r.aiter_lines():
                    for ev in mb.iterar_eventos_sse([linha]):
                        delta = mb.extrair_delta(ev)["conteudo"]
                        if delta:
                            yield delta
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            raise ErroTransitorio(type(exc).__name__) from exc

    async def fechar(self) -> None:
        await self._cliente.aclose()


def _sse(evento: str, dados: Dict[str, object]) -> str:
    return f"event: {evento}\ndata: {json.dumps(dados, ensure_ascii=False)}\n\n"


async def gerar_eventos(provedor, pedido: PedidoResposta, id_req: str, *, desconectado: Callable[[], Awaitable[bool]],
                        disjuntor: Disjuntor, contadores: Dict[str, int], avaliador: AvaliadorContinuo, tracer,
                        tentativas: int = 3, dormir=asyncio.sleep, rng: Optional[random.Random] = None) -> AsyncIterator[str]:
    """Gerador SSE com retry antes do 1º token, cancelamento por desconexão e span por requisição."""
    with tracer.start_as_current_span("chat " + str(getattr(provedor, "modelo", "?"))) as span:
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.request.model", str(getattr(provedor, "modelo", "?")))
        span.set_attribute("gen_ai.request.max_tokens", pedido.max_tokens)
        span.set_attribute("aurora.id_requisicao", id_req)
        span.set_attribute("aurora.prompt_sha", hash_curto(pedido.prompt))
        partes, primeiro, t0 = [], None, time.perf_counter()
        fluxo = None
        try:
            disjuntor.permitir()

            async def abrir():
                nonlocal fluxo
                fluxo = provedor.gerar(pedido.prompt, pedido.max_tokens).__aiter__()
                try:
                    return await fluxo.__anext__()
                except StopAsyncIteration:
                    return ""

            primeiro = await com_retry(abrir, tentativas=tentativas, dormir=dormir, rng=rng,
                                       ao_tentar=lambda n, e: contadores.__setitem__("retries", contadores["retries"] + 1))
            span.set_attribute("aurora.ttft_ms", round((time.perf_counter() - t0) * 1000, 3))
            if primeiro:
                partes.append(primeiro)
                yield _sse("delta", {"texto": primeiro})
            async for pedaco in fluxo:
                if await desconectado():
                    contadores["cancelados"] += 1
                    span.set_attribute("aurora.cancelado", True)
                    return
                partes.append(pedaco)
                yield _sse("delta", {"texto": pedaco})
            disjuntor.registrar_sucesso()
            texto = "".join(partes)
            aval = avaliador.avaliar(id_req, texto)
            span.set_attribute("aurora.caracteres_saida", len(texto))
            contadores["sucessos"] += 1
            contadores["latencia_ms_soma"] = round(contadores.get("latencia_ms_soma", 0.0) + (time.perf_counter() - t0) * 1000, 3)
            contadores["latencia_ms_contagem"] = contadores.get("latencia_ms_contagem", 0) + 1
            yield _sse("fim", {"id_requisicao": id_req, "caracteres": len(texto), "avaliacao": aval})
        except CircuitoAberto as exc:
            contadores["rejeitados_disjuntor"] += 1
            span.set_status(Status(StatusCode.ERROR, "disjuntor aberto"))
            yield _sse("erro", {"tipo": "disjuntor_aberto", "retry_after_s": round(exc.retry_after_s, 1)})
        except (ErroTransitorio, ErroPermanente) as exc:
            disjuntor.registrar_falha()
            contadores["falhas"] += 1
            span.set_status(Status(StatusCode.ERROR, str(exc)))
            yield _sse("erro", {"tipo": type(exc).__name__, "mensagem": str(exc)})
        except (asyncio.CancelledError, GeneratorExit):
            contadores["cancelados"] += 1
            span.set_attribute("aurora.cancelado", True)
            raise
        finally:
            if fluxo is not None and hasattr(fluxo, "aclose"):
                await fluxo.aclose()  # interrompe a geração no provedor


def _formatar_prometheus(contadores: Dict[str, float], disjuntor: Disjuntor, avaliador: AvaliadorContinuo) -> str:
    resumo = avaliador.resumo()
    estado_atual = disjuntor.estado
    linhas = [
        "# HELP aurora_requisicoes_total Total de requisicoes por resultado.",
        "# TYPE aurora_requisicoes_total counter",
    ]
    for rotulo, chave in (
        ("sucesso", "sucessos"),
        ("falha", "falhas"),
        ("cancelado", "cancelados"),
        ("rejeitado_disjuntor", "rejeitados_disjuntor"),
        ("rejeitado_auth", "rejeitados_auth"),
        ("rejeitado_rate_limit", "rejeitados_rate_limit"),
    ):
        linhas.append(f'aurora_requisicoes_total{{resultado="{rotulo}"}} {int(contadores.get(chave, 0))}')
    linhas.extend([
        "# HELP aurora_retries_total Total de novas tentativas ao provedor.",
        "# TYPE aurora_retries_total counter",
        f"aurora_retries_total {int(contadores.get('retries', 0))}",
        "# HELP aurora_disjuntor_estado Estado atual do disjuntor (1 = ativo).",
        "# TYPE aurora_disjuntor_estado gauge",
    ])
    for estado in ("fechado", "meio_aberto", "aberto"):
        linhas.append(f'aurora_disjuntor_estado{{estado="{estado}"}} {1 if estado_atual == estado else 0}')
    linhas.extend([
        "# HELP aurora_avaliacao_continua_avaliadas_total Respostas avaliadas continuamente.",
        "# TYPE aurora_avaliacao_continua_avaliadas_total counter",
        f"aurora_avaliacao_continua_avaliadas_total {int(resumo['avaliadas'])}",
        "# HELP aurora_avaliacao_continua_aprovadas_total Respostas aprovadas na avaliacao continua.",
        "# TYPE aurora_avaliacao_continua_aprovadas_total counter",
        f"aurora_avaliacao_continua_aprovadas_total {int(resumo['aprovadas'])}",
        "# HELP aurora_avaliacao_continua_falhas_total Falhas na avaliacao continua por motivo.",
        "# TYPE aurora_avaliacao_continua_falhas_total counter",
    ])
    for motivo in ("vazia", "pii", "longa_demais"):
        linhas.append(f'aurora_avaliacao_continua_falhas_total{{motivo="{motivo}"}} {int(resumo["falhas"].get(motivo, 0))}')
    linhas.extend([
        "# HELP aurora_avaliacao_continua_alerta Alerta ativo na avaliacao continua (1 = alerta).",
        "# TYPE aurora_avaliacao_continua_alerta gauge",
        f"aurora_avaliacao_continua_alerta {1 if resumo['alerta'] else 0}",
        "# HELP aurora_tokens_total Total de tokens processados por direcao.",
        "# TYPE aurora_tokens_total counter",
        f'aurora_tokens_total{{direcao="entrada"}} {int(contadores.get("tokens_entrada", 0))}',
        f'aurora_tokens_total{{direcao="saida"}} {int(contadores.get("tokens_saida", 0))}',
        f'aurora_tokens_total{{direcao="cache"}} {int(contadores.get("tokens_cache", 0))}',
        "# HELP aurora_latencia_ms_sum Soma das latencias das requisicoes concluidas em ms.",
        "# TYPE aurora_latencia_ms_sum counter",
        f"aurora_latencia_ms_sum {float(contadores.get('latencia_ms_soma', 0.0)):.3f}",
        "# HELP aurora_latencia_ms_count Quantidade de requisicoes medidas em latencia.",
        "# TYPE aurora_latencia_ms_count counter",
        f"aurora_latencia_ms_count {int(contadores.get('latencia_ms_contagem', 0))}",
    ])
    return "\n".join(linhas) + "\n"


def criar_app(provedor, *, tracer_provider=None, disjuntor: Optional[Disjuntor] = None,
              avaliador: Optional[AvaliadorContinuo] = None, tentativas: int = 3, dormir=asyncio.sleep,
              rng: Optional[random.Random] = None, api_keys: Optional[Sequence[str]] = None,
              limite_taxa: int = 0, janela_taxa_s: float = 60.0,
              relogio: Callable[[], float] = time.monotonic) -> FastAPI:
    if tracer_provider is None:
        tracer_provider, _ = configurar_telemetria("nenhum")
    tracer = tracer_provider.get_tracer("aurora.api_llmops")
    disjuntor = disjuntor or Disjuntor()
    avaliador = avaliador or AvaliadorContinuo()
    contadores: Dict[str, float] = {
        "sucessos": 0, "falhas": 0, "retries": 0, "cancelados": 0, "rejeitados_disjuntor": 0,
        "rejeitados_auth": 0, "rejeitados_rate_limit": 0,
        "tokens_entrada": 0, "tokens_saida": 0, "tokens_cache": 0,
        "latencia_ms_soma": 0.0, "latencia_ms_contagem": 0,
    }
    @asynccontextmanager
    async def ciclo_de_vida(_app):
        yield
        if hasattr(provedor, "fechar"):
            await provedor.fechar()
        tracer_provider.shutdown()

    app = FastAPI(title="Aurora API LLMOps (laboratório)", lifespan=ciclo_de_vida)
    app.state.contadores = contadores
    app.state.disjuntor = disjuntor
    app.state.avaliador = avaliador
    instalar_seguranca_http(
        app,
        api_keys=api_keys,
        limite_taxa=limite_taxa,
        janela_taxa_s=janela_taxa_s,
        rotas_publicas=("/saude",),
        relogio=relogio,
        contadores=contadores,
    )

    @app.get("/saude")
    async def saude():
        return {"status": "ok", "disjuntor": disjuntor.estado}

    @app.post("/v1/respostas")
    async def respostas(pedido: PedidoResposta):
        id_req = pedido.id_requisicao or uuid.uuid4().hex
        t0 = time.perf_counter()
        with tracer.start_as_current_span("chat " + str(getattr(provedor, "modelo", "?"))) as span:
            span.set_attribute("gen_ai.operation.name", "chat")
            span.set_attribute("gen_ai.request.model", str(getattr(provedor, "modelo", "?")))
            span.set_attribute("aurora.id_requisicao", id_req)
            try:
                disjuntor.permitir()
            except CircuitoAberto as exc:
                contadores["rejeitados_disjuntor"] += 1
                span.set_status(Status(StatusCode.ERROR, "disjuntor aberto"))
                return JSONResponse({"erro": "disjuntor_aberto"}, status_code=503,
                                    headers={"Retry-After": str(max(1, round(exc.retry_after_s)))})
            n = {"tentativas": 0}

            async def chamar():
                n["tentativas"] += 1
                return await provedor.completar(pedido.prompt, pedido.max_tokens)

            try:
                r = await com_retry(chamar, tentativas=tentativas, dormir=dormir, rng=rng,
                                    ao_tentar=lambda i, e: contadores.__setitem__("retries", contadores["retries"] + 1))
            except (ErroTransitorio, ErroPermanente) as exc:
                disjuntor.registrar_falha()
                contadores["falhas"] += 1
                span.set_status(Status(StatusCode.ERROR, str(exc)))
                falha_upstream = isinstance(exc, ErroTransitorio) or getattr(exc, "status_code", None) in (401, 403, 404)
                codigo = 502 if falha_upstream else 400
                return JSONResponse({"erro": type(exc).__name__, "mensagem": str(exc)}, status_code=codigo)
            disjuntor.registrar_sucesso()
            contadores["sucessos"] += 1
            tokens_cache = int(r.get("tokens_cache") or 0)
            contadores["tokens_entrada"] += int(r["tokens_entrada"])
            contadores["tokens_saida"] += int(r["tokens_saida"])
            contadores["tokens_cache"] += tokens_cache
            contadores["latencia_ms_soma"] = round(contadores["latencia_ms_soma"] + (time.perf_counter() - t0) * 1000, 3)
            contadores["latencia_ms_contagem"] += 1
            span.set_attribute("gen_ai.usage.input_tokens", r["tokens_entrada"])
            span.set_attribute("gen_ai.usage.output_tokens", r["tokens_saida"])
            if tokens_cache:
                span.set_attribute("gen_ai.usage.cache_read.input_tokens", tokens_cache)
            span.set_attribute("aurora.tentativas", n["tentativas"])
            return {"id_requisicao": id_req, "texto": r["texto"], "tentativas": n["tentativas"],
                    "tokens_saida": r["tokens_saida"], "tokens_cache": tokens_cache,
                    "avaliacao": avaliador.avaliar(id_req, r["texto"])}

    @app.post("/v1/respostas/stream")
    async def respostas_stream(pedido: PedidoResposta, request: Request):
        id_req = pedido.id_requisicao or uuid.uuid4().hex
        return StreamingResponse(
            gerar_eventos(provedor, pedido, id_req, desconectado=request.is_disconnected, disjuntor=disjuntor,
                          contadores=contadores, avaliador=avaliador, tracer=tracer, tentativas=tentativas,
                          dormir=dormir, rng=rng),
            media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    @app.get("/v1/metricas")
    async def metricas():
        return {"contadores": dict(contadores), "disjuntor": disjuntor.estado, "avaliacao_continua": avaliador.resumo()}

    @app.get("/metrics")
    async def metrics_prometheus():
        return PlainTextResponse(
            _formatar_prometheus(contadores, disjuntor, avaliador),
            media_type="text/plain; version=0.0.4; charset=utf-8",
        )

    return app


def criar_app_de_ambiente() -> FastAPI:
    provedor = ProvedorOpenAICompativel(os.environ.get("LLM_BASE_URL", "http://127.0.0.1:8081/v1"),
                                        os.environ.get("LLM_MODELO", "modelo-local"),
                                        api_key=os.environ.get("LLM_API_KEY", ""))
    tp, _ = configurar_telemetria(os.environ.get("OTEL_EXPORTADOR", "console"))
    seg = carregar_seguranca_de_ambiente("LLMOPS_")
    return criar_app(provedor, tracer_provider=tp, api_keys=seg["api_keys"], limite_taxa=seg["limite_taxa"])
