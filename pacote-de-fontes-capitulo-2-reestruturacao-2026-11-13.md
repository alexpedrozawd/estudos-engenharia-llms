# Pacote de fontes do capítulo 2 (reestruturação), 13/11/2026

Autoria: claude - pessoal. Não autoriza ações: revalide antes de usar. Projeto sem Git.

**Método.** Cada página foi aberta em 13/11/2026 por agente de leitura. Só entra aqui trecho **literal visto no corpo da página** (máx. 30 palavras). Resumo gerado por modelo não vale como prova. Valores numéricos de limites e preços não são copiados.
**Limite do método.** As citações foram relatadas por agentes de leitura de páginas, e eu não reabri as páginas por conta própria. Os agentes divergiram em pontos (Prompt caching e Structured outputs saíram como “não encontrado” numa leitura e como literais em outra). Antes de publicar, reconferir as citações que viram aspas no guia.
**Legenda.** `OK` = literal visto. `PARCIAL` = só parte lida ou palavra diferente. `NÃO VERBATIM` = não confirmado; não entra no guia como citação. `CORRIGIR` = texto atual do guia diverge da fonte.

## 1. Plano de partes que usam estas fontes

2.1 (a peças e fronteiras; b três formas de chegar; c caminho do pedido) · 2.2 (a pedido e resposta; b sem memória; c motivo de parada) · 2.3 (a dois tempos; b streaming; c transmissão interrompida) · 2.4 (a limites e classes de erro; b quando repetir; c identificador) · 2.5 (a onde mora o estado; b o que guardar; c retomada e **registros: parte nova**) · 2.6 (a muitos pedidos; b fila, limite, recusa, disjuntor; c sobrecarga e tentativas; d **pedidos longos: parte nova**). Seis questões, uma por unidade.

## 2. Fontes verificadas, por assunto

### 2.1 Componentes, fronteiras, acessos
| Fonte (URL) | Trecho literal | Estado |
|---|---|---|
| MDN, Overview of HTTP (developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview), alterada em 08/10/2026 | "HTTP is a client-server protocol: requests are sent by one entity, the user-agent (or a proxy on behalf of it)." / "HTTP is stateless: there is no link between two requests being successively carried out on the same connection." | OK |
| Ollama, OpenAI compatibility (docs.ollama.com/api/openai-compatibility) | "Ollama supports a subset of the" API da OpenAI (a página lista /v1/chat/completions, /v1/embeddings e outras; /v1/responses só sem estado) | OK. "experimental compatibility" não está na página: não usar |
| llama.cpp, tools/server/README.md (github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md) | "OpenAI API" compatible chat completions, responses, and embeddings routes; "Parallel decoding with multi-user support"; "Continuous batching" | PARCIAL (cerca de 40 mil de 90 mil caracteres lidos) |
| MCP, especificação (modelcontextprotocol.io/specification/latest) | "is an open protocol that" … "enables seamless integration between LLM applications and external data sources and tools." / "Stateless, self-contained requests" (Base Protocol); caminhos da página citam 2026-07-28 | OK. Link do changelog não localizado |
| Anthropic, Building effective agents, 19/12/2024 (anthropic.com/engineering/building-effective-agents) | "we recommend finding the simplest solution possible, and only increasing complexity when needed"; "an LLM enhanced with augmentations such as retrieval, tools, and memory" | OK. A página avisa que parte das ferramentas mudou desde 2024 |

