# 06 — Integrador de produção

Assistente acadêmico ponta a ponta (`integrador_app.py`), reutilizando os projetos 02, 03 e 05 e o cliente neutro de `laboratorios/comum`:

1. **Guardrail de entrada:** bloqueia padrões de injeção de prompt antes de qualquer chamada ao LLM; mascara CPF, e-mail e telefone.
2. **Roteamento:** dado pessoal → local; pergunta complexa com orçamento → fronteira; sem cliente de fronteira → local com motivo `fallback`.
3. **Ferramenta MCP:** perguntas de prazo chamam `consultar_prazo` no servidor do projeto 03 (em processo, só leitura); o resultado entra como trecho citável.
4. **RAG:** busca híbrida do projeto 02 (pgvector em produção).
5. **Guardrail de saída:** sem citação válida → recusa segura; fidelidade lexical abaixo de 0,5 → `aprovado_com_alerta` para revisão amostral; PII mascarada.
6. **Relatório** (`GET /v1/relatorio`): requisições por rota, bloqueios, alertas, fallbacks, latência p50/p95 total e por etapa, tokens e custo.

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

Fronteira opcional: `FRONTEIRA_PROVEDOR=openai|anthropic|gemini` (+ `FRONTEIRA_MODELO` e a chave do provedor por variável de ambiente).

Em 24/11/2026 (sem fronteira configurada): 6 cenários, 5 respondidos na rota local e 1 bloqueado na entrada; 1 CPF mascarado; 1 chamada MCP; 1 fallback cuja resposta veio sem citação e virou recusa segura; latência p50 1,7 s e p95 7,0 s (CPU). Rodadas repetidas variam: temperatura 0 em CPU com 2 slots paralelos não garante saída idêntica.

Limites: regras de roteamento e padrões de injeção são didáticos (listas fixas não bastam contra ataques adaptativos); combine com as defesas do Cap. 12 do guia (Segurança, Guardrails e IA Responsável).
