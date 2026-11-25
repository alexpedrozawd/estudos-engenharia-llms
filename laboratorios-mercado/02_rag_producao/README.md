# 02 — RAG de produção com pgvector

Fluxo completo: PDF com tabela → trechos → embeddings → PostgreSQL + `pgvector` (índice HNSW por cosseno) e busca lexical (`tsvector` em português) → fusão RRF → reranker → resposta com citações `[T1]` → métricas.

- `rag_ingestao.py`: lê o PDF em modo `layout` (pypdf), transforma blocos alinhados em tabela Markdown e repete o cabeçalho em cada pedaço; texto corrido em janelas com sobreposição.
- `rag_store.py`: `EmbedderOpenAICompativel` (`/v1/embeddings`), `ArmazemPgvector` (SQL parametrizado, sem sintaxe de busca vinda do usuário) e `ArmazemMemoria`/`EmbedderHash` para testes.
- `rag_pipeline.py`: RRF, `ReordenadorLexico`, `ReordenadorLLM` (nota 0–3, falha segura), recall@k, MRR, nDCG@k e fidelidade lexical (frases apoiadas no trecho citado).
- `corpus_aurora.py` e `dados/consultas_ouro.json`: corpus fictício (`12` PDFs, `41` trechos com `4` tabelas Markdown, versões conflitantes 2024 vs 2026, distrações lexicais e documentos restritos por perfil) e `28` consultas ouro (incluindo versões conflitantes, ACL e `3` sem resposta).
- `rag_store.py` e `rag_pipeline.py`: `FiltroBusca` com pré-filtragem SQL parametrizada (ACL por `perfis` e `vigente`) antes do `ORDER BY ... LIMIT`, modos `vetorial`, `lexical` e `hibrida` (RRF), `ReordenadorLexico`, `ReordenadorLLM` e `auditar_acl`.
- `executar_rag_real.py`: ingestão, comparação de `5` variantes (`vetorial`, `lexical`, `hibrida_rrf`, `hibrida_reranker_lexico`, `hibrida_reranker_llm`), auditoria de vazamentos ACL e geração.

## Execução real

```bash
podman compose -f laboratorios-mercado/compose.yaml --profile serving --profile rag up -d
PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
.venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/executar_rag_real.py \
  --embed-base-url http://127.0.0.1:8082/v1 --embed-modelo embed-local \
  --llm-base-url http://127.0.0.1:8081/v1 --llm-modelo modelo-local --registrar
```

Resultado da Fase 6 (`25/11/2026`, `qwen3-embedding:0.6b` + `qwen3:4b-instruct`, `12` PDFs, `41` trechos, `28` consultas): `auditoria_acl` com `0` vazamentos em `4` consultas restritas; `recall@4` `1,0` (`vetorial`), `0,92` (`lexical`), `0,98` (`híbrida RRF`), `0,94` (*reranker* léxico) e `0,98` (*reranker* LLM); MRR `0,9333` (`vetorial`), `0,92` (`híbrida RRF`), `0,88` (*reranker* LLM); geração com `23/25` conteúdos esperados, `3/3` recusas corretas e fidelidade lexical média `0,84`.

Limites: cada operação abre uma conexão (simples para estudo; em produção use `psycopg_pool`); a fidelidade lexical não reconhece paráfrase (ex.: `q01` citou a data do calendário em vez do texto do regulamento) e serve só de portão barato antes de avaliador por LLM ou humano; PDFs escaneados ou tabelas sem alinhamento de texto exigem OCR ou extrator de layout (ou extração VLM no Projeto 07).
