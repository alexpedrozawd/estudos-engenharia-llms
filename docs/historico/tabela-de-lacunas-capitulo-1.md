# Tabela de lacunas do capítulo 1

Data: 13/11/2026. Autoria: claude - pessoal. Base: texto do HTML de 15/10/2026 (hash `6136c61124752bf0`), plano de 13/11 e fontes da 1.7 lidas hoje. Onde o plano diz "o operador decide o que entra", a decisão abaixo é minha, pelos critérios do plano: só entra o que tem fonte lida, cabe nos tópicos do capítulo e não repete capítulo futuro. **Você pode vetar qualquer linha da coluna "Decisão".**

| Unidade | O que o texto diz | O que falta | Decisão | Fonte |
|---|---|---|---|---|
| 1.1 Modelo de linguagem | Modelo calcula a chance da continuação; token, LLM, prompt, inferência; modelo x sistema em volta | Modelos que não escrevem texto ou que não são só de texto | Entra só um ponteiro para a 1.7. "Agente" fica para o capítulo 11 | Jurafsky e Martin §1.1, §1.7 |
| 1.2 Treinamento e inferência | Pesos; treino x inferência; 4 etapas; data de corte; mistura de especialistas; LoRA; pesos abertos x proprietários | Tipos de modelo (acesso, treino, tamanho) espalhados em um parágrafo | O parágrafo "Dois tipos de modelo" vai para a 1.7a, com ponteiro na 1.2. Mistura de especialistas e LoRA ficam na 1.2; a 1.7c retoma a mistura. Destilação e leis de escala ficam de fora: sem fonte lida | Plano §4; OSI 1.0 |
| 1.3 Tokens e contexto | Subpalavras, BPE; janela como orçamento; *context rot* | Contagem real por provedor; tokens de imagem e áudio | Nada novo. Contagem vai para o capítulo 4; gestão de contexto para o 8 | Anthropic, *Context windows* |
| 1.4 Geração | Laço; escolha gulosa, sorteio, temperatura; raciocínio | Parâmetros e saída estruturada dos provedores; geração que não é token a token | Parâmetros ficam para o capítulo 4. Difusão e modelos de decisão entram na 1.7 | Jurafsky e Martin §7.6; Mercury, LLaDA |
| 1.5 Atenção e Transformers | Atenção, camadas, custo quadrático; menção a KV cache e PagedAttention | Arquiteturas sem a atenção padrão | Mamba entra na 1.7c como menção curta. KV cache em detalhe fica para o capítulo 12 | Gu e Dao, 01/12/2023 |
| 1.6 Capacidades e limitações | Onde o LLM ajuda; limites; controles proporcionais | Escolher o tipo certo de modelo para cada tarefa | Ponteiro para a 1.7. Uso prático de decisão, *embeddings* e *rerankers* fica para os capítulos 5, 10 e 13 | Plano §4 |
| **1.7 Tipos de modelos (nova)** | — | Tudo | 3 partes: 1.7a acesso e função; 1.7b treino e dados; 1.7c arquitetura, tamanho e além do texto. Cada afirmação usa só fonte lida em 13/11/2026 | Lista abaixo |
| Questões do capítulo | 5 questões | Nenhuma sobre tipos de modelo | Entra 1 questão nova (6ª, nível médio). O requisito de "5 por módulo" passa a "5 ou 6" | Plano §4 |

## Fontes da 1.7 e como entram
- **Decisão:** Thoughtworks Radar, 04/11/2026 (anel *Assess*); Simon Willison, 21/09/2026; TypeSafe (post de 15/09/2026); InfoQ, 01/10/2026. Entra a definição (saída em valores predefinidos, não em texto) e a crítica de que o valor pode ser válido e errado. Números de velocidade e custo ficam de fora (são da empresa; a análise independente que a InfoQ cita não é fonte primária).
- **Kev:** repositório, Apache-2.0, Kev 1.0 (0,8B, 4B, 9B, 27B), LoRA mais uma cabeça pequena sobre um modelo Qwen. Entra como exemplo de modelo de decisão que se treina e roda sozinho, com os limites declarados pelos autores. Sem data de lançamento.
- **Instruído, raciocínio, guarda, SLM, difusão, Mamba:** Ouyang (04/03/2022); DeepSeek-R1; Llama Guard (07/12/2023); Belcak et al. (02/06/2025, artigo de posição); LLaDA (14/02/2025); Mercury (17/06/2025, números são dos autores); Mamba (01/12/2023).
- ***Embeddings* e *reranker*:** Sentence-BERT (27/08/2019); MTEB (13/10/2022); Passage Re-ranking with BERT (13/01/2019).
- **Além do texto:** π0 (31/10/2024); Gemini Robotics 2 (30/07/2026; acesso restrito a parceiros, números da empresa); Genie 3 (05/08/2025; limites declarados pela página).
- **"Aberto":** Open Source AI Definition 1.0 (OSI). A página mostra só "versão 1.0", sem data. Entra sem data.

## Fora do guia por falta de fonte primária
Microsoft Decision-1; "DiffusionGemma"; valores e datas de AMI Labs e World Labs; Mercury 3; fonte de modelos de mundo além do Genie 3.

## Lacunas que continuam abertas
Data do OSAID 1.0; data de lançamento do Kev; fonte primária de modelos de mundo além do Genie 3. Cada uma aparece no texto como "sem data confirmada" ou fica de fora.

## Registro das minhas decisões (para veto)
1. Mistura de especialistas e LoRA ficam na 1.2 (a 1.7c retoma a mistura).
2. Destilação e leis de escala não entram.
3. Mamba entra só como menção.
4. Questão nova vira a 6ª do capítulo 1.
5. Imagens: só moldura com texto alternativo até o texto ficar pronto e validado; depois, poucas imagens (regra do operador, 13/11/2026).

claude - pessoal, 13/11/2026

## Aplicação em 13/11/2026

- Todas as decisões acima foram aplicadas ao HTML: 23 partes, unidade 1.7 em três partes, ponteiros para o capítulo 11 e para os capítulos 5, 10 e 13, e a sexta questão.
- Ficaram de fora, como decidido: destilação, leis de escala, números de velocidade e custo das empresas e as fontes sem leitura.
- Imagens: seis molduras com texto alternativo (1.1a, 1.2b, 1.3b, 1.4b, 1.6b, 1.7a); nenhuma imagem gerada entrou.
- O operador pode vetar qualquer linha depois de ler o capítulo novo.

Assinatura da aplicação: deepseek - conta não verificada.
