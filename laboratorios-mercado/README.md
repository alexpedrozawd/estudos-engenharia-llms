# Laboratórios de mercado (Camada 3)

Sete projetos com serviços reais, complementares aos laboratórios offline em [`../laboratorios/`](../laboratorios/README.md) (que continuam só com biblioteca padrão). Cada projeto tem smoke-tests offline e determinísticos, além de um roteiro de execução real com registro em [`execucoes/`](execucoes/). Os exemplos usam a Aurora Educação, instituição fictícia, como proposta didática.

| Projeto | Capítulos | O que pratica | Serviço real |
|---|---|---|---|
| [`01_serving_local`](01_serving_local/README.md) | 14 | Benchmark assíncrono: TTFT, TPOT, p95, goodput e memória | llama.cpp server, Ollama ou vLLM |
| [`02_rag_producao`](02_rag_producao/README.md) | 5, 7 | 12 PDFs com tabelas e versões → `pgvector` + ACL por perfil → RRF → reranker → citações | PostgreSQL + pgvector, embeddings |
| [`03_mcp_sandbox`](03_mcp_sandbox/README.md) | 10, 12, 13 | Servidor e cliente MCP (stdio e Streamable HTTP), Pydantic, aprovação humana, container sem rede | SDK oficial `mcp` 2.x, Podman/Docker |
| [`04_qlora_peft`](04_qlora_peft/README.md) | 6, 15 | Receita QLoRA reproduzível, manifesto, avaliação por fatia e portão antes/depois | `peft`/`trl` (GPU CUDA ou AMD ROCm 7.x) |
| [`05_api_llmops`](05_api_llmops/README.md) | 2, 17 | FastAPI, auth/rate limit, SSE com cancelamento, retry/disjuntor, Prometheus `/metrics`, OTLP → Jaeger e avaliação contínua | Endpoint OpenAI-compatível + Jaeger |
| [`06_integrador_producao`](06_integrador_producao/README.md) | 12, 16, 18 | Guardrails PII/injeção, roteamento, laço agêntico MCP (`tool_calls`), `json_schema` estrito, RAG com ACL e relatório de custo/cache | Todos os anteriores |
| [`07_evals_e_multimodal`](07_evals_e_multimodal/README.md) | 4, 5 | Evals A vs B com juiz calibrado (inversão A/B, *kappa* de Cohen, bootstrap pareado) e PDF → PNG (`pdftoppm`) → VLM/Pydantic | Endpoint OpenAI-compatível (e VLM opcional) |

## Ambiente (sem alterar a imagem do sistema)

```bash
# na raiz do repositório; Python 3.11+ (3.13 recomendado)
python3.13 -m venv .venv-mercado
.venv-mercado/bin/python -m pip install -e "./laboratorios-mercado[containers]"
```

- `[containers]` instala o `podman-compose`, que o `podman compose` usa quando não há `docker-compose`. Com o venv no `PATH`: `export PATH="$PWD/.venv-mercado/bin:$PATH"`.
- `[finetuning]` (torch, transformers, peft, trl, datasets, bitsandbytes>=0.50, accelerate) só é necessário para treinar no projeto 04 e exige GPU (CUDA ou AMD ROCm via perfil `finetuning` do `compose.yaml`).
- Use instalação editável (`-e`): os registros de execução são gravados em `laboratorios-mercado/execucoes/`.

## Smoke-tests offline

```bash
.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py            # todos (83 testes)
.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py --alvo 07_evals_e_multimodal
```

Não usam rede, GPU nem containers: `httpx.MockTransport`, armazém vetorial em memória, conexão SQL falsa, MCP em processo, executor de sandbox falso e relógios injetados. O mesmo comando roda no CI ([`../.github/workflows/testes-offline.yml`](../.github/workflows/testes-offline.yml)).

## Modo exercício

