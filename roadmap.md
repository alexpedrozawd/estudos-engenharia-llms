# Roadmap — Pendências para fechamento final

Estado atual (`17/11/2026`, commit `acdcb4c` em `main`): os 16 capítulos (`325` páginas lógicas, `385` questões equilibradas, `375` termos no glossário, `657` links externos) e as validações automatizadas (`validar-guia.py`, `conferir-trechos.py`, `reflow` em `320 px`, `axe-core` e PDF de `968` páginas A4) estão concluídos.

## Pendências abertas

1. **Imagens em aquarela (`67` molduras `data-imagem=`):**
   - Gerar e inserir as 67 ilustrações em aquarela de fantasia medieval (`1056×704`, sem texto, letras, logotipos ou personagens reconhecíveis) seguindo `requisitos-de-formato-html-do-material.md` (§8), substituindo as molduras atuais em `guia-engenharia-llms.html`.
   - Ao concluir, regerar `guia-engenharia-llms.pdf` via Chrome headless, inspecionar amostras visuais e revalidar com `ferramentas/validar-guia.py`.

2. **Validação manual em uso real (operador):**
   - **Três aparelhos reais:** leitura confortável no Galaxy S24 (retrato e paisagem), Acer Nitro 5 (`15"` / `1080p`) e tela APSRV (`55"` / `4K`).
   - **Leitor de tela real:** conferência de navegação, tabelas com `.rolagem`, blocos de código e retorno `aria-live` das questões.
   - **Impressão física:** conferência em papel A4 (quebras de página de abertura e questões, margens e legibilidade).

Assinatura: agy - ap (Gemini 4 Hydrogen High), 17/11/2026.
