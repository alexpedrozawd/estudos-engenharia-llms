# 05 — API LLMOps (FastAPI, SSE, resiliência e OpenTelemetry)

- `llmops_api.py`: `POST /v1/respostas`, `POST /v1/respostas/stream` (SSE), `GET /v1/metricas`, `GET /saude`. Entrada validada por Pydantic. No streaming, o retry vale só **antes do primeiro token** (depois disso duplicaria texto); se o cliente desconecta, o stream do provedor é fechado e o cancelamento é contado.
- `llmops_resiliencia.py`: erros transitórios (408, 429, 5xx, timeout) e permanentes; backoff exponencial com *full jitter* respeitando `Retry-After`; disjuntor fechado → aberto → meio-aberto com uma sonda.
- `llmops_telemetria.py`: `TracerProvider` próprio com spans `gen_ai.*` (convenções GenAI do OpenTelemetry, em estágio *development*), sem gravar prompt nem resposta (só hash e tamanhos); exportador `console`, `otlp` (Jaeger, Phoenix ou Langfuse via OTLP/HTTP) ou `memoria`. `AvaliadorContinuo`: amostragem determinística por id, checagens de resposta vazia, PII e tamanho, e alerta por taxa de aprovação.
- `cliente_api_real.py`: exercita resposta completa, stream, cancelamento e métricas.

## Execução real

```bash
LLM_BASE_URL=http://127.0.0.1:8081/v1 LLM_MODELO=modelo-local OTEL_EXPORTADOR=console \
.venv-mercado/bin/python -I -m uvicorn --app-dir laboratorios-mercado/05_api_llmops \
  --factory llmops_api:criar_app_de_ambiente --port 8000 &
.venv-mercado/bin/python -I laboratorios-mercado/05_api_llmops/cliente_api_real.py --registrar
```

Ou em container: `podman compose -f laboratorios-mercado/compose.yaml --profile app up -d api-llmops`. Para ver os traces no Jaeger: perfil `observabilidade`, `OTEL_EXPORTADOR=otlp` e `OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318`.

Em 24/11/2026: resposta completa, SSE com TTFT de 235 ms no cliente e cancelamento detectado pelo servidor (`cancelados: 1`, span com `aurora.cancelado`). O serviço em container respondeu pela rede do compose.
