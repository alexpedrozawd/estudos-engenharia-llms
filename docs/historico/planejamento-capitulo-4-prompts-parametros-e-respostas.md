# Planejamento do Capítulo 4 — Prompts, parâmetros e respostas

Data: 13/11/2026. Autoria: deepseek - conta não verificada (painel). Etapa: **somente planejamento**; nada redigido no guia, nenhuma fonte baixada. Depende de aprovação do operador antes do Bloco 1.

Base: [plano mestre](planejamento-completo-estudos-engenharia-llms.md), [plano do Capítulo 3](planejamento-capitulo-3-problemas-e-especificacoes.md), [requisitos de formato](../../requisitos-de-formato-html-do-material.md) (§8, parte curta; §9, impressão e exemplos), [protocolo de economia de tokens](../../protocolo-de-economia-de-tokens-entre-sessoes.md). Herda o método de produção dos capítulos 2 e 3 e a divisão em partes curtas de 13/11/2026.

## 1. Objetivo, escopo e aceite

**Objetivo:** ao concluir o capítulo, o estudante transforma a especificação do capítulo 3 num prompt que se monta, se mede e se confere: separa instrução de dado, escolhe exemplos e técnicas com base em fonte, organiza mensagens e papéis, conta tokens antes de enviar, escolhe parâmetros que existem no provedor certo e trata a resposta inválida sem fingir que não houve.

**Escopo:** abertura, seis unidades em partes curtas, seis questões, termos do glossário e referências. Progressão fixada no plano mestre: instruções e exemplos → técnicas de prompt com fonte primária → mensagens → contagem de tokens → parâmetros → schemas, templates e tratamento de falhas.

**Fora do escopo:** avaliar qualidade e comparar modelos (módulo 5); injeção de prompt, permissões e isolamento (módulo 6); proporcionalidade e custo total (módulo 7); contexto, histórico e compactação (módulo 8); contratos de ferramentas e MCP (módulo 9); RAG (módulo 10); agentes e ciclos (módulo 11); inferência local (módulo 12); escolha e troca de modelo (módulo 13); operação (módulo 14); cache, esforço e economia (módulo 15). Só menção, com ponte.

**Aceite:**
- cada unidade em partes de 400 a 500 palavras, no molde do §8: resumo "Em 3 linhas", imagem opcional, analogia, texto, uma pergunta, ponto de retomada, notas de fonte; a última parte traz *Ler*, *Assistir* e *Aprofundar* (sem *Assistir* se não houver vídeo conferido, como no capítulo 3);
- nenhum trecho de programa; prompt e JSON aparecem em `figure.bloco-codigo` com `data-executavel="false"` e legenda que declara "ilustrativo, não executado";
- toda técnica de prompt com fonte primária e trecho literal conferido; nenhuma afirmação sobre comportamento de provedor sem data de consulta;
- exemplos sem nomes internos: Aurora Educação (fictícia) e plataforma interna de IA genérica;
- seis questões (duas fáceis, três médias, uma difícil), gabarito sem padrão regular e diferente dos capítulos 1, 2 e 3;
- `validar-guia.py` sem falha; PDF em A4 sem bloco dividido; Chrome de 320 a 1920 px sem rolagem horizontal; mecânica das questões OK.

## 2. Decisões de desenho