Para praticar sem a solução, gere a cópia com trechos em branco: `python3 -I ferramentas/gerar-exercicios.py` (roteiro em [README.md](../README.md#modo-exercício-labs-sem-a-solução)).

## Serviços (`compose.yaml`, Podman ou Docker)

Todos os serviços ficam em perfis e escutam só em `127.0.0.1`.

| Perfil | Serviços | Porta no host |
|---|---|---|
| `serving` | `llama-chat` (`--jinja`), `llama-embed` (llama.cpp server) | 8081, 8082 |
| `rag` | `postgres` (pgvector), `llama-embed` | 5433, 8082 |
| `app` | `api-llmops`, `integrador` (imagem do [`Containerfile`](Containerfile)) e dependências | 8000, 8001 |
| `ollama` / `vllm` | Ollama em container / vLLM (exige GPU NVIDIA) | 11435 / 8083 |
| `observabilidade` | Jaeger (UI, query v3 e OTLP/HTTP) | 16686, 4318 |
| `sandbox` | Modelo de container restrito usado pelo projeto 03 | — |
| `finetuning` | `qlora-rocm` (`rocm/pytorch` com `/dev/kfd` e `/dev/dri` para GPU AMD) | — |

```bash
export MODELOS_DIR=/caminho/dos/gguf MODELO_CHAT_ARQUIVO=chat.gguf MODELO_CHAT_ALIAS=modelo-local \
       MODELO_EMBED_ARQUIVO=embed.gguf MODELO_EMBED_ALIAS=embed-local
podman compose -f laboratorios-mercado/compose.yaml --profile serving --profile rag up -d
podman compose -f laboratorios-mercado/compose.yaml --profile serving --profile rag config -q   # validação
```

- `PG_SENHA` tem um padrão só para laboratório local; troque fora da sua máquina.
- Autenticação opcional e limite de taxa nas APIs (`05` e `06`): configure `AURORA_API_KEYS` (aceita `X-API-Key` ou `Authorization: Bearer`) e `AURORA_RATE_LIMIT_RPM`.
- Para reaproveitar modelos já baixados pelo Ollama sem copiar, aponte `MODELOS_DIR` para `~/.ollama/models/blobs` e use o nome `sha256-...` da camada `model` do manifesto em `~/.ollama/models/manifests/`. O volume é somente leitura; `label=disable` evita reetiquetar arquivos do daemon do host em SELinux (em pastas dedicadas de modelos, prefira `:ro,Z` sem `label=disable`).
- Modelos "Thinking" (ex.: Qwen3-4B-Thinking-2507, a tag `qwen3:4b` do Ollama em 11/2026) sempre raciocinam: `--reasoning off` não desliga. Para respostas diretas e *tool calling*, use uma variante Instruct (ex.: `qwen3:4b-instruct`).

## Provedores de fronteira (opcionais)

Os projetos reaproveitam [`../laboratorios/comum/cliente_llm.py`](../laboratorios/comum/cliente_llm.py): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` ou `GEMINI_API_KEY` só por variável de ambiente. A chave Gemini vai apenas no cabeçalho `x-goog-api-key`, nunca na URL. Nenhum teste nem o CI usa chaves.

## Execuções reais registradas (24–25/11/2026)

Máquina: CPU de 16 núcleos, 31 GiB de RAM, sem GPU CUDA; llama.cpp server em container (CPU, `--jinja`); PostgreSQL 17 + pgvector; Jaeger `v2.23.0`. Detalhes em [`changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md`](../docs/changelogs/changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md) e [`changelog-fase-6-mercado-producao-2026-11-25.md`](../docs/changelogs/changelog-fase-6-mercado-producao-2026-11-25.md).

| Projeto | Resultado |
|---|---|
| 01 | Qwen3-4B-Thinking-2507 Q4_K_M, 2 slots: concorrência 1 → TTFT p95 88 ms, 14,4 tokens/s, 100% no SLO; concorrência 4 → TTFT p95 6,0 s, 22,0 tokens/s, 25% no SLO; RSS 5,2 GiB |
| 02 | Fase 6: 12 PDFs, 41 trechos, `qwen3-embedding:0.6b` + `qwen3:4b-instruct`; `auditoria_acl` com `0` vazamentos; `recall@4` `1,0` vetorial / `0,98` híbrida RRF / `0,92` lexical; `23/25` acertos, `3/3` recusas corretas, fidelidade média `0,84` |
| 03 | stdio e Streamable HTTP; validação recusou nota 11; código aprovado rodou em container sem rede (`Network unreachable` na tentativa de conexão) |
| 04 | QLoRA 4-bit NF4 real em AMD RX 9070 XT (`rocm7.14.1` + `bitsandbytes 0.50.2`, `Qwen/Qwen3-1.7B`): base `0,6667`; `3` épocas (`8,55 s`) `0,5833` reprovada pelo portão (`informal` caiu); `12` épocas (`22,53 s`) `0,9167` (`+0,25` em todas as fatias), aprovada pelo portão antigo, mas **inconclusiva** pelo portão estatístico de 25/11/2026 (8/12 → 11/12, McNemar exato `p ≥ 0,25`; épocas escolhidas no teste) |
| 05 | Fase 6: `401` sem chave, `200` com `X-API-Key`, SSE (TTFT `199 ms`), cancelamento (`cancelados: 1`), `GET /metrics` Prometheus e `6` spans recebidos na API v3 do Jaeger |
| 06 | Fase 6 + anti-BFLA real: `8` cenários com `5` chamadas MCP nativas via `tool_calls` (`0` reparos de `json_schema`, `0` bloqueios de saída, `13.555` tokens em cache de prefixo, PII mascarada, injeção bloqueada) e `4/4` verificações anti-BFLA reais (`401` sem chave, `403` na elevação `aluno -> admin`, `200` sem vazamento vs `admin` autorizado) |
| 07 | Fase 6: calibração `kappa = 0,7391` (`12` pares), avaliação `16` casos (`B = 13`, `empate = 3`, `A = 0`; `3` vieses neutralizados; `+1,5625` no bootstrap, `promover_b = true`) e PNG real via `pdftoppm` (VLM remoto arquivado pelo operador) |
