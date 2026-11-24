# Planejamento do Capítulo 5 — Avaliação e experimentação

Data: 16/11/2026. Autoria: claude - pessoal (Sonnet 5.5 High, painel). Etapa: **somente planejamento**; nada redigido no guia, nenhuma fonte baixada ou conferida por trecho. Depende de aprovação do operador antes do Bloco 1.

Base: [plano mestre](planejamento-completo-estudos-engenharia-llms.md) (módulo 5), [plano do Capítulo 4](planejamento-capitulo-4-prompts-parametros-e-respostas.md) (molde), [requisitos de formato](requisitos-de-formato-html-do-material.md) (§8 e §9), [protocolo de economia de tokens](protocolo-de-economia-de-tokens-entre-sessoes.md), handoff do capítulo 4 (`arquivo/handoff-capitulo-4-concluido-2026-11-14.md`, arquivado localmente fora do Git). Herda o método dos capítulos 2 a 4 (partes curtas, pacote de fontes, pausa após a primeira unidade).

## 1. Objetivo, escopo e aceite

**Objetivo:** ao concluir o capítulo, o estudante transforma o critério de aceite do capítulo 3 e o prompt do capítulo 4 em uma medição repetível: define o que é "resultado adequado", reúne casos reais e falhas, fixa uma referência inicial, escolhe quem confere (código, modelo ou pessoa), vigia regressões e só declara "melhorou" quando a comparação é confiável.

**Escopo:** abertura, seis unidades em partes curtas, seis questões, glossário e referências. Progressão fixada no plano mestre: resultado adequado → exemplos e falhas → referência inicial → testes e avaliações → regressões → comparações confiáveis.

**Fora do escopo (só menção, com ponte):** injeção de prompt e testes adversariais de segurança (módulo 6); proporcionalidade e custo total da avaliação (módulo 7); avaliação de recuperação e de resposta com fontes (módulo 10); avaliação de agentes com ferramentas e ciclos (módulo 11); comparar e escolher modelo para uma rota (módulo 13); operação, monitoramento e observabilidade em produção (módulo 14); custo e cache (módulo 15). Sem programar: o guia descreve o desenho da avaliação, não escreve o código dela.

**Promessas do capítulo 4 que o 5 deve cumprir:**
1. comparar v1 (4.1c) e v2 (4.2d) do prompt sobre os mesmos casos, com critério escrito de acerto;
2. medir se pedir passos intermediários ajuda (a coluna "provavelmente" da 4.2b);
3. escolher parâmetros por medição, não por tabela (4.5c).
Também a distinção já posta na 3.4c: o **aceite** autoriza a entrada; a **avaliação contínua** diz se ele continua verdadeiro após cada mudança de modelo, texto ou fonte.

**Aceite:**
- partes de 400 a 500 palavras (meta; ver pendência 2 do handoff sobre partes acima disso), no molde do §8: resumo "Em 3 linhas", moldura de imagem opcional, analogia, texto, uma pergunta, ponto de retomada, notas de fonte, navegação; a última parte de cada unidade traz *Ler* e *Aprofundar*;
- nenhum trecho de programa; casos, rubricas e tabelas de resultado em tabela ou `figure.bloco-codigo` com `data-executavel="false"` (até 12 linhas);
- toda afirmação sobre método com fonte primária e trecho literal conferido; sem trecho = *proposta didática*;
- toda afirmação sobre parâmetro leva provedor, versão da API e data; no caso da Anthropic (versão 2026-10-21), `temperature`, `top_p` e `top_k` são rejeitados e o parâmetro medido é o esforço (`output_config.effort`), que não equivale à temperatura; nada generalizado para outros provedores;
- números só quando medidos e datados; todo número de exemplo da Aurora marcado *ilustrativo, não medido*;
- exemplos sem nomes internos (Aurora Educação, plataforma interna de IA genérica);
- seis questões (duas fáceis, três médias, uma difícil), gabarito sem padrão regular e diferente dos capítulos 1 a 4;
- `validar-guia.py` sem falha; PDF A4 sem bloco dividido; Chrome de 320 a 1920 px sem rolagem horizontal (esta última validação segue pendente por natureza).

## 2. Decisões de desenho