1. **Nível:** quem leu os capítulos 1 a 3. O prompt parte da especificação já escrita: a 3.6d deixou problema, usuário, resultado, restrições, aceite e contratos; aqui eles viram texto enviado ao modelo.
2. **Eixo:** prompt não é truque nem fórmula. É um artefato com entrada, formato, custo e modo de falha — montado, medido e conferido.
3. **Caso principal:** o assistente de matrícula da Aurora, especificado no capítulo 3. Ele aparece no fechamento de cada unidade (versão 1, versão 2, orçamento, parâmetros, resposta inválida), não em todas as partes. Para não repetir, duas cenas curtas de contexto diferente: extração de campos de um formulário e redação de um comunicado. Assim cada técnica tem onde brilhar e onde falhar.
4. **Partes curtas:** 20 partes, na proporção 3/4/3/3/3/4. A 4.2 tem quatro porque carrega as três técnicas com fonte primária; a 4.6 tem quatro porque fecha schemas, templates, falhas e o caso.
5. **Uma tabela por parte, no máximo.** Comparação antes/depois de prompt, orçamento de tokens e tabela de falhas.
6. **Prompts como texto, não como código.** Bloco `figure.bloco-codigo` com `pre.codigo`, `tabindex="0"`, `aria-label`, `data-executavel="false"` e legenda "prompt ilustrativo, não executado". Até 12 linhas, como o JSON do capítulo 2. O capítulo não ensina a programar: mostra o que o modelo recebe.
7. **Qualificadores mantidos:** *registrado na documentação*, *registrado na norma*, *verificado no código local*, *proposta didática*.
8. **Parâmetros mudam.** Indício registrado em material técnico consultado nesta sessão (não em fonte primária lida, por isso fica como hipótese forte): a API da Anthropic teria passado a rejeitar `temperature`, `top_p` e `top_k`, com o controle de profundidade em `effort`. O Bloco 1 confirma ou derruba isso com trecho literal. Se confirmar, a 4.5a ensina o fato em vez de fingir que os botões antigos continuam iguais em todo provedor; se não confirmar, a unidade descreve os parâmetros conforme a documentação vigente. Em qualquer caso, a regra didática é: **conferir a documentação do provedor e do modelo antes de usar um parâmetro**.
9. **Ids:** `capitulo-4`, `unidade-4-1a` a `unidade-4-6d`, `questoes-capitulo-4`, `c4q1` a `c4q6`. O sumário passa a apontar para `#unidade-4-1a`.
10. **Links externos** em nova guia (`target="_blank" rel="noopener noreferrer"`).
11. **Imagens:** poucas. Proposta de três molduras (4.1a, 4.3a, 4.6b), só com `role="img"` e `aria-label` até o texto estar finalizado, revisado e validado. Geração na última etapa, com autorização.
12. **Ponte com o capítulo 3:** a especificação é a entrada; o prompt é a tradução dela. Nenhuma unidade reexplica problema, aceite ou contrato.

## 3. Fontes (nenhuma lida nesta sessão; conferir e extrair no Bloco 1)

| Fonte | Papel | Estado |
|---|---|---|
| Anthropic — documentação de *prompt engineering* (visão geral e técnicas) | Instruções claras, exemplos, tags XML, passos; aviso de que técnicas são empíricas | A localizar e ler |
| Anthropic — referência da Messages API | Papéis, blocos de conteúdo, `max_tokens`, `stop_sequences`, parâmetros de amostragem e status atual | A ler só as seções citadas |
| Anthropic — *Token counting* (`POST /v1/messages/count_tokens`) | Contar antes de enviar; estimativa contra medida | A ler |
| Anthropic — *Structured outputs* (`output_config.format`, `messages.parse`) | Formato de resposta definido por schema | A ler |
| Anthropic — página de esforço (declarada em 13/11/2026) | `effort` como controle de profundidade | A ler; trecho literal |
| Brown et al., *Language Models are Few-Shot Learners* (arXiv:2005.14165, 2020) | Exemplos no prompt | A ler o trecho sobre in-context learning |
| Wei et al., *Chain-of-Thought Prompting* (arXiv:2201.11903, 2022) | Raciocínio passo a passo | A ler o trecho de resultado |
| Min et al., *Rethinking the Role of Demonstrations* (arXiv:2202.12837, 2022) | Contraponto: o que o exemplo ensina de fato | A ler só a conclusão |
| OpenAI — *Structured Outputs* e guia de prompt | Segunda implementação; schema e limites | A ler |
| JSON Schema (json-schema.org) | Definição formal de schema | A ler só a visão geral |
| `docs/09` do Router (interna) | Antipadrão: empilhar instruções sem medir; prompt patching | Lido em 13/11/2026; sem link público |
| Medição local de 23/10/2026 e protocolo de economia de tokens | Ordem de grandeza de tokens por caractere | Já no projeto |

**Evidência local (leitura, lista fechada, sem execução):** plataforma interna de IA — campos do pedido, contagem de tokens e tratamento de resposta inválida, se documentados; serve de exemplo de contrato existente. Aurora Educação — situação construída, marcada *proposta didática*, sem pessoas, dados de clientes ou nomes de fornecedores. Nenhuma chamada real a modelo, nenhuma chave lida.

## 4. Mapa por unidade