### 2.2 A chamada ao modelo
| Fonte | Trecho literal | Estado |
|---|---|---|
| Anthropic, Using the Messages API (platform.claude.com/docs/en/build-with-claude/working-with-messages) | "The Messages API is stateless, which means that you always send the full conversational history to the API." A mesma página registra um modo em beta em que a API guarda a conversa | OK. **Não escrever "toda API é sem estado"** |
| OpenAI, Conversation state (developers.openai.com/api/docs/guides/conversation-state) | "While each text generation request is independent and stateless"; `previous_response_id`: "This parameter lets you chain responses and create a threaded conversation."; "Response objects are saved for 30 days by default." | OK |
| Anthropic, Stop reasons and fallback (platform.claude.com/docs/en/build-with-claude/handling-stop-reasons) | "The `stop_reason` field is part of every successful Messages API response." / "The response reached your `max_tokens` limit." Valores na tabela: end_turn, max_tokens, stop_sequence, tool_use, pause_turn, refusal, model_context_window_exceeded | PARCIAL (40 mil de 124 mil caracteres). A palavra "truncated" **não** aparece para max_tokens |
| Anthropic, Extended thinking (…/extended-thinking) | "Thinking tokens count toward the `max_tokens` limit for the turn, so the budget must leave room for the final response." | OK. **CORRIGIR**: as duas citações atuais da nota de 2.2 ("are billed as output tokens, even when…" e "The billed output token count does not match…") **não estão** nesta página. "Cobrado como saída" só tem apoio indireto aqui: "reports how many of the billed output tokens were internal reasoning". Resolvido em 13/11/2026: a página **Thinking** (…/thinking) contém a frase de cobrança na íntegra; a página **Steering thinking** (…/thinking-steering-and-cost), aberta em 13/11/2026, confirma "Tokens Claude uses while thinking (billed as output tokens)" e "You are billed for the full thinking process, not the thinking content visible in the response." |
| Anthropic, Structured outputs (…/structured-outputs) | "Structured outputs guarantee schema-compliant responses through constrained decoding:" / "The output might not match your schema because the refusal message takes precedence over schema constraints." / com max_tokens: "The output might be incomplete and not match your schema." | OK |
| Anthropic, Errors (platform.claude.com/docs/en/api/errors) | "The response also includes a `request_id` field for easier tracking and debugging." | OK |
| Ollama, api.md (github.com/ollama/ollama/blob/main/docs/api.md; a página diz que a documentação mudou para docs.ollama.com/api) | "`prompt_eval_count`: number of tokens in the prompt" / "`eval_count`: number of tokens in the response" | OK |

### 2.3 Streaming e latência
| Fonte | Trecho literal | Estado |
|---|---|---|
| Anthropic, Streaming messages (…/build-with-claude/streaming) | "you can set `"stream": true` to incrementally stream the response"; eventos `message_start`, `content_block_delta`, `message_delta`, `message_stop`; `event: error` com `overloaded_error` | PARCIAL. Como retomar fluxo interrompido: **NÃO VERBATIM** (só em resumo) |
| Anthropic, Errors | "an error can occur after the API returns a 200 response." | OK |
| OpenAI, Streaming API responses (developers.openai.com/api/docs/guides/streaming-responses) | "This guide focuses on HTTP streaming (`stream=true`) over server-sent events (SSE)." | OK |
| MDN, Using server-sent events, 03/09/2026 | "This is a one-way connection, so you can't send events from a client to a server." / "…needs to respond using the MIME type `text/event-stream`." | OK |
| Anthropic, Reducing latency (platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency; o endereço …/build-with-claude/reduce-latency dá 404) | "This metric measures the time it takes for the model to generate the first token of the response"; streaming: "This can significantly improve the perceived responsiveness of your application" | OK |
| OpenAI, Latency optimization (…/guides/latency-optimization) | "Generate fewer tokens."; "cutting 50% of your output tokens may cut ~50% of your latency" | OK |
| NVIDIA, LLM Inference Benchmarking: Fundamental Concepts, 02/04/2025 (developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/) | "Time to first token (TTFT) is the time it takes to process the prompt and generate the first token (Figure 2)." / "Intertoken latency (ITL) is the average time between the generation of consecutive tokens in a sequence." | OK. **CORRIGIR**: a frase da nota atual ("time to first token, end-to-end request latency, intertoken latency, tokens per second") só aparece na caixa "AI-Generated Summary" da página, não no texto do artigo. Trocar pelas frases acima |
| Anthropic, Prompt caching (…/prompt-caching) | "By default, the cache has a 5-minute lifetime." / "Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions)." | PARCIAL (167 mil caracteres; 27 mil finais não lidos). Citar com a ressalva do rodapé |

