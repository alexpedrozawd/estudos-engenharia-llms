# Changelog — Revisões 1 e 2 (cobertura além do autor; linguagem simples)

Data: 15/10/2026. Pasta fora de repositório Git: sem commit nem push. Redação: claude - pessoal (Sonnet 5.5, effort High declarado pelo operador). Revisão final e leitura de fidelidade: claude - pessoal (Opus 5.5; effort High declarado pelo operador, não verificável).

## 1. Pedido e aprovações
- Revisão 1: ver se o conteúdo cobre só o que o operador desenvolveu ou também técnicas, métodos e estudos promissores que ele ainda não usou. Revisão 2: linguagem mais simples possível, como para um leigo total.
- Aprovado em 15/10/2026 ("ok aprovo"): o tom do piloto da unidade 1.1; mover citações e etiquetas de confiança para "Notas de fonte" no fim de cada unidade; as inserções P1 e as pontes P2; atualizar o plano mestre.
- Relatório da revisão 1: `revisao-1-cobertura-alem-do-que-foi-desenvolvido.md`. Piloto: `piloto-linguagem-simples-unidade-1-1.md`.

## 2. O que mudou no guia
- **Linguagem (revisão 2), em todo o texto das páginas 2 a 20:** introdução, aberturas, 12 unidades, questões, glossário e referências reescritos com frases mais curtas, termos explicados na primeira vez, português antes do inglês e comparações do dia a dia. Média de palavras por frase no texto principal: de 18,3 para 15,9 (as unidades mais simples chegam a 12,8). Citações entre parênteses por unidade: de 13–24 para 6–17. Sumário e capa intactos.
- **Notas de fonte (novo, em cada unidade):** cada afirmação continua rastreável, com a fonte, a data e a etiqueta de confiança. Etiquetas novas: *registrado em artigo* e, para rascunhos da IETF, *registrado na norma*.
- **Inserções (revisão 1):**
  - 1.2: mistura de especialistas (Mixtral) e LoRA; 1.3: *Lost in the Middle* e *Context Rot* como apoio independente ao *context rot*, com os limites de cada estudo; compactação.
  - 1.4: modelos que raciocinam antes de responder (custo, limite de saída, tempo); 1.5: PagedAttention e decodificação especulativa como menção.
  - 1.6: apoio público ao princípio da simplicidade (*Building effective agents*).
  - 2.1: MCP como fronteira de ferramentas; 2.2: raciocínio no limite de saída e saídas estruturadas (forma garantida, verdade não); 2.3: raciocínio e primeiro texto, cache de prefixo e processamento em lote.
  - 2.4: `Idempotency-Key` é rascunho expirado da IETF, e não padrão; 2.5: retomada em sistemas de agentes (relato público da Anthropic); 2.6: disjuntor (*circuit breaker*) e uma linha na tabela.
- **Glossário:** de 82 para 93 termos. **Referências:** 13 entradas novas (16 fontes); *Building effective agents* saiu de "não lido" para "consultada em 15/10/2026".
- **Rótulo:** "Ver feedback" virou "Ver retorno" em todas as perguntas.
- **Plano mestre:** nova tabela "Referências públicas por módulo" (módulos 5, 6, 8, 9, 10, 11, 12, 14 e 15). **Requisitos de formato:** nova regra de linguagem simples e notas de fonte.

