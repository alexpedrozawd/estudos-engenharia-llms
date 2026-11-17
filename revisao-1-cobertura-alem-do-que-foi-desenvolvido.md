# Revisão 1 — o guia cobre só o que o operador desenvolveu?

Data: 15/10/2026. Autoria: claude - pessoal (Sonnet 5.5, effort High declarado pelo operador). Escopo: capítulos 1 e 2, introdução, glossário, referências e o mapa dos módulos 3 a 15. **Estado: diagnóstico aprovado e aplicado em 15/10/2026** (as inserções P1, as pontes P2 e a atualização do plano mestre; ver `changelog-revisoes-1-e-2.md`). O texto abaixo é o diagnóstico original, feito sobre o guia de hash `d900f667fda6ef0c`.

## 1. Resposta curta

**Não é só o que você desenvolveu, mas a seleção tem um viés e há lacunas.**
- O conteúdo técnico dos capítulos 1 e 2 vem de fontes públicas: Jurafsky e Martin, documentação da Anthropic, da OpenAI, do Ollama e do llama.cpp, RFCs, AWS e Google SRE. O Router e a Nanda Mac aparecem como exemplos: 25 e 17 menções em cerca de 15 mil palavras.
- O viés está em três pontos: (a) regras suas, das diretrizes locais, aparecem como princípio sem apoio público (13 citações); (b) só há dois sistemas reais de exemplo, ambos seus; (c) técnicas importantes que você ainda não usou ficaram de fora ou só apareceram no mapa dos módulos futuros.

## 2. Evidência medida (texto do guia, sem código, fontes e feedback)

| Item | Resultado |
|---|---|
| Menções ao Router / à Nanda Mac | 25 / 17 |
| Citações das "diretrizes locais" (fonte interna, sem link público) | 13: 1.2 (4), 1.3 (2), 1.6 (4), 2.6 (2), abertura do cap. 2 (1) |
| Termos vindos das suas diretrizes (sem fonte pública citada no guia) | *code-first, LLM-second*; *prompt patching*; *fine-tuning prematuro*; *entupimento de contexto*; fila distribuída como antipadrão. "Controle proporcional" é *proposta didática* |
| Fontes marcadas "não lido" | Weng, CS224N, CS336 e *Building effective agents* |

## 3. Achados A — regras locais sem apoio público (corrigir com convergência, sem apagar)

| Regra no guia | Apoio público verificado em 15/10/2026 | Proposta |
|---|---|---|
| "Código primeiro, LLM depois" e "usar LLM para lógica simples é inofensivo" (1.6) | Anthropic, *Building effective agents*, 19/12/2024: "find the simplest solution possible, and only increasing complexity when needed"; agentes só quando soluções simples falham | Acrescentar a fonte pública ao lado da regra local |
| "Entupimento de contexto" e "mais contexto não é melhor" (1.3) | Anthropic, *Effective context engineering*, 29/09/2025 (conjunto mínimo de tokens úteis; compactação, notas, subagentes, busca sob demanda); Liu et al., *Lost in the Middle*, arXiv jul/2023 (a precisão cai quando a informação está no meio); Chroma, *Context Rot*, 14/07/2025 (18 modelos; tarefas simples; os autores não explicam o mecanismo) | Hoje só a Anthropic sustenta o *context rot*. Acrescentar dois estudos independentes e os limites deles |
| "Fila distribuída é antipadrão" (2.6) | Google SRE (já citado) sustenta fila pequena e recusa controlada, mas não esse antipadrão | Manter como regra local rotulada; não dar a entender que é consenso |
| "Chave de idempotência" (2.4) | IETF, *Idempotency-Key header*: é um *Internet-Draft* **expirado** (rev. 07, 15/10/2025), não padrão | Corrigir o texto: prática comum, mas o cabeçalho ainda é rascunho |

