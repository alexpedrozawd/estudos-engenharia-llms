# Changelog: Capítulo 16 — Eficiência e economia (17/11/2026)

Autoria: deepseek - painel. Quinto e último capítulo da Parte III; com ele o guia fecha os 16 capítulos.

## O que mudou
- `guia-engenharia-llms.html`: Capítulo 16 (abertura, 18 partes `16.1a`–`16.6c`, 6 questões `c16q1`–`c16q6`, 3 molduras de imagem sem geração), 7 termos novos no Glossário (368 no total), bloco *Fontes do capítulo 16* nas Referências, Sumário com as seis unidades e listas de `@media print` com `#capitulo-16` e `#questoes-capitulo-16`. Glossário na p. 336 e Referências na p. 337, como o plano previa para o fim da Parte III.
- `guia-engenharia-llms.pdf`: regerado com Chrome for Testing 158 (`--headless=new --no-sandbox --no-pdf-header-footer --print-to-pdf`), **983 páginas A4** (`594,96 × 841,92 pts`), com os 16 capítulos.
- `pacote-de-fontes-capitulo-16-eficiencia-e-economia-2026-11-17.md`: 9 fontes, 43 trechos literais, 0 reprovados.
- `planejamento-completo-estudos-engenharia-llms.md`, `CLAUDE.md` e `README.md`: Módulo 16 concluído, Parte III fechada e contagens atualizadas.

## Decisões e ressalvas
- O capítulo não fixa valores de preço: trabalha com multiplicadores (gravação de cache a 1,25× e 2×, leitura a 0,1×), pontos de equilíbrio (uma leitura para 5 minutos, duas para 1 hora) e descontos descritos (até 95% na OpenAI, 90% no cache implícito do Google, 50% no lote). Valores envelhecem em semanas; as regras, não.
- O "ponto ótimo de sessão" não tem fonte primária: é método de estimativa marcado como *proposta didática*.
- O capítulo remete a contexto e compactação (Cap. 9), escolha de modelo e esforço (14.3), contratos de ferramenta (Cap. 10) e operação (Cap. 15) sem repetir trechos.
- A página de cache de contexto do Google descreve multiplicadores que valem a partir da data indicada na própria página; o texto registra a data da consulta.

## Validação (17/11/2026)
- `conferir-trechos.py`: 43 aprovados, 0 reprovados. `validar-guia.py`: 16 OK, 0 FALHA.
- Verificação estrutural: 20 seções, nenhuma parte acima de 500 palavras (maior: 379), 143/143 tabelas com `.rolagem`, `page-nav` sequencial, níveis 2/3/1, zero termos proibidos, Glossário sem duplicatas e em ordem.
- Chrome em 320 px: `clientWidth` 305 = `scrollWidth` 305, 0 estouros em 23 seções; retorno interativo conferido.
- PDF: páginas renderizadas em PNG conferidas (capa, tabela com `rolagem` impressa, questão com gabarito, glossário).

## Hashes (16)
`guia-engenharia-llms.html` `770a1261bac3da88`; `guia-engenharia-llms.pdf` `fff8c6fd1068abd8`; pacote do Cap. 16 `40ad47918af45b80`; `planejamento-completo-estudos-engenharia-llms.md` `4eb8331bdb3b8275`; `CLAUDE.md` `45638000cc4d80bc`; `README.md` `d127b115b0f82f6a`.

Assinatura: deepseek - painel, 17/11/2026.
