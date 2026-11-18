# Changelog — Pendências finais do guia, exceto imagens e aparelhos reais (18/11/2026)

## Escopo

Pedido do operador: corrigir as pendências abertas e fora do escopo, menos a geração das 67 imagens e a validação manual nos três aparelhos reais.

## Mudanças

- **Viés de tamanho nas questões (pendência 1):** 59 questões das Partes I–II (`p1`, `p2`, `c2q`, `p3`, `c3q`, `p4`, `c4q`, `p5`, `c5q`) tinham a alternativa correta estritamente mais longa; 130 alternativas reescritas (enunciado correto encurtado e/ou distratores alongados com detalhe plausível), sem mudar gabaritos nem explicações. Resultado: 0/376 com a correta estritamente mais longa; gabaritos `94/94/94/94`; 12 empates no topo (fora desta lista, aceitos). Resíduo: a correta é a 2ª mais longa em 165/376 questões (44%), viés menor e menos detectável; não tratado.
- **`<dfn>` duplicados (pendência 2):** removida a marcação em `tokens` (4.1), `tokenizador` (4.3) e `temperatura` (4.5), mantendo a definição original em 1.1, 1.3 e 1.4 (Glossário já cita essas unidades). `Cliente` e `Servidor` não eram duplicatas: 2.1 define o conceito de rede e 10.6 define `Cliente`/`Servidor` do MCP (entradas próprias no Glossário). `<dfn>` únicos: 0 repetições.
- **Acessibilidade:** `span.page-number` ganhou `role="img"` (corrige `aria-prohibited-attr` do axe nos 316 números de página); `ferramentas/renumerar-paginas.py` ajustado ao novo marcado. `color-contrast` segue como `incomplete` (limite do axe com `<pre>` sem fundo próprio e rolagem): cálculo manual `--ink #000` sobre `--paper #f5f1e8` ≈ 18:1.
- **Ferramenta nova:** `ferramentas/auditar-guia-navegador.mjs` (reflow 320 px, clique em **todas** as 376 questões com checagem de veredito, letra correta, região `aria-live` e travamento, e `axe-core` em 1280×800 e 320×640). Recebe caminhos por argumento, sem caminhos pessoais.
- **`[Não verificado]`:** 13 afirmações numéricas/técnicas conferidas online e registradas em `pacote-de-fontes-conferencia-final-2026-11-18.md` (25.000 tokens do Claude Code, 5,7%→1,9%, 150/20, 200 mil tokens, 55K, 3–5 e 30–50 ferramentas, 150 mil→2 mil, MTEB 8/58/112, Chroma 18 LLMs, Ollama e llama.cpp), sem divergência com o texto. Os demais itens listados nos changelogs das Partes II e III (cerca de cem afirmações menores) seguem como lacuna declarada.
- **Código ilustrativo:** os 21 blocos `ilustrativo` continuam sem execução por desenho (pseudo-pedidos e prompts).

## Validação (18/11/2026)

- `renumerar-paginas.py`: 316 páginas, nada a mudar. `validar-guia.py`: `16 OK, 0 FALHA`. `executar-trechos-de-codigo.py`: `0 FALHA`, 21 ilustrativos.
- `auditar-guia-navegador.mjs` (chromium-1254): reflow `docScroll = bodyScroll = 320`, 0 estouros, 0 erros de página; 376/376 questões com veredito correto e 0 falhas; `axe-core` `45 passes`, 0 violações, 1 `incomplete` (`color-contrast`).
- PDF regerado (Chrome, `--headless=new --no-pdf-header-footer --print-to-pdf`): 533 páginas A4 (antes 532); p. 100 renderizada e inspecionada.
- Hashes: HTML `0df68a358f415004`; PDF `23fe2a8bfda2c697`.

## Pendente

Geração das 67 imagens em aquarela; validação manual nos três aparelhos reais, com leitor de tela e impressão física; regerar o PDF depois das imagens.

Assinatura: claude - pessoal