1. **Nível:** quem leu os capítulos 1 a 4. Entrada: especificação (cap. 3) e prompt (cap. 4). Saída: um conjunto de casos, uma rubrica e uma regra de decisão.
2. **Eixo:** avaliar é comparar o resultado com um critério escrito, sobre casos conhecidos, e repetir. Impressão não é medida; uma execução não é medida.
3. **Caso principal:** o assistente de matrícula da Aurora, com as versões v1 (4.1c) e v2 (4.2d) do capítulo 4. Aparece no fechamento de cada unidade. Duas cenas curtas de outro contexto: extração de campos de formulário (conferível por código) e redação de comunicado (conferível só por pessoa ou rubrica).
4. **Partes curtas:** 20 partes, 3/3/3/4/3/4. A 5.4 tem quatro por tratar dos três tipos de avaliador; a 5.6 tem quatro por fechar variação, tamanho de amostra, comparação e o caso.
5. **Uma tabela por parte, no máximo.** Rubrica, tabela de casos, comparação antes/depois.
6. **Números de exemplo:** tabelas de resultado usam valores pequenos e explicitamente fictícios, para ensinar a ler (por exemplo, 14 de 20), sem sugerir taxa real de modelo algum.
7. **Qualificadores mantidos:** *registrado na documentação*, *registrado na fonte*, *verificado no código local*, *proposta didática*.
8. **Ids:** `capitulo-5`, `unidade-5-1a` a `unidade-5-6d`, `questoes-capitulo-5`, `c5q1` a `c5q6`; o sumário passa a apontar para `#unidade-5-1a`. Remissões futuras: "módulo N".
9. **Links externos** em nova guia (`target="_blank" rel="noopener noreferrer"`).
10. **Imagens:** poucas. Proposta de três molduras (5.1a, 5.4a, 5.6b), só `role="img"` + `aria-label` até o texto estar aprovado. Geração na última etapa, com autorização.
11. **Ponte com o capítulo 4:** a 5.6d fecha as três promessas acima; nenhuma unidade reexplica prompt, parâmetro ou schema.

## 3. Fontes (nenhuma conferida por trecho; Bloco 1)

| Fonte | Papel | Estado |
|---|---|---|
| Anthropic, *Demystifying evals for AI agents* (engineering, 09/01/2026; `anthropic.com/engineering/demystifying-evals-for-ai-agents`) | Casos tirados de falhas reais, 20 a 50 tarefas para começar, avaliadores por código, por modelo e por pessoa, avaliar o resultado e não o caminho | Existência confirmada hoje por busca; texto integral não lido. A ler e extrair trechos |
| Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (arXiv:2306.05685, 2023) | Juiz-LLM e seus vieses (posição, tamanho, autopreferência) | A ler; conferir o número "mais de 80%" no texto, não no resumo de segunda mão |
| Anthropic, documentação de critérios de sucesso e avaliações (página a localizar) | Critério específico e mensurável; tipos de avaliação; método prático | A localizar e ler |
| Estatística de comparação entre modelos: candidato Miller, *Adding Error Bars to Evals* (arXiv:2411.00640, 2024) | Incerteza em resultados de avaliação, comparação pareada | **Candidato recordado, não verificado.** Confirmar título, autoria e trecho antes de usar; se não confirmar, usar só a explicação da fonte da Anthropic e marcar *proposta didática* |
| Viés de posição em juiz-LLM: candidato Wang et al., *Large Language Models are not Fair Evaluators* (arXiv:2305.17926, 2023) | Trocar a ordem das respostas muda o veredito | **Candidato recordado, não verificado.** Mesma regra |
| OpenAI, guia de avaliações (página a localizar) | Segunda implementação do mesmo método; terminologia | A localizar; opcional |
| Capítulos 3 e 4 do guia; pacote de fontes do capítulo 4 | Aceite, v1/v2, promessas ao módulo 5, números de tokens já conferidos | Já no projeto |
| `docs/09` do Router (interna) | Antipadrão: dizer "melhorou" sem medir; prompt patching | Fonte interna, sem link público |

Evidência local (leitura, lista fechada, sem execução): se a plataforma interna de IA documentar um conjunto de casos ou revisão com teste, serve de exemplo de contrato existente; sem isso, só a Aurora (situação construída, *proposta didática*, sem pessoas, dados de clientes ou fornecedores). Nenhuma chamada real a modelo, nenhuma chave lida, nenhuma avaliação executada.

## 4. Mapa por unidade

