# Changelog — Capítulo 2 (Arquitetura de sistemas com LLM)

Data: 15/10/2026. Pasta fora de repositório Git: sem commit nem push. Capítulo redigido por claude - pessoal (Sonnet 5.5 High, effort declarado pelo operador) e lido por claude - pessoal (Opus 5.5 High).

## 1. O que entrou no guia
- Abertura do capítulo (página 11), seis unidades (páginas 12 a 17), cinco questões (página 18), glossário (página 19, 82 termos) e referências (página 20). `guia-engenharia-llms.html` tem 20 páginas.
- Unidades: 2.1 Componentes e fronteiras; 2.2 A chamada ao modelo; 2.3 Streaming e latência; 2.4 Limites, erros e novas tentativas; 2.5 Estado e persistência; 2.6 Simultaneidade e capacidade. Formato do Capítulo 1 (objetivo, conceito, funcionamento, exemplo resolvido, aplicação e limites, pergunta com feedback, ponto de retomada, fontes).
- Dois textos para ler, sem programa e rotulados *ilustrativo, não executado*: pedido e resposta com corte por limite de saída (2.2) e resposta 429 com `retry-after` (2.4). Diagramas só com `ol.fluxo` e tabelas; nenhum componente novo.
- Questões (gabarito C, A, D, B, A): Q1 fácil (2.1), Q2 fácil (2.2/2.5), Q3 média (2.2/2.3), Q4 média (2.4/2.6), Q5 difícil (2.1, 2.4 a 2.6).
- 37 termos novos no glossário (7 na 2.1 e 30 nas demais; de 45 para 82) e 9 grupos de referências novos (Ollama, llama.cpp, MDN ×2, Anthropic, OpenAI, IETF, AWS, Google SRE), mais a nota sobre código local lido.
- Navegação encadeada (página 10 → capítulo 2 → 2.1 … 2.6 → questões → glossário → referências); sumário e abertura com link para todas as unidades.

## 2. Decisões e desvios
- O operador aprovou o plano e o nome do módulo, e depois nível de entrada, diagrama e texto para ler ("Aprovo os 3 itens"). Texto para ler da 2.2: limite de saída 12 e tokens de saída 12 (a proposta inicial dizia 200, incoerente com um texto curto).
- vLLM e a página de perguntas frequentes do Ollama não extraíram: o capítulo não afirma nada sobre paralelismo do Ollama e usa o llama.cpp como servidor local. "Tempo até o primeiro token" é termo de trabalho do livro, sem fonte.
- Exemplos do Router e do webhook da Nanda Mac: lidos em cópia somente leitura (`router-main`, `router-database`, `router-queue-worker`, `pay-webhook-route`, `docs09`), citados como estrutura e marcados *verificado no código local*; nada executado, sem nome de fornecedor ("gateway de pagamento").
- Pacote de fontes: de 109 para 126 trechos, todos aprovados por `conferir-trechos.py` (campos do exemplo, classes de status, `Retry-After`, quatro casos do Router sobre repetição e reinício, `message_delta`, reabastecimento contínuo, expectativas a verificar).
- Tamanho: 2.1 1.336; 2.2 1.359; 2.3 1.252; 2.4 1.382; 2.5 1.354; 2.6 1.286 (Capítulo 1: 1.153 a 1.325). A 2.4 ficou 32 palavras acima do teto de 1.350 e não foi aparada para não perder conteúdo.

## 3. Leitura do Opus (Bloco 3)
Nenhum erro que exigisse reescrever. Correções: etiquetas novas explicadas na abertura; "leva três coisas" → "costuma levar" (2.2); "recomenda" → "sugere considerar" e fim da transmissão como motivo de parada mais sinal de encerramento (2.3); linha de status completa e tabela de tempo esgotado ajustada (2.4); "ausência de filas" como expectativa a verificar (2.6). Detalhes na §9 do plano.

## 4. Validação executada em 15/10/2026
- `python -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: 16 OK, 0 falha.
- `conferir-trechos.py`: 126 aprovados, 0 reprovados.
- Chrome (Playwright, `channel="chrome"`, venv temporário): sem rolagem horizontal em 320, 480, 768, 1024, 1280 e 1920 px; nenhum elemento fora de região de rolagem em 320 e 1280 px; axe-core 4.10.2 sem violações (incompleta conhecida: `aria-prohibited-attr` nos números de página); questões dos dois capítulos travam na primeira resposta e dão retorno (5 de 5 em cada); 92 links internos com alvo.
- Tags equilibradas; ids sem duplicata; Capítulo 1, CSS e script comparados com a versão anterior ao capítulo 2: idênticos, exceto a navegação da página 10 (agora aponta para o capítulo 2) e o sumário.
- Não verificado: Galaxy S24, Nitro 5 e APSRV reais; conforto de leitura.

## 5. Hashes finais (SHA-256, 16 primeiros caracteres)
`guia-engenharia-llms.html` d900f667fda6ef0c; `pacotes-de-fontes-capitulo-2.md` 577aee116a3aec9c; plano mestre e4e071cac7dbfed4; `requisitos-de-formato-html-do-material.md` a4f5348c5909b146; contextos de estudo do Router 5fbb64b2fb19f78a e da Nanda Mac a7aebd9addaa0383; Capítulo 1 (plano 43b3d5d71d5d9d18, pacote bbb9c5bef5767b44, changelog c85d783156deefa0) e ferramentas inalterados.

## 6. Pendências abertas
Aparelhos reais; título de tabela cortado em 320 px dentro da região com rolagem e `aria-label` nos números de página; referência a `docs/09` sem link público; fontes "não lido" do Capítulo 1; top-k e top-p no plano do Capítulo 1; "busca por símbolos" do módulo 10 (decidir no plano dele); fontes extraídas do capítulo 2 só na pasta temporária da sessão (para reconferir, baixar de novo as URLs da §3 do plano).

claude - pessoal, 15/10/2026
