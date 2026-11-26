# Changelog — Vistoria e correção de quebras no PDF (26/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High). Alterações apenas no CSS de [guia-engenharia-llms.html](../../guia-engenharia-llms.html), regeração do [guia-engenharia-llms.pdf](../../guia-engenharia-llms.pdf) e documentação correspondente.

## Vistoria do PDF anterior (`736` páginas, sha16 `8431be316ec3b881`)

A inspeção do layout extraído via `pdftohtml -xml` e das páginas renderizadas via `pdftoppm` identificou cinco causas concretas de quebras indevidas:

1. **Questões partidas entre páginas (`146` de `502`):** `fieldset.questao` não possuía `break-inside: avoid`, deixando caixas cortadas ao meio e gabaritos órfãos. Além disso, no Chromium, `<fieldset>` com `<legend>` e regras conflitantes de `break-inside`/`break-after` nos filhos internos (`> p`, `.alternativa`, `.gabarito-impresso`) ainda fragmentava `23` questões mesmo com `break-inside: avoid` no pai.
2. **Quebras de linha dentro dos quadros `.resumo` (`5` quadros afetados):** `.resumo strong { display: block; }` atingia qualquer `<strong>` dentro dos itens `<li>`, quebrando a linha antes e depois de termos em negrito (ex.: `atributos rígidos`, `DEVE`, `DEVERIA`, `PODE`, `TTFT`, `TPOT`).
3. **Termos do Glossário órfãos (`23` ocorrências):** `dt` tinha `break-inside: avoid`, mas não `break-after: avoid`, ficando sozinho no fim da página separado da definição `<dd>`.
4. **Capítulos partidos no Sumário (`p. 2`–`6`):** `.contents > li` e `.chapter-name` não bloqueavam quebra, deixando título de capítulo órfão no fim da página ou o bloco do capítulo dividido.
5. **Quebras em código, rótulos de saída e tabelas com `<code>`:** `pre.codigo` e `pre.saida` usavam `overflow-wrap: anywhere` com `font-size: .72em` (cortando identificadores e chaves no meio da palavra); `.rolagem .tabela code` mantinha `white-space: nowrap` no `@media print` (esticando colunas com código longo e espremendo colunas vizinhas); faltava `break-after: avoid` em `.rotulo-saida` e `break-inside: avoid` em `ol.fluxo`.

## Correções aplicadas

- `guia-engenharia-llms.html`:
  - `.resumo strong` → `.resumo > strong` (restringe `display: block` apenas ao título do quadro, valendo em tela e impressão).
  - `@media print`:
    - `fieldset.questao`: `display: flex; flex-direction: column; break-inside: avoid; page-break-inside: avoid;`, removendo `break-inside`/`break-after` conflitantes de `legend`, `fieldset.questao > p`, `.alternativa` e `.gabarito-impresso`.
    - `break-after: avoid` adicionado a `dt`, `.chapter-name` e `.rotulo-saida`.
    - `break-inside: avoid` adicionado a `.contents > li` e `.fluxo`.
    - `.page` e `.page code` com `overflow-wrap: break-word` (preservando `.fontes, .fontes code { overflow-wrap: anywhere; }` para URLs nas notas e referências).
    - `.rolagem .tabela code { white-space: normal; overflow-wrap: break-word; }` para liberar quebra limpa dentro de células com código.
    - `pre.codigo, pre.saida` ajustados para `overflow-wrap: break-word; font-size: .68em; padding: .55em .75em;`.
- `guia-engenharia-llms.pdf`: regerado via `python3 -I ferramentas/guia.py pdf --substituir --motivo correcao-quebras-pdf` (`749` páginas, sha16 `ad7931f935356117`; cópia anterior preservada em `arquivo/antes-correcao-quebras-pdf-2026-11-26/`).
- Documentação atualizada: [CLAUDE.md](../../CLAUDE.md), [README.md](../../README.md) e [requisitos-de-formato-html-do-material.md](../../requisitos-de-formato-html-do-material.md) (§9).

## Validação após a última edição

- `python3 -I ferramentas/testar-ferramentas.py`: `24` testes OK (`64,89 s`).
- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`renumerar-paginas.py` OK, `validar-guia.py` `18 OK / 0 FALHA`, `executar-trechos-de-codigo.py` `28 OK / 0 FALHA`, `426` partes, `502` questões, `168` tabelas com `.rolagem`, `552` termos no glossário, HTML sha16 `4620c46dd4e721c0`, PDF `749` páginas sha16 `ad7931f935356117`).
- Auditoria do layout do novo PDF (`pdftohtml -xml` + inspeção visual com `pdftoppm`): `0` questões partidas entre páginas (de `146`), `0` `<dt>` órfãos no glossário (de `23`), `0` capítulos partidos no sumário, `0` quebras por `<strong>` em `.resumo` (de `5`), `0` tabelas divididas e `0` páginas em branco ou estouros horizontais.
- Nota: `ferramentas/auditar-guia-navegador.mjs` (reflow em `320 px` e `axe-core`) não foi executado por ausência dos pacotes Node `playwright` e `axe-core` instalados no ambiente; a alteração em tela restringiu-se a `.resumo > strong`.
