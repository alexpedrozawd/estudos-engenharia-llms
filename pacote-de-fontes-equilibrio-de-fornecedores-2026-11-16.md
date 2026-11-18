# Pacote de fontes: equilíbrio de fornecedores e modelos abertos, capítulos 1, 3, 4 e 5 (16/11/2026)

Pedido do operador em 16/11/2026: equilibrar as fontes, sem focar só na Anthropic. Todos os trechos abaixo foram conferidos por busca literal (43 citações na primeira rodada e 31 na segunda; as divergências da segunda, três citações montadas a partir de tabelas e listas, foram reescritas, e a conferência automática não reconhece o símbolo de controle do Gemma, conferido à mão) contra as páginas baixadas em 16/11/2026. As páginas ficaram em `/tmp/eq-fontes` (temporária, não é fonte de verdade); baixe de novo para reconferir.

## 1. Como reconferir
Baixar as páginas em Markdown (OpenAI e Google oferecem a versão `.md`) com `curl -sL` e buscar cada trecho sem diferenciar quebras de linha.

| Página | Endereço baixado | Hash (16) |
|---|---|---|
| OpenAI, Evaluation best practices | developers.openai.com/api/docs/guides/evaluation-best-practices.md | `92179b5f723b63b7` |
| OpenAI, Prompt engineering | developers.openai.com/api/docs/guides/prompt-engineering.md | `a77f44ef8cead1d4` |
| OpenAI, Using GPT-6 | developers.openai.com/api/docs/guides/latest-model.md | `b12f5dde985df0ac` |
| Google, Prompt design strategies | ai.google.dev/gemini-api/docs/prompting-strategies (redireciona para aistudio.google.com/docs/prompting-strategies; `.md.txt`) | `32285484f9b4d91f` |
| Google Cloud, Gen AI evaluation service overview | cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview (redireciona para docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-overview) | `496e7691f54cc0fc` |

| Qwen, ficha do Qwen3.8-27B (Hugging Face) | huggingface.co/Qwen/Qwen3.8-27B/raw/main/README.md | `7c24f46af1e0024e` |
| Google, ficha do Gemma 4 31B-it (Hugging Face) | huggingface.co/google/gemma-4-31B-it/raw/main/README.md (a ficha do 26B-A4B é igual nos pontos citados: `4f463225c4fe49ec`) | `e209f5c435b1e660` |

## 2. Trechos e onde entram
- **Parâmetros (4.5a, notas; 5.6a):** Google: “Gemini 4 and Gemini 3.6+ models ignore custom values for temperature, top_p, and top_k and return deprecation warning headers (and will return 400 errors in a future release)”; “For earlier Gemini 3 models, keep these parameters at their default values to avoid degraded reasoning performance”. OpenAI, Using GPT-6: “When reasoning effort is not none, remove temperature, top_p, and top_logprobs”.
- **Exemplos (4.2a):** Google: “We recommend to always include few-shot examples in your prompts”; “it is essential to ensure a consistent format across all examples”.
- **Delimitadores (4.2c):** OpenAI: “Markdown headers and lists can be helpful to mark distinct sections of a prompt”; “XML tags can help delineate where one piece of content (like a supporting document used for reference) begins and ends”. Google: “Employ clear delimiters to separate different parts of your prompt”; “Choose one format and use it consistently within a single prompt”.
- **Objetivo e erros de avaliação (3.4a, 5.2a):** OpenAI: “Define eval objective. What’s the success criteria for the eval?”; “Biased design: Creating eval datasets that don’t faithfully reproduce production traffic patterns”; “Vibe-based evals: …waiting until you ship before implementing any evals”; “Log everything: Log as you develop so you can mine your logs for good eval cases”.
- **Avaliadores (5.4a):** OpenAI: “Metric-based evals”, “Human evals”, “LLM-as-a-judge and model graders”; “Human judgment evals provide the highest quality but are slow and expensive”. Google Cloud: “Computation-based metrics: Use deterministic algorithms like ROUGE or BLEU when a ground truth is available”; “Evaluation rubrics are similar to unit tests in software development”; “Rubric-based metrics: Incorporate LLMs into evaluation workflows to assess the quality of model responses”.
- **Juiz (5.4c):** OpenAI: “Position bias (response order), verbosity bias (preferring longer responses)”; “Use pairwise comparison or pass/fail for more reliability”; “Control for response lengths”; “Once the LLM judge reaches a point where it’s faster, cheaper, and consistently agrees with human annotations, scale up”; “No strategy is perfect”.
- **Avaliação contínua (5.5c):** OpenAI: “Set up continuous evaluation (CE) to run evals on every change…”; “OpenAI is deprecating the Evals platform”; “Evals will become read-only for existing users on October 31, 2026, and the platform is scheduled to shut down on November 30, 2026”.

- **Modelos abertos (1.3c, 1.4c, 1.4d, 1.7a, 1.7c, 4.5a):** Qwen3.8-27B: licença Apache 2.0; “a compact, deployment-friendly dense model: a native vision-language model that understands images and videos”; “Context Length: 262,144 natively and extensible up to 1,000,000 tokens”; “Thinking mode is on by default and can be disabled per request”; amostragem recomendada (raciocínio: temperature=1.0, top_p=0.95, top_k=20; sem raciocínio: temperature=0.7, top_p=0.80, top_k=20); “the support for sampling parameters varies according to inference frameworks”. Gemma 4: licença Apache 2.0; “open-weights models”; 31B denso (30,7 bi) e 26B A4B MoE (25,2 bi no total, 3,8 bi ativos), “runs much faster than its 26B total might suggest”; contexto de 128K (pequenos) e 256K (médios); “To disable thinking, remove the token”; amostragem “standardized sampling configuration across all use cases” com temperature=1.0, top_p=0.95, top_k=64.

## 3. Limites e ressalvas
- A comparação entre Anthropic, Google e OpenAI na 4.5a é leitura do guia (proposta didática); cada provedor descreve só o seu produto.
- A página do Google fala de modelos Gemini 4 e 3.6 em diante; o guia não verificou outros produtos do Google nem modelos abertos.
- A plataforma de avaliações da OpenAI está em descontinuação; reconferir a data antes de citar como vigente depois de 30/11/2026 (reconferido em 17/11/2026: frase de descontinuação mantida).
- Não verificado: datas de publicação das páginas (ausentes no texto extraído); segunda leitura independente.
- As fichas do Qwen e do Gemma são do fabricante: números de contexto e velocidade são afirmações dele, sem medição nossa. Conformidade com a definição de “aberto” da OSI: verificada em 16/11/2026 só pelas fichas, e as fichas não a demonstram (ver abaixo).
- Decisão do operador: ignorar o Mistral; o foco em modelos abertos é Qwen3.8 e Gemma 4. Benchmarks das fichas não são citados no guia.
- **OSI (1.7a):** OSI, Open Source AI Definition 1.0 (opensource.org/ai/open-source-ai-definition, hash `410a85c6be656536`) exige dados (descrição completa, listas de dados públicos e de terceiros), código completo de treino e execução e parâmetros em termos aprovados. Apache 2.0 consta como aprovada (opensource.org/license/apache-2-0). Gemma 4: a ficha traz um resumo geral dos dados (“web documents, code, images, audio, with a cutoff date of January 2025”) e links para GitHub e relatório técnico (arXiv:2607.02770, não lido). Qwen3.8-27B: a ficha não descreve dados de treino. Nenhuma declara conformidade. Conclusão: o guia os chama de “pesos abertos”, sem afirmar nem negar conformidade com a OSI.

Assinatura: claude - pessoal, 16/11/2026.
