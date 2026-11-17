# Planejamento do Capítulo 1 — Fundamentos de IA e LLMs

Data: 13/10/2026 (revisão final com benchmarks). Autoria: claude (perfil `.claude-ap`; planejamento em Sonnet 5.5 High). Etapa: somente planejamento; nenhuma unidade foi redigida e o HTML não foi alterado.

Base: [planejamento aprovado](planejamento-completo-estudos-engenharia-llms.md), [requisitos de formato](requisitos-de-formato-html-do-material.md), [contexto do Router](contexto-de-estudo-ap-ai-router.md), [contexto da Nanda Mac](contexto-de-estudo-nanda-mac.md) e handoff de 13/10/2026.

## 1. Objetivo, escopo e aceite

**Objetivo:** ao concluir o capítulo, o estudante explica como um LLM produz uma resposta e usa isso para decidir o que fica no código, o que vai ao modelo e o que exige validação humana.

**Escopo:** abertura do capítulo, seis unidades (1.1–1.6) no formato de sete itens do planejamento, cinco questões, termos para o glossário e referências do capítulo. Ordem curricular preservada.

**Fora do escopo:** laboratórios, execução de código ou de tokenizadores, ações nos projetos-fonte. Assuntos com módulo próprio recebem só menção: parâmetros e schemas (4), contexto e memória (8), embeddings e RAG (10), KV cache e quantização (12), fine-tuning (condicional).

**Aceite:**
- cada unidade tem objetivo concreto, termos definidos, exemplo resolvido, limites, pergunta com feedback e ponto de retomada;
- toda afirmação técnica rastreia a uma fonte verificada (com seção e edição) ou é marcada como proposta didática;
- as cinco questões cobrem os seis tópicos, com pelo menos um caso profissional integrado;
- nenhum exemplo apresenta como implementado o que as fontes tratam como proposta, histórico ou futuro.

## 2. Decisões de desenho

1. **Ordem mantida.** *Token* aparece informalmente na 1.1 ("pedaço de texto") e é formalizado na 1.3. O Jurafsky & Martin também começa por "próxima palavra" antes de tokenizar.
2. **Base de IA dentro da 1.1** (recomendado); dividir em 1.0 só se a leitura mostrar sobrecarga.
3. **Qualificadores obrigatórios** nos exemplos reais: *verificado no código local*, *registrado na documentação*, *histórico/desativado*, *proposta didática*.
4. **Sem números sujeitos a mudança** (janelas, preços, versões). Quando indispensáveis: datados, com fonte. Divisões de tokens são rotuladas como ilustrativas, pois não se executa tokenizador nesta fase.
5. **Linguagem sobre o modelo.** Seguir o Jurafsky & Martin §1.11: "aprender", "esquecer" e "prever" são usados como atalho, com aviso; "entender" e "pretender" são evitados ou definidos. Analogia com autocompletar vem com seu limite.
6. **Exemplos da Nanda Mac:** funções e processos fictícios, sem nomes de pessoas, dados de clientes ou menção a ferramentas internas de análise.
7. **Figuras próprias.** Nenhuma figura de terceiros é reproduzida (Illustrated Transformer é CC BY-NC-SA 4.0).
8. **Fontes por unidade em três linhas curtas** no fim de cada unidade: *Ler*, *Assistir*, *Aprofundar*. Acrescenta-se ao formato de sete itens sem alterá-lo.

## 3. Fontes: o melhor de cada uma

**Critério de escolha:** atualidade e reputação. Não medi avaliações numéricas da comunidade; uso como indicador a adoção por universidade e o alcance do canal. Em empate, vence a edição mais recente. Nenhuma fonte paga é base de afirmação.

