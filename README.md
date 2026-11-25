# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, com programação em duas camadas (blocos curtos executáveis no HTML e laboratórios em `laboratorios/`) e uma trilha prática de mercado com serviços reais em `laboratorios-mercado/`.

## Estado atual (25/11/2026)

- **Guia completo e congelado (Fases 3, Blocos 1–4 e Fases 5A–5E):** `18` capítulos em três partes, integrando integralmente os dois livros de Chip Huyen (*AI Engineering* e *Designing Machine Learning Systems*) às fontes públicas de nov/2026 (`205` atuais em cache; `18` chaves anteriores registradas como consulta manual), com `385` páginas lógicas (`345` partes de conteúdo), `453` questões (`113/113/114/113`, com `91/108` questões de fechamento endurecidas na `5B`), `157` tabelas com `.rolagem`, `528` termos no Glossário, `26` blocos Python executáveis, `22` diagramas técnicos `<svg>` inline acessíveis, `18` aquarelas de abertura embutidas no HTML (`data-imagem="cap-1"`..`"cap-18"`) e um estudo de caso com rubrica quantitativa por capítulo (`18/18` atualizadas na `5B`). Etapa `L2` em telas encerrada em 24/11/2026 após aprovação no Galaxy S24 ([roteiro-piloto-e-validacao-em-telas-2026-11-24.md](docs/historico/roteiro-piloto-e-validacao-em-telas-2026-11-24.md)); PDF definitivo com `664` páginas A4. Ver [changelog-fase-5a-lacunas-2026-2026-11-24.md](docs/changelogs/changelog-fase-5a-lacunas-2026-2026-11-24.md), [changelog-fase-5b-questoes-e-rubricas-2026-11-24.md](docs/changelogs/changelog-fase-5b-questoes-e-rubricas-2026-11-24.md), [changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md](docs/changelogs/changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md) e [changelog-fase-5e-aquarelas-pdf-definitivo-e-encerramento-2026-11-24.md](docs/changelogs/changelog-fase-5e-aquarelas-pdf-definitivo-e-encerramento-2026-11-24.md).
  - **Parte I — Fundamentos, arquitetura, especificação e avaliação:** Caps. 1–5.
  - **Parte II — Dados, conhecimento, contexto e agentes:** Cap. 6 (Engenharia de Dados e Datasets), 7 (Busca, Indexação e RAG), 8 (Grafos), 9 (Contexto, Memória e Feedback), 10 (Ferramentas e Protocolos), 11 (Harnesses, Workflows e Agentes).
  - **Parte III — Segurança, adaptação, operação e economia:** Cap. 12 (Segurança e Guardrails), 13 (Atos Autodestrutivos), 14 (Inferência Local), 15 (Fine-tuning, Quantização e Destilação), 16 (Seleção e Roteamento), 17 (LLMOps), 18 (Eficiência e Economia).
- **Laboratórios offline ([`laboratorios/`](laboratorios/README.md)):** um laboratório por capítulo mais o projeto integrador, em Python padrão, com `84` testes determinísticos (`python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`) e adaptadores HTTP opcionais em [`laboratorios/comum/cliente_llm.py`](laboratorios/comum/cliente_llm.py).
- **Laboratórios de mercado (Camada 3 — Fases 5D, 6 e ROCm/anti-BFLA):** [`laboratorios-mercado/`](laboratorios-mercado/README.md) traz **7 projetos** com serviços reais (`01_serving_local`, `02_rag_producao` com `12` PDFs / `41` trechos e ACL no `pgvector`, `03_mcp_sandbox`, `04_qlora_peft` compatível com CUDA e AMD ROCm/`gfx1201`, `05_api_llmops` com auth/rate limit, Prometheus `/metrics` e OTLP → Jaeger, `06_integrador_producao` com laço agêntico via `tool_calls`, `json_schema` estrito, proteção anti-BFLA `403` e degradação segura sem `500`, e `07_evals_e_multimodal` com LLM-as-a-judge calibrado e renderização PDF → PNG via `pdftoppm`), `compose.yaml` para Podman/Docker, `83` smoke-tests offline e execuções reais registradas; CI offline em [`.github/workflows/testes-offline.yml`](.github/workflows/testes-offline.yml) incluindo build e smoke do [`Containerfile`](laboratorios-mercado/Containerfile). Ver [changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md](docs/changelogs/changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md), [changelog-fase-6-mercado-producao-2026-11-25.md](docs/changelogs/changelog-fase-6-mercado-producao-2026-11-25.md), [changelog-versao-final-e-revisao-adversarial-2026-11-25.md](docs/changelogs/changelog-versao-final-e-revisao-adversarial-2026-11-25.md) e [changelog-rocm-qlora-e-validacao-bfla-2026-11-25.md](docs/changelogs/changelog-rocm-qlora-e-validacao-bfla-2026-11-25.md).
- **Versão Final 1.0 (encerrada em 25/11/2026; nota realista `9,1 / 10` e técnica `9,3 / 10`):** por decisão do operador, `L1` (revisão técnica humana) e `L2` (piloto com estudantes) foram encerrados e substituídos pela revisão adversarial automatizada (sem simulação humana), fechando o material para uso pessoal de estudo ([roadmap.md](roadmap.md) e [changelog-rocm-qlora-e-validacao-bfla-2026-11-25.md](docs/changelogs/changelog-rocm-qlora-e-validacao-bfla-2026-11-25.md)).

