# Changelog — conclusão da Parte II (Capítulos 9, 10 e 11) (17/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Escopo aprovado pelo operador em 17/11/2026: concluir o Capítulo 9 e todo o restante da Parte II (Capítulos 10 e 11).

## Backup
- `arquivo/antes-parte-2-caps-9-11-2026-11-17/`: HTML `c591f425aeb2c8f7`, PDF `5db03d0f1e926efe`, `planejamento-completo-estudos-engenharia-llms.md` `c7f46755bacba41f`, `CLAUDE.md` `1ba2bc15e39505d7`.

## Mudanças
- **Pacotes de fontes públicas conferidos (`conferir-trechos.py`):**
  - `pacote-de-fontes-capitulo-9-contexto-e-memoria-2026-11-17.md` (`521e6aa801a53963`): **77 trechos aprovados, 0 reprovados** (`CM-01`–`CM-77`, 14 fontes públicas: Anthropic, OpenAI e Google Cloud + ilustração local de 23/10/2026 rotulada como amostra pequena).
  - `pacote-de-fontes-capitulo-10-ferramentas-e-integracoes-2026-11-17.md` (`9afa157a2e21c70e`): **53 trechos aprovados, 0 reprovados** (`FI-01`–`FI-53`, 16 fontes públicas: especificação MCP `2026-07-28`, JSON Schema, Anthropic, OpenAI e Google Cloud).
  - `pacote-de-fontes-capitulo-11-busca-indexacao-e-rag-2026-11-17.md` (`fafd6cbf02b3896d`): **42 trechos aprovados, 0 reprovados** (`BR-01`–`BR-42`, 15 fontes públicas: `arXiv:2005.11401`, `1908.10084`, `1901.04085`, `2210.07316`, `2309.15217`, Anthropic, OpenAI, Google Cloud, `ripgrep` e `Tree-sitter`).
- **`guia-engenharia-llms.html` (`c591f425aeb2c8f7` → `718ddeec0ecb86d8`):**
  - Atualizado o Sumário (Capítulos 9, 10 e 11 com links para todas as unidades e páginas de questões), as regras `@media print` (`#capitulo-9..11` e `#questoes-capitulo-9..11`) e o encadeamento `page-nav` a partir de `#questoes-capitulo-8`.
  - **Capítulo 9 — Contexto e memória** (páginas **176 a 195**, 20 páginas lógicas): abertura, 18 partes curtas (`9.1a`–`9.6c`, **5.208 palavras** até `Pergunta`, média **289,3**, faixa **237–433**), 5 tabelas com `.rolagem`, bloco `cod-9-4b` ilustrativo, 4 molduras `role="img"` e 6 questões (`c9q1`–`c9q6`).
  - **Capítulo 10 — Ferramentas e integrações** (páginas **196 a 215**, 20 páginas lógicas): abertura, 18 partes curtas (`10.1a`–`10.6c`, **4.865 palavras** até `Pergunta`, média **270,3**, faixa **236–327**), 2 tabelas com `.rolagem`, bloco `cod-10-2a` ilustrativo, 4 molduras `role="img"` e 6 questões (`c10q1`–`c10q6`).
  - **Capítulo 11 — Busca, indexação e RAG** (páginas **216 a 235**, 20 páginas lógicas): abertura, 18 partes curtas (`11.1a`–`11.6c`, **4.719 palavras** até `Pergunta`, média **262,2**, faixa **229–300**), 4 tabelas com `.rolagem`, bloco `cod-11-2c` ilustrativo, 4 molduras `role="img"` e 6 questões (`c11q1`–`c11q6`).
  - Atualizados **Glossário** (página **236**, 312 termos em ordem alfabética com ampliação de termos compartilhados e correção da referência de `MCP` para o capítulo 10) e **Referências** (página **237**, seções dos Capítulos 9, 10 e 11).
- **`guia-engenharia-llms.pdf` (`5db03d0f1e926efe` → `3893b8e1553e915f`):**
  - Regerado com Chrome 158: **720 páginas A4** (10.548.929 bytes). Conferidas visualmente 7 páginas renderizadas (`4, 5, 523, 580, 586, 650, 717`).
- **`planejamento-completo-estudos-engenharia-llms.md` (`c7f46755bacba41f` → `53dc380144e0f69b`):**
  - Marcados os Módulos 9, 10 e 11 como concluídos em 17/11/2026 com referência aos pacotes de fontes conferidos.
- **Handoff e ponteiros:** movido `handoff-pos-capitulo-8-2026-11-17.md` para `arquivo/` e criado `handoff-pos-capitulo-11-2026-11-17.md`; atualizado `CLAUDE.md`.

## Validações
- `conferir-trechos.py`: Cap. 9 (**77 aprovados, 0 reprovados**), Cap. 10 (**53 aprovados, 0 reprovados**), Cap. 11 (**42 aprovados, 0 reprovados**).
- `validar-guia.py`: **16 OK, 0 FALHA** (237 páginas lógicas, 464 links web, 277 questões/regiões/fieldsets).
- Verificação estrutural por script: **88/88** tabelas com `.rolagem`, **0** termos proibidos, **0** duplicatas no Glossário, `page-nav` sequencial em todas as seções de conteúdo.
- Auditoria em **320 px** (Chrome 158 via `iframe` HTTP local `320px`): `innerW: 320`, `clientWidth: 305`, `scrollWidth: 305`, **0 estouros** fora de `.rolagem`/`pre` nas **63 seções** verificadas (Sumário, Caps. 9–11, Glossário e Referências) + teste interativo de retorno em `c9q3`, `c10q4` e `c11q5`.
- Pendente por natureza: leitura nos aparelhos físicos reais (Galaxy S24, Nitro 5 e APSRV 55").

Assinatura: agy - ap, 17/11/2026.