| Fonte | Papel no capítulo | Estado verificado em 13/10/2026 |
|---|---|---|
| **Jurafsky & Martin, *Speech and Language Processing*, 3ª ed. (rascunho de 19/08/2026)** | Espinha dorsal: definições, terminologia e ordem lógica. Cap. 1 já percorre os seis tópicos. | Cap. 1, 2, 7 e 8 abertos; seções abaixo conferidas nos PDFs. Gratuito online. Rascunho: citar com edição e data. |
| **Karpathy, *Deep Dive into LLMs like ChatGPT*** | Panorama de ponta a ponta para 1.1, 1.2, 1.4 e 1.6. | Título confere. Data e duração (fev/2025, cerca de 3h30) vêm de resumos de terceiros. Marcar trechos na redação. |
| **Karpathy, *Let's build the GPT Tokenizer*** e ***Let's build GPT*** | Tokenização e falhas dela (1.3); aprofundamento opcional da 1.5. | Existem e são gratuitos no YouTube; sem datas na página. |
| **3Blue1Brown, *Deep Learning* caps. 5 e 6** | Intuição visual de Transformers e atenção (1.5). | Título do cap. 5 confirmado; demais dados vêm de listagens de terceiros. |
| **Stanford CS224N (Winter 2026)** | Sequência didática atual: aulas Transformers, Pretraining e Post-training. | Slides públicos; vídeos de 2026 restritos a alunos (os de Spring 2024 são livres). |
| **Stanford CS336 (Spring 2025)** | Tokenização e inferência vistas por sistemas (1.3, 1.4). | Slides e notas linkados; oferta de 2026 não confirmada; licença e vídeos não confirmei. |
| **Vaswani et al. 2017 (arXiv 1706.03762)** | Fonte primária da atenção e do Transformer (1.5). | PDF livre, versão 7 (2023). Numeração de seções a conferir na redação. |
| **Hugging Face: *Text generation* e *Generation strategies*** | Comportamento prático da geração e dos parâmetros (1.4). | Lidas integralmente. Padrões descrevem a biblioteca, não provedores. |
| **Anthropic: janelas de contexto** | Fonte primária de "o que conta na janela" e contagem de tokens (1.3). | Só o trecho devolvido pela busca; reler a página na redação. |
| **Google ML Crash Course, módulo LLM (09/01/2026)** | Porta de entrada simples e ordem didática (1.1, 1.5). | Obtido por resumo automático; reler antes de citar. O resumo cita treino por tokens mascarados, o que diverge do §7 do Jurafsky & Martin (modelagem causal): prevalece o Jurafsky & Martin. |
| **Lilian Weng: *Extrinsic Hallucinations in LLMs* (07/2024)** | Complemento para alucinação (1.6). | Existe na lista do blog; texto não lido. |
| **Raschka, Alammar/Grootendorst, Huyen** | Leitura opcional, por capítulo. | Livros comerciais; só sumários conferidos. |

**Seções do Jurafsky & Martin a usar (conferidas nos títulos):**
- Cap. 1: §1.1 (o que é um LLM), §1.2 (o que se aprende ao prever tokens), §1.6 (treinamento: pré-treino, instruction tuning, RL para raciocínio), §1.7 (inferência), §1.10 (segurança e limitações: alucinação, excesso de confiança, má calibração), §1.11 (antropomorfismo e terminologia).
- Cap. 2: §2.4 (BPE; 2.4.1–2.4.3). Cap. 2 §2.3 (Unicode) só menção.
- Cap. 7: §7.1–7.2 (atenção e blocos), §7.5 (cabeça de modelagem), §7.6 (decodificação: gulosa, amostragem aleatória, amostragem por temperatura), §7.7 (pré-treinamento), nota sobre custo quadrático da atenção, §7.8 (KV cache, só ponte para o módulo 12).
- Cap. 8: §8.1 (instruction tuning), §8.3–8.4 (preferências, visão geral), §8.4.4 (limitações).

## 4. Mapa por unidade

Competência → conceitos → fontes (Ler / Assistir / Aprofundar) → aplicação → exemplo resolvido → equívocos (alimentam distratores) → critério de compreensão.

### 1.1 O que é um modelo de linguagem e como ele produz uma resposta?
- **Competência:** explicar que um LLM é uma função aprendida que calcula a distribuição de probabilidade do próximo pedaço de texto; distinguir *modelo* de *sistema ao redor* (instruções, ferramentas, estado, permissões).
- **Conceitos:** IA, aprendizado de máquina, modelo, modelo de linguagem, LLM, prompt, token (informal), probabilidade, harness.
- **Fontes:** *Ler* — Jurafsky & Martin cap. 1 §1.1, §1.2 e §1.11. *Assistir* — Karpathy, *Deep Dive* (trecho de abertura). *Aprofundar* — Google MLCC módulo 1.
- **Aplicação:** Router — o modelo gera texto; persistência, despacho, permissões e validação de caminhos são código (*verificado no código local*). Nanda Mac — o assistente interpreta o pedido; identidade, cálculo e status são do sistema (*registrado*).
- **Exemplo resolvido:** versão autoral do jogo de Shannon (adivinhar a próxima palavra de frases fictícias), seguido de um pedido percorrendo o fluxo simplificado do Router.
- **Equívocos:** consulta uma base de respostas; entende como pessoa; sabe fatos atuais; modelo = produto de chat.
- **Critério:** "Num assistente que responde dúvidas, o que faz o modelo e o que faz o sistema ao redor?"

