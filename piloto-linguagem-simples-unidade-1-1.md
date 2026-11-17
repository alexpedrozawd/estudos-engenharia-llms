# Piloto da revisão 2 — unidade 1.1 em linguagem simples

Data: 15/10/2026. Autoria: claude - pessoal (Sonnet 5.5, effort High declarado pelo operador). **Piloto aprovado e aplicado em 15/10/2026**; o texto final, com pequenos ajustes da leitura em Opus 5.5 High, está no guia. Este arquivo fica só como registro.

## Regras de linguagem usadas aqui
1. Frases curtas, uma ideia por frase (meta: até 15 palavras; nunca mais de 25).
2. Todo termo técnico é explicado **na primeira vez** em que aparece, com palavras do dia a dia. Primeiro o português; o termo em inglês entra uma vez, entre parênteses, só se você for vê-lo em documentações.
3. Nada de sigla ou palavra de especialista sem explicar (probabilidade, distribuição, determinístico, HTTP, API...).
4. Uma comparação do cotidiano antes da definição formal.
5. As citações e as etiquetas de confiança (*registrado na documentação*, *proposta didática*...) saem do meio do texto e vão para **"Notas de fonte"** no fim da unidade. Nada se perde: cada afirmação continua rastreável. O texto principal fica limpo.
6. Os links e a estrutura da unidade (objetivo, conceito, como funciona, exemplo, cuidados, pergunta, retomada, fontes) não mudam.

---

## 1.1 O que é um modelo de linguagem e como ele responde?

### Objetivo
Ao final desta unidade, você explica com suas palavras o que um modelo de linguagem faz. E separa duas coisas: o que o modelo faz e o que o sistema em volta dele faz.

### Conceito
Vamos começar com um jogo. Complete a frase:

“Para trocar uma lâmpada, primeiro desligue a …”

Você pensou em “energia” ou “chave”. Quase ninguém pensa em “geladeira”. Sem perceber, você fez o que um modelo de linguagem faz: olhou o começo de um texto e adivinhou o que provavelmente vem depois.

Um **modelo de linguagem** é um programa que faz exatamente isso. Ele recebe o começo de um texto e calcula a chance de cada continuação possível. Depois de “desligue a”, “energia” tem uma chance alta. “Geladeira” tem uma chance quase zero.

Uma observação sobre “palavra”. O modelo não lê palavras inteiras. Ele lê pedaços de texto, chamados **tokens**. Um token pode ser uma palavra, um pedaço de palavra ou uma só letra. Por enquanto, pense em token como “pedaço de texto”. A unidade 1.3 explica melhor.

Agora, alguns nomes que vamos usar o tempo todo:

- **LLM** é a sigla, em inglês, de *large language model*, ou “modelo de linguagem de grande porte”. É um modelo de linguagem muito grande. Os assistentes de conversa que você conhece usam LLMs.
- **Prompt** é o texto que você dá ao modelo para ele continuar. Pode ser uma pergunta, uma instrução ou o começo de uma frase.
- **Inferência** é o momento em que o modelo, já pronto, recebe um prompt e escreve a resposta. É o “uso” do modelo. A unidade 1.2 mostra a diferença entre usar o modelo e treiná-lo.

Mais dois nomes, bem amplos:

- **Inteligência artificial (IA)** é o nome geral para programas que fazem tarefas ligadas à linguagem, à imagem ou ao raciocínio.
- **Aprendizado de máquina** é quando ninguém escreve cada regra do programa. Em vez disso, o programa é ajustado com muitos exemplos.

O último nome organiza o livro todo. O modelo, sozinho, só escreve texto. Em volta dele existe um **sistema** que faz o resto: monta o prompt, guarda a conversa, oferece ferramentas, confere quem pode ver o quê, anota o que aconteceu e confere a resposta antes de usá-la. Em inglês, esse sistema em volta se chama **harness**. Neste livro, vamos dizer “sistema em volta do modelo”. O modelo escreve o texto. O sistema decide o que fazer com ele.

