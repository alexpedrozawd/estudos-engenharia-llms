# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, com programação em duas camadas (blocos curtos executáveis no HTML e laboratórios em `laboratorios/`) e uma trilha prática de mercado com serviços reais em `laboratorios-mercado/`.

## Estado atual (24/11/2026)

- **Fase 3, consolidação editorial (Blocos 1–4) e Fases 5A–5D concluídas:** `18` capítulos em três partes, integrando integralmente os dois livros de Chip Huyen (*AI Engineering* e *Designing Machine Learning Systems*) às fontes públicas de nov/2026 (`205` atuais em cache; `18` chaves anteriores registradas como consulta manual), com programação em duas camadas e cobertura das lacunas 2026 (decodificação restrita com `XGrammar`/`Outlines`/`GBNF`, `SGLang`/`RadixAttention`, desagregação *prefill*/*decode*, `FlashAttention`, `MLA`, `YaRN`, `FP4`, `gVisor`/`Firecracker`, `EU AI Act`/`ISO 42001`/`SOC 2`, VLMs/`ColPali`, `FastAPI`/`asyncio`, contêineres OCI e `Prometheus`/`Grafana`/`CI/CD`). São `385` páginas lógicas (`345` partes de conteúdo), `453` questões (`113/113/114/113`, com `91/108` questões de fechamento endurecidas na `5B`), `157` tabelas com `.rolagem`, `528` termos no Glossário, `26` blocos Python executáveis, `22` diagramas técnicos `<svg>` inline acessíveis, `18` molduras `data-imagem=` de abertura por capítulo e um estudo de caso com rubrica quantitativa por capítulo (`18/18` atualizadas na `5B`). Etapa `L2` encerrada em 24/11/2026 após aprovação no Galaxy S24 ([roteiro-piloto-e-validacao-em-telas-2026-11-24.md](roteiro-piloto-e-validacao-em-telas-2026-11-24.md)); PDF provisório regerado na Fase 5C com `664` páginas A4 (PDF definitivo previsto na Fase 5E). Ver [changelog-fase-5a-lacunas-2026-2026-11-24.md](changelog-fase-5a-lacunas-2026-2026-11-24.md), [changelog-fase-5b-questoes-e-rubricas-2026-11-24.md](changelog-fase-5b-questoes-e-rubricas-2026-11-24.md) e [changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md](changelog-fase-5c-diagramas-svg-e-molduras-2026-11-24.md).
  - **Parte I — Fundamentos, arquitetura, especificação e avaliação:** Caps. 1–5.
  - **Parte II — Dados, conhecimento, contexto e agentes:** Cap. 6 (Engenharia de Dados e Datasets), 7 (Busca, Indexação e RAG), 8 (Grafos), 9 (Contexto, Memória e Feedback), 10 (Ferramentas e Protocolos), 11 (Harnesses, Workflows e Agentes).
  - **Parte III — Segurança, adaptação, operação e economia:** Cap. 12 (Segurança e Guardrails), 13 (Atos Autodestrutivos), 14 (Inferência Local), 15 (Fine-tuning, Quantização e Destilação), 16 (Seleção e Roteamento), 17 (LLMOps), 18 (Eficiência e Economia).
- **Laboratórios:** `laboratorios/` traz um laboratório por capítulo e o projeto integrador, em Python padrão, com `84` testes offline (`python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`) e adaptadores HTTP reais opcionais em `laboratorios/comum/cliente_llm.py`.
- **Laboratórios de mercado (Fase 5D):** [`laboratorios-mercado/`](laboratorios-mercado/README.md) traz 6 projetos com serviços reais (serving local, RAG com `pgvector`, MCP com sandbox, QLoRA, API LLMOps e integrador), `compose.yaml` para Podman e Docker, `56` smoke-tests offline e execuções reais registradas; CI offline em [`.github/workflows/testes-offline.yml`](.github/workflows/testes-offline.yml). Ver [changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md](changelog-fase-5d-laboratorios-mercado-e-ci-2026-11-24.md).
- **Próximo (evolução rumo à nota 10 e fechamento da Fase 4):** plano aprovado em [plano-evolucao-mercado-e-nota-10-2026-11-24.md](plano-evolucao-mercado-e-nota-10-2026-11-24.md) e cadência por sessão em [roteiro-central-evolucao-nota-10-por-sessao.md](roteiro-central-evolucao-nota-10-por-sessao.md) (Fases `5A`–`5D` concluídas; pendente `5E`: revisão/piloto humano `L1`/`L2`, geração das `18` aquarelas e PDF definitivo) ([roadmap.md](roadmap.md)).

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões com retorno imediato em `aria-live`, diagramas técnicos SVG inline, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 provisória gerada via Chromium headless (`664` páginas).
- `planejamento-reestruturado-2026-11-23.md` — plano curricular vigente (`18` capítulos + programação).
- `laboratorios/` — `18` laboratórios e projeto integrador, com testes offline.
- `laboratorios-mercado/` — Camada 3: 6 projetos com serviços reais, smoke-tests offline e registros em `execucoes/`.
- `.github/workflows/` — CI offline (labs, guia, ferramentas e smoke-tests da Camada 3).
- `planejamento-completo-estudos-engenharia-llms.md` — plano curricular anterior (`16` módulos).
- `plano-de-lacunas-para-nota-10-2026-11-19.md` — plano de lacunas de qualidade (`L1`–`L8`).
- `pacote-de-fontes-*.md` — trechos literais conferidos de fontes públicas primárias.
- `ferramentas/` — `guia.py`, `fontes.py`, `livros.py`, `validar-guia.py`, `renumerar-paginas.py`, `executar-trechos-de-codigo.py`, `conferir-trechos.py`, `extrair-texto-web.py`, `auditar-guia-navegador.mjs` e testes (`testar-ferramentas.py`, `testar-fontes.py`, `testar-livros.py`, `testar-llm-local.py`).
- `CLAUDE.md` — estado atual, instruções de retomada e protocolo de economia de tokens (`protocolo-de-economia-de-tokens-entre-sessoes.md`).

## Validação rápida

```bash
python3 -I ferramentas/guia.py fechar
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py
```
