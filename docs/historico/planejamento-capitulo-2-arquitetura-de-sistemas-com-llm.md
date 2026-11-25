# Planejamento do Capítulo 2 — Arquitetura de sistemas com LLM

Data: 15/10/2026. Autoria: claude - pessoal (Opus 5.5, effort High declarado pelo operador). Etapa: **somente planejamento**; nada redigido no guia, nenhuma fonte baixada.

Base: [plano mestre](planejamento-completo-estudos-engenharia-llms.md), [plano do Capítulo 1](planejamento-capitulo-1-fundamentos-de-ia-e-llms.md), [requisitos de formato](../../requisitos-de-formato-html-do-material.md), [reestruturação](planejamento-reestruturacao-sem-programacao.md), contextos do [Router](../../contexto-de-estudo-ap-ai-router.md) e da [Nanda Mac](../../contexto-de-estudo-nanda-mac.md). Herda do Capítulo 1 o formato de unidade (sete itens mais "Fontes da unidade"), as questões, os qualificadores, a regra de linguagem sobre o modelo e os limites. O plano do Capítulo 2 antigo (arquivado) serve só de modelo de método.

## 1. Objetivo, escopo e aceite

**Objetivo:** ao concluir o capítulo, o estudante descreve a arquitetura de um sistema com LLM, local ou de fronteira, e segue o caminho de um pedido; explica o que a chamada ao modelo recebe e devolve, por que ela é lenta, limitada, sem estado e sujeita a falha; e decide controles (tempo limite, nova tentativa, persistência, fila) sem escrever código.

**Escopo:** abertura, seis unidades, cinco questões, termos do glossário e referências. Progressão (substitui a linha provisória do plano mestre, após aprovação): componentes e fronteiras → a chamada ao modelo → streaming e latência → limites, erros e novas tentativas → estado e persistência → simultaneidade e capacidade.

**Fora do escopo:** programação em qualquer forma; laboratórios; execução nos projetos-fonte. Só menção, com ponte: conteúdo do pedido, parâmetros e schemas (4); segurança e fronteira de confiança (6); o que entra no contexto e histórico (8); ferramentas (9); ciclo de agente (11); servidor local por dentro, quantização, KV cache, lotes (12); troca de provedor (13); observabilidade e lançamento (14); custo e cache (15).

**Aceite:**
- cada unidade com objetivo, termos definidos, funcionamento (diagrama quando ajudar), exemplo resolvido, limites, pergunta com feedback, ponto de retomada e fontes;
- nenhum trecho de programa; textos de configuração ou de resposta só para ler, rotulados *ilustrativo, não executado*;
- toda afirmação técnica rastreia fonte datada ou é *proposta didática*; nenhum limite numérico de provedor sem data e fonte;
- pelo menos dois provedores de fronteira e um servidor local nas fontes, para o conhecimento ser transferível;
- unidades na faixa do Capítulo 1 (cerca de 1.200 a 1.350 palavras), sem repetir a 1.1 e a 1.3;
- `validar-guia.py` com 0 falha; Chrome em 320 a 1920 px sem rolagem horizontal; axe sem violações; mecânica das questões OK.

## 2. Decisões de desenho

1. **Nível:** quem leu o Capítulo 1. Sem pré-requisito de programação; HTTP, JSON e servidor são explicados como conceitos no ponto em que aparecem.
2. **Eixo:** o modelo é uma peça externa, lenta, limitada e falível; a arquitetura decide o que acontece em volta dela. Liga com 1.1 ("sistema ao redor") e 1.6 (o que fica no código determinístico).
3. **Diagramas:** reusar os componentes existentes (`ol.fluxo` da 1.1 e tabelas). Sem componente novo, sem SVG. Se um diagrama não couber nesses dois, propor na pausa do Bloco 2.
4. **Textos para ler:** pedido e resposta de API, cabeçalho de erro e arquivo de parâmetros, com até cerca de 12 linhas, valores fictícios, em `figure.bloco-codigo` com `data-executavel="false"`. Uso só quando o texto mostra algo que a prosa não mostra (por exemplo, o motivo de parada ou o `retry-after`).
5. **Neutralidade de provedor:** conceitos primeiro; nomes de campo e códigos de um provedor só como exemplo, com data, e ao lado do equivalente de outro quando existir.
6. **Exemplos:** Router no nível de arquitetura (camadas, adaptador, despacho, fila, trava da GPU, persistência), sem mostrar código; Nanda Mac com processos fictícios, sem pessoas, dados de clientes, nome de fornecedor ("gateway de pagamento") nem ferramentas internas de análise. Assistentes por login com modelo local compartilhado: *proposta didática* (decisão aberta no contexto, §8).
7. **Qualificadores** do Capítulo 1 mantidos.
8. **Links externos** em nova guia (`target="_blank" rel="noopener noreferrer"`).
9. **Ids livres e reaproveitados:** `capitulo-2`, `unidade-2-1` a `unidade-2-6`, `questoes-capitulo-2`, `c2q1` a `c2q5`. O arquivo antigo está fora do guia.