### 1.2 Treinamento e inferência
- **Competência:** distinguir treinamento (ajuste de parâmetros) de inferência (parâmetros fixos); descrever pré-treinamento e pós-treinamento; explicar data de corte; justificar por que regras de negócio mutáveis vão ao contexto e não aos pesos; diferenciar modelo de fronteira (API) e local, no nível conceitual.
- **Conceitos:** parâmetros/pesos, dados de treino, pré-treinamento, instruction tuning, ajuste por preferências, inferência, data de corte.
- **Fontes:** *Ler* — Jurafsky & Martin cap. 1 §1.6 e §1.7; cap. 8 §8.1 e §8.3–8.4 (visão geral). *Assistir* — Karpathy, *Deep Dive* (pré-treino e pós-treino); slides CS224N "Pretraining" e "Post-training". *Aprofundar* — cap. 7 §7.7.
- **Aplicação:** Router — uso por inferência (Ollama local e clientes de fronteira); os contextos não registram treinamento. Antipadrão "fine-tuning prematuro" (`docs/09`). Nanda Mac — "assistente independente por login" significa contexto, histórico e permissões próprios, não um modelo treinado por pessoa.
- **Exemplo resolvido:** colaborador corrige o assistente numa conversa; o que muda no modelo (nada) e no contexto daquela conversa (*proposta didática*).
- **Equívocos:** cada conversa treina o modelo; modelo local aprende com o uso; inferência é treino rápido; um modelo por funcionário.
- **Critério:** "O colaborador corrigiu o assistente e, no dia seguinte, o erro voltou. Por quê?"
- **Limite:** sem retropropagação nem gradientes.

### 1.3 Tokens e contexto
- **Competência:** explicar que o modelo opera sobre tokens, não sobre caracteres ou palavras; tratar a janela de contexto como orçamento que inclui instruções, histórico, fontes, definições de ferramentas, resultados e a saída; saber que a contagem exata depende do tokenizador do modelo.
- **Conceitos:** token, tokenização por subpalavras (BPE), tokenizador, vocabulário, token especial, janela de contexto, orçamento de entrada e saída.
- **Fontes:** *Ler* — Jurafsky & Martin cap. 2 §2.4; documentação da Anthropic sobre janelas de contexto. *Assistir* — Karpathy, *GPT Tokenizer*. *Aprofundar* — slides CS336 "Overview and tokenization"; Hugging Face "Text generation" (*chat template*, tokens especiais).
- **Aplicação:** Router — janela local estimada por envelope mais reserva de saída, com teto Qwen de 64k declarado no código; caracteres são estimativa, não contagem de tokens (*verificado no código local*). Antipadrão "entupimento de contexto". Nanda Mac — descrições de ferramentas e schemas também consomem contexto.
- **Exemplo resolvido:** montar o orçamento de um pedido fictício (instrução + histórico + documento + ferramentas + espaço de resposta). Divisão em tokens ilustrativa. Pode inspirar-se no exercício 2.2 do cap. 2 (tokenizar número longo, URL, fórmula).
- **Equívocos:** token = palavra; janela grande = pôr tudo; caracteres ÷ 4 é exato; contexto = memória permanente.
- **Critério:** "O que ocupa a janela numa chamada com histórico e uma ferramenta?" e "por que 'cabe' não significa 'convém'".
- **Ponte:** módulos 4 e 8.

### 1.4 Como o modelo gera a resposta
- **Competência:** descrever o laço autorregressivo (calcular distribuição → escolher token → anexar → repetir até fim de sequência ou limite); explicar por que respostas variam; relacionar limite de saída, decodificação gulosa, amostragem e temperatura ao comportamento; saber que baixa variação não garante correção.
- **Conceitos:** distribuição de probabilidade, geração autorregressiva, decodificação gulosa, amostragem, temperatura, token de fim de sequência, limite de saída; beam search e logits só como menção.
- **Fontes:** *Ler* — Jurafsky & Martin cap. 7 §7.5 e §7.6; Hugging Face "Text generation" e "Generation strategies". *Assistir* — Karpathy, *Deep Dive* (parte de inferência). *Aprofundar* — Lilian Weng sobre computação na inferência (menção a raciocínio).
- **Aplicação:** Router — o chat Ollama usa `/api/generate`, sem ferramentas; marcador de conclusão não prova proposta útil (*verificado no código local*). Nanda Mac — valor cobrado é calculado em código; o modelo, no máximo, redige ou explica (*registrado*).
- **Exemplo resolvido:** tabela fictícia de probabilidades do próximo token, comparando guloso e amostragem em três passos (*proposta didática*).
- **Equívocos:** temperatura baixa = resposta verdadeira ou reprodutível em qualquer ambiente; resposta cortada = modelo "desistiu"; variação = defeito. Valores padrão da biblioteca não valem para provedores: verificar a documentação do provedor antes de afirmar.
- **Critério:** "A mesma pergunta gerou duas respostas diferentes: quando isso é aceitável e quando exige controle em código?"
- **Limite:** schemas → módulo 4.

