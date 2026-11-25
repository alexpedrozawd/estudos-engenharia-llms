# Changelog — Fase 6: Endurecimento de mercado, Projeto 07, higiene `docs/` e CI (25/11/2026)

Data: 25/11/2026. Autoria: `agy - ap`.
Plano de referência: [`plano-evolucao-mercado-e-nota-10-2026-11-24.md`](../historico/plano-evolucao-mercado-e-nota-10-2026-11-24.md) e [`roteiro-central-evolucao-nota-10-por-sessao.md`](../historico/roteiro-central-evolucao-nota-10-por-sessao.md).

## 1. O que mudou

1. **Etapa 6.1 — Endurecimento de `mercado_base/`, `05_api_llmops` e `06_integrador_producao`:**
   - Criado [`laboratorios-mercado/mercado_base/pii.py`](../../laboratorios-mercado/mercado_base/pii.py) com validação de dígitos verificadores de CPF (`cpf_valido`), `RE_EMAIL` e `RE_TELEFONE`, aplicando substituição de CPF antes de telefone (`mascarar_pii`). Aplicado em `AvaliadorContinuo` (`05_api_llmops/llmops_telemetria.py`) e em `verificar_entrada`/`verificar_saida` (`06_integrador_producao/integrador_app.py`).
   - Criado [`laboratorios-mercado/mercado_base/seguranca_http.py`](../../laboratorios-mercado/mercado_base/seguranca_http.py) com autenticação opcional (`X-API-Key` / `Authorization: Bearer` via `hmac.compare_digest`) e *rate limiting* em janela deslizante (`429` + `Retry-After`), aplicado nas rotas HTTP de `05` e `06` (mantendo `/saude` público).
   - Em `05_api_llmops`: `ErroPermanente` upstream `401/403/404` mapeado para HTTP `502` (`llmops_api.py`, `llmops_resiliencia.py`); exposto endpoint `GET /metrics` no formato Prometheus; `cliente_api_real.py` atualizado para testar `401`, `/metrics` e traces OTLP na API v3 do Jaeger (`v2.23.0`).
   - Em `06_integrador_producao/integrador_app.py`: `Assistente.registros` migrado para `collections.deque(maxlen=...)` preservando acumuladores cumulativos em `_totais`.
2. **Etapa 6.2 — *Tool calling* nativo, *structured outputs* reais e laço agêntico MCP:**
   - Criado [`laboratorios-mercado/mercado_base/cliente_openai.py`](../../laboratorios-mercado/mercado_base/cliente_openai.py) (`ClienteChatOpenAI`, `ClienteChatFalso`, `esquema_json_estrito`, `gerar_estruturado` com reparo via Pydantic e extração de `cached_tokens`/`timings.cache_n`).
   - Adicionada flag `--jinja` ao serviço `llama-chat` em [`laboratorios-mercado/compose.yaml`](../../laboratorios-mercado/compose.yaml).
   - Substituído o disparo por palavras-chave em `integrador_app.py` pelo laço agêntico real via `mcp_tools_para_openai` (integrando `consultar_prazo`, `calcular_media_ponderada` e `executar_python_isolado` com *elicitation*/falha fechada) e consolidação por `RespostaEstruturada`.
3. **Etapa 6.3 — Escala do RAG com ACL e corpus não trivial (`02_rag_producao`):**
   - `corpus_aurora.py` expandido de `3` para `12` PDFs (`41` trechos com `4` tabelas Markdown, versões revogadas de 2024 vs vigentes 2026, distrações em biblioteca/estágio e documentos restritos a `docente`, `coordenacao` e `admin`); `dados/consultas_ouro.json` expandido para `28` consultas.
   - `FiltroBusca` com pré-filtragem SQL parametrizada em `ArmazemPgvector` (`%s = ANY(perfis)`, `vigente`, `departamento`, `versao`, `tipo`) e `ArmazemMemoria`, antes do `ORDER BY ... LIMIT`.
   - `rag_pipeline.py` atualizado com modos `vetorial`, `lexical`, `hibrida` (RRF) e função `auditar_acl`; `integrador_app.py` atualizado com `perfil` e `apenas_vigentes`.
