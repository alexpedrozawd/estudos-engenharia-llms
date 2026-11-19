# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, sem exigir programação.

## Estado atual (19/11/2026)

- **Capítulos 1 a 16 concluídos, revisados e fechados:** `316` partes (`175.906` palavras em partes; HTML `sha256` `19a020013721c5a5`), `376` questões (`94/94/94/94`), `141` tabelas (`141` com `.rolagem`), `402` termos `<dt>` no Glossário (`395` `<dfn>`), `67` molduras `data-imagem=` e `722` links externos (`275` URLs únicas); o PDF, de `534` páginas A4 (`sha256` `10ff8c03dd8dfe83`), foi regerado em 18/11/2026 após a conferência dos itens `[Não verificado]` e fechamento das pendências finais.
  - **Parte I — Fundamentos e controle:** Cap. 1 (`19` partes), Cap. 2 (`18`), Cap. 3 (`17`), Cap. 4 (`18`), Cap. 5 (`17`).
  - **Parte II — Contexto, grafos, segurança e proporcionalidade:** Cap. 6 (Engenharia de grafos aplicada a LLMs), Cap. 7 (Segurança e governança), Cap. 8 (Atos autodestrutivos e proporcionalidade), Cap. 9 (Contexto e memória), Cap. 10 (Ferramentas e integrações), Cap. 11 (Busca, indexação e RAG).
  - **Parte III — Operação, desempenho e economia:** Cap. 12 (Harnesses, workflows e agentes), Cap. 13 (Inferência local), Cap. 14 (Seleção e roteamento), Cap. 15 (Integração empresarial e LLMOps), Cap. 16 (Eficiência e economia).
- **Conferência, acessibilidade e ferramentas sem LLM (18–19/11/2026):** fontes conferidas nos `pacote-de-fontes-*.md`, gabaritos equilibrados (`94` por letra), `Assistir:` padronizado nas unidades, validações aprovadas (`guia.py fechar` com `0` falhas, `executar-trechos-de-codigo.py` com `0` falhas, `auditar-guia-navegador.mjs` em `320 px` com `0` estouros, `376/376` questões com `aria-live` e `axe-core` com `0` violações), e camada determinística de economia de tokens criada em `ferramentas/guia.py` e `ferramentas/fontes.py` (com suíte de testes sem warnings). Ver `changelog-conferencia-nao-verificado-2026-11-18.md` e `changelog-ferramentas-de-economia-de-tokens-2026-11-19.md`.
- **Próximas etapas e pendências:** ver [roadmap.md](roadmap.md) e [plano-de-lacunas-para-nota-10-2026-11-19.md](plano-de-lacunas-para-nota-10-2026-11-19.md) (decisões do operador sobre L1–L8, revisão externa, piloto com leitores, validação manual nos três aparelhos, leitor de tela e papel A4, e geração das 67 imagens em aquarela por último).

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões com retorno imediato em `aria-live`, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 gerada via Chromium headless (`534` páginas).
- `planejamento-completo-estudos-engenharia-llms.md` — plano curricular de 16 módulos e referências públicas.
- `plano-de-lacunas-para-nota-10-2026-11-19.md` — proposta de evolução (lacunas L1–L8).
- `pacote-de-fontes-*.md` — trechos literais conferidos de fontes públicas primárias.
- `ferramentas/` — `guia.py`, `fontes.py`, `validar-guia.py`, `renumerar-paginas.py`, `executar-trechos-de-codigo.py`, `conferir-trechos.py`, `extrair-texto-web.py`, `auditar-guia-navegador.mjs` e testes (`testar-ferramentas.py`, `testar-fontes.py`, `testar-llm-local.py`).
- `CLAUDE.md` — estado atual, instruções de retomada e protocolo de economia de tokens (`protocolo-de-economia-de-tokens-entre-sessoes.md`).

## Validação rápida

```bash
python3 -I ferramentas/guia.py fechar
```