## 3. Fontes (nenhuma lida nesta sessão; conferir e extrair no Bloco 1)

| Fonte | Papel | Estado |
|---|---|---|
| Anthropic — *Messages*, *Streaming messages*, *Rate limits*, *Errors* | Pedido e resposta, ausência de estado, eventos de streaming, limites e cabeçalhos, códigos de erro | A ler; *API errors* teve trechos conferidos em 15/10 no pacote arquivado (reconferir) |
| OpenAI — guia de *Rate limits* e *Error codes* | Segundo provedor; espera crescente recomendada | A ler |
| Ollama — documentação da API (`/api/generate`, `/api/chat`, streaming, compatibilidade OpenAI) | Servidor local; é o que o Router usa | A ler |
| llama.cpp — README do servidor HTTP | Servidor local compatível; atendimento de pedidos simultâneos | A ler |
| ~~vLLM — servidor compatível com OpenAI~~ | Retirada no Bloco 1: página não extraiu | Fora do capítulo |
| IETF RFC 9110 (§9.2.2 idempotência, §10.2.3 `Retry-After`, classes 4xx e 5xx) e RFC 6585 (§4, 429) | Norma de HTTP | RFC 9110 conferida em parte em 15/10 (pacote arquivado); RFC 6585 a ler |
| MDN — *Overview of HTTP* e *Using server-sent events* | Cliente e servidor, sem estado; SSE | *Overview* conferido em 15/10 (arquivo); SSE a ler |
| AWS Builders' Library — *Timeouts, retries, and backoff with jitter* | Tempo limite, nova tentativa, variação aleatória, amplificação | A ler |
| Google SRE Book, cap. 21 *Handling Overload* e cap. 22 *Addressing Cascading Failures* (gratuito) | Sobrecarga, fila, recusa controlada, tentativas em cascata | A ler |
| `docs/09` do Router (interna) | Antipadrões (filas sem necessidade, LLM para lógica simples) | Lido em 15/10; mesma pendência de publicação |

**Evidência local (leitura, lista fechada, sem execução):** Router — camadas do contexto (§4), adaptador `dispatch-agent.ps1`, chat local por `/api/generate`, `request_id` com *fingerprint* (409 para pedido diferente, resultado salvo para pedido repetido), trava da GPU e travas por conversa, fila com tempo limite, SQLite em WAL; clientes por login e plano diferentes de API cobrada por uso (§8 do contexto). Nanda Mac — IA de leads com três famílias de provedor e resposta estruturada; assistente do banco de contratos com tempo limite e teto de resultados; webhook do gateway que ignora evento já processado. Conferir cada um de novo antes de citar; nunca ler `panel.db`, `history.jsonl`, `*.log`, credenciais ou bancos.

## 4. Mapa por unidade

### 2.1 Componentes e fronteiras
- **Competência:** nomear as peças de um sistema com LLM (interface, serviço de aplicação, montagem de contexto, chamada ao modelo, validação, persistência) e dizer o que cada uma decide; distinguir três formas de acesso ao modelo: API de provedor, servidor local e cliente por assinatura.
- **Conceitos:** componente, fronteira, serviço, cliente e servidor, provedor, servidor local, adaptador.
- **Exemplo resolvido:** caminho de um pedido no Router (camadas do contexto, §4), em `ol.fluxo`, ampliando o fluxo da 1.1.
- **Equívocos:** "o modelo é o sistema"; "local e fronteira exigem arquiteturas diferentes"; "trocar de provedor é trocar uma linha".
- **Critério:** "No assistente de cobrança fictício, que peça decide o valor devido e qual redige a mensagem?"
- **Ponte:** 3, 6 e 9.

