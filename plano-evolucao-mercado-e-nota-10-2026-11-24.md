# Plano de evolução rumo à nota 10 — Mercado de trabalho e revisão visual (24/11/2026)

Estado: **aprovado pelo operador em 24/11/2026 (`Fases 5A–5E` concluídas, com `L1`/`L2` bloqueados por falta de participantes humanos; cadência por sessão conforme [`roteiro-central-evolucao-nota-10-por-sessao.md`](roteiro-central-evolucao-nota-10-por-sessao.md)).**

## 1. Contexto, baseline e objetivo

- **Baseline pós-auditoria de 24/11/2026:** nota realista **7,2 / 10** (`8,5 / 10` em arquitetura conceitual; `5,0 / 10` em prática hands-on de mercado; `5,5 / 10` em acabamento visual e validação externa).
- **Estado após a Fase 5C (24/11/2026):** `guia-engenharia-llms.html` (`385` seções, `453` questões `113/113/114/113`, `26` blocos executáveis, `528` termos no Glossário, `18` molduras `data-imagem="cap-1".."cap-18"`, `22` diagramas `<svg>` inline acessíveis, sha `45e11a0cd880451a`), `guia-engenharia-llms.pdf` (`664` páginas A4, sha `482a150cb91f3efc`) e `laboratorios/` (`18` labs offline + projeto integrador, `84` testes).
- **Decisões aprovadas pelo operador em 24/11/2026:** `5C` = reduzir aquarelas de `73` para `18` (uma abertura por capítulo) + diagramas técnicos SVG; `5D` = diretório `laboratorios-mercado/` na raiz, `pgvector` como banco vetorial padrão do projeto 02 e workflow `.github/workflows/` para CI offline; cadência = 1 fase aprofundada por sessão com 1 `/handoff` limpo ao fim de cada fase finalizada.
- **Ambiente local verificado:** `podman` (`/usr/bin/podman`) e `ollama` (`/home/linuxbrew/.linuxbrew/bin/ollama`) disponíveis; `docker` e `nvidia-smi` ausentes no `PATH` atual.
- **Objetivo:** levar o material o mais próximo possível de **10 / 10** para formar arquitetos e engenheiros de LLMs de fronteira ou locais conforme a realidade do mercado, sem quebrar o formato TDAH, as validações determinísticas nem a trilha offline rápida existente.
- **Fora do escopo deste plano:** alterar `guia-engenharia-llms.html` ou regerar `guia-engenharia-llms.pdf` durante o planejamento; gerar a arte final antes de estabilizar textos, diagramas e decisões pendentes.

---

## 2. Fases verificáveis (5A–5E + Encerramento)

### ✅ Fase 5A — Fechamento das 5 lacunas conceituais de 2026 no HTML (concluída em 24/11/2026)
- **O que fazer:** adicionar partes curtas pontuais (sem inflar capítulos) cobrindo os temas de mercado 2025–2026 hoje ausentes ou sub-representados:
  1. **Decodificação restrita (*constrained decoding*):** gramáticas livres de contexto, `XGrammar`, `Outlines` e garantia estrutural de JSON/ferramentas em modelos locais (Cap. 4 ou 14).
  2. **Serviço de inferência moderno:** `SGLang` / `RadixAttention`, desagregação de *prefill* e *decode*, `FP4`, extensão de contexto (`RoPE` / `YaRN`), `MLA` e papel de `FlashAttention` (Cap. 14).
  3. **Sandboxing real e governança corporativa:** isolamento em produção (`Docker`/`Podman`, `gVisor`, `Firecracker`) e marcos regulatórios/auditoria (`EU AI Act`, `ISO 42001`, `SOC 2`) (Cap. 12).
  4. **Multimodalidade prática:** VLMs aplicados a PDFs complexos, imagens e áudio em tempo real (Caps. 7 e 10).
  5. **Empacotamento e operação de sistemas:** containers (`Docker`/`Podman`), backend assíncrono (`asyncio`, `FastAPI`, pools HTTP), `Prometheus`/`Grafana` e `CI/CD` de avaliações (Caps. 2 e 17).
- **Fontes e controle:** registrar trechos literais em pacote de fontes e validar via `ferramentas/fontes.py` e `ferramentas/conferir-trechos.py`; atualizar `#sumario`, `#glossario` e `#referencias`.
- **Resultado verificável:** `python3 -I ferramentas/guia.py fechar` com `0` falhas e `node ferramentas/auditar-guia-navegador.mjs` com `0` estouros em `320 px` e `0` violações `axe-core`.

