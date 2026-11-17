# Pacote de fontes — Revisão 1 (técnicas e estudos além do que o operador desenvolveu)

Data: 15/10/2026. Autoria: claude - pessoal (Sonnet 5.5, effort High declarado pelo operador). Apoia as inserções aprovadas em 15/10/2026 nos capítulos 1 e 2 (ver `revisao-1-cobertura-alem-do-que-foi-desenvolvido.md`). Não altera o guia HTML.

Formato: igual ao dos pacotes dos capítulos 1 e 2. Cada linha traz um trecho literal copiado da fonte extraída; `ferramentas/conferir-trechos.py` confere cada trecho contra o texto da fonte. Páginas baixadas com `curl -L` para pasta própria e vazia e convertidas por `ferramentas/extrair-texto-web.py` em 15/10/2026. Páginas de documentação mudam: valem como estado de 15/10/2026 e não trazem data própria de publicação (as da Anthropic em `platform.claude.com`).

Qualificadores: *registrado na documentação*, *registrado na norma* (aqui: rascunho da IETF), *registrado em artigo* (artigo científico ou relatório técnico), *proposta didática*.

Cuidados para a redação:
- Nenhum valor numérico de preço, desconto ou tempo de cache entra no livro como fato fixo; só a forma ("leitura de cache custa uma fração da entrada normal").
- O *Idempotency-Key* é um rascunho da IETF **expirado**, não um padrão.
- O estudo da Chroma testa tarefas simples e controladas e **não explica o mecanismo** da piora; *Lost in the Middle* é de 2023 e testou modelos daquela época.
- Ganhos de velocidade de artigos (2 a 3 vezes, 2 a 4 vezes) valem para o teste dos autores, não para qualquer modelo.

## R1 — Raciocínio, MoE, contexto longo (capítulo 1)

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| R1-T1 | 1.4 | texto | anthropic-thinking | Introdução | Anthropic, *Thinking*, 15/10/2026 | registrado na documentação | the tokens Claude spends reasoning are billed as output tokens, even when the thinking text isn't returned to you, and they count toward `max_tokens` alongside the response text |
| R1-T1b | 2.2 | texto | anthropic-thinking | Cobrança | Anthropic, *Thinking*, 15/10/2026 | registrado na documentação | The billed output token count does not match the count of tokens you see in the response |
| R1-T2 | 1.4 | texto | anthropic-thinking | Ligar o raciocínio | Anthropic, *Thinking*, 15/10/2026 | registrado na documentação | which lets Claude determine when and how deeply to think based on the request |
| R1-T3 | 1.4 | texto | arxiv-deepseek-r1 | Resumo | DeepSeek-AI, arXiv:2501.12948, v2 | registrado em artigo | the reasoning abilities of LLMs can be incentivized through pure reinforcement learning (RL), obviating the need for human-labeled reasoning trajectories |
| R1-T3b | 1.4 | texto | arxiv-deepseek-r1 | Resumo | DeepSeek-AI, arXiv:2501.12948, v2 | registrado em artigo | the trained model achieves superior performance on verifiable tasks such as mathematics, coding competitions, and STEM fields |
| R1-T3c | 1.4 | texto | arxiv-deepseek-r1 | Resumo | DeepSeek-AI, arXiv:2501.12948, v2 | registrado em artigo | advanced reasoning patterns, such as self-reflection, verification, and dynamic strategy adaptation |
| R1-T4 | 1.2 | texto | arxiv-mixtral | Resumo | Jiang et al., arXiv:2401.04088, 08/01/2024 | registrado em artigo | For every token, at each layer, a router network selects two experts to process the current state and combine their outputs |
| R1-T5 | 1.2 | texto | arxiv-mixtral | Resumo | Jiang et al., arXiv:2401.04088, 08/01/2024 | registrado em artigo | each token has access to 47B parameters, but only uses 13B active parameters during inference |
| R1-T6 | 1.3 | texto | arxiv-lost-in-the-middle | Resumo | Liu et al., arXiv:2307.03172, 06/07/2023 | registrado em artigo | performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts, even for explicitly long-context models |
| R1-T7 | 1.3 | texto | chroma-context-rot | Introdução | Chroma, *Context Rot*, 14/07/2025 | registrado em artigo | model performance degrades as input length increases, often in surprising and non-uniform ways |
| R1-T7b | 1.3 | texto | chroma-context-rot | Resumo | Chroma, *Context Rot*, 14/07/2025 | registrado em artigo | An evaluation across 18 LLMs, including leading closed-source and open-weights models, revealing nonuniform performance with increasing input length |
| R1-T8 | 1.3 | texto | chroma-context-rot | Limites | Chroma, *Context Rot*, 14/07/2025 | registrado em artigo | We also do not explain the mechanisms behind this performance degradation |
| R1-T9 | 1.3 | texto | anthropic-context-engineering | Princípio | Anthropic, 29/09/2025 | registrado na documentação | good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome |
| R1-T10 | 1.3 | texto | anthropic-context-engineering | Compactação | Anthropic, 29/09/2025 | registrado na documentação | Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary |
| R1-T11 | 1.6 | texto | anthropic-building-effective-agents | Resumo | Anthropic, 19/12/2024 | registrado na documentação | we recommend finding the simplest solution possible, and only increasing complexity when needed |
| R1-T12 | 1.6 | texto | anthropic-building-effective-agents | Conclusão | Anthropic, 19/12/2024 | registrado na documentação | add multi-step agentic systems only when simpler solutions fall short |
| R1-T13 | 1.5 | texto | arxiv-speculative | Resumo | Leviathan et al., arXiv:2211.17192, 30/11/2022 | registrado em artigo | we can make exact decoding from the large models faster, by running them in parallel on the outputs of the approximation models |
| R1-T13b | 1.5 | texto | arxiv-speculative | Resumo | Leviathan et al., arXiv:2211.17192, 30/11/2022 | registrado em artigo | We demonstrate it on T5-XXL and show a 2X-3X acceleration compared to the standard T5X implementation, with identical outputs |
| R1-T14 | 1.5 | texto | arxiv-pagedattention | Resumo | Kwon et al., arXiv:2309.06180, 12/09/2023 | registrado em artigo | near-zero waste in KV cache memory |
| R1-T14b | 1.5 | texto | arxiv-pagedattention | Resumo | Kwon et al., arXiv:2309.06180, 12/09/2023 | registrado em artigo | vLLM improves the throughput of popular LLMs by 2-4 |
| R1-T15 | 1.2 | texto | arxiv-lora | Resumo | Hu et al., arXiv:2106.09685, 17/06/2021 | registrado em artigo | freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture, greatly reducing the number of trainable parameters for downstream tasks |

