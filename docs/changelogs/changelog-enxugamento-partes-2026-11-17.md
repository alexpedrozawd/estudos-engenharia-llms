# Changelog — enxugamento das partes acima de 500 palavras, 17/11/2026

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Pedido do operador em 17/11/2026: enxugar as partes acima de 500 palavras preservando contexto, qualidade da informação e facilidade de leitura.

## Backup
- `arquivo/antes-enxugamento-2026-11-17/`: HTML `2506a4d2339513ac`, PDF `486d3ac1cf400e3e`.

## Mudanças (`guia-engenharia-llms.html`)
Reduzidas as 8 partes que passavam de 500 palavras no texto principal até `<h3>Pergunta</h3>` (eliminando repetições entre prosa e citações/tabelas já registradas em `Notas de fonte`, mantendo todos os termos `<dfn>`, datas, versões e ressalvas):
- `1.3c`: 520 → **472** palavras (mantidos janelas de Qwen3.8-27B e Gemma 4, *context rot*, *Lost in the Middle*, Chroma e compactação).
- `1.7a`: 657 → **489** palavras (unificada a explicação de OSI com os exemplos de Qwen3.8-27B e Gemma 4 sem perder Apache 2.0, resumo de dados e Jev/Kev).
- `1.7c`: 555 → **428** palavras (mantidos Gemma 4 31B/26B A4B/E2B/E4B, Qwen3.8-27B denso/VLM, SLM, LLaDA/Mercury, Mamba, Genie 3 e VLA).
- `3.1b`: 536 → **426** palavras (mantidos os quatro papéis, tabela, NASA e definição de persona do Nielsen Norman Group).
- `3.5a`: 515 → **442** palavras (mantidos regra determinística vs. modelo, tabela, antipadrões e recomendação de simplicidade da Anthropic).
- `4.2a`: 570 → **442** palavras (mantidos Brown et al., Min et al., cena do centro comunitário e recomendação do Google).
- `4.2c`: 531 → **383** palavras (mantidos tabela da biblioteca, Anthropic, OpenAI e Google sobre delimitadores e *prompt patching*).
- `4.5a`: 831 → **444** palavras e **2 → 1 tabela** (removida a tabela isolada da Anthropic e consolidado `output_config.effort` na tabela única de três provedores e dois modelos abertos, cumprindo a regra de no máximo uma tabela por parte).

Observação: `5.1c` (396 palavras até a pergunta; 508 até `Notas de fonte`) e `4.6d` (383 até a pergunta; 479 até notas) já estavam dentro da meta e não precisaram de corte.

## Validação após edição
- Contagem automática nas 103 partes (`unidade-*`): **0 partes > 500 palavras** até `Pergunta`; **0 partes > 1 tabela**.
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (117 páginas lógicas).
- PDF regerado com Chrome for Testing 158: **385 páginas A4** (`594.96 x 841.92 pts`).
- Não executado: reflow em 320 px e leitura em aparelhos reais.

Hashes finais: HTML `fc6e9b03ec4bf587`; PDF `fff4e10a9c2f0a74`.

Assinatura: agy - ap, 17/11/2026.
