# Roteiro Central de Evolução para Nota 10 (por sessão)

Data: 24/11/2026. Autoria: agy - ap.
Referência técnica completa: [`plano-evolucao-mercado-e-nota-10-2026-11-24.md`](plano-evolucao-mercado-e-nota-10-2026-11-24.md).

## 1. Objetivo, baseline e decisões aprovadas

- **Meta:** elevar `guia-engenharia-llms.html` e a trilha prática de **7,2 / 10** (`8,5` conceitual; `5,0` hands-on de mercado; `5,5` visual e validação externa) rumo a **10 / 10** sem quebrar o formato TDAH (§8 de [`requisitos-de-formato-html-do-material.md`](requisitos-de-formato-html-do-material.md)), as validações determinísticas nem a trilha offline rápida em `laboratorios/`.
- **Baseline inicial (24/11/2026, antes da Fase 5A):** `377` seções, `445` questões, `26` blocos Python executáveis, `502` termos no Glossário, `73` molduras `data-imagem=`, `0` `<svg>`, `guia-engenharia-llms.pdf` com `657` páginas A4, `laboratorios/` com `84` testes offline.
- **Decisões do operador aprovadas em 24/11/2026:**
  1. **Fase 5C (visual):** reduzir aquarelas artísticas de `73` para `18` (uma abertura por capítulo) combinadas com `18–24` diagramas técnicos `<svg>` inline acessíveis.
  2. **Fase 5D (diretório da Camada 3):** `laboratorios-mercado/` na raiz do projeto, preservando `laboratorios/` intacta.
  3. **Fase 5D (banco vetorial padrão do projeto 02):** `pgvector` sobre PostgreSQL.
  4. **Fase 5D (CI):** incluir workflow `.github/workflows/` para testes offline automáticos.
  5. **Cadência entre sessões:** executar **1 fase aprofundada por sessão**, com fechamento completo (validações + docs/changelog + commit/push em `main`) e **1 `/handoff` limpo ao final de cada fase finalizada**. Exceção prevista: se a Fase 5D crescer além do conforto da janela de contexto, pode ser dividida em `5D-1` (infraestrutura + projetos 01–03) e `5D-2` (projetos 04–06 + CI).
  6. **Política de PDF:** não regerar `guia-engenharia-llms.pdf` nas Fases 5A e 5B; regerar o PDF provisório ao final da **Fase 5C** (texto + questões + SVGs estabilizados) e o PDF definitivo ao final da **Fase 5E**.

### Restrições fixas (válidas em todas as sessões)
- Não alterar a imagem base do sistema (Bazzite): usar `venv` dedicado e contêineres compatíveis com `Podman` e `Docker`.
- Chave Gemini (quando usada em código de mercado) apenas no cabeçalho `x-goog-api-key`, nunca na URL.
- Manter neutralidade multi-fornecedor (zero menções a sistemas ou empresas reais internas do autor; exemplos empresariais na fictícia Aurora Educação marcados como *proposta didática*).
- Não usar `ferramentas/llm-local.py` no fluxo do projeto (ver §9 de [`protocolo-de-economia-de-tokens-entre-sessoes.md`](protocolo-de-economia-de-tokens-entre-sessoes.md)).
- Em cada abertura de sessão, revalidar `git status -sb`, branch `main` (`alexpedrozawd`), hashes e ferramentas reais antes de editar.

---

## 2. Mapa das sessões

| Sessão | Fase | Foco principal | PDF regerado? | Handoff gerado | Estado |
|---|---|---|---|---|---|
| **Sessão 1** | **Fase 5A** | Fechamento das 5 lacunas conceituais 2026 no HTML (8 partes curtas + fontes conferidas) | Não | Fase 5A → Fase 5B | Concluída (24/11/2026) |
| **Sessão 2** | **Fase 5B** | Endurecimento das `108` questões de fechamento e rubricas quantitativas dos `18` estudos de caso | Não | Fase 5B → Fase 5C | Concluída (24/11/2026) |
| **Sessão 3** | **Fase 5C** | `18–24` diagramas `<svg>` inline acessíveis, redução `73 → 18` molduras de aquarela e atualização do validador | Sim (provisório) | Fase 5C → Fase 5D | Concluída (24/11/2026) |
| **Sessão 4** | **Fase 5D** | Camada 3 prática em `laboratorios-mercado/` (6 projetos OCI + `pgvector` + smoke-tests + execução real) e `.github/workflows/` | Não | Fase 5D → Fase 5E | Concluída (24/11/2026) |
| **Sessão 5** | **Fase 5E** | Validação externa humana (`L1`/`L2`), geração das `18` aquarelas (`L8`), PDF definitivo e encerramento | Sim (definitivo) | Encerramento final | Concluída em 24/11/2026 (`L8` + PDF); `L1`/`L2` bloqueados |