## Roteiro de estudo pessoal

1. **Teoria e fundamentos (`guia-engenharia-llms.html` ou `guia-engenharia-llms.pdf`):** estude na sequência Partes I → II → III, respondendo às questões com retorno imediato no navegador e revisando as rubricas quantitativas de estudo de caso ao fim de cada capítulo.
2. **Prática determinística sem infraestrutura ([`laboratorios/`](laboratorios/README.md)):** após cada capítulo do guia, rode e inspecione o laboratório correspondente (`lab_01`..`lab_18`) e feche com o `projeto_integrador/` para consolidar contratos, métricas e *guardrails* em Python puro.
3. **Prática de produção com serviços reais ([`laboratorios-mercado/`](laboratorios-mercado/README.md)):** avance pelos 7 projetos com `.venv-mercado` e `compose.yaml` (`83` smoke-tests offline):
   - `01_serving_local` (Cap. 14): benchmark assíncrono TTFT/TPOT/goodput no `llama.cpp:server`.
   - `02_rag_producao` (Caps. 5, 7): ingestão de PDF com tabelas, `pgvector` HNSW + `tsvector`, ACL por perfil, fusão RRF e comparação vetorial/lexical/híbrida/*reranker*.
   - `03_mcp_sandbox` (Caps. 10, 12, 13): servidor/cliente MCP 2.x com aprovação humana (*elicitation*) e container sem rede.
   - `04_qlora_peft` (Caps. 6, 15): receita QLoRA reproduzível, avaliação por fatia e portão antes/depois.
   - `05_api_llmops` (Caps. 2, 17): FastAPI, SSE com cancelamento, retry/disjuntor, autenticação, rate limit (`429`), `/metrics` Prometheus e traces OTLP no Jaeger.
   - `06_integrador_producao` (Caps. 12, 16, 18): assistente com PII/injeção, roteamento, *tool calling* nativo MCP, *structured outputs* (`json_schema`), ACL e relatório de custo/cache.
   - `07_evals_e_multimodal` (Caps. 4, 5): avaliação A vs B com juiz calibrado (inversão de ordem, *kappa* de Cohen, bootstrap pareado) e extração multimodal PDF → PNG (`pdftoppm`) → Pydantic.

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões em `aria-live`, diagramas SVG inline, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 definitiva gerada via Chromium headless (`664` páginas).
- `laboratorios/` — `18` laboratórios e projeto integrador, com `84` testes offline.
- `laboratorios-mercado/` — Camada 3: `7` projetos com serviços reais, `74` smoke-tests offline e registros em `execucoes/`.
- `.github/workflows/` — CI offline (labs, guia, ferramentas, smoke-tests, `compose.yaml` e build/smoke do `Containerfile`).
- `docs/` — históricos organizados em [`docs/changelogs/`](docs/changelogs/), [`docs/fontes/`](docs/fontes/) e [`docs/historico/`](docs/historico/) (inclui [`planejamento-reestruturado-2026-11-23.md`](docs/historico/planejamento-reestruturado-2026-11-23.md)).
- `ferramentas/` — `guia.py`, `fontes.py`, `livros.py`, `validar-guia.py`, `renumerar-paginas.py`, `executar-trechos-de-codigo.py`, `conferir-trechos.py`, `extrair-texto-web.py`, `auditar-guia-navegador.mjs` e testes (`testar-ferramentas.py`, `testar-fontes.py`, `testar-livros.py`, `testar-llm-local.py`).
- [`CLAUDE.md`](CLAUDE.md) — estado atual, instruções de retomada e protocolo de economia de tokens ([`protocolo-de-economia-de-tokens-entre-sessoes.md`](protocolo-de-economia-de-tokens-entre-sessoes.md)).

## Validação rápida

```bash
python3 -I ferramentas/guia.py fechar
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py
.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py
```
