# Pacote de fontes do capítulo 4

Data: 13/11/2026. Autoria: deepseek - conta não verificada (painel). Cobre as fontes citadas no capítulo 4 do guia (33 trechos; C4-25 a C4-33 acrescentados em 14/11/2026). Cada trecho foi conferido contra o texto baixado na mesma data; o resultado do `conferir-trechos.py` está na seção 3.

## 1. Como reconferir

Baixar as fontes para uma pasta vazia e extrair o texto, com as chaves da coluna “Fonte”:

- `arxiv-2005.14165.txt`, `arxiv-2201.11903.txt` e `arxiv-2202.12837.txt` — páginas de resumo em https://arxiv.org/abs/2005.14165, https://arxiv.org/abs/2201.11903 e https://arxiv.org/abs/2202.12837, extraídas com `ferramentas/extrair-texto-web.py`
- `2005.14165.txt`, `2201.11903.txt` e `2202.12837.txt` — PDFs em https://arxiv.org/pdf/2005.14165, https://arxiv.org/pdf/2201.11903 e https://arxiv.org/pdf/2202.12837, convertidos com `pdftotext -layout`
- `anthropic-prompt-best-practices.txt` — https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- `anthropic-token-counting.txt` — https://platform.claude.com/docs/en/build-with-claude/token-counting
- `anthropic-migration-2026-10-21.txt` — https://platform.claude.com/docs/en/api/migration-2026-10-21
- `anthropic-effort.txt` — https://platform.claude.com/docs/en/build-with-claude/effort
- `anthropic-structured-outputs.txt` — https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- `anthropic-working-with-messages.txt` — https://platform.claude.com/docs/en/build-with-claude/working-with-messages
- `anthropic-handling-stop-reasons.txt` — https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons
- `openai-structured-outputs.txt` — https://developers.openai.com/api/docs/guides/structured-outputs
- `openai-prompt-guide.txt` — https://developers.openai.com/api/docs/guides/prompt-engineering
- `json-schema-overview.txt` — https://json-schema.org/overview/what-is-jsonschema

As páginas HTML são extraídas com `python3 -I ferramentas/extrair-texto-web.py --entrada <pasta-bruta> --saida <pasta-textos>`.

Comando: `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-4-2026-11-13.md --textos <pasta> --projeto .`

## 2. Fontes e trechos

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| C4-01 | 4.1 Instruções e exemplos | texto | 2005.14165 | Figura 1.1 | Brown et al., 2020 | registrado no artigo | We use the term “in-context learning” to describe the inner loop of this process, which occurs within the forward-pass upon each sequence. |
| C4-02 | 4.1 Instruções e exemplos | texto | arxiv-2005.14165 | Resumo | Brown et al., 2020 | registrado no artigo | GPT-3 is applied without any gradient updates or fine-tuning, with tasks and few-shot demonstrations specified purely via text interaction with the model. |
| C4-03 | 4.1 Instruções e exemplos | texto | anthropic-prompt-best-practices | Use examples effectively | consultada em 13/11/2026 | registrado na documentação | Examples are one of the most reliable ways to steer Claude’s output format, tone, and structure. |
| C4-04 | 4.1 Instruções e exemplos | texto | anthropic-prompt-best-practices | Use examples effectively | consultada em 13/11/2026 | registrado na documentação | Include 3–5 examples for best results. |
| C4-05 | 4.1 Instruções e exemplos | texto | arxiv-2202.12837 | Resumo | Min et al., 2022 | registrado no artigo | randomly replacing labels in the demonstrations barely hurts performance |
| C4-06 | 4.1 Instruções e exemplos | texto | arxiv-2202.12837 | Resumo | Min et al., 2022 | registrado no artigo | other aspects of the demonstrations are the key drivers of end task performance |
| C4-07 | 4.1 Instruções e exemplos | texto | anthropic-prompt-best-practices | Structure prompts with XML tags | consultada em 13/11/2026 | registrado na documentação | XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs. |
| C4-08 | 4.1 Instruções e exemplos | texto | anthropic-prompt-best-practices | Structure prompts with XML tags | consultada em 13/11/2026 | registrado na documentação | Wrapping each type of content in its own tag (for example, <instructions>, <context>, <input>) reduces misinterpretation. |
| C4-09 | 4.2 Técnicas de prompt com fonte primária | texto | 2201.11903 | Seção 1 | Wei et al., 2022 | registrado no artigo | A chain of thought is a series of intermediate natural language reasoning steps that lead to the final output |
| C4-10 | 4.2 Técnicas de prompt com fonte primária | texto | arxiv-2201.11903 | Resumo | Wei et al., 2022 | registrado no artigo | prompting a 540B-parameter language model with just eight chain of thought exemplars achieves state of the art accuracy on the GSM8K benchmark of math word problems |
| C4-11 | 4.2 Técnicas de prompt com fonte primária | texto | arxiv-2202.12837 | Resumo | Min et al., 2022 | registrado no artigo | they provide a few examples of (1) the label space, (2) the distribution of the input text, and (3) the overall format of the sequence |
| C4-12 | 4.2 Técnicas de prompt com fonte primária | texto | openai-prompt-guide | Prompt engineering | consultado em 13/11/2026 | registrado na documentação | Prompt engineering is the process of writing effective instructions for a model, such that it consistently generates content that meets your requirements. |
| C4-13 | 4.3 Mensagens e papéis | texto | anthropic-working-with-messages | Conversa e histórico | consultada em 13/11/2026 | registrado na documentação | The Messages API is stateless, which means that you always send the full conversational history to the API. |
| C4-14 | 4.3 Mensagens e papéis | texto | anthropic-working-with-messages | Papel de sistema | consultada em 13/11/2026 | registrado na documentação | A mid-conversation system message has the same authority as the top-level system field, but because it is appended to the end of the message history, it does not invalidate any cached prefix that came before it. |
| C4-15 | 4.4 Contagem de tokens | texto | anthropic-token-counting | Introdução | consultada em 13/11/2026 | registrado na documentação | Token counting lets you determine the number of tokens in a message before you send it to Claude. |
| C4-16 | 4.4 Contagem de tokens | texto | anthropic-token-counting | Estimativa | consultada em 13/11/2026 | registrado na documentação | The token count is an estimate. |
| C4-17 | 4.4 Contagem de tokens | texto | anthropic-token-counting | Tokenizadores por modelo | consultada em 13/11/2026 | registrado na documentação | The same input text produces approximately 30 percent more tokens than on earlier models. |
| C4-18 | 4.5 Parâmetros | texto | anthropic-migration-2026-10-21 | Parâmetros de amostragem | consultada em 13/11/2026 | registrado na documentação | In 2026-10-21, a request that sends temperature, top_p, or top_k returns a 400 error, even at the parameter’s default value. |
| C4-19 | 4.5 Parâmetros | texto | anthropic-effort | Como o esforço funciona | consultada em 13/11/2026 | registrado na documentação | The effort parameter lets you control how many tokens Claude spends when responding to requests. |
| C4-20 | 4.5 Parâmetros | texto | anthropic-effort | Definir o nível | consultada em 13/11/2026 | registrado na documentação | Set output_config.effort on the request. |
| C4-21 | 4.5 Parâmetros | texto | anthropic-handling-stop-reasons | Motivos de parada | consultada em 13/11/2026 | registrado na documentação | The response reached your max_tokens limit. |
| C4-22 | 4.6 Saída estruturada, templates e falhas | texto | anthropic-structured-outputs | Introdução | consultada em 13/11/2026 | registrado na documentação | Structured outputs constrain Claude’s responses to follow a specific schema, ensuring valid, parseable output for downstream processing. |
| C4-23 | 4.6 Saída estruturada, templates e falhas | texto | openai-structured-outputs | Introdução | consultada em 13/11/2026 | registrado na documentação | Your application still needs to handle refusals, incomplete responses, and API errors, and validate any business rules that the schema does not express. |
| C4-24 | 4.6 Saída estruturada, templates e falhas | texto | json-schema-overview | What is JSON Schema? | consultada em 13/11/2026 | registrado na documentação | JSON Schema is a declarative language for defining structure and constraints for JSON data. |
| C4-25 | 4.4 Contagem de tokens | texto | anthropic-token-counting | Preço e limites | consultada em 14/11/2026 | registrado na documentação | Token counting is free to use but subject to requests per minute rate limits based on your usage tier. |
| C4-26 | 4.4 Contagem de tokens | texto | anthropic-token-counting | Tokenizadores por modelo | consultada em 14/11/2026 | registrado na documentação | don’t reuse token counts measured on the older model to estimate costs or context window fit. |
| C4-27 | 4.5 Parâmetros | texto | anthropic-handling-stop-reasons | Motivos de parada | consultada em 14/11/2026 | registrado na documentação | Claude emitted one of your stop_sequences. |
| C4-28 | 4.6 Saída estruturada, templates e falhas | texto | anthropic-structured-outputs | Limite de tokens | consultada em 14/11/2026 | registrado na documentação | The output might be incomplete and not match your schema. |
| C4-29 | 4.6 Saída estruturada, templates e falhas | texto | openai-structured-outputs | Structured Outputs vs JSON mode | consultada em 14/11/2026 | registrado na documentação | While both ensure valid JSON is produced, only Structured Outputs ensure schema adherence. |
| C4-30 | 4.2 Técnicas de prompt com fonte primária | texto | arxiv-2201.11903 | Resumo | Wei et al., 2022 | registrado no artigo | chain of thought prompting improves performance on a range of arithmetic, commonsense, and symbolic reasoning tasks. |
| C4-31 | 4.3 Mensagens e papéis | texto | anthropic-token-counting | Entradas aceitas | consultada em 14/11/2026 | registrado na documentação | Send images and PDFs as base64 to count them. |
| C4-32 | 4.6 Saída estruturada, templates e falhas | texto | anthropic-structured-outputs | Visão geral | consultada em 14/11/2026 | registrado na documentação | Get Claude’s response in a specific JSON format |
| C4-33 | 4.6 Saída estruturada, templates e falhas | texto | anthropic-structured-outputs | Recusa | consultada em 14/11/2026 | registrado na documentação | The response has stop_reason: "refusal". |
| C4-34 | 4.2 Técnicas de prompt com fonte primária | texto | 2202.12837 | Seção 2 | Min et al., 2022 | registrado no artigo | We experiment with 12 models in total. |
| C4-35 | 4.2 Técnicas de prompt com fonte primária | texto | 2202.12837 | Seção 2 | Min et al., 2022 | registrado no artigo | datasets are classification and multi-choice tasks. |
| C4-36 | 4.3 Mensagens e papéis | texto | anthropic-token-counting | Entradas aceitas | consultada em 17/11/2026 | registrado na documentação | endpoint accepts the same structured list of inputs for creating a message, including support for system prompts, tools, images, and PDFs. |
| C4-37 | 4.3 Mensagens e papéis | texto | anthropic-token-counting | Entradas rejeitadas | consultada em 17/11/2026 | registrado na documentação | This endpoint returns an invalid_request_error for a few inputs that the Messages API accepts: Server tools such as web search, web fetch, code execution, and tool search (every server tool except the advisor tool) |

## 3. Resultado da conferência

```
python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-capitulo-4-2026-11-13.md --textos /tmp/cap4-fontes/txt --projeto .
```

Saída registrada em 13/11/2026: 24 trechos, 24 aprovados, 0 reprovados. Em 14/11/2026, as fontes foram baixadas de novo e o comando foi repetido sobre as 33 linhas (C4-01 a C4-33, as 9 últimas novas): 33 aprovados, 0 reprovados (claude - pessoal). A pasta `/tmp` não é permanente; para reconferir, baixar as fontes pelo procedimento da seção 1.

## 4. Lacunas e ressalvas

- **Artigos do arXiv:** lidos no resumo e no trecho citado, em cópia baixada em 13/11/2026; o guia não afirma que os resultados se repetem em outros modelos ou tarefas.
- **Documentação da Anthropic e da OpenAI:** páginas mudam sem aviso; toda afirmação sobre parâmetro leva a data de consulta. O guia não afirma conformidade com nenhuma das duas.
- **Remoção de `temperature`, `top_p` e `top_k` na Anthropic:** o fato está registrado no guia de migração da versão `2026-10-21`, consultado em 13/11/2026. A mudança vale para a API da Anthropic; outros provedores mantêm os campos, e o guia não generaliza.
- **Contagem de tokens:** a página avisa que o número é estimativa; o guia não trata a contagem como medida exata.
- **Aurora Educação:** situação construída para o livro; nenhum dado real de aluno ou de escola foi usado. Os prompts são ilustrativos e não foram executados.
- **Não verificado:** segunda leitura independente dos trechos por outra pessoa; comportamento de modelos que o guia não cita; datas de publicação das páginas da Anthropic e da OpenAI, ausentes no texto extraído.

Assinatura: deepseek - conta não verificada, 13/11/2026.