---

## 3. Detalhamento por sessão

### Sessão 1 — Fase 5A: Lacunas conceituais de 2026 no HTML
- **Escopo:**
  - Criar `pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md` com fontes oficiais e artigos primários (2024–2026) conferidos via `ferramentas/fontes.py`.
  - Inserir **8 partes curtas cirúrgicas** (400–520 palavras, formato TDAH §8) em `guia-engenharia-llms.html`:
    1. `2.6f`: Backend assíncrono (`FastAPI`, `asyncio`, pool `httpx.AsyncClient`) e contêineres OCI (`Podman`/`Docker`).
    2. `4.5e`: Decodificação restrita (*constrained decoding*, `XGrammar`, `Outlines`, `GBNF`).
    3. `7.4e`: Multimodalidade prática com VLMs em PDFs visuais (`ColPali` vs. parser de layout), custo por resolução e ponte com áudio/ferramentas.
    4. `12.5d`: Isolamento real em produção (`Docker`/`Podman` rootless vs. `gVisor` vs. `Firecracker`).
    5. `12.6e`: Marcos regulatórios e auditoria (`EU AI Act`, `ISO/IEC 42001`, `SOC 2` articulados à `LGPD`).
    6. `14.3d`: Atenção moderna e extensão de contexto (`FlashAttention`, `MLA` e `RoPE` + `YaRN`).
    7. `14.6c`: Motores e formatos modernos de serviço (`SGLang` + `RadixAttention`, desagregação *prefill*/*decode* e `FP4`).
    8. `17.4d`: Observabilidade operacional (`Prometheus`, `Grafana`) e `CI/CD` de avaliações.
  - Atualizar rótulos `parte X de N`, mover `Fontes da unidade`, atualizar `#sumario`, `#glossario` (sem `<dfn>` duplicados), `#referencias` e renumerar páginas lógicas (`377 → 385`).
- **Aceite:** `fontes.py conferir/vigencia` (`0` falhas), `guia.py fechar` (`0` falhas), `auditar-guia-navegador.mjs` (`0` estouros em `320 px`, `453/453` questões, `0` violações `axe-core`), equilíbrio `A/B/C/D` com `LONGEST_TRUE = 0`, `testar-fontes.py`, `testar-livros.py` e `executar_labs.py` OK.
- **Resultado em 24/11/2026:** ✅ **Concluída** (`385` partes, `453` questões `113/113/114/113`, `528` termos no Glossário, `guia-engenharia-llms.html` sha `0f1dfaea62cd3fa2`, `34/34` trechos conferidos, `0` violações no navegador; ver [`changelog-fase-5a-lacunas-2026-2026-11-24.md`](changelog-fase-5a-lacunas-2026-2026-11-24.md)).
- **Fechamento da sessão:** changelog + docs + commit/push em `main` + `/handoff` para Sessão 2.

### Sessão 2 — Fase 5B: Endurecimento pedagógico (questões e estudos de caso)
- **Escopo:**
  - Revisar os distratores das `108` questões de fechamento (`6 × 18` capítulos), priorizando médias e difíceis, trocando alternativas caricatas por trade-offs reais de arquitetura e produção.
  - Endurecer critérios quantitativos nas rubricas dos `18` estudos de caso (contas de VRAM/`KV cache`, intervalos de Wilson, latência `p95`, orçamento mensal e critérios de bloqueio).
- **Invariantes:** distribuição equilibrada `A/B/C/D`, `LONGEST_TRUE = 0`, `BAD_EXP = 0` (`Correta.` / `Incorreta.` em toda alternativa).
- **Aceite:** `validar-guia.py` (`16 OK, 0 FALHA`), `guia.py fechar` (`0` falhas), `auditar-guia-navegador.mjs` (`453+` questões clicáveis sem falhas) e auditoria Python de equilíbrio/comprimento sem violações.
- **Resultado em 24/11/2026:** ✅ **Concluída** (`91/108` questões de fechamento endurecidas mantendo `113/113/114/113`, `LONGEST_TRUE = 0`, `BAD_EXP = 0`, `SHORTEST_TRUE = 0`; `18/18` rubricas com critérios quantitativos e bloqueios; `guia-engenharia-llms.html` sha `81ff0e778f2ba073`; `guia.py fechar` e `auditar-guia-navegador.mjs` com `0` falhas; PDF `53129052eebf7800` mantido até a Fase 5C; ver [`changelog-fase-5b-questoes-e-rubricas-2026-11-24.md`](changelog-fase-5b-questoes-e-rubricas-2026-11-24.md)).
- **Fechamento da sessão:** changelog + docs + commit/push em `main` + `/handoff` para Sessão 3.

### Sessão 3 — Fase 5C: Diagramas técnicos SVG e redução de aquarelas (`73 → 18`)
- **Escopo:**
  - Inserir **18 a 24 diagramas técnicos em `<svg>` inline** (sem fontes ou scripts externos, com `role="img"`, `<title>`, `<desc>`, alto contraste, responsivos em `320 px` e legíveis em `@media print` A4) nas unidades estruturais centrais: pilha Transformer/`Q·K`, arquitetura em 5 camadas, fluxo RAG híbrido + RRF, GraphRAG vs. grafo de estado, orçamento/compactação de contexto, fluxo MCP + sandbox, defesa em profundidade, memória GPU/`KV cache`/`GQA`/`PagedAttention`/desagregação, memória LoRA/`QLoRA`, gateway de roteamento, pipeline LLMOps/canário/drift e fluxo de cache por prefixo.
  - Aplicar a decisão aprovada: reduzir molduras `data-imagem=` de `73` para `18` (uma abertura por capítulo).
  - Atualizar `requisitos-de-formato-html-do-material.md` (§8 e §9) e `ferramentas/validar-guia.py` (validação de `<svg>` acessíveis) + `ferramentas/testar-ferramentas.py`.
  - Regerar o PDF provisório via `guia.py pdf --substituir --motivo fase-5c-diagramas-svg` e inspecionar amostras renderizadas em HTML e PDF.
- **Aceite:** `guia.py fechar` (`0` falhas), `testar-ferramentas.py` OK, `auditar-guia-navegador.mjs` (`0` estouros `320 px` e `0` violações `axe-core`) e inspeção visual aprovada.
- **Resultado em 24/11/2026:** ✅ **Concluída** (`22` diagramas `<svg>` inline acessíveis com `0` sobreposições/overflows em `320 px` e `1280 px`; molduras reduzidas de `73` para `18` aberturas `cap-1`..`cap-18`; `requisitos-de-formato-html-do-material.md` §8–§9, `validar-guia.py` `18 OK`, `guia.py` e `testar-ferramentas.py` `19 tests OK` sem `--rapido`; `guia-engenharia-llms.html` sha `45e11a0cd880451a`; PDF provisório regerado com `664` páginas A4 sha `482a150cb91f3efc`, anterior em `arquivo/antes-fase-5c-diagramas-svg-2026-11-24/`; `auditar-guia-navegador.mjs` com `46 passes`, `0` violações `axe-core` e `453/453` questões OK; ver [`changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md`](changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md)).
- **Fechamento da sessão:** changelog + docs + commit/push em `main` + `/handoff` para Sessão 4.

### Sessão 4 — Fase 5D: Camada 3 prática de mercado (`laboratorios-mercado/`) e CI
- **Escopo:**
  - Criar `laboratorios-mercado/` na raiz (sem alterar `laboratorios/`), com `pyproject.toml`, instruções de `venv` dedicado (sem mexer na imagem base do Bazzite) e `compose.yaml` compatível com **Podman e Docker**, reutilizando `laboratorios/comum/cliente_llm.py` (`x-goog-api-key` em header):
    1. `01_serving_local`: subir `ollama` / `llama-server` / `vLLM` + benchmark assíncrono (`asyncio`/`httpx`) medindo `TTFT`, `TPOT`, `p95`, `goodput` e memória real.
    2. `02_rag_producao`: `pgvector` sobre PostgreSQL em container + embeddings reais + *reranker* + ingestão de PDFs com tabelas + avaliação de recuperação/fidelidade.
    3. `03_mcp_sandbox`: servidor e cliente MCP reais (`stdio` e Streamable HTTP), validação `Pydantic`, execução isolada em container restrito e aprovação humana.
    4. `04_qlora_peft`: ajuste fino `QLoRA`/`LoRA` reproduzível com `peft`/`trl` (`1B–3B`) + avaliação antes/depois por fatia + manifesto.
    5. `05_api_llmops`: `FastAPI` + `asyncio` + SSE real com cancelamento, retry/backoff/disjuntor + `OpenTelemetry` (traces reais) + avaliação contínua.
    6. `06_integrador_producao`: assistente ponta a ponta integrando API `FastAPI`, RAG `pgvector`, MCP isolado, roteamento local/fronteira, guardrails e relatório de custo/latência.
  - Criar workflow em `.github/workflows/` para executar automaticamente as suítes offline (`executar_labs.py`, smoke-tests de `laboratorios-mercado/`, `validar-guia.py` e testes de ferramentas).
- **Aceite:** smoke-tests offline determinísticos passando sem `ResourceWarning`, `podman compose config` válido, execução real de ao menos 1 projeto ponta a ponta contra Ollama/serviço local registrada em log/changelog e CI offline validado.
- **Resultado em 24/11/2026:** ✅ **Concluída** (`laboratorios-mercado/` com 6 projetos, `pyproject.toml`, `compose.yaml` [9 serviços, 7 perfis; `podman compose config -q` OK] e `Containerfile`; `56` smoke-tests offline OK sem `ResourceWarning`; execução real dos 6 projetos registrada em `laboratorios-mercado/execucoes/` [llama.cpp em container + `pgvector`; QLoRA `treinar` não executado por falta de GPU CUDA]; `.github/workflows/testes-offline.yml`; `laboratorios/` intacta [84 testes OK]; HTML e PDF inalterados; ver [`changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md`](changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md)).
- **Fechamento da sessão:** changelog + docs + commit/push em `main` + `/handoff` para Sessão 5.

### Sessão 5 — Fase 5E: Validação externa (`L1`/`L2`), arte final (`L8`) e PDF definitivo
- **Escopo:**
  1. **Revisão técnica humana (`L1`):** submeter capítulos críticos (`5`, `12`, `14`, `15`, `17`) e 2 projetos de `laboratorios-mercado/` a engenheiros humanos de produção, registrando objeções e resoluções.
  2. **Piloto de aprendizagem (`L2`):** aplicar leitura cronometrada + questões + estudo de caso + 1 projeto prático a 2–3 estudantes do público-alvo e ajustar pontos de trava.
  3. **Arte final e PDF definitivo (`L8`):** gerar as `18` aquarelas aprovadas (uma por abertura de capítulo, 1056×704, fantasia medieval sem texto), inserir no HTML e regerar o PDF final via `python3 -I ferramentas/guia.py pdf --substituir --motivo fechamento-nota-10`.
- **Dependência externa:** itens 1 e 2 dependem de participantes humanos externos; caso ocorram em paralelo antes da geração final, registrar evidências nominais no changelog antes do fechamento.
- **Fechamento final:** suítes completas (`executar_labs.py`, `laboratorios-mercado/`, `guia.py fechar`, `testar-ferramentas.py`, `testar-fontes.py`, `testar-livros.py`, `auditar-guia-navegador.mjs`), consolidação documental e commit/push final em `main`.
- **Resultado em 24/11/2026:** `L8` ✅ (`18` aquarelas geradas localmente com Qwen-Image 2.1 no `stable-diffusion.cpp`, inspecionadas e embutidas em JPEG; HTML sha `bb004776a6cdc9cb`); PDF definitivo ✅ (`664` páginas A4, sha `81d2fffd7394a880`); `L1` e `L2` **bloqueados** (operador sem revisores nem estudantes; nada simulado); todas as suítes aprovadas. Ver [`changelog-fase-5e-aquarelas-pdf-definitivo-e-encerramento-2026-11-24.md`](changelog-fase-5e-aquarelas-pdf-definitivo-e-encerramento-2026-11-24.md).

---

## 4. Protocolo obrigatório de troca de sessão (1 handoff por fase)

1. Nenhuma fase se fecha sem passar por todas as suas validações determinísticas.
2. Só após aprovar todas as validações da fase atual: atualizar este roteiro, o `plano-evolucao-mercado-e-nota-10-2026-11-24.md`, `CLAUDE.md`, `README.md`, `roadmap.md` e gerar o `changelog-fase-<X>-*.md`.
3. Realizar commit único da fase concluída e `git push origin main` na conta `alexpedrozawd`.
4. Gerar **exatamente um `/handoff` ao fim da fase finalizada**, declarando expressamente no bloco copiável que **cada sessão executa uma fase completa e gera um novo handoff apenas na conclusão da fase**, para permitir limpar a sessão com segurança antes de iniciar a fase seguinte.

Assinatura: agy - ap. Atualizado em 24/11/2026 por claude - pessoal (Fases 5D e 5E concluídas).