### 2.2 A chamada ao modelo
- **Competência:** descrever pedido e resposta (modelo, mensagens, limite de saída; texto, motivo de parada, uso de tokens, identificador); explicar que a API não guarda a conversa e que o histórico é reenviado (liga com 1.3); reconhecer que servidores locais costumam imitar o formato de um provedor.
- **Conceitos:** requisição, resposta, código de status, JSON (como formato de leitura), motivo de parada, uso reportado, identificador de requisição, API sem estado, compatibilidade de formato.
- **Texto para ler:** um pedido e uma resposta mínimos, fictícios, com motivo de parada por limite de saída (liga com 1.4).
- **Equívocos:** "o modelo lembra da conversa"; "resposta com status de sucesso está completa"; "formato compatível garante comportamento igual".
- **Ponte:** 4 (parâmetros e schemas) e 8 (histórico).

### 2.3 Streaming e latência
- **Competência:** separar tempo até o primeiro token e tempo total; explicar streaming como entrega em partes enquanto a geração ocorre (liga com 1.4); saber o custo para a validação (não dá para validar o todo antes de mostrar) e o que fazer quando a transmissão cai no meio.
- **Conceitos:** latência, tempo até o primeiro token, streaming, eventos enviados pelo servidor (SSE), interrupção, processamento da entrada e geração (só menção; 12 e 15).
- **Exemplo resolvido:** resposta longa do assistente com streaming contra resposta curta validada antes de mostrar (*proposta didática*).
- **Equívocos:** "streaming deixa o modelo mais rápido"; "o que já apareceu na tela foi validado"; "transmissão interrompida é resposta completa".

### 2.4 Limites, erros e novas tentativas
- **Competência:** ler limites de taxa (pedidos e tokens por período) e erros por classe (pedido inválido, limite, sobrecarga, falha do servidor); decidir quando repetir, com espera crescente e variação aleatória, respeitando `Retry-After`; saber que tempo limite não prova que a ação não ocorreu e que repetir só é seguro com operação idempotente ou identificador de pedido.
- **Conceitos:** limite de taxa, 429, 5xx, sobrecarga, tempo limite, nova tentativa, espera crescente, variação aleatória (*jitter*), idempotência, chave de idempotência, amplificação de tentativas.
- **Texto para ler:** resposta de erro 429 com cabeçalho de espera (fictício, no formato documentado).
- **Exemplos:** Router devolve o resultado salvo a um pedido repetido e recusa o mesmo identificador com conteúdo diferente (*verificado no código local*); webhook do gateway ignora evento já processado (*verificado*).
- **Equívocos:** "toda falha merece nova tentativa imediata"; "429 e 500 são o mesmo problema"; "tempo limite = nada aconteceu".
- **Ponte:** 13 (contingência entre provedores) e 14.

### 2.5 Estado e persistência
- **Competência:** dizer onde o estado mora (a aplicação, não o modelo); escolher o que persistir e por quê (retomada, auditoria, custo, reprodução de uma resposta); separar estado da conversa, estado do pedido e resultado.
- **Conceitos:** estado, persistência, banco de dados (conceito, sem SQL), registro de pedido, retomada, retenção.
- **Exemplo resolvido:** Router guarda conversas, mensagens e pedidos de despacho em banco local (*verificado*); por que reiniciar o serviço não pode perder um pedido em andamento.
- **Equívocos:** "o histórico do chat é memória do modelo"; "guardar tudo é sempre seguro"; "recursos de estado do provedor dispensam persistência própria".
- **Ponte:** 6 (privacidade e retenção), 8 (o que volta ao contexto), 11 (estado do agente).

### 2.6 Simultaneidade e capacidade
- **Competência:** explicar o que acontece quando muitos pedidos chegam juntos: limite de taxa na fronteira, capacidade fixa no local; decidir entre fila, limite de simultaneidade e recusa controlada; reconhecer que mais tentativas sob sobrecarga pioram a sobrecarga.
- **Conceitos:** simultaneidade, capacidade, fila, limite de simultaneidade, recusa controlada, sobrecarga, condição de corrida (conceito), lotes no servidor local (só menção; 12).
- **Exemplos:** Router serializa a inferência local com uma trava e ordena pedidos por conversa (*verificado*). Dez colaboradores e um modelo local compartilhado (*proposta didática*).
- **Equívocos:** "mais pedidos simultâneos é sempre mais rápido"; "fila resolve qualquer pico"; "fila distribuída desde o início" (antipadrão, `docs/09`).

## 5. Matriz das cinco questões (4 alternativas, 1 correta, primeira resposta trava)

