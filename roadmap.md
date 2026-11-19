# Roadmap — Pendências para fechamento e evolução do guia

Estado atual (`19/11/2026`, `main`): os 16 capítulos (`316` partes, `175.906` palavras em partes, `376` questões equilibradas `94/94/94/94`, `141` tabelas todas com `.rolagem`, `402` termos `<dt>` no glossário, `395` `<dfn>`, `722` links externos / `275` URLs únicas, `67` molduras `data-imagem=`), todas as validações automatizadas (`guia.py fechar` com `0` falhas, `executar-trechos-de-codigo.py` `0` falhas, `auditar-guia-navegador.mjs` em `320 px` com `0` estouros, `376/376` questões com `aria-live` e `axe-core` com `0` violações), o PDF A4 de `534` páginas (`sha256` `10ff8c03dd8dfe83`) e as ferramentas sem LLM (`ferramentas/guia.py` e `ferramentas/fontes.py`) estão concluídos.

## Decisões abertas do operador

Definições necessárias na seção 4 de [plano-de-lacunas-para-nota-10-2026-11-19.md](plano-de-lacunas-para-nota-10-2026-11-19.md) para destravar a próxima fase:
- **L6:** confirmar se a trilha de laboratórios segue sem programação (fora do texto principal) ou se haverá trilha opcional com código.
- **L1:** definir os 2–3 revisores técnicos humanos de engenharia de LLMs.
- **L3–L5:** confirmar se as novas partes de profundidade mecânica, estatística reproduzível e estudos de caso entram apenas como blocos `Aprofundar`.

## Pendências de evolução e fechamento

Ordem alinhada a `plano-de-lacunas-para-nota-10-2026-11-19.md`:

1. **L1 — Revisão técnica humana externa:** parecer por capítulo e planilha de objeções com fontes.
2. **L2 — Piloto e validação manual em uso real (operador):**
   - Piloto com 3–5 leitores em dois capítulos (um conceitual, um operacional).
   - **Três aparelhos reais:** leitura confortável no Galaxy S24 (retrato e paisagem), Acer Nitro 5 (`15"` / `1080p`) e tela APSRV (`55"` / `4K`).
   - **Leitor de tela real:** conferência de navegação, tabelas com `.rolagem`, blocos de código e retorno `aria-live` das questões.
   - **Impressão física:** conferência em papel A4 (quebras de página de abertura e questões, margens e legibilidade).
3. **L3, L4 e L5 — Profundidade técnica, avaliação reproduzível e casos abertos:**
   - L3: atenção (Q·K, softmax, custo quadrático), pós-treino (RLHF, DPO) e serviço (batching contínuo, paralelismo, PagedAttention).
   - L4: estender a unidade 5.6 com método reproduzível (Wilson, bootstrap, exemplo pareado da Aurora Educação, tamanho mínimo de amostra).
   - L5: 1 estudo de caso aberto com rubrica por capítulo e 1 projeto integrador na Parte III.
4. **L7 — Tabela de vigência e revisão periódica:**
   - Implementar o subcomando `vigencia` das `275` URLs únicas em `ferramentas/fontes.py` (pendente de aprovação de L7) e tratar páginas alteradas na origem (ex.: `openai-model-selection`, atualizada após 17/11/2026) e as 25 fontes bloqueadas ao download automático via busca da fronteira.
5. **L6 — Trilha prática separada:** laboratórios após definição de L3 e L4.
6. **L8 — Imagens em aquarela (`67` molduras `data-imagem=`):**
   - Executar somente após L1–L5 estabilizarem o texto: gerar e inserir as 67 ilustrações em aquarela de fantasia medieval (`1056×704`, sem texto, letras, logotipos ou personagens reconhecíveis) conforme `requisitos-de-formato-html-do-material.md` (§8).
   - Ao concluir, fazer backup prévio em `arquivo/antes-<motivo>-<data>/`, regerar o PDF via `python3 -I ferramentas/guia.py pdf --substituir --motivo <motivo>`, inspecionar amostras visuais e revalidar com `guia.py fechar`.

Assinatura: agy - ap (Gemini 4 Hydrogen High), atualizado em 19/11/2026.
