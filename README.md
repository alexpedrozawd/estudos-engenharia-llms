# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, sem exigir programação.

## Estado atual (18/11/2026)

- **Capítulos 1 a 16 concluídos, revisados e expandidos (Grupo A):** `333` páginas lógicas no HTML, `393` questões, `397` entradas `<dt>` no Glossário e `682` links externos; o PDF, de `989` páginas A4, foi regerado em 18/11/2026.
  - **Parte I — Fundamentos e controle:** Cap. 1 (Fundamentos de IA e LLMs), Cap. 2 (Arquitetura de sistemas com LLM), Cap. 3 (Problemas e especificações), Cap. 4 (Prompts, parâmetros e respostas), Cap. 5 (Avaliação e experimentação).
  - **Parte II — Contexto, grafos, segurança e proporcionalidade:** Cap. 6 (Engenharia de grafos aplicada a LLMs), Cap. 7 (Segurança e governança), Cap. 8 (Atos autodestrutivos e proporcionalidade), Cap. 9 (Contexto e memória), Cap. 10 (Ferramentas e integrações), Cap. 11 (Busca, indexação e RAG).
  - **Parte III — Operação, desempenho e economia:** Cap. 12 (Harnesses, workflows e agentes), Cap. 13 (Inferência local), Cap. 14 (Seleção e roteamento), Cap. 15 (Integração empresarial e LLMOps), Cap. 16 (Eficiência e economia).
- **Fechamento técnico (17/11/2026), revisão geral e expansão do Grupo A (18/11/2026):** fontes conferidas nos `pacote-de-fontes-*.md`, gabaritos equilibrados nas questões de fechamento e nos 8 novos blocos (`2.3d`, `4.5d`, `5.6e`, `10.6d`, `11.3d`, `11.4c`, `13.6d`, `15.6d`), `Assistir:` padronizado nas unidades, revisão geral técnica aplicada e validações concluídas (`validar-guia.py` com `16 OK, 0 FALHA`, `reflow` em `320 px` com `0` estouros no documento e nas 8 partes novas, e `axe-core` com `45 passes` e `0 violations`). Ver `changelog-fechamento-tecnico-2026-11-17.md`, `changelog-revisao-geral-2026-11-18.md` e `changelog-expansao-grupo-a-2026-11-18.md`.
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
