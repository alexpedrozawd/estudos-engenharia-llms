# Roadmap — Pendências para fechamento e evolução do guia

Estado atual (`24/11/2026`, `main`): **Fases 0–3 concluídas.** Guia com `18` capítulos, `360` páginas lógicas, `427` questões, `22` blocos executáveis, estudo de caso com rubrica por capítulo, `18` laboratórios e projeto integrador (`82` testes offline), PDF provisório de `628` páginas; `guia.py fechar` com `0` falhas e auditoria `320 px`/`axe-core` sem violações. Ver [changelog-fase-3-reestruturacao-huyen-2026-11-24.md](changelog-fase-3-reestruturacao-huyen-2026-11-24.md).

## Decisões definidas pelo operador (23/11/2026)

- **Fontes primárias e secundárias:** os dois livros de Chip Huyen (*AI Engineering* e *Designing Machine Learning Systems*) passam a ser fontes primárias estruturantes, complementados pelo material e pelas fontes web de 2026 já conferidas.
- **Programação incluída em duas camadas:** snippets executáveis curtos em Python padrão/`unittest.mock` no HTML (`executar-trechos-de-codigo.py`) + `18` laboratórios e projeto integrador em `laboratorios/`.
- **Estrutura curricular:** reorganização para **18 capítulos** em 3 partes (Caps. 1–5; Caps. 6–11 incluindo Cap. 6 novo de Engenharia de Dados/Datasets; Caps. 12–18 incluindo Cap. 15 novo de Fine-tuning/Quantização/Destilação), preservando partes curtas para TDAH.
- **Pendente de definição externa:** definir 2–3 revisores técnicos humanos (`L1`) após estabilizar o novo texto.

## Pendências de execução (após Handoff)

Ordem alinhada a [planejamento-reestruturado-2026-11-23.md](planejamento-reestruturado-2026-11-23.md) e [plano-de-lacunas-para-nota-10-2026-11-19.md](plano-de-lacunas-para-nota-10-2026-11-19.md):

1. ✅ **Fase 1 — Fichamento local dos livros (`cache-fontes/livros/fichamentos/`):** leitura contínua capítulo a capítulo via `ferramentas/livros.py ler` (com `pagina-png` pontual em figuras/tabelas/fórmulas), nunca carregando os livros inteiros nem versionando trechos protegidos no Git.
2. ✅ **Fase 2 — Backup e estrutura de laboratórios:** copiar HTML e PDF atuais para `arquivo/antes-reestruturacao-huyen-<data>/` e criar a pasta `laboratorios/` com suíte determinística por mocks.
3. ✅ **Fase 3 — Execução por lotes (Caps. 1–18 + `L3`, `L4`, `L5`, `L6`, `L7`):**
   - Atualizar e criar os 18 capítulos com snippets executáveis `data-executavel="true"`, estudos de caso abertos com rubrica (`L5`) e 18 laboratórios + projeto integrador (`L6`).
   - Incluir profundidade mecânica (`L3`), estatística reproduzível na unidade 5.6 (`L4`), subcomando `vigencia` em `ferramentas/fontes.py` (`L7`, incluindo atualização de `openai-model-selection`) e validação contínua com `guia.py fechar`.
- **Pendências registradas na Fase 3:** Caps. 6 e 15 (novos) com `12` e `7` partes, contra `17`–`22` nos demais (ampliar só com decisão do operador); `fontes.py vigencia` com `97` hashes divergentes e `25` fontes fora do cache, para reconferir na Fase 4.
4. **Fase 4 — Revisão externa (`L1`), piloto/validação manual (`L2`) e arte (`L8`):**
   - Revisão técnica humana por capítulo (`L1`).
   - Piloto com 3–5 leitores + validação nos três aparelhos reais (Galaxy S24, Acer Nitro 5, tela 55" 4K), leitor de tela e papel A4 (`L2`).
   - Geração das imagens em aquarela (`L8`, por último, após texto estabilizado), regeração do PDF via `guia.py pdf --substituir --motivo ...` e validação final completa (`auditar-guia-navegador.mjs` + `guia.py fechar`).

Assinatura: agy - ap (Gemini 4 Hydrogen High), atualizado em 23/11/2026; atualizado em 24/11/2026 por claude - pessoal (fechamento da Fase 3).
