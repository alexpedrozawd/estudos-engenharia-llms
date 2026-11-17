**O objetivo da formação é você conseguir especificar, arquitetar, integrar, avaliar e operar sistemas com LLMs, locais ou de fronteira, sem precisar programar**, explicando suas escolhas de modelos, contexto, ferramentas, segurança e custo.

**Decisão do operador (16/11/2026): o guia forma profissionais em arquitetura e engenharia de LLMs e não se limita ao AP AI Router.** Cada módulo ensina o conceito geral, com fonte pública conferida, e o aplica em exemplos empresariais (a Aurora Educação, fictícia, e a plataforma interna de IA descrita de forma genérica). O Router é fonte de experiência do autor, não caso principal: o nome não aparece no texto do guia, e uma medição ou decisão local entra só como uma ilustração entre outras, rotulada, nunca como única base de uma afirmação. Em cada exemplo, distinguimos fato registrado em fonte, situação construída (proposta didática) e, quando vier de evidência local, a sua origem e data.

**Regras de neutralidade para os módulos 6 a 16 (e revisões dos 1 a 5):**
1. Todo módulo abre pelo conceito geral e traz ao menos uma fonte pública (documentação, norma ou pesquisa) conferida por trecho literal. Fonte interna ou medição local não bastam sozinhas.
2. Cada assunto mostra mais de uma opção de fornecedor ou ferramenta quando elas existem (por exemplo, Anthropic, OpenAI e Google nas APIs; Ollama, llama.cpp e vLLM nos servidores). Nos modelos abertos, o foco são o Qwen3.8 e o Gemma 4, que o operador usa no servidor, com a ficha do fabricante como fonte; outros modelos abertos entram só se o operador pedir, sem preferir uma por ser a usada no Router. Prioridade para os módulos 11 (RAG), 13 (inferência local), 14 (roteamento) e 15 (LLMOps).
3. Termos, produtos e caminhos internos do Router não entram no texto; usar descrição genérica.
4. Dados do Router servem de insumo para exemplos numéricos só quando marcados como medição local ou situação construída.

**Esta é a sequência do conteúdo.** Dentro de cada linha, os assuntos avançam da esquerda para a direita.