| # | Nível | Unidades | Situação e foco | Distratores |
|---|---|---|---|---|
| Q1 | Fácil | 2.1 | Assistente de cobrança fictício: qual peça decide o valor, qual redige, qual guarda | o modelo calcula; a interface valida |
| Q2 | Fácil | 2.2, 2.5 | Assistente "esqueceu" a conversa após trocar de servidor | o modelo perdeu memória; precisa treinar o modelo |
| Q3 | Média | 2.2, 2.3 | Texto de resposta com motivo de parada por limite de saída e resposta cortada na tela | status de sucesso basta; streaming causou o corte |
| Q4 | Média | 2.4, 2.6 | Pico de pedidos, 429 com `Retry-After` e tentativas imediatas em laço | repetir na hora; aumentar a simultaneidade |
| Q5 | Difícil | 2.1, 2.4–2.6 | Pedido de registro de rascunho duplicado após tempo limite, com modelo local compartilhado: escolher o desenho (identificador de pedido, estado persistido, fila) e achar a premissa falha | tempo limite = nada ocorreu; trava resolve entre processos |

Cobertura: todas as unidades; Q3 a Q5 com texto ou caso para analisar. Gabarito definido na redação, sem padrão regular e diferente do Capítulo 1 (B, D, A, C, B).

## 6. Produção: blocos, modelos e efforts

Só as três combinações do projeto. Preflight em cada bloco; divergência `atual → recomendado` e pausa.

| Bloco | Modelo / effort | Conteúdo | Gate |
|---|---|---|---|
| 0 | — (operador) | Aprovar este plano e o nome do módulo. Depois, atualizar a linha 2 do plano mestre e os tópicos do sumário do guia; validar. | Aprovação |
| 1 | Sonnet 5.5 High | Baixar as fontes da §3 para pasta temporária vazia (`curl -L`), extrair com `extrair-texto-web.py`; copiar só a lista fechada de arquivos locais; montar `pacotes-de-fontes-capitulo-2.md` (trechos literais com seção e data); `conferir-trechos.py`. Reaproveitar do pacote arquivado só o que for reconferido. Não editar o guia. | Pacote aprovado pelo script |
| 2 | Sonnet 5.5 High | Abertura e 2.1. **Pausa: operador aprova nível, diagrama e texto para ler.** Depois 2.2 a 2.6, questões, glossário (reescrever sem "Em Python" os termos arquivados que voltarem), referências; páginas 11 a 18, glossário 19, referências 20; navegação da página 10 volta para `#capitulo-2` e a do glossário para `#questoes-capitulo-2`; sumário com links das unidades. | Validador sem falha |
| 3 | Opus 5.5 High | Ler contra fontes e requisitos: afirmações de provedor, HTTP, streaming e tentativas; coerência com o Capítulo 1; sobreposição com 4, 8, 12 a 15. Correções pequenas; erro que exija reescrever volta ao Sonnet. | Sem achado material |
| 4 | Sonnet 5.5 High | Validador, Chrome (6 larguras, axe, questões), `changelog-capitulo-2.md`, handoff. Sem Git (pasta fora de repositório). | Resultados registrados |

O `executar-trechos-de-codigo.py` não entra (nenhum trecho executável). Tempo: não estimado; depende das pausas do operador.

## 7. Riscos e controles

| Risco | Controle |
|---|---|
| Documentação de provedor muda ou difere entre provedores | Data de consulta; conceito antes do campo; dois provedores e um local |
| Capítulo vira manual de um provedor | Decisão 5; Opus confere no Bloco 3 |
| Sobreposição com 4, 8, 12 a 15 | Pontes explícitas; aprofundamento fica no módulo dono |
| Escorregar para programação | Só textos para ler; questões sem programa; Opus confere |
| Repetir 1.1 e 1.3 | 2.1 e 2.2 partem do que já foi dito e avançam |
| Afirmar implementação a partir de proposta | Qualificadores; assistentes por login como proposta didática |
| Números de limite citados como fixos | Proibidos sem data e fonte; preferir a forma do limite ao valor |
| Unidades longas | Faixa do Capítulo 1; aparar na redação |

Segurança e LGPD: sem dados pessoais nem credenciais; sem gatilho para triagem. Proporcionalidade: nenhum componente novo, ferramenta nova ou fonte paga.

