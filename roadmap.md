# Roadmap — Pendências para fechamento e evolução do guia

Estado atual (`24/11/2026`, `main`): **Fases 0–3, consolidação editorial (Blocos 1–4) e Fase 5A concluídas.** Guia com `18` capítulos, `385` páginas lógicas, `453` questões (`113/113/114/113`), `26` blocos executáveis, `528` termos no Glossário, estudo de caso com rubrica por capítulo, `18` laboratórios e projeto integrador (`84` testes offline; adaptadores HTTP reais opcionais em `laboratorios/comum/cliente_llm.py`), `205` fontes web atuais em cache (`0` vencidas/divergentes; `18` registradas como consulta manual por bloqueio externo), `guia.py fechar` e `auditar-guia-navegador.mjs` com `0` falhas; PDF provisório de `657` páginas mantido até a Fase 5C. Ver [changelog-fase-5a-lacunas-2026-2026-11-24.md](changelog-fase-5a-lacunas-2026-2026-11-24.md) e [roteiro-central-evolucao-nota-10-por-sessao.md](roteiro-central-evolucao-nota-10-por-sessao.md).

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
- ✅ **Pendências herdadas da Fase 3 resolvidas em 24/11/2026:** Caps. 6 e 15 ampliados para `18` partes cada; reconferência web fechada com `178` chaves atuais (incluindo `7` da vLLM via GitHub oficial), `0` vencidas/divergentes e `18` chaves (`13` URLs) registradas como consulta manual por bloqueio externo, com comando `fontes.py importar` pronto caso venham a ser salvas localmente.
4. **Fase 4 — Revisão (`L1`), piloto/validação em telas (`L2`) e arte (`L8`):**
   - ✅ Revisão técnica `L1` por agentes de IA (subagentes somente leitura sobre Caps. 6, 9, 15, Sumário, Glossário e Referências, com correções aplicadas e validadas).
   - ✅ Validação em telas (`L2`, sem papel A4): encerrada em 24/11/2026 pelo operador após aprovação no Galaxy S24 (Acer Nitro 5 ignorado e demais itens dispensados pelo operador; zero ajustes necessários no HTML/CSS). Registro em [roteiro-piloto-e-validacao-em-telas-2026-11-24.md](roteiro-piloto-e-validacao-em-telas-2026-11-24.md).
   - ✅ **Fase 5A — Lacunas conceituais 2026 no HTML (concluída em 24/11/2026):** `8` partes curtas (`2.6f`, `4.5e`, `7.4e`, `12.5d`, `12.6e`, `14.3d`, `14.6c`, `17.4d`), `27` fontes conferidas (`34/34` trechos OK), `#sumario`, `#glossario` (`528`) e `#referencias` atualizados.
   - ⏳ **Fases 5B–5E em cadência de 1 fase por sessão** ([roteiro-central-evolucao-nota-10-por-sessao.md](roteiro-central-evolucao-nota-10-por-sessao.md) e [plano-evolucao-mercado-e-nota-10-2026-11-24.md](plano-evolucao-mercado-e-nota-10-2026-11-24.md)): `5B` endurecimento de questões/estudos de caso; `5C` diagramas SVG + redução para `18` aquarelas + PDF provisório; `5D` Camada 3 prática em `laboratorios-mercado/` com `pgvector` e `.github/workflows/`; `5E` revisão/piloto humano (`L1`/`L2`), geração das `18` aquarelas (`L8`) e PDF definitivo.

Assinatura: agy - ap (Gemini 4 Hydrogen High), atualizado em 23/11/2026; atualizado em 24/11/2026 por claude - pessoal (fechamento da Fase 3) e agy - ap (ampliação dos Caps. 6 e 15, reconferência de fontes, L1, L2, consolidação editorial Blocos 1–4, ajustes pontuais de laboratórios/docs e plano nota 10).