### 1.5 Atenção e Transformers
- **Competência:** explicar em alto nível que na autoatenção cada token pondera os demais; descrever o Transformer só-decodificador como pilha de camadas que produz a distribuição do próximo token; relacionar o custo da atenção ao tamanho do contexto.
- **Conceitos:** autoatenção, multi-cabeça, camadas, decodificador causal, posição, custo crescente com o contexto.
- **Fontes:** *Ler* — Jurafsky & Martin cap. 7 §7.1–7.2 e a nota sobre custo quadrático; Vaswani et al. 2017 (arquitetura e atenção). *Assistir* — 3Blue1Brown caps. 5 e 6; slides CS224N "Transformers". *Aprofundar* — Karpathy, *Let's build GPT*; Illustrated Transformer (só como leitura).
- **Aplicação:** por que contexto longo custa mais e pode piorar o resultado; liga-se à economia de contexto do Router e a selecionar fontes e ferramentas por etapa. KV cache (cap. 7 §7.8) fica para o módulo 12.
- **Exemplo resolvido:** frase em português com referência ambígua ("…a aluna enviou à secretária o documento que *ela* havia pedido"), mostrando o que a atenção resolve; analogia autoral rotulada como intuição.
- **Equívocos:** atenção = foco ou consciência; Transformer = ChatGPT; pesos de atenção explicam a decisão do modelo (não afirmar sem fonte).
- **Critério:** "Dobrar o contexto sai de graça? Por quê?"
- **Limite:** sem álgebra além de uma caixa opcional sobre Q/K/V. O custo quadrático vale para o mecanismo padrão; otimizações ficam fora.

### 1.6 Capacidades e limitações
- **Competência:** identificar onde LLMs agregam valor (linguagem, síntese, ambiguidade) e onde cabe código determinístico; reconhecer limites (alucinação, excesso de confiança, data de corte, variação, sensibilidade ao formato do prompt, custo, contexto finito); escolher controles proporcionais (fonte, validação, revisão humana, código).
- **Conceitos:** alucinação, calibração, determinismo, *code-first, LLM-second*, controle proporcional, responsabilidade humana.
- **Fontes:** *Ler* — Jurafsky & Martin cap. 1 §1.10 e §1.11; cap. 8 §8.4.4; `docs/09` (fonte interna). *Assistir* — Karpathy, *Deep Dive* (alucinação e falhas). *Aprofundar* — Lilian Weng, *Extrinsic Hallucinations*; Anthropic, *Building effective agents*.
- **Aplicação:** Nanda Mac — software, LLM e pessoa têm responsabilidades distintas; regras de cobrança, preço, status e permissão não dependem de interpretação probabilística. A recusa de senha de administrador relatada em ata é *observado em ata*, sem presumir implementação. Router — prompt orienta; autorização é aplicada pelo sistema (*verificado*).
- **Exemplo resolvido:** classificar quatro tarefas fictícias (somar parcelas; redigir lembrete; checar permissão; resumir contrato) em código, LLM, pessoa ou híbrido.
- **Equívocos:** texto fluente é texto correto; "NUNCA faça X" no prompt é controle; modelo maior elimina alucinação; usar LLM para lógica simples é inofensivo.
- **Critério:** "Dada uma tarefa, em qual camada ela fica e que controle é proporcional?"
- **Ponte:** módulos 3, 5, 6, 7 e 8.

## 5. Matriz das cinco questões (padrão adotado: 4 alternativas, 1 correta, primeira resposta trava — ver §8)

| # | Nível | Tópicos | Situação-base e foco | Distratores (equívocos) |
|---|---|---|---|---|
| Q1 | Fácil | 1.1, 1.2 | Colaborador corrige o assistente; o que mudou no modelo | treino contínuo; modelo por pessoa; "memorizou" |
| Q2 | Fácil | 1.3 | O que ocupa a janela numa chamada | só a pergunta; token = palavra; histórico não conta |
| Q3 | Média | 1.4 | Respostas diferentes e resposta cortada; diagnóstico | defeito do modelo; temperatura baixa garante verdade |
| Q4 | Média | 1.5, 1.3, 1.6 | Equipe cola 30 documentos "porque cabe"; escolher conduta | janela grande = melhor; custo constante |
| Q5 | Difícil | 1.1, 1.2, 1.4, 1.6 | Assistente de cobrança fictício: dividir responsabilidades entre código, LLM e pessoa; achar a premissa falha | prompt como controle; treinar com regras; LLM calcula valores |