## 8. Decisões pedidas ao operador
1. Aprovar o plano (escopo, seis unidades, questões, blocos).
2. Nome do módulo: "Arquitetura de sistemas com LLM" (recomendado) ou outro.

Padrões adotados se não houver outra decisão: pausa após a 2.1; diagramas só com `ol.fluxo` e tabelas; textos para ler no máximo um por unidade.

## 9. Estado de continuidade (15/10/2026)
- **Bloco 0 concluído:** operador aprovou o plano e o nome "Arquitetura de sistemas com LLM". Linha 2 do plano mestre e tópicos do sumário do guia atualizados (Opus 5.5 High); validador sem falha.
- **Bloco 1 concluído (Sonnet 5.5 High, effort declarado pelo operador, 15/10/2026):** `pacotes-de-fontes-capitulo-2.md` com 109 trechos literais (2.1: 15; 2.2: 16; 2.3: 14; 2.4: 30; 2.5: 14; 2.6: 20), montados por âncoras e conferidos por `conferir-trechos.py`: 109 aprovados, 0 reprovados. Fontes lidas: Anthropic (5 páginas), OpenAI (4), Ollama (2), llama.cpp, RFC 9110 e 6585, MDN (2), AWS Builders' Library, Google SRE (2).
- **Desvios do plano:** (a) vLLM não extraiu (página vazia) e saiu do capítulo; (b) a página de perguntas frequentes do Ollama não extraiu, então o capítulo não afirma nada sobre paralelismo do Ollama e usa o llama.cpp para servidor local; (c) acrescentadas duas páginas da Anthropic (*Handling stop reasons*, *Working with messages*) e duas da OpenAI (*Conversation state*, *Streaming responses*); (d) o texto do trecho de código do Nanda Mac (webhook) usa só "evento já processado", sem nome de fornecedor; (e) "tempo até o primeiro token" não tem fonte que o defina: termo de trabalho do livro.
- As fontes extraídas e o script de montagem ficam na pasta temporária da sessão (`scratchpad\cap2n-textos`, `montar-pacote.py`) e podem sumir; para reconferir, baixar de novo as URLs da §3 e copiar só a lista fechada de arquivos locais (`main.py`, `database.py`, `queue_worker.py` do Router; `route.ts` do webhook; `docs/09`).
- **Bloco 2, etapa 1 concluída (Sonnet 5.5 High, 15/10/2026):** abertura do capítulo (página 11) e unidade 2.1 (página 12, 1.341 palavras com a mesma contagem que dá 1.230 e 1.296 às unidades 1.3 e 1.4) inseridas no guia. Sumário com link só para as páginas prontas; 7 termos novos no glossário e 3 fontes novas nas referências; glossário e referências provisoriamente nas páginas 13 e 14 (voltam a 19 e 20 quando o capítulo fechar). Validador 15 OK, 0 falha; tags equilibradas; Chrome em 320 e 1280 px sem rolagem horizontal, axe sem violações, questões do capítulo 1 OK.
- **Pausa do plano (§6, Bloco 2) resolvida:** o operador aprovou nível de entrada, diagrama (`ol.fluxo` de seis passos mais tabela) e o texto para ler da 2.2 ("Aprovo os 3 itens", 15/10/2026).
- **Bloco 2 concluído (Sonnet 5.5 High, effort declarado pelo operador, 15/10/2026):**
  - **Unidades 2.2 a 2.6 e cinco questões no guia.** Páginas: abertura 11; unidades 12 a 17; questões 18; glossário 19 (82 termos); referências 20. Sumário e abertura com link para todas as unidades e as questões; navegação encadeada.
  - **Palavras** (mesma contagem de 1.3 e 1.4): 2.1 1.336; 2.2 1.358; 2.3 1.248; 2.4 1.368; 2.5 1.354; 2.6 1.280 (Capítulo 1: 1.153 a 1.325). A 2.4 ficou 18 palavras acima do teto de 1.350.
  - **Textos para ler:** 2.2 (pedido e resposta, `max_tokens`, `figure.bloco-codigo` com `pre.codigo` e `pre.saida`) e 2.4 (resposta 429 com `retry-after`); ambos `data-executavel="false"`, valores fictícios.
  - **Questões** (gabarito C, A, D, B, A; Capítulo 1: B, D, A, C, B): Q1 fácil (2.1), Q2 fácil (2.2/2.5), Q3 média (2.2/2.3), Q4 média (2.4/2.6), Q5 difícil (2.1, 2.4 a 2.6).
  - **Pacote de fontes** ampliado de 109 para 123 trechos (campos do exemplo de resposta e do 429, classes 2xx/4xx/5xx, `Retry-After`, e quatro casos do Router sobre pedido repetido e reinício), todos aprovados por `conferir-trechos.py` (123 aprovados, 0 reprovados). As fontes extraídas continuam na pasta temporária da sessão.
  - **Validação:** `validar-guia.py` 16 OK, 0 falha; tags equilibradas; ids sem duplicata; Chrome (Playwright, `channel="chrome"`) sem rolagem horizontal em 320, 480, 768, 1024, 1280 e 1920 px, nenhum elemento fora de região de rolagem em 320 e 1280 px, axe 0 violações (1 incompleta `aria-prohibited-attr`, conhecida), 92 links internos sem alvo ausente, mecânica das questões OK nos dois capítulos (5 de 5 em cada).
  - **Cuidados de redação a conferir no Bloco 3:** afirmações atribuídas a provedores (tradução nossa), a Parte 2 da 2.5 (reinício do Router: rotinas lidas, nada executado), a Parte 1 da 2.6 (a trava vive na memória do serviço; a consequência é *proposta didática*), "balde de fichas" (token bucket) e a tabela de condutas da 2.4 (4xx/429/5xx).