### 4.1 Instruções e exemplos (3 partes)
- **Competência:** separar instrução de dado; escrever instrução com objetivo, entrada, saída e limite; decidir quando mostrar um exemplo e o que ele ensina; reconhecer que instrução não substitui validação.
- **Partes:** *4.1a O modelo recebe texto, não intenção* — tudo chega no mesmo canal; marcar onde a instrução termina e o dado começa. *4.1b Mostrar em vez de descrever* — um ou dois exemplos ensinam formato e tom; não ensinam fato novo nem regra que o modelo não tem. *4.1c A primeira instrução do assistente de matrícula* — objetivo, fontes permitidas, o que não responder, formato; o que ainda falta.
- **Conceitos:** instrução, dado, delimitador, exemplo, formato de saída.
- **Equívocos:** "quanto mais texto, melhor"; "maiúsculas e 'NUNCA' são controle" (retomada do prompt patching, 1.6); "um exemplo garante acerto".
- **Ponte:** 4.2 (técnicas) e 6 (injeção de prompt).

### 4.2 Técnicas de prompt com fonte primária (4 partes)
- **Competência:** aplicar três técnicas com o que o artigo mediu e o que não mediu; reconhecer custo em tokens e latência; não tratar técnica como garantia nem como receita que atravessa modelos.
- **Partes:** *4.2a Exemplos no prompt, com a fonte na mão* — Brown et al.; o que o experimento mostrou; Min et al. como contraponto (o rótulo importa menos que o formato). *4.2b Raciocínio passo a passo* — Wei et al.; quando ajuda (várias etapas, aritmética, lógica); custo em tokens; quando atrapalha (tarefa simples, resposta factual) e a diferença para modelos que já pensam internamente (1.4c). *4.2c Instruções estruturadas* — passos numerados, formato explícito, marcas; documentação da Anthropic como fonte; o que muda entre instrução vaga e estruturada. *4.2d O prompt do assistente, versão 2* — aplica as três; tabela antes/depois; o que melhorou, o que continua sendo responsabilidade do sistema.
- **Conceitos:** exemplo no prompt, raciocínio passo a passo, instrução estruturada, custo do prompt, transferência entre modelos.
- **Equívocos:** "existe o prompt perfeito"; "funcionou num modelo, funciona em todos"; "mais raciocínio é sempre melhor".
- **Ponte:** módulo 5 (medir se melhorou) e 15 (custo).

### 4.3 Mensagens e papéis (3 partes)
- **Competência:** montar a lista de mensagens com papéis; entender que o papel organiza a conversa e não cria permissão; reconhecer tipos de conteúdo; saber o que o histórico faz com o custo.
- **Partes:** *4.3a Quem fala o quê* — `system`, `user`, `assistant`; a instrução do sistema; o que é do sistema e não do modelo. *4.3b O conteúdo tem tipos* — texto, imagem, resultado de ferramenta no mesmo canal; a documentação como fonte. *4.3c Instrução não é permissão* — o prompt de sistema não é fronteira de segurança; quem autoriza é o sistema em volta; ponte para 6.
- **Conceitos:** mensagem, papel, prompt de sistema, bloco de conteúdo, histórico.
- **Equívocos:** "system prompt é firewall"; "o modelo lembra sozinho"; "histórico é grátis".
- **Ponte:** 2.2b (a chamada não guarda a conversa), 8 (histórico) e 6 (permissões).

### 4.4 Contagem de tokens (3 partes)
- **Competência:** saber o que entra na conta; medir em vez de estimar; usar a contagem para orçamento e corte.
- **Partes:** *4.4a O que entra na conta* — instrução, histórico, documentos, definições de ferramenta e a resposta que vai ser escrita; entrada e saída no mesmo orçamento (retomada curta de 1.3 e 2.2a). *4.4b Medir, não adivinhar* — endpoint de contagem, tokenizador e a regra prática de caracteres ÷ 3,5 como estimativa; a medição local de 23/10/2026 como prova de ordem de grandeza. *4.4c O orçamento do assistente de matrícula* — quanto cabe, o que cortar primeiro, o que nunca cortar.
- **Conceitos:** contagem de tokens, tokenizador, estimativa, orçamento de entrada, orçamento de saída.
- **Equívocos:** "uma palavra é um token"; "estimar por caracteres basta"; "o modelo avisa quando não cabe".
- **Ponte:** 2.3 (limites) e 15 (custo).

