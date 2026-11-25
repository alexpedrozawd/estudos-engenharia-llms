# Changelog — Capítulo 19 (Frameworks de orquestração e agentes) e P08 LangGraph (25/11/2026)

Autoria: claude - pessoal. Etapa 5B, primeira entrega, do [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md). Lacuna fechada: frameworks de orquestração (55% das vagas do [mapa de vagas](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md); LangChain 45%, LangGraph 38%). Plano de 6 etapas aprovado pelo operador; etapas 1 a 5 sem commit, fechadas num único commit na etapa 6.

## Decisões do operador (25/11/2026)

- **D1** capítulo no formato do Cap. 18; **D2** extra `agentes` no `pyproject.toml`, instalado no CI, com `langgraph-checkpoint-sqlite` na série 3.x (teto `<4`); **D3** adaptador MCP próprio (sem `langchain-mcp-adapters`); **D4** supervisor em `StateGraph` puro; **D5** 27B como agente e 4B só para comparação; **D6** um `<svg>` do grafo do P08. Todas cumpridas.
- **Parte IV (decisão desta entrega, reversível, a confirmar pelo operador):** o Cap. 19 abre uma nova **Parte IV — Frameworks e plataformas de mercado** no sumário (`<ol start="19">`), que também receberá o Cap. 20. A introdução passa a dizer "19 capítulos em quatro partes". Alternativa, se o operador preferir: mover o Cap. 19 para o fim da Parte III.

## Etapas 1 a 4 — fontes, P08 e capítulo

- **Fontes:** [pacote-de-fontes-capitulo-19-frameworks-de-orquestracao-e-agentes-2026-11-25.md](../fontes/pacote-de-fontes-capitulo-19-frameworks-de-orquestracao-e-agentes-2026-11-25.md) com `59` trechos literais (LangChain, LangGraph, CrewAI, LlamaIndex, OpenAI Agents SDK, Semantic Kernel e Microsoft Agent Framework; o AutoGen está arquivado e o capítulo aponta o sucessor). `anthropic.com` bloqueia download: o capítulo remete à 8.1c para "começar sem framework". No [pacote de grafos](../fontes/pacote-de-fontes-engenharia-de-grafos-2026-11-17.md), hashes novos de `4` fontes LangGraph/LlamaIndex rebaixadas.
- **P08 [`08_langgraph_agentes`](../../laboratorios-mercado/08_langgraph_agentes/README.md):** laço agêntico do P06 portado para `StateGraph` (LangGraph `1.2.24`, `langchain-openai` `1.8.5`, `langgraph-checkpoint-sqlite` `3.1.3`): checkpoint SQLite, aprovação humana por `interrupt()` antes de ferramenta sensível (duas travas, com a *elicitation* do P03), lista de ferramentas permitidas, `max_passos = 4` e `recursion_limit = 25` convertido em recusa, supervisor com dois subagentes e marcadores de exercício. `13` smoke-tests offline com modelo falso. O P06 não mudou.
- **Execução real (Ollama `/v1`, RX 9070 XT):** 27B `8/8` e 4B `7/8` nas variantes P06, P08 (cliente próprio e `ChatOpenAI`) e supervisor; registros `execucoes/p08-langgraph-agentes-2026-11-25T14-41-44-0300.json` (27B) e `...T14-42-51-0300.json` (4B). Leitura dos números no README do P08.
- **HTML:** abertura + `18` partes `19.1a`–`19.6c` (framework ou código próprio, LangChain, grafo/estado/arestas, persistência e humano no circuito, multiagentes, panorama e operação), `24` questões (`18` de parte + `6` de fechamento), estudo de caso com rubrica, diagrama 19.1 (grafo do P08), bloco executável `cod-19-3c-py`, Parte IV no sumário, `12` termos no Glossário e Referências.
- **Aquarela `cap-19`:** gerada localmente (Qwen-Image), semente `6019`, prompt da linha `cap-19` de `arquivo/aquarelas-fase-5e/prompts.tsv` (oficina de cartógrafos com mesas ligadas por fios e um guardião no portão esperando o sinal, sem símbolos). A semente `5019` foi descartada por pseudoletras nos mapas. Embutida como `<img>` JPEG (`137 KB`); o CSS `.moldura`/`.moldura-texto`, já sem uso, saiu do HTML.
- **Integração:** `mercado_base/__init__.py` (projeto 08 em `PROJETOS`), `pyproject.toml` (extra `agentes`), `testes-offline.yml` (instala `[agentes]`), `testar-ferramentas.py` (8 projetos de mercado).