## 4. Achados B — lacunas nos capítulos 1 e 2 (promissoras, relevantes, ainda não usadas por você)

Prioridade P1 = entra agora, como parágrafo curto, porque o capítulo fica incompleto ou desatualizado sem ela. P2 = só ponte e referência; o módulo dono aprofunda.

| # | Tema | Onde | Por que importa | Fonte verificada (15/10/2026) | Prior. |
|---|---|---|---|---|---|
| 1 | **Raciocínio antes de responder** (*thinking*, esforço) | 1.4 (+ 2.2, 2.3) | Muda custo, tempo e o limite de saída: os tokens de raciocínio contam como saída. Você já escolhe "effort" ao usar os modelos. A 1.4 só diz que o modelo "gera token a token" | DeepSeek-R1, arXiv:2501.12948 (jan/2025, v2 jan/2026): aprendizado por reforço fortalece raciocínio em tarefas verificáveis. Anthropic, *Extended thinking*: modo "adaptativo" e parâmetro de esforço nos modelos atuais; tokens de raciocínio faturados como saída | P1 |
| 2 | **Mistura de especialistas (MoE)** | 1.2 (parâmetros) | "Tamanho do modelo" deixa de ser um número só: total de parâmetros ≠ parâmetros ativos. Pesa na escolha de modelo local e na RAM (módulo 12) | Mixtral, arXiv:2401.04088: 47 bi no total, 13 bi usados por token | P1 |
| 3 | **Disjuntor** (*circuit breaker*) | 2.4 / 2.6 | Complementa espera crescente: parar de chamar um serviço que está falhando evita cascata. O capítulo cita a cascata e não dá esse remédio | Fowler, *CircuitBreaker* (06/03/2014); Google SRE cap. 22 (já citado) | P1 |
| 4 | **Cache de prefixo e processamento em lote** | 2.3 / 2.4 | São as duas alavancas de custo e latência mais usadas; o capítulo menciona "lote" sem explicar. Ligam com estado (2.5) | Anthropic, *Prompt caching* e *Batch processing* (leitura de cache bem mais barata que entrada normal; lote com desconto e conclusão assíncrona). Não citar valores no livro: mudam | P1 |
| 5 | **Saídas estruturadas** | 2.2 | A 2.2 diz "trate o texto como livre e valide". Hoje há geração restrita a um esquema: formato garantido, **verdade não**; recusa e corte por limite ainda precisam de tratamento | Anthropic, *Structured outputs* (GA) | P1 (ponte; módulo 4 aprofunda) |
| 6 | **MCP** (protocolo de ferramentas) | 2.1 | É uma fronteira nova: como o sistema liga modelo a ferramentas e dados. A especificação mais recente (2026-07-28) trata pedidos como sem estado e traz extensão para tarefas longas | modelcontextprotocol.io, especificação 2026-07-28; mantida sob a Agentic AI Foundation (Linux Foundation) segundo fontes secundárias | P2 |
| 7 | **Exemplo público de arquitetura real** | 2.4 / 2.5 | Hoje os únicos sistemas reais são seus. Há um relato público com checkpoints, retomada, novas tentativas e custo de 4× (agente) e 15× (multiagente) tokens | Anthropic, *Multi-agent research system* (13/06/2025) | P2 |
| 8 | **Decodificação especulativa, PagedAttention, LoRA/QLoRA** | 1.2, 1.5 | Explicam por que o servidor local fica mais rápido, como a memória do KV cache é gerida e como "ajustar" um modelo ficou barato. Hoje "fine-tuning" aparece só como erro | Leviathan et al., arXiv:2211.17192 (2–3× no teste dos autores); Kwon et al., arXiv:2309.06180; Hu et al., arXiv:2106.09685; Dettmers et al., arXiv:2305.14314 | P2 (módulos 12/15) |

Já cobertos e sem mudança: tokens, janela, geração, atenção, status HTTP, streaming, espera crescente, idempotência, fila.