Um cuidado com as palavras. Dizemos que o modelo “aprende”, “esquece” e “entende”. São jeitos de falar. O modelo não tem vontade nem intenção, como uma pessoa. Neste livro, evitamos os verbos “entender” e “pretender” para falar do modelo.

### Como funciona
Para escrever uma resposta, o modelo repete um ciclo curto:

1. Ele recebe o prompt.
2. Ele calcula a chance de cada continuação possível.
3. Ele escolhe uma delas. Como ele escolhe é assunto da unidade 1.4.
4. Ele coloca o pedaço escolhido no fim do texto. O ciclo recomeça e só para quando a resposta termina.

Esse resumo é uma simplificação, feita para esta unidade.

Repare no que falta. O modelo só escreve texto. Lembrar a conversa, consultar um sistema, bloquear uma ação e calcular um valor certo não são trabalho dele. São trabalho do sistema em volta. O fluxo abaixo mostra quem faz o quê.

**Fluxo simplificado de um pedido**

1. **Pessoa:** faz um pedido.
2. **Sistema em volta:** descobre quem está pedindo e monta o prompt com as instruções, a conversa até ali e as fontes que podem ser usadas.
3. **Modelo:** escreve a resposta.
4. **Sistema em volta:** confere o resultado, registra e só então mostra ou executa o que for permitido.
5. **Pessoa:** lê a resposta e decide o que fazer.

### Exemplo resolvido
**Parte 1 — o jogo da próxima palavra.** Veja esta frase inventada: “A reunião de planejamento foi remarcada para amanhã às …”. A tabela mostra como um modelo poderia avaliar três continuações. Os números são inventados, só para ilustrar. Um modelo de verdade dá uma nota a todas as continuações possíveis, e as notas somam 100%.

| Continuação | Chance (inventada) |
|---|---|
| “dez” | alta (por exemplo, 40%) |
| “nove” | média (por exemplo, 25%) |
| “azul” | muito baixa (menos de 1%) |

O mesmo jogo aparece no livro de Jurafsky e Martin. Para “so long and thanks for” (“tchau e obrigado por”), “all” e “everything” são prováveis, e “of” ou “wasn’t” são improváveis. Note o que o modelo **não** faz: ele não procura a resposta numa lista pronta. Ele calcula a chance de cada continuação e escreve o texto passo a passo.

**Parte 2 — o AP AI Router.** O Router junta várias peças: regras de trabalho, procedimentos que podem ser reaproveitados, um painel de conversa, o envio de pedidos a modelos de empresas e um modelo que roda no próprio computador. Quando o modelo local é usado para programar, ele escreve uma proposta de código, em texto, e mais nada. Aplicar e testar essa proposta não acontece sozinho na conversa com o modelo local. A divisão é a do fluxo acima: o modelo escreve a proposta, e o sistema em volta e a revisão decidem o que fazer com ela.

**Parte 3 — um assistente financeiro inventado.** Imagine que alguém do financeiro pergunte: “Quanto falta pagar da parcela deste aluno?”. Os dados e as funções desse exemplo são fictícios. Primeiro, o sistema descobre quem está perguntando e confere se essa pessoa pode ver aquele cadastro. Depois, o sistema busca a parcela e faz a conta do valor em aberto. Só no fim o modelo recebe os dados prontos e escreve a resposta em linguagem clara. A regra por trás disso: cobrança, preço, situação do cadastro e permissão não devem depender de um palpite do modelo, quando o sistema já consegue aplicar a regra com certeza.

### Cuidados e limites
Use a divisão como primeira pergunta de qualquer projeto: **esta tarefa é de linguagem, que o modelo pode fazer, ou é uma regra, que o sistema deve cumprir?** Quatro ideias erradas atrapalham essa pergunta:

