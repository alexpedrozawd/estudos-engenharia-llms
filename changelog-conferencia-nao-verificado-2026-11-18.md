# Changelog — Conferência dos itens `[Não verificado]` das Partes II e III (18/11/2026)

## Escopo

Pedido do operador: terminar a conferência online dos itens `[Não verificado]` dos Caps. 6 a 16, corrigindo o guia onde a fonte divergir; exceto imagens e aparelhos reais. Fontes baixadas em pasta limpa, lidas como texto e comparadas com o HTML. Trechos em `pacote-de-fontes-conferencia-nao-verificado-2026-11-18.md` (127 linhas, `CNV-01` a `CNV-127`).

## Resultado

[ANALISADO / NÃO ALTERADO]

- Confirmados sem mudança: Cap. 9 (cache na janela, regra das duas correções), Cap. 12 (ADK, harness hospedado, exemplo de quatro voltas, retomada), Cap. 14 (LiteLLM, fatores da Anthropic, tarefas simples da OpenAI), Cap. 15 (staging, rotação de chave, escala, Bedrock, OTel, `request-id`, estados do modelo), Cap. 16 (50%, 24 h, 29 dias, 4 marcações, 95%, 90%).
- Cap. 7 e tabela da 7.6b (retenção, CORS em ZDR, `store=false`, log desativado, `store` do Interactions API): confirmados.

[CORRIGIDO / AJUSTADO]

- **16.5b e 9.6b:** a leitura de cache da Anthropic não é só 0,1×; a página de preços traz 0,05× (Opus 5.5, Sonnet 5.5) e 0,025× (Fable, Mythos). Quadros corrigidos.
- **11.5b:** a OpenAI só diz "resposta concisa com base nas fontes"; declarar a lacuna e indicar o canal oficial virou proposta didática.
- **7.2b:** a OpenAI recomenda revisão humana das saídas, não aprovação de ações; texto separado da OWASP.
- **7.4b e 7.2c:** OWASP diz "não está claro que exista método à prova de falhas" e "orienta" mediação completa (antes "é clara" e "exige").
- **8.3a:** "reversão automatizada" trocada por rollback; "derrubando os servidores" trocado por "piorando a situação". **8.4b:** milhares de ferramentas (não centenas) levam a centenas de milhares de tokens; hooks × `CLAUDE.md` alinhados à página.
- **11.4b e 11.2b:** removido "bases grandes"; perda no meio da janela atribuída a Liu et al.
- **15.2c e 15.5a:** `Retry-After` em 429 e 503; não reenviar após o stream marcado como proposta didática; versão da API pode mudar condições de erro.
- **6.2c, 6.5a, 13.1a, 13.1b, 13.6b, 16.1c:** afirmações sem fonte removidas ou marcadas como leitura didática (custo de embeddings, causas do multiplicador 15×, caminhos de carga, velocidade por parâmetros ativos, gradientes e otimizador, "erro comum" no diagnóstico de custo).

[PENDENTE / BLOQUEADO]

- Imagens em aquarela e teste nos três aparelhos reais: com o operador.
- Não reconferidos: "Denison sem exemplo prévio" (8.1b); exposição de servidores locais só na rede interna (7.5c, já proposta didática); lacuna da 14.6c (invalidação de cache ao trocar de modelo) segue declarada.

## Validações

- `renumerar-paginas.py`: 316 páginas, nada a mudar. `validar-guia.py`: 16 OK, 0 FALHA. `executar-trechos-de-codigo.py`: 0 FALHA, 21 ilustrativos.
- `auditar-guia-navegador.mjs` (Chrome 1254): reflow 320 px com 0 estouros em 316 seções; 376/376 questões com veredito correto; axe-core 45 passes, 0 violações (1 "incomplete" de color-contrast, limite da ferramenta).
- Limites de formato: unidades alteradas entre 244 e 457 palavras antes de "Pergunta"; notas de fonte inalteradas. Nenhuma alternativa de questão alterada (gabaritos 94/94/94/94 e viés de tamanho inalterados).
- PDF regerado: 533 páginas A4; página 483 (quadro da 16.5b) renderizada e conferida.

## Hashes (16 caracteres)

- `guia-engenharia-llms.html`: antes `0df68a358f415004` → depois `7cbcd8ebfce0dbb8`.
- `guia-engenharia-llms.pdf`: antes `23fe2a8bfda2c697` → depois `6cfd4d86cbc0b51d`.

Assinatura: claude - pessoal
