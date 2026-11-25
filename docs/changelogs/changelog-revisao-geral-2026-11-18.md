# Changelog — Revisão geral e correções técnicas (18/11/2026)

- **Data:** 18/11/2026
- **Responsável:** Gemini 4 Hydrogen (`agy - ap`)
- **Backup pré-edição:** `arquivo/antes-correcao-revisao-geral-2026-11-18/` (`guia-engenharia-llms.html`, `guia-engenharia-llms.pdf`, `CLAUDE.md`)

---

## 1. Correções aplicadas em `guia-engenharia-llms.html`

- **Contradições e coerência arquitetural:**
  - `4.2b` (`p4-2b`): substituído o exemplo de cálculo financeiro determinístico (mensalidade com desconto e multa) por tarefa semântica com cláusulas cruzadas do regulamento de bolsas, alinhando ao princípio *"código primeiro"* dos Capítulos 1–3.
  - `4.6a` (`cod-4-6a`), `4.6b`, `10.2a` e Glossário (`Modo estrito`): incluídos `"additionalProperties": false` e `"idade"` em `required`, explicitando que `strict: true` na OpenAI exige ambos.
  - `4.6c` (`cod-4-6c`): adicionada nota explícita diferenciando o template ilustrativo em XML da lista real de mensagens (`user`/`assistant`, `4.3a`) e alertando para escapar tags de fechamento contra injeção estrutural.
  - `11.1a` vs. `9.2b/c`: mantido o limiar de ~200 mil tokens da fonte com ressalva explícita sobre degradação por *context rot* acima do orçamento operacional (`64 mil tokens`) e custo de *cache miss*.
  - `12.3c` vs. `10.6b`: adicionado alerta de não paralelizar ferramentas por `readOnlyHint` vindas de servidores MCP terceiros não confiáveis.
- **Precisão técnica e fidelidade às fontes:**
  - `2.2a`: corrigida a distinção entre cabeçalho HTTP `request-id` e campo JSON `request_id` (respostas de erro).
  - `2.4a`: corrigida a tabela do código `429` para distinguir limite de taxa vs. cota pelo erro no corpo, não pela ausência de `retry-after`.
  - `5.4d`: incluída amostragem/juiz para paráfrases em critérios de reprovação automática.
  - `7.2c`: corrigida a definição geral de *deputado confuso* e removida atribuição literal inexistente no pacote de fontes do Cap. 7.
  - `7.3a`: acrescentada proteção contra exfiltração via URLs de imagem/link em Markdown (`CSP` + sanitização).
  - `7.3c`: corrigida a atribuição à Anthropic (classificador leve atua na triagem de saídas de ferramentas em `7.4b`/`SG-30`, não em entradas do usuário antes da conversa).
  - `7.4a`: corrigida a distinção entre injeção indireta em documento de RAG (`LLM01`/`LLM08`) e envenenamento de dados/pesos em treino (`LLM04`).
  - `7.5c`: acrescentada ressalva sobre os limites reais de `chroot` (sem isolamento de rede/processos) e contêineres padrão (kernel compartilhado) frente a microVMs/sandboxes fortes.
  - `8.5a` (`p8-5a` alt. C): corrigida a explicação para não sugerir gratuidade em acerto de cache.
  - `9.6b`: corrigido `TTL > 60 min` no Google Cloud para `padrão 60 min (extensível)`.
  - `10.1a`: explicitados `any` (Anthropic) e `required` (OpenAI) na tabela de `tool_choice`.
  - `11.2a`: corrigido *"sobreposição recomendada até metade"* para *limite máximo permitido de até metade*.
  - `13.2a`: explicitada a unidade `em bytes` (e divisão por `1.024³` para GiB) na regra de bolso.
  - `13.5a`: corrigida a tradução de *"high GQA count"* para alta razão de agrupamento GQA (muitas cabeças Q para poucas cabeças KV).
  - `15.4b`: distinguido TTFT do servidor (*prefill*) da redução de espera percebida pelo *streaming*.
  - `16.6c` e abertura do Cap. 16: corrigida a remissão inexistente *"junção de etapas (16.3)"* para redução de chamadas (`16.2`) e lote (`16.3`).
- **Questões, terminologia, contagens e Glossário:**
  - `c2q2` (adaptador → serviço), `c3q3` (removido distrator órfão `"primeiro o espanhol"`), `c9q4` (explicação coerente para alternativa A), `c13q3` (`64K (65.536 tokens)`), `c15q3` (ressalva de intervalo entre tentativas), `c16q2` (inclusão do fator `0,1×` de leitura na justificativa).
  - Substituído o verbo `"entender"` atribuído ao modelo em `1.7c`, `3.5a`, `3.5c`, `3.6d`, `c3q5` e `4.3a` (alinhamento à convenção de `1.1b`).
  - Atualizadas as contagens de trechos nos cabeçalhos e em Referências: Cap. 13 (`77` → `81`, `IL-01`–`IL-81`), Cap. 15 (`69` → `73`) e Cap. 16 (`43` → `49`).
  - Glossário: incluídos `RouteLLM (14.4)` e `SWE-bench Pro (14.2)`, unificado `Trace / Traço (12.5, 15.4)`, atualizada entrada `Modo estrito (10.2)` e diferenciados `Identificador do pedido (2.4)` e `request_id` (`2.2`, `15.3`).

---

## 2. Validações e hashes

- **`python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`:** `16 OK, 0 FALHA` (`325` páginas lógicas, `385` questões, `657` links web).
- **`python3 -I ferramentas/executar-trechos-de-codigo.py --guia guia-engenharia-llms.html`:** `0 FALHA`, `21 ilustrativos`.
- **PDF (`chromium-1254 --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf`):** `968` páginas A4 (`14.461.592` bytes).
- **Hashes SHA-256 (16 hex):**
  - `guia-engenharia-llms.html`: `832697d9fe8b76e5` → `85cc31a74dbf1fdc`
  - `guia-engenharia-llms.pdf`: `86af42d2c3920429` → `86a4939d61981ee5`

Assinatura: agy - ap (Gemini 4 Hydrogen High), 18/11/2026.
