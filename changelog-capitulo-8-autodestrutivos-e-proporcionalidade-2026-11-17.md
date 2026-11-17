# Changelog — criação do Capítulo 8 (Atos autodestrutivos e proporcionalidade) e publicação Git (17/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Decisão confirmada pelo operador em 17/11/2026: avançar para a escrita do Capítulo 8 com base no pacote de fontes conferido e criar repositório público em `alexpedrozawd`.

## Backup
- `arquivo/antes-capitulo-8-autodestrutivos-2026-11-17/`: HTML `bd6d6879fdad526a`, PDF `f784970f98cdc891`, `planejamento-completo-estudos-engenharia-llms.md` `9caec488d3ffa872`, `CLAUDE.md` `2dcf3b5d13859d6d`.

## Mudanças
- **`pacote-de-fontes-capitulo-8-autodestrutivos-e-proporcionalidade-2026-11-17.md` (`21dabff79e1fad03`):**
  - Baixadas e conferidas **28 fontes públicas primárias**: Denison et al. (`arXiv:2406.10162`), MacDiarmid et al. (`arXiv:2511.18397`), Ovadia et al. (`arXiv:2312.05934`), Liu et al. (`arXiv:2307.03172`), Chroma (*Context Rot*, 14/07/2025), NIST AI 100-1 e AI 600-1, OWASP Top 10 for LLM 2025 v2.0 (`LLM06`, `LLM10`), Google SRE Book (caps. 8, 9, 13, 14, 21, 22), Anthropic (*Building effective agents*, *Effective context engineering*, *Effective harnesses*, *Writing tools for agents*, *Code execution with MCP*, *Best Practices for Claude Code*), OpenAI (*Errors and recovery*, *Guardrails and human review*, *Spend limits*, *Cost optimization*, *Optimizing LLM Accuracy*) e Google Cloud (*Introduction to tuning*, *Grounding overview*).
  - Conferência literal via `conferir-trechos.py`: **60 aprovados, 0 reprovados** (`AP-01`–`AP-60`).
- **`guia-engenharia-llms.html` (`bd6d6879fdad526a` → `c591f425aeb2c8f7`):**
  - Atualizado o Sumário (Capítulo 8 com links para `8.1`–`8.6` e `Questões do capítulo 8`) e regras `@media print` para `#capitulo-8` e `#questoes-capitulo-8`.
  - Atualizado o link seguinte de `#questoes-capitulo-7` para `#capitulo-8`.
  - Adicionado o **Capítulo 8 — Atos autodestrutivos e proporcionalidade** (**20 páginas lógicas**, páginas **156 a 175**): abertura (`#capitulo-8`), 18 partes curtas (`8.1a`–`8.6c`, **5.479 palavras** até `Pergunta`, média **304,4**, faixa **251–384** palavras; 5 tabelas com `.rolagem`; bloco ilustrativo `cod-8-6a` não executado; 5 molduras `role="img"`) e 6 questões de fechamento (`c8q1`–`c8q6`: 2 fáceis, 3 médias, 1 difícil).
  - Atualizados Glossário (página **176**, 23 novos termos em ordem alfabética + ampliação de `Compactação`, `Context rot`, `Disjuntor`, `Fine-tuning prematuro` e `Prompt patching`) e Referências (página **177**, seção do Cap. 8 com todas as fontes conferidas em 17/11/2026).
- **`guia-engenharia-llms.pdf` (`f784970f98cdc891` → `5db03d0f1e926efe`):**
  - Regerado com Chrome for Testing 158: **561 páginas A4** (8.059.534 bytes). Conferidas visualmente 7 páginas renderizadas (`4, 467, 474, 509, 518, 523, 556`).
- **`planejamento-completo-estudos-engenharia-llms.md` (`9caec488d3ffa872` → `c7f46755bacba41f`):**
  - Marcado o Módulo 8 como concluído em 17/11/2026 com referência ao pacote de 60 trechos conferidos (substituindo a dependência exclusiva da diretriz interna).
- **Repositório Git e GitHub público:**
  - Criados `.gitignore` (excluindo `arquivo/`, `contexto-de-estudo-*.md` e `HANDOFF-formacao-engenharia-llms-para-claude-2026-10-13.md`) e `README.md`, movido `handoff-pos-capitulo-7-2026-11-17.md` para `arquivo/` e criado o repositório público `https://github.com/alexpedrozawd/estudos-engenharia-llms`.

## Validações
- `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-8-autodestrutivos-e-proporcionalidade-2026-11-17.md --textos /tmp/cap8-textos --projeto .`: **60 aprovados, 0 reprovados**.
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (177 páginas lógicas, 375 links web, 205 questões/regiões/fieldsets).
- Verificação estrutural por script: 0 erros de `page-nav` nas 177 páginas, 77/77 tabelas com `.rolagem`, 0 termos proibidos.
- Auditoria em **320 px** (Chrome 158 via `iframe` HTTP local de `320px`): `innerW: 320`, `clientWidth: 305`, `scrollWidth: 305`, **0 estouros** fora de `.rolagem`/`pre` nas 22 seções verificadas (Cap. 8, Glossário e Referências) + teste interativo de retorno em `c8q2`.
- Pendente por natureza: leitura nos aparelhos físicos reais (Galaxy S24, Nitro 5 e APSRV 55").

Assinatura: agy - ap, 17/11/2026.