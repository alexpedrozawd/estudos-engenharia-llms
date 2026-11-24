# Changelog: Ampliação dos Caps. 6 e 15, reconferência de fontes web, L1 (agentes) e roteiro L2 em telas — 24/11/2026

Fecha as pendências herdadas da Fase 3 e avança os entregáveis preparatórios da Fase 4 em [roadmap.md](roadmap.md) e [planejamento-reestruturado-2026-11-23.md](planejamento-reestruturado-2026-11-23.md), seguindo as decisões do operador desta sessão.

## Autoria

- **24/11/2026, `agy - ap` (Gemini 4 Hydrogen High):** reconferência completa das fontes web (`fontes.py`), ampliação dos capítulos 6 e 15 para `18` partes cada, revisão técnica `L1` por 3 subagentes de IA (Gemini, autorizado pelo operador diante da indisponibilidade de revisores humanos), preparação do roteiro de piloto e validação em telas `L2` (sem papel A4), regeração do PDF provisório e validações completas.

## O que mudou

- **Reconferência das fontes web (`pacote-de-fontes-*.md`):**
  - Download e extração de `171` das `196` chaves únicas de manifesto em cache local (`25` permanecem bloqueadas por `HTTP 403`/`400` ou redirecionamento `http://`, sem contorno de bloqueio).
  - Atualização de `106` hashes em `12` arquivos `pacote-de-fontes-*.md` e atualização dos trechos `CM-32` (`anthropic-cc-memory`) e `CM-08` no pacote do Cap. 9 e em `9.1b` / `9.4b` / `#referencias` do HTML.
  - `fontes.py vigencia`: `196` chaves únicas | `171` atuais | `25` fora do cache | `0` vencidas | `0` hash divergente.
- **Ampliação dos capítulos 6 e 15 (`guia-engenharia-llms.html`, `6351f700e6b8644d` → `bb1ff5a2a4db25f3`):**
  - **Capítulo 6 (Engenharia de Dados e Datasets para IA):** `12` → `18` partes (`6.1a`–`6.6c`), somando `6.1c`, `6.2c`, `6.3c` (`cod-6-3c-py`), `6.4c` (`cod-6-4c-py` + moldura `6-4c`), `6.5c` e `6.6b` (moldura `6-6b`), com antiga `6.6b` renumerada para `6.6c`.
  - **Capítulo 15 (Fine-tuning, Quantização e Destilação):** `7` → `18` partes (`15.1a`–`15.6c`) e `5` → `6` questões de fechamento (`c15q1`–`c15q6`), incluindo os snippets executáveis `cod-15-3c-py`, `cod-15-4a-py` e `cod-15-4c-py`, 3 molduras (`15-1a`, `15-4a`, `15-5b`), atualização do `#sumario`, `#referencias` (`openai-rft` corrigido para `https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning` e inclusão de *DMLS* cap. 11) e `+22` entradas no `#glossario` (`479` → `501` termos).
  - **Estado atual do guia:** `377` páginas lógicas (`337` partes de conteúdo), `219.231` palavras em partes, `445` questões (`111/111/112/111`, nenhuma com a correta estritamente mais longa), `149` tabelas com `.rolagem`, `501` termos no Glossário, `476` `<dfn>`, `26` blocos Python executáveis (`21` ilustrativos), `276` links web únicos e `73` molduras `data-imagem=`.
- **Revisão técnica `L1` (via 3 subagentes de pesquisa somente leitura + aplicação direta):**
  - Revisados os novos conteúdos dos Caps. 6 e 15, as atualizações do Cap. 9, `#sumario`, `#glossario` e `#referencias`. Corrigidos links de navegação `page-nav` em `6.2a`–`6.5a` e `15.2a`, remissão `5.6` → `5.3c` em `6.4a`/`6.4c`, explicações breves na 1ª ocorrência de termos técnicos, alinhamento do texto de `alignment tax` (`15.1b`), ajuste `quatro` → `três` hiperparâmetros em `15.6a`, limpeza de referências órfãs (`Google Cloud` em `15.0` e `Ollama FAQ` em `15.6c`), atualização de `LLMOps (15.0)` → `(17.0)` e `5` inversões alfabéticas no Glossário.
- **Roteiro de piloto e validação em telas (`L2`, [roteiro-piloto-e-validacao-em-telas-2026-11-24.md](roteiro-piloto-e-validacao-em-telas-2026-11-24.md)):**
  - Documento pronto para execução manual com 3–5 leitores, smartphone (Galaxy S24), tablet, notebook (Acer Nitro 5), televisor 55" 4K e leitor de tela. Validação em papel A4 explicitamente excluída conforme decisão do operador.
- **PDF provisório (`guia-engenharia-llms.pdf`):**
  - Regerado com `654` páginas A4 (`15.745.034` bytes, sha256 `76ba915a7e6723aa`). Cópia anterior (`628` páginas) preservada em `arquivo/antes-fase-4-ampliacao-e-l1-2026-11-24/`.

## Validações após a última edição (24/11/2026)

- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`validar-guia.py` com `16 OK, 0 FALHA`; `executar-trechos-de-codigo.py` com `26 OK, 0 FALHA` e `21` ilustrativos; numeração `1..377`, IDs, `<dfn>`, glossário, sumário, `.rolagem` e `445` gabaritos OK).
- Equilíbrio das `445` questões conferido via `html.parser`: `111/111/112/111` (`a/b/c/d`) e `0` questões com alternativa correta estritamente mais longa.
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `82` testes OK.
- `testar-ferramentas.py`: `15` OK; `testar-fontes.py`: `12` OK; `testar-livros.py`: `2` OK; `fontes.py vigencia`: `196` chaves | `171` atuais | `25` fora do cache | `0` vencidas | `0` hash divergente.
- `auditar-guia-navegador.mjs` (Chromium `1254`, Playwright e `axe-core`): `377` seções sem estouro de reflow a `320 px` (`docClient/docScroll/bodyScroll = 320`); `445/445` questões com `0` falhas; `axe-core` com `45` passes e `0` violações em `1280×800` e `320×640`.

## Pendente para encerramento da Fase 4

- Execução manual do piloto e testes em telas + leitor de tela (`L2`, [roteiro-piloto-e-validacao-em-telas-2026-11-24.md](roteiro-piloto-e-validacao-em-telas-2026-11-24.md)).
- Geração das `73` imagens em aquarela (`L8`, passo final) e emissão do PDF definitivo após as imagens.

Assinatura: agy - ap (24/11/2026).
