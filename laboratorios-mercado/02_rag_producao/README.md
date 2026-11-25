# 02 — RAG de produção com pgvector

Fluxo completo: PDF com tabela → trechos → embeddings → PostgreSQL + `pgvector` (índice HNSW por cosseno) e busca lexical (`tsvector` em português) → fusão RRF → reranker → resposta com citações `[T1]` → métricas.

- `rag_ingestao.py`: lê o PDF em modo `layout` (pypdf), transforma blocos alinhados em tabela Markdown e repete o cabeçalho em cada pedaço; texto corrido em janelas com sobreposição.
- `rag_store.py`: `EmbedderOpenAICompativel` (`/v1/embeddings`), `ArmazemPgvector` (SQL parametrizado, sem sintaxe de busca vinda do usuário) e `ArmazemMemoria`/`EmbedderHash` para testes.
- `rag_pipeline.py`: RRF, `ReordenadorLexico`, `ReordenadorLLM` (nota 0–3, falha segura), recall@k, MRR, nDCG@k e fidelidade lexical (frases apoiadas no trecho citado).
- `corpus_aurora.py` e `dados/consultas_ouro.json`: corpus fictício (3 documentos) e 10 perguntas com relevância por critério estável (documento, página, texto), incluindo uma sem resposta.
- `executar_rag_real.py`: ingestão, avaliação de três variantes (sem reranker, léxico, LLM) e geração com a variante de melhor MRR medido.

## Execução real

```bash
podman compose -f laboratorios-mercado/compose.yaml --profile serving --profile rag up -d
PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
.venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/executar_rag_real.py \
  --embed-base-url http://127.0.0.1:8082/v1 --embed-modelo embed-local \
  --llm-base-url http://127.0.0.1:8081/v1 --llm-modelo modelo-local --registrar
```

Resultado de 24/11/2026 (qwen3-embedding 0.6B + Qwen3-4B-Instruct-2507): recall@3 = 1,0; MRR 0,94 sem reranker contra 0,80 (léxico) e 0,83 (LLM). **Nem todo reranker ajuda: meça antes de pôr em produção.** Geração: 9/9 com o conteúdo esperado, recusa correta na pergunta sem resposta, fidelidade lexical média 0,83.

Limites: cada operação abre uma conexão (simples para estudo; em produção use `psycopg_pool`); corpus pequeno (9 trechos) deixa o recall trivial; a fidelidade lexical não reconhece paráfrase (a resposta em primeira pessoa da q02 marcou 0,0) e serve só de portão barato antes de avaliador por LLM ou humano; PDFs escaneados ou tabelas sem alinhamento de texto exigem OCR ou extrator de layout.
