# Plano de lacunas para elevar a nota do guia (de 6,0 rumo a 10)

Estado: proposta para decisão do operador (19/11/2026). Não altera o guia nem autoriza ações.
Base: revisão de 18/11/2026 (nota realista 6,0/10) por amostra: estrutura, contagens no HTML, partes 1.5a, 13.2a e 5.3a. O texto integral (174.722 palavras, excl. capa, segundo o `README.md`) não foi relido; a nota varia cerca de ±0,5.

## 1. Leitura honesta da meta

- **10/10 não se alcança só editando.** A nota máxima exige reconhecimento externo (revisão por especialistas, uso real com alunos) que o autor não produz sozinho.
- **Sem revisores externos (L1), a nota não passa de cerca de 7.** Só L3, L4, L5 e L7 são trabalho interno.
- **Com L1 e L2 feitos, a estimativa é 7,5 a 8,5.** Acima disso depende de L6 e dos resultados do piloto, que ainda não existem.
- **As faixas de nota são estimativas de julgamento [Hipótese], sem prova.** Só a revisão externa as confirma.
- **Restrições vigentes que o plano respeita:** sem programação no texto principal (decisão de 15/10/2026); neutralidade de fornecedores; formato de partes curtas para leitura com TDAH; fontes públicas primárias com trecho literal conferido; sem imagens antes do texto validado.

## 2. Correção da avaliação anterior

Dois pontos da revisão de 18/11/2026 ficaram imprecisos e mudam o plano:

- **Estatística de avaliação:** o texto não é ausente. A unidade 5.6 tem 5 partes (5.6a–5.6e) com intervalo de confiança, erro-padrão agrupado e amostras pequenas, citando Miller (2024). A comparação pareada também aparece ("paired differences", Miller, arXiv:2411.00640). O que não aparece é método reproduzível (`Wilson` e `bootstrap`: 0 menções). A lacuna é de **profundidade**, não de existência.
- **Prática:** o plano de 2026 já prevê laboratórios "sem programação" e com "escopo próprio" (`planejamento-completo-estudos-engenharia-llms.md`, linhas 36 e 66), e há 96 blocos `Aprofundar:`. A lacuna é que **nenhum laboratório foi escrito**, não que a ideia foi vetada.

## 3. Lacunas, ações e critérios de aceite

Ordem = maior retorno por esforço. Esforço: B (baixo), M (médio), A (alto).

| ID | Lacuna (evidência) | Ação | Critério de aceite observável | Esforço |
|---|---|---|---|---|
| L1 | Todo o conteúdo foi escrito e revisado por LLMs; 26 commits, um autor; `conferir-trechos.py` confere se o trecho existe, não se a interpretação está certa | Revisão técnica por 2–3 engenheiros de LLMs humanos, por capítulo, com planilha de objeções (trecho, objeção, fonte, resolução) | Todo capítulo com parecer registrado; objeções materiais resolvidas ou recusadas com fonte; nomes e escopo de cada revisor documentados | A (depende de pessoas externas) |
| L2 | Sem piloto com leitores reais; leitura nos 3 aparelhos, leitor de tela e papel ainda pendentes (`roadmap.md`) | Piloto com 3–5 leitores do público-alvo em 2 capítulos (um conceitual, um operacional), com tarefa e tempo medidos | Relatório com taxa de acerto nas questões, trechos onde travaram e ajustes feitos; validação manual do `roadmap.md` concluída | M |
| L3 | Profundidade mecânica baixa: `softmax` 0, `FlashAttention` 0, `RLHF` 4, `continuous batching` 2, `tensor parallel` 0 | Novas partes curtas `Aprofundar` (sem excluir o formato atual) em: atenção com a conta (Q·K, softmax, custo quadrático), pós-treino (RLHF, DPO), servir modelos (batching contínuo, paralelismo, PagedAttention) | Cada parte com fonte primária e trecho literal em pacote conferido; uma questão de cálculo ou diagnóstico por parte; `validar-guia.py` sem falha | M |
| L4 | Avaliação sem método reproduzível (5.6 já trata intervalo de confiança, erro-padrão agrupado e diferenças pareadas, só em conceito) | Estender 5.6 com: intervalo para proporção (ex.: Wilson), bootstrap em palavras simples, um exemplo numérico pareado da v1 contra a v2 nos mesmos casos, tamanho de amostra mínimo | Exemplo numérico com dados fictícios da Aurora Educação reproduzível à mão ou em planilha; fonte pública conferida para cada fórmula | B–M |
| L5 | Só 376 questões de múltipla escolha; escolher alternativa não demonstra projetar ou operar (`requisitos-de-formato-html-do-material.md`, linha 85) | Adicionar por capítulo 1 estudo de caso com resposta aberta e rubrica de correção; 1 projeto integrador na Parte III | Rubrica com critérios observáveis; cada caso resolvido por revisor humano (L1) antes de publicar | M |
| L6 | Nenhum laboratório escrito | Trilha de laboratórios separada do texto principal, **sem programação**: executar comandos prontos de runtime, ler logs, medir com planilha | Cada laboratório com pré-requisitos, passos, resultado esperado e tempo; executado do zero uma vez e registrado | A |
| L7 | Dado volátil (preços, modelos, ferramentas) com "consultada em" | Tabela de vigência por afirmação volátil e rotina de revisão trimestral com `conferir-trechos.py` | Lista de itens voláteis com data e dono; primeira rodada executada e registrada em changelog | B |
| L8 | 67 molduras de imagem sem arte | Fim da fila (regra de 13/11/2026): gerar imagens só após L1–L5 estabilizarem o texto | 67 imagens inseridas; PDF regerado e conferido | M |

## 4. Decisões que cabem ao operador

1. **L6 com código?** Uma trilha opcional com programação contraria a decisão de 15/10/2026. Se for desejada, precisa de aprovação explícita e fica fora do guia principal. O plano assume que **não**.
2. **Quem revisa (L1)?** O guia não define revisores nem orçamento. Sem pessoas externas, a nota não passa de cerca de 7 (seção 1).
3. **Crescimento do texto:** L3, L4 e L5 aumentam o guia depois de um enxugamento de 9%. Proposta: entrar só como `Aprofundar`, sem aumentar o caminho obrigatório de leitura.

## 5. Ordem e dependências

1. L1 e L2 começam cedo, porque seus achados reorientam o resto.
2. L3, L4 e L5 em paralelo, cada um com pacote de fontes próprio e `conferir-trechos.py`.
3. L7 junto com o fechamento de cada capítulo.
4. L6 depois que L3 e L4 definirem o que vale praticar.
5. L8 por último.

Validação a cada entrega: `ferramentas/validar-guia.py --guia guia-engenharia-llms.html`, `conferir-trechos.py` nos pacotes novos, `executar-trechos-de-codigo.py`, auditoria no navegador em 320 px e regeração do PDF. Atualizar `CLAUDE.md`, `README.md`, `roadmap.md` e criar um `changelog-*.md` por entrega.

## 6. O que não fazer

- Não reescrever capítulos inteiros nem multiplicar partes sem fonte primária conferida.
- Não citar autores ou livros como se fossem fonte sem leitura e trecho literal conferido.
- Não nomear o Router nem expor dados reais; exemplos seguem com a Aurora Educação (fictícia).
- Não declarar nota nova antes de L1 e L2: nota interna feita pelo mesmo processo que escreveu o guia não prova nada.

claude - pessoal, 19/11/2026.
