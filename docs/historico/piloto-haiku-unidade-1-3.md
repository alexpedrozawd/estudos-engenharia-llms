# Piloto Haiku 5.5 High — Unidade 1.3 (Tokens e contexto)

Data: 15/10/2026. Autoria: claude - ap (Haiku 5.5 High, piloto do Bloco 4b). Não altera o guia. Base: pacotes-de-fontes-capitulo-1.md e molde da unidade 1.1. Os identificadores entre colchetes (ex.: [1.3-T2]) indicam o trecho do pacote usado em cada afirmação.

Aviso: a versão final da 1.3, feita pelo Sonnet, estava no contexto desta sessão antes do piloto. A comparação não é cega.

## Objetivo

Ao final desta unidade, você explica que o modelo trabalha com tokens, e não com letras ou palavras; trata a janela de contexto como um orçamento que inclui tudo o que entra e tudo o que sai numa chamada; e sabe que a contagem exata depende do tokenizador do modelo.

## Conceito

Na unidade 1.1, usamos "token" como "pedaço de texto". Agora, a definição. A tokenização é o processo de segmentar o texto de entrada em tokens (Jurafsky e Martin, rascunho de 19/08/2026, cap. 2, §2.4) [1.3-T2]. O método descrito no livro é guiado pelos dados: os tokens costumam ter o tamanho de morfemas ou de palavras e, às vezes, o de um caractere [1.3-T6]. Essa técnica chama-se tokenização por subpalavras, e um dos métodos é o BPE (*byte-pair encoding*).

Quem faz a divisão é o tokenizador. O conjunto de tokens que ele reconhece é o vocabulário. Como o vocabulário vem dos dados, cada tokenizador tem o seu. A contagem exata só sai do tokenizador do modelo que você usa. A documentação da Anthropic indica a API de contagem de tokens para estimar o uso antes de enviar mensagens (página "Context windows", consultada em 13/10/2026) [1.3-T12].

A tokenização também depende do idioma: o número de caracteres por token muda de um idioma para outro (Google, *Machine Learning Crash Course*, módulo LLM, consultado em 13/10/2026) [1.3-T3]. Por isso, "caracteres divididos por quatro" é, no máximo, uma estimativa.

Modelos de chat esperam uma estrutura. A documentação da Hugging Face diz que um modelo de chat recebe a entrada num *chat template*, com papel e conteúdo, e que passar o prompt como uma única string nem sempre dá o resultado esperado. Ela descreve a biblioteca Transformers, não os provedores de API [1.3-T7] [1.3-T14].

A janela de contexto é todo o texto que o modelo pode referenciar ao gerar uma resposta, inclusive a própria resposta (Anthropic, "Context windows") [1.3-T10]. Ela funciona como uma memória de trabalho e não se confunde com os dados em que o modelo foi treinado [1.3-T11].

Entram na janela o prompt de sistema, as mensagens, inclusive resultados de ferramentas, imagens e documentos, e as definições de ferramentas [1.3-T1]. Entra também a saída gerada naquela vez, com o raciocínio estendido, se houver [1.3-T4]. A janela é um orçamento: entrada e saída dividem o mesmo espaço.

Espaço sobrando não garante resultado melhor. Mais contexto não é automaticamente melhor: conforme o número de tokens cresce, a precisão e a lembrança diminuem. A Anthropic chama esse efeito de *context rot* [1.3-T5].

## Funcionamento

Primeiro, a divisão em tokens. A palavra "reembolsável" poderia ser dividida em "re", "embols" e "ável". Essa divisão é ilustrativa (proposta didática): um tokenizador real pode dividir de outro modo, e nenhum tokenizador foi executado para este livro.

Segundo, o orçamento. A tabela mostra uma chamada fictícia com histórico e uma ferramenta. Os valores são inventados (proposta didática).

| Componente | Tokens |
|---|---|
| Instruções do sistema | 1.000 |
| Histórico da conversa | 3.000 |
| Documento anexado | 2.500 |
| Definições de ferramentas | 800 |
| Reserva para a resposta | 1.200 |
| Total | 8.500 |
| Folga na janela de 10.000 | 1.500 |

