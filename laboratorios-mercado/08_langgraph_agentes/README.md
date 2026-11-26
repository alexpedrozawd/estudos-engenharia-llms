# 08 — Agentes com LangGraph

O laço agêntico do projeto 06 (ferramentas MCP, `tool_calls`, mensagens `tool` e resposta estruturada) portado para um `StateGraph` do LangGraph, com checkpoint em SQLite, aprovação humana por `interrupt()`, limite de passos e um supervisor com dois subagentes. Proposta didática da Aurora Educação, instituição fictícia. O P06 não muda: o P08 reaproveita os guardrails, o `RespostaEstruturada` e a conversão MCP → `tools` do P06, o RAG do P02, o servidor MCP do P03 e o `mercado_base`.

```text
START → verificar_entrada ─(bloqueado)→ END
             │
         recuperar → agente ─(sem chamadas)→ consolidar → verificar_saida → END
                       │  ↑
      (sensível)→ aprovar │   interrupt(): pausa e grava o checkpoint até a decisão humana
                       ↓  │
                    ferramentas ─(passos >= max_passos)→ consolidar

Supervisor: START → verificar_entrada → supervisor → academico | calculo (subgrafos acima, sem a guarda) → END
```

| Arquivo | Papel |
|---|---|
| `agente_grafo.py` | `Estado`, nós, arestas condicionais, `construir_grafo`, `construir_supervisor` e a fachada `AgenteLangGraph` (`perguntar`, `retomar`, recusa segura no `GraphRecursionError`) |
| `ferramentas_mcp_grafo.py` | adaptador próprio MCP → grafo (37 linhas lógicas), sem `langchain-mcp-adapters` |
| `modelo_langchain.py` | adaptador de um chat model do LangChain (`ChatOpenAI`) para a interface `completar_chat` |
| `executar_p08_real.py` | bateria do P06 contra o Ollama `/v1`: P06 × P08 no mesmo RAG e no mesmo modelo |
| `test_p08_langgraph.py` | 13 smoke-tests offline com modelo falso, MCP em processo e um checkpointer novo por teste |

## Dependências

Extra opcional `agentes` (`langgraph`, `langchain-openai`, `langgraph-checkpoint-sqlite`), instalado também no CI:

```bash
.venv-mercado/bin/pip install -e "./laboratorios-mercado[agentes]"
.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py --alvo 08_langgraph_agentes
```

Versões conferidas em 25/11/2026: `langgraph 1.2.24`, `langgraph-checkpoint-sqlite 3.1.3` (numeração própria, série 3.x; por isso o teto é `<4`), `langchain-core 1.8.4`, `langchain-openai 1.8.5`, `mcp 2.3.0`.

## Decisões e segurança

- **Aprovação humana não contornável.** Toda ferramenta sem `readOnlyHint` no servidor MCP é sensível (hoje, `executar_python_isolado`). O nó `aprovar` chama `interrupt()` antes do nó `ferramentas`; antes do `interrupt()` ele só lê o estado, porque na retomada o nó roda de novo desde o início, e não há `try/except` em volta dele. Valor de retomada que não seja `{"aprovar": true}` conta como negado.
- **Duas travas.** Mesmo aprovada no grafo, a execução passa pela *elicitation* do servidor do P03, que o adaptador só aceita para a chamada aprovada; qualquer outra é recusada.
- **Negar não é fingir sucesso.** Ferramenta negada não executa, e a mensagem `tool` diz isso ao modelo. Ferramenta fora da lista permitida do agente também não executa.
- **Limite de passos.** `max_passos = 4` chamadas ao modelo (como no P06) leva à consolidação; `recursion_limit = 25` é a rede de segurança: estourou, vira recusa (`status = "limite_de_passos"`), nunca exceção para quem chamou; as ferramentas que já rodaram continuam em `ferramentas_chamadas`, lidas do checkpoint (desde 25/11/2026).
- **Persistência.** `SqliteSaver` serve para desenvolvimento e testes; em produção, use `PostgresSaver`. O `thread_id` é o cursor da conversa: o teste retoma, com um grafo **novo** sobre o mesmo arquivo SQLite, uma execução pausada no `interrupt()`.
- **PII fora do checkpoint.** O checkpointer grava a entrada antes do primeiro nó, e o histórico não é reescrito. Por isso `AgenteLangGraph.perguntar` mascara CPF, e-mail e telefone antes do `invoke`; o teste do caminho feliz confere que o CPF não aparece em nenhum checkpoint. Quem chamar `grafo.invoke` direto precisa mascarar antes. O banco ainda guarda mensagens, resultados de ferramentas e decisões humanas: defina retenção, acesso e exclusão. As execuções reais de 25/11/2026 são anteriores a essa correção, que não muda o texto enviado ao modelo.
- **Supervisor com StateGraph puro** (sem `langgraph-supervisor`). O supervisor classifica em JSON validado; destino inválido cai no fallback `academico`. Cada subagente só vê as ferramentas do seu papel (`academico`: `consultar_prazo`; `calculo`: `calcular_media_ponderada` e `executar_python_isolado`), e o `interrupt()` funciona dentro do subgrafo.
- **Armadilha do redutor.** Com `Annotated[list, operator.add]`, um subgrafo usado como nó devolve o estado inteiro, e o pai soma de novo o que já tinha (mensagens duplicadas; reproduzido em `langgraph 1.2.24`). Por isso nenhum campo do `Estado` usa redutor: cada nó devolve a lista completa.