### 5.1 Resultado adequado (3 partes)
- **Competência:** transformar "ficou bom" em critério observável, com dono e limite; separar correto, aceitável e perigoso.
- **Partes:** *5.1a Bom para quem?* — adequado depende de usuário e uso; retomada do aceite (3.4c). *5.1b Critério escrito* — o que se verifica, quem declara, o que reprova; custo e tempo de resposta também entram como critério ("acertou, mas custou quanto?"), com ponte para os módulos 7 e 15. *5.1c O critério do assistente de matrícula* — três a cinco critérios verificáveis; o que ainda não dá para medir.
- **Conceitos:** resultado adequado, critério, rubrica, reprovação automática.
- **Equívocos:** "se eu leio e gosto, está bom"; "acerto total é meta".
- **Ponte:** 3.4c (aceite) e 5.2.

### 5.2 Exemplos e falhas (3 partes)
- **Competência:** montar um conjunto de casos a partir de uso e de falhas reais; incluir caso normal, de borda, de recusa e de falha.
- **Partes:** *5.2a De onde vêm os casos* — falhas observadas, pedidos reais, casos de recusa; começar pequeno (a fonte da Anthropic fala em 20 a 50 tarefas; conferir o trecho). *5.2b Caso bem escrito* — entrada, contexto, resultado esperado, motivo; caso ambíguo vira decisão, não palpite. *5.2c Casos do assistente* — 12 a 20 casos fictícios cobrindo matrícula, recusa e dado pessoal (ilustrativo).
- **Conceitos:** caso de teste, conjunto de casos, caso de borda, caso de recusa.
- **Equívocos:** "casos inventados por quem escreveu o prompt bastam"; "quanto mais casos, melhor, sem olhar a variedade".
- **Ponte:** 3.4b (casos de falha e recusa) e 5.3; dados pessoais reais nos casos, módulo 6.

### 5.3 Referência inicial (3 partes)
- **Competência:** medir o ponto de partida antes de mexer; saber o que a medida inicial não prova.
- **Partes:** *5.3a Sem linha de base não há melhora* — medir a v1 antes de criar a v2. *5.3b Referência simples* — respostas de pessoa, regra fixa ou sistema atual como comparação; o que cada uma representa. Benchmark público não substitui a avaliação própria: mede outra tarefa, com outros dados (*proposta didática* até haver fonte lida). *5.3c A v1 medida* — leitura de uma tabela fictícia, com margem de erro dita em palavras.
- **Conceitos:** linha de base, referência, valor de partida.
- **Equívocos:** "comparar com o modelo mais forte é a única referência"; "a v1 é fraca, não precisa medir".
- **Ponte:** 5.6 (comparação) e 13 (escolha de modelo).

### 5.4 Testes e avaliações (4 partes)
- **Competência:** escolher o avaliador certo por tipo de critério e saber o limite de cada um.
- **Partes:** *5.4a Três avaliadores* — código, modelo, pessoa: o que cada um confere bem e mal. *5.4b Conferir com regra* — formato, campo, número, lista proibida; barato e repetível (ponte com a validação do 4.6). *5.4c Modelo como juiz* — rubrica, vieses de posição, tamanho e autopreferência; calibrar contra pessoa antes de confiar. *5.4d Pessoa e amostra* — quando vale o custo; instrução de revisão, concordância entre revisores; fechamento com o assistente.
- **Conceitos:** avaliador, juiz-LLM, rubrica, calibração, concordância.
- **Equívocos:** "juiz-LLM dispensa pessoa"; "o mesmo modelo avalia a si mesmo sem viés"; "avaliar o caminho do modelo em vez do resultado".
- **Ponte:** 6 (avaliações de segurança), 10 e 11 (avaliar recuperação e agente).

### 5.5 Regressões (3 partes)
- **Competência:** perceber que uma melhora em um ponto pode piorar outro, e montar uma rotina de reexecução.
- **Partes:** *5.5a O que é regressão* — mudança de prompt, de modelo, de parâmetro ou de fonte que quebra o que funcionava. *5.5b Conjunto de regressão* — casos que já falharam e foram corrigidos viram teste permanente; capacidade (o que ainda não faz) contra regressão (o que já fazia). *5.5c Quando rodar e o que fazer ao falhar* — gatilhos de reexecução, bloqueio de mudança, registro; sem prometer monitoramento de produção (módulo 14).
- **Conceitos:** regressão, conjunto de regressão, gatilho de reexecução.
- **Equívocos:** "se melhorou na média, não regrediu"; "avaliar uma vez, no início, basta".
- **Ponte:** 3.4c (aceite contínuo), 13 (troca de modelo) e 14 (operação).