Cobertura: 1.1 (Q1, Q5), 1.2 (Q1, Q5), 1.3 (Q2, Q4), 1.4 (Q3, Q5), 1.5 (Q4), 1.6 (Q4, Q5). Q3–Q5 trazem casos, restrições ou trechos para analisar. Cada explicação diz por que a correta serve e por que cada distrator falha.

## 6. Produção do capítulo: evidência, fases, modelos e efforts

### 6.1 Evidência de benchmarks (família 5.5, consultas de 13/10/2026)

**Fontes primárias:** system cards da Anthropic — Haiku 5.5 (07/10/2026), Sonnet 5.5 (28/09/2026) e Opus 5.5 (22/09/2026), baixados e lidos em texto — e as páginas oficiais "Choosing the right model" e "Optimizing for cost and intelligence". **Independentes:** Artificial Analysis (GDPval-AA, AA-Briefcase e AA-Omniscience; os dois primeiros foram publicados pela Anthropic). Agregadores e blogs entram só como complemento e divergem entre si (marcados com †). Scores no effort máximo, salvo indicação.

| Ótica do projeto | Benchmark | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 | Leitura |
|---|---|---|---|---|---|
| Documentos profissionais | GDPval-AA v2.1 (Elo) | 1620 | 1840 | 1846† | Haiku ~220 pontos abaixo |
| Trabalho longo de conhecimento | AA-Briefcase v1.1 (Elo) | 1578 | 1824 | 1822† | Idem |
| Fundamentar em documentos dados | OfficeQA / Pro | 73,5 / 60,3 | 76,9 / 65,6 | — | Diferença pequena com a fonte à mão |
| Factualidade sem fonte | AA-Omniscience (saldo) | 0,12 | 0,35 | 0,58 | **Maior lacuna**; Haiku ~40% de alucinação (AA, via †) |
| Honestidade sob pressão | MASK | ≈ Sonnet | ≈ Haiku | — | Sem lacuna relevante |
| Multilíngue (42 idiomas) | GMMLU | 87,8 | 92,1 | 94,3 | Português não é separado |
| Seguir instruções | Auditoria comportamental | Melhor que Haiku 4.5; similar ou pouco pior que Sonnet; pior que Opus | — | — | Mais recusas indevidas que qualquer modelo testado |
| Código delimitado | SWE-bench Multilingual | 83,7 | 90,3 | — | Lacuna menor |
| Código difícil | SWE-Bench Pro | 64,8 | 81,3 | 89,9† | Lacuna grande |
| Código agêntico longo | Terminal-Bench 4.0 | 39,2 (AA: 33) | 70,6 | 66,4 | Fora do perfil do Haiku |
| Contexto longo | ProgramBench | 82,0 | 79,7 | 91,2 | Sem lacuna para o Sonnet |
| Fontes externas não confiáveis | Injeção de prompt (Gray Swan, k=15) | 7,1% de sucesso do ataque (Haiku 4.5: 83,2%) | — | — | "Comparável à fronteira" na maioria dos testes |

**Sensibilidade ao effort (system card do Haiku, §8.11.3 e §8.10):**
- HealthBench Professional, Haiku: 57,9 (low), 59,9 (medium), 61,3 (high), 61,0 (xhigh), 64,8 (max). Tempo de 8 a 21 s até xhigh e ~110 s no max. Sonnet, Opus e Fable variam menos de 2 pontos entre os níveis e superam o Haiku em todos abaixo do max.
- PhysicianBench, Haiku: 17,8 / 25,2 / 31,6 / 35,8 / 43,0 de low a max.
- GDPval-AA, Haiku: 1277 em medium (cerca de um décimo dos tokens do max) contra 1620 em max. Em AA-Briefcase: 1372 contra 1578.
- Teste independente de 8 tarefas de código (uma rodada)†: low 8/8 com 6.444 tokens; medium 8/8 com 8.360; high 8/8 com 10.830; **max 7/8 com 132.499 tokens**, com relato de orçamento inteiro gasto em raciocínio sem produzir texto.

**Posicionamento oficial:** Haiku para resumos, compactação, consultas, classificação e subagentes, "para trabalho com saídas verificáveis"; Sonnet e Opus para código agêntico complexo. A documentação recomenda partir do modelo barato, testar e subir só onde houver lacuna, mas avisa que "a conta é decidida pelas tarefas que o modelo barato falha" e que o Haiku só foi medido como executor, não como worker: testar em tarefas próprias.

**Limite da evidência:** nenhum benchmark mede texto didático em pt-BR, fidelidade a uma seção citada ou qualidade pedagógica. Os mais próximos são GDPval-AA e AA-Briefcase (documentos), OfficeQA (fundamentação) e GMMLU (multilíngue). Os números sustentam hipóteses; o piloto (§6.4) decide.