## Execução real (25/11/2026)

```bash
.venv-mercado/bin/python -I laboratorios-mercado/08_langgraph_agentes/executar_p08_real.py --modelos qwen3.8:27b-ud-iq3_xxs --registrar
.venv-mercado/bin/python -I laboratorios-mercado/08_langgraph_agentes/executar_p08_real.py --modelos qwen3:4b-instruct --registrar
```

Ollama `/v1` na GPU (AMD RX 9070 XT), `reasoning_effort = "none"`, temperatura `0`, embeddings `qwen3-embedding:0.6b` sobre os `41` trechos do corpus Aurora em armazém em memória, uma chamada de aquecimento por modelo. Os `8` cenários são os do P06 (`cliente_integrador_real.CENARIOS`); o pedido de execução de código é negado por política. Registros: `execucoes/p08-langgraph-agentes-2026-11-25T14-41-44-0300.json` (27B) e `...T14-42-51-0300.json` (4B).

| Modelo | Variante | Critérios | p50 | p95 | Chamadas MCP | Interrupções | Tokens em cache |
|---|---|---|---|---|---|---|---|
| 27B (agente) | P06, laço próprio | 8/8 | 6,58 s | 20,61 s | 5 | 0 | 9.462 |
| 27B (agente) | P08, cliente próprio | 8/8 | 5,89 s | 19,72 s | 4 | 1 | 12.936 |
| 27B (agente) | P08, `ChatOpenAI` | 8/8 | 5,87 s | 27,34 s | 4 | 1 | 12.935 |
| 27B (agente) | P08, supervisor | 8/8 | 7,32 s | 18,41 s | 2 | 1 | 7.799 |
| 4B (comparação) | P06, laço próprio | 7/8 | 1,53 s | 4,77 s | 5 | 0 | 9.414 |
| 4B (comparação) | P08, cliente próprio | 7/8 | 1,05 s | 4,72 s | 4 | 1 | 11.750 |
| 4B (comparação) | P08, `ChatOpenAI` | 7/8 | 1,03 s | 5,72 s | 4 | 1 | 11.750 |
| 4B (comparação) | P08, supervisor | 7/8 | 1,43 s | 5,45 s | 2 | 1 | 7.591 |

Latência sobre os `7` cenários não bloqueados. VRAM no Ollama: 27B `10,01 GiB`, 4B `2,96 GiB`, embeddings `1,13 GiB`.

Como ler:

- **Qualidade igual.** Com temperatura `0`, P06 e P08 (cliente próprio) deram respostas idênticas em `6` dos `8` cenários em cada modelo, e o P08 com `ChatOpenAI` repetiu as do cliente próprio em `8/8`: o adaptador LangChain não mudou o comportamento. O 4B falha o mesmo cenário (`pii`) em todas as variantes: cita os 75% e depois diz que "não é possível determinar". É limite do modelo, não da orquestração.
- **A latência não mede o framework.** As variantes rodam sempre na mesma ordem, e as primeiras pagam o *prefill* que as seguintes reaproveitam do cache de prefixo (por isso o P06, que roda primeiro, tem menos tokens em cache). O p95 com `n = 7` é praticamente o pior caso (`complexa-fallback`, que variou de 22 s a 35 s no 27B). A sobrecarga do grafo aparece limpa no caminho bloqueado, sem modelo: de `2` a `3 ms` no P08 (com gravação do checkpoint no SQLite) contra `0,01` a `0,02 ms` no P06.
- **Diferença de comportamento no código.** O P06 chama `executar_python_isolado` e o servidor nega por falta de aprovação; o P08 pausa **antes** de chamar, e a ferramenta nem chega ao servidor (`4` chamadas MCP contra `5`).
- **Supervisor.** Custa uma chamada de classificação a mais (+1,4 s no p50 do 27B; +0,4 s no 4B) e roteou do mesmo jeito nos dois modelos os `7` cenários não bloqueados (`calculo` para média e código; `academico` para o resto). Com menos ferramentas à vista, os subagentes chamaram menos ferramentas (`2`), sem perder critério nesta bateria.
- **Código.** O laço do P06 (`_executar_agente_e_gerar`) tem `148` linhas lógicas; o núcleo do grafo do P08 tem `205`, mais `37` do adaptador MCP. A diferença paga persistência, retomada, aprovação humana, lista de ferramentas permitidas e limite de passos, que o P06 não tem. O supervisor soma `35` linhas; a fachada, `29`; o adaptador LangChain, `38`. Método: linhas não vazias, sem comentários e sem docstrings, contadas com `ast`.

Limites: `8` cenários servem para leitura qualitativa, não para inferência estatística; a ordem das variantes não foi sorteada; os critérios são verificações de texto simples e estão em `CRITERIOS`.
