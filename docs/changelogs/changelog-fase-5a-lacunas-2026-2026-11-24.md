# Changelog: Fase 5A — Fechamento das lacunas conceituais de 2026 (24/11/2026)

Registra a criação do roteiro central por sessão ([roteiro-central-evolucao-nota-10-por-sessao.md](../historico/roteiro-central-evolucao-nota-10-por-sessao.md)), do pacote de fontes verificadas ([pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md](../fontes/pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md)) e a inserção cirúrgica de **8 partes curtas** em [guia-engenharia-llms.html](../../guia-engenharia-llms.html) cobrindo as 5 lacunas de mercado 2025–2026. Conforme política definida para o ciclo, o PDF provisório ([guia-engenharia-llms.pdf](../../guia-engenharia-llms.pdf), `657` páginas) permaneceu inalterado nesta fase e será regerado ao final da **Fase 5C**.

## Autoria

- **24/11/2026, `agy - ap`:** pesquisa e conferência das 27 fontes primárias, redação das 8 partes no formato TDAH, atualização de `#sumario`, `#glossario` (`502 → 528` termos) e `#referencias`, renumeração (`377 → 385`), validações completas e fechamento Git da Fase 5A.

## O que mudou

- **Roteiro central e registro das decisões do operador:**
  - Criado [roteiro-central-evolucao-nota-10-por-sessao.md](../historico/roteiro-central-evolucao-nota-10-por-sessao.md) organizando a cadência de 1 fase aprofundada + 1 handoff limpo por sessão (`5A`–`5E`).
  - Registradas em [plano-evolucao-mercado-e-nota-10-2026-11-24.md](../historico/plano-evolucao-mercado-e-nota-10-2026-11-24.md) as 4 decisões aprovadas pelo operador: `18` aquarelas na abertura dos capítulos combinadas com diagramas SVG (`5C`); trilha prática em `laboratorios-mercado/` na raiz (`5D`); `pgvector` sobre PostgreSQL como banco vetorial padrão do projeto 02 (`5D`); e inclusão de `.github/workflows/` para CI offline (`5D`).
- **Pacote de fontes da Fase 5A ([pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md](../fontes/pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md)):**
  - `27` chaves únicas baixadas em `cache-fontes/` (`223` chaves únicas no manifesto global, `205` atuais em cache, `0` vencidas, `0` hash divergente) e `34` trechos literais (`F5A-01`–`F5A-34`) aprovados em `conferir-trechos.py`.
- **8 novas partes curtas em [guia-engenharia-llms.html](../../guia-engenharia-llms.html) (formato TDAH §8, 1 questão cada):**
  - `2.6f` — Backend assíncrono (`FastAPI`, `asyncio`, pool `httpx.AsyncClient`) e empacotamento em contêineres OCI (`Podman`/`Docker`). Gabarito `A`.
  - `4.5e` — Decodificação restrita (`XGrammar`, `Outlines`, `GBNF`) e interação com blocos de raciocínio/delimitadores. Gabarito `B`.
  - `7.4e` — Multimodalidade prática com VLMs e recuperação visual de documentos (`ColPali`, blocos de `28×28` pixels e controle de detalhe). Gabarito `C`.
  - `12.5d` — Isolamento real em produção (`Docker`/`Podman` rootless vs. `gVisor` Sentry vs. `Firecracker` microVM). Gabarito `D`.
  - `12.6e` — Marcos regulatórios e auditoria (`EU AI Act`, `ISO/IEC 42001` e `SOC 2` articulados à `LGPD` e `NIST AI 600-1`). Gabarito `A`.
  - `14.3d` — Atenção moderna e extensão de contexto (`FlashAttention`, `MLA` e `RoPE` + `YaRN`). Gabarito `B`.
  - `14.6c` — Serviço moderno em escala (`SGLang` + `RadixAttention`, desagregação de *prefill*/*decode* e `FP4`/`MXFP4`). Gabarito `C`.
  - `17.4d` — Métricas operacionais (`Prometheus`/`Grafana`) e portões automatizados de avaliação em `CI/CD` (`GitHub Actions`). Gabarito `D`.
- **Atualizações coordenadas no HTML e nos documentos:**
  - Atualizados rótulos `parte X de N`, migrados e preservados integralmente os blocos `Fontes da unidade` das 8 unidades, encadeados os `page-nav` e renumeradas as páginas (`377 → 385`).
  - Atualizados `#sumario`, `#glossario` (`502 → 528` termos, `476 → 502` `<dfn>` únicos, zero repetições), `#referencias`, [CLAUDE.md](../../CLAUDE.md), [README.md](../../README.md) e [roadmap.md](../../roadmap.md).

## Hashes (SHA-256, 16 primeiros dígitos)

- `guia-engenharia-llms.html`: `0f1dfaea62cd3fa2` (`385` partes, `453` questões, `157` tabelas, `528` termos no Glossário, `502` `<dfn>` únicos, `304` links web únicos, `22.881` linhas)
- `guia-engenharia-llms.pdf`: `53129052eebf7800` (`657` páginas A4 — mantido da rodada anterior; regeração provisória prevista ao fim da Fase 5C)
- `pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md`: `43d0f15f821b9fd6`
- `roteiro-central-evolucao-nota-10-por-sessao.md`: `50abb98ecfd6c8d5`

## Validações executadas

- `python3 -I ferramentas/fontes.py conferir --pacote pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md`: `34 aprovados, 0 reprovados`.
- `python3 -I ferramentas/fontes.py vigencia --pacote pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md --estrito`: `27 chaves únicas | 27 atuais | 0 fora do cache | 0 vencidas | 0 hash divergente` (global: `223` chaves únicas, `205` atuais, `18` bloqueadas anteriores, `0` divergentes).
- `python3 -I ferramentas/guia.py fechar --guia guia-engenharia-llms.html`: `0` falhas (`16 OK, 0 FALHA` em `validar-guia.py`; `26 OK, 0 FALHA` em `executar-trechos-de-codigo.py`; `157/157` tabelas em `.rolagem`; `0` `<dfn>` ou IDs duplicados; sequência `1..385`).
- Auditoria Python de questões (`453` questões): `A=113, B=113, C=114, D=113`, `LONGEST_TRUE = 0`, `BAD_EXP = 0`.
- `node ferramentas/auditar-guia-navegador.mjs` (Chromium `1254`, Playwright e `axe-core`): `docClient=320, docScroll=320, bodyScroll=320`, `385` seções, `totalEstouros: 0`, `453/453` questões com `falhas: []`, `axe-core` com `45 passes` e `0 violations` em `1280×800` e `320×640`, `errosDePagina: []`.
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `Ran 14 tests -> OK`.
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `Ran 84 tests -> OK`.
- `python3 -I ferramentas/testar-livros.py`: `Ran 2 tests -> OK`.
- `python3 -I ferramentas/testar-ferramentas.py --rapido`: `Ran 15 tests -> OK (skipped=2)` (execução sem `--rapido` teve `14 OK` e `1` falha esperada em `test_pdf_tem_as_mesmas_paginas_do_pdf_versionado` — `671 != 657` — pois o PDF provisório só será regerado na Fase 5C).

Assinatura: agy - ap (24/11/2026).
