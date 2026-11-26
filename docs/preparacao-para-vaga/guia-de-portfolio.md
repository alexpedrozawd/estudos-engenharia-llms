# Guia de portfólio: como apresentar os projetos

Quatro projetos cobrem o que as vagas mais pedem (agentes `84%`, APIs `80%`, RAG `78%`, avaliação `60%`, segundo o [mapa reconferido](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md#reconferência-em-26112026-55-vagas)). Para cada um, há um resumo de 30 segundos, uma versão de 2 minutos, as perguntas prováveis e o que não afirmar.

## Regras para todos

- **Número com origem:** todo número sai de um registro em `laboratorios-mercado/execucoes/` ou de um teste. Diga a data, o modelo e o tamanho da amostra.
- **Limite junto do resultado:** dados sintéticos gerados pelo `qwen3.8:27b-ud-iq3_xxs`, revisão amostral feita por modelo de fronteira, sem revisão humana, hardware local (RX 9070 XT de 16 GB compartilhada) e nenhum usuário real.
- **Decisão com motivo:** para cada escolha, a alternativa descartada e o que faria mudar de ideia.
- **Não diga** "em produção", "com clientes" ou "sem alucinação". Diga "projeto de estudo com práticas de produção".
- **Demonstração:** os smoke-tests rodam offline e sem chave (`.venv-mercado/bin/python -I laboratorios-mercado/executar_smoke.py`). A execução real exige Ollama e `pgvector` locais (comandos no README de cada projeto).

## P02 — RAG de produção com `pgvector`

**30 segundos:** "Montei um RAG com busca híbrida no PostgreSQL com `pgvector`, controle de acesso por perfil dentro da consulta SQL e avaliação estatística. Com `151` perguntas, mostrei que a reordenação por LLM melhora a posição do trecho certo, mas que, no acerto entre os quatro primeiros, a diferença contra a busca híbrida ainda pode ser acaso."

**2 minutos:**
- **Problema:** perguntas sobre regulamentos com siglas, tabelas, versões revogadas e documentos restritos.
- **Decisões:** `pgvector` em vez de banco vetorial dedicado, para ter ACL e vigência na mesma consulta SQL (trade-off no [caso 1](casos-de-system-design.md#caso-1--rag-sobre-documentos-internos-com-controle-de-acesso)); busca lexical em português + vetorial com RRF; tabelas em Markdown com cabeçalho repetido; perguntas que escolhem a variante separadas das que medem.
- **Números (26/11/2026, `57` documentos, `275` trechos):** *reranker* LLM com acerto@4 `63/74` (Wilson 95% [`0,75`; `0,91`]) e MRR `+0,16` a `+0,18` sobre as demais variantes, com intervalo acima de zero; contra as híbridas no acerto@4, McNemar `p = 0,125` e `0,22`; `0` vazamentos de ACL em `26` consultas restritas; p50/p95 da geração `1.337 / 1.643 ms`.
- **Limites:** corpus e perguntas do mesmo LLM; fidelidade lexical não reconhece paráfrase; conexão por operação (em produção, *pool*); varredura iterativa do `pgvector` desligada.

**Perguntas prováveis:** por que não Pinecone; como o filtro de ACL interage com o índice HNSW; como escolheu `k = 4`; quanto custa o *reranker* (`8` chamadas por pergunta); como trocaria o modelo de embedding sem parar o serviço.

## P06 — Integrador de produção

**30 segundos:** "É uma API FastAPI que junta RAG com ACL, agente com ferramentas MCP, saída estruturada, roteamento entre modelo local e de nuvem, guardrails e observabilidade. Testei com red teaming automatizado: foram `342` tentativas e `3` achados, todos corrigidos com teste de regressão."

**2 minutos:**
- **Problema:** um assistente acadêmico que lida com dado pessoal, documento restrito e ações por ferramenta.
- **Decisões:** perfil máximo vinculado à chave no servidor (anti-BFLA); dado pessoal sempre na rota local; `json_schema` estrito com reparo e degradação segura; histórico limitado; traces `gen_ai.*` sem texto nem PII; provedores de nuvem pelo endpoint compatível com OpenAI de cada um.
- **Números:** anti-BFLA real `4/4` (`401`, `403` na elevação, `200` sem vazamento e `200` autorizado); na GPU (25/11/2026), 27B com p50 `7,9 s` / p95 `17,8 s` e 4B com p50 `2,4 s` / p95 `4,6 s`, ambos com `0` reparos de esquema; garak `0.17.1` com `14` sondas e `342` tentativas, corrigindo `500` → `503` com `Retry-After`, *tags* Unicode ocultas e controles ANSI; `33` testes offline (`20` do integrador e `13` de nuvem).
- **Limites:** padrões de injeção em lista fixa; tokens do Entra ID e do OAuth do Vertex sem renovação; nuvem testada só offline; preços ilustrativos.

**Perguntas prováveis:** como a autenticação decide o perfil; o que acontece quando o modelo de nuvem cai; por que `503` e não `500`; o que o red teaming não cobre (ataques adaptativos e várias rodadas); como mediria custo por rota.

## P08 — Agentes com LangGraph

**30 segundos:** "Portei o laço do agente do P06 para LangGraph, com *checkpoint*, pausa para aprovação humana antes de ferramenta sensível, limite de passos e um supervisor com dois subagentes. Comparei com o laço próprio no mesmo modelo e no mesmo RAG: mesma qualidade, mais garantias e mais código."

**2 minutos:**
- **Problema:** ações sensíveis precisam de aprovação humana que sobreviva a uma pausa longa.
- **Decisões:** `interrupt()` antes do nó de ferramentas, sem efeito colateral antes da pausa; duas travas (grafo e *elicitation* do servidor MCP); PII mascarada antes de entrar no *checkpoint*; supervisor com `StateGraph` puro; nenhum redutor `operator.add` no estado, porque o subgrafo duplicava mensagens (bug reproduzido em `langgraph 1.2.24`).
- **Números (25/11/2026, 27B):** `8/8` critérios em todas as variantes; `4` chamadas MCP contra `5` do P06 (a sensível nem chega ao servidor); supervisor `+1,4 s` no p50; sem modelo, `2` a `3 ms` de sobrecarga do grafo; `205` linhas lógicas no núcleo do grafo contra `148` do laço próprio; `13` smoke-tests offline.
- **Limites:** `8` cenários (leitura qualitativa); ordem das variantes não sorteada; `SqliteSaver` só para desenvolvimento (em produção, `PostgresSaver`).

**Perguntas prováveis:** quando não usar framework; como retomar uma conversa dias depois; o que guarda o *checkpoint* e por quanto tempo; quando um supervisor compensa.

## Projeto final — assistente acadêmico (`laboratorios/projeto_integrador/`)

**30 segundos:** "É o estudo de caso final do guia: um esqueleto que junta guardrails, RAG com citação conferida, chamado com aprovação e idempotência, roteamento pelo risco, rastros, custo mensal e portão de versão pelo limite inferior de Wilson. Os testes cobrem os caminhos críticos com um modelo simulado."

**2 minutos:**
- **Decisões:** risco alto nunca é rebaixado para um modelo mais barato e vai para a fila humana quando a fronteira cai; resposta que cita fonte não recuperada é barrada; chamado não duplica (chave de idempotência); a versão só sobe se o limite inferior de Wilson passar o mínimo.
- **Números:** `5` testes offline (caminho feliz com dado pessoal mascarado, bloqueios e risco, chamado sem duplicar, portão e rastros, custo).
- **Limites:** modelo simulado, sem execução real; é a ponte entre os labs didáticos e os projetos de mercado (P02, P06 e P08 são a versão real das mesmas ideias).

**Como apresentar:** como mapa de decisões, não como produto. Mostre a tabela "peça → laboratório de origem" do README e aponte qual projeto de mercado leva cada peça adiante.

## Ordem sugerida numa entrevista

1. P06 como visão geral (2 min).
2. Um aprofundamento escolhido pela vaga: P02 (RAG ou dados), P08 (agentes ou framework) ou P04 e P07 (avaliação ou fine-tuning; números nos casos [5](casos-de-system-design.md#caso-5--lançar-uma-versão-nova-sem-susto) e [7](casos-de-system-design.md#caso-7--ajustar-recuperar-ou-só-instruir)).
3. Um erro que você encontrou e corrigiu, com o método do [bloco de diagnóstico](entrevista-comunicacao-e-diagnostico.md#3-diagnosticar-falhas-não-determinísticas).
4. O que faria a seguir: revisão humana dos dados, deploy com teto de gasto, carga com usuários reais.

claude - pessoal, 26/11/2026.