### 6.2 Conclusão de encaixe

- **O Haiku cabe** onde a entrada traz tudo o que ele precisa, há verificação determinística e o erro é barato de detectar.
- **Não cabe** onde o texto exige conhecimento fora da fonte (exemplos, analogias, distratores) ou julgamento pedagógico: a lacuna de factualidade sem fonte é a maior, e as demais lacunas crescem com a dificuldade.
- **Ordem de grandeza** (estimativa, não medição): uma unidade tem alguns milhares de tokens de saída, cerca de US$ 0,03–0,08 no Sonnet contra US$ 0,002–0,004 no Haiku, nos preços de API. O ganho real está na cota do plano e na latência. Isso não justifica arriscar a prosa conceitual.
- **Opus 5.5** tem o menor saldo de erro factual (0,58) e a melhor nota multilíngue; serve a uma única leitura final do capítulo. No trabalho de documentos fica quase igual ao Sonnet (1846† contra 1840) por duas vezes o preço, então não é redator.

### 6.3 Blocos de execução (decisão do operador em 13/10/2026: quatro blocos)

As etapas são agrupadas por modelo e effort para reduzir trocas: três trocas de modelo (Haiku → Sonnet → Opus → Haiku). Cada bloco roda em sessão própria, aberta com este plano como entrada — use o handoff vigente e revalide os hashes —, porque o cache é por modelo e a sessão de planejamento está longa. **Preflight em cada bloco:** conferir modelo e effort ativos; se divergirem do bloco, registrar `atual → recomendado` e pausar. Recomendação; a configuração não comprova o que está rodando.

| Bloco | Modelo / effort | Conteúdo, em ordem | Saída e gate |
|---|---|---|---|
| **1** | **Haiku 5.5 Medium** | (a) Pacotes de fontes das seis unidades em `pacotes-de-fontes-capitulo-1.md`: trechos literais com seção, edição e data. (b) `ferramentas/conferir-trechos.py`: confirma que cada trecho existe no texto extraído da fonte (pdftotext em área temporária). (c) `ferramentas/mecanica-questoes-prototipo.html`: radios, correção local, `success`/`danger`, redução de movimento, anúncio a tecnologias assistivas, com perguntas de teste e testes de gabarito. (d) `ferramentas/validar-guia.py`: roteiro de validação (§6.3, fim). **Não editar `guia-engenharia-llms.html`.** | Script de trechos passa; qualquer trecho ausente reprova o pacote da unidade e ele é refeito no Bloco 2 |
| **2** | **Sonnet 5.5 High** | 2.1 Conferir as saídas do Bloco 1. 2.2 Abertura do capítulo + unidade 1.1 no HTML, com link no sumário e numeração. **Pausa: operador aprova o formato.** 2.3 Unidades 1.2 a 1.6 em sequência (leitura da seção, redação, revisão breve, link e numeração a cada unidade). 2.4 Integrar o JS e as cinco questões; revisar semântica e acessibilidade do código do Haiku. 2.5 Glossário e referências do capítulo. 2.6 Rodar a validação e corrigir. | HTML do capítulo completo; validação passa |
| **3** | **Opus 5.5 Medium** | Ler o capítulo inteiro contra os requisitos e as fontes; relatório de achados; aplicar correções pequenas. Erro conceitual que exija reescrever uma unidade: registrar e voltar ao Sonnet High (troca extra). | Sem achado material |
| **4** | **Haiku 5.5 Low** | Rodar a validação de novo, registrar changelog em `.md`; Git só se houver repositório indicado. | Resultado do script e autorização vigente |
| **4b** (opcional) | **Haiku 5.5 High** | Piloto (§6.4). | Decisão para os capítulos 2 a 15 |

**Regras de effort do Haiku:**
- **Low:** edição e execução mecânicas já conferidas por script; nunca para conteúdo.
- **Medium:** extração com fonte à mão e código delimitado com testes.
- **High:** só no piloto.
- **xhigh:** não compensa, pois fica igual ao high.
- **Max:** vetado: 12 vezes os tokens do high, ~110 s por resposta e risco de esgotar o orçamento em raciocínio.
- **Falhou na verificação:** a classe de tarefa passa ao Sonnet, sem laços de nova tentativa.

Fable fica fora (emergência manual, por regra). O Opus só entra no Bloco 3.

**Roteiro de validação** (`ferramentas/validar-guia.py`): idioma e viewport; textos exatos da capa; links internos e para documentos locais; nenhuma dependência externa; um gabarito por questão; páginas e links do sumário consistentes; reflow simulado em 320 px CSS sem rolagem horizontal. Pendente por natureza: conforto nos três aparelhos reais.

