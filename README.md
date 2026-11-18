# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, sem exigir programação.

## Estado atual (17/11/2026)

- **Capítulos 1 a 16 concluídos e validados** (`325` páginas lógicas no HTML; o PDF, de `968` páginas A4, foi regerado em 17/11/2026 após o fechamento técnico completo).
  - **Parte I — Fundamentos e controle:** Cap. 1 (Fundamentos de IA e LLMs), Cap. 2 (Arquitetura de sistemas com LLM), Cap. 3 (Problemas e especificações), Cap. 4 (Prompts, parâmetros e respostas), Cap. 5 (Avaliação e experimentação).
  - **Parte II — Contexto, grafos, segurança e proporcionalidade:** Cap. 6 (Engenharia de grafos aplicada a LLMs), Cap. 7 (Segurança e governança), Cap. 8 (Atos autodestrutivos e proporcionalidade), Cap. 9 (Contexto e memória), Cap. 10 (Ferramentas e integrações), Cap. 11 (Busca, indexação e RAG).
  - **Parte III — Operação, desempenho e economia:** Cap. 12 (Harnesses, workflows e agentes), Cap. 13 (Inferência local), Cap. 14 (Seleção e roteamento), Cap. 15 (Integração empresarial e LLMOps), Cap. 16 (Eficiência e economia).
- **Fechamento técnico concluído em 17/11/2026:** fontes online conferidas e salvas nos `pacote-de-fontes-*.md`, gabaritos das 385 questões equilibrados sem viés de comprimento nos capítulos ajustados, `reflow` em `320 px` (`0` estouros), auditoria `axe-core` (`0` violações) e `Assistir:` padronizado em todas as unidades; ver `changelog-fechamento-tecnico-2026-11-17.md`.
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
