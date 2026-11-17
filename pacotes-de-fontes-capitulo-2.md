# Pacotes de fontes — Capítulo 2 (Arquitetura de sistemas com LLM)

Data: 15/10/2026. Autoria: claude - pessoal (Bloco 1 em Sonnet 5.5 High, effort declarado pelo operador). Não altera o guia HTML. O pacote do Capítulo 2 antigo está arquivado em `arquivo\capitulo-2-software\`; nada dele foi reaproveitado sem nova conferência.

Formato: cada linha traz um trecho literal copiado da fonte extraída, montado por script a partir de âncoras de início e fim (nada foi completado de memória). O script `ferramentas/conferir-trechos.py` confere cada trecho contra o texto da fonte; trecho ausente reprova o pacote da unidade.

Extração (15/10/2026): páginas HTML e RFCs baixadas com `curl -L` para pasta própria e vazia, convertidas por `ferramentas/extrair-texto-web.py`. Arquivos de código copiados em modo leitura, em lista fechada, como `<chave>.txt` (linhas citadas na coluna Local valem para a cópia de 15/10/2026): `router-main` (`panel/backend/main.py`), `router-database` (`repositories/database.py`), `router-queue-worker` (`queue_worker.py`), `pay-webhook-route` e `docs09`. Fontes de provedor e de servidor local valem como estado de 15/10/2026.

Qualificadores: *registrado na documentação*, *registrado na norma*, *verificado no código local*, *registrado no contexto*, *registrado nas diretrizes locais*, *proposta didática*. Código citado prova a existência da estrutura, não a execução nem a produção. Casos da Nanda Mac não trazem nomes de pessoas, dados de clientes nem de fornecedor; no livro, usar "gateway de pagamento".

Fontes lidas e fontes que ficaram de fora:
- Lidas por extração em texto: Anthropic (*Errors*, *Rate limits*, *Streaming messages*, *Handling stop reasons*, *Working with messages*, referência de *Messages*), OpenAI (*Rate limits*, *Error codes*, *Conversation state*, *Streaming responses*), Ollama (API e compatibilidade com OpenAI), llama.cpp (servidor HTTP), RFC 9110, RFC 6585, MDN (*Overview of HTTP*, *Using server-sent events*), AWS Builders' Library (*Timeouts, retries, and backoff with jitter*), Google SRE Book (caps. 21 e 22).
- **vLLM:** a página não foi extraída (resultou vazia). Fora do capítulo; se citado, só como menção sem afirmação técnica.
- **Ollama, concorrência:** a página de perguntas frequentes não pôde ser extraída. O capítulo não afirma nada sobre paralelismo ou fila do Ollama; para servidor local usa a documentação do llama.cpp (espaços de atendimento, lotes contínuos, requisições adiadas).

Cuidados que seguem para a redação:
- **Tempo até o primeiro token** não tem definição em nenhuma fonte baixada; é termo de trabalho do livro (*proposta didática*). A única menção literal é a do llama.cpp (2.3-T14), sobre o limite de geração medido a partir do primeiro token.
- **Estado de conversa:** a API de mensagens da Anthropic e a de texto da OpenAI são sem estado e exigem reenviar o histórico (2.2-T1, T2); a OpenAI também oferece estado guardado pelo provedor (*Conversations API* e `previous_response_id`, 2.2-T4, T5), que pode não ser resolvido (2.5-T3, T4). Os dois modelos de uso convivem; não generalizar para "toda API é sem estado".
- **Limites e erros:** códigos, cabeçalhos e valores de limite mudam por provedor e por plano; citar a forma (429 com `retry-after`, 429 por teto de gasto sem `retry-after`, 529/503 por sobrecarga), nunca o número.
- **Streaming:** erro pode chegar depois do status 200 (2.3-T4, T5); a validação da resposta inteira não ocorre antes de mostrar.
- **Router:** o pacote não cita `panel.db`, `history.jsonl`, `*.log`, credenciais nem bancos.

## Unidade 2.1

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 2.1-T1 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §3 (problema, público e propósito) | Contexto de 13/10/2026 | registrado no contexto | modelo gera ou interpreta conteúdo; o sistema ao redor organiza instruções, ferramentas, estado, persistência, permissões, execução e avaliação. |
| 2.1-T2 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §4 (arquitetura encontrada), linha da API | Contexto de 13/10/2026 | registrado no contexto | Receber pedidos, compor contexto, coordenar despacho e resultados. |
| 2.1-T3 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §4, linha da persistência | Contexto de 13/10/2026 | registrado no contexto | Conversas, mensagens, triagens, pedidos de despacho e registros de jobs. |
| 2.1-T4 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §4, linha do adaptador | Contexto de 13/10/2026 | registrado no contexto | Transportar o pedido e chamar o destino selecionado com parâmetros explícitos. |
| 2.1-T5 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §4, linha da fronteira | Contexto de 13/10/2026 | registrado no contexto | Executar a etapa pelas capacidades e limites do cliente. |
| 2.1-T6 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §4, linha do local | Contexto de 13/10/2026 | registrado no contexto | Gerar respostas e propostas textuais. |
| 2.1-T7 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §8 (qualidade, velocidade e custo) | Contexto de 13/10/2026 | registrado no contexto | Clientes usados por login/plano diferem das APIs empresariais cobradas por uso. |
| 2.1-T8 | 2.1 | texto | contexto-de-estudo-ap-ai-router | §5 (pipeline triangular) | Contexto de 13/10/2026 | registrado no contexto | O chat Ollama usa `/api/generate`, sem ferramentas para ler o projeto, editar arquivos ou executar testes. |
| 2.1-T9 | 2.1 | texto | contexto-de-estudo-nanda-mac | §9 (fronteira entre software, LLM e ação humana) | Contexto de 13/10/2026 | registrado no contexto | Identidade, permissões, cálculo financeiro, status, validação, contratos de API, persistência, confirmação de ações, auditoria e recuperação. |
| 2.1-T10 | 2.1 | texto | contexto-de-estudo-nanda-mac | §6 (comportamentos úteis aos estudos) | Contexto de 13/10/2026 | registrado no contexto | o serviço consultado suporta famílias Claude, Gemini e OpenAI para análise qualitativa e resposta estruturada. |
| 2.1-T11 | 2.1 | texto | contexto-de-estudo-nanda-mac | §8 (assistentes individuais) | Contexto de 13/10/2026 | registrado no contexto | Para os estudos, “independente” significa preservar identidade, contexto, histórico e permissões do colaborador. |
| 2.1-T12 | 2.1 | texto | contexto-de-estudo-nanda-mac | §8 | Contexto de 13/10/2026 | registrado no contexto | Não implica um modelo treinado, processo de inferência ou chave de API exclusivo para cada pessoa. |
| 2.1-T13 | 2.1 | texto | mdn-http | HTTP is stateless, but not sessionless | 15/10/2026 | registrado na documentação | HTTP is stateless: there is no link between two requests being successively carried out on the same connection. |
| 2.1-T14 | 2.1 | texto | ollama-openai | Introdução | 15/10/2026 | registrado na documentação | Ollama supports a subset of the OpenAI API. |
| 2.1-T15 | 2.1 | texto | llamacpp-servidor | Introdução do servidor | 15/10/2026 | registrado na documentação | compatible chat completions, responses, and embeddings routes |

## Unidade 2.2

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 2.2-T1 | 2.2 | texto | anthropic-mensagens-uso | Mensagens: conversa de vários turnos | 15/10/2026 | registrado na documentação | The Messages API is stateless, which means that you always send the full conversational history to the API. |
| 2.2-T2 | 2.2 | texto | openai-estado | Conversation state | 15/10/2026 | registrado na documentação | While each text generation request is independent and stateless, you can still implement multi-turn conversations by providing additional messages as parameters to your text generation request. |
| 2.2-T3 | 2.2 | texto | openai-estado | Conversation state (manual) | 15/10/2026 | registrado na documentação | By using alternating user and assistant messages, you capture the previous state of a conversation in one request to the model. |
| 2.2-T4 | 2.2 | texto | openai-estado | Conversations API | 15/10/2026 | registrado na documentação | The Conversations API works with the Responses API to persist conversation state as a long-running object with its own durable identifier. |
| 2.2-T5 | 2.2 | texto | openai-estado | previous_response_id | 15/10/2026 | registrado na documentação | Another way to manage conversation state is to share context across generated responses with the previous_response_id parameter. |
| 2.2-T6 | 2.2 | texto | ollama-api | Chat (histórico de mensagens) | 15/10/2026 | registrado na documentação | Send a chat message with a conversation history. |
| 2.2-T7 | 2.2 | texto | anthropic-paradas | Stop reasons | 15/10/2026 | registrado na documentação | Every Messages API response includes a stop_reason field that tells you why Claude stopped generating. |
| 2.2-T8 | 2.2 | texto | anthropic-paradas | max_tokens | 15/10/2026 | registrado na documentação | The response reached your max_tokens limit. |
| 2.2-T9 | 2.2 | texto | anthropic-paradas | Resumo das paradas | 15/10/2026 | registrado na documentação | Treat the response as truncated. |
| 2.2-T10 | 2.2 | texto | anthropic-paradas | The stop_reason field | 15/10/2026 | registrado na documentação | Unlike errors, which indicate failures in processing your request, stop_reason tells you why Claude completed its response generation. |
| 2.2-T11 | 2.2 | texto | anthropic-erros | Error shapes | 15/10/2026 | registrado na documentação | The API always returns errors as JSON, with a top-level error object that always includes a type and message value. |
| 2.2-T12 | 2.2 | texto | anthropic-erros | Request IDs | 15/10/2026 | registrado na documentação | Every API response includes a unique request-id header. |
| 2.2-T13 | 2.2 | texto | ollama-api | Generate a completion (resposta final) | 15/10/2026 | registrado na documentação | `prompt_eval_count`: number of tokens in the prompt |
| 2.2-T14 | 2.2 | texto | ollama-api | Generate a completion (resposta final) | 15/10/2026 | registrado na documentação | `eval_count`: number of tokens in the response |
| 2.2-T15 | 2.2 | texto | mdn-http | HTTP is stateless, but not sessionless | 15/10/2026 | registrado na documentação | HTTP is stateless: there is no link between two requests being successively carried out on the same connection. |
| 2.2-T16 | 2.2 | texto | rfc9110 | §3.3 (conexões, clientes e servidores) | RFC 9110, jun/2022 | registrado na norma | HTTP is defined as a stateless protocol, meaning that each request message's semantics can be understood in isolation |
| 2.2-T17 | 2.2 | texto | anthropic-paradas | Example response | 15/10/2026 | registrado na documentação | "usage": { "input_tokens": 100, "output_tokens": 50 } |
| 2.2-T18 | 2.2 | texto | anthropic-paradas | max_tokens | 15/10/2026 | registrado na documentação | Raise max_tokens or continue the response. |
| 2.2-T19 | 2.2 | texto | rfc9110 | §15.3 Successful 2xx | RFC 9110, jun/2022 | registrado na norma | The 2xx (Successful) class of status code indicates that the client's request was successfully received, understood, and accepted. |

## Unidade 2.3

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 2.3-T1 | 2.3 | texto | anthropic-streaming | Streaming Messages | 15/10/2026 | registrado na documentação | When creating a Message, you can set "stream": true to incrementally stream the response using server-sent events (SSE). |
| 2.3-T2 | 2.3 | texto | anthropic-streaming | Event types | 15/10/2026 | registrado na documentação | Each server-sent event includes a named event type and associated JSON data. |
| 2.3-T3 | 2.3 | texto | anthropic-streaming | Error events | 15/10/2026 | registrado na documentação | The API may occasionally send errors in the event stream. |
| 2.3-T4 | 2.3 | texto | anthropic-erros | Errors in streaming | 15/10/2026 | registrado na documentação | an error can occur after the API returns a 200 response. |
| 2.3-T5 | 2.3 | texto | anthropic-erros | Errors in streaming | 15/10/2026 | registrado na documentação | In that case, error handling doesn't follow these standard mechanisms. |
| 2.3-T6 | 2.3 | texto | anthropic-erros | Long requests | 15/10/2026 | registrado na documentação | Consider using the streaming Messages API or Message Batches API for long-running requests, especially those over 10 minutes. |
| 2.3-T7 | 2.3 | texto | openai-streaming | Streaming responses | 15/10/2026 | registrado na documentação | This guide focuses on HTTP streaming (stream=true) over server-sent events (SSE). |
| 2.3-T8 | 2.3 | texto | mdn-sse | Sending events from the server | 15/10/2026 | registrado na documentação | The server-side script that sends events needs to respond using the MIME type text/event-stream. |
| 2.3-T9 | 2.3 | texto | ollama-api | Convenções (streaming) | 15/10/2026 | registrado na documentação | Certain endpoints stream responses as JSON objects. |
| 2.3-T10 | 2.3 | texto | ollama-api | Generate a completion (parâmetros) | 15/10/2026 | registrado na documentação | `stream`: if `false` the response will be returned as a single response object, rather than a stream of objects |
| 2.3-T11 | 2.3 | texto | ollama-api | Generate a completion (resposta) | 15/10/2026 | registrado na documentação | `load_duration`: time spent in nanoseconds loading the model |
| 2.3-T12 | 2.3 | texto | ollama-api | Generate a completion (parâmetros) | 15/10/2026 | registrado na documentação | `keep_alive`: controls how long the model will stay loaded into memory following the request |
| 2.3-T13 | 2.3 | texto | llamacpp-servidor | Opções de /completion | 15/10/2026 | registrado na documentação | `t_max_predict_ms`: Set a time limit in milliseconds for the prediction (a.k.a. text-generation) phase. |
| 2.3-T14 | 2.3 | texto | llamacpp-servidor | Opções de /completion | 15/10/2026 | registrado na documentação | measured since the first token was generated |
| 2.3-T15 | 2.3 | texto | anthropic-streaming | Exemplo de fluxo (message_delta) | 15/10/2026 | registrado na documentação | data: {"type": "message_delta", "delta": {"stop_reason": "end_turn" |

## Unidade 2.4

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 2.4-T1 | 2.4 | texto | anthropic-limites | Rate limits | 15/10/2026 | registrado na documentação | Short bursts of requests can exceed the limit and trigger rate limit errors. |
| 2.4-T2 | 2.4 | texto | anthropic-limites | Rate limits | 15/10/2026 | registrado na documentação | The API uses the token bucket algorithm to do rate limiting. |
| 2.4-T3 | 2.4 | texto | anthropic-limites | Rate limits | 15/10/2026 | registrado na documentação | If you exceed any of the rate limits you will get a 429 error describing which rate limit was exceeded. |
| 2.4-T4 | 2.4 | texto | anthropic-limites | Rate limits | 15/10/2026 | registrado na documentação | When the response has a retry-after header, wait that many seconds before retrying. |
| 2.4-T5 | 2.4 | texto | anthropic-limites | Spend cap | 15/10/2026 | registrado na documentação | but the response has no retry-after header. |
| 2.4-T6 | 2.4 | texto | anthropic-limites | Spend cap | 15/10/2026 | registrado na documentação | Retrying, including the SDK's automatic retries, fails until access resumes. |
| 2.4-T7 | 2.4 | texto | anthropic-limites | Acceleration limits | 15/10/2026 | registrado na documentação | To avoid hitting acceleration limits, ramp up your traffic gradually and maintain consistent usage patterns. |
| 2.4-T8 | 2.4 | texto | anthropic-erros | HTTP errors (500) | 15/10/2026 | registrado na documentação | Retry the request with exponential backoff |
| 2.4-T9 | 2.4 | texto | anthropic-erros | HTTP errors (504) | 15/10/2026 | registrado na documentação | The request timed out while processing. |
| 2.4-T10 | 2.4 | texto | anthropic-erros | HTTP errors (529) | 15/10/2026 | registrado na documentação | The API is temporarily overloaded. |
| 2.4-T11 | 2.4 | texto | openai-limites | Rate limit headers | 15/10/2026 | registrado na documentação | The minimum number of seconds to wait before retrying a temporary rate-limit error, when present. |
| 2.4-T12 | 2.4 | texto | openai-limites | Handling errors | 15/10/2026 | registrado na documentação | Follow Retry-After when it’s present, reduce your request rate, and then increase it gradually. |
| 2.4-T13 | 2.4 | texto | openai-limites | Handling errors | 15/10/2026 | registrado na documentação | If Retry-After is missing, increase the delay between retries and add a small random delay. |
| 2.4-T14 | 2.4 | texto | openai-erros | Rate limits and spend | 15/10/2026 | registrado na documentação | Retrying billing, spend, or quota errors won’t restore API access. |
| 2.4-T15 | 2.4 | texto | openai-erros | 429 - Rate limit reached | 15/10/2026 | registrado na documentação | If it’s missing, use exponential backoff with jitter and limit the number of retries. |
| 2.4-T16 | 2.4 | texto | rfc6585 | §4 429 Too Many Requests | RFC 6585, abr/2012 | registrado na norma | The 429 status code indicates that the user has sent too many requests in a given amount of time ("rate limiting"). |
| 2.4-T17 | 2.4 | texto | rfc6585 | §4 | RFC 6585, abr/2012 | registrado na norma | MAY include a Retry-After header indicating how long to wait before making a new request. |
| 2.4-T18 | 2.4 | texto | rfc9110 | §15.6.4 503 Service Unavailable | RFC 9110, jun/2022 | registrado na norma | is currently unable to handle the request due to a temporary overload or scheduled maintenance |
| 2.4-T19 | 2.4 | texto | rfc9110 | §9.2.2 Idempotent Methods | RFC 9110, jun/2022 | registrado na norma | A request method is considered "idempotent" if the intended effect on the server of multiple identical requests with that method is the same as the effect for a single such request. |
| 2.4-T20 | 2.4 | texto | rfc9110 | §9.2.2 | RFC 9110, jun/2022 | registrado na norma | unless it has some means to know that the request semantics are actually idempotent |
| 2.4-T21 | 2.4 | texto | aws-tentativas | Retries and backoff | 15/10/2026 | registrado na documentação | A timeout or failure doesn't necessarily mean that side effects haven't happened. |
| 2.4-T22 | 2.4 | texto | aws-tentativas | Deciding when to retry | 15/10/2026 | registrado na documentação | APIs with side effects aren't safe to retry unless they provide idempotency. |
| 2.4-T23 | 2.4 | texto | aws-tentativas | Jitter | 15/10/2026 | registrado na documentação | Jitter adds some amount of randomness to the backoff to spread the retries around in time. |
| 2.4-T24 | 2.4 | texto | aws-tentativas | Timeouts | 15/10/2026 | registrado na documentação | A best practice in Amazon is to set a timeout on any remote call |
| 2.4-T25 | 2.4 | texto | sre-cascata | Missed RPC deadlines | 15/10/2026 | registrado na documentação | The work the server did to respond is then wasted, and clients may retry the RPCs, leading to even more overload. |
| 2.4-T26 | 2.4 | texto | anthropic-limites | Reaching your spend cap | 15/10/2026 | registrado na documentação | "type": "error", "error": { "type": "rate_limit_error", "message": |
| 2.4-T27 | 2.4 | texto | openai-erros | 429 - slow_down | 15/10/2026 | registrado na documentação | indicates that your request rate increased faster than the service can safely handle. |
| 2.4-T28 | 2.4 | texto | anthropic-erros | HTTP errors (529) | 15/10/2026 | registrado na documentação | 529 errors can occur when the API experiences high traffic across all users. |
| 2.4-T29 | 2.4 | texto | rfc9110 | §15.5 Client Error 4xx | RFC 9110, jun/2022 | registrado na norma | The 4xx (Client Error) class of status code indicates that the client seems to have erred. |
| 2.4-T30 | 2.4 | texto | rfc9110 | §15.6 Server Error 5xx | RFC 9110, jun/2022 | registrado na norma | The 5xx (Server Error) class of status code indicates that the server is aware that it has erred or is incapable of performing the requested method. |
| 2.4-T31 | 2.4 | texto | rfc9110 | §10.2.3 Retry-After | RFC 9110, jun/2022 | registrado na norma | The Retry-After field value can be either an HTTP-date or a number of seconds to delay after receiving the response. |
| 2.4-T32 | 2.4 | texto | anthropic-limites | Rate limits | 15/10/2026 | registrado na documentação | your capacity is continuously replenished up to your maximum limit, rather than being reset at fixed intervals. |
| 2.4-C1 | 2.4 | caso | router-main | pedido repetido (request_id) | Cópia de 15/10/2026 | verificado no código local | raise HTTPException(status_code=409, detail='request_id já usado para outro pedido ou contexto') |
| 2.4-C2 | 2.4 | caso | router-main | pedido concluído repetido | Cópia de 15/10/2026 | verificado no código local | if saved['status'] == 'concluido' and saved['response']: |
| 2.4-C3 | 2.4 | caso | router-main | pedido repetido ainda em curso | Cópia de 15/10/2026 | verificado no código local | detail=f"pedido {saved['status']}; confira histórico e estado real antes de retomar" |
| 2.4-C6 | 2.4 | caso | router-main | linha 893 | Cópia de 15/10/2026 | verificado no código local | return DispatchResponse(**json.loads(saved['response'])) |
| 2.4-C4 | 2.4 | caso | pay-webhook-route | registro de evento repetido | Cópia de 15/10/2026 | verificado no código local | eventId já processado: |
| 2.4-C5 | 2.4 | caso | pay-webhook-route | comentário sobre repetição | Cópia de 15/10/2026 | verificado no código local | Registramos cada evento e ignoramos repetições já processadas. |

## Unidade 2.5

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 2.5-T1 | 2.5 | texto | anthropic-mensagens-uso | Mensagens: conversa de vários turnos | 15/10/2026 | registrado na documentação | you always send the full conversational history to the API. |
| 2.5-T2 | 2.5 | texto | openai-estado | Conversations API | 15/10/2026 | registrado na documentação | persist conversation state as a long-running object with its own durable identifier |
| 2.5-T3 | 2.5 | texto | openai-erros | previous_response_not_found | 15/10/2026 | registrado na documentação | The previous_response_id cannot be resolved from available state. |
| 2.5-T4 | 2.5 | texto | openai-erros | previous_response_not_found | 15/10/2026 | registrado na documentação | Retry with full input context and previous_response_id set to null. |
| 2.5-T5 | 2.5 | texto | contexto-de-estudo-ap-ai-router | §6 (contexto, ferramentas e continuidade) | Contexto de 13/10/2026 | registrado no contexto | O histórico ativo é preservado; não presumir compactação semântica ou redução de tokens por bifurcar a conversa. |
| 2.5-T6 | 2.5 | texto | contexto-de-estudo-nanda-mac | §8 (roadmap documental de 09/10) | Contexto de 13/10/2026 | registrado no contexto | propõe histórico vinculado ao usuário, prompts/ferramentas por função, persistência de conversas, controle de orçamento e liberação gradual. |
| 2.5-T7 | 2.5 | texto | contexto-de-estudo-nanda-mac | §8 (decisões abertas) | Contexto de 13/10/2026 | registrado no contexto | O que será memória pessoal, contexto compartilhado da empresa ou informação acessível só a uma área. |
| 2.5-T8 | 2.5 | texto | contexto-de-estudo-nanda-mac | §8 (decisões abertas) | Contexto de 13/10/2026 | registrado no contexto | Políticas de uso, conservação de histórico, observabilidade e tratamento de falhas apropriadas à aplicação. |
| 2.5-T9 | 2.5 | texto | anthropic-erros | Request IDs | 15/10/2026 | registrado na documentação | When contacting support about a specific request, include this ID |
| 2.5-C1 | 2.5 | caso | router-database | SCHEMA, linha 29 | Cópia de 15/10/2026 | verificado no código local | PRAGMA journal_mode=WAL; |
| 2.5-C2 | 2.5 | caso | router-database | SCHEMA, linha 62 | Cópia de 15/10/2026 | verificado no código local | CREATE TABLE IF NOT EXISTS dispatch_requests ( |
| 2.5-C3 | 2.5 | caso | router-database | SCHEMA, linha 68 | Cópia de 15/10/2026 | verificado no código local | fingerprint TEXT NOT NULL, |
| 2.5-C4 | 2.5 | caso | router-database | SCHEMA, linha 33 | Cópia de 15/10/2026 | verificado no código local | CREATE TABLE IF NOT EXISTS conversations ( |
| 2.5-C5 | 2.5 | caso | router-database | SCHEMA, linha 43 | Cópia de 15/10/2026 | verificado no código local | CREATE TABLE IF NOT EXISTS messages ( |
| 2.5-C6 | 2.5 | caso | router-database | linha 378 | Cópia de 15/10/2026 | verificado no código local | Reinício não repete ações cujo resultado é desconhecido. |
| 2.5-C7 | 2.5 | caso | router-database | linha 380 | Cópia de 15/10/2026 | verificado no código local | UPDATE dispatch_requests SET status = 'interrompido' WHERE status = 'executando' |
| 2.5-C8 | 2.5 | caso | router-main | linha 198 | Cópia de 15/10/2026 | verificado no código local | await db.interrupt_dispatches() |
| 2.5-C9 | 2.5 | caso | router-database | linha 641 | Cópia de 15/10/2026 | verificado no código local | Recupera jobs sem dono; etapas com efeitos incertos não são repetidas. |

## Unidade 2.6

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 2.6-T1 | 2.6 | texto | llamacpp-servidor | Opções do servidor | 15/10/2026 | registrado na documentação | number of server slots (default: -1, -1 = auto) |
| 2.6-T2 | 2.6 | texto | llamacpp-servidor | Opções do servidor | 15/10/2026 | registrado na documentação | whether to enable continuous batching (a.k.a dynamic batching) (default: enabled) |
| 2.6-T3 | 2.6 | texto | llamacpp-servidor | GET /props | 15/10/2026 | registrado na documentação | `total_slots` - the total number of slots for process requests |
| 2.6-T4 | 2.6 | texto | llamacpp-servidor | Métricas (/metrics) | 15/10/2026 | registrado na documentação | Number of requests deferred. |
| 2.6-T5 | 2.6 | texto | llamacpp-servidor | Loading model | 15/10/2026 | registrado na documentação | "message": "Loading model", "type": "unavailable_error" |
| 2.6-T6 | 2.6 | texto | sre-cascata | Queue Management | 15/10/2026 | registrado na documentação | Queued requests consume memory and increase latency. |
| 2.6-T7 | 2.6 | texto | sre-cascata | Queue Management | 15/10/2026 | registrado na documentação | it is usually better to have small queue lengths relative to the thread pool size |
| 2.6-T8 | 2.6 | texto | sre-cascata | Load Shedding | 15/10/2026 | registrado na documentação | one effective approach is to return an HTTP 503 (service unavailable) to any incoming request when there are more than a given |
| 2.6-T9 | 2.6 | texto | sre-sobrecarga | Client-Side Throttling | 15/10/2026 | registrado na documentação | When a client detects that a significant portion of its recent requests have been rejected due to "out of quota" errors, it starts self-regulating and caps the amount of outgoing traffic it generates. |
| 2.6-T10 | 2.6 | texto | sre-cascata | Cascading failures | 15/10/2026 | registrado na documentação | A cascading failure is a failure that grows over time as a result of positive feedback. |
| 2.6-T11 | 2.6 | texto | openai-limites | Rate limits | 15/10/2026 | registrado na documentação | Rate limits can be hit across any of the options depending on what occurs first |
| 2.6-T12 | 2.6 | texto | docs09 | §2 | Atualização de 2026 (diretrizes locais) | registrado nas diretrizes locais | Adotar bancos vetoriais, orquestradores em grafo ou filas distribuídas sem validação prévia de necessidade com SDK nativo. |
| 2.6-T13 | 2.6 | texto | contexto-de-estudo-nanda-mac | §8 (decisões abertas) | Contexto de 13/10/2026 | registrado no contexto | Onde modelos locais serão executados, como será a concorrência e qual capacidade será demonstrada por avaliação. |
| 2.6-T14 | 2.6 | texto | contexto-de-estudo-nanda-mac | §8 | Contexto de 13/10/2026 | registrado no contexto | Não transformar “privacidade absoluta”, “ausência de filas” |
| 2.6-T15 | 2.6 | texto | contexto-de-estudo-nanda-mac | §8 | Contexto de 13/10/2026 | registrado no contexto | aqui são expectativas a verificar por implementação, configuração, evidências e condições do caso. |
| 2.6-C1 | 2.6 | caso | router-main | linha 126 | Cópia de 15/10/2026 | verificado no código local | _gpu_lock = asyncio.Lock() |
| 2.6-C2 | 2.6 | caso | router-main | linha 132 | Cópia de 15/10/2026 | verificado no código local | Serializa inferência local e mantém o recurso até o processo filho terminar. |
| 2.6-C3 | 2.6 | caso | router-main | linha 127 | Cópia de 15/10/2026 | verificado no código local | _triage_locks: dict[str, asyncio.Lock] = {} |
| 2.6-C4 | 2.6 | caso | router-main | linha 826 | Cópia de 15/10/2026 | verificado no código local | conversa possui operação em andamento; aguarde |
| 2.6-C5 | 2.6 | caso | router-queue-worker | linha 166 | Cópia de 15/10/2026 | verificado no código local | self._task = asyncio.create_task(self._loop()) |
| 2.6-C6 | 2.6 | caso | router-queue-worker | linha 189 | Cópia de 15/10/2026 | verificado no código local | await asyncio.wait_for(self._wake.wait(), timeout=self.deps.poll_seconds) |
