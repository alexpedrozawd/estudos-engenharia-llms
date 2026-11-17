# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, sem exigir programação.

## Estado atual (17/11/2026)

- **Capítulos 1 a 8 concluídos e validados** (`177` páginas lógicas no HTML; `561` páginas A4 no PDF).
  - **Parte I — Fundamentos e controle:** Cap. 1 (Fundamentos de IA e LLMs), Cap. 2 (Arquitetura de sistemas com LLM), Cap. 3 (Problemas e especificações), Cap. 4 (Prompts, parâmetros e respostas), Cap. 5 (Avaliação e experimentação).
  - **Parte II — Contexto, grafos, segurança e proporcionalidade:** Cap. 6 (Engenharia de grafos aplicada a LLMs), Cap. 7 (Segurança e governança), Cap. 8 (Atos autodestrutivos e proporcionalidade).
- **Próximo passo:** Capítulo 9 — Contexto e memória (conforme `planejamento-completo-estudos-engenharia-llms.md`).

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões com retorno imediato em `aria-live`, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 gerada via Chrome for Testing 158.
- `planejamento-completo-estudos-engenharia-llms.md` — plano curricular de 16 módulos e referências públicas.
- `pacote-de-fontes-*.md` — trechos literais conferidos de fontes públicas primárias.
- `ferramentas/` — `validar-guia.py`, `conferir-trechos.py` e `extrair-texto-web.py` (Python 3 padrão).
- `CLAUDE.md` e `handoff-pos-capitulo-8-2026-11-17.md` — instruções de retomada e protocolo de economia de tokens (`protocolo-de-economia-de-tokens-entre-sessoes.md`).

## Validação rápida

```bash
python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html
```