### 2.4 Limites, erros e novas tentativas
| Fonte | Trecho literal | Estado |
|---|---|---|
| Anthropic, Errors | Códigos 400, 401, 402, 403, 404, 409, 413, 429 `rate_limit_error`, 500 `api_error`, 504, 529 `overloaded_error`: "The API is temporarily overloaded." / SDK: "honoring the `retry-after` header when present." | OK |
| Anthropic, Rate limits (…/api/rate-limits) | "measured in requests per minute (RPM), input tokens per minute (ITPM), and output tokens per minute (OTPM)"; "When the response has a `retry-after` header, wait that many seconds before retrying."; "The API uses the token bucket algorithm to do rate limiting."; o 429 por teto de gasto "has no `retry-after` header" | OK |
| OpenAI, Error codes (…/guides/error-codes) | "Pace your requests and follow the Retry-After header when it's present." / "If it's missing, use exponential backoff with jitter and limit the number of retries." / "Retrying billing, spend, or quota errors won't restore API access." | OK |
| OpenAI, Rate limits (…/guides/rate-limits) | "Note that unsuccessful requests contribute to your per-minute limit, so continuously resending a request won't work." / "If it's missing or invalid, fall back to exponential backoff with jitter." | OK. "Limite aplicado em janelas menores que o exibido": **NÃO VERBATIM**, não afirmar |
| RFC 6585, seção 4 (rfc-editor.org/rfc/rfc6585.html), abril de 2012 | "The 429 status code indicates that the user has sent too many requests in a given amount of time ('rate limiting')." / "MAY include a Retry-After header indicating how long to wait before making a new request." / "this specification does not define how the origin server identifies the user, nor how it counts requests." | OK |
| RFC 9110 (rfc-editor.org/rfc/rfc9110.html), junho de 2022 | 10.2.3: "The Retry-After field value can be either an HTTP-date or a number of seconds to delay after receiving the response." · 15.6.4: "The server MAY send a Retry-After header field" · 15.5.9: "The 408 (Request Timeout) status code indicates that the server did not receive a complete request message" · 9.2.2: "Of the request methods defined by this specification, PUT, DELETE, and safe request methods are idempotent." / "A client SHOULD NOT automatically retry a request with a non-idempotent method unless it has some means to know that the request semantics are actually idempotent" | OK. **Não existe frase "POST não é idempotente"** no RFC; POST só fica fora da lista. Para "POST não é garantido": MDN |
| MDN, Idempotent (Glossary), 24/07/2025 | "All safe methods are idempotent, as well as PUT and DELETE." / "The POST and PATCH methods are not guaranteed to be idempotent." | OK |
| IETF, Idempotency-Key (datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/) | **Revisão 08, de 22/10/2026, rascunho ativo, expira em 25/04/2027** (a 07, de 15/10/2025, já expirou). Resumo: "can be used to make non-idempotent HTTP methods such as POST or PATCH fault-tolerant." Reuso com outro conteúdo: "the resource SHOULD reply with an HTTP 422 status code." Pedido simultâneo: "the resource SHOULD reply with an HTTP 409 status code." | OK. Citar sempre como "rascunho (rev. 08)" |
| Stripe, Idempotent requests (docs.stripe.com/api/idempotent_requests) | "A client generates an idempotency key, which is a unique key that the server uses to recognize subsequent retries of the same request." / "For API v1, Stripe saves the status code and body of the first request made with a given idempotency key after endpoint execution begins." / "…errors if they're not the same to prevent accidental misuse." | OK. **CORRIGIR**: a nota atual corta "For API v1" e "after endpoint execution begins"; a retenção de 24 horas vale só para v1 |
| AWS, Timeouts, retries, and backoff with jitter, 05/12/2019, Marc Brooker (o endereço aws.amazon.com/builders-library/… redireciona 301 para builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter) | "Retries are “selfish.”" / "retries that increase load can make matters significantly worse" / "Jitter adds some amount of randomness to the backoff to spread the retries around in time." / "our best practice is to retry at a single point in the stack." / "APIs with side effects aren't safe to retry unless they provide idempotency." / "start with the latency metrics of the downstream service" | OK. **Atualizar o link** |
| AWS Architecture Blog, Exponential Backoff and Jitter, 04/03/2015 (aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) | "The no-jitter exponential backoff approach is the clear loser." | OK |

