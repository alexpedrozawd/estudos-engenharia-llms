# Changelog: Consolidação final da reescrita editorial (Blocos 1 a 4) — 24/11/2026

Registra o fechamento do Bloco 4 da reescrita editorial de [guia-engenharia-llms.html](../../guia-engenharia-llms.html), integrando Chip Huyen (*AI Engineering*, dez/2024 © 2025, e *Designing Machine Learning Systems*, mai/2022) às fontes públicas vigentes de novembro de 2026 em todos os `18` capítulos, com revisão de `#glossario`, `#referencias`, regeneração de [guia-engenharia-llms.pdf](../../guia-engenharia-llms.pdf) e validações completas.

## Autoria

- **24/11/2026, `agy - ap`:** execução do Bloco 4 (aplicação das 5 decisões aprovadas pelo operador e das 16 consolidações técnicas dos arquivos locais `rascunho-local/conflitos-bloco-{1,2,3}-parte-{1,2,3}.md`, atualização de `#glossario`, `#referencias`, [README.md](../../README.md), [roadmap.md](../../roadmap.md), [CLAUDE.md](../../CLAUDE.md), regeneração do PDF e revisão adversarial final).

## O que mudou

- **Decisões consolidadas (`C1-01`–`C1-08`, `C2-01`–`C2-07`, `C3-01`–`C3-06`):**
  - `C1-04`: mantida a linha histórica/migração de `thinking.budget_tokens` (descontinuado em Claude 4.7+) na unidade `4.5d`.
  - `C1-03`: mantido o aviso de `Chat Completions` vs. `Responses API` na `4.5d` e explicitada a *Responses API* em `#referencias` vinculada às páginas já conferidas em cache (`Conversation state` com `previous_response_id` / `/v1/responses` e `Streaming API responses`).
  - `C1-01`, `C2-05`, `C3-04`: unificados no `#glossario` os verbetes `Esforço (4.5, 9.6, 16.3)` (cobertura multi-provedor 2026), `Esforço por mensagem (16.6)` (corrigido para explicitar invalidação condicional de cache ao alterar esforço global) e `Orçamento de raciocínio (9.2)`, mantendo o quadro comparativo sem duplicação apenas em `4.5a`/`4.5c`.
  - `C3-03`: mantido o destaque de `GRPO` na `15.5a` demarcado como evolução pós-livro e explicitado `GRPO` em `DeepSeek-R1` e nas fontes do capítulo 15 em `#referencias`.
  - `C1-05`: adicionada separação editorial explícita em `#referencias` entre marcos fundacionais (Chip Huyen 2022/2024–2025 e artigos seminais) e fichas/especificações operacionais de 2026.
- **Consistência cruzada no corpo de [guia-engenharia-llms.html](../../guia-engenharia-llms.html):**
  - `2.3d`: incluída remissão cruzada para o Capítulo 14 (TTFT, TPOT e serviço de inferência local).
  - `8.3c` e `11.1c`: incluídas remissões para o Capítulo 17 (observabilidade e *LLMOps* em produção), alinhadas a `11.5c`.
  - `14.2c`: datada explicitamente no corpo (`em 17/11/2026`) a divergência entre as páginas do Ollama sobre o contexto padrão (`4096` vs. VRAM).
  - Conferida a permanência de `5.4a–b` (`BLEU`/`ROUGE` vs. *embeddings*/juiz), `5.5b` (aviso do desligamento da plataforma legada OpenAI Evals em novembro de 2026), `9.6b`/`18.5a–c` (tarifas de cache `0,1×`/`0,05×`/`0,025×`, `TTL` `5 min`/`1 h` e descontos de `17/11/2026`) e `10.3c` (*sandbox*/Cap. 12).
- **Atualização de `#glossario` e `#referencias`:**
  - `#glossario` atualizado para `502` termos únicos em ordem alfabética (refinamentos em `Esforço`, `Esforço por mensagem`, `Orçamento de raciocínio`, `Raciocínio passo a passo`, `Span`, `Traço / rastro (trace)` e inclusão de `Repositório de modelos (model store) (17.5)` para os oito artefatos de *DMLS* cap. 10).
  - `#referencias` atualizado com cobertura bibliográfica de Chip Huyen nos capítulos 1–5 e revisão das entradas dos capítulos 7–18 (substituindo menções restritas a partes isoladas da Fase 3 pela integração ao longo de cada capítulo).
- **PDF e documentação:**
  - [guia-engenharia-llms.pdf](../../guia-engenharia-llms.pdf) regerado com `657` páginas A4 (cópia anterior de `654` páginas preservada em `arquivo/antes-consolidacao-reescrita-huyen-bloco-4-2026-11-24/`, fora do Git).
  - Atualizados [README.md](../../README.md), [roadmap.md](../../roadmap.md) e [CLAUDE.md](../../CLAUDE.md).

## Contagens e hashes finais

- **HTML ([guia-engenharia-llms.html](../../guia-engenharia-llms.html)):** `377` seções/páginas lógicas (`221.986` palavras nas partes, `22.392` linhas, `2.701.612` bytes), `445` questões (`a:111, b:111, c:112, d:111`, `LONGEST_TRUE=0`, `BAD_EXP=0`), `149` tabelas em `.rolagem`, `26` blocos Python executáveis (+ `21` ilustrativos), `476` `<dfn>` únicos, `502` termos no Glossário, `276` links web únicos, SHA-256 `eff7ad47d12bf57a` (16 primeiros dígitos).
- **PDF ([guia-engenharia-llms.pdf](../../guia-engenharia-llms.pdf)):** `657` páginas A4, `16.120.199` bytes, SHA-256 `53129052eebf7800` (16 primeiros dígitos).

## Validações (após a última edição do HTML e regeneração do PDF)

- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`numeração`, `validar-guia.py` `16 OK, 0 FALHA`, `executar-trechos-de-codigo.py` `26 OK, 0 FALHA, 21 ilustrativos`, `ids` únicos, `476` `<dfn>` únicos, `502` termos sem repetição, sumário completo, `149/149` tabelas em `.rolagem`, `445/445` questões/gabaritos).
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `Ran 82 tests in 0.122s -> OK`.
- `python3 -I ferramentas/testar-ferramentas.py`: `Ran 15 tests in 33.875s -> OK` (incluindo verificação completa de PDF com `657` páginas).
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `Ran 14 tests in 0.536s -> OK`.
- `python3 -I ferramentas/testar-livros.py`: `Ran 2 tests in 0.091s -> OK`.
- Auditoria global via `HTMLParser`: `DFN_TOTAL=476`, `DFN_UNIQUE=476`, `Q_TOTAL=445`, `LONGEST_TRUE=0`, `BAD_EXP=0`, `GLOSS_DTS=502`, `DUP_DTS=0`, `BROKEN_INTERNAL_HREFS=0`, zero nomes internos proibidos.
- `node ferramentas/auditar-guia-navegador.mjs` (Chromium `1254`, `playwright-core` e `axe-core` em `/tmp/auditoria-navegador`): `docClient=320`, `docScroll=320`, `bodyScroll=320`, `377` seções, `totalEstouros=0`, `445/445` questões com `falhas: []`, `axe-core` com `45 passes` e `0 violations` em `1280×800` e `320×640`, `errosDePagina: []`, `falhas: 0`.

Assinatura: agy - ap (24/11/2026).