**Git:** a pasta não é repositório. Commit e push só se você indicar um repositório; sem isso, o fechamento é o changelog `.md`.

### 6.4 Piloto (Bloco 4b, opcional)

Serve aos capítulos 2 a 15. O Haiku High refaz a unidade 1.3 a partir do pacote de fontes e do molde da 1.1; compara-se com a versão final do Sonnet (baseline pronta). O consumo é medido pelo `/usage`.

**Checklist:**
- cada afirmação rastreável à seção citada;
- nenhuma fonte inventada;
- verbos antropomórficos definidos ou evitados;
- sete itens da unidade presentes;
- pt-BR simples;
- qualificadores corretos nos exemplos reais;
- extensão da 1.1.

**Adoção:** o Haiku passa em no máximo uma rodada de correção e o consumo total é menor que o do Sonnet. Caso contrário, os capítulos seguintes mantêm o Sonnet para redação.

## 7. Riscos e controles

| Risco | Controle |
|---|---|
| Rascunho do Jurafsky & Martin muda | Citar edição e data; reler a seção ao redigir |
| Resumos automáticos de fontes distorcem o texto | Reler a fonte original; Google MLCC e vídeos têm cautela explícita |
| Simplificação que distorce o mecanismo | Definir termos, declarar limite da analogia, revisão contra a fonte |
| Fato sujeito a mudança (janelas, padrões de API) | Evitar números; datar e citar |
| Mistura de realidade e proposta nos exemplos | Qualificadores obrigatórios |
| Unidade longa ou termo novo demais | Um conceito por unidade; calibrar na F1 |
| Exposição de dados ou ferramentas internas | Exemplos fictícios; funções em vez de nomes |
| Questões que premiam memorização | Q3–Q5 com casos; distratores vindos de equívocos reais |
| Haiku afirma sem fonte | Só recebe tarefas de entrada completa e com verificação por script; falha devolve ao Sonnet |
| Recusas indevidas do Haiku (maior taxa entre os modelos testados) | Capítulo 1 é conteúdo benigno; reavaliar no módulo 6 (segurança) |
| Benchmarks sem medida de texto didático em pt-BR | Piloto da §6.4 com checklist próprio |
| Números de agregadores divergem (ex.: Terminal-Bench) | Marcados com †; decisões usam cards e AA |

Segurança e LGPD: sem dados pessoais ou credenciais no escopo; sem gatilho para triagem. Proporcionalidade: sem indício material de excesso.

## 8. Decisões e pendências

**Decisões confirmadas pelo operador em 13/10/2026:**
- Estrutura em **quatro blocos** (§6.3). Isso inclui o Haiku 5.5 nos blocos 1 e 4 e o Opus 5.5 Medium no bloco 3; tratado como autorização restrita a esses blocos. O CLAUDE.md veda modelos "mini/sub-par" sem classificar o Haiku; para liberar de forma geral, a mudança é em `guidelines/`.
- Fontes: Jurafsky & Martin (19/08/2026) como texto-base; livros pagos apenas opcionais (§3).
- Haiku nunca em max; o Haiku só recebe tarefas de entrada completa e com verificação por script.

**Padrões adotados enquanto o operador não decidir outra coisa** (ajustáveis na pausa do Bloco 2 ou antes):
1. A base de IA e aprendizado de máquina entra **dentro da 1.1**; divide-se em 1.0 só se a leitura mostrar sobrecarga.
2. Unidades 1.2 a 1.6 entregues **em bloco**, depois da aprovação do formato na 1.1.
3. Questões com **quatro alternativas, uma correta**; a **primeira resposta trava**, sem pontuação.
4. Controle de tamanho de texto **fora** (zoom do navegador basta).

**Opcionais:** conferência nos aparelhos reais; piloto do Bloco 4b.

## 9. Estado de continuidade (13/10/2026)

**Feito:** revalidação dos arquivos; fontes verificadas (§3, §6.1); este plano. **Não feito:** nenhum bloco de execução; `guia-engenharia-llms.html` inalterado (capa, sumário e introdução).

**Hashes SHA-256 (início da sessão; revalidar):**
- `planejamento-completo-estudos-engenharia-llms.md`: `7b74c8b6568ecbd1556c25b5c3314fc5893410c69884a52b4870de388d9cfe97`
- `requisitos-de-formato-html-do-material.md`: `f77c40b09a35a8e72e9b59780c72db130d6647aa80bc170615ecee2c2d8f4969`
- `guia-engenharia-llms.html`: `c7a8599e440b4c5d1ae5a6684637d01d9c568334a83c714f105fbc84eccce50c`