### 5.6 Comparações confiáveis (4 partes)
- **Competência:** decidir "A é melhor que B" sem se enganar por sorte, variação ou viés.
- **Partes:** *5.6a Variação da resposta* — repetir o mesmo caso dá resultados diferentes; acertar uma vez é diferente de acertar sempre, e o critério precisa dizer qual se exige (sem afirmar que temperatura resolve: ver 4.5; métricas de repetição só com fonte lida). *5.6b Quanto dá para concluir* — tamanho de amostra e incerteza em linguagem simples; "14 de 20 contra 16 de 20" não decide. *5.6c Comparar do jeito certo* — mesmos casos, mesmas condições, uma mudança por vez, ordem sorteada, critério escrito antes. Casos de ajuste e casos reservados: o que se usou para melhorar o prompt não serve para provar que melhorou; separar um conjunto que ninguém olhou durante o ajuste. *5.6d As promessas do capítulo 4 cumpridas* — v1 contra v2, passos intermediários com e sem, parâmetro escolhido por medição; decisão registrada com versão, data e motivo. O "parâmetro" medido é o esforço (`effort`), com provedor, versão da API e data.
- **Conceitos:** variação, amostra, incerteza, comparação pareada, uma variável por vez, conjunto de ajuste, conjunto reservado.
- **Equívocos:** "uma rodada basta"; "mudar prompt e modelo juntos e comparar"; "diferença pequena é vitória"; "ajustei o prompt vendo os casos e ele acertou todos, logo melhorou".
- **Ponte:** 13 (seleção), 15 (custo por acerto), 7 (custo total da avaliação).

## 5. Matriz das seis questões (4 alternativas, 1 correta, primeira resposta trava)

| # | Nível | Unidade | Situação e foco | Distratores |
|---|---|---|---|---|
| Q1 | Fácil | 5.1 | "A resposta ficou boa" como único critério de aceite | pedir opinião a mais gente; trocar de modelo; aceitar se ninguém reclamar |
| Q2 | Fácil | 5.2 | Conjunto de casos só com perguntas que o assistente acerta | aumentar a quantidade igual; remover casos difíceis; usar só casos inventados pelo autor do prompt |
| Q3 | Média | 5.3 | v2 aprovada sem medir a v1 | comparar com impressão; medir só a v2; confiar no modelo maior |
| Q4 | Média | 5.4 | Juiz-LLM escolhe sempre a primeira resposta mostrada | trocar de juiz sem checar; confiar na média; pedir "seja imparcial" |
| Q5 | Média | 5.5 | Prompt corrigido para um caso piora outros dois | aceitar a troca; descartar os dois; avaliar só o caso novo |
| Q6 | Difícil | 5.6 | v2 acerta 16 de 20 e v1, 14 de 20; mudou prompt e esforço (`effort`) juntos, e a v2 foi ajustada vendo os mesmos 20 casos | declarar vitória; repetir só a v2; usar mais casos sem corrigir o desenho |

Cobertura: todas as unidades; Q4 e Q6 com situação para analisar. Gabarito definido na redação, sem padrão regular e diferente dos capítulos 1 (C, A, D, B, C, D), 2 (C, D, A, B, D, A), 3 (A, C, D, A, B, C) e 4 (B, D, A, C, B, D), conferidos no HTML em 16/11/2026. Cuidado: o validador exige explicação coerente com o gabarito em cada alternativa.

## 6. Produção: blocos, modelos e efforts

Só as combinações do projeto (Sonnet 5.5 High, Opus 5.5 High; Git, Haiku 5.5 Medium, mas não há Git). Preflight em cada bloco; divergência `atual → recomendado` e pausa.

| Bloco | Modelo / effort | Conteúdo | Gate |
|---|---|---|---|
| 0 | — (operador) | Aprovar este plano e as decisões da §8; atualizar o sumário e validar | Aprovação |
| 1 | Sonnet 5.5 High | Baixar fontes da §3 para pasta temporária vazia, extrair com `extrair-texto-web.py`; verificar os dois candidatos não confirmados; montar `pacote-de-fontes-capitulo-5-2026-11-….md` com citação literal, seção e data; `conferir-trechos.py` | Pacote aprovado pelo script |
| 2 | Sonnet 5.5 High | Abertura e 5.1; **pausa para o operador aprovar nível, exemplo e tabela**; depois 5.2 a 5.6, questões, glossário, referências, sumário | Validador sem falha |
| 3 | Opus 5.5 High (opcional, decisão do operador) ou segunda leitura em Sonnet | Ler contra fontes e requisitos; coerência com 3 e 4; sobreposição com 6 a 15 | Sem achado material |
| 4 | Sonnet 5.5 High | Validador, PDF com Chrome for Testing 158, backup em `arquivo/antes-capitulo-5-2026-11-…/`, changelog, handoff | Resultados registrados |

