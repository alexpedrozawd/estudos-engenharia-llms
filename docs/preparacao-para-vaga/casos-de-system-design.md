# Casos de system design de LLM com rubrica

Dez casos para treinar entrevistas de arquitetura (`73%` das vagas do [mapa reconferido em 26/11/2026](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md#reconferência-em-26112026-55-vagas)). Cada um parte de um estudo de caso do guia, que é mais curto, e acrescenta o que a entrevista cobra: perguntas de esclarecimento, estimativas, alternativas e números medidos no projeto. Empresa dos enunciados: Aurora Educação, fictícia.

Premissas marcadas com "suponha" são hipóteses de treino. Números com origem em `laboratorios-mercado/execucoes/` foram medidos na RX 9070 XT local, com dados sintéticos e revisão amostral por modelo de fronteira (revisão humana fora do escopo por uso pessoal).

## Como treinar (45 minutos)

1. **Esclarecer (5 min):** usuários, volume, risco, o que é sucesso e o que fica fora.
2. **Estimar (5 min):** requisições por segundo no pico, tokens por requisição, custo por mês e latência p95 desejada.
3. **Desenhar (15 min):** fluxo de dados de ponta a ponta, com contratos e pontos de falha.
4. **Escolher e defender (10 min):** pelo menos dois trade-offs, cada um com o que mudaria a decisão.
5. **Avaliar e operar (10 min):** conjunto de avaliação, portão de versão, observabilidade, contingência e custo.

Fale em voz alta e grave. Depois, pontue com a rubrica e compare com a resposta de referência do caso.

## Rubrica comum (0 a 16)

| Critério | 0 — insuficiente | 1 — esperado de pleno | 2 — sinal de sênior |
|---|---|---|---|
| 1. Esclarecimento | começa desenhando | pergunta usuários, volume, risco, sucesso mensurável e restrições (LGPD, orçamento) | negocia escopo e diz o que não fará na primeira versão |
| 2. Estimativas | nenhuma | ordem de grandeza de volume, tokens, custo e p95 | usa a conta para decidir (cache, GPU própria, tamanho do índice) |
| 3. Arquitetura | caixas sem fluxo | componentes com contratos, dados e pontos de falha | evolução por fases e o que fica reversível |
| 4. Modelo e recuperação | "o maior modelo" | modelo por tarefa, roteamento e recuperação medida | compara opções com dado ou propõe o teste que decide |
| 5. Avaliação | "testar na mão" | conjunto de avaliação, métrica e portão de versão | juiz calibrado, intervalos de confiança, offline × online |
| 6. Segurança e privacidade | ignora | ACL na busca, PII, injeção e menor privilégio | modelo de ameaça, red teaming, retenção e base legal |
| 7. Operação | nada | traces, métricas, timeouts, contingência e cotas | SLO, canário, rollback, teto de gasto e runbook |
| 8. Trade-offs e comunicação | solução única, sem custo | dois trade-offs explícitos | explica limites para o negócio e separa decisão reversível de irreversível |

**Referência para autoavaliação** (didática, não é padrão de mercado): pleno a partir de `9`, sem zero nos critérios 1, 5 e 6; sênior a partir de `13`, sem zeros.

## Mapa dos casos

| Caso | Tema | Base no guia | Prática no projeto |
|---|---|---|---|
| 1 | RAG com controle de acesso e escolha do banco vetorial | Cap. 7 (busca de editais), Cap. 12 | P02 |
| 2 | Agente com ferramentas, aprovação humana e supervisor | Caps. 10, 11 e 19 (agente de matrícula) | P03, P08 |
| 3 | Gateway de modelos para três áreas | Cap. 16 (gateway), Cap. 20 | P06 |
| 4 | Extração estruturada de documentos | Cap. 4 (extração de inscrições), Cap. 6 | P06, P07 |
| 5 | Lançar uma versão nova sem susto | Cap. 5 (troca v1 → v2), Cap. 17 (v5) | P07 |
| 6 | Servir localmente ou contratar API gerenciada | Cap. 14 (30 tutores), Cap. 20 (nuvem) | P01 |
| 7 | Ajustar, recuperar ou só instruir | Cap. 15 (ajustar ou não) | P04 |
| 8 | Tutoria com sessões longas | Cap. 9 (tutoria), Cap. 18 | P06 |
| 9 | Dados de alunos com provedor externo | Cap. 12 (dados de alunos), Cap. 13 | P06 e red teaming |
| 10 | A qualidade caiu e ninguém sabe por quê | Cap. 17, Cap. 9 (feedback) | P05, P06, Langfuse |

---

## Caso 1 — RAG sobre documentos internos com controle de acesso

**Enunciado:** "Queremos que alunos, docentes e a coordenação perguntem sobre regulamentos, editais e manuais. Alguns documentos são restritos. Como você faria?"

**Perguntas que você deve fazer:** quantos documentos e com que frequência mudam; quem pode ver o quê (perfil, curso, unidade); se há versões vigentes e revogadas; tabelas e PDFs escaneados; latência aceitável; se a empresa já usa PostgreSQL e em qual nuvem.

**Suponha:** 20 mil documentos, 2 milhões de trechos de 300 palavras, embeddings de `1024` dimensões, 50 consultas por segundo no pico, p95 da busca até 300 ms.

**Arquitetura de referência:**
- Ingestão: extração com tabelas preservadas (cabeçalho repetido em cada pedaço), metadados de perfil e vigência em cada trecho e reindexação por evento de publicação.
- Busca: híbrida (lexical para siglas e códigos + vetorial), fusão RRF e *reranker* (reordenação por um modelo) só nos primeiros candidatos.
- ACL: filtro por perfil **na consulta ao banco**, nunca depois da geração. O perfil vem da autenticação, não do pedido do usuário (anti-BFLA, ou seja, contra o uso de função sem permissão).
- Geração com citação obrigatória e recusa quando nada relevante for recuperado.

**Trade-off central: onde guardar os vetores**

| Opção | Bom para | Cuidado |
|---|---|---|
| `pgvector` no PostgreSQL | dados e vetores no mesmo banco ([BV-01](../fontes/pacote-de-fontes-bancos-vetoriais-2026-11-26.md)), com ACID e `JOIN` com as tabelas de permissão (BV-22); busca exata por padrão, com *recall* (proporção dos relevantes recuperados) perfeito (BV-02) | com índice aproximado, o filtro roda **depois** da varredura do índice: um filtro que casa `10%` das linhas devolve em média `4` linhas com HNSW e `ef_search = 40` (BV-05); use varredura iterativa, disponível desde a `0.8.0` (BV-06). O HNSW gasta mais memória e demora mais para construir (BV-04) |
| Pinecone (gerenciado) | sem operar servidor; roda como serviço gerenciado na AWS, no GCP e na Azure (BV-12); *namespaces* isolam inquilinos (BV-14) | filtrar por metadado num *namespace* grande cobra a varredura de tudo: `100` RUs contra `1` RU com um *namespace* por inquilino (BV-15); dados fora do seu banco, com contrato e residência a conferir (Cap. 20) |
| Weaviate (banco vetorial dedicado) | busca híbrida nativa com BM25F (BV-19), *multi-tenancy* com um *shard* por inquilino (BV-20) e índice *flat* para coleções pequenas (BV-18) | mais um sistema para operar ou contratar; mesma análise de residência |
| FAISS (biblioteca) | busca em memória, inclusive em GPU (BV-07, BV-08), para lotes, protótipos e serviços sem filtro complexo | não é banco: sem ACL, transação nem persistência própria; todos os índices ficam na RAM (BV-10) |

**Conta que decide:** pela fórmula do FAISS, o HNSW gasta `(d × 4 + M × 2 × 4)` bytes por vetor (BV-21). Com `d = 1024` e `M = 32`, são `4.352` bytes, e dois milhões de trechos ocupam cerca de `8,7 GB`. O `pgvector` tem estrutura própria, mas a ordem de grandeza mostra que o índice cabe numa máquina. Esse volume, com ACL por perfil, cabe no `pgvector` com varredura iterativa. Um serviço gerenciado passa a valer quando há muitos inquilinos isolados, muita escrita ou falta de equipe para operar o PostgreSQL.

**Armadilhas:** filtrar ACL na resposta (o modelo já viu o trecho); medir só a resposta e não a busca; trocar de banco sem um conjunto de perguntas para comparar; prometer "zero alucinação".

**Sinais de sênior:** propõe medir *recall* com e sem filtro por perfil; separa as perguntas que escolhem a variante das que medem o resultado; cita o custo de reindexar quando o modelo de embedding muda.

**Evidência no projeto (P02, 26/11/2026):** `57` documentos, `275` trechos, `151` perguntas, `pgvector` com HNSW e filtro SQL por perfil e vigência. Escolhendo em `74` perguntas e medindo em outras `74`, o *reranker* LLM teve acerto@4 de `63/74` (Wilson 95% [`0,75`; `0,91`]) e MRR `+0,16` a `+0,18` sobre as demais variantes, mas **sem diferença significativa** no acerto@4 contra as híbridas (McNemar `p = 0,125` e `0,22`). ACL: `0` vazamentos em `26` consultas restritas. Limite: o P02 não liga a varredura iterativa do `pgvector`. Com `275` trechos isso não pesa, mas em escala o filtro por perfil reduziria o *recall*.

---

## Caso 2 — Agente de matrícula com ferramentas e aprovação humana

**Enunciado:** "Queremos um agente que consulte prazos, calcule médias e, quando preciso, abra pedidos no sistema acadêmico."

**Perguntas:** quais ações escrevem dados ou custam dinheiro; quem aprova; quanto tempo uma aprovação pode esperar; o que acontece se o agente repetir uma ação; se há mais de um domínio de tarefa.

**Arquitetura de referência:**
- Ferramentas expostas por MCP (protocolo de contexto de modelo, padrão aberto para ligar ferramentas a modelos), com esquema validado e marcação de "só leitura". Ferramenta que escreve é sensível por padrão.
- Laço do agente como grafo de estado: verificar entrada → recuperar → agente → (aprovação) → ferramentas → consolidar → verificar saída.
- Pausa para humano com estado salvo em *checkpoint* e retomada pelo identificador da conversa; chave de idempotência nas ações que escrevem, para que repetir não duplique.
- Limite de passos e recusa segura quando ele estoura; ferramentas fora da lista do agente nunca rodam.
- Supervisor com subagentes só quando os domínios são claramente distintos, e cada subagente vê só as próprias ferramentas.

**Trade-offs:** framework (LangGraph) × laço próprio, em que o framework dá persistência, retomada e pausa humana, mas custa dependência e mais código. Supervisor × agente único: menos ferramentas à vista, ao custo de uma chamada a mais.

**Armadilhas:** dar ao modelo a decisão final sobre ações sensíveis; *checkpoint* com dado pessoal sem retenção definida; tratar ferramenta negada como sucesso.

**Sinais de sênior:** explica que o nó de aprovação roda de novo inteiro na retomada (por isso não pode ter efeito colateral antes da pausa); define retenção e exclusão do *checkpoint*.

**Evidência no projeto (P08 × P06, 25/11/2026, 27B):** `8/8` critérios nas quatro variantes; o P08 pausa **antes** de chamar a ferramenta sensível (`4` chamadas MCP contra `5` do P06). O supervisor custou `+1,4 s` no p50 e roteou igual nos dois modelos. No caminho bloqueado, sem chamar o modelo, o grafo custou de `2` a `3 ms` (com gravação do *checkpoint*). Limite: `8` cenários servem para leitura qualitativa, não para estatística.

---

## Caso 3 — Gateway de modelos para três áreas

**Enunciado:** "Atendimento, secretaria e pesquisa querem usar LLMs. Cada área quer um fornecedor. Como organizar?"

**Perguntas:** volume e orçamento por área; que dado cada área envia (pessoal ou público); exigência de residência no Brasil; tolerância a indisponibilidade; contratos já existentes (Azure, AWS ou Google).

**Arquitetura de referência:**
- Um gateway com API compatível com OpenAI na frente de modelos locais e de nuvem; chaves por área, cota por minuto e teto de gasto por mês.
- Roteamento por política, decidido no código: dado pessoal vai ao modelo local; pergunta complexa com orçamento vai à fronteira; sem fronteira disponível, cai no local com motivo registrado.
- Contingência entre provedores com o mesmo contrato de saída (`json_schema`) e teste de compatibilidade de cada rota.
- Cache de prefixo e de respostas onde a política permitir; custo e latência por rota no painel.

**Trade-offs:** gateway próprio × serviço gerenciado (controle e neutralidade contra operação); um provedor (desconto e simplicidade) × vários (resiliência e poder de negociação, com custo de testes por rota).

**Armadilhas:** contingência que troca de provedor e manda dado pessoal para fora; rota sem teste de formato; preço fixo no código.

**Sinais de sênior:** trata identidade gerenciada e renovação de token como requisito, não como detalhe; mede quanto custa cada ponto de qualidade.

**Evidência no projeto (P06):** roteamento local/fronteira/contingência com motivo; fronteira opcional em `openai`, `anthropic` e `gemini` e, desde o Cap. 20, em `azure`, `bedrock` e `vertex`, estes com `13` testes offline de formato (sem chave). Limite declarado: tokens do Entra ID e do OAuth do Vertex não são renovados.

---

## Caso 4 — Extração estruturada de documentos de inscrição

**Enunciado:** "Recebemos 5 mil PDFs de inscrição por semestre, alguns escaneados. Queremos os campos num sistema."

**Perguntas:** quais campos, quais são obrigatórios e qual o custo de um erro em cada um; proporção de escaneados; prazo (lote ou tempo real); quem corrige os casos duvidosos.

**Arquitetura de referência:**
- Texto quando houver camada de texto; imagem da página para um modelo com visão (VLM) quando não houver.
- Saída por `json_schema` estrito, validada por Pydantic, com reparo automático limitado e fila humana quando a validação falha.
- Regras determinísticas depois do modelo: CPF com dígito verificador, somas, datas e listas fechadas.
- Avaliação por campo (exatidão e cobertura), não por documento inteiro.

**Trade-offs:** VLM em toda página × só nas escaneadas (custo contra simplicidade); lote assíncrono (mais barato) × tempo real.

**Armadilhas:** confiar no formato válido como prova de conteúdo certo; não guardar a página de origem de cada campo.

**Sinais de sênior:** define o limiar de confiança por campo pelo custo do erro e mede quanto vai para a fila humana.

**Evidência no projeto:** P06 com `json_schema` estrito, `0` reparos nas execuções reais e degradação segura sem HTTP `500`; P07 com `pdftoppm`, payload multimodal, Pydantic e auditoria aritmética determinística dos totais. Limite: a chamada real ao VLM foi arquivada, então só o caminho offline está testado.

---

## Caso 5 — Lançar uma versão nova sem susto

**Enunciado:** "Mudamos o prompt e o modelo do assistente. Como saber se a v5 é melhor antes de liberar para todos?"

**Perguntas:** o que é "melhor" para o negócio; quantos casos reais com resposta conhecida existem; quanto tempo há; o que acontece se a v5 piorar uma fatia (ex.: alunos com deficiência, perguntas financeiras).

**Arquitetura de referência:**
- Conjunto de avaliação versionado, com fatias e casos de recusa.
- Juiz LLM calibrado contra rótulos humanos (*kappa* de Cohen, que mede concordância além do acaso), com ordem A/B invertida para neutralizar viés de posição. Juiz diferente do gerador.
- Decisão estatística: comparação pareada e intervalo por *bootstrap* (reamostragem); bloqueio quando alguma fatia cai além da tolerância.
- Liberação em canário com métricas online e *rollback* pronto.

**Trade-offs:** juiz LLM (barato e escalável) × humano (caro, mas necessário para calibrar); avaliação offline × teste A/B online.

**Armadilhas:** juiz igual ao gerador; escolher a variante e medir nas mesmas perguntas; reportar média sem intervalo.

**Sinais de sênior:** sabe que um *kappa* alto contra rótulos fáceis não prova calibração em casos difíceis.

**Evidência no projeto (P07, 26/11/2026):** `150` casos e `40` pares de calibração; *kappa* `0,955` [`0,86`; `1,0`] (`0,871` nos `12` pares pré-rotulados); placar `B = 137`, `empate = 9`, `A = 4` e diferença `+0,98` [`0,84`; `1,11`]. Limite: os rótulos humanos independentes estão pendentes, e casos e juiz vêm do mesmo modelo.

---

## Caso 6 — Servir localmente ou contratar API gerenciada

**Enunciado:** "Temos 30 tutores usando o assistente ao mesmo tempo. Compramos uma GPU ou usamos API?"

**Perguntas:** concorrência real no pico; TTFT (tempo até o primeiro token) aceitável; dado pode sair da empresa; volume mensal de tokens; equipe para operar GPU.

**Arquitetura de referência:** servidor de inferência com *batching* contínuo, limite de concorrência e fila; modelo menor para a maioria das perguntas e maior só onde a avaliação provar ganho; teste de carga com SLO antes de comprar.

**Conta que decide:** custo mensal da API (tokens × preço vigente) contra hardware amortizado + energia + horas de operação. Com dado sensível, a residência pode decidir antes do custo.

**Trade-offs:** local (controle, dado em casa, custo fixo) × API (elasticidade, modelos de ponta, custo variável); modelo grande × pequeno sob concorrência.

**Armadilhas:** medir com uma requisição e extrapolar para 30; ignorar a memória que o cache KV consome por conversa.

**Sinais de sênior:** pede o teste de carga com a distribuição real de tamanhos de prompt.

**Evidência no projeto (P01, 25/11/2026, RX 9070 XT, Ollama):** com concorrência `4`, o 4B ficou `100%` dentro do SLO (TTFT p95 `1.030 ms`, `185` tok/s); o 27B caiu para `25%` (TTFT p95 `4.706 ms`, `40` tok/s, `10,0 GiB` de VRAM). Limite: `8` requisições por medida, numa GPU compartilhada com o desktop.

---

## Caso 7 — Ajustar, recuperar ou só instruir

**Enunciado:** "O assistente classifica mal os chamados da secretaria. Vale fazer fine-tuning?"

**Perguntas:** o erro é de conhecimento (falta informação) ou de comportamento (formato, tom, critério); quantos exemplos rotulados existem; com que frequência as categorias mudam; quem mantém o modelo ajustado.

**Caminho de referência:** primeiro, prompt com exemplos e saída estruturada; se o erro for de conhecimento, RAG; fine-tuning (LoRA ou QLoRA, que treinam poucos parâmetros extras) só para comportamento estável, com divisão por grupo, épocas escolhidas na validação e teste usado uma vez.

**Trade-offs:** custo de treino e manutenção contra custo por chamada (modelo menor ajustado pode substituir um grande); risco de esquecer o que o modelo sabia.

**Armadilhas:** escolher hiperparâmetros olhando o teste; aprovar por média quando uma fatia piorou.

**Sinais de sênior:** pede portão estatístico com comparação pareada por caso e regressão máxima por fatia.

**Evidência no projeto (P04):** com `12` exemplos de teste, `12` épocas pareciam aprovar (`8/12 → 11/12`), mas o resultado foi reclassificado como **inconclusivo** (faixas de Wilson sobrepostas e épocas escolhidas no teste). Com `360` chamados divididos por grupo, a validação escolheu `6` épocas e o teste foi de `0,610` a `0,976`, com `45` ganhos e `0` perdas (McNemar `p < 10⁻⁶`), sem queda em fatia. Limite: dados sintéticos, sem revisão humana.

---

## Caso 8 — Tutoria com sessões longas

**Enunciado:** "Alunos conversam com o tutor por semanas. Ele esquece o que foi combinado e o custo sobe a cada mensagem."

**Perguntas:** o que precisa ser lembrado (preferências, progresso) e por quanto tempo; o que não pode ser guardado; tamanho típico de sessão; custo por aluno aceitável.

**Arquitetura de referência:** histórico curto na janela, resumo progressivo e memória de longo prazo estruturada (fatos com origem e data), recuperada por relevância; prefixo estável (instruções e ferramentas) para aproveitar o cache de prefixo do provedor; exclusão sob pedido do aluno.

**Trade-offs:** janela longa (simples, cara e com queda de atenção no meio) × resumo e recuperação (barato, mas pode perder detalhe).

**Armadilhas:** guardar tudo para sempre; resumo que reescreve fatos; quebrar o cache mudando o início do prompt a cada turno.

**Sinais de sênior:** mede a taxa de acerto do cache e o custo por sessão; trata a memória como dado pessoal sujeito à LGPD.

**Evidência no projeto (P06, Fase 6):** histórico limitado com `deque(maxlen=...)`; `13.555` de `16.641` tokens de entrada vieram do cache de prefixo.

---

## Caso 9 — Dados de alunos com provedor externo

**Enunciado:** "O assistente usa um modelo de nuvem e responde sobre notas e financeiro. O jurídico está preocupado."

**Perguntas:** quais dados pessoais passam; base legal; contrato com o provedor (retenção, uso para treino, região); quem pode ver o quê; o que já foi atacado.

**Arquitetura de referência:**
- Mascarar PII antes de qualquer envio externo; rota local para pergunta com dado pessoal.
- Autenticação e vínculo chave → perfil máximo no servidor, com HTTP `403` em tentativa de elevação.
- Guardrails de entrada (injeção, caracteres invisíveis) e de saída (PII que escapou, citação válida, caracteres de controle).
- Red teaming antes de liberar e a cada mudança grande; logs sem texto de prompt nem PII.

**Trade-offs:** bloquear demais (falsos positivos irritam) × bloquear de menos; provedor com rede privada e região definida (mais caro) × endpoint público.

**Armadilhas:** confiar em lista fixa de padrões contra ataque adaptativo; mandar PII para o trace.

**Sinais de sênior:** lembra que "zero falhas" numa amostra pequena tem limite superior alto e pede mais tentativas nas sondas que importam.

**Evidência no projeto (P06):** anti-BFLA real em `4/4` verificações (`401`, `403`, `200` sem vazamento e `200` com acesso autorizado). garak `0.17.1` com `14` sondas e `342` tentativas: `3` achados corrigidos com teste (`500` → `503` com `Retry-After`, *tags* Unicode bloqueadas, controles ANSI removidos). Com `0` falhas em `20` tentativas, o limite superior de Wilson 95% ainda é de `16%`.

---

## Caso 10 — A qualidade caiu e ninguém sabe por quê

**Enunciado:** "Há duas semanas os alunos reclamam mais do assistente. Nada mudou no código."

**Perguntas:** o que mudou fora do código (versão do modelo no provedor, documentos, perfil das perguntas, época do semestre); que sinais existem (avaliação do usuário, recusas, latência); se há traces por pergunta.

**Diagnóstico de referência:**
1. Separar busca de geração: o *recall* caiu ou a resposta piorou com o mesmo contexto?
2. Comparar a distribuição das perguntas atuais com a do conjunto de avaliação (*drift*, ou mudança dos dados ao longo do tempo).
3. Conferir a versão efetiva do modelo e dos parâmetros nos traces.
4. Rodar de novo o conjunto de avaliação fixo contra a versão atual.
5. Corrigir, adicionar os casos novos ao conjunto e criar um alerta para o sinal que faltou.

**Arquitetura de referência:** traces com atributos `gen_ai.*` (modelo, tokens, latência, rota) sem texto nem PII; métricas Prometheus; feedback do usuário ligado ao trace; avaliação contínua numa amostra.

**Trade-offs:** guardar texto (diagnóstico fácil) × não guardar (privacidade); amostrar (barato) × rastrear tudo.

**Armadilhas:** procurar o bug no código antes de olhar os dados; métrica média que esconde a fatia que piorou.

**Sinais de sênior:** fixa versão de modelo e prompt e trata a mudança deles como deploy.

**Evidência no projeto:** P05 com `/metrics` e spans no Jaeger; P05 e P06 enviando traces ao Langfuse auto-hospedado (`5/5` observações com tokens de entrada, saída e cache, sem texto nem PII).

claude - pessoal, 26/11/2026; atualizado em 26/11/2026 por agy - ap (Gemini 4 Hydrogen High).
