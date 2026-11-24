# Lab 07 — Busca, Indexação e RAG Híbrido

Mini pipeline de RAG sobre as políticas fictícias da Aurora Educação: fatiamento
com sobreposição, BM25 para termos exatos, *embedding* local por hashing de
palavras (didático, sem modelo), fusão RRF com `k = 60`, métricas de
recuperação (`recall@K`, MRR, NDCG@K) e checagem de fidelidade das citações.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_07_rag_hibrido
```

Para usar *embeddings* reais, troque `vetor()` por um modelo local (por exemplo,
via Ollama) e mantenha os testes de métricas como regressão.
