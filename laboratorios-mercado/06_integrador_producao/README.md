# 06 — Integrador de produção

Assistente acadêmico ponta a ponta (`integrador_app.py`), reutilizando os projetos 02, 03 e 05 e `mercado_base/` (além do cliente neutro em `laboratorios/comum` para provedores de fronteira opcionais):

1. **Segurança HTTP opcional e anti-BFLA:** autenticação via `X-API-Key` / `Authorization: Bearer`, vínculo opcional chave → perfil máximo (`AURORA_PERFIS_CHAVES`, bloqueando elevação com HTTP `403`) e *rate limiting* (`429 + Retry-After`) via `mercado_base.seguranca_http`.
2. **Guardrail de entrada:** bloqueia padrões de injeção de prompt antes de qualquer chamada ao LLM; mascara CPF (com validação de dígitos verificadores), e-mail e telefone via `mercado_base.pii`.
3. **Roteamento:** dado pessoal → local; pergunta complexa com orçamento → fronteira; sem cliente de fronteira → local com motivo `fallback`.
4. **RAG com ACL e vigência:** busca híbrida do projeto 02 com `FiltroBusca(perfil=..., apenas_vigentes=...)` pré-filtrado em SQL no `pgvector`.
5. **Laço agêntico MCP + *structured outputs*:** converte as ferramentas do servidor MCP (`consultar_prazo`, `calcular_media_ponderada`, `executar_python_isolado` com *elicitation*/falha fechada) para `tools` OpenAI via `mcp_tools_para_openai`, executa até `max_passos_agente` passos via `ClienteChatOpenAI` e consolida em `RespostaEstruturada` (`response_format` `json_schema` estrito + reparo automático via Pydantic + degradação segura sem HTTP `500` em falha persistente de schema), medindo `tokens_cache`.
6. **Guardrail de saída e histórico limitado:** mascara CPF, e-mail e telefone que escaparem; exige citação `[Tn]` válida; registra histórico em `collections.deque(maxlen=...)` mantendo contadores cumulativos em `GET /v1/relatorio`.

Preços: `Precos` vem com fronteira em valores **ilustrativos** (USD por milhão de tokens); configure `INTEGRADOR_PRECOS_JSON` com a tabela vigente do seu fornecedor. O custo local não inclui energia nem hardware.

## Execução real

```bash
podman compose -f laboratorios-mercado/compose.yaml --profile serving --profile rag up -d
PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
EMBED_BASE_URL=http://127.0.0.1:8082/v1 EMBED_MODELO=embed-local \
LLM_LOCAL_BASE_URL=http://127.0.0.1:8081/v1 LLM_LOCAL_MODELO=modelo-local INTEGRADOR_INGERIR=1 \
.venv-mercado/bin/python -I -m uvicorn --app-dir laboratorios-mercado/06_integrador_producao \
  --factory integrador_app:criar_app_de_ambiente --port 8001 &
.venv-mercado/bin/python -I laboratorios-mercado/06_integrador_producao/cliente_integrador_real.py --registrar
```

Fronteira opcional: `FRONTEIRA_PROVEDOR=openai|anthropic|gemini` (+ `FRONTEIRA_MODELO` e a chave do provedor por variável de ambiente). Para modelos locais com modo *thinking* no Ollama `/v1`, defina `LLM_LOCAL_REASONING_EFFORT=none`.

Em 25/11/2026 (Fase 6, `qwen3:4b-instruct` com `--jinja` + `pgvector`): `8` cenários, `7` respondidos na rota local e `1` bloqueado na entrada; `0` bloqueios de saída; `5` chamadas nativas MCP via `tool_calls` (`consultar_prazo`, `calcular_media_ponderada` com média `6.7`, `executar_python_isolado` negado por padrão em falha fechada); `0` reparos de JSON; `13.555` tokens em cache de prefixo de `16.641` tokens de entrada; CPF e telefone mascarados.

Em 25/11/2026 (Etapa 2 na GPU via Ollama `/v1`, `LLM_LOCAL_REASONING_EFFORT=none`): `qwen3:4b-instruct` (`5` chamadas MCP, `9.511` tokens em cache, p50 `2,37 s` / p95 `4,58 s`, `4,09 GiB` VRAM) vs `qwen3.8:27b-ud-iq3_xxs` (`3` chamadas MCP, `8.075` tokens em cache, p50 `7,93 s` / p95 `17,78 s`, `11,14 GiB` VRAM), ambos com `0` reparos/falhas de esquema e `0` bloqueios de saída.

Em 25/11/2026 (validação real anti-BFLA com `INTEGRADOR_PERFIS_CHAVES`): `4/4` verificações aprovadas contra `uvicorn` + `llama.cpp` + `pgvector` — HTTP `401` (`nao_autenticado`) sem chave, HTTP `403` (`perfil_nao_autorizado`, `perfil_maximo: "aluno"`) ao solicitar `perfil: "admin"` com chave de aluno, HTTP `200` sem vazamento de `manual-financeiro-administrativo` no perfil `aluno` e HTTP `200` com acesso ao trecho restrito no perfil `admin` (registro em `execucoes/p06-integrador-anti-bfla-*.json`).

Limites: regras de roteamento e padrões de injeção são didáticos (listas fixas não bastam contra ataques adaptativos); combine com as defesas do Cap. 12 do guia (Segurança, Guardrails e IA Responsável).