Se a pessoa anexar mais um documento de 2.000 tokens, o total passa de 10.000. Será preciso reduzir o histórico, o documento ou a reserva. Uma reserva menor pode cortar a resposta no meio, o que é assunto da unidade 1.4.

## Exemplo resolvido

**Cenário fictício (proposta didática).** Uma equipe quer que o assistente resuma um contrato. O contrato tem anexos sem relação com a pergunta. Pela tabela, o total cabe na janela, com folga. Mas convém enviar tudo? Os anexos consomem orçamento e, pelo que vimos, mais contexto não é melhor. A conduta mais sensata é recuperar apenas as cláusulas pertinentes e preservar a origem de cada uma.

As diretrizes locais descrevem esse problema como antipadrão, o *entupimento de contexto*: enviar arquivos inteiros sem necessidade só porque a janela comporta. A solução registrada é recuperar fontes pertinentes e preservar origem e requisitos antes de compactar. Também não se deve substituir o excesso por cortes cegos (docs/09-antipadroes-e-boas-praticas-llm.md, §3, antipadrão 4; diretrizes locais, consultadas em 13/10/2026) [1.3-T8] [1.3-T9].

**No Router.** O contexto de uma chamada inclui instruções, exemplos, histórico, fontes, contratos, definições e resultados de ferramentas [1.3-C1]. Para o modelo local, a janela é estimada a partir do envelope do pedido e da reserva de saída, com um teto declarado no código. Caracteres são uma estimativa, não contagem exata de tokens nem prova de capacidade disponível [1.3-C4] [1.3-C2] (registrado na documentação de estudo do Router).

**Na Nanda Mac.** Descrições de ferramentas, schemas e resultados também consomem contexto. Selecionar fontes e ferramentas por etapa faz parte da arquitetura (registrado na documentação de estudo da Nanda Mac) [1.3-C3].

## Aplicação e limites

Quatro equívocos comuns:

- **"Token é uma palavra."** Não: é um pedaço de texto. Pode ser uma palavra, parte dela ou um caractere.
- **"Janela grande significa pôr tudo."** Cabe não significa convém. Mais contexto pode reduzir a precisão.
- **"Caracteres divididos por quatro é exato."** É uma estimativa, e a razão muda com o idioma e o tokenizador.
- **"Contexto é memória permanente."** A janela é a memória de trabalho de uma chamada. O que o sistema não reenviar não está lá.

Esta unidade não executa tokenizador nem dá números válidos para um modelo específico. Contagem de tokens e parâmetros são assunto do módulo 4; histórico e memória, do módulo 8.

## Uma pergunta

O que ocupa a janela numa chamada com histórico e uma ferramenta? E por que "cabe" não significa "convém"? Responda antes de abrir o feedback.

<details class="feedback">
<summary>Ver feedback</summary>
<p>Ocupam a janela o prompt de sistema, o histórico, o documento, as definições da ferramenta, o resultado dela e a resposta que o modelo vai gerar. "Cabe" diz só que o total não passa do limite. "Convém" pergunta se tudo isso é necessário, porque mais contexto não é automaticamente melhor e a precisão pode cair conforme o número de tokens cresce.</p>
</details>

## Ponto de retomada

O modelo trabalha com tokens. A janela de contexto é um orçamento que cobre entrada e saída. A contagem exata depende do tokenizador, e mais contexto não garante melhor resultado. Na unidade 1.4, veremos como o modelo gera a resposta dentro desse orçamento.

## Fontes da unidade

**Ler:** Jurafsky e Martin, cap. 2, §2.4 (rascunho de 19/08/2026); Anthropic, *Context windows*, consultada em 13/10/2026.

**Assistir:** Karpathy, *Let's build the GPT Tokenizer* (publicado em 20/02/2024; 2 h 13 min) — youtube.com/watch?v=zduSFxRajkE. Não assisti; os dados vêm dos metadados.

**Aprofundar:** Hugging Face, *Text generation* (chat template e tokens especiais); slides do Stanford CS336 sobre tokenização (não lidos).