## 5. Achados C — o que falta no mapa dos módulos 3 a 15

O mapa cobre bem a estrutura, mas deixa de citar estas referências públicas (todas verificadas):

| Módulo | Acrescentar ao plano do módulo |
|---|---|
| 5 Avaliação | Anthropic, *Demystifying evals for AI agents* (09/01/2026): começar com 20 a 50 tarefas tiradas de falhas reais; avaliadores por código, por modelo e por pessoa; avaliar o resultado, não o caminho. Zheng et al., arXiv:2306.05685: juiz-LLM concorda com pessoas em mais de 80%, mas tem vieses de posição, de tamanho e de autopreferência |
| 6 Segurança | OWASP Top 10 for LLM Applications 2025 (lista: injeção de prompt, vazamento de dados, cadeia de suprimentos, envenenamento, tratamento de saída, agência excessiva, vazamento do prompt de sistema, fraquezas de vetores, desinformação, consumo ilimitado; confirmada por fontes secundárias, o site oficial bloqueou a leitura direta). NIST AI 600-1, perfil de IA generativa (26/07/2024), complemento do AI RMF 1.0. LGPD e Lei de IA: **não verificadas nesta sessão** |
| 8 Contexto | Anthropic, *Effective context engineering* (compactação, notas fora da janela, subagentes, busca sob demanda) |
| 9 Ferramentas | MCP (especificação 2026-07-28); Anthropic, *Writing tools for agents* (11/09/2025): nomes claros, respostas enxutas, avaliar as ferramentas |
| 10 RAG | Lewis et al., arXiv:2005.11401 (origem); Anthropic, *Contextual retrieval* (19/09/2024): busca híbrida (palavras + significado) e reordenação; ganhos medidos pelos próprios autores, que variam por modelo e base. O mapa tem "busca por símbolos" mas não cita busca híbrida nem reordenação |
| 11 Agentes | *Building effective agents*: cinco padrões de fluxo (encadeamento, roteamento, paralelização, orquestrador-trabalhadores, avaliador-otimizador); multiagente só quando vale o custo |
| 12 Inferência local | MoE, PagedAttention, decodificação especulativa, LoRA/QLoRA (itens acima); quantização (fonte ainda a escolher) |
| 14 LLMOps | OpenTelemetry, convenções para IA generativa: **ainda em estado "Development"** (instáveis; nomes já mudaram em 2026). Lançamento "arco-íris" do relato multiagente |
| 15 Eficiência | Cache de prefixo, lote, esforço de raciocínio, multiplicador de tokens de agentes |

## 6. Limites desta revisão
- As leituras da web foram **resumos por ferramenta**, não trechos literais. Nada disso entra no guia sem o fluxo do projeto: pacote de fontes com trechos literais, `conferir-trechos.py` e leitura em Opus 5.5 High.
- Não mediu qualidade pedagógica nem testou o guia com leitor real.
- Multimodalidade, quantização, LGPD, Lei de IA e comparações de modelos não foram pesquisadas aqui: ficam como candidatas.
- Páginas de documentação mudam (a de cache e a de raciocínio não trazem data): citar com data de consulta e sem valores numéricos.

## 7. Restrição de tamanho
As unidades já estão no teto (entre 1.150 e 1.380 palavras; a 2.4 passa do teto em 32). As inserções P1 somam cerca de 700 palavras no total. **Elas só cabem se a revisão 2 (linguagem simples) enxugar o texto.** Por isso a recomendação é fazer as duas juntas, unidade por unidade.

## 8. Decisões pedidas (aprovadas pelo operador em 15/10/2026: "ok aprovo")
1. Aplicar as inserções P1 (itens 1 a 5 + convergência pública do Achado A)? P2 entram só como frase de ponte e referência.
2. Atualizar o plano mestre com o Achado C (referências por módulo)?

claude - pessoal, 15/10/2026
