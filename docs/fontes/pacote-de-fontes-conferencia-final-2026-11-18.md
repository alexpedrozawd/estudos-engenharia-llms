# Pacote de fontes — conferência final de afirmações numéricas (18/11/2026)

Conferência online, em 18/11/2026, de afirmações antes marcadas como `[Não verificado]`. Trechos literais lidos diretamente nas páginas; nenhuma divergência com o texto do guia.

| ID | Unidade | Fonte | Trecho literal | Resultado |
|---|---|---|---|---|
| CF-01 | 10.4a | anthropic.com/research/writing-tools-for-agents | "For Claude Code, we restrict tool responses to 25,000 tokens by default." | confirma |
| CF-02 | 11.4a | anthropic.com/news/contextual-retrieval | "reduced the top-20-chunk retrieval failure rate by 67% (5.7% → 1.9%)" | confirma |
| CF-03 | 11.4a | anthropic.com/news/contextual-retrieval | "(we used the top 150)"; "(we used the top 20)" | confirma |
| CF-04 | Cap. 11 | anthropic.com/news/contextual-retrieval | "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material)" | confirma |
| CF-05 | 11.2c | anthropic.com/news/contextual-retrieval | "the one-time cost to generate contextualized chunks is $1.02 per million document tokens" | confirma (premissas: chunks de 800 tokens, documentos de 8k) |
| CF-06 | 10.3b | anthropic.com/engineering/advanced-tool-use | "That's 58 tools consuming approximately 55K tokens before the conversation even starts." | confirma (cinco servidores MCP) |
| CF-07 | 10.3b | anthropic.com/engineering/advanced-tool-use | "Tools discovered on-demand as needed (3-5 relevant tools, ~3K tokens)" | confirma |
| CF-08 | 10.3b | platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool | "Claude’s ability to pick the right tool degrades once you exceed 30–50 available tools." | confirma |
| CF-09 | 10.3b | anthropic.com/engineering/code-execution-with-mcp | "This reduces the token usage from 150,000 tokens to 2,000 tokens—a time and cost saving of 98.7%" | confirma |
| CF-10 | 11.3c | arxiv.org/abs/2210.07316 | "MTEB spans 8 embedding tasks covering a total of 58 datasets and 112 languages." | confirma |
| CF-11 | 8.5a | trychroma.com/research/context-rot | "In this report, we evaluate 18 LLMs, including the state-of-the-art GPT-4.1, Claude 4, Gemini 2.5, and Qwen3 models." | confirma |
| CF-12 | Cap. 13 (sem menção no texto atual; registro de lacuna antiga) | docs.ollama.com/faq | "`OLLAMA_KV_CACHE_TYPE` - The quantization type for the K/V cache. Default is `f16`." (valores `f16`, `q8_0`, `q4_0`; exige Flash Attention) | confirma |
| CF-13 | Cap. 13 (idem) | github.com/ggml-org/llama.cpp (tools/server/README.md) | `-ctk, --cache-type-k TYPE` e `-ctv, --cache-type-v TYPE`, padrão `f16` | confirma |

Observação: o `research.trychroma.com/context-rot` redireciona (301) para `trychroma.com/research/context-rot`. As URLs `anthropic.com/engineering/*` redirecionam para `anthropic.com/research/*`, usadas no guia.

Não conferido nesta rodada: os demais itens `[Não verificado]` listados em `changelog-revisao-parte-2-2026-11-17.md` e `changelog-revisao-parte-3-2026-11-17.md` (cerca de cem afirmações menores por capítulo); permanecem como lacuna declarada, sem alteração do texto.

Assinatura: claude - pessoal