|Ordem|Módulo|Progressão principal|
|-:|-|-|
|**1**|**Fundamentos de IA e LLMs**|Modelo → treinamento e inferência → tokens e contexto → geração → atenção e Transformers → capacidades e limitações → tipos de modelos|
|**2**|**Arquitetura de sistemas com LLM**|Componentes e fronteiras → a chamada ao modelo → streaming e latência → limites, erros e novas tentativas → estado e persistência → simultaneidade e capacidade|
|**3**|**Problemas e especificações**|Problema e usuário → resultado esperado → restrições → aceite → escolha do uso de IA → contratos e decomposição|
|**4**|**Prompts, parâmetros e respostas**|Instruções e exemplos → técnicas de prompt com fonte primária (exemplos, raciocínio passo a passo, instruções estruturadas) → mensagens → contagem de tokens → parâmetros → schemas → templates e tratamento de falhas|
|**5**|**Avaliação e experimentação**|Resultado adequado → exemplos e falhas → referência inicial → testes e avaliações → regressões → comparações confiáveis|
|**6**|**Engenharia de grafos aplicada a LLMs** *(concluído no guia em 17/11/2026)*|Dois sentidos de grafo → workflows, agentes e harness → quando não usar grafo → GraphRAG (global, local, multi-salto e custo de indexação) → grafos de estado, FSMs e eventos → checkpointers, stores e idempotência → subagentes e janelas limpas → custo 4×/15×, paralelismo e escada de decisão → casos na Aurora Educação|
|**7**|**Segurança e governança** *(concluído no guia em 17/11/2026)*|Dados e instruções → permissões → validação de ações → prompt injection → isolamento → privacidade e rastreabilidade|
|**8**|**Atos autodestrutivos e proporcionalidade** *(concluído no guia em 17/11/2026)*|Danos e fuga de escopo → preservação → recuperação → condições de parada → custo total → entupimento de contexto → decisões de baixo retorno|
|**9**|**Contexto e memória** *(concluído no guia em 17/11/2026)*|Informação necessária → fontes → orçamento de contexto → recuperação sob demanda → notas externas estruturadas fora da janela → histórico → continuidade e compactação vs. limpeza (referenciando subagentes do Cap. 6 sem duplicar) → ciclo de vida da sessão (quando limpar, handoff, retomada, pausa longa e expiração do cache)|
|**10**|**Ferramentas e integrações** *(concluído no guia em 17/11/2026)*|Chamada de função → contratos → processamento determinístico → filtros → erros e efeitos → interfaces e protocolos|
|**11**|**Busca, indexação e RAG** *(concluído no guia em 17/11/2026)*|Busca textual e por símbolos → estratégias de fragmentação (*chunking*) → índices → embeddings → recuperação híbrida (BM25 + vetor + *reranking*) → conexão com grafos de conhecimento/GraphRAG do Cap. 6 (sem duplicar) → geração com fontes → avaliação separada de recuperação e resposta|
|**12**|**Harnesses, workflows e agentes** *(concluído no guia em 17/11/2026)*|Aprofundamento de componentes e *harnesses* em laço (verificação fim a fim, teto de tentativas, registro estruturado em JSON; referenciando Cap. 6 sem duplicar) → interação simples → ferramentas → ciclo, desvios e limites → interrupção e retomada|
|**13**|**Inferência local** *(concluído no guia em 17/11/2026)*|Pesos e *runtime* → dimensionamento RAM/VRAM por perfil de setup (pesos totais em densos/MoE + KV cache + folga) → contexto de 8k a 256k (impacto linear do KV cache e GQA) → quantização de pesos (GGUF `Q4_K_M`/`Q6_K`/`Q8_0`; vLLM `AWQ`/`GPTQ`/`FP8`) e de KV cache (`f16` vs. `q8_0`/`fp8` vs. risco de `q4_0`; perplexidade vs. JSON/ferramentas) → quando ajustar localmente (QLoRA vs. RAG/prompt, requisitos de VRAM de treino) → diagnóstico|
|**14**|**Seleção e roteamento**|Caracterizar tarefas e matriz por finalidade (e-mail/rotina, escrita/materiais, revisões, dev *full stack* multi-arquivo) com *benchmarks* públicos (`IFEval`, `LiveCodeBench`, `SWE-bench`) e nível de supervisão humana (sem rótulos subjetivos de cargo humano) → comparar modelos → escolher destino → regras simples → escalonamento → contingência e reavaliação; trocar modelo ou esforço só ao abrir conversa nova|
|**15**|**Integração empresarial e LLMOps**|Sistema existente → integração por APIs → dados e ações → observabilidade → versionamento → lançamento e recuperação|
|**16**|**Eficiência e economia**|Medição → gargalos → eliminar redundância → melhorar ferramentas e contexto → cache e esforço (o que invalida o cache e quanto custa) → ponto ótimo de sessão → ajustes → compromissos e manutenção|



