# Changelog — reflow em 320 px e enxugamento do Capítulo 6 (17/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Escopo aprovado pelo operador em 17/11/2026: Opção 2 (enxugar apenas o Capítulo 6, preservando o texto dos Capítulos 1–5 intacto) + correção/validação de reflow em 320 px no guia inteiro + revisão final (`/revisar`).

## Backup
- `arquivo/antes-reflow-enxugamento-2026-11-17/`: HTML `69e6292f1b8569dd`, PDF `c52b195af4fca244`, `CLAUDE.md` `2cf69989a6003e29`.

## Mudanças (`guia-engenharia-llms.html`, `69e6292f1b8569dd` → `4c0d8ec01a595e79`)
1. **Reflow em 320 px (CSS global + 2 tabelas do Cap. 1):**
   - Envolvidas em `<div class="rolagem" role="region" ... tabindex="0">` as 2 tabelas que estavam sem `.rolagem` (`1.1a` e `1.3b`), padronizando todas as **67/67** tabelas do guia.
   - Adicionado `.page > *, .page-nav > *, figure.bloco-codigo { min-width: 0; }`, restringido `white-space: nowrap` de código em tabela para `.rolagem .tabela code`, e incluído `@media (max-width: 24rem)` ajustando `.page-nav` (`gap` e `overflow-wrap: anywhere`) e alinhamento à esquerda em `.resumo li, .page li` para evitar espaçamentos largos em colunas estreitas de 320 px.
2. **Enxugamento do Capítulo 6 (18 partes curtas + abertura):**
   - Reduzido o texto principal até `<h3>Pergunta</h3>` nas 18 partes de **6.764 → 5.064 palavras** (**-25,1%**; média de **375 → 281** palavras, faixa `216–349`).
   - Invariantes verificados: mantidos **33/33** `<dfn>`, **19/19** URLs externas, todas as analogias, tabelas, o bloco `cod-6-3a`, molduras de imagem, qualificadores `<span class="qual">`, notas de fonte e questões.
3. **PDF (`guia-engenharia-llms.pdf`, `c52b195af4fca244` → `405a2ab5fee1c9c9`):**
   - Regerado com Chrome for Testing 158: **443 páginas A4** (6.286.459 bytes).

## Validações
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (137 páginas lógicas, 289 links web, 157 questões/regiões/fieldsets).
- `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-engenharia-de-grafos-2026-11-17.md --textos /tmp/grafos-textos --projeto .`: **43 aprovados, 0 reprovados**.
- Auditoria em **320 px** (Chrome 158 via `iframe` HTTP local de `width: 320px`): `innerW: 320`, `clientWidth: 305`, `scrollWidth: 305`, **0 estouros** fora de `.rolagem`/`pre`; inspeção visual de capturas PNG em 320×700 (`capa`, `sumario`, `1.1a`, `2.2a`, `6.1a`, `6.2c`, `6.3a`, `questoes-capitulo-6`, `referencias`, `.page-nav` e `.rolagem` de `6.1a`).
- Pendente por natureza: conforto visual em aparelhos reais (Galaxy S24, Nitro 5 e APSRV 55").

Assinatura: agy - ap, 17/11/2026.