## Etapa 5 — auditoria (`/auditorias`)

- **Médio, corrigido — PII crua no checkpoint.** O LangGraph grava a entrada antes do primeiro nó, então o checkpoint guardava o CPF sem máscara (reproduzido com teste). Agora `AgenteLangGraph.perguntar` mascara a PII (`mercado_base.pii.mascarar_pii`) antes do `invoke`; o nó `verificar_entrada` junta os tipos de PII que já vêm no estado; o teste do caminho feliz confere todo o histórico do checkpoint (`get_state_history`). As execuções reais são anteriores à correção, que não muda o texto enviado ao modelo. A parte 19.4a ("Checkpoint também é dado pessoal") e a 19.6 foram reescritas conforme esse comportamento; o README do P08 ganhou o item "PII fora do checkpoint".
- **Médio, corrigido — instalação incompleta.** `laboratorios-mercado/README.md` instalava só `[containers]`, e os smoke-tests do P08 falhavam sem LangGraph. Agora instala `[containers,agentes]` e explica o extra.
- **Conferidos sem achados:** `24` questões contra código e pacote; `interrupt()` não contornável, lista permitida, sensível sem aprovação negado, limite de passos e recursão; P06 e `laboratorios/` sem diff; CI.

## Etapa 6 — documentação e validação

- Documentos: [`requisitos-de-formato-html-do-material.md`](../../requisitos-de-formato-html-do-material.md) §8 (uma aquarela por capítulo, hoje `19`; diagramas `18` a `24`, hoje `23`; remoção do CSS `.moldura`), `laboratorios-mercado/README.md` (8 projetos, `100` smoke-tests, linha do P08), `README.md`, `roadmap.md`, `CLAUDE.md` e o plano de prontidão.
- Contagens: `405` páginas lógicas, `477` questões (`119/119/120/119`, nenhuma com a correta estritamente mais longa), `163/163` tabelas com `.rolagem`, `540` termos, `514` `<dfn>`, `27` blocos executáveis (`24` ilustrativos), `23` SVG, `19` aquarelas. HTML sha `8f138045667262d9`; PDF regerado com `698` páginas A4 (antes `664`), sha `570e409a4985a2cb`, anterior em `arquivo/antes-capitulo-19-2026-11-25/`; páginas 7 (introdução), 611 (abertura e aquarela), 621 (diagrama 19.1) e 622 (questão) conferidas renderizadas.
- Validações: `guia.py fechar` `0` falhas (`validar-guia` `18 OK`); `laboratorios/executar_labs.py` `84` OK; `executar_smoke.py` `100` OK (P08 com `13`); `testar-ferramentas.py` `24` OK; `testar-fontes.py` `14` OK; `testar-livros.py` OK; `conferir-trechos.py` Cap. 19 `59/59` (grafos `29/46`: as `17` reprovações são fontes `anthropic-*` fora do cache, exceção já registrada); `gerar-exercicios.py --checar` `82` trechos em `27` labs e `--verificar labs|mercado` OK; `auditar-guia-navegador.mjs` (Playwright `chromium-1254` + `axe-core`): `0` estouros a `320 px` em `405` seções, `477/477` questões, `0` violações axe em `1280×800` e `320×640` (`color-contrast` como incompleto, para revisão manual).

## Achados baixos em aberto (aguardam decisão do operador)

- `agente_grafo.py`, `AgenteLangGraph._rodar`, ramo `GraphRecursionError`: devolve `ferramentas_chamadas = []` mesmo se ferramentas já rodaram. Inalcançável no fluxo normal (`max_passos = 4` para bem antes de `recursion_limit = 25`). Ajuste mínimo: ler `grafo.get_state(config).values`.
- Nota fora de escopo, pré-existente e não investigada: no Glossário, "Agente (8.1)" e "Workflow (8.1)" talvez apontem unidade defasada pela renumeração.

## Próximo

Etapa 5B, segunda entrega: Cap. 20 (LLMs em nuvem e serviços gerenciados) e Langfuse auto-hospedado no `compose.yaml`.
