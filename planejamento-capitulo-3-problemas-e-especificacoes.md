# Planejamento do Capítulo 3 — Problemas e especificações

Data: 13/11/2026. Autoria: deepseek - conta não verificada (painel). Etapa: **somente planejamento**; nada redigido no guia, nenhuma fonte baixada. Aprovado pelo operador em 13/11/2026 para começar; o primeiro passo é este plano, não a redação.

Base: [plano mestre](planejamento-completo-estudos-engenharia-llms.md), [plano do Capítulo 2](planejamento-capitulo-2-arquitetura-de-sistemas-com-llm.md), [requisitos de formato](requisitos-de-formato-html-do-material.md) (§8, parte curta; §9, impressão e exemplos), [protocolo de economia de tokens](protocolo-de-economia-de-tokens-entre-sessoes.md). Herda do Capítulo 2 o método de produção; herda do formato de 13/11/2026 a divisão em partes curtas.

## 1. Objetivo, escopo e aceite

**Objetivo:** ao concluir o capítulo, o estudante transforma um pedido vago — "queremos um chatbot" — numa especificação curta: problema e usuário, resultado esperado e como medi-lo, restrições, critério de aceite, decisão sobre onde a IA entra e contratos entre as partes. Ele justifica cada escolha e reconhece uma especificação fraca.

**Escopo:** abertura, seis unidades em partes curtas, seis questões, termos do glossário e referências. Progressão fixada no plano mestre: problema e usuário → resultado esperado → restrições → aceite → escolha do uso de IA → contratos e decomposição.

**Fora do escopo:** redigir prompts e parâmetros (módulo 4); construir avaliações e comparar modelos (módulo 5); segurança, permissões e LGPD em profundidade (módulo 6); proporcionalidade e custo total (módulo 7); arquitetura de componentes (capítulo 2, já feito); contratos de ferramentas, MCP e protocolos (módulo 9); operação e lançamento (módulo 14). Só menção, com ponte.

**Aceite:**
- cada unidade em partes de 400 a 500 palavras, no molde do §8: resumo "Em 3 linhas", imagem opcional, analogia, texto, uma pergunta, ponto de retomada, notas de fonte; a última parte traz *Ler*, *Assistir* e *Aprofundar*;
- nenhum trecho de programa; a especificação aparece como tabela ou lista, não como documento executável;
- toda afirmação rastreia fonte datada ou é *proposta didática*; norma citada com nome e versão, nunca "conforme a ISO";
- exemplos sem nomes internos: a empresa fictícia Aurora Educação e a plataforma interna de IA genérica;
- seis questões (duas fáceis, três médias, uma difícil), com gabarito sem padrão regular e diferente dos capítulos 1 e 2;
- `validar-guia.py` sem falha; PDF em A4 sem bloco dividido; Chrome de 320 a 1920 px sem rolagem horizontal; mecânica das questões OK.

## 2. Decisões de desenho

1. **Nível:** quem leu os capítulos 1 e 2. A especificação parte do que já foi visto: componentes, fronteiras, chamada ao modelo e falhas.
2. **Eixo:** antes de escolher modelo, prompt ou ferramenta, decide-se o que o sistema resolve, para quem, com que limites e como saber se deu certo. Especificar é decidir; o documento é consequência.
3. **Espinha dorsal única:** a Aurora Educação cresce ao longo das seis unidades e fecha na 3.6d. O capítulo 2 alternava exemplos; aqui, um caso só deixa ver a especificação nascer. Controle do risco de repetição: cada unidade muda o foco (problema, resultado, restrição, aceite, decisão, contrato), sem recontar o caso inteiro.
4. **Partes curtas:** 20 partes, na proporção 3/3/3/4/3/4. A unidade 3.4 tem quatro partes porque aceite é o núcleo prático do capítulo; a 3.6 também, porque fecha o caso e a especificação.
5. **Sem programação e sem componente novo:** diagramas só com `ol.fluxo` e tabelas, no máximo uma tabela por parte. A especificação é apresentada como tabela de campos e como lista de critérios.
6. **Qualificadores mantidos:** *registrado na norma*, *registrado na documentação*, *registrado nas diretrizes locais*, *verificado no código local*, *proposta didática*.
7. **Fontes normativas com ressalva:** RFC 2119, NASA SE Handbook, NIST AI RMF e Scrum Guide entram por trecho literal e seção; o guia **não afirma conformidade** com nenhuma delas. NIST e NASA são volumosos: conferir só a seção citada, sem ler o documento inteiro.
8. **Português claro sobre jargão:** "requisito", "critério de aceite", "contrato" e "decomposição" são definidos como termos de trabalho do livro, com a fonte ao lado quando houver.
9. **Ids:** `capitulo-3`, `unidade-3-1a` a `unidade-3-6d`, `questoes-capitulo-3`, `c3q1` a `c3q6`. O sumário passa a apontar para `#unidade-3-1a`.
10. **Links externos** em nova guia (`target="_blank" rel="noopener noreferrer"`).
11. **Imagens:** poucas. Proposta de três molduras (3.1a, 3.4b, 3.6d), só com `role="img"` e `aria-label` até o texto estar finalizado, revisado e validado. Geração na última etapa.
12. **Ponte com o capítulo 2:** a especificação não repete componentes nem a chamada; usa-os como peças já conhecidas.

