"""API de LLM pronta para operação (projeto 05): FastAPI + asyncio + SSE com cancelamento.

Endpoints:
- `POST /v1/respostas`: resposta completa, com retry/backoff, disjuntor e span OpenTelemetry.
- `POST /v1/respostas/stream`: SSE (`event: delta` ... `event: fim`); se o cliente desconecta,
  a geração no provedor é interrompida (fecha o stream upstream) e o cancelamento é contado.
  Retry só antes do primeiro token: repetir no meio duplicaria texto já enviado.
- `GET /v1/metricas`: contadores, estado do disjuntor e avaliação contínua.
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
from typing import AsyncIterator, Awaitable, Callable, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

import httpx  # noqa: E402
from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse, StreamingResponse  # noqa: E402
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
        return {"texto": ((d.get("choices") or [{}])[0].get("message") or {}).get("content") or "",
                "tokens_entrada": int(uso.get("prompt_tokens") or 0), "tokens_saida": int(uso.get("completion_tokens") or 0)}

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


def criar_app(provedor, *, tracer_provider=None, disjuntor: Optional[Disjuntor] = None,
              avaliador: Optional[AvaliadorContinuo] = None, tentativas: int = 3, dormir=asyncio.sleep,
              rng: Optional[random.Random] = None) -> FastAPI:
    if tracer_provider is None:
        tracer_provider, _ = configurar_telemetria("nenhum")
    tracer = tracer_provider.get_tracer("aurora.api_llmops")
    disjuntor = disjuntor or Disjuntor()
    avaliador = avaliador or AvaliadorContinuo()
    contadores = {"sucessos": 0, "falhas": 0, "retries": 0, "cancelados": 0, "rejeitados_disjuntor": 0}
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

    @app.get("/saude")
    async def saude():
        return {"status": "ok", "disjuntor": disjuntor.estado}

    @app.post("/v1/respostas")
    async def respostas(pedido: PedidoResposta):
        id_req = pedido.id_requisicao or uuid.uuid4().hex
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
                codigo = 502 if isinstance(exc, ErroTransitorio) else 400
                return JSONResponse({"erro": type(exc).__name__, "mensagem": str(exc)}, status_code=codigo)
            disjuntor.registrar_sucesso()
            contadores["sucessos"] += 1
            span.set_attribute("gen_ai.usage.input_tokens", r["tokens_entrada"])
            span.set_attribute("gen_ai.usage.output_tokens", r["tokens_saida"])
            span.set_attribute("aurora.tentativas", n["tentativas"])
            return {"id_requisicao": id_req, "texto": r["texto"], "tentativas": n["tentativas"],
                    "tokens_saida": r["tokens_saida"], "avaliacao": avaliador.avaliar(id_req, r["texto"])}

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

    return app


def criar_app_de_ambiente() -> FastAPI:
    provedor = ProvedorOpenAICompativel(os.environ.get("LLM_BASE_URL", "http://127.0.0.1:8081/v1"),
                                        os.environ.get("LLM_MODELO", "modelo-local"),
                                        api_key=os.environ.get("LLM_API_KEY", ""))
    tp, _ = configurar_telemetria(os.environ.get("OTEL_EXPORTADOR", "console"))
    return criar_app(provedor, tracer_provider=tp)
