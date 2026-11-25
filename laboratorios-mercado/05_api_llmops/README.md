# 05 — API LLMOps (FastAPI, SSE, resiliência e OpenTelemetry)

- `llmops_api.py`: `POST /v1/respostas`, `POST /v1/respostas/stream` (SSE), `GET /v1/metricas` (JSON), `GET /metrics` (Prometheus) e `GET /saude`. Entrada validada por Pydantic; autenticação opcional (`X-API-Key`/`Bearer`) e *rate limiting* (`429 + Retry-After`) via `mercado_base.seguranca_http`. Erros permanentes upstream `401/403/404` são mapeados para HTTP `502`. No streaming, o retry vale só **antes do primeiro token** (depois disso duplicaria texto); se o cliente desconecta, o stream do provedor é fechado e o cancelamento é contado.
- `llmops_resiliencia.py`: erros transitórios (408, 429, 5xx, timeout) e permanentes (guardando `status_code`); backoff exponencial com *full jitter* respeitando `Retry-After`; disjuntor fechado → aberto → meio-aberto com uma sonda.
- `llmops_telemetria.py`: `TracerProvider` próprio com spans `gen_ai.*` (convenções GenAI do OpenTelemetry, em estágio *development*), sem gravar prompt nem resposta (só hash e tamanhos); exportador `console`, `otlp` (Jaeger, Phoenix ou Langfuse via OTLP/HTTP) ou `memoria`. `AvaliadorContinuo`: amostragem determinística por id, checagens de resposta vazia, PII (CPF com dígitos verificadores, e-mail e telefone via `mercado_base.pii`) e tamanho, e alerta por taxa de aprovação.
- `cliente_api_real.py`: exercita auth (`401`/`200`), resposta completa, stream, cancelamento, `/v1/metricas`, `/metrics` e consulta traces OTLP na API v3 do Jaeger.

## Execução real

```bash
LLM_BASE_URL=http://127.0.0.1:8081/v1 LLM_MODELO=modelo-local OTEL_EXPORTADOR=console \
.venv-mercado/bin/python -I -m uvicorn --app-dir laboratorios-mercado/05_api_llmops \
  --factory llmops_api:criar_app_de_ambiente --port 8000 &
.venv-mercado/bin/python -I laboratorios-mercado/05_api_llmops/cliente_api_real.py --registrar
```

Ou em container: `podman compose -f laboratorios-mercado/compose.yaml --profile app up -d api-llmops`. Para ver os traces no Jaeger: perfil `observabilidade`, `OTEL_EXPORTADOR=otlp` e `OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318`.

Em 24–25/11/2026 (Fase 6, com Jaeger `v2.23.0` + `AURORA_API_KEYS` + `OTEL_EXPORTADOR=otlp`): `401` sem chave, `200` com `X-API-Key`, SSE com TTFT de `199 ms`, cancelamento detectado (`cancelados: 1`), `GET /metrics` Prometheus `200` e `6` spans recebidos em `GET /api/v3/traces` do Jaeger.