## 7. Riscos e controles

| Risco | Controle |
|---|---|
| Capítulo virar lista de métricas e siglas | Cada ideia com decisão, caso e limite; poucos termos, definidos na primeira ocorrência |
| Número de exemplo ser lido como medida real | Marca *ilustrativo, não medido* em toda tabela; valores redondos e pequenos |
| Afirmar vieses ou percentuais de memória | Só com trecho literal conferido; "mais de 80%" não entra sem leitura do artigo |
| Candidatos de fonte (Miller; Wang et al.) não existirem como lembrados | Verificar no Bloco 1; se falhar, remover e usar *proposta didática* |
| Estatística demais para quem não programa | Linguagem simples, sem fórmula; tabela de decisão; sem prometer significância |
| Sobreposição com 6, 10, 11, 13, 14 e 15 | Pontes explícitas; aprofundamento no módulo dono |
| Ajustar o prompt aos casos e declarar melhora | Conjunto reservado na 5.6c; Q6 cobre o erro |
| Dados pessoais nos casos de teste | Casos fictícios; menção ao módulo 6 para dados reais |
| Página da Anthropic mudar entre escrita e publicação | Data de consulta no texto; nota no changelog |
| Quem escreveu também revisa | Segunda leitura (Opus ou nova sessão) recomendada, como no capítulo 4 |

Segurança e LGPD: exemplos sem dados reais, sem chave, sem chamada a modelo. Sem gatilho para triagem. Proporcionalidade: nenhuma dependência, componente ou fonte paga.

## 8. Decisões pedidas ao operador

1. Aprovar o plano: seis unidades, 20 partes (3/3/3/4/3/4), seis questões.
2. Confirmar o assistente de matrícula (v1 e v2 do capítulo 4) como caso principal, só no fechamento das unidades, mais as duas cenas curtas.
3. Confirmar a pausa após a 5.1.
4. Confirmar as fontes da §3, ciente de que dois artigos são candidatos a verificar.
5. Confirmar três molduras de imagem (5.1a, 5.4a, 5.6b), só moldura até o texto estar validado.
6. Decidir se a segunda leitura será por Opus 5.5 High ou Sonnet em sessão separada.

Padrões adotados se não houver outra decisão: abertura própria; no máximo uma tabela por parte; sem componente novo; meta de 400 a 500 palavras por parte; partes acima disso seguem a decisão pendente do operador (handoff, pendência 2).

## 9. Estado de continuidade (16/11/2026)

- **Capítulo escrito por inteiro (16/11/2026):** unidade 5.1 aprovada e capítulo autorizado pelo operador; ver `changelog-capitulo-5-conclusao-2026-11-16.md` e `handoff-capitulo-5-concluido-2026-11-16.md` (HTML `820e006c24e4a899`, PDF `a2be776b9f931796`). Imagens: só no fim, por ordem do operador.

- **Decisões do operador (16/11/2026):** itens 1 a 5 da §8 aprovados; item 6: a segunda leitura continua em Sonnet 5.5 High, em sessão separada.
- **Bloco 1 concluído:** `pacote-de-fontes-capitulo-5-2026-11-16.md`, 44 trechos, 44 aprovados no `conferir-trechos.py`; Miller e Wang et al. confirmados (título, autoria e resumo lidos). Texto integral da Anthropic lido; data de publicação 09/01/2026 pelo metadado da página.
- **Bloco 2 iniciado (16/11/2026):** abertura e 5.1a a 5.1c escritas no guia (HTML `e01217e94cc2dfab`, PDF `ee1d06226d5a7331`); pausa para o operador aprovar nível, exemplo e tabelas. Detalhes: `changelog-capitulo-5-bloco-2-2026-11-16.md` e `handoff-capitulo-5-bloco-2-2026-11-16.md`.

- Plano escrito e revisado em 16/11/2026 (`/revisar`: 6 ajustes e 4 sugestões de conteúdo aplicados com autorização do operador); nada alterado no guia. Estado verificado antes: validador 16 OK, 0 FALHA; HTML `bdb34977877270ed`, PDF `1d1dfb567fb3e5db`.
- Próxima ação: decisões da §8; depois, Bloco 1 (pacote de fontes).

claude - pessoal, 16/11/2026
