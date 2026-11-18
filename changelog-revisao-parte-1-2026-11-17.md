# Revisão da Parte I (Capítulos 1 a 5) — 17/11/2026

Autoria: claude - pessoal (Sonnet 5.5 High). Pedido do operador: revisar cada capítulo da Parte I isoladamente (`/revisar`), conferir pelas fontes já salvas, corrigir tudo e fechar com PDF, commit e push. Método: um subagente somente leitura por capítulo, com lista de checagem comum (`requisitos-de-formato-html-do-material.md` §8–§9, planejamentos, pacotes de fontes, remissões, gabaritos, neutralidade); todo achado foi conferido no HTML antes de editar. Nenhuma URL foi baixada.

## Resultado

- 73 linhas alteradas em `guia-engenharia-llms.html` (`git diff --stat`), inclusive 2 entradas do glossário (KV cache e PagedAttention). Estrutura intacta: 325 páginas lógicas, 16 OK / 0 FALHA no `validar-guia.py`, PDF com 963 páginas A4.
- Sem achado de estrutura, gabarito, neutralidade, link, âncora ou tamanho de parte (nenhuma parte acima de 520 palavras até a "Pergunta").

## Correções por causa

| Causa | Onde | Ajuste |
|---|---|---|
| Remissões com numeração anterior à inserção do Cap. 6 | Caps. 1, 4 e 5 e glossário | "módulo N" → "capítulo N" com o número atual (6→7, 7→8, 8→9, 9→10, 12→13, 13→14, 14→15, 15→16; 4 e 5 mantidos), por ser o termo usado nas Partes II e III |
| Introdução desatualizada | Introdução | Engenharia de grafos na Parte II; "em todos os capítulos" no lugar de "capítulos 1 a 5"; "os 16 capítulos estão prontos" |
| Promessa sem destino | 1.7b | "decisão, embeddings e rerankers ... capítulos 5, 10 e 13, ainda não escritos" → embeddings e rerankers no capítulo 11 (a "decisão" não tem capítulo próprio) |
| Rótulo de processo editorial | Cap. 2 (notas de fonte) | "nesta rodada" removido; frase de retirada de afirmação apagada |
| Enunciados e explicações | p1-5a, 2.6a, p3-5c, c4q6 | pronome "it" explicado; "em média" removido; alternativa C e explicação alinhadas ao não-objetivo; "quatro falhas" corrigido |
| Contradição interna do Cap. 3 | 3.4d, 3.3c, 3.2c, 3.6b | quem aceita passou a ser a direção de operações (quem executa não se autoaceita); resumo da 3.3c bate com a tabela; 2% marcado como limite provisório |
| Fidelidade à fonte | nota J&M (Cap. 1), NIST e NASA (Cap. 3) | seção citada precisa; "praticamente a lista" → "pontos em comum"; "proibidos" → "não verificáveis" |
| "Sobre as fontes" incompleto | Cap. 3, 4, 5 | acrescentados NN/g, OpenAI, Google, modelos abertos e datas de consulta reais |
| Redação | Caps. 1, 2, 3 e 5 | unidade 1.6 não é "capítulo"; "O fluxo" sem referente; frase truncada; "regressão" definida; dfn "resultado esperado" distinguido; "fronteira" × "interface"; "fecham a Parte I" |
| Tabela incompleta | Cap. 5, tabela da 5.4d | linha do critério 5 (tempo e custo) |

## Pendências conhecidas (não alteradas)

- Sem trecho literal salvo (marcados [Não verificado] na revisão): "v2" do DeepSeek-R1 sem ano; Ouyang (1,3B × GPT-3 175B); Thoughtworks (1.7); notas 1936–1999 do Cap. 1 (Sentence-BERT, MTEB, Llama Guard, Mamba, LLaDA, Mercury, Belcak, Genie 3, π0, Gemini Robotics 2); "Source realistic tasks…" e "Using 'it seems like it's working'…" (Cap. 3); "OpenAI is deprecating the Evals platform" (5.5). Para fechar, reabrir as URLs e atualizar o pacote.
- OpenAI: as avaliações ficam somente leitura em 31/10/2026 (data já passada) e a reconferência da página convém antes de 30/11/2026.
- 3.2b/3.2c: "o módulo de eficiência volta a ele" (custo de medir a base): [Hipótese], o Cap. 16 trata de tokens e custo por chamada, não do custo de medir.
- Registro apenas: questões c2q1/c2q2/c2q3/c2q6 repetem quase por inteiro perguntas de parte; em 11 das 29 questões do Cap. 1 a alternativa correta é a mais longa.
- Rótulo "Cap. 21" nas notas do Cap. 2 é o capítulo 21 do livro *Site Reliability Engineering* (Google), não do guia; mantido.

## Hashes (16 caracteres)

- `guia-engenharia-llms.html`: antes `15fbd07700d2d531` → depois `8bc0ab88dd0f2fb1` (backup em `arquivo/antes-revisao-parte-1-2026-11-17/`, fora do Git).
- `guia-engenharia-llms.pdf`: `fbc329c4b91597aa` (Chrome for Testing 158, `--headless=new --no-sandbox --no-pdf-header-footer --print-to-pdf`, 963 páginas).

Assinatura: claude - pessoal.
