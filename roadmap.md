# Roadmap — Pendências para fechamento final

Estado atual (`18/11/2026`, após revisão geral `9556cda`, expansão do Grupo A `a0fb31c` e enxugamento global + compactação de impressão `ced628f` em `main`): os 16 capítulos (`316` páginas lógicas, `376` questões equilibradas `94/94/94/94`, `397` entradas `<dt>` no glossário, `682` links externos, `67` molduras `data-imagem=`) e todas as validações automatizadas (`validar-guia.py`, `executar-trechos-de-codigo.py`, Chrome `158` / Playwright `chromium-1254` `reflow 320 px` com `0` estouros, questões fundidas com `aria-live`, `axe-core 4.11.0` com `45 passes` e `0` violações em `1280×800` e `320×640`, e PDF A4 de `531` páginas) estão concluídos.

## Pendências abertas

1. **Imagens em aquarela (`67` molduras `data-imagem=`):**
   - Gerar e inserir as 67 ilustrações em aquarela de fantasia medieval (`1056×704`, sem texto, letras, logotipos ou personagens reconhecíveis) seguindo `requisitos-de-formato-html-do-material.md` (§8), substituindo as molduras atuais em `guia-engenharia-llms.html`.
   - Ao concluir, regerar `guia-engenharia-llms.pdf` via Chrome headless, inspecionar amostras visuais e revalidar com `ferramentas/validar-guia.py`.

2. **Validação manual em uso real (operador):**
   - **Três aparelhos reais:** leitura confortável no Galaxy S24 (retrato e paisagem), Acer Nitro 5 (`15"` / `1080p`) e tela APSRV (`55"` / `4K`).
   - **Leitor de tela real:** conferência de navegação, tabelas com `.rolagem`, blocos de código e retorno `aria-live` das questões.
   - **Impressão física:** conferência em papel A4 (quebras de página de abertura e questões, margens e legibilidade).

Assinatura: agy - ap (Gemini 4 Hydrogen High), atualizado em 18/11/2026.