- **“O modelo consulta uma base de respostas.”** Não. Ele calcula chances e escreve o texto passo a passo.
- **“O modelo entende como uma pessoa.”** “Entender” é um atalho que engana. Veja o cuidado com as palavras, acima.
- **“O modelo sabe o que aconteceu hoje.”** Não necessariamente. A unidade 1.2 mostra de onde vem o que o modelo sabe e por que isso tem uma data.
- **“Modelo e aplicativo de chat são a mesma coisa.”** Não. O aplicativo de chat é o modelo mais o sistema em volta.

Esta unidade não explica como o modelo foi construído nem como ele escolhe cada continuação. Isso vem nas unidades 1.2 a 1.5. Os fluxos são simplificados e não descrevem um sistema real por inteiro.

### Uma pergunta
Num assistente que responde dúvidas dos colaboradores, o que faz o modelo e o que faz o sistema em volta? Pense na resposta antes de abrir o retorno.

> **Retorno:** O modelo recebe o prompt e escreve a resposta. O sistema em volta descobre quem está perguntando, decide o que essa pessoa pode ver, monta o prompt com as fontes certas, guarda a conversa e confere o que sai antes de mostrar ou executar. Se a sua resposta pôs identidade, permissão ou conta dentro do modelo, releia o Conceito: o modelo só escreve texto.

### Ponto de retomada
Um modelo de linguagem calcula a chance de cada continuação de um texto e escreve a resposta pedaço por pedaço. Todo o resto é trabalho do sistema em volta: lembrar a conversa, cumprir regras, conferir permissões e agir. Na unidade 1.2, vamos ver como o modelo foi preparado (treinamento) e o que muda quando só o usamos (inferência).

### Notas de fonte
Cada nota liga uma afirmação do texto à sua fonte e ao grau de confiança, como no guia atual.

- **Definição de modelo de linguagem, jogo da próxima palavra e exemplo “so long and thanks for”:** Jurafsky e Martin, *Speech and Language Processing*, 3ª ed., rascunho de 19/08/2026, §1.1.
- **Prompt e inferência:** Jurafsky e Martin, §1.7.
- **Cuidado com “aprender”, “esquecer”, “entender” e “pretender”:** Jurafsky e Martin, §1.11.
- **Tokens:** definidos na unidade 1.3; aqui, só como “pedaço de texto”.
- **Definições de IA e de aprendizado de máquina:** definições de trabalho do livro (*proposta didática*), não citações.
- **Harness (sistema em volta do modelo):** *registrado na documentação* de estudo do AP AI Router, que trata esse sistema de execução como harness.
- **Ciclo de quatro passos e fluxo do pedido:** simplificações montadas para esta unidade (*proposta didática*).
- **Router:** peças e uso do modelo local *registrados na documentação* de estudo. A documentação registra que aplicar e testar a proposta não acontece automaticamente pela chamada local do chat.
- **Assistente financeiro:** situação inventada (*proposta didática*). O princípio de que cobrança, preço, status e permissão não dependem de interpretação probabilística, quando o sistema já pode aplicá-los de forma determinística, está *registrado na documentação* de estudo da Nanda Mac.

### Fontes da unidade
- **Ler:** Jurafsky e Martin, *Speech and Language Processing*, 3ª ed., rascunho de 19/08/2026, cap. 1, §1.1, §1.2, §1.7 e §1.11 — web.stanford.edu/~jurafsky/slp3/1.pdf
- **Assistir:** Karpathy, *Deep Dive into LLMs like ChatGPT* (05/02/2025; 3 h 31 min), capítulo “introduction” (00:00) — youtube.com/watch?v=7xTGNNLPyMI
- **Aprofundar:** Google, *Machine Learning Crash Course*, módulo de modelos de linguagem, consultado em 13/10/2026 — developers.google.com/machine-learning/crash-course/llm

claude - pessoal, 15/10/2026
