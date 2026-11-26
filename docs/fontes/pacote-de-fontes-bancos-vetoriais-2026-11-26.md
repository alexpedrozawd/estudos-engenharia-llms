# Pacote de fontes: bancos vetoriais para os casos de system design (26/11/2026)

Data: 26/11/2026. Autoria: claude - pessoal. Etapa 5 do [plano de prontidão](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md). Base do trade-off entre `pgvector` e bancos vetoriais gerenciados ou bibliotecas (Pinecone, Weaviate, FAISS) no caso 1 de [casos-de-system-design.md](../preparacao-para-vaga/casos-de-system-design.md). O guia HTML não cita esses produtos; o pacote serve só aos documentos de `docs/preparacao-para-vaga/`.

## 1. Fontes baixadas e como reconferir

Baixadas para `cache-fontes/bruto/` e extraídas para `cache-fontes/textos/` com `python3 -I ferramentas/fontes.py baixar --pacote pacote-de-fontes-bancos-vetoriais-2026-11-26.md && python3 -I ferramentas/fontes.py extrair`. Preços e limites de plano mudam com frequência e ficaram fora: confira na página do fornecedor no dia da decisão.

| Chave | Fonte pública e endereço efetivo | Hash bruto (16) |
|---|---|---|
| `pgvector-readme` | pgvector, *README* (repositório oficial) — https://raw.githubusercontent.com/pgvector/pgvector/master/README.md | `09822384ee0ebd5d` |
| `faiss-readme` | Meta, *Faiss README* (repositório oficial) — https://raw.githubusercontent.com/facebookresearch/faiss/main/README.md | `24679e12982711be` |
| `faiss-escolher-indice` | Meta, *Guidelines to choose an index* (wiki oficial) — https://raw.githubusercontent.com/wiki/facebookresearch/faiss/Guidelines-to-choose-an-index.md | `ea092c6db681526e` |
| `pinecone-indexacao` | Pinecone, *Indexing overview* — https://docs.pinecone.io/guides/indexes/index-data-overview.md | `dc07d473f23fc45a` |
| `pinecone-arquitetura` | Pinecone, *Architecture* — https://docs.pinecone.io/guides/get-started/architecture.md | `7e862827d37916bb` |
| `pinecone-multitenancy` | Pinecone, *Implement multitenancy* — https://docs.pinecone.io/guides/data/implement-multitenancy.md | `3382a8a20e3d1af6` |
| `pinecone-hibrida` | Pinecone, *Hybrid search* — https://docs.pinecone.io/guides/search/hybrid-search.md | `31a7577e623b53b4` |
| `weaviate-indice-vetorial` | Weaviate, *Vector indexing* — https://docs.weaviate.io/weaviate/concepts/vector-index.md | `657a704666833b55` |
| `weaviate-hibrida` | Weaviate, *Hybrid search* — https://docs.weaviate.io/weaviate/search/hybrid | `e6d67e9f5517695b` |
| `weaviate-multi-tenancy` | Weaviate, *Multi-tenancy operations* — https://docs.weaviate.io/weaviate/manage-collections/multi-tenancy | `66cf875b12a4b128` |

Comando de conferência: `python3 -I ferramentas/conferir-trechos.py --pacote docs/fontes/pacote-de-fontes-bancos-vetoriais-2026-11-26.md --textos cache-fontes/textos --projeto .`

