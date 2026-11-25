# Changelog — enxugamento da Parte II (17/11/2026)

Autoria: deepseek - painel. Escopo decidido pelo operador em 17/11/2026: opção **P2** do
`planejamento-enxugamento-parte-2-2026-11-17.md` — duas fusões por capítulo nos capítulos 6 a 11,
sem tocar no texto dos capítulos 1–5 e 12–16, nas imagens (molduras preservadas) e nas seis questões
de fechamento de cada capítulo.

## Resultado

| Item | Antes | Depois |
| --- | --- | --- |
| Páginas lógicas | 337 | **325** (−12) |
| Parte II (caps. 6–11) | 120 páginas / 108 partes | **108 páginas / 96 partes** |
| Partes por capítulo (6–11) | 18 | **16** |
| PDF A4 | 983 páginas | **963 páginas** |
| Questões de parte | 397 | **385** (12 a menos, uma por fusão) |
| Questões de fechamento | 6 por capítulo | 6 por capítulo (intactas) |
| Molduras `role="img"` | 67 | 67 (nenhuma removida) |
| Tabelas com `.rolagem` | 143 | 142 (a tabela de topologias da 6.3 foi absorvida pelo texto) |

## Fusões executadas

Cada par virou uma parte com a estrutura do §8: resumo de três linhas, analogia, corpo, uma questão
com quatro alternativas, ponto de retomada e notas de fonte. As partes fundidas ficaram entre 517 e
560 palavras (o teto P2), e a parte que sobreviveu de cada unidade foi renumerada de `c` para `b`.

| Capítulo | Fusão | Nova parte | Palavras |
| --- | --- | --- | --- |
| 6 | 6.3a + 6.3b | 6.3a Anatomia do grafo de fluxo e três topologias | 550 |
| 6 | 6.4a + 6.4b | 6.4a Subagentes, janelas limpas e revisão | 520 |
| 7 | 7.4a + 7.4b | 7.4a Injeção de prompt: tipos e onde o ataque se esconde | 558 |
| 7 | 7.1b + 7.1c | 7.1b Prompt de sistema, dados delimitados e fluxo de controle | 560 |
| 8 | 8.2b + 8.2c | 8.2b Estado limpo, efeitos verificados e preservação ao compactar | 558 |
| 8 | 8.4a + 8.4b | 8.4a Custo total e complexidade acidental | 560 |
| 9 | 9.1a + 9.1b | 9.1a Contexto, curadoria e o menor conjunto de alto sinal | 549 |
| 9 | 9.5a + 9.5b | 9.5a Compactação e limpeza de resultados de ferramentas | 555 |
| 10 | 10.1a + 10.1b | 10.1a Chamada de função: pedido, execução e modos de escolha | 560 |
| 10 | 10.4a + 10.4b | 10.4a Alto sinal, paginação e corte orientado | 517 |
| 11 | 11.4a + 11.4b | 11.4a Recuperação híbrida e reordenação em dois estágios | 539 |
| 11 | 11.6a + 11.6b | 11.6a Separar avaliação de recuperação e de resposta | 538 |

## O que mudou no texto

- As duas questões de parte de cada par viraram uma questão que cobre o conteúdo fundido; as
  explicações foram reescritas para manter coerência com o novo gabarito.
- Notas de fonte foram unidas sem perder vínculo com as fontes originais; a última parte de cada
  unidade continua com *Fontes da unidade* (97 unidades, 97 blocos).
- Na unidade 6.3, a tabela comparativa de topologias saiu e o conteúdo foi absorvido pelo parágrafo,
  para caber no teto de palavras sem perder a comparação; o bloco ilustrativo `cod-6-3a` foi mantido.
- Na unidade 9.5, a moldura `9-5b` e o exemplo de compactação opaca passaram para a parte 9.5a; na
  11.4, a moldura `11-4b` passou para a 11.4a. Os identificadores das molduras foram preservados.
