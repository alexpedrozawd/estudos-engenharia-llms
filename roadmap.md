# Roadmap — Pendências para fechamento e evolução do guia

Estado atual (`24/11/2026`, `main`): **Fases 0–3 concluídas e etapa preparatória da Fase 4 concluída.** Guia com `18` capítulos (`6` e `15` ampliados para `18` partes cada), `377` páginas lógicas, `445` questões (`111/111/112/111`), `26` blocos executáveis, `501` termos no Glossário, estudo de caso com rubrica por capítulo, `18` laboratórios e projeto integrador (`82` testes offline), `171` fontes web atuais em cache (`0` vencidas/divergentes, `25` fora do cache por bloqueio externo), revisão técnica `L1` concluída por agentes de IA, roteiro `L2` preparado para telas, PDF provisório de `654` páginas; `guia.py fechar` com `0` falhas e auditoria `320 px`/`axe-core` sem violações. Ver [changelog-fase-4-ampliacao-fontes-l1-l2-2026-11-24.md](changelog-fase-4-ampliacao-fontes-l1-l2-2026-11-24.md).

## Decisões definidas pelo operador (23 e 24/11/2026)

- **Fontes primárias e secundárias:** os dois livros de Chip Huyen (*AI Engineering* e *Designing Machine Learning Systems*) passam a ser fontes primárias estruturantes, complementados pelo material e pelas fontes web de 2026 já conferidas.
- **Programação incluída em duas camadas:** snippets executáveis curtos em Python padrão/`unittest.mock` no HTML (`executar-trechos-de-codigo.py`) + `18` laboratórios e projeto integrador em `laboratorios/`.
- **Estrutura curricular:** reorganização para **18 capítulos** em 3 partes (Caps. 1–5; Caps. 6–11 incluindo Cap. 6 novo de Engenharia de Dados/Datasets; Caps. 12–18 incluindo Cap. 15 novo de Fine-tuning/Quantização/Destilação), preservando partes curtas para TDAH; Caps. 6 e 15 ampliados de `12` e `7` para `18` partes cada em 24/11/2026.
- **Decisões de 24/11/2026 (Fase 4):** revisão técnica (`L1`) confiada a agentes de IA (Gemini/Claude); validação física (`L2`) restrita a **telas e leitor de tela** (papel A4 desconsiderado); geração das imagens em aquarela (`L8`) mantida como passo final.

## Pendências de execução (após Handoff)

Ordem alinhada a [planejamento-reestruturado-2026-11-23.md](planejamento-reestruturado-2026-11-23.md) e [plano-de-lacunas-para-nota-10-2026-11-19.md](plano-de-lacunas-para-nota-10-2026-11-19.md):

1. ✅ **Fase 1 — Fichamento local dos livros (`cache-fontes/livros/fichamentos/`):** leitura contínua capítulo a capítulo via `ferramentas/livros.py ler` (com `pagina-png` pontual em figuras/tabelas/fórmulas), nunca carregando os livros inteiros nem versionando trechos protegidos no Git.
2. ✅ **Fase 2 — Backup e estrutura de laboratórios:** copiar HTML e PDF atuais para `arquivo/antes-reestruturacao-huyen-<data>/` e criar a pasta `laboratorios/` com suíte determinística por mocks.
3. ✅ **Fase 3 — Execução por lotes (Caps. 1–18 + `L3`, `L4`, `L5`, `L6`, `L7`):**
   - Atualizar e criar os 18 capítulos com snippets executáveis `data-executavel="true"`, estudos de caso abertos com rubrica (`L5`) e 18 laboratórios + projeto integrador (`L6`).
   - Incluir profundidade mecânica (`L3`), estatística reproduzível na unidade 5.6 (`L4`), subcomando `vigencia` em `ferramentas/fontes.py` (`L7`, incluindo atualização de `openai-model-selection`) e validação contínua com `guia.py fechar`.
- ✅ **Pendências herdadas da Fase 3 resolvidas em 24/11/2026:** Caps. 6 e 15 ampliados para `18` partes cada; reconferência web fechada com `171` chaves atuais, `0` vencidas/divergentes e `25` fora do cache por bloqueio externo.
4. **Fase 4 — Revisão (`L1`), piloto/validação em telas (`L2`) e arte (`L8`):**
   - ✅ Revisão técnica `L1` por agentes de IA (subagentes somente leitura sobre Caps. 6, 9, 15, Sumário, Glossário e Referências, com correções aplicadas e validadas).
   - ⏳ Piloto com 3–5 leitores + validação em telas (smartphone, tablet, notebook, TV 55" 4K) e leitor de tela (`L2`, sem papel A4): roteiro pronto em [roteiro-piloto-e-validacao-em-telas-2026-11-24.md](roteiro-piloto-e-validacao-em-telas-2026-11-24.md), aguardando execução manual do operador.
   - ⏳ Geração das `73` imagens em aquarela (`L8`, passo final), regeração do PDF definitivo via `guia.py pdf --substituir --motivo ...` e validação final completa (`auditar-guia-navegador.mjs` + `guia.py fechar`).

Assinatura: agy - ap (Gemini 4 Hydrogen High), atualizado em 23/11/2026; atualizado em 24/11/2026 por claude - pessoal (fechamento da Fase 3) e agy - ap (ampliação dos Caps. 6 e 15, reconferência de fontes, L1 e roteiro L2).