## 3. Revisão final e leitura de fidelidade (Opus 5.5 High)
Guia inteiro lido contra a versão anterior, os pacotes de fontes e os requisitos. Nenhum erro exigiu reescrever. Correções pequenas:
1. 1.1 e glossário: IA ligada a "imagem" estreitava a definição original ("percepção") → "percepção (como ver e ouvir)".
2. 1.2: Mixtral "13 bilhões em cada palavra" → "em cada token" (o livro distingue token de palavra); frase confusa "erro oposto" sobre *fine-tuning* prematuro reescrita; redação "aparecem cedo em quem estuda" corrigida.
3. 1.4: "quase não é usada" voltou a "na prática, não é usada" (fiel ao livro-base); "Muitos modelos atuais" → "Alguns" (sem fonte para "muitos"); "o modelo testa passos e muda de ideia" passou a citar os comportamentos descritos no DeepSeek-R1, com trecho literal novo no pacote.
4. 2.2: "dessa regra" apontava para algo ainda não dito; "uso reportado maior que o texto visível" ganhou trecho literal da Anthropic.
5. 2.4: retirada a generalização sem fonte "cada provedor define o seu jeito".
6. 2.5: a frase traduzida "não dá para simplesmente recomeçar do zero" ganhou o trecho original nas notas.
7. 2.6: notas citavam "lotes contínuos", que saiu do texto; o teste depois de um tempo do disjuntor passou a ter trecho literal de Fowler.
8. Questão 5 do cap. 2: "modelo local dividido por dez pessoas" → "compartilhado" (como no original).
9. Glossário: "Compactação" fora da ordem alfabética; "Escolha gulosa" ganhou a condição "com o mesmo contexto e o mesmo modelo".
10. Documentos: relatório da revisão 1 dizia que alguns termos "só existem" nas diretrizes do autor (não verificado) → "sem fonte pública citada no guia"; changelog contava "11 fontes novas" (eram 13 entradas, 16 fontes); piloto marcado como aplicado.
- Conferido sem mudança: gabarito idêntico ao anterior (B, D, A, C, B; C, A, D, B, A); afirmações das fontes novas contra os 39 trechos; pontes para os módulos 4, 8, 9, 12, 13, 14 e 15; nenhuma regra local apresentada como consenso.
- Riscos da sessão revisados: guia anterior arquivado antes da troca; nada apagado; projetos-fonte não tocados; ferramentas de teste só na pasta temporária.

## 4. Validação executada em 15/10/2026 (depois das correções)
- `python -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: 16 OK, 0 falha.
- `conferir-trechos.py` em `pacotes-de-fontes-revisao-1.md`: **39 aprovados, 0 reprovados**. Os textos extraídos ficaram na pasta temporária da sessão (podem sumir; para reconferir, baixar de novo as URLs).
- Chrome (Playwright `channel="chrome"`, venv temporário): sem rolagem horizontal em 320, 480, 768, 1024, 1280 e 1920 px; nenhum elemento fora de região de rolagem; axe-core 4.10.2 sem violações (incompleta conhecida: `aria-prohibited-attr`, 20 nós nos números de página); questões 5 de 5 em cada capítulo; 92 links internos com alvo.
- Comparação com o guia anterior (`arquivo\antes-da-revisao-linguagem-simples\`): CSS, script, cabeçalho, capa, sumário e navegações idênticos; ids iguais, sem duplicata; tags equilibradas; glossário em ordem alfabética.
- Não verificado: aparelhos reais (S24, Nitro 5, APSRV); conforto de leitura.

## 5. Decisões e cuidados
- Nenhum valor de preço, desconto ou tempo de cache entra como fato fixo: aparece com a data (15/10/2026) e com o aviso de que muda.
- Fontes sem trecho conferido, fora do livro (só no plano mestre): OWASP Top 10 for LLM 2025 (site oficial bloqueou a leitura), NIST AI 600-1, OpenTelemetry, *Contextual retrieval*, *Writing tools*, *Demystifying evals*, Zheng et al.
- Tamanho (palavras do texto principal, sem notas, fontes e retorno): 1.1 1.230; 1.2 1.300; 1.3 1.212; 1.4 1.361; 1.5 889; 1.6 1.078; 2.1 1.258; 2.2 1.358; 2.3 1.336; 2.4 1.193; 2.5 1.302; 2.6 1.369. Passam do teto de 1.350: 1.4 (+11), 2.2 (+8) e 2.6 (+19). Contagem diferente da dos changelogs anteriores.

## 6. Hashes (SHA-256, 16 primeiros caracteres)
`guia-engenharia-llms.html` 6136c61124752bf0 (anterior às revisões: d900f667fda6ef0c, arquivado); `pacotes-de-fontes-revisao-1.md` 31ab02f6e88e7f4e; `planejamento-completo-estudos-engenharia-llms.md` 81f5dda223ba10ac; `requisitos-de-formato-html-do-material.md` 2ca42c9c34a7876d; `revisao-1-cobertura-alem-do-que-foi-desenvolvido.md` 0d20adbf9aa59f2c; `piloto-linguagem-simples-unidade-1-1.md` ad389b7f1e117ce2.

## 7. Pendências
1. Aparelhos reais; título de tabela cortado em 320 px; `aria-label` nos números de página; referência ao `docs/09` sem link público; fontes "não lido" (CS224N, CS336, Weng).
2. Plano do Capítulo 1 sem top-k e top-p no pacote de fontes.
3. Unidades 1.4, 2.2 e 2.6 um pouco acima do teto (aparar só se pedido).
4. Capítulo 3 e seguintes: só se o operador pedir.

claude - pessoal, 15/10/2026