### 2.5 Estado, persistência, registros
| Fonte | Trecho literal | Estado |
|---|---|---|
| Anthropic, multi-agent research system, 13/06/2025 (anthropic.com/engineering/multi-agent-research-system) | "When errors occur, we can't just restart from the beginning: restarts are expensive and frustrating for users." / "Instead, we built systems that can resume from where the agent was when the errors occurred." / dados de 4× e 15× tokens: frase confirmada (126 caracteres, não reproduzida aqui) | OK |
| OpenTelemetry, convenções de IA generativa (mudaram para github.com/open-telemetry/semantic-conventions-genai; opentelemetry.io/docs/specs/semconv/gen-ai/… é só um aviso de mudança) | Estado: **Development**. Intervalo de inferência: "Span name SHOULD be `{gen_ai.operation.name} {gen_ai.request.model}`." Atributos `gen_ai.usage.input_tokens` e `gen_ai.usage.output_tokens`. Métrica de tempo até o primeiro trecho: `gen_ai.client.inference.time_to_first_chunk` | PARCIAL. Conteúdo de prompt e resposta como opt-in: **NÃO VERBATIM**. Nome `gen_ai.client.token.usage` **não** existe nas páginas lidas. Só para ponte; não ensinar nomes de campo |
| Anthropic, Errors | `request_id` ao falar com o suporte (ver 2.2) | OK |

### 2.6 Simultaneidade, capacidade, pedidos longos
| Fonte | Trecho literal | Estado |
|---|---|---|
| Google SRE, cap. 21 Handling Overload (sre.google/sre-book/handling-overload/), © 2017, sem data | "eventually some part of your system will become overloaded" / "One option for handling overload is to serve degraded responses" / "A request will only be retried as long as this ratio is below 10%." (com limite de até três tentativas por pedido) / "Client-side throttling addresses this problem." | OK. O termo "load shedding" **não** está neste capítulo |
| Google SRE, cap. 22 Addressing Cascading Failures | "The most common cause of cascading failures is overload." / "Load shedding drops some proportion of load by dropping traffic as the server approaches overload conditions." / "Usually, if the queue is full, the server will reject new requests." | PARCIAL (40 mil de 63 mil caracteres) |
| Fowler, CircuitBreaker, 06/03/2014 (martinfowler.com/bliki/CircuitBreaker.html) | "You wrap a protected function call in a circuit breaker object, which monitors for failures." / "Once the failures reach a certain threshold, the circuit breaker trips" / "There is now a third state present - half open -" / "Any change in breaker state should be logged and breakers should reveal details of their state for deeper monitoring." | OK. Frase sobre Nygard da nota atual: não reconferida |
| Ollama, FAQ (docs.ollama.com/faq) | "If too many requests are sent to the local Ollama server, it responds with a `503` overloaded error." / `OLLAMA_NUM_PARALLEL`: "The maximum number of parallel requests each model will process at the same time, default 1." / fila: "The default is 512" | OK. Padrões podem mudar: citar com data |
| **Parte nova — pedidos longos.** RFC 9110 15.3.3 | "The 202 (Accepted) status code indicates that the request has been accepted for processing" | OK |
| MDN, 202 Accepted, 04/07/2025 | "indicates that a request has been accepted for processing, but processing has not been completed or may not have started" | OK |
| OpenAI, Background mode (…/guides/background) | "To start response generation in the background, make an API request with background set to true" / "Keep polling while the request is in the queued or in_progress state." / "Response data is temporarily stored to disk for roughly 10 minutes to enable asynchronous execution and polling." | OK. Lista completa de estados **não** consta |
| OpenAI, Batch API (…/guides/batch) | "Each batch completes within 24 hours (and often more quickly)" / "50% cost discount compared to synchronous APIs" / "Batch API rate limits are separate from existing per-model rate limits." | OK |
| Anthropic, Batch processing (…/batch-processing) | "The batch is then processed asynchronously, with each request handled independently." / "You can access batch results when all messages have completed or after 24 hours, whichever comes first." / "All usage is charged at 50 percent of the standard API prices." / "…with most batches finishing in less than 1 hour…" | PARCIAL (40 mil de 81 mil). Duas frases: "até 24 horas" e "a maioria em menos de 1 hora" |
| Anthropic, Errors, seção "Long requests" | "Consider using the streaming Messages API or Message Batches API for long-running requests, especially those over 10 minutes." | OK |

