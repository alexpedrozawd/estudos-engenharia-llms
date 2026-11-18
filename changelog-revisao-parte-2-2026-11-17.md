# Revisão da Parte II (Capítulos 6 a 11) — 17/11/2026

Autoria: claude - pessoal (Sonnet 5.5 High, varredura somente leitura por capítulo) e agy - ap (Orchestrator Argon, conferência direta no HTML e pacotes, aplicação das correções, validação e fechamento). Pedido do operador: revisar cada capítulo da Parte II isoladamente (`/revisar`), conferir pelas fontes já salvas, corrigir os achados aplicáveis, regerar o PDF, fazer commit/push e preparar novo handoff para a Parte III. Nenhuma URL foi baixada.

## Resultado

- 104 correções aplicadas em `guia-engenharia-llms.html` (`103 insertions(+), 103 deletions(-)` no `git diff --stat`). Estrutura intacta: 325 páginas lógicas, `validar-guia.py` com **16 OK / 0 FALHA**, PDF regerado com **963 páginas A4** (Chrome for Testing 158; páginas 380 e 381 inspecionadas em PNG).
- Sem achado de estrutura de parte curta, link quebrado, ID duplicado, neutralidade ou excesso de tamanho (todas as partes abaixo do teto P2 de 560 palavras até a "Pergunta").

## Correções por causa

| Causa | Onde | Ajuste |
|---|---|---|
| Fidelidade às fontes | Caps. 6, 7, 8, 9 e 10 | Cap. 6: `4×` e `15×` atribuídos a agente em laço e multiagente (EG-33). Cap. 7: NIST AI 600-1 `GOVERN 1.1`/`1.5` como pontos de partida (SG-51/52); deputado confuso separado de repasse cego de token (SG-15/16). Cap. 8: "todas as máquinas envolvidas" no SRE cap. 13 (AP-02); "outro risco" em AP-10; artigo de blog em AP-13; quatro travas em 8.3b com Anthropic/OpenAI/SRE (AP-26/28/29/30); acurácia sem "alucinações" em AP-51; ajuste fino não supervisionado em Ovadia et al. (AP-52). Cap. 9: 14ª fonte (*Best Practices for Claude Code*) listada na abertura; modal "podem/pode ser mais adequada" na estratégia híbrida (CM-23/24); Google Cloud recomenda conteúdo grande no início vs. prefixo idêntico na OpenAI (CM-68/73); TTL de 1 h em plano de assinatura no Claude Code vs. 5 min em API/nuvem/créditos (CM-54). Cap. 10: mudança de `tool_choice` invalidando cache (FI-07); especificação MCP "orienta" (FI-51) e seção de deputado confuso (FI-53) |
| Enunciados e explicações de questões | Caps. 6, 7, 8, 9 e 11 | Explicações alinhadas às alternativas marcadas e ao conteúdo em `c6q6-D`, `p7-1a-A`, `p7-3b-C/D`, `p7-5a-D`, `p7-6a-D`, `p8-5a-D`, `p8-5b-B/C`, `p8-6b-C`, `p9-2b-D`, `p11-1b-C`, `p11-2b-C`, `p11-3b-A`, `p11-5c-D`, `p11-6b-C`, `c11q2-C` e `c11q5-C`; enunciado `c7q3` trocado para "conjunto de correções" |
| Coerência interna e contagens | Caps. 8, 10 e 11 | Cap. 8: resumo da 8.6a alinhado ao JSON de reversão. Cap. 10: faixa de 5 a 15 ferramentas na tabela da 10.3c; "três primitivas" na 10.6a; "decisões integradas em três grupos" na 10.6c. Cap. 11: "seis pilares" da Parte II na 11.6b |
| Rótulos, IDs de molduras e remissões | Caps. 6, 7, 8, 9, 10 e 11 | Qualificador `registrado no artigo` em 6.4b e 7.1b; `data-imagem` alinhado ao ID da parte após fusões em `9-5a`, `10-4b` e `11-4a`; códigos `EG-*` identificados como trechos do pacote do capítulo 6 em 9.0, 9.5b, 11.0 e 11.5c; padronização de `capítulo N` no corpo dos Caps. 6, 8, 9, 10 e 11; separação de `Aprofundar:` nas 18 seções `Fontes da unidade` dos Caps. 9 a 11 |
| Redação e termos explicados na 1ª ocorrência | Caps. 6, 10 e 11 | Cap. 6: pergunta de abertura, explicação de `top-k`, `Cypher` e `superpassos` e remoção do identificador `kg_extractors`. Cap. 10: definição de `CRM` e `JSON-RPC`, "desde o início"/"no início" no lugar de "de saída", correção de negação em 10.5b ("não corrige nada"). Cap. 11: título da 11.1a para "Quando dispensar o RAG e busca lexical (BM25)" |

## Pendências conhecidas (não alteradas)

- **Itens `[Não verificado]` (resolvidos em 18/11/2026):** conferidos online contra as fontes primárias, com trechos literais em `pacote-de-fontes-conferencia-nao-verificado-2026-11-18.md` (Caps. 6 a 11). Divergências e afirmações sem fonte foram corrigidas ou qualificadas no HTML; ver `changelog-conferencia-nao-verificado-2026-11-18.md`. A listagem original por unidade foi removida porque já não reflete o estado do texto.
- **Observação de gabaritos (não alterada):** nas perguntas e questões de fechamento da Parte II há forte concentração da alternativa correta na letra `B` (Cap. 6: 17/22; Cap. 7: 18/22; Cap. 8: 19/22; Cap. 9: 19/22; Cap. 10: 22/22; Cap. 11: 22/22), e no Cap. 9 e Cap. 10 a correta coincide com a alternativa mais longa. Reordenar alternativas requer decisão e mudança ampla de `value`/`data-correta`.
- **Links de vídeo em `Fontes da unidade`:** a linha `Assistir:` permanece ausente nos capítulos fora do Cap. 1, padrão já seguido nos Caps. 2 a 8.

## Hashes (16 caracteres)

- `guia-engenharia-llms.html`: antes `8bc0ab88dd0f2fb1` → depois `c76ed16502a32702` (backup em `arquivo/antes-revisao-parte-2-2026-11-17/`, fora do Git).
- `guia-engenharia-llms.pdf`: antes `fbc329c4b91597aa` → depois `153d3355f845e332` (Chrome for Testing 158, `--headless=new --no-sandbox --no-pdf-header-footer --print-to-pdf`, 963 páginas).

Assinatura: claude - pessoal e agy - ap.
