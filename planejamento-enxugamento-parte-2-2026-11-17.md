# Planejamento do enxugamento da Parte II (Capítulos 6–11)

Data: 17/11/2026. Estado de referência: HEAD `316320d`, árvore limpa, guia com 337 páginas lógicas
(`sha256 770a1261…26f`) e PDF de 983 páginas A4 (`sha256 fff8c6fd…5cc`).

## 1. Objetivo e escopo

Reduzir a quantidade de páginas lógicas da Parte II sem perder contexto nem qualidade de informação.
Fora do escopo: texto dos capítulos 1–5 e 12–16, imagens (molduras ficam como estão), revisão por
outro modelo, publicação e merge.

## 2. Estado medido (Parte II inteira)

| Bloco | Páginas | Palavras | Observação |
| --- | --- | --- | --- |
| 6 aberturas de capítulo | 6 | 2.249 | 354–393 palavras cada |
| 108 partes | 108 | 50.755 | média 470; 24 passam de 500; 6 abaixo de 400 |
| 6 páginas de questões | 6 | 4.572 | 722–826 palavras; não são alvo de corte |
| **Total** | **120** | **57.576** | 26 tabelas, 28 figuras, 144 regiões aria-live |

Composição de uma parte média de 470 palavras:

| Bloco | Palavras |
| --- | --- |
| resumo «Em 3 linhas» | 54 |
| analogia | 39 |
| questão com explicações | 90 |
| ponto de retomada | 35 |
| notas de fonte | 51 |
| corpo (título, seções, tabela, navegação) | ~200 |

Ou seja, cerca de 56% das palavras de cada parte são moldura fixa exigida pelo §8 dos requisitos.
O corpo próprio — a informação nova — é de ~200 palavras por parte, ~21.700 na Parte II inteira.

## 3. Por que cortar palavras não reduz páginas lógicas

Página lógica é uma `<section class="page">`. Enxugar frases dentro das partes reduz o PDF (A4), não
a contagem lógica. Para reduzir páginas lógicas é preciso fundir partes. E cada parte tem moldura
fixa de ~270 palavras (resumo, analogia, questão, retomada, notas): fundir duas partes elimina uma
moldura inteira, mas os dois corpos continuam a existir e, somados, estouram a meta de 400–500
palavras. Logo, **toda fusão cobra um preço em conteúdo**, e o tamanho do corte define a meta.

## 4. Opções de meta

| Opção | Partes por capítulo | Fusões | Páginas da Parte II | Palavras | Corpo cortado |
| --- | --- | --- | --- | --- | --- |
| P1 | 18 → 17 | 6 (1 por capítulo) | 114 (−5%) | ~55.600 (−3,4%) | ~370 palavras (1,7%) |
| P2 | 18 → 16 | 12 (2 por capítulo) | 108 (−10%) | ~53.400 (−7,3%) | ~1.000 palavras (4,5%) |
| P3 | 18 → 15 | 18 (3 por capítulo) | 102 (−15%) | ~50.700 (−12%) | ~2.000 palavras (9,3%) |

Recomendação: **P2 (108 páginas)**. É a maior redução que ainda cabe na meta de 400–500 palavras por
parte com corte pequeno de corpo; P3 só é defensável aceitando perder cerca de 2.000 palavras de
conteúdo próprio. P1 rende pouco (−6 páginas) para justificar mexer na estrutura.

## 5. Método de fusão

Regras que cada parte fundida obedece:

1. Estrutura do §8 preservada: resumo de três linhas (reunindo os pontos das duas), uma analogia,
   corpo único, uma questão com quatro alternativas e explicação coerente, ponto de retomada e notas
   de fonte (união das duas).
2. Teto de 400–520 palavras (P3) ou 400–560 (P2); no máximo uma tabela com `.rolagem`.
3. A unidade continua com a última parte trazendo «Fontes da unidade».
4. Corte preferencial: frases que repetem a analogia, recapitulações de capítulos anteriores e
   afirmações já feitas em outra parte da mesma unidade. Toda perda de afirmação fica registrada no
   changelog; afirmação factual nova exige fonte no pacote do capítulo.
5. Neutralidade intacta: nenhum nome interno, mais de um fornecedor por módulo.

## 6. Candidatos por capítulo (medidos)

Similaridade de cosseno sobre o corpo (sem moldura) e tamanho estimado da parte fundida.
Cada capítulo perde uma parte a cada fusão; a letra das partes seguintes é renomeada (c → b etc.).