## 3. Fontes (nenhuma lida nesta sessão; conferir e extrair no Bloco 1)

| Fonte | Papel | Estado |
|---|---|---|
| IETF RFC 2119 (Bradner, março de 1997) | Linguagem de obrigação: DEVE, NÃO DEVE, DEVERIA, PODE | A ler |
| NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev2 | Requisito verificável, critério de verificação, rastreabilidade | A ler só a seção de requisitos |
| NIST AI RMF 1.0 (NIST AI 100-1, 26/01/2023) | Contexto de uso e propósito declarado do sistema | A ler só o trecho de contexto de uso |
| Scrum Guide 2020 (Schwaber e Sutherland) | Definição de Pronto; aceite combinado antes | A ler |
| Anthropic — *Demystifying evals for AI agents* (09/01/2026) | Definir sucesso a partir de tarefas reais e falhas | A ler; reaberta em 13/11/2026 no pacote do capítulo 2 |
| Anthropic — *Building effective agents* (19/12/2024) | Começar simples; complexidade só com ganho demonstrável | A ler; reaberta em 13/11/2026 |
| Nielsen Norman Group — página sobre personas ou análise de tarefas (escolher na conferência) | Usuário e tarefa | A escolher e ler |
| `docs/09` do Router (interna) | Antipadrão: LLM para lógica simples; fila sem necessidade | Lido em 13/11/2026; sem link público |
| Especificação MCP 2026-07-28 (só menção) | Contrato entre sistema e ferramentas; ponte para o módulo 9 | Já citada na 2.1c; reconferir a frase |

**Evidência local (leitura, lista fechada, sem execução):** plataforma interna de IA — contrato de despacho com campos explícitos, `fingerprint` do pedido, recusa 409 para o mesmo identificador com conteúdo diferente, prazo e fila; serve de exemplo de contrato já existente. Aurora Educação — situação construída, marcada *proposta didática*, sem pessoas, dados de clientes ou nomes de fornecedores. Nunca ler bancos, logs ou credenciais.

## 4. Mapa por unidade

### 3.1 Problema e usuário (3 partes)
- **Competência:** separar sintoma, problema e solução embutida; escrever o problema em uma frase com evidência; identificar usuário direto, afetado, quem aprova e quem vai operar; registrar tarefa, volume e frequência.
- **Partes:** *3.1a O pedido não é o problema* — "queremos um chatbot" como solução disfarçada; o que é evidência. *3.1b Quem faz o quê, com que frequência* — usuário, afetado, aprovador, operador, tarefa, persona leve como registro. *3.1c O problema da Aurora, em uma frase* — secretaria escolar e dúvidas de matrícula; evidência de volume e tempo; quem aprova e quem opera; o que fica fora.
- **Conceitos:** problema, sintoma, usuário, afetado, aprovador, operador, tarefa, evidência.
- **Equívocos:** "o pedido do chefe é o problema"; "persona é personagem"; "se a pessoa pediu, o problema está provado"; "quem opera aparece depois".
- **Ponte:** 3.2 e módulo 5 (tarefas reais para avaliar).

### 3.2 Resultado esperado (3 partes)
- **Competência:** distinguir saída de resultado; definir o que a pessoa conseguirá fazer; escolher uma medida, uma linha de base e uma meta inicial; reconhecer métrica que premia o errado.
- **Partes:** *3.2a Saída não é resultado* — "ter chatbot" não é resultado. *3.2b Uma medida e uma linha de base* — indicador, base, meta, custo de medir. *3.2c O resultado do assistente de matrícula* — tempo de resposta e resolução sem escalar; o que não é resultado.
- **Conceitos:** saída, resultado, indicador, linha de base, meta inicial.
- **Equívocos:** "entregar o sistema é o resultado"; "medir tudo"; "meta sem base é meta".
- **Ponte:** módulo 5 (avaliação) e 15 (custo de medir).

