# Changelog — pesquisa e integração de Engenharia de Grafos (17/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Decisões do operador em 17/11/2026: (1) confirmar ajustes da revisão no pacote de fontes; (2) aplicar **Opção A** (preservar Capítulos 1–5 intactos e integrar Engenharia de Grafos nos planos dos Módulos 8, 10 e 11); (3) não incluir o vídeo da Attekita Dev nas referências do guia.

## Mudanças
- **`pacote-de-fontes-engenharia-de-grafos-2026-11-17.md` (criado e revisado, hash `ab2a45074daa6d07`):**
  - Consolidados **37 trechos literais** de 15 páginas/artigos públicos primários cobrindo GraphRAG / Grafos de Conhecimento (Edge et al. `arXiv:2404.16130`, Microsoft GraphRAG, Neo4j `neo4j-graphrag-python`, LlamaIndex `PropertyGraphIndex`), Grafos de Estado e Fluxos em Agentes (LangGraph, Pydantic Graph, LlamaIndex Workflows, Anthropic `Effective context engineering` e `Multi-agent research system`) e Proporcionalidade (Anthropic `Building effective agents` + alertas de custo e complexidade das próprias ferramentas).
  - Aplicados os ajustes da revisão: corrigido `EG-12` para a descrição completa do `HybridRetriever`, adicionado `EG-37` (`HybridCypherRetriever`), acrescentados `EG-31` a `EG-36` (subagentes com janelas limpas, resumo de 1.000–2.000 tokens, multiplicador 4×/15× e falhas de coordenação), e explicitada na Seção 4 a separação entre autopreferência entre modelos (Zheng et al.) e hipótese didática de revisão na mesma janela.
- **`planejamento-completo-estudos-engenharia-llms.md` (`2931d5a1a2a516bc` → `45ee99a31303cfed`):**
  - **Módulo 8 (Contexto e memória):** incluído *isolamento de contexto em subagentes* com referência aos trechos `EG-31` e `EG-32`.
  - **Módulo 10 (Busca, indexação e RAG):** incluídos *recuperação híbrida* e *grafos de conhecimento e GraphRAG (local, global, multi-salto e custo de indexação)* com referência a `EG-01`–`EG-14` e `EG-37`.
  - **Módulo 11 (Harnesses, workflows e agentes):** incluídos *harnesses*, comparativo *loop* vs. grafo de estado e paralelismo, orçamento 4×/15×, idempotência na retomada e referências `EG-15`–`EG-30` e `EG-33`–`EG-36` (com adaptação didática sem programação para a Aurora Educação).
  - **Linha 74:** registrada a preservação dos Capítulos 1–5 e a distribuição sem sobreposição pelos Módulos 8, 10 e 11.
- **`guia-engenharia-llms.html` (`fc6e9b03ec4bf587`) e `guia-engenharia-llms.pdf` (`fff4e10a9c2f0a74`):** não alterados (conforme Opção A).

## Validações
- `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-engenharia-de-grafos-2026-11-17.md --textos /tmp/grafos-textos --projeto .`: **37 aprovados, 0 reprovados**.
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (117 páginas lógicas).
- Sem repositório Git: commit e push permanecem bloqueados até autorização do operador.

Assinatura: agy - ap, 17/11/2026.
