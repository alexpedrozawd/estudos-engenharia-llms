# 01 — Serving local e benchmark

Mede o que importa para operar um modelo local: TTFT (tempo até o primeiro token), TPOT (tempo por token de saída depois do primeiro), latência p50/p95, vazão, **goodput** (requisições por segundo que cumprem o SLO) e memória real.

- `serving_bench.py`: cliente assíncrono (`asyncio` + `httpx`) para qualquer endpoint OpenAI-compatível com streaming (`llama-server`, Ollama, vLLM). Usa `usage` do stream quando o servidor informa; senão, conta eventos com token. Conta raciocínio visível no TTFT.
- Memória: `--memoria-ollama URL` (lê `/api/ps`) ou `--memoria-pid PID` (`VmRSS`/`VmHWM` em `/proc`; para container: `podman inspect --format '{{.State.Pid}}' <nome>`).
- `test_p01_serving.py`: métricas e parsing com `httpx.MockTransport` e relógio falso.

## Execução real

```bash
podman compose -f laboratorios-mercado/compose.yaml --profile serving up -d
PID=$(podman inspect --format '{{.State.Pid}}' laboratorios-mercado_llama-chat_1)
.venv-mercado/bin/python -I laboratorios-mercado/01_serving_local/serving_bench.py \
  --base-url http://127.0.0.1:8081/v1 --modelo modelo-local --requisicoes 8 --concorrencia 4 \
  --memoria-pid "$PID" --registrar
```

Experimento sugerido: rode com `--concorrencia 1`, `2` e `4` contra um servidor com `--parallel 2`. Em 24/11/2026 (CPU), a vazão subiu de 14,4 para 22,0 tokens/s, mas o TTFT p95 foi de 88 ms para 6,0 s e a fração no SLO caiu de 100% para 25%: a fila come o ganho de vazão. Em 25/11/2026 (RX 9070 XT via Ollama `/v1` + `--sem-raciocinio`), `qwen3:4b-instruct` atingiu `185,5 tok/s` (`100%` SLO em c=4, `2,96 GiB` VRAM) e `qwen3.8:27b-ud-iq3_xxs` atingiu `39,7 tok/s` em c=1 (`100%` SLO, `10,01 GiB` VRAM) e `40,1 tok/s` em c=4 (`25%` SLO, TTFT p95 `4,71 s`). Registros em [`../execucoes/`](../execucoes/).

Limites: tokens contados por evento são aproximação quando o servidor não envia `usage`; vLLM exige GPU NVIDIA (perfil `vllm`).
