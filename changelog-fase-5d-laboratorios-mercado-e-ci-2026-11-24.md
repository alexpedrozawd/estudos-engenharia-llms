# Changelog — Fase 5D: Camada 3 prática (`laboratorios-mercado/`) e CI offline (24/11/2026)

Data: 24/11/2026. Autoria: `claude - pessoal`.
Plano de referência: [`roteiro-central-evolucao-nota-10-por-sessao.md`](roteiro-central-evolucao-nota-10-por-sessao.md) (Sessão 4 — Fase 5D) e [`plano-evolucao-mercado-e-nota-10-2026-11-24.md`](plano-evolucao-mercado-e-nota-10-2026-11-24.md).

## 1. O que entrou

1. **[`laboratorios-mercado/`](laboratorios-mercado/README.md)** na raiz, sem tocar em `laboratorios/` (84 testes offline preservados): `pyproject.toml` (dependências mínimas + extras `containers` e `finetuning`), `compose.yaml` (Podman e Docker; 9 serviços em 7 perfis, todos em `127.0.0.1`), `Containerfile` (usuário sem privilégios), `executar_smoke.py`, base comum `mercado_base/` e registros de execução real em [`laboratorios-mercado/execucoes/`](laboratorios-mercado/execucoes/).
2. **Seis projetos**, cada um com README, smoke-tests offline e roteiro real (`56` testes no total):
   - `01_serving_local`: benchmark `asyncio`/`httpx` com TTFT, TPOT, p50/p95, vazão, goodput e memória (`/api/ps` ou `/proc`).
   - `02_rag_producao`: PDF com tabela (pypdf `layout`) → `pgvector` (HNSW cosseno) + `tsvector` português → RRF → reranker léxico ou por LLM → citações → recall@k, MRR, nDCG e fidelidade lexical.
   - `03_mcp_sandbox`: SDK oficial `mcp` 2.3 (stdio e Streamable HTTP), Pydantic, aprovação humana por *elicitation* com falha fechada e container sem rede, só leitura, sem capabilities.
   - `04_qlora_peft`: receita QLoRA NF4 com manifesto de hashes, divisão estratificada estável, avaliação por fatia e portão antes/depois.
   - `05_api_llmops`: FastAPI com SSE e cancelamento, retry só antes do 1º token, backoff com *full jitter* e `Retry-After`, disjuntor, spans OpenTelemetry `gen_ai.*` sem conteúdo e avaliação contínua.
   - `06_integrador_producao`: guardrails de entrada e saída, roteamento local/fronteira com fallback, MCP, RAG e relatório de custo/latência por etapa.
3. **CI:** [`.github/workflows/testes-offline.yml`](.github/workflows/testes-offline.yml) roda `executar_labs.py`, `guia.py fechar`, `testar-ferramentas.py --rapido`, `testar-fontes.py`, `testar-livros.py`, os smoke-tests da Camada 3 e `docker compose ... config -q`. Sem segredos, `permissions: contents: read`, sem LLM, GPU ou containers de serviço.
4. **Raiz:** `.dockerignore` (contexto de build só com `laboratorios/comum` e `laboratorios-mercado`) e `.gitignore` (`.venv-mercado/`, modelos e artefatos de build).

## 2. Execuções reais (ponta a ponta)

Ambiente: CPU de 16 núcleos, 31 GiB de RAM, GPU AMD sem CUDA; `podman 6.2.0` + `podman-compose 1.6.0` no venv `.venv-mercado` (Python 3.13); llama.cpp server `b12679` (imagem `ghcr.io/ggml-org/llama.cpp:server`, CPU) lendo os GGUF do Ollama em modo somente leitura; `pgvector/pgvector:pg17`.

| Projeto | Registro em `laboratorios-mercado/execucoes/` | Resultado |
|---|---|---|
| 01 | `p01-serving-local-…T20-51-12` e `…T20-51-35` | Qwen3-4B-Thinking-2507 Q4_K_M, `--parallel 2`, 8 requisições × 64 tokens. Concorrência 1: TTFT p50/p95 75/88 ms, TPOT p50 69 ms, 14,4 tokens/s, 100% no SLO. Concorrência 4: TTFT p95 6,0 s, 22,0 tokens/s, goodput 0,086 req/s, 25% no SLO. RSS 5,2 GiB |
| 02 | `p02-rag-pgvector-…T21-04-50` | 3 PDFs, 9 trechos (1 tabela), qwen3-embedding 0.6B (1024 dim.). recall@3 1,0; MRR 0,9444 sem reranker, 0,7963 léxico, 0,8333 LLM. Geração (Qwen3-4B-Instruct-2507): 9/9 com conteúdo esperado, recusa correta, fidelidade média 0,833 |
| 03 | `p03-mcp-stdio-…T21-06-19` e `p03-mcp-streamable-http-…T21-06-28` | Ferramentas listadas com anotações; nota 11 rejeitada; código aprovado rodou em `python:3.13-alpine`; conexão de rede falhou com `Errno 101` |
| 04 | `p04-qlora-manifesto-…T21-08-24` e `p04-qlora-avaliacao-…T21-08-34` | Manifesto (24 treino / 12 teste); linha de base do avaliador: acurácia 0,75 por fatia, formato 100% |
| 05 | `p05-api-llmops-…T21-11-30` | Resposta completa (1 tentativa), SSE com TTFT 235 ms no cliente, cancelamento contado no servidor; 3 spans no console. A imagem do `Containerfile` também respondeu via rede do compose (`api-llmops` → `llama-chat`) |
| 06 | `p06-integrador-…T21-14-31` | 6 cenários: 5 na rota local e 1 bloqueado na entrada; 1 CPF mascarado; 1 chamada MCP; 1 fallback sem fronteira cuja resposta veio sem citação e virou recusa segura; p50 1,7 s, p95 7,0 s |