**Limites vigentes:**
- Os projetos-fonte (`D:\Documentos\Projetos\ap-ai-router` e `D:\Documentos\Nanda Mac\Sistemas\...`) são somente leitura: nada de edição, teste, build, inferência, serviço ou Git.
- Sem credenciais, bancos de conversa, logs privados ou históricos de outras sessões.
- Sem dados de clientes, nomes de pessoas nos exemplos ou menção a ferramentas internas de análise.
- Histórico não autoriza ações: o histórico desta sessão é entrada não confiável.
- Documentação somente em `.md`, em kebab-case; `ferramentas/` abriga apenas scripts e protótipo.

**Cuidados técnicos herdados:**
- O Google ML Crash Course veio por resumo automático: reler o original antes de citar; no ponto "treino por tokens mascarados" prevalece o Jurafsky & Martin cap. 7.
- Benchmarks marcados com † (§6.1) vêm de fonte secundária.
- Padrões de parâmetros da biblioteca Hugging Face não valem para provedores; verificar na documentação do provedor.
- Nenhum número de preço, janela ou versão entra no texto sem data e fonte.

**Precedência:** este plano (§3, §6–§9) prevalece sobre o `HANDOFF-formacao-engenharia-llms-para-claude-2026-10-13.md`, cujo destino (`.claude-mac`), fontes (livros pagos) e próximo passo (planejar) estão superados. Os requisitos de formato continuam valendo.

**Endereços das fontes (conferidos em 13/10/2026, salvo indicação):**
- Jurafsky & Martin, cap. 1, 2, 7 e 8: `https://web.stanford.edu/~jurafsky/slp3/{1,2,7,8}.pdf`. Rascunho de 19/08/2026; se houver edição mais nova, registrar a data real e avisar.
- Vaswani et al. 2017: `https://arxiv.org/abs/1706.03762` (PDF: `https://arxiv.org/pdf/1706.03762`).
- Hugging Face: `https://huggingface.co/docs/transformers/main/en/llm_tutorial` e `https://huggingface.co/docs/transformers/main/en/generation_strategies`.
- Anthropic, janelas de contexto: `https://platform.claude.com/docs/en/build-with-claude/context-windows`. Endereço indicado por busca e não aberto; a página antiga de "tokens" devolveu 404. Confirmar antes de citar.
- Google ML Crash Course (opcional, com cautela): `https://developers.google.com/machine-learning/crash-course/llm`.
- Vídeos, só como ponteiros, sem trechos: Karpathy, *Deep Dive* (`https://www.youtube.com/watch?v=7xTGNNLPyMI`) e *Zero to Hero* (`https://karpathy.ai/zero-to-hero.html`); 3Blue1Brown cap. 5 (`https://www.youtube.com/watch?v=wjZofJX0v4M`); slides CS224N (`https://web.stanford.edu/class/cs224n/`).

**Bloco 1: formato e regras**
- **Pacote de fontes:** por unidade, uma tabela com id da afirmação-alvo, trecho literal, fonte, seção, edição ou data, tipo (texto ou caso) e, nos casos, o qualificador (verificado, registrado, histórico ou proposta).
- **Casos:** trechos literais dos dois contextos de estudo (com a seção), sem nomes de pessoas nem dados de clientes. Os trechos de casos também passam pelo script de conferência, contra os `.md` locais.
- **Conferência:**
  - baixar com `curl -L` para pasta própria e vazia, em área temporária;
  - extrair com `pdftotext` (disponível pelo Bash);
  - manter os scripts em outra pasta, com Python `-I` e só biblioteca padrão;
  - normalizar espaços, quebras de linha e hifenização de fim de linha antes de comparar;
  - reportar a contagem de trechos aprovados e reprovados.
- **Arquivos novos permitidos:** somente `pacotes-de-fontes-capitulo-1.md`, `ferramentas/conferir-trechos.py`, `ferramentas/mecanica-questoes-prototipo.html` e `ferramentas/validar-guia.py`. Não sobrescrever nada; sem Git; sem tocar no HTML do guia nem nos projetos-fonte.
- **Testes:** executar com o que existir no ambiente (Node, se disponível; senão verificação estática por script) e declarar o que foi e o que não foi executado. Sem navegador, nada se afirma sobre aparência.
- **Haiku:** extrair, não completar de memória. Trecho não encontrado reprova o pacote da unidade. Sem laços de nova tentativa; falhou, passa ao Sonnet.
- **Assinatura:** `claude (perfil .claude-ap, <modelo>)`. O CLAUDE.md não define rótulo para este perfil.

**Próximo passo:** Bloco 1 (§6.3), com preflight de Haiku 5.5 Medium.

Assinatura: claude (perfil `.claude-ap`) — 13/10/2026.