- **Bloco 3 concluído (Opus 5.5 High; modelo confirmado pela sessão, effort não verificável, 15/10/2026):** capítulo lido contra as fontes extraídas, os requisitos de formato e o Capítulo 1. Nenhum erro que exija reescrever. Correções pequenas aplicadas:
  1. Abertura: explicadas as etiquetas novas *registrado na norma* e *registrado nas diretrizes locais*, usadas no capítulo e antes sem explicação.
  2. 2.2: "leva três coisas" → "costuma levar três coisas" (a obrigatoriedade do limite de saída varia por destino e não está nas fontes extraídas).
  3. 2.3: "recomenda" → "sugere considerar" (a fonte diz *consider*); o fim da transmissão passou a ser "motivo de parada e sinal de encerramento" (na Anthropic, o motivo vem num evento anterior ao de encerramento), em quatro pontos.
  4. 2.4: linha de status do texto para ler completa (`429 Too Many Requests`); linha "Tempo esgotado" da tabela separa gerar texto (repetir sem duplicar efeito) de registrar ou enviar (só com identificador).
  5. 2.6: "recomenda não prometer ausência de filas" → "trata ausência de filas como expectativa a verificar, e não como fato" (texto do contexto).
  - Pacote de fontes: +3 trechos (evento `message_delta` com motivo de parada, reabastecimento contínuo do limite, expectativas a verificar) → 126 aprovados, 0 reprovados.
  - Conferido sem mudança: travas do Router são por conversa (chave `conversation_id`); `dispatch_requests` guarda `response`, `status` e `fingerprint`; recusa por 503 e filas pequenas no SRE; afirmações de Anthropic, OpenAI, Ollama, llama.cpp, RFCs e AWS; pontes para 4, 8 e 12 a 15; coerência com 1.3, 1.4 e 1.6; gabarito e explicações das questões.
  - Revalidação: `validar-guia.py` 16 OK, 0 falha; Chrome nas 6 larguras sem rolagem horizontal, axe 0 violações, questões 5 de 5 nos dois capítulos, 92 links internos OK. Palavras: 2.4 com 1.382 (32 acima do teto), demais entre 1.252 e 1.359.
- **Bloco 4 concluído (Sonnet 5.5 High, effort declarado pelo operador, 15/10/2026):** hashes revalidados; `validar-guia.py` 16 OK, 0 falha; `conferir-trechos.py` 126 aprovados; Chrome nas 6 larguras, axe, questões e links OK; Capítulo 1, CSS e script comparados com a versão anterior (idênticos, exceto a navegação da página 10 e o sumário). Criados `changelog-capitulo-2.md` e `handoff-capitulo-2-fechado-2026-10-15.md`; `CLAUDE.md` e memória atualizados. Sem Git (pasta fora de repositório).
- **Capítulo 2 fechado.** Conforme pedido do operador, pausa para as duas revisões que ele vai pedir; nada além disso sem pedido. **Pedido do operador (15/10/2026):** ao fechar o capítulo por completo, parar e aguardar dois pedidos de revisão dele; não iniciar nenhuma revisão antes.

claude - pessoal, 15/10/2026
