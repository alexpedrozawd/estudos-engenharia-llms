# Changelog: Capítulo 12 — Harnesses, workflows e agentes (17/11/2026)

Autoria: claude - pessoal (Sonnet 5.5 High, painel). Abre a Parte III.

## O que mudou
- `guia-engenharia-llms.html`: Capítulo 12 (abertura, 18 partes `12.1a`–`12.6c`, 6 questões `c12q1`–`c12q6`, 5 molduras de imagem sem geração), 12 termos novos no Glossário (324 no total), bloco *Fontes do capítulo 12* nas Referências, Sumário com as seis unidades e listas de `@media print` com `#capitulo-12`, `#questoes-capitulo-12` e os `> h2` correspondentes.
- `pacote-de-fontes-capitulo-12-harnesses-workflows-e-agentes-2026-11-17.md`: 16 fontes (Anthropic, OpenAI, Google ADK), 99 trechos literais, 0 reprovados no `conferir-trechos.py`. Trechos já citados nos Capítulos 6, 8 e 9 foram substituídos para não repetir.
- `planejamento-completo-estudos-engenharia-llms.md` e `CLAUDE.md`: Módulo 12 concluído, contagens e numeração atualizadas.

## Decisão de numeração
O pedido previa o Cap. 12 nas páginas 238–257 e Glossário/Referências em 338/339, mas a última página do Cap. 11 é a 235; começar em 238 deixa um buraco e o `validar-guia.py` exige sequência. Adotado: Cap. 12 em 236–255, Glossário 256, Referências 257; ao fim da Parte III, Glossário 336 e Referências 337.

## Validação (17/11/2026)
- `validar-guia.py`: 16 OK, 0 FALHA (301 questões, 498 links web).
- Verificação estrutural: 20 seções, nenhuma parte acima de 500 palavras (maior: 383), 96/96 tabelas com `.rolagem`, prefixos de `data-explicacao`, `page-nav` sequencial, níveis 2 fáceis/3 médias/1 difícil, zero termos proibidos, Glossário sem duplicatas e em ordem.
- Chrome em 320 px: `clientWidth` 305 = `scrollWidth` 305, 0 estouros em 23 seções; retorno interativo conferido em `c12q1`, `c12q6`, `p12-1a` e `p12-3c`.

## Observações
- A documentação consultada (OpenAI Agents SDK, Anthropic Agent SDK, Google ADK) muda sem aviso; valem como estado de 17/11/2026. A página *Building effective agents* traz nota de que parte das ferramentas descritas mudou desde dezembro de 2024.
- Achado independente (não corrigido): as listas de `@media print` não incluem `#capitulo-5` nem `#questoes-capitulo-5`, então o Cap. 5 não força quebra de página na impressão.
- PDF não regerado (720 páginas A4, defasado); regeração prevista ao fim da Parte III.

## Hashes (16)
`guia-engenharia-llms.html` `eff831d097dcc553`; pacote do Cap. 12 `8bc3d318f95ddf39`; `planejamento-completo-estudos-engenharia-llms.md` `5b81872774d0df27`.

Assinatura: claude - pessoal, 17/11/2026.
