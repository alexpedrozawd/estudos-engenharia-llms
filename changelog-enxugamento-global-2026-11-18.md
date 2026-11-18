# Changelog — Enxugamento global e compactação do PDF (18/11/2026)

## Objetivo e escopo

Reduzir redundâncias editoriais e a extensão física do PDF A4 em `guia-engenharia-llms.html` e `guia-engenharia-llms.pdf` preservando 100% do conteúdo técnico, termos `<dfn>`, `67` molduras `data-imagem=`, `6` questões de fechamento por capítulo, citações (`arXiv:` e URLs) e pedagogia adaptada (*Em 3 linhas*, *Pense assim*, *Pergunta*, *Ponto de retomada*, `Fontes da unidade`).

Backup anterior mantido em `arquivo/antes-enxugamento-global-2026-11-18/` (fora do Git via `.gitignore`).

## Mudanças aplicadas

### 1. Compactação confortável de `@media print` (`guia-engenharia-llms.html`)

- `--reading-size: 10.5pt`, `line-height: 1.42`, `@page { size: A4; margin: 15mm 17mm 17mm; }`.
- `figure.imagem { width: 92mm; }` com `.moldura { height: 155pt; }`.
- `fieldset.questao` permite quebra entre alternativas sem gerar grandes espaços em branco; `fieldset.questao > p` mantém `break-after: avoid`, e `.alternativa` e `.gabarito-impresso` mantêm `break-inside: avoid`.
- Regra de tela (`--reading-size: 1.08rem`, `line-height: 1.7`) preservada sem alteração.
- Documentação atualizada em `requisitos-de-formato-html-do-material.md` (§9).

### 2. Fusões pontuais e padronização na Parte I (Capítulos 1–5: `106 → 89` partes)

- **Capítulo 1 (`23 → 19`):** `1.1a+b`, `1.2a+b`, `1.5a+b`, `1.6a+b`; renumerações `1.1c→b`, `1.2c→b`, `1.2d→c`, `1.5c→b`, `1.6c→b`; notas condensadas preservando todas as fontes/datas.
- **Capítulo 2 (`21 → 18`):** `2.2b+c` (com `Fontes da unidade` preservado), `2.4a+b`, `2.5a+b`; renumerações `2.4c→b`, `2.5c→b`, `2.5d→c`.
- **Capítulo 3 (`20 → 17`):** `3.1b+c`, `3.2b+c`, `3.5b+c` (com `Fontes da unidade` preservado).
- **Capítulo 4 (`21 → 18`):** `4.2a+b`, `4.3a+b` (preservando `data-imagem="4-3a"` e `cod-4-3a`), `4.4a+b`; renumerações `4.2c→b`, `4.2d→c` (`cod-4-2c`), `4.3c→b`, `4.4c→b`; notas de `4.1b`, `4.5a` e `4.6a` condensadas.
- **Capítulo 5 (`21 → 17`):** `5.1b+c` (`cod-5-1b`, `Fontes da unidade` preservado), `5.2b+c` (`Fontes da unidade` preservado), `5.3a+b`, `5.5a+b`; renumerações `5.3c→b`, `5.5c→b`; notas condensadas em `5.2a`, `5.4a`, `5.4c`, `5.4d`, `5.6a`, `5.6b`.
- **Remissões e qualidade editorial:** corrigidas 4 remissões residuais (`5.2a` para `5.1b`; Cap. 13 para `1.2c` e `1.5b`) e ajustadas 4 partes anteriores (`1.3a`, `2.1b`, `2.1c`, `2.3c`, `3.4a`) para que todas as 316 páginas tenham `<= 500` palavras antes de `Pergunta` e `<= 85` palavras em `Notas de fonte`.

### 3. Reequilíbrio de gabaritos (`A/B/C/D`)

- Reordenamento das alternativas em `p1-6a` (`d→b`), `p2-3a` (`d→c`), `p3-2a` (`c→d`), `p4-5b` (`c→a`) e `p5-6d` (`c→b`).
- Resultado em todos os Capítulos 1–5: `diff <= 1` e `max_streak = 1`. Total global nas `376` questões: `a=94, b=94, c=94, d=94`.

## Métricas antes × depois

| Indicador | Antes (`arquivo/antes-enxugamento-global-2026-11-18/`) | Depois (`18/11/2026`) | Variação |
| --- | --- | --- | --- |
| Páginas lógicas (`<section class="page">`) | `333` | `316` | `-17` (`-5,11%`) |
| Páginas no PDF A4 | `989` | `531` | `-458` (`-46,31%`) |
| Palavras (excluindo capa) | `191.993` | `174.722` | `-17.271` (`-9,00%`) |
| Questões (`fieldsets`) | `393` (`98/98/98/99`) | `376` (`94/94/94/94`) | `-17` |
| Molduras `data-imagem=` | `67` | `67` | `0` |
| Entradas `<dt>` no Glossário | `397` | `397` | `0` |
| IDs `arXiv:` únicos | `81` | `81` | `0` perdidos |
| URLs `href` externas únicas | `275` | `275` | `0` perdidos |

## Hashes SHA-256 (primeiros 16 hex)

- Antes (`arquivo/antes-enxugamento-global-2026-11-18/`):
  - `guia-engenharia-llms.html`: `6787437d3daeddba`
  - `guia-engenharia-llms.pdf`: `0688ded7c6ffb3cf`
- Depois:
  - `guia-engenharia-llms.html`: `0991acdad5c8891a`
  - `guia-engenharia-llms.pdf`: `f9812b57492537a2`

## Validações executadas após a edição final

- `python3 -I ferramentas/renumerar-paginas.py --guia guia-engenharia-llms.html --aplicar`: `316` páginas sequenciais (`1..316`).
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: `16 OK, 0 FALHA`.
- `python3 -I ferramentas/executar-trechos-de-codigo.py --guia guia-engenharia-llms.html`: `0 FALHA`, `21` ilustrativos (não executados).
- Chrome for Testing `158.0.8127.18` (headless CDP): `reflow 320 px` (`scrollWidth = 305 <= 320`, `0` estouros), `376/376` `.gabarito-impresso` conferidos e `17/17` questões das partes fundidas testadas com retorno `aria-live` (`Correto.` / `Incorreto.`).
- Geração final do PDF via Chrome `158` (`531` páginas A4, `12.502.933` bytes) e inspeção visual via `pdftoppm` em amostras de capa, sumário, tabelas, figuras e questões.

Assinatura: agy - ap
