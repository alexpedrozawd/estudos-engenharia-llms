# Changelog — criação do Capítulo 7 (Segurança e governança) (17/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Decisão confirmada pelo operador em 17/11/2026: aprovação do pacote de fontes públicas primárias (`pacote-de-fontes-capitulo-7-seguranca-e-governanca-2026-11-17.md`) e do mapa de 6 unidades (18 partes curtas) + 6 questões de fechamento.

## Backup
- `arquivo/antes-capitulo-7-seguranca-2026-11-17/`: HTML `4c0d8ec01a595e79`, PDF `405a2ab5fee1c9c9`, `planejamento-completo-estudos-engenharia-llms.md` `f0406e8a6b6a3c29`, `CLAUDE.md` `618ac007a36068cb`.

## Mudanças
- **`pacote-de-fontes-capitulo-7-seguranca-e-governanca-2026-11-17.md` (`094777e203be5a9e`):**
  - Baixadas e conferidas **20 fontes públicas primárias**: OWASP Top 10 for LLM Applications 2025 v2.0 (`LLM00`, `LLM01`, `LLM02`, `LLM05`, `LLM06`, `LLM07`, `LLM08`, `LLM10` via repositório oficial no GitHub), NIST AI 600-1 (26/07/2024), Lei nº 13.709/2018 (LGPD atualizada no Portal da Câmara dos Deputados), MCP *Security Best Practices*, Wallace et al. (`arXiv:2404.13208`), Debenedetti et al. (`arXiv:2503.18813`), Anthropic (*sandboxing*, *mitigate jailbreaks*, *API and data retention*), OpenAI (*safety best practices*, *your data*) e Google Cloud (*Model Armor*, *zero data retention*).
  - Conferência literal via `conferir-trechos.py`: **52 aprovados, 0 reprovados** (`SG-01`–`SG-52`).
- **`guia-engenharia-llms.html` (`4c0d8ec01a595e79` → `bd6d6879fdad526a`):**
  - Atualizado o Sumário (Capítulo 7 com links para 7.1–7.6 e Questões do capítulo 7) e regras `@media print` para `#capitulo-7` e `#questoes-capitulo-7`.
  - Atualizado o link seguinte de `#questoes-capitulo-6` para `#capitulo-7`.
  - Adicionado o **Capítulo 7 — Segurança e governança** (**20 páginas lógicas**, páginas **136 a 155**): abertura (`#capitulo-7`), 18 partes curtas (`7.1a`–`7.6c`, **5.300 palavras** até `Pergunta`, média **294,4**, faixa **261–374** palavras; 5 tabelas com `.rolagem`; bloco ilustrativo `cod-7-1c` não executado; 5 molduras `role="img"` + `aria-label`) e 6 questões de fechamento (`c7q1`–`c7q6`: 2 fáceis, 3 médias, 1 difícil).
  - Atualizados Glossário (página **156**, 24 novos termos em ordem alfabética + ampliação de `Prompt de sistema (4.3, 7.1)`) e Referências (página **157**, seção do Cap. 7 com todas as fontes conferidas em 17/11/2026).
- **`guia-engenharia-llms.pdf` (`405a2ab5fee1c9c9` → `f784970f98cdc891`):**
  - Regerado com Chrome for Testing 158: **499 páginas A4** (7.146.684 bytes). Conferidas visualmente 7 páginas renderizadas (`4, 413, 419, 420, 454, 455, 460`).
- **`planejamento-completo-estudos-engenharia-llms.md`:**
  - Marcado o Módulo 7 como concluído em 17/11/2026 com a referência ao pacote de 52 trechos conferidos.

## Validações
- `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-7-seguranca-e-governanca-2026-11-17.md --textos /tmp/seguranca-textos --projeto .`: **52 aprovados, 0 reprovados**.
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (157 páginas lógicas, 323 links web, 181 questões/regiões/fieldsets).
- Verificação estrutural por script: 0 erros de `page-nav` nas 157 páginas, 72/72 tabelas com `.rolagem`, 0 termos proibidos.
- Auditoria em **320 px** (Chrome 158 via `iframe` HTTP local de `320px`): `innerW: 320`, `clientWidth: 305`, `scrollWidth: 305`, **0 estouros** fora de `.rolagem`/`pre` no Capítulo 7, Glossário e Referências + teste interativo de retorno em `c7q2`.
- Pendente por natureza: leitura nos aparelhos físicos reais (Galaxy S24, Nitro 5 e APSRV 55").

Assinatura: agy - ap, 17/11/2026.