**Capítulo 6**
1. 6.3a + 6.3b — anatomia do grafo de fluxo e topologias; ~698 palavras, cos 0,42
2. 6.4a + 6.4b — subagentes/janelas limpas e poluição/autopreferência; ~622, cos 0,35
3. 6.2b + 6.2c — GraphRAG e custo de indexação; ~758, cos 0,45

**Capítulo 7**
1. 7.4a + 7.4b — tipos de injeção e onde o ataque se esconde; ~595, cos 0,17
2. 7.1b + 7.1c — mito do prompt secreto e separação de dados; ~674, cos 0,27
3. 7.2b + 7.2c — menor privilégio e identidade/deputado confuso; ~636, cos 0,18

**Capítulo 8**
1. 8.2b + 8.2c — estado limpo e preservação ao compactar; ~646, cos 0,17
2. 8.4a + 8.4b — custo total e complexidade acidental; ~670, cos 0,16
3. 8.1a + 8.1b — ações destrutivas e atalhos/vitória prematura; ~764, cos 0,21

**Capítulo 9**
1. 9.1a + 9.1b — engenharia de contexto e alto sinal; ~503, cos 0,30
2. 9.5a + 9.5b — compactação e limpeza de resultados; ~557, cos 0,34
3. 9.4a + 9.4b — notas estruturadas e controle do cliente; ~609, cos 0,40

**Capítulo 10**
1. 10.4a + 10.4b — alto sinal na saída e paginação/corte; ~518, cos 0,26
2. 10.1a + 10.1b — modelo emite pedido e modos de escolha; ~627, cos 0,39
3. 10.5b + 10.5c — retentativas e aprovação antes de efeito; ~609, cos 0,19

**Capítulo 11**
1. 11.4a + 11.4b — recuperação híbrida e reranking; ~500, cos 0,27
2. 11.6a + 11.6b — separar avaliação e quatro métricas; ~515, cos 0,37
3. 11.1b + 11.1c — busca textual e busca por símbolos; ~591, cos 0,43

Em P2 entram os dois primeiros de cada capítulo; em P3, os três.

## 7. Renumeração e navegação

- Não existe referência textual a número de página do guia (só «página 14 de um contrato», que é
  analogia). Renumerar é mecânico: percorrer as seções em ordem e reescrever
  `<span class="page-number" aria-label="Página N">N</span>`.
- Fusão remove ids `#unidade-x-yz`: é preciso reescrever a navegação do pé (anterior, próxima,
  capítulo), as frases «Na parte x.yz…» do ponto de retomada e o rótulo «parte i de n».
- O sumário lista unidades, não partes: continua válido enquanto as unidades não mudarem de nome.
- Script novo: `ferramentas/renumerar-paginas.py`, somente leitura por padrão e `--aplicar` para
  gravar. `validar-guia.py` confere 1..N e links internos.

## 8. Validação e fechamento

1. `validar-guia.py` sem falhas, com 6 questões por capítulo e numeração 1..N.
2. `conferir-trechos.py` nos pacotes dos capítulos 6 a 11.
3. Reflow em 320 px no Chrome (clientWidth = scrollWidth) nas partes fundidas.
4. Regerar o PDF e conferir páginas renderizadas.
5. Atualizar CLAUDE.md (total de páginas e faixas por capítulo), README.md, changelog do
   enxugamento e handoff; commit e push únicos no fim.

## 9. Riscos e limites

- As partes da Parte II são pouco redundantes entre si (cosseno ≤ 0,49): fusão remove conteúdo, não
  só repetição. O corte precisa ser redigido, não apagado em bloco.
- Parte fundida acima de 520 palavras contraria a meta de leitura curta; abaixo de 400, a de
  profundidade.
- Mudanças em caps. 12–16 se limitam à renumeração de páginas e a referências de parte renomeada.

## 10. Decisão e resultado

O operador escolheu **P2** em 17/11/2026: duas fusões por capítulo, 108 páginas lógicas na Parte II.
Executado e validado na mesma data: 337 → 325 páginas lógicas (96 partes na Parte II), PDF de 983 →
963 páginas A4, `validar-guia.py` 16 OK/0 FALHA, reflow 320 px sem estouros. Detalhes em
`changelog-enxugamento-parte-2-2026-11-17.md`. A execução foi feita por deepseek - painel.

deepseek - painel
