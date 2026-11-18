# Pacote de fontes: Capítulo 16 — Eficiência e economia (17/11/2026)

Data: 17/11/2026. Autoria: deepseek - painel. Cobre as seis unidades do Módulo 16 (`medição → gargalos → eliminar redundância → melhorar ferramentas e contexto → cache e esforço → ponto ótimo de sessão e manutenção`) com a documentação de cache de prompt e de preços da Anthropic e da OpenAI, a visão de cache de contexto do Google Cloud, as APIs de lote dos dois fornecedores, a contagem de tokens da Anthropic e o rastreio de custo do LiteLLM. Contexto e compactação ficam no Capítulo 9, escolha de modelo e esforço no Capítulo 14, ferramentas no Capítulo 10 e operação no Capítulo 15; o capítulo remete a eles e não repete os trechos. Números de preço não entram no texto corrido: o guia trabalha com multiplicadores e pontos de equilíbrio, que envelhecem mais devagar que a tabela.

## 1. Fontes baixadas e como reconferir

Baixar as páginas para uma pasta nova e vazia (`/tmp/cap16-bruto`) e extrair com `python3 -I ferramentas/extrair-texto-web.py`. As páginas da Anthropic e da OpenAI trazem tabelas de preço por modelo; o guia cita apenas os multiplicadores e as regras, nunca os valores, porque mudam com frequência. A página de cache de contexto do Google Cloud descreve o cache implícito (ligado por padrão) e o explícito; os trechos de multiplicador do Google valem a partir da data indicada na própria página e por isso aparecem com a ressalva de data.

| Chave | Fonte pública e endereço efetivo | Hash bruto (16) |
|---|---|---|
| `anthropic-caching` | Anthropic, *Prompt caching* — https://platform.claude.com/docs/en/build-with-claude/prompt-caching | `fd2bf0775ec4d3cc` |
| `anthropic-pricing` | Anthropic, *Pricing* — https://platform.claude.com/docs/en/about-claude/pricing | `2c76555607eafaf0` |
| `anthropic-batch` | Anthropic, *Batch processing* — https://platform.claude.com/docs/en/build-with-claude/batch-processing | `920ffb005a26632c` |
| `anthropic-tokens` | Anthropic, *Token counting* — https://platform.claude.com/docs/en/build-with-claude/token-counting | `427144317fb8c989` |
| `openai-cost` | OpenAI, *Cost optimization* (API Guides) — https://developers.openai.com/api/docs/guides/cost-optimization | `e02427b547b2f05b` |
| `openai-batch` | OpenAI, *Batch API* (API Guides) — https://developers.openai.com/api/docs/guides/batch | `b2928e7f90a2df00` |
| `openai-caching` | OpenAI, *Prompt caching* (API Guides) — https://developers.openai.com/api/docs/guides/prompt-caching | `f936fb3b087c0359` |
| `gcp-caching` | Google Cloud, *Context caching overview* — https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview | `090b754ff70f743b` |
| `litellm-cost` | LiteLLM, *Cost Tracking* — https://docs.litellm.ai/docs/proxy/cost_tracking | `9ef50e7d051b8ae0` |

Comando de conferência: `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-16-eficiencia-e-economia-2026-11-17.md --textos /tmp/cap16-textos --projeto .`

