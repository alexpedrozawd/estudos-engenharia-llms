# Roadmap — Pendências para fechamento final

Estado atual (`18/11/2026`, após revisão geral `9556cda` e expansão do Grupo A em `main`): os 16 capítulos (`333` páginas lógicas, `393` questões, `397` entradas `<dt>` no glossário, `682` links externos) e as validações automatizadas disponíveis (`validar-guia.py`, `executar-trechos-de-codigo.py`, `conferir-trechos.py` e PDF de `989` páginas A4) estão concluídos.

## Pendências abertas

1. **Validação automatizada em navegador das 8 partes novas do Grupo A (`2.3d`, `4.5d`, `5.6e`, `10.6d`, `11.3d`, `11.4c`, `13.6d`, `15.6d`):**
   - Rodar novamente `reflow` em `320 px` e `axe-core` quando `playwright` estiver disponível no ambiente (as 326 seções anteriores já haviam passado sem violações no fechamento de 17/11/2026).

2. **Imagens em aquarela (`67` molduras `data-imagem=`):**
   - Gerar e inserir as 67 ilustrações em aquarela de fantasia medieval (`1056×704`, sem texto, letras, logotipos ou personagens reconhecíveis) seguindo `requisitos-de-formato-html-do-material.md` (§8), substituindo as molduras atuais em `guia-engenharia-llms.html`.
   - Ao concluir, regerar `guia-engenharia-llms.pdf` via Chrome headless, inspecionar amostras visuais e revalidar com `ferramentas/validar-guia.py`.

3. **Validação manual em uso real (operador):**
   - **Três aparelhos reais:** leitura confortável no Galaxy S24 (retrato e paisagem), Acer Nitro 5 (`15"` / `1080p`) e tela APSRV (`55"` / `4K`).
   - **Leitor de tela real:** conferência de navegação, tabelas com `.rolagem`, blocos de código e retorno `aria-live` das questões.
   - **Impressão física:** conferência em papel A4 (quebras de página de abertura e questões, margens e legibilidade).

Assinatura: agy - ap (Gemini 4 Hydrogen High), atualizado em 18/11/2026.
