# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira, com programação em duas camadas: blocos curtos executáveis no HTML e laboratórios em `laboratorios/`.

## Estado atual (24/11/2026)

- **Fase 3 concluída; `L1`, `L2` e consolidação editorial (Blocos 1–4) concluídas:** `18` capítulos em três partes, integrando integralmente os dois livros de Chip Huyen (*AI Engineering* e *Designing Machine Learning Systems*) às fontes públicas de nov/2026 (`178` atuais em cache após migração da vLLM para Markdown oficial no GitHub; `18` chaves bloqueadas registradas como consulta manual, com suporte a importação em `ferramentas/fontes.py importar`), com programação em duas camadas. São `377` páginas lógicas (`337` partes de conteúdo), `445` questões (`111/111/112/111`), `149` tabelas com `.rolagem`, `502` termos no Glossário, `26` blocos Python executáveis e um estudo de caso com rubrica por capítulo. Caps. 6 e 15 ampliados para `18` partes cada, revisados por agentes de IA (`L1`), etapa `L2` encerrada em 24/11/2026 após aprovação no Galaxy S24 ([roteiro-piloto-e-validacao-em-telas-2026-11-24.md](roteiro-piloto-e-validacao-em-telas-2026-11-24.md)) e consolidação editorial final (Blocos 1–4) fechada em 24/11/2026 com PDF provisório de `657` páginas A4. Ver [changelog-consolidacao-reescrita-huyen-2026-11-24.md](changelog-consolidacao-reescrita-huyen-2026-11-24.md).
  - **Parte I — Fundamentos, arquitetura, especificação e avaliação:** Caps. 1–5.
  - **Parte II — Dados, conhecimento, contexto e agentes:** Cap. 6 (Engenharia de Dados e Datasets), 7 (Busca, Indexação e RAG), 8 (Grafos), 9 (Contexto, Memória e Feedback), 10 (Ferramentas e Protocolos), 11 (Harnesses, Workflows e Agentes).
  - **Parte III — Segurança, adaptação, operação e economia:** Cap. 12 (Segurança e Guardrails), 13 (Atos Autodestrutivos), 14 (Inferência Local), 15 (Fine-tuning, Quantização e Destilação), 16 (Seleção e Roteamento), 17 (LLMOps), 18 (Eficiência e Economia).
- **Laboratórios:** `laboratorios/` traz um laboratório por capítulo e o projeto integrador, em Python padrão, com `84` testes offline (`python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`) e adaptadores HTTP reais opcionais em `laboratorios/comum/cliente_llm.py`.
- **Próximo (evolução rumo à nota 10 e fechamento da Fase 4):** plano em [plano-evolucao-mercado-e-nota-10-2026-11-24.md](plano-evolucao-mercado-e-nota-10-2026-11-24.md) (lacunas 2026, endurecimento de questões, diagramas SVG técnicos, Camada 3 prática de mercado, revisão/piloto humano `L1`/`L2`) + etapa visual final (`L8`) e PDF definitivo quando autorizado pelo operador ([roadmap.md](roadmap.md)).

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões com retorno imediato em `aria-live`, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 gerada via Chromium headless (`657` páginas).
- `planejamento-reestruturado-2026-11-23.md` — plano curricular vigente (`18` capítulos + programação).
- `laboratorios/` — `18` laboratórios e projeto integrador, com testes offline.
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