## 2. Fontes e trechos

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| BV-01 | Caso 1 — pgvector | texto | pgvector-readme | Introdução | GitHub, consultado em 26/11/2026 | registrado na documentação | Store your vectors with the rest of your data. |
| BV-02 | Caso 1 — pgvector | texto | pgvector-readme | Querying | GitHub, consultado em 26/11/2026 | registrado na documentação | By default, pgvector performs exact nearest neighbor search, which provides perfect recall. |
| BV-03 | Caso 1 — pgvector | texto | pgvector-readme | Indexing | GitHub, consultado em 26/11/2026 | registrado na documentação | You can add an index to use approximate nearest neighbor search, which trades some recall for speed. Unlike typical indexes, you will see different results for queries after adding an approximate index. |
| BV-04 | Caso 1 — pgvector | texto | pgvector-readme | HNSW | GitHub, consultado em 26/11/2026 | registrado na documentação | An HNSW index creates a multilayer graph. It has better query performance than IVFFlat (in terms of speed-recall tradeoff), but has slower build times and uses more memory. |
| BV-05 | Caso 1 — pgvector | texto | pgvector-readme | Filtering | GitHub, consultado em 26/11/2026 | registrado na documentação | With approximate indexes, filtering is applied *after* the index is scanned. If a condition matches 10% of rows, with HNSW and the default `hnsw.ef_search` of 40, only 4 rows will match on average. |
| BV-06 | Caso 1 — pgvector | texto | pgvector-readme | Iterative Index Scans | GitHub, consultado em 26/11/2026 | registrado na documentação | Starting with 0.8.0, you can enable iterative index scans, which will automatically scan more of the index until enough results are found (or it reaches `hnsw.max_scan_tuples` or `ivfflat.max_probes`). |
| BV-22 | Caso 1 — pgvector | texto | pgvector-readme | Introdução | GitHub, consultado em 26/11/2026 | registrado na documentação | compliance, point-in-time recovery, JOINs, and all of the other |
| BV-07 | Caso 1 — FAISS | texto | faiss-readme | Introdução | GitHub, consultado em 26/11/2026 | registrado na documentação | Faiss is a library for efficient similarity search and clustering of dense vectors. |
| BV-08 | Caso 1 — FAISS | texto | faiss-readme | Introdução | GitHub, consultado em 26/11/2026 | registrado na documentação | Some of the most useful algorithms are implemented on the GPU. |
| BV-09 | Caso 1 — FAISS | texto | faiss-escolher-indice | Then: "Flat" | Wiki do Faiss, consultada em 26/11/2026 | registrado na documentação | The only index that can guarantee exact results is the IndexFlatL2 or IndexFlatIP. |
| BV-10 | Caso 1 — FAISS | texto | faiss-escolher-indice | If not | Wiki do Faiss, consultada em 26/11/2026 | registrado na documentação | Keep in mind that all Faiss indexes are stored in RAM. |
| BV-11 | Caso 1 — FAISS | texto | faiss-escolher-indice | HNSW | Wiki do Faiss, consultada em 26/11/2026 | registrado na documentação | If you have a lots of RAM or the dataset is small, HNSW is the best option, it is a very fast and accurate index. |
| BV-21 | Caso 1 — FAISS | texto | faiss-escolher-indice | HNSW | Wiki do Faiss, consultada em 26/11/2026 | registrado na documentação | The memory usage is (_d_ * 4 + _M_ * 2 * 4) bytes per vector. |
| BV-12 | Caso 1 — Pinecone | texto | pinecone-arquitetura | Serverless infrastructure | Pinecone Docs, consultada em 26/11/2026 | registrado na documentação | Pinecone runs as a managed service on AWS, GCP, and Azure. |
| BV-13 | Caso 1 — Pinecone | texto | pinecone-arquitetura | Serverless infrastructure | Pinecone Docs, consultada em 26/11/2026 | registrado na documentação | All your data is stored in distributed |
| BV-14 | Caso 1 — Pinecone | texto | pinecone-indexacao | Namespaces | Pinecone Docs, consultada em 26/11/2026 | registrado na documentação | Within an index, records or documents are partitioned into namespaces |
| BV-15 | Caso 1 — Pinecone | texto | pinecone-multitenancy | How it works | Pinecone Docs, consultada em 26/11/2026 | registrado na documentação | With 100 tenants of 1 GB each, searching one tenant's namespace costs 1 RU. Using metadata filtering in a single 100 GB namespace would cost 100 RUs for the same search, because it scans all data regardless of filters. |
| BV-16 | Caso 1 — Pinecone | texto | pinecone-hibrida | Introdução | Pinecone Docs, consultada em 26/11/2026 | registrado na documentação | Hybrid search combines two or more retrieval signals so your results benefit from each. |
| BV-17 | Caso 1 — Weaviate | texto | weaviate-indice-vetorial | Introdução | Weaviate Docs, consultada em 26/11/2026 | registrado na documentação | a more complex index that is slower to build, but it scales well to large datasets as queries have a logarithmic time complexity. |
| BV-18 | Caso 1 — Weaviate | texto | weaviate-indice-vetorial | Dynamic index | Weaviate Docs, consultada em 26/11/2026 | registrado na documentação | The flat index is ideal for use cases with a small object count and provides lower memory overhead and good latency. |
| BV-19 | Caso 1 — Weaviate | texto | weaviate-hibrida | Hybrid search | Weaviate Docs, consultada em 26/11/2026 | registrado na documentação | Hybrid search combines the results of a vector search and a keyword (BM25F) search by fusing the two result sets. |
| BV-20 | Caso 1 — Weaviate | texto | weaviate-multi-tenancy | Multi-tenancy | Weaviate Docs, consultada em 26/11/2026 | registrado na documentação | Multi-tenancy provides data isolation. Each tenant is stored on a separate shard. Data stored in one tenant is not visible to another tenant. |

claude - pessoal, 26/11/2026.