- Referências cruzadas renomeadas: `6.3b` → `6.3a` (topologias), `6.4b` → `6.4a` (autopreferência),
  `8.4b` → `8.4a` (complexidade acidental), `6.3c` → `6.3b` (JSON), `6.4c` → `6.4b` (limites do
  multiagente); links de navegação e rótulos «parte i de n» reescritos nas unidades fundidas.

## Validações

1. `validar-guia.py`: **16 OK, 0 FALHA** — 325 páginas em sequência, 16 capítulos com 6 questões,
   385 regiões `aria-live`, links internos válidos, blocos de código conformes.
2. `renumerar-paginas.py`: numeração 1..325 aplicada; nenhuma seção sem marcador.
3. Reflow em 320 px (Chrome for Testing 158, `iframe` de 320 px): `clientWidth` 305 = `scrollWidth`
   305, **0 estouros** nas 325 seções.
4. PDF regerado com Chrome (`--headless=new --no-sandbox --no-pdf-header-footer --print-to-pdf`):
   **963 páginas A4**; páginas 378, 379, 416 e 564 conferidas em PNG (início e continuação de 6.3a,
   bloco de código de 7.1b e início de 10.1a).
5. Neutralidade: nenhuma ocorrência de nome interno; fontes de mais de um fornecedor preservadas.
6. `conferir-trechos.py` nos seis pacotes da Parte II: **327 trechos, 327 aprovados, 0 reprovados**.
   A pendência registrada na primeira versão deste changelog partia de um diagnóstico errado: os
   textos extraídos das sessões anteriores continuavam em `/tmp` (`grafos-textos`,
   `seguranca-textos`, `cap8-textos`, `cap9-textos`, `cap10-textos`, `cap11-textos`), com os mesmos
   nomes de chave dos pacotes. Contagem por capítulo:

   | Capítulo | Pacote | Pasta de textos | Trechos |
   | --- | --- | --- | --- |
   | 6 | `pacote-de-fontes-engenharia-de-grafos-2026-11-17.md` | `/tmp/grafos-textos` | 43 |
   | 7 | `pacote-de-fontes-capitulo-7-seguranca-e-governanca-2026-11-17.md` | `/tmp/seguranca-textos` | 52 |
   | 8 | `pacote-de-fontes-capitulo-8-autodestrutivos-e-proporcionalidade-2026-11-17.md` | `/tmp/cap8-textos` | 60 |
   | 9 | `pacote-de-fontes-capitulo-9-contexto-e-memoria-2026-11-17.md` | `/tmp/cap9-textos` | 77 |
   | 10 | `pacote-de-fontes-capitulo-10-ferramentas-e-integracoes-2026-11-17.md` | `/tmp/cap10-textos` | 53 |
   | 11 | `pacote-de-fontes-capitulo-11-busca-indexacao-e-rag-2026-11-17.md` | `/tmp/cap11-textos` | 42 |

   Comando, igual para cada linha (troque pacote e pasta):
   `python -I ferramentas/conferir-trechos.py --pacote <pacote>.md --textos /tmp/<pasta> --projeto .`
   Os pacotes não foram tocados nesta rodada (último commit deles: `fbdb6f8`), então os textos
   conferidos são os mesmos de quando cada capítulo foi escrito.

## Pendências

- Nenhuma no enxugamento. `/tmp` é apagado no desligamento: para reconferir depois, os pacotes
  trazem, na seção 1, a URL de cada fonte e o hash bruto de 16 caracteres; basta baixar de novo e
  reextrair com `extrair-texto-web.py`.
- Geração das imagens segue fora de escopo, a pedido do operador.

## Arquivos

- `guia-engenharia-llms.html` (fusões, navegação, renumeração)
- `guia-engenharia-llms.pdf` (regerado)
- `ferramentas/renumerar-paginas.py` (novo utilitário)
- `planejamento-enxugamento-parte-2-2026-11-17.md` (decisão e resultado)
- `CLAUDE.md`, `README.md` (estado e páginas)

deepseek - painel
