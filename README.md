# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, sem exigir programação.

## Estado atual (18/11/2026)

- **Capítulos 1 a 16 concluídos, revisados, expandidos (Grupo A) e enxugados:** `316` páginas lógicas no HTML (`174.722` palavras excl. capa), `376` questões (`94/94/94/94`), `397` entradas `<dt>` no Glossário, `67` molduras `data-imagem=` e `682` links externos (`275` URLs únicas, `81` IDs `arXiv:`); o PDF, de `531` páginas A4 (`989 → 531` após compactação de `@media print` e fusões pontuais da Parte I), foi regerado em 18/11/2026.
  - **Parte I — Fundamentos e controle:** Cap. 1 (`19` partes), Cap. 2 (`18`), Cap. 3 (`17`), Cap. 4 (`18`), Cap. 5 (`17`).
  - **Parte II — Contexto, grafos, segurança e proporcionalidade:** Cap. 6 (Engenharia de grafos aplicada a LLMs), Cap. 7 (Segurança e governança), Cap. 8 (Atos autodestrutivos e proporcionalidade), Cap. 9 (Contexto e memória), Cap. 10 (Ferramentas e integrações), Cap. 11 (Busca, indexação e RAG).
  - **Parte III — Operação, desempenho e economia:** Cap. 12 (Harnesses, workflows e agentes), Cap. 13 (Inferência local), Cap. 14 (Seleção e roteamento), Cap. 15 (Integração empresarial e LLMOps), Cap. 16 (Eficiência e economia).
- **Fechamento técnico (17/11/2026), revisão geral, expansão do Grupo A e enxugamento global (18/11/2026):** fontes conferidas nos `pacote-de-fontes-*.md`, gabaritos equilibrados (`94` por letra), `Assistir:` padronizado nas unidades, enxugamento da Parte I (`106 → 89` partes) mantendo `0` perdas de `<dfn>`, URLs ou `arXiv:`, e validações concluídas (`validar-guia.py` `16 OK, 0 FALHA`, `executar-trechos-de-codigo.py` `0 FALHA`, Chrome `158` `reflow 320 px` com `0` estouros e `17/17` questões fundidas com `aria-live`). Ver `changelog-fechamento-tecnico-2026-11-17.md`, `changelog-revisao-geral-2026-11-18.md`, `changelog-expansao-grupo-a-2026-11-18.md` e `changelog-enxugamento-global-2026-11-18.md`.
- **Pendências finais:** ver [roadmap.md](roadmap.md) (geração das 67 imagens em aquarela e validação manual nos três aparelhos reais, leitor de tela e impressão física).

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões com retorno imediato em `aria-live`, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 gerada via Chrome for Testing 158.
- `planejamento-completo-estudos-engenharia-llms.md` — plano curricular de 16 módulos e referências públicas.
- `pacote-de-fontes-*.md` — trechos literais conferidos de fontes públicas primárias.
- `ferramentas/` — `validar-guia.py`, `conferir-trechos.py`, `extrair-texto-web.py` e `renumerar-paginas.py` (Python 3 padrão).
- `CLAUDE.md` — estado atual, instruções de retomada e protocolo de economia de tokens (`protocolo-de-economia-de-tokens-entre-sessoes.md`).

## Validação rápida

```bash
python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html
```
