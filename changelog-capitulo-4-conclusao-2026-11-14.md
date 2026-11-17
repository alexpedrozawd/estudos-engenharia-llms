# Changelog: capítulo 4 concluído (14/11/2026)

Autoria: claude - pessoal (Sonnet 5.5 High, painel). Backup: `arquivo/antes-capitulo-4-conclusao-2026-11-14/` (cópia feita antes de editar; hashes iguais aos de entrada).

## Revisão do trabalho do DeepSeek (somente leitura, antes de corrigir)

| Achado | Prova | Ajuste |
|---|---|---|
| Gabarito das perguntas 4.1a, 4.1b e 4.1c sempre “A” | leitura dos `data-correta` | alternativas reordenadas (4.1b → C, 4.1c → D) |
| Bloco do prompt v1 (4.1c) com 15 linhas; o plano limita a 12 | contagem de linhas | fonte e pergunta em uma linha cada (10 linhas) |
| Nota “Prompt engineering” (OpenAI) na 4.1c sem afirmação no texto | leitura | movida para a 4.2c, onde sustenta o texto |
| Abertura citava “referência da Messages API”; as fontes usadas são outras páginas | pacote de fontes | texto ajustado |
| Handoff dizia “11 fontes”; o pacote tem 12 fontes (3 artigos, 7 páginas Anthropic, 2 OpenAI, JSON Schema) | contagem das chaves | registrado no handoff novo |
| Trechos só conferidos em `/tmp` (pasta perdida) | pasta ausente | fontes baixadas de novo; 33 de 33 aprovados em 14/11/2026 |

Sem achado em: hashes de entrada (batiam com o handoff), validador (16 OK), links, citações da 4.1 (literais no pacote).

## O que foi feito

- 17 partes novas (4.2a a 4.6d), 6 questões (gabarito B, D, A, C, B, D), glossário (+22 termos), referências do capítulo 4 e sumário com links. Molduras de imagem em 4.3a e 4.6b (só `role="img"` e `aria-label`).
- Pacote de fontes: 9 trechos novos (C4-25 a C4-33), total 33. Esforço e parâmetros seguem as páginas da Anthropic: o texto afirma que o esforço **não equivale** à temperatura (a página diz só que controla quantos tokens o modelo gasta).
- Numeração: questões na 93, glossário na 94, referências na 95 (95 páginas lógicas).
- Texto de introdução “capítulos 1, 2 e 3” trocado por “1 a 4”.

## Validação

- `validar-guia.py`: 16 OK, 0 FALHA. Blocos de código do capítulo 4: 4 a 11 linhas, todos `data-executavel="false"`.
- PDF: 320 páginas A4, Chrome for Testing 158.0.8127.18; capítulo 4 na página física 233. Conferidas em PNG as páginas 253 (4.2d) e 288 (4.6d). A página 291 traz só a linha “Aprofundar” da 4.6d (cosmético).

## Hashes (16 caracteres)

HTML `fffe13bd5c4b0109`; PDF `0cfe42f8ab886203`; pacote de fontes `f169d2f2629c8bd1`.

## Não verificado

Reflow em 320 px e conforto em aparelhos reais; revisão do texto por Opus 5.5 High (Bloco 3 do plano); geração das imagens (última etapa); fatos fora dos trechos literais do pacote (por exemplo, definições de top-k e top-p) estão marcados como proposta didática.

Assinatura: claude - pessoal, 14/11/2026.
