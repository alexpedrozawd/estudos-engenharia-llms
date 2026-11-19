# Roteiro de aprofundamento: engenharia de prompt, engenharia de contexto e gestão de sessões

Data: 13/11/2026. Autoria: claude - pessoal. Pedido do operador no painel (ap-ai-router).
Estado: **integrado em 13/11/2026**. O §2, os acréscimos de referência e as descrições dos capítulos 4, 7, 8, 13 e 15 foram levados ao plano mestre e ao sumário do guia pela sessão de reestruturação. As fontes continuam como candidatas: só entram no livro com trecho literal conferido. Este arquivo fica como registro; não autoriza ações.

## 1. Cobertura atual (conferida em 13/11/2026 no sumário do HTML e no plano mestre)

| Tema | Onde está | Estado |
|---|---|---|
| Engenharia de prompt | Cap. 4 "Prompts, parâmetros e respostas" (instruções e exemplos, mensagens, contagem de tokens, parâmetros, schemas, templates, tratamento de falhas) | Só no sumário; não escrito. **A tabela "Referências públicas por módulo" não tem linha para o módulo 4.** |
| Engenharia de contexto | Cap. 8 "Contexto e memória" (orçamento de contexto, recuperação sob demanda, histórico, continuidade e compactação) | Só no sumário; fonte já prevista: Anthropic, *Effective context engineering for AI agents* (29/09/2025) |
| Boas práticas e proporcionalidade | Cap. 7 "Atos autodestrutivos e proporcionalidade" (custo total, decisões de baixo retorno) | Só no sumário; sem referência pública na tabela |
| Cache e esforço | Cap. 15 "Eficiência e economia" (medição, cache, ajustes); unidades 1.4 (raciocínio) e 2.3 (cache de prefixo) | Cap. 15 só no sumário; 1.4 e 2.3 escritas. Conferido no HTML: cache de prefixo está na 2.3 (10 menções); "esforço" de raciocínio quase não aparece (1 menção, na 1.6) |
| Escolha e troca de modelo ou esforço | Cap. 13 "Seleção e roteamento" (escalonamento, contingência) | Só no sumário; sem referência pública na tabela |
| **Ciclo de vida da sessão** (quando limpar, handoff, retomada, ponto ótimo de custo) | **Não está explícito em nenhum capítulo** | Lacuna |

## 2. Acréscimos propostos (onde inserir)

| Módulo | Acréscimo | Motivo |
|---|---|---|
| 4 | Incluir técnicas de prompt com fonte primária (exemplos, raciocínio passo a passo, instruções estruturadas) e a linha de referências que falta | O capítulo existe, mas sem fonte pública planejada |
| 8 | Nova unidade "Ciclo de vida da sessão": custo do contexto que cresce a cada chamada, quando limpar, handoff e prompt de retomada, pausa longa e expiração do cache | Lacuna; é o que o operador vive no dia a dia |
| 13 | Nota: trocar modelo ou esforço só na fronteira de uma conversa nova; rota automática dentro da conversa tende a custar mais (ver §3) | Evita ensinar roteamento que destrói o cache |
| 15 | Unidade "Cache e esforço: o que invalida o cache e quanto custa" e o modelo de ponto ótimo de sessão, para medir no próprio uso | Une as evidências do §3 à medição já feita em 23/10/2026 |
| 7 | Ligar "entupimento de contexto" (diretriz local `docs/09-antipadroes-e-boas-praticas-llm.md`) ao custo total | Boas práticas com base local; o 09 ainda não tem link público |

Mantém-se o formato de partes curtas aprovado em 13/11/2026 (ver `plano-de-reestruturacao-e-adaptacao-de-leitura-2026-11-13.md`).

## 3. Evidências levantadas nesta sessão (para os módulos 8, 13 e 15)

- **Cache por prefixo.** Cobre ferramentas, instruções e mensagens. TTL padrão de 5 minutos, com opção de 1 hora. Fonte: [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). [Declarado: lida por agente em 13/11/2026, parte por resumo; conferir trechos literais antes de entrar no guia]
- **Mudar o thinking invalida o cache das mensagens; mudar o esforço também pode.** Só o valor padrão do modelo não invalida; a página de [esforço](https://platform.claude.com/docs/en/build-with-claude/effort) recomenda manter o esforço constante numa conversa com cache. [Declarado, mesmas condições]
- **Preço relativo (API):** leitura de cache 0,05× o preço base de entrada no Sonnet 5.5 e no Opus 5.5 (0,1× nos demais); escrita 1,25× (5 min) e 2× (1 h). [Declarado, mesmas condições]
- **Troca de modelo:** as páginas lidas não dizem se invalida o cache. [Hipótese: modelo diferente não reaproveita os estados internos de outro]
- **Medição local de 23/10/2026** (`medicao-fluxo-de-tokens-20261023.md`, relatório local fora deste repositório): no Claude, 20 sessões e 2.025 respostas; cache lido 481 M contra 2,33 M de saída (≈0,5%); contexto fixo inicial ≈ 44,5 mil tokens (≈ 18% do volume); crescimento ≈ 2,7 mil tokens por chamada; as 3 maiores sessões somam 46% do cache lido. [Provado no relatório; amostra pequena e dominada por um projeto]
- **Modelo de ponto ótimo (estimativa minha).** Custo por chamada = leitura do contexto + escrita do contexto inicial dividida pelas chamadas da sessão. Tamanho ótimo ≈ raiz de [2 × escrita × (contexto fixo + reorientação) ÷ (leitura × crescimento por chamada)]. Com leitura 0,05× a 0,1×, escrita 1,25×, fixo 44,5 mil, reorientação 5 mil e crescimento 2,7 mil: **≈ 20 a 30 chamadas** (contexto de ~100 a 130 mil tokens). Custo por chamada relativo ao ótimo: +44% limpando a cada 10 chamadas, +16% com 60, +52% com 100. [Estimativa: supõe cache sempre aproveitado, sem efeito de qualidade e com preços da API]
- **Limite:** o operador usa plano Pro e CLIs; a contagem de cota delas pode diferir dos preços da API. [Não verificado]
- Regras práticas derivadas: agrupar demandas do mesmo assunto; limpar ao mudar de assunto, em ~100 a 130 mil tokens ou antes de pausa longa com contexto grande; trocar modelo ou esforço só ao limpar.

## 4. Fontes candidatas ainda não conferidas (verificar antes de usar)

- Módulo 4: documentação oficial de prompting dos provedores; Brown et al., arXiv:2005.14165 (exemplos no prompt); Wei et al., arXiv:2201.11903 (raciocínio passo a passo).
- Módulo 8: Liu et al., arXiv:2307.03172 (informação no meio do contexto longo).
- Entram no livro só com trecho literal conferido, como nos capítulos 1 e 2.

## 5. Integração feita em 13/11/2026

1. Feito: §2 no plano mestre (módulos 4, 7, 8, 13, 15) e linhas dos módulos 4, 7 e 13 na tabela "Referências públicas por módulo".
2. Feito: descrições dos capítulos 4, 7, 8, 13 e 15 no sumário, sem criar páginas vazias.
3. Feito: registrado no changelog e no handoff de 13/11/2026; arquivo marcado como integrado.

claude - pessoal, 13/11/2026

Assinatura da integração: deepseek - conta não verificada, 13/11/2026.