## R2 — Capítulo 2: arquitetura

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| R2-T1 | 2.2 | texto | anthropic-structured-outputs | Garantias | Anthropic, *Structured outputs*, 15/10/2026 | registrado na documentação | Structured outputs guarantee schema-compliant responses through constrained decoding |
| R2-T2 | 2.2 | texto | anthropic-structured-outputs | Recusa | Anthropic, *Structured outputs*, 15/10/2026 | registrado na documentação | The output may not match your schema because the refusal message takes precedence over schema constraints |
| R2-T3 | 2.2 | texto | anthropic-structured-outputs | Corte | Anthropic, *Structured outputs*, 15/10/2026 | registrado na documentação | Token limit reached |
| R2-T4 | 2.3 | texto | anthropic-prompt-caching | Introdução | Anthropic, *Prompt caching*, 15/10/2026 | registrado na documentação | This significantly reduces processing time and costs for repetitive tasks or prompts with consistent elements |
| R2-T5 | 2.3 | texto | anthropic-prompt-caching | Vida útil | Anthropic, *Prompt caching*, 15/10/2026 | registrado na documentação | By default, the cache has a 5-minute lifetime |
| R2-T5b | 2.3 | texto | anthropic-prompt-caching | Correspondência | Anthropic, *Prompt caching*, 15/10/2026 | registrado na documentação | Cache hits require 100% identical prompt segments |
| R2-T6 | 2.3 | texto | anthropic-prompt-caching | Preço | Anthropic, *Prompt caching*, 15/10/2026 | registrado na documentação | Cache read tokens are 0.1 times the base input tokens price |
| R2-T7 | 2.3 | texto | anthropic-batch | Introdução | Anthropic, *Batch processing*, 15/10/2026 | registrado na documentação | most batches finishing in less than 1 hour while reducing costs by 50% and increasing throughput |
| R2-T8 | 2.4 | texto | ietf-idempotency-key | Resumo | IETF, *draft-ietf-httpapi-idempotency-key-header* | registrado na norma | The HTTP Idempotency-Key request header field can be used to make non-idempotent HTTP methods such as POST or PATCH fault-tolerant |
| R2-T9 | 2.4 | texto | ietf-idempotency-key | Estado | IETF, *draft-ietf-httpapi-idempotency-key-header* | registrado na norma | Expired Internet-Draft |
| R2-T10 | 2.6 | texto | fowler-circuit-breaker | Ideia básica | Fowler, *CircuitBreaker*, 06/03/2014 | registrado em artigo | Once the failures reach a certain threshold, the circuit breaker trips, and all further calls to the circuit breaker return with an error, without the protected call being made at all |
| R2-T10b | 2.6 | texto | fowler-circuit-breaker | Reinício | Fowler, *CircuitBreaker*, 06/03/2014 | registrado em artigo | self-resetting behavior by trying the protected call again after a suitable interval, and resetting the breaker should it succeed |
| R2-T11 | 2.6 | texto | fowler-circuit-breaker | Origem | Fowler, *CircuitBreaker*, 06/03/2014 | registrado em artigo | Michael Nygard popularized the Circuit Breaker pattern to prevent this kind of catastrophic cascade |
| R2-T12 | 2.1 | texto | mcp-spec | Visão geral | Model Context Protocol, especificação 2026-07-28 | registrado na documentação | is an open protocol that enables seamless integration between LLM applications and external data sources and tools |
| R2-T13 | 2.1 | texto | mcp-spec | Protocolo base | Model Context Protocol, especificação 2026-07-28 | registrado na documentação | Stateless, self-contained requests |
| R2-T14 | 2.5 | texto | anthropic-multi-agent | Confiabilidade | Anthropic, 13/06/2025 | registrado na documentação | we built systems that can resume from where the agent was when the errors occurred |
| R2-T14b | 2.5 | texto | anthropic-multi-agent | Confiabilidade | Anthropic, 13/06/2025 | registrado na documentação | When errors occur, we can't just restart from the beginning: restarts are expensive and frustrating for users |
| R2-T15 | 2.5 | texto | anthropic-multi-agent | Custo | Anthropic, 13/06/2025 | registrado na documentação | agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats |
