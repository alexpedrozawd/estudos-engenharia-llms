# Pacotes de fontes — Capítulo 1 (Fundamentos de IA e LLMs)

Data: 13/10/2026; trechos acrescentados em 15/10/2026. Autoria: claude - ap (Bloco 1 em Haiku 5.5 High; ampliação do Bloco 2 em Sonnet 5.5 High; revisão do Bloco 3 em Opus 5.5 High, com os trechos 1.1-T6 a T8, 1.2-T15 e T16, 1.3-T14, 1.4-T15 a T19 e 1.6-T11, conferidos contra o mesmo rascunho de 19/08/2026). Não altera o guia HTML.

Extração dos PDFs para o script: `pdftotext` sem `-layout`; com `-layout`, as notas de margem do Jurafsky & Martin entram no meio das frases e geram reprovações falsas.

Formato: cada linha traz um trecho literal copiado da fonte extraída. O script `ferramentas/conferir-trechos.py` confere cada trecho contra o texto da fonte. Trecho ausente reprova o pacote da unidade (regra da §9); nada foi completado de memória.

Qualificadores: *verificado no código local*, *registrado na documentação*, *observado em ata*, *histórico/desativado* e *proposta didática*. Os trechos de casos vêm dos contextos de estudo locais e não incluem nomes de pessoas, dados de clientes nem detalhes internos de PR.

Fontes de vídeo (Karpathy, 3Blue1Brown), slides (CS224N, CS336), livros, Lilian Weng e *Building effective agents* não entram aqui: não há texto lido para trecho literal. Ficam como ponteiros, com aviso de que não foram lidos.

Decisões do operador em 13/10/2026:
- §8.4.4 do Jurafsky & Martin (cap. 8): o título existe no rascunho, mas o corpo não aparece no texto extraído. Fica fora do pacote e do texto.
- `docs/09-antipadroes-e-boas-praticas-llm.md`: está em `C:\Users\ap\.config\ai-agent-guidelines\docs\` (diretrizes, não o repositório do Router); lido em modo somente leitura e usado como fonte interna nas unidades 1.2, 1.3 e 1.6.
- "Data de corte": nenhuma fonte lida define o termo. A 1.2 trata o conceito como consequência lógica do pré-treinamento e o marca como proposta didática.

## Unidade 1.1

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 1.1-T1 | 1.1 | texto | jurafsky-cap1 | §1.1 | Rascunho de 19/08/2026 | registrado na documentação | A language model is a computational system that can predict the next word from previous words. |
| 1.1-T2 | 1.1 | texto | jurafsky-cap1 | §1.11 | Rascunho de 19/08/2026 | registrado na documentação | This is anthropomorphism: assigning human traits, emotions, or cognition to non-human animals or objects. |
| 1.1-T3 | 1.1 | texto | google-mlcc-llm | Módulo LLM | Página consultada em 13/10/2026 | registrado; aprofundamento, ler antes de citar | This module explores language models, which estimate the probability of a token or sequence of tokens occurring within a longer sequence |
| 1.1-C1 | 1.1 | caso | contexto-de-estudo-ap-ai-router | §3 (problema, público e propósito) | Contexto de 13/10/2026 | registrado no contexto | modelo gera ou interpreta conteúdo; o sistema ao redor organiza instruções, ferramentas, estado, persistência, permissões, execução e avaliação |
| 1.1-C2 | 1.1 | caso | contexto-de-estudo-nanda-mac | §9 (fronteira entre software, LLM e ação humana) | Contexto de 13/10/2026 | registrado no contexto | Textos do modelo, resultados de ferramentas e documentos de negócio são dados, não autorização |
| 1.1-T4 | 1.1 | texto | jurafsky-cap1 | §1.11 | Rascunho de 19/08/2026 | registrado na documentação | words like understand or intend imply something incorrect about the kinds of agency and intentionality a language model possesses |
| 1.1-T5 | 1.1 | texto | jurafsky-cap1 | §1.7 | Rascunho de 19/08/2026 | registrado na documentação | At inference, we prompt a model and conditionally generate text. |
| 1.1-C3 | 1.1 | caso | contexto-de-estudo-nanda-mac | §9 (fronteira entre software, LLM e ação humana) | Contexto de 13/10/2026 | registrado no contexto | Regras de cobrança, preço, status ou permissão não devem depender de interpretação probabilística quando o sistema já pode aplicá-las de forma determinística. |
| 1.1-C4 | 1.1 | caso | contexto-de-estudo-ap-ai-router | §5 (Pipeline Triangular) | Contexto de 13/10/2026 | registrado no contexto | Aplicar e testar a proposta não acontece automaticamente pela chamada local do chat. |
| 1.1-T6 | 1.1 | texto | jurafsky-cap1 | §1.1 | Rascunho de 19/08/2026 | registrado na documentação | given a context or prefix of words, a language model assigns a probability distribution over possible next words. |
| 1.1-T7 | 1.1 | texto | jurafsky-cap1 | §1.1 (Fig. 1.1) | Rascunho de 19/08/2026 | registrado na documentação | we can guess that the next word might be all or everything but is unlikely to be of or |
| 1.1-T8 | 1.1 | texto | jurafsky-cap1 | §1.11 | Rascunho de 19/08/2026 | registrado na documentação | the reader should think about this terminology as merely a convenient shorthand. |
| 1.1-C5 | 1.1 | caso | contexto-de-estudo-ap-ai-router | §3 (problema, público e propósito) | Contexto de 13/10/2026 | registrado no contexto | Ele combina diretrizes compartilhadas, procedimentos reutilizáveis chamados skills, painel de conversa, despacho de clientes de fronteira e inferência local. |

## Unidade 1.2

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 1.2-T1 | 1.2 | texto | jurafsky-cap1 | Introdução ao §1.2 | Rascunho de 19/08/2026 | registrado na documentação | simply by learning to predict words, large language models acquire enormous amounts of knowledge |
| 1.2-T2 | 1.2 | texto | jurafsky-cap1 | §1.7 | Rascunho de 19/08/2026 | registrado na documentação | Inference means running the model and generating text. |
| 1.2-T3 | 1.2 | texto | jurafsky-cap8 | §8.1 | Rascunho de 19/08/2026 | registrado na documentação | Instruction tuning is a form of supervised learning where the training data consists of instructions and we continue training the model on them using the same language modeling objective used to train the original model. |
| 1.2-T4 | 1.2 | texto | jurafsky-cap1 | §1.1 (parâmetros) | Rascunho de 19/08/2026 | registrado na documentação | A parameter is a single real-valued number that is trained in a neural network and used for computation |
| 1.2-T5 | 1.2 | texto | jurafsky-cap1 | §1.6 | Rascunho de 19/08/2026 | registrado na documentação | when we are training them, i.e. setting the weights of the neural networks in the system, and when we are doing inference, which is the technical term for when we are prompting them to generate text. |
| 1.2-T6 | 1.2 | texto | jurafsky-cap1 | §1.6 | Rascunho de 19/08/2026 | registrado na documentação | in the pretraining stage, the model is trained to predict the next word, one by one, in enormous text corpora of billions of tokens drawn from the web. |
| 1.2-T7 | 1.2 | texto | jurafsky-cap1 | §1.6 | Rascunho de 19/08/2026 | registrado na documentação | in instruction tuning, also called supervised fine-tuning or SFT, the base model learns to follow instructions, like answering questions, writing code, translating, and so on |
| 1.2-T8 | 1.2 | texto | jurafsky-cap1 | §1.6 | Rascunho de 19/08/2026 | registrado na documentação | in the preference alignment stage, the model is trained to try to match human preferences with the goal of making it less harmful and more helpful. |
| 1.2-T9 | 1.2 | texto | jurafsky-cap1 | §1.3 | Rascunho de 19/08/2026 | registrado na documentação | open-weight models, in which the model creator gives out all the different weights, allowing anyone to run the model on their own machines, and closed-weight or proprietary models, for which the creator does not give out the weights, and only allows people to interact with the model via a web/app or API interface. |
| 1.2-T10 | 1.2 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 5 (fine-tuning prematuro) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Afinar pesos para ensinar regras de negócio mutáveis da empresa. |
| 1.2-T11 | 1.2 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 5 (solução) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | *In-Context Learning*: modelo base congelado com contexto atualizado. |
| 1.2-T12 | 1.2 | texto | jurafsky-cap8 | §8.5 (resumo) | Rascunho de 19/08/2026 | registrado na documentação | Three stages of post-training are instruction tuning (supervised fine-tuning or SFT), preference alignment, and RLVR. |
| 1.2-T13 | 1.2 | texto | jurafsky-cap1 | §1.6.1 | Rascunho de 19/08/2026 | registrado na documentação | Each time the language model fails, just like the corrections we give the humans in the Shannon game, we'll correct the language model by telling it what it should have guessed. |
| 1.2-T14 | 1.2 | texto | jurafsky-cap1 | §1.6 | Rascunho de 19/08/2026 | registrado na documentação | in RL for reasoning, or RL with verifiable rewards, the model is further trained to reason. |
| 1.2-T15 | 1.2 | texto | jurafsky-cap1 | §1.1 (parâmetros) | Rascunho de 19/08/2026 | registrado na documentação | up of two kinds of numbers called weights and biases. |
| 1.2-T16 | 1.2 | texto | jurafsky-cap1 | §1.6 | Rascunho de 19/08/2026 | registrado na documentação | We use tasks with multiple steps of reasoning and a clear right answer |
| 1.2-C1 | 1.2 | caso | contexto-de-estudo-nanda-mac | §8 (direção dos assistentes) | Contexto de 13/10/2026 | registrado no contexto | Não implica um modelo treinado, processo de inferência ou chave de API exclusivo para cada pessoa. |
| 1.2-C3 | 1.2 | caso | contexto-de-estudo-ap-ai-router | §5 (Pipeline Triangular) | Contexto de 13/10/2026 | registrado no contexto | O chat Ollama usa `/api/generate`, sem ferramentas para ler o projeto, editar arquivos ou executar testes. |
| 1.2-C2 | 1.2 | caso | contexto-de-estudo-ap-ai-router | §5 (local atual, histórico e futuro) | Contexto de 13/10/2026 | verificado no código local | `local_model_policy.py` aceita somente o alvo Qwen |

## Unidade 1.3

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 1.3-T1 | 1.3 | texto | anthropic-context-windows | Página "Context windows" | Página consultada em 13/10/2026 | registrado na documentação | Everything in the request counts toward the context window: the system prompt, every message in messages (including tool results, images, and documents), and your tool definitions. |
| 1.3-T2 | 1.3 | texto | jurafsky-cap2 | §2.4 (BPE) | Rascunho de 19/08/2026 | registrado na documentação | Tokenization, the first stage of natural language processing, is the process of segmenting the running input text into tokens. |
| 1.3-T3 | 1.3 | texto | google-mlcc-llm | Módulo LLM | Página consultada em 13/10/2026 | registrado; aproximação, não cálculo | Tokenization is language specific, so the number of characters per token differs across languages. |
| 1.3-T4 | 1.3 | texto | anthropic-context-windows | Página "Context windows" | Página consultada em 13/10/2026 | registrado na documentação | The output Claude generates for the turn, including its extended thinking, counts too. |
| 1.3-T5 | 1.3 | texto | anthropic-context-windows | Página "Context windows" | Página consultada em 13/10/2026 | registrado na documentação | A larger context window allows the model to handle more complex and lengthy prompts, but more context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot. |
| 1.3-T6 | 1.3 | texto | jurafsky-cap2 | §2.4 | Rascunho de 19/08/2026 | registrado na documentação | use a data-driven approach to define tokens that will generally result in units about the size of morphemes or words, but occasionally use units as small as characters. |
| 1.3-T7 | 1.3 | texto | hf-llm-tutorial | Chat template | Página consultada em 13/10/2026 | registrado; descreve a biblioteca, não provedores | a chat model expects the input as a chat template. Your prompt should include a role and content to indicate who is participating in the conversation. |
| 1.3-T8 | 1.3 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 4 (entupimento de contexto) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Recuperar fontes pertinentes; preservar origem e requisitos antes de compactar. |
| 1.3-T9 | 1.3 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 4 (entupimento de contexto) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Não substituir excesso por cortes cegos. |
| 1.3-T12 | 1.3 | texto | anthropic-context-windows | Página "Context windows" | Página consultada em 13/10/2026 | registrado na documentação | use the token counting API to estimate token usage before sending messages |
| 1.3-T13 | 1.3 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 4 (entupimento de contexto) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Arquivos inteiros sem necessidade porque |
| 1.3-T10 | 1.3 | texto | anthropic-context-windows | Página "Context windows" | Página consultada em 13/10/2026 | registrado na documentação | refers to all the text a language model can reference when generating a response, including the response itself. |
| 1.3-T11 | 1.3 | texto | anthropic-context-windows | Página "Context windows" | Página consultada em 13/10/2026 | registrado na documentação | This is different from the large corpus of data the language model was trained on, and instead represents a "working memory" for the model. |
| 1.3-T14 | 1.3 | texto | hf-llm-tutorial | Chat template | Página consultada em 15/10/2026 | registrado; descreve a biblioteca, não provedores | If you try to pass your prompt as a single string, the model |
| 1.3-C4 | 1.3 | caso | contexto-de-estudo-ap-ai-router | §6 (contexto, ferramentas e continuidade) | Contexto de 13/10/2026 | registrado no contexto | A janela local é estimada a partir do envelope e da reserva de saída, com teto Qwen de 64k declarado no código. |
| 1.3-C1 | 1.3 | caso | contexto-de-estudo-ap-ai-router | §6 (contexto, ferramentas e continuidade) | Contexto de 13/10/2026 | registrado no contexto | O contexto contém mais que a mensagem do usuário: instruções, exemplos, histórico, fontes, contratos, definições de ferramentas e resultados de ferramentas também podem consumir a entrada do modelo. |
| 1.3-C2 | 1.3 | caso | contexto-de-estudo-ap-ai-router | §6 (contexto, ferramentas e continuidade) | Contexto de 13/10/2026 | registrado no contexto | Caracteres são uma estimativa, não contagem exata de tokens nem prova de capacidade disponível. |
| 1.3-C3 | 1.3 | caso | contexto-de-estudo-nanda-mac | §9 (fronteira entre software, LLM e ação humana) | Contexto de 13/10/2026 | registrado no contexto | Descrição de ferramenta, schema e resultado também consomem contexto; selecionar fontes e ferramentas por etapa faz parte da arquitetura |

## Unidade 1.4

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 1.4-T1 | 1.4 | texto | hf-generation-strategies | "Greedy search" | Página consultada em 13/10/2026 | registrado; padrão da biblioteca, não do provedor | Greedy search works well for tasks with relatively short outputs where creativity is not a priority. |
| 1.4-T2 | 1.4 | texto | jurafsky-cap7 | §7.6.1 | Rascunho de 19/08/2026 | registrado na documentação | In practice, however, we don't use greedy decoding with large language models. |
| 1.4-T3 | 1.4 | texto | jurafsky-cap7 | §7.6.2 | Rascunho de 19/08/2026 | registrado na documentação | Alas, it turns out random sampling doesn't work well either. |
| 1.4-T4 | 1.4 | texto | hf-llm-tutorial | Introdução | Página consultada em 13/10/2026 | registrado; descreve a biblioteca, não provedores | A LLM is trained to generate the next word (token) given some initial text (prompt) along with its own generated outputs up to a predefined length or when it reaches an end-of-sequence (EOS) token. |
| 1.4-T5 | 1.4 | texto | jurafsky-cap7 | §7.6.1 | Rascunho de 19/08/2026 | registrado na documentação | if the context is identical, and the probabilistic model is the same, greedy decoding will always result in generating exactly the same string. |
| 1.4-T6 | 1.4 | texto | jurafsky-cap7 | §7.6.2 | Rascunho de 19/08/2026 | registrado na documentação | In other words, greedy decoding is too boring, and random sampling is too random. |
| 1.4-T7 | 1.4 | texto | jurafsky-cap7 | §7.6.3 | Rascunho de 19/08/2026 | registrado na documentação | Methods that emphasize the most probable words tend to produce generations that are rated by people as more accurate, more coherent, and more factual, but also more boring and more repetitive. |
| 1.4-T8 | 1.4 | texto | jurafsky-cap7 | §7.6.3 | Rascunho de 19/08/2026 | registrado na documentação | The idea of temperature sampling is to reshape the probability distribution to increase the probability of the high probability tokens and decrease the probability of the low probability tokens. |
| 1.4-T9 | 1.4 | texto | hf-generation-strategies | "Greedy search" | Página consultada em 13/10/2026 | registrado; padrão da biblioteca, não do provedor | Greedy search is the default decoding strategy. |
| 1.4-T10 | 1.4 | texto | hf-generation-strategies | "Beam search" | Página consultada em 13/10/2026 | registrado; apenas menção | Beam search keeps track of several generated sequences (beams) at each time step. |
| 1.4-T11 | 1.4 | texto | hf-generation-strategies | "Greedy search" | Página consultada em 13/10/2026 | registrado; padrão da biblioteca, não do provedor | Unless specified in GenerationConfig, this strategy generates a maximum of 20 new tokens. |
| 1.4-T12 | 1.4 | texto | jurafsky-cap7 | Introdução do cap. 7 | Rascunho de 19/08/2026 | registrado na documentação | left-to-right (sometimes called causal or autoregressive or decoder) language modeling, in which we are given a sequence of input tokens and predict output tokens one by one by conditioning on the prior context |
| 1.4-T13 | 1.4 | texto | jurafsky-cap7 | §7.6.3 | Rascunho de 19/08/2026 | registrado na documentação | we may want to flatten the word probability distribution instead of making it greedy. |
| 1.4-T14 | 1.4 | texto | jurafsky-cap7 | §7.6.3 | Rascunho de 19/08/2026 | registrado na documentação | Methods that give a bit more weight to the middle-probability words tend to be more creative and more diverse, but less factual and more likely to be incoherent or otherwise low-quality. |
| 1.4-T15 | 1.4 | texto | jurafsky-cap7 | §7.6.1 | Rascunho de 19/08/2026 | registrado na documentação | the resulting text is generic and often quite repetitive. |
| 1.4-T16 | 1.4 | texto | jurafsky-cap7 | §7.6.2 | Rascunho de 19/08/2026 | registrado na documentação | there are many odd, low-probability tokens in the tail of the distribution. |
| 1.4-T17 | 1.4 | texto | jurafsky-cap7 | §7.6.2 | Rascunho de 19/08/2026 | registrado na documentação | There are three standard sampling methods that modify random sampling to |
| 1.4-T18 | 1.4 | texto | jurafsky-cap7 | §7.6.3 | Rascunho de 19/08/2026 | registrado na documentação | enable trading off two important factors in generation: quality and diversity. |
| 1.4-T19 | 1.4 | texto | jurafsky-cap7 | §7.6.4 | Rascunho de 19/08/2026 | registrado na documentação | it is common to combine both top-k and top-p sampling |
| 1.4-C1 | 1.4 | caso | contexto-de-estudo-ap-ai-router | §5 (Pipeline Triangular) | Contexto de 13/10/2026 | registrado no contexto | Um marcador de conclusão na resposta não comprova que exista uma proposta útil. |
| 1.4-C2 | 1.4 | caso | contexto-de-estudo-nanda-mac | §5 (jornada e sistemas) | Contexto de 13/10/2026 | registrado no contexto | cálculo de valores no servidor, validação de entrada com Zod, tratamento de webhooks e registros de entrega de eventos são exemplos de responsabilidades determinísticas |

## Unidade 1.5

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 1.5-T15 | 1.5 | texto | vaswani-2017 | Resumo (abstract) | arXiv:1706.03762v7, PDF consultado em 13/10/2026 | registrado na documentação | We propose a new simple network architecture, the Transformer |
| 1.5-T1 | 1.5 | texto | vaswani-2017 | §3.2.1 (Scaled Dot-Product Attention) | arXiv:1706.03762v7, PDF consultado em 13/10/2026 | registrado na documentação | We call our particular attention |
| 1.5-T2 | 1.5 | texto | jurafsky-cap7 | §7.1 (Attention) | Rascunho de 19/08/2026 | registrado na documentação | But in context it has a much richer meaning. |
| 1.5-T3 | 1.5 | texto | jurafsky-cap7 | §7.1.1 (nota sobre custo) | Rascunho de 19/08/2026 | registrado na documentação | attention is quadratic in the length of the input, since at each layer we need to compute dot products between each pair |
| 1.5-T4 | 1.5 | texto | jurafsky-cap7 | Introdução do cap. 7 | Rascunho de 19/08/2026 | registrado na documentação | In this chapter we introduce the transformer, the standard architecture for building large language models, and how to pretrain them and how to use them to generate text. |
| 1.5-T5 | 1.5 | texto | jurafsky-cap7 | §7.1 (Attention) | Rascunho de 19/08/2026 | registrado na documentação | Attention can be thought of as a way to build contextual representations of a token's meaning by attending to and integrating information from surrounding tokens |
| 1.5-T6 | 1.5 | texto | jurafsky-cap7 | §7.1.1, Fig. 7.4 | Rascunho de 19/08/2026 | registrado na documentação | When processing each input xi, the model attends to all the inputs up to, and including xi. |
| 1.5-T7 | 1.5 | texto | jurafsky-cap7 | §7.1 (exemplos 7.1 e 7.2) | Rascunho de 19/08/2026 | registrado na documentação | The chicken didn't cross the road because it was too tired. |
| 1.5-T8 | 1.5 | texto | jurafsky-cap7 | §7.1 (exemplos 7.1 e 7.2) | Rascunho de 19/08/2026 | registrado na documentação | The chicken didn't cross the road because it was too wide. |
| 1.5-T9 | 1.5 | texto | jurafsky-cap7 | Figura 7.2 | Rascunho de 19/08/2026 | registrado na documentação | showing how each input token gets encoded, passed through a set of stacked transformer blocks, and then a language model head that predicts the next token. |
| 1.5-T10 | 1.5 | texto | jurafsky-cap7 | Introdução do cap. 7 | Rascunho de 19/08/2026 | registrado na documentação | this multi-head attention layer, also called a self-attention layer. |
| 1.5-T11 | 1.5 | texto | jurafsky-cap7 | §7.1.1 (papéis de query e key) | Rascunho de 19/08/2026 | registrado na documentação | As the current element being compared to the preceding inputs. We'll refer to this role as a query. |
| 1.5-T12 | 1.5 | texto | jurafsky-cap7 | §7.1.1 (papéis de query e key) | Rascunho de 19/08/2026 | registrado na documentação | In its role as a preceding input that is being compared to the current element to determine a similarity weight. We'll refer to this role as a key. |
| 1.5-T14 | 1.5 | texto | jurafsky-cap7 | §7.1.1 (papéis de query, key e value) | Rascunho de 19/08/2026 | registrado na documentação | And finally, as a value of a preceding element that gets weighted and summed up to compute the output for the current element. |
| 1.5-T13 | 1.5 | texto | jurafsky-cap7 | §7.8 (KV cache) | Rascunho de 19/08/2026 | registrado na documentação | The KV cache is a technique to avoid this waste of time. |
| 1.5-C2 | 1.5 | caso | contexto-de-estudo-nanda-mac | §9 (fronteira entre software, LLM e ação humana) | Contexto de 13/10/2026 | registrado no contexto | Descrição de ferramenta, schema e resultado também consomem contexto; selecionar fontes e ferramentas por etapa faz parte da arquitetura |
| 1.5-C1 | 1.5 | caso | contexto-de-estudo-ap-ai-router | §6 (contexto, ferramentas e continuidade) | Contexto de 13/10/2026 | registrado no contexto | O contexto contém mais que a mensagem do usuário: instruções, exemplos, histórico, fontes, contratos, definições de ferramentas e resultados de ferramentas também podem consumir a entrada do modelo. |

## Unidade 1.6

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| 1.6-T1 | 1.6 | texto | jurafsky-cap1 | §1.10 (Safety and Alignment) | Rascunho de 19/08/2026 | registrado na documentação | LLMs can be overconfident, using very certain language |
| 1.6-T2 | 1.6 | texto | jurafsky-cap1 | §1.10 (Safety and Alignment) | Rascunho de 19/08/2026 | registrado na documentação | LLMs are not well calibrated, meaning the model's actual accuracy doesn't match the score or probability they assign. |
| 1.6-T3 | 1.6 | texto | jurafsky-cap1 | §1.10 (Safety and Alignment) | Rascunho de 19/08/2026 | registrado na documentação | LLMs can hallucinate, which we use technically in NLP to mean generating text that is factually incorrect, especially emphasizing cases like inventing people or facts that simply don't exist. |
| 1.6-T4 | 1.6 | texto | jurafsky-cap1 | §1.10 (Safety and Alignment) | Rascunho de 19/08/2026 | registrado na documentação | because LLMs are very expensive, for many text processing tasks it's still worthwhile to use more lightweight methods |
| 1.6-T10 | 1.6 | texto | jurafsky-cap1 | §1.10 (Safety and Alignment) | Rascunho de 19/08/2026 | registrado na documentação | Each of these issues is an important area of active research. |
| 1.6-T11 | 1.6 | texto | jurafsky-cap1 | §1.10 (Safety and Alignment) | Rascunho de 19/08/2026 | registrado na documentação | even when they are wrong. LLMs are not well calibrated |
| 1.6-T5 | 1.6 | texto | docs-09-antipadroes-e-boas-praticas-llm | §1 (code-first, LLM-second) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Prefira código/controles existentes para regras determinísticas, quando a solução for sustentável pelo benefício, risco e custo total. |
| 1.6-T6 | 1.6 | texto | docs-09-antipadroes-e-boas-praticas-llm | §1 (code-first, LLM-second) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Modelos de linguagem são motores semânticos probabilísticos para lidar com ambiguidade, síntese e linguagem natural. |
| 1.6-T7 | 1.6 | texto | docs-09-antipadroes-e-boas-praticas-llm | §1 (code-first, LLM-second) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Usá-los para lógica booleana, parse trivial ou cálculos introduz latência, custo e falhas silenciosas evitáveis. |
| 1.6-T8 | 1.6 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 2 (prompt patching) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Acúmulo de parágrafos em CAPS LOCK a cada erro de borda |
| 1.6-T9 | 1.6 | texto | docs-09-antipadroes-e-boas-praticas-llm | §3, antipadrão 7 (LLM para lógica simples) | Diretrizes locais, consultadas em 13/10/2026 | registrado; fonte interna | Comportamento não determinístico em tarefas de precisão matemática. |
| 1.6-C1 | 1.6 | caso | contexto-de-estudo-nanda-mac | §9 (fronteira entre software, LLM e ação humana) | Contexto de 13/10/2026 | registrado no contexto | A escolha de usar LLM deve ter benefício justificado. |
| 1.6-C2 | 1.6 | caso | contexto-de-estudo-nanda-mac | §7 (Estado registrado e limites da verificação; acréscimo de 13/10) | Contexto de 13/10/2026 | observado em ata | a ata relata recusas de pedidos de senha de administrador |
| 1.6-C3 | 1.6 | caso | contexto-de-estudo-ap-ai-router | §7 (código determinístico e interpretação pela LLM) | Contexto de 13/10/2026 | registrado no contexto | Prompt é orientação para o modelo; autorização e limites de ação precisam ser aplicados pelo sistema. |

---

Assinatura: claude - ap — 13/10/2026.