### 4.5 Parâmetros (3 partes)
- **Competência:** escolher parâmetro que existe no provedor e no modelo usados; entender o que cada um muda; distinguir controle de variação de garantia de correção; ler a documentação antes de copiar receita.
- **Partes:** *4.5a Os botões que existem e os que saíram* — amostragem (temperatura, top-p, top-k) onde ainda existe; o caso da Anthropic, que passou a rejeitar esses campos e a usar `effort`; a lição: parâmetro é do provedor. *4.5b Tamanho e parada* — `max_tokens`, `stop_sequences` e o motivo de parada (2.2c); corte não é erro de rede. *4.5c Os parâmetros do assistente* — escolha por tarefa: extração pede pouca variação, redação pede alguma; por que "temperatura 0" não garante resposta igual.
- **Conceitos:** temperatura, top-p, top-k, `max_tokens`, sequência de parada, esforço, parâmetro.
- **Equívocos:** "temperatura 0 garante repetição"; "`max_tokens` maior deixa mais inteligente"; "receita de tutorial vale para qualquer modelo".
- **Ponte:** 1.4b (amostragem), 13 (esforço e troca de modelo) e 15 (custo).

### 4.6 Saída estruturada, templates e falhas (4 partes)
- **Competência:** pedir resposta em formato definido; validar antes de usar; montar template reutilizável e versionado; prever falha e decidir o que fazer.
- **Partes:** *4.6a Pedir no formato certo* — schema, campos obrigatórios, exemplos de saída; saída estruturada na Anthropic e na OpenAI como duas implementações. *4.6b Conferir antes de usar* — validação; JSON inválido, campo ausente, valor fora da faixa; quando reparar com o modelo e quando recusar. *4.6c O template da tarefa* — partes fixas e variáveis, versão, o que não entra no template. *4.6d Quando a resposta falha* — recusa, corte, formato inválido, repetição, fato inventado; o que fazer em cada caso; checklist do assistente e fechamento do capítulo.
- **Conceitos:** schema, validação, template, versão do prompt, recusa, corte, reparo.
- **Equívocos:** "JSON válido é resposta correta"; "reparar com o modelo sempre resolve"; "template é prompt maior".
- **Ponte:** módulo 5 (avaliação), 6 (falha segura) e 9 (contratos de ferramentas).

## 5. Matriz das seis questões (4 alternativas, 1 correta, primeira resposta trava)

| # | Nível | Unidades | Situação e foco | Distratores |
|---|---|---|---|---|
| Q1 | Fácil | 4.1 | Instrução e dados do aluno colados no mesmo parágrafo: o que fazer primeiro | aumentar a instrução; pedir ao modelo para "ignorar" o dado; trocar de modelo |
| Q2 | Fácil | 4.4 | "O prompt tem 800 caracteres, logo o custo está resolvido" | ignorar histórico e saída; medir só a entrada; confiar em estimativa |
| Q3 | Média | 4.2 | Raciocínio passo a passo pedido para classificar uma etiqueta simples | exigir mais passos; trocar por exemplo; culpar o modelo |
| Q4 | Média | 4.5 | Receita de tutorial manda `temperature: 0.7`; o provedor rejeita o campo | insistir; trocar de modelo; culpar a rede |
| Q5 | Média | 4.3 | Instrução no `system` tratada como permissão de acesso | confiar no prompt; mover para o usuário; pedir senha ao modelo |
| Q6 | Difícil | 4.6 | Resposta em JSON com campo ausente, valor inventado e corte por `max_tokens`: achar a premissa falha | validar só o JSON; aumentar `max_tokens`; pedir "mais cuidado" |

Cobertura: todas as unidades; Q4 e Q6 com situação para analisar. Gabarito na redação, sem padrão regular e diferente do capítulo 1 (B, D, A, C, B), do 2 (C, D, A, B, D, A) e do 3 (A, C, D, A, B, C). O validador confere de 5 a 6 questões por capítulo.

## 6. Produção: blocos, modelos e efforts

Só as combinações do projeto. Preflight em cada bloco; divergência `atual → recomendado` e pausa.