### ✅ Fase 5B — Endurecimento pedagógico (questões e estudos de caso; concluída em 24/11/2026)
- **O que fazer:**
  - Revisar os distratores das `108` questões de fechamento (`6 × 18` capítulos), priorizando médias e difíceis, trocando alternativas caricatas por trade-offs plausíveis de arquitetura.
  - Reforçar critérios quantitativos nas rubricas dos `18` estudos de caso (contas de VRAM/`KV cache`, limites de Wilson, latência `p95`, orçamento mensal).
- **Invariantes obrigatórios:** manter distribuição equilibrada `A/B/C/D`, `LONGEST_TRUE=0` (correta nunca estritamente a maior), `BAD_EXP=0` e explicação coerente em cada alternativa.
- **Resultado verificável:** `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html` (`16 OK, 0 FALHA`), `auditar-guia-navegador.mjs` (`445+` questões clicáveis sem falhas) e auditoria de comprimento/distribuição com `0` violações. ✅ **Concluída:** `91/108` questões endurecidas, `18/18` rubricas quantitativas, `453/453` questões aprovadas no navegador (`changelog-fase-5b-questoes-e-rubricas-2026-11-24.md`).

### ✅ Fase 5C — Revisão dos diagramas técnicos SVG e estratégia visual (`L8` redesenhado; concluída em 24/11/2026)
- **O que fazer:**
  - Inserir **18 a 24 diagramas técnicos em `<svg>` inline** (sem fontes/scripts externos, com `role="img"`, `<title>`, `<desc>`, alto contraste e adaptação responsiva em `320 px` e `@media print` A4) nas unidades estruturais centrais: pilha Transformer/`Q·K`, arquitetura em 5 camadas, fluxo RAG híbrido + RRF, GraphRAG vs. grafo de estado, orçamento/compactação de contexto, fluxo MCP + sandbox, defesa em profundidade, memória GPU/`KV cache`/`GQA`/`PagedAttention`/desagregação, memória LoRA/`QLoRA`, gateway de roteamento, pipeline LLMOps/canário/drift e fluxo de cache por prefixo.
  - Atualizar `requisitos-de-formato-html-do-material.md` (§8 e §9) e `ferramentas/validar-guia.py` se necessário para validar `<svg>` acessíveis.
- **Decisão aprovada (24/11/2026):** reduzir as ilustrações artísticas em aquarela de `73` para `18` (uma abertura por capítulo), combinadas com `22` diagramas técnicos SVG nas partes.
- **Resultado verificável:** ✅ **Concluída:** `22` diagramas `<svg>` inline acessíveis, `18` molduras `cap-1`..`cap-18`, `validar-guia.py` (`18 OK`), `testar-ferramentas.py` (`19 tests OK` sem `--rapido`), `guia.py fechar` (`0` falhas), `auditar-guia-navegador.mjs` (`0` estouros `320 px` + `axe-core` `0` violações), inspeção visual HTML/PDF aprovada e PDF provisório regerado com `664` páginas A4 (`changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md`).

### Fase 5D — Camada 3 prática de mercado (6 projetos reais opt-in)
- **O que fazer:** criar trilha prática separada da pasta `laboratorios/` (preservando os `18` labs offline rápidos intactos), com `pyproject.toml` / `venv` próprio e `compose.yaml` compatível com **Podman e Docker**, integrando `laboratorios/comum/cliente_llm.py` e runtimes/serviços reais:
  1. `01_serving_local`: subir `ollama` / `llama-server` / `vLLM`, benchmark assíncrono (`asyncio`/`httpx`) medindo `TTFT`, `TPOT`, `p95`, `goodput` e memória real.
  2. `02_rag_producao`: banco vetorial real em container (`pgvector` ou `Qdrant`) + embeddings reais + *reranker* + ingestão de PDFs com tabelas + avaliação de recuperação/fidelidade.
  3. `03_mcp_sandbox`: servidor e cliente MCP reais (`stdio` e Streamable HTTP), validação `Pydantic`, execução de ferramenta isolada em container restrito e aprovação humana.
  4. `04_qlora_peft`: ajuste fino `QLoRA`/`LoRA` reproduzível com `peft`/`trl` em modelo pequeno (`1B–3B`) + avaliação antes/depois por fatia + manifesto.
  5. `05_api_llmops`: `FastAPI` + `asyncio` + streaming SSE real com cancelamento, retry/backoff/disjuntor + `OpenTelemetry` exportando traces reais (compatível com Langfuse/Phoenix/console) + avaliação contínua.
  6. `06_integrador_producao`: assistente fim a fim ligando API `FastAPI`, RAG real, MCP real, roteamento local/fronteira, guardrails e relatório de custo/latência.