### 3.3 Restrições (3 partes)
- **Competência:** listar restrições de prazo, orçamento, dados, privacidade, sistema existente, capacidade e condições do provedor; nomear requisitos não funcionais (latência, disponibilidade, custo, privacidade, acessibilidade); registrar a força de cada uma (deve, deveria, pode); separar restrição de preferência.
- **Partes:** *3.3a O que não está sob nosso controle* — as famílias de restrição, incluindo dados (disponibilidade, qualidade, dono) e requisitos não funcionais. *3.3b Deve, deveria, pode* — força da restrição, com RFC 2119 como modelo; priorização. *3.3c As restrições da Aurora* — janela de matrícula, orçamento, dados de alunos, sistema acadêmico legado.
- **Conceitos:** restrição, preferência, obrigatório, desejável, opcional, prioridade, requisito não funcional, qualidade do dado.
- **Equívocos:** "restrição é desculpa"; "tudo é obrigatório"; "dado existe, então está disponível"; "LGPD é assunto só do jurídico" (ponte para 6).
- **Ponte:** módulo 6 (privacidade e permissões) e 14 (sistema existente).

### 3.4 Aceite (4 partes)
- **Competência:** escrever critério observável e verificável, combinado antes e com quem aceita; separar pronto de aceito; cobrir caso normal, falha e recusa; reconhecer o que o aceite de texto gerado pode e não pode prometer.
- **Partes:** *3.4a Combinado antes, verificável depois* — critério de aceite, quem aceita e Definição de Pronto. *3.4b Um critério que se testa* — condição, ação, resultado esperado; casos de falha e recusa. *3.4c Aceite de texto gerado* — o objetivo (formato, campos, fonte) e o que exige amostra (qualidade); ponte para 5. *3.4d O aceite do assistente de matrícula* — três famílias de critério; o que ainda depende de avaliação.
- **Conceitos:** critério de aceite, verificável, pronto, aceito, caso de falha, amostra.
- **Equívocos:** "resposta boa e rápida é critério"; "passou no teste, está pronto"; "aceite se define no fim".
- **Ponte:** módulo 5 (avaliação e regressões).

### 3.5 Escolha do uso de IA (3 partes)
- **Competência:** decidir quando a tarefa pede modelo e quando pede regra determinística; escolher o grau de autonomia (assistir, sugerir com aprovação, automatizar com conferência); justificar o que fica fora.
- **Partes:** *3.5a Quando o modelo ajuda e quando atrapalha* — linguagem aberta contra regra; antipadrão do LLM para lógica simples (`docs/09`). *3.5b Três graus de autonomia* — onde a pessoa fica em cada um. *3.5c A decisão da Aurora* — formulário, busca e modelo; o que não vira IA.
- **Conceitos:** regra determinística, tarefa aberta, autonomia, aprovação humana, conferência.
- **Equívocos:** "IA é sempre melhor"; "automatizar tudo é o objetivo"; "o modelo decide o valor".
- **Ponte:** capítulo 1 (1.6) e módulo 7 (proporcionalidade).

### 3.6 Contratos e decomposição (4 partes)
- **Competência:** descrever o contrato de uma fronteira (entra, sai, garantido, pode falhar); decompor o problema em partes contratáveis por resultado; montar a especificação de uma página, com suposições, não-objetivos e registro de decisões; revisar uma especificação contra uma lista.
- **Partes:** *3.6a O contrato de uma fronteira* — quatro perguntas do contrato. *3.6b Decompor sem inventar* — partes, responsável, dado, interface; decomposição por resultado. *3.6c A especificação em uma página* — estrutura mínima (problema, usuário, resultado, restrições, aceite, decisão de IA, contratos, suposições, não-objetivos), o que não precisa constar e o registro de decisões. *3.6d A especificação completa da Aurora* — o caso inteiro; checklist de revisão; fechamento.
- **Conceitos:** contrato, interface, entrada, saída, garantia, falha prevista, decomposição, suposição, não-objetivo.
- **Equívocos:** "contrato é documento jurídico"; "decompor por tecnologia"; "mais partes é mais profissional"; "suposição que não se escreve é fato".
- **Ponte:** capítulo 2 (fronteiras e erro) e módulo 9 (contratos de ferramentas).

## 5. Matriz das seis questões (4 alternativas, 1 correta, primeira resposta trava)

| # | Nível | Unidades | Situação e foco | Distratores |
|---|---|---|---|---|
| Q1 | Fácil | 3.1 | Pedido "queremos um chatbot" chega pronto: o que ainda falta para virar problema | aceitar o pedido como problema; pedir mais um sistema; culpar o usuário |
| Q2 | Fácil | 3.2 | "Entregamos o chatbot" apresentado como resultado | confundir entrega com resultado; medir adoção como sucesso; meta sem base |
| Q3 | Média | 3.3 | Restrições da Aurora registradas com força trocada ("seria bom" para prazo legal) | tratar tudo como opcional; transformar preferência em obrigação; ignorar LGPD |
| Q4 | Média | 3.4 | Critério "resposta clara, rápida e correta" proposto como aceite | aceitar adjetivo como critério; trocar por opinião do chefe; exigir 100% de acerto |
| Q5 | Média | 3.5 | Cálculo de desconto e resposta a dúvida aberta no mesmo fluxo: onde a IA entra | modelo para o cálculo; regra para a dúvida aberta; automatizar sem conferência |
| Q6 | Difícil | 3.4–3.6 | Especificação da Aurora com três defeitos (aceite sem caso de recusa, contrato sem o que pode falhar, suposição não escrita tratada como fato): achar a premissa falha | "mais partes resolve"; "o aceite se ajusta depois"; "o contrato é jurídico" |