**Nenhum módulo ensina nem exige programar** (decisão de 15/10/2026). Os módulos 4, 5, 6, 10, 11, 12 e 15 tratam de desenho, contratos, critérios, falhas e operação. No texto do guia, textos curtos de configuração (JSON de requisição, schema, arquivo de parâmetros) e linhas de comando do runtime podem aparecer, só para ler e explicar; laboratórios seguem com escopo próprio (ver abaixo), sem programação. "Código determinístico" segue como conceito de arquitetura: o que o sistema decide sem o modelo. Quando um exemplo vier de um sistema que trata tarefas de código (como o Router), estuda-se a arquitetura (contrato, despacho, revisão, estado), não o código produzido. O módulo 2 absorve os conceitos de API, limite de taxa, streaming, estado e simultaneidade que os módulos seguintes pressupõem; o plano dele delimita a sobreposição com os módulos 4 (parâmetros e mensagens), 6 (grafos de estado e retomada), 9 (histórico), 12 (ciclo e estado), 13 (servidor local), 14 (contingência), 15 (operação) e 16 (custo e latência). O antigo módulo 2 (Software para sistemas com IA) está arquivado em `arquivo\capitulo-2-software\`. Avaliação, segurança, proporcionalidade e medição aparecerão também nos exemplos posteriores, com aprofundamento conforme necessário.

**Cada unidade de estudo terá uma estrutura previsível:**

1. **Objetivo concreto:** o que você conseguirá explicar ou fazer.
2. **Conceito:** explicação simples, definindo os termos novos.
3. **Funcionamento:** poucos passos, com um diagrama quando ajudar.
4. **Exemplo resolvido:** situação empresarial (Aurora ou plataforma interna genérica), com fonte pública quando houver.
5. **Aplicação e limites:** quando usar, condições e falhas relevantes.
6. **Uma pergunta:** recuperação do conteúdo, seguida de feedback.
7. **Ponto de retomada:** aprendizado central e próximo passo.

Usaremos parágrafos curtos, exemplos interessantes e poucas mudanças de assunto. Revisões breves serão espaçadas; exemplos resolvidos darão lugar gradualmente a decisões mais independentes. Essas estratégias têm apoio na [referência de aprendizagem do IES](https://ies.ed.gov/ncee/wwc/PracticeGuide/1).

O ritmo será ajustável, com pausas e retomadas fáceis. Períodos menores de foco e instruções escritas estão entre as adaptações descritas pelo [NICE](https://www.nice.org.uk/guidance/ng87/chapter/recommendations). Ajustaremos o formato pela sua experiência, preservando as preferências pedagógicas sem reproduzir detalhes de saúde nas aulas.

**A criação do material ocorrerá em cinco etapas.**



|Etapa|O que produziremos|Critério para avançar|
|-|-|-|
|**1. Preparar a entrada**|Uma primeira unidade do módulo 1, com exemplo e pergunta simples|Linguagem compreensível, extensão manejável e ponto de partida adequado|
|**2. Ajustar o formato**|Refinar explicações, exemplos, ritmo e tamanho a partir da sua resposta|Você consegue explicar a ideia central; dificuldades orientam o próximo bloco|
|**3. Produzir progressivamente**|Unidades numeradas, na sequência do mapa, incorporando pré-requisitos necessários|Cada unidade tem propósito claro, conteúdo correto e aplicação relevante|
|**4. Integrar conhecimentos**|Estudos de caso que combinam contexto, ferramentas, avaliação, modelos e operação|Você consegue justificar uma solução e reconhecer alternativas e limites|
|**5. Consolidar competências**|Revisões direcionadas e decisões profissionais mais completas|Você especifica, desenha, avalia e diagnostica uma solução com autonomia crescente|



Começaremos pela conversa. Não criaremos todos os capítulos antecipadamente: o formato será ajustado antes de multiplicar material. Exercícios iniciais serão conceituais e somente leitura. Laboratórios com execução dependerão de escopo próprio, preservando a sessão paralela e o ambiente operacional.

**O módulo de proporcionalidade terá duas partes complementares.**

* **Prevenção de danos:** ambiente errado, sobrescrita, perda de contexto, permissões excessivas, operações duplicadas e recuperação insegura.
* **Decisão de investimento:** técnicas que acrescentam mais estudo, chamadas, infraestrutura ou manutenção do que benefício.

Usaremos poucos casos representativos para ensinar a decisão: qual problema existe, se uma solução simples atende, que evidência justificaria aprofundar e qual é o custo total.

Engenharia de Grafos (GraphRAG e grafos de estado em agentes) foi consolidada no **Capítulo 6** em 17/11/2026 (decisão do operador, abrindo a Parte II e deslocando os módulos 6–15 anteriores para 7–16), com base nos 43 trechos conferidos em `pacote-de-fontes-engenharia-de-grafos-2026-11-17.md`. Os módulos futuros 9 (Contexto e memória), 11 (Busca, indexação e RAG) e 12 (Harnesses, workflows e agentes) referenciam o Capítulo 6 para evitar duplicação, aprofundando o que for específico de cada camada. Roteadores aprendidos, múltiplas GPUs, kernels, métodos formais, fine-tuning e arquiteturas multiagente complexas receberão **menções explicativas e sinais de necessidade** (quando compensam versus busca/fluxo simples), conforme a recomendação de aumentar complexidade apenas quando ela melhora os resultados de forma demonstrável ([referência de arquitetura](https://www.anthropic.com/research/building-effective-agents)).

**A qualidade será conferida durante a produção, em uma revisão breve de cada unidade:** fidelidade técnica, fonte pertinente, pré-requisitos, clareza, preservação das informações necessárias e ausência de aprofundamentos sem finalidade.

Usaremos documentação oficial vigente para parâmetros e implementação, pesquisas primárias para conceitos e, só como complemento rotulado, evidências locais. Afirmações sobre melhorias indicarão condições e limites. Por exemplo, cache de prefixo pode economizar processamento da entrada, mas não acelera diretamente a geração dos novos tokens. [Limite documentado pelo vLLM](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching/).

**Escolhi essa estrutura para desenvolver capacidade de decisão profissional com um custo de aprendizagem controlado.** Os fundamentos explicam os mecanismos; os módulos de arquitetura e de uso permitem aplicá-los; avaliação e operação permitem verificar e sustentar o resultado. As especializações ficam disponíveis sem disputar atenção com as competências centrais.

O ponto de partida será a primeira unidade do módulo 1: **“O que é um modelo de linguagem e como ele produz uma resposta?”**

**Referências públicas por módulo (revisão 1, 15/10/2026).** Para o guia não depender só do que o autor já usou, cada módulo deve incluir, além dos exemplos locais, as fontes públicas abaixo (consultadas em 15/10/2026 por resumo; entram no livro só com trechos literais conferidos, como nos capítulos 1 e 2). Detalhes e ressalvas em `revisao-1-cobertura-alem-do-que-foi-desenvolvido.md`.

|Módulo|Acrescentar ao plano do módulo|
|-|-|
|**4**|Técnicas de prompt com fonte primária: documentação oficial de prompting (página e data a conferir); Brown et al., arXiv:2005.14165 (exemplos no prompt); Wei et al., arXiv:2201.11903 (raciocínio passo a passo). Só entram com trecho literal conferido|
|**5**|Anthropic, *Demystifying evals for AI agents* (09/01/2026): 20 a 50 tarefas tiradas de falhas reais; avaliadores por código, por modelo e por pessoa; avaliar o resultado, não o caminho. Zheng et al., arXiv:2306.05685: juiz-LLM e seus vieses (posição, tamanho, autopreferência)|
|**6 (concluído)**|Engenharia de grafos aplicada a LLMs: 43 trechos literais de 16 fontes públicas primárias conferidos em `pacote-de-fontes-engenharia-de-grafos-2026-11-17.md` (`EG-01`–`EG-43`): Edge et al. (`arXiv:2404.16130`), Microsoft GraphRAG, Neo4j, LlamaIndex (`PropertyGraphIndex` e `Workflows`), LangGraph, Pydantic Graph e Anthropic (*Building effective agents*, *Multi-agent research system*, *Effective context engineering* e *Effective harnesses for long-running agents*). Casos adaptados para a Aurora Educação e comparativos de topologia marcados como *proposta didática*|
|**7 (concluído)**|52 trechos literais de 20 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-7-seguranca-e-governanca-2026-11-17.md` (`SG-01`–`SG-52`): OWASP Top 10 for LLM Applications 2025 v2.0 (`LLM00`–`LLM10` via repositório oficial no GitHub), NIST AI 600-1 (26/07/2024), LGPD (Lei nº 13.709/2018 atualizada, Portal da Câmara dos Deputados), MCP *Security Best Practices*, Wallace et al. (`arXiv:2404.13208`), Debenedetti et al. (`arXiv:2503.18813` / CaMeL), Anthropic (*sandboxing*, *mitigate jailbreaks*, *API and data retention*), OpenAI (*safety best practices*, *your data*) e Google Cloud (*Model Armor*, *zero data retention*)|
|**8 (concluído)**|60 trechos literais de 28 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-8-autodestrutivos-e-proporcionalidade-2026-11-17.md` (`AP-01`–`AP-60`): Denison et al. (`arXiv:2406.10162`), MacDiarmid et al. (`arXiv:2511.18397`), Ovadia et al. (`arXiv:2312.05934`), Liu et al. (`arXiv:2307.03172`), Chroma (*Context Rot*, 14/07/2025), NIST AI 100-1 e AI 600-1, OWASP v2.0 (`LLM06`, `LLM10`), Google SRE Book (caps. 8, 9, 13, 14, 21, 22), Anthropic (*Building effective agents*, *Effective context engineering*, *Effective harnesses*, *Writing tools for agents*, *Code execution with MCP*, *Best Practices for Claude Code*), OpenAI (*Errors and recovery*, *Guardrails and human review*, *Spend limits*, *Cost optimization*, *Optimizing LLM Accuracy*) e Google Cloud (*Introduction to tuning*, *Grounding overview*). Casos da Aurora Educação, tabela comparativa e método das quatro perguntas marcados como *proposta didática*|
|**9 (concluído)**|77 trechos literais de 14 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-9-contexto-e-memoria-2026-11-17.md` (`CM-01`–`CM-77`): Anthropic (*Effective context engineering*, *Effective harnesses*, *Context windows*, *Memory tool*, *Compaction overview*, *Context editing*, *Prompt caching*, *Effort*, *How Claude remembers your project*, *Best Practices for Claude Code*), OpenAI (*Conversation state*, *Compaction*, *Prompt caching*) e Google Cloud (*Context caching overview*), mais ilustração local de 23/10/2026 rotulada como amostra pequena|
|**10 (concluído)**|53 trechos literais de 16 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-10-ferramentas-e-integracoes-2026-11-17.md` (`FI-01`–`FI-53`): especificação oficial MCP `2026-07-28` (*Specification*, *Architecture*, *Tools*, *Resources*, *Security Best Practices*), JSON Schema, Anthropic (*Building effective agents*, *Writing effective tools*, *Code execution with MCP*, *Tool use*, *Implement tool use*, *Tool search tool*), OpenAI (*Function calling*, *Connectors and MCP servers*, *Errors and recovery*) e Google Cloud (*Function calling*)|
|**11 (concluído)**|42 trechos literais de 15 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-11-busca-indexacao-e-rag-2026-11-17.md` (`BR-01`–`BR-42`): Lewis et al. (`arXiv:2005.11401`), Reimers e Gurevych (`arXiv:1908.10084`), Nogueira e Cho (`arXiv:1901.04085`), Muennighoff et al. (`arXiv:2210.07316`), Es et al. (`arXiv:2309.15217`), Anthropic (*Contextual Retrieval*, *Effective context engineering*), OpenAI (*Embeddings*, *Retrieval*, *File search*), Google Cloud (*Get text embeddings*, *RAG Engine overview*, *Grounding overview*), `ripgrep` e `Tree-sitter` (incluindo decisão sobre busca por símbolos e referência ao Cap. 6 para GraphRAG)|
|**12 (concluído)**|99 trechos literais de 16 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-12-harnesses-workflows-e-agentes-2026-11-17.md` (`HW-01`–`HW-99`): Anthropic (*Building effective agents*, *Effective harnesses for long-running agents*, *Agent SDK overview*, *How the agent loop works*, *Work with sessions*), OpenAI (*Agents*, Agents SDK: *Running agents*, *Agent orchestration*, *Guardrails*, *Human-in-the-loop*, *Tracing*) e Google (ADK: *Agents*, *Loop agents*, *Resume stopped agents*). Referencia o Capítulo 6 (`EG-15`–`EG-30`, `EG-33`–`EG-43`) e não repete trechos dos Capítulos 6, 8 e 9. Casos da Aurora Educação, quadros e o registro de funcionalidades marcados como *proposta didática*|
|**13 (concluído)**|77 trechos literais de 20 fontes públicas primárias conferidos em `pacote-de-fontes-capitulo-13-inferencia-local-2026-11-17.md` (`IL-01`–`IL-77`): llama.cpp (*Quantize*, *HTTP server*), GGUF, vLLM (*Quantization*, AutoAWQ, GPTQModel, FP8, INT4, *Quantized KV Cache*, *Speculative Decoding*), Ollama (*FAQ*, *Context length*), PagedAttention (`arXiv:2309.06180`), decodificação especulativa (`arXiv:2211.17192`), LoRA (`arXiv:2106.09685`), QLoRA (`arXiv:2305.14314`), Mixtral (`arXiv:2401.04088`), GQA (`arXiv:2305.13245`) e as fichas do Qwen3.8-27B e do Gemma 4. Cálculos de memória (modelo ilustrativo de 40 camadas e 8 cabeças KV), quadros e casos da Aurora Educação marcados como *proposta didática*; a divergência entre as duas páginas do Ollama sobre o contexto padrão está registrada|
|**15**|OpenTelemetry, convenções para IA generativa (estado "Development" em 15/10/2026: nomes ainda mudam); lançamento sem interrupção, do relato multiagente|
|**14**|Matriz por finalidade e *benchmarks* públicos (`IFEval`, `LiveCodeBench`, `SWE-bench Verified/Pro` — trechos literais a conferir, ligando autonomia à revisão humana sem rótulos de senioridade humana). Troca de modelo ou esforço só em conversa nova: página de *esforço* da Anthropic (declarada em 13/11/2026, a conferir trecho literal) recomenda manter o esforço constante em conversa com cache; a página de *prompt caching* sustenta o custo da invalidação. Sobre troca de modelo invalidar o cache não há fonte lida (hipótese registrada)|
|**16**|Cache de prefixo e lote (unidade 2.3), esforço de raciocínio (unidade 1.4), multiplicador de tokens de agentes. Cache e esforço: o que invalida o cache, TTL de 5 min e 1 h, preços relativos (páginas da Anthropic, declaradas em 13/11/2026). Ponto ótimo de sessão: medição local de 23/10/2026 e modelo de estimativa (não é resultado medido)|

<!-- Autoria da transcrição: codex - ap. -->