| Bloco | Modelo / effort | Conteúdo | Gate |
|---|---|---|---|
| 0 | — (operador) | Aprovar este plano e as decisões da §8. Depois, atualizar o sumário e validar. | Aprovação |
| 1 | Sonnet 5.5 High | Baixar as fontes da §3 para pasta temporária vazia (`curl -L`), extrair com `extrair-texto-web.py`; ler os trechos locais; montar `pacote-de-fontes-capitulo-4-2026-11-…md` com citação literal, seção e data; `conferir-trechos.py`. Não editar o guia. | Pacote aprovado pelo script |
| 2 | Sonnet 5.5 High | Abertura e 4.1. **Pausa: operador aprova nível, exemplo e tabela.** Depois 4.2 a 4.6, questões, glossário, referências; páginas novas na sequência; navegação; sumário. | Validador sem falha |
| 3 | Opus 5.5 High | Ler contra fontes e requisitos: técnicas, parâmetros, schema, coerência com 1 a 3 e sobreposição com 5 a 15. Correções pequenas; erro que exija reescrever volta ao Sonnet. | Sem achado material |
| 4 | Sonnet 5.5 High | Validador, PDF com Chrome for Testing, backup em `arquivo/antes-capitulo-4-2026-11-…/`, changelog, handoff. | Resultados registrados |

## 7. Riscos e controles

| Risco | Controle |
|---|---|
| Capítulo virar catálogo de "truques de prompt" | Cada técnica com fonte, condição e limite; nenhuma promessa sem medida |
| Repetir o capítulo 1 em temperatura e amostragem | Retomada curta; foco no que o provedor aceita hoje |
| Afirmar comportamento de provedor que muda | Data de consulta em toda afirmação; trecho literal; qualificador *registrado na documentação* |
| Prompt de exemplo virar aula de programação | Bloco não executável, até 12 linhas, legenda explícita |
| Exemplar da Aurora cansar como no capítulo 3 | Caso só no fechamento das unidades; duas cenas curtas de outro contexto |
| Sobreposição com 5, 6, 8, 9, 13 e 15 | Pontes explícitas; aprofundamento fica no módulo dono |
| Artigo citado de memória | Pacote de fontes com trecho literal conferido antes da redação |
| Página da Anthropic mudar entre a escrita e a publicação | Data de consulta no texto; nota no changelog |
| Questão com resposta opinativa | Situação com critério verificável na explicação |

Segurança e LGPD: prompts de exemplo sem dados pessoais reais; dados de alunos da Aurora são fictícios e de menor sensibilidade; nenhuma chave, token ou credencial no texto; nenhuma chamada real a modelo. Sem gatilho para triagem. Proporcionalidade: nenhuma dependência nova, nenhum componente, nenhuma fonte paga.

## 8. Decisões pedidas ao operador

1. Aprovar o plano: seis unidades, 20 partes (3/4/3/3/3/4), seis questões.
2. Confirmar o assistente de matrícula da Aurora como caso principal, só no fechamento das unidades, com duas cenas curtas de outro contexto.
3. Confirmar a pausa após a 4.1, como nos capítulos 2 e 3.
4. Confirmar as fontes da §3, em especial os três artigos (Brown, Wei, Min) e as páginas da Anthropic e da OpenAI, com a ressalva de não afirmar conformidade nem comportamento sem trecho literal.
5. Confirmar três molduras de imagem (4.1a, 4.3a, 4.6b), só como moldura até a validação.
6. Decidir o formato de prompt no guia: bloco não executável (recomendado) ou caixa de citação sem `pre`.

Padrões adotados se não houver outra decisão: abertura própria; no máximo uma tabela por parte; prompts em tabela ou em bloco não executável; sem componente novo.

## 9. Estado de continuidade (13/11/2026)

- Plano escrito nesta sessão; nada redigido no guia, nenhuma fonte baixada.
- Estado verificado antes: 73 páginas lógicas, validador 16 OK e 0 FALHA; hashes `guia-engenharia-llms.html` `78afd3998fa2c19e`, `guia-engenharia-llms.pdf` `a0b8f86d9f2a6df3`, `pacote-de-fontes-capitulo-3-2026-11-13.md` `3237eff413c3cb2f`.
- O sumário lista o capítulo 4 na linha 282, sem links nem conteúdo.
- Próxima ação: decisões da §8; depois, Bloco 1 (pacote de fontes).

deepseek - conta não verificada, 13/11/2026