- **Riscos e cuidados:**
  - Não alterar imagem base do sistema (Bazzite): usar `venv` dedicado e containers `Podman`/`Docker`.
  - Cada projeto deve trazer smoke-tests determinísticos com mocks/fixtures (para rodar em máquina sem GPU ou sem API paga) além do roteiro de execução real.
- **Decisões materiais pendentes do operador (antes de iniciar 5D):**
  1. Diretório da Camada 3: `laboratorios-mercado/` na raiz (recomendado) ou `laboratorios/mercado/`.
  2. Banco vetorial padrão do projeto 02: `pgvector` (PostgreSQL, recomendado pela adoção corporativa) ou `Qdrant`.
  3. Incluir workflow `.github/workflows/` para CI automático dos testes offline.
- **Resultado verificável:** suíte própria de smoke-tests offline passando sem `ResourceWarning`, `compose config` válido em `podman`/`docker` e execução real de ao menos um projeto ponta a ponta contra Ollama/API local registrada em log/changelog.
- **Resultado:** ✅ **Concluída em 24/11/2026:** `56` smoke-tests OK, `podman compose config -q` OK (Docker no CI), 6 projetos executados contra llama.cpp em container e `pgvector` (QLoRA `treinar` pendente de GPU CUDA), workflow `testes-offline.yml` ([`changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md`](changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md)).

### Fase 5E — Validação externa (`L1` humano + `L2` piloto real) e fechamento definitivo (`L8` + PDF final)
- **O que fazer:**
  1. **Revisão técnica humana (`L1`):** submeter ao menos os capítulos críticos (5, 12, 14, 15 e 17) e 2 projetos da Camada 3 a engenheiros humanos de produção, registrando objeções e resoluções.
  2. **Piloto de aprendizagem (`L2`):** aplicar leitura cronometrada + questões + estudo de caso + 1 projeto prático a 2–3 estudantes do público-alvo, ajustando pontos de trava.
  3. **Arte final e PDF definitivo (`L8`):** gerar as aquarelas aprovadas (`18` ou `73`), inserir no HTML e regerar o PDF via `python3 -I ferramentas/guia.py pdf --substituir --motivo fechamento-nota-10`.
- **Dependência externa:** etapas 1 e 2 dependem de participantes humanos externos (sem isso, a nota permanece limitada pela ausência de validação fora da bolha de IA).
- **Resultado:** ✅ **`L8` e PDF definitivo concluídos em 24/11/2026** (`18` aquarelas locais com Qwen-Image 2.1, PDF `664` páginas sha `81d2fffd7394a880`); `L1` e `L2` **bloqueados** (operador sem revisores nem estudantes). Ver [`changelog-fase-5e-aquarelas-pdf-definitivo-e-encerramento-2026-11-24.md`](changelog-fase-5e-aquarelas-pdf-definitivo-e-encerramento-2026-11-24.md).

### Fase Final — Encerramento da entrega
- Em cada fase executada (ou ao concluir o bloco), consolidar `README.md`, `roadmap.md`, `CLAUDE.md` e `changelog-*.md`, executar todas as suítes (`executar_labs.py`, `guia.py fechar`, `testar-ferramentas.py`, `testar-fontes.py`, `testar-livros.py`, `auditar-guia-navegador.mjs` e suíte da Camada 3), conferir estado Git (`alexpedrozawd`, branch `main`) e fazer commit/push apenas no fechamento da entrega (nunca por subetapa).

---

## 3. Modelo/effort recomendado para execução

- **Fases 5A, 5B e 5C (conteúdo, questões e SVGs no HTML):** **HIGH** (capacidade de fronteira; Gemini 4 Neon/Argon ou Claude Sonnet/Opus 5.5 High).
- **Fase 5D (Camada 3 prática em Python/containers/testes):** **HIGH** para desenho dos contratos e revisão; implementação modular pode seguir com fronteira suficiente vigente em High.
- **Fechamento documental e Git:** preservar configuração suficiente vigente da demanda em High.

Assinatura: agy - ap (24/11/2026). Atualizado em 24/11/2026 por claude - pessoal (resultados das Fases 5D e 5E).