## 2. Fontes e trechos

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| AT-01 | 16.1 Medição | texto | anthropic-tokens | Introdução | Anthropic, consultada em 17/11/2026 | registrado na documentação | The token count is an estimate. In some cases, the actual number of input tokens used when creating a message might differ by a small amount. |
| AT-02 | 16.1 Medição | texto | anthropic-tokens | Introdução | Anthropic, consultada em 17/11/2026 | registrado na documentação | Count tokens before sending requests. |
| AT-03 | 16.1 Medição | texto | anthropic-tokens | Perguntas frequentes | Anthropic, consultada em 17/11/2026 | registrado na documentação | token counting provides an estimate without using caching logic |
| LC-01 | 16.1 Medição | texto | litellm-cost | Introdução | consultada em 17/11/2026 | registrado na documentação | LiteLLM automatically tracks spend for all known models. |
| LC-02 | 16.1 Medição | texto | litellm-cost | Cabeçalhos de resposta | consultada em 17/11/2026 | registrado na documentação | Expect to see x-litellm-response-cost in the response headers with calculated cost |
| LC-03 | 16.1 Medição | texto | litellm-cost | Introdução | consultada em 17/11/2026 | registrado na documentação | Sync model pricing data from GitHub to ensure accurate cost tracking. |
| LC-04 | 16.1 Medição | texto | litellm-cost | Introdução | consultada em 17/11/2026 | registrado na documentação | one WARNING line in the proxy log naming the model group, the deployment's pricing entry and the pricing key it is missing |
| OC-01 | 16.2 Gargalos | texto | openai-cost | Introdução | OpenAI, consultada em 17/11/2026 | registrado na documentação | Reducing tokens and requests can lower costs and shorten response times. |
| OC-02 | 16.2 Gargalos | texto | openai-cost | Cost and latency | OpenAI, consultada em 17/11/2026 | registrado na documentação | Reduce requests: Limit the number of necessary requests to complete tasks. |
| OC-03 | 16.2 Gargalos | texto | openai-cost | Cost and latency | OpenAI, consultada em 17/11/2026 | registrado na documentação | Minimize tokens: Lower the number of input tokens and optimize for shorter model outputs. |
| OC-04 | 16.2 Gargalos | texto | openai-cost | Cost and latency | OpenAI, consultada em 17/11/2026 | registrado na documentação | Select a smaller model: Use models that balance reduced costs and latency with maintained accuracy. |
| OK-01 | 16.2 Gargalos | texto | openai-caching | Measure and optimize | OpenAI, consultada em 17/11/2026 | registrado na documentação | Measure actual cache performance. |
| OK-02 | 16.2 Gargalos | texto | openai-caching | Measure and optimize | OpenAI, consultada em 17/11/2026 | registrado na documentação | Track the token cache-hit rate by dividing total cached tokens by total input tokens, aggregating both counts by user, workspace, day, or another useful grouping. |
| OK-03 | 16.2 Gargalos | texto | openai-caching | Measure and optimize | OpenAI, consultada em 17/11/2026 | registrado na documentação | An example deployment using these principles reported a token cache-hit rate >90%. |
| OB-01 | 16.3 Eliminar redundância | texto | openai-batch | Introdução | OpenAI, consultada em 17/11/2026 | registrado na documentação | Learn how to use OpenAI’s Batch API to send asynchronous groups of requests with 50% lower costs, a queued-token limit separate from per-minute limits, and a clear 24-hour turnaround time. |
| OB-02 | 16.3 Eliminar redundância | texto | openai-batch | Benefícios | OpenAI, consultada em 17/11/2026 | registrado na documentação | Better cost efficiency: 50% cost discount compared to synchronous APIs |
| AB-01 | 16.3 Eliminar redundância | texto | anthropic-batch | Introdução | Anthropic, consultada em 17/11/2026 | registrado na documentação | This approach is well-suited to tasks that do not require immediate responses, with most batches finishing in less than 1 hour while reducing costs by 50 percent and increasing throughput. |
| AB-02 | 16.3 Eliminar redundância | texto | anthropic-batch | Como funciona | Anthropic, consultada em 17/11/2026 | registrado na documentação | The system processes each batch as fast as possible, with most batches completing within 1 hour. |
| AB-03 | 16.3 Eliminar redundância | texto | anthropic-batch | Como funciona | Anthropic, consultada em 17/11/2026 | registrado na documentação | Batches expire if processing does not complete within 24 hours. |
| AB-04 | 16.3 Eliminar redundância | texto | anthropic-batch | Como funciona | Anthropic, consultada em 17/11/2026 | registrado na documentação | Batch results are available for 29 days after creation. |
| AP-01 | 16.3 Eliminar redundância | texto | anthropic-pricing | Batch processing | Anthropic, consultada em 17/11/2026 | registrado na documentação | The Batch API allows asynchronous processing of large volumes of requests with a 50 percent discount on both input and output tokens. |
| GC-01 | 16.4 Melhorar ferramentas e contexto | texto | gcp-caching | Dicas para acerto de cache | Google Cloud, consultada em 17/11/2026 | registrado na documentação | Place large and common contents at the beginning of your prompt. |
| GC-02 | 16.4 Melhorar ferramentas e contexto | texto | gcp-caching | Dicas para acerto de cache | Google Cloud, consultada em 17/11/2026 | registrado na documentação | Send requests with a similar prefix in a short amount of time. |
| OK-04 | 16.4 Melhorar ferramentas e contexto | texto | openai-caching | Boas práticas | OpenAI, consultada em 17/11/2026 | registrado na documentação | Choose breakpoints deliberately. Place explicit markers at the end of stable content. |
| OK-05 | 16.4 Melhorar ferramentas e contexto | texto | openai-caching | Boas práticas | OpenAI, consultada em 17/11/2026 | registrado na documentação | Use explicit-only mode to avoid unnecessary cache writes for changing suffixes. |
| AC-01 | 16.4 Melhorar ferramentas e contexto | texto | anthropic-pricing | Cache de prompt | Anthropic, consultada em 17/11/2026 | registrado na documentação | Prompt caching reduces costs and latency by reusing previously processed portions of your prompt across API calls. |
| AC-02 | 16.5 Cache e esforço | texto | anthropic-caching | Como funciona | Anthropic, consultada em 17/11/2026 | registrado na documentação | By default, the cache has a 5-minute lifetime. The cache is refreshed for no additional cost each time the cached content is used. |
| AC-03 | 16.5 Cache e esforço | texto | anthropic-caching | Como funciona | Anthropic, consultada em 17/11/2026 | registrado na documentação | If 5 minutes is too short, you can use a 1-hour cache duration at additional cost (see Pricing). |
| AC-04 | 16.5 Cache e esforço | texto | anthropic-caching | Preços | Anthropic, consultada em 17/11/2026 | registrado na documentação | Cache write tokens with a 5-minute TTL are 1.25 times the base input tokens price. |
| AC-05 | 16.5 Cache e esforço | texto | anthropic-caching | Preços | Anthropic, consultada em 17/11/2026 | registrado na documentação | Cache write tokens with a 1-hour TTL are 2 times the base input tokens price. |
| AC-06 | 16.5 Cache e esforço | texto | anthropic-caching | Preços | Anthropic, consultada em 17/11/2026 | registrado na documentação | Cache read tokens are 0.1 times the base input tokens price (see the table footnote for per-model exceptions). |
| AC-07 | 16.5 Cache e esforço | texto | anthropic-caching | Preços | Anthropic, consultada em 17/11/2026 | registrado na documentação | These multipliers stack with other pricing modifiers such as the Batch API discount, long context pricing, and data residency. |
| AP-02 | 16.5 Cache e esforço | texto | anthropic-pricing | Cache de prompt | Anthropic, consultada em 17/11/2026 | registrado na documentação | 5-minute duration (1.25x write): after one cache read |
| AP-03 | 16.5 Cache e esforço | texto | anthropic-pricing | Cache de prompt | Anthropic, consultada em 17/11/2026 | registrado na documentação | 1-hour duration (2x write): after two cache reads |
| AP-04 | 16.5 Cache e esforço | texto | anthropic-pricing | Cache de prompt | Anthropic, consultada em 17/11/2026 | registrado na documentação | Cache write tokens are charged when content is first stored. Cache read tokens are charged when a subsequent request retrieves the cached content. |
| OK-06 | 16.5 Cache e esforço | texto | openai-caching | Introdução | OpenAI, consultada em 17/11/2026 | registrado na documentação | Cheaper input tokens: Pay the model’s reduced cached-input rate for reused tokens, discounted up to 95%. |
| GC-03 | 16.5 Cache e esforço | texto | gcp-caching | Cache implícito | Google Cloud, consultada em 17/11/2026 | registrado na documentação | Implicit caching provides a 90% discount on cached tokens compared to standard input tokens. |
| GC-04 | 16.5 Cache e esforço | texto | gcp-caching | Cache implícito | Google Cloud, consultada em 17/11/2026 | registrado na documentação | A cached prefix expires no later than 24 hours after it's created, and most entries are evicted earlier. |
| GC-05 | 16.5 Cache e esforço | texto | gcp-caching | Custos de armazenamento | Google Cloud, consultada em 17/11/2026 | registrado na documentação | For explicit caching, there are also storage costs based on how long caches are stored. |
| AP-05 | 16.6 Ponto ótimo de sessão e manutenção | texto | anthropic-pricing | Preços de contexto longo | Anthropic, consultada em 17/11/2026 | registrado na documentação | Prompt caching and batch processing discounts apply at standard rates across the full context window. |
| AP-06 | 16.6 Ponto ótimo de sessão e manutenção | texto | anthropic-pricing | Preços de uso de ferramentas | Anthropic, consultada em 17/11/2026 | registrado na documentação | A request’s prompt length counts all of its input tokens, including cache reads and cache writes. |
| LC-05 | 16.6 Ponto ótimo de sessão e manutenção | texto | litellm-cost | Introdução | consultada em 17/11/2026 | registrado na documentação | Use the step-by-step workflow in Debugging a cost discrepancy |
| OC-05 | 16.6 Ponto ótimo de sessão e manutenção | texto | openai-cost | Flex processing | OpenAI, consultada em 17/11/2026 | registrado na documentação | Get significantly lower costs for Chat Completions or Responses requests in exchange for slower response times and occasional resource unavailability. |
| AT-04 | 16.1 Medição | texto | anthropic-tokens | Tokenizadores | Anthropic, consultada em 17/11/2026 | registrado na documentação | Recount prompts against the model you plan to use rather than reusing counts measured against earlier models. |
| LC-06 | 16.1 Medição | texto | litellm-cost | Requests that price to $0 | consultada em 17/11/2026 | registrado na documentação | the Prometheus counter litellm_zero_cost_requests_total |
| AB-05 | 16.3 Eliminar redundância | texto | anthropic-batch | Spend limit | Anthropic, consultada em 17/11/2026 | registrado na documentação | batches might go slightly over the spend limit configured in the Claude Console for your Workspace. |
| AB-06 | 16.3 Eliminar redundância | texto | anthropic-batch | Rate limits | Anthropic, consultada em 17/11/2026 | registrado na documentação | Rate limits apply to both Batches API HTTP requests and the number of requests within a batch waiting to be processed. |
| AC-08 | 16.4 Melhorar ferramentas e contexto | texto | anthropic-caching | Breakpoints | Anthropic, consultada em 17/11/2026 | registrado na documentação | You can define up to 4 cache breakpoints |
| GC-06 | 16.5 Cache e esforço | texto | gcp-caching | Implicit caching | Google Cloud, consultada em 17/11/2026 | registrado na documentação | Implicit caching: Automatic caching enabled by default that provides cost savings when cache hits occur. |

Pendência declarada: o guia não fixa valores de preço nem limites por modelo. Os pontos de equilíbrio do cache (uma leitura para o cache de 5 minutos, duas para o de 1 hora) vêm da página de preços da Anthropic e valem para os multiplicadores ali descritos; outros fornecedores usam contas próprias. O "ponto ótimo de sessão" não tem fonte primária: é um método de estimativa marcado como proposta didática.