4. **Etapa 6.4 — Novo Projeto [`07_evals_e_multimodal`](../../laboratorios-mercado/07_evals_e_multimodal/README.md):**
   - `eval_pipeline.py` + `dados/casos_eval.json`: `12` pares de calibração + `16` casos de avaliação comparando `PROMPT_A` vs `PROMPT_B` com LLM-as-a-judge estruturado, inversão A/B, *kappa* de Cohen (`>= 0,60`) e bootstrap pareado.
   - `extracao_multimodal.py`: conversão PDF → PNG via `pdftoppm` (`poppler-utils`, sem adicionar `Pillow`), payload OpenAI `image_url` base64, validação Pydantic `FaturaExtraida` e auditoria aritmética determinística.
   - Registrado em `mercado_base/__init__.py`, `Containerfile` e `pyproject.toml`.
5. **Etapa 6.5 — Higiene em `docs/`, `README.md` e fortalecimento do CI:**
   - Movidos via `git mv` os arquivos históricos soltos da raiz para [`docs/changelogs/`](../changelogs/), [`docs/fontes/`](../fontes/) e [`docs/historico/`](../historico/), mantendo na raiz apenas os arquivos principais e os ignorados locais.
   - Atualizados [`ferramentas/fontes.py`](../../ferramentas/fontes.py), [`ferramentas/testar-fontes.py`](../../ferramentas/testar-fontes.py), [`ferramentas/conferir-trechos.py`](../../ferramentas/conferir-trechos.py), links em [`README.md`](../../README.md), [`CLAUDE.md`](../../CLAUDE.md), [`roadmap.md`](../../roadmap.md) e documentos em `docs/`.
   - Adicionado roteiro de estudo pessoal ao [`README.md`](../../README.md), documentada alternativa `:ro,Z` ao `label=disable` em [`compose.yaml`](../../laboratorios-mercado/compose.yaml) e incluído build/smoke do `Containerfile` em [`.github/workflows/testes-offline.yml`](../../.github/workflows/testes-offline.yml).

## 2. Execuções reais registradas (25/11/2026)

Ambiente: `llama.cpp:server` em container (CPU, `--jinja`, `qwen3:4b-instruct` e `qwen3-embedding:0.6b`), `pgvector/pgvector:pg17`, `jaegertracing/jaeger:latest` (`v2.23.0`), encerrados via `podman compose down` ao fim.

- **`05_api_llmops`** (`p05-api-llmops-2026-11-25T00-07-46-0300.json`): `401` sem chave, `200` com `X-API-Key`, SSE TTFT `199,0 ms`, cancelamento detectado, `GET /metrics` Prometheus `200` e `6` spans recebidos na API v3 do Jaeger (`aurora-api-llmops`).
- **`02_rag_producao`** (`p02-rag-pgvector-2026-11-25T00-15-39-0300.json`): `12` documentos, `41` trechos; `auditoria_acl` com `0` vazamentos em `4` consultas; `recall@4` `1,0` (vetorial), `0,92` (lexical), `0,98` (híbrida RRF), `0,94` (léxico) e `0,98` (LLM); MRR `0,9333` (vetorial), `0,92` (híbrida RRF); geração `23/25` acertos, `3/3` recusas corretas, fidelidade média `0,84`.
- **`06_integrador_producao`** (`p06-integrador-2026-11-25T00-45-13-0300.json`): `8` cenários, `0` bloqueios de saída, `5` chamadas MCP nativas via `tool_calls`, `0` reparos de `json_schema`, `13.555` tokens em cache de prefixo (de `16.641` de entrada), PII (`cpf` + `telefone`) mascarada e injeção bloqueada.
- **`07_evals_e_multimodal`** (`p07-evals-e-multimodal-2026-11-25T00-40-58-0300.json`): calibração `kappa = 0,7391` (`12` pares); avaliação `16` casos com `B = 13`, `empate = 3`, `A = 0` (`3` vieses neutralizados, `+1,5625` no bootstrap, `promover_b = true`); renderização `pdftoppm` gerou PNG real (`55.395` bytes) e payload VLM validado (`vlm_remoto_executado: false` sem VLM local).

## 3. Preservação dos artefatos congelados

- `guia-engenharia-llms.html`: `sha256` `bb004776a6cdc9cbabb78399747157bf9f82909391411e7ade96e0e3a3245195` (intacto).
- `guia-engenharia-llms.pdf`: `sha256` `81d2fffd7394a8800eaf51b5c2c90409062dbee373e7c45ec9e7890843cadd84` (intacto).
- `laboratorios/`: `0` alterações (`84` testes offline intactos).
- `L1` (revisão técnica humana) e `L2` (piloto com estudantes) permanecem bloqueados fora do escopo desta fase.
