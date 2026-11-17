# Changelog — segunda leitura e ajustes pós-equilíbrio, 16/11/2026

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Autorização do operador em 16/11/2026: após o relato dos achados da segunda leitura, aplicar em um único lote os ajustes dos itens 1 a 6, regerar o PDF, rodar o validador e atualizar changelog e handoff.

## Backup
- `arquivo/antes-segunda-leitura-2026-11-16/`: HTML `e257b994ee8a28e2`, PDF `b5f8b55ea5538aaa`.

## Segunda leitura (sem edição prévia)
- Capítulo 5 completo (abertura, 5.1a a 5.6d, questões, glossário e referências): 47 trechos conferidos por `ferramentas/conferir-trechos.py` contra fontes baixadas em `/tmp/cap5-fontes` (**47 aprovados, 0 reprovados**); coerência numérica confirmada entre 5.2b (caso 07), 5.2c (16 casos), 5.3c (v1 12/16), 5.5a (v2 14/16), 5.5c (10/10 capacidade, 4/6 regressão), 5.6c e 5.6d (+3 ganhos, -1 perda); tom cauteloso na tabela da 5.6b confirmado; 117 ligações `page-nav` conferidas contra a ordem do documento (**0 erros**).
- 15 partes com OpenAI, Google, Qwen3.8-27B e Gemma 4 (`1.2d`, `1.3c`, `1.4c`, `1.4d`, `1.7a`, `1.7c`, `3.4a`, `4.2a`, `4.2c`, `4.5a`, `5.2a`, `5.4a`, `5.4c`, `5.5c`, `5.6a`): trechos reconferidos contra `/tmp/eq-fontes` (hashes idênticos aos do pacote em OpenAI, Qwen e Gemma; Google Prompting Strategies sem data de publicação no Markdown e mantendo o texto sobre Gemini 4 e 3.6+; Google Cloud Evaluation Overview com `Last updated 2026-11-16`; OpenAI Evals confirmando encerramento em 30/11/2026).

## Ajustes aplicados (`guia-engenharia-llms.html`)
1. **Pontuação em `Fontes da unidade -> Aprofundar` (`4.2d`, `4.5c`, `5.2c`, `5.4d`, `5.5c`):** removido `.;` após o primeiro link e restaurado o ponto final do parágrafo.
2. **Notas de fonte da `5.6a`:** atualizada a nota de parâmetros para incluir Google e OpenAI remetendo à parte 4.5 (consultados em 16/11/2026), alinhada ao texto principal.
3. **Referências (página 117):** atualizado o parágrafo introdutório com os 47 trechos do capítulo 5 e as conferências de 16/11/2026 (OSI, fichas de Qwen3.8-27B e Gemma 4, OpenAI e Google); corrigidos os cabeçalhos de data das seções 1.7, capítulo 3 e capítulo 4; explicitada a data `Consultado em 16/11/2026` na entrada do Google (*Prompt design strategies*).
4. **Glossário (página 116):** unificados os pares duplicados `Caso de recusa (3.4, 5.2)` e `Linha de base (3.2, 5.3)`.
5. **Clareza na `5.3c`:** ajustado `"os quatro casos de borda juntos"` para `"os dois casos de borda que falharam juntos"`, evitando ambiguidade com a tabela (4 casos, 2 aprovados).
6. **Notas de fonte da `1.7a`:** fundida a nota redundante sobre a definição da OSI (13/11/2026 e 16/11/2026) em uma entrada única.

## Validação após edição
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (117 páginas lógicas em sequência).
- Verificação de navegação `page-nav` e ausência de `</a>.;`: **0 erros**.
- PDF regerado com Chrome for Testing 158 (`--headless=new --no-sandbox --no-pdf-header-footer --print-to-pdf`): **387 páginas A4** (`594.96 x 841.92 pts`).
- Não executado: reflow em 320 px e leitura em aparelhos reais (pendentes por natureza).

Hashes finais: HTML `2506a4d2339513ac`; PDF `486d3ac1cf400e3e`.

Assinatura: agy - ap, 16/11/2026.