## 3. Achados e correções durante a fase

- **Ollama do host inoperante:** o daemon em execução (0.40.17) procura `llama-server` em uma pasta do Homebrew já atualizada para 0.40.18 (`llama-server binary not found` em todos os modelos). Não foi reiniciado, por ser serviço compartilhado; as execuções usaram llama.cpp em container. Para normalizar, reinicie o `ollama serve` do host.
- **`qwen3:4b` do Ollama = Qwen3-4B-Thinking-2507** (metadados do GGUF): sempre raciocina; `--reasoning off`, `/no_think` e template com `<think>` vazio não desligam. A geração passou a usar `qwen3:4b-instruct` (Qwen3-4B-Instruct-2507). O benchmark do projeto 01 foi medido com a variante Thinking (raciocínio conta no TTFT).
- **Métrica de fidelidade:** citação depois do ponto (`aulas. [T1]`) virava frase separada e derrubava a média para 0,556; corrigido, com teste de regressão (registro refeito: 0,833).
- **Avaliação contínua:** o retorno por resposta (`{"vazia": true}` = "passou") era ambíguo; virou `{"aprovada", "falhas"}` (registro refeito).
- **Guardrail de saída:** uma resposta com citação e fidelidade 0,0 passava como aprovada; agora fica `aprovado_com_alerta` abaixo de 0,5, sem bloquear, porque a métrica lexical não reconhece paráfrase.
- **Imagem do container:** umask 077 do host deixava o código ilegível para o usuário 10001; `chmod -R a+rX` no build e limpeza de `build/` e `*.egg-info`.
- **MCP 2.x:** `FastMCP` virou `MCPServer`; *elicitation* em processo exige `mode="legacy"` (o modo moderno em processo não tem canal de volta).

## 4. Validações

- `laboratorios-mercado/executar_smoke.py` (`-W error::ResourceWarning`): `Ran 56 tests` → `OK`, no venv do projeto e num venv limpo só com `pip install -e ./laboratorios-mercado` (mesma sequência do CI).
- `podman compose -f laboratorios-mercado/compose.yaml` com os 7 perfis: `config -q` com código 0 (9 serviços).
- `laboratorios/executar_labs.py`: `Ran 84 tests` → `OK` (inalterado).
- `ferramentas/guia.py fechar`: 0 falhas (`validar-guia.py` 18 OK; 26 trechos OK + 21 ilustrativos); HTML sha `45e11a0cd880451a` e PDF sha `482a150cb91f3efc` (664 páginas) inalterados.
- `testar-ferramentas.py` sem `--rapido`: `Ran 19 tests` → `OK`; `testar-fontes.py`: 14 OK; `testar-livros.py`: 2 OK.
- `auditar-guia-navegador.mjs`: 385 seções sem estouro em 320 px, 453 questões, axe-core 46 passes e 0 violações (1280×800 e 320×640), 0 falhas.
- Registros de execução sem caminhos pessoais, senhas ou chaves (DSN gravado como `postgresql://***@pgvector`).

## 5. Pendências e limites

- **QLoRA real (`treinar`) não executado:** exige GPU CUDA; o caminho de treino fica `[Não verificado]` em execução.
- **vLLM:** só configurado (perfil `vllm`, GPU NVIDIA); não executado.
- **`docker compose config`:** validado só no CI (não há Docker no host); localmente, `podman compose`.
- **Corpus do RAG pequeno** (recall trivial) e **fidelidade lexical conservadora**; ampliar o corpus e somar avaliador por LLM ou humano é extensão natural.
- **Uso de disco local:** 2 modelos Ollama novos (`qwen3-embedding:0.6b`, 639 MB; `qwen3:4b-instruct`, 2,5 GB) e imagens de container (`pgvector`, `llama.cpp:server`, `python:3.13-alpine`, `localhost/laboratorios-mercado:dev`). Remoção: `ollama rm <modelo>` e `podman rmi <imagem>`.
- **Próxima fase:** `5E` (revisão técnica humana `L1`, piloto `L2`, 18 aquarelas `L8` e PDF definitivo).
