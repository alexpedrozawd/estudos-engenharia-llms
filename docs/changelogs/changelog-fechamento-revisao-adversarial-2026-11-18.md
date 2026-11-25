# Changelog — Fechamento da revisão adversarial (18/11/2026)

## Escopo

Etapas 1–3 (agy - ap): revisão linha a linha da Parte III (Caps. 12–16), `#glossario` e `#referencias` contra os pacotes de fontes e o Grupo A. Etapa 4 (claude - pessoal): validações finais, PDF e Git.

## Mudanças no `guia-engenharia-llms.html`

- Parte III: fidelidade às fontes, `<dfn>`, qualificadores inline, remissões, introdução/escalonamento de `14.5a`; reescrita de `c12q4`, `c13q5`, `c14q4`–`c14q6`.
- Viés de tamanho removido das 122 questões da Parte III (0/122); gabaritos `31/30/30/31`.
- Notas de fonte da Parte III com pontuação final padronizada (máx. 77 palavras; máx. 402 palavras antes de `Pergunta`).
- Glossário: 402 termos, 0 erros alfabéticos, cobertura dos `<dfn>` da Parte III.
- Referências: contagens dos Caps. 6–11 e links faltantes; 265 URLs únicas nos Caps. 1–16, 0 ausentes.

## Validação (Etapa 4, reexecutada em 18/11/2026)

- `renumerar-paginas.py`: 316 páginas em sequência, nada a mudar.
- `validar-guia.py`: `16 OK, 0 FALHA`.
- `executar-trechos-de-codigo.py`: `0 FALHA`, `21` ilustrativos não executados, 0 blocos sem classe.
- Playwright `chromium-1254` (`/tmp/auditar-guia-playwright.mjs`): reflow em `320 px` com `docScroll = bodyScroll = 320`, `0` estouros, `0` erros de página; 8 questões novas do Grupo A com `aria-live` funcional; `axe-core`: `45 passes`, `0 violations`, `2 incomplete` pré-existentes.
- PDF: Chrome `chromium-1254 --headless=new --no-pdf-header-footer --print-to-pdf`, `532` páginas A4 (`12.602.214` bytes; antes `531`); amostras das p. 300 e 500 inspecionadas por `pdftoppm`.
- Hashes: HTML `2762792470a42044…`; PDF `60d1a33d445d56af…`.

## Pendente (decisão do operador; não alterado)

Achados independentes herdados das Partes I–II (fora do escopo das Etapas 1–3):

- 60 questões com a alternativa correta mais longa (`p1`:5, `p2`:7, `c2q`:2, `p3`:15, `c3q`:4, `p4`:3, `c4q`:1, `p5`:16, `c5q`:6, `c9q`:1).
- 5 `<dfn>` duplicados: tokens, tokenizador, temperatura, cliente, servidor.
- Imagens em aquarela (67 molduras) e testes nos três aparelhos reais seguem pendentes.

Assinatura: agy - ap (interrompido por cota; Etapas 1–3)
Assinatura: claude - pessoal (Etapa 4)
