# Entrevista: comunicar limites, especificar e diagnosticar

Três roteiros para as perguntas que mais aparecem fora do system design. Comunicação com o negócio aparece em `69%` das `55` vagas do [mapa reconferido](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md#reconferência-em-26112026-55-vagas). Os exemplos vêm dos projetos; cite os números só como estão nos registros de `laboratorios-mercado/execucoes/`.

Use o formato situação → ação → resultado → aprendizado, em até 2 minutos por resposta.

## 1. Explicar limites da IA a quem não é técnico

**Roteiro de quatro frases:**
1. **O que faz:** a tarefa em linguagem do usuário, com a taxa medida.
2. **O que não faz:** onde erra e por quê, sem jargão.
3. **Como saberemos:** a métrica que acompanha e quem olha.
4. **O que acontece quando errar:** a rede de proteção (fila humana, recusa, rollback).

**Exemplo (P02, RAG):** "Com perguntas naturais sem cabeçalho de tema, o assistente achou o trecho certo entre os quatro primeiros em `45` de `74` perguntas de teste, cerca de `61%` (antes, quando a pergunta repetia o tema do documento, passava para `63` de `74`, `85%`). Ele erra mais quando a pergunta usa sinônimos ou não cita o serviço exato. Toda resposta mostra o trecho de origem, e, quando não acha nada relevante, ele diz que não sabe em vez de inventar. Vamos acompanhar as perguntas sem resposta toda semana."

**Exemplo (amostra pequena engana):** "Com `28` perguntas, a busca vetorial achou o trecho certo em todas. Com `151` perguntas naturais, a busca vetorial achou em metade (`0,50`) e a busca só por palavra-chave caiu para `0,40`. Por isso não prometo número antes de testar com perguntas reais de vocês."

**Exemplo ("zero falhas" não é garantia):** "No teste de ataque, nenhuma das `20` tentativas de uma sonda funcionou. Isso não quer dizer risco zero: com essa amostra, a taxa real ainda pode chegar a `16%`. Para afirmar mais, precisamos de mais tentativas."

**Exemplo (mesma pergunta, respostas diferentes):** "O modelo sorteia palavras. Mesmo com a configuração mais estável, a forma muda um pouco. Por isso medimos o comportamento em muitas perguntas, e não numa só, e travamos o formato da saída com um esquema."

**Perguntas de treino:**
- "Por que não dá para garantir que a IA nunca erre?"
- "O concorrente diz que o produto dele tem 99% de acerto. E o nosso?" (pergunte: medido em quê, com quantos casos, com que intervalo)
- "Podemos usar a IA para decidir bolsas sozinha?" (resposta: decisão com impacto sobre pessoas fica com humano; a IA prepara e justifica, base no Cap. 12)

**Armadilhas:** prometer porcentagem sem amostra; esconder o erro em média; usar "alucinação" sem explicar.

## 2. Traduzir pedido vago em especificação

**Perguntas que transformam o pedido (Cap. 3):** quem usa e em que momento; qual decisão ou tarefa muda; entrada e saída exatas; como medir sucesso e qual o mínimo aceitável; o que fica fora; que dado pode ser usado; quanto pode custar por mês; o que acontece quando a IA erra.

**Modelo de especificação de uma página:**

| Campo | Conteúdo |
|---|---|
| Problema | uma frase, com o custo atual (tempo, dinheiro, reclamações) |
| Usuário e momento | quem, onde, com que frequência |
| Entrada → saída | formato exato (de preferência um esquema JSON) |
| Aceite | métrica, limiar, tamanho da amostra e fatias que não podem piorar |
| Fora do escopo | o que a primeira versão não faz |
| Dados e privacidade | origem, base legal, retenção e quem pode ver |
| Riscos e rede de proteção | erro mais caro e o que o contém |
| Custo e prazo | teto mensal e marcos |

**Exemplo 1 — "Quero uma IA que ajude a secretaria com os chamados" (P04):**
- Problema: chamados chegam sem categoria e esperam triagem manual.
- Entrada → saída: texto do chamado → `{"categoria": "<categoria>"}`, com quatro categorias fixas (financeiro, acadêmico, acesso e secretaria) e formato conferido.
- Aceite: acurácia no teste com intervalo de Wilson acima da linha de base, comparação pareada caso a caso (McNemar) e nenhuma fatia (formal, informal, com ruído) caindo mais de `0,05`.
- Resultado medido: `0,610 → 0,976` em `123` chamados de teste, `45` ganhos e `0` perdas, portão aprovado sem intervenção. Limite: dados sintéticos.

**Exemplo 2 — "O assistente tem que ser seguro" (P06):**
- Tradução em requisitos verificáveis: sem chave, `401`; aluno pedindo perfil de admin, `403`; nenhum trecho restrito na resposta de quem não tem acesso; injeção e caracteres invisíveis bloqueados na entrada; PII mascarada na saída; falha do modelo vira `503`, nunca `500` com detalhe interno.
- Como provar: testes de regressão para cada item e red teaming com garak (`14` sondas, `342` tentativas, `3` achados corrigidos).

**Perguntas de treino:**
- "Queremos um chatbot para o site." (descubra a tarefa real antes do canal)
- "Faça a IA ler os contratos e achar os problemas." (defina "problema" com o jurídico e monte `20` exemplos rotulados antes de qualquer código)

**Armadilhas:** aceitar "melhorar a experiência" como critério; começar pela escolha do modelo; esquecer o caso de erro.

## 3. Diagnosticar falhas não determinísticas

**Método:**
1. **Registrar e reproduzir:** prompt exato, modelo e versão, parâmetros (temperatura, `max_tokens`, modo de raciocínio), contexto recuperado e ferramentas chamadas. Sem trace, primeiro instrumente.
2. **Isolar a camada:** entrada → recuperação → modelo → ferramenta → saída → infraestrutura. Troque uma de cada vez por uma versão fixa.
3. **Medir a taxa, não o caso:** repita `N` vezes e reporte a proporção com intervalo; compare antes e depois nos mesmos casos (teste pareado).
4. **Corrigir com teste de regressão** e adicionar o caso ao conjunto de avaliação.

**Casos reais dos projetos:**

| Sintoma | Causa encontrada | Correção | Onde |
|---|---|---|---|
| Ollama devolvia `500` em parte das chamadas e o lote do garak travava | instrução escondida em caracteres Unicode de *tags* chegava ao agente com ferramentas; o P06 repassava `500` e o cliente insistia | bloqueio de *tags* na entrada (com NFKC e remoção de invisíveis) e `503` com `Retry-After` em falha do modelo | P06, [relatório de red teaming](../../laboratorios-mercado/06_integrador_producao/redteam/relatorio-red-teaming-p06-2026-11-26.md) |
| O 27B falhava com `json_schema` e `max_tokens = 256` | o modo de raciocínio gastava os tokens antes do conteúdo | `reasoning_effort = "none"` nas chamadas | [README da camada 3](../../laboratorios-mercado/README.md) |
| Fine-tuning "aprovado" com `12` épocas | épocas escolhidas olhando o teste, com `12` casos (faixas de Wilson sobrepostas) | validação separada, divisão por grupo e `360` exemplos | P04 |
| Juiz LLM mudava o veredito ao trocar a ordem de A e B | viés de posição | julgar nas duas ordens; divergência vira empate (`7` casos no P07) | P07 |
| p95 do mesmo cenário variou de `22 s` a `35 s` | cache de prefixo aquecido pelas variantes anteriores e amostra de `7` | não comparar latência entre variantes rodadas em ordem fixa; sortear a ordem ou aquecer igual | P08 |
| garak acusou `16` falhas de DAN | o detector só reconhece recusas em inglês; as respostas eram recusas em português | leitura manual das saídas antes de contar falha | P06 |

**Pergunta de treino:** "Em produção, 3% das respostas saem com JSON inválido, mas você não consegue reproduzir. O que faz?"
**Resposta esperada:** registrar entrada, parâmetros e saída crua das falhas; ver se há padrão (tamanho do contexto, ferramenta chamada, provedor de contingência); reproduzir em lote com as entradas registradas e medir a taxa; usar saída estruturada estrita, validação com reparo limitado e degradação segura (resposta neutra, sem `500`); criar alerta para a taxa.

**Armadilhas:** "rodei de novo e funcionou"; mudar várias coisas de uma vez; culpar o modelo antes de olhar a recuperação.

claude - pessoal, 26/11/2026; atualizado em 26/11/2026 por agy - ap (Gemini 4 Hydrogen High).