### Leitura complementar (didática)
- Chip Huyen, *AI Engineering* (O'Reilly, 2025): página do autor huyenchip.com/books/ — "This book discusses AI engineering: the process of building applications with readily available foundation models." A página da O'Reilly deu 403; sem data exata de publicação.
- Sem curso em vídeo conferido para este capítulo. A linha "Assistir" não entra.

## 3. Achados contra o texto atual do capítulo 2

| # | Achado | Ação proposta |
|---|---|---|
| 1 | Nota da 2.2 cita duas frases de "Extended thinking" que não estão na página atual | Resolvido: a nota usa a frase verificada do limite; a cobrança como saída está na página Thinking e na Steering thinking (aberta em 13/11/2026) |
| 2 | Nota da 2.3 cita NVIDIA com frase que só está na caixa de resumo gerada | Usar as frases do corpo (TTFT e ITL) |
| 3 | Stripe: citação sem "For API v1" e sem "after endpoint execution begins" | Completar |
| 4 | Links da OpenAI usam platform.openai.com/docs/guides/… | Usar developers.openai.com/api/docs/guides/… (carregaram todos) |
| 5 | Link da AWS redireciona (301) | Usar builder.aws.com/… ou manter o endereço antigo com aviso |
| 6 | Link do Ollama api.md aponta para repositório que migrou | Preferir docs.ollama.com/api (não aberto; conferir) |
| 7 | Todas as datas "consultada em 15/10/2026" | Trocar por 13/11/2026 nas fontes reabertas aqui |
| 8 | "Antipadrão da fila distribuída: diretrizes locais do autor (documento não público)" | Decisão do operador: remover ou manter como critério do autor, sem citação |
| 9 | Remissões "módulo N" | Trocar por "mais adiante no guia" (decidido) |
| 10 | RFC 9110 não diz que POST não é idempotente | Escrever "POST não é garantido" e citar MDN |

## 4. Lacunas (não verificado)

- Retomada de fluxo interrompido na Anthropic (resumo, não literal).
- ~~Billing do raciocínio como saída (página Steering thinking).~~ Resolvido em 13/11/2026: "Tokens Claude uses while thinking (billed as output tokens)".
- Afirmação da AWS de que a idempotência se apoia em mecanismos baseados em identificador (a frase “APIs with side effects…” foi confirmada; a parte do identificador não).
- Frase de Nygard na nota do disjuntor (o guia novo não a usa); trechos finais de caps. 22, README do llama.cpp, Prompt caching.
- Estados de resposta em segundo plano da OpenAI além de queued e in_progress.
- Capítulo 2 não tem vídeo conferido; data e duração de vídeos do capítulo 1 seguem pendentes.
- Nenhuma fonte de terceiros (blogs de comparação) entrou; as buscas as trouxeram, e foram descartadas.

## 5. Complemento: citações lidas por agentes e usadas no guia, sem linha própria nas tabelas

Todas reportadas como literais no corpo da página, em 13/11/2026.
- MDN, Overview of HTTP: "There are two types of HTTP messages, requests and responses, each with its own format."
- Anthropic, Reducing latency: "Latency refers to the time it takes for the model to process a prompt and generate an output"
- Ollama, API: "`keep_alive`: controls how long the model will stay loaded into memory following the request (default: `5m`)"; "Streaming can be disabled by providing `{"stream": false}` for these endpoints."
- Anthropic, Prompt caching: "This significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements."
- Ollama, Local FAQ: "`OLLAMA_NUM_PARALLEL` - The maximum number of parallel requests each model will process at the same time, default 1."
- llama.cpp, README: "number of server slots (default: -1, -1 = auto)"
- Google SRE cap. 22: "retries can destabilize a system"; cap. 21: "requests should not be retried and errors should bubble up all the way to the caller"

URLs abertas por agentes e usadas como link no capítulo 2: todas as que constam nas tabelas acima, mais `developers.openai.com/api/docs/guides/` (error-codes, rate-limits, background, batch, conversation-state, streaming-responses, latency-optimization), `rfc-editor.org/rfc/rfc9110` e `rfc6585`, `developer.mozilla.org` (Overview of HTTP, Idempotent, 202, 429, Using server-sent events), `sre.google/sre-book/` (caps. 21 e 22), `anthropic.com/engineering/` (building-effective-agents, multi-agent-research-system), `builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/…` e `docs.ollama.com/faq`.

claude - pessoal