Cobertura: todas as unidades; Q5 e Q6 com caso para analisar. Gabarito na redação, sem padrão regular e diferente do capítulo 1 (B, D, A, C, B) e do capítulo 2 (C, A, D, B, A). O validador confere de 5 a 6 questões por capítulo.

## 6. Produção: blocos, modelos e efforts

Só as combinações do projeto. Preflight em cada bloco; divergência `atual → recomendado` e pausa.

| Bloco | Modelo / effort | Conteúdo | Gate |
|---|---|---|---|
| 0 | — (operador) | Aprovar este plano e as decisões da §8. Depois, atualizar o sumário (links do capítulo 3) e validar. | Aprovação |
| 1 | Sonnet 5.5 High | Baixar as fontes da §3 para pasta temporária vazia (`curl -L`), extrair com `extrair-texto-web.py`; ler os trechos locais da lista fechada; montar `pacote-de-fontes-capitulo-3.md` com citação literal, seção e data; `conferir-trechos.py`. Não editar o guia. | Pacote aprovado pelo script |
| 2 | Sonnet 5.5 High | Abertura e 3.1. **Pausa: operador aprova nível, exemplo e tabela.** Depois 3.2 a 3.6, questões, glossário, referências; páginas novas na sequência; navegação; sumário. | Validador sem falha |
| 3 | Opus 5.5 High | Ler contra fontes e requisitos: normas, aceite, contrato, coerência com 2 e sobreposição com 4 a 9. Correções pequenas; erro que exija reescrever volta ao Sonnet. | Sem achado material |
| 4 | Sonnet 5.5 High | Validador, PDF com Chrome for Testing, backup em `arquivo/antes-capitulo-3-2026-11-13/`, changelog, handoff. | Resultados registrados |

## 7. Riscos e controles

| Risco | Controle |
|---|---|
| Capítulo virar manual de documento de requisitos | Especificar é decidir; o documento aparece só na 3.6c, curto |
| Norma citada como conformidade | Ressalva explícita; trecho literal com seção; nunca "conforme a ISO" |
| Caso único da Aurora cansar ou repetir | Cada unidade muda o foco; caso completo só na 3.6d |
| Sobreposição com 4, 5, 6, 7 e 9 | Pontes explícitas; aprofundamento fica no módulo dono |
| Aceite prometer precisão que não se mede | Separar critério objetivo de amostra; ponte para 5 |
| Especificação sem suposições e não-objetivos vira armadilha | A 3.6c exige as duas listas; a Q6 cobra a suposição não escrita |
| Escorregar para programação | Sem código; especificação em tabela e lista |
| Questões com resposta opinativa | Situação com critério verificável na explicação |
| Documentos normativos longos consumirem a sessão | Ler só a seção citada; protocolo §3 |

Segurança e LGPD: exemplos sem dados pessoais reais; dados de alunos da Aurora são fictícios e de menor sensibilidade no texto; sem gatilho para triagem. Proporcionalidade: nenhum componente, ferramenta nova ou fonte paga.

## 8. Decisões pedidas ao operador

1. Aprovar o plano: seis unidades, 20 partes (3/3/3/4/3/4), seis questões.
2. Confirmar a espinha dorsal única da Aurora Educação, crescendo até a 3.6d.
3. Confirmar a pausa após a 3.1, como no capítulo 2.
4. Confirmar as fontes normativas (RFC 2119, NASA SE Handbook, NIST AI RMF, Scrum Guide) e as duas páginas da Anthropic já reabertas, com a ressalva de não afirmar conformidade.
5. Confirmar três molduras de imagem (3.1a, 3.4b, 3.6d), só como moldura até a validação.

Padrões adotados se não houver outra decisão: abertura própria; no máximo uma tabela por parte; textos de especificação em tabela; sem componente novo.

## 9. Estado de continuidade (13/11/2026)

- Plano escrito nesta sessão; nada redigido no guia, nenhuma fonte baixada.
- Estado verificado antes: guia 51 páginas, validador 16 OK e 0 FALHA; hashes conferidos com o handoff vigente.
- O sumário lista o capítulo 3 na linha 271, sem links nem conteúdo.
- Próxima ação: decisões da §8; depois, Bloco 1 (pacote de fontes).

deepseek - conta não verificada, 13/11/2026